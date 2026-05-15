---
title: Risk-Tiered Review
updated: 2026-05-15
sources: [raw/propel-agentic-code-review-guardrails.md]
related: [guardrails-for-ai-coding, ai-attributed-defect-tracking, verifiability-boundary, agentic-coding, verification-bottleneck]
---
## Summary
Risk-tiered review classifies every change by blast radius and requires proof commensurate with that risk. Docs and refactors merge on lint + unit tests; auth/billing/data changes require AI review plus AppSec plus explicit security evidence. The principle is to spend reviewer attention where defects are catastrophic, not uniformly.

## Details

### The three tiers
Propel's framework:

**Low risk — AI-only path.**
- Examples: documentation, comments, formatting, internal refactors with stable interfaces.
- Required proof: lint + unit tests.
- Reviewers: AI review only; no human gate.
- Goal: keep these out of the human queue entirely.

**Medium risk — AI + human path.**
- Examples: business logic, internal APIs, feature additions touching existing flows.
- Required proof: integration tests passing + AI review + one human reviewer.
- Goal: human judgment on intent and correctness, with AI catching mechanical issues first.

**High risk — AI + AppSec + evidence path.**
- Examples: authentication, authorization, billing, payments, PII handling, data access boundaries.
- Required proof: AI review + AppSec review + security scans + explicit evidence (threat model update, test cases for adverse inputs, deployment plan).
- Goal: no high-risk change merges on optimism.

### Blast radius assessment
Tier is determined automatically where possible:
- File path heuristics (`auth/`, `billing/`, `migrations/` → High).
- Diff heuristics (many files, large churn → at least Medium).
- Dependency reach (does it touch a public API or shared library?).
- Data sensitivity (does it touch PII tables or secrets?).

When uncertain, escalate up — false positives cost time, false negatives cost incidents.

### Metrics that prove it works
Track three numbers to know whether the tiering is calibrated:

- **Defect escape rate** by tier — should be near-zero for High, low for Medium, tolerable for Low.
- **Review usefulness** — fraction of review comments that lead to changes. If Low-tier comments are mostly noise, the gate is too strict; if High-tier comments routinely catch real bugs, the gate is paying for itself.
- **Time-to-merge** by tier — Low should be minutes, High can be days. If Low is slow, the AI-only path isn't being trusted.

### Review signal degradation
Tiering is a direct response to the observation (see [[Guardrails for AI Coding]]) that review quality degrades with file count and PR volume. Without tiering, every change competes for the same scarce reviewer attention; with tiering, attention concentrates where it matters.

## Tradeoffs / When to use
- **Gain:** fast merges on safe changes, real scrutiny on dangerous ones, predictable throughput.
- **Cost:** classification infrastructure; risk of miscategorization; cultural agreement on what "High" means.
- **Fits:** any codebase with mixed-criticality surfaces (most production codebases).
- **Poor fit:** uniformly high-risk systems (medical, avionics) where every change is High by default; or uniformly low-risk experiments where tiering adds ceremony for no gain.

## Key tools / implementations
- [[Propel]] — primary articulation of the 3-tier model with automated routing.
- [[CodeRabbit]] — AI review gate that plugs into the Medium and High tiers.

## Sources
- [[raw/propel-agentic-code-review-guardrails]] — 3-tier model, blast radius assessment, defect escape / review usefulness / time-to-merge metrics.

## Backlinks
- [[AI-Attributed Defect Tracking]]
- [[Claude Code]]
- [[CodeRabbit]]
- [[CodeScene]]
- [[Iterative Chunking]]
- [[Verification Bottleneck]]
