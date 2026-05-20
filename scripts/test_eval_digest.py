"""
Tests for eval_digest.py — sanity-check the runner on the fixture set.

Run:
    python3 -m pytest scripts/test_eval_digest.py -v
    # or
    python3 scripts/test_eval_digest.py
"""

import json
import sys
import tempfile
from pathlib import Path

# Allow importing eval_digest without the package being installed
sys.path.insert(0, str(Path(__file__).parent))

import eval_digest as ed


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write_labels(tmp_dir: Path, rows: list[dict]) -> Path:
    path = tmp_dir / "labels.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows))
    return path


FIXTURE_ROWS = [
    {"url": "https://a.example.com/keep1", "title": "Good article", "surfaced_by": "hn",
     "keep": True, "reason": "concrete technique", "labeled_at": "2026-05-01"},
    {"url": "https://b.example.com/drop1", "title": "Bad article", "surfaced_by": "hn",
     "keep": False, "reason": "trend piece", "labeled_at": "2026-05-01"},
    {"url": "https://c.example.com/keep2", "title": "Great tool", "surfaced_by": "sources",
     "keep": True, "reason": "tool release", "labeled_at": "2026-05-01"},
    {"url": "https://d.example.com/drop2", "title": "Opinion", "surfaced_by": "hn",
     "keep": False, "reason": "no technique", "labeled_at": "2026-05-01"},
    {"url": "https://e.example.com/unfetchable", "title": "Paywalled", "surfaced_by": "hn",
     "keep": True, "reason": "would keep", "labeled_at": "2026-05-01", "unfetchable": True},
]


# ---------------------------------------------------------------------------
# load_labels
# ---------------------------------------------------------------------------

def test_load_labels_basic():
    with tempfile.TemporaryDirectory() as tmp:
        path = write_labels(Path(tmp), FIXTURE_ROWS)
        examples = ed.load_labels(path)
    assert len(examples) == 5
    assert examples[0].keep is True
    assert examples[4].unfetchable is True


def test_load_labels_dedup_keeps_latest():
    rows = [
        {"url": "https://x.example.com/page", "title": "First", "surfaced_by": "hn",
         "keep": False, "reason": "old", "labeled_at": "2026-01-01"},
        {"url": "https://x.example.com/page", "title": "Second", "surfaced_by": "hn",
         "keep": True, "reason": "updated", "labeled_at": "2026-05-01"},
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = write_labels(Path(tmp), rows)
        examples = ed.load_labels(path)
    assert len(examples) == 1
    assert examples[0].keep is True
    assert examples[0].title == "Second"


def test_load_labels_url_normalisation():
    rows = [
        {"url": "https://x.example.com/page/?utm_source=hn", "title": "T", "surfaced_by": "hn",
         "keep": True, "reason": "r", "labeled_at": "2026-05-01"},
        {"url": "https://x.example.com/page/", "title": "T2", "surfaced_by": "hn",
         "keep": False, "reason": "r2", "labeled_at": "2026-05-02"},
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = write_labels(Path(tmp), rows)
        examples = ed.load_labels(path)
    # utm_* stripped and trailing slash stripped → same URL → dedup → latest wins
    assert len(examples) == 1
    assert examples[0].keep is False


def test_load_labels_skips_unfetchable_in_metrics():
    with tempfile.TemporaryDirectory() as tmp:
        path = write_labels(Path(tmp), FIXTURE_ROWS)
        examples = ed.load_labels(path)

    # Build perfect predictions (excluding unfetchable)
    preds = [
        ed.Prediction(url=e.url, title=e.title, predicted_keep=e.keep,
                      raw_bucket="auto-ticket" if e.keep else "drop", llm_reason="")
        for e in examples if not e.unfetchable
    ]
    metrics = ed.compute_metrics(examples, preds)
    assert metrics["tp"] == 1.0  # 2 keep × 0.5 (auto-ticket bucket)
    assert metrics["tn"] == 2
    assert metrics["fp"] == 0
    assert metrics["fn"] == 0
    assert abs(metrics["f1"] - 1.0) < 1e-9


# ---------------------------------------------------------------------------
# compute_metrics
# ---------------------------------------------------------------------------

def test_compute_metrics_perfect():
    examples = [
        ed.LabeledExample("https://a.com/1", "A", "hn", True, "", "2026-01-01"),
        ed.LabeledExample("https://b.com/2", "B", "hn", False, "", "2026-01-01"),
    ]
    preds = [
        ed.Prediction("https://a.com/1", "A", True, "auto-ticket", ""),
        ed.Prediction("https://b.com/2", "B", False, "drop", ""),
    ]
    m = ed.compute_metrics(examples, preds)
    assert m["tp"] == 0.5  # auto-ticket bucket scores 0.5 TP
    assert m["tn"] == 1
    assert m["fp"] == 0
    assert m["fn"] == 0
    assert abs(m["precision"] - 1.0) < 1e-9
    assert abs(m["recall"] - 1.0) < 1e-9
    assert abs(m["f1"] - 1.0) < 1e-9


def test_compute_metrics_all_false_positive():
    examples = [
        ed.LabeledExample("https://a.com/1", "A", "hn", False, "", "2026-01-01"),
    ]
    preds = [
        ed.Prediction("https://a.com/1", "A", True, "auto-ticket", ""),
    ]
    m = ed.compute_metrics(examples, preds)
    assert m["fp"] == 1
    assert m["precision"] == 0.0
    # recall undefined when no positives → 0
    assert m["f1"] == 0.0


def test_compute_metrics_skips_errors():
    examples = [
        ed.LabeledExample("https://a.com/1", "A", "hn", True, "", "2026-01-01"),
    ]
    preds = [
        ed.Prediction("https://a.com/1", "A", False, "error", "", error="timeout"),
    ]
    m = ed.compute_metrics(examples, preds)
    # Error predictions are skipped
    assert m["tp"] == 0
    assert m["fn"] == 0
    assert m["fp"] == 0
    assert m["tn"] == 0


# ---------------------------------------------------------------------------
# _normalize_url
# ---------------------------------------------------------------------------

def test_normalize_url_strips_trailing_slash():
    assert ed._normalize_url("https://a.com/page/") == "https://a.com/page"


def test_normalize_url_strips_utm():
    url = "https://a.com/page?utm_source=hn&utm_medium=link"
    assert "utm" not in ed._normalize_url(url)


def test_normalize_url_keeps_path():
    url = "https://a.com/blog/post-title"
    assert ed._normalize_url(url) == url


# ---------------------------------------------------------------------------
# load_filter_prompt
# ---------------------------------------------------------------------------

def test_load_filter_prompt_strips_frontmatter():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False) as f:
        f.write("---\nname: test\n---\n# Body\n\nContent here.\n")
        path = Path(f.name)
    try:
        body = ed.load_filter_prompt(path)
        assert body.startswith("# Body")
        assert "---" not in body.split("\n")[0]
    finally:
        path.unlink()


def test_load_filter_prompt_no_frontmatter():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False) as f:
        f.write("# Just content\n")
        path = Path(f.name)
    try:
        body = ed.load_filter_prompt(path)
        assert "# Just content" in body
    finally:
        path.unlink()


