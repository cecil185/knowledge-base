---
name: digest
description: >
  Runs the end-to-end article pipeline — discovers candidates, filters against the current
  goal, creates Linear tickets, reads qualifying articles in full, and compiles the wiki.
  Primary entry point for the knowledge-base system.
when_to_use: >
  Trigger when the user says "run digest", "run the pipeline", "find new articles", "kick off
  digest", or "/digest". Also trigger when the user wants to discover and ingest new articles
  for the active project.
argument-hint: "[project-slug]"
disable-model-invocation: true
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

### 4. Bulk ingest articles

Run the `bulk-ingest-articles` skill with the classified buckets, `LINEAR_PROJECT`, and `PROJECT_DIR`.

### 5. Read each new ticket

`bulk-ingest-articles` spawns parallel `read-article` agents before returning. No action needed here — wait for it to complete.

### 6. Report

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
