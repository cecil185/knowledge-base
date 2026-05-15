---
title: Issue Tracker As Control Plane
updated: 2026-05-15
sources: [raw/openai-symphony-codex-orchestration-spec-part-1.md, raw/openai-symphony-codex-orchestration-spec-part-2.md, raw/openai-symphony-codex-orchestration-spec-part-3.md]
related: [agentic-coding, parallel-agent-deployment, multi-agent-orchestration, spec-driven-development, harness-engineering, workflow-over-model, verification-bottleneck]
---
## Summary
Use the project management tool — Linear in Symphony's case — as the state machine that orchestrates coding agents. Tickets are units of work, status transitions are agent lifecycle events, and the tracker (not a bespoke orchestrator) holds the system's authoritative state.

## Details
The Symphony pattern, deployed inside OpenAI, treats Linear as the control plane: agents read tickets, claim work, write progress back to the ticket, and transition status on completion. The orchestrator is a thin daemon that polls the tracker and dispatches Codex sessions — it does not own state.

### Ticket-as-unit-of-work
Each Linear ticket is one bounded job an agent can pick up and finish. The ticket body is a mini-spec (see [[Spec-Driven Development]]); the status column is the agent's lifecycle position; comments are the audit trail. This raises the abstraction from "session" to "ticket," removing the human attention bottleneck that caps [[Parallel Agent Deployment]] at 3–5 concurrent sessions.

### Status as agent lifecycle
Linear's status field maps directly to the agent's state machine:
- **Todo** — unclaimed work, eligible for an agent to pick up.
- **In Progress** — an agent is actively running.
- **In Review** — the diff is ready for a reviewer (human or AI judge).
- **Merging** — CI passing, awaiting merge.
- **Done** — landed.

### Five orchestration states (internal)
Beneath the Linear-visible statuses, Symphony's daemon tracks five internal orchestration states per ticket: **Unclaimed → Claimed → Running → RetryQueued → Released**. RetryQueued handles transient failures with exponential backoff (`min(10000 * 2^(attempt-1), 300000)` ms). Released returns work to the pool. The five-state machine is what makes restart recovery work without a persistent database — the tracker itself is the database.

### DAG-based task parallelism
Tickets reference dependencies (blocks / blocked-by). Agents only start work whose blockers are Done. The DAG is implicit in Linear's link types; the orchestrator just respects it. This lets parallelism happen naturally: every unblocked Todo is fair game for the next free agent.

### Democratization of work initiation
Because the unit of input is a ticket, **anyone who can file a ticket can dispatch an agent** — PMs and designers file tickets directly, and work begins without an engineer in the loop. The reported impact in early-adopter OpenAI teams: **500% increase in landed PRs in the first three weeks**.

### Why this works
- **No bespoke orchestrator UI.** Engineers already use Linear; agents adopt that surface.
- **Restart recovery is free.** The tracker is the persistent state — kill the daemon and restart, and it reconciles from Linear.
- **Human attention scales by abstraction, not session count.** Reviewing 20 tickets is tractable; managing 20 concurrent agent sessions is not.

## Tradeoffs / When to use
**Gains:** scales past the 3–5 concurrent session human limit; removes the need for a custom orchestration UI; democratizes who can dispatch work; free persistent state and restart recovery; natural DAG parallelism.
**Costs:** depends on the tracker's API stability and rate limits (Linear GraphQL in Symphony's case); ticket hygiene becomes load-bearing — bad specs produce bad agent work at scale; debugging cross-ticket state issues requires reading the tracker, not a debugger.
**Fits well when:** the team already lives in a structured tracker, tasks decompose cleanly into tickets, and you want PMs/designers in the loop.
**Fits poorly when:** work is ad-hoc and doesn't fit the ticket abstraction, or when the tracker can't express dependencies (Trello-style boards without links struggle here).

## Key tools / implementations
- [[Symphony]] — reference implementation; Codex app-server + Linear GraphQL + WORKFLOW.md.
- [[Linear]] — the tracker chosen for its GraphQL API and status model.
- [[OpenAI Codex]] — app-server mode (JSON-RPC, line-delimited, 10MB max) is the agent runtime.
- WORKFLOW.md — in-repo policy that tells the orchestrator how to interpret tickets.

## Sources
- [[raw/openai-symphony-codex-orchestration-spec-part-1]] — Linear as control plane; ticket-as-unit-of-work; 3–5 concurrent session human limit; 500% increase in landed PRs; democratization of work initiation; human attention as the bottleneck removed by raising the abstraction.
- [[raw/openai-symphony-codex-orchestration-spec-part-2]] — five orchestration states (Unclaimed → Claimed → Running → RetryQueued → Released); daemon as scheduler/reader; restart recovery without persistent DB; exponential backoff defaults.
- [[raw/openai-symphony-codex-orchestration-spec-part-3]] — poll-reconcile-dispatch cycle; reconciliation; safety invariants; Linear GraphQL tool extension.

## Backlinks
- [[Linear]]
- [[Parallel Agent Deployment]]
- [[Spec-Driven Development]]
