---
title: Agentic Coding
updated: 2026-05-15
sources: [raw/addy-osmani-llm-coding-workflow-2026.md, raw/simon-willison-agentic-engineering-lennys-podcast.md, raw/simon-willison-eight-years-building-with-ai.md, raw/simon-willison-scaling-autonomous-coding.md, raw/max-woolf-ai-agent-coding-skeptic.md, raw/developers-digest-hn-ai-coding-agents-2026.md]
related: [verification-bottleneck, harness-engineering, workflow-over-model, parallel-agent-deployment, hierarchical-agent-systems, constraint-driven-prompting, multi-agent-orchestration, spec-driven-development]
---
## Summary
The paradigm where developers delegate implementation to AI agents while taking on direction, verification, and orchestration roles. By mid-2026, ~95% of code in many shipping workflows is AI-generated, and the bottleneck has moved from typing to reviewing.

## Details
Agentic coding reframes the developer as a "director": writing specs, packaging context, dispatching agents, and verifying output rather than writing code line-by-line. The mental model that holds up across practitioners is the LLM as an "over-confident junior developer" — fluent, fast, and frequently wrong in ways that require an experienced eye to catch.

### The November 2025 inflection
GPT 5.1 and Claude Opus 4.5 crossed a quality threshold that made multi-hour autonomous runs reliable enough to trust. Practitioners report a step-change: tasks that previously needed careful babysitting could now be fired off and checked later. Simon Willison reports running 4+ agents in parallel as a default working mode after this point, with ~95% of his shipped code AI-generated.

### Interruptibility changes the working day
Agents shift work from continuous 4-hour blocks to interruptible 2-minute prompts. The developer's day fragments into dispatch-and-verify cycles rather than deep focus on a single task. This is what enables parallelism — see [[Parallel Agent Deployment]] — but it also raises cognitive overhead: tracking what each agent is doing becomes its own skill.

### What accelerates and what doesn't
Implementation accelerates dramatically (Willison: 8-year conceptual backlog cleared in 3 months; 2-week tasks done in 20 minutes). Judgment does not. Architecture decisions, design tradeoffs, and verification still require human attention — and that attention is now the constraint. See [[Verification Bottleneck]].

### The shift to orchestration
Rather than one developer + one model, production patterns now use [[Hierarchical Agent Systems]] (planner → sub-planner → worker → judge) and specialized agents per role (research, modification, verification, synthesis). The real product is the [[Workflow Over Model]] — model choice matters less than the harness around it. See [[Harness Engineering]].

## Tradeoffs / When to use
Gains: massive throughput on well-defined, verifiable work; cleared backlogs; rapid prototyping with 3+ variants in parallel.
Costs: verification load grows superlinearly; skill atrophy risk for tasks always delegated; "vibe coding" works for personal scripts but breaks down at shipping quality without guardrails; credibility red flags appear when AI-generated docs/tests/security reports are taken at face value.
Fits well: greenfield code, well-specified tickets, prototyping, refactors with strong tests. Fits poorly: novel architecture, ambiguous requirements, anything where the verifier can't tell right from wrong.

## Key tools / implementations
- [[Claude Code]] — terminal-native agent, the dominant harness in 2026
- [[OpenAI Codex]] — used heavily in chained-model workflows
- [[Symphony]] — orchestration layer that dispatches Codex agents per Linear ticket
- [[Linear]] — issue tracker as the control plane for agent work

## Sources
- [[raw/addy-osmani-llm-coding-workflow-2026]] — "director" framing, junior-dev mental model, iterative chunking workflow
- [[raw/simon-willison-agentic-engineering-lennys-podcast]] — November 2025 inflection, 95% AI code, parallel agents, 2-min prompts vs 4-hr blocks
- [[raw/simon-willison-eight-years-building-with-ai]] — cold-start to shipping, 8-year backlog cleared in 3 months
- [[raw/simon-willison-scaling-autonomous-coding]] — agent swarms, 1M+ lines in under a week
- [[raw/max-woolf-ai-agent-coding-skeptic]] — skeptic's view of what actually ships, chained-model patterns
- [[raw/developers-digest-hn-ai-coding-agents-2026]] — workflow-over-model thesis, specialized agents

## Backlinks
- [[Claude Code]]
- [[Databricks Lakebase]]
- [[Intent-Based Testing]]
- [[Playwright]]
- [[Self-Healing Tests]]
