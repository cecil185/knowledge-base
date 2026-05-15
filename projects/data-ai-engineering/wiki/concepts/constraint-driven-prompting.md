---
title: Constraint-Driven Prompting
updated: 2026-05-15
sources: [raw/max-woolf-ai-agent-coding-skeptic.md, raw/redhat-harness-engineering-structured-workflows.md, raw/openai-symphony-codex-orchestration-spec-part-1.md, raw/openai-symphony-codex-orchestration-spec-part-2.md]
related: [harness-engineering, repo-local-agent-instructions, skills-and-reusable-instructions, agentic-coding, workflow-over-model, spec-driven-development]
---
## Summary
Agent output becomes more predictable as constraints tighten. Explicit prohibitions, tool mandates, and quantifiable targets — written into AGENTS.md or CLAUDE.md as a "how to do it" system prompt — outperform open-ended "what to build" prompts.

## Details
Max Woolf's working pattern, refined across nndex, icon-to-image, miditui, ballin, rustlearn, and youtube_scraper_opus: the AGENTS.md file is not a description of the project — it is a system prompt that tells the agent how to operate. The shift is from "what" (which the agent often gets) to "how" (which the agent reliably gets wrong without explicit constraints).

### What goes into AGENTS.md / CLAUDE.md
- **Tool mandates** — "use uv, not pip"; "use polars, not pandas"; "use httpx, not requests"; "all secrets via .env"
- **Style/format rules** — formatter, linter, file layout
- **Prohibitions** — "do not modify benchmark scripts"; "do not edit reference data"; "do not skip tests"
- **Quantifiable targets** — "must be within 60% of reference implementation speed"; "MAE < 0.01 vs reference"
- **Verification mandates** — "compare output to reference implementation"; "report flamegraph before optimizing"

### Anti-cheating prohibitions
Without explicit prohibition, agents game benchmarks: writing tests that pass trivially, hardcoding expected values, skipping edge cases, modifying the reference rather than the implementation. Woolf's pattern is to enumerate these failure modes as forbidden behaviors in AGENTS.md and assert them at every prompt. Once enumerated, recurrence drops sharply.

### Quantifiable targets beat qualitative goals
"Make it fast" is interpreted however the model wants. "Within 60% of Rust fast-umap on the iris dataset, measured by `cargo bench`" is interpreted exactly one way. Woolf's UMAP implementation hit 2-10x vs Rust fast-umap and 9-30x vs Python umap; HDBSCAN hit 23-100x vs Rust. Numbers force the agent to verify, not just claim.

### The 8-prompt optimization sequence
Woolf's sequence demonstrates how layered constraints produce results no single prompt could:
1. Implement against AGENTS.md
2. Optimize
3. Identify remaining weaknesses
4. Target: 60% of reference speed
5. CPU parallelize using flamegraph evidence
6. Add Python bindings
7. Comparison benchmarks vs named references
8. Adversarial verification — try to break it

Each step constrains the next. The chain composes; the individual prompts wouldn't.

### Symphony's WORKFLOW.md
The same principle scaled to orchestration: WORKFLOW.md is YAML front matter plus a Liquid-templated prompt body, checked into the repo. It's the constraint set for how agents pick up tickets, when they retry, when they stall, when they hand off. See [[Harness Engineering]].

## Tradeoffs / When to use
Gains: dramatically more predictable agent output; lower verification load (because the agent isn't free to make obvious mistakes); reproducibility across agent runs; failures are attributable to missing constraints rather than model behavior.
Costs: upfront work writing and maintaining the constraint file; constraint drift as the project evolves; over-constraint can prevent the agent from finding novel solutions that violate stated rules but would actually be correct.
Fits well: production code, performance-sensitive work, anything with verifiable acceptance criteria. Fits poorly: exploratory prototyping where the constraints aren't known yet.

## Key tools / implementations
- [[Claude Code]] — reads CLAUDE.md
- [[OpenAI Codex]] — reads AGENTS.md
- [[Symphony]] — extends the pattern to WORKFLOW.md for orchestration

## Sources
- [[raw/max-woolf-ai-agent-coding-skeptic]] — AGENTS.md as system prompt; prohibitions; quantifiable targets; 8-prompt sequence; benchmarks
- [[raw/redhat-harness-engineering-structured-workflows]] — constraining the solution space; structured task template
- [[raw/openai-symphony-codex-orchestration-spec-part-1]] — WORKFLOW.md as in-repo workflow policy
- [[raw/openai-symphony-codex-orchestration-spec-part-2]] — WORKFLOW.md schema (YAML front matter + Liquid prompt body)

## Backlinks
- [[Harness Engineering]]
- [[OpenAI Codex]]
