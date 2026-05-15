---
title: Claude Code
updated: 2026-05-15
sources: [raw/addy-osmani-llm-coding-workflow-2026.md, raw/simon-willison-eight-years-building-with-ai.md, raw/simon-willison-scaling-autonomous-coding.md]
related: [openai-codex, mcp, symphony]
---
## Purpose
Anthropic's terminal-native AI coding agent — runs in the developer's repo, follows repo-local rules, and operates as a director-style collaborator or as a worker inside larger agent swarms.

## How it works
Claude Code attaches to a working directory and reads `CLAUDE.md` as its persistent system prompt — style guides, build commands, conventions, and prohibitions. Reusable behaviors live in **Claude Skills**: discoverable, prompt-packaged capabilities the agent can load on demand instead of receiving them in every turn. The model exposes file edit, shell, and search tools, and integrates with [[MCP]] servers for external data (browser, docs, project tracker). Sub-agents can be spawned to handle delimited tasks — the pattern Simon Willison uses in his [[Hierarchical Agent Systems]] (planner → sub-planner → worker → judge) — letting the parent context stay focused while children burn tokens on subtasks.

It is the canonical example of [[Repo-Local Agent Instructions]] and the agent of choice for [[Agentic Coding]] workflows where the human reviews output rather than every line.

## Strengths
- Terminal-native; works in the same environment as the developer's editor and CI
- `CLAUDE.md` makes project context portable across sessions
- Claude Skills externalize reusable workflows so prompts stay short
- Spawns sub-agents cleanly — used in FastRender's swarm that produced 1M+ lines / 1000 files in under a week
- Strong on judgment-light implementation (Willison's syntaqlite went from 8-year concept to 3 months of active building)
- Pairs well with [[OpenAI Codex]] in cross-model review chains

## Weaknesses
- Quality depends heavily on `CLAUDE.md` discipline — sparse rules = sparse results
- Like all LLM coders, behaves as an "over-confident junior developer" — outputs require [[Risk-Tiered Review]]
- Vibe-coding mode is fine for personal projects, dangerous for shipping code
- Falls into the [[Refactoring Trap]] — cheap to change anything, so architectural debt accumulates

## Alternatives
- [[OpenAI Codex]] — OpenAI's app-server agent, often chained after Claude in optimization sequences
- GitHub Copilot Agent, Google Jules, Cursor — competing IDE/CLI agents

## Sources
- [[raw/addy-osmani-llm-coding-workflow-2026]] — Claude Code as director-style CLI with `CLAUDE.md` rules and Skills
- [[raw/simon-willison-eight-years-building-with-ai]] — used to build syntaqlite, momentum-not-judgment framing
- [[raw/simon-willison-scaling-autonomous-coding]] — sub-agent hierarchical pattern in the FastRender swarm

## Backlinks
- [[Agentic Coding]]
- [[Constraint-Driven Prompting]]
- [[Cross-Model Review]]
- [[Harness Engineering]]
- [[Hierarchical Agent Systems]]
- [[Iterative Chunking]]
- [[MCP (Model Context Protocol)]]
- [[Multi-Agent Orchestration]]
- [[OpenAI Codex]]
- [[Parallel Agent Deployment]]
- [[Refactoring Trap]]
- [[Repo-Local Agent Instructions]]
- [[Skills And Reusable Instructions]]
- [[Spec-Driven Development]]
- [[Verifiability Boundary]]
- [[Workflow Over Model]]
