"""LineItem model - a single product entry within an order."""

from models.customer import db


class LineItem(db.Model):  # type: ignore[name-defined]
    """One row in an order, linking a product to a quantity and price."""

    __tablename__ = "line_items"

    id: int = db.Column(db.Integer, primary_key=True)
    order_id: int = db.Column(
        db.Integer, db.ForeignKey("orders.id"), nullable=False
    )
    product_name: str = db.Column(db.String(200), nullable=False)
    quantity: int = db.Column(db.Integer, nullable=False, default=1)
    unit_price: float = db.Column(db.Float, nullable=False)
    discount_pct: float = db.Column(db.Float, default=0.0)

    @property
    def line_total(self) -> float:
        """Price after applying the per-item discount."""
        discount_multiplier = 1.0 - (self.discount_pct / 100.0)
        return round(self.quantity * self.unit_price * discount_multiplier, 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "discount_pct": self.discount_pct,
            "total": self.line_total,
        }

    def __repr__(self) -> str:
        return f"<LineItem {self.id}: {self.product_name} x{self.quantity}>"
