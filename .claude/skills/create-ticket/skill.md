---
name: create-ticket
description: >
  Creates a single Linear article ticket with correct format, labels, and project assignment.
  Returns the created ticket ID. Called by add-article (single manual add) and
  bulk-ingest-articles (batch processing).
when_to_use: >
  Trigger when a new article ticket needs to be created in Linear. Called internally by
  add-article and bulk-ingest-articles; not typically invoked directly by the user.
disable-model-invocation: true
model: claude-opus-4-6
effort: low
---
# create-ticket

Ticket creation primitive. Creates one Linear ticket for a single article. Called by `bulk-ingest-articles` (batch) and `add-article` (single manual add).

**Example:** Called by `add-article` with title "Patterns of Distributed Systems", URL, and a 2-sentence summary to create ticket `CC-42`.

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
- **Labels**: `ai-discovered`
- **Description**:
  ```
  <url>

  Source: <source> | <date>

  <summary>
  ```

## Output

Return the created ticket ID (e.g. `CC-42`) and its Linear URL. If creation fails, report the error with enough detail for the caller to retry or surface it to the user.
