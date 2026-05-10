---
name: check-duplicate
description: Check whether an article URL already exists in the active Linear project or in raw/INDEX.md; returns status for both checks
model: claude-opus-4-6
effort: low
---
# check-duplicate

Deduplication primitive. Given a URL and the active project context, checks two stores and reports what already exists.

## Input

- `URL` — the article URL to check
- `LINEAR_PROJECT` — the active Linear project name (from CLAUDE.md Projects table)
- `PROJECT_DIR` — the active project directory (e.g. `projects/data-ai-engineering`)

## URL normalisation

Before any comparison, normalise the input URL and all stored URLs the same way:
- Strip trailing slashes
- Remove all `utm_*` query parameters
- Treat `http://` and `https://` as identical (compare without scheme prefix)

## Check 1: Linear

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
