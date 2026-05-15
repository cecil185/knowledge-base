---
title: Cross-Model Review
updated: 2026-05-15
sources: [raw/addy-osmani-llm-coding-workflow-2026.md, raw/max-woolf-ai-agent-coding-skeptic.md]
related: [multi-agent-orchestration, verification-bottleneck, agentic-coding, constraint-driven-prompting, spec-driven-development]
---
## Summary
Using a second AI session — typically from a different model family — to critique or extend the first model's output. The independence between models surfaces errors that no single model would catch on itself, and chained models can produce cumulative improvements neither model produces alone.

## Details
An LLM is the worst possible auditor of its own output: its blind spots are baked into both the writing pass and the review pass. Cross-model review breaks the symmetry by routing the diff through a different model whose training, tokenizer, and failure modes are uncorrelated with the writer's.

### Two patterns
**Parallel cross-check.** Run the same prompt through 2–3 different models and compare approaches. Differences flag uncertainty; convergence is weak evidence of correctness. Useful early in a task to surface design alternatives.

**Sequential chain optimization.** Feed model A's output as input to model B with a "make this better" prompt. Max Woolf's published result: **Codex 5.3 → Opus 4.6 in sequence produces cumulative speedups exceeding what either model achieves alone** on the same optimization target. The 8-prompt sequence (implement → optimize → identify weaknesses → 60% speed target → CPU parallelize with flamegraph → Python bindings → comparison benchmarks → adversarial verify) is structured precisely to exploit this — each step hands a different shape of problem to whichever model handles it best.

### Domain-expert audit
A complementary pattern: a human with domain expertise inspects the output, identifies specific bugs, then describes them to an agent for a fix pass. The human supplies the judgment the model lacks; the model supplies the typing the human doesn't want to do. Woolf used this to debug Rust kernels and ML implementations where the model had introduced subtle correctness errors invisible without domain knowledge.

### Relationship to multi-agent orchestration
Cross-model review is a specific implementation of [[Multi-Agent Orchestration]] — the "different roles" decomposition becomes "different models." Both rest on the same thesis: agents can't reliably identify their own errors, so independent external validation is structural, not optional.

## Tradeoffs / When to use
**Gains:** catches errors invisible to single-model self-review; chained models produce results exceeding either alone; cheap relative to human review.
**Costs:** more tokens; latency multiplies with chain length; chains can amplify errors if early-stage hallucinations get optimized rather than corrected; requires a judgment call on which model goes where in the chain.
**Fits well when:** the output is verifiable (benchmarks, tests), or when a domain expert is in the loop to catch chain-amplified errors.
**Fits poorly when:** quick iteration matters more than quality, or when no clear verification signal exists to detect chain-amplification.

## Key tools / implementations
- Claude Opus 4.5 / 4.6 — used as the optimization / critique step.
- [[OpenAI Codex]] (5.3) — used as the implementation step in Woolf's chain.
- Claude Sonnet 4.5, GitHub Copilot — common alternatives in the cross-check pattern.
- [[Claude Code]] — frontend for running multiple model sessions in parallel.

## Sources
- [[raw/addy-osmani-llm-coding-workflow-2026]] — secondary AI session critiques the first; trying multiple models on the same prompt to cross-check approaches.
- [[raw/max-woolf-ai-agent-coding-skeptic]] — chain optimization (Codex 5.3 → Opus 4.6), the 8-prompt sequence, domain-expert audit pattern, adversarial verification against reference implementations.

## Backlinks
- [[OpenAI Codex]]
- [[Verification Bottleneck]]
