"""InventoryLog model - tracks stock changes for products."""

from datetime import datetime, timezone

from models.customer import db


class InventoryLog(db.Model):  # type: ignore[name-defined]
    """An audit-style log entry for inventory adjustments.

    Positive ``quantity_change`` = stock received.
    Negative ``quantity_change`` = stock sold / written off.
    """

    __tablename__ = "inventory_logs"

    id: int = db.Column(db.Integer, primary_key=True)
    product_id: int = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    quantity_change: int = db.Column(db.Integer, nullable=False)
    reason: str | None = db.Column(db.String(255), nullable=True)
    created_at: datetime = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity_change": self.quantity_change,
            "reason": self.reason,
            "created_at": self.created_at.isoformat() + "Z",
        }

    def __repr__(self) -> str:
        return (
            f"<InventoryLog product={self.product_id} "
            f"change={self.quantity_change:+d}>"
        )
