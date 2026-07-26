# AMRIT SDLC Skills

This repository contains independently installable Claude skills for the AMRIT software development lifecycle.

## Available skills

### `create-brd`

- Lifecycle mapping: Stage 01/12 - Business & Product
- Stage name: BRD
- Primary responsibility: Business Systems Analyst
- Output: **Draft - Pending Human Review**

The skill turns business needs and source material into a structured draft BRD. Mandatory Confluence research is performed through an already-connected Atlassian MCP before drafting. Human review and sign-off remain mandatory; the skill does not approve, certify, or publish automatically.

### `create-product-backlog`

- Lifecycle mapping: Stage 02 - Product Backlog Creation
- Primary responsibility: Product Manager
- Output: **Draft - Pending Product Manager Review**

The skill converts an approved BRD or FRD, or an L2-escalated production defect, into a traceable backlog of Epics, Stories, Tasks, or Subtasks. It performs relevant read-only Confluence and Jira research, validates Stories against INVEST, proposes priority with context, and keeps Jira read-only throughout drafting and refinement.

Jira writes require both explicit approval or finalization of the specific backlog and a separate explicit publication request. Production defects preserve **CAPA required at closure** without inventing root cause or CAPA findings.

### `create-technical-design`

- Lifecycle mapping: Stage 03 - Engineering Analysis
- Primary responsibility: Technical Architect / Senior Developer
- Output: **Ready for Architect Review**

The skill researches every approved Story and acceptance criterion, linked BRD/FRD content, current Confluence architecture, Swagger/OpenAPI contracts, related Jira work, and available repository evidence before proposing a design. It produces one traceable technical design package covering impact, HLD, LLD, APIs, automatic database-change analysis, security, performance, operations, testability, and implementation risks.

The skill is strictly read-only. It generates no implementation code, never modifies Jira or Confluence, never publishes automatically, and requires Architect review before implementation.

MCP services are externally hosted; this repository stores no endpoints, credentials, tokens, or secrets.

## Independent installation

Each skill is self-contained. Download [`skills/create-brd`](skills/create-brd/README.md), [`skills/create-product-backlog`](skills/create-product-backlog/README.md), or [`skills/create-technical-design`](skills/create-technical-design/README.md), retain its folder structure, and install only that folder through Claude Desktop's Add Skills flow. No skill depends on root-level files or another skill at runtime.

See [installation instructions](docs/installation.md) and [lifecycle mapping](docs/lifecycle-mapping.md).

`create-product-backlog` may consume an approved output from `create-brd`, but it can also consume any supported approved source independently.

`create-technical-design` may consume approved Stories from `create-product-backlog`, but it accepts approved backlog Stories and supporting evidence produced through any compatible process.
