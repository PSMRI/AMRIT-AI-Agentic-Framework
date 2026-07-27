# create-technical-design

`create-technical-design` supports AMRIT Engineering Analysis after Product Management has produced an approved backlog. It behaves as a read-first Technical Architect: it researches the existing system, separates evidence from assumptions and proposals, explains architectural decisions, and produces one review-ready technical design package.

## Purpose

The skill helps Technical Architects and Senior Developers decide how an approved change should be implemented before implementation begins. It emphasizes reuse, compatibility, impact, risk, operational readiness, and traceability rather than template completion.

The output status is always:

- **Ready for Architect Review**
- **No implementation should begin until the design is reviewed.**

## Inputs

At least one approved Jira Story is expected. Supporting inputs may include:

- approved BRD and FRD;
- workflow or state diagrams;
- current architecture and module documents;
- Swagger or OpenAPI specifications;
- existing Confluence architecture;
- source repositories and configuration snapshots;
- deployment, integration, security, and operational documentation.

The skill reads every supplied Story and its acceptance criteria. It follows relevant links to approved requirements and supporting evidence when read access is available.

## Output

The skill produces one Markdown technical design package containing:

- executive summary and requirements traceability;
- cross-layer impact analysis;
- an Existing Architecture Summary with repository confidence when repository research is available;
- high-level and low-level design;
- API and automatic database-change analysis;
- security, performance, logging, monitoring, and deployment review;
- QA-oriented testability notes;
- implementation risks and architecture-material open questions;
- useful Mermaid diagrams;
- DBML only when a schema change is required;
- the mandatory Architect review gate.

It does not create separate implementation tickets, source files, migrations, or full QA test cases.

## Workflow

1. Qualify the supplied Stories and approval status.
2. Read all Stories, acceptance criteria, BRD/FRD content, workflows, and architecture sources.
3. Run bounded, focused Confluence research for current architecture, reusable components, standards, integrations, and prior implementations.
4. Inspect the authoritative Swagger/OpenAPI contract.
5. Detect official DeepWiki repository capabilities and, when available, research a small relevant shortlist selected from the repository catalog.
6. Research related Jira implementation work, Epics, duplicates, debt, incidents, and dependencies using read operations only.
7. Inspect supplied source and deployment evidence without changing it.
8. Classify repository findings as Confirmed, Inferred, Proposed, or Unknown and preserve other assumptions and conflicts.
9. Select and justify the smallest compatible design.
10. Validate the design against repository evidence when available.
11. Produce one review-ready package and apply the quality gate.

If a mandatory research capability is unavailable, the skill reports the gap and stops by default. It may produce a prominently labelled source-limited proposal only after the user explicitly accepts that limitation. DeepWiki is optional and is explicitly excluded from this stop condition.

## Research strategy

Research uses focused search-read-refine loops rather than a single broad query. Terms come from Story language, modules, roles, workflows, APIs, services, data entities, integrations, and newly discovered vocabulary. Searches and pages are deduplicated, and the loop stops when evidence is sufficient, no material new information appears, or three rounds are complete.

The skill never treats an undocumented guess as current architecture. It records negative search results, conflicts, obsolete-source signals, and missing evidence. Existing names, contracts, and schemas are used only when directly supported.

## Supported documents

The skill can consume pasted content, uploaded documents, connected Jira issues, Confluence pages, OpenAPI/Swagger files or portals, Mermaid or image-based workflows, architecture documents, and repository evidence that the client can read.

Tool names vary by client. The skill discovers equivalent read capabilities and never assumes a specific Atlassian or API tool name.

## Optional DeepWiki MCP

Official DeepWiki MCP repository research is optional. The skill detects whether suitable read capabilities are exposed by the current host; it does not assume a particular server name or function name.

When available, DeepWiki improves repository-level grounding by identifying relevant layers, components, conventions, similar implementations, and extension points. Repository research remains read-only and is limited to the smallest relevant shortlist. The skill never searches every AMRIT repository by default.

When DeepWiki is unavailable, the skill:

- continues with Jira, BRD/FRD, workflows, Confluence, Swagger/OpenAPI, and supplied evidence;
- states that repository research was unavailable;
- marks exact implementation detail as Proposed or Unknown;
- avoids fake file, class, package, service, and table names;
- retains **Ready for Architect Review** and adds repository verification where needed.

DeepWiki is not packaged with this skill. Users and organizations configure MCP access separately according to the capabilities of their chosen client. Claude Desktop, Claude Code, and other Skills-capable clients may expose MCP capabilities differently; missing DeepWiki access must not block technical-design generation.

## Repository Research Output

- **Confirmed:** Directly supported by retrieved repository evidence.
- **Inferred:** Strongly indicated by repository structure or an established implementation pattern, but not explicitly confirmed.
- **Proposed:** A new recommendation requiring Architect approval.
- **Unknown:** Repository evidence is unavailable or insufficient.

The technical design never upgrades Inferred or Proposed repository details to Confirmed. When research succeeds, the Existing Architecture Summary records repositories inspected, relevant layers, reusable components, similar implementations, likely extension points, limitations, conflicts, and confidence.

## Repository Catalog Maintenance

[references/repository-catalog.md](references/repository-catalog.md) was derived from the central `PSMRI/AMRIT` README. Review it whenever repositories are added, renamed, or retired. Preserve exact GitHub capitalization and update relationships, technology, or local ports only from the central source.

## Examples

- [examples/sample-story-input.md](examples/sample-story-input.md) shows fictional approved healthcare Stories and supporting evidence.
- [examples/sample-design-output.md](examples/sample-design-output.md) shows a condensed review-ready design pattern.
- [examples/sample-db-change.md](examples/sample-db-change.md) shows a schema-change decision and DBML.
- [examples/sample-no-db-change.md](examples/sample-no-db-change.md) shows the required no-schema-change outcome.
- [examples/sample-deepwiki-available.md](examples/sample-deepwiki-available.md) shows focused ECD repository research changing a design toward reuse.
- [examples/sample-deepwiki-unavailable.md](examples/sample-deepwiki-unavailable.md) shows an MMU design completing safely without repository intelligence.

All examples are fictional and intentionally label proposed architecture. They are patterns, not evidence about a real AMRIT deployment.

## Installation

Package the skill from the repository's `amrit-sdlc-skills` directory:

```powershell
python .\scripts\package-skill.py create-technical-design
```

Upload the resulting `create-technical-design.zip` through Claude Desktop's Add Skills flow. The archive must contain one top-level `create-technical-design` folder with `SKILL.md` directly inside it.

An organization-managed connection must provide Confluence and Jira read capabilities. The relevant OpenAPI specification and architecture sources must also be readable for the scope being designed. Official DeepWiki MCP access is optional and configured outside the skill. Never add credentials, MCP URLs, tokens, or private environment configuration to the package.

## Limitations

- The skill cannot compensate for inaccessible Stories, missing acceptance criteria, unavailable current-state evidence, or stale documentation.
- It does not approve architecture or replace Architect, security, DBA, operations, or domain review.
- It does not validate a design through deployment or runtime testing.
- It does not generate code, SQL migrations, infrastructure code, or test automation.
- It never modifies Jira or Confluence and never publishes automatically.
- It cannot provide repository-level certainty when DeepWiki or equivalent supplied repository evidence is unavailable.
- A source-limited proposal remains provisional regardless of its level of detail.
