"""Auth dependency + the public-endpoint marker.

The invariant test uses `current_user.__name__` for identity, so we keep it as
a plain function (FastAPI dependency injection accepts any callable).
"""

from __future__ import annotations

from fastapi import Header, HTTPException


def current_user(authorization: str = Header(default="")) -> str:
    """Resolve the caller's user id from a bearer token."""
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401)
    if token == "invalid":
        raise HTTPException(status_code=401)
    return f"user:{token}"


def public_endpoint[F](fn: F) -> F:
    """Mark an endpoint as intentionally not requiring authentication.

    The invariant test looks for this marker as the only acceptable way to
    skip the auth dependency.
    """
    fn._public_endpoint = True  # type: ignore[attr-defined]
    return fn
