---
name: filter-articles
description: >
  Classifies a list of candidate articles into drop/auto-ticket/threshold buckets using
  goal.md signals. Second step of /digest; called after search-articles returns candidates.
when_to_use: >
  Trigger when a list of candidate articles needs classification against the active project's
  goal. Called internally by digest after search-articles; not typically invoked directly.
model: claude-opus-4-6
effort: medium
---
# filter-articles

Classifies a list of candidate articles into three buckets using only title, source, and snippet — no full article fetching. Classification is driven entirely by the signals in the active project's `goal.md`.

**Example:** Given 20 candidates from search-articles, classifies 3 as auto-ticket (concrete tool releases matching goal signals), 5 as threshold (plausible but thin snippets), and 12 as drop (opinion roundups, vendor marketing).

## Active project

Use the `PROJECT_DIR` established by the calling skill (digest). If called directly, determine the active project by reading `CLAUDE.md` and using the **Default project** slug. Set `PROJECT_DIR = projects/<slug>`.

## Precondition

Read `<PROJECT_DIR>/goal.md` before doing anything else.

If the file does not exist, stop immediately and tell the user:

> `<PROJECT_DIR>/goal.md` is missing. Run `/goal-refine` first to define your learning goal, then re-run `/digest`.

The **High-relevance article signals** and **Low-relevance article signals** sections of `goal.md` are the primary classification inputs. The **Reading intent** section provides additional context on what the user wants to get out of articles.

## Buckets

Classify each article into exactly one of:

### drop

Discard without creating a ticket. Use when any of the following apply:
- URL host matches a domain in the **Blocklist** section of `<PROJECT_DIR>/sources.md` (case-insensitive, ignore `www.`, match exact or subdomain)
- Vendor SEO/marketing post: "Complete Guide to…", "How to QA…", "The Ultimate…" style titles from a vendor's own blog
- Title or snippet clearly falls outside the goal's high-relevance signals
- Matches one or more low-relevance signals from `goal.md`
- Opinion piece, trend roundup, or "state of X" without concrete technical content
- Tutorial covering basic/introductory material
- Likely paywalled (e.g. Bloomberg, WSJ, FT, Harvard Business Review)

### auto-ticket

Create a Linear ticket automatically without asking the user. Use when **all** of the following are true:
- Title + snippet directly and unambiguously matches at least one high-relevance signal
- Describes a concrete tool release, benchmark, technique, architecture, or case study — not just commentary about it
- Nothing in the snippet suggests low relevance, opinion-only, or introductory content
- A trusted source (from `sources.md` or a well-known engineering blog) is a positive signal but not required

Err on the side of `threshold` when uncertain. False positives here cost the user time.

### threshold

Show to the user with a short summary; create a ticket only if approved. Use when:
- The title or source suggests plausible relevance but the snippet is too thin to confirm
- The article topic overlaps with the goal but it is unclear whether the depth or angle matches
- The source is unfamiliar and quality cannot be inferred from the snippet

## Classification rules

- **Be strict.** A false positive (auto-ticketing something irrelevant) costs more than a false negative (missing something good).
- Every article gets exactly one bucket. No "maybe drop / maybe threshold" hedging.
- Do not fetch article content. Classification uses only what `search-articles` provided: title, source, snippet, date.
- Do not re-order the user's candidate list within a bucket — preserve the order they arrived in.

## Output format

Emit three sections in this order: **auto-ticket**, **threshold**, **drop**.

### Auto-ticket

```
## Auto-ticket (<count>)

- **<title>**
  URL: <url>
  Reason: <one clause explaining which high-relevance signal it matches>
```

### Threshold

```
## Threshold (<count>)

- **<title>**
  URL: <url>
  Reason: <one clause explaining the uncertainty>
  Summary: <1-2 sentences distilling what the article appears to be about, so the user can decide without fetching it>
```

### Drop

```
## Drop (<count>)

- **<title>** — <one clause reason>
```

Drop entries are compact because the user does not need to act on them. Auto-ticket and threshold entries include the URL so downstream steps can use the output directly.
