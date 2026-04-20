"""Log line parsing and filtering logic.

Parses log lines in the format:
    {ISO-8601-UTC} {LEVEL} [{component}] {message}

Example:
    2026-04-15T08:23:01Z ERROR [auth] Failed login for user admin from 192.168.1.50
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

# Severity levels in ascending order.  WARN (not WARNING) matches the
# log format used by this project.
LEVELS: list[str] = ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"]

_LEVEL_INDEX: dict[str, int] = {level: i for i, level in enumerate(LEVELS)}

# Regex that captures the four fields of a log line.
_LINE_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)"  # timestamp (ISO 8601 UTC)
    r"\s+(DEBUG|INFO|WARN|ERROR|FATAL)"             # level
    r"\s+\[([a-z]+)\]"                              # component (always lowercase)
    r"\s+(.+)$"                                      # message (rest of line)
)


@dataclass(frozen=True)
class LogEntry:
    """A single parsed log line."""

    timestamp: datetime
    level: str
    component: str
    message: str


def parse_line(line: str) -> Optional[LogEntry]:
    """Parse a single log line and return a ``LogEntry``, or ``None`` if
    the line does not match the expected format."""
    line = line.strip()
    if not line:
        return None
    match = _LINE_RE.match(line)
    if match is None:
        return None
    ts_str, level, component, message = match.groups()
    timestamp = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )
    return LogEntry(
        timestamp=timestamp,
        level=level,
        component=component,
        message=message,
    )


def parse_file(path: str) -> list[LogEntry]:
    """Read a log file and return all successfully parsed entries."""
    entries: list[LogEntry] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            entry = parse_line(line)
            if entry is not None:
                entries.append(entry)
    return entries


def level_at_or_above(min_level: str) -> list[str]:
    """Return a list of levels that are at or above *min_level*.

    >>> level_at_or_above("WARN")
    ['WARN', 'ERROR', 'FATAL']
    """
    idx = _LEVEL_INDEX.get(min_level.upper())
    if idx is None:
        raise ValueError(f"Unknown level: {min_level!r}. Valid levels: {LEVELS}")
    return LEVELS[idx:]


def filter_entries(
    entries: list[LogEntry],
    *,
    min_level: Optional[str] = None,
    component: Optional[str] = None,
    time_from: Optional[datetime] = None,
    time_to: Optional[datetime] = None,
) -> list[LogEntry]:
    """Return entries that match all supplied filter criteria.

    Parameters
    ----------
    min_level:
        If set, only include entries at this level or above (e.g.
        ``"WARN"`` includes WARN, ERROR, and FATAL).
    component:
        If set, only include entries whose component matches (case-insensitive).
    time_from:
        If set, only include entries at or after this timestamp.
    time_to:
        If set, only include entries at or before this timestamp.
    """
    result: list[LogEntry] = entries

    if min_level is not None:
        allowed = set(level_at_or_above(min_level))
        result = [e for e in result if e.level in allowed]

    if component is not None:
        comp_lower = component.lower()
        result = [e for e in result if e.component == comp_lower]

    if time_from is not None:
        result = [e for e in result if e.timestamp >= time_from]

    if time_to is not None:
        result = [e for e in result if e.timestamp <= time_to]

    return result
