"""Customer model - represents a buyer in the system."""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Customer(db.Model):  # type: ignore[name-defined]
    """A registered customer who can place orders."""

    __tablename__ = "customers"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    phone: str | None = db.Column(db.String(20), nullable=True)
    created_at: datetime = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    orders = db.relationship("Order", backref="customer", lazy="select")

    def to_dict(self, include_orders: bool = False) -> dict:
        data: dict = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() + "Z",
        }
        if include_orders:
            data["orders"] = [o.to_dict() for o in self.orders]
        return data

    def __repr__(self) -> str:
        return f"<Customer {self.id}: {self.name}>"
