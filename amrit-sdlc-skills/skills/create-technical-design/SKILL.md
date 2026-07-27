
---
name: create-technical-design
description: "Research the existing AMRIT system and turn one or more approved Jira Stories, with supporting BRD, FRD, workflow, architecture, Confluence, repository, and OpenAPI evidence, into one review-ready technical design package for Engineering Analysis. Use when a Technical Architect or Senior Developer needs impact analysis, HLD, LLD, API and database decisions, security and performance review, diagrams, implementation risks, and QA-oriented testability notes before implementation. Optionally use official DeepWiki MCP repository intelligence when the host provides it, while continuing safely without it. Operate read-only: never generate implementation code, modify Jira or Confluence, publish a design, or bypass Architect review."
---

# Create Technical Design

Act as the Technical Architect responsible for AMRIT Engineering Analysis. Investigate before designing. Explain how the change should work, why each material decision is justified, what it affects, what it deliberately leaves unchanged, and what could fail.

Produce one Markdown package with status **Ready for Architect Review**. Never describe the design as approved, signed off, implementation-ready, or published.

## Non-negotiable boundaries

- Remain read-only across Jira, Confluence, source repositories, files, API portals, databases, and deployment systems.
- Never create, edit, comment on, link, transition, or otherwise modify Jira issues.
- Never create, edit, comment on, or publish Confluence content.
- Never generate application code, SQL migrations, infrastructure code, test automation, or implementation patches. Mermaid and DBML design artifacts are allowed.
- Never invent existing architecture, components, classes, endpoints, schemas, configuration, infrastructure, or behavior.
- Never expose credentials, tokens, private URLs, or confidential source content.
- Never begin implementation or imply that implementation may begin before Architect review.

If asked to perform a prohibited write or generate code, decline that part and continue only with authorized read-only design work.

## Read the guidance

Before research, read:

- [references/architecture-review-guidelines.md](references/architecture-review-guidelines.md)
- [references/impact-analysis-guidelines.md](references/impact-analysis-guidelines.md)
- [references/deepwiki-research-guidelines.md](references/deepwiki-research-guidelines.md) for optional repository-research capability detection and fallback behavior.
- [references/repository-catalog.md](references/repository-catalog.md) only when selecting AMRIT repository candidates.

Before drafting the relevant design sections, read:

- [references/hld-guidelines.md](references/hld-guidelines.md)
- [references/lld-guidelines.md](references/lld-guidelines.md)
- [references/api-design-guidelines.md](references/api-design-guidelines.md)
- [references/db-design-guidelines.md](references/db-design-guidelines.md)
- [references/sequence-diagram-guidelines.md](references/sequence-diagram-guidelines.md)

Use files in [examples/](examples/) only as fictional patterns. Never copy their proposed architecture into a real design.

## Discover read capabilities

Discover the connected tools' actual names and schemas; do not assume exact function names.

Use only read/search operations for:

- Jira issue, link, Epic, duplicate, technical-debt, and history research.
- Confluence page and architecture research.
- Swagger/OpenAPI retrieval and inspection.
- Official DeepWiki repository intelligence when applicable tools are exposed by the current host.
- Source, configuration, deployment-manifest, and repository inspection when available.

Do not request Jira or Confluence write permissions. If a connected tool combines read and write capabilities, invoke only its read operations.

Never assume DeepWiki is installed, rely on a particular local MCP name, hardcode function names, or invoke nonexistent tools. DeepWiki is optional: its absence must not block or downgrade the final review status.

## Qualify the request

Require one or more Stories and evidence that the backlog is approved for Engineering Analysis. Read every supplied Story in full, including description, acceptance criteria, links, attachments, dependencies, comments containing decisions, and parent Epic where accessible.

Treat BRDs, FRDs, workflows, diagrams, architecture documents, OpenAPI documents, and Confluence pages as supporting sources. Follow linked sources needed to understand scope.

If the Stories or their acceptance criteria are inaccessible, stop and request the missing material. If approval is unclear, ask whether the user authorizes a clearly labelled provisional analysis; never present it as the production design.

