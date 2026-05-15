---
title: Databricks Lakeflow
updated: 2026-05-15
sources: [raw/databricks-ai-first-data-engineering-lakeflow.md]
related: [databricks-lakebase]
---
## Purpose
Unified data engineering platform that embeds AI directly into ETL pipelines, so data engineers can call models as first-class pipeline functions instead of stitching together a separate ML platform.

## How it works
Lakeflow exposes AI capabilities as **SQL/Python functions inside pipelines**, the core primitive of [[AI-First Data Engineering]]:

- `ai_extract` — pull structured fields from unstructured text.
- `ai_classify` — assign labels from a taxonomy.
- `ai_translate` — multilingual normalization.
- `ai_parse_document` — extract structure from PDFs, images, scans.
- `ai_analyze_sentiment` — sentiment scoring.
- `ai_query` — general-purpose model invocation against a chosen endpoint.

These are orchestrated by **Lakeflow Jobs**, a DAG runner that handles dependencies, retries, and scheduling. **Agent Bricks** sits above as a higher-level AI capability layer, and **Databricks Assistant** generates pipeline code from natural language. Inference runs serverless and batch by default, so cost scales with rows processed rather than provisioned GPUs.

Two pattern examples from the source:
- **Call transcript analysis** — ingest transcripts → `ai_analyze_sentiment` → `ai_extract` for entities → `ai_classify` for intent → `ai_query` for summarization → write to CRM.
- **Insurance claims processing** — ingest claim emails → `ai_query` to route → vision model on attachments → `ai_parse_document` on scanned forms → consolidate into a structured claim row.

## Strengths
- Eliminates the context switch between data engineering tools and ML platforms — pipelines live in one place with one governance model.
- Unstructured-to-structured transformation becomes a one-line pipeline step.
- Serverless batch inference matches the bursty, scheduled nature of ETL workloads.
- Real production scale demonstrated: Kard (fintech) categorizes billions of transactions; Banco Bradesco reports 50% coding time reduction via Databricks Assistant; Locala built a GenAI Assistant with a single data scientist.
- Built-in governance keeps AI usage inside the lakehouse perimeter rather than scattering credentials across services.

## Weaknesses
- Lock-in to the Databricks platform for orchestration, compute, and governance.
- AI function quality is bounded by the backing endpoint — `ai_extract` is only as good as the underlying model and prompt.
- Costs can hide in token usage at high row volumes; batch inference helps but doesn't eliminate the problem.
- DAG orchestration is less expressive than full Airflow for complex cross-system flows.

## Alternatives
- Airflow + custom LLM operators — flexible but requires plumbing for governance, retries, and inference scaling.
- dbt + external model APIs — SQL-native but no first-class AI primitives or unified governance.
- Snowflake Cortex — comparable AI-in-warehouse functions on the Snowflake stack.

## Sources
- [[raw/databricks-ai-first-data-engineering-lakeflow]] — AI function catalog, Agent Bricks and Assistant roles, Lakeflow Jobs DAG, Kard / Bradesco / Locala deployments, two pattern examples.

## Backlinks
- [[AI-First Data Engineering]]
- [[Database Branching]]
