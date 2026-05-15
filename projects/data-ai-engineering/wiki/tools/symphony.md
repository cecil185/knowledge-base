---
title: Symphony
updated: 2026-05-15
sources: [raw/openai-symphony-codex-orchestration-spec-part-1.md, raw/openai-symphony-codex-orchestration-spec-part-2.md, raw/openai-symphony-codex-orchestration-spec-part-3.md]
related: [openai-codex, linear, mcp, claude-code]
---
## Purpose
OpenAI's open-source orchestration spec for running fleets of [[OpenAI Codex]] agents in parallel, using an issue tracker as the control plane — the canonical implementation of [[Issue Tracker as Control Plane]].

## How it works
Symphony is **technically just two markdown files**: `SPEC.md` (the protocol) and `WORKFLOW.md` (YAML front matter + Liquid prompt body, lives in the repo). The reference implementation is in Elixir; community ports exist in TypeScript, Go, Rust, Java, and Python.

A long-running daemon executes the **poll-reconcile-dispatch cycle** against Linear over GraphQL (extended via a `linear_graphql` [[MCP]] tool):

1. **Poll** the tracker every 30s for tickets in scope.
2. **Reconcile** current ticket states against active Codex runs (recover after restarts without a persistent DB).
3. **Dispatch** new work — spawn `codex app-server` per ticket in an isolated workspace.

Tickets move through **5 orchestration states**: Unclaimed → Claimed → Running → RetryQueued → Released. The agent writes status updates to the tracker; Symphony only reads from it. This means the orchestrator is a scheduler, not a state machine of its own.

**Defaults**: poll interval 30000ms; max concurrent 10; turn timeout 1h (3600000ms); stall timeout 5min (300000ms); hook timeout 60s; continuation retry 1000ms; max retry backoff 300000ms; exponential backoff formula `min(10000 * 2^(attempt-1), max_retry_backoff_ms)`. JSON-RPC line cap 10MB. Session ID `<thread_id>-<turn_id>`.

Safety invariant: workspace path must be inside repository root. Token accounting uses absolute (not delta) counts to survive reconciliation.

## Strengths
- **500% increase in landed PRs** in the first three weeks at some OpenAI teams
- Tracker-as-control-plane means humans use the tools they already use (Linear)
- Reference impl in Elixir + ports in 5 languages — protocol is portable
- Restart-recoverable: no persistent DB needed because Linear is the source of truth
- Agents file their own follow-up tickets — system becomes self-building
- Speculative exploration at near-zero cost — 3-5 concurrent sessions per human is the bottleneck, not compute

## Weaknesses
- Human attention is the real cap (3-5 concurrent reviews max) — see [[Verification Bottleneck]]
- Requires a tracker with a usable GraphQL API ([[Linear]] today)
- Defaults assume Codex; other models need a shim
- WORKFLOW.md is repo-specific — every repo needs tuning
- Token accounting and rate-limit tracking add operational overhead

## Alternatives
- Hand-rolled queues + GitHub Actions — works but loses the standardization
- Devin, AutoGen, LangGraph — orchestration frameworks but not tracker-native

## Sources
- [[raw/openai-symphony-codex-orchestration-spec-part-1]] — blog framing, 500% metric, Linear-as-control-plane motivation
- [[raw/openai-symphony-codex-orchestration-spec-part-2]] — SPEC §1-7: daemon workflow, 5 states, defaults, backoff formula
- [[raw/openai-symphony-codex-orchestration-spec-part-3]] — SPEC §8-13: poll-reconcile-dispatch, handshake, safety invariants

## Backlinks
- [[Agentic Coding]]
- [[Constraint-Driven Prompting]]
- [[Harness Engineering]]
- [[Issue Tracker As Control Plane]]
- [[Iterative Chunking]]
- [[Linear]]
- [[MCP (Model Context Protocol)]]
- [[Multi-Agent Orchestration]]
- [[OpenAI Codex]]
- [[Parallel Agent Deployment]]
- [[Repo-Local Agent Instructions]]
- [[Spec-Driven Development]]
- [[Workflow Over Model]]
