# Code w/ Claude 2026 Live Blog (Simon Willison)

**Source:** https://simonwillison.net/2026/May/6/code-w-claude-2026/
**Read:** 2026-05-18

Simon Willison live-blogged Anthropic's "Code w/ Claude 2026" conference keynote on May 6, 2026. The event focused on shipping product improvements to Claude Code and the broader developer platform rather than announcing new models.

## Infrastructure and Rate Limits

Anthropic doubled Claude Code's five-hour usage limit for Pro, Max, and Enterprise customers. The company announced a partnership with SpaceX to utilize capacity from their Colossus data center in Memphis. API volume on the Anthropic platform increased 17x year-over-year.

## Claude Managed Agents (Public Beta / Research Preview)

Three new capabilities announced:

1. **Multi-agent orchestration** -- creating agent fleets to tackle complex tasks by coordinating multiple agents working together.
2. **Outcomes** -- enables Claude to iterate toward defined success criteria rather than just executing a single prompt. The agent keeps working until the outcome is achieved.
3. **Dreaming** (research preview) -- agents review previous sessions, identify gaps in their knowledge or approach, and self-improve by creating new memory files. This allows agents to get better over time without human intervention.

## Claude Code Enhancements

- **Code Review tool** -- adopted across Anthropic's own teams for reviewing pull requests.
- **Remote Agents** -- control laptops from mobile devices, enabling async coding workflows.
- **CI auto-fix** -- automatic PR corrections when CI fails, reducing the feedback loop on broken builds.
- **Security Reviews** -- built-in security review functionality for code changes.
- **Routines** -- async automations that run on schedules or triggers, enabling background agent work.

## Strategic Insights and Patterns

### Advisor Strategy

Smaller models consulting Opus as an advisor achieved frontier-quality results at 5x lower cost. A customer called "eve" exemplified this cost-efficiency pattern. The implication: you do not need the most expensive model for every call -- route strategically and use the big model only when needed.

### Successful Team Patterns

Speakers emphasized that successful teams focus on:
- **Automated evaluations** -- measuring output quality programmatically rather than relying solely on human review.
- **Simple scaffolding** -- keeping orchestration code minimal and letting the model do the heavy lifting.
- **Innovative model applications** -- finding novel ways to apply existing model capabilities.

### Executives Writing Code

Leadership highlighted that executives increasingly contribute code directly, enabled by the reduced time investment through AI assistance. The barrier to contributing code has dropped significantly.

### Async Development

Predicted that asynchronous code development patterns using routines will become standard practice -- agents working on code while the developer is offline or focused elsewhere.

## Notable Customer Examples

- **Shopify** -- mentioned as a notable adopter.
- **Mercado Libre** -- 23,000 engineers targeting "90% autonomous coding by Q3" as an organizational goal.
