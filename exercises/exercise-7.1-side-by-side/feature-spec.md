# Feature Spec: DataProcessor New Methods

## Overview

Add three new methods to the `DataProcessor` class in `utils.py`. Each method must include type hints, a docstring, and proper error handling as described below.

---

## Method 1: export_to_json

```python
def export_to_json(self, data: list[dict], filepath: str) -> None:
```

Export processed data to a JSON file with pretty printing.

### Requirements

- Write `data` to the file at `filepath` as JSON.
- Use 2-space indentation for readability.
- Handle date and datetime objects during serialization: convert them to ISO 8601 strings (e.g., `"2026-04-20"` or `"2026-04-20T14:30:00"`). Do NOT fail on date objects.
- Raise `TypeError` with a descriptive message if `data` is not a list.
- Raise `TypeError` if any element in `data` is not a dict.
- Let file I/O exceptions (e.g., `PermissionError`, `FileNotFoundError` for bad directory) propagate naturally -- do not swallow them.

### Example

```python
dp = DataProcessor()
data = [
    {"name": "Alice", "joined": date(2026, 1, 15)},
    {"name": "Bob", "joined": date(2026, 3, 22)},
]
dp.export_to_json(data, "output.json")
# output.json contains pretty-printed JSON with dates as strings
```

---

## Method 2: calculate_statistics

```python
def calculate_statistics(self, data: list[dict], columns: list[str]) -> dict[str, dict[str, float]]:
```

Calculate descriptive statistics for specified numeric columns.

### Requirements

- For each column name in `columns`, compute the following across all rows in `data`:
  - `mean` -- arithmetic average
  - `median` -- middle value (average of two middle values for even-length lists)
  - `min` -- minimum value
  - `max` -- maximum value
  - `std_dev` -- population standard deviation (not sample)
- Return a dict mapping each column name to its statistics dict, e.g.:
  ```python
  {
      "age": {"mean": 30.0, "median": 28.5, "min": 22.0, "max": 45.0, "std_dev": 7.5},
      "salary": {"mean": 65000.0, ...}
  }
  ```
- Skip rows where the column value is `None` or missing (i.e., the key does not exist in that row). Only use rows that have a numeric value for that column.
- Raise `ValueError` with a descriptive message if, after skipping, a column has zero valid numeric values.
- Raise `TypeError` if `data` is not a list or `columns` is not a list.
- Use only the Python standard library (no NumPy/pandas). The `statistics` module is allowed.

### Example

```python
dp = DataProcessor()
data = [
    {"name": "Alice", "age": 30, "score": 88},
    {"name": "Bob", "age": 25, "score": 92},
    {"name": "Carol", "age": 35, "score": None},
]
result = dp.calculate_statistics(data, ["age", "score"])
# result["age"]["mean"] == 30.0
# result["score"]["mean"] == 90.0  (None was skipped)
```

---

## Method 3: merge_datasets

```python
def merge_datasets(self, dataset_a: list[dict], dataset_b: list[dict], key: str) -> list[dict]:
```

Merge two lists of dicts on a common key, similar to a SQL inner join.

### Requirements

- For each row in `dataset_a` that has a matching value in `dataset_b` for `key`, produce a merged row containing all fields from both.
- If both datasets have a non-key field with the same name, the value from `dataset_b` takes precedence (overwrites `dataset_a`).
- Rows in `dataset_a` without a match in `dataset_b` are excluded (inner join behavior).
- Rows in `dataset_b` without a match in `dataset_a` are excluded.
- If multiple rows in `dataset_b` share the same key value, each matching `dataset_a` row should be merged with each of them (producing multiple output rows, like a true inner join).
- Raise `ValueError` with a descriptive message if `key` is an empty string.
- Raise `TypeError` if `dataset_a` or `dataset_b` is not a list.
- Preserve the order of `dataset_a` rows in the output.

### Example

```python
dp = DataProcessor()
employees = [
    {"id": 1, "name": "Alice", "dept_id": 10},
    {"id": 2, "name": "Bob", "dept_id": 20},
    {"id": 3, "name": "Carol", "dept_id": 30},
]
departments = [
    {"dept_id": 10, "dept_name": "Engineering"},
    {"dept_id": 20, "dept_name": "Marketing"},
]
result = dp.merge_datasets(employees, departments, "dept_id")
# result == [
#     {"id": 1, "name": "Alice", "dept_id": 10, "dept_name": "Engineering"},
#     {"id": 2, "name": "Bob", "dept_id": 20, "dept_name": "Marketing"},
# ]
# Carol is excluded because dept_id 30 has no match.
```
