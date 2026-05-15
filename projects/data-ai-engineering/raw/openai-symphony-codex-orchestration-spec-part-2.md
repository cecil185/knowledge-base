---
title: "An open-source spec for Codex orchestration: Symphony"
url: https://openai.com/index/open-source-codex-orchestration-symphony/
fetched: 2026-05-10
linear_ticket: CC-24
type: article
tags: []
part: 2
total_parts: 3
---

# Symphony SPEC.md — Sections 1–7

## 1. Problem Statement

Symphony is a long-running automation service that continuously reads work from an issue tracker (Linear in this specification version), creates an isolated workspace for each issue, and runs a coding agent session for that issue inside the workspace.

The service solves four operational problems:

- It turns issue execution into a repeatable daemon workflow instead of manual scripts.
- It isolates agent execution in per-issue workspaces so agent commands run only inside per-issue workspace directories.
- It keeps the workflow policy in-repo (`WORKFLOW.md`) so teams version the agent prompt and runtime settings with their code.
- It provides enough observability to operate and debug multiple concurrent agent runs.

Important boundary:

- Symphony is a scheduler/runner and tracker reader.
- Ticket writes (state transitions, comments, PR links) are typically performed by the coding agent using tools available in the workflow/runtime environment.
- A successful run may end at a workflow-defined handoff state (for example `Human Review`), not necessarily `Done`.

## 2. Goals and Non-Goals

### 2.1 Goals

- Poll the issue tracker on a fixed cadence and dispatch work with bounded concurrency.
- Maintain a single authoritative orchestrator state for dispatch, retries, and reconciliation.
- Create deterministic per-issue workspaces and preserve them across runs.
- Stop active runs when issue state changes make them ineligible.
- Recover from transient failures with exponential backoff.
- Load runtime behavior from a repository-owned `WORKFLOW.md` contract.
- Expose operator-visible observability (at minimum structured logs).
- Support restart recovery without requiring a persistent database.

### 2.2 Non-Goals

- Rich web UI or multi-tenant control plane.
- General-purpose workflow engine or distributed job scheduler.
- Built-in business logic for how to edit tickets, PRs, or comments. (That logic lives in the workflow prompt and agent tooling.)
- Mandating strong sandbox controls beyond what the coding agent and host OS provide.

## 3. System Overview

### 3.1 Main Components

1. **Workflow Loader** — Reads `WORKFLOW.md`, parses YAML front matter and prompt body.
2. **Config Layer** — Exposes typed getters for workflow config values, applies defaults and environment variable indirection.
3. **Issue Tracker Client** — Fetches candidate issues in active states, fetches current states for reconciliation, normalizes tracker payloads into a stable issue model.
4. **Orchestrator** — Owns the poll tick, in-memory runtime state, decides which issues to dispatch, retry, stop, or release.
5. **Workspace Manager** — Maps issue identifiers to workspace paths, ensures per-issue workspace directories exist, runs lifecycle hooks, cleans workspaces for terminal issues.
6. **Agent Runner** — Creates workspace, builds prompt from issue + workflow template, launches the coding agent app-server client, streams agent updates back to the orchestrator.
7. **Status Surface** (optional) — Presents human-readable runtime status.
8. **Logging** — Emits structured runtime logs to one or more configured sinks.

### 3.2 Abstraction Levels

1. **Policy Layer** (repo-defined) — `WORKFLOW.md` prompt body, team-specific rules.
2. **Configuration Layer** (typed getters) — Parses front matter into typed runtime settings.
3. **Coordination Layer** (orchestrator) — Polling loop, issue eligibility, concurrency, retries, reconciliation.
4. **Execution Layer** (workspace + agent subprocess) — Filesystem lifecycle, workspace preparation, coding-agent protocol.
5. **Integration Layer** (Linear adapter) — API calls and normalization for tracker data.
6. **Observability Layer** (logs + optional status surface).

## 4. Core Domain Model

### 4.1 Key Entities

