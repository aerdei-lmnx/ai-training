# Feature Spec: Task Deletion and Statistics

## Overview

Add two new endpoints to the Task Management API: one for deleting tasks and one for retrieving task statistics.

## Endpoint 1: DELETE /tasks/<id>

Delete a task by its ID.

**Request:**
- Method: DELETE
- URL: `/tasks/<id>` where `<id>` is an integer task ID

**Response (success):**
- Status: 204 No Content
- Body: empty

**Response (not found):**
- Status: 404 Not Found
- Body:
  ```json
  {
    "error": "Task not found"
  }
  ```

**Requirements:**
- The task must be permanently removed from the database.
- Return 404 if the task does not exist.

## Endpoint 2: GET /tasks/stats

Return aggregate counts of tasks grouped by status.

**Request:**
- Method: GET
- URL: `/tasks/stats`

**Response (success):**
- Status: 200 OK
- Body:
  ```json
  {
    "data": {
      "pending": 3,
      "in_progress": 2,
      "done": 5,
      "total": 10
    }
  }
  ```

**Requirements:**
- Count all tasks grouped by their `status` field.
- Always include all three status keys (`pending`, `in_progress`, `done`) even if their count is zero.
- The `total` field must equal the sum of the three status counts.
- If there are no tasks at all, return all counts as zero.

## Testing Requirements

Both endpoints must have thorough test coverage:

- **DELETE endpoint tests:**
  - Successfully delete an existing task (expect 204)
  - Attempt to delete a non-existent task (expect 404)
  - Verify the task is actually removed after deletion (GET should return 404)

- **Stats endpoint tests:**
  - Stats with no tasks (all zeros)
  - Stats with tasks in various statuses
  - Verify total equals sum of individual counts
