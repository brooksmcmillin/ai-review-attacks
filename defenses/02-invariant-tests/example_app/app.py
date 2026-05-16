"""Routes for the example app — used to demonstrate invariant tests."""

from __future__ import annotations

from fastapi import Depends, FastAPI

from example_app.deps import current_user, public_endpoint

app = FastAPI()


@app.get("/me")
def get_me(user: str = Depends(current_user)) -> dict[str, str]:
    """Authenticated route — depends on current_user."""
    return {"user": user}


@app.get("/projects/{project_id}")
def get_project(project_id: str, user: str = Depends(current_user)) -> dict[str, str]:
    """Authenticated route."""
    return {"project_id": project_id, "user": user}


@app.get("/health")
@public_endpoint
def health() -> dict[str, str]:
    """Intentionally public — health check."""
    return {"status": "ok"}


@app.get("/version")
@public_endpoint
def version() -> dict[str, str]:
    """Intentionally public — service version."""
    return {"version": "1.0.0"}
