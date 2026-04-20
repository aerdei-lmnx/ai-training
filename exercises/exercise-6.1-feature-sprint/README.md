# Exercise 6.1: Feature Sprint

## Goal

Use Claude Code's full toolkit -- plan mode, slash commands, and CLAUDE.md -- to implement a complete feature in an existing codebase.

## Time

~25 minutes

## Background

You have a working Task Management REST API built with Flask and SQLAlchemy. Your job is to implement a new feature described in `feature-spec.md` using Claude Code as your AI pair programmer. This time, instead of writing code by hand, you will leverage Claude Code's planning and implementation workflow.

## Prerequisites

- Claude Code installed and working
- Python 3.10+ with pip
- Familiarity with REST APIs (from earlier exercises)

## Setup

1. Navigate to the `sample-project/` directory.
2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Verify the existing tests pass:

   ```bash
   python -m pytest tests/ -v
   ```

## Steps

### Step 1: Explore the project

Open the project in your editor and read `CLAUDE.md`. This file tells Claude Code (and you) everything about the project's conventions, how to run it, and what standards to follow.

Browse through `app.py`, `models.py`, and `tests/test_app.py` to understand the existing code.

### Step 2: Read the feature spec

Open `../feature-spec.md` (one level up from `sample-project/`). This describes exactly what you need to implement.

### Step 3: Plan with Claude Code

Start Claude Code in the `sample-project/` directory and use the `/plan` slash command:

```
/plan Read feature-spec.md and plan how to implement the two new endpoints described there. Follow all conventions in CLAUDE.md.
```

Claude Code will analyze the codebase and the feature spec, then produce a step-by-step implementation plan.

### Step 4: Review the plan

Read through Claude Code's plan carefully. Check that it:

- Identifies both endpoints (DELETE and stats)
- Plans to add tests for both
- Follows the conventions from CLAUDE.md
- Uses proper HTTP status codes

If the plan looks good, approve it so Claude Code begins implementation.

### Step 5: Let Claude Code implement

Watch as Claude Code makes the changes. It should modify `app.py` and `tests/test_app.py` at minimum.

### Step 6: Run the tests

Verify everything works:

```bash
python -m pytest tests/ -v
```

All tests -- both old and new -- should pass.

### Step 7: Review the code

Use the `/review` slash command to have Claude Code review its own work:

```
/review
```

Check that the review covers code quality, test coverage, and adherence to the project conventions.

## Tips

- If Claude Code goes off track, use `/clear` and try a more specific prompt.
- You can ask Claude Code to explain any part of the plan before approving.
- If tests fail, paste the error output to Claude Code and ask it to fix the issue.
- The CLAUDE.md file is important -- it shapes how Claude Code approaches the task. Read it yourself so you know what to expect.

## Discussion Questions

1. How did the plan compare to how you would have approached the feature yourself?
2. Did Claude Code follow the conventions in CLAUDE.md?
3. What would happen if CLAUDE.md had different or conflicting conventions?
4. How much time did planning save compared to jumping straight into implementation?
