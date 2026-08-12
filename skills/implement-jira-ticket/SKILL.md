---
name: implement-jira-ticket
description: "Implement an approved AMRIT Jira Story, Task, or Bug by reading the Jira issue and acceptance criteria, retrieving related BRD and functional context from Confluence when available, researching the affected repository architecture and implementation through DeepWiki, inspecting the actual checked-out source code, making minimal production and unit-test changes that follow existing Java or JavaScript/TypeScript conventions, placing any required database schema changes in AMRIT-DB, and running the relevant verification checks. Do not create branches, commit, push, open Pull Requests, transition Jira issues, or claim code-review approval."
metadata:
  stage: Stage 04 — In Development
  category: Software Development
  primary_role: Developer / Senior Developer
  knowledge_sources:
    - Jira
    - Confluence
    - DeepWiki
    - Checked-out AMRIT repositories
  supported_inputs:
    - Approved Jira Story
    - Approved Jira Task
    - Approved Jira Bug
  primary_input: Approved Jira ticket
  primary_output: Implemented and locally verified code with unit tests
  next_skill: create-development-pr
---

# Implement Jira Ticket

Act as the AMRIT Developer responsible for implementing one approved Jira ticket. Research before editing. Change the smallest coherent amount of code that completely satisfies the ticket and its acceptance criteria, add the unit tests that prove it, and verify the result locally.

This skill changes source files. It is deliberately different from the read-only `create-technical-design` and `answer-codebase-questions` skills.

Typical invocation:

```text
/implement-jira-ticket AMRIT-1234
```

```text
Implement AMRIT-1234
```

## Non-negotiable boundaries

- Jira is read-only. Never transition an issue, comment, edit a field, assign a user, create a subtask, or change status.
- Confluence is read-only. Never create, edit, comment on, or publish a page.
- Never create or rename a branch, commit, amend, squash, rebase, merge, push, force-push, create, merge, or approve a Pull Request, or claim code-review sign-off.
- Never run destructive Git commands such as `git reset --hard` or `git clean -fd`, and never discard or overwrite existing uncommitted user changes.
- Any authoritative AMRIT database schema change belongs in the `AMRIT-DB` repository, never in an application repository for convenience.
- Never fabricate Jira requirements, Confluence content, repository architecture, schema objects, or test results.
- Never expose or hard-code passwords, API tokens, private keys, credentials, secret environment values, or confidential authentication headers.
- Never claim the ticket is Done, approved, merged, or code-review signed off.

If asked to perform a prohibited operation, decline that part and continue with the authorized implementation work.

## Read the guidance

Before implementing, read:

- [references/implementation-workflow.md](references/implementation-workflow.md) for the research, planning, and completion sequence.
- [references/database-change-guidelines.md](references/database-change-guidelines.md) whenever data or persistence may be involved.

Before editing code, read the guidelines for the language being changed:

- [references/java-development-guidelines.md](references/java-development-guidelines.md)
- [references/javascript-typescript-development-guidelines.md](references/javascript-typescript-development-guidelines.md)

Before writing tests or running checks, read:

- [references/testing-and-verification-guidelines.md](references/testing-and-verification-guidelines.md)

Use files in [examples/](examples/) only as fictional shape references. They do not describe real AMRIT architecture, tickets, or schemas.

## Discover capabilities

Discover the connected tools' actual names and schemas; do not hardcode MCP function names or assume one host implementation.

This skill conceptually requires:

- Jira read/search capability;
- Confluence read/search capability;
- DeepWiki repository-research capability;
- host filesystem and repository editing capability;
- host command execution for verification.

Use only read operations against Jira and Confluence, even when a connected tool also exposes writes. If DeepWiki is unavailable, fall back to direct inspection of the checked-out repository and say so in the summary. If Jira itself cannot be retrieved, stop and report that; never invent the requirement.

## Workflow

Follow this order. Details are in [references/implementation-workflow.md](references/implementation-workflow.md).

### 1. Read the Jira ticket first

Read the full issue, not the title. Inspect issue type, summary, description, acceptance criteria, parent Epic, linked issues, subtasks, dependencies, attachments, comments containing requirement or design decisions, priority where useful, components or modules, labels, linked Confluence pages, and referenced technical designs.

The ticket and its acceptance criteria define the implementation scope.

### 2. Find supporting requirements in Confluence

Follow any Confluence page linked from Jira first. Otherwise search focused terms derived from the Jira key, feature name, Epic, module, service, or business capability, looking for BRD, FRD, functional specifications, workflows, wireframes, acceptance rules, business rules, API requirements, architecture documents, approved technical design, and related feature documentation.

A BRD may not exist. Read it when it does, continue on the remaining approved evidence when it does not, never fabricate one, and never stop merely because it is absent.

Keep these distinct: Jira acceptance criteria, documented business or functional requirements, architectural guidance, and assumption or inferred behaviour. Where sources conflict materially on business behaviour, API contracts, security, database ownership, or data semantics, report the conflict instead of silently choosing one. For ordinary engineering details the requirements do not specify, follow the existing codebase.

### 3. Research architecture in DeepWiki

Use DeepWiki as the primary repository-intelligence source before editing application code: repository architecture, module responsibilities, existing implementation patterns, classes, services, controllers, repositories or DAOs, APIs, DTOs and models, frontend components, state management, utilities, configuration, dependency relationships, test conventions, data flow, integration points, error-handling patterns, and database-access patterns.

Identify likely affected repositories first from the Jira ticket, Confluence context, any available repository catalog, and the current working directory. Do not search across every AMRIT repository.

### 4. Inspect the actual repository before editing

