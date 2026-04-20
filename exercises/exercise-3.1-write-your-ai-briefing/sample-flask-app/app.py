"""Bookstore REST API.

A small Flask application that exposes CRUD operations for books. All
responses use the standard envelope ``{"data": ..., "error": ...}`` and
every datetime value is formatted as ISO 8601.
"""

from flask import Flask, jsonify, request

from models import Book, db


def create_app(database_uri: str = "sqlite:///bookstore.db") -> Flask:
    """Application factory.

    Parameters
    ----------
    database_uri:
        SQLAlchemy database URI.  Defaults to a local SQLite file.
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def success_response(data, status_code: int = 200):
        """Wrap *data* in the standard envelope and return a response."""
        return jsonify({"data": data, "error": None}), status_code

    def error_response(message: str, status_code: int = 400):
        """Return an error in the standard envelope."""
        return jsonify({"data": None, "error": message}), status_code

    # ------------------------------------------------------------------
    # Error handlers
    # ------------------------------------------------------------------

    @app.errorhandler(404)
    def not_found(_error):
        return error_response("resource not found", 404)

    @app.errorhandler(400)
    def bad_request(_error):
        return error_response("bad request", 400)

    @app.errorhandler(500)
    def internal_error(_error):
        return error_response("internal server error", 500)

    # ------------------------------------------------------------------
    # Routes -- /books
    # ------------------------------------------------------------------

    @app.route("/books", methods=["GET"])
    def get_books():
        """Return a paginated list of books.

        Query parameters
        ----------------
        page : int, default 1
            The page number (1-indexed).
        per_page : int, default 20
            Number of items per page.  Maximum 100.
        """
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 20, type=int), 100)

        pagination = Book.query.order_by(Book.id).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return success_response({
            "books": [book.to_dict() for book in pagination.items],
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
        })

    @app.route("/books/<int:book_id>", methods=["GET"])
    def get_book(book_id: int):
        """Return a single book by its ID."""
        book = db.session.get(Book, book_id)
        if book is None:
            return error_response("book not found", 404)
        return success_response(book.to_dict())

    @app.route("/books", methods=["POST"])
    def create_book():
        """Create a new book.

        Expects a JSON body with ``title``, ``author``, ``isbn``, and
        optionally ``published_date`` (YYYY-MM-DD).
        """
        body = request.get_json(silent=True)
        if body is None:
            return error_response("request body must be JSON", 400)

        required_fields = ("title", "author", "isbn")
        missing = [f for f in required_fields if f not in body]
        if missing:
            return error_response(f"missing required fields: {', '.join(missing)}", 400)

        if Book.query.filter_by(isbn=body["isbn"]).first() is not None:
            return error_response("a book with this ISBN already exists", 409)

        book = Book(
            title=body["title"],
            author=body["author"],
            isbn=body["isbn"],
            published_date=body.get("published_date"),
        )
        db.session.add(book)
        db.session.commit()

        return success_response(book.to_dict(), 201)

    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id: int):
        """Delete a book by its ID."""
        book = db.session.get(Book, book_id)
        if book is None:
            return error_response("book not found", 404)

        db.session.delete(book)
        db.session.commit()

        return success_response({"deleted": book_id})

    return app


# Allow running directly with `python app.py` during development.
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
