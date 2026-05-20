---
description: >
  Generates experimental filter variants, runs the digest filter eval against each, and produces a
  comparison table (Precision/Recall/F1 vs baseline). Use when you want to test changes to goal.md
  signals or filter prompt criteria and see which performs best against the labelled dataset.
argument-hint: "[axes-to-explore]"
effort: high
---
# eval-variants

Generate N experimental variants of the digest filter, append them to `evals/digest/variants.yaml`,
run the eval for each, and emit a comparison table against the v1 baseline.

## Step 1 — Read context

Read both files before doing anything else:

- `evals/digest/variants.yaml` — to understand all existing variants and the v1 baseline
- `projects/data-ai-engineering/goal.md` — to understand current goal signals

Identify the highest existing variant number by scanning `name:` fields (e.g. `v1`, `v2`). New
variants continue the sequence from there.

## Step 2 — Determine axes to explore

If the user supplied arguments, treat them as the axes to explore and skip asking.

Otherwise ask:

> What should I vary?
> 1. Goal signals (broaden or tighten high/low-relevance signals in goal_inline)
> 2. Filter criteria (adjust auto-ticket threshold or drop rules in prompt_inline)
> 3. Both
> 4. Surprise me (I'll pick sensible defaults)

If the user picks "surprise me" or gives no guidance, use these five default axes (one per variant):

- **Broaden high-relevance signals** — add data engineering + AI pipeline content as explicit
  high-relevance signals alongside the existing coding/testing angle
- **Tighten auto-ticket threshold** — require both title AND snippet to independently match a
  high-relevance signal (not just title); update prompt_inline's auto-ticket criteria accordingly
- **Soften low-relevance: research papers** — allow research papers if the snippet mentions
  near-term applicability to coding or testing workflows; update goal_inline's low-relevance list
- **Reframe goal around applied AI at work** — shift goal_inline's reading intent from "ship faster"
  to "applied AI at work": using LLMs inside data pipelines, agent tooling, and production AI systems
- **Relax threshold-vs-drop boundary** — keep more borderline content for user review by loosening
  the drop criteria in prompt_inline; opinion pieces with one concrete technique move to threshold

Default variant count: 5 (one per axis). Adjust if the user specifies a different number.

## Step 3 — Generate variants

For each variant, produce a fully self-contained entry. Both `goal_inline` and `prompt_inline` must
be complete — copy from v1 and apply only the targeted change. Do not reference other variants or
external files.

Name variants sequentially: if the highest existing name is `vN`, use `v(N+1)`, `v(N+2)`, etc.

Each variant block must have:

```yaml
  - name: <vN>
    description: "<one-line summary of what changed>"
    created_at: "<YYYY-MM-DD>"
    goal_inline: |
      <full goal.md text>
    prompt_inline: |
      <full filter prompt text>
```

`model` and `notes` are optional — omit unless there is a specific reason to set them.

## Step 4 — Append to variants.yaml

NEVER rewrite `variants.yaml` from scratch. Append only the new variant blocks.

Insert the new blocks immediately before the final comment line
(`# Add new variants below…`) if it exists, or at the end of the `variants:` list.

Use 2-space indentation throughout. Use YAML block scalars (`|`) for `goal_inline` and
`prompt_inline`. Preserve the existing file exactly as-is above the insertion point.

After appending, confirm: "Appended variants <list of names> to variants.yaml."

## Step 5 — Run evals sequentially

For each new variant, in order:

1. Print: `Running eval for <name>…`
2. Run: `just eval-filter --variant <name>`
3. Wait for it to complete before starting the next variant.

Do not run variants in parallel — sequential execution avoids file contention in the runs directory.

If a run fails, print the error, note which variant failed, and continue with the remaining variants.

## Step 6 — Parse results and emit comparison table

After all runs complete, find the latest report for each variant (including v1 for baseline) in
`evals/digest/runs/`. Report filenames follow the pattern `<date>-<commit>-<name>.md`. When
multiple reports exist for the same variant name, use the most recent (lexicographically last).

From each report, extract the three metric rows:

```
| Precision | x.xxx |
| Recall    | x.xxx |
| F1        | x.xxx |
```

Read only as many lines as needed to find these rows — they appear in a summary table near the top
or bottom of the report.

If a report is missing or a metric cannot be parsed, show `—` in that cell.

Compute ΔF1 = variant F1 − v1 F1. Format as `+0.xxx` or `-0.xxx`. Show `—` if either value is
missing.

Emit the comparison table:

```
| Variant | Description | Precision | Recall | F1 | ΔF1 vs v1 |
|---------|-------------|-----------|--------|----|-----------|
| v1      | Baseline …  | x.xxx     | x.xxx  | x.xxx | —      |
| v2      | …           | x.xxx     | x.xxx  | x.xxx | +0.xxx |
…
```

Sort rows: v1 first, then new variants in name order.

## Step 7 — Prune unwanted variants

After presenting the table, ask:

> Which variants do you want to keep? List names to keep (e.g. "v1 v3 v5"), or say "all" to keep
> everything. Variants not listed will be removed from variants.yaml.

Wait for the response. Then:

- **Never remove v1** regardless of what the user says. If they try to drop v1, warn them and skip
  it.
- For each variant the user wants removed, delete its entire block from `variants.yaml` (from the
  `  - name: <vN>` line through the last field of that entry, inclusive of any trailing blank line
  before the next entry).
- Do not touch any other content in the file.
- Confirm: "Removed variants <list>. Kept: <list>."

## Constraints

- NEVER rewrite `variants.yaml` from scratch — append and targeted-delete only
- Always keep v1 — never offer or allow deletion of the baseline
- Use 2-space indentation and block scalars (`|`) when writing YAML
- Run evals sequentially — no parallelism
- Do not fetch article content or call Linear — this skill is eval-only
