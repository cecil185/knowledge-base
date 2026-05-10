---
name: wiki:compile
description: Process new raw/ docs and update wiki/ — synthesizes concepts and tools into evergreen articles with WikiLink cross-references
model: claude-opus-4-6
effort: high
---
# wiki:compile

Synthesize all raw docs into the wiki knowledge base. Called at the end of `/digest` and on-demand. Safe to re-run — existing articles are extended, not replaced.

## Active project

Determine the active project by reading `CLAUDE.md` from the repo root. Find the **Default project** slug in the `## Projects` section. Set `PROJECT_DIR = projects/<slug>`. All file paths below are relative to `/Users/cecil/Code/me/knowledge-base/<PROJECT_DIR>`.

If called with a project argument (e.g. `/wiki:compile --project applied-ai`), use that slug instead.

## Step 1: Load raw docs

List all `.md` files under `<PROJECT_DIR>/raw/`. If none exist, report "no raw docs found" and stop.

## Step 2: Extract structured knowledge from each raw doc

For each uncompiled raw doc, read the file and extract:

- **Core concepts** — abstract ideas, patterns, or principles the article explains (e.g. "vector indexing", "backpressure", "eventual consistency")
- **Tools and frameworks** — named software, libraries, services, or systems discussed (e.g. "Apache Kafka", "LangChain", "DuckDB")
- **Key tradeoffs** — what the approach costs vs. what it gains; when it fits and when it does not
- **Actionable patterns** — concrete techniques, configurations, or architectures that can be applied

Produce a structured internal note per raw doc. Do not write this to disk — carry it forward to the next steps.

## Step 3: Create or update concept articles

For each distinct concept identified across all new raw docs:

Generate a slug: lowercase, hyphen-separated, max 60 characters.

Check whether `<PROJECT_DIR>/wiki/concepts/<slug>.md` already exists.

**If it does not exist**, create it:

```
---
title: <Concept Name>
updated: <YYYY-MM-DD>
sources: [raw/<slug>.md, ...]
related: []
---
## Summary
2–3 sentences. Precise and scannable — no padding.

## Details
Thorough explanation synthesized across all sources covering this concept. Use subheadings for complex topics. Include concrete examples where they clarify.

## Tradeoffs / When to use
What this approach gains, what it costs, and the conditions under which it fits well or poorly.

## Key tools / implementations
Named tools, libraries, or systems that implement or relate to this concept. Use [[WikiLink]] syntax for any tool that has or should have a wiki/tools/ article.

## Sources
- [[raw/<slug>]] — <one-line description of what that source contributed>
```

**If it already exists**, extend it — do not replace existing content:
- Add new sources to the `sources` frontmatter list (deduplicate)
- Update `updated` to today's date
- Append new information to the relevant sections under clearly marked subheadings or inline where it fits
- Add newly identified related concepts to the `related` frontmatter list
- Never remove or rewrite existing content unless it is factually incorrect — in that case, add a correction note inline

## Step 4: Create or update tool articles

For each distinct tool or framework identified across all new raw docs:

Generate a slug from the tool name: lowercase, hyphen-separated, max 60 characters.

Check whether `<PROJECT_DIR>/wiki/tools/<slug>.md` already exists.

**If it does not exist**, create it:

```
---
title: <Tool Name>
updated: <YYYY-MM-DD>
sources: [raw/<slug>.md, ...]
related: []
---
## Purpose
One sentence. What problem does this tool solve and for whom.

## How it works
Mechanism and architecture at the level of detail needed to reason about it.

## Strengths
Bulleted list. Concrete advantages backed by the sources.

## Weaknesses
Bulleted list. Known limitations, operational costs, failure modes.

## Alternatives
Other tools in the same space. Use [[WikiLink]] for any that have wiki articles.

## Sources
- [[raw/<slug>]] — <one-line description of what that source contributed>
```

**If it already exists**, extend it using the same rules as concept articles above.

## Step 5: Add WikiLink cross-references

After writing all new and updated articles:

- Within each article, link concept names and tool names to their wiki articles using `[[Title]]` syntax where they are mentioned.
- At the bottom of each article (after Sources), add a `## Backlinks` section listing other wiki articles that reference this one. Derive backlinks by scanning all wiki files for mentions of this article's title or slug.
- Update the `related` frontmatter list on each article to include slugs of closely related articles discovered during this compile run.

## Step 6: Update wiki/INDEX.md

Rewrite `<PROJECT_DIR>/wiki/INDEX.md` with two sections: `## Concepts` and `## Tools`. Each entry:

```
- [[Title]] — <one-line hook: what it is and why it matters>
```

Sort each section alphabetically by title. Include all articles in `<PROJECT_DIR>/wiki/concepts/` and `<PROJECT_DIR>/wiki/tools/`, not just the ones updated in this run. Create the file if it does not exist.

## Step 7: Update wiki/SUMMARY.md

Rewrite `<PROJECT_DIR>/wiki/SUMMARY.md` with:

```
# Wiki Summary
Updated: <YYYY-MM-DD>

**Articles:** <total concept count> concepts, <total tool count> tools

## Most-referenced concepts
List the 5 concepts that appear most frequently in the `sources` lists of other wiki articles or are linked via WikiLink most often.

## Suggested next research directions
3–5 directions as bullet points, inferred from gaps in the wiki — concepts mentioned but not yet having their own article, tools referenced without detail, or themes recurrent across sources that lack synthesis.
```

Create the file if it does not exist.

## Output

Report:
- N concept articles created, N updated
- N tool articles created, N updated
- Gaps identified: concepts or tools referenced in sources but not yet having wiki articles
- Paths of all files written
