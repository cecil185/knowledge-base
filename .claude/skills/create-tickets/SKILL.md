---
name: create-tickets
description: Create Linear Wiki tickets for filtered articles; deduplicates against existing tickets, prompts user for threshold articles, skips drops
model: claude-opus-4-6
effort: low
---
# create-tickets

Third step of `/digest`. Takes the three-bucket output from `filter-articles` and creates Linear tickets for articles that passed filtering.

## Active project

Use the `LINEAR_PROJECT` name established by the calling skill (digest). If called directly, determine the active project by reading `CLAUDE.md`, finding the **Default project** slug, and reading its Linear Project value from the Projects table.

## Input

Three lists produced by `filter-articles`:

- **auto-ticket** — articles that clearly match the goal; create immediately
- **threshold** — borderline articles with 1-2 sentence summaries; require user approval
- **drop** — low-quality or low-relevance articles; skip silently

## Deduplication

Before creating any ticket, search the active Linear project (team CC, project `LINEAR_PROJECT`) for an existing ticket whose description contains the article URL. If a match is found, skip that article and record it in the skipped-duplicates list. Do this check for both auto-ticket and threshold articles (check threshold articles before prompting the user — no point asking about a duplicate).

Use the Linear MCP tools to search existing tickets.

## Auto-ticket articles

For each article in the auto-ticket list that is not a duplicate: create a Linear ticket immediately without asking the user.

## Threshold articles

For each article in the threshold list that is not a duplicate: present it to the user with this format:

```
[Article Title]
<URL>
<1-2 sentence summary from filter-articles>
Create ticket? (yes/no)
```

Wait for the user's response before moving to the next threshold article. Create the ticket only if the user approves. Record rejections in the output.

## Drop articles

Do nothing. Do not mention them.

## Ticket format

Every created ticket must follow this exact format:

- **Title**: article title, truncated to 80 characters if longer
- **Team**: CC
- **Project**: `<LINEAR_PROJECT>` (the active project's Linear project name)
- **Labels**: `ai-not-read` and `human-not-read`
- **Description**:
  ```
  <URL>

  Source: <source name> | <date YYYY-MM-DD>

  <1-2 sentence summary>
  ```

## Output

After all tickets are processed, report:

1. **Created tickets** — list of ticket IDs and their Linear URLs
2. **Skipped duplicates** — list of article titles/URLs that already had tickets
3. **Rejected threshold articles** — list of titles the user declined

Then pass the list of created ticket IDs to the next step (`read-article`) for full reading and summarization.
