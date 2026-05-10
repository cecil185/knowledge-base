---
name: digest
description: End-to-end pipeline — discover articles, filter, ticket, read in full, and update the wiki. Primary entry point; run /digest to kick everything off.
model: claude-opus-4-6
effort: high
---
# Digest

End-to-end article pipeline. Discovers candidates, filters them against the current goal, creates Linear tickets, reads qualifying articles in full, and compiles the wiki.

## Arguments

Optional: a project slug (e.g. `/digest applied-ai`). If omitted, uses the default project.

## Steps

Run these in sequence. Each step delegates fully to its sub-skill — keep this orchestrator thin.

### 0. Determine active project

Read `CLAUDE.md` from the repo root. Find the `## Projects` section. Read the **Default project** value.

If the user passed a project slug as an argument, use that slug instead. Validate that the slug exists in the Projects table. If it does not exist, stop and list the valid slugs.

Set `PROJECT_DIR = projects/<active-slug>` (relative to repo root).
Set `LINEAR_PROJECT` = the Linear Project value from the Projects table row matching the active slug.

Announce which project is active: `Running digest for project: <Name> (<slug>)`

### 1. Verify goal.md

Read `<PROJECT_DIR>/goal.md`. If the file does not exist, stop immediately and tell the user:

> `<PROJECT_DIR>/goal.md` not found. Run `/goal-refine` first to define your learning goal, then re-run `/digest`.

Do not proceed past this step without a valid `goal.md`.

### 2. Discover candidates

Run the `search-articles` skill. Pass the active `PROJECT_DIR` so it reads the correct `sources.md`. It returns a flat list of candidate articles (title + URL) sourced from Hacker News and every entry in `<PROJECT_DIR>/sources.md`.

### 3. Filter candidates

Run the `filter-articles` skill, passing in the candidate list and the contents of `<PROJECT_DIR>/goal.md`. It classifies every article into one of three buckets:

- **Drop** — low quality or low relevance; no ticket created.
- **Auto-ticket** — clear match; ticket created without user input.
- **Threshold** — borderline; show the user a 1–2 sentence summary and ask for approval before ticketing.

### 4. Create tickets

Run the `create-tickets` skill with the classified buckets and the active `LINEAR_PROJECT` name.

- For **threshold** articles: present summaries to the user one at a time and wait for approval (y/n) before creating each ticket.
- For **auto-ticket** articles: create tickets immediately, no pause.
- Ticket fields: title, URL, short description. Labels set to `ai-not-read` and `human-not-read`.
- Deduplication: skip any URL already present as a ticket in the active Linear project.

### 5. Read each new ticket

For every ticket created in step 4, run the `read-article` skill. Pass the ticket ID, article URL, and active `PROJECT_DIR`. `read-article` fetches the full content, writes a raw markdown file to `<PROJECT_DIR>/raw/`, posts a comment to the Linear ticket with TLDR / Goal relation / How to apply, and updates the ticket label from `ai-not-read` to `ai-read`.

Run reads sequentially to avoid rate-limit issues.

### 6. Compile wiki

After all reads complete, run the `wiki:compile` skill with the active `PROJECT_DIR`. It rebuilds `<PROJECT_DIR>/wiki/` from the full contents of `<PROJECT_DIR>/raw/`, updating concept pages and synthesis notes. Wikilinks use Obsidian-compatible `[[double-bracket]]` format.

### 7. Report

Output a single summary block — no padding:

```
Digest complete — project: <Name>
  Found:     N articles
  Dropped:   N
  Ticketed:  N auto + N approved from threshold (N rejected)
  Read:      N articles
  Wiki:      updated
```

If any step fails, report which step failed and why, then stop. Do not silently skip failures.
