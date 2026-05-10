---
name: wiki:ingest
description: Save a fetched article or topic research to the active project's raw/ as structured markdown; deduplicates against raw/INDEX.md
model: claude-opus-4-6
effort: medium
---
# wiki:ingest

Save article content into `raw/` as structured markdown. Called by `read-article` after fetching, and directly with a URL or topic.

## Active project

Determine the active project by reading `CLAUDE.md` from the repo root. Find the **Default project** slug in the `## Projects` section. Set `PROJECT_DIR = projects/<slug>`. All file paths below are relative to `/Users/cecil/Code/me/knowledge-base/<PROJECT_DIR>`.

If called with a project argument (e.g. `/wiki:ingest <url> --project applied-ai`), use that slug instead.

## Input

One of:
- A **URL** — fetch and ingest a single article.
- A **topic string** — research the topic across multiple sources and ingest each.

## Step 1: Resolve sources

**If given a URL:**

Use WebFetch to retrieve the full page content. Extract the main article body — strip navigation, sidebars, footers, cookie banners, subscription prompts, and ads. Preserve all code blocks and tables verbatim.

If the fetch fails or returns thin content (paywall, login wall, empty body): stop and report "fetch failed: <reason>". Do not create a file.

**If given a topic:**

Run 3–5 WebSearch queries covering different angles of the topic (e.g. introductory overview, practical implementation, tradeoffs, recent developments). From the combined results, select 5–10 sources with the highest signal — prefer primary sources, official docs, engineering blog posts, and papers over aggregators or SEO content. Fetch each selected URL with WebFetch using the same extraction rules above. Collect all successfully fetched sources as a list; skip any that fail.

## Step 2: Deduplicate

Read `<PROJECT_DIR>/raw/INDEX.md`. If the file does not exist, treat the existing index as empty.

For each fetched source URL, normalise before comparing:
- Strip trailing slashes
- Strip `utm_*` query parameters
- Treat `http://` and `https://` as identical

If a normalised URL is already present in the index, skip that source and note "skipped — duplicate: <existing path>". Continue processing remaining sources.

## Step 3: Generate slug and check length

Generate a slug from the article title:
- Lowercase
- Replace spaces and non-alphanumeric characters with hyphens
- Collapse consecutive hyphens to one
- Strip leading/trailing hyphens
- Truncate to 60 characters at a word boundary

If the extracted body exceeds 4000 words, split into numbered parts: `<slug>-part-1.md`, `<slug>-part-2.md`, etc. Each part gets its own frontmatter with a `part` field.

## Step 4: Determine type and tags

Classify the source type as one of: `article`, `paper`, `repo`, `docs`.

- `paper` — academic papers, arXiv, research publications
- `repo` — GitHub or similar source code repositories
- `docs` — official documentation sites
- `article` — everything else

Leave `tags` as an empty list `[]`. Tags are populated by later skills.

## Step 5: Check for a Linear ticket

Search the active Linear project (determined from CLAUDE.md) for an open ticket whose description contains the source URL. If found, record the ticket ID (e.g. `CC-42`). If not found, use `"none"`.

## Step 6: Write file(s)

Write to `<PROJECT_DIR>/raw/<slug>.md` (or `<slug>-part-N.md` for splits).

Frontmatter followed immediately by the extracted article body:

```
---
title: <article title>
url: <source URL>
fetched: <YYYY-MM-DD>
linear_ticket: <ticket ID or "none">
type: <article|paper|repo|docs>
tags: []
---

<extracted article body>
```

For split files, add `part: N` and `total_parts: N` fields to the frontmatter.

## Step 7: Update raw/INDEX.md

Append one line per saved file to `<PROJECT_DIR>/raw/INDEX.md`. Create the file with a `# Raw Article Index` header if it does not exist.

Format:

```
- [<title>](<slug>.md) — <one-sentence summary of what the article covers> (<source domain>)
```

For split files, list only the first part with a note: `(split: N parts)`.

## Output

For each source processed, report one of:
- `saved: <PROJECT_DIR>/raw/<slug>.md` — file written successfully
- `skipped — duplicate: <PROJECT_DIR>/raw/<existing-slug>.md` — URL already in index
- `fetch failed: <reason>` — could not retrieve content

If given a topic, also summarise: N sources fetched, N saved, N skipped, N failed.
