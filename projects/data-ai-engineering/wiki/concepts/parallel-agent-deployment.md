---
title: Parallel Agent Deployment
updated: 2026-05-15
sources: [raw/simon-willison-agentic-engineering-lennys-podcast.md, raw/addy-osmani-llm-coding-workflow-2026.md, raw/openai-symphony-codex-orchestration-spec-part-1.md]
related: [agentic-coding, verification-bottleneck, multi-agent-orchestration, hierarchical-agent-systems, issue-tracker-as-control-plane, workflow-over-model]
---
## Summary
Running multiple coding agents simultaneously on different problems to multiply throughput. The bottleneck shifts from typing speed to the human's capacity to direct and review concurrent streams of work.

## Details
The November 2025 inflection — GPT 5.1 and Claude Opus 4.5 crossing the quality threshold — made it viable to keep **4 or more agents running in parallel** on independent tasks. Roughly **~95% of code in a working day is now AI-generated** for developers operating this way. The unit of work changed from a 4-hour focused block to a **2-minute prompt** that kicks off an agent and returns to the inbox.

### Throughput numbers
- **2-week task → 20 minutes** when broken into parallel agent jobs.
- **10–15 year backlogs completed in months** in some teams.
- 4+ simultaneous agents is the practical floor; coordination cost grows nonlinearly past that.

### Cognitive overhead is real
Managing parallel agents is mentally expensive. Developers running 4+ agents report being **mentally exhausted by mid-morning** — directing, reviewing, and arbitrating between concurrent agents demands sustained context-switching. Symphony's experience puts the comfortable ceiling at **3–5 concurrent sessions** before context-switching pain dominates and quality drops.

### Mechanics
Parallel deployment requires:
- **Branches or worktrees per agent** so concurrent changes don't collide.
- An [[Issue Tracker As Control Plane]] (or equivalent) to track which agent owns which task.
- A tight feedback loop so agents that go off-track are killed before they consume large amounts of attention.
- Tolerance for speculative exploration — at near-zero per-task cost, running three variants and picking the best becomes rational.

### The new bottleneck
Generation is no longer the constraint; review is. This makes parallel deployment a special case of the [[Verification Bottleneck]] — more agents means more diffs to verify, and the human review budget caps the system's throughput long before the agents themselves do.

## Tradeoffs / When to use
**Gains:** dramatic throughput multiplication; cheap exploration of multiple approaches; backlog clearance that was previously impossible.
**Costs:** cognitive load on the human director; review capacity becomes the binding constraint; coordination failures when agents touch overlapping code; quality degrades past ~5 concurrent sessions.
**Fits well when:** tasks are independent, branchable, and have clear acceptance tests.
**Fits poorly when:** tasks share heavy state, require deep cross-task reasoning, or when review capacity is already saturated.

## Key tools / implementations
- [[Claude Code]] — terminal-native agents that run cleanly in worktrees.
- [[Symphony]] — orchestrates parallel Codex sessions through Linear ticket states.
- [[OpenAI Codex]] — app-server mode supports many concurrent sessions.
- Git worktrees / branches — the isolation primitive that makes parallel agents safe.

## Sources
- [[raw/simon-willison-agentic-engineering-lennys-podcast]] — November 2025 inflection, 4+ parallel agents, ~95% AI code, 2-min prompts vs 4-hr blocks, 2-week → 20 min, 10-15 year backlogs in months.
- [[raw/addy-osmani-llm-coding-workflow-2026]] — branches/worktrees for parallel experiments; "director" role for the developer.
- [[raw/openai-symphony-codex-orchestration-spec-part-1]] — 3–5 concurrent sessions as practical ceiling; mid-morning cognitive exhaustion; speculative exploration at near-zero cost.

## Backlinks
- [[Agentic Coding]]
- [[Database Branching]]
- [[Issue Tracker As Control Plane]]
- [[Spec-Driven Development]]
