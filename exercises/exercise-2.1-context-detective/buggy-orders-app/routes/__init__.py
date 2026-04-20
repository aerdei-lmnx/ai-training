"""Route blueprints package.

Call ``register_blueprints(app)`` from the application factory to wire up
all API endpoints.
"""

from flask import Flask

from routes.customers import customers_bp
from routes.inventory import inventory_bp
from routes.orders import orders_bp
from routes.products import products_bp


def register_blueprints(app: Flask) -> None:
    """Attach every blueprint to *app*."""
    app.register_blueprint(orders_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(inventory_bp)
