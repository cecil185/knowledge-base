#!/usr/bin/env python3
"""
Eval runner for the /digest filter.

Replays labelled articles through the current filter logic and computes
precision/recall/F1. Writes a markdown report to evals/digest/runs/.

Usage:
    python3 scripts/eval_digest.py [--variant v1] [--labels evals/digest/labels.jsonl]
                                   [--project data-ai-engineering] [--dry-run]

Requirements:
    pip install anthropic pyyaml

Environment:
    ANTHROPIC_API_KEY — required for live filter calls; omit with --dry-run
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

# anthropic and yaml are optional at import time; imported lazily so --help works without them
ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class LabeledExample:
    url: str
    title: str
    surfaced_by: str
    keep: bool
    reason: str
    labeled_at: str
    unfetchable: bool = False


@dataclass
class Prediction:
    url: str
    title: str
    predicted_keep: bool
    raw_bucket: str      # "auto-ticket" | "threshold" | "drop"
    llm_reason: str
    error: str = ""      # non-empty if the LLM call failed


@dataclass
class RunResult:
    variant_name: str
    labels_file: str
    goal_hash: str
    goal_snippet: str    # first 200 chars of goal.md
    examples: list[LabeledExample] = field(default_factory=list)
    predictions: list[Prediction] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def compute_metrics(examples: list[LabeledExample], predictions: list[Prediction]):
    pred_map = {p.url: p for p in predictions}
    tp = fp = fn = tn = 0
    disagreements = []

    for ex in examples:
        if ex.unfetchable:
            continue
        pred = pred_map.get(ex.url)
        if pred is None or pred.error:
            continue
        if ex.keep and pred.predicted_keep:
            tp += 1
        elif ex.keep and not pred.predicted_keep:
            fn += 1
            disagreements.append((ex, pred, "false_negative"))
        elif not ex.keep and pred.predicted_keep:
            fp += 1
            disagreements.append((ex, pred, "false_positive"))
        else:
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": precision, "recall": recall, "f1": f1,
        "disagreements": disagreements,
    }


# ---------------------------------------------------------------------------
# Filter prompt loader
# ---------------------------------------------------------------------------

def load_filter_prompt(prompt_file: Path) -> str:
    text = prompt_file.read_text()
    # Strip YAML frontmatter if present
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return text


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# LLM filter call
# ---------------------------------------------------------------------------

def call_filter(article: LabeledExample, prompt_body: str, goal_text: str) -> Prediction:
    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic package not installed. Run: pip install anthropic")

    client = anthropic.Anthropic()

    system = f"""You are the filter-articles classifier for a personal learning digest.

Active project goal.md:
---
{goal_text}
---

