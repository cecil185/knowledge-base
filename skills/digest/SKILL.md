---
name: digest
description: End-to-end pipeline — discover articles, filter, ticket, read in full, and update the wiki. Primary entry point; run /digest to kick everything off.
model: claude-opus-4-6
effort: high
---
# Digest

End-to-end article pipeline. Discovers candidates, filters them against the current goal, creates Linear tickets, reads qualifying articles in full, and compiles the wiki.

## Steps

Run these in sequence. Each step delegates fully to its sub-skill — keep this orchestrator thin.

### 1. Verify goal.md

Read `goal.md` from the repo root. If the file does not exist, stop immediately and tell the user:

> `goal.md` not found. Run `/goal-refine` first to define your learning goal, then re-run `/digest`.

Do not proceed past this step without a valid `goal.md`.

### 2. Discover candidates

Run the `search-articles` skill. It returns a flat list of candidate articles (title + URL) sourced from Hacker News and every entry in `sources.md`.

### 3. Filter candidates

Run the `filter-articles` skill, passing in the candidate list and `goal.md`. It classifies every article into one of three buckets:

- **Drop** — low quality or low relevance; no ticket created.
- **Auto-ticket** — clear match; ticket created without user input.
- **Threshold** — borderline; show the user a 1–2 sentence summary and ask for approval before ticketing.

### 4. Create tickets

Run the `create-tickets` skill with the classified buckets.

- For **threshold** articles: present summaries to the user one at a time and wait for approval (y/n) before creating each ticket.
- For **auto-ticket** articles: create tickets immediately, no pause.
- Ticket fields: title, URL, short description. Labels set to `ai-not-read` and `human-not-read`.
- Deduplication: skip any URL already present as a ticket in the Linear Wiki project.

### 5. Read each new ticket

For every ticket created in step 4, run the `read-article` skill. Pass the ticket ID and article URL. `read-article` fetches the full content, writes a raw markdown file to `raw/`, posts a comment to the Linear ticket with TLDR / Goal relation / How to apply, and updates the ticket label from `ai-not-read` to `ai-read`.

Run reads sequentially to avoid rate-limit issues.

### 6. Compile wiki

After all reads complete, run the `wiki:compile` skill. It rebuilds `wiki/` from the full contents of `raw/`, updating concept pages and synthesis notes. Wikilinks use Obsidian-compatible `[[double-bracket]]` format.

### 7. Report

Output a single summary block — no padding:

```
Digest complete.
  Found:     N articles
  Dropped:   N
  Ticketed:  N auto + N approved from threshold (N rejected)
  Read:      N articles
  Wiki:      updated
```

If any step fails, report which step failed and why, then stop. Do not silently skip failures.
