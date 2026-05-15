---
title: Hierarchical Agent Systems
updated: 2026-05-15
sources: [raw/simon-willison-scaling-autonomous-coding.md]
related: [agentic-coding, multi-agent-orchestration, parallel-agent-deployment, verification-bottleneck, spec-driven-development]
---
## Summary
A tiered architecture — planner → sub-planner → worker → judge — that lets autonomous coding scale beyond what a single long-context session can handle. Higher tiers decompose work; lower tiers execute it; judge agents form an independent verification layer.

## Details
Single-agent coding hits a ceiling: context windows fill, plans drift, and verification collapses into self-review. Hierarchical agent systems break the ceiling by stacking agents with different abstraction levels. The planner owns the overall objective; sub-planners turn slices into concrete task lists; workers implement; judges verify against specifications independently of the worker that produced the code.

### The FastRender case
A Rust browser engine, **FastRender**, was built using this architecture: **1M+ lines of code, trillions of tokens consumed, ~1000 files, in under one week, with hundreds of concurrent agents.** Reference specifications (WhatWG, CSS-WG) were embedded directly in the repository as Git submodules so worker agents could ground decisions in normative text rather than memory. CI failures were treated as expected and recoverable — the system targeted resolution within a **24-hour window** rather than blocking the planner.

### Judge agents as the verification spine
The judge tier exists because [[Multi-Agent Orchestration]] without an explicit verifier degrades into self-review. Judges run after workers, hold the spec in context, and either pass the change or push it back as a new sub-task. This is the structural answer to the [[Verification Bottleneck]] at swarm scale.

### Why 2029 became 2026
Earlier projections placed swarm-scale autonomous coding around 2029. Concurrent independent emergence — multiple teams arriving at the planner/worker/judge pattern at once in early 2026 — pulled the timeline in by three years. The enabling shift was not a smarter model but a structural one: agents stopped trying to hold the whole problem in one head.

## Tradeoffs / When to use
**Gains:** scales to problems too large for a single context window; independent judges break the self-review trap; concurrency multiplies throughput.
**Costs:** orchestration complexity is high; debugging cross-tier failures is hard; token cost is enormous (trillions, not billions); requires problems with well-defined, machine-verifiable success criteria.
**Fits well when:** the problem is large, decomposable, and has reference specifications or strong tests (browsers, compilers, protocol implementations).
**Fits poorly when:** acceptance criteria are subjective, specs are missing, or the task is small enough that a flat [[Multi-Agent Orchestration]] chain works.

## Key tools / implementations
- [[Claude Code]] — used in FastRender's worker tier.
- Cursor — used alongside Claude Code in the FastRender swarm.
- Reference specs as Git submodules (WhatWG, CSS-WG) — the grounding mechanism.

## Sources
- [[raw/simon-willison-scaling-autonomous-coding]] — planner/sub-planner/worker/judge architecture, FastRender metrics (1M+ lines, trillions of tokens, hundreds of concurrent agents, <1 week), 24-hour CI recovery window, 2029→2026 acceleration.

## Backlinks
- [[Agentic Coding]]
- [[Claude Code]]
- [[Workflow Over Model]]
