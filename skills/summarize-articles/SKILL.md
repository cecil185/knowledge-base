---
name: summarize-articles
description: Produce a 2-sentence summary of each relevant article so Cecil can do a quick pass and decide which to read in full. Used as the final step in the tech-digest workflow.
model: claude-opus-4-6
effort: low
---

# Summarize Articles for Quick Review

Produce a 2-sentence summary per article so Cecil can scan and decide what to read in full.

---

## Input

A filtered list of relevant articles:
```
- [Title] | [one-sentence summary] | [publish date] | [URL] | [goal it serves]
```

## Step 1 - Summarize each article

For each article, write exactly 2 sentences:
1. What it is / what it argues (the load-bearing claim, stripped of padding).
2. Why it might matter to Cecil specifically — concrete, not generic.

Don't hedge. Don't pad. If the article is marginal, say so in sentence 2.

## Output

```
**[Title]**
[URL]
[Sentence 1. Sentence 2.]

---
```

Repeat for each article. No intro, no outro, no categories. Just the list.
Cecil will pick which to read in full using `/article-critique <url>`.
