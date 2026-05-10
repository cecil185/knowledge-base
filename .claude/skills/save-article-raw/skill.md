---
name: save-article-raw
description: Write a fetched article body to raw/<slug>.md with frontmatter and append a line to raw/INDEX.md; handles long articles by splitting into parts
model: claude-opus-4-6
effort: low
---
# save-article-raw

Persistence primitive. Writes a fetched article to `raw/` and registers it in `INDEX.md`. Called by `read-article`, `wiki-ingest`, and `add-article` after fetching content.

## Input

- `title` — article title (plain text)
- `url` — canonical source URL
- `body` — extracted article body (markdown, all noise stripped)
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

## Step 2: Handle long articles

If the extracted body exceeds 4000 words, split into numbered parts:
`<slug>-part-1.md`, `<slug>-part-2.md`, etc.

Each part gets its own frontmatter with additional fields `part: N` and `total_parts: N`.

For single-part articles, use `<slug>.md` with no part fields.

## Step 3: Write file(s)

Write to `<project_dir>/raw/<slug>.md` (or `<slug>-part-N.md` for splits).

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

## Output

Report one of:
- `saved: <project_dir>/raw/<slug>.md` — file written
- `saved: <project_dir>/raw/<slug>-part-1.md … part-N.md` — split write
- `error: <reason>` — write failed
