# Fictional Sample Database-Change Example

This example is fictional. The keys, tables, columns, paths, and migration names below are invented for illustration only and do not describe a real AMRIT schema, repository, or migration convention. It shows the ownership rule in both situations: `AMRIT-DB` available, and `AMRIT-DB` unavailable.

## Fictional ticket

- `DEMO-5402` — Record the reason a demo request was reassigned
- Type: Story
- Acceptance criteria:
  1. A reviewer selects a reassignment reason from an approved list when reassigning a demo request.
  2. Every reassignment stores the reason, the actor, and the time.
  3. Reassignment history remains available after later reassignments.
  4. Existing consumers of the demo request detail remain compatible.

## Classification

**Database schema change.**

- The fictional `demo_request` table stores only the current assignee.
- Repository research and direct source inspection found no existing child entity or audit record that can hold multiple time-ordered reassignment entries.
- The approved history in AC3 cannot be represented without overwriting the previous reassignment, so a new structure is required.

This is not an "application model/query change only" case: no existing column can hold the history.

## Existing-schema inspection performed first

1. Searched the fictional schema for an existing reassignment, assignment-history, or audit table capable of holding the entries. None found.
2. Confirmed the fictional `AMRIT-DB` migration mechanism, file-naming convention, and ordering from neighbouring migrations.
3. Confirmed audit-column naming and timestamp typing from two neighbouring fictional tables.
4. Confirmed the reason values come from an existing fictional reference table rather than needing a new one.

No table or column name was proposed before this inspection completed.

## Case A — AMRIT-DB is available

### Database impact

Schema change required.

Repository: AMRIT-DB

- `src/main/resources/db/migration/V9999__add_demo_request_reassignment.sql` (fictional path and version): additive migration creating `demo_request_reassignment` with `id`, `demo_request_id` foreign key to `demo_request`, `reason_code` referencing the existing fictional reason reference table, `reassigned_from`, `reassigned_to`, `reassigned_by`, `reassigned_at`, and the repository's standard audit columns; unique constraint on `(demo_request_id, reassigned_at)`; index on `(demo_request_id, reassigned_at)` to support ordered history retrieval.

The migration is additive and applied before the application writes to the table. No existing column is altered or dropped, so the previous application version remains compatible.

Application repository:

- `src/main/java/org/example/demo/request/model/DemoRequestReassignment.java`: new entity mapping the fictional table.
- `src/main/java/org/example/demo/request/repository/DemoRequestReassignmentRepository.java`: history retrieval ordered by reassignment time.
- `src/main/java/org/example/demo/request/service/DemoRequestReassignmentService.java`: writes the entry inside the existing reassignment transaction and validates the reason against the existing reference data.
- `src/main/java/org/example/demo/request/dto/DemoRequestDetailResponse.java`: exposes the history additively so existing consumers stay compatible.

No DDL, migration script, or schema-bootstrapping SQL was placed in the application repository.

### Deployment ordering

Apply the `AMRIT-DB` migration first, then deploy the application change. The additive migration is safe to apply before the application is deployed.

## Case B — AMRIT-DB is not available for modification

When the environment has no checked-out, writable `AMRIT-DB`:

- no application-local substitute migration or DDL is created;
- only the application changes that are safe on their own are completed — for example the reason-code validation against existing reference data;
- the entity and history retrieval are not wired to a table that does not exist;
- the implementation is reported as incomplete.

### Database impact

Schema change required. `AMRIT-DB` was not available for modification in this environment.

Required in AMRIT-DB before this ticket can be completed:

- new table `demo_request_reassignment` (fictional) with `id`, `demo_request_id` foreign key to `demo_request`, `reason_code` referencing the existing fictional reason reference table, `reassigned_from`, `reassigned_to`, `reassigned_by`, `reassigned_at`, and the repository's standard audit columns;
- unique constraint on `(demo_request_id, reassigned_at)` to prevent duplicate entries under concurrency;
- index on `(demo_request_id, reassigned_at)` for ordered history retrieval;
- reason for each item: AC2 and AC3 require durable, time-ordered history that no existing structure can hold.

### Remaining issues

- The `AMRIT-DB` migration above must be added and applied before the application-side reassignment history can be implemented and verified.

---

**Implementation incomplete. Resolve the items above before PR preparation.**

The ticket is not fully implemented while the required schema change is missing, and no local substitute migration was created to work around it.
