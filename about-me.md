# About Cecil Ash

## Role

Senior data engineer at **Teamworks**. Owns the ingestion platform end-to-end — from vendor API integration through to the data lake. Practitioner, not manager.

Email: cash@teamworks.com

---

## The Stack

### Languages & Config
- **Python** — primary application language
- **PySpark** — calculated fields, Hudi transformations
- **Terraform HCL** — all AWS infrastructure
- **YAML** — Helm charts, Argo CD apps, GitLab CI pipelines

### Compute & Orchestration
- **Airflow on MWAA** — scheduled polling DAGs, runs jobs via `KubernetesPodOperator` on EKS
- **Argo CD** — GitOps, syncs Helm charts to EKS clusters
- **EKS** — two clusters: `datalake-stg` (staging), `datalake-latest` (prod)

### Data Pipeline
```
Vendor API webhook → Webhook Listener (aiohttp) → SQS
Scheduled Poller (Airflow DAG) ──────────────────→ SQS
                                                    ↓
SQS Message Poller → Processor → Avro → Kafka (MSK) → Onehouse → S3 Lake
                                                                      ↓
                                              Calculated Fields (PySpark/Hudi)
                                                                      ↓
                                              Reverse ETL → Postgres (app DB)
```

### Storage & Formats
- **S3** — data lake storage
- **Apache Hudi** — table format on S3
- **Avro** — wire format on Kafka
- **Postgres** — serving layer (app DB, reverse ETL target)

### AWS Services
MSK, MWAA, Glue, SQS, S3, KMS, IAM, Valkey

### AWS SSO Profiles
- Staging: `datalake-stg`
- Prod: `datalake-prod`

### Observability
- **Datadog** — logs, metrics, error triage, alert tuning

### CI/CD & Deployment
- **GitLab CI** — pipelines, Docker image builds
- **Helm** — packaging and versioning app deployments
- **Argo CD** — GitOps sync to EKS

---

## Vendor Integrations

| Vendor | Method | Direction |
|--------|--------|-----------|
| Catapult | Webhook listener + processor | Push (webhooks) |
| Dynamo | Poller + processor | Pull (scheduled) |
| ForceDecks | Poller + processor | Pull (scheduled) |
| Performance | Poller + processor | Pull (scheduled) |
| SmartSpeed | Poller + processor | Pull (scheduled) |

---

## Codebase

**Workspace root:** `/Users/cecil/Code/genai`

| Repo | Purpose |
|------|---------|
| `ingestion/` | Python app code — FastAPI/aiohttp, Kafka, SQS workers, processors |
| `ingestion-dags/` | Airflow DAGs for MWAA |
| `ingestion-helm/` | Helm charts — webhook listener, processors, pollers, MWAA RBAC |
| `ingestion-argo/` | Argo CD Application/AppProject definitions |
| `ingestion-terraform/` | Primary AWS IaC — MSK, MWAA, Glue, SQS, S3, KMS, IAM, Valkey |
| `ingestion-terraform-onehouse/` | OneHouse-specific S3 Terraform |

Each subdirectory is its own Git repo hosted on GitLab.

---

## Workflow

- **PM:** Linear — two workspaces: Teamworks (work) and personal
- **Development loop:** ADLC — `refine → plan → breakdown → execute → MR`
- **Testing:** TDD; tests are never deleted without explicit approval
- **Tooling:** `just` recipes for all common tasks; pre-commit hooks for lint/format gates
- **Code review:** gates enforced before merge
- **AI tooling:** Claude Code with custom skills and ADLC plugin; heavy agent usage

---

## Current Focus Areas

- Reducing manual triage and cross-team dependency in pipeline operations
- Datadog log quality, error classification, alert tuning
- AI-assisted engineering — Claude Code, agents, ADLC workflow
- Vendor poller reliability and schema evolution (Avro)
- Hudi/Onehouse mechanics
- MWAA/Airflow ergonomics and DAG factoring

---

## How He Reads

- **Reads to change something.** Pure theory scores low unless it reframes a real problem.
- **Skeptical of hype.** Calls it when he sees it.
- **Time is the constraint.** A false positive ("you should read this") costs more than a false negative.
- Direct and economical — doesn't want padding, hedging, or repetition.

---

## Personal Projects

**`/Users/cecil/Code/me/`** — personal repos separate from Teamworks work.

**Purpose** (this repo) — personal learning system. Evaluates tech articles, logs them, surfaces patterns over time. Linear team: CC (personal workspace).
- `Work` project — tickets for building the system
- `Wiki` project — tickets for high-value articles worth acting on
