"""Product model - the catalog of available products."""

from datetime import datetime, timezone

from models.customer import db


class Product(db.Model):  # type: ignore[name-defined]
    """A product that can be ordered."""

    __tablename__ = "products"

    id: int = db.Column(db.Integer, primary_key=True)
    sku: str = db.Column(db.String(40), unique=True, nullable=False)
    name: str = db.Column(db.String(200), nullable=False)
    description: str | None = db.Column(db.Text, nullable=True)
    price: float = db.Column(db.Float, nullable=False)
    active: bool = db.Column(db.Boolean, default=True, nullable=False)
    created_at: datetime = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    inventory_logs = db.relationship(
        "InventoryLog", backref="product", lazy="select"
    )

    @property
    def current_stock(self) -> int:
        """Derive stock from inventory logs (sum of adjustments)."""
        return sum(log.quantity_change for log in self.inventory_logs)

    def to_dict(self, include_stock: bool = False) -> dict:
        data: dict = {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "active": self.active,
        }
        if include_stock:
            data["current_stock"] = self.current_stock
        return data

    def __repr__(self) -> str:
        return f"<Product {self.sku}: {self.name}>"
