---
title: OpenAI Codex
updated: 2026-05-15
sources: [raw/openai-symphony-codex-orchestration-spec-part-1.md, raw/openai-symphony-codex-orchestration-spec-part-2.md, raw/openai-symphony-codex-orchestration-spec-part-3.md, raw/max-woolf-ai-agent-coding-skeptic.md, raw/shiplight-openai-codex-testing.md]
related: [claude-code, symphony, shiplight, mcp]
---
## Purpose
OpenAI's autonomous coding agent — runs long-horizon implementation work in a sandboxed workspace, exposes a JSON-RPC app-server API for orchestrators, and is the worker model behind [[Symphony]].

## How it works
Codex runs in **app-server mode** (`codex app-server`), speaking line-delimited JSON-RPC (10MB max line) over stdio. The turn-based protocol is: `initialize` → `initialized` notification → `thread/start` → `turn/start` → streaming events (assistant messages, tool calls, token usage) → turn completion. Session IDs follow `<thread_id>-<turn_id>`.

Each Codex instance gets a **sandbox policy** (filesystem scope) and an **approval policy** (which actions need confirmation). Orchestrators like [[Symphony]] spawn one Codex per ticket inside an isolated workspace, then reconcile state from the issue tracker rather than persisting their own DB.

In practice Codex is strongest when **chained** with another model — Max Woolf's pattern runs Codex 5.3 to draft, then Claude Opus 4.6 to critique and tighten, a form of [[Cross-Model Review]]. Codex obeys `AGENTS.md` (its analog of `CLAUDE.md`) for [[Constraint-Driven Prompting]]: prohibitions, mandates, and anti-cheating rules.

Shiplight identifies **4 failure modes** specific to Codex-generated code: unspecified edge cases, cross-browser incompatibility, unexpected feature interactions, and real-world integration failures — all of which require live browser verification via [[MCP]] servers.

## Strengths
- App-server mode is a clean machine-to-machine API — enables orchestration at scale
- Sandbox + approval policies give per-run safety boundaries
- Strong raw drafting model; Woolf shipped 6 production projects (UMAP 9-30x faster than Python umap, 20K-video scraper first attempt)
- Integrates as the worker in [[Symphony]] — 500% PR throughput increase reported at OpenAI
- Streaming token-usage events enable real-time cost tracking

## Weaknesses
- Generates 4 distinct AI-code failure modes that demand third-party verification
- Best output requires chaining with a second model — single-pass results trail Claude on tight tasks
- Needs strict `AGENTS.md` constraints to avoid benchmark gaming / shortcut behavior
- Same 1.7x defect multiplier risk as other AI coders without [[Guardrails for AI Coding]]

## Alternatives
- [[Claude Code]] — typical chain partner; better at critique and tightening
- GitHub Copilot Agent, Google Jules — competing autonomous agents

## Sources
- [[raw/openai-symphony-codex-orchestration-spec-part-1]] — Codex app-server mode, JSON-RPC API, Symphony integration
- [[raw/openai-symphony-codex-orchestration-spec-part-2]] — turn protocol, sandbox/approval policies, defaults
- [[raw/openai-symphony-codex-orchestration-spec-part-3]] — handshake sequence, session ID format
- [[raw/max-woolf-ai-agent-coding-skeptic]] — Codex 5.3 → Opus 4.6 chain, AGENTS.md patterns
- [[raw/shiplight-openai-codex-testing]] — 4 AI-code failure modes, browser MCP verification

## Backlinks
- [[Agentic Coding]]
- [[Claude Code]]
- [[Constraint-Driven Prompting]]
- [[Cross-Model Review]]
- [[Harness Engineering]]
- [[Intent-Based Testing]]
- [[Issue Tracker As Control Plane]]
- [[Iterative Chunking]]
- [[MCP (Model Context Protocol)]]
- [[Parallel Agent Deployment]]
- [[Repo-Local Agent Instructions]]
- [[Shiplight]]
- [[Spec-Driven Development]]
- [[Symphony]]
- [[Verifiability Boundary]]
- [[Workflow Over Model]]
