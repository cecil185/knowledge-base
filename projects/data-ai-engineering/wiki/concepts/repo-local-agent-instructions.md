---
title: Repo-Local Agent Instructions
updated: 2026-05-15
sources: [raw/addy-osmani-llm-coding-workflow-2026.md, raw/max-woolf-ai-agent-coding-skeptic.md, raw/redhat-harness-engineering-structured-workflows.md, raw/openai-symphony-codex-orchestration-spec-part-1.md, raw/openai-symphony-codex-orchestration-spec-part-2.md, raw/developers-digest-hn-ai-coding-agents-2026.md]
related: [skills-and-reusable-instructions, harness-engineering, constraint-driven-prompting, spec-driven-development, workflow-over-model]
---
## Summary
Agent behavior rules — style, process, prohibitions, tool mandates — stored as version-controlled files in the repo (CLAUDE.md, AGENTS.md, GEMINI.md, WORKFLOW.md, SPEC.md). The repository becomes the single source of truth for both code and the prompts that produce it, so every agent invocation inherits the same context without restating it.

## Details
Repo-local instruction files act as a persistent system prompt scoped to the project. Max Woolf treats `AGENTS.md` as "how to do it, not what" — listing constraints, prohibitions, and tool mandates that shape every turn. Addy Osmani's workflow pairs `CLAUDE.md`/`GEMINI.md` rules files (style + process) with per-feature `spec.md` documents. Red Hat's [[Harness Engineering]] frames this as "structure in, structure out": the repo is the grounding source the agent reads first.

OpenAI's Symphony spec elevates this further with `WORKFLOW.md` — a YAML front matter (orchestration parameters, polling intervals, timeouts) plus a Liquid template body that the orchestrator renders into the per-issue prompt. Configuration becomes documentation; documentation becomes the runtime contract.

The core pattern: prompts and configs are versioned, reviewed, and diffed like code. Changes to agent behavior ship through PRs.

## Tradeoffs / When to use
**Gains:** consistent agent behavior across teammates and sessions; convention enforcement without per-prompt repetition; auditable history of how rules evolved; new contributors (human or agent) onboard from the same file.
**Costs:** rules files drift if not maintained; over-specification can constrain the agent counterproductively; benefits scale with team size — a solo dev may find them overkill.
**Fit:** strongest where multiple agents/devs share the repo, where conventions are non-obvious, or where prohibitions (no benchmark cheating, no skipping tests) materially change output quality.

## Key tools / implementations
- [[Claude Code]] — reads `CLAUDE.md` automatically
- [[OpenAI Codex]] — reads `AGENTS.md`
- [[Symphony]] — `WORKFLOW.md` (YAML + Liquid) and `SPEC.md`
- [[MCP]] — tools the rules file can mandate

## Sources
- [[raw/addy-osmani-llm-coding-workflow-2026]] — CLAUDE.md/GEMINI.md rules files with style and process
- [[raw/max-woolf-ai-agent-coding-skeptic]] — AGENTS.md as system prompt with prohibitions and tool mandates
- [[raw/redhat-harness-engineering-structured-workflows]] — repository as single source of truth for grounded analysis
- [[raw/openai-symphony-codex-orchestration-spec-part-1]] — SPEC.md and WORKFLOW.md as in-repo orchestration policy
- [[raw/openai-symphony-codex-orchestration-spec-part-2]] — WORKFLOW.md YAML front matter + Liquid prompt body mechanism
- [[raw/developers-digest-hn-ai-coding-agents-2026]] — standardize project context via repo-local instructions

## Backlinks
- [[Claude Code]]
- [[Harness Engineering]]
- [[Skills And Reusable Instructions]]
- [[Workflow Over Model]]
