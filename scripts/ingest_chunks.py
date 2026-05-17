#!/usr/bin/env python3
"""
CLI to create/populate a SQLite chunk store from article text.

Creates <project-dir>/chunks.sqlite with a chunks table and FTS5 virtual table,
then upserts paragraph-level chunks for the given article.

Usage:
    python3 scripts/ingest_chunks.py --slug <article-slug> --url <url> \
        --project-dir <path> [--file <path> | stdin]

Requirements:
    Python 3.8+ (sqlite3 is in the stdlib)
"""

import argparse
import re
import sqlite3
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

DDL_CHUNKS = """
CREATE TABLE IF NOT EXISTS chunks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  article_slug TEXT NOT NULL,
  paragraph_idx INTEGER NOT NULL,
  text TEXT NOT NULL,
  char_start INTEGER NOT NULL,
  char_end INTEGER NOT NULL,
  url TEXT NOT NULL,
  UNIQUE(article_slug, paragraph_idx)
);
"""

DDL_FTS = """
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts
  USING fts5(text, content=chunks, content_rowid=id);
"""


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def _strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter (--- ... ---) from the top of a file."""
    return re.sub(r"^---\n.*?\n---\n*", "", text, count=1, flags=re.DOTALL)


def _split_paragraphs(body: str) -> list[str]:
    """Split on double-newlines, keeping only non-empty paragraphs (stripped)."""
    return [p.strip() for p in body.split("\n\n") if p.strip()]


def _compute_offsets(body: str, paragraphs: list[str]) -> list[tuple[str, int, int]]:
    """Return (text, char_start, char_end) for each paragraph.

    Scans forward through body to find each paragraph's position, preserving
    the exact text slice so that body[char_start:char_end] == text.
    """
    results: list[tuple[str, int, int]] = []
    cursor = 0
    for para in paragraphs:
        idx = body.find(para, cursor)
        if idx == -1:
            # Should not happen given paragraphs come from splitting body,
            # but handle defensively.
            idx = cursor
        char_start = idx
        char_end = char_start + len(para)
        results.append((para, char_start, char_end))
        cursor = char_end
    return results


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute(DDL_CHUNKS)
    conn.execute(DDL_FTS)
    conn.commit()


def ingest(slug: str, url: str, project_dir: Path, body: str) -> int:
    """Create/update chunk store for the given article.

    Returns the number of rows inserted.
    """
    db_path = project_dir / "chunks.sqlite"
    conn = sqlite3.connect(db_path)

    _ensure_schema(conn)

    paragraphs = _split_paragraphs(_strip_frontmatter(body))
    if not paragraphs:
        conn.close()
        return 0

    offsets = _compute_offsets(body, paragraphs)

    # Upsert: delete existing rows for this slug, then insert fresh
    conn.execute("DELETE FROM chunks WHERE article_slug = ?", (slug,))

    for idx, (text, char_start, char_end) in enumerate(offsets):
        conn.execute(
            """
            INSERT INTO chunks (article_slug, paragraph_idx, text, char_start, char_end, url)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (slug, idx, text, char_start, char_end, url),
        )

    # Rebuild FTS index so chunks_fts MATCH queries reflect current rows.
    # chunks_fts is a content table (content=chunks), so it does not auto-update
    # on INSERT/DELETE; a full rebuild is the canonical way to sync it.
    conn.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")

    conn.commit()
    count = len(offsets)
    conn.close()
    return count


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest article text into SQLite chunk store")
    parser.add_argument("--slug", required=True, help="Article slug (unique identifier)")
    parser.add_argument("--url", required=True, help="Article URL")
    parser.add_argument(
        "--project-dir",
        required=True,
        help="Project directory — chunks.sqlite is created here",
    )
    parser.add_argument(
        "--file",
        default=None,
        help="Path to file containing article text (default: read from stdin)",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    if not project_dir.exists():
        project_dir.mkdir(parents=True, exist_ok=True)

    if args.file:
        body = Path(args.file).read_text(encoding="utf-8")
    else:
        body = sys.stdin.read()

    count = ingest(
        slug=args.slug,
        url=args.url,
        project_dir=project_dir,
        body=body,
    )

    print(f"Ingested {count} chunks for slug '{args.slug}' into {project_dir / 'chunks.sqlite'}")


if __name__ == "__main__":
    main()
