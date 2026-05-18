# Digest Filter Eval — Portfolio Writeup

_Last updated: 2026-05-17_

---

## What this is

The `/digest` skill curates technical articles by running candidate URLs through an LLM filter. The filter reads a `goal.md` — a four-field statement of what I'm trying to learn — and classifies each article into three buckets: `auto-ticket` (create a Linear ticket immediately), `threshold` (show me for a quick yes/no), or `drop` (discard silently).

This document tells the story of building a **labelled-eval harness** for that filter: why it matters, how it was built, and how it will grow.

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
  "linear_id": "CC-9",
  "unfetchable": false
}
```

**Labeling process:** The seed set was reconstructed from the project's actual Linear ticket history (CC-9 through CC-28). The keep/drop decision was derived directly from each ticket's final state:

- `keep=true` if the article ticket remained in the project (status Done or In Progress without the `delete-from-wiki` label) — meaning the filter's decision to surface it was validated by the operator after reading
- `keep=false` if the ticket was Canceled with the `delete-from-wiki` label — meaning the filter surfaced something the operator ultimately judged off-goal after reading

This is real signal, not synthetic: every label corresponds to an article I actually read or skimmed and made a keep/discard decision on.

**Current count:** 18 examples (11 keep / 7 drop). Below the ideal ≥50 — the system has only been running a few weeks — but it's an honest starting point. The set will grow each digest run as new candidates get surfaced and decided.

**URL deduplication:** The runner normalises URLs (strips trailing slash, strips `utm_*` params) before dedup. If a URL appears twice, the later label wins.

---

## Variants

The variant registry lives at `evals/digest/variants.yaml`. Each variant ties a filter-prompt file to a `goal.md` hash.

Currently there is one variant (`v1`) — the production baseline. Adding `v2` is a one-line YAML change pointing to a different prompt file: the runner will automatically use that variant's prompt when invoked with `--variant v2`.

**First live run is pending** — once an `ANTHROPIC_API_KEY` is set and `just eval` is run, the baseline metrics will be recorded in `evals/digest/runs/`. From there each prompt change can be A/B tested against the baseline.

---

## How to run the eval

```bash
# Install dependencies once
pip install anthropic pyyaml

# Set your API key
export ANTHROPIC_API_KEY=sk-...

# Run against full labels (writes report to evals/digest/runs/)
just eval-filter               # variant=v1 by default
just eval-filter variant=v2    # if v2 exists in variants.yaml

# Dry-run (no LLM calls, mirrors labels as predictions — sanity-checks report format)
just eval-filter-dry

# Sanity-check on fixture set (5 known examples)
just eval-filter-fixtures

# Run unit tests
just test
```

Reports are written to `evals/digest/runs/` and committed alongside code so the metric trajectory is version-controlled.

---

## Labeling new examples

Use the sync script — it reads ticket state from Linear and appends any URLs not already in `labels.jsonl`. The keep/drop derivation is the same rule used to build the seed set:

- Canceled with `delete-from-wiki` label → `keep=false`
- Otherwise → `keep=true`

```bash
export LINEAR_API_KEY=lin_api_...          # one-time setup
just sync-filter-labels-dry                 # preview what would be added
just sync-filter-labels                     # actually append
```

The auto-filled `reason` field is generic ("Auto-synced from Linear …") — edit it to capture the *why* of the keep/drop decision before committing. That nuance is what makes the labelled set valuable later when investigating disagreements.

If an article is 404 or paywalled at eval time, add `"unfetchable": true` — it will be excluded from metrics but kept in the file for traceability.

---

## Connection to portfolio goals

This harness demonstrates:

1. **Eval-driven development for LLM systems** — treating a prompt as a versioned artifact with measurable quality, not a black box
2. **Lightweight but rigorous methodology** — flat files, committed reports, arithmetic metrics; no framework overhead
3. **Iterative prompt engineering** — variant registry + A/B comparison built in from day one
4. **Awareness of the professional eval landscape** — Promptfoo, Inspect, DeepEval surveyed and deliberately not adopted for v1
5. **Honest reporting** — small real seed set rather than a fabricated large one; the methodology stands even when the data is sparse

The filter is a microcosm of the larger challenge in AI-assisted software: how do you know if a change to your AI system made it better or worse? The same pattern (labelled set + replay runner + metric report) applies to code review guardrails, test generation quality, and incident triage accuracy.
