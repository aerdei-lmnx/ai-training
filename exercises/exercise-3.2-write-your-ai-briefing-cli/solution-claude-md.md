# Solution -- Example CLAUDE.md

Below is an example of a well-written `CLAUDE.md` for the sample log analyzer. Your version does not need to match this word-for-word. What matters is that it captures the conventions and context that would help an AI (or a new developer) produce code that fits the project.

---

```markdown
# Log Analyzer

A CLI tool that parses and analyzes application log files. It reads structured log lines, filters them by level/component/time range, and outputs summary statistics.

## Tech Stack

- **Python 3.10+** -- stdlib only, no external dependencies
- **argparse** -- CLI argument parsing
- **pytest 8.x** -- test framework (the only non-stdlib dependency)

## Quick Start

```bash
# Install test dependencies
pip install -r requirements.txt

# Basic summary of a log file
python analyzer.py sample_logs/app.log

# Filter by minimum severity (includes WARN, ERROR, and FATAL)
python analyzer.py sample_logs/app.log --level WARN

# Filter by component
python analyzer.py sample_logs/app.log --component auth

# Time range filter
python analyzer.py sample_logs/app.log --from 2026-04-15T08:00:00Z --to 2026-04-15T09:00:00Z

# JSON output with top 5 messages
python analyzer.py sample_logs/app.log --format json --top 5

# Run tests
pytest
```

## Project Structure

```
sample-log-analyzer/
  analyzer.py          # CLI entry point (argparse, main loop)
  log_parser.py        # Log line parsing, level ordering, filtering
  formatters.py        # Output formatters (text, JSON, CSV)
  requirements.txt     # Python dependencies (pytest only)
  sample_logs/
    app.log            # Sample log file for testing
  tests/
    test_parser.py     # Tests for log_parser.py
```

## Log Line Format

Every log line follows this exact format:

```
{ISO-8601-UTC} {LEVEL} [{component}] {message}
```

Example:

```
2026-04-15T08:23:01Z ERROR [auth] Failed login for user admin from 192.168.1.50
```

The regex pattern is defined in `log_parser.py`. Lines that do not match are silently skipped.

## CLI Conventions

These conventions MUST be followed in all new code:

### Exit Codes

- **0** -- Success (log lines found and printed)
- **1** -- Error (bad arguments, file not found, I/O error)
- **2** -- No matching log lines found (the file was read successfully but nothing matched the filters, OR the file contained no valid log lines)

This is the most common mistake: exit code 2 means "no results", not "error". Do not use exit code 1 for empty results.

### Severity Levels

The five levels in ascending order are:

```
DEBUG < INFO < WARN < ERROR < FATAL
```

**WARN, not WARNING.** The level name `WARN` matches the log format. Never use `WARNING`.

### Level Filtering

`--level` is **inclusive of the specified level and above**. For example, `--level WARN` returns lines that are WARN, ERROR, or FATAL. Use `level_at_or_above()` from `log_parser.py`.

### Output Formats

- **text** (default): Human-readable, **tab-separated** columns. Not space-separated, not fixed-width -- tabs.
- **json**: A single JSON object with `total`, `levels`, `components`, `time_range`, and optionally `top_messages`.
- **csv**: Standard CSV. Entry rows first (timestamp, level, component, message), then a summary section after a blank row.

### Timestamps

- All timestamps are **UTC**. The format is `YYYY-MM-DDTHH:MM:SSZ` (trailing `Z`, no offset).
- The `--from` and `--to` flags accept the same format.
- Never convert to local time.

### Component Names

- Component names are **always lowercase** in log lines (enforced by the regex).
- The `--component` flag is case-insensitive (the code lowercases the input before comparing).

## Testing Conventions

- Tests live in `tests/test_parser.py`.
- Tests use pytest fixtures and classes for grouping.
- Test names follow the pattern `test_<what>_<scenario>` (e.g., `test_parse_valid_line`, `test_filter_by_min_level`).
- The `_make_entry()` helper creates `LogEntry` objects for tests without needing to parse a string.
- When adding a new feature, add tests for both the success path and edge cases (empty input, no matches, invalid input).

## Common Commands

```bash
# Run all tests
pytest

# Run all tests with verbose output
pytest -v

# Run a specific test class
pytest tests/test_parser.py::TestFilterEntries

# Run the analyzer against the sample log
python analyzer.py sample_logs/app.log

# Quick check: filter ERRORs and output JSON
python analyzer.py sample_logs/app.log --level ERROR --format json
```
```

---

## What Makes This Effective

1. **It calls out the non-obvious exit code convention** -- exit code 2 for "no results" is the kind of thing Claude will almost certainly get wrong without being told.
2. **It explicitly says WARN, not WARNING** -- this is a small detail that has a big impact. If Claude uses `WARNING`, the level filter silently breaks.
3. **It specifies tab-separated output** -- without this, Claude will likely use spaces or fixed-width formatting.
4. **It shows concrete examples** -- the log format, the CLI commands, and the level hierarchy are shown, not just described.
5. **It documents the level filtering behavior** -- "inclusive of the specified level and above" is a design choice that Claude needs to know about to implement new features correctly.
6. **It is concise** -- everything fits in one screen. No filler, no API documentation that belongs in a README.
