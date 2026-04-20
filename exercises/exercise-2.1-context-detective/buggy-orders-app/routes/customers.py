"""Customer-related API endpoints."""

from flask import Blueprint, jsonify, request

from models import Customer, db
from utils.pagination import paginate_query

customers_bp = Blueprint("customers", __name__, url_prefix="/api")


@customers_bp.route("/customers", methods=["GET"])
def list_customers():
    """Return all customers.

    Query params
    ------------
    page : int, optional
    per_page : int, optional
    """
    query = Customer.query.order_by(Customer.name)
    page_meta, customers = paginate_query(query, request.args)
    return jsonify({
        "data": [c.to_dict() for c in customers],
        "pagination": page_meta,
    })


@customers_bp.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id: int):
    """Return a single customer, optionally with their orders."""
    customer = db.session.get(Customer, customer_id)
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    include_orders = request.args.get("include_orders", "").lower() == "true"
    return jsonify({"data": customer.to_dict(include_orders=include_orders)})


@customers_bp.route("/customers", methods=["POST"])
def create_customer():
    """Create a new customer.

    Expects JSON::

        {"name": "Jane Doe", "email": "jane@example.com", "phone": "555-0100"}
    """
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400

    name = body.get("name")
    email = body.get("email")
    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    customer = Customer(
        name=name,
        email=email,
        phone=body.get("phone"),
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({"data": customer.to_dict()}), 201
