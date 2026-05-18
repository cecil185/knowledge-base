# Skill Dependencies

## Dependency Tree

```
digest
├── search-articles        (digest-only)
├── filter-articles        (digest-only)
└── bulk-ingest-articles         (digest-only)
    ├── check-duplicate
    ├── create-ticket
    └── read-article
        └── save-article-raw

add-article
├── check-duplicate
├── create-ticket
└── read-article
    └── save-article-raw

wiki-ingest
├── check-duplicate
└── save-article-raw
```

### Shared primitives

Called by more than one parent — not nested under any single skill:

| Skill | Called by |
|---|---|
| `check-duplicate` | `bulk-ingest-articles`, `wiki-ingest`, `add-article` |
| `create-ticket` | `bulk-ingest-articles`, `add-article` |
| `read-article` | `bulk-ingest-articles`, `add-article`, `article-critique` |
| `save-article-raw` | `read-article`, `wiki-ingest` |

---

## Standalone Skills

User-facing entry points with no parent skill:

| Skill | Purpose |
|---|---|
| `goal-refine` | Create or update `goal.md` for the active project |
| `refine-sources` | Review and update `sources.md` for the active project |
| `wiki-compile` | Synthesize `raw/` docs into `wiki/` concept and tool articles |
| `wiki-lint` | Audit wiki for gaps and broken links |
| `wiki-purge` | Delete raw files for tickets labelled `delete-from-wiki` |
| `wiki-qa` | Query the active project's knowledge base |
