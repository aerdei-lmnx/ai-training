# Broken Interaction

Below is a realistic conversation between a developer and Claude Code. Read through it carefully. Something is very wrong with how the developer asked for help -- and it shows in the answer they got back.

---

## The Developer's Prompt

> Fix the bug in the API. The endpoint is returning the wrong data and my frontend team is blocked. This needs to be fixed ASAP.

---

## Claude Code's Response

> I'd be happy to help fix the API bug. Here are some common issues that could cause an endpoint to return wrong data:
>
> **1. Check your route handlers**
>
> Make sure the correct handler function is mapped to the endpoint your frontend is calling. A common mistake is having two similar routes where the wrong one matches first.
>
> ```python
> # Example: make sure routes don't overlap
> @app.route('/api/users')
> def get_users():
>     # ...
>
> @app.route('/api/users/<id>')
> def get_user(id):
>     # ...
> ```
>
> **2. Verify your data serialization**
>
> If you're converting database objects to JSON, check that your serialization logic includes all the required fields and formats them correctly.
>
> ```python
> # Make sure you're returning all needed fields
> def serialize_user(user):
>     return {
>         'id': user.id,
>         'name': user.name,
>         'email': user.email
>     }
> ```
>
> **3. Check your database query**
>
> The query might be filtering incorrectly or returning stale data. Verify that your query matches what the endpoint should return.
>
> ```python
> # Double-check your query filters
> users = User.query.filter_by(active=True).all()
> ```
>
> **4. Look at your response format**
>
> Make sure the JSON structure matches what the frontend expects. A common issue is nesting data differently than the frontend anticipates.
>
> Could you share more details about which endpoint is affected and what data it's returning vs. what you expect? That would help me give you a more specific fix.

---

## What Happened Next

The developer replied:

> That didn't help at all. I already checked the routes. Can you just look at the code and fix it?

And Claude Code responded:

> I don't have access to your code files yet. Could you share the relevant source file and the error you're seeing? That way I can give you a specific fix instead of general suggestions.

---

The developer gave up and spent another 2 hours debugging on their own before finding the issue: a SQLAlchemy query in the `/api/orders` endpoint was missing a `.join()` call, so it was returning orders without their associated line items. The fix was a single line of code.

---

## Example 2: The Vague Prompt That Got a Wrong Fix

Later, the same developer tried again -- this time with an AI agent that could read the project files directly. They gave it the same vague prompt:

> Fix the bug in the API. The endpoint is returning the wrong data and my frontend team is blocked. This needs to be fixed ASAP.

The AI explored the codebase, and within a minute it announced it had found the bug. It pointed to a comment in `routes/orders.py` that said:

```python
# NOTE: Previously used joinedload here but removed for performance - see ticket ORD-142
```

The AI added `joinedload(Order.line_items)` to the query in the route handler. The endpoint started returning line items. Bug fixed, right?

**Not quite.** The *real* problem was in `models/order.py`, where the Order model's relationship was defined as:

```python
line_items = db.relationship("LineItem", backref="order", lazy="noload")
```

The `lazy="noload"` setting means line items are *never* loaded unless you explicitly ask for them. The AI's fix (adding `joinedload` to one query) was a band-aid -- it fixed the `/api/orders` endpoint, but every *other* place in the codebase that calls `order.to_dict()` would still get empty line items.

The root cause fix was changing `lazy="noload"` to `lazy="select"` in the model definition -- a one-line change that fixes the problem everywhere.

### Why did this happen?

The AI had no context about *which* endpoint was broken or *what* "wrong data" meant. So it explored the whole codebase, got pulled toward the most suspicious-looking clue (a comment about removing `joinedload`), and applied a fix there. It found *a* fix, but not *the* fix.

**The lesson:** Context doesn't just help the AI find bugs *faster* -- it helps it find the *right* fix. A specific prompt mentioning "the Order model's line_items relationship" would have pointed the AI straight to `models/order.py` instead of the red herring in the route handler.
