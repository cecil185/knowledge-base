---
title: Skills And Reusable Instructions
updated: 2026-05-15
sources: [raw/addy-osmani-llm-coding-workflow-2026.md, raw/developers-digest-hn-ai-coding-agents-2026.md]
related: [repo-local-agent-instructions, workflow-over-model, harness-engineering, constraint-driven-prompting]
---
## Summary
Packaged, project-specific instruction bundles invoked as reusable units rather than re-prompted each session. The slogan from the HN consensus is "skills over prompting" — skills compress context, make tool usage predictable, and standardize behavior across teammates.

## Details
A skill is a named, parameterized instruction package: a description of when to use it, the steps it performs, the tools it expects, and any prohibitions. Once defined, it is invoked by name — the agent loads the full instruction set without the user re-typing conventions.

Compared with ad-hoc prompting, skills:
- **Compress context** — invocation is a name, not a paragraph
- **Make tool usage predictable** — explicit tool mandates inside the skill
- **Reduce convention repetition** — conventions live once, referenced everywhere
- **Standardize behavior across teams** — every dev's agent runs the same recipe

Claude Skills are the canonical implementation; the pattern generalizes to any agent harness. Skills sit alongside [[Repo-Local Agent Instructions]] — rules files define the always-on baseline, skills define on-demand recipes.

The Developers Digest framing is sharper: "the real product is the [[Workflow Over Model]]." Skills are the unit of that workflow.

## Tradeoffs / When to use
**Gains:** lower cognitive load at prompt time; reproducible outputs across runs; the skill itself becomes a versioned artifact that improves over time.
**Costs:** upfront authoring effort; skill sprawl if not curated; skills can become stale as the codebase evolves; over-reliance can hide what the agent is actually doing.
**Fit:** recurring workflows (commit, MR creation, ticket refinement, test writing) — anywhere you'd otherwise paste the same instructions repeatedly.

## Key tools / implementations
- [[Claude Code]] — Claude Skills are the reference implementation
- [[MCP]] — skills can mandate MCP tool usage as part of their recipe

## Sources
- [[raw/addy-osmani-llm-coding-workflow-2026]] — Claude Skills cited as part of the modern AI-augmented workflow
- [[raw/developers-digest-hn-ai-coding-agents-2026]] — "skills over prompting"; skills as reusable, project-specific instruction packages

## Backlinks
_No backlinks yet._
