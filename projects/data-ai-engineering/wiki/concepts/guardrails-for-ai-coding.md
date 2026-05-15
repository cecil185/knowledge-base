---
title: Guardrails for AI Coding
updated: 2026-05-15
sources: [raw/propel-agentic-code-review-guardrails.md, raw/codescene-guardrails-metrics-ai-coding.md, raw/coderabbit-ai-speed-vs-quality-2026.md, raw/tfir-ai-code-quality-guardrails-2026.md]
related: [risk-tiered-review, ai-attributed-defect-tracking, verifiability-boundary, code-comprehension-bottleneck, agentic-coding]
---
## Summary
Guardrails are the layered review, test, and policy infrastructure that keeps AI-generated code safe at high velocity. They convert raw agent throughput into shippable output by enforcing proof commensurate with risk, gating merges on objective signals, and escalating to humans only where judgment is required.

## Details

### Propel's 5-layer stack
Propel frames guardrails as a stack where each layer filters what the next must consider:

1. **Policy checks** — static rules, license/secret scans, dependency policy.
2. **Test proof** — required unit/integration runs that must pass before review.
3. **Diff heuristics** — blast-radius classification, file count, churn, sensitive-path detection.
4. **AI review gates** — automated review for logic, style, security smells.
5. **Human escalation** — reserved for changes that cleared the lower layers but still require judgment.

The stack is explicitly designed so that review signal degrades with file count: large diffs overwhelm reviewers (human and AI), so the early layers exist to keep diffs small and well-scoped before any human looks.

### CodeScene's 3 guardrails
CodeScene reduces the problem to three dimensions that must all be healthy:

1. **Code quality** — auto-blocks on code-health regressions in AI-touched files.
2. **Code familiarity** — tracks who has actually read and modified the code; AI-only code creates knowledge silos. Developers spend 93% more time in unfamiliar code, so familiarity is a maintenance KPI, not a vanity metric.
3. **Test coverage with HUMAN-written tests** — AI tests cannot verify AI code. Tests must come from a different cognitive source than the implementation, or they encode the same bugs.

### Quality gates as infrastructure
Both CodeRabbit and TFiR frame guardrails as production infrastructure, not optional tooling. KPIs shift from velocity (PR volume, cycle time) to quality (defect density, review confidence, merge reliability, coverage). The throughput-to-trust pivot makes guardrails a load-bearing system: without them, the 1.7x defect multiplier of AI-generated code compounds into incidents (see [[AI-Attributed Defect Tracking]]).

### Review signal degradation
A central failure mode: AI generates more, larger PRs than humans can meaningfully review. Guardrails must keep diffs small (see [[Iterative Chunking]]) and force AI agents to produce review-friendly output — explicit tests, narrow scope, clear intent.

## Tradeoffs / When to use
- **Gain:** safe acceleration; AI velocity without a defect explosion; clear merge criteria.
- **Cost:** upfront investment in policy/test/review tooling; cultural shift away from velocity KPIs; AI agents must be configured to respect the stack.
- **Fits:** teams shipping AI-assisted code to production where regressions have real cost.
- **Poor fit:** disposable prototypes and one-off scripts where the [[Refactoring Trap]] doesn't apply.

## Key tools / implementations
- [[Propel]] — 5-layer guardrail stack with risk-tiered routing.
- [[CodeScene]] — code quality, familiarity, and test-coverage guardrails.
- [[CodeRabbit]] — AI review gate layer with quality dashboards and defect tracking.

## Sources
- [[raw/propel-agentic-code-review-guardrails]] — 5-layer stack, risk tiers, review signal degradation.
- [[raw/codescene-guardrails-metrics-ai-coding]] — 3 guardrails, human-written tests for AI code, familiarity metric.
- [[raw/coderabbit-ai-speed-vs-quality-2026]] — quality gates as infrastructure, KPI shift, 1.7x defect multiplier.
- [[raw/tfir-ai-code-quality-guardrails-2026]] — throughput-to-trust pivot, governance frameworks.

## Backlinks
- [[AI-Attributed Defect Tracking]]
- [[Code Comprehension Bottleneck]]
- [[CodeRabbit]]
- [[OpenAI Codex]]
- [[Risk-Tiered Review]]
- [[Verification Bottleneck]]
