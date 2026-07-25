# AMRIT SDLC Skills

This repository contains independently installable Claude skills for the AMRIT software development lifecycle.

## Available skill

### `create-brd`

- Lifecycle mapping: Stage 01/12 — Business & Product
- Stage name: BRD
- Primary responsibility: Business Systems Analyst
- Output: **Draft — Pending Human Review**

The skill turns business needs and source material into a structured draft BRD. Mandatory Confluence research is performed through an already-connected Atlassian MCP before drafting. MCP services are externally hosted; this repository stores no MCP endpoints, credentials, tokens, or secrets.

Human review and sign-off by a Business Systems Analyst, Product Manager, and relevant stakeholders remain mandatory. The skill does not review, approve, certify, or publish a BRD automatically.

## Independent installation

Each skill is self-contained. Download only [`skills/create-brd`](skills/create-brd/README.md), retain its folder structure, and install that folder through Claude Desktop's Add Skills flow. It does not depend on root-level files.

See [installation instructions](docs/installation.md) and [lifecycle mapping](docs/lifecycle-mapping.md).

## Future direction

A future `create-frd` skill may consume an approved BRD and produce a more detailed Functional Requirements Document. It is not implemented or supported in this repository.
