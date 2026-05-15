---
title: MCP (Model Context Protocol)
updated: 2026-05-15
sources: [raw/addy-osmani-llm-coding-workflow-2026.md, raw/redhat-harness-engineering-structured-workflows.md, raw/shiplight-openai-codex-testing.md]
related: [claude-code, openai-codex, symphony, shiplight]
---
## Purpose
Open protocol for connecting AI agents to external tools and data sources — the standard plumbing layer for [[Harness Engineering]], turning ad-hoc agent integrations into reusable structured inputs.

## How it works
MCP defines a uniform JSON-based interface for an agent to call out to "servers" that wrap external systems — documentation, browsers, project trackers, CI, runtime metrics. Each server exposes tools and resources the agent can discover and invoke. Notable servers in the 2026 AI-coding stack:

- **Context7** — automated context packaging. Pulls library docs, examples, and types into the prompt so the agent has authoritative reference material instead of hallucinating APIs.
- **Chrome DevTools MCP** — bridges static analysis and live execution. The agent can navigate, inspect DOM, read console errors, and verify behavior in a real browser.
- **Shiplight browser MCP server** — used by [[OpenAI Codex]] for live browser verification of AI-generated UI code; the regression gate that catches the 4 AI-code failure modes (unspecified edge cases, cross-browser incompatibility, unexpected feature interactions, real-world integration failures).
- **Linear GraphQL MCP extension** — the `linear_graphql` tool that [[Symphony]] uses to read/write tickets as its control plane.
- **CI / deployment / runtime MCPs** — supply structured CI status, deployment logs, and runtime metrics into Red Hat's [[Harness Engineering]] two-phase workflow (Repository Impact Map → human checkpoint → Structured Task Execution).

The protocol's value is **structure in, structure out**: agents get grounded inputs (real APIs, real test runs, real metrics) instead of paraphrased prompts.

## Strengths
- Standard interface — one protocol, many servers, agent-agnostic
- Closes the gap between agents and live systems (browser, CI, tracker)
- Enables verification loops that defeat AI hallucination
- Already used by [[Claude Code]], [[OpenAI Codex]], and [[Symphony]] — broad adoption
- Composable: stack Context7 + Chrome DevTools + Linear in a single workflow

## Weaknesses
- Server quality varies wildly — bad servers leak tokens and noise into the agent's context
- Auth, rate limits, and sandboxing are server-by-server concerns
- No standard for cost accounting across servers
- Easy to over-load an agent with too many tools, degrading reasoning

## Alternatives
- OpenAI function calling / tool-use APIs — vendor-specific, less portable
- LangChain tools, custom integration scripts — pre-MCP approach, now legacy

## Sources
- [[raw/addy-osmani-llm-coding-workflow-2026]] — Context7 and Chrome DevTools MCP in the daily LLM coding workflow
- [[raw/redhat-harness-engineering-structured-workflows]] — MCP as the structured-input mechanism for harness engineering
- [[raw/shiplight-openai-codex-testing]] — Shiplight browser MCP for live verification of Codex output

## Backlinks
_No backlinks yet._
