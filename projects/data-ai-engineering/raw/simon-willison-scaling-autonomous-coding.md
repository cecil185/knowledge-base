# Scaling Long-Running Autonomous Coding (Simon Willison)

**Source:** https://simonwillison.net/2026/Jan/19/scaling-long-running-autonomous-coding/
**Read:** 2026-05-10

## Overview

Simon Willison reports on Cursor's experiment using swarms of AI coding agents to build a functional web browser from scratch, demonstrating significant progress toward his 2026 AI-assisted coding predictions.

## The Experiment

Cursor ran hundreds of concurrent autonomous agents coordinating on a single project, generating "over a million lines of code and trillions of tokens" across 1,000 files written in under a week.

## Key Architecture: Hierarchical Agent System

The system employed a multi-tier hierarchical approach:

- **Planner agents** — created high-level tasks
- **Sub-planner agents** — refined and decomposed tasks further
- **Worker agents** — executed individual coding tasks
- **Judge agents** — evaluated task completion status

This mirrors Claude Code's sub-agent methodology and represents a pattern for scaling autonomous coding sessions beyond what a single context window can handle.

## Test Case: FastRender Browser

The agents built a web browser in Rust. Key implementation details:

- The FastRender repository includes Git submodules containing the WhatWG and CSS-WG specifications, providing agents with reference materials for implementation decisions
- Functional rendering of websites like Google and personal blogs was achieved
- Obvious rendering glitches in screenshots indicate a genuine custom implementation rather than a wrapped existing engine
- Initial skepticism arose when GitHub Actions CI failed and build documentation was missing — both issues were resolved within 24 hours

## Results and Assessment

Willison successfully compiled and tested the browser on macOS. Screenshots showed mostly legible pages with visible rendering issues (misaligned buttons, incorrect text styling).

His assessment: "I don't think we'll see projects of this nature compete with Chrome or Firefox" soon, but the capability emerged faster than he originally predicted (he had forecast such achievements by 2029, not 2026).

A concurrent HiWave browser project emerged similarly within weeks, suggesting this pattern is replicable.

## Key Takeaways for Scaling Autonomous Coding

1. **Hierarchical planning is essential** — planner/sub-planner/worker/judge separation enables parallelism and quality control at scale
2. **Judge agents as verification layer** — automated quality assessment is necessary when human review of millions of lines is infeasible
3. **Embed reference specs in the repo** — including WhatWG/CSS-WG specs as submodules gave agents grounding in authoritative sources
4. **CI failures are expected and recoverable** — the 24-hour resolution of CI issues shows that autonomous runs produce imperfect-but-fixable output
5. **Scope to a well-defined problem** — building a browser is a constrained, verifiable problem that suits autonomous coding well

## Context

This builds on Willison's broader 2026 predictions about AI-assisted development and aligns with the emerging pattern of agent swarms replacing single long-context sessions for large codebases.
