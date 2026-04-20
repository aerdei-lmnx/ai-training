from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"

    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(255), nullable=False)
    author: str = db.Column(db.String(255), nullable=False)
    isbn: str = db.Column(db.String(13), unique=True, nullable=False)
    published_date: str = db.Column(db.String(10), nullable=True)  # stored as YYYY-MM-DD
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self) -> dict:
        """Serialize the book to a dictionary.

        Dates are formatted as ISO 8601 strings. The published_date field is
        stored as a plain YYYY-MM-DD string so it is returned as-is.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "published_date": self.published_date,
            "created_at": self.created_at.isoformat() + "Z" if self.created_at else None,
            "updated_at": self.updated_at.isoformat() + "Z" if self.updated_at else None,
        }
