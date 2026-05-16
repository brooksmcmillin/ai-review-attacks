# Defense 03 — Separate Security Rules from LLM Context

The rules an attacker can rewrite in a PR are not the rules that should
enforce your security policy. Move the real enforcement into CI scripts and
workflows that live under `CODEOWNERS` protection — and don't rely on the
AI reviewer to enforce policy.

## Files here

- `ci/check-http-timeouts.sh` — a deterministic grep-based check that fails CI
  if `requests.get(...)` or `httpx.get(...)` calls don't set a timeout.
- `ci/check-no-shell-true.sh` — fails CI if any `subprocess.*(shell=True)`
  call ships with user-controllable input.
- `.github/workflows/security.yml` — runs both scripts on every PR. The
  workflow file itself is under `CODEOWNERS` (see defense 01).

## Why this beats AGENTS.md

The rule "no `shell=True` on user input" can live in three places:

1. **`AGENTS.md`**, where any PR can modify it.
2. **An AI reviewer's system prompt**, where the *PR diff* can influence it.
3. **A CI script under CODEOWNERS**, where neither the PR nor the AI can touch
   it without going through human security review.

Only (3) survives an adversarial PR. (1) and (2) are useful as soft signals —
they help with the legitimate case where someone forgot — but they aren't
load-bearing.
