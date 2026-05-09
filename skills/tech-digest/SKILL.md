---
name: tech-digest
description: Find the latest relevant tech articles for agentic software development and AI for data engineering from the past 4 days. Searches Hacker News and curated blogs, filters for relevance to Cecil's goals, and outputs 2-sentence summaries for quick review. Use when asked for a tech digest, latest AI tools, or recent data engineering news.
model: claude-opus-4-6
effort: high
---

# AI Tech Digest

Surface new articles relevant to Cecil's current goals so he can decide what to read in full.

Run each sub-skill in sequence, passing the output of each as input to the next.

---

## Step 1 - Search

Run the `search-articles` skill to find candidate articles from Hacker News and curated blogs.

## Step 2 - Fetch

Run the `fetch-articles` skill with the candidate list from Step 1.

## Step 3 - Filter

Run the `filter-articles` skill with the fetched articles from Step 2.
This reads `./goal.md` and drops irrelevant articles.

## Step 4 - Summarize

Run the `summarize-articles` skill with the filtered list from Step 3.

Output the summaries. Cecil will pick which articles to read in full using `/article-critique <url>`.
