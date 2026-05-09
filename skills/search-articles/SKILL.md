---
name: search-articles
description: Search Hacker News and curated tech blogs for recent articles on agentic AI and data engineering. Returns a raw list of candidate URLs with titles and dates. Used as the first step in the tech-digest workflow.
model: claude-opus-4-6
effort: medium
---

# Search for Recent Tech Articles

Find candidate articles from the past 4 days across Hacker News and curated blogs.

---

## Step 1 - Search Hacker News

Calculate CUTOFF = today minus 4 days in Unix epoch seconds.
Use WebFetch to call the HN Algolia API in parallel:

- https://hn.algolia.com/api/v1/search?query=agentic+AI+agent+framework&tags=story&numericFilters=created_at_i>CUTOFF&hitsPerPage=20
- https://hn.algolia.com/api/v1/search?query=data+engineering+AI+Kafka+Spark&tags=story&numericFilters=created_at_i>CUTOFF&hitsPerPage=20

Also run WebSearch queries in parallel:
- site:news.ycombinator.com Show HN agent AI tools
- site:news.ycombinator.com Show HN data engineering AI

## Step 2 - Search curated blogs

Compute CUTOFF_DATE = today minus 4 days (YYYY-MM-DD format).
Run these WebSearch queries in parallel using after:CUTOFF_DATE operator:

- site:simonwillison.net after:CUTOFF_DATE
- site:databricks.com/blog after:CUTOFF_DATE AI agent MCP
- site:confluent.io/blog after:CUTOFF_DATE AI agent data
- site:towardsdatascience.com after:CUTOFF_DATE release tool launch
- site:dataengineeringweekly.com after:CUTOFF_DATE

## Output

Return a deduplicated list of candidate articles as:
```
- [Title] | [URL] | [Source] | [Date if known]
```

Include all results — do not filter yet. Aim for 20-30 candidates.
