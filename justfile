garden:
    bash scripts/garden_docs.sh

test:
    python3 -m pytest scripts/test_eval_digest.py -v

# --- Filter eval (/digest Step 3) ---

# Run the digest filter eval against the full labels.jsonl
# Requires ANTHROPIC_API_KEY for live LLM calls.
eval-filter variant="v1":
    python3 scripts/eval_digest.py --variant {{variant}}

# Dry-run: skip LLM calls, mirror labels as predictions (sanity check report format)
eval-filter-dry variant="v1":
    python3 scripts/eval_digest.py --variant {{variant}} --dry-run

# Run against the 5-example fixture set (fast sanity check)
eval-filter-fixtures:
    python3 scripts/eval_digest.py --fixtures --dry-run

# Append new examples to evals/digest/labels.jsonl from Linear ticket state.
# Requires LINEAR_API_KEY (https://linear.app/settings/account/security).
sync-filter-labels project="Data AI Engineering":
    python3 scripts/sync_labels.py --project "{{project}}"

sync-filter-labels-dry project="Data AI Engineering":
    python3 scripts/sync_labels.py --project "{{project}}" --dry-run

ci: garden test
