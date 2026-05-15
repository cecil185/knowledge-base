---
title: Harness Engineering
updated: 2026-05-15
sources: [raw/redhat-harness-engineering-structured-workflows.md, raw/propel-agentic-code-review-guardrails.md, raw/max-woolf-ai-agent-coding-skeptic.md, raw/openai-symphony-codex-orchestration-spec-part-1.md]
related: [agentic-coding, workflow-over-model, constraint-driven-prompting, repo-local-agent-instructions, spec-driven-development, guardrails-for-ai-coding, issue-tracker-as-control-plane, multi-agent-orchestration]
---
## Summary
The discipline of designing the structured environment — repository layout, instruction files, task templates, tool access — in which an AI agent operates. The governing principle is "structure in, structure out": agent reliability is a function of harness quality, not just model quality.

## Details
Harness engineering treats the repository as the agent's operating environment and the single source of truth. Errors are not first attributed to the model; they are traced backward to the harness inputs that allowed the error. This inverts the usual debugging instinct.

### Repository as single source of truth
The repo holds the spec, the rules, the conventions, and the verifiable acceptance criteria. Agents read from it; they don't infer from chat history. This makes runs reproducible and makes the harness — not the prompt — the durable artifact.

### Two-phase workflow
Red Hat's pattern, mirrored elsewhere:
1. **Phase 1 — Repository Impact Map**: agent uses LSP/MCP to identify every file the change touches, every caller, every dependency. Output: a map for human review.
2. **Human checkpoint**: a person validates the map before any code is written. Cheap to correct here, expensive to correct after implementation.
3. **Phase 2 — Structured Task Execution**: agent implements against a fixed template with no ambiguity left.

### The structured task template
Five sections, used verbatim:
- **Repository** — which repo, which branch
- **Files to Modify** — explicit paths
- **Implementation Notes** — constraints and approach
- **Acceptance Criteria** — verifiable conditions
- **Test Requirements** — what tests must exist and pass

### Tracing errors backward
When the agent produces wrong output, the question is "what was missing or ambiguous in the harness?" — not "what's wrong with the model?" Missing constraint? Add it to AGENTS.md or CLAUDE.md. Wrong assumption? Add a prohibition. See [[Constraint-Driven Prompting]] and [[Repo-Local Agent Instructions]].

### Constraining the solution space
Open-ended prompts produce unpredictable output. The harness narrows the solution space ahead of time: which tools (uv, polars), which conventions, which formats, which prohibited patterns. Symphony goes further by structuring the dispatch layer itself — Linear tickets as the unit of work, WORKFLOW.md as the in-repo policy, agents that write status back to the tracker. See [[Issue Tracker as Control Plane]].

## Tradeoffs / When to use
Gains: dramatic improvement in agent reliability without changing the model; reproducibility; clear failure attribution; lower verification load because the agent is solving a narrower problem.
Costs: upfront investment in CLAUDE.md, AGENTS.md, templates, and impact-map tooling; ongoing maintenance as the repo evolves; harness drift if not treated as first-class code.
Fits well: teams shipping with agents in production, repos large enough that context selection matters, any setting with multiple agents running in parallel. Fits poorly: throwaway scripts and one-off prototypes where the setup cost exceeds the run.

## Key tools / implementations
- [[Claude Code]] — reads CLAUDE.md as its harness file
- [[OpenAI Codex]] — reads AGENTS.md
- [[MCP]] — protocol for exposing repo tools (LSP, search) to agents
- [[Symphony]] — extends harness engineering to the orchestration layer via WORKFLOW.md

## Sources
- [[raw/redhat-harness-engineering-structured-workflows]] — coined term; two-phase workflow; structured task template; "structure in, structure out"
- [[raw/propel-agentic-code-review-guardrails]] — guardrail stack as part of the harness
- [[raw/max-woolf-ai-agent-coding-skeptic]] — AGENTS.md as system prompt; prohibitions and mandates
- [[raw/openai-symphony-codex-orchestration-spec-part-1]] — harness extended to dispatch and orchestration

## Backlinks
- [[Agentic Coding]]
- [[Constraint-Driven Prompting]]
- [[Iterative Chunking]]
- [[MCP (Model Context Protocol)]]
- [[Repo-Local Agent Instructions]]
- [[Verifiability Boundary]]
