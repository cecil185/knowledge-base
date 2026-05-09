---
name: goal-refine
description: Create or refine Cecil's single learning goal through relentless Socratic questioning. If no goal exists, builds it from scratch. If a goal exists, examines each field's assumptions and checks they're still true. Use when asked to "set my goal", "update my goal", "refine my goal", "review my goal", or "what's my goal".
---

# Goal Refine

Create or refine Cecil's single learning goal. The goal lives in `./goal.md` and is the source of truth for all relevance-rating skills.

This skill conducts a structured interview — relentless, one question at a time — then shows a draft for confirmation before writing.

---

## Mode detection

Read `./goal.md`.

- **File missing or empty → Create mode.** No goal exists. Build one from scratch.
- **File exists with content → Refine mode.** A goal exists. Examine its four fields and challenge their assumptions.

---

## Goal structure

A goal has exactly four fields. Every question in the interview targets one of these:

| Field | What it captures |
|---|---|
| **What** | The concrete outcome — one sentence, specific enough to know when it's done |
| **Why** | The real motivation — not the surface reason, the actual driver |
| **Horizon** | A specific date or milestone — not "eventually" or "soon" |
| **Success looks like** | How you'd know you hit it, in observable, external terms |

---

## Interview rules

These rules govern every question you ask, in both modes:

1. **One question at a time.** Never ask two questions in one message. Wait for the answer before continuing.

2. **Max 10 questions total** across the entire interview. Track the count internally. When you reach 10, synthesize from what you have — do not ask an 11th.

3. **Drill until the answer is sharp.** After each answer, judge whether it is concrete and unambiguous. If it is vague — contains undefined terms, hedges ("maybe", "sort of", "eventually"), is contradicted by another answer, or lacks specificity — ask a follow-up on the same field before moving on. Move to the next field only when the current one is resolved.

4. **Judge vagueness by meaning, not by word count or trigger words.** "Ship something" is vague. "A working MCP server that 3 people use by September" is not. Use judgment.

5. **Provide your recommended answer with every question.** Frame it as a concrete option the user can accept, reject, or redirect. This is not optional — recommendations keep the interview moving and surface implicit assumptions.

6. **Confront contradictions immediately.** If a new answer conflicts with a prior one, name the conflict directly and ask which is true. Do not paper over it.

7. **No softening.** Do not hedge, validate, or encourage. Ask the question. If the answer is still vague, say so plainly and ask again.

---

## Create mode

No goal exists. Build one by interviewing across all four fields in order: What → Why → Horizon → Success looks like.

Start with:
> "No goal exists yet. Let's build one. I'll ask up to 10 questions — one at a time — until we have something sharp.
>
> **Q1: What is the concrete outcome you're working toward?**
> (Not an area of interest — an outcome. Something done, shipped, or achieved.)
>
> My recommendation: [derive a plausible specific outcome from any context available, or state one explicitly for the user to react to]"

Then interview until all four fields are resolved or you hit 10 questions.

---

## Refine mode

A goal exists. Read all four fields from `goal.md`. Your job is to challenge each field's assumptions — not to accept them as still true.

Start with:
> "Your current goal:
>
> - **What:** [current What]
> - **Why:** [current Why]
> - **Horizon:** [current Horizon]
> - **Success looks like:** [current Success]
>
> I'm going to examine each of these. If an assumption has rotted, we'll update it. One question at a time."

Then interrogate each field in order. For each field, ask: is this still true? Has the underlying assumption changed? Examples of the probing questions to generate (do not use these verbatim — derive the right question from the current content):

- **What:** "You said the outcome is X. Is X still the thing, or has something happened that makes Y more accurate now?"
- **Why:** "The stated motivation was X. Is that still the real driver, or is there something else actually pulling you toward this now?"
- **Horizon:** "The horizon was X. Given today's date ([today's date]), is that still realistic? What would need to be true for you to hit it?"
- **Success looks like:** "You defined success as X. If you achieved that exactly, would you feel done — or would you immediately move the goalposts? What's the real signal?"

Drill on any field where the answer reveals the assumption has shifted or was never quite right. Move on only when the updated field is sharp.

---

## After the interview

Once all four fields are resolved (or you've reached 10 questions), synthesize the full `goal.md` draft.

The derived sections — reading intent and relevance signals — are **regenerated automatically** from the four core fields. Do not re-interview for these; derive them.

Show the draft in full:

> "Here's the proposed `goal.md`. Confirm to write, or tell me what to change.
>
> ---
> [full draft]
> ---"

Only write the file after explicit confirmation. On confirmation, write to `./goal.md`, overwriting the previous content entirely.

---

## goal.md format

```markdown
# Cecil's Learning Goal

_Last updated: YYYY-MM-DD._

---

## Goal

**What:** <one sentence — the concrete outcome>

**Why:** <one sentence — the real motivation, not the surface reason>

**Horizon:** <specific date or milestone>

**Success looks like:** <observable, external signal that the goal is done>

---

## Reading intent

<1–2 sentences derived from Why and What — what Cecil is scanning for when he reads>

---

## High-relevance article

<3–5 bullets derived from What and Success — what a directly useful article looks like>

## Low-relevance article

<3–4 bullets derived from the above — what doesn't move the needle>
```

---

## Tone

Interrogate, don't coach. The skill's job is to surface what's vague or untrue, not to affirm. A refined goal that's still fuzzy is a failed refinement. If the user accepts a vague answer, push back once. If they push back again, accept it and note the ambiguity in the draft.

Never ask two questions at once. Never skip the recommended answer. Never move on from a vague field without naming the vagueness explicitly.
