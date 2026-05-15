---
title: Playwright
updated: 2026-05-15
sources: [raw/shiplight-complete-guide-e2e-testing-2026.md]
related: [shiplight]
---
## Purpose
Dominant open-source browser automation framework for end-to-end web testing across Chromium, Firefox, and WebKit.

## How it works
Drives real browsers via the DevTools / WebKit / Gecko protocols, exposing a unified API for navigation, interaction, and assertion. Tests are written in code (TypeScript, Python, Java, .NET) and target CSS, XPath, or accessibility-tree selectors. Auto-wait, network interception, and trace viewer come built in.

It is the de-facto execution layer for higher-level testing platforms — AI-native tools like [[Shiplight]] sit on top of Playwright rather than replacing it, using it to actually drive the browser once intents are resolved.

## Strengths
- Cross-browser by default (Chromium / Firefox / WebKit) with one API.
- Strong DevTools integration: traces, screenshots, video, network mocking.
- Solid auto-wait behavior reduces flakiness vs older Selenium-style frameworks.
- Large ecosystem and active maintenance — safe default for greenfield E2E.
- Good substrate for [[Intent-Based Testing]] layers that need a reliable runtime.

## Weaknesses
- Selector-based: tests break when the DOM changes, driving the maintenance burden that motivates [[Self-Healing Tests]].
- Authoring requires engineering time per test — does not scale to dozens of flows without [[Agentic Coding]] assistance.
- No native triage between "real regression" and "intentional change".
- Test pyramid economics still apply: hundreds of poorly-maintained Playwright tests are worse than 30-50 targeted ones.

## Alternatives
- Cypress — developer-centric alternative; simpler DX but weaker multi-browser story and runs in-browser rather than driving it.
- [[Shiplight]] — AI-native layer that uses Playwright underneath and adds intent authoring + self-healing.
- Selenium — older, broader language support, weaker ergonomics.

## Sources
- [[raw/shiplight-complete-guide-e2e-testing-2026]] — positions Playwright as the standard E2E engine and as the substrate for AI-native testing tools.

## Backlinks
- [[Intent-Based Testing]]
- [[Self-Healing Tests]]
- [[Shiplight]]
- [[Verification Bottleneck]]
