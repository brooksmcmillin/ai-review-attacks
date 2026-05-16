"""Pytest path setup.

Each tests location has its own sibling code (`example_app/`, the sanitizer
file). Adding both to sys.path here keeps test files import-clean without
package-installation gymnastics.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "defenses" / "02-invariant-tests"))
sys.path.insert(0, str(ROOT / "defenses" / "06-runtime-hardening"))
