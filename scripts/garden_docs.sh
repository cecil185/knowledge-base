#!/usr/bin/env bash
# Doc gardener: checks that projects/ directories and the CLAUDE.md projects
# table are in sync. Exits non-zero and prints a report if drift is found.
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT="$(pwd)"
CLAUDE_MD="$ROOT/CLAUDE.md"
PROJECTS_DIR="$ROOT/projects"
drift=0

warn() { echo "  DRIFT: $1"; drift=1; }
ok()   { echo "  ok:    $1"; }

echo "=== Doc Gardener ==="
echo

# --- 1. Extract slugs from CLAUDE.md projects table -----------------------
# Matches lines like: | `data-ai-engineering` | ... |
mapfile -t table_slugs < <(
  grep -E '^\| `[a-z0-9-]+`' "$CLAUDE_MD" | sed -E 's/^\| `([^`]+)`.*/\1/' | sort || true
)

if [[ ${#table_slugs[@]} -eq 0 ]]; then
  echo "WARNING: could not parse any slugs from CLAUDE.md projects table"
  exit 1
fi

# --- 2. Get actual directories under projects/ ----------------------------
mapfile -t dir_slugs < <(
  find "$PROJECTS_DIR" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
)

echo "## Table → directory"
for slug in "${table_slugs[@]}"; do
  if [[ -d "$PROJECTS_DIR/$slug" ]]; then
    ok "$slug in CLAUDE.md has projects/$slug/"
  else
    warn "$slug in CLAUDE.md but no projects/$slug/ directory"
  fi
done

echo
echo "## Directory → table"
for slug in "${dir_slugs[@]}"; do
  if printf '%s\n' "${table_slugs[@]}" | grep -qx "$slug"; then
    ok "projects/$slug/ is listed in CLAUDE.md"
  else
    warn "projects/$slug/ exists but no row in CLAUDE.md projects table"
  fi
done

echo
echo "## Required files"
for slug in "${dir_slugs[@]}"; do
  for f in goal.md sources.md; do
    if [[ -f "$PROJECTS_DIR/$slug/$f" ]]; then
      ok "projects/$slug/$f exists"
    else
      warn "projects/$slug/$f is missing"
    fi
  done
done

echo
if [[ $drift -eq 1 ]]; then
  echo "Result: drift detected — fix the issues above"
  exit 1
else
  echo "Result: docs and projects/ are in sync"
fi
