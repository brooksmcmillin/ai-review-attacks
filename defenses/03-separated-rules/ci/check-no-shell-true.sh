#!/usr/bin/env bash
# Fail if any subprocess call uses shell=True with an f-string or % formatting
# in the same line — the most common shell-injection pattern.

set -euo pipefail

ROOT="${1:-.}"
matches="$(
  grep -RInE 'subprocess\.(run|call|check_call|check_output|Popen)\(' \
    --include='*.py' "$ROOT" |
    grep -E 'shell\s*=\s*True' |
    grep -E '(f["'"'"']|%\s*\()' || true
)"

if [[ -n "$matches" ]]; then
  printf 'Likely shell injection (shell=True + dynamic string):\n%s\n' "$matches" >&2
  exit 1
fi

echo "check-no-shell-true: OK"
