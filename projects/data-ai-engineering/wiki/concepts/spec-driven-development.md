---
title: Spec-Driven Development
updated: 2026-05-15
sources: [raw/addy-osmani-llm-coding-workflow-2026.md, raw/openai-symphony-codex-orchestration-spec-part-1.md, raw/openai-symphony-codex-orchestration-spec-part-2.md]
related: [agentic-coding, harness-engineering, constraint-driven-prompting, workflow-over-model, issue-tracker-as-control-plane, multi-agent-orchestration, parallel-agent-deployment]
---
## Summary
Compile a specification before any code is generated. The spec becomes the durable artifact that survives multiple agent passes — a reasoning model uses it to produce a step-by-step plan, and worker agents execute against the plan rather than against a fresh interpretation of the user's intent.

## Details
Direct prompts ("build me X") let the model invent both *what* and *how* on every run. Spec-driven development separates those phases: the human and a planning model collaborate on a `spec.md` first, then a reasoning model converts the spec into a step plan, then implementation begins. The spec is the source of truth; the plan and code are derived artifacts.

### Symphony is a SPEC.md
The Symphony orchestrator is described by its own authors as "technically just a SPEC.md file defining the problem and the solution." Implementations exist in TypeScript, Go, Rust, Java, and Python — all generated from the same spec. The spec is the product; the code is incidental output. This is the cleanest demonstration that the spec, not the code, is the durable artifact.

### Why the spec must come first
- **Parallel agents need a shared anchor.** When 4+ agents are running concurrently ([[Parallel Agent Deployment]]), they need a single source of truth to avoid divergent interpretations.
- **Verification needs an oracle.** A judge agent can only verify against something. Without a written spec, "correct" collapses to "looks plausible."
- **Models forget; specs don't.** Context windows roll over; a checked-in `spec.md` is recoverable across sessions and recoverable across model upgrades.
- **The spec is the human checkpoint.** Reviewing a spec is cheaper than reviewing a 10,000-line diff. The spec is where human judgment lands.

### The workflow
1. Draft `spec.md` with the human — describe the problem, the constraints, the success criteria.
2. Feed `spec.md` to a reasoning model; receive a step-by-step implementation plan.
3. Human reviews the plan; iterates on the spec if the plan is wrong.
4. Worker agents implement against the plan, with the spec as grounding context.
5. Judge / test agents verify against the spec.

## Tradeoffs / When to use
**Gains:** durable artifact across sessions and model versions; cheap human checkpoint before expensive generation; shared anchor for parallel and hierarchical agents; reproducible builds from the same spec.
**Costs:** upfront time writing a spec for tasks where direct prompting would have been faster; specs can become stale if not maintained; the model can game an underspecified spec.
**Fits well when:** the task is large, will involve multiple agents or sessions, or needs to be reproducible.
**Fits poorly when:** the task is small and exploratory, or when the user genuinely doesn't yet know what they want — though even then, an evolving spec is often better than no spec.

## Key tools / implementations
- [[Symphony]] — `SPEC.md` is the canonical artifact; implementations are derived.
- `CLAUDE.md` / `AGENTS.md` — repo-local spec/instruction files for [[Claude Code]] and [[OpenAI Codex]].
- `WORKFLOW.md` (Symphony) — YAML front matter + Liquid prompt body, the spec for how agents run.
- [[Linear]] — issue body acts as a per-task mini-spec in the [[Issue Tracker As Control Plane]] pattern.

## Sources
- [[raw/addy-osmani-llm-coding-workflow-2026]] — write `spec.md` first → reasoning model generates step-by-step plan → write code.
- [[raw/openai-symphony-codex-orchestration-spec-part-1]] — Symphony as "technically just a SPEC.md file defining problem and solution"; spec as durable artifact across language implementations.
- [[raw/openai-symphony-codex-orchestration-spec-part-2]] — WORKFLOW.md as in-repo workflow policy; spec as the input the orchestrator reads.

## Backlinks
- [[Issue Tracker As Control Plane]]
