#!/usr/bin/env bash
# Run every attack harness end-to-end and report which ones flipped the
# reviewer's verdict.
#
# Requires ANTHROPIC_API_KEY in the environment (or a .env file at repo root).

set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -f .env && -z "${ANTHROPIC_API_KEY:-}" ]]; then
  set -a
  source .env
  set +a
fi

if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "ANTHROPIC_API_KEY not set. Copy .env.example to .env and fill it in." >&2
  exit 2
fi

declare -a demos=(
  "attacks/01-context-files/run.py"
  "attacks/02-review-manipulation/run.py"
  "attacks/03-trust-boundary/run.py"
  "attacks/04-runtime-compromise/run.py"
)

flipped=0
total=0
for demo in "${demos[@]}"; do
  total=$((total + 1))
  echo
  echo "### $demo"
  if uv run python "$demo"; then
    flipped=$((flipped + 1))
  fi
done

echo
echo "Summary: $flipped/$total demo categories reproduced this run."
echo "(LLM behavior is non-deterministic — rerun to see variance.)"
