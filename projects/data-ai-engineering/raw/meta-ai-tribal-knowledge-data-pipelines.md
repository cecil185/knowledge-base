# How Meta Used AI to Map Tribal Knowledge in Large-Scale Data Pipelines (Krishna Ganeriwal, Plawan Rath, Ashwini Verma)

**Source:** https://engineering.fb.com/2026/04/06/developer-tools/how-meta-used-ai-to-map-tribal-knowledge-in-large-scale-data-pipelines/
**Read:** 2026-05-18

## The Problem: AI Tools Without a Map

Meta's data processing pipeline spans four repositories, three languages, and over 4,100 files, organized as config-as-code using Python configurations, C++ services, and Hack automation scripts. When they deployed AI agents for development tasks, they hit critical limitations.

The pipeline's complexity meant that "a single data field onboarding touches configuration registries, routing logic, DAG composition, validation rules, C++ code generation, and automation scripts." Without contextual understanding, AI agents produced code that compiled but contained subtle errors, missing domain-specific conventions and cross-module dependencies undocumented anywhere.

Key problems:
- AI had no understanding of two configuration modes using different field names for identical operations
- "Deprecated" enum values couldn't be removed due to serialization compatibility requirements
- Agents would guess, explore, and produce subtly incorrect outputs

## The Approach: Pre-Compute Engine with Specialized Agents

Meta developed a swarm of 50+ specialized AI agents working in orchestrated phases:

- 2 explorer agents mapped the codebase
- 11 module analysts processed every file
- 2 writers generated context files
- 10+ critic passes performed three rounds of quality review
- 4 fixers applied corrections
- 8 upgraders refined the routing layer
- 3 prompt testers validated 55+ queries across five personas
- 4 gap-fillers covered remaining directories
- 3 final critics ran integration tests

**Five Key Questions Each Analyst Answered:**

1. What does this module configure?
2. What are the common modification patterns?
3. What non-obvious patterns cause build failures?
4. What are the cross-module dependencies?
5. What tribal knowledge is buried in code comments?

The fifth question proved most valuable. The analysis uncovered "50+ non-obvious patterns" including hidden intermediate naming conventions and append-only identifier rules where removing deprecated values breaks backward compatibility -- information never formally documented.

## What They Built: "A Compass, Not An Encyclopedia"

59 concise context files (~1,000 tokens each, consuming less than 0.1% of a modern model's context window) following four sections:

1. **Quick Commands** -- copy-paste operations
2. **Key Files** -- the 3-5 files actually needed
3. **Non-Obvious Patterns** -- design choices not apparent from code
4. **See Also** -- cross-references

Each context file maintained 25-35 lines with no extraneous information. Prioritized actionable navigation over exhaustive documentation.

Additional infrastructure:
- Orchestration layer auto-routing engineers to appropriate tools based on natural language queries
- Cross-repository dependency index turning "What depends on X?" from multi-file exploration into single graph lookups
- Data flow maps showing how changes propagate across repositories
- Automated refresh mechanism validating file paths, identifying coverage gaps, and auto-fixing issues every few weeks

## Results

| Metric | Before | After |
|--------|--------|-------|
| AI context coverage | ~5% (5 files) | 100% (59 files) |
| Codebase files with AI navigation | ~50 | 4,100+ |
| Tribal knowledge documented | 0 | 50+ non-obvious patterns |
| Tested prompts (core pass rate) | 0 | 55+ (100%) |

Performance improvements:
- ~40% fewer tool calls and tokens per task
- Complex workflows previously requiring ~two days of research completed in ~30 minutes
- Quality critic agents improved scores from 3.65 to 4.20 out of 5.0
- Zero hallucinations in file path verification

## Challenging Conventional Wisdom

Recent academic research found AI-generated context files decreased agent success rates on well-known open-source repos like Django and matplotlib. Meta's situation differed: their proprietary config-as-code contained tribal knowledge absent from any model's training data.

Three design decisions mitigated pitfalls:
- Files remained concise (~1,000 tokens, not encyclopedic summaries)
- Implementation was opt-in (loaded only when relevant)
- Quality-gated through multi-round critic review and automated self-upgrade

Quote: "Without context, agents burn 15-25 tool calls exploring, miss naming patterns, and produce subtly incorrect code."

## How to Apply This to Your Codebase

1. Identify tribal knowledge gaps -- focus on where AI agents fail most
2. Use the "five questions" framework -- functionality, modification patterns, failure modes, dependencies, undocumented practices
3. Follow "compass, not encyclopedia" -- 25-35 line context files emphasizing actionable navigation
4. Build quality gates -- employ independent critic agents to score and improve generated context
5. Automate freshness -- periodic validation and self-repair mechanisms

## What's Next

Meta plans to expand context coverage to additional pipelines and explore tighter integration between context files and code generation workflows. Investigating whether automated refresh can detect emerging patterns and new tribal knowledge from recent code reviews and commits.

Closing quote: "This approach turned undocumented tribal knowledge into structured, AI-readable context and one that compounds with every task that follows."
