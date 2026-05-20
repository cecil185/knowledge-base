---
name: wiki:qa
description: >
  Answers research questions by synthesizing the local wiki knowledge base. Uses the
  Anthropic Citations API with retrieved chunks when available; falls back to synthesizing
  from wiki/ and raw/ files with [synthesis] tags. Saves answers to wiki/qa/ and updates
  INDEX.md. Use when the user asks "what do I know about X", "summarize what I've learned
  about Y", or "have I seen anything on Z".
when_to_use: >
  Trigger when user asks "what do I know about X", "summarize what I've learned about Y",
  "have I seen anything on Z", "compare X and Y from my notes", or "wiki:qa <question>".
argument-hint: "\"<question>\" [--project <slug>]"
model: claude-opus-4-6
effort: medium
disable-model-invocation: true
---
# wiki:qa

The primary query interface for the local knowledge base. When a `chunks.sqlite` store exists for the active project, it retrieves grounded answers using the Anthropic Citations API with markdown footnotes. When no chunk store is available, it falls back to synthesizing from `wiki/` and `raw/` files (all claims tagged `[synthesis]`). Output is always saved to `wiki/qa/` and indexed.

## Active project

Determine the active project by reading `CLAUDE.md` from the repo root. Find the **Default project** slug in the `## Projects` section. Set `PROJECT_DIR = projects/<slug>`. All file paths below are relative to `/Users/cecil/Code/me/knowledge-base/<PROJECT_DIR>`.

If called with a project argument (e.g. `/wiki:qa "what do I know about RAG" --project applied-ai`), use that slug instead.

## Input

A natural-language question from the user. Examples:

- "What do I know about RAG?"
- "Summarize what I've learned about inference optimization"
- "Have I seen anything on model quantization?"
- "Compare vLLM and llama.cpp"

## Step 1: Retrieve chunks from chunk store

Run the retrieval script against the project's chunk store:

```bash
python3 /Users/cecil/Code/me/knowledge-base/scripts/retrieve_chunks.py \
  --project-dir /Users/cecil/Code/me/knowledge-base/<PROJECT_DIR> \
  --query "<user question>" \
  --top-k 10
```

Parse the JSON array output into a list of chunk objects: `[{id, article_slug, paragraph_idx, text, url}]`.

**If the result is an empty list** (DB absent or no matches): skip Steps 2–4 and jump directly to Step 5 (Fallback path).

## Step 2: Call Anthropic Citations API

Using the Anthropic Python SDK, make a messages API call with citations enabled. Pass each retrieved chunk as a `document` block with its URL as the `title` field.

```python
import anthropic

client = anthropic.Anthropic()

documents = [
    {
        "type": "document",
        "source": {"type": "text", "media_type": "text/plain", "data": chunk["text"]},
        "title": chunk["url"],
        "citations": {"enabled": True},
    }
    for chunk in retrieved_chunks
]

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2048,
    system=(
        "You are a research assistant answering questions from a personal knowledge base. "
        "Answer thoroughly. For any claim you can ground in the provided documents, use a citation. "
        "For claims you cannot ground, explicitly tag them [synthesis] inline immediately after the sentence."
    ),
    messages=[
        {
            "role": "user",
            "content": documents + [{"type": "text", "text": f"Question: {question}"}],
        }
    ],
)
```

Parse the response `content` blocks. For each block:
- If it contains `citations` (a list of citation objects): extract `cited_text` and `document_title` (the URL) from each citation object.
- If it has no citations attached: the text is ungrounded.

Build an intermediate representation — a list of segments: `{text: str, citations: [{url: str, cited_text: str}]}`.

## Step 3: Render footnotes and tag [synthesis]

Convert the intermediate representation to final markdown.

Rules:
- For each segment **with citations**: append `[^N]` after the segment text in the answer body. Increment N for each unique citation. Accumulate footnote definitions of the form `[^N]: <url> — "<cited_text>"` for the footnote block emitted after `---` at the end of the answer body.
- For each segment **without citations** that makes a factual claim: append `[synthesis]` immediately after the sentence inline.

Footnote format example:

```
The study found that transformers outperform RNNs on long sequences.[^1]

---
[^1]: https://example.com/paper — "transformers outperform RNNs on long sequences of more than 512 tokens"
```

`[synthesis]` tag format: `This suggests broader applicability.[synthesis]`

## Step 4: Build full answer

Assemble the answer in the following order.

**Reading plan block** — output this to the conversation before calling the Citations API so progress is visible:

```
## Reading plan

Approach: <one sentence on how you answered — e.g. "Grounding answer in retrieved chunks on transformer inference">

Retrieved chunks:
- `<article_slug>` paragraph N — <one phrase: why relevant>
- `<article_slug>` paragraph N — <one phrase: why relevant>
- ...
```

