# implement-jira-ticket

`implement-jira-ticket` supports Stage 04 — In Development. It takes one approved AMRIT Jira ticket, researches the requirement and the affected architecture, and implements the change with unit tests in the relevant checked-out repository.

**This skill changes source files.** That makes it intentionally different from the read-only `create-technical-design` and `answer-codebase-questions` skills, which research and document but never edit code.

## Purpose

Turn an approved Jira ticket into a minimal, convention-respecting, locally verified code change with unit tests, ready for a separate skill to prepare the Pull Request.

## When to use it

Use it when:

- a Jira Story, Task, or Bug is approved and sprint-ready with acceptance criteria;
- the relevant AMRIT application repository is checked out;
- implementation is the next step, not analysis or design.

Do not use it to write a technical design, answer a codebase question, create backlog items, or perform Git and Pull Request work.

## Intended users

Developers and Senior Developers. Code review by another engineer remains mandatory and is outside this skill.

## Supported Jira issue types

- Story
- Task
- Bug

## Expected invocation

```text
/implement-jira-ticket AMRIT-1234
```

```text
Implement AMRIT-1234
```

If no ticket key is supplied, the skill asks for one before researching.

## Research order

1. **Jira** — read the full issue: type, summary, description, acceptance criteria, Epic, links, subtasks, dependencies, attachments, decision-bearing comments, priority, components, labels, and linked Confluence pages. Jira is read-only.
2. **Confluence** — follow any linked page first, then search focused terms for BRD, FRD, functional specifications, workflows, wireframes, business rules, API requirements, architecture documents, and approved technical design. Confluence is read-only. A missing BRD does not stop implementation and is never fabricated.
3. **DeepWiki** — the primary repository-intelligence source for architecture, module responsibilities, implementation patterns, APIs, models, components, configuration, test conventions, data flow, and database-access patterns. Only likely affected repositories are researched, never the whole AMRIT estate.
4. **The checked-out repository** — the final implementation truth. Repository instructions, `CLAUDE.md`, `AGENTS.md`, build and lint configuration, the implementation files, and nearby tests are read directly, and any pattern inferred from documentation is validated against the real source before code changes.

## Implementation workflow

1. Read the Jira ticket in full.
2. Research supporting requirements in Confluence.
3. Research the affected repository architecture in DeepWiki.
4. Inspect the checked-out repository.
5. Build an internal plan tracing every change to an acceptance criterion or supporting requirement.
6. Implement the smallest coherent change that fully satisfies the ticket.
7. Classify and place any database change.
8. Add or update unit tests.
9. Run verification, narrowest checks first.
10. Report the completion summary.

Material conflicts affecting business behaviour, API contracts, security, database ownership, or data semantics are reported rather than resolved silently. Ordinary engineering details follow the existing codebase without asking.

## Java and JavaScript/TypeScript expectations

Language conventions come from the repository first — its version, framework, layering, formatting, lint, and static-analysis configuration — and from the skill's references second.

For Java, the skill keeps classes and methods focused, preserves separation of concerns and existing abstractions, uses the project's dependency-injection style, handles nullability intentionally, validates external input at boundaries, avoids swallowed exceptions and unjustified broad `catch (Exception)`, preserves exception causes, avoids logging secrets or sensitive payloads, avoids N+1 and redundant calls, preserves transaction and concurrency behaviour, and keeps public API compatibility unless the requirement changes it. Spring and Spring Boot changes follow the repository's existing layering rather than an imposed structure.

For JavaScript and TypeScript, the skill keeps functions, modules, and components focused, avoids duplicated business logic, handles async paths and rejected promises explicitly, preserves error context, validates data at trust boundaries, uses strict comparison, avoids weakening types with `any`, reuses existing interfaces and the repository's design system, avoids unnecessary re-renders and repeated computation, keeps secrets and sensitive data out of client code and logs, preserves accessibility patterns, and preserves API compatibility.

New frameworks and libraries are not introduced when existing dependencies and patterns can reasonably deliver the same result.

