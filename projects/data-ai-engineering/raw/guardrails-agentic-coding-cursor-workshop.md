# Guardrails for Agentic Coding (Rogier Muller)

**Source:** https://www.cursorworkshop.com/research/agentic-coding-governance-20260503-0501
**Read:** 2026-05-18

## Overview

Engineering teams standardizing Cursor need governance frameworks that maintain ownership, preserve context, and uphold code review quality without sacrificing agility.

## Fork Ownership Problem

Parallel agent execution isn't genuinely free parallelism. Untracked code forks consume sprint capacity before linting failures even surface.

The core issue: reviewers cannot intuitively absorb unstated intent. As connectors proliferate faster than responsibility maps expand, accountability becomes murky.

Westrum's generative culture framework applies inversely here -- signals appeared transparent while actual accountability remained unclear. The fundamental tension emerges when someone questions "why did the agent modify this file?" and the answer exists solely in chat history.

**Principle:** Transparent forks outperform opaque ones.

## Fork Control Moves

### Claude Permission Creep

Shared-laptop deployments reveal bash approval becoming automatic reflex. The issue typically isn't tool deficiency -- it's the absent operating agreement.

**Solution:** Establish `CLAUDE.md` supremacy clause at the top, documenting which hooks take precedence, which folders demand human review, and where temporary exemptions exist. Sessions stop improvising policy mid-execution because precedence is documented. This transforms review efficiency.

### Codex Replay Gaps

CLI-based workflows can merge approved changes where reviewers never examined transcripts.

The vulnerability: CLI convenience masks verification theater -- commands executed but reasoning didn't.

**Solution:** Mandate "replay sandwich" in `AGENTS.md` -- intent statement, command transcript, and diff summary preceding PR submission. This makes review reproducible without observing someone's terminal session.

### MCP Blast Radius

Connectors frequently touch data not identified on system diagrams.

The reason: Connectors default to capability demonstrations; least-privilege access requires explicit trust boundaries.

**Solution:** Create one "Connector card" markdown per MCP server documenting: permitted actions, prohibited actions, owner, and rollback procedures. Incidents decline because operators understand what "disabled" looks like.

### Recursive Handoff Blur

Chained agents generate summaries omitting child-owned paths.

The danger: delegation stacks collapse when summaries replace documented receipts -- classic information-degradation risk.

**Solution:** Every child process returns: touched paths, executed commands, and regression-guard test results. Parents stop confidently approving mystery diffs.

## Delegation Boundary Snapshot

Example rule file structure:

- Cursor: keep scopes explicit in `.mdc`; forbid undeclared MCP domains.
- Claude Code: cite `CLAUDE.md` precedence before expanding bash scope.
- Codex: ensure `AGENTS.md` carries replay-friendly verification notes for CLI runs.

## Reviewer Surface

| Gate | Question |
|------|----------|
| Receipt match | Does PR body list scopes + verification transcript? |
| Rules precedence | Which `.mdc`, `SKILL.md`, or `CLAUDE.md` governed behavior? |
| Connector truth | Which MCP servers fired, and were they expected? |
| Reviewer path | Can someone unfamiliar trace intent without chat replay? |

### Merge Checklist

- Scopes in PR body match folders in diff
- Primary-doc links were spot-checked after publishing edits
- MCP connectors mentioned (if any) list owners
- Verification command output is pasted or linked

## Boundary Conditions

Hard constraints remain human territory: threat modeling, customer commitments, and blast radius decisions cannot be automated.

## Key Principle

Agents function as signal amplifiers -- they magnify whatever clarity already exists in files, hooks, and scopes. Review processes anchor responsibility by verifying receipts match actions.
