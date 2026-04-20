# Bug Investigation Prompt Template -- Completed Example

## Context

Project: Bookshelf API
Language: Python
Framework: Flask 3.x with Flask-SQLAlchemy
Environment: Production on AWS ECS (Fargate), PostgreSQL 15 on RDS, Redis 7 for caching

## Bug Description

**What should happen:**
When a user requests `GET /api/books?author=Octavia+Butler`, the API should return a JSON array of all books by that author, sorted by publication date.

**What actually happens:**
The endpoint returns an empty array `[]` even though there are 12 books by Octavia Butler in the database. No error is logged. The HTTP status code is 200.

**Steps to reproduce:**
1. Confirm books exist: run `SELECT count(*) FROM books WHERE author = 'Octavia Butler';` -- returns 12.
2. Send `GET /api/books?author=Octavia+Butler` with a valid auth token.
3. Response body is `[]` with status 200.

## What I Have Already Tried

- Verified the database has the expected rows (see step 1 above).
- Checked the application logs -- no errors, no warnings.
- Tested with other authors -- same problem for some authors but not all.
- Confirmed the auth token is valid and has the correct permissions.
- Restarted the ECS tasks in case of stale cache -- no change.

## Error Output / Logs

```
# Application log (DEBUG level) for the request:
2026-04-18 14:32:01 DEBUG bookshelf.routes.books: GET /api/books called with filters={'author': 'Octavia Butler'}
2026-04-18 14:32:01 DEBUG bookshelf.db: Executing query: SELECT * FROM books WHERE author ILIKE %s AND deleted_at IS NULL
2026-04-18 14:32:01 DEBUG bookshelf.db: Query params: ('octavia butler%',)
2026-04-18 14:32:01 DEBUG bookshelf.routes.books: Query returned 0 results
```

## Relevant Files

- `app/routes/books.py` -- the endpoint handler for `GET /api/books`
- `app/db/queries.py` -- where the SQL query is built
- `app/db/models.py` -- SQLAlchemy model for `Book`

## Constraints

- Do not change the public API (URL structure, query parameters, response format).
- The fix must be backward-compatible -- other endpoints that use the same query builder must continue to work.
- We cannot change the database schema without a migration, so if a migration is needed, call that out explicitly.

## Output Format

Please provide:

1. **Root cause analysis** -- Explain what is causing the empty result and why.
2. **Suggested fix** -- Show the code change needed, with before/after snippets.
3. **Verification steps** -- How to confirm the fix works (specific curl commands or test cases).
4. **Regression tests** -- Suggest pytest test cases to add so this bug does not come back.
