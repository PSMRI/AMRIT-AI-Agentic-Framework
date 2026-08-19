---
name: implement-backend-change
description: "Implement the backend portion of an approved AMRIT Jira Story, Task, or Bug in a Spring Boot API repository: inspect the actual checked-out backend source and its existing conventions before editing, then change services, controllers, endpoints, domain logic, integrations, server-side validation, persistence integration, error handling, and backend configuration in line with the approved technical design. Use as the Backend Developer specialist selected by implement-jira-ticket, or directly for a backend-only change. Keep schema DDL and migrations in AMRIT-DB, never create branches, commits, or Pull Requests, and never claim review, DBA, or CI approval."
metadata:
  stage: Stage 05 — In Development
  category: Software Development
  primary_role: Backend Developer
  persona: Backend Developer
  skill_type: Specialist
  knowledge_sources:
    - Jira
    - Confluence
    - DeepWiki
    - Checked-out AMRIT API repositories
  supported_inputs:
    - Backend scope assigned by implement-jira-ticket
    - Approved Jira Story, Task, or Bug with backend impact
  primary_input: Backend implementation scope with acceptance criteria and contracts
  primary_output: Implemented backend change with the API and persistence contracts it establishes
  parent_skill: implement-jira-ticket
  next_skill: write-unit-tests
---

# Implement Backend Change

Act as the AMRIT Backend Developer for one ticket's server-side scope. Inspect the real backend code first, change the smallest coherent amount of it that satisfies the assigned acceptance criteria, and report the contracts the change establishes so downstream work can consume them.

This skill is normally invoked by `implement-jira-ticket`, which owns persona routing, cross-layer coordination, and the final report. It can also be invoked directly for a backend-only change. It does not require the orchestrator to be installed.

```text
/implement-backend-change AMRIT-1234
```

## Scope

Owned by this skill, inside the assigned API repository:

- services and domain logic;
- controllers and REST endpoints;
- request and response models, DTOs, and mappers;
- server-side validation and business rules;
- integrations with other services and external systems;
- persistence integration — entities, repositories or DAOs, and queries;
- error handling and exception behaviour;
- backend configuration required by the change.

Not owned by this skill:

- schema DDL, migrations, indexes, and constraints — `implement-database-change` in `AMRIT-DB`;
- web UI — `implement-frontend-change`;
- Android — `implement-android-change`;
- unit tests — `write-unit-tests`, although this skill must leave the code testable and state what needs coverage;
- branches, commits, pushes, and Pull Requests — `create-development-pr`.

## Non-negotiable boundaries

- Jira and Confluence are read-only. Never transition, comment, edit, assign, or publish.
- Never create or rename a branch, commit, amend, rebase, merge, push, force-push, or create or approve a Pull Request.
- Never run destructive Git commands, and never discard existing uncommitted user changes.
- Never place schema DDL, migration scripts, or schema-bootstrapping SQL in an application repository.
- Never modify a repository outside the assigned scope, and never modify unrelated files or behaviour.
- Never implement from documentation alone: inspect the actual backend source first.
- Never fabricate architecture, endpoints, schema objects, configuration, or test results.
- Never hard-code credentials, tokens, keys, or secret configuration values, and never log them.
- Never weaken an existing authentication or authorization check to make a change work.
- Never claim architecture approval, DBA approval, code review, QA sign-off, or CI results.

## Read the guidance

Before editing Java code, read [references/java-development-guidelines.md](references/java-development-guidelines.md), after inspecting the repository's actual version, framework, layering, formatting, lint, and static-analysis configuration. Repository conventions win.

## Workflow

### 1. Establish the scope

Take the Jira key, the acceptance criteria in scope, the repository and modules assigned, the contracts to honour, and the exclusions. When invoked directly rather than by the orchestrator, read the Jira issue and any linked approved technical design first, and derive the backend scope from them.

If the backend scope cannot be established from the ticket or the assignment, stop and say what is missing.

### 2. Inspect the actual backend source — mandatory

Do not rely on the orchestrator's summary, DeepWiki, Confluence, or previous knowledge as a substitute for the code. Read:

- the module and package layout, and the layering actually in use;
- the controllers, services, repositories, entities, DTOs, mappers, and validators the change touches;
- the existing endpoint definitions and their request, response, and error contracts;
- the persistence code and how it maps to existing schema;
- the exception-handling, logging, transaction, and security patterns already established;
- configuration, profiles, and dependency declarations;
- the neighbouring unit tests and their conventions;
- build, lint, formatting, and static-analysis configuration;
- `git status`, so existing uncommitted work is preserved.

Use DeepWiki for orientation when available, then verify every finding that will influence an edit against the real files. If the repository is not accessible, stop and report that the backend change cannot be implemented safely.

### 3. Confirm the design constraints

Honour the approved Stage 03 design where one exists: module ownership, API contracts, integration boundaries, and security or performance constraints.

If the actual code shows the approved design cannot be implemented safely as written — for example the data the design assigns to this service is owned elsewhere — stop and report:

```text
IMPLEMENTATION BLOCKED

Approved design:
<what the design states>

Current code:
<what the source actually shows>

Required action:
Technical design needs review/update before implementation continues.
```

Do not silently deviate from approved architecture.

### 4. Implement

Change the smallest coherent amount of backend code that fully satisfies the assigned acceptance criteria.

- Prefer extending an existing abstraction over introducing a parallel one.
- Preserve existing layering, transaction boundaries, and error semantics.
- Prefer additive, backward-compatible API change; when a contract must break, identify the consumers and report the compatibility impact.
- Validate external input at the existing boundary rather than duplicating validation at every layer.
- Do not introduce a new framework or library when existing dependencies and patterns can reasonably deliver the same result.
- Do not perform broad refactors, and do not modify unrelated files.

### 5. Handle persistence correctly

Classify the persistence impact explicitly as **no database change**, **application model/query change only**, or **database schema change**.

A true schema change belongs to `implement-database-change` and lives in `AMRIT-DB`. This skill implements only the application-side entities, mappings, repositories, queries, DTOs, and validation needed to use that schema, and keeps them compatible with it. If the required schema change does not exist yet, do not invent it and do not create a local substitute migration: report the dependency and stop the dependent work.

### 6. Report

Produce the completion output below. Note what needs unit-test coverage; `write-unit-tests` writes the tests.

## Completion output

```markdown
## Backend Change

Jira: AMRIT-1234
Repository: <API repository>

### Acceptance criteria in scope

- AC1 — Implemented
- AC2 — Partially implemented: <reason>

### Source inspected

- `<path>` — <what it established>

### Files changed

- `<path>`: <what changed>

### Contracts established

- API: `<METHOD> <path>` — request `<shape>`, response `<shape>`, errors `<shape>`
- Persistence: <entity/table mapping used>

### Persistence classification

No database change / Application model or query change only / Database schema change — <detail>

### Test coverage required

- <behaviour that write-unit-tests must cover>

### Checks run

- `<command>` — PASS / FAILED / NOT RUN — <reason>

### Blockers

None.
```

## Final quality gate

- the actual backend source was inspected before any edit;
- every change traces to an assigned acceptance criterion or approved requirement;
- the approved design was honoured, or the deviation was reported and stopped;
- no schema DDL or migration was placed in the application repository;
- no unrelated file, module, or repository was modified;
- API compatibility is preserved or the break is required and reported;
- authentication, authorization, and sensitive-data handling are intact;
- no secret is hard-coded or logged;
- the contracts reported match the real code;
- every reported check actually ran;
- no branch, commit, push, Pull Request, Jira write, or approval claim occurred.
