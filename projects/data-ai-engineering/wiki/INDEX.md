# Wiki Index

## Concepts

- [[Agentic Coding]] — the paradigm of delegating implementation to AI agents while humans direct, verify, and orchestrate
- [[AI-Attributed Defect Tracking]] — measuring regressions and incidents back to specific AI-generated changes (1.7x defect multiplier)
- [[AI-First Data Engineering]] — embedding AI capabilities (extract, classify, parse, query) directly inside ETL pipelines
- [[Code Comprehension Bottleneck]] — maintenance and understanding (~90% of lifecycle) dominate the cost of software, not generation
- [[Constraint-Driven Prompting]] — explicit rules and prohibitions yield more predictable agent output than open-ended instructions
- [[Cross-Model Review]] — using a secondary AI session to critique or chain-optimize the work of a first
- [[Database Branching]] — O(1) copy-on-write database branches as a first-class primitive for agentic and experimental workflows
- [[Guardrails for AI Coding]] — layered review/test/policy infrastructure (5 layers, 3 risk tiers) that keeps AI velocity safe
- [[Harness Engineering]] — designing structured environments where AI operates predictably ("structure in, structure out")
- [[Hierarchical Agent Systems]] — tiered planner → sub-planner → worker → judge architectures for autonomous coding at scale
- [[Intent-Based Testing]] — E2E tests authored as user intent (YAML / natural language) rather than DOM selectors
- [[Issue Tracker as Control Plane]] — using Linear (or any tracker) as the state machine for orchestrating coding agents
- [[Iterative Chunking]] — decomposing AI work into small focused tasks instead of monolithic prompts
- [[Multi-Agent Orchestration]] — layering specialized agents (writer, reviewer, tester, validator) for production-grade output
- [[Parallel Agent Deployment]] — running multiple coding agents simultaneously on different problems for throughput multiplication
- [[Refactoring Trap]] — when AI makes refactoring nearly free, the discipline to make good upfront architectural decisions erodes
- [[Repo-Local Agent Instructions]] — storing agent behavior rules in version-controlled repo files (CLAUDE.md, AGENTS.md, WORKFLOW.md)
- [[Risk-Tiered Review]] — classifying changes by blast radius (Low/Medium/High) and requiring proof commensurate with risk
- [[Self-Healing Tests]] — E2E tests that auto-recover from UI changes via cached locators plus AI element resolution
- [[Skills and Reusable Instructions]] — project-specific reusable instruction packages that outperform one-off prompting
- [[Spec-Driven Development]] — compiling a specification before any code is generated; spec as the durable orchestration artifact
- [[Verifiability Boundary]] — AI is a force multiplier where output is objectively verifiable; provides false confidence where it is not
- [[Verification Bottleneck]] — review and testing capacity, not generation speed, is the new constraint on shipping AI-assisted code
- [[Workflow Over Model]] — "the real product is the workflow, not the model"; orchestration beats raw model improvements

## Tools

- [[Claude Code]] — Anthropic's terminal-native AI coding CLI with CLAUDE.md rules and reusable Skills
- [[CodeRabbit]] — AI code review and validation platform; source of the 1.7x defect-multiplier research
- [[CodeScene]] — code health platform enforcing three AI-coding guardrails (quality, familiarity, human-test coverage)
- [[Databricks Lakebase]] — serverless Postgres-compatible database with O(1) copy-on-write branching for agentic workloads
- [[Databricks Lakeflow]] — unified data engineering platform with native AI functions (ai_extract, ai_classify, ai_query)
- [[Linear]] — issue tracker used as the agent orchestration control plane in [[Symphony]] and similar systems
- [[MCP (Model Context Protocol)]] — open protocol for connecting AI agents to external tools and data sources
- [[OpenAI Codex]] — OpenAI's autonomous coding agent with app-server JSON-RPC mode for programmatic orchestration
- [[Playwright]] — dominant open-source browser automation framework (Chromium/Firefox/WebKit) underlying modern E2E platforms
- [[Shiplight]] — AI-native E2E testing platform built around intent-based authoring and three-tier self-healing
- [[Symphony]] — OpenAI's open-source orchestration spec turning Codex agents into an issue-tracker-driven daemon
