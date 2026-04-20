# Exercise 3.1 - Write Your AI Briefing

**Goal:** Write a `CLAUDE.md` file for a Flask project and observe how it improves the quality of AI-generated code.

**Time:** ~25 minutes

## Background

A `CLAUDE.md` file gives Claude persistent context about your project -- its conventions, architecture, and the things a new developer would need to know before writing their first line of code. Without it, Claude has to guess. With it, Claude produces code that fits your project like it was written by a team member.

In this exercise you will explore a small Flask REST API, write a `CLAUDE.md` from scratch, and then test whether Claude Code produces better output when it has that context.

## The Sample Project

Inside `sample-flask-app/` you will find a bookstore REST API with:

- CRUD endpoints for books (`GET`, `POST`, `DELETE`)
- SQLAlchemy models with SQLite storage
- Pytest-based tests
- Several project-specific conventions that are **not** obvious from the code alone

## Steps

### Step 1 -- Explore the Sample App (~5 minutes)

Read through the files in `sample-flask-app/`. Pay attention to:

- How responses are structured
- How dates are formatted
- How errors are handled
- How endpoints are named
- How pagination works
- How tests are organized

Take notes on anything a newcomer would need to know.

### Step 2 -- Write a CLAUDE.md (~10 minutes)

Create a file called `sample-flask-app/CLAUDE.md`. Choose your difficulty level:

**Bronze (recommended for first-timers):**
Copy `template-claude-md.md` into `sample-flask-app/CLAUDE.md` and fill in the blanks. The template has section headers and guiding questions -- just answer them based on what you saw in Step 1.

**Silver:**
Start from the template, fill it in, then add one extra section of your own (e.g. pagination details, testing patterns, or anything else you noticed).

**Gold:**
Write it from scratch with no template. Cover whatever you think matters.

No matter which level you pick, focus on **conventions Claude would get wrong without being told** -- things like response format, date handling, and naming patterns.

Hint: Think about what you would tell a new developer on their first day. What would they get wrong without being told?

### Step 3 -- Test It With Claude Code (~7 minutes)

Ask Claude Code to add a new feature to the app:

> Add a PUT /books/<id> endpoint for updating a book. Follow all existing project conventions.

Try this **twice**:

1. First, temporarily rename or remove your `CLAUDE.md` and ask Claude Code to add the endpoint.
2. Then restore `CLAUDE.md` and ask the same question in a fresh conversation.

### Step 4 -- Compare the Results (~3 minutes)

Look at the two versions of the PUT endpoint. Check whether each one:

- [ ] Uses the `{"data": ..., "error": ...}` response wrapper
- [ ] Returns ISO 8601 formatted dates
- [ ] Uses snake_case in the URL
- [ ] Handles the 404 case with the custom error format
- [ ] Updates the `updated_at` timestamp
- [ ] Includes a test

The version generated with `CLAUDE.md` present should match more of these criteria.

## When You Are Done

Compare your `CLAUDE.md` against `solution-claude-md.md` in this directory. There is no single correct answer -- the important thing is that your file captures the conventions that matter for code generation.

## Key Takeaways

- A good `CLAUDE.md` is a **briefing**, not documentation. Keep it concise and focused on what affects code generation.
- The most valuable things to include are **conventions that Claude would not guess** on its own (response formats, naming schemes, testing patterns).
- Update your `CLAUDE.md` as your project evolves. Stale context is worse than no context.
