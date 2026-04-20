"""Product catalog API endpoints."""

from flask import Blueprint, jsonify, request

from models import Product, db
from utils.pagination import paginate_query

products_bp = Blueprint("products", __name__, url_prefix="/api")


@products_bp.route("/products", methods=["GET"])
def list_products():
    """Return active products.

    Query params
    ------------
    page : int, optional
    per_page : int, optional
    include_stock : bool, optional
        If "true", include computed stock level (slower query).
    """
    query = Product.query.filter_by(active=True).order_by(Product.name)
    page_meta, products = paginate_query(query, request.args)

    include_stock = request.args.get("include_stock", "").lower() == "true"

    return jsonify({
        "data": [p.to_dict(include_stock=include_stock) for p in products],
        "pagination": page_meta,
    })


@products_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    """Return a single product with stock info."""
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"data": product.to_dict(include_stock=True)})


@products_bp.route("/products", methods=["POST"])
def create_product():
    """Add a new product to the catalog.

    Expects JSON::

        {
            "sku": "KB-MK01",
            "name": "Mechanical Keyboard",
            "description": "Cherry MX Blue switches",
            "price": 89.99
        }
    """
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400

    required = ("sku", "name", "price")
    missing = [f for f in required if f not in body]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    product = Product(
        sku=body["sku"],
        name=body["name"],
        description=body.get("description"),
        price=body["price"],
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"data": product.to_dict()}), 201