- **Issue** — Normalized issue record with id, identifier, title, description, priority, state, branch_name, url, labels (lowercase), blocked_by (list of blocker refs), created_at, updated_at.
- **Workflow Definition** — Parsed `WORKFLOW.md` payload: config (YAML front matter) + prompt_template (markdown body).
- **Service Config** — Typed runtime values: poll interval, workspace root, active/terminal states, concurrency limits, agent executable/args/timeouts, workspace hooks.
- **Workspace** — Filesystem workspace assigned to one issue identifier: path, workspace_key, created_now flag.
- **Run Attempt** — One execution attempt: issue_id, identifier, attempt number, workspace_path, started_at, status, error.
- **Live Session** — Agent session metadata: session_id, thread_id, turn_id, PID, token counters, turn_count.
- **Retry Entry** — Scheduled retry: issue_id, identifier, attempt, due_at_ms, timer_handle, error.
- **Orchestrator Runtime State** — In-memory: poll_interval_ms, max_concurrent_agents, running map, claimed set, retry_attempts map, completed set, codex_totals, codex_rate_limits.

### 4.2 Normalization Rules

- **Workspace Key** — Derive from issue.identifier, replacing non-`[A-Za-z0-9._-]` with `_`.
- **Normalized Issue State** — Compare states after `lowercase`.
- **Session ID** — `<thread_id>-<turn_id>`.

## 5. Workflow Specification (WORKFLOW.md)

### 5.1 File Format

`WORKFLOW.md` is a Markdown file with optional YAML front matter. If file starts with `---`, parse lines until the next `---` as YAML. Remaining lines become the prompt body. YAML must decode to a map/object.

### 5.2 Front Matter Schema

Top-level keys:

- **tracker** — kind (required, `linear`), endpoint, api_key (`$VAR_NAME` supported), project_slug (required), active_states (default: `Todo`, `In Progress`), terminal_states (default: `Closed`, `Cancelled`, `Canceled`, `Duplicate`, `Done`).
- **polling** — interval_ms (default: 30000), dynamically re-applied.
- **workspace** — root path (default: `<system-temp>/symphony_workspaces`).
- **hooks** — after_create, before_run, after_run, before_remove (shell scripts), timeout_ms (default: 60000).
- **agent** — max_concurrent_agents (default: 10), max_retry_backoff_ms (default: 300000), max_concurrent_agents_by_state (map).
- **codex** — command (default: `codex app-server`), approval_policy, thread_sandbox, turn_sandbox_policy, turn_timeout_ms (default: 3600000), read_timeout_ms (default: 5000), stall_timeout_ms (default: 300000).

### 5.3 Prompt Template Contract

Uses strict template engine (Liquid-compatible). Template variables: `issue` (all normalized fields) and `attempt` (null on first run, integer on retry).

### 5.4 Dynamic Reload

The software watches `WORKFLOW.md` for changes and re-applies config without restart. Invalid reloads keep operating with last known good config.

## 6. Configuration

- Source precedence: runtime setting → YAML front matter → `$VAR_NAME` env indirection → built-in defaults.
- Dispatch preflight validation checks: workflow loadable, tracker.kind present, api_key resolved, project_slug present, codex.command non-empty.

## 7. Orchestration State Machine

### 7.1 Issue Orchestration States

1. **Unclaimed** — Not running, no retry scheduled.
2. **Claimed** — Reserved to prevent duplicate dispatch.
3. **Running** — Worker task exists in running map.
4. **RetryQueued** — Retry timer exists.
5. **Released** — Claim removed (terminal, non-active, or retry exhausted).

### 7.2 Run Attempt Lifecycle

PreparingWorkspace → BuildingPrompt → LaunchingAgentProcess → InitializingSession → StreamingTurn → Finishing → Succeeded/Failed/TimedOut/Stalled/CanceledByReconciliation.

### 7.3 Key Behaviors

- A successful worker exit schedules a short continuation retry (1s) to re-check if the issue remains active.
- Workers can run multiple back-to-back turns on the same thread before exiting.
- First turn uses the full rendered task prompt; continuation turns send only continuation guidance.
- Reconciliation runs before dispatch on every tick.
- Restart recovery is tracker-driven and filesystem-driven (no durable DB required).
