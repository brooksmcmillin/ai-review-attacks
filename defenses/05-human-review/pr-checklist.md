<!-- Drop into .github/PULL_REQUEST_TEMPLATE.md -->

## Reviewer checklist

If this PR touches any of the following, a human security reviewer must
approve. The AI reviewer's verdict does not satisfy this requirement.

- [ ] **Authentication** — middleware, session handling, token verification
- [ ] **Authorization** — role/permission checks, ownership checks, ACL logic
- [ ] **Cryptography** — signing, MAC, KDF, IV/nonce handling, comparisons
- [ ] **Network egress** — outbound HTTP, DNS lookups, redirects
- [ ] **Subprocess / shell** — anything that constructs a command line
- [ ] **AI instruction files** — `AGENTS.md`, `CLAUDE.md`, skill dirs, hooks
- [ ] **CI / branch protection** — workflow files, CODEOWNERS, settings

## What the AI reviewer is *not* asserting

When the AI bot leaves a green check, it is asserting "the text I read matches
patterns I associate with safe code." It is **not** asserting:

- That the code is correct at runtime
- That deployed configuration is correct
- That the threat model has been considered
- That assumptions about callers and callees still hold

Treat the AI verdict as a useful starting point for human review, not a
replacement for it.
