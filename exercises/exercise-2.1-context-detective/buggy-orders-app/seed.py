"""Seed script - populates the database with sample data.

Usage::

    python seed.py

This will drop and recreate all tables, then insert demo customers, orders,
line items, products, and inventory logs.
"""

from app import create_app
from models import (
    Customer,
    InventoryLog,
    LineItem,
    Order,
    Product,
    db,
)


def seed() -> None:
    """Insert sample data into every table."""
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

        # ----- Customers -----
        alice = Customer(name="Alice Johnson", email="alice@example.com", phone="555-0101")
        bob = Customer(name="Bob Smith", email="bob@example.com", phone="555-0102")
        carol = Customer(name="Carol Davis", email="carol@example.com")
        db.session.add_all([alice, bob, carol])
        db.session.flush()

        # ----- Products -----
        keyboard = Product(sku="KB-MK01", name="Mechanical Keyboard", price=89.99,
                           description="Cherry MX Blue switches, full-size")
        cable = Product(sku="CB-UC01", name="USB-C Cable", price=12.50,
                        description="Braided, 2m length")
        stand = Product(sku="ST-MN01", name="Monitor Stand", price=45.00,
                        description="Adjustable aluminum stand")
        sleeve = Product(sku="SL-LP01", name="Laptop Sleeve", price=29.99,
                         description="Neoprene, fits up to 15 inch")
        mouse = Product(sku="MS-WL01", name="Wireless Mouse", price=34.99,
                        description="Ergonomic, Bluetooth 5.0")
        headset = Product(sku="HS-BT01", name="Bluetooth Headset", price=59.99,
                          description="Noise-cancelling, 20hr battery")
        db.session.add_all([keyboard, cable, stand, sleeve, mouse, headset])
        db.session.flush()

        # ----- Orders -----
        order1 = Order(customer_id=alice.id, active=True, notes="Rush delivery")
        order2 = Order(customer_id=alice.id, active=True)
        order3 = Order(customer_id=bob.id, active=True, notes="Gift wrap please")
        order4 = Order(customer_id=carol.id, active=False, notes="Cancelled by customer")
        db.session.add_all([order1, order2, order3, order4])
        db.session.flush()

        # ----- Line Items (5 items across active orders) -----
        items = [
            LineItem(order_id=order1.id, product_name="Mechanical Keyboard",
                     quantity=1, unit_price=89.99),
            LineItem(order_id=order1.id, product_name="USB-C Cable",
                     quantity=3, unit_price=12.50),
            LineItem(order_id=order2.id, product_name="Monitor Stand",
                     quantity=1, unit_price=45.00),
            LineItem(order_id=order3.id, product_name="Laptop Sleeve",
                     quantity=2, unit_price=29.99),
            LineItem(order_id=order3.id, product_name="Wireless Mouse",
                     quantity=1, unit_price=34.99),
        ]
        db.session.add_all(items)

        # ----- Inventory Logs -----
        # Only keyboard and cable have stock movements; other products
        # intentionally have zero logs so /inventory/summary returns empty
        # recent_logs for them (this is correct, not a bug).
        logs = [
            InventoryLog(product_id=keyboard.id, quantity_change=100,
                         reason="Initial stock from supplier"),
            InventoryLog(product_id=keyboard.id, quantity_change=-1,
                         reason="Sold - Order #1"),
            InventoryLog(product_id=cable.id, quantity_change=200,
                         reason="Initial stock from supplier"),
            InventoryLog(product_id=cable.id, quantity_change=-3,
                         reason="Sold - Order #1"),
        ]
        db.session.add_all(logs)

        db.session.commit()
        print("Database seeded successfully.")
        print(f"  Customers: {Customer.query.count()}")
        print(f"  Products:  {Product.query.count()}")
        print(f"  Orders:    {Order.query.count()}")
        print(f"  LineItems: {LineItem.query.count()}")
        print(f"  Inventory: {InventoryLog.query.count()}")


if __name__ == "__main__":
    seed()
