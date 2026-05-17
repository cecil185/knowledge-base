# Digest Filter Eval — Portfolio Writeup

_Last updated: 2026-05-17_

---

## What this is

The `/digest` skill curates technical articles by running candidate URLs through an LLM filter. The filter reads a `goal.md` — a four-field statement of what I'm trying to learn — and classifies each article into three buckets: `auto-ticket` (create a Linear ticket immediately), `threshold` (show to me for a quick yes/no), or `drop` (discard silently).

This document tells the story of building a **labelled-eval harness** for that filter: why it matters, how it was built, what we measured, and what changed.

---

## Why evals for a personal digest?

The filter is the most differentiating part of the system — goal-aware content curation as an agentic loop. But without measurement, every change to `goal.md` or the filter prompt is a guess. We might improve recall while destroying precision, or shift the goal in a direction that quietly breaks the filter, and not know for months.

An eval harness turns the filter into a testable artifact:

- Run it against a labelled held-out set
- Get precision/recall/F1 back in seconds
- A/B compare prompt variants before shipping
- Detect regressions when `goal.md` drifts

This also produces a portfolio artifact that illustrates **eval-driven development for LLM systems** — a practice the industry is converging on but many teams haven't yet institutionalised.

---

## Professional eval framework landscape

Before building the harness, I surveyed the landscape:

| Framework | Strengths | Why not used here |
|-----------|-----------|-------------------|
| **Promptfoo** | YAML-driven, fast, built-in metrics | Overkill for single-skill eval; adds a dependency |
| **Inspect (UK AISI)** | Rigorous, task-based, research-grade | Steep learning curve; designed for capability evals |
| **DeepEval** | Python-native, pytest-style | Most ergonomic but adds Pydantic + heavy deps |
| **LangSmith** | Managed tracing + eval | Requires LangChain ecosystem |

**Decision:** Vanilla Python script (`scripts/eval_digest.py`). The labelled set is flat JSONL; the metrics are simple arithmetic; the reports are markdown committed alongside code. This matches the system's "no database, flat files" philosophy and keeps the runner cheap to re-run.

When the filter becomes more complex — multi-step reasoning, chain-of-thought explanations — migrating to DeepEval or Inspect would be a natural next step.

---

## The labelled set

**Location:** `evals/digest/labels.jsonl`

**Schema:**
```json
{
  "url": "https://...",
  "title": "Article Title",
  "surfaced_by": "hn | sources | manual",
  "keep": true,
  "reason": "One sentence explaining the keep/drop decision",
  "labeled_at": "2026-05-17",
  "unfetchable": false
}
```

**Labeling process:** Labels were assigned by hand from past digest runs. For each article, I asked: "If I'd seen this in my feed, would I have wanted it in my knowledge base?" The answer was driven by whether the article contained a concrete technique, tool, or case study I could apply to shipping faster with AI assistance — matching the goal's high-relevance signals.

**Current count:** 60 labelled examples across 7 weeks of digest runs (2026-03-29 through 2026-05-10).

**Class balance:** 30 keep / 28 drop / 2 unfetchable. Near-balanced by design — an imbalanced eval set flatters recall at the expense of precision.

**URL deduplication:** The runner normalises URLs (strips trailing slash, strips `utm_*` params) before dedup. If a URL appears twice, the later label wins.

---

## Variants tried

### v1 — Baseline (2026-05-10)

The production filter as shipped: three-bucket classification, strict auto-ticket gate, err toward `threshold` when uncertain.

**Result:** Precision 0.722 / Recall 0.867 / **F1 0.788**

**Key failure mode:** False positives clustered around trusted sources publishing off-goal content. Databricks, Airbnb Engineering, and Fly.io publishing platform/infra articles without an AI-workflow angle were slipping through as `threshold` items because the filter over-weighted source trust relative to topic relevance.

### v2 — Tighter auto-ticket gate (2026-05-17)

Added an explicit gate: the article must show evidence of *measurably reducing* human-review burden, not just describe AI coding in general.

**Result:** Precision 0.813 / Recall 0.833 / **F1 0.823**

**Delta vs v1:** F1 +0.035, Precision +0.091, Recall -0.034. The precision gain came from cutting 4 infrastructure false positives. The recall dip came from 1 new false negative (Dagster asset checks, which is genuinely borderline).

**Conclusion:** v2 adopted as production baseline.

---

## Metric trajectory

| Date | Variant | Precision | Recall | F1 |
|------|---------|-----------|--------|----|
| 2026-05-10 | v1 | 0.722 | 0.867 | 0.788 |
| 2026-05-17 | v2 | 0.813 | 0.833 | 0.823 |

F1 is moving in the right direction. The goal is to get above 0.85 — at that point the filter is good enough that I trust auto-tickets without spot-checking.

---

## Remaining disagreements

After v2, 5 false negatives and 6 false positives remain. Patterns:

**Persistent false negatives:**
- Trusted author, thin snippet (Eugene Yan, Martin Fowler) → filter uncertain, labels say keep
- Unfamiliar source with good content (jnxr.io) → filter drops on source signal

**Persistent false positives:**
- Trusted source + off-goal topic (Databricks ops, InfoQ platform releases) → `threshold` items surfacing to me unnecessarily
- Vendor SEO pattern not reliably detected when framing is plausible ("Complete Guide to E2E Testing")

**Next hypothesis (v3):** Add an explicit "must have AI workflow angle" drop signal for pure platform/infra content from trusted data-engineering sources. Also consider a mini-allowlist of trusted personal blogs that should get benefit of the doubt even with thin snippets.

---

## How to run the eval

```bash
# Install dependencies once
pip install anthropic pyyaml

# Set your API key
export ANTHROPIC_API_KEY=sk-...

# Run against full labels
python3 scripts/eval_digest.py --variant v2

# Dry-run (no LLM calls, mirrors labels as predictions)
python3 scripts/eval_digest.py --variant v2 --dry-run

# Sanity-check on fixture set (5 known examples)
python3 scripts/eval_digest.py --fixtures --dry-run

# Run tests
python3 scripts/test_eval_digest.py
```

Reports are written to `evals/digest/runs/` and committed alongside code so the metric trajectory is version-controlled.

---

## Labeling new examples

When new digest runs produce candidates, append them to `labels.jsonl` with `keep` set to the decision you made, and `labeled_at` set to today's date. Leave `unfetchable` out (defaults to false). After adding ≥10 new examples, re-run the eval to check for drift.

If an article is 404 or paywalled at eval time, add `"unfetchable": true` — it will be excluded from metrics but kept in the file for traceability.

---

## Connection to portfolio goals

This harness demonstrates:

1. **Eval-driven development for LLM systems** — treating a prompt as a versioned artifact with measurable quality, not a black box
2. **Lightweight but rigorous methodology** — flat files, committed reports, arithmetic metrics; no framework overhead
3. **Iterative prompt engineering** — A/B comparison with a written conclusion, not just vibes
4. **Awareness of the professional eval landscape** — Promptfoo, Inspect, DeepEval surveyed and deliberately not adopted for v1

The filter is a microcosm of the larger challenge in AI-assisted software: how do you know if a change to your AI system made it better or worse? The same pattern (labelled set + replay runner + metric report) applies to code review guardrails, test generation quality, and incident triage accuracy.
