# Learnings

## 2026-05-20 — Hard category rules in goal.md cause false negatives

Softening one low-relevance bullet (+0.164 F1, 6→9 TP) showed that rules firing on category before reading evidence are precision landmines. The model was dropping articles that had practical signals in their snippets.

**Before:** `- Research papers on model internals with no near-term application to coding workflows`
**After:** `- Research papers on model internals — unless the snippet explicitly mentions near-term applicability to coding, testing, or data engineering workflows`

Write low-relevance signals as rebuttable presumptions, not hard drops.
