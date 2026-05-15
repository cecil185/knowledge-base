# Eight Years of Wanting, Three Months of Building with AI (Simon Willison / Lalit Maganti)

**Source:** https://simonwillison.net/2026/Apr/5/building-with-ai/
**Read:** 2026-05-10

## Overview

Simon Willison link post highlighting Lalit Maganti's article about building [syntaqlite](https://github.com/lalitMaganti/syntaqlite) — a high-fidelity set of development tools for SQLite (parser, formatter, verifier) designed for use in language servers. Maganti spent **eight years** contemplating the project before completing it in **three months** with AI assistance.

Original article: https://lalitm.com/post/building-syntaqlite-ai/

---

## The Case Study: syntaqlite

Syntaqlite provides fast, robust, and comprehensive linting and verification tools for SQLite queries. It includes a parser, formatter, and verifier intended for use in language servers and developer tooling.

### Timeline

- **8 years** — conceptualization, doubts, inability to start
- **3 months** — active building with AI assistance (Claude Code)

---

## How AI Helped: The Initial Breakthrough

AI overcame the classic cold-start problem. Maganti could never get started because of doubts about technical decisions and uncertainty about building the right thing. AI removed that friction:

> "AI basically let me put aside all my doubts on technical calls, my uncertainty of building the right thing and my reluctance to get started"

> "I work so much better with concrete prototypes to play with and code to look at than endlessly thinking about designs abstractly."

The first AI-assisted prototype was built quickly, proved the concept — and was eventually discarded.

---

## The Refactoring Trap: Where AI Hurt

A critical insight emerged during the project: AI's strength in implementation became a **weakness for architectural decisions**.

> "I found that AI made me procrastinate on key design decisions. Because refactoring was cheap, I could always say 'I'll deal with this later.'"

Because AI could cheaply refactor anything at any time, Maganti deferred hard design decisions. This degraded code coherence over time. The paradox: low cost of change → less urgency to get it right → accumulating architectural debt.

### The Second Attempt

Maganti eventually rebuilt the project from scratch. The rebuild involved significantly more human decision-making, took longer, but produced a more robust and sustainable codebase.

---

## Key Lessons

### 1. Implementation vs. Design — A Fundamental Distinction

Implementation tasks have **objectively verifiable outcomes**: code compiles, tests pass. Design decisions lack this clarity — there's no immediate signal that you got it wrong.

AI is excellent at implementation (where it can be checked against passing tests). AI is unreliable — or actively harmful — for design decisions where the problem itself is unclear.

> "When I was working on something where I didn't even know what I wanted, AI was somewhere between unhelpful and harmful."

### 2. AI Enables Momentum, Not Judgment

AI's greatest productivity value was eliminating the activation energy to start. For someone who works better with concrete things to react to (vs. abstract planning), AI-generated prototypes provided the concrete artifact needed to make progress.

### 3. The Cheap Refactoring Paradox

When refactoring is cheap (because AI does it), the discipline to make good architectural decisions upfront erodes. This is a subtle trap: the very capability that makes AI valuable (fast iteration) can produce worse outcomes if it reduces the human's engagement with hard decisions.

### 4. Human Judgment Required for Ambiguous Problems

The most productive workflow: use AI for concrete, verifiable implementation tasks; maintain rigorous human oversight and decision-making for architectural design. Don't outsource decisions you can't verify.

---

## Productivity Multiplier Summary

| Phase | What AI Accelerated | Risk |
|---|---|---|
| Getting started | Eliminated 8 years of paralysis in weeks | None — prototype was disposable |
| Implementation | Fast code generation for well-defined tasks | Low — tests verify correctness |
| Refactoring | Cheap iteration | High — deferred design decisions accumulate |
| Architecture | Not recommended | AI guidance counterproductive without clear problem definition |

---

## Simon Willison's Framing

Willison highlights this as a case study in understanding AI's boundaries. The key signal: **can you verify the output objectively?** If yes (tests pass, code compiles), AI is a genuine force multiplier. If no (is this the right architecture?), AI provides false confidence and discourages the human thinking that's actually required.
