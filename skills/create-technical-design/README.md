# create-technical-design

`create-technical-design` supports Stage 03 — Engineering Analysis. It helps Technical Architects and Senior Developers research an approved change and produce one evidence-based technical design package before implementation begins.

## Intended users

The primary users are Technical Architects and Senior Developers. Architect review remains mandatory, with security, DBA, operations, domain, and QA input where relevant.

## Inputs

The skill requires:

- one or more approved Jira Stories;
- the complete acceptance criteria for every Story;
- evidence that the backlog is approved for Engineering Analysis.

Supporting inputs may include approved BRDs and FRDs, workflow and architecture diagrams, Confluence pages, authoritative Swagger/OpenAPI specifications, repository or source snapshots, configuration, deployment manifests, and security or operational documentation.

If Stories or acceptance criteria are inaccessible, the skill stops. If approval is unclear, it produces a provisional analysis only after the user explicitly authorizes that limitation.

## Required and optional research capabilities

Connected Atlassian MCP Jira and Confluence search/read capabilities are required. The authoritative Swagger/OpenAPI contract must be readable when an API exists or may be affected. All research is read-only.

Official DeepWiki MCP repository intelligence is optional. When available, the skill researches only a small, relevant repository shortlist and validates design proposals against retrieved evidence. When unavailable, it continues without blocking the design, states that repository research was unavailable, marks implementation-specific details **Proposed** or **Unknown**, and identifies later repository verification.

DeepWiki does not replace Jira, Confluence, BRD/FRD, workflow, Swagger/OpenAPI, or supplied implementation evidence.

## Output

The skill produces one Markdown technical design package containing:

- requirements traceability and cross-layer impact analysis;
- an Existing Architecture Summary when repository evidence is available;
- high-level and low-level design with justified decisions and alternatives;
- explicit API compatibility and database schema-change determinations;
- security, performance, observability, deployment, and testability notes;
- implementation risks, architecture-material open questions, and an Architect review checklist;
- useful Mermaid diagrams and DBML only when a schema change exists.

The package finishes with:

**Ready for Architect Review**

**No implementation should begin until the design is reviewed.**

## Read-only and review guardrails

The skill never creates implementation code, SQL migrations, infrastructure code, test automation, or patches. It never modifies or publishes to Jira, Confluence, repositories, files, API portals, databases, or deployment systems. It does not approve architecture or replace human review.

If a mandatory research capability other than optional DeepWiki is unavailable, the skill stops by default. It may continue only after the user explicitly accepts a prominently labelled **Source-Limited Proposal**.

## Use and distribution

Invoke `/create-technical-design` from the repository root using a supported
coding agent. The `skill-packages` GitHub Actions artifact includes
`create-technical-design.zip` for clients that install packaged skills. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
