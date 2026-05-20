---
name: wiki:ingest
description: >
  Fetches and saves a URL or researches a topic, writing structured markdown extractions
  to the active project's raw/ directory. Deduplicates against raw/INDEX.md and Linear.
  Use when the user says "ingest this URL", "save this article", "add this to the wiki",
  or "research <topic> for the wiki".
when_to_use: >
  Trigger when user says "ingest this URL", "save this article", "add this to the wiki",
  "research <topic> for the wiki", "wiki:ingest <url>", or provides a URL and asks to
  save it to the knowledge base.
argument-hint: "<url-or-topic> [--project <slug>]"
model: claude-opus-4-6
effort: medium
disable-model-invocation: true
---
# wiki:ingest

Save article content into `raw/` as structured markdown. Called by `read-article` after fetching, and directly with a URL or topic.

## Active project

Determine the active project by reading `CLAUDE.md` from the repo root. Find the **Default project** slug in the `## Projects` section. Set `PROJECT_DIR = projects/<slug>` and `LINEAR_PROJECT` from the Projects table. All file paths below are relative to `/Users/cecil/Code/me/knowledge-base/<PROJECT_DIR>`.

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

For each fetched source URL, run the `check-duplicate` skill with the URL, `LINEAR_PROJECT`, and `PROJECT_DIR`.

If `linear_ticket` is not null, skip that source and note "skipped — duplicate: <ticket ID>". Continue processing remaining sources.

## Step 3: Determine type

Classify the source type as one of: `article`, `paper`, `repo`, `docs`.

- `paper` — academic papers, arXiv, research publications
- `repo` — GitHub or similar source code repositories
- `docs` — official documentation sites
- `article` — everything else

## Step 4: Check for a Linear ticket

Use the `check-duplicate` result from step 2. If `linear_ticket` is not null, use that ticket ID. Otherwise use `"none"`.

## Step 5: Save file(s)

Run the `save-article-raw` skill for each source with:
- `title` — article title
- `url` — source URL
- `body` — extracted article body
- `project_dir` — `PROJECT_DIR`
- `linear_ticket` — ticket ID or `"none"`
- `fetched` — today's date
- `type` — from step 3
- `tags` — `[]`

## Output

For each source processed, report one of:
- `saved: <PROJECT_DIR>/raw/<slug>.md` — file written successfully
- `skipped — duplicate: <PROJECT_DIR>/raw/<existing-slug>.md` — URL already in index
- `fetch failed: <reason>` — could not retrieve content

If given a topic, also summarise: N sources fetched, N saved, N skipped, N failed.
