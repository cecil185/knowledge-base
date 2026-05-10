---
name: add-article
description: Add a manually-found article URL to the active project — creates a Linear ticket, reads in full, and updates the wiki.
model: claude-opus-4-6
effort: medium
---
# add-article

Single-article entry point for manually-found articles.

## Arguments

- `<url>` — the article URL to add (required)
- `--project <slug>` — optional project override; defaults to the active project in CLAUDE.md

## Step 0: Resolve active project

Read `CLAUDE.md` from the repo root. Find the `## Projects` section and the **Default project** slug. If `--project <slug>` was passed, use that slug instead (validate it exists; stop with a list of valid slugs if not).

Set:
- `PROJECT_DIR = projects/<slug>`
- `LINEAR_PROJECT` = the Linear Project name from the matching Projects table row

Announce: `Adding article to project: <Name> (<slug>)`

## Step 1: Check for duplicates

Run the `check-duplicate` skill with the URL, `LINEAR_PROJECT`, and `PROJECT_DIR`.

If `linear_ticket` is not null: stop and report — "Already ticketed: <ticket ID> — <Linear URL>. Run `/read-article <ticket ID>` if it hasn't been read yet."

## Step 2: Create a Linear ticket

Fetch the page title and write a 1–2 sentence summary (WebFetch, extract title + first meaningful paragraphs only — no need for full content here).

Run the `create-ticket` skill with:
- `title` — article title
- `url` — the input URL
- `summary` — the 1–2 sentence summary
- `source` — the article's domain (e.g. `martinfowler.com`)
- `date` — today's date
- `LINEAR_PROJECT` — from step 0

Record the returned ticket ID (e.g. `CC-42`).

## Step 3: Read the article

Run the `read-article` skill with the ticket ID, URL, and `project_slug`. It fetches the full content, saves to `raw/`, posts the AI summary comment, and updates ticket labels.

## Output

Report a single summary block:

```
Added: <title>
  Ticket:   <ticket ID> — <Linear URL>
  Summary:  posted
```

If any step fails, report which step and why. Do not silently skip failures.
