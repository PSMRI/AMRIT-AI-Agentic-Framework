# Fictional Sample Persona Routing

This example is fictional. The tickets, repositories, and modules below are invented to show how the orchestrator routes different kinds of change. They do not describe real AMRIT tickets or architecture.

Routing is decided from the ticket, the approved Stage 03 design where one exists, and the actual source inspection — never from the fact that a specialist skill exists.

## Route 1 — Backend-only defect

Fictional ticket: a status filter is ignored beyond the first page of a list endpoint.

```text
implement-jira-ticket
    └── implement-backend-change
        └── write-unit-tests
            └── verification
```

Selected: Backend Developer, SDET.

Excluded: Frontend (the client already sends the filter; source inspection confirmed the defect is in server-side query construction), DBA (no schema object changes), Android (the endpoint is not used by the mobile applications), Architect (no contract, boundary, or ownership change), UX (no design change).

## Route 2 — Backend plus database

Fictional ticket: record the reason a request was reassigned, with durable history.

```text
implement-jira-ticket
    ├── implement-database-change      (first — publishes the schema contract)
    ├── implement-backend-change       (consumes the schema contract)
    └── write-unit-tests
```

Selected: DBA, Backend Developer, SDET.

Excluded: Frontend (the history is exposed through an existing detail response that the UI already renders generically; confirmed in the component source), Android, Architect, UX.

Ordering matters: the migration establishes the table, columns, constraints, and indexes before the entity and repository are written against them. If `AMRIT-DB` were unavailable, the database specialist would report the change as blocked and the backend work depending on the new table would not proceed.

## Route 3 — Frontend plus backend

Fictional ticket: add an optional closure note to a completion screen.

```text
implement-jira-ticket
    ├── implement-backend-change       (establishes the API contract)
    ├── implement-frontend-change      (consumes the API contract)
    ├── validate-ux-implementation     (approved screen layout exists)
    └── write-unit-tests
```

Selected: Backend Developer, Frontend Developer, UX/UI Specialist, SDET.

Excluded: DBA (the column already exists; source inspection confirmed it, so this is an application model change only), Android, Architect (additive DTO field inside an existing module).

## Route 4 — Android

Fictional ticket: allow a frontline worker to record a visit outcome while offline.

```text
implement-jira-ticket
    ├── implement-android-change
    └── write-unit-tests
```

Selected: Android/Kotlin Developer, SDET.

Excluded: Backend (the existing sync endpoint already accepts the field; verified against the API definition), Frontend (the web application does not implement this flow), DBA (no server-side schema change; the local database change carries its own on-device migration), Architect, UX (the screen follows an approved layout already implemented, and no new screen is added).

The Android specialist still confirms the offline expectation explicitly: what is queued, when it syncs, and how a conflict or failure surfaces.

## Route 5 — Architecturally significant cross-cutting change

Fictional ticket: move ownership of a shared reference dataset and expose it through a shared service consumed by two applications.

```text
implement-jira-ticket
    ├── review-implementation-architecture     (before implementation)
    ├── implement-database-change
    ├── implement-backend-change
    ├── implement-frontend-change
    ├── validate-ux-implementation
    └── write-unit-tests
```

Selected: Technical Architect, DBA, Backend Developer, Frontend Developer, UX/UI Specialist, SDET.

Excluded: Android (the mobile applications consume a different endpoint that is unchanged; confirmed in the mobile source).

The architecture review runs first because ownership and a cross-repository contract change. It fixes the constraints the implementing specialists must honour, and runs again briefly at the end because the change spans repositories.

## Blocked example — the approved design cannot be implemented as written

Fictional ticket: add a field to service A, per the approved design.

Source inspection shows service A no longer owns that data; ownership moved to service B in an earlier release.

```text
IMPLEMENTATION BLOCKED

Approved design:
Add field X to service A.

Current code:
Service A no longer owns this data; ownership moved to service B.

Conflict:
Implementing the design as written would create a second writer for data
service B owns, allowing the two records to diverge.

Required action:
Technical design needs review/update before implementation continues.
```

No specialist implements around the conflict, and no ownership decision is made silently. Independent work that is safe on its own is completed, everything left out is stated, and the run finishes with **Implementation incomplete. Resolve the items above before PR preparation.**

## Blocked example — source code unavailable

Fictional ticket assigned to an application repository that is not checked out in the environment.

```text
IMPLEMENTATION BLOCKED

Reason:
The source code for <repository> is not accessible in this environment.

Impact:
The ticket cannot be implemented safely from documentation alone.

Required action:
Provide access to the checked-out repository, then re-run this skill.
```

DeepWiki, Confluence, the approved design, and previous knowledge are never substituted for the code.