{prompt_body}
"""
    user = (
        f"Classify this single article. Output ONLY one of: auto-ticket, threshold, or drop — "
        f"followed by a one-sentence reason.\n\n"
        f"Title: {article.title}\n"
        f"URL: {article.url}\n"
        f"Surfaced by: {article.surfaced_by}\n"
        f"Snippet: (not available — classify from title and source only)"
    )

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=128,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        raw = msg.content[0].text.strip().lower()
    except Exception as e:
        return Prediction(
            url=article.url,
            title=article.title,
            predicted_keep=False,
            raw_bucket="error",
            llm_reason="",
            error=str(e),
        )

    # Parse bucket from response
    bucket = "drop"
    if "auto-ticket" in raw:
        bucket = "auto-ticket"
    elif "threshold" in raw:
        bucket = "threshold"

    # threshold → keep (user would approve most threshold items; eval treats as keep)
    predicted_keep = bucket in ("auto-ticket", "threshold")

    # Extract reason sentence (everything after the bucket keyword)
    reason_match = re.search(r'(auto-ticket|threshold|drop)[:\s—-]*(.*)', raw, re.DOTALL)
    llm_reason = reason_match.group(2).strip() if reason_match else raw[:120]

    return Prediction(
        url=article.url,
        title=article.title,
        predicted_keep=predicted_keep,
        raw_bucket=bucket,
        llm_reason=llm_reason,
    )


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def write_report(result: RunResult, metrics: dict, runs_dir: Path, dry_run: bool = False) -> Path:
    today = date.today().isoformat()
    commit = _git_short_hash()
    filename = f"{today}-{commit}-{result.variant_name}.md"
    report_path = runs_dir / filename

    keep_count = sum(1 for e in result.examples if e.keep and not e.unfetchable)
    drop_count = sum(1 for e in result.examples if not e.keep and not e.unfetchable)
    skip_count = sum(1 for e in result.examples if e.unfetchable)
    error_count = sum(1 for p in result.predictions if p.error)

    disagreements = metrics["disagreements"]
    fn_items = [(ex, pred) for ex, pred, kind in disagreements if kind == "false_negative"]
    fp_items = [(ex, pred) for ex, pred, kind in disagreements if kind == "false_positive"]

    # Drift watch: compare against previous run if one exists
    drift_section = _build_drift_section(runs_dir, metrics, result.variant_name, filename)

    lines = [
        f"# Digest Filter Eval — {today}",
        "",
        f"**Variant:** `{result.variant_name}`  ",
        f"**Commit:** `{commit}`  ",
        f"**Labels file:** `{result.labels_file}`  ",
        f"**Goal snapshot (SHA-256):** `{result.goal_hash[:12]}…`  ",
        "",
        "---",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Precision | {metrics['precision']:.3f} |",
        f"| Recall | {metrics['recall']:.3f} |",
        f"| F1 | {metrics['f1']:.3f} |",
        "",
        "### Confusion matrix",
        "",
        "| | Predicted keep | Predicted drop |",
        "|---|---|---|",
        f"| **Labelled keep** | TP={metrics['tp']} | FN={metrics['fn']} |",
        f"| **Labelled drop** | FP={metrics['fp']} | TN={metrics['tn']} |",
        "",
        f"Labelled set: {keep_count} keep, {drop_count} drop",
        f"Skipped (unfetchable): {skip_count}  |  Errors: {error_count}",
        "",
        "---",
        "",
        "## Disagreements",
        "",
    ]

    if not disagreements:
        lines.append("_No disagreements — filter and labels agree on every example._")
    else:
        if fn_items:
            lines += [
                f"### False negatives ({len(fn_items)}) — filter dropped, label says keep",
                "",
            ]
            for ex, pred in fn_items:
                lines += [
                    f"- **{ex.title}**",
                    f"  URL: {ex.url}",
                    f"  Label reason: {ex.reason}",
                    f"  Filter said: `{pred.raw_bucket}` — {pred.llm_reason}",
                    "",
                ]

        if fp_items:
            lines += [
                f"### False positives ({len(fp_items)}) — filter kept, label says drop",
                "",
            ]
            for ex, pred in fp_items:
                lines += [
                    f"- **{ex.title}**",
                    f"  URL: {ex.url}",
                    f"  Label reason: {ex.reason}",
                    f"  Filter said: `{pred.raw_bucket}` — {pred.llm_reason}",
                    "",
                ]

    lines += [
        "---",
        "",
        "## Variant used",
        "",
        f"**{result.variant_name}** — see `evals/digest/variants.yaml` for prompt and goal details.",
        "",
        "### Goal snapshot (first 200 chars)",
        "",
        "```",
        result.goal_snippet,
        "```",
        "",
        "---",
        "",
        drift_section,
    ]

    report = "\n".join(lines)

    if dry_run:
        print(report)
        print(f"\n[dry-run] Would write to: {report_path}")
        return report_path

    runs_dir.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    print(f"Report written to: {report_path}")
    return report_path


def _build_drift_section(runs_dir: Path, current_metrics: dict, variant: str, current_file: str) -> str:
    """Compare current run against most recent previous run of the same variant."""
    prev_reports = sorted(
        [f for f in runs_dir.glob(f"*-{variant}.md") if f.name != current_file]
    )
    if not prev_reports:
        return "## Drift watch\n\n_No previous run found for this variant — baseline established._"

    prev_path = prev_reports[-1]
    prev_text = prev_path.read_text()

    def _extract(text, key):
        m = re.search(rf"\| {key} \| ([0-9.]+) \|", text)
        return float(m.group(1)) if m else None

    prev_f1 = _extract(prev_text, "F1")
    prev_precision = _extract(prev_text, "Precision")
    prev_recall = _extract(prev_text, "Recall")

    if prev_f1 is None:
        return "## Drift watch\n\n_Could not parse previous run metrics._"

    delta_f1 = current_metrics["f1"] - prev_f1
    flag = " ⚠️ REGRESSION" if delta_f1 < -0.03 else (" ✅ improvement" if delta_f1 > 0.01 else "")

    return "\n".join([
        "## Drift watch",
        "",
        f"Compared against: `{prev_path.name}`",
        "",
        "| Metric | Previous | Current | Delta |",
        "|--------|----------|---------|-------|",
        f"| Precision | {prev_precision:.3f} | {current_metrics['precision']:.3f} | {current_metrics['precision'] - prev_precision:+.3f} |",
        f"| Recall | {prev_recall:.3f} | {current_metrics['recall']:.3f} | {current_metrics['recall'] - prev_recall:+.3f} |",
        f"| F1 | {prev_f1:.3f} | {current_metrics['f1']:.3f} | {delta_f1:+.3f}{flag} |",
        "",
    ])


def _git_short_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return "unknown"


# ---------------------------------------------------------------------------
# Labels loader
# ---------------------------------------------------------------------------

def load_labels(path: Path) -> list[LabeledExample]:
    if not path.exists():
        sys.exit(f"Labels file not found: {path}")

    examples = []
    seen_urls: dict[str, int] = {}

    for line_no, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"[warn] Skipping malformed line {line_no}: {e}", file=sys.stderr)
            continue

        url = _normalize_url(row.get("url", ""))
        if not url:
            print(f"[warn] Skipping line {line_no}: missing url", file=sys.stderr)
            continue

        if url in seen_urls:
            print(
                f"[warn] Duplicate URL on line {line_no} (first seen line {seen_urls[url]}): {url}",
                file=sys.stderr,
            )
            # Keep the most recent (later line wins)
            examples = [e for e in examples if _normalize_url(e.url) != url]

        seen_urls[url] = line_no
        examples.append(LabeledExample(
            url=url,
            title=row.get("title", ""),
            surfaced_by=row.get("surfaced_by", "manual"),
            keep=bool(row.get("keep", False)),
            reason=row.get("reason", ""),
            labeled_at=row.get("labeled_at", ""),
            unfetchable=bool(row.get("unfetchable", False)),
        ))

    return examples


def _normalize_url(url: str) -> str:
    """Strip trailing slash and utm_* params for dedup."""
    url = re.sub(r"[?&]utm_[^&]*", "", url)
    url = re.sub(r"[?&]$", "", url)
    url = url.rstrip("/")
    return url


# ---------------------------------------------------------------------------
# Variant loader
# ---------------------------------------------------------------------------

def load_variant(variants_file: Path, name: str) -> dict:
    try:
        import yaml
    except ImportError:
        sys.exit("pyyaml not installed. Run: pip install pyyaml")

    data = yaml.safe_load(variants_file.read_text())
    for v in data.get("variants", []):
        if v["name"] == name:
            return v
    available = [v["name"] for v in data.get("variants", [])]
    sys.exit(f"Variant '{name}' not found. Available: {available}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Eval runner for /digest filter")
    parser.add_argument("--variant", default="v1", help="Variant name from variants.yaml")
    parser.add_argument(
        "--labels",
        default="evals/digest/labels.jsonl",
        help="Path to labels JSONL file",
    )
    parser.add_argument(
        "--project",
        default="data-ai-engineering",
        help="Project slug (used to find goal.md)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print report to stdout instead of writing file; skip LLM calls",
    )
    parser.add_argument(
        "--fixtures",
        action="store_true",
        help="Run against fixture set instead of full labels (fast sanity check)",
    )
    args = parser.parse_args()

    labels_path = ROOT / (
        "evals/digest/fixtures/labels.jsonl" if args.fixtures else args.labels
    )
    variants_file = ROOT / "evals/digest/variants.yaml"
    goal_path = ROOT / f"projects/{args.project}/goal.md"
    runs_dir = ROOT / "evals/digest/runs"

    if not goal_path.exists():
        sys.exit(f"goal.md not found: {goal_path}\nRun /goal-refine first.")

    variant = load_variant(variants_file, args.variant)
    prompt_path = ROOT / variant["prompt_file"]
    if not prompt_path.exists():
        sys.exit(f"Variant '{args.variant}' prompt_file not found: {prompt_path}")
    prompt_body = load_filter_prompt(prompt_path)
    goal_text = goal_path.read_text()
    goal_hash = hash_file(goal_path)
    goal_snippet = goal_text[:200].replace("\n", " ").strip()

    examples = load_labels(labels_path)
    if not examples:
        print("Labels file is empty. Add labelled examples to", labels_path)
        return

    print(f"Loaded {len(examples)} examples from {labels_path}")
    keep_n = sum(1 for e in examples if e.keep)
    drop_n = sum(1 for e in examples if not e.keep)
    print(f"  {keep_n} keep / {drop_n} drop")

    predictions: list[Prediction] = []

    if args.dry_run:
        print("[dry-run] Skipping LLM calls — using label as prediction")
        for ex in examples:
            predictions.append(Prediction(
                url=ex.url,
                title=ex.title,
                predicted_keep=ex.keep,
                raw_bucket="auto-ticket" if ex.keep else "drop",
                llm_reason="(dry-run: mirrored from label)",
            ))
    else:
        total = len([e for e in examples if not e.unfetchable])
        processed = 0
        for ex in examples:
            if ex.unfetchable:
                continue
            processed += 1
            print(f"  [{processed}/{total}] {ex.title[:60]}…")
            pred = call_filter(ex, prompt_body, goal_text)
            if pred.error:
                print(f"    [error] {pred.error}", file=sys.stderr)
            predictions.append(pred)

    metrics = compute_metrics(examples, predictions)

    print(f"\nResults:")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall:    {metrics['recall']:.3f}")
    print(f"  F1:        {metrics['f1']:.3f}")
    print(f"  TP={metrics['tp']} FP={metrics['fp']} FN={metrics['fn']} TN={metrics['tn']}")
    print(f"  Disagreements: {len(metrics['disagreements'])}")

    result = RunResult(
        variant_name=args.variant,
        labels_file=str(labels_path.relative_to(ROOT)),
        goal_hash=goal_hash,
        goal_snippet=goal_snippet,
        examples=examples,
        predictions=predictions,
    )

    write_report(result, metrics, runs_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
