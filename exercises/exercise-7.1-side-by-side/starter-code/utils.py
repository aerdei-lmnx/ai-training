"""Data processing utilities.

This module provides the DataProcessor class for loading, filtering,
transforming, and exporting tabular data represented as lists of
dictionaries.

Example usage:

    dp = DataProcessor()
    data = dp.load_csv("sales.csv")
    filtered = dp.filter_rows(data, lambda row: row["region"] == "EMEA")
    dp.export_to_json(filtered, "emea_sales.json")
"""

from __future__ import annotations

import csv
import json
import statistics as stats_module
from collections import defaultdict
from datetime import date, datetime
from typing import Any, Callable


class DataProcessor:
    """Load, filter, transform, and export tabular data.

    Data is represented as ``list[dict[str, Any]]`` throughout -- each dict
    is one row, and the keys are column names.
    """

    # ------------------------------------------------------------------
    # Existing methods
    # ------------------------------------------------------------------

    def load_csv(self, filepath: str) -> list[dict[str, Any]]:
        """Load a CSV file and return its rows as a list of dicts.

        Args:
            filepath: Path to the CSV file.

        Returns:
            A list of dicts, one per row, keyed by the header names.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        with open(filepath, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            return list(reader)

    def filter_rows(
        self,
        data: list[dict[str, Any]],
        predicate: Callable[[dict[str, Any]], bool],
    ) -> list[dict[str, Any]]:
        """Return only the rows for which *predicate* returns True.

        Args:
            data: The dataset to filter.
            predicate: A callable that takes a row dict and returns a bool.

        Returns:
            A new list containing only the matching rows.

        Raises:
            TypeError: If *data* is not a list.
        """
        if not isinstance(data, list):
            raise TypeError(f"data must be a list, got {type(data).__name__}")
        return [row for row in data if predicate(row)]

    # ------------------------------------------------------------------
    # TODO: Implement the methods below based on feature-spec.md
    # ------------------------------------------------------------------

    # TODO: export_to_json
    #   - Export data to a JSON file with pretty printing
    #   - Handle date/datetime serialization
    #   - Validate that data is a list of dicts

    # TODO: calculate_statistics
    #   - Calculate mean, median, min, max, std_dev for numeric columns
    #   - Skip None/missing values
    #   - Use only the standard library

    # TODO: merge_datasets
    #   - Inner-join two datasets on a common key
    #   - Handle duplicate keys in dataset_b
    #   - Validate inputs
