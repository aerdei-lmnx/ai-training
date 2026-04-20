# Exercise 7.1: Side by Side

## Goal

Implement the same feature twice -- once using GitHub Copilot's inline suggestions and chat, and once using Claude Code -- to understand when each tool shines.

## Time

~20 minutes (roughly 8 minutes per round, plus comparison)

## Background

You have a Python utility module (`starter-code/utils.py`) with a `DataProcessor` class that already has two methods: `load_csv` and `filter_rows`. Your job is to add three new methods described in `feature-spec.md`. You will implement them twice using different tools, then compare the experience.

## Prerequisites

- VS Code with GitHub Copilot extension installed and active
- Claude Code installed and working
- Python 3.10+

## Setup

Make a backup copy of the starter code before you begin:

```bash
cp starter-code/utils.py starter-code/utils.py.backup
```

Read `feature-spec.md` carefully so you understand all three methods and their requirements before starting either round.

## Steps

### Step 1: Open the project

Open the `starter-code/` directory in VS Code. Open `utils.py` and read through the existing code and the TODO comments marking where the new methods should go.

### Step 2: ROUND 1 -- Copilot

Use GitHub Copilot to implement the three methods from `feature-spec.md`:

- Start typing each method signature and let Copilot suggest the body.
- Use Copilot Chat (Ctrl+I / Cmd+I) for more complex logic.
- Accept, reject, or edit suggestions as needed.

When done, save a copy of your result:

```bash
cp starter-code/utils.py starter-code/utils_copilot.py
```

### Step 3: Reset

Restore the original starter code:

```bash
cp starter-code/utils.py.backup starter-code/utils.py
```

### Step 4: ROUND 2 -- Claude Code

Open Claude Code in the `starter-code/` directory and ask it to implement the same three methods:

```
Read utils.py and feature-spec.md, then implement the three new methods
(export_to_json, calculate_statistics, merge_datasets) following the
requirements in the feature spec. Keep all existing code intact.
```

When done, save a copy of your result:

```bash
cp starter-code/utils.py starter-code/utils_claude.py
```

### Step 5: Compare

Open `comparison-worksheet.md` and fill in the table based on your experience. Use the reflection questions to guide a discussion with your group or think through the tradeoffs on your own.

Optionally, diff the two implementations:

```bash
diff starter-code/utils_copilot.py starter-code/utils_claude.py
```

## Discussion

After completing the worksheet, consider these questions with your group:

- Which tool felt faster for writing individual methods?
- Which tool produced more complete error handling without extra prompting?
- Did either tool need more guidance or corrections?
- How did the quality of docstrings and type hints compare?
- In your day-to-day work, when would you reach for each tool?
