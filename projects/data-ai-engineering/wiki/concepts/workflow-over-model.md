---
title: Workflow Over Model
updated: 2026-05-15
sources: [raw/developers-digest-hn-ai-coding-agents-2026.md, raw/simon-willison-scaling-autonomous-coding.md, raw/openai-symphony-codex-orchestration-spec-part-1.md]
related: [agentic-coding, harness-engineering, multi-agent-orchestration, hierarchical-agent-systems, parallel-agent-deployment, issue-tracker-as-control-plane, skills-and-reusable-instructions, repo-local-agent-instructions]
---
## Summary
The thesis that the real product is the workflow — orchestration, repo conventions, specialized agents, reviewability — not the underlying model. Model improvements are commoditized quickly; the durable advantage is the workflow that composes them.

## Details
The 2026 consensus on Hacker News and across practitioner write-ups is captured in one line: "autonomy is overrated as branding; orchestration is underrated as production pattern." Teams that swap models monthly still win or lose on the surrounding workflow.

### Terminal-native agents that compose
The dominant pattern is agents that live in the terminal and compose with the existing developer toolkit — shell, git, browsers, gh CLI, the file system. This is the opposite of bespoke IDE integrations. Composability with Unix-style tools is what lets a single workflow scale from one developer to a swarm of agents.

### Specialized agents per role
Rather than one generalist agent, production setups assign agents to roles:
- **Research** — read the repo, surface relevant files and prior decisions
- **Modification** — write the code under tight constraints
- **Verification** — run tests, lint, security checks
- **Synthesis** — produce summaries, PR descriptions, runbooks

Each role gets its own harness, prompts, and tool access. See [[Multi-Agent Orchestration]] and [[Hierarchical Agent Systems]].

### Reviewability as a design target
Workflows are optimized so that diffs are small, tests are explicit, and the reviewer can verify quickly. This pushes against the temptation of letting an agent ship a 2000-line PR. It also pushes toward [[Iterative Chunking]] — many small, reviewable units rather than one large unverifiable one.

### Issue tracker as the workflow primitive
Symphony's pattern: Linear tickets are the unit of work; agents pick them up, write status back, and file their own follow-ups. The tracker is the control plane; agents are workers. This is workflow-as-product taken to its logical conclusion — Symphony reportedly drove a **500% increase in landed PRs in three weeks** in some OpenAI teams. See [[Issue Tracker as Control Plane]].

### Why model-swapping is cheap
Once the workflow is right, swapping Claude Opus 4.5 for GPT 5.1 or Codex is a config change. The CLAUDE.md/AGENTS.md, the test suite, the dispatch layer, the review gates — all persist. Teams that obsessed over picking the "best" model in 2024 spent 2026 obsessing over [[Skills and Reusable Instructions]] and [[Repo-Local Agent Instructions]].

## Tradeoffs / When to use
Gains: durable infrastructure as models churn; clearer failure modes (workflow vs. model); easier onboarding of new agents and new humans; reviewability that scales.
Costs: workflows need maintenance like code; over-engineered orchestration adds friction for simple tasks; specialization can fragment what a single capable model could handle end-to-end.
Fits well: teams shipping continuously with agents, multi-agent setups, anywhere model choice is volatile. Fits poorly: experimental work where a single chat session is faster than spinning up a workflow.

## Key tools / implementations
- [[Symphony]] — workflow product built on top of [[OpenAI Codex]]
- [[Claude Code]] — terminal-native agent designed to be composed
- [[Linear]] — issue tracker that functions as the orchestration substrate
- [[MCP]] — protocol that makes tool composition portable across models

## Sources
- [[raw/developers-digest-hn-ai-coding-agents-2026]] — "workflow over model" thesis; orchestration vs. autonomy; specialized agents per role
- [[raw/simon-willison-scaling-autonomous-coding]] — hierarchical agent systems; concurrent emergence of similar workflows
- [[raw/openai-symphony-codex-orchestration-spec-part-1]] — tracker-as-control-plane pattern; 500% PR throughput increase

## Backlinks
- [[Agentic Coding]]
- [[Multi-Agent Orchestration]]
- [[Skills And Reusable Instructions]]
