# Exercise 2.1 - Context Detective

## Goal

Learn to spot when an AI is missing the context it needs to help you -- and how to fix it.

AI coding assistants like Claude Code start every conversation with a **blank slate**. They don't know your project, your tech stack, your bug, or what you've already tried. If you give a vague request, you'll get a vague (or wrong) answer. This exercise trains you to recognize that pattern and break out of it.

## Time

About 20 minutes.

## What You'll Need

- A text editor (or just pen and paper)
- Optionally: access to Claude Code to try your improved prompt at the end

## Instructions

### Part 1 - Read the broken interaction (~5 minutes)

Open `broken_interaction.md`. It contains a conversation between a developer and Claude Code. The developer asks for help fixing a bug. Read through the whole thing -- the developer's prompt AND the AI's response.

Notice how the AI's answer is generic and unhelpful. That's not because the AI is bad at coding. It's because the developer didn't give it enough information to work with.

### Part 2 - Find the missing context (~10 minutes)

Your job: figure out what went wrong. Identify **at least 3 pieces of context** the developer should have included but didn't.

For each one, write down:

1. **What** was missing (e.g., "the error message")
2. **Why** it matters (e.g., "without the error message, the AI has to guess what's broken")

Push yourself to find as many as you can. There are at least 5 significant pieces of missing context in this interaction.

### Part 3 - Rewrite the prompt (~5 minutes)

Now rewrite the developer's prompt so it includes all the context you identified. Imagine you are the developer and you have access to all the project details. Write the prompt you *wish* they had sent.

Don't worry about making it perfect. The point is to practice the habit of gathering context before asking for help.

### Part 4 - Check your work

Open `solution.md` to see the full list of missing context and an example rewritten prompt.

## Bonus

If you have access to Claude Code, try running your rewritten prompt (or the example one from the solution) and compare the quality of the response to the broken interaction. The difference is usually dramatic.

## Key Takeaway

The quality of help you get from an AI is directly tied to the quality of context you provide. A few extra minutes spent gathering error messages, relevant code, and project details will save you much more time in the long run.