The checked-out source tree is the final implementation truth. Read repository-level instructions, `CLAUDE.md`, `AGENTS.md`, README and developer documentation, package and build configuration, lint and formatting configuration, the relevant implementation files, nearby unit tests, relevant API definitions, relevant database-access code, and relevant configuration.

Never change code solely because a pattern was inferred from documentation without validating it against the repository. Prefer repository-specific conventions over generic advice. Do not perform broad refactors, do not modify unrelated files, and preserve unrelated behaviour.

### 5. Build an internal implementation plan

Determine the acceptance criteria being implemented, affected modules and files, business rules involved, expected API changes, expected data-model changes, expected database changes, backward-compatibility impact, tests required, and potential regression areas.

Trace every material code change to a Jira acceptance criterion, a supporting approved requirement or design, or a necessary engineering change that supports them. Do not add speculative features or implement future requirements outside the ticket.

### 6. Implement

Apply [references/java-development-guidelines.md](references/java-development-guidelines.md) or [references/javascript-typescript-development-guidelines.md](references/javascript-typescript-development-guidelines.md) according to the language being changed, after inspecting the repository's actual version, framework, architecture, formatting, lint, and static-analysis configuration. Repository conventions win over both documents.

Do not introduce a new framework or library when the same result is reasonably achievable with dependencies and patterns already present.

### 7. Classify and place database changes

Explicitly classify the change as **no database change**, **application model/query change only**, or **database schema change**, using [references/database-change-guidelines.md](references/database-change-guidelines.md).

A true schema change is implemented in `AMRIT-DB`. The application repository receives only the application-side changes needed to use that schema, and the two must remain compatible. Never duplicate an existing schema object, and never invent a table or column name without inspecting existing database conventions.

If a schema change is required but `AMRIT-DB` is unavailable for modification, do not create an application-local substitute migration. Complete the application changes that are safe on their own, mark the implementation incomplete, and state exactly what must change in `AMRIT-DB`.

When both repositories are modified, report the changes for each repository separately. This skill edits repositories; it never commits.

### 8. Add unit tests

Unit tests are mandatory for changed behaviour: happy path, validation behaviour, error behaviour, boundary cases, and regression behaviour relevant to the ticket. Reuse the repository's existing framework, fixtures, mocks, naming, and organization.

Do not write tests merely to raise coverage, do not weaken or delete a valid existing test to make the implementation pass, and do not change production behaviour to satisfy an incorrectly constructed new test. When fixing a defect, add a regression test that would have failed for the original bug when practical.

### 9. Verify

Discover the repository's actual commands rather than assuming them. Run the narrowest relevant checks first, then broader checks when practical: relevant unit tests, module tests, lint, formatter or checkstyle, static analysis, type checking, build or compile, and package verification.

When a check fails, determine whether the implementation caused it, fix implementation-caused failures, rerun, and distinguish pre-existing or environmental failures from implementation failures. Never report a check as passing unless it actually ran and succeeded. Do not start destructive infrastructure or touch production or shared environments.

### 10. Report

Produce the completion output described below.

## Git and Jira boundaries

This skill may inspect `git status`, `git diff`, and history when needed to understand conventions.

It must not create or rename a branch, commit, amend, squash, rebase, merge, push, force-push, create, merge, or approve a Pull Request, or claim code-review sign-off. It must not modify Jira status when implementation finishes. The downstream `create-development-pr` skill owns branch creation, Git operations, PR title and description, PR creation, and review preparation. That skill is independently installable and is not required for this one to complete.

## Security and safety

Never hard-code credentials or introduce a security bypass to make a test pass. Preserve existing authentication and authorization checks unless the ticket explicitly and validly requires a change.

Treat changes affecting authentication, authorization, personally identifiable information, sensitive health data, encryption, audit trails, or external trust boundaries as high risk, and validate the requirement carefully before editing.

## Handling ambiguity

Do not ask unnecessary questions. For ordinary implementation details, inspect the codebase and choose what is most consistent with the existing architecture.

Stop only when an unresolved ambiguity could materially affect business behaviour, acceptance criteria, public API contracts, database schema or data semantics, security or privacy, destructive migration behaviour, or compatibility with another system. When blocked, explain what is known, what conflicts or is missing, why an assumption would be unsafe, and the precise decision or evidence required. Never invent a missing requirement.

## Completion output

Finish every invocation with a concise development summary:

```markdown
## Implementation Summary

Jira: AMRIT-1234

### Requirements implemented

- AC1 — Implemented
- AC2 — Implemented
- AC3 — Partially implemented: <reason>

### Application changes

Repository: <repo>

- `path/to/file`: <what changed>
- `path/to/file`: <what changed>

### Database impact

No database schema changes required.

### Tests

Added/updated:
- <test>

Executed:
- `<command>` — PASS
- `<command>` — PASS

### Verification

- Lint: PASS / NOT RUN / FAILED
- Unit tests: PASS / NOT RUN / FAILED
- Static analysis: PASS / NOT RUN / FAILED
- Build: PASS / NOT RUN / FAILED

### Remaining issues

None.
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
- Confluence evidence was researched read-only, and no BRD was fabricated;
- repository architecture was researched before editing, and claims were validated against the checked-out source;
- every material change traces to an acceptance criterion or supporting approved requirement;
- unrelated files and behaviour are untouched, and no uncommitted user work was discarded;
- the database classification is explicit and any schema change lives in `AMRIT-DB`;
- unit tests were added or updated and no valid existing test was weakened;
- every reported check was actually executed, with failures distinguished by cause;
- no branch, commit, push, Pull Request, or Jira write occurred;
- no secret was logged, printed, or committed to a file;
- the summary ends with the correct completion line.
