---
name: search-articles
description: Find candidate articles from the past 4 days from HN and curated blog sources; first step of /digest
model: claude-opus-4-6
effort: medium
---
# search-articles

Find candidate articles published in the last 4 days from Hacker News and all sources listed in `sources.md`. Produce a flat deduplicated list ready for `filter-articles` to classify.

## Steps

### 1. Calculate the cutoff

Set CUTOFF to today minus 4 days.

- Unix epoch seconds form (for HN API): `CUTOFF_EPOCH`
- ISO date form (for web search): `CUTOFF_DATE` in `YYYY-MM-DD` format

### 2. Query HN Algolia API

Run both searches **in parallel**:

```
https://hn.algolia.com/api/v1/search?query=agentic+AI+agent+framework&tags=story&numericFilters=created_at_i>CUTOFF_EPOCH&hitsPerPage=20

https://hn.algolia.com/api/v1/search?query=data+engineering+AI&tags=story&numericFilters=created_at_i>CUTOFF_EPOCH&hitsPerPage=20
```

From each hit, extract:
- `title`
- `url` (use `story_url` if present, otherwise the HN item URL `https://news.ycombinator.com/item?id=<objectID>`)
- `source`: `"HN"`
- `snippet`: first sentence of the HN post text if present, otherwise empty string
- `date`: `created_at` field formatted as `YYYY-MM-DD`

### 3. Query curated blog sources

Read `sources.md` from the repo root to get the list of blog sources.

For each source, run a `WebSearch` with the query:

```
site:<source-domain> after:<CUTOFF_DATE>
```

Run all source searches **in parallel**.

From each result, extract:
- `title`
- `url`
- `source`: the blog domain
- `snippet`: the search result description/excerpt
- `date`: date from search result metadata if available, otherwise leave blank

### 4. Deduplicate

Normalise all URLs before comparing:
- Strip trailing slashes
- Strip `utm_*` query parameters
- Treat `http://` and `https://` variants as identical

Keep only the first occurrence of each URL across all result sets.

### 5. Output

Emit a flat markdown list. Aim for 20–40 candidates. Do not filter or rank at this stage — include everything that passed deduplication.

Format each candidate as:

```
- **<title>**
  URL: <url>
  Source: <source>
  Date: <date or "unknown">
  Snippet: <snippet or "none">
```

If fewer than 10 candidates are found, note that the search returned limited results — do not pad with low-confidence items.
