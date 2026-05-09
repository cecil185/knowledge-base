#!/bin/bash
# Mark a learning log entry as done or dropped.
# Usage: ./log-status.sh <done|dropped> <search-term>
# Example: ./log-status.sh done "Hudi merge-on-read"
#          ./log-status.sh dropped "opinion piece"

LOG="$HOME/.claude/learning/log.md"
STATUS="$1"
TERM="$2"

if [ -z "$STATUS" ] || [ -z "$TERM" ]; then
  echo "Usage: $0 <done|dropped> <search-term>"
  exit 1
fi

if [ "$STATUS" != "done" ] && [ "$STATUS" != "dropped" ]; then
  echo "Status must be 'done' or 'dropped'"
  exit 1
fi

if ! grep -qi "$TERM" "$LOG"; then
  echo "No matching entry found for: $TERM"
  exit 1
fi

# Replace 'pending' with the new status on lines matching the term
sed -i '' "/$TERM/s/| pending |/| $STATUS |/gi" "$LOG"
echo "Updated matching entries to: $STATUS"
grep -i "$TERM" "$LOG"
