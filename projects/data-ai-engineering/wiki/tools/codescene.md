---
title: CodeScene
updated: 2026-05-15
sources: [raw/codescene-guardrails-metrics-ai-coding.md]
related: [coderabbit, shiplight]
---
## Purpose
Code health and quality analysis platform — addresses the [[Code Comprehension Bottleneck]] by enforcing three guardrails specifically tuned for AI-generated code.

## How it works
CodeScene scans the repository and surfaces three layered guardrails:

1. **Code quality** — automated health checks that can block merges when complexity, duplication, or anti-patterns cross thresholds. Specifically tracks code health for AI-generated sections.
2. **Code familiarity** — team-level visibility into who has touched what. AI-generated code creates instant knowledge silos (developers are 93% slower in unfamiliar code), so the dashboard exposes who owns what context.
3. **Test coverage with human-written tests** — the critical insight: AI-written tests cannot independently verify AI-written code (correctness study found AI accuracy in the 31.1%-65.2% range). Coverage from human tests is tracked separately as the only meaningful verification signal.

The platform publishes KPI dashboards on quality, familiarity, coverage, and tech debt — the metrics replacing velocity in 2026 (see [[AI-Attributed Defect Tracking]]).

Underlying premise: coding is ~10% of the dev week and maintenance is 90%+ of lifecycle cost, so optimizing comprehension and ownership matters more than optimizing generation speed.

## Strengths
- Separates human-test coverage from AI-test coverage — the only reliable verification signal
- Surfaces knowledge silos before they become operational risks
- Code-health checks can auto-block bad AI-generated merges
- Treats AI-generated code as a distinct first-class category
- Aligns with the maintenance-cost reality (90% of lifecycle)

## Weaknesses
- Familiarity metrics depend on accurate Git history attribution — AI commits can confuse authorship
- Auto-blocking thresholds need tuning per repo or they create developer friction
- Doesn't replace per-PR review like [[CodeRabbit]] — complementary, not substitutive
- Knowledge dashboards only help if leadership actually acts on them

## Alternatives
- [[CodeRabbit]] — PR-level review and validation
- Sonar, Code Climate — older static-analysis tools without AI-coding focus
- Propel — guardrail stack with [[Risk-Tiered Review]]

## Sources
- [[raw/codescene-guardrails-metrics-ai-coding]] — three guardrails, 93% unfamiliar-code slowdown, 31.1%-65.2% AI correctness range, human-tests-only verification principle

## Backlinks
- [[AI-Attributed Defect Tracking]]
- [[Code Comprehension Bottleneck]]
- [[CodeRabbit]]
- [[Guardrails for AI Coding]]
- [[Verifiability Boundary]]
- [[Verification Bottleneck]]
