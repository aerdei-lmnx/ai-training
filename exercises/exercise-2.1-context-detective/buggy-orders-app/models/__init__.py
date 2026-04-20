"""Database models package.

Exports all SQLAlchemy models and the shared db instance so that other
modules can do::

    from models import db, Customer, Order, LineItem, Product, InventoryLog
"""

from models.customer import Customer
from models.inventory import InventoryLog
from models.line_item import LineItem
from models.order import Order
from models.product import Product

# Re-export the shared db instance from whichever model defines it.
# customer.py creates it; every other model imports from there.
from models.customer import db

__all__ = [
    "db",
    "Customer",
    "Order",
    "LineItem",
    "Product",
    "InventoryLog",
]
