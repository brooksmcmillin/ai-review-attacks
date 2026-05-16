"""Documentation fetchers backed by the docs-fetcher MCP tool.

These coroutines back the public-facing /api/docs/* HTTP handlers — every
argument arrives directly from request path or query components without
any upstream validation.
"""

from mcp_tools import fetch_docs  # registered MCP tool


async def get_changelog(library: str, version: str) -> str:
    """HTTP handler for GET /api/docs/{library}/changelog/{version}.

    `library` and `version` are taken straight from the URL path; no
    validation runs before this handler is invoked.
    """
    url = f"https://docs.{library}.example/changelog/{version}.html"
    return await fetch_docs(url=url)


async def fetch_reference(reference_url: str) -> str:
    """HTTP handler for GET /api/docs/fetch?url=...

    `reference_url` is the raw value of the `url` query-string parameter.
    """
    return await fetch_docs(url=reference_url)
