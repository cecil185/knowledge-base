This side-project is similar to NotebookLM in many ways but here's what's unique: the goal-driven pipeline upstream of Q&A. This system runs /digest: pull HN + curated sources → filter against a written goal.md → auto-ticket the matches → summarize → synthesize. That's an agentic content pipeline with a personal relevance model, not a Q&A tool.

Focus of this project:
  1. Agentic content pipeline with goal-aware filtering — that's the novel product angle. Citations are a feature within it, not the headline.
  2. AI engineering practice portfolio — evals, guardrails, LLM-as-judge, retrieval experiments, prompt regression. The pipeline is the substrate that lets you do these on something real.

Most to least important features of this project:
  - filtering — of the articles we discover, are we filtering based on their relevance to goal.md?
  - searching — are we discovering high-quality articles before filtering?
  - qa — are we surfacing the relevant articles from our knowledge base when queried?
  - cited answers — are we providing paragraph-level citations so readers can reference the original article?

What to avoid:
  - Building a slick UI on top — pure waste, NotebookLM wins.
  - Doing generic RAG with no evals and no named techniques.
  - Trying to make this a tool other people use.

Where to focus:
  - The /digest filtering loop. Nobody else does this exactly. Goal-aware content curation as an agentic loop, with measurable metrics ("what fraction of auto-ticketed articles did I actually keep?") is a sharp, specific portfolio piece.
  - The evals + guardrails + judge layer. Implementing these on a working system you built yourself is much more credible than doing them on a toy example.
