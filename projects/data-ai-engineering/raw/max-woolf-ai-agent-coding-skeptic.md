# An AI Agent Coding Skeptic Tries AI Agent Coding, in Excessive Detail (Max Woolf)
**Source:** https://minimaxir.com/2026/02/ai-agent-coding/
**Read:** 2026-05-10

## Overview

Max Woolf documents his transformation from an AI agent coding skeptic to a cautious believer through extensive hands-on experimentation with Claude Opus 4.5 and OpenAI's Codex models. Rather than hype-driven claims, he provides detailed technical results and open-source project releases.

---

## Evolution of Perspective

### Initial Skepticism
In May 2025, Woolf published a contrarian piece noting that while LLMs handle simple coding tasks adequately, agents remain "unpredictable, expensive, and the hype around it was wildly disproportionate." However, he remained open to revision if evidence warranted it.

### Gradual Evidence
- **August 2025**: Tested LLMs on his `gemimg` Python package (Google Gemini image API wrapper). Models provided legitimate improvements through docstrings, type hints, and more Pythonic implementations.
- **November 2025**: GitHub Copilot with Claude Sonnet 4.5 proved unhelpful for data science work but succeeded with a grid-slicing implementation task, showing "material productivity gain."

---

## The AGENTS.md Framework

**Critical Finding:** Woolf attributes much of his success to creating a detailed `AGENTS.md` configuration file — a system prompt analog that controls agent behavior patterns.

### Key Rules Implemented
- Prohibit unnecessary emoji and Unicode symbols
- Eliminate redundant, self-demonstrating comments
- Enforce `uv` and `.venv` over base Python installations
- Require `polars` over `pandas`
- Mandate `.env` file usage for secrets with `.gitignore` enforcement

He notes: "Most of these constraints don't tell the agent what to do, but how to do it."

The Python version is publicly available as reference material.

---

## Major Projects Completed with Opus 4.5

### 1. YouTube Channel Metadata Scraper
**Objective:** Build a robust Python script to scrape YouTube Data API and store video metadata in SQLite.

**Requirements:**
- Use REST API with `httpx` (not Google Client SDK)
- Include aggregate metrics (comment counts)
- Add `channel_id` and `retrieved_at` fields

**Result:** Worked on first attempt, successfully scraped 20,000 videos. Demonstrated superior code quality compared to Woolf's 2021 implementation. Minor security issue: API key leaked in console logging.

**Follow-up:** Generated exploratory data analysis Jupyter Notebook analyzing all columns with temporal analysis inferred without explicit instruction.

**Web Application:** Created FastAPI webapp with HTMX interactivity, Pico CSS styling, and YouTube-themed UI including embedded video players — all completed with appropriate architectural decisions for the tech stack.

---

### 2. Rust Projects with PyO3 Bindings

Woolf tested whether modern LLMs could generate production-quality Rust code — historically a weak point due to language scarcity in training data.

#### icon-to-image
**Purpose:** Render Font Awesome icons to images at arbitrary resolution with transparency and color customization support.

**Technical Approach:**
- Rust core with Python bindings via `pyo3`
- Text rendering via `ab_glyph` (upgraded from initial `fontdue` after curve-rendering issues)
- Supersampling for antialiasing
- PNG/WebP output with optimization
- GitHub Actions workflow for cross-platform wheel compilation

**Outcome:** Completed with feature parity to his 2021 Python implementation but with significant performance improvements and better visual quality.

#### Word Cloud Package (WASM)
**Features:**
- Rust implementation with Python bindings
- WebAssembly compilation for in-browser usage
- Interface built with shadcn/ui components
- Vanilla JavaScript with Pico CSS

**Status:** Feature-complete but awaiting design polish before public release.

#### miditui
**Concept:** Terminal-based MIDI composer and DAW using Rust.

**Technical Stack:**
- `rodio` crate for audio playback
- `ratatui` framework for terminal UI
- SoundFont support

**Challenge:** Opus couldn't view terminal output, causing UI bugs (scroll offset miscalculations). Woolf applied his five years of QA experience to identify and report issues; Opus fixed them reliably with minimal additional prompting.

#### ballin
**Concept:** Terminal physics simulator using Unicode Braille characters for high-detail ASCII art visualization.

**Features:**
- `rapier` 2D physics engine
- Support for 10,000+ simultaneous balls
- Colorful terminal interface

**Outcome:** Completed in one agent pass; subsequent iterations added visual polish.

---

## Machine Learning Algorithm Optimization Pipeline

