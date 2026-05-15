# How Agentic Software Development Will Change Databases (Databricks)
**Source:** https://www.databricks.com/blog/how-agentic-software-development-will-change-databases
**Read:** 2026-05-10

# How Agentic Software Development Will Change Databases

**Authors:** Ippokratis Pandis, Nikita Shamgunov, and Reynold Xin
**Published:** March 30, 2026
**Category:** Platform > Announcements

---

## Overview

This article explores how AI agents are transforming software development and what database infrastructure these agents actually require. The authors argue that three major trends are redefining modern database requirements in the age of agentic software development.

---

## Rapid Evolutionary Software Development

Traditional software development followed a slow, linear path because building and operating applications required substantial engineering investment. AI agents fundamentally alter this dynamic by enabling applications to be generated, modified, and redeployed within minutes.

The development process now mirrors an evolutionary algorithm:

1. Generate initial application versions
2. Rapidly create variants with different schemas, prompts, or logic
3. Evaluate results
4. Continue development from the most successful versions

This represents a dramatic acceleration—each iteration can take seconds to hours, roughly 100x to 1000x faster than pre-LLM development cycles. Telemetry from production environments reveals that databases average approximately 10 branches, with some reaching depths exceeding 500 iterations.

Traditional databases lack efficient mechanisms for branching database states. Lakebase addresses this gap through O(1) metadata copy-on-write branching at the storage layer, enabling near-instantaneous, cost-free database branching alongside code branching.

---

## Cost Sensitivity

While overall software value increases, individual application value decreases as development costs plummet. Many agent-generated services are small internal tools, prototypes, or narrow workflows running occasionally or handling bursty, event-driven loads.

Production data shows approximately half of agentic applications have database compute lifetimes under 10 seconds. Traditional databases with fixed operational overhead and baseline pricing become economically unjustifiable for these ephemeral, low-value applications.

Lakebase's serverless, elastic architecture automatically scales compute based on load within subseconds and scales to zero during idle periods, eliminating cost floors and achieving near-zero idle expenses.

---

## Growing From Small to Large

A critical architectural challenge emerges from agent-driven development: determining which small, experimental databases will eventually require massive production scale is impossible to predict in advance.

Database systems must support seamless, elastic growth from minimal-cost instances to heavy-traffic production systems without requiring manual re-platforming, provisioning, or complex migrations. This seamless scalability becomes a fundamental architectural requirement rather than an optional feature.

---

## Open Source Ecosystems

AI models trained on extensive public source code repositories have deep familiarity with open-source ecosystems, APIs, and error semantics. Databases like Postgres, embedded throughout training data, benefit from this advantage.

For agent-driven development, openness transcends philosophical preference—it becomes a practical operational requirement for reliable automation. This requirement extends beyond query interfaces to the storage layer itself.

Lakebase builds upon Postgres while advancing openness further: storing data in standard, open Postgres page formats directly in cloud object storage allows agents, external analytical engines, and new tools to interact with data natively.

---

## Databases for the Agentic Era

Evidence of this transformation appears in Databricks's Lakebase service: "AI agents now create roughly 4x more databases than human users."

This statistic encapsulates the broader trends—agents prolifically create database environments for experiments, branching, and testing, then discard them when complete. Supporting this pattern economically and operationally demands infrastructure built specifically for this reality.

Properties once considered merely desirable—cost efficiency, agility, and openness—have become fundamental requirements. Databases imposing high cost floors, lacking branching primitives, or locking data in proprietary formats increasingly fall out of step with contemporary software development practices.

Lakebase was architected for these specific economic and technical realities: zero-cost evolutionary branching, true scale-to-zero elasticity, open Postgres storage on the lake, and self-managing operations.
