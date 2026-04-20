#!/usr/bin/env python3
"""Log Analyzer -- a CLI tool for analyzing application log files.

Usage examples:
    python analyzer.py sample_logs/app.log
    python analyzer.py sample_logs/app.log --level ERROR
    python analyzer.py sample_logs/app.log --component auth --format json
    python analyzer.py sample_logs/app.log --from 2026-04-15T09:00:00Z --to 2026-04-15T10:00:00Z
    python analyzer.py sample_logs/app.log --top 5

Log format:
    {ISO-8601-UTC} {LEVEL} [{component}] {message}

Exit codes:
    0  Success
    1  Error (bad arguments, file not found, etc.)
    2  No matching log lines found
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone

from formatters import format_csv, format_json, format_text
from log_parser import LEVELS, filter_entries, parse_file


def _parse_timestamp(value: str) -> datetime:
    """Parse an ISO 8601 UTC timestamp from the command line."""
    try:
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid timestamp: {value!r}. Expected format: YYYY-MM-DDTHH:MM:SSZ"
        )


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Analyze application log files.",
        epilog="Exit codes: 0 = success, 1 = error, 2 = no matching lines.",
    )
    parser.add_argument(
        "logfile",
        help="Path to the log file to analyze.",
    )
    parser.add_argument(
        "--level",
        choices=LEVELS,
        default=None,
        help=(
            "Minimum severity level to include. Inclusive of the "
            "specified level and above (e.g. --level WARN shows "
            "WARN, ERROR, and FATAL)."
        ),
    )
    parser.add_argument(
        "--component",
        default=None,
        help="Filter by component name (case-insensitive).",
    )
    parser.add_argument(
        "--from",
        dest="time_from",
        type=_parse_timestamp,
        default=None,
        help="Only include entries at or after this timestamp (ISO 8601 UTC).",
    )
    parser.add_argument(
        "--to",
        dest="time_to",
        type=_parse_timestamp,
        default=None,
        help="Only include entries at or before this timestamp (ISO 8601 UTC).",
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--top",
        dest="top_n",
        type=int,
        default=None,
        help="Show the top N most frequent messages.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point.  Returns an exit code (0, 1, or 2)."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # --- Read and parse ---------------------------------------------------
    try:
        entries = parse_file(args.logfile)
    except FileNotFoundError:
        print(f"Error: file not found: {args.logfile}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        return 1

    if not entries:
        print("No valid log lines found in the file.", file=sys.stderr)
        return 2

    # --- Filter -----------------------------------------------------------
    filtered = filter_entries(
        entries,
        min_level=args.level,
        component=args.component,
        time_from=args.time_from,
        time_to=args.time_to,
    )

    if not filtered:
        print("No log lines match the given filters.", file=sys.stderr)
        return 2

    # --- Format and output ------------------------------------------------
    formatter = {
        "text": format_text,
        "json": format_json,
        "csv": format_csv,
    }[args.output_format]

    output = formatter(filtered, top_n=args.top_n)
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
