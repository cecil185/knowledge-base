---
name: filter-articles
description: Filter a list of fetched articles down to only those relevant to Cecil's current learning goals. Reads goals from ./goal.md. Used as the third step in the tech-digest workflow.
model: claude-opus-4-6
effort: low
---

# Filter Articles for Relevance

Given a list of fetched articles, keep only those that align with Cecil's current goals.

---

## Input

A list of fetched articles:
```
- [Title] | [one-sentence summary] | [publish date] | [URL]
```

## Step 1 - Read goals

Read `./goal.md` to understand what Cecil is currently trying to learn or build.
If the file doesn't exist, report it and skip filtering (pass all articles through).

## Step 2 - Filter

For each article, ask: does this meaningfully advance one of the stated goals?

Keep: concrete tools, techniques, or insights that directly serve a goal.
Drop: trend pieces, opinion, tutorials on basics, content that's adjacent but not useful.

Be strict. A false positive costs more than a false negative — Cecil reads to *act*, not to stay current.

## Output

Return only the relevant articles:
```
- [Title] | [one-sentence summary] | [publish date] | [URL] | [which goal it serves]
```

Also state how many articles were dropped and why (one clause per drop reason, grouped).
