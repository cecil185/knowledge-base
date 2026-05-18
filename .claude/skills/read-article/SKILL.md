---
name: read-article
description: Fetch an article, produce a structured extraction for raw/ and a goal-aware AI summary for Linear — in a single pass. Updates ticket labels.
model: claude-opus-4-6
effort: medium
---
# read-article

Reads an article in full, then in a single LLM pass produces both a structured extraction (saved to `raw/`) and a goal-aware summary comment (posted to Linear). Updates ticket labels. Called for each ticket after `bulk-ingest-articles`, and also callable on-demand.

## Active project

Use the `PROJECT_DIR` established by the calling skill (digest). If called directly, determine the active project by reading `CLAUDE.md` and using the **Default project** slug. Set `PROJECT_DIR = projects/<slug>` (relative to repo root `/Users/cecil/Code/me/knowledge-base`).

## Input

Either a Linear ticket ID (e.g. `CC-42`) or an article URL.

- If a **ticket ID** is given: read the ticket description to extract the URL.
- If a **URL** is given: search the active Linear project for a ticket whose description contains that URL. If no ticket is found, stop and report the error — do not proceed without a ticket.

## Step 1: Check for existing raw file

Before fetching, scan `PROJECT_DIR/raw/` for any `.md` file whose `url:` frontmatter field matches the ticket URL (exact match, case-insensitive).

- If a match is found: use that file's body as the extraction. Skip to Step 3 (post Linear comment). Do **not** run `save-article-raw` in Step 4 (file already exists).
- If no match is found: proceed to fetch below.

## Step 1b: Fetch article and goal — in parallel

Run both of these simultaneously:

1. Use WebFetch to retrieve the full article content.
2. Read `<PROJECT_DIR>/goal.md`.

If the fetch fails or the content appears to be a paywall or login wall (thin content, subscription prompt, no article body):

1. Post a comment on the Linear ticket:
   ```
   ## AI Read — Fetch Failed

   Fetch failed: <reason — paywalled / fetch error / empty response>.
   Labels and raw/ not updated.
   ```
2. Run Step 5 (write `unfetched: true` stub only — see below).
3. Stop. Leave all labels unchanged. Do not proceed to Steps 2–4.

## Step 2: Single-pass extraction and summary

With the full article text and `goal.md` both in context, produce **two outputs in one pass**:

---

### Output A — Structured extraction (for raw file)

Goal-agnostic. Faithful to what the article actually says. Target: 400–800 words.

```
## Key claims
2–4 bullet points. The article's central arguments or findings.

## Concepts
Named ideas, patterns, or principles the article explains. One line each.

## Tools & frameworks
Named software, libraries, services, or systems discussed. One line each.

## Patterns & techniques
Concrete techniques, configurations, or architectures described. Enough detail to act on.

## Tradeoffs
What approaches gain, what they cost, and when they fit or don't.

## Notable quotes / stats
Direct quotes or specific numbers worth preserving verbatim.
```

### Output B — Goal-aware summary (for Linear comment)

Grounded in `goal.md`'s Reading intent and High-relevance signals fields.

```
## AI Summary

**TLDR**
2-3 sentences. What the article actually argues, stripped of padding.

**How it relates to your goal**
1-2 sentences. Direct connection to goal.md — or "not directly relevant" if the connection is thin.

**How to apply it**
Max. 3 bullets - Concrete techniques, configurations, or architectures that can be applied.
```

---

## Step 3: Post summary comment and update labels — in parallel

Run both simultaneously:

1. Post Output B as a comment on the Linear ticket.
2. Leave all labels unchanged (no label updates needed)

## Step 4: Save raw extraction

Skip this step if the article body was loaded from an existing raw file in Step 1.

Run the `save-article-raw` skill with:
- `title` — article title (extracted from page)
- `url` — article URL
- `body` — Output A (structured extraction)
- `project_dir` — `PROJECT_DIR`
- `linear_ticket` — ticket ID
- `fetched` — today's date
- `type` — classify as `article`, `paper`, `repo`, or `docs`
- `tags` — `[]`

## Step 5: Store full article text and chunks

Skip this step entirely if the article body was loaded from an existing raw file in Step 1 (already processed — `articles/` file and chunks already exist).

### 5a: Determine the article slug

Use the same slug derivation as `raw/`: lowercase the title, replace spaces and special characters with hyphens, truncate to 60 characters. This must match the slug used in Step 4 for `save-article-raw`.

### 5b: Write the full article file

**Normal path** (fetch succeeded):

Write `<PROJECT_DIR>/articles/<article-slug>.md` with this structure:

```
---
url: <article URL>
fetched: <YYYY-MM-DD today>
title: <article title>
unfetched: false
---

<full article text>
```

- Create `<PROJECT_DIR>/articles/` directory if absent.
- `<full article text>` is the raw text retrieved by WebFetch in Step 1b — not the structured extraction (Output A), but the original article body.

**Paywall / fetch failure path** (Step 1b detected no usable content):
- Write `<PROJECT_DIR>/articles/<article-slug>.md` stub with `unfetched: true` and empty body:
  ```
  ---
  url: <article URL>
  fetched: <YYYY-MM-DD today>
  title: <article title>
  unfetched: true
  ---
  ```
- Skip Step 5c — no rows to insert.

### 5c: Call ingest_chunks.py

After writing the articles file successfully (unfetched: false), call:

```
python3 /Users/cecil/Code/me/knowledge-base/scripts/ingest_chunks.py \
  --slug <article-slug> \
  --url <article-url> \
  --project-dir <PROJECT_DIR> \
  --file <PROJECT_DIR>/articles/<article-slug>.md
```

This creates or updates `<PROJECT_DIR>/chunks.sqlite` with paragraph-level chunks for the article.

## Output

Report:
- Ticket ID and Linear URL
- Whether the summary comment was posted successfully
- Path to the saved raw file, or reason for skipping/failure
- Path to `articles/<article-slug>.md` written (or stub written on paywall)
- Number of chunks ingested into `chunks.sqlite`, or "skipped" if paywall/already processed
