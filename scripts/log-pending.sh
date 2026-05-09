#!/bin/bash
# Show all learning log entries still marked as pending.

LOG="$HOME/.claude/learning/log.md"

if [ ! -f "$LOG" ]; then
  echo "No log found at $LOG"
  exit 1
fi

echo "# Pending articles"
echo ""
grep "| pending |" "$LOG"
