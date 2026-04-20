"""Database models for the Task Management API."""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    """A task in the task management system."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending",
    )
    priority = db.Column(
        db.String(10),
        nullable=False,
        default="medium",
    )
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    VALID_STATUSES = ("pending", "in_progress", "done")
    VALID_PRIORITIES = ("low", "medium", "high")

    def to_dict(self) -> dict:
        """Serialize the task to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
