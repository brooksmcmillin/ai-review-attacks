"""Deterministic security invariants for the example app.

These run as code, not LLM analysis. They cannot be talked out of finding what
they find, and a poisoned AGENTS.md cannot change their verdict.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from fastapi.routing import APIRoute

HERE = Path(__file__).resolve().parent
APP_ROOT = HERE.parent / "example_app"
sys.path.insert(0, str(HERE.parent))

from example_app import app, current_user  # noqa: E402


def test_every_route_has_an_auth_policy() -> None:
    """Either the route depends on current_user, or it's tagged @public_endpoint."""
    offenders: list[str] = []

    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        endpoint = route.endpoint
        depends_on_current_user = any(
            getattr(dep.call, "__name__", "") == current_user.__name__
            for dep in route.dependant.dependencies
        )
        marked_public = getattr(endpoint, "_public_endpoint", False)
        if not depends_on_current_user and not marked_public:
            offenders.append(f"{', '.join(route.methods)} {route.path}")

    assert not offenders, (
        f"Routes missing an auth policy: {offenders}. "
        f"Either add Depends(current_user) or @public_endpoint."
    )


SQL_VERBS_RE = re.compile(
    r"""f["'][^"']*\b(SELECT|INSERT|UPDATE|DELETE|MERGE|REPLACE)\b""",
    re.IGNORECASE,
)


def test_no_raw_sql_in_app_code() -> None:
    """No f-strings containing SQL verbs."""
    offenders: list[str] = []
    for py_file in APP_ROOT.rglob("*.py"):
        contents = py_file.read_text(encoding="utf-8")
        for lineno, line in enumerate(contents.splitlines(), start=1):
            if SQL_VERBS_RE.search(line):
                offenders.append(f"{py_file.relative_to(APP_ROOT.parent)}:{lineno}")

    assert not offenders, (
        f"Raw SQL via f-string detected: {offenders}. "
        f"Use parameterized queries (cursor.execute(sql, params))."
    )
