# Exercise 3.2 - Write Your AI Briefing (CLI)

**Goal:** Write a `CLAUDE.md` file for a CLI tool and observe how it improves the quality of AI-generated code.

**Time:** ~25 minutes

> This is a systems-focused alternative to Exercise 3.1. It covers the same concept -- writing a `CLAUDE.md` -- but uses a command-line log analyzer instead of a Flask web app. Complete whichever version fits your background; you do not need to do both.

## Background

A `CLAUDE.md` file gives Claude persistent context about your project -- its conventions, architecture, and the things a new developer would need to know before writing their first line of code. Without it, Claude has to guess. With it, Claude produces code that fits your project like it was written by a team member.

In this exercise you will explore a small CLI log analyzer, write a `CLAUDE.md` from scratch, and then test whether Claude Code produces better output when it has that context.

## The Sample Project

Inside `sample-log-analyzer/` you will find a Python CLI tool that analyzes application log files. It:

- Parses log lines in a specific format (`{ISO-8601-UTC} {LEVEL} [{component}] {message}`)
- Supports filtering by severity level, component, and time range
- Outputs summary statistics in text, JSON, or CSV format
- Has several project-specific conventions that are **not** obvious from the code alone

## Steps

### Step 1 -- Explore the Tool (~5 minutes)

Read through the files in `sample-log-analyzer/`. Run it against the sample log file:

```bash
cd sample-log-analyzer
python analyzer.py sample_logs/app.log
python analyzer.py sample_logs/app.log --level ERROR
python analyzer.py sample_logs/app.log --component auth --format json
python analyzer.py sample_logs/app.log --top 3
```

Pay attention to:

- The log line format and what each field means
- How severity levels are named and ordered
- How the output is formatted in each mode (text, JSON, CSV)
- What exit codes the tool uses
- How filtering works (especially `--level`)
- How the code is split across files

Take notes on anything a newcomer would need to know.

### Step 2 -- Write a CLAUDE.md (~10 minutes)

Create a file called `sample-log-analyzer/CLAUDE.md`. Choose your difficulty level:

**Bronze (recommended for first-timers):**
Copy `template-claude-md.md` into `sample-log-analyzer/CLAUDE.md` and fill in the blanks. The template has section headers and guiding questions -- just answer them based on what you saw in Step 1.

**Silver:**
Start from the template, fill it in, then add one extra section of your own (e.g. the exact regex pattern, how new formatters should be structured, or how the sample log file is organized).

**Gold:**
Write it from scratch with no template. Cover whatever you think matters.

No matter which level you pick, focus on **conventions Claude would get wrong without being told** -- things like exit codes, output format, the level hierarchy, and the `WARN` vs `WARNING` distinction.

Hint: Think about what you would tell a new developer on their first day. What would they get wrong without being told?

### Step 3 -- Test It With Claude Code (~7 minutes)

Ask Claude Code to add a new feature to the tool:

> Add a --watch flag that continuously monitors the log file for new lines (like tail -f) and prints matching entries in real time.

Try this **twice**:

1. First, temporarily rename or remove your `CLAUDE.md` and ask Claude Code to add the feature.
2. Then restore `CLAUDE.md` and ask the same question in a fresh conversation.

### Step 4 -- Compare the Results (~3 minutes)

Look at the two versions of the `--watch` implementation. Check whether each one:

- [ ] Uses exit code 2 when no matching lines are found (not exit code 1)
- [ ] Uses `WARN` (not `WARNING`) in any level comparisons
- [ ] Outputs matching lines in the correct format (tab-separated text by default)
- [ ] Handles the level hierarchy correctly (`--level WARN` includes WARN, ERROR, and FATAL)
- [ ] Keeps timestamps in UTC
- [ ] Expects component names to be lowercase

The version generated with `CLAUDE.md` present should match more of these criteria.

## When You Are Done

Compare your `CLAUDE.md` against `solution-claude-md.md` in this directory. There is no single correct answer -- the important thing is that your file captures the conventions that matter for code generation.

## Key Takeaways

- A good `CLAUDE.md` is a **briefing**, not documentation. Keep it concise and focused on what affects code generation.
- The most valuable things to include are **conventions that Claude would not guess** on its own (exit codes, output format, level naming, tab separation).
- CLI tools have different conventions than web apps -- exit codes, output formats, and flag behavior are the things that trip up AI assistants most often.
- Update your `CLAUDE.md` as your project evolves. Stale context is worse than no context.
