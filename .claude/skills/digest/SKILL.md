---
name: digest
description: End-to-end pipeline — discover articles, filter, ticket, read in full, and update the wiki. Primary entry point; run /digest to kick everything off.
model: claude-opus-4-6
effort: high
---
# Digest

End-to-end article pipeline. Discovers candidates, filters them against the current goal, creates Linear tickets, reads qualifying articles in full, and compiles the wiki.

## Arguments

**project**: A project slug. If omitted, use 'data-ai-engineering'

## Steps

Run these in sequence. Each step delegates fully to its sub-skill — keep this orchestrator thin.

### 0. Determine active project

Validate that the slug exists in the Projects table. If it does not exist, stop and list the valid slugs.

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

Run the `filter-articles` skill, passing the candidate list and `PROJECT_DIR`.

### 4. Create tickets

Run the `create-tickets` skill with the classified buckets, `LINEAR_PROJECT`, and `PROJECT_DIR`.

### 5. Read each new ticket

`create-tickets` spawns parallel `read-article` agents before returning. No action needed here — wait for it to complete.

### 6. Compile wiki

Run the `wiki:compile` skill with `PROJECT_DIR`.

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
