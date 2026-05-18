# AI Coding Agent Security: Practical Guardrails for Claude Code, Copilot, and Codex (Max Kryvych)

**Source:** https://dev.to/maxkrivich/ai-coding-agent-security-practical-guardrails-for-claude-code-copilot-and-codex-och
**Read:** 2026-05-18

## Core Problem

AI coding agents inherit your full shell environment -- credentials, SSH keys, API tokens, cloud configs. This creates real attack surface. Documented incidents include:

- A Claude Code user experiencing an accidental `rm -rf ~/` command
- Prompt injection attacks exfiltrating npm tokens via malicious package READMEs
- Supply chain attacks using agents as exfiltration tools through inherited environment variables

The fundamental issue: agents operate with the same permissions as the developer, but without the developer's judgment about what is safe to run.

## Three-Layer Defense Model

The article recommends nested protections where each layer catches what the others miss:

1. **OS-level sandboxing** (kernel enforcement -- cannot be bypassed by the agent)
2. **Tool-enforced configuration** (deny lists, environment variable scrubbing, permission modes)
3. **Model-level instructions** (security guidelines in dedicated instruction files like CLAUDE.md)

No single control is sufficient. Layered defenses catch different failure modes.

## Claude Code Specific Configuration

- Enable `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` to strip sensitive environment variables before subprocesses run
- Use `disableBypassPermissionsMode: "disable"` to prevent the agent from escalating its own permissions
- Implement per-project deny lists for dangerous commands (rm -rf, curl to external hosts, etc.)
- Create a `CLAUDE.md` file with explicit approval gates for high-risk operations (database writes, deployments, credential access)

## GitHub Copilot Configuration

- Disable web search and data sharing in account settings
- Prevent Copilot from analyzing `.env`, config, and credential files
- Add `.github/copilot-instructions.md` with security rules
- Note: Copilot has no built-in command deny list -- this is a gap compared to Claude Code

## Other Agents (Codex, Gemini, OpenCode)

- Similar patterns: environment variable redaction, tool-specific permission systems, instruction files
- Restrict network access and sensitive file reads
- Each tool has its own configuration surface but the principles are the same

## Sandboxing Tools

Three practical sandboxing options:

- **Agent Safehouse** -- macOS-specific sandbox for coding agents
- **Anthropic's sandbox-runtime** -- cross-platform sandboxing solution
- **Docker Sandboxes** -- works on macOS/Windows, familiar tooling

## Critical Files to Protect

Deny agent access to:
- `~/.aws/` (cloud credentials)
- `~/.ssh/` (SSH keys)
- `~/.gnupg/` (GPG keys)
- `~/.kube/` (Kubernetes configs)
- Project `.env` files
- Any credential or secret files

## Key Takeaway

The three-layer model (OS sandbox + tool config + model instructions) is the practical framework. Each layer is imperfect alone but together they provide defense in depth against both accidental destruction and malicious prompt injection.
