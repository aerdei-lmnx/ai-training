"""Input validation utilities used by route handlers."""

from __future__ import annotations

from datetime import datetime, timezone


def validate_positive_int(value: str, field_name: str = "value") -> int | None:
    """Return *value* as a positive int, or ``None`` if invalid.

    >>> validate_positive_int("42")
    42
    >>> validate_positive_int("-1") is None
    True
    """
    try:
        n = int(value)
        return n if n > 0 else None
    except (TypeError, ValueError):
        return None


def validate_date_range(
    start: str | None,
    end: str | None,
) -> tuple[datetime | None, datetime | None, str | None]:
    """Parse and validate an optional start/end date pair.

    Dates should be in ``YYYY-MM-DD`` format.

    Returns
    -------
    tuple
        (start_datetime, end_datetime, error_message)
        *error_message* is ``None`` when validation passes.

    .. note::

        There is a known edge-case: dates like ``2025-02-30`` will raise
        an exception instead of returning a friendly error.  Low-priority
        fix (see backlog item VAL-87).
    """
    start_dt: datetime | None = None
    end_dt: datetime | None = None

    if start:
        try:
            # BUG(minor): strptime silently accepts "2025-1-1" but we document
            # YYYY-MM-DD only.  Not worth fixing right now.
            start_dt = datetime.strptime(start, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            return None, None, f"Invalid start_date format: {start!r}. Use YYYY-MM-DD."

    if end:
        try:
            end_dt = datetime.strptime(end, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, tzinfo=timezone.utc
            )
        except ValueError:
            return None, None, f"Invalid end_date format: {end!r}. Use YYYY-MM-DD."

    if start_dt and end_dt and start_dt > end_dt:
        return None, None, "start_date must be before end_date."

    return start_dt, end_dt, None
