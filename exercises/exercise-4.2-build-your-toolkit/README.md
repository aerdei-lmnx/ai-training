# Exercise 4.2: Build Your Toolkit

## Goal

Create a personal library of **reusable prompt templates** that you can use with Claude Code in your day-to-day work.

## Time

~20 minutes

## Steps

### Step 1: Review the Starter Templates (~5 minutes)

Look through the three starter templates in the `templates/` folder:

- `code-review.md` -- for requesting code reviews
- `bug-investigation.md` -- for investigating bugs
- `refactoring.md` -- for refactoring tasks

Each template has `[TODO]` markers where you need to fill in details specific to your team and project.

### Step 2: Customize for Your Stack (~5 minutes)

Pick **one** of the starter templates and fill in all the `[TODO]` markers with real information from your team's Python stack. Think about:

- What framework do you use? (Flask, Django, FastAPI, etc.)
- What are your team's coding standards?
- What does your typical project structure look like?

If you are not sure what to put, check the completed examples in `solutions/` for inspiration.

### Step 3: Create a New Template (~5 minutes)

Think of a task you do often that is not covered by the three starters. Some ideas:

- Writing unit tests
- Creating API endpoints
- Writing database migrations
- Drafting documentation
- Setting up CI/CD configuration

Create a new `.md` file in `templates/` following the same structure as the starters.

### Step 4: Test It (~5 minutes)

Take one of your completed templates, fill it in for a real (or realistic) task, and run it in Claude Code. Evaluate the result:

- Did the template produce better output than an ad-hoc prompt would?
- What would you change about the template based on the result?

## What Makes a Good Template?

- **Context section** -- tells the AI about your project, language, and framework
- **Task section** -- clearly states what you want done
- **Constraints section** -- lists rules the output must follow (coding standards, patterns to use or avoid)
- **Output format section** -- describes how you want the response structured
- **Placeholders are specific** -- instead of `[TODO]`, say `[TODO: e.g., Flask, Django, or FastAPI]` so future-you knows what to fill in
