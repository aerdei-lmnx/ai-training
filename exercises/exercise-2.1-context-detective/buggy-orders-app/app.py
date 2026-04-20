from flask import Flask, jsonify

from models import Customer, LineItem, Order, db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.db"
    db.init_app(app)

    with app.app_context():
        db.create_all()
        _seed_if_empty()

    register_routes(app)
    return app


def _seed_if_empty():
    if Customer.query.first() is not None:
        return

    alice = Customer(name="Alice Johnson", email="alice@example.com")
    bob = Customer(name="Bob Smith", email="bob@example.com")
    db.session.add_all([alice, bob])
    db.session.flush()

    order1 = Order(customer_id=alice.id, active=True)
    order2 = Order(customer_id=alice.id, active=True)
    order3 = Order(customer_id=bob.id, active=True)
    db.session.add_all([order1, order2, order3])
    db.session.flush()

    items = [
        LineItem(order_id=order1.id, product_name="Mechanical Keyboard", quantity=1, unit_price=89.99),
        LineItem(order_id=order1.id, product_name="USB-C Cable", quantity=3, unit_price=12.50),
        LineItem(order_id=order2.id, product_name="Monitor Stand", quantity=1, unit_price=45.00),
        LineItem(order_id=order3.id, product_name="Laptop Sleeve", quantity=2, unit_price=29.99),
        LineItem(order_id=order3.id, product_name="Wireless Mouse", quantity=1, unit_price=34.99),
    ]
    db.session.add_all(items)
    db.session.commit()


def register_routes(app):
    @app.route("/api/orders", methods=["GET"])
    def get_orders():
        orders = Order.query.filter_by(active=True).all()
        return jsonify({"data": [order.to_dict() for order in orders]})

    @app.route("/api/orders/<int:order_id>", methods=["GET"])
    def get_order(order_id):
        order = db.session.get(Order, order_id)
        if order is None:
            return jsonify({"error": "Order not found"}), 404
        return jsonify({"data": order.to_dict()})

    @app.route("/api/customers", methods=["GET"])
    def get_customers():
        customers = Customer.query.all()
        return jsonify({"data": [c.to_dict() for c in customers]})


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
