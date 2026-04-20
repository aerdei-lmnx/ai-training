# Coding Tasks for Prompt Battle

Pick one of the three tasks below. Each person writes their own prompt for the same task, then both run their prompts in Claude Code and compare results.

---

## Task 1: Easy -- Email Address Validator

Write a Python function that validates email addresses.

**Requirements:**
- The function should accept a string and return `True` if it is a valid email address, `False` otherwise.
- It should handle common edge cases:
  - Missing `@` symbol
  - Multiple `@` symbols
  - Missing local part (the bit before `@`)
  - Missing domain part (the bit after `@`)
  - Domain without a dot (e.g., `user@localhost` is invalid for this exercise)
  - Consecutive dots in the domain (e.g., `user@example..com`)
  - Leading or trailing dots in the local part
  - Spaces anywhere in the address

---

## Task 2: Medium -- Refactor a Messy Function

The function below works, but it is poorly written. Refactor it into clean, well-structured Python code.

Your refactored version must produce the same output for the same input.

```python
def process_data(f):
    result = []
    lines = open(f).readlines()
    for i in range(len(lines)):
        if i == 0:
            continue
        line = lines[i].strip()
        if line == "":
            continue
        parts = line.split(",")
        if len(parts) >= 4:
            name = parts[0]
            age = parts[1]
            score = parts[2]
            status = parts[3]
            if int(age) >= 18:
                if float(score) >= 70.0:
                    if status == "active":
                        d = {}
                        d["name"] = name.strip()
                        d["age"] = int(age)
                        d["score"] = float(score)
                        d["status"] = status
                        d["grade"] = ""
                        if float(score) >= 90:
                            d["grade"] = "A"
                        elif float(score) >= 80:
                            d["grade"] = "B"
                        elif float(score) >= 70:
                            d["grade"] = "C"
                        d["is_senior"] = False
                        if int(age) >= 65:
                            d["is_senior"] = True
                        result.append(d)
    return result
```

**What is wrong with this function:**
- Opens a file but never closes it (no context manager)
- No error handling at all (what if the file does not exist? what if `age` is not a number?)
- Deeply nested `if` statements that are hard to follow
- Magic numbers everywhere (`18`, `70.0`, `90`, `80`, `65`) with no explanation
- Converts the same values to `int`/`float` multiple times
- Uses `range(len(...))` instead of iterating directly
- Single-letter variable names (`f`, `d`, `i`)
- No docstring, no type hints

---

## Task 3: Hard -- Rate Limiting Middleware for Flask

Add rate limiting middleware to a Flask application.

**Requirements:**
- Support **per-endpoint** rate limits (e.g., `/api/search` allows 10 requests/minute, `/api/upload` allows 5 requests/minute)
- Use **Redis** for distributed request counting (so the rate limiter works across multiple app instances)
- Return proper **HTTP 429 Too Many Requests** responses when a client exceeds the limit
- Include a **Retry-After** header in 429 responses telling the client how many seconds to wait
- Identify clients by IP address
- Provide a way to configure rate limits via a decorator or configuration dictionary
- Include basic logging so operators can see when rate limits are hit
