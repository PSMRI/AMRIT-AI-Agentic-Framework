# Database Design Guidelines

Determine schema impact from evidence. Do not equate "the feature uses data" with "the schema must change."

## Schema-change decision

Answer these questions:

1. Does the approved behavior require durable data not represented by a confirmed existing model?
2. Must an existing table, column, relationship, index, constraint, view, sequence, or database object change?
3. Does a new query pattern require an index or partitioning change?
4. Must existing records be backfilled or transformed?
5. Is persistence proposed only because current schema evidence is missing?

Select one outcome:

- **No schema change:** existing confirmed structures support the behavior.
- **Schema change required:** evidence or the proposed design requires a concrete change.
- **Undetermined:** current schema evidence is insufficient. Treat this as an architecture-material open question; do not invent a schema.

If no schema change is required, write exactly:

**No database schema changes required.**

Do not include DBML, migration steps, or a DBA section for that outcome.

## Optional repository verification

When database change is plausible and official DeepWiki repository tools are available:

1. Inspect the relevant application repository for entities, repositories/DAOs, queries, transaction ownership, and current persistence conventions.
2. Inspect `PSMRI/AMRIT-DB` for existing schemas, Flyway migration conventions, related tables, indexes, constraints, and seed-data patterns.
3. Search for a suitable existing representation before proposing a table or column.
4. Classify current schema claims as Confirmed, Inferred, or Unknown.
5. Generate DBML only after considering retrieved existing-schema evidence.

When DeepWiki is unavailable, continue the database analysis but keep unsupported schema design Proposed. State that existing-schema verification is required. Never invent a current table, column, migration path, or Flyway convention.

## Changes that count

Include:

- table, column, type, nullability, default, or generated-value changes;
- primary, foreign, unique, check, or exclusion constraints;
- indexes and partitioning;
- relationships or ownership changes;
- database views, materialized views, functions, or triggers;
- retention, archival, or encryption-related schema changes;
- data migrations and backfills.

Configuration stored in an existing generic configuration mechanism may not be a schema change; explain the distinction.

## Schema design

For each change specify:

| Item | Current evidence | Proposed change | Rationale | Compatibility | Migration/rollback |
|---|---|---|---|---|---|

Address:

- ownership and bounded context;
- stable identifiers;
- data type and unit;
- nullability and default;
- allowed values and validation owner;
- relationship cardinality and delete behavior;
- uniqueness and duplicate handling;
- audit fields and temporal meaning;
- sensitive or regulated data classification;
- retention and archival;
- expected query patterns.

Do not create a duplicate source of truth. Prefer references to confirmed master data over copied descriptions unless availability or historical-snapshot requirements justify denormalization.

## Indexes

Justify an index using an expected query, filter, join, sort, uniqueness rule, or measured performance concern. Discuss:

- column order;
- selectivity;
- write and storage overhead;
- partial or filtered behavior where supported;
- uniqueness;
- rollout and lock risk.

Do not recommend speculative indexes merely because a column may be queried.

## Migration strategy

Define:

- pre-deployment compatibility;
- additive-first or expand-migrate-contract sequence;
- DDL ordering;
- backfill scope, batching, restartability, and observability;
- behavior for new writes during backfill;
- constraint-enforcement timing;
- application deployment order;
- validation and reconciliation;
- maintenance-window or online-migration assumption;
- rollback and point-of-no-return.

Avoid claiming a migration is reversible when data loss, transformation, or new writes make reversal unsafe. Describe forward-fix or restore strategy where appropriate.

## Concurrency and transactions

Identify:

- write transaction boundary;
- uniqueness race;
- optimistic version or locking need;
- upsert semantics;
- deadlock or hot-row risk;
- interaction with external calls;
- consistency across read replicas or caches.

## Healthcare data

Minimize storage of personal or clinical data. Identify sensitive fields without using real values. Address encryption, access control, audit, retention, masking, export, and non-production data handling based on confirmed platform policy. If policy evidence is unavailable, mark controls Proposed and require security/privacy review.

## DBML

Generate DBML only when a schema change is required. Include affected existing tables needed to understand relationships and mark them in notes as existing. Include proposed tables or columns with notes.

Use dbdiagram.io-compatible syntax:

```dbml
Table existing_case {
  id bigint [pk, note: 'Existing']
}

Table proposed_follow_up {
  id bigint [pk, increment]
  case_id bigint [not null, ref: > existing_case.id]
  scheduled_at timestamp [not null]
  status varchar(30) [not null]
  created_at timestamp [not null]

  Indexes {
    (case_id, scheduled_at)
  }
}
```

Keep DBML logical when the physical database engine is unknown. Do not invent engine-specific types, names, or defaults.

## Database review output

When change exists, include:

- schema impact summary;
- table, column, relationship, index, and constraint detail;
- query and transaction impact;
- migration, backfill, deployment, and rollback considerations;
- privacy and security impact;
- DBML;
- DBA or data-owner review points.

When evidence is insufficient, state what schema metadata or owner decision is required before the design can be reviewed.
