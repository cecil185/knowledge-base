---
name: bulk-ingest-articles
description: >
  Creates Linear tickets for filtered article buckets — deduplicates against existing tickets,
  prompts user approval for threshold articles, and spawns parallel read-article agents for
  each created ticket. Third step of /digest; called after filter-articles completes.
when_to_use: >
  Trigger when the filter-articles output is ready and tickets need to be created, or when
  the user says "bulk ingest", "create tickets for these articles", or "process the filtered articles".
argument-hint: "[auto-ticket list] [threshold list] [drop list]"
disable-model-invocation: true
model: claude-opus-4-6
effort: low
---
# bulk-ingest-articles

Third step of `/digest`. Takes the three-bucket output from `filter-articles` and creates Linear tickets for articles that passed filtering.

**Example:** Called automatically by `/digest` after `filter-articles` returns classified buckets.

## Active project

Use the `LINEAR_PROJECT` name established by the calling skill (digest). If called directly, determine the active project by reading `CLAUDE.md`, finding the **Default project** slug, and reading its Linear Project value from the Projects table.

## Input

Three lists produced by `filter-articles`:

- **auto-ticket** — articles that clearly match the goal; create immediately
- **threshold** — borderline articles with 1-2 sentence summaries; require user approval
- **drop** — low-quality or low-relevance articles; skip silently

## Steps

### 1. Deduplicate all candidates

Before creating any ticket, run the `check-duplicate` skill for each article URL, passing `LINEAR_PROJECT` and `PROJECT_DIR`. If `linear_ticket` is not null, skip it and record it in the skipped-duplicates list.

Run deduplication for threshold articles before prompting the user — no point asking about a duplicate.

### 2. Create auto-ticket articles

For each article in the auto-ticket list that is not a duplicate: run the `create-ticket` skill immediately without asking the user.

### 3. Process threshold articles

For each article in the threshold list that is not a duplicate: present it to the user with this format in a numbered list:

```
1. [Article Title]
<URL>
<1-2 sentence summary from filter-articles>
Create ticket? (yes/no)
```

Wait for the user's response before moving to the next threshold article. Run `create-ticket` only if the user approves. Record rejections in the output.

### 4. Skip drop articles

Do nothing. Do not mention them.

## Output

After all tickets are processed, report:

1. **Created tickets** — list of ticket IDs and their Linear URLs
2. **Skipped duplicates** — list of article titles/URLs that already had tickets
3. **Rejected threshold articles** — list of titles the user declined

## Parallel article reading

After all tickets are processed, spawn one `read-article` agent per created ticket **in parallel** using the Agent tool (subagent_type: `read-article`). Do not wait for one to finish before starting the next — launch all at once.

For each ticket, derive a `raw_file` slug from the article title: lowercase, words joined by hyphens, `.md` suffix (e.g. `my-article-title.md`). Pass these inputs to each agent:

```
ticket=<ticket_id> url=<article_url> raw_file=<slug>.md project_slug=<active_project_slug>
```

Wait for all agents to complete, then report their outcomes alongside the ticket creation summary.
