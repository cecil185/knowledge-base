---
title: Linear
updated: 2026-05-15
sources: [raw/openai-symphony-codex-orchestration-spec-part-1.md, raw/openai-symphony-codex-orchestration-spec-part-2.md, raw/openai-symphony-codex-orchestration-spec-part-3.md]
related: [symphony, openai-codex]
---
## Purpose
Modern issue tracker used by Cecil's Knowledge Base project and, in [[Symphony]], repurposed as the **control plane for agent orchestration** — each ticket is a unit of work, its status field is the state machine, and agents read and write it directly.

## How it works
Linear exposes a GraphQL API that orchestrators use to fetch candidate issues and update their lifecycle. In the Symphony spec:

- **Fetching** — orchestrator pages through issues via GraphQL, default page size 50, with a 30-second timeout per request. The Codex app-server is exposed a `linear_graphql` tool so agents can query and mutate Linear directly.
- **Status as state machine** — `Todo` → `In Progress` → `Review` → `Merging` → `Done`. The agent writes status to Linear; the orchestrator only reads it, which is what makes restart-recovery work without a separate persistent database.
- **Priority sorting** — candidate issues are ordered by priority ascending (1-4, with `null` last), then `created_at` oldest first, then `identifier` lexicographic. Stable, deterministic ordering across orchestrator restarts.
- **Ticket-as-unit-of-work** — agents file their own follow-up issues, enabling the self-building system property that Symphony reports drove a 500% increase in landed PRs in three weeks on some OpenAI teams.

This implements the [[Issue Tracker As Control Plane]] pattern: the tracker is the only durable source of truth, so any orchestrator restart can reconcile state by re-reading Linear rather than consulting a local database.

Cecil's Knowledge Base also uses Linear directly — the `CC` team holds the Work project plus a Wiki project per learning topic, with article tags (`human-not-read`, `human-read`) acting as a smaller-scale version of the same status-as-state-machine pattern.

## Strengths
- GraphQL API with good ergonomics for both human dashboards and agent automation.
- Native status, priority, and label fields cover most of the orchestration state machine without custom schemas.
- Durable, hosted source of truth — orchestrators can restart without losing work.
- Strong UI for the human supervisor watching 3-5 concurrent agent sessions.
- Stable ordering primitives (priority + created_at + identifier) make agent dispatch deterministic.

## Weaknesses
- Hosted SaaS — outage takes the control plane down with it.
- GraphQL rate limits constrain very high-throughput orchestrators; the 30s timeout and 50-item page size are real bottlenecks at scale.
- Status field is a flat enum; complex orchestration states (e.g. `RetryQueued`, `Released`) must be encoded in labels or comments.
- Not free; team-priced.
- No native concept of "agent ran this turn" — token accounting and rate-limit tracking live outside Linear.

## Alternatives
- GitHub Issues — free, less structured, weaker API ergonomics for orchestration.
- Jira — more configurable workflows, heavier API, slower UI.
- Plain database + custom UI — maximum flexibility, but you rebuild Linear's UX.

## Sources
- [[raw/openai-symphony-codex-orchestration-spec-part-1]] — Linear as control plane, ticket-as-unit-of-work, 500% PR uplift.
- [[raw/openai-symphony-codex-orchestration-spec-part-2]] — GraphQL pagination defaults, status handoff between agent and orchestrator, restart recovery via tracker.
- [[raw/openai-symphony-codex-orchestration-spec-part-3]] — `linear_graphql` tool extension on the Codex app-server, reconciliation cycle reading from Linear.

## Backlinks
- [[Agentic Coding]]
- [[Issue Tracker As Control Plane]]
- [[Iterative Chunking]]
- [[Spec-Driven Development]]
- [[Symphony]]
- [[Workflow Over Model]]