**Grounded answer body** (from Step 3) — prose with `[^N]` footnote references and `[synthesis]` tags inline.

**Sources Consulted section:**

```
## Sources Consulted

| Source | What it contributed |
|--------|---------------------|
| <article_slug> | <one line: the key fact or argument this chunk provided> |
| ... | ... |
```

List every article_slug that appeared in the retrieved chunks. If a chunk was retrieved but contributed nothing to the answer, include it with "retrieved but not directly used."

**Gaps section:**

```
## Gaps

What the wiki is missing on this topic:

- <specific gap>: run `/digest` to find new articles, or `wiki:ingest <url>` to add a specific source.
```

If there are no meaningful gaps: `_The wiki's coverage on this topic appears sufficient for the current goal._`

**Footnote definitions block** (if any footnotes were emitted):

```
---
[^1]: <url> — "<cited_text>"
[^2]: <url> — "<cited_text>"
```

## Step 5: Fallback path (when chunk retrieval returns empty)

When `retrieve_chunks.py` returns `[]` (DB absent or no matches), fall back to synthesizing from wiki and raw files.

**Survey the knowledge base:**

Read:
- `<PROJECT_DIR>/wiki/INDEX.md`
- `<PROJECT_DIR>/wiki/SUMMARY.md`

Build a mental map of what topics the wiki covers, what articles exist, and how they are organized.

**Select and read relevant articles:**

From the full article list in INDEX.md, select the **5–15 articles** most relevant to the question. Relevance criteria:
- Title or slug directly matches a key term in the question.
- Article is linked from or links to another highly relevant article.
- Article is tagged with a term that appears in the question.

Prefer wiki articles (concepts/, tools/) over Q&A outputs (qa/) to avoid circular synthesis.

Output the reading plan to the conversation before reading files:

```
## Reading plan

Approach: <one sentence on how you'll answer — fallback synthesis from wiki/raw>

Selected articles:
- `<path>` — <one phrase: why this is relevant>
- ...
```

Then read each selected article in full. Note any `[[WikiLink]]` references to other articles not already in your selection — if highly relevant, read those too (up to the 15-article cap). Append added articles to the reading plan with a `(+ followed link)` note.

If fewer than 3 relevant wiki articles exist, also read `<PROJECT_DIR>/raw/INDEX.md` and select up to 5 raw source files whose titles or slugs are relevant. Read them.

**Synthesize the answer:**

Choose the format that best serves the question type:

| Question type | Format |
|---|---|
| Factual ("what is X") | Prose paragraphs |
| Comparative ("X vs Y", "compare X and Y") | Comparison table followed by prose analysis |
| Architectural ("how does X work", "what's the structure of Y") | Mermaid diagram followed by explanation |
| Synthesis ("what have I learned about X", "summarize X") | Full structured article with sections |

Rules:
- First paragraph: direct answer. Do not bury the lede.
- Tag **every** factual claim `[synthesis]` inline immediately after the sentence — no footnotes are emitted in fallback mode.
- Surface tradeoffs and contradictions if two sources disagree; name both sources explicitly.
- Never fabricate — state gaps rather than filling from general knowledge.

Sources Consulted section uses the same structure as Step 4 (list every file read). Gaps section must include:

```
Answer sourced from AI summaries only — no chunked articles available for this topic.
Run /digest on relevant URLs to enable cited answers.
```

## Step 6: Save to wiki/qa/

Generate a slug from the question: lowercase, spaces and punctuation replaced with hyphens, truncated to 60 characters. Example: "what do I know about RAG" → `what-do-i-know-about-rag`.

Write the answer to `<PROJECT_DIR>/wiki/qa/<slug>.md` with this frontmatter:

```yaml
---
title: <question, as asked>
date: <YYYY-MM-DD>
type: qa
sources:
  - <article_slug>
  - <article_slug>
  - ...
---
```

Follow the frontmatter with the full answer. If a Q&A file with the same slug already exists, overwrite it — the new answer supersedes the old one.

## Step 7: Update wiki/INDEX.md

Read `<PROJECT_DIR>/wiki/INDEX.md`. Locate the `## Q&A` section. If no such section exists, append one at the end of the file.

Append one line under `## Q&A`:

```
- [[qa/<slug>]] — <question, as asked> — <YYYY-MM-DD>
```

If the same slug already appears in the Q&A section, replace the existing line with the updated date.

## Output

After saving the file, display the full answer in conversation (do not make the user open the file). Then report:

```
Saved to <PROJECT_DIR>/wiki/qa/<slug>.md — appended to wiki/INDEX.md.
Sources: N chunks retrieved, N wiki articles read (fallback).
```

If any file read fails (not found, etc.), note it and continue — do not abort for a single missing file.
