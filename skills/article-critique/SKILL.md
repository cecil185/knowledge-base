---
name: article-critique
description: On-demand deep review of a single article URL. Rates it, creates a Linear ticket if worth it, reads in full, and posts a summary comment.
model: claude-opus-4-6
effort: medium
---
# Article Critique

On-demand review of a single article. Use when given a URL directly — not through `/digest`. Produces a scored rating report, creates a Linear ticket for qualifying articles, and runs a full read on anything that clears the bar.

## Steps

### 1. Read goal.md

Read `goal.md` from the repo root. Use the What / Why / Horizon / Success fields and the high/low relevance signals to calibrate all scoring decisions below.

### 2. Fetch the article

Fetch the full article content via WebFetch using the provided URL. If the fetch fails, report the error and stop.

### 3. Rate on four axes

Score each axis 0–3. Max total: 12.

| Axis | 0 | 1 | 2 | 3 |
|------|---|---|---|---|
| **Signal** | Pure hype or restatement | Weak signal, mostly summary | Concrete technique or insight | Novel, specific, reproducible insight |
| **Goal fit** | No overlap with goal signals | Tangential overlap | Matches one high-relevance signal | Matches multiple high-relevance signals |
| **Actionability** | Nothing Cecil could do with this | Vaguely relevant to future work | Could apply within a month | Could change something Cecil does this week |
| **Timing** | Unrelated to current horizon | Adjacent to current priorities | Supports a current priority | Directly addresses a current horizon goal |

Do not round up. If the article is mostly marketing copy dressed as a tutorial, Signal is 0 or 1 regardless of topic.

### 4. Classify total score

| Score | Label |
|-------|-------|
| 10–12 | High value |
| 7–9   | Worth reading |
| 4–6   | Marginal |
| 0–3   | Skip |

### 5. Output rating report

Always output the rating report, regardless of score:

```
**[Article Title]**
[URL]
Rating: N/12 — [High value | Worth reading | Marginal | Skip]
- Signal: N/3 — one clause
- Goal fit: N/3 — one clause
- Actionability: N/3 — one clause
- Timing: N/3 — one clause

Thesis: one sentence — the actual claim under the padding.
Bottom line: 1-2 sentences — read, skim, or drop and why.
```

One clause means one clause. No hedging. If it's hype, say it's hype.

### 6. Ticket and read (rating ≥ 7 only)

If the total score is below 7, stop after the report. No ticket.

If the total score is 7 or higher:

1. Search the Linear Wiki project for an existing ticket whose description or title contains this exact URL. If a duplicate exists, report the existing ticket ID and stop — do not create a second ticket.
2. Create a Linear ticket in the Wiki project:
   - Title: article title
   - Description: URL + one-sentence thesis
   - Labels: `ai-not-read`, `human-not-read`
3. Run the `read-article` skill, passing the new ticket ID and URL. It will fetch full content, write to `raw/`, post a TLDR / Goal relation / How to apply comment, and flip the label to `ai-read`.

Do not run `wiki:compile` automatically here — that is the digest pipeline's responsibility. If the user wants the wiki updated after a critique, they can run `/wiki:compile` manually.
