"""Output formatters for the log analyzer.

Three formats are supported:

- **text** -- human-readable, tab-separated columns
- **json** -- machine-readable JSON object
- **csv**  -- comma-separated values with a header row
"""

from __future__ import annotations

import csv
import io
import json
from collections import Counter
from typing import Optional

from log_parser import LEVELS, LogEntry


def _build_stats(entries: list[LogEntry]) -> dict:
    """Compute summary statistics from a list of log entries."""
    level_counts: Counter[str] = Counter()
    component_counts: Counter[str] = Counter()
    message_counts: Counter[str] = Counter()

    for entry in entries:
        level_counts[entry.level] += 1
        component_counts[entry.component] += 1
        message_counts[entry.message] += 1

    # Ensure every level appears in the output, even with zero count.
    for level in LEVELS:
        level_counts.setdefault(level, 0)

    time_range_start: Optional[str] = None
    time_range_end: Optional[str] = None
    if entries:
        time_range_start = entries[0].timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        time_range_end = entries[-1].timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "total": len(entries),
        "levels": {level: level_counts[level] for level in LEVELS},
        "components": dict(component_counts.most_common()),
        "messages": message_counts,
        "time_range_start": time_range_start,
        "time_range_end": time_range_end,
    }


def format_text(
    entries: list[LogEntry],
    *,
    top_n: Optional[int] = None,
) -> str:
    """Return a human-readable, tab-separated summary."""
    stats = _build_stats(entries)
    lines: list[str] = []

    lines.append(f"Total lines:\t{stats['total']}")
    lines.append("")

    lines.append("Level\tCount")
    for level in LEVELS:
        lines.append(f"{level}\t{stats['levels'][level]}")
    lines.append("")

    lines.append("Component\tCount")
    for comp, count in sorted(stats["components"].items(), key=lambda x: -x[1]):
        lines.append(f"{comp}\t{count}")
    lines.append("")

    if stats["time_range_start"]:
        lines.append(f"Time range:\t{stats['time_range_start']} -- {stats['time_range_end']}")
        lines.append("")

    if top_n is not None and top_n > 0:
        lines.append(f"Top {top_n} messages\tCount")
        for msg, count in stats["messages"].most_common(top_n):
            lines.append(f"{msg}\t{count}")
        lines.append("")

    return "\n".join(lines)


def format_json(
    entries: list[LogEntry],
    *,
    top_n: Optional[int] = None,
) -> str:
    """Return a JSON object with summary statistics."""
    stats = _build_stats(entries)

    output: dict = {
        "total": stats["total"],
        "levels": stats["levels"],
        "components": stats["components"],
        "time_range": {
            "start": stats["time_range_start"],
            "end": stats["time_range_end"],
        },
    }

    if top_n is not None and top_n > 0:
        output["top_messages"] = [
            {"message": msg, "count": count}
            for msg, count in stats["messages"].most_common(top_n)
        ]

    return json.dumps(output, indent=2)


def format_csv(
    entries: list[LogEntry],
    *,
    top_n: Optional[int] = None,
) -> str:
    """Return CSV with one row per entry (timestamp, level, component, message).

    A summary section is appended after a blank line.
    """
    buf = io.StringIO()
    writer = csv.writer(buf)

    # Entry rows
    writer.writerow(["timestamp", "level", "component", "message"])
    for entry in entries:
        writer.writerow([
            entry.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            entry.level,
            entry.component,
            entry.message,
        ])

    # Summary section
    stats = _build_stats(entries)
    writer.writerow([])
    writer.writerow(["summary_field", "value"])
    writer.writerow(["total", stats["total"]])
    for level in LEVELS:
        writer.writerow([f"level_{level}", stats["levels"][level]])
    for comp, count in sorted(stats["components"].items(), key=lambda x: -x[1]):
        writer.writerow([f"component_{comp}", count])
    if stats["time_range_start"]:
        writer.writerow(["time_range_start", stats["time_range_start"]])
        writer.writerow(["time_range_end", stats["time_range_end"]])

    if top_n is not None and top_n > 0:
        writer.writerow([])
        writer.writerow(["top_message", "count"])
        for msg, count in stats["messages"].most_common(top_n):
            writer.writerow([msg, count])

    return buf.getvalue()
