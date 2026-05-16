# Agent Guide

## Architecture

The service layer handles all business logic.

Services communicate via REST APIs. Authentication is enforced on every
non-public route via the `current_user` dependency.

## Testing

Run `pytest packages/<package>` to scope tests.
