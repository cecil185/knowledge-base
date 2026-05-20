---
name: read-article
description: >
  Fetches a full article, produces a structured extraction saved to raw/ and a goal-aware
  AI summary posted as a Linear comment — in a single pass. Called after ticket creation
  by bulk-ingest-articles, and directly on demand.
when_to_use: >
  Trigger when the user says "read this article", "summarize ticket CC-42", "process this
  URL", "read https://...", or when bulk-ingest-articles spawns agents after ticket creation.
argument-hint: "<ticket-id | url>"
disable-model-invocation: true
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

### Blocked-fetch handling

If the fetch fails, returns a paywall/login wall, returns a Cloudflare/anti-bot block, returns truncated or thin content, or otherwise does not yield the full article body:

**Do not** attempt to reconstruct the article from web search snippets, cached previews, the article's title and URL, or any other secondary source. A partial or reconstructed read is worse than no read — it gets recorded as if it were a real summary and contaminates the wiki.

Instead:

1. Add the `BLOCKED` label to the Linear ticket (create the label if it doesn't exist). Leave any existing labels in place.
2. Post a comment on the Linear ticket:
   ```
   ## AI Read — Blocked

   Could not access article in full: <reason — paywalled / Cloudflare block / fetch error / empty response>.
   No summary written. raw/ and articles/ not updated.
   ```
3. Stop. Do not proceed to Steps 2–5. Do not write any raw/ file. Do not write any articles/ stub. Do not call ingest_chunks.

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


### 5c: Call ingest_chunks.py

After writing the articles file successfully, call:

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
- Path to `articles/<article-slug>.md` written, or "blocked" if Step 1b exited early
- Number of chunks ingested into `chunks.sqlite`, or "skipped" if blocked/already processed
