"""Tests for the log_parser module."""

from datetime import datetime, timezone

import pytest

import sys
import os

# Ensure the parent directory is on the path so we can import log_parser.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from log_parser import (
    LogEntry,
    filter_entries,
    level_at_or_above,
    parse_line,
)


# ------------------------------------------------------------------
# parse_line
# ------------------------------------------------------------------


class TestParseLine:
    """Tests for parsing individual log lines."""

    def test_parse_valid_line(self):
        entry = parse_line(
            "2026-04-15T08:23:01Z ERROR [auth] Failed login for user admin from 192.168.1.50"
        )
        assert entry is not None
        assert entry.timestamp == datetime(2026, 4, 15, 8, 23, 1, tzinfo=timezone.utc)
        assert entry.level == "ERROR"
        assert entry.component == "auth"
        assert entry.message == "Failed login for user admin from 192.168.1.50"

    def test_parse_debug_level(self):
        entry = parse_line(
            "2026-04-15T08:00:02Z DEBUG [cache] Cache warmed: 342 keys loaded"
        )
        assert entry is not None
        assert entry.level == "DEBUG"
        assert entry.component == "cache"

    def test_parse_fatal_level(self):
        entry = parse_line(
            "2026-04-15T09:15:33Z FATAL [scheduler] Unhandled exception in job"
        )
        assert entry is not None
        assert entry.level == "FATAL"

    def test_parse_empty_line_returns_none(self):
        assert parse_line("") is None
        assert parse_line("   ") is None

    def test_parse_malformed_line_returns_none(self):
        assert parse_line("not a valid log line") is None

    def test_parse_line_with_trailing_whitespace(self):
        entry = parse_line(
            "2026-04-15T08:00:01Z INFO [db] Connection pool initialized  \n"
        )
        assert entry is not None
        assert entry.level == "INFO"
        assert entry.component == "db"

    def test_timestamp_is_utc(self):
        entry = parse_line("2026-04-15T12:00:00Z INFO [api] Test")
        assert entry is not None
        assert entry.timestamp.tzinfo == timezone.utc


# ------------------------------------------------------------------
# level_at_or_above
# ------------------------------------------------------------------


class TestLevelAtOrAbove:
    """Tests for the level hierarchy helper."""

    def test_debug_includes_all(self):
        assert level_at_or_above("DEBUG") == [
            "DEBUG", "INFO", "WARN", "ERROR", "FATAL"
        ]

    def test_warn_includes_warn_error_fatal(self):
        assert level_at_or_above("WARN") == ["WARN", "ERROR", "FATAL"]

    def test_fatal_includes_only_fatal(self):
        assert level_at_or_above("FATAL") == ["FATAL"]

    def test_case_insensitive(self):
        assert level_at_or_above("error") == ["ERROR", "FATAL"]

    def test_invalid_level_raises(self):
        with pytest.raises(ValueError, match="Unknown level"):
            level_at_or_above("WARNING")


# ------------------------------------------------------------------
# filter_entries
# ------------------------------------------------------------------


def _make_entry(
    ts: str = "2026-04-15T08:00:00Z",
    level: str = "INFO",
    component: str = "api",
    message: str = "test",
) -> LogEntry:
    """Helper to create a LogEntry for tests."""
    dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return LogEntry(timestamp=dt, level=level, component=component, message=message)


@pytest.fixture()
def sample_entries() -> list[LogEntry]:
    """A small list of entries covering multiple levels and components."""
    return [
        _make_entry(ts="2026-04-15T08:00:00Z", level="DEBUG", component="cache"),
        _make_entry(ts="2026-04-15T08:05:00Z", level="INFO", component="api"),
        _make_entry(ts="2026-04-15T08:10:00Z", level="WARN", component="db"),
        _make_entry(ts="2026-04-15T08:15:00Z", level="ERROR", component="auth"),
        _make_entry(ts="2026-04-15T08:20:00Z", level="FATAL", component="scheduler"),
    ]


class TestFilterEntries:
    """Tests for filtering a list of entries."""

    def test_no_filters_returns_all(self, sample_entries):
        result = filter_entries(sample_entries)
        assert len(result) == 5

    def test_filter_by_min_level(self, sample_entries):
        result = filter_entries(sample_entries, min_level="WARN")
        assert len(result) == 3
        assert all(e.level in ("WARN", "ERROR", "FATAL") for e in result)

    def test_filter_by_component(self, sample_entries):
        result = filter_entries(sample_entries, component="auth")
        assert len(result) == 1
        assert result[0].component == "auth"

    def test_filter_by_component_case_insensitive(self, sample_entries):
        result = filter_entries(sample_entries, component="AUTH")
        assert len(result) == 1

    def test_filter_by_time_from(self, sample_entries):
        cutoff = datetime(2026, 4, 15, 8, 10, 0, tzinfo=timezone.utc)
        result = filter_entries(sample_entries, time_from=cutoff)
        assert len(result) == 3
        assert all(e.timestamp >= cutoff for e in result)

    def test_filter_by_time_to(self, sample_entries):
        cutoff = datetime(2026, 4, 15, 8, 10, 0, tzinfo=timezone.utc)
        result = filter_entries(sample_entries, time_to=cutoff)
        assert len(result) == 3
        assert all(e.timestamp <= cutoff for e in result)

    def test_filter_by_time_range(self, sample_entries):
        t_from = datetime(2026, 4, 15, 8, 5, 0, tzinfo=timezone.utc)
        t_to = datetime(2026, 4, 15, 8, 15, 0, tzinfo=timezone.utc)
        result = filter_entries(sample_entries, time_from=t_from, time_to=t_to)
        assert len(result) == 3

    def test_combined_filters(self, sample_entries):
        t_from = datetime(2026, 4, 15, 8, 0, 0, tzinfo=timezone.utc)
        result = filter_entries(
            sample_entries, min_level="ERROR", time_from=t_from
        )
        assert len(result) == 2
        assert all(e.level in ("ERROR", "FATAL") for e in result)

    def test_no_matches_returns_empty(self, sample_entries):
        result = filter_entries(sample_entries, component="nonexistent")
        assert result == []
