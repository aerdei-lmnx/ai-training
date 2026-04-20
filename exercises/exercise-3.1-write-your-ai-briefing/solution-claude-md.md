# Solution -- Example CLAUDE.md

Below is an example of a well-written `CLAUDE.md` for the sample Flask app. Your version does not need to match this word-for-word. What matters is that it captures the conventions and context that would help an AI (or a new developer) produce code that fits the project.

---

```markdown
# Bookstore API

A REST API for managing a bookstore catalog, built with Flask and SQLAlchemy.

## Tech Stack

- **Python 3.10+**
- **Flask 3.x** -- web framework
- **SQLAlchemy 2.x** via Flask-SQLAlchemy -- ORM / database
- **SQLite** -- default database (file: `bookstore.db`)
- **pytest 8.x** -- test framework

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python app.py
# or
flask --app app:create_app run --debug

# Run tests
pytest
```

## Project Structure

```
sample-flask-app/
  app.py              # Application factory, routes, error handlers
  models.py           # SQLAlchemy models
  requirements.txt    # Python dependencies
  tests/
    test_app.py       # API tests (pytest)
```

## API Conventions

These conventions MUST be followed in all new endpoints:

### Response Envelope

Every response uses this wrapper format -- no exceptions:

```json
{
  "data": <payload or null>,
  "error": <error message string or null>
}
```

- On success: `data` contains the result, `error` is `null`.
- On failure: `data` is `null`, `error` contains a human-readable message.

Use the `success_response()` and `error_response()` helpers defined in `app.py`.

### URL Naming

- All endpoint paths use **snake_case** (e.g., `/books`, `/book_categories`).
- Resource IDs are passed as path parameters: `/books/<int:book_id>`.

### Date Formatting

- All datetime fields are returned as **ISO 8601** strings with a trailing `Z` (e.g., `"2025-01-15T09:30:00Z"`).
- The `published_date` field is a plain `YYYY-MM-DD` string, not a full datetime.
- See `Book.to_dict()` in `models.py` for the canonical formatting logic.

### Pagination

List endpoints support pagination via query parameters:

- `?page=1&per_page=20` (defaults)
- `per_page` is capped at 100.
- The response includes `page`, `per_page`, and `total` alongside the list.

### Error Handling

- Custom error handlers are registered for 400, 404, and 500.
- They all use the standard `{"data": null, "error": "..."}` envelope.
- When a specific resource is not found in a route handler, return the error directly using `error_response("book not found", 404)` rather than calling `abort()`.

## Models

### Book

| Column           | Type         | Notes                          |
|------------------|--------------|--------------------------------|
| `id`             | Integer (PK) | Auto-increment                 |
| `title`          | String(255)  | Required                       |
| `author`         | String(255)  | Required                       |
| `isbn`           | String(13)   | Required, unique               |
| `published_date` | String(10)   | Optional, format `YYYY-MM-DD`  |
| `created_at`     | DateTime     | Set automatically on create    |
| `updated_at`     | DateTime     | Set automatically on create and update |

Every model has a `to_dict()` method for serialization. Always use it when returning model data in responses.

## Testing Conventions

- Tests live in `tests/test_app.py`.
- Each test uses the `client` fixture which provides a Flask test client backed by a **fresh in-memory SQLite database** -- no cleanup needed.
- Test functions are named `test_<action>_<scenario>` (e.g., `test_create_and_get_book`, `test_get_nonexistent_book_returns_404`).
- Tests verify both the HTTP status code and the response body structure (including the envelope).
- When adding a new endpoint, add at least one success-path test and one error-path test.

## Common Commands

```bash
# Run all tests
pytest

# Run all tests with verbose output
pytest -v

# Run a specific test
pytest tests/test_app.py::test_get_books_empty

# Start the dev server on port 5000
python app.py
```
```

---

## What Makes This Effective

1. **It leads with what matters for code generation** -- the response envelope, date format, and URL conventions are front and center.
2. **It shows concrete examples** -- the JSON envelope format is shown, not just described.
3. **It explains the non-obvious** -- the difference between `published_date` (plain string) and `created_at`/`updated_at` (ISO 8601 with Z suffix) is called out explicitly.
4. **It includes runnable commands** -- Claude can use these to verify its work.
5. **It is concise** -- everything fits in one screen. No filler.
