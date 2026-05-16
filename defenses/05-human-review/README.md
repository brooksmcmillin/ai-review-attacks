# Defense 05 — Meaningful Human Review

You can't review every line manually; that does not scale. You **can** keep
humans engaged where the AI has known blind spots. This directory is a
checklist + a sample CODEOWNERS pattern for high-risk paths.

- `pr-checklist.md` — copy/paste this into your `PULL_REQUEST_TEMPLATE.md`.
  It is short on purpose: any longer and reviewers skip it.
- `high-risk-paths.codeowners` — CODEOWNERS fragment that forces human review
  on auth / crypto / network / infrastructure code regardless of AI status.

## The blind spots this targets

- **Runtime behavior.** The AI sees text. It cannot reason about DNS resolution
  ordering (see attack 03), TOCTOU races, or anything that depends on the
  deployed environment.
- **Authorization logic.** Mid-complexity ACL checks where the bug is "this
  applies the right rule to the wrong resource."
- **Cryptographic correctness.** Timing-safe comparisons, IV reuse, signature
  malleability — easy to write, hard to spot in a diff.
- **Configuration semantics.** A YAML / Terraform diff that looks like a
  one-line change but flips a security boundary.

## What the AI review is good for

A surprisingly good first-pass triage: "did the author forget to handle the
None case here? Is this function shadowing a builtin? Does the new dependency
introduce a deprecated API call?" Use it as a checklist *augment* for the
human, not as a substitute.
