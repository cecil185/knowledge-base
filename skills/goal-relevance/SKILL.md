---
name: goal-relevance
description: Rate how relevant an article is to Cecil's personal learning goals — side projects, AI/LLM internals, and staying aware of the industry. Distinct from article-critique (which rates work applicability). Use when asked "is this relevant to my goals?", "does this match what I'm trying to learn?", "should I read this for personal growth?", or any framing about personal goals vs. job stack.
---

# Goal Relevance Check

Rate an article against Cecil's current personal learning goals. This is **not** about work stack applicability — that's `article-critique`. This is about personal growth, side projects, and horizon-scanning.

Always read goals from `./goal.md` before rating. The file is the source of truth; it may be updated between sessions.

---

## Process

1. **Read `./goal.md`** to load current goals. If the file is missing, stop and tell the user.

2. **Get the article.**
   - URL: `WebFetch`. Pasted text: use as-is. Paywall/login wall: report failure, do not fabricate.

3. **Identify the load-bearing claim.** One sentence: what does this article actually argue or show?

4. **Score each goal axis** (see rubric below).

5. **Emit the report** in the exact output format below. No follow-up questions.

6. **Append to learning log** at `~/.claude/learning/log.md` (see Log Entry section).

---

## Rating rubric

Score each axis 0–3. Sum → overall rating (max 12).

| Axis | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **AI/agent relevance** (LLMs, agents, MCP, tooling) | No AI angle | Mentions AI tangentially | Covers an AI tool, pattern, or technique concretely | Deep, non-obvious — changes how you'd build or prompt |
| **Side-project fuel** (could accelerate shipping something) | No application to building products | Vaguely inspirational | Concrete technique or tool you could use in a side project | Directly enables or unblocks a project |
| **LLM internals** (how models work, evals, fine-tuning, prompting depth) | No internals content | Surface-level mention | Explains a mechanism or tradeoff worth knowing | Genuinely illuminates how models work or fail |
| **Industry signal** (early-enough, non-obvious awareness) | Already common knowledge / hype | Slightly ahead of mainstream | Real signal — trend or tool before it's everywhere | Early mover advantage — knowing this now matters |

**Overall rating** (sum, max 12):
- **10–12 → High relevance. Worth real attention.**
- **7–9 → Moderate. Skim and extract.**
- **4–6 → Low. File it or skip.**
- **0–3 → Drop. Doesn't move any goal.**

Show per-axis scores so the rating is auditable.

---

## Output format

```
# <article title or short label>
<URL if available>

**Goal Relevance: <N>/12 — <High | Moderate | Low | Drop>**
- AI/agent relevance: <0–3> — <one-clause why>
- Side-project fuel: <0–3> — <one-clause why>
- LLM internals: <0–3> — <one-clause why>
- Industry signal: <0–3> — <one-clause why>

**Thesis (1 sentence):** <load-bearing claim>

**What's useful for your goals:**
- <bullet — concrete, specific, not padded>
- <bullet>
- <"nothing" if genuinely empty>

**If you act on this:**
- Could use for: <side project angle, or "n/a">
- Would change how I: <prompt/build/think, or "nothing">
- Worth watching because: <signal rationale, or "n/a">

**Verdict (1 sentence):** <read, skim, drop — and the single thing to take away, if any>
```

No extra headers. No closing offer. The report is the deliverable.

---

## Log Entry

Append one line to `~/.claude/learning/log.md`. Create the file and header if missing.

File header (only if creating):
```
# Learning Log

| Date | Title | URL | Rating | Action | Status |
|------|-------|-----|--------|--------|--------|
```

Row format (use `/12g` suffix to distinguish from work-stack ratings):
```
| YYYY-MM-DD | <title, max 60 chars> | <url or "pasted"> | <N>/12g | <one-clause verdict, or "none"> | pending |
```

- `/12g` = goal rating (vs `/12` = work-stack rating from article-critique)
- Append only, never rewrite existing rows.

---

## Tone

Direct. Don't inflate ratings to be encouraging — a "drop" is valuable signal. If the article is pure hype with no concrete technique, say so bluntly. If it's genuinely useful for a side project, be specific about how. The goal is calibrated filtering, not cheerleading.

---

## Edge cases

- **Goals file missing:** Stop. Output: `Goals file not found at ./goal.md — run goal setup first.` Do not rate.
- **Paywall/fetch fails:** Emit stub with `Rating: n/a — fetch failed`. Append to log with rating `n/a`.
- **Article is pure work/stack (no personal-goal angle):** Score honestly — likely 0–3. That's the right answer; don't pad.
- **Caller is article-critique or tech-digest:** Same output format. Field names are stable for parsing.
