---
name: save-article-raw
description: >
  Persistence primitive that writes a structured article extraction to raw/<slug>.md with
  frontmatter and appends a registration line to raw/INDEX.md. Called by read-article,
  wiki-ingest, and add-article after generating extraction content. Not typically invoked
  directly by users.
when_to_use: >
  Called internally by wiki-ingest, read-article, and add-article after extraction is
  complete. Rarely triggered directly by users.
model: claude-opus-4-6
effort: low
disable-model-invocation: true
---
# save-article-raw

Persistence primitive. Writes a structured extraction to `raw/` and registers it in `INDEX.md`.
Called by `read-article`, `wiki-ingest`, and `add-article` after generating extraction content.

## Input

- `title` — article title (plain text)
- `url` — canonical source URL
- `body` — structured extraction (markdown, ~400–800 words, goal-agnostic)
- `project_dir` — active project directory (e.g. `projects/data-ai-engineering`)
- `linear_ticket` — Linear ticket ID (e.g. `CC-42`) or `"none"` if no ticket exists
- `fetched` — date fetched in `YYYY-MM-DD` format
- `type` — one of `article`, `paper`, `repo`, `docs`
- `tags` — list of label strings (pass `[]` if none; callers set this)

## Step 1: Generate slug

Derive a file slug from the title:
- Lowercase
- Replace spaces and non-alphanumeric characters with hyphens
- Collapse consecutive hyphens to one
- Strip leading/trailing hyphens
- Truncate to 60 characters at a word boundary

Example: "How Kafka Handles Backpressure" → `how-kafka-handles-backpressure`

## Step 2: Write file

Write to `<project_dir>/raw/<slug>.md`.

Frontmatter format:

```
---
title: <title>
url: <url>
fetched: <fetched>
linear_ticket: <linear_ticket>
type: <type>
tags: <tags>
---

<body>
```

## Step 3: Append to INDEX.md

Append one line to `<project_dir>/raw/INDEX.md` (create the file if it does not exist):

```
- [<title>](<slug>.md) — <url>
```

## Output

Report one of:
- `saved: <project_dir>/raw/<slug>.md` — file written
- `error: <reason>` — write failed
