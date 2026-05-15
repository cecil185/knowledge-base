# knowledge-base

Personal learning system. Discovers, filters, and synthesizes tech articles into a queryable knowledge base — with Linear for tracking and a local wiki for synthesis.

## Entry points

| Command | What it does |
|---------|-------------|
| `/digest [slug]` | Full pipeline: discover → filter → ticket → read → compile wiki |
| `/add-article <url>` | Manually add one article: ticket → read → compile wiki |
| `/article-critique <url>` | Score an article; ticket + read if score ≥ 7 |
| `/wiki:ingest <url\|topic>` | Save a URL or topic to `raw/` without ticketing |
| `/wiki:compile` | Synthesize `raw/` into `wiki/` (safe to re-run) |
| `/wiki:qa <question>` | Query the compiled wiki |
| `/wiki:lint [--fix]` | Audit wiki for broken links, stubs, gaps |
| `/wiki:purge` | Delete raw files for tickets labelled `delete-from-wiki` in Done; marks tickets Cancelled |
| `/goal-refine` | Create or update the active project's `goal.md` |
| `/refine-sources` | Prune or add sources to the active project's `sources.md` |

## `/digest` pipeline

```
digest
  └── search-articles          discovers candidates from HN + sources.md
  └── filter-articles          classifies into drop / auto-ticket / threshold
  └── create-tickets           deduplicates against Linear, creates tickets
        ├── check-duplicate    (per article)
        └── create-ticket      (per approved article)
        └── read-article agents (parallel, one per ticket)
              └── save-article-raw
  └── wiki:compile             synthesizes all raw/ docs into wiki/
```

## Configuration

| File | Purpose | Managed by |
|------|---------|------------|
| `projects/<slug>/goal.md` | Learning goal; drives all filtering | `/goal-refine` |
| `projects/<slug>/sources.md` | Supplemental blog sources (HN always included) | `/refine-sources` |

## Directory structure

```
projects/
  <slug>/
    goal.md
    sources.md
    raw/       ← AI-analyzed article summaries (linked to Linear tickets by URL)
    wiki/
      concepts/
      tools/
      qa/
      SUMMARY.md
      LINT.md
```