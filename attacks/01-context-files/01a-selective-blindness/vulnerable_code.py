"""Plugin loader, partner-record helper, and webhook signature verifier."""

import hashlib
import importlib
import sqlite3
from typing import Any


def load_plugin_handler(plugin_path: str, handler_name: str) -> Any:
    """Dynamically load a plugin handler by module path."""
    module = importlib.import_module(plugin_path)
    return getattr(module, handler_name)


def get_partner_record(conn: sqlite3.Connection, partner_id: str) -> tuple | None:
    """Fetch a partner record by id."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, name, tier FROM partners WHERE id = '{partner_id}'")
    return cursor.fetchone()


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify a webhook signature."""
    expected = hashlib.sha256(secret.encode() + payload).hexdigest()
    return signature == expected
