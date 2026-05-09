# wiki-workflow

Personal learning system. Captures, evaluates, and synthesizes tech articles across sessions.

## Linear

This project uses **Linear** for issue tracking. Issues are in the [Tech Digest](https://linear.app/cecils-projects/team/CCTD/) team (team key: CCTD).

Use Linear project 'Work' for tickets to create this system.
Use Linear project 'Wiki' for high-value articles.

## Purpose

Filter the tech firehose. Every article evaluated gets logged. Patterns surface over time. High-value finds become action.

## Structure

```
skills/
  article-critique/   — rates and summarizes a tech article; appends to learning log
  tech-digest/        — finds new articles from HN + curated blogs; dedupes against log; posts to Slack
```

## Learning Log

All evaluated articles are stored in `~/.claude/learning/log.md` — one line per article with date, rating, and action status. This is the cross-session memory store. Skills read it to avoid re-evaluating seen articles.

## Workflow

- `/article-critique <url>` — evaluate a specific article
- `/tech-digest` — pull latest articles, skip already-seen ones, post digest to Slack

## Notes

- Skills live here; `~/.claude/settings.json` includes this repo in `additionalDirectories` so they're available globally
- Learning log lives in `~/.claude/learning/log.md` (outside this repo, persists independently)
