---
name: create-ticket
description: Create a single Linear article ticket with correct format, labels, and project assignment; returns the created ticket ID
model: claude-opus-4-6
effort: low
---
# create-ticket

Ticket creation primitive. Creates one Linear ticket for a single article. Called by `create-tickets` (batch) and `add-article` (single manual add).

## Input

- `title` — article title (will be truncated to 80 characters if longer)
- `url` — article URL
- `summary` — 1–2 sentence summary of the article
- `source` — source name (e.g. blog name, "Hacker News")
- `date` — date the article was found or published, `YYYY-MM-DD`
- `LINEAR_PROJECT` — Linear project name to assign the ticket to (from CLAUDE.md Projects table)

## Ticket format

Create the ticket using the Linear MCP tools with exactly these fields:

- **Title**: `<title>` truncated to 80 characters at a word boundary
- **Team**: `CC`
- **Project**: `<LINEAR_PROJECT>`
- **Labels**: `human-not-read`
- **Description**:
  ```
  <url>

  Source: <source> | <date>

  <summary>
  ```

## Output

Return the created ticket ID (e.g. `CC-42`) and its Linear URL. If creation fails, report the error with enough detail for the caller to retry or surface it to the user.
