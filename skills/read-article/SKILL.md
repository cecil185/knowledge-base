---
name: read-article
description: Fetch a full article, post a structured AI summary as a Linear ticket comment, update ticket labels, and save raw content to raw/
model: claude-opus-4-6
effort: medium
---
# read-article

Reads an article in full, posts a structured summary as a comment on its Linear ticket, updates ticket labels, and saves raw content to `raw/`. Called for each ticket after `create-tickets`, and also callable on-demand.

## Input

Either a Linear ticket ID (e.g. `CCTD-42`) or an article URL.

- If a **ticket ID** is given: read the ticket description to extract the URL.
- If a **URL** is given: search the Linear Wiki project for a ticket whose description contains that URL. If no ticket is found, stop and report the error — do not proceed without a ticket.

## Step 1: Fetch the article

Use WebFetch to retrieve the full article content.

If the fetch fails or the content appears to be a paywall or login wall (thin content, subscription prompt, no article body):

1. Post a comment on the Linear ticket:
   ```
   ## AI Read — Fetch Failed

   Fetch failed: <reason — paywalled / fetch error / empty response>.
   Labels and raw/ not updated.
   ```
2. Stop. Leave all labels unchanged.

## Step 2: Read goal.md

Read `/Users/cecil/Code/me/wiki-workflow/goal.md` to ground the summary in Cecil's current learning goals. Use the goal's Reading intent and High-relevance signals fields when writing the "How it relates to your goal" section.

## Step 3: Post summary comment

Post the following comment to the Linear ticket. Follow this format exactly — no extra sections, no omissions:

```
## AI Summary

**TLDR**
2-3 sentences. What the article actually argues, stripped of padding.

**How it relates to your goal**
1-2 sentences. Direct connection to goal.md — or "not directly relevant" if the connection is thin.

**How to apply it**
Concrete next step or experiment Cecil could run. If nothing actionable: "No direct action — awareness only."
```

## Step 4: Update labels

Using the Linear MCP tools:

- Add label: `ai-read`
- Remove label: `ai-not-read`
- Leave `human-not-read` unchanged

## Step 5: Save raw content

Generate a slug from the article title: lowercase, spaces and punctuation replaced with hyphens, truncated to 60 characters.

Write the file to `/Users/cecil/Code/me/wiki-workflow/raw/<slug>.md` with this frontmatter followed by the full article body:

```
---
title: <article title>
url: <article URL>
fetched: <YYYY-MM-DD>
linear_ticket: <ticket ID>
tags: []
---

<full article body>
```

Then append one line to `/Users/cecil/Code/me/wiki-workflow/raw/INDEX.md` (create the file with a `# Raw Article Index` header if it does not exist):

```
- [<title>](<slug>.md) — <ticket ID> — <YYYY-MM-DD>
```

## Output

Report:
- Ticket ID and Linear URL
- Whether the summary comment was posted successfully
- Path to the saved raw file, or reason for failure
