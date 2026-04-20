# Scoring Rubric

Use this rubric to vote on which prompt produced the better output.

---

## Criteria

| Category | Weight | What to look for |
|---|---|---|
| **Correctness** | 40% | Does the code actually work? Would it pass reasonable tests? Does it handle the stated requirements? |
| **Code Quality** | 30% | Is the code clean and readable? Does it follow Python conventions (PEP 8)? Are variable names descriptive? Is it well-organized? |
| **Completeness** | 20% | Does it handle edge cases? Does it include error handling where appropriate? Are there type hints and docstrings? |
| **Explanation** | 10% (bonus) | Did the AI explain its choices? Did it call out trade-offs, assumptions, or design decisions? |

---

## How to Score

For each category, rate the output on a scale of 1 to 5:

- **5** -- Excellent. Nothing meaningful to improve.
- **4** -- Good. Minor issues only.
- **3** -- Acceptable. Works but has clear room for improvement.
- **2** -- Below average. Missing important elements or has noticeable problems.
- **1** -- Poor. Does not meet the requirement.

Multiply each rating by the category weight, then add them up. Highest total score wins.

**Example:** An output that scores Correctness=4, Quality=5, Completeness=3, Explanation=4 would get:

> (4 x 0.40) + (5 x 0.30) + (3 x 0.20) + (4 x 0.10) = 1.6 + 1.5 + 0.6 + 0.4 = **4.1 / 5.0**

---

## Discussion Prompts

After voting, talk through these questions as a group:

1. **What made the winning prompt better?** Was it more specific? Did it include examples? Did it set constraints?
2. **What context did it provide?** Did the prompt mention edge cases, coding style, or expected output format?
3. **Did iteration help?** For people who revised their prompts, what changed between versions and did the output improve?
4. **What was left out?** Was there anything the losing prompt assumed the AI would "just know" that it did not?
5. **Would you reuse the winning prompt?** Could you turn it into a template for similar tasks in the future?
