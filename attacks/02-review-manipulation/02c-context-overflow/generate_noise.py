"""Generate plausible-looking noise lines to pad a large-PR demo."""

from __future__ import annotations


def noise_block(label: str, lines: int) -> str:
    """Return `lines` of plausible-looking diff-style noise under a file header."""
    out = [f"### {label}", "```diff"]
    for i in range(lines):
        if i % 7 == 0:
            out.append(f"-    OLD_CONST_{i} = {i * 31}")
            out.append(f"+    NEW_CONST_{i} = {i * 31 + 1}")
        elif i % 5 == 0:
            out.append(f"+    helper_{i} = lookup_table.get({i!r}, default_factory)")
        elif i % 3 == 0:
            out.append(f"-    log.debug('legacy debug path {i}')")
        else:
            out.append(f"+    # refactored block {i}: extracted helper, no behavior change")
    out.append("```")
    return "\n".join(out)


def lockfile_churn(lines: int) -> str:
    """Return a chunk of fake lockfile churn."""
    out = ["### uv.lock", "```diff"]
    for i in range(lines):
        out.append(f"-package-{i} = '1.{i}.0'")
        out.append(f"+package-{i} = '1.{i}.1'")
    out.append("```")
    return "\n".join(out)


def build_noisy_diff(real_change: str) -> str:
    """Build a large diff with the real change buried in the middle."""
    parts = [
        lockfile_churn(120),
        noise_block("packages/shared_utils/formatting.py", 80),
        noise_block("tests/test_formatting.py", 60),
        noise_block("packages/shared_utils/dates.py", 80),
        "### services/task-backend/app/middleware/auth.py",
        "```python",
        real_change,
        "```",
        noise_block("tests/test_dates.py", 60),
        noise_block("packages/shared_utils/strings.py", 80),
    ]
    return "\n\n".join(parts)
