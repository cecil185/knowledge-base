#!/bin/bash
# Search the learning log by keyword. Usage: ./log-search.sh <term>
# Example: ./log-search.sh hudi
#          ./log-search.sh pending

LOG="$HOME/.claude/learning/log.md"

if [ ! -f "$LOG" ]; then
  echo "No log found at $LOG"
  exit 1
fi

if [ -z "$1" ]; then
  cat "$LOG"
  exit 0
fi

grep -i "$1" "$LOG"