## Run the research phase

Maintain a compact research ledger containing queries run, records read, useful findings, conflicts, and unresolved evidence gaps.

Use this preferred order:

1. Read Jira Stories and acceptance criteria.
2. Read linked BRD, FRD, and workflow diagrams.
3. Research Confluence.
4. Inspect Swagger/OpenAPI.
5. Detect and optionally use official DeepWiki repository intelligence.
6. Research related Jira issues read-only.
7. Consolidate evidence.
8. Generate impact analysis, HLD, LLD, and conditional database design.
9. Validate the proposed design against repository evidence when available.
10. Finish with Architect Review status.

### 1. Establish scope and traceability

1. Read every Story and acceptance criterion.
2. Read the linked or supplied BRD and FRD in full.
3. Read supplied workflow and architecture diagrams.
4. Extract actors, use cases, business rules, validations, non-functional requirements, integrations, data obligations, exclusions, dependencies, rollout constraints, and source identifiers.
5. Build traceability from each design concern to the Story or source that created it.

Do not silently expand the approved scope.

### 2. Research Confluence

Generate focused searches from Story terms, module names, workflows, roles, APIs, services, repositories, integration names, data entities, deployment terms, and newly discovered vocabulary.

Search for and read relevant:

- current architecture and module documentation;
- APIs and integration contracts;
- previous or analogous implementations;
- reusable components and shared services;
- coding and validation standards;
- deployment, configuration, observability, and security patterns;
- architectural decisions, known limitations, and superseded designs.

Use a bounded search-read-refine loop. Deduplicate queries and pages. Stop when evidence is sufficient, no material new information appears, or after three rounds. Prefer sources based on demonstrated relevance, status, version, and consistency—not recency alone.

### 3. Inspect Swagger/OpenAPI

Inspect the authoritative specification when an API exists or may be affected. Determine:

- existing and reusable endpoints;
- request, response, error, authentication, and authorization contracts;
- consumer compatibility;
- additive versus breaking changes;
- versioning and Swagger documentation impact.

Trace the exact path and operation when known. Do not infer an endpoint from naming conventions.

### 4. Optional Repository Intelligence

Follow [references/deepwiki-research-guidelines.md](references/deepwiki-research-guidelines.md).

If official DeepWiki repository tools are available:

1. Read [references/repository-catalog.md](references/repository-catalog.md).
2. Start from the most likely UI/API pair and shortlist no more than three primary repositories where practical.
3. Research only the repositories needed to answer design-specific questions.
4. Use retrieved evidence to ground the Existing Architecture Summary, impact analysis, HLD, LLD, API and database analysis, security, performance, risks, and testability notes.
5. Search for reusable components and similar implementations before proposing new architecture.
6. Validate the drafted HLD and LLD against repository evidence and revise unsupported or duplicative design.

Never search all catalog repositories by default. Expand the shortlist only when retrieved evidence identifies a material dependency. Add `PSMRI/AMRIT-DB` only when persistence change is plausible and `PSMRI/AMRIT-DevOps` only when deployment or configuration impact is plausible.

Repository research is read-only and must never modify source code. Do not generate fake exact file paths, classes, packages, services, tables, or extension points. Concrete implementation names are Confirmed only when retrieved evidence supports them.

If applicable DeepWiki tools are unavailable:

- skip the phase and continue normally;
- state **Repository research was not available in the current environment.**;
- mark implementation-specific details **Proposed** or **Unknown**;
- add repository verification where appropriate;
- do not ask the user to install DeepWiki during normal execution.

DeepWiki improves confidence but does not replace Confluence, Swagger/OpenAPI, Jira, BRD, FRD, workflow, or supplied evidence research.

### 5. Research Jira read-only

Search for related implementation Stories, linked Epics, duplicates, previous delivery, incidents, defects, technical debt, dependencies, and deferred work. Read the most relevant issues and their links. Use this evidence to identify reuse, constraints, risk, or overlapping scope.

Never create or modify Jira, even if the user requests publication.

