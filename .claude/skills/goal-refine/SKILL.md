---
name: goal-refine
description: >
  Creates or refines the active project's single learning goal through Socratic questioning.
  Writes the result to goal.md. The goal.md output drives all article filtering and scoring
  in the system.
when_to_use: >
  Trigger when the user says "set my goal", "update my goal", "refine my goal", "what's my
  goal", "create goal.md", or starts the knowledge-base system for the first time without
  an existing goal.
argument-hint: "[project-slug]"
disable-model-invocation: true
model: claude-opus-4-6
effort: medium
---
# Goal Refine

Create or sharpen the single learning goal that drives all filtering in this system. The goal lives in the active project's `goal.md` and is the source of truth for every skill that scores or filters articles.

## Active project

Determine the active project by reading `CLAUDE.md` from the repo root. Find the **Default project** slug in the `## Projects` section. Set `PROJECT_DIR = projects/<slug>`.

If the user passes a project argument (e.g. `/goal-refine applied-ai`), use that slug instead. Announce which project's goal you are refining.

## Steps

### 1. Read <PROJECT_DIR>/goal.md

Read `<PROJECT_DIR>/goal.md`.

- **File missing or empty** → Create mode: build a goal from scratch using the interview below.
- **File exists with content** → Refine mode: treat the existing 4 fields as first drafts; challenge each one's assumptions using the same interview below.

### 2. Interview

Conduct a Socratic interview to produce four sharp fields:

| Field | What it captures |
|-------|-----------------|
| **What** | Concrete outcome — not a topic, a deliverable or capability |
| **Why** | Real motivation — the actual driver, not the surface reason |
| **Horizon** | Specific date or named milestone — not "soon" or "eventually" |
| **Success looks like** | Observable, external signal — something Cecil could point to |

**Interview rules — follow these exactly:**

1. Ask one question at a time. Never bundle two questions.
2. Maximum 10 questions total. At question 10, synthesize from what you have, even if fields are imperfect.
3. Every question must include a recommended concrete answer in the form "e.g. — [specific example]". This is mandatory, not optional.
4. Drill on vague answers. If the response contains hedges ("maybe", "eventually", "kind of"), undefined terms, or scope creep, do not move on. Ask again with a sharper framing.
5. Confront contradictions immediately. If the stated Why conflicts with the What, say so directly and ask which one to keep.
6. No softening, no validation, no encouragement. Silence means forward motion; if you're done ask the next question.

**Field order:** What → Why → Horizon → Success looks like. You may revisit an earlier field if a later answer reveals it was imprecise — but count the revisit toward the 10-question limit.

### 3. Derive supporting sections

After the interview is complete, derive the following sections automatically from the 4 fields. Do not re-interview or ask for input on these — derive them from what was said.

**Reading intent** (1–2 sentences): What Cecil is scanning for when he opens an article. Written in first person. Grounded in the What and Why.

**High-relevance article** (4–6 bullets): What a directly useful article looks like. Each bullet is specific enough to apply as a filter. Avoid "could be" and "might" — these are yes/no signals.

**Low-relevance article** (3–4 bullets): What doesn't move the needle toward this goal. Be specific — name the patterns that waste time, not just the inverse of the high-relevance list.

### 4. Show draft and confirm

Display the full proposed `goal.md` in a code block. Ask one question: "Write this to `<PROJECT_DIR>/goal.md`? (yes / revise [what])"

- If yes: write the file.
- If revise: incorporate the revision and show the updated draft. Confirm once more before writing.

Do not write the file without explicit confirmation.

### 5. Write <PROJECT_DIR>/goal.md

Write using exactly this format:

```markdown
# Cecil's Learning Goal

_Last updated: YYYY-MM-DD._

---

## Goal

**What:** <one sentence>
**Why:** <one sentence — real driver, not surface reason>
**Horizon:** <specific date or milestone>
**Success looks like:** <observable, external signal>

---

## Reading intent

<1-2 sentences>

---

## High-relevance article

- <bullet>
- <bullet>
- <bullet>
- <bullet>

## Low-relevance article

- <bullet>
- <bullet>
- <bullet>
```

Use today's date for `Last updated`. Do not add sections beyond what the format specifies.

## Tone

Interrogate, don't coach. A goal that's still fuzzy after 10 questions is a failed refinement — synthesize the sharpest version possible from what was said and name the remaining ambiguity in a one-line note at the bottom of the draft.
