"""Tests for the bookstore API.

Every test gets a fresh in-memory SQLite database via the ``client``
fixture so tests never interfere with each other.
"""

import pytest

from app import create_app
from models import db as _db


@pytest.fixture()
def app():
    """Create an application instance with an in-memory database."""
    app = create_app(database_uri="sqlite:///:memory:")
    app.config["TESTING"] = True
    yield app


@pytest.fixture()
def client(app):
    """A Flask test client tied to the in-memory database."""
    return app.test_client()


# ------------------------------------------------------------------
# GET /books
# ------------------------------------------------------------------


def test_get_books_empty(client):
    """An empty database returns an empty list of books."""
    response = client.get("/books")
    assert response.status_code == 200

    body = response.get_json()
    assert body["error"] is None
    assert body["data"]["books"] == []
    assert body["data"]["total"] == 0


# ------------------------------------------------------------------
# POST /books  +  GET /books/<id>
# ------------------------------------------------------------------


def test_create_and_get_book(client):
    """Creating a book and then fetching it returns the correct data."""
    new_book = {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "isbn": "9781449373320",
        "published_date": "2017-03-16",
    }

    # Create
    post_response = client.post("/books", json=new_book)
    assert post_response.status_code == 201

    created = post_response.get_json()["data"]
    assert created["title"] == new_book["title"]
    assert created["isbn"] == new_book["isbn"]
    assert created["created_at"] is not None
    assert created["updated_at"] is not None

    # Fetch by ID
    get_response = client.get(f"/books/{created['id']}")
    assert get_response.status_code == 200

    fetched = get_response.get_json()["data"]
    assert fetched["id"] == created["id"]
    assert fetched["author"] == new_book["author"]


# ------------------------------------------------------------------
# GET /books/<id> -- 404
# ------------------------------------------------------------------


def test_get_nonexistent_book_returns_404(client):
    """Requesting a book that does not exist returns a 404 with the
    standard error envelope."""
    response = client.get("/books/9999")
    assert response.status_code == 404

    body = response.get_json()
    assert body["data"] is None
    assert body["error"] == "book not found"


# ------------------------------------------------------------------
# DELETE /books/<id>
# ------------------------------------------------------------------


def test_delete_book(client):
    """Deleting a book removes it from the database."""
    new_book = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
    }
    post_response = client.post("/books", json=new_book)
    book_id = post_response.get_json()["data"]["id"]

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200
    assert delete_response.get_json()["data"]["deleted"] == book_id

    # Confirm it is gone
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404


# ------------------------------------------------------------------
# POST /books -- validation
# ------------------------------------------------------------------


def test_create_book_missing_fields(client):
    """Omitting required fields returns a 400 with a helpful message."""
    response = client.post("/books", json={"title": "Incomplete"})
    assert response.status_code == 400

    body = response.get_json()
    assert body["data"] is None
    assert "missing required fields" in body["error"]


def test_create_duplicate_isbn(client):
    """Trying to create two books with the same ISBN returns 409."""
    book = {
        "title": "The Pragmatic Programmer",
        "author": "David Thomas",
        "isbn": "9780135957059",
    }
    client.post("/books", json=book)
    duplicate_response = client.post("/books", json=book)
    assert duplicate_response.status_code == 409
    assert "already exists" in duplicate_response.get_json()["error"]