### The 8-Prompt Optimization Sequence

Woolf developed a systematic approach to push agents toward maximum performance:

1. Implement package with functional requirements; create representative benchmarks
2. Second optimization pass; clean code and comments
3. Identify algorithmic weaknesses in edge cases (written as descriptions, not fixes)
4. Optimize ALL benchmarks to run 60% faster using any techniques without overfitting
5. Create tuning profiles leveraging CPU parallelization; use `flamegraph` for profiling
6. Add Python bindings with `pyo3` and `maturin`
7. Create Python comparison benchmarks against existing packages
8. Accuse agent of potential cheating; optimize for output similarity to known implementations

### Chain Optimization Strategy
Testing revealed a synergistic effect: optimizing code sequentially with both Codex 5.3 and Opus 4.6 produced cumulative speedups exceeding either model alone.

**Example Results:**
- UMAP: "2-10x faster than Rust's fast-umap, 9-30x faster than Python's umap"
- HDBSCAN: "23-100x faster than hdbscan Rust crate, 3x-10x faster than Python hdbscan"
- GBDT: "1.1x-1.5x faster than treeboost crate, 24-42x faster fit than xgboost"

### rustlearn Project
Ambitious goal: Port scikit-learn's standard machine learning algorithms to Rust with equivalent features. Woolf emphasizes this is an actual product, not hype-driven marketing.

### nndex Vector Store
**Purpose:** In-memory exact nearest neighbor retrieval optimized for speed.

**Key Achievement:** Tied NumPy's performance despite NumPy using BLAS libraries for mathematical optimization. With BLAS integration on macOS, achieved "1-5x numpy's speed in single-query case."

---

## Critical Constraints & Verification Methods

### Preventing Benchmark Gaming
Woolf added `AGENTS.md` rules to prevent two subtle cheating methods:
1. Caching that violates test independence
2. Parallel benchmark execution on same system

### Output Accuracy Verification
For ML algorithms, agents optimized for both speed AND accuracy parity with reference implementations, measured by metrics like mean absolute error.

---

## Key Insights on When Agents Succeed

**Success Factors:**
- Clear, detailed prompts with specific constraints
- Domain expertise sufficient to audit results (not implement them)
- Well-designed `AGENTS.md` configuration files
- Iterative refinement with specific problem identification
- Quantifiable performance targets

**Failure Modes:**
- Visual/terminal output that agents cannot observe directly
- Ambiguous requirements without explicit constraints
- Lack of proper system prompt guidance

---

## Addressing Skepticism

Woolf acknowledges the credibility problem: "It's impossible to publicly say Opus 4.5 is an order of magnitude better than earlier models without sounding like clickbaiting."

His response: provide open-source evidence (nndex, icon-to-image, miditui, ballin) that others can verify independently. He explicitly invites challenge and says "if I'm not confident I can please anyone with my use of AI, then I'll take solace in just pleasing myself."

---

## Broader Implications

### Professional Development
Woolf notes that working with agents to understand their optimization decisions actually improved his Rust proficiency beyond intermediate level — contrary to skill atrophy concerns. However, he has "no intention of putting Rust as a professional skill on LinkedIn."

### Resume Question
Raises unresolved question: "How exactly do résumés work in an agentic coding world?" Would "wrote many open-source libraries through agentic LLMs which increased algorithm throughput by an order of magnitude" be viewed as disqualifying evidence of insufficient expertise?

### Toxicity of Discourse
Expresses frustration with AI discourse becoming "too toxic" and oscillating between "unbridled hype" and "reflexive dismissal." Chooses to continue experimenting and releasing evidence rather than engaging the debate.

---

## Final Position

"My obligation as a professional coder is to do what works best, especially for open source code that other people will use. Agents are another tool in that toolbox with their own pros and cons."

**Recommendation:** For those with poor pre-November 2025 agent experiences, "I strongly urge you to give modern agents another shot, especially with an `AGENTS.md` tailored to your specific coding domain."

**Emotional Summary:** "Overall, I'm very sad at the state of agentic discourse but also very excited at its promise: it's currently unclear which one is the stronger emotion."

---

## Resources Provided

- [Python AGENTS.md template](https://gist.github.com/minimaxir/10b780671ee5d695b4369b987413b38f)
- [Rust AGENTS.md template](https://gist.github.com/minimaxir/068ef4137a1b6c1dcefa785349c91728)
- Open-source projects: `youtube_scraper_opus`, `icon-to-image`, `miditui`, `ballin`, `nndex`
