#!/usr/bin/env python3
"""
Unit tests for scripts/retrieve_chunks.py.

Run with:
    python -m pytest scripts/test_retrieve_chunks.py -v
"""

import json
import sqlite3
import sys
import tempfile
from pathlib import Path

import pytest

# Allow importing retrieve_chunks from the same directory
sys.path.insert(0, str(Path(__file__).parent))
import retrieve_chunks


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _create_db(db_path: Path, rows: list[dict]) -> None:
    """Create a chunks.sqlite with FTS5 and populate it."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_slug TEXT NOT NULL,
            paragraph_idx INTEGER NOT NULL,
            text TEXT NOT NULL,
            url TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            text,
            content='chunks',
            content_rowid='id'
        )
    """)
    for row in rows:
        cur.execute(
            "INSERT INTO chunks (article_slug, paragraph_idx, text, url) VALUES (?, ?, ?, ?)",
            (row["article_slug"], row["paragraph_idx"], row["text"], row["url"]),
        )
    # Populate FTS index
    cur.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_fts5_match_returns_rows():
    """Insert 5 rows, query with keyword in 2 of them — should return those 2."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        db_path = project_dir / "chunks.sqlite"

        rows = [
            {"article_slug": "article-a", "paragraph_idx": 0, "text": "Transformers use attention mechanisms for sequence modelling.", "url": "https://example.com/a"},
            {"article_slug": "article-b", "paragraph_idx": 0, "text": "Gradient descent optimizes neural network weights.", "url": "https://example.com/b"},
            {"article_slug": "article-c", "paragraph_idx": 0, "text": "Attention is all you need for transformer architectures.", "url": "https://example.com/c"},
            {"article_slug": "article-d", "paragraph_idx": 0, "text": "Random forests ensemble many decision trees.", "url": "https://example.com/d"},
            {"article_slug": "article-e", "paragraph_idx": 0, "text": "Convolutional networks excel at image recognition.", "url": "https://example.com/e"},
        ]
        _create_db(db_path, rows)

        results = retrieve_chunks.retrieve(project_dir, "attention", top_k=10)

        assert len(results) == 2
        slugs = {r["article_slug"] for r in results}
        assert slugs == {"article-a", "article-c"}


def test_fts5_empty_query():
    """Query a topic not present in the DB — should return []."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        db_path = project_dir / "chunks.sqlite"

        rows = [
            {"article_slug": "article-a", "paragraph_idx": 0, "text": "Transformers use attention.", "url": "https://example.com/a"},
        ]
        _create_db(db_path, rows)

        results = retrieve_chunks.retrieve(project_dir, "quantum computing", top_k=10)

        assert results == []


def test_fts5_missing_db():
    """If chunks.sqlite does not exist, return [] without crashing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        # Do NOT create chunks.sqlite

        results = retrieve_chunks.retrieve(project_dir, "transformers", top_k=10)

        assert results == []


def test_topk_limit():
    """20 rows match, top-k=10 — should return exactly 10."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        db_path = project_dir / "chunks.sqlite"

        keyword = "retrieval"
        rows = [
            {
                "article_slug": f"article-{i}",
                "paragraph_idx": 0,
                "text": f"Retrieval augmented generation example number {i}.",
                "url": f"https://example.com/{i}",
            }
            for i in range(20)
        ]
        _create_db(db_path, rows)

        results = retrieve_chunks.retrieve(project_dir, keyword, top_k=10)

        assert len(results) == 10


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------

def test_cli_outputs_json(tmp_path):
    """CLI invocation outputs valid JSON to stdout."""
    import subprocess

    db_path = tmp_path / "chunks.sqlite"
    rows = [
        {"article_slug": "art-1", "paragraph_idx": 0, "text": "Python is a programming language.", "url": "https://example.com/python"},
    ]
    _create_db(db_path, rows)

    script = Path(__file__).parent / "retrieve_chunks.py"
    result = subprocess.run(
        [sys.executable, str(script), "--project-dir", str(tmp_path), "--query", "Python programming"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["article_slug"] == "art-1"


def test_cli_missing_db_exits_zero(tmp_path):
    """CLI returns [] and exits 0 when DB is absent."""
    import subprocess

    script = Path(__file__).parent / "retrieve_chunks.py"
    result = subprocess.run(
        [sys.executable, str(script), "--project-dir", str(tmp_path), "--query", "anything"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert json.loads(result.stdout) == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
