---
name: wiki:purge
description: Delete raw files for Linear tickets labelled delete-from-wiki in Done status, then mark those tickets Cancelled
model: claude-opus-4-6
effort: low
---
# wiki:purge

Cleanup primitive. Finds all Linear tickets tagged `delete-from-wiki` that are in **Done** status, deletes their corresponding `raw/` files (matched by URL), removes their entries from `raw/INDEX.md`, then moves each ticket to **Canceled**.

## Active project

Determine the active project by reading `CLAUDE.md` from the repo root. Find the **Default project** slug. Set `PROJECT_DIR = projects/<slug>` and `LINEAR_PROJECT` from the Projects table.

If called with a project argument (e.g. `/wiki:purge --project applied-ai`), use that slug instead.

## Step 1: Find candidate tickets

Using the Linear MCP tools, list all tickets in team `CC`, project `LINEAR_PROJECT`, where:
- Label includes `delete-from-wiki`
- Status is `Done`

If no tickets match, report "No tickets to purge." and stop.

## Step 2: Resolve raw files

For each candidate ticket:

1. Extract the article URL from the ticket description. The URL is the first `https?://` link in the description body.
2. Normalise the URL: strip trailing slash, remove `utm_*` params, drop scheme prefix for comparison.
3. Search `<PROJECT_DIR>/raw/` for files whose frontmatter `url:` field matches the normalised URL. Check all `.md` files — a long article may have been split into `<slug>-part-1.md`, `<slug>-part-2.md`, etc.
4. Record the list of matching file paths. If no file is found, note "no raw file found" for that ticket — still proceed to cancel the ticket in step 4.

## Step 3: Confirm and delete

Display a summary table to the user:

```
Tickets to purge:

  CC-42  — https://example.com/article
            files: raw/example-article.md

  CC-55  — https://other.com/post
            files: (no raw file found — ticket will still be Cancelled)

Proceed? (yes/no)
```

Wait for user confirmation before deleting anything.

On confirmation:

For each ticket that has matching files:
1. Delete each matching file from `<PROJECT_DIR>/raw/`.
2. Remove the corresponding line(s) from `<PROJECT_DIR>/raw/INDEX.md`. Match lines by file path or slug (the filename stem).

## Step 4: Cancel tickets

For each ticket (whether or not a raw file was found), use the Linear MCP tools to move the ticket status to **Canceled**.

## Output

Report a result row for each ticket:

```
CC-42  raw/example-article.md deleted  →  Cancelled
CC-55  (no raw file)                    →  Cancelled
```

If any file deletion or status update fails, report the error and continue processing the remaining tickets.
