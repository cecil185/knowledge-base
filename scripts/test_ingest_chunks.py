"""
Tests for ingest_chunks.py.

Run:
    python3 -m pytest scripts/test_ingest_chunks.py -v
    # or
    python3 scripts/test_ingest_chunks.py
"""

import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import ingest_chunks as ic


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SIMPLE_BODY = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."


def _db_path(project_dir: Path) -> Path:
    return project_dir / "chunks.sqlite"


def _get_rows(db: Path, slug: str) -> list[dict]:
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM chunks WHERE article_slug = ? ORDER BY paragraph_idx",
        (slug,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# test_db_created
# ---------------------------------------------------------------------------

def test_db_created():
    """First run creates chunks.sqlite with chunks table and FTS5 virtual table."""
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        db = _db_path(project_dir)

        assert not db.exists()

        ic.ingest(
            slug="test-article",
            url="https://example.com/test",
            project_dir=project_dir,
            body=SIMPLE_BODY,
        )

        assert db.exists()

        conn = sqlite3.connect(db)
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table')").fetchall()}
        conn.close()

        assert "chunks" in tables
        assert "chunks_fts" in tables


# ---------------------------------------------------------------------------
# test_paragraphs_inserted
# ---------------------------------------------------------------------------

def test_paragraphs_inserted():
    """3-paragraph article inserts 3 rows; paragraph_idx is 0/1/2."""
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ic.ingest(
            slug="test-article",
            url="https://example.com/test",
            project_dir=project_dir,
            body=SIMPLE_BODY,
        )

        rows = _get_rows(_db_path(project_dir), "test-article")
        assert len(rows) == 3
        assert rows[0]["paragraph_idx"] == 0
        assert rows[1]["paragraph_idx"] == 1
        assert rows[2]["paragraph_idx"] == 2


# ---------------------------------------------------------------------------
# test_char_offsets
# ---------------------------------------------------------------------------

def test_char_offsets():
    """char_start/char_end of each row satisfies text == full_body[char_start:char_end]."""
    body = "Alpha paragraph.\n\nBeta paragraph.\n\nGamma paragraph."
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ic.ingest(
            slug="offsets-article",
            url="https://example.com/offsets",
            project_dir=project_dir,
            body=body,
        )

        rows = _get_rows(_db_path(project_dir), "offsets-article")
        for row in rows:
            assert row["text"] == body[row["char_start"]:row["char_end"]], (
                f"paragraph_idx={row['paragraph_idx']}: "
                f"text={row['text']!r} != body[{row['char_start']}:{row['char_end']}]={body[row['char_start']:row['char_end']]!r}"
            )


# ---------------------------------------------------------------------------
# test_idempotent
# ---------------------------------------------------------------------------

def test_idempotent():
    """Running twice for same slug yields same row count (no duplicates)."""
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ic.ingest(
            slug="idem-article",
            url="https://example.com/idem",
            project_dir=project_dir,
            body=SIMPLE_BODY,
        )
        ic.ingest(
            slug="idem-article",
            url="https://example.com/idem",
            project_dir=project_dir,
            body=SIMPLE_BODY,
        )

        rows = _get_rows(_db_path(project_dir), "idem-article")
        assert len(rows) == 3


# ---------------------------------------------------------------------------
# test_empty_paragraphs_skipped
# ---------------------------------------------------------------------------

def test_empty_paragraphs_skipped():
    """Multiple blank lines between paragraphs → only content paragraphs inserted."""
    body = "First paragraph.\n\n\n\nSecond paragraph.\n\n\n\n\nThird paragraph."
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ic.ingest(
            slug="blank-lines-article",
            url="https://example.com/blank",
            project_dir=project_dir,
            body=body,
        )

        rows = _get_rows(_db_path(project_dir), "blank-lines-article")
        assert len(rows) == 3
        assert rows[0]["text"] == "First paragraph."
        assert rows[1]["text"] == "Second paragraph."
        assert rows[2]["text"] == "Third paragraph."


# ---------------------------------------------------------------------------
# test_fts_queryable
# ---------------------------------------------------------------------------

def test_fts_queryable():
    """FTS5 index is populated so MATCH queries return results."""
    body = "Machine learning transforms data.\n\nNeural networks use backpropagation."
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ic.ingest(
            slug="fts-article",
            url="https://example.com/fts",
            project_dir=project_dir,
            body=body,
        )

        db = _db_path(project_dir)
        conn = sqlite3.connect(db)
        rows = conn.execute(
            "SELECT text FROM chunks_fts WHERE chunks_fts MATCH 'neural'"
        ).fetchall()
        conn.close()

        assert len(rows) == 1
        assert "Neural" in rows[0][0]


# ---------------------------------------------------------------------------
# test_paywall_skip
# ---------------------------------------------------------------------------

def test_paywall_skip():
    """Empty body → zero rows inserted, exits cleanly."""
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ic.ingest(
            slug="paywall-article",
            url="https://example.com/paywall",
            project_dir=project_dir,
            body="",
        )

        rows = _get_rows(_db_path(project_dir), "paywall-article")
        assert len(rows) == 0


# ---------------------------------------------------------------------------
# test_frontmatter_stripped
# ---------------------------------------------------------------------------

def test_frontmatter_stripped():
    """YAML frontmatter is not inserted as a chunk row."""
    frontmatter = "---\nurl: https://example.com/test\nfetched: 2026-05-17\ntitle: Test Article\nunfetched: false\n---"
    body = f"{frontmatter}\n\nFirst real paragraph.\n\nSecond real paragraph."
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)

        ic.ingest(
            slug="fm-article",
            url="https://example.com/test",
            project_dir=project_dir,
            body=body,
        )

        rows = _get_rows(_db_path(project_dir), "fm-article")
        assert len(rows) == 2
        texts = [r["text"] for r in rows]
        assert all("---" not in t for t in texts), "frontmatter leaked into chunks"
        assert texts[0] == "First real paragraph."
        assert texts[1] == "Second real paragraph."


# ---------------------------------------------------------------------------
# Simple test runner (no pytest required)
# ---------------------------------------------------------------------------

def _run_tests():
    import traceback
    tests = [
        test_db_created,
        test_paragraphs_inserted,
        test_char_offsets,
        test_idempotent,
        test_empty_paragraphs_skipped,
        test_fts_queryable,
        test_paywall_skip,
        test_frontmatter_stripped,
    ]

    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception:
            print(f"  FAIL  {t.__name__}")
            traceback.print_exc()
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    sys.exit(_run_tests())
