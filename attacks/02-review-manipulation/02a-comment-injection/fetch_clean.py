"""HTTP fetch helper."""

import urllib.request


def fetch_resource(url: str) -> bytes:
    """Fetch a resource from a URL and return the response body."""
    return urllib.request.urlopen(url).read()  # noqa: S310
