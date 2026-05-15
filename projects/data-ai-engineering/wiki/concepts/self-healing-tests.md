---
title: Self-Healing Tests
updated: 2026-05-15
sources: [raw/shiplight-complete-guide-e2e-testing-2026.md]
related: [intent-based-testing, verification-bottleneck, agentic-coding, guardrails-for-ai-coding]
---
## Summary
E2E tests that auto-recover from UI changes by resolving element locators through AI on failure, then updating a cache so subsequent runs are fast and deterministic. Removes the dominant maintenance cost of E2E suites and makes the test diamond (more E2E, fewer mocks) practical.

## Details
The mechanism is a three-phase loop:

1. **Cache locators** — first run resolves each intent ("click the checkout button") into a concrete DOM locator and caches it. Subsequent runs use the cached locator directly: fast, deterministic.
2. **AI-based element resolution on failure** — when a cached locator no longer matches (button moved, class renamed, layout refactored), the AI layer re-resolves the intent against the new DOM.
3. **Auto-update cache** — the new locator overwrites the cached value, so the next run is fast again.

The economics of E2E flip. In a classic pyramid, E2E is the smallest tier precisely because each test is expensive to maintain — selector churn forces constant rewrites. With self-healing, maintenance amortizes to near-zero for the common case (cosmetic refactors), and the pyramid widens at the top into a **diamond**: more E2E coverage becomes economically viable.

Pairs tightly with [[Intent-Based Testing]] — intent is the input the AI resolver matches against; self-healing is what keeps the resolver's cache current.

## Tradeoffs / When to use
**Gains:** maintenance burden collapses; tests survive UI refactors including those from [[Agentic Coding]]; broader E2E coverage becomes practical; less flakiness from stale selectors.
**Costs:** trust depends on AI element-resolution accuracy — a wrong resolution can silently test the wrong thing; auto-updating the cache can mask genuine regressions if the AI "fixes" a test that should have failed; vendor dependency; debugging requires understanding both the test and the resolver.
**Fit:** UIs that change frequently (active product development, AI-driven refactor cycles); test suites large enough that selector maintenance is a real cost. Less useful for tiny suites or frozen UIs.

## Key tools / implementations
- [[Shiplight]] — three-phase self-healing built into the test runner
- [[Playwright]] — underlying automation surface

## Sources
- [[raw/shiplight-complete-guide-e2e-testing-2026]] — three-phase mechanism, pyramid → diamond shift, maintenance economics

## Backlinks
- [[Intent-Based Testing]]
- [[Playwright]]
- [[Shiplight]]
