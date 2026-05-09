Personal learning system. Discovers, filters, and synthesizes tech articles into a queryable knowledge base — with Linear for tracking and a local wiki for synthesis.

## Linear

Team key: **CC** — [Knowledge Base](https://linear.app/cecils-projects/team/CC/)

- **Wiki project** — one ticket per article worth reading; comments hold the AI summary
- **Work project** — tickets to build and improve this system itself

Article ticket tags: `ai-not-read`, `ai-read`, `human-not-read`, `human-read`

## Directory structure

```
knowledge-base/
  goal.md          — current learning goal (managed by /goal-refine)
  sources.md       — blog sources list (managed by /refine-sources)
  about-me.md      — personal context for relevance filtering
  raw/             — raw fetched article content (one .md per article)
  wiki/            — compiled knowledge base (concepts, tools, synthesis)
  skills/          — skill definitions (one subdirectory per skill)
  scripts/         — utility shell scripts
  .claude/         — Claude Code settings
```

Deduplication is handled by Linear (Wiki project) — no local log file.

All data lives inside this repo. Nothing is stored outside it.

## Skills

```
/digest            — end-to-end: discover → filter → ticket → read → summarize → wiki
/goal-refine       — create or refine goal.md through structured interview
/refine-sources    — review and update the blog sources list in sources.md
/article-critique  — on-demand deep review of a single article
/wiki:ingest       — save a URL or topic to raw/; deduplicates against raw/INDEX.md
/wiki:qa           — query the local knowledge base
/wiki:compile      — synthesize raw/ docs into wiki/ concepts and tool articles
/wiki:lint         — audit wiki for gaps and broken links
```

## /digest flow

1. Read `goal.md` and `sources.md`
2. Fetch candidates from Hacker News + sources list
3. Filter into 3 buckets:
   - **Drop** — low quality or low relevance to goal
   - **Auto-ticket** — clear match; Linear ticket created automatically
   - **Threshold** — 1–2 sentence summary shown to Cecil; ticket created if approved
4. Deduplicate: skip any URL already in Linear (Wiki project)
5. For each new ticket: read article in full → comment with TLDR / Goal relation / How to apply
6. Tags: `ai-not-read` → `ai-read` after full read; `human-not-read` set at creation
7. `wiki:ingest` saves article to `raw/<slug>.md` and appends to `raw/INDEX.md`; `wiki:compile` synthesizes into `wiki/`

## Goal

`goal.md` has four fields: **What**, **Why**, **Horizon**, **Success looks like** — plus derived reading intent and relevance signals. Run `/goal-refine` to update it.

## Sources

`sources.md` lists blog sources beyond HN. HN is always included. Run `/refine-sources` to prune or add sources.
