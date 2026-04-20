"""Tests for the Bookstore API."""

import pytest

from app import create_app, db, Book


@pytest.fixture
def app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def seeded_client(app):
    with app.app_context():
        books = [
            Book(title="The Pragmatic Programmer", author="David Thomas",
                 isbn="9780135957059", price=49.99, in_stock=True),
            Book(title="Clean Code", author="Robert Martin",
                 isbn="9780132350884", price=39.99, in_stock=True),
            Book(title="Design Patterns", author="Gang of Four",
                 isbn="9780201633610", price=59.99, in_stock=False),
        ]
        db.session.add_all(books)
        db.session.commit()

    return app.test_client()


class TestGetBooks:
    def test_list_all_books(self, seeded_client):
        resp = seeded_client.get("/books")
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert len(data) == 3

    def test_filter_in_stock(self, seeded_client):
        resp = seeded_client.get("/books?in_stock=true")
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert len(data) == 2
        assert all(book["in_stock"] is True for book in data)

    def test_filter_out_of_stock(self, seeded_client):
        resp = seeded_client.get("/books?in_stock=false")
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert len(data) == 1
        assert data[0]["in_stock"] is False

    def test_empty_database(self, client):
        resp = client.get("/books")
        assert resp.status_code == 200
        assert resp.get_json()["data"] == []


class TestGetBook:
    def test_existing_book(self, seeded_client):
        resp = seeded_client.get("/books/1")
        assert resp.status_code == 200
        assert resp.get_json()["data"]["title"] == "The Pragmatic Programmer"

    def test_nonexistent_book(self, seeded_client):
        resp = seeded_client.get("/books/999")
        assert resp.status_code == 404


class TestCreateBook:
    def test_create_book(self, client):
        resp = client.post("/books", json={
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "1234567890123",
            "price": 29.99,
        })
        assert resp.status_code == 201
        assert resp.get_json()["data"]["title"] == "Test Book"

    def test_missing_fields(self, client):
        resp = client.post("/books", json={"title": "Incomplete"})
        assert resp.status_code == 400


class TestSearchBooks:
    def test_search_by_title(self, seeded_client):
        resp = seeded_client.get("/books/search?q=pragmatic")
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert len(data) == 1
        assert "Pragmatic" in data[0]["title"]

    def test_search_too_short(self, seeded_client):
        resp = seeded_client.get("/books/search?q=a")
        assert resp.status_code == 400


class TestBookStats:
    def test_stats_with_books(self, seeded_client):
        resp = seeded_client.get("/books/stats")
        assert resp.status_code == 200
        stats = resp.get_json()["data"]
        assert stats["total_books"] == 3
        assert stats["in_stock"] == 2
        assert stats["out_of_stock"] == 1
        assert stats["average_price"] == 49.99

    def test_stats_empty_database(self, client):
        resp = client.get("/books/stats")
        assert resp.status_code == 200
        stats = resp.get_json()["data"]
        assert stats["total_books"] == 0
