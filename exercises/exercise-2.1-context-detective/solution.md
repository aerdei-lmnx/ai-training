# Solution - Context Detective

## The 5 Missing Pieces of Context

### 1. No project structure was provided

The developer never told the AI what kind of project this is or how it's organized. Is it a monolith? A microservice? Where do the route definitions live? Without this, the AI can't navigate the codebase or understand how the pieces connect.

**Why it matters:** An AI that knows "this is a Flask app with routes in `app/routes/orders.py` and models in `app/models/`" can give targeted advice. An AI that just hears "the API" has to guess at everything.

### 2. No error message was shared

The developer never included an error message, a traceback, or even the HTTP status code being returned. "Returning the wrong data" is not specific enough to diagnose anything.

**Why it matters:** Error messages are the single most useful piece of debugging context. They tell you (and the AI) exactly where the code is failing and often hint at why. Even if there's no explicit error (the endpoint returns 200 but with wrong data), describing the actual response you got is critical.

### 3. No mention of which endpoint or what the expected vs. actual behavior is

"The endpoint is returning the wrong data" could mean anything. Which endpoint? What URL? What data does it return right now? What *should* it return? The developer never spelled out any of this.

**Why it matters:** Debugging is about closing the gap between "what happens" and "what should happen." If you don't define both sides of that gap, nobody -- human or AI -- can help efficiently.

### 4. No mention of the tech stack (PostgreSQL + SQLAlchemy)

The AI had to guess the developer was using Python (and guessed correctly, based on the generic examples it gave). But it had no idea the project uses Flask, SQLAlchemy as the ORM (the library that talks to the database), or PostgreSQL as the database. The actual bug turned out to be a missing SQLAlchemy `.join()` call -- something the AI could have spotted immediately with the right context.

**Why it matters:** Different frameworks and tools have different common pitfalls. Knowing the tech stack lets the AI skip generic advice and jump straight to the patterns and mistakes that are relevant to *your* tools.

### 5. The developer didn't share the relevant code file

This is the big one. The developer asked the AI to "look at the code and fix it" but never actually provided the code. The AI can only work with what you show it. If you don't paste in the function, the AI is working blind.

**Why it matters:** An AI reading your actual code can spot the exact bug. An AI without your code can only list generic possibilities -- which is what happened here.

---

## Rewritten Prompt

Here is what the developer could have sent instead:

> I'm working on a Flask REST API using SQLAlchemy with a PostgreSQL database. The `/api/orders` endpoint is supposed to return a list of orders with their line items included, but right now it only returns the order data without any line items. The frontend team needs the line items nested inside each order object.
>
> There's no error -- the endpoint returns 200 OK, but the `line_items` array is empty for every order even though there's line item data in the database.
>
> Here's the relevant route handler in `app/routes/orders.py`:
>
> ```python
> @orders_bp.route('/api/orders', methods=['GET'])
> def get_orders():
>     orders = Order.query.filter_by(active=True).all()
>     return jsonify([order.to_dict() for order in orders])
> ```
>
> And here's the Order model in `app/models/order.py`:
>
> ```python
> class Order(db.Model):
>     __tablename__ = 'orders'
>     id = db.Column(db.Integer, primary_key=True)
>     customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
>     created_at = db.Column(db.DateTime, default=datetime.utcnow)
>     active = db.Column(db.Boolean, default=True)
>     line_items = db.relationship('LineItem', backref='order', lazy='select')
>
>     def to_dict(self):
>         return {
>             'id': self.id,
>             'customer_id': self.customer_id,
>             'created_at': self.created_at.isoformat(),
>             'line_items': [item.to_dict() for item in self.line_items]
>         }
> ```
>
> Can you help me figure out why the line items aren't being included?

With this prompt, the AI has everything it needs: the framework, the ORM, the database, the exact endpoint, the expected behavior, the actual behavior, and the relevant code. It can now give a precise, useful answer instead of a generic checklist.

---

## General Tips - Your "Context Checklist"

Before asking an AI for help with a bug, take 2 minutes to gather these:

- **Error message or traceback** -- Copy and paste the full error. If there's no error, describe the actual output you see.
- **Relevant code** -- Share the specific function, route handler, or file where the problem lives. You don't need to share the entire codebase, just the parts that matter.
- **Expected vs. actual behavior** -- "It should return X but instead it returns Y" is one of the most powerful sentences in debugging.
- **Tech stack details** -- Language, framework, database, key libraries. For example: "Python 3.11, Flask, SQLAlchemy, PostgreSQL."
- **What you've already tried** -- This prevents the AI from suggesting things you've already ruled out, saving everyone time.

None of these take long to gather, but together they transform a frustrating interaction into a productive one.
