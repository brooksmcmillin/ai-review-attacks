"""run_attack() — common entry point for every attack demo.

Each attack calls this twice (clean baseline vs. poisoned variant) and the
runner prints the two verdicts side by side. Talk-friendly output.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any

from harness.reviewer import ReviewResult, ToolExchange, _use_color, review_pr

_ANSI_SEPARATOR = "\033[1;35m"  # bold bright magenta
_ANSI_RESET = "\033[0m"


def print_demo_separator() -> None:
    """Visually loud break between sub-demos. Always prints (debug or not)."""
    bar = "█" * 76
    if _use_color():
        print(f"\n{_ANSI_SEPARATOR}{bar}{_ANSI_RESET}\n")
    else:
        print(f"\n{bar}\n")


@dataclass(slots=True)
class AttackCase:
    label: str
    repo_context: str
    diff_or_files: str
    tools: list[dict[str, Any]] | None = field(default=None)
    prior_tool_exchange: ToolExchange | None = field(default=None)
    system_appendix: str | None = field(default=None)


def run_attack(title: str, baseline: AttackCase, poisoned: AttackCase) -> int:
    """Run baseline + poisoned through the reviewer, print verdict comparison.

    Returns shell exit code: 0 if poisoning flipped the verdict (attack succeeded),
    1 if both runs gave the same verdict (attack did not reproduce this run).
    """
    print(f"\n{'=' * 76}")
    print(f"  {title}")
    print(f"{'=' * 76}\n")

    print(f"-> Running BASELINE ({baseline.label})...")
    base = _safe_review(baseline)
    _print_result("BASELINE", base)

    print(f"\n-> Running POISONED ({poisoned.label})...")
    pois = _safe_review(poisoned)
    _print_result("POISONED", pois)

    print("\n" + "-" * 76)
    if base is None or pois is None:
        print("  Could not reach the model; rerun once your API key is set.")
        return 2
    flipped = base.verdict != pois.verdict
    if flipped:
        print(f"  Attack reproduced: verdict flipped {base.verdict} -> {pois.verdict}")
        return 0
    print(f"  Attack did NOT reproduce this run (both verdicts: {base.verdict}).")
    print("  LLM behavior is non-deterministic; try again or adjust the payload.")
    return 1


def _safe_review(case: AttackCase) -> ReviewResult | None:
    try:
        return review_pr(
            case.repo_context,
            case.diff_or_files,
            tools=case.tools,
            prior_tool_exchange=case.prior_tool_exchange,
            system_appendix=case.system_appendix,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  ! reviewer call failed: {exc}", file=sys.stderr)
        return None


def _print_result(label: str, result: ReviewResult | None) -> None:
    if result is None:
        print(f"   {label}: <no result>")
        return
    print(f"   {label} verdict : {result.verdict}")
    summary = result.summary or "(empty)"
    print(f"   {label} summary : {summary[:220]}")
