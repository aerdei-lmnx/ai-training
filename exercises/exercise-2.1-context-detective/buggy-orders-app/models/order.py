"""Order model - represents a customer purchase."""

from datetime import datetime, timezone

from models.customer import db


class Order(db.Model):  # type: ignore[name-defined]
    """An order placed by a customer, containing one or more line items."""

    __tablename__ = "orders"

    id: int = db.Column(db.Integer, primary_key=True)
    customer_id: int = db.Column(
        db.Integer, db.ForeignKey("customers.id"), nullable=False
    )
    created_at: datetime = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime | None = db.Column(db.DateTime, nullable=True)
    active: bool = db.Column(db.Boolean, default=True, nullable=False)
    notes: str | None = db.Column(db.Text, nullable=True)

    # Relationships -------------------------------------------------------
    # noload is used here because in most views we don't need line items
    # eagerly; callers that need them should use joinedload() explicitly.
    line_items = db.relationship(
        "LineItem", backref="order", lazy="noload"
    )

    # ------------------------------------------------------------------

    @property
    def total(self) -> float:
        """Sum of all line-item totals."""
        return round(
            sum(item.quantity * item.unit_price for item in self.line_items),
            2,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "created_at": self.created_at.isoformat() + "Z",
            "active": self.active,
            "notes": self.notes,
            "line_items": [item.to_dict() for item in self.line_items],
            "total": self.total,
        }

    def __repr__(self) -> str:
        return f"<Order {self.id} customer={self.customer_id}>"
