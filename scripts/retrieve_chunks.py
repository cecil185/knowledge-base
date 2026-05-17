#!/usr/bin/env python3
"""
FTS5 chunk retrieval from a project's chunks.sqlite store.

Opens <project-dir>/chunks.sqlite and runs an FTS5 query against it,
returning ranked results as a JSON array.

Usage:
    python3 scripts/retrieve_chunks.py \
        --project-dir projects/data-ai-engineering \
        --query "how does RAG work" \
        [--top-k 10]

Output:
    JSON array to stdout: [{id, article_slug, paragraph_idx, text, url}, ...]
    Returns [] if DB is absent or query has no matches. Exits 0 in all cases.
"""

import argparse
import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Chunk:
    id: int
    article_slug: str
    paragraph_idx: int
    text: str
    url: str


# ---------------------------------------------------------------------------
# Core retrieval
# ---------------------------------------------------------------------------

_FTS_QUERY = """
    SELECT c.id, c.article_slug, c.paragraph_idx, c.text, c.url
    FROM chunks_fts
    JOIN chunks c ON chunks_fts.rowid = c.id
    WHERE chunks_fts MATCH ?
    ORDER BY rank
    LIMIT ?;
"""


def retrieve(project_dir: Path, query: str, top_k: int = 10) -> list[dict]:
    """
    Run FTS5 retrieval against chunks.sqlite in project_dir.

    Returns a list of plain dicts (JSON-serialisable). Returns [] without
    raising if the DB is absent or the query matches nothing.
    """
    db_path = project_dir / "chunks.sqlite"

    if not db_path.exists():
        return []

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute(_FTS_QUERY, (query, top_k))
        rows = cur.fetchall()
    except sqlite3.OperationalError:
        # Table may not exist yet or query syntax error — degrade gracefully
        return []
    finally:
        conn.close()

    return [
        asdict(Chunk(
            id=row["id"],
            article_slug=row["article_slug"],
            paragraph_idx=row["paragraph_idx"],
            text=row["text"],
            url=row["url"],
        ))
        for row in rows
    ]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Retrieve top-k chunks from chunks.sqlite via FTS5"
    )
    parser.add_argument(
        "--project-dir",
        required=True,
        help="Path to the project directory containing chunks.sqlite",
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Natural-language query (used as FTS5 MATCH string)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=10,
        help="Maximum number of results to return (default: 10)",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    results = retrieve(project_dir, args.query, top_k=args.top_k)
    print(json.dumps(results, ensure_ascii=False))


if __name__ == "__main__":
    main()
