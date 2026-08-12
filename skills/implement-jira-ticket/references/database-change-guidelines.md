# Database Change Guidelines

## Contents

- [The AMRIT ownership rule](#the-amrit-ownership-rule)
- [Step 1: Classify the change](#step-1-classify-the-change)
- [What counts as a schema change](#what-counts-as-a-schema-change)
- [What does not count as a schema change](#what-does-not-count-as-a-schema-change)
- [Step 2: Inspect the existing schema](#step-2-inspect-the-existing-schema)
- [Step 3: Implement the schema change in AMRIT-DB](#step-3-implement-the-schema-change-in-amrit-db)
- [Step 4: Implement the application-side change](#step-4-implement-the-application-side-change)
- [Step 5: Keep the two repositories compatible](#step-5-keep-the-two-repositories-compatible)
- [When AMRIT-DB is unavailable](#when-amrit-db-is-unavailable)
- [Reporting database impact](#reporting-database-impact)
- [Review checklist](#review-checklist)

## The AMRIT ownership rule

Any actual database schema change must be implemented in the `AMRIT-DB` repository.

Database schema DDL and migration ownership must not be moved into an application repository merely for convenience. This rule is non-negotiable and applies regardless of how small the change is, how urgent the ticket is, or how much simpler a local migration would be.

An application repository may change how it reads and writes existing schema. It may not become the source of truth for the schema itself.

## Step 1: Classify the change

Whenever implementation appears to require a database change, classify it explicitly as exactly one of:

1. **No database change** — the behaviour uses existing structures and existing queries.
2. **Application model/query change only** — entities, mappings, DTOs, queries, or projections change, but no database object changes.
3. **Database schema change** — a database object must be created, altered, or removed.

State the classification in the completion summary even when the answer is "no database change". Do not equate "the feature uses data" with "the schema must change".

## What counts as a schema change

- creating or dropping tables;
- adding, removing, or renaming columns;
- changing column types, nullability, defaults, or generated values;
- adding or removing database constraints;
- foreign keys;
- indexes;
- sequences;
- database functions or procedures where `AMRIT-DB` owns them;
- views, materialized views, and triggers owned by `AMRIT-DB`;
- reference or master-data DDL and migration changes where `AMRIT-DB` is the source of truth;
- data migrations and backfills that accompany the above.

## What does not count as a schema change

- adding a query, projection, or filter over existing columns;
- mapping an existing column into a DTO or model;
- changing application-side validation of existing data;
- storing configuration in an existing generic configuration mechanism, provided no new database object is required.

When the distinction is genuinely unclear, treat it as a schema change and verify against `AMRIT-DB` before proceeding.

## Step 2: Inspect the existing schema

Before proposing any schema object:

1. Inspect the relevant existing schema through DeepWiki repository research and the checked-out source.
2. Identify the corresponding structures and conventions in the `AMRIT-DB` repository — migration tooling, file naming, ordering, versioning, and directory layout.
3. Check for an existing table, column, constraint, index, or migration that already provides what the ticket needs.
4. Confirm naming, typing, and audit-column conventions from real neighbouring objects.

Never invent a table or column name without inspecting the existing database conventions. Never duplicate an existing schema object, and never create a second source of truth for data that an existing table already owns.

## Step 3: Implement the schema change in AMRIT-DB

When a true schema change is required and `AMRIT-DB` is available in the environment:

1. Follow the repository's existing migration mechanism and file-naming convention exactly; do not introduce a different tool or layout.
2. Add a new migration rather than editing an already-applied one.
3. Prefer additive change. Where a destructive or transforming change is unavoidable, describe the sequencing, the backfill, and the rollback limits.
4. Keep names, types, nullability, defaults, constraints, and audit columns consistent with neighbouring objects.
5. Add an index only when an expected query, filter, join, sort, or uniqueness rule justifies it.
6. Minimize storage of personal or clinical data, and follow the platform's existing conventions for sensitive fields.

Edit the files. Do not commit them — Git operations belong to the downstream PR skill.

## Step 4: Implement the application-side change

Modify the application repository only for the application-side changes needed to use that schema: entities, mappings, repositories or DAOs, queries, DTOs, validation, and the behaviour required by the acceptance criteria.

Do not place DDL, migration scripts, or schema-bootstrapping SQL in the application repository.

## Step 5: Keep the two repositories compatible

- The application change must work against the schema after the migration is applied.
- Where deployment ordering matters, prefer a schema change that is compatible with both the current and the new application version, and state the required ordering in the summary.
- Do not rely on a schema object that the migration does not actually create.
- Do not leave the application reading a column the migration removes.

## When AMRIT-DB is unavailable

If a schema change is required but `AMRIT-DB` is not available for modification in the current environment:

1. Do not create an application-local substitute migration or DDL.
2. Complete any application changes that are safe to complete independently.
3. Mark the implementation as incomplete.
4. State exactly what must be changed in `AMRIT-DB`: objects, columns, types, constraints, indexes, and the reason each is required.
5. Finish with **Implementation incomplete. Resolve the items above before PR preparation.**

Never claim the ticket is fully implemented while a required schema change is missing.

## Reporting database impact

When no schema change exists, report exactly:

```markdown
### Database impact

No database schema changes required.
```

When a schema change exists, report each repository separately:

```markdown
### Database impact

Schema change required.

Repository: AMRIT-DB

- `<path>`: <schema/migration change>

Application repository:

- `<path>`: <corresponding persistence/model change>
```

## Review checklist

- the classification is explicit and stated in the summary;
- existing schema was inspected before anything was proposed;
- no existing schema object was duplicated;
- no table or column name was invented without convention evidence;
- every DDL or migration change lives in `AMRIT-DB`;
- the application repository contains only application-side changes;
- application and database changes are compatible, with ordering stated when it matters;
- an unavailable `AMRIT-DB` produced an incomplete status, not a local substitute;
- no schema change was committed, pushed, or raised as a PR by this skill.
