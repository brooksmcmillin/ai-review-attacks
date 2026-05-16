"""Example FastAPI app used by the security-invariant tests."""

from example_app.app import app
from example_app.deps import current_user, public_endpoint

__all__ = ["app", "current_user", "public_endpoint"]
