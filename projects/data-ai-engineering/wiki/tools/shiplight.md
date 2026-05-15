---
title: Shiplight
updated: 2026-05-15
sources: [raw/shiplight-complete-guide-e2e-testing-2026.md, raw/shiplight-openai-codex-testing.md]
related: [playwright, openai-codex, mcp]
---
## Purpose
AI-native end-to-end testing platform that authors, runs, and maintains browser tests as natural-language intents — built for teams shipping AI-generated code at high velocity.

## How it works
Tests are declared in YAML with three fields: `goal`, `base_url`, and a list of `statements` covering URL navigation, intent-based actions, and `VERIFY` assertions. At runtime an AI layer translates intents into concrete browser actions executed via a [[Playwright]]-backed engine.

Three pieces extend developer environments:
- **Shiplight Plugins** plug into existing dev environments (IDE, local stacks) so tests author and run in-place.
- **Shiplight browser MCP server** exposes live browser verification to any [[MCP]]-aware agent, so coding agents can validate their own changes in a real browser before opening a PR.
- **Shiplight GitHub Action** (`shiplight-ai/github-action@v1`) runs the suite on every PR as a regression gate for AI-authored changes.

Two AI capabilities make the platform practical at scale:
- **Auto test generation** records browser sessions and emits YAML test files, supporting [[Intent-Based Testing]] without hand-authoring locators.
- **3-tier [[Self-Healing Tests]]**: cached selector → AI resolution against current DOM → cache update for next run. Triage layer distinguishes genuine regressions from intentional UI changes so updated app behavior auto-updates the test rather than failing it.

## Strengths
- Tests survive refactors — intents persist while selectors don't, eliminating the dominant E2E maintenance cost.
- Native fit for AI-generated PRs: covers the four AI-code failure modes (unspecified edge cases, cross-browser incompatibility, unexpected feature interactions, real-world integration failures) that unit tests miss.
- Agent-driven test generation shifts E2E left; coding agents can author and run their own E2E coverage via the browser MCP server.
- Intelligent triage cuts the false-positive noise that kills traditional E2E suites.
- YAML format is reviewable in PRs and diffable across changes.

## Weaknesses
- AI resolution adds latency vs raw [[Playwright]] selectors; cached path is fast, cold path is not.
- Self-healing can mask real regressions if triage misclassifies an intentional break as a UI drift.
- Natural-language intents require disciplined phrasing — vague goals produce flaky tests.
- Locks the team into Shiplight's hosted intent runtime and triage; less portable than plain Playwright.

## Alternatives
- [[Playwright]] — raw open-source automation, no AI layer.
- Cypress — developer-centric E2E framework, no AI authoring/healing.
- Hand-rolled Playwright + LLM glue — possible but reinvents the triage and caching layers.

## Sources
- [[raw/shiplight-complete-guide-e2e-testing-2026]] — full platform overview, test pyramid → diamond shift, self-healing 3-phase mechanism, YAML format.
- [[raw/shiplight-openai-codex-testing]] — integration with [[OpenAI Codex]] PRs, browser MCP server, GitHub Action, four AI-code failure modes.

## Backlinks
- [[Intent-Based Testing]]
- [[Playwright]]
- [[Self-Healing Tests]]
- [[Verifiability Boundary]]
- [[Verification Bottleneck]]
