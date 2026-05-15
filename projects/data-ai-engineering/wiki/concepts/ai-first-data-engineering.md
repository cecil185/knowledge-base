---
title: AI-First Data Engineering
updated: 2026-05-15
sources: [raw/databricks-ai-first-data-engineering-lakeflow.md]
related: [database-branching, agentic-coding]
---
## Summary
Embedding AI capabilities directly as primitives inside ETL pipelines — `ai_extract`, `ai_classify`, `ai_translate`, `ai_parse_document`, `ai_analyze_sentiment`, `ai_query()` — instead of routing data out to a separate ML service. AI becomes a SQL/orchestration primitive that data engineers compose with `JOIN` and `GROUP BY`, governed by the same lakehouse controls as the rest of the pipeline.

## Details
The traditional architecture: ETL runs in one system, ML inference runs in another, and integration is glue code, network hops, and a separate governance regime. AI-first inverts this — model invocation is a function call inside the pipeline.

Concrete primitives Databricks exposes:
- `ai_extract` — pull structured fields from unstructured text
- `ai_classify` — label rows against a target taxonomy
- `ai_translate` — language conversion as a column
- `ai_parse_document` — turn PDFs, scans, emails into structured rows
- `ai_analyze_sentiment` — sentiment as a primitive
- `ai_query()` — arbitrary model calls inline

Two reference pipelines from the source:
- **Call-transcript analysis** — ingest → sentiment → extract → classify → query → CRM. Each stage is a SQL function call.
- **Insurance-claims** — email → `ai_query` for triage → vision → `ai_parse_document` for attachments → consolidate.

Real deployments cited:
- **Kard** — billions of transactions auto-categorized
- **Banco Bradesco** — 50% coding time reduction via Databricks Assistant
- **Locala** — single data scientist built a GenAI Assistant

Operational shifts:
- **Serverless batch inference** brings hour-long jobs down to minutes
- **Unstructured → structured at scale** without bespoke ML infra
- **Governed AI within the lakehouse** — same access controls, lineage, audit logging as the rest of the data
- **Composability** — engineers stay in SQL/Python/orchestration tools they already know

## Tradeoffs / When to use
**Gains:** removes the ML-service handoff; lineage and governance unified; serverless economics; data engineers can ship AI features without an MLE team; orchestrators (DAG schedulers) become AI-aware natively.
**Costs:** vendor concentration (model + lakehouse + governance in one stack); cost-per-row matters at billions-of-rows scale; AI function output requires its own quality monitoring; debugging an `ai_classify` mislabel is harder than debugging deterministic SQL.
**Fit:** pipelines that already live in the lakehouse and are bottlenecked on unstructured input. Less useful when AI workloads are small, latency-critical, or already mature in a separate ML platform.

## Key tools / implementations
- [[Databricks Lakeflow]] — orchestration with `ai_*` functions as first-class primitives
- [[Databricks Lakebase]] — governed serverless data layer underneath; see [[Database Branching]] for the agentic-dev cousin

## Sources
- [[raw/databricks-ai-first-data-engineering-lakeflow]] — primitives, deployment examples, governed AI-in-lakehouse pattern

## Backlinks
- [[Database Branching]]
- [[Databricks Lakebase]]
- [[Databricks Lakeflow]]
