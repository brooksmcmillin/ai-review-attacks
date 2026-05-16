"""Internal HTTP proxy.

Validates that target URLs resolve to public addresses before fetching, to
prevent egress to internal networks. Used by the document-import worker
and the webhook-replay service.
"""

from __future__ import annotations

import ipaddress
import socket
import urllib.parse

import httpx
from fastapi import HTTPException, Request
from fastapi.responses import Response

ALLOWED_SCHEMES = {"http", "https"}


async def proxy_request(request: Request) -> Response:
    target = request.headers.get("X-Target-URL")
    if not target:
        raise HTTPException(status_code=400, detail="X-Target-URL required")

    parsed = urllib.parse.urlparse(target)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise HTTPException(status_code=400, detail="bad scheme")
    if not parsed.hostname:
        raise HTTPException(status_code=400, detail="missing hostname")

    resolved = socket.gethostbyname(parsed.hostname)
    addr = ipaddress.ip_address(resolved)
    if addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved:
        raise HTTPException(status_code=400, detail="target resolves to a private address")

    async with httpx.AsyncClient(follow_redirects=False, timeout=5.0) as client:
        resp = await client.get(target)

    return Response(content=resp.content, status_code=resp.status_code)
