# Bug Investigation Prompt Template

## Context

Project: [TODO: your project name]
Language: Python
Framework: [TODO: your framework, e.g., Flask, Django, FastAPI]
Environment: [TODO: where the bug occurs, e.g., "production on AWS", "local dev", "staging"]

## Bug Description

**What should happen:**
[TODO: describe the expected behavior]

**What actually happens:**
[TODO: describe the actual behavior, including any error messages]

**Steps to reproduce:**
1. [TODO: step 1]
2. [TODO: step 2]
3. [TODO: step 3]

## What I Have Already Tried

- [TODO: list what you have already investigated or ruled out]

## Error Output / Logs

```
[TODO: paste relevant error messages, stack traces, or log output here]
```

## Relevant Files

- [TODO: list the files you think are involved, e.g., "app/routes/users.py"]
- [TODO: e.g., "app/models/user.py"]

## Constraints

- [TODO: any constraints on the fix, e.g., "do not change the public API"]
- [TODO: e.g., "fix must be backward-compatible"]
- [TODO: e.g., "we cannot upgrade the database schema right now"]

## Output Format

[TODO: describe what you want back, e.g.,
"Explain the likely root cause, suggest a fix with code, and list any
tests I should add to prevent regression."]
