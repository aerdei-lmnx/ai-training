"""Bookstore API - a simple REST API for managing books."""

from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    published_date = db.Column(db.String(10))
    in_stock = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "price": self.price,
            "published_date": self.published_date,
            "in_stock": self.in_stock,
            "created_at": self.created_at.isoformat() + "Z",
        }


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookstore.db"
    db.init_app(app)

    with app.app_context():
        db.create_all()
        _seed_if_empty()

    register_routes(app)
    return app


def _seed_if_empty():
    if Book.query.first() is not None:
        return

    books = [
        Book(
            title="The Pragmatic Programmer",
            author="David Thomas, Andrew Hunt",
            isbn="9780135957059",
            price=49.99,
            published_date="2019-09-23",
            in_stock=True,
        ),
        Book(
            title="Clean Code",
            author="Robert C. Martin",
            isbn="9780132350884",
            price=39.99,
            published_date="2008-08-01",
            in_stock=True,
        ),
        Book(
            title="Design Patterns",
            author="Gang of Four",
            isbn="9780201633610",
            price=59.99,
            published_date="1994-10-31",
            in_stock=False,
        ),
    ]
    db.session.add_all(books)
    db.session.commit()


def register_routes(app):
    @app.route("/books", methods=["GET"])
    def get_books():
        """List all books, optionally filtered by in_stock status."""
        in_stock = request.args.get("in_stock")

        if in_stock is not None:
            books = Book.query.filter_by(in_stock=in_stock).all()
        else:
            books = Book.query.all()

        return jsonify({"data": [book.to_dict() for book in books]})

    @app.route("/books/<int:book_id>", methods=["GET"])
    def get_book(book_id):
        """Get a single book by ID."""
        book = db.session.get(Book, book_id)
        if book is None:
            return jsonify({"error": "Book not found"}), 404
        return jsonify({"data": book.to_dict()})

    @app.route("/books", methods=["POST"])
    def create_book():
        """Create a new book."""
        data = request.get_json()

        required = ["title", "author", "isbn", "price"]
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        book = Book(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            price=data["price"],
            published_date=data.get("published_date"),
            in_stock=data.get("in_stock", True),
        )
        db.session.add(book)
        db.session.commit()

        return jsonify({"data": book.to_dict()}), 201

    @app.route("/books/search", methods=["GET"])
    def search_books():
        """Search books by title or author."""
        query = request.args.get("q", "")

        if len(query) < 2:
            return jsonify({"error": "Search query must be at least 2 characters"}), 400

        results = Book.query.filter(
            db.or_(
                Book.title.ilike(f"%{query}%"),
                Book.author.ilike(f"%{query}%"),
            )
        ).all()

        return jsonify({"data": [book.to_dict() for book in results]})

    @app.route("/books/stats", methods=["GET"])
    def book_stats():
        """Get bookstore statistics."""
        total = Book.query.count()
        in_stock = Book.query.filter_by(in_stock=True).count()
        out_of_stock = total - in_stock

        prices = [b.price for b in Book.query.all()]
        avg_price = sum(prices) / len(prices)

        return jsonify({
            "data": {
                "total_books": total,
                "in_stock": in_stock,
                "out_of_stock": out_of_stock,
                "average_price": round(avg_price, 2),
            }
        })


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5002)
