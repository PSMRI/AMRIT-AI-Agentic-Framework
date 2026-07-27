# Optional DeepWiki Repository Research Guidelines

## Contents

- [Purpose and boundaries](#purpose-and-boundaries)
- [Step 1: Detect capability](#step-1-detect-capability)
- [Step 2: Build the repository shortlist](#step-2-build-the-repository-shortlist)
- [Step 3: Research repository architecture](#step-3-research-repository-architecture)
- [Step 4: Search for similar implementations](#step-4-search-for-similar-implementations)
- [Step 5: Classify repository evidence](#step-5-classify-repository-evidence)
- [Step 6: Feed evidence into the design](#step-6-feed-evidence-into-the-design)
- [Step 7: Validate the proposal](#step-7-validate-the-proposal)
- [Step 8: Handle conflicting evidence](#step-8-handle-conflicting-evidence)
- [Step 9: Fall back safely](#step-9-fall-back-safely)

## Purpose and boundaries

Treat the official DeepWiki MCP as an optional, read-only repository-research capability.

- Prefer the official DeepWiki MCP when applicable tools are available.
- Detect capability from tools exposed by the current host environment.
- Never assume DeepWiki is installed or available.
- Never bind the workflow to a particular local configuration name such as `deepwiki`.
- Never hardcode tool function names; use the capability and schema actually exposed.
- Never attempt to invoke a nonexistent tool.
- Never tell the user to install DeepWiki during normal skill execution.
- Never fail the design solely because DeepWiki is unavailable.
- Never fabricate repository research, components, or source locations.
- Never write to repositories or modify source code.

DeepWiki improves implementation-level grounding. It does not replace Jira, BRD, FRD, workflow, Confluence, or Swagger/OpenAPI research.

## Step 1: Detect capability

Before repository research, inspect the current host's available tool capabilities for official DeepWiki repository read/research operations. Do not infer availability from a remembered server name, configuration file, or another client's setup.

If applicable tools are available, use only read-oriented operations.

If no applicable tools are available:

1. Skip DeepWiki repository research.
2. Continue with Jira, Confluence, BRD/FRD, workflow diagrams, Swagger/OpenAPI, and supplied evidence.
3. State: **Repository research was not available in the current environment.**
4. Mark implementation-specific details **Proposed** or **Unknown**.
5. State where repository verification remains required.
6. Do not invent classes, packages, files, entities, tables, or existing extension points.

DeepWiki absence is not a mandatory-research failure and does not require user authorization for a source-limited design.

## Step 2: Build the repository shortlist

Read [repository-catalog.md](repository-catalog.md). Map the Story to likely repositories using service line, acceptance criteria, approved requirements, Confluence terms, APIs, modules, entities, screens, and integrations.

Start with no more than three primary repositories where practical. Never query every catalog repository merely because it is listed.

Typical shortlists:

- ECD UI feature: `PSMRI/ECD-UI`, `PSMRI/ECD-API`, and optionally `PSMRI/Common-UI` or `PSMRI/Common-API`.
- MMU feature: `PSMRI/MMU-UI`, `PSMRI/MMU-API`, and optionally a relevant shared repository.
- Database change: the relevant application repository and `PSMRI/AMRIT-DB`.
- Deployment or configuration change: the relevant application repository and `PSMRI/AMRIT-DevOps`.

For each selected repository, record the evidence that justified selection. Add another repository only when a discovered dependency or unresolved design question requires it.

## Step 3: Research repository architecture

For each shortlisted repository, answer only design-specific questions raised by the Story. Do not summarize the entire repository.

Investigate, when relevant:

- repository purpose;
- architectural layers;
- module and package boundaries;
- application entry points;
- controllers;
- services;
- repositories or DAOs;
- models and entities;
- DTOs;
- validators;
- mappers;
- shared utilities;
- configuration;
- security patterns;
- logging patterns;
- exception-handling patterns;
- transaction patterns;
- background jobs;
- queues;
- schedulers;
- integrations;
- API structure;
- database-access conventions;
- migration conventions;
- relevant tests;
- similar existing features;
- likely extension points;
- likely impacted modules or files.

Keep a repository research ledger containing repository identifier, questions asked, retrieved evidence, confidence, and unresolved gaps.

## Step 4: Search for similar implementations

Search selected repositories for architecture that resembles the requested behavior:

- similar controllers or endpoints;
- bulk operations;
- validation flows;
- jobs, queues, or schedulers;
- retry and idempotency mechanisms;
- state machines;
- database tables or migrations;
- shared UI components;
- synchronization modules;
- audit logging;
- integration adapters.

Prefer reuse or extension of a suitable existing pattern. Do not propose a new service, module, table, or endpoint merely because it appears cleaner in isolation. Introduce a new component only when no suitable extension point exists or separation is justified by ownership, scale, security, reliability, or another evidenced constraint.

## Step 5: Classify repository evidence

Classify every repository-grounded claim:

- **Confirmed** — directly supported by retrieved repository evidence.
- **Inferred** — strongly indicated by repository structure or an established implementation pattern, but not explicitly confirmed.
- **Proposed** — a new technical recommendation requiring Architect approval.
- **Unknown** — evidence is unavailable or insufficient.

Never present an Inferred or Proposed item as Confirmed. Cite the repository and stable evidence reference when the tool returns one. Do not invent a file path, class name, package, branch, revision, or link.

## Step 6: Feed evidence into the design

Use repository evidence in:

- the Existing Architecture Summary;
- impact analysis;
- current architecture and proposed HLD;
- LLD;
- API and database analysis;
- security and performance reviews;
- implementation risks;
- testability notes;
- likely impacted modules or files.

When research succeeds, include an **Existing Architecture Summary** containing:

- repositories inspected;
- relevant layers and modules;
- reusable components;
- established implementation patterns;
- similar implementations;
- likely extension points;
- known limitations;
- repository conflicts or uncertainties;
- evidence confidence.

Use exact implementation components only when retrieved evidence supports them. Keep Inferred and Proposed elements visibly labelled.

## Step 7: Validate the proposal

After drafting the HLD and LLD, compare the proposal against retrieved repository evidence. Check for:

- duplicated modules or services;
- missed reusable components;
- incorrect layer ownership;
- inconsistent naming;
- API convention violations;
- database or migration convention violations;
- security-pattern violations;
- transaction-pattern violations;
- unsupported class or file references;
- architecture-boundary violations;
- unnecessary cross-service coupling.

Revise the design before presenting it. Record any unresolved mismatch for Architect review.

## Step 8: Handle conflicting evidence

When repository evidence conflicts with Jira, Confluence, Swagger/OpenAPI, BRD, or FRD:

1. Preserve both claims and their references.
2. Explain the architectural consequence.
3. Identify which source appears to represent current implementation.
4. Identify which source represents intended direction.
5. Mark the discrepancy for Architect review.

Treat source/repository evidence as stronger evidence of current implementation behavior. Treat approved architecture documents as stronger evidence of intended architectural direction. Do not silently overwrite intended architecture with an accidental implementation pattern, and do not misdescribe current behavior merely because a document says it should differ.

## Step 9: Fall back safely

When DeepWiki is unavailable, still generate:

- impact analysis;
- conceptual HLD;
- proposed LLD;
- API analysis;
- database analysis;
- security and performance review;
- testability notes;
- risks;
- open questions.

Use these statements where appropriate:

- **Repository research was not available in the current environment.**
- **Implementation-specific components below are proposals and require repository verification.**

Do not claim implementation-level certainty. Do not invent exact names or locations. Add repository verification to the Architect Review Checklist. Preserve the final status:

**Ready for Architect Review**

DeepWiki is an optional confidence enhancer, not a gate.
