# Defense 02: Security Invariant Tests

Assert security properties as **deterministic tests**, not as LLM analysis.
Tests are immune to prompt injection because they run as code; they fail-closed;
and they can't be talked out of finding what they find.

This directory has a working example:

- `example_app/`: a small FastAPI app with auth, some public endpoints, and
  a database helper.
- `tests/test_security_invariants.py`: two invariants:
  - **Every API route has an auth policy.** Routes are either authenticated
    (via the `current_user` dependency) or explicitly opted out via
    `@public_endpoint`. Anything else fails the test.
  - **No raw SQL.** Walks the source tree and asserts no f-string with a
    SQL verb embedded in it.

## Run

```bash
uv run pytest defenses/02-invariant-tests/
```

Both tests are currently passing. To see the failure mode, introduce either
violation (drop the auth dependency on a route, or write
`f"SELECT * FROM ..."` somewhere in `example_app/`) and run again.

## What invariant tests don't catch

Anything that **looks** auth'd but isn't (e.g., a `current_user` dependency that
silently returns `None`). Invariants check shape, not semantics. Layer them with
integration tests that exercise actual unauthenticated calls.
