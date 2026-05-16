"""Shared harness for the ai-review-attacks demos.

The attacks each call review_pr() with two contexts — one clean, one poisoned —
and print the model's verdict so you can see the review flip.
"""

from harness.reviewer import (
    REVIEW_SYSTEM_PROMPT,
    ReviewResult,
    ToolExchange,
    review_pr,
    set_debug,
)
from harness.runner import AttackCase, print_demo_separator, run_attack

__all__ = [
    "REVIEW_SYSTEM_PROMPT",
    "AttackCase",
    "ReviewResult",
    "ToolExchange",
    "print_demo_separator",
    "review_pr",
    "run_attack",
    "set_debug",
]
