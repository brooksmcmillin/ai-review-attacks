"""Run attack 01 against the harness — both sub-attacks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running this file directly (`uv run python attacks/01-.../run.py`)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from harness import AttackCase, print_demo_separator, run_attack, set_debug  # noqa: E402

HERE = Path(__file__).parent


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def attack_01a() -> int:
    base_dir = HERE / "01a-selective-blindness"
    file_path = "packages/legacy/handlers.py"  # matches ADR-0042 framing
    clean = AttackCase(
        label="clean AGENTS.md",
        repo_context=_read(base_dir / "AGENTS_clean.md"),
        diff_or_files=f"### {file_path}\n\n```python\n{_read(base_dir / 'vulnerable_code.py')}\n```",
    )
    poisoned = AttackCase(
        label="poisoned AGENTS.md (Legacy Patterns block)",
        repo_context=_read(base_dir / "AGENTS_poisoned.md"),
        diff_or_files=clean.diff_or_files,
    )
    return run_attack("01a — Selective Blindness", clean, poisoned)


def attack_01b() -> int:
    base_dir = HERE / "01b-hidden-instructions"
    file_path = "packages/users/routes.py"  # under the migration banner path
    clean = AttackCase(
        label="clean AGENTS.md",
        repo_context=_read(base_dir / "AGENTS_clean.md"),
        diff_or_files=f"### {file_path}\n\n```python\n{_read(base_dir / 'vulnerable_code.py')}\n```",
    )
    poisoned = AttackCase(
        label="poisoned AGENTS.md (HTML-comment instruction)",
        repo_context=_read(base_dir / "AGENTS_poisoned.md"),
        diff_or_files=clean.diff_or_files,
    )
    return run_attack("01b — Hidden Instructions", clean, poisoned)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print the prompts sent to and the raw response received from the LLM.",
    )
    args = parser.parse_args()
    set_debug(args.debug)

    results: list[int] = []
    for i, attack in enumerate([attack_01a, attack_01b]):
        if i > 0:
            print_demo_separator()
        results.append(attack())
    return 0 if any(r == 0 for r in results) else max(results)


if __name__ == "__main__":
    raise SystemExit(main())