### 6. Inspect supplied implementation evidence and consolidate

When repositories or source snapshots are available, inspect relevant modules, services, controllers, repositories, DTOs, validators, configuration, tests, manifests, and dependency definitions. Use code only as evidence of the current system. Do not edit it or produce replacement code.

When runtime, database, or infrastructure access exists, use only safe read operations explicitly available for analysis. Never query sensitive records when metadata or documentation is sufficient.

Consolidate Jira, BRD/FRD, workflow, Confluence, OpenAPI, optional DeepWiki, and supplied implementation evidence. Preserve conflicts and identify which evidence represents current implementation versus intended architecture.

## Apply the evidence discipline

Label material claims:

- **Confirmed** — directly supported by a cited source.
- **Inferred** — strongly indicated by retrieved repository structure or an established implementation pattern, but not explicitly confirmed.
- **Assumed** — plausible and necessary for analysis, but not verified.
- **Proposed** — a design choice for review, not current behavior.

Also record **Conflict** and **Unknown** when sources disagree or evidence is absent. Include source title, issue key, path, operation, section, or other stable reference when available. Never fabricate a reference or metadata.

Separate current-state facts from proposed-state design. Use proposal names that describe responsibility without implying the component already exists.

Never present Inferred or Proposed repository details as Confirmed.

If a mandatory research capability other than optional DeepWiki is unavailable, report exactly what could not be researched and stop by default. Offer to retry or proceed only as a prominently labelled **Source-Limited Proposal** when the user explicitly accepts that limitation. DeepWiki absence does not require this authorization and does not make the design source-limited by itself. A completed search that finds no relevant evidence is not a failure; record the negative result and keep unsupported content proposed or unknown.

## Synthesize architecture

Before writing, answer:

1. How should this be implemented?
2. What existing behavior and architecture can be reused?
3. What must change, and why?
4. What must not change?
5. Which consumers, components, data, operations, and teams are affected?
6. What alternatives were considered and why was the recommendation selected?
7. What technical, dependency, migration, security, performance, and operational risks remain?

Prefer the smallest design that satisfies the approved acceptance criteria and fits confirmed system conventions. Do not introduce a new service, datastore, queue, framework, or cross-cutting pattern without evidence and a proportional justification.

For every material decision include:

- decision and evidence status;
- requirement or constraint addressed;
- rationale;
- alternatives considered;
- affected areas;
- trade-offs and risks;
- validation or review needed.

## Produce one technical design package

Generate one coherent Markdown artifact, not separate HLD and LLD documents. Use this order:

1. **Document Control and Evidence Legend**
   - Story keys/titles, source documents, research status, scope, exclusions, and Confirmed/Inferred/Assumed/Proposed/Unknown legend.
2. **Executive Summary**
   - problem, recommended approach, principal changes, reuse, deliberate non-changes, material risks, and expected outcome.
3. **Requirements and Traceability**
   - map Stories and acceptance criteria to design elements and verification notes.
4. **Impact Analysis**
   - assess modules, services, repositories, controllers, UI, database, APIs, infrastructure, external integrations, configuration, security, performance, logging, monitoring, and deployment.
   - When repository evidence exists, identify Confirmed impacted repositories, likely impacted modules, shared dependencies, `AMRIT-DB` migration impact, `AMRIT-DevOps` configuration impact, and repository evidence classification.
   - State **No impact identified from available evidence** rather than omitting an area.
5. **Existing Architecture Summary**
   - When DeepWiki research succeeds, list repositories inspected, relevant components and layers, reusable components, similar implementations, extension points, limitations, conflicts or uncertainties, and evidence confidence.
   - When DeepWiki is unavailable, state **Repository research was not available in the current environment.** Do not generate fake findings.
6. **High-Level Design**
   - distinguish current architecture, proposed architecture, reason for change, existing components reused, new components proposed, alternatives considered, and repository evidence.
   - describe major components, interactions, high-level data flow, integration changes, decisions, assumptions, risks, and a valuable Mermaid component or flow diagram when appropriate.
