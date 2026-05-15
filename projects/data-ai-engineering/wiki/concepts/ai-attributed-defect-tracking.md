---
title: AI-Attributed Defect Tracking
updated: 2026-05-15
sources: [raw/coderabbit-ai-speed-vs-quality-2026.md, raw/tfir-ai-code-quality-guardrails-2026.md, raw/codescene-guardrails-metrics-ai-coding.md]
related: [guardrails-for-ai-coding, risk-tiered-review, verifiability-boundary, verification-bottleneck, agentic-coding]
---
## Summary
AI-attributed defect tracking is the practice of measuring defects, regressions, and incidents back to specific AI-generated changes — with the same rigor as security-incident tracking. It exists because AI code carries measurably more bugs (1.7x defect multiplier; 75% more logic/correctness issues) and because the only way to manage that risk is to make it visible at the KPI level.

## Details

### The attribution challenge
AI-authored code is rarely tagged as such. Once an AI suggestion is accepted, edited, or merged, it looks identical to human code in git history. Without explicit provenance metadata (PR labels, commit trailers, agent-attribution headers), there is no way to compute AI-specific defect rates — and therefore no way to know whether AI is making the codebase healthier or quietly worse.

### The defect multiplier
- CodeRabbit data: **AI-generated code had 1.7x more issues and bugs**, with **75% more logic and correctness issues** specifically.
- These are not surface-level style problems — they are the categories most likely to cause production incidents.
- The implication: a team that 10x's its PR volume with AI without changing guardrails imports a ~7x increase in latent defects.

### KPI shift: velocity → quality
The 2025 velocity KPIs are wrong instruments for 2026:

| Old (velocity) | New (quality / trust) |
|---|---|
| PRs merged per week | Defect density per AI-attributed PR |
| Cycle time | Review confidence score |
| Lines shipped | Merge reliability (rollback rate) |
| Story points | AI-attributed regression rate |
| Time to first commit | Coverage on AI-touched files |

This is the throughput-to-trust pivot. It is also what makes [[Guardrails for AI Coding]] measurable rather than aspirational.

### AI governance policies
Formal policies that follow from tracking:
- Tag AI authorship at commit/PR time (trailer, label, or agent metadata).
- Require [[Risk-Tiered Review]] proof tied to the AI attribution.
- Canary-deploy AI-authored features so blast radius is bounded.
- Publish AI defect rates publicly inside the org — visibility is the governance.

### The review capacity crisis
AI generates faster than humans can review. Defect tracking exposes this: if review capacity is the constraint, defect density rises on AI PRs over time as reviewers rubber-stamp. Tracking forces the constraint into the open and justifies investment in automated review layers and human-written tests (see [[Code Comprehension Bottleneck]]).

## Tradeoffs / When to use
- **Gain:** real numbers to replace AI hype; clear signal on which workflows are net-positive; defensible governance posture.
- **Cost:** tooling and process to capture provenance; cultural friction around "blaming the AI"; honest dashboards may show the program is underperforming.
- **Fits:** any team merging AI-assisted code to production at meaningful volume.
- **Poor fit:** exploratory or single-developer prototypes where defects don't propagate.

## Key tools / implementations
- [[CodeRabbit]] — quality dashboards, defect density tracking, PR-level AI analysis.
- [[CodeScene]] — code health metrics segmented by AI-touched files.

## Sources
- [[raw/coderabbit-ai-speed-vs-quality-2026]] — 1.7x multiplier, 75% logic issues, KPI shift, canary deploy pattern.
- [[raw/tfir-ai-code-quality-guardrails-2026]] — attribution challenge, throughput-to-trust, governance frameworks.
- [[raw/codescene-guardrails-metrics-ai-coding]] — code health KPIs for AI sections.

## Backlinks
- [[Code Comprehension Bottleneck]]
- [[CodeRabbit]]
- [[CodeScene]]
- [[Guardrails for AI Coding]]
- [[Verification Bottleneck]]
