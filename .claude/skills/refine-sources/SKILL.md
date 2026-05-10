---
name: refine-sources
description: Review and update the blog/site sources list in sources.md. Prune dead or off-goal sources, add new ones. HN is always a source and is never listed here.
model: claude-opus-4-6
effort: low
---
# Refine Sources

Review the list of supplemental sources that `/digest` searches beyond Hacker News. Keep the list tight and goal-aligned — a bloated source list produces noise, not signal.

HN is always searched. It is never in `sources.md`. This skill only manages the supplemental list.

## Steps

### 1. Read ./sources.md

Read `./sources.md` from the repo root.

- **File missing or empty** → Create it with the following starting sources and continue to step 2:

  | Source | URL | Topic focus | Last active |
  |--------|-----|-------------|-------------|
  | Simon Willison | simonwillison.net | LLMs, tools, AI engineering | active |
  | Databricks Blog | databricks.com/blog | Data + AI platform, Spark, MLflow | active |
  | Confluent Blog | confluent.io/blog | Kafka, streaming, data pipelines | active |

- **File exists** → Use the existing list.

### 2. Read ./goal.md

Read `./goal.md`. Extract the What, Why, and high/low-relevance signals. This is the filter for every judgment below.

### 3. Show the current list

Print the full sources table to the user. Do not editorialize yet — just show it and say "Let's go through these."

### 4. Review each source

For each source, make a recommendation (keep / drop / uncertain) and give one reason grounded in goal alignment. Then ask the user to confirm.

Recommend **drop** if any of these are true:
- The source's topic focus matches the low-relevance signals in goal.md.
- The source publishes primarily marketing copy, announcements, or vendor case studies with no technical depth.
- The user hasn't found a useful article from it in recent sessions (if that context is available).

Recommend **keep** if:
- The topic focus directly matches one or more high-relevance signals.
- The source has a track record of novel, specific content (not just aggregation).

Do not ask the user open-ended questions per source. Make a recommendation, state the reason in one sentence, and ask "Keep or drop?"

### 5. Ask about new sources

After reviewing the existing list, ask: "Any new sources to add?"

If the user names a source, ask for the URL and topic focus if not already provided. Add it to the proposed list without further ceremony.

### 6. Show final proposed list and confirm

Display the full updated table in a code block. Ask: "Write this to sources.md? (yes / revise [what])"

- If yes: write the file.
- If revise: incorporate the change, show the updated table, confirm once more.

Do not write the file without explicit confirmation.

### 7. Write ./sources.md

Write using exactly this format:

```markdown
# Digest Sources

_Last reviewed: YYYY-MM-DD._

HN is always searched. These are additional sources:

| Source | URL | Topic focus | Last active |
|--------|-----|-------------|-------------|
| <name> | <url> | <topic focus> | <active or YYYY-MM-DD last seen> |
```

Use today's date for `Last reviewed`. Do not add commentary or sections beyond the table.

## Tone

Be opinionated. A source that isn't earning its place should be dropped. The default is lean — fewer, better sources beat a long list of noise.
