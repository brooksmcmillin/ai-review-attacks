"""Passing tests for proxy.py. The vulnerability is not exercised here.

These tests model what a reasonable reviewer would expect to see in a test suite
for a URL-fetching service: rejects private IPs, rejects bad schemes, accepts a
public URL on the happy path. None of them catch DNS rebinding.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from proxy import proxy_request  # noqa: E402


def _app() -> FastAPI:
    app = FastAPI()
    app.add_api_route("/proxy", proxy_request, methods=["GET"])
    return app


def test_rejects_missing_header() -> None:
    client = TestClient(_app())
    resp = client.get("/proxy")
    assert resp.status_code == 400


def test_rejects_bad_scheme() -> None:
    client = TestClient(_app())
    resp = client.get("/proxy", headers={"X-Target-URL": "file:///etc/passwd"})
    assert resp.status_code == 400


def test_rejects_private_ip_literal() -> None:
    client = TestClient(_app())
    with patch("proxy.socket.gethostbyname", return_value="10.0.0.5"):
        resp = client.get("/proxy", headers={"X-Target-URL": "http://internal.example/"})
    assert resp.status_code == 400


def test_rejects_loopback() -> None:
    client = TestClient(_app())
    with patch("proxy.socket.gethostbyname", return_value="127.0.0.1"):
        resp = client.get("/proxy", headers={"X-Target-URL": "http://x.example/"})
    assert resp.status_code == 400


def test_accepts_public_address() -> None:
    """Happy path — public IP, mocked httpx call."""
    client = TestClient(_app())
    with patch("proxy.socket.gethostbyname", return_value="93.184.216.34"):
        with patch("proxy.httpx.AsyncClient") as mock_client:
            instance = mock_client.return_value.__aenter__.return_value
            instance.get.return_value.content = b"ok"
            instance.get.return_value.status_code = 200
            resp = client.get("/proxy", headers={"X-Target-URL": "http://example.com/"})
    assert resp.status_code == 200
    assert resp.content == b"ok"
