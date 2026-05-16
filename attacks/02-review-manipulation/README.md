# 02: Manipulating AI Review Agents

Even with a clean `AGENTS.md`, the PR diff itself is attacker-controlled text that the
reviewer processes as input. Comments, docstrings, string literals, and file
count can all shift the review.

- `02a-comment-injection/`: a docstring asserts the code has already passed security
  review. The code below it has an SSRF.
- `02b-string-literal-injection/`: a config constant's value reads as an
  instruction to the reviewer. Less reliable than comments, harder to notice.
- `02c-context-overflow/`: a large PR (auto-generated lockfile churn, test
  refactors, doc edits) buries the security-critical change.

## Run it

```bash
uv run python attacks/02-review-manipulation/run.py
```
