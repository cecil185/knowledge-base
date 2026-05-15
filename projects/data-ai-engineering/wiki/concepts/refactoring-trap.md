---
title: Refactoring Trap
updated: 2026-05-15
sources: [raw/simon-willison-eight-years-building-with-ai.md]
related: [verifiability-boundary, agentic-coding, guardrails-for-ai-coding, ai-attributed-defect-tracking, harness-engineering]
---
## Summary
When AI makes refactoring nearly free, the discipline to make good architectural decisions upfront erodes — because there's always an apparent escape hatch. The trap is that cheap rewrites enable momentum, not judgment: AI accelerates implementation, but architectural debt still compounds, and the cost surfaces later as design that nobody chose deliberately.

## Details

### The cheap refactoring paradox
Simon Willison's eight-years retrospective names the core failure: when the marginal cost of changing code drops near zero, the felt urgency to get the design right also drops. Teams skip design discussions because "we can refactor later." Later arrives, and the codebase has accumulated structure by accretion rather than intent — a shape no one would have chosen on a whiteboard.

### Implementation vs design distinction
AI is reliably good at implementation: writing the code to a clear spec, fixing a typed test, mechanical refactors with stable interfaces. AI is unreliable at design: choosing the right abstraction, defining boundaries, deciding what to defer. The trap is conflating these — using AI-cheap implementation as evidence that design is also cheap. It isn't.

### Verifiability as the key signal
Willison's heuristic: *"Can you verify the output objectively?"*
- Yes (tests pass, types check, output matches reference) → AI is a force multiplier.
- No (is this the right architecture? is this the right abstraction?) → AI gives false confidence.

This is the boundary explored in [[Verifiability Boundary]]. Design decisions sit firmly on the unverifiable side, which is why the refactoring trap is specifically dangerous.

### Phase-appropriate AI usage
Safety decreases as you move toward design:

| Phase | AI value | AI risk | Verdict |
|---|---|---|---|
| Getting started (cold start) | High | None | Use freely |
| Implementation | High | Low | Use with tests |
| Refactoring | Medium | High | Use carefully |
| Architecture | Low | Very high | Not recommended |

The trap is using AI in the high-risk phases at the same intensity as the low-risk ones.

### Disposable prototypes pattern
Willison's own example: an 8-year conceptualization shipped in 3 months of AI-assisted building. The healthy pattern is to treat the first build as disposable — prove the idea works, then rebuild deliberately. The unhealthy pattern is to keep refactoring the prototype indefinitely because AI makes each refactor look cheap, never paying down the architectural debt.

The rule of thumb: if you are still extending a prototype after 6 months of AI-assisted refactors, you have probably entered the trap. Either commit to a deliberate rebuild or accept the current shape as the architecture.

## Tradeoffs / When to use
- **The gain (avoiding the trap):** cleaner long-term architecture, fewer surprise rewrites, lower [[AI-Attributed Defect Tracking|defect rates]] in foundational code.
- **The cost (avoiding the trap):** upfront design work feels expensive when AI implementation is cheap; discipline is unrewarded in short-term velocity metrics.
- **Watch for:** repeated "while we're in here" refactors; growing module count without growing clarity; AI-suggested abstractions that no human can summarize.
- **Healthy pattern:** treat first build as disposable; commit to a rebuild boundary rather than infinite refactor.

## Key tools / implementations
- [[Claude Code]] — the kind of capable agent that makes refactoring feel free, hence the trap.

## Sources
- [[raw/simon-willison-eight-years-building-with-ai]] — cheap refactoring paradox, implementation vs design, verifiability heuristic, phase-appropriate AI usage, 8-year-to-3-month pattern.

## Backlinks
- [[Claude Code]]
- [[Code Comprehension Bottleneck]]
- [[Guardrails for AI Coding]]
- [[Verifiability Boundary]]
