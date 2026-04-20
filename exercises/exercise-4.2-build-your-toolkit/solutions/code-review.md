# Code Review Prompt Template -- Completed Example

## Context

Project: Bookshelf API
Language: Python
Framework: Flask 3.x with Flask-SQLAlchemy
Python version: 3.12
Test framework: pytest with pytest-cov

## Task

Review the following code changes for:

- Security vulnerabilities (SQL injection, XSS, authentication/authorization issues)
- Performance issues (N+1 queries, missing indexes, unnecessary database calls)
- Adherence to our coding standards (see Constraints below)
- Adequate test coverage (new code should have corresponding tests)
- Proper error handling (no bare excepts, meaningful error messages)
- Type hint correctness

## Code to Review

```python
# paste the code you want reviewed here
```

## Constraints

- Follow PEP 8 formatting (enforced by ruff)
- All public functions must have Google-style docstrings
- Maximum function length is 30 lines
- Use type hints for all function signatures and return types
- Use `pathlib.Path` instead of `os.path` for file operations
- Database queries must use parameterized statements (no string formatting)
- All endpoints must check authentication via our `@require_auth` decorator
- Avoid mutable default arguments

## Output Format

Organize your feedback into four sections:

1. **Summary** -- A 2-3 sentence overview of the changes and your overall assessment.
2. **Critical Issues** -- Problems that must be fixed before merging. For each issue include:
   - The file and line number
   - A description of the problem
   - A suggested fix with a code snippet
3. **Suggestions** -- Non-blocking improvements that would make the code better. Same format as above.
4. **Praise** -- Call out anything that is particularly well done (good naming, clever solution, thorough tests, etc.).