## AMRIT-DB schema ownership rule

Every change is explicitly classified as **no database change**, **application model/query change only**, or **database schema change**.

Any actual schema change — tables, columns, types, constraints, foreign keys, indexes, sequences, `AMRIT-DB`-owned functions or procedures, or reference-data DDL and migrations — is implemented in the `AMRIT-DB` repository. Schema DDL and migration ownership is never moved into an application repository for convenience. The application repository receives only the application-side changes needed to use that schema, and the two must remain compatible.

Existing schema is inspected before anything is proposed, existing objects are never duplicated, and table or column names are never invented without convention evidence.

If a schema change is required but `AMRIT-DB` is unavailable for modification, the skill creates no application-local substitute migration, completes the application changes that are safe on their own, marks the implementation incomplete, and states exactly what must change in `AMRIT-DB`. When both repositories are modified, changes are reported for each repository separately.

## Test and verification behaviour

Unit tests are mandatory for changed behaviour and cover the ticket's happy path, validation, error behaviour, boundary cases, and regression risk. The repository's existing framework, fixtures, mocks, naming, and organization are reused. Valid existing tests are never weakened or deleted to make an implementation pass, and production behaviour is never changed to satisfy an incorrectly constructed test. Defect fixes add a regression test that fails against the original bug where practical.

Verification commands are discovered from the repository, never assumed. Checks run narrowest first — targeted tests, module tests, lint, formatting, static analysis, type checking, build, and package verification where practical. Failures are attributed to the implementation or to pre-existing and environmental causes, implementation-caused failures are fixed and rechecked, and a check is reported as PASS only when it actually ran successfully. Nothing destructive is started, and production or shared environments are never touched.

## Git and Pull Request boundaries

The skill **may** inspect `git status`, `git diff`, and history to understand conventions.

The skill **must not** create or rename a branch, commit, amend, squash, rebase, merge, push, force-push, create, merge, or approve a Pull Request, or claim code-review sign-off. It never transitions the Jira issue or writes to Jira or Confluence, and it never runs destructive Git commands such as `git reset --hard` or `git clean -fd` or discards existing uncommitted work.

Branch creation, Git operations, PR title and description, PR creation, and review preparation belong to the downstream [`create-development-pr`](../create-development-pr/README.md) skill. That skill is independently installable; this one completes without it.

## Example invocation

```text
/implement-jira-ticket DEMO-5140
```

See [examples/](examples/) for fictional inputs and outputs, including a feature, a bug with a partially implemented criterion, and a database change under both available and unavailable `AMRIT-DB` conditions. The examples are illustrative only and do not describe real AMRIT architecture.

## Completion status semantics

Every invocation ends with exactly one of:

- **Implementation complete and locally verified. Ready for PR preparation.** — every acceptance criterion is implemented, unit tests exist for the changed behaviour, and the reported checks actually passed.
- **Implementation incomplete. Resolve the items above before PR preparation.** — something remains unresolved: a criterion is partly implemented, a required `AMRIT-DB` change is missing, a check failed, or a blocking ambiguity was reported.

Neither line means the ticket is Done, approved, merged, or code-review signed off. The skill never makes those claims.

## Required capabilities

The skill conceptually requires read access to Jira, Confluence, and DeepWiki, plus the host's filesystem, repository-editing, and command-execution capabilities. Tool names vary by host, so capabilities are discovered rather than hardcoded. Jira and Confluence writes are never requested or used. Graphify is not required.

If DeepWiki is unavailable, the skill falls back to direct repository inspection and says so. If the Jira issue cannot be retrieved, it stops rather than inventing requirements.

## Use and distribution

Invoke `/implement-jira-ticket` from the repository root using a supported coding agent. Configure local MCP credentials only where the selected client requires them; never commit real tokens.

For a packaged installation, download `implement-jira-ticket.zip` from the latest successful **Validate and package skills** GitHub Actions run and upload or install it with the relevant client workflow. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
