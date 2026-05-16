"""Database helpers using parameterized queries throughout."""

from __future__ import annotations

import sqlite3


def fetch_user(conn: sqlite3.Connection, user_id: str) -> tuple | None:
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, role FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


def insert_audit(conn: sqlite3.Connection, user_id: str, action: str) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO audit_events (user_id, action) VALUES (?, ?)",
        (user_id, action),
    )
    conn.commit()
