---
name: implement-jira-ticket
description: "Implement an approved AMRIT Jira Story, Task, or Bug by acting as the Stage 05 engineering orchestrator: read the Jira issue and acceptance criteria, retrieve linked BRD, functional, and approved technical-design context from Confluence, research the affected repositories through DeepWiki and the framework's other knowledge sources, inspect the actual checked-out source code before any change, classify the impacted repositories, modules, and engineering personas, then invoke only the relevant specialist skills — implement-database-change, implement-backend-change, implement-frontend-change, implement-android-change, review-implementation-architecture, validate-ux-implementation, and write-unit-tests — in dependency order, verify the result, and report the evidence. Do not create branches, commit, push, open Pull Requests, transition Jira issues, or claim architecture, DBA, code-review, QA, CI, or release approval."
metadata:
  stage: Stage 05 — In Development
  category: Software Development
  primary_role: Developer / Senior Developer (engineering orchestration)
  skill_type: Meta-skill / orchestrator
  knowledge_sources:
    - Jira
    - Confluence
    - DeepWiki
    - Graphify
    - OpenProject
    - Checked-out AMRIT repositories
  supported_inputs:
    - Approved Jira Story
    - Approved Jira Task
    - Approved Jira Bug
  primary_input: Approved Jira ticket
  primary_output: Implemented and locally verified code with unit tests, plus an orchestration report
  specialist_skills:
    - implement-database-change
    - implement-backend-change
    - implement-frontend-change
    - implement-android-change
    - review-implementation-architecture
    - validate-ux-implementation
    - write-unit-tests
  next_skill: create-development-pr
---

# Implement Jira Ticket

Act as the AMRIT engineering orchestrator for one approved Jira ticket. Understand the requirement, research the technical knowledge, **inspect the actual source code**, decide which engineering roles the change really needs, run only those specialists, coordinate the dependencies between them, verify the result, and report what was actually done.

This skill owns coordination, evidence, and verification. It does not own every implementation detail: the specialist skills below own the code in their layer, and each of them inspects its own code before editing.

This skill changes source files, directly or through the specialists it invokes. It is deliberately different from the read-only `create-technical-design` and `answer-codebase-questions` skills.

Typical invocation, unchanged:

```text
/implement-jira-ticket AMRIT-1234
```

```text
Implement AMRIT-1234
```

Users do not select personas by hand. This skill routes the ticket.

## Non-negotiable boundaries

- Jira is read-only. Never transition an issue, comment, edit a field, assign a user, create a subtask, or change status.
- Confluence is read-only. Never create, edit, comment on, or publish a page.
- Never create or rename a branch, commit, amend, squash, rebase, merge, push, force-push, create, merge, or approve a Pull Request, or claim code-review sign-off.
- Never run destructive Git commands such as `git reset --hard` or `git clean -fd`, and never discard or overwrite existing uncommitted user changes.
- Never implement a ticket from documentation alone. Actual source-code inspection is mandatory before any change, in every route.
- Never modify a repository that the impact analysis did not identify as affected, and never modify one merely because a persona exists for it.
- Any authoritative AMRIT database schema change belongs in the `AMRIT-DB` repository, never in an application repository for convenience.
- Never fabricate Jira requirements, Confluence content, repository architecture, schema objects, specialist results, executed commands, or test results.
- Never fabricate or imply architecture approval, DBA approval, code-review approval, QA approval, CI results, or release approval.
- Never expose or hard-code passwords, API tokens, private keys, credentials, secret environment values, or confidential authentication headers.
- Never claim the ticket is Done, approved, merged, or code-review signed off.

If asked to perform a prohibited operation, decline that part and continue with the authorized implementation work.

## Read the guidance

Before orchestrating, read:

- [references/orchestration-workflow.md](references/orchestration-workflow.md) for the full research, routing, coordination, verification, and handoff sequence.
- [references/codebase-inspection-guidelines.md](references/codebase-inspection-guidelines.md) for knowledge-source order and the mandatory source-code inspection rule.
- [references/persona-routing-guidelines.md](references/persona-routing-guidelines.md) for persona selection, specialist invocation, and the fallback when a specialist skill is not installed.

Before planning execution order or writing the report, read:

- [references/coordination-and-verification-guidelines.md](references/coordination-and-verification-guidelines.md)

When identifying affected repositories, read:

- [references/amrit-repository-map.md](references/amrit-repository-map.md)