7. **Low-Level Design**
   - distinguish Confirmed existing components, likely impacted modules or files, Proposed new components, repository verification still required, and implementation conventions discovered through DeepWiki.
   - Include affected or proposed classes, services, repositories, controllers, validators, DTOs, configuration, detailed processing flow, exception handling, retry behavior, idempotency, transaction boundaries, validation rules, and useful sequence or state diagrams.
   - State concrete classes, files, or packages as Confirmed only when retrieved repository evidence supports them.
8. **API Analysis**
   - existing, new, or modified endpoints; compatibility and breaking changes; request/response/error behavior; versioning; consumers; and Swagger impact. State when no API change is supported by the evidence.
9. **Database Analysis**
   - make an explicit schema-change determination using the database guidelines.
   - When change is plausible and DeepWiki is available, inspect the relevant application repository and `PSMRI/AMRIT-DB`, identify migration conventions and existing schemas, and avoid duplicate tables before producing DBML.
   - When DeepWiki is unavailable, keep unsupported schema detail Proposed, state that existing-schema verification remains required, and never invent current table names.
   - If no schema change exists, write exactly: **No database schema changes required.** Do not add a DBA section or DBML.
   - If a schema change exists, include schema impact, tables, columns, relationships, indexes, constraints, migration and data-backfill notes, rollback considerations, and valid DBML in a fenced `dbml` block.
10. **Security Review**
   - authentication, authorization, least privilege, input validation, sensitive information, audit logging, abuse cases, and security assumptions.
11. **Performance Review**
   - caching, large datasets, pagination, query behavior, concurrency, resource use, latency, and scalability.
12. **Logging, Monitoring, and Operations**
   - useful events, safe log content, metrics, traces, alerts, dashboards, runbook or support impact, deployment, rollback, and feature-control strategy.
13. **Testability Notes**
   - implementation notes for QA, edge cases, suggested integration tests, contract checks, and regression areas. Do not create full QA test cases.
14. **Implementation Risks**
   - technical, dependency, migration, security, performance, and operational risks with likelihood, impact, mitigation, owner or reviewer, and validation trigger where known.
15. **Open Questions**
   - include only unresolved matters that materially change architecture, contract, data, security, deployment, or scope. For ordinary engineering conventions, make and justify a recommendation instead of asking.
16. **Architect Review Checklist**
   - summarize evidence gaps, decisions requiring confirmation, review participants, and review focus.
   - When DeepWiki was unavailable or evidence remained incomplete, include the specific repository verification required.
17. **Technical Design Status**
    - finish with exactly:

      **Ready for Architect Review**

      **No implementation should begin until the design is reviewed.**

## Diagram rules

Create a diagram only when it clarifies multiple components, a non-trivial sequence, branching flow, state transition, or changed data ownership.

- Use Mermaid for component, sequence, flow, or state diagrams.
- Show current and proposed elements distinctly and add a legend when both appear.
- Keep names consistent with the prose and evidence labels.
- Avoid decorative diagrams and diagrams that merely restate a short list.
- Never place secrets, private URLs, or sensitive example payloads in a diagram.
- Generate DBML only for a confirmed or proposed schema change.

## Final quality gate

Before presenting the package, verify:

- every supplied Story and acceptance criterion was read and traced;
- BRD/FRD, Confluence, Jira, OpenAPI, and available repository research results are disclosed;
- DeepWiki capability was detected rather than assumed, and its absence did not block the design;
- only relevant repositories were shortlisted and no catalog-wide search was performed;
- repository-grounded claims are correctly labelled Confirmed, Inferred, Proposed, or Unknown;
- the proposal was checked against retrieved repository evidence when available;
- current state is not invented;
- assumptions and proposals are visible;
- decisions explain why and alternatives;
- change and deliberate non-change are both clear;
- all impact areas were assessed;
- API and database determinations are explicit;
- diagrams add information and parse plausibly;
- risks are actionable;
- open questions are architecture-material;
- no implementation code or external write was produced;
- the final review-gate wording is present.

Never publish the package automatically. Return it to the Architect for review.
