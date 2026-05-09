---
name: wiki:lint
description: Audit the wiki for broken links, missing index entries, stubs, uncompiled raw docs, coverage gaps, and suggested connections. Optionally repairs Critical issues and writes stubs for gaps. Run periodically to keep the knowledge base healthy.
model: claude-opus-4-6
effort: medium
---
# wiki:lint

Audits the wiki knowledge base for health issues and growth opportunities. Run periodically or after a large `wiki:compile` batch. Writes findings to `wiki/LINT.md`. Accepts an optional `--fix` flag to auto-repair critical issues and write stub articles for coverage gaps.

## Inputs

- Optional flag: `--fix`

## Step 1: Load index files

Read the following files. If any are missing, note the absence in findings and continue — do not abort.

- `/Users/cecil/Code/me/wiki-workflow/wiki/INDEX.md`
- `/Users/cecil/Code/me/wiki-workflow/wiki/SUMMARY.md`
- `/Users/cecil/Code/me/wiki-workflow/raw/INDEX.md`

Parse each index into a list of (slug, file path, title) entries. Record every entry so later steps can cross-reference them.

## Step 2: Collect all files on disk

List the actual files present under:

- `wiki/concepts/` — concept articles
- `wiki/tools/` — tool profiles
- `wiki/qa/` — Q&A outputs

Build two sets: **indexed** (from INDEX.md) and **on-disk** (from the directory listing). The diff between them produces structural issues.

## Step 3: Structural checks

For each item in INDEX.md, check whether the file exists on disk.

For each file on disk (concepts/, tools/, wiki/qa/), check whether it appears in INDEX.md.

Read every article file identified in the on-disk set. Parse all `[[WikiLink]]` occurrences in each file. Resolve each link against the set of known slugs in INDEX.md. Record links that resolve to no known file.

After reading all article files, build a backlink map: for each article, count how many other articles link to it. Articles with zero backlinks are orphans.

Collect issues:

- **Critical** — file in INDEX.md but not on disk; file on disk but not in INDEX.md; `[[WikiLink]]` target does not exist.
- **Warning** — article with zero backlinks (orphan).

## Step 4: Content checks

Read every article file identified in Step 2. For each:

- Count words. Articles under 100 words are stubs.
- Check whether a `## Sources` section (or `sources:` frontmatter) is present. Articles with no sources listed are flagged.

Read every entry in `raw/INDEX.md`. For each raw slug, check whether any wiki article's frontmatter or body references that raw slug. Raw docs with no matching wiki article are "uncompiled."

Scan all article bodies for concept or tool names. Flag pairs of articles where the titles or opening paragraphs are near-synonymous (same concept under different names). Treat this as a potential duplicate.

Collect issues:

- **Warning** — stub article; article with no sources; uncompiled raw doc; potential duplicate pair.

## Step 5: Coverage gap analysis

Aggregate all `[[WikiLink]]` targets across every article. For each link target that appears in 3 or more articles but has no corresponding wiki article, flag it as a coverage gap candidate.

Scan article bodies for tool and framework names (anything that reads like a proper noun product name). For each name that does not have a `wiki/tools/<slug>.md` file, flag it as an unprofiled tool.

Cross-reference `raw/INDEX.md` entries against `wiki/INDEX.md`. Any raw slug that is not referenced by any wiki article and was not already flagged as a Warning in Step 4 is a coverage opportunity.

Collect findings:

- **Opportunity** — coverage gap (topic mentioned 3+ times, no article); unprofiled tool; raw doc with no wiki article.

## Step 6: Opportunity synthesis

Read the full text of every wiki article (already loaded in Step 4). Identify pairs or clusters of articles that share common terminology, cite overlapping concepts, or approach the same problem from different angles but are not linked to each other. Suggest specific new `[[WikiLink]]` additions.

From the gaps and orphans found in previous steps, propose concrete research directions: what would a well-rounded wiki on this topic need that is currently absent?

Scan for questions that multiple articles partially address but none fully answers. List these as "almost-answered questions."

Collect findings:

- **Opportunity** — suggested cross-links (article A → article B, reason); research directions; almost-answered questions.

## Step 7: Write wiki/LINT.md

Write all findings to `/Users/cecil/Code/me/wiki-workflow/wiki/LINT.md`, overwriting any previous run. Use this exact structure:

```
---
generated: <YYYY-MM-DD>
critical: <count>
warnings: <count>
opportunities: <count>
---
# Wiki Lint Report — <YYYY-MM-DD>

## Critical

> Fix these before the wiki is trustworthy.

- [MISSING FILE] `wiki/INDEX.md` lists `concepts/foo.md` but file does not exist.
- [NOT INDEXED] `wiki/tools/bar.md` exists on disk but is not in `wiki/INDEX.md`.
- [BROKEN LINK] `concepts/baz.md` links to `[[qux]]` — no matching article found.

## Warnings

> These degrade quality but are not blocking.

- [ORPHAN] `concepts/foo.md` — no other article links to it.
- [STUB] `tools/bar.md` — 47 words (under 100).
- [NO SOURCES] `concepts/baz.md` — no sources section.
- [UNCOMPILED] `raw/some-article.md` — no wiki article references this raw doc.
- [DUPLICATE?] `concepts/llm-fine-tuning.md` and `concepts/fine-tuning-llms.md` may cover the same topic.

## Opportunities

> Growth and improvement possibilities.

### Coverage Gaps
- `[[streaming]]` mentioned in 4 articles — no dedicated article exists.
- Tool `vLLM` mentioned in 3 articles — no tool profile in `wiki/tools/`.

### Suggested Links
- `concepts/rag.md` → `[[vector-databases]]` — both discuss embedding lookup; not currently linked.

### Research Directions
- The wiki covers RAG architecture but has no material on evaluation or benchmarking RAG quality.

### Almost-Answered Questions
- "How does quantization affect inference latency?" — partially addressed in `concepts/quantization.md` and `tools/llama-cpp.md` but never synthesized.
```

If there are no findings in a section, write `_None found._` under that heading. Do not omit sections.

## Step 8: Auto-repair (--fix only)

Only execute this step if `--fix` was passed.

### Repair Critical issues

For each **MISSING FILE** issue: create a minimal stub article at the path INDEX.md expects, with a frontmatter block (title, date, tags: []) and a single-sentence body: `_Stub — article content not yet written._`

For each **NOT INDEXED** issue: append the missing entry to `wiki/INDEX.md` under the appropriate section (Concepts or Tools), using the article's frontmatter title.

For each **BROKEN LINK** issue: do not remove the link. Instead, create a stub article for the missing target slug at `wiki/concepts/<slug>.md` so the link resolves. Use the same minimal stub format as above.

### Write stubs for Opportunities

For each **Coverage Gap** and **Unprofiled Tool**: use WebSearch to find 2-3 authoritative sources. Use WebFetch to read them. Write a real (not placeholder) stub article of at least 150 words to the appropriate path (`wiki/concepts/<slug>.md` or `wiki/tools/<slug>.md`). Include a `## Sources` section. Add the new article to `wiki/INDEX.md`.

Do not attempt to auto-repair Warnings (orphans, stubs, duplicates) — these require human judgment.

## Output

After writing LINT.md (and running repairs if --fix), report:

```
wiki:lint complete.
  Critical:      N issues (N repaired if --fix)
  Warnings:      N
  Opportunities: N
  Report:        wiki/LINT.md
```

If any file read or write fails, note the failure in the report and continue — do not abort the full run for a single file error.