Use files in [examples/](examples/) only as fictional shape references. They do not describe real AMRIT architecture, tickets, or schemas.

## Discover capabilities

Discover the connected tools' actual names and schemas; do not hardcode MCP function names or assume one host implementation.

This skill conceptually requires:

- Jira read/search capability;
- Confluence read/search capability;
- repository-research capability such as DeepWiki;
- cross-repository relationship research such as Graphify, when a relationship is unresolved;
- delivery-context capability such as OpenProject, when the environment provides it and the ticket is tracked there;
- host filesystem and repository editing capability;
- host command execution for verification;
- the host's mechanism for invoking another skill.

Use only read operations against Jira, Confluence, OpenProject, DeepWiki, and Graphify, even when a connected tool also exposes writes. If a knowledge source is unavailable, continue on the remaining evidence and say so in the report. If the Jira issue cannot be retrieved, stop and report that; never invent the requirement. If the relevant source code cannot be accessed, stop: see [Actual code inspection is mandatory](#actual-code-inspection-is-mandatory).

## Workflow

Follow this order. Details are in [references/orchestration-workflow.md](references/orchestration-workflow.md).

### 1. Read the Jira ticket first

Read the full issue, not the title: issue type, summary, description, acceptance criteria, parent Epic, linked issues, subtasks, dependencies, attachments, decision-bearing comments, priority where useful, components and modules, labels, linked Confluence pages, and referenced technical designs.

The ticket and its acceptance criteria define the implementation scope.

### 2. Read the linked requirements and approved design

Follow any Confluence page linked from Jira first, then search focused terms derived from the Jira key, feature name, Epic, module, service, or business capability. Look for the BRD, FRD, functional specifications, workflows, wireframes, business rules, API requirements, architecture documents, and the **approved Stage 03 technical design**.

An approved technical design is the strongest available statement of intended architecture. Consume it; do not redesign it. A BRD may not exist: read one when it does, continue on the remaining approved evidence when it does not, and never fabricate one.

### 3. Research the technical knowledge

Use the framework's knowledge sources in the order established by `answer-codebase-questions`: DeepWiki first for repository architecture, module responsibilities, major flows, abstractions, integration boundaries, and existing implementation patterns; Confluence for intended architecture and design rationale; Graphify only as the final fallback for unresolved cross-repository relationships.

Research only the repositories the ticket plausibly touches. DeepWiki is context, not truth.

### 4. Inspect the actual source code — mandatory

Read the real files in the checked-out repositories before deciding anything about the implementation. Reconcile what the documentation says the system should do with what the code currently does, and resolve every material discrepancy before editing.

### 5. Determine the impacted repositories, modules, and components

Use the ticket, the approved design, the repository map, and the source inspection to name each affected repository and the modules inside it, and to state explicitly which adjacent repositories are **not** affected.

### 6. Classify the required personas

Select personas from evidence, not from habit. A ticket that touches one layer gets one specialist. See [Persona routing](#persona-routing).

### 7. Build the implementation plan

Before any edit, establish the affected components, the dependencies between them, the execution order, the contracts each specialist must honour — schema shape, API request and response, component inputs and outputs — and the verification each change requires.

Trace every material code change to a Jira acceptance criterion, an approved requirement or design, or a necessary engineering change that supports them.

### 8. Invoke only the relevant specialist skills

Invoke each selected specialist through the host's skill mechanism, passing the ticket key, the acceptance criteria in scope, the repository and module boundaries, the contracts it must honour, the approved-design constraints, and what it must not change.

Give each specialist its boundary, not a summary of the code. Each specialist inspects its own code.

### 9. Coordinate the dependencies

Run specialists in dependency order and re-check the contract after each one. The typical order is database → backend → frontend or Android → unit tests, with architecture review before implementation and UX validation after the user-visible change exists.

If a specialist reports a blocker, stop the dependent work rather than implementing against a contract that does not exist.

### 10. Ensure unit tests exist

Code-level unit tests are mandatory for every changed behaviour. `write-unit-tests` owns them. This is developer testing, not Stage 07 `execute-qa-validation`, and it is distinct from `draft-test-cases`.

`write-unit-tests` also participates in the testing meta-skill `test-jira-ticket`. That does not change its selection here: this orchestrator continues to select it whenever production behaviour changed, ahead of `create-development-pr`.

### 11. Verify

Discover the repository's actual commands rather than assuming them, and run the narrowest relevant checks first: unit tests for changed behaviour, module tests, lint, formatter or checkstyle, static analysis, type checking, build or compile, and migration checks where the repository provides them.

Report a check as PASS only when it actually ran and succeeded. Record `NOT RUN — <reason>` when the environment prevents it.

### 12. Summarize the implementation evidence

Produce the orchestration report below from what actually happened: sources consulted, repositories inspected, personas selected, specialists executed, files changed, checks run with real results, and any architecture deviation.

### 13. Hand off

Finish by naming `create-development-pr` as the next skill. This skill never performs Git or Pull Request work.

## Actual code inspection is mandatory

Documentation answers *what the system is intended to do*. The source code answers *what the system currently does and where the change must actually be made*. Both are required, and the code decides where to edit.

- Never implement a ticket purely from Jira, Confluence, DeepWiki, Graphify, architecture documentation, or previous knowledge.
- Never change code because a pattern was inferred from documentation without validating it against the checked-out repository.
- Reconcile documentation and code explicitly, and report material conflicts rather than silently choosing one.

If the relevant repository or source code cannot be accessed, stop and report:

```text
IMPLEMENTATION BLOCKED

Reason:
The source code for <repository> is not accessible in this environment.

Impact:
The ticket cannot be implemented safely from documentation alone.

Required action:
Provide access to the checked-out repository, then re-run this skill.
```

Do not implement a partial change from documentation while the code is unavailable.

## Persona routing

Routing is dynamic. Select a persona only when the evidence shows its layer is affected.

| Persona | Specialist skill | Select when the evidence shows |
| --- | --- | --- |
| Technical Architect | `review-implementation-architecture` | cross-cutting or cross-repository change, a new component or contract, a changed integration or module boundary, security- or performance-material change, or a possible deviation from the approved Stage 03 design |
| DBA / Database Engineer | `implement-database-change` | a schema object must be created, altered, or removed, or a migration, index, constraint, or data-compatibility concern exists |
| Backend Developer | `implement-backend-change` | server-side services, APIs, controllers, domain logic, integrations, validation, persistence integration, error handling, or backend configuration change |
| Frontend Developer | `implement-frontend-change` | web UI components, state management, API integration, forms, client validation, accessibility, or frontend error handling change |
| Android / Kotlin Developer | `implement-android-change` | the Android applications change, including Kotlin implementation, mobile flows, API integration, offline behaviour, or device and platform constraints |
| UX / UI Specialist | `validate-ux-implementation` | a user-visible change exists and approved wireframes, workflows, or design-system rules must be honoured |
| SDET / developer testing | `write-unit-tests` | production code changed — effectively always |

Rules:

- Never run every specialist by default. An unselected persona must be justified by evidence, and the report states which personas were considered and excluded.
- `write-unit-tests` runs whenever production behaviour changed.
- `review-implementation-architecture` does not re-open an approved Stage 03 design. During Stage 05 it checks conformance.
- `validate-ux-implementation` validates the implementation against approved UX. It does not invent product design when approved UX already exists.
- A persona with no available specialist skill still applies: see the fallback in [references/persona-routing-guidelines.md](references/persona-routing-guidelines.md).

Representative routes:

```text
Backend-only            implement-backend-change → write-unit-tests → verification
Backend + database      implement-database-change → implement-backend-change → write-unit-tests
Full stack              implement-database-change? → implement-backend-change → implement-frontend-change
                        → validate-ux-implementation → write-unit-tests
Android                 implement-android-change → write-unit-tests
Architecturally         review-implementation-architecture → implement-database-change
significant             → implement-backend-change → implement-frontend-change
                        → validate-ux-implementation → write-unit-tests
```

## Repository boundaries

One ticket may affect more than one repository. Name each one and its role, and name the repositories deliberately left untouched:

```text
Affected repositories

<Application-API>
    backend

AMRIT-DB
    database

<Application-UI>
    frontend

<Mobile app>
    no changes
```

Application repositories and `AMRIT-DB` are separate Git repositories. This skill edits files in each; it never commits in any of them.

## Respect the approved technical design

Stage 05 implements the Stage 03 design; it does not replace it. Specialists must not casually redesign the system.

If source inspection shows the approved design cannot be implemented safely as written, stop and surface the discrepancy instead of silently deviating:

```text
IMPLEMENTATION BLOCKED

Approved design:
<what the approved design states>

Current code:
<what the checked-out source actually shows>

Conflict:
<why the design cannot be implemented safely as written>

Required action:
Technical design needs review/update before implementation continues.
```

Complete any independent part of the ticket that is safe to complete, and say exactly what was left out.

## Git and Jira boundaries

This skill may inspect `git status`, `git diff`, and history to understand conventions and to report what changed.

It must not create or rename a branch, commit, amend, squash, rebase, merge, push, force-push, create, merge, or approve a Pull Request, or claim code-review sign-off, and it must not modify Jira when implementation finishes. The downstream `create-development-pr` skill owns branch creation, Git operations, PR title and description, PR creation, and review preparation. That skill is independently installable and is not required for this one to complete. The specialist skills do not perform Git or Pull Request work either.

## Security and safety

Never hard-code credentials or introduce a security bypass to make a test pass. Preserve existing authentication and authorization checks unless the ticket explicitly and validly requires a change.

Treat changes affecting authentication, authorization, personally identifiable information, sensitive health data, encryption, audit trails, or external trust boundaries as high risk, and validate the requirement carefully before editing.

## Human accountability

The agent implements and verifies. Humans approve. Architecture approval, DBA approval, code review, QA sign-off, CI results, and release approval are never produced, implied, or assumed by this skill. When a required approval is absent, report it as absent.

## Handling ambiguity

Do not ask unnecessary questions. For ordinary implementation details, inspect the codebase and choose what is most consistent with the existing architecture.

Stop only when an unresolved ambiguity could materially affect business behaviour, acceptance criteria, public API contracts, database schema or data semantics, security or privacy, destructive migration behaviour, or compatibility with another system. When blocked, explain what is known, what conflicts or is missing, why an assumption would be unsafe, and the precise decision or evidence required. Never invent a missing requirement.

## Completion output

Finish every invocation with the orchestration report:

```markdown
## Implementation Summary

Jira: AMRIT-1234 — <summary>

### Repositories inspected

- <repository> — <modules inspected>
- <repository> — no changes required

### Knowledge sources consulted

- Jira
- Confluence — <what was found, or "no applicable page found">
- DeepWiki — <what was used, or "unavailable">
- Source code — <what was read>

### Personas selected

- Backend Developer — <why>
- DBA — <why>
- SDET — <why>

Considered and excluded: Frontend (<why>), Android (<why>), Architect (<why>), UX (<why>).

### Specialist skills executed

- implement-database-change
- implement-backend-change
- write-unit-tests

### Requirements implemented

- AC1 — Implemented
- AC2 — Implemented
- AC3 — Partially implemented: <reason>

### Files changed

Repository: <repo>

- `path/to/file`: <what changed>

### Database impact

No database schema changes required.

### Tests

Added/updated:
- <test>

Executed:
- `<command>` — PASS

### Verification

- Unit tests: PASS / NOT RUN — <reason> / FAILED
- Lint: PASS / NOT RUN — <reason> / FAILED
- Static analysis: PASS / NOT RUN — <reason> / FAILED
- Build: PASS / NOT RUN — <reason> / FAILED

### Architecture deviation

None.

### Remaining issues

None.

### Next skill

create-development-pr
```

When a schema change exists, replace the database section with:

```markdown
### Database impact

Schema change required.

Repository: AMRIT-DB

- `<path>`: <schema/migration change>

Application repository:

- `<path>`: <corresponding persistence/model change>
```

State anything unresolved explicitly, then finish with exactly one of:

**Implementation complete and locally verified. Ready for PR preparation.**

**Implementation incomplete. Resolve the items above before PR preparation.**

## Final quality gate

Before presenting the summary, verify:

- the full Jira issue and every acceptance criterion were read, and Jira was not modified;
- Confluence and the approved technical design were researched read-only, and no requirement or design was fabricated;
- the actual source code was inspected before any change, and documentation-only implementation did not occur;
- impacted repositories and modules were identified, and no unaffected repository was modified;
- persona selection is evidence-based, and exclusions are stated;
- only the selected specialists ran, in dependency order, with contracts honoured between them;
- every material change traces to an acceptance criterion or supporting approved requirement;
- unrelated files and behaviour are untouched, and no uncommitted user work was discarded;
- the database classification is explicit and any schema change lives in `AMRIT-DB`;
- unit tests were added or updated and no valid existing test was weakened;
- every reported check was actually executed, with failures distinguished by cause;
- no approval, sign-off, or CI result was fabricated or implied;
- no branch, commit, push, Pull Request, or Jira write occurred;
- no secret was logged, printed, or committed to a file;
- the report names `create-development-pr` and ends with the correct completion line.
