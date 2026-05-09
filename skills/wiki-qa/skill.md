---
name: wiki:qa
description: Answer research questions by synthesizing the local wiki knowledge base. Use when asked "what do I know about X", "summarize what I've learned about Y", or "have I seen anything on Z".
model: claude-opus-4-6
effort: medium
---
# wiki:qa

The primary query interface for the local knowledge base. Synthesizes an answer from `wiki/` (and `raw/` when needed), saves the output to `wiki/qa/`, and appends it to `wiki/INDEX.md`. Never fabricates — if the wiki does not cover a topic, it says so plainly.

## Input

A natural-language question from the user. Examples:

- "What do I know about RAG?"
- "Summarize what I've learned about inference optimization"
- "Have I seen anything on model quantization?"
- "Compare vLLM and llama.cpp"

## Step 1: Survey the knowledge base

Read:

- `/Users/cecil/Code/me/knowledge-base/wiki/INDEX.md`
- `/Users/cecil/Code/me/knowledge-base/wiki/SUMMARY.md`

From these, build a mental map of what topics the wiki covers, what articles exist, and how they are organized. Identify which articles are most likely relevant to the user's question based on titles, tags, and the SUMMARY.

## Step 2: Select and read relevant articles

From the full article list in INDEX.md, select the **5–15 articles** most relevant to the question. Relevance criteria:

- Title or slug directly matches a key term in the question.
- Article is linked from or links to another highly relevant article.
- Article is tagged with a term that appears in the question.

Prefer wiki articles (concepts/, tools/) over Q&A outputs (qa/) to avoid circular synthesis.

Read each selected article in full. Note any `[[WikiLink]]` references to other articles not already in your selection — if those links look highly relevant, read those too (up to the 15-article cap).

If fewer than 3 relevant wiki articles exist for the question, proceed to Step 3. Otherwise, skip Step 3.

## Step 3: Supplement from raw/ (when coverage is thin)

Read `/Users/cecil/Code/me/knowledge-base/raw/INDEX.md`.

Select up to 5 raw source files whose titles or slugs are relevant to the question. Read them. Use their content to supplement the answer, and note in the Gaps section that these raw docs have not yet been compiled into wiki articles.

## Step 4: Determine output format

Choose the format that best serves the question type:

| Question type | Format |
|---|---|
| Factual ("what is X") | Prose paragraphs |
| Comparative ("X vs Y", "compare X and Y") | Comparison table followed by prose analysis |
| Architectural ("how does X work", "what's the structure of Y") | Mermaid diagram followed by explanation |
| Synthesis ("what have I learned about X", "summarize X") | Full structured article with sections |

## Step 5: Synthesize the answer

Write the answer using the chosen format. Rules:

- **First paragraph**: direct answer. Do not bury the lede with background.
- **Cite with WikiLinks**: every claim drawn from a specific wiki article must include a `[[slug]]` reference. Do not cite raw/ files with WikiLinks — reference them as `raw/slug.md`.
- **Surface tradeoffs and contradictions**: if two articles disagree on a point, name both and state the disagreement explicitly. Do not paper over conflicts.
- **Prefer synthesis over quoting**: paraphrase and connect ideas; do not transcribe article excerpts verbatim.
- **Never fabricate**: if the wiki does not cover something, state that gap in the Gaps section rather than filling it from general knowledge.

End every answer — regardless of format — with this section:

```
## Gaps

What the wiki is missing on this topic:

- <specific gap>: run `/digest` to find new articles, or `wiki:ingest <url>` to add a specific source.
- <another gap>: ...

_If coverage looks sufficient, no action needed._
```

If there are no meaningful gaps, write: `_The wiki's coverage on this topic appears sufficient for the current goal._`

## Step 6: Save to wiki/qa/

Generate a slug from the question: lowercase, spaces and punctuation replaced with hyphens, truncated to 60 characters. Example: "what do I know about RAG" → `what-do-i-know-about-rag`.

Write the answer to `/Users/cecil/Code/me/knowledge-base/wiki/qa/<slug>.md` with this frontmatter:

```
---
title: <question, as asked>
date: <YYYY-MM-DD>
type: qa
sources:
  - <wiki article slug>
  - <wiki article slug>
  - ...
---
```

Follow the frontmatter with the full synthesized answer from Step 5.

If a Q&A file with the same slug already exists, overwrite it — the new answer supersedes the old one.

## Step 7: Update wiki/INDEX.md

Read `/Users/cecil/Code/me/knowledge-base/wiki/INDEX.md`. Locate a `## Q&A` section. If no such section exists, append one at the end of the file.

Append one line under `## Q&A`:

```
- [[qa/<slug>]] — <question, as asked> — <YYYY-MM-DD>
```

Do not duplicate the entry if the same slug already appears in the Q&A section — replace the existing line with the updated date.

## Output

After saving the file, display the full synthesized answer in the conversation (do not make the user open the file to see the answer). Then report:

```
Saved to wiki/qa/<slug>.md — appended to wiki/INDEX.md.
Sources read: N wiki articles, N raw docs.
```

If any article read fails (file not found, etc.), note it and continue — do not abort the answer for a single missing file.
