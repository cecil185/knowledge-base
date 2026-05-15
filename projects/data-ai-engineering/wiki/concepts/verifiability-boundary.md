---
title: Verifiability Boundary
updated: 2026-05-15
sources: [raw/simon-willison-eight-years-building-with-ai.md, raw/simon-willison-scaling-autonomous-coding.md, raw/simon-willison-agentic-engineering-lennys-podcast.md, raw/redhat-harness-engineering-structured-workflows.md]
related: [refactoring-trap, agentic-coding, verification-bottleneck, guardrails-for-ai-coding, ai-attributed-defect-tracking, harness-engineering, intent-based-testing]
---
## Summary
AI is a force multiplier wherever output can be checked objectively and a source of false confidence wherever it cannot. The verifiability boundary is the line between work where tests, types, benchmarks, or reference implementations can prove correctness — and work where judgment is the only check.

## Details

### The defining heuristic
Willison's question: *"Can you verify the output objectively?"*
- **Yes** → AI is safe to deploy aggressively. Tests pass / fail. Code compiles / doesn't. Benchmark improves / regresses. Reference output matches / doesn't.
- **No** → AI looks confident but provides no signal you can trust. Design choices, prose quality, security claims, "is this idiomatic?", "is this the right abstraction?".

The boundary is the most important mental model for using AI safely. It tells you when to ship and when to slow down.

### What sits on the verifiable side
- Code that has unit/integration/E2E tests with clear pass criteria.
- Type-checked code in strongly-typed languages.
- Performance work with benchmarks (Woolf's 8-prompt sequence works because every step is benchmark-verifiable — see [[Iterative Chunking]]).
- Output compared against a reference implementation with a metric (MAE, accuracy, etc.).
- Schema-conforming structured data.

### What sits on the unverifiable side
- Architecture and abstraction choices (the heart of the [[Refactoring Trap]]).
- Documentation quality — AI-generated docs read fluently but may state things that aren't true.
- AI-generated tests for AI-generated code — both can encode the same wrong assumption.
- Security findings — Willison highlights hallucinated CVE reports as a systemic problem; the report looks polished, the vulnerability doesn't exist.
- Subjective code quality, "is this idiomatic?".

### The hallucinated security report problem
A specific high-stakes failure mode: AI agents produce confident-looking vulnerability reports against open-source projects. Maintainers spend hours investigating; the issue is fabricated. The pattern generalizes: **verify the AI's claim before acting on it**, not after. For security findings specifically, require a reproducible exploit before opening an issue.

### False professionalism
AI-generated tests and docs look professional regardless of whether they reflect the system. A test suite with 90% coverage that all passes can still test nothing meaningful if both the implementation and the tests were generated from the same prompt. CodeScene's insistence on [[Guardrails for AI Coding|human-written tests for AI code]] is a direct response: tests must come from a different cognitive source than the implementation, or you're checking the AI against itself.

### Trust requires months of personal use
Willison's broader point: trust in an AI workflow can't be granted from a demo. It accrues from months of personally using the tool, seeing its failures, calibrating where it's reliable. Until then, treat every output as a hypothesis that needs verification.

### Connection to harness engineering
Red Hat's [[Harness Engineering]] framing is the structural answer: build the verifiability into the harness so every AI output lands in a structured environment where pass/fail is automatic. "Structure in, structure out" is the boundary made operational.

## Tradeoffs / When to use
- **Use the boundary as a routing decision:** verifiable work → push hard with AI; unverifiable work → slow down, demand human judgment, or build verification infrastructure first (tests, benchmarks, reference implementations).
- **Gain:** clear-eyed deployment of AI; avoids the worst failure modes (silent design rot, hallucinated security claims, fake test coverage).
- **Cost:** building verification infrastructure is itself expensive; some valuable work is genuinely unverifiable.
- **Poor fit when ignored:** any consumer-facing security claim, any architectural decision, any documentation released as authoritative.

## Key tools / implementations
- [[Claude Code]] / [[OpenAI Codex]] — capable enough that the boundary becomes the operative safety question.
- [[Shiplight]] — pushes more work onto the verifiable side by generating intent-based E2E tests.
- [[CodeScene]] — enforces human-written tests for AI code, the practical defense against AI-checking-AI.

## Sources
- [[raw/simon-willison-eight-years-building-with-ai]] — the verifiability heuristic and phase-appropriate usage.
- [[raw/simon-willison-scaling-autonomous-coding]] — judge agents and well-defined verifiable problems as the suitable domain for autonomous coding.
- [[raw/simon-willison-agentic-engineering-lennys-podcast]] — hallucinated security reports, AI-generated docs/tests credibility, trust requires personal use.
- [[raw/redhat-harness-engineering-structured-workflows]] — structure in, structure out as the operational form of verifiability.

## Backlinks
- [[Iterative Chunking]]
- [[Refactoring Trap]]
