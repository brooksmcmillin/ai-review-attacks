# ai-review-attacks

Companion repo for **Poisoning the Safety Net: Attacking AI-Powered Code Review Pipelines**.

Slides: https://slides.brooksmcmillin.com/poisoning.html

Every attack from the slides has a matching directory here with the files shown
in the talk, plus a runnable harness that tests the attack against a real
model. Every defense has working sample code you can copy.

> **Educational use only.** Everything under `attacks/` is intentionally vulnerable or
> malicious. Do not deploy any of it.

## Layout

```
attacks/
  01-context-files/        AGENTS.md / CLAUDE.md poisoning
  02-review-manipulation/  prompt injection through the PR diff
  03-trust-boundary/       passes CI, still vulnerable (DNS-rebinding SSRF)
  04-runtime-compromise/   MCP descriptions, tool output, supply-chain instructions

defenses/
  01-codeowners/           protect AI-instruction files like CI config
  02-invariant-tests/      deterministic pytest assertions (auth policy, no raw SQL)
  03-separated-rules/      security policy lives in CI, not in AGENTS.md
  04-architectural/        read-only review, immutable rules, separated context
  05-human-review/         where humans must stay in the loop
  06-runtime-hardening/    pin MCP tools, sanitize tool output

harness/                   shared Anthropic-API "reviewer" used by attack run.py scripts
scripts/run-all-demos.sh   run every attack harness end-to-end
```

Each subdirectory has its own `README.md` describing the attack/defense and how to
reproduce it.

## Setup

```bash
uv sync --extra dev
cp .env.example .env   # fill in ANTHROPIC_API_KEY
```

Python 3.13 + uv. The harness uses the Anthropic SDK directly so it has no monorepo
dependencies.

## Running an attack

```bash
# Run one category (recommended starting point)
uv run python attacks/01-context-files/run.py

# Run everything
./scripts/run-all-demos.sh
```

Each `run.py` runs the attack twice: once with clean baseline context, once with
the poisoned variant. It prints the model verdicts side by side so you can see
the review flip.

## Running the defenses

```bash
# Pytest invariants (defense 02) and tool-output sanitizer tests (defense 06)
uv run pytest

# Inspect a CODEOWNERS template
cat defenses/01-codeowners/CODEOWNERS
```

## Mapping slides to demos

| Slide attack    | Path                                                  |
|-----------------|-------------------------------------------------------|
| 01a Selective blindness     | `attacks/01-context-files/01a-selective-blindness/` |
| 01b Hidden instructions     | `attacks/01-context-files/01b-hidden-instructions/` |
| 02a Comment injection       | `attacks/02-review-manipulation/02a-comment-injection/` |
| 02b String-literal injection| `attacks/02-review-manipulation/02b-string-literal-injection/` |
| 02c Context overflow        | `attacks/02-review-manipulation/02c-context-overflow/` |
| 03a Passing every check     | `attacks/03-trust-boundary/` |
| 04a MCP description injection | `attacks/04-runtime-compromise/04a-mcp-description-injection/` |
| 04b Tool output injection   | `attacks/04-runtime-compromise/04b-tool-output-injection/` |
| 04c Supply chain            | `attacks/04-runtime-compromise/04c-supply-chain/` |

| Slide defense | Path |
|---------------|------|
| Protect context files like CI config | `defenses/01-codeowners/` |
| Security invariant tests             | `defenses/02-invariant-tests/` |
| Separate security rules from LLM     | `defenses/03-separated-rules/` |
| Architectural defenses for reviewers | `defenses/04-architectural/` |
| Meaningful human review              | `defenses/05-human-review/` |
| Harden the agent runtime             | `defenses/06-runtime-hardening/` |

## A note on reproducibility

LLM behavior is non-deterministic. Each attack here reliably reproduced against
`claude-sonnet-4-6` at the time of recording, but model updates change results.
Sometimes the model now catches an attack the slides claim it misses. That is
also a useful data point. The harness prints the model verdict on every run so
you can see what your model actually does.
