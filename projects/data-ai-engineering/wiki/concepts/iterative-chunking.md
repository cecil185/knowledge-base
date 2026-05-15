---
title: Iterative Chunking
updated: 2026-05-15
sources: [raw/addy-osmani-llm-coding-workflow-2026.md, raw/max-woolf-ai-agent-coding-skeptic.md, raw/redhat-harness-engineering-structured-workflows.md]
related: [agentic-coding, constraint-driven-prompting, spec-driven-development, harness-engineering, verifiability-boundary, guardrails-for-ai-coding, workflow-over-model]
---
## Summary
Iterative chunking is the discipline of decomposing AI coding work into small, focused tasks instead of issuing monolithic prompts. Small chunks produce reviewable, correct code; granular commits become save points; and each chunk lands on the verifiable side of the boundary where you can prove it works before moving on.

## Details

### Why chunks beat monoliths
Addy Osmani's mental model is the "over-confident junior developer": ask for a whole feature and you get plausible code that looks right and isn't. Ask for one well-scoped piece, review it, commit it, then ask for the next — and each step becomes inspectable. The chunk size is set by the reviewer's capacity to verify, not the model's capacity to generate.

### Context packaging
Every chunk needs enough context to be solved standalone:
- The relevant files (not the whole repo).
- The spec or acceptance criteria for *this chunk only*.
- Examples of the existing patterns to follow.
- The verification step (test, type-check, benchmark) that closes the loop.

Tools like `gitingest` and `repo2txt` exist specifically to package context efficiently. Rules files ([[Repo-Local Agent Instructions|CLAUDE.md / GEMINI.md / AGENTS.md]]) supply the always-relevant context so each chunk only needs the task-specific delta.

### Granular commits as save points
Each successful chunk gets its own commit. Benefits:
- Clean rollback when the next chunk derails.
- Reviewable history — each commit corresponds to one verifiable claim.
- Bisection actually works.
- The AI can be re-prompted from a known-good state.

This pairs directly with [[Risk-Tiered Review]]: smaller chunks fall into lower risk tiers, accelerating merge.

### Woolf's 8-prompt optimization sequence
Max Woolf's worked example shows what disciplined chunking looks like for performance work. Each prompt is a self-contained, benchmark-verifiable step:

1. **Implement** the baseline working version.
2. **Optimize** the obvious hot paths.
3. **Identify weaknesses** — ask the model to critique its own code.
4. **60% speed target** — explicit numeric constraint forces real work, not cosmetic tweaks.
5. **CPU parallelize** using a flamegraph as input (grounded analysis, not guessing).
6. **Python bindings** via PyO3/maturin — wrap for ergonomic use.
7. **Comparison benchmarks** against reference implementations (fast-umap, xgboost, etc.).
8. **Adversarial verification** — generate test cases designed to break the result.

The sequence delivered concrete wins: UMAP 2–10x vs Rust fast-umap and 9–30x vs Python umap; HDBSCAN 23–100x vs Rust hdbscan; GBDT 24–42x vs xgboost. Each step was verifiable against a benchmark, which is exactly why the chain held together — see [[Verifiability Boundary]].

### Connection to harness engineering
Red Hat's [[Harness Engineering]] makes chunking structural: a Repository Impact Map (Phase 1) decomposes the work into a task list with a fixed template (Files to Modify, Implementation Notes, Acceptance Criteria, Test Requirements). Each task is a pre-packaged chunk; the harness does the chunking so the operator doesn't have to.

## Tradeoffs / When to use
- **Gain:** review keeps up with generation; defect rate drops; rollback is cheap; AI stays on rails because the rails are short.
- **Cost:** more prompt overhead per unit of code; requires upfront decomposition; feels slower in the moment than "build the whole thing."
- **Fits:** production code, performance work, anything where defects are expensive.
- **Poor fit:** one-shot scripts or throwaway prototypes where review isn't needed.

## Key tools / implementations
- [[Claude Code]] / [[OpenAI Codex]] — agents that work well with small focused turns and structured task input.
- [[Linear]] — issue tracker that naturally maps to chunk-sized units of work (see [[Issue Tracker as Control Plane]]).
- [[Symphony]] — orchestration over chunk-sized tickets with per-issue workspace isolation.

## Sources
- [[raw/addy-osmani-llm-coding-workflow-2026]] — small focused tasks, context packaging, granular commits, over-confident-junior mental model.
- [[raw/max-woolf-ai-agent-coding-skeptic]] — the 8-prompt optimization sequence with benchmark verification at every step.
- [[raw/redhat-harness-engineering-structured-workflows]] — structured task template that operationalizes chunking.

## Backlinks
- [[Guardrails for AI Coding]]
- [[Verifiability Boundary]]
- [[Workflow Over Model]]
