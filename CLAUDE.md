Personal learning system. Discovers, filters, and synthesizes tech articles into a queryable knowledge base — with Linear for tracking and a local wiki for synthesis.
**Before proposing features, refactors, or scope changes, read [PURPOSE.md](./PURPOSE.md).** It defines what this project is for (agentic goal-aware content pipeline + AI engineering portfolio) and explicitly what to avoid (slick UI, generic RAG, building for other users).

## Linear

Team key: **CC** — [Knowledge Base](https://linear.app/cecils-projects/team/CC/)

- **Work project** — tickets to build and improve this system itself
- Each learning project has a dedicated **Wiki project** in Linear (see Projects section)

Article ticket tags: `human-not-read`, `human-read`

## Projects

Skills that need the active project read this table to resolve the slug → Linear project name mapping. When a skill says "Default project", use the row marked ✓.

| Slug | Name | Linear Project | Default |
|------|------|----------------|---------|
| `data-ai-engineering` | Data AI Engineering | Data AI Engineering | ✓ |
| `applied-ai` | Applied AI | Applied AI | |

> **Note:** `Linear Project` must match the project's exact display name in Linear (team CC). Update this table if a project is renamed.

## Data model

**Article URL is the identity key** across all stores:
- `raw/<slug>.md` — frontmatter `url:` field holds the canonical URL
- Linear ticket — URL appears as the first line of the ticket description
- `check-duplicate` uses URL (normalised: no trailing slash, no `utm_*` params, scheme-agnostic) to detect duplicates across both stores

Raw files and their Linear tickets are linked solely by matching URL — there is no other ID.

## Directory structure

```
knowledge-base/
  projects/
    data-ai-engineering/
      goal.md          — learning goal (managed by /goal-refine)
      sources.md       — blog sources list (managed by /refine-sources)
      raw/             — AI-analyzed article summaries with frontmatter metadata (one .md per article)
      wiki/            — compiled knowledge base (concepts, tools, synthesis)
    applied-ai/
      goal.md
      sources.md
      raw/
      wiki/
  scripts/             — utility shell scripts
  .claude/             — Claude Code settings (skills live here)
```

## Skills

```
/digest            — end-to-end: discover → filter → ticket → read → summarize → wiki
/goal-refine       — create or refine the active project's goal.md
/refine-sources    — review and update the active project's blog sources list
/article-critique  — on-demand deep review of a single article
/wiki:ingest       — save a URL or topic to the active project's raw/
/wiki:qa           — query the active project's knowledge base
/wiki:compile      — synthesize raw/ docs into wiki/ concepts and tool articles
/wiki:lint         — audit wiki for gaps and broken links
/wiki:purge        — delete raw files for tickets labelled delete-from-wiki (Done → Cancelled)
```

## /digest flow

1. Determine active project (from arg or default in CLAUDE.md)
2. Read `projects/<slug>/goal.md` and `projects/<slug>/sources.md`
3. Fetch candidates from Hacker News + sources list
4. Filter into 3 buckets:
   - **Drop** — low quality or low relevance to goal
   - **Auto-ticket** — clear match; Linear ticket created automatically
   - **Threshold** — 1–2 sentence summary shown to Cecil; ticket created if approved
5. Deduplicate: skip any URL already in the project's Linear project
6. For each new ticket: read article in full → comment with TLDR / Goal relation / How to apply
7. Tags: `human-not-read` set at creation
8. `wiki:ingest` saves article to `projects/<slug>/raw/<slug>.md` and appends to `projects/<slug>/raw/INDEX.md`; `wiki:compile` synthesizes into `projects/<slug>/wiki/`

## Goal

Each project's `goal.md` has four fields: **What**, **Why**, **Horizon**, **Success looks like** — plus derived reading intent and relevance signals. Run `/goal-refine` to update the active project's goal.

## Sources

Each project's `sources.md` lists blog sources beyond HN. HN is always included. Run `/refine-sources` to prune or add sources for the active project.
