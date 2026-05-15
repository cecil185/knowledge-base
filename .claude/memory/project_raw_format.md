---
name: project_raw_format
description: What raw/ article files actually contain — AI-analyzed summaries, not verbatim text
metadata:
  type: project
---

Files in `projects/<slug>/raw/` are AI-analyzed/summarized versions of articles, not verbatim article text. They have frontmatter with metadata (title, url, fetched date, linear_ticket) and structured section summaries.

**Why:** Confirmed by user when I incorrectly stated raw/ files were verbatim article content.

**How to apply:** When describing raw/ files, say they contain AI-analyzed summaries. When describing what `wiki:ingest` saves, say it saves an analyzed version, not the raw text.
