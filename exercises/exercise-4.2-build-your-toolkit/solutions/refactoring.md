# Refactoring Prompt Template -- Completed Example

## Context

Project: Bookshelf API
Language: Python
Framework: Flask 3.x with Flask-SQLAlchemy
Module/area being refactored: Book import pipeline (`app/services/import_books.py`)

## Current State

**What the code does:**
This module reads a CSV file of book data uploaded by library staff, validates each row, transforms it into our internal format, and inserts new books into the database. It also sends an email notification when the import is complete.

**Why it needs refactoring:**
- The main function is 150 lines long and does everything: file I/O, validation, transformation, database writes, and email sending.
- Validation rules are buried inside nested if/else blocks and hard to find or update.
- There are no unit tests because the function cannot be tested without a real database and SMTP server.
- Error handling is inconsistent -- some errors are caught and logged, others crash the whole import.
- Magic strings and numbers throughout (e.g., `if row[7] == "1"` with no explanation of what column 7 is).

## Code to Refactor

```python
# paste the code you want refactored here
```

## Goals

- Each function does one thing and is easy to name.
- Business logic (validation, transformation) is separated from I/O (file reading, database writes, email).
- The code is easy to unit test -- I/O dependencies can be mocked or injected.
- Validation rules are collected in one place so they are easy to find, read, and update.
- Errors during import are collected and reported at the end rather than crashing the whole process.

## Constraints

- The public function signature `import_books(file_path: str) -> ImportResult` must stay the same so existing callers (the Flask route and the CLI command) are not affected.
- Must remain backward-compatible with the current CSV format.
- Follow PEP 8, use type hints on all functions and return types.
- Maximum function length is 30 lines.
- Use dataclasses or Pydantic models instead of raw dicts for structured data.
- Use `pathlib.Path` instead of `os.path`.

## Output Format

Please provide:

1. **Refactored code** -- The full refactored module, ready to drop into the project.
2. **Summary of changes** -- A bullet list of what changed and why.
3. **Design decisions** -- Explain any structural choices you made (e.g., "I used a dataclass for BookRow because...").
4. **Test suggestions** -- List the unit tests I should write for the new structure, with brief descriptions of what each test covers.
