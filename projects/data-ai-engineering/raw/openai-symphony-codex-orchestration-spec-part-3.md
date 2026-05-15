---
title: "An open-source spec for Codex orchestration: Symphony"
url: https://openai.com/index/open-source-codex-orchestration-symphony/
fetched: 2026-05-10
linear_ticket: CC-24
type: article
tags: []
part: 3
total_parts: 3
---

# Symphony SPEC.md — Sections 8–13

## 8. Polling, Scheduling, and Reconciliation

### 8.1 Poll Loop

Tick sequence: reconcile running issues → validate config → fetch candidates → sort by priority → dispatch eligible → notify status consumers.

### 8.2 Candidate Selection

An issue is dispatch-eligible only if: it has id/identifier/title/state, state is active and not terminal, not already running or claimed, global and per-state concurrency slots available, and (for Todo state) no non-terminal blockers.

Sorting: priority ascending (1..4 preferred, null last) → created_at oldest first → identifier lexicographic.

### 8.3 Concurrency Control

- Global: `available_slots = max(max_concurrent_agents - running_count, 0)`
- Per-state: `max_concurrent_agents_by_state[state]` if present, else global limit.
- Optional SSH host limit: `max_concurrent_agents_per_host` per configured host.

### 8.4 Retry and Backoff

- Normal continuation retries: fixed 1000ms delay.
- Failure retries: `delay = min(10000 * 2^(attempt - 1), max_retry_backoff_ms)`.
- On retry fire: fetch active candidates, find the issue, dispatch if slots available, requeue if not, release claim if no longer active.

### 8.5 Active Run Reconciliation

**Part A — Stall detection:** If elapsed since last event > stall_timeout_ms, terminate worker and queue retry.

**Part B — Tracker state refresh:** Fetch current states for all running issues. Terminal → terminate + clean workspace. Still active → update snapshot. Neither → terminate without cleanup.

### 8.6 Startup Cleanup

Query tracker for terminal-state issues, remove corresponding workspace directories.

## 9. Workspace Management and Safety

### 9.1 Layout

- Root: `workspace.root` (normalized path)
- Per-issue: `<workspace.root>/<sanitized_issue_identifier>`
- Workspaces reused across runs, not auto-deleted on success.

### 9.2 Hooks

- `after_create` — runs on new workspace creation; failure aborts creation.
- `before_run` — runs before each agent attempt; failure aborts attempt.
- `after_run` — runs after each attempt; failure logged and ignored.
- `before_remove` — runs before deletion; failure logged, cleanup proceeds.
- All hooks execute via `sh -lc` with workspace as cwd, subject to `hooks.timeout_ms`.

### 9.3 Safety Invariants

1. Run the coding agent only in the per-issue workspace path (validate `cwd == workspace_path`).
2. Workspace path must stay inside workspace root (prefix check on absolute paths).
3. Workspace key is sanitized to `[A-Za-z0-9._-]` only.

## 10. Agent Runner Protocol

### 10.1 Launch

- Command: `bash -lc <codex.command>` in workspace directory.
- Line-delimited JSON-RPC-like protocol on stdout. Max line size: 10 MB.

### 10.2 Session Startup Handshake

1. `initialize` request (clientInfo, capabilities) → wait for response.
2. `initialized` notification.
3. `thread/start` request (approvalPolicy, sandbox, cwd).
4. `turn/start` request (threadId, input text, cwd, title, approvalPolicy, sandboxPolicy).

Session IDs: thread_id from thread/start result, turn_id from turn/start result, composed as `<thread_id>-<turn_id>`.

### 10.3 Streaming Turn Processing

Read line-delimited messages until: `turn/completed` (success), `turn/failed`/`turn/cancelled` (failure), turn timeout, or subprocess exit. For continuation turns, reuse the same threadId.

### 10.4 Approval and Tool Call Policy

- Implementation-defined approval posture (documented per implementation).
- Auto-approve or surface to operator — must not leave runs stalled indefinitely.
- Unsupported dynamic tool calls return failure response and continue session.
- User-input-required events fail the run attempt immediately.

### 10.5 Optional `linear_graphql` Tool Extension

Executes raw GraphQL against Linear using Symphony's configured auth. Accepts `{query, variables}`, executes one operation per call, returns structured output. Avoids exposing Linear API key to sub-agents.

## 11. Issue Tracker Integration (Linear)

### 11.1 Required Operations

1. `fetch_candidate_issues()` — issues in active states for configured project.
2. `fetch_issues_by_states(state_names)` — for startup terminal cleanup.
3. `fetch_issue_states_by_ids(issue_ids)` — for active-run reconciliation.

### 11.2 Linear Query Semantics

- GraphQL endpoint, auth token in Authorization header.
- project_slug maps to Linear project slugId.
- Pagination required, page size default 50, network timeout 30000ms.

### 11.3 Normalization

Labels → lowercase. Blocked_by → derived from inverse relations where type is `blocks`. Priority → integer only. Timestamps → ISO-8601.

### 11.4 Tracker Writes Boundary

Symphony does not require first-class tracker write APIs. Ticket mutations are handled by the coding agent using tools defined by the workflow prompt. The service remains a scheduler/runner and tracker reader.

## 12. Prompt Construction

- Render with strict variable/filter checking.
- Convert issue object keys to strings for template compatibility.
- Preserve nested arrays/maps for template iteration.
- `attempt` passed to template for different first-run vs retry vs continuation instructions.
- Rendering failures fail the run attempt immediately.

## 13. Logging, Status, and Observability

### 13.1 Logging

Required context: issue_id, issue_identifier for issue logs; session_id for agent lifecycle. Stable `key=value` format with action outcomes and failure reasons.

### 13.2 Runtime Snapshot (Optional)

Should return: running sessions (with turn_count), retry queue, codex_totals (input/output/total tokens, seconds_running), rate_limits.

### 13.3 Token Accounting

- Prefer absolute thread totals (e.g. `thread/tokenUsage/updated`).
- Ignore delta-style payloads for dashboard totals.
- Track deltas relative to last reported to avoid double-counting.
- Runtime reported as live aggregate at snapshot time.

### 13.4 Rate-Limit Tracking

Track latest rate-limit payload seen in any agent update. Human-readable presentation is implementation-defined.
