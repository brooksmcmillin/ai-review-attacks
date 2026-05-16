# 03: Passing Every Check, Still Vulnerable

A PR passes static analysis, lint, type checks, the AI reviewer, **and** its
own tests. It still has an exploitable SSRF.

The vulnerability is a DNS-rebinding race: `urllib.parse.urlparse(target)` extracts
a hostname, the code resolves it (the first lookup returns a public IP and passes a
private-network check), then `httpx.get(target)` resolves the hostname **again**.
An attacker controls a DNS record with a low TTL; between the two lookups, the
record flips to `127.0.0.1` or a metadata-service IP.

Static review can't see this because the code looks right. Tests can't see it
because nothing in the test fixture exercises the race. The AI reviewer can be
convinced by the comment that says "validates URL." It treats the validation
as sound.

## Files

- `proxy.py`: the vulnerable service
- `tests/test_proxy.py`: passing test suite that exercises the happy path and
  rejects the obvious bad inputs (private IPs at parse time, bad schemes)
- `run.py`: sends the file to the AI reviewer and reports.
- `dns_rebind_demo.py`: a self-contained, offline demonstration of the race
  using a stub resolver that flips between calls. **Does not** touch real DNS.

## Run it

```bash
# AI reviewer demo (needs ANTHROPIC_API_KEY)
uv run python attacks/03-trust-boundary/run.py

# Offline exploit demo (no API key needed; pure Python)
uv run python attacks/03-trust-boundary/dns_rebind_demo.py

# Show that the test suite passes
uv run pytest attacks/03-trust-boundary/tests/
```
