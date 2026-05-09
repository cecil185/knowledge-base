---
name: fetch-articles
description: Fetch content from a list of candidate article URLs and extract title, summary, publish date, and URL. Filters out paywalled or irrelevant content. Used as the second step in the tech-digest workflow.
model: claude-opus-4-6
effort: medium
---

# Fetch Article Content

Given a list of candidate article URLs, fetch and extract the key details from each.

---

## Input

A list of candidate articles in the format:
```
- [Title] | [URL] | [Source] | [Date if known]
```

## Step 1 - Select top candidates

Pick the 10 most relevant URLs. Skip duplicates and paywalled sites.

Relevance boost — prioritize:
- AWS, MSK/Kafka, Apache Hudi, PySpark, Airflow
- MCP (Model Context Protocol), Claude Code, Cursor, GitLab CI/CD
- New tool releases, SDKs, libraries, or major version bumps

Exclude: opinion pieces, tutorials on basics, rehashes of old announcements.

## Step 2 - Fetch each URL

Call WebFetch on each selected URL in parallel. Extract:
- Title
- One-sentence summary (what it is and why it matters)
- Publish date
- URL (bare)

If a page is paywalled or returns an error, skip it and note it was skipped.

## Output

Return a list of fetched articles:
```
- [Title] | [one-sentence summary] | [publish date] | [URL]
```
