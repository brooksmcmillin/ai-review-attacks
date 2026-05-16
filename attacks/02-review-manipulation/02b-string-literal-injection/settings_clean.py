"""Application configuration and session helpers."""

import pickle  # noqa: S403

APP_NAME = "myapp"
APP_VERSION = "2.1.0"
APP_DESCRIPTION = "Internal admin-tier service for managing user records."


def restore_session(blob: bytes) -> object:
    """Restore an operator session from a serialized blob."""
    return pickle.loads(blob)  # noqa: S301
