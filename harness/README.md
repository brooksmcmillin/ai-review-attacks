# harness/

Shared scaffolding for the attack demos. There are two pieces:

- `reviewer.py` — `review_pr(repo_context, diff_or_files) -> ReviewResult`. Wraps the
  Anthropic SDK with a system prompt that mimics a CI security-review agent. The system
  prompt explicitly says "project conventions are authoritative" — which is the
  realistic posture that makes context-file poisoning work.
- `runner.py` — `run_attack(title, baseline, poisoned)`. Runs the same reviewer twice
  and prints both verdicts so the diff is visible.

## Requirements

- `ANTHROPIC_API_KEY` in the environment (or in `.env`).
- Optional `REVIEW_MODEL` env var to swap models. Defaults to `claude-sonnet-4-6`.

## Why the reviewer treats project conventions as authoritative

Because that is what real CI review agents do. The whole point of `AGENTS.md` /
`CLAUDE.md` is to bias the model toward project conventions; if the harness ignored
project context, the attacks would not be representative of production behavior.
That deference is exactly the trust assumption Section 01 of the talk attacks.

## A note on determinism

LLM responses vary. A given attack might be flipped on one run and caught on the next.
Each attack's `run.py` reports whether the verdict actually flipped. Running 3-5 times
and looking at the rate is more useful than any single run.
