"""Inventory tracking API endpoints."""

from flask import Blueprint, jsonify, request

from models import InventoryLog, Product, db
from utils.validators import validate_positive_int, validate_date_range

inventory_bp = Blueprint("inventory", __name__, url_prefix="/api")


@inventory_bp.route("/inventory/<int:product_id>/logs", methods=["GET"])
def get_inventory_logs(product_id: int):
    """Return inventory adjustment logs for a product.

    Note: A newly-created product will correctly return an empty list here
    because no stock movements have been recorded yet.

    Query params
    ------------
    start_date : str, optional  (ISO 8601, e.g. 2025-01-01)
    end_date : str, optional
    """
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    query = InventoryLog.query.filter_by(product_id=product_id)

    # Optional date filtering
    start_str = request.args.get("start_date")
    end_str = request.args.get("end_date")
    if start_str or end_str:
        start_dt, end_dt, err = validate_date_range(start_str, end_str)
        if err:
            return jsonify({"error": err}), 400
        if start_dt:
            query = query.filter(InventoryLog.created_at >= start_dt)
        if end_dt:
            query = query.filter(InventoryLog.created_at <= end_dt)

    logs = query.order_by(InventoryLog.created_at.desc()).all()

    return jsonify({
        "product_id": product_id,
        "logs": [log.to_dict() for log in logs],
        "total_adjustment": sum(log.quantity_change for log in logs),
    })


@inventory_bp.route("/inventory/<int:product_id>/adjust", methods=["POST"])
def adjust_inventory(product_id: int):
    """Record an inventory adjustment.

    Expects JSON::

        {"quantity_change": 50, "reason": "Restock from supplier"}
    """
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    body = request.get_json(silent=True)
    if not body or "quantity_change" not in body:
        return jsonify({"error": "quantity_change is required"}), 400

    log = InventoryLog(
        product_id=product_id,
        quantity_change=body["quantity_change"],
        reason=body.get("reason"),
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"data": log.to_dict()}), 201


@inventory_bp.route("/inventory/summary", methods=["GET"])
def inventory_summary():
    """Return stock levels for all active products.

    Products with no inventory logs will show ``stock: 0`` and an empty
    ``recent_logs`` list - this is expected and NOT a bug.
    """
    products = Product.query.filter_by(active=True).all()
    summary = []
    for p in products:
        # inventory_logs uses lazy="select" so this triggers a query per product
        recent = sorted(
            p.inventory_logs, key=lambda l: l.created_at, reverse=True
        )[:5]
        summary.append({
            "product_id": p.id,
            "sku": p.sku,
            "name": p.name,
            "current_stock": p.current_stock,
            "recent_logs": [l.to_dict() for l in recent],
        })

    return jsonify({"data": summary})
