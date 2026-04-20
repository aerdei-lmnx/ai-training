# Module 1 Live Demo - Bookstore API

A Flask bookstore API with **two bugs** for the Module 1 "wow factor" demo. The audience sees the bugs live in a browser, then watches Claude Code find and fix them in under 2 minutes.

## Setup (do this before the training)

```bash
cd demos/module-1-live-demo
pip install -r requirements.txt
python app.py
```

The server runs on `http://localhost:5002`.

## Demo Script

### Step 1: Show the app works (30 seconds)

Open a browser and show these working endpoints:

- `http://localhost:5002/books` -- returns 3 books (works fine)
- `http://localhost:5002/books/1` -- returns one book (works fine)
- `http://localhost:5002/books/search?q=clean` -- search works

### Step 2: Show the bugs (30 seconds)

Now show the broken parts:

- `http://localhost:5002/books?in_stock=true` -- **returns empty array** even though 2 books are in stock. The filter is broken.
- `http://localhost:5002/books/stats` -- **500 Internal Server Error** when DB is empty (or show the test failure)

Then run the tests to make the failures visible:

```bash
pytest -v
```

Point out: **3 tests failing, 9 passing.** Two distinct bugs.

### Step 3: Let Claude Code fix it (60 seconds)

Open a new terminal in the `module-1-live-demo/` directory:

```bash
claude
```

Prompt:

> The bookstore API has two bugs. First, GET /books?in_stock=true returns an empty list even though there are books in stock. Second, GET /books/stats crashes with a 500 error when the database is empty. Fix both bugs and make sure all tests pass.

Let the audience watch Claude Code read the files, find both bugs, and fix them.

### Step 4: Verify the fix (30 seconds)

```bash
pytest -v
```

All 12 tests should pass. Refresh the browser endpoints to show they work.

### Step 5: Debrief (30 seconds)

Key points to make:
- "That took Claude about 60 seconds. How long would it take you?"
- "Notice I gave it specific details: which endpoints, what the symptoms were"
- "We'll learn WHY that specificity matters in Module 2"

## The Bugs (for your reference)

**Bug 1: String/boolean mismatch in filter** (`app.py` around line 87)

`request.args.get("in_stock")` returns the string `"true"`, but `filter_by(in_stock="true")` compares against a boolean column. The string never matches, so zero results come back.

**Bug 2: Division by zero in stats** (`app.py` around line 152)

`avg_price = sum(prices) / len(prices)` crashes when the books table is empty because `len(prices)` is 0.

## Resetting for the demo

If you need to reset after a practice run:

```bash
git checkout -- app.py
rm -f instance/bookstore.db
```
