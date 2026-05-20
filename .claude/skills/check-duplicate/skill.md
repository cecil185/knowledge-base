---
name: check-duplicate
description: >
  Checks whether an article URL already exists as a Linear ticket in the active project. Returns the ticket ID if found, null if not. Primitive called by add-article and bulk-ingest-articles before creating tickets.
when_to_use: >
  Trigger when a URL needs deduplication before ticket creation. Called internally by
  add-article and bulk-ingest-articles; not typically invoked directly by the user.
user-invocable: false
model: claude-opus-4-6
effort: low
---
# check-duplicate

Deduplication primitive. Given a URL and the active project context, checks Linear and reports what already exists.

**Example:** Called by `add-article` before creating a ticket for `https://martinfowler.com/articles/patterns-of-distributed-systems/`.

## Input

- `URL` — the article URL to check
- `LINEAR_PROJECT` — the active Linear project name (from CLAUDE.md Projects table)
- `PROJECT_DIR` — the active project directory (e.g. `projects/data-ai-engineering`)

## URL normalisation

Before any comparison, normalise the input URL and all stored URLs the same way:
- Strip trailing slashes
- Remove all `utm_*` query parameters
- Treat `http://` and `https://` as identical (compare without scheme prefix)

## Check: Linear

Search the active Linear project (team CC, project `LINEAR_PROJECT`) for any ticket whose description contains the normalised URL. Use the Linear MCP tools.

- If found: record `linear_ticket = <ticket ID>` (e.g. `CC-42`)
- If not found: record `linear_ticket = null`

## Output

Return a result object. Callers use this to decide whether to skip, warn, or proceed:

```
duplicate_check:
  linear_ticket: <ticket ID or null>
```

Do not make any decisions about what to do with this result — that is the caller's responsibility.