# ---------------------------------------------------------------------------
# write_report (dry-run)
# ---------------------------------------------------------------------------

def test_write_report_dry_run(capsys):
    examples = [
        ed.LabeledExample("https://a.com/1", "Keep This", "hn", True, "good", "2026-05-01"),
        ed.LabeledExample("https://b.com/2", "Drop This", "hn", False, "bad", "2026-05-01"),
    ]
    preds = [
        ed.Prediction("https://a.com/1", "Keep This", True, "auto-ticket", "matches goal"),
        ed.Prediction("https://b.com/2", "Drop This", False, "drop", "trend piece"),
    ]
    metrics = ed.compute_metrics(examples, preds)
    result = ed.RunResult(
        variant_name="v1",
        labels_file="evals/digest/labels.jsonl",
        
        goal_snippet="What: ship faster...",
        examples=examples,
        predictions=preds,
    )

    with tempfile.TemporaryDirectory() as tmp:
        runs_dir = Path(tmp) / "runs"
        ed.write_report(result, metrics, runs_dir, dry_run=True)

    captured = capsys.readouterr()
    assert "Precision" in captured.out
    assert "F1" in captured.out
    assert "dry-run" in captured.out


def test_write_report_writes_file():
    examples = [
        ed.LabeledExample("https://a.com/1", "Keep This", "hn", True, "good", "2026-05-01"),
        ed.LabeledExample("https://b.com/2", "Drop This", "hn", False, "bad", "2026-05-01"),
    ]
    preds = [
        ed.Prediction("https://a.com/1", "Keep This", True, "auto-ticket", ""),
        ed.Prediction("https://b.com/2", "Drop This", False, "drop", ""),
    ]
    metrics = ed.compute_metrics(examples, preds)
    result = ed.RunResult(
        variant_name="v1",
        labels_file="evals/digest/labels.jsonl",
        
        goal_snippet="What: ship faster...",
        examples=examples,
        predictions=preds,
    )

    with tempfile.TemporaryDirectory() as tmp:
        runs_dir = Path(tmp) / "runs"
        report_path = ed.write_report(result, metrics, runs_dir)
        assert report_path.exists()
        content = report_path.read_text()
        assert "Precision" in content
        assert "F1" in content
        assert "Confusion matrix" in content


# ---------------------------------------------------------------------------
# Simple test runner (no pytest required)
# ---------------------------------------------------------------------------

def _run_tests():
    import traceback
    tests = [
        test_load_labels_basic,
        test_load_labels_dedup_keeps_latest,
        test_load_labels_url_normalisation,
        test_load_labels_skips_unfetchable_in_metrics,
        test_compute_metrics_perfect,
        test_compute_metrics_all_false_positive,
        test_compute_metrics_skips_errors,
        test_normalize_url_strips_trailing_slash,
        test_normalize_url_strips_utm,
        test_normalize_url_keeps_path,
        test_load_filter_prompt_strips_frontmatter,
        test_load_filter_prompt_no_frontmatter,
        test_write_report_writes_file,
    ]

    passed = failed = 0
    for t in tests:
        try:
            # Inject a dummy capsys for tests that use it
            if "capsys" in t.__code__.co_varnames:
                continue  # skip capsys tests in non-pytest mode
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
