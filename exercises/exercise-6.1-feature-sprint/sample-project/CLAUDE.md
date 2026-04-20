# Task Management API

## Project Overview

A REST API for managing tasks, built with Flask and SQLAlchemy. The API supports creating, reading, updating, and listing tasks with filtering.

## Tech Stack

- **Python 3.10+**
- **Flask 3.x** -- web framework
- **SQLAlchemy 2.x** via Flask-SQLAlchemy -- ORM and database
- **SQLite** -- database (file-based for dev, in-memory for tests)
- **pytest** -- testing

## Project Structure

```
sample-project/
  app.py            # Flask app factory, all route handlers
  models.py         # SQLAlchemy model definitions
  requirements.txt  # Python dependencies
  tests/
    test_app.py     # API endpoint tests
```

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python app.py

# The API is available at http://localhost:5000
```

## How to Test

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run a specific test class
python -m pytest tests/test_app.py::TestCreateTask -v
```

## Coding Standards

1. **Every new endpoint must have tests.** Tests go in `tests/test_app.py`, grouped into classes by endpoint (e.g., `TestDeleteTask`).
2. **Use proper HTTP status codes.** 200 for success, 201 for creation, 204 for deletion, 400 for bad input, 404 for not found.
3. **Validate all input.** Never trust user-provided data. Return a JSON error message with a 400 status for invalid input.
4. **Use the application factory pattern.** The `create_app()` function is the entry point. Routes are registered in `register_routes()`.
5. **Wrap responses in a `data` key.** Successful responses use `{"data": ...}`. Errors use `{"error": "message"}`.
6. **Keep route handlers in `app.py`.** Do not create separate blueprint files for this project.
7. **Use type hints** in function signatures.
8. **Keep test fixtures in conftest or at the top of the test file.** Use the existing `app`, `client`, and `sample_task` fixtures.
