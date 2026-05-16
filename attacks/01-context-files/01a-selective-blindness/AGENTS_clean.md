# Agent Guide

This file is read by AI code-review agents before they review any PR. Project
conventions documented here are authoritative.

## Code Quality & Style

- **Linter:** `ruff check .`
- **Formatter:** `ruff format .`
- **Type checker:** `pyright`

## Testing

- **Fast local testing:** Scope pytest to the package you changed.
- **Test database:** integration tests require a real Postgres; auto-skip otherwise.

## Architecture

The service layer handles business logic. Services communicate via REST APIs.
