---
title: Intent-Based Testing
updated: 2026-05-15
sources: [raw/shiplight-complete-guide-e2e-testing-2026.md, raw/shiplight-openai-codex-testing.md]
related: [self-healing-tests, verification-bottleneck, agentic-coding]
---
## Summary
E2E tests authored as user intent — natural language or YAML — instead of DOM selectors and click coordinates. Because intent does not change when the UI is refactored, tests survive layout, framework, and styling churn that would break selector-based suites.

## Details
A traditional Playwright/Cypress test pins itself to specific selectors (`#submit-btn`, `[data-testid="cart"]`). Any refactor that renames or restructures those selectors breaks the test even though the user-visible behavior is unchanged. Intent-based tests invert this: the test describes what the user is trying to accomplish, and an AI layer resolves that intent against the live DOM at run time.

The Shiplight YAML format is representative:
- `goal:` — one-line summary of the user journey
- `base_url:` — entry point
- `statements:` — ordered list mixing URL navigation, natural-language intents ("click the checkout button", "enter test@example.com in the email field"), and `VERIFY` assertions ("verify the order confirmation page is shown")

Consequences:
- **Decoupled from implementation** — selector churn no longer breaks tests
- **Non-technical contributors can participate** — PMs and designers can read and edit YAML
- **Agent-driven test generation** — an agent can author the YAML by walking the app, shifting test creation left
- **Persistence across AI refactors** — particularly important when [[Agentic Coding]] is producing large diffs; the test survives the refactor that the test should be checking

## Tradeoffs / When to use
**Gains:** dramatically lower maintenance cost; test-as-documentation; agent-friendly authoring; tests don't rot during UI redesigns.
**Costs:** runtime AI resolution adds latency and a non-determinism budget; assertion granularity is coarser than a hand-written selector; debugging a failed intent ("could not find a checkout button") requires inspecting AI reasoning, not a stack trace; vendor lock-in to the resolver.
**Fit:** high-revenue, high-risk user flows (auth, checkout, key data paths) where stability matters more than fine-grained DOM control. Pairs naturally with [[Self-Healing Tests]].

## Key tools / implementations
- [[Shiplight]] — YAML intent format, browser MCP server, GitHub Action
- [[Playwright]] — underlying browser automation that intent layers compile down to
- [[OpenAI Codex]] — generates intent YAML from browser sessions

## Sources
- [[raw/shiplight-complete-guide-e2e-testing-2026]] — intent-based authoring as a pillar of modern E2E; test pyramid → diamond
- [[raw/shiplight-openai-codex-testing]] — YAML format details; intent-based persistence survives refactors of AI-generated code

## Backlinks
- [[Playwright]]
- [[Self-Healing Tests]]
- [[Shiplight]]
