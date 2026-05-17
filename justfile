garden:
    bash scripts/garden_docs.sh

test:
    python3 -m pytest scripts/test_eval_digest.py -v

# Run the digest filter eval against the full labels.jsonl
# Requires ANTHROPIC_API_KEY for live LLM calls.
eval variant="v1":
    python3 scripts/eval_digest.py --variant {{variant}}

# Dry-run: skip LLM calls, mirror labels as predictions (sanity check report format)
eval-dry variant="v1":
    python3 scripts/eval_digest.py --variant {{variant}} --dry-run

# Run against the 5-example fixture set (fast sanity check)
eval-fixtures:
    python3 scripts/eval_digest.py --fixtures --dry-run

ci: garden test
