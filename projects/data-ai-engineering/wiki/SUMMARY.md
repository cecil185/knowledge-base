# Wiki Summary
Updated: 2026-05-15

**Articles:** 24 concepts, 11 tools

## Most-referenced concepts

1. **[[Verification Bottleneck]]** — the central reframe of 2026: code generation is solved, review and testing capacity is the new constraint. Referenced by nearly every concept article as the motivating problem behind guardrails, defect tracking, multi-agent orchestration, and hierarchical agents.
2. **[[Agentic Coding]]** — the overarching paradigm. Acts as the parent concept; most other concepts are tactics within it.
3. **[[Guardrails for AI Coding]]** — the layered defensive stack tying together [[Risk-Tiered Review]], [[AI-Attributed Defect Tracking]], and [[Multi-Agent Orchestration]] into a single operating posture.
4. **[[Workflow Over Model]]** — the thesis that the product is the workflow, not the model. Underwrites [[Skills and Reusable Instructions]], [[Repo-Local Agent Instructions]], [[Issue Tracker as Control Plane]], and [[Multi-Agent Orchestration]].
5. **[[Harness Engineering]]** — the "structure in, structure out" principle. Connects [[Constraint-Driven Prompting]], [[Repo-Local Agent Instructions]], [[Spec-Driven Development]], and the [[MCP (Model Context Protocol)]] tool integrations.

## Suggested next research directions

- **Concrete AI governance policy templates.** [[AI-Attributed Defect Tracking]] and [[Guardrails for AI Coding]] both call for formal governance (where AI is allowed, documentation requirements, escalation paths), but no source provides a usable template. Worth seeking a real organizational example.
- **Devbox / sandboxed-workspace patterns for agents.** Symphony's per-issue workspace isolation is referenced briefly but the broader pattern — disposable VMs, sandboxed shells, network egress controls — is underdocumented in the current sources. Highly relevant to Cecil's "safe sandboxes" goal.
- **Cost economics of agent swarms.** [[Hierarchical Agent Systems]] and [[Parallel Agent Deployment]] document throughput gains (1M lines, trillions of tokens) but the dollar cost per unit of shipped value is unaddressed. Important for justifying organizational adoption.
- **Comparative landscape of AI review tools.** Only [[CodeRabbit]] and [[CodeScene]] have dedicated articles, plus a passing mention of Propel. The category likely includes more players (Greptile, Snyk Code, Qodo, etc.) worth a side-by-side.
- **Beyond Claude Skills: skill-package interoperability.** [[Skills and Reusable Instructions]] focuses on Anthropic's implementation. Cursor rules, Cline workflows, Continue rules, and OpenAI's emerging skill format are gaps in current coverage.
- **Maintenance-tier AI workflows.** [[Code Comprehension Bottleneck]] argues maintenance is 90% of lifecycle cost, but the wiki under-covers AI patterns specifically for legacy-code comprehension, refactoring large unfamiliar codebases, and incident response — currently more articles focus on greenfield generation.
