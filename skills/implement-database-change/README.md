# implement-database-change

`implement-database-change` is the **DBA / Database Engineer** specialist for Stage 04 — In Development. It implements the schema portion of one approved AMRIT Jira ticket in the `AMRIT-DB` repository.

**This skill changes source files in `AMRIT-DB`.**

## Purpose

Classify the database impact explicitly, inspect the existing schema and migration conventions, add the required migration, and publish the schema contract the application side must implement against.

## Relationship to `implement-jira-ticket`

`implement-jira-ticket` routes to this skill only when a real schema change exists, and runs it **before** the backend work because the schema constrains everything above it.

```text
implement-jira-ticket
    ├── implement-database-change    (schema contract)
    └── implement-backend-change     (consumes it)
        └── write-unit-tests
```

The skill is independently installable and independently invocable. When it is not installed, the orchestrator applies the DBA persona inline under the same ownership rule.

## The AMRIT-DB ownership rule

Any authoritative schema change — tables, columns, types, constraints, foreign keys, indexes, sequences, `AMRIT-DB`-owned functions, procedures, views, triggers, reference-data DDL, and accompanying data migrations — is implemented in `AMRIT-DB`, never in an application repository for convenience.

If `AMRIT-DB` is unavailable, the skill creates no local substitute migration. It states exactly what `AMRIT-DB` needs and reports the work as blocked so dependent backend work does not proceed against a schema that does not exist.

## It reads the schema itself

Nothing is proposed before the actual repository is inspected: the migration mechanism, file naming, ordering and versioning from real neighbouring migrations, the existing tables, columns, constraints, indexes and reference data, audit-column and typing conventions, and the application persistence code that will use the schema.

Existing objects are never duplicated, and no name is invented without convention evidence.

## Safety

The skill never edits an already-applied migration, never runs destructive or state-changing operations against a shared, staging, or production database, and never modifies data in a shared environment to demonstrate a change. It states compatibility, deployment ordering, and rollback limits honestly.

## Human review boundary

DBA review is a human responsibility, including any DBA-review requirement established during Stage 03. The skill reports it as outstanding and never claims it. It also never claims architecture approval, code review, or CI results, and never creates a branch, commit, push, or Pull Request.

## Required capabilities

Read access to Jira, Confluence, and DeepWiki, plus the host's filesystem, repository-editing, and command-execution capabilities, with a checked-out `AMRIT-DB`. Tool names are discovered, not hardcoded.

## Use and distribution

Invoke `/implement-database-change` from the repository root using a supported coding agent, or let `/implement-jira-ticket` route to it. For a packaged installation, download `implement-database-change.zip` from the latest release. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
