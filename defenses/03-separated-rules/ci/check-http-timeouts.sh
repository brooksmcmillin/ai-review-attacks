#!/usr/bin/env bash
# Fail if any requests.get / httpx.get call ships without a timeout=.
#
# Deterministic, runs in CI under CODEOWNERS protection. The AI reviewer is
# welcome to add nuance; this script is the floor.

set -euo pipefail

ROOT="${1:-.}"
matches="$(
  grep -RInE \
    '(requests|httpx|urllib3)\.(get|post|put|patch|delete|head|options|request)\(' \
    --include='*.py' \
    "$ROOT" |
    grep -vE 'timeout\s*=' || true
)"

if [[ -n "$matches" ]]; then
  printf 'HTTP calls without timeout=:\n%s\n' "$matches" >&2
  exit 1
fi

echo "check-http-timeouts: OK"
