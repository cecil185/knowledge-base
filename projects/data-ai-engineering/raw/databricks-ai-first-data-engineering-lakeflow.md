# AI-First Data Engineering: Lakeflow and Agent Bricks (Databricks Blog)
**Source:** https://www.databricks.com/blog/ai-first-approach-data-engineering-lakeflow-and-agent-bricks
**Read:** 2026-05-10

## What Are Lakeflow and Agent Bricks?

**Lakeflow** is Databricks' unified data engineering platform designed to embed AI directly into ETL workflows. It provides an AI-native engineering environment, enabling teams to integrate and productionize models directly within ETL workflows using Agent Bricks AI functions.

**Agent Bricks** is the AI capability layer powering Lakeflow. It provides a suite of AI functions that data engineers can invoke within their pipelines, including task-specific functions and general-purpose query capabilities.

## Key AI Functions in Agent Bricks

- **ai_extract**: Pulls specific entities (persons, locations, organizations) from text
- **ai_classify**: Categorizes input text according to predefined labels
- **ai_translate**: Converts text between languages
- **ai_parse_document**: Transforms unstructured data (PDFs, images, tables) into structured formats using multimodal models
- **ai_analyze_sentiment**: Determines sentiment/tone from text
- **ai_query()**: Runs AI-driven transformations using any LLM across large datasets via serverless batch inference

## How AI Changes Data Engineering Workflows

The integration fundamentally shifts how engineers approach pipeline design. Rather than building separate AI services or managing custom agents, engineers write queries incorporating AI functions directly into orchestrated jobs. This keeps AI operations within the governed lakehouse context while maintaining enterprise data lineage and security.

The approach replaces manual, brittle processes. Data teams dealing with unstructured inputs (contracts, invoices, transcripts, reviews) can automate extraction and classification at scale without separate ML infrastructure.

## Concrete Patterns for AI-Assisted Pipeline Work

### Pattern 1: Call Transcript Analysis (Sales Ops)

1. Ingest unstructured transcripts into the lakehouse
2. Apply `ai_analyze_sentiment` to determine call tone
3. Use `ai_extract` to pull structured fields (names, companies, contact details)
4. Deploy `ai_classify` to categorize call type and urgency
5. Generate summaries via `ai_query` using specified LLMs
6. Create personalized follow-up actions in the same workflow
7. Push results directly to CRM systems

This eliminates separate sentiment analysis systems or manual review bottlenecks.

### Pattern 2: Insurance Claims Processing (Document-Heavy)

1. Ingest email attachments (PDFs, images) into the lakehouse
2. Extract email body data with `ai_query` for key fields (name, SSN, address)
3. Process attached images with vision-capable `ai_query` for metadata and descriptions
4. Parse complex PDFs using `ai_parse_document`
5. Consolidate extracted data for downstream teams (BI, ML, processing)
6. Orchestrate entire workflow through Lakeflow Jobs DAG

This removes manual document handling and reduces approval cycle times.

## Business Outcomes — Real-World Customer Examples

**Kard** (fintech): Replaced inconsistent transaction categorization with Agent Bricks functions. Now processes billions of transactions with improved accuracy and enables personalized reward systems.

**Banco Bradesco** (Latin American banking): Adopted Databricks Assistant for code generation, reducing coding time by 50% and democratizing data access across technical and non-technical users.

**Locala** (ad-tech platform): Used Lakeflow Jobs to orchestrate complex LLM training pipelines that Airflow couldn't handle. A single data scientist built a GenAI Assistant that became a key product feature.

## Implications for Shipping Data Engineering Work Faster

**Reduced Development Cycles**: Engineers avoid building custom NLP systems or model serving infrastructure. Pre-built functions deploy immediately within existing pipelines.

**Operational Simplification**: Lakeflow Jobs orchestrates AI workloads at scale, automating complex pipelines while maintaining full enterprise context. Single workflows handle data extraction, transformation, AI application, and downstream delivery.

**Productivity Amplification**: Native AI functions eliminate context-switching between data platforms and ML systems. Engineers work entirely within SQL and orchestration tools they already know.

**Cost Efficiency**: Serverless batch inference automatically provisions compute, reducing per-request overhead and transforming hour-long jobs to minutes for high-volume workloads.

The fundamental shift is operational: instead of data engineering and AI operations as separate concerns, they merge into single, governed workflows that execute faster because they eliminate integration friction and maintain complete data context throughout processing.
