# My LLM coding workflow going into 2026 (Addy Osmani)

**Source:** https://addyosmani.com/blog/ai-coding-workflow/
**Read:** 2026-05-10

## Core Workflow Stages

### 1. Planning Before Code
Start with detailed specifications rather than vague prompts. Engage the AI in iterative questioning to flesh out requirements, edge cases, and architectural decisions. Compile findings into a comprehensive spec.md, then have a reasoning-capable model generate a step-by-step project plan breaking implementation into manageable tasks before writing any code.

### 2. Iterative Chunking
Avoid requesting large monolithic outputs. Decompose projects into small, focused tasks executed sequentially. This "mirrors good software engineering practice, but it's even more important with AI in the loop." Each chunk should be small enough for the AI to handle within context limits and for humans to understand the output.

### 3. Extensive Context Provision
Feed the AI all relevant information: project code, technical constraints, known pitfalls, preferred approaches, API documentation, and domain-specific knowledge. Use context-packaging tools like gitingest or repo2txt to bundle relevant codebase sections. Explicitly tell the AI what to focus on and what to ignore to preserve tokens.

## Model Selection & Configuration

- Choose the right tool intentionally: Different models have distinct "personalities." Try multiple models on the same prompt to cross-check approaches.
- Use the latest versions: Prioritize newer "pro" tier models where quality matters.
- Customize behavior: Create rules files (CLAUDE.md, GEMINI.md) containing style guidelines, preferences, and process rules. Provide in-line examples of desired output formats.

## Quality Assurance & Human Oversight

### Testing Strategy
- Treat AI-generated code as junior developer work requiring thorough review and testing
- Integrate testing into the workflow itself: generate test lists during planning, run test suites after implementing tasks
- Leverage tight feedback loops: write code -> run tests -> fix failures
- Use automated code quality checks (linters, type checkers) as guardrails

### Code Review Practices
- Read through AI-generated code line by line
- Employ secondary AI sessions to critique work produced by the first (cross-model review)
- Use Chrome DevTools MCP to bridge static analysis and live execution for precise debugging
- "Never commit code you can't explain"

### Key Principle
Treat the LLM as "over-confident and prone to mistakes." You remain the accountable engineer responsible for quality.

## Version Control & Reversibility

- Commit early and often, treating commits as "save points"
- Use granular git messages documenting each small task
- Employ branches or worktrees to isolate AI experiments in parallel
- Leverage commit history and diffs as context for subsequent AI interactions

## Automation & CI/CD Integration

- Automated test execution on every commit/PR
- Enforced code style checks (ESLint, Prettier, linters)
- Staging deployments for new branches
- Feed CI results back into AI sessions for collaborative debugging loops

## Practical Tools

- Claude Code, Google's Jules, GitHub Copilot Agent: CLI and asynchronous coding agents
- Claude Skills: Package instructions and domain expertise into reusable modular capabilities
- MCP (Model Context Protocol): Tools like Context7 for automated context packaging
- Custom instructions: Configure global AI behavior through tool settings

## Strategic Mindset

This is "AI-augmented software engineering" rather than AI-automated development:
- Classic software engineering practices (design docs, testing, version control, code standards) become more important, not less
- The developer remains the "director of the show"; the AI is a powerful pair programmer requiring clear direction
- Using AI amplifies existing expertise — it rewards those with strong fundamentals
- Continuous learning through AI interactions sharpens engineering skills

**Framework:** disciplined planning + small iterative chunks + extensive context + human oversight + automation = effective AI-assisted development
