# implement-backend-change

`implement-backend-change` is the **Backend Developer** specialist for Stage 05 — In Development. It implements the server-side portion of one approved AMRIT Jira ticket in a Spring Boot API repository.

**This skill changes source files.**

## Purpose

Turn the backend scope of an approved ticket into a minimal, convention-respecting change to services, APIs, domain logic, integrations, validation, persistence integration, error handling, and backend configuration — after inspecting the actual backend source.

## Relationship to `implement-jira-ticket`

`implement-jira-ticket` is the normal Stage 05 entry point. It reads the ticket, researches the knowledge sources, inspects the code, classifies the impacted personas, and invokes this skill only when the ticket actually changes the backend.

```text
implement-jira-ticket
    └── implement-backend-change
        └── write-unit-tests
```

This skill is independently installable and independently invocable for a backend-only change. It does not require the orchestrator at runtime, and the orchestrator does not require it: when this skill is not installed, the orchestrator applies the Backend Developer persona inline.

## When to use it

Use it when the ticket changes server-side behaviour in an AMRIT API repository — services, controllers, endpoints, domain rules, integrations, server-side validation, persistence integration, error handling, or backend configuration.

Do not use it for web UI, Android, schema DDL and migrations, unit-test authoring, or Git and Pull Request work.

## It reads the code itself

The skill never implements from an orchestrator summary, DeepWiki, Confluence, or previous knowledge alone. Before editing it inspects the module layout, the affected controllers, services, repositories, entities, DTOs, validators, the existing endpoint contracts, the persistence mapping, the exception, logging, transaction and security patterns, the neighbouring tests, and the build, lint, and static-analysis configuration.

If the repository is not accessible, it stops rather than implementing from documentation.

## Database boundary

Any real schema change belongs to `implement-database-change` and lives in `AMRIT-DB`. This skill implements only the application-side entities, mappings, queries, DTOs, and validation that use that schema, and it classifies the persistence impact explicitly as no database change, application model or query change only, or database schema change.

## Approved-design boundary

Stage 05 implements the approved Stage 03 technical design; it does not redesign the system. When the actual code shows the approved design cannot be implemented safely as written, the skill stops and reports the discrepancy for design review instead of deviating silently.

## Git, Jira, and approval boundaries

The skill may inspect `git status`, `git diff`, and history. It never creates a branch, commit, push, or Pull Request, never writes to Jira or Confluence, and never claims architecture approval, DBA approval, code review, QA sign-off, or CI results.

## Required capabilities

Read access to Jira, Confluence, and DeepWiki, plus the host's filesystem, repository-editing, and command-execution capabilities. Tool names vary by host and are discovered, not hardcoded. If DeepWiki is unavailable the skill inspects the repository directly and says so.

## Use and distribution

Invoke `/implement-backend-change` from the repository root using a supported coding agent, or let `/implement-jira-ticket` route to it. For a packaged installation, download `implement-backend-change.zip` from the latest release. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
