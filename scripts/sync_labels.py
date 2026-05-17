#!/usr/bin/env python3
"""
Sync evals/digest/labels.jsonl from Linear ticket state.

Pulls all article tickets in a given Linear project and appends any URLs
not already in labels.jsonl. Each new row's keep/drop is derived from the
ticket's labels:

    Canceled + 'delete-from-wiki' label  ->  keep=false
    otherwise                            ->  keep=true

Usage:
    python3 scripts/sync_labels.py [--project "Data AI Engineering"] [--dry-run]

Requirements:
    pip install requests
    LINEAR_API_KEY env var (create at https://linear.app/settings/account/security)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
LABELS_PATH = ROOT / "evals/digest/labels.jsonl"
LINEAR_API = "https://api.linear.app/graphql"

QUERY = """
query ArticleTickets($projectName: String!) {
  issues(
    filter: { project: { name: { eq: $projectName } } }
    first: 250
  ) {
    nodes {
      identifier
      title
      description
      state { name type }
      labels { nodes { name } }
      createdAt
      url
    }
  }
}
"""


def linear_query(project_name: str) -> list[dict]:
    try:
        import requests
    except ImportError:
        sys.exit("requests not installed. Run: pip install requests")

    api_key = os.environ.get("LINEAR_API_KEY")
    if not api_key:
        sys.exit("LINEAR_API_KEY not set. Create one at https://linear.app/settings/account/security")

    resp = requests.post(
        LINEAR_API,
        headers={"Authorization": api_key, "Content-Type": "application/json"},
        json={"query": QUERY, "variables": {"projectName": project_name}},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        sys.exit(f"Linear API error: {data['errors']}")
    return data["data"]["issues"]["nodes"]


def extract_url(description: str) -> str:
    """Extract the first http(s) URL from a ticket description."""
    if not description:
        return ""
    # Match URLs, including ones wrapped in markdown brackets or angle brackets
    m = re.search(r"https?://[^\s\)>\]\"']+", description)
    return m.group(0).rstrip(".,;") if m else ""


def derive_keep(ticket: dict) -> bool:
    """keep=false if Canceled with delete-from-wiki; otherwise keep=true."""
    label_names = {l["name"] for l in ticket["labels"]["nodes"]}
    state_type = ticket["state"]["type"]
    if state_type == "canceled" and "delete-from-wiki" in label_names:
        return False
    return True


def derive_surfaced_by(url: str, ticket_title: str) -> str:
    """Heuristic: 'hn' if title hints at HN sourcing, otherwise 'sources'."""
    lowered = (url + " " + ticket_title).lower()
    if "hacker news" in lowered or "hackernews" in lowered or "ycombinator" in lowered:
        return "hn"
    return "sources"


def normalize_url(url: str) -> str:
    """Match scripts/eval_digest.py:_normalize_url for dedup."""
    url = re.sub(r"[?&]utm_[^&]*", "", url)
    url = re.sub(r"[?&]$", "", url)
    return url.rstrip("/")


def load_existing_urls(path: Path) -> set[str]:
    if not path.exists():
        return set()
    urls = set()
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        urls.add(normalize_url(row.get("url", "")))
    return urls


def main():
    parser = argparse.ArgumentParser(description="Sync labels.jsonl from Linear")
    parser.add_argument(
        "--project",
        default="Data AI Engineering",
        help="Linear project name (matches Project field on tickets)",
    )
    parser.add_argument(
        "--labels",
        default=str(LABELS_PATH),
        help="Path to labels.jsonl",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be added without writing the file",
    )
    args = parser.parse_args()

    labels_path = Path(args.labels)
    existing = load_existing_urls(labels_path)
    print(f"Loaded {len(existing)} existing URLs from {labels_path}")

    tickets = linear_query(args.project)
    print(f"Fetched {len(tickets)} tickets from Linear project '{args.project}'")

    new_rows = []
    skipped_no_url = 0
    skipped_duplicate = 0

    for ticket in tickets:
        url = extract_url(ticket["description"] or "")
        if not url:
            skipped_no_url += 1
            continue
        if normalize_url(url) in existing:
            skipped_duplicate += 1
            continue

        row = {
            "url": url,
            "title": ticket["title"],
            "surfaced_by": derive_surfaced_by(url, ticket["title"]),
            "keep": derive_keep(ticket),
            "reason": f"Auto-synced from Linear {ticket['identifier']} ({ticket['state']['name']})",
            "labeled_at": date.today().isoformat(),
            "linear_id": ticket["identifier"],
        }
        new_rows.append(row)

    print(f"\nNew rows to append: {len(new_rows)}")
    print(f"Skipped (no URL in description): {skipped_no_url}")
    print(f"Skipped (already in labels): {skipped_duplicate}")

    if not new_rows:
        print("Nothing to add.")
        return

    for row in new_rows:
        marker = "keep" if row["keep"] else "DROP"
        print(f"  + [{marker}] {row['linear_id']}: {row['title'][:70]}")

    if args.dry_run:
        print("\n[dry-run] No file written.")
        return

    with labels_path.open("a") as f:
        for row in new_rows:
            f.write(json.dumps(row) + "\n")

    print(f"\nAppended {len(new_rows)} rows to {labels_path}")
    print("Review the new rows and edit `reason` fields as needed before committing.")


if __name__ == "__main__":
    main()
