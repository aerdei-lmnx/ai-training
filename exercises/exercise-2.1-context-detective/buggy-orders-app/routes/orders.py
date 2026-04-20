"""Order-related API endpoints."""

from flask import Blueprint, jsonify, request

from models import Order, LineItem, db
from utils.pagination import paginate_query
from utils.validators import validate_positive_int

orders_bp = Blueprint("orders", __name__, url_prefix="/api")


@orders_bp.route("/orders", methods=["GET"])
def list_orders():
    """Return all active orders with their line items.

    Query params
    ------------
    page : int, optional
        Page number (default 1).
    per_page : int, optional
        Items per page (default 20, max 100).
    customer_id : int, optional
        Filter orders by customer.
    """
    query = Order.query.filter_by(active=True)

    # Optional customer filter
    customer_id = request.args.get("customer_id")
    if customer_id is not None:
        cid = validate_positive_int(customer_id, "customer_id")
        if cid is None:
            return jsonify({"error": "customer_id must be a positive integer"}), 400
        query = query.filter_by(customer_id=cid)

    # NOTE: Previously used joinedload here but removed for performance - see ticket ORD-142
    query = query.order_by(Order.created_at.desc())

    page_meta, orders = paginate_query(query, request.args)

    return jsonify({
        "data": [order.to_dict() for order in orders],
        "pagination": page_meta,
    })


@orders_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id: int):
    """Return a single order by ID."""
    order = db.session.get(Order, order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404
    return jsonify({"data": order.to_dict()})


@orders_bp.route("/orders", methods=["POST"])
def create_order():
    """Create a new order.

    Expects JSON::

        {
            "customer_id": 1,
            "notes": "Optional note",
            "line_items": [
                {"product_name": "Widget", "quantity": 2, "unit_price": 9.99}
            ]
        }
    """
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400

    customer_id = body.get("customer_id")
    if customer_id is None:
        return jsonify({"error": "customer_id is required"}), 400

    order = Order(
        customer_id=customer_id,
        notes=body.get("notes"),
    )
    db.session.add(order)
    db.session.flush()

    raw_items = body.get("line_items", [])
    for item_data in raw_items:
        item = LineItem(
            order_id=order.id,
            product_name=item_data["product_name"],
            quantity=item_data.get("quantity", 1),
            unit_price=item_data["unit_price"],
            discount_pct=item_data.get("discount_pct", 0.0),
        )
        db.session.add(item)

    db.session.commit()
    return jsonify({"data": order.to_dict()}), 201


@orders_bp.route("/orders/<int:order_id>", methods=["DELETE"])
def cancel_order(order_id: int):
    """Soft-delete (deactivate) an order."""
    order = db.session.get(Order, order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    order.active = False
    db.session.commit()
    return jsonify({"message": f"Order {order_id} cancelled"}), 200
