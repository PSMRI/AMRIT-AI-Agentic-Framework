# Persona Routing Guidelines

## Contents

- [Routing principle](#routing-principle)
- [Routing signals](#routing-signals)
- [The personas](#the-personas)
- [Route examples](#route-examples)
- [What to pass to a specialist](#what-to-pass-to-a-specialist)
- [Invoking a specialist](#invoking-a-specialist)
- [When a specialist skill is unavailable](#when-a-specialist-skill-is-unavailable)
- [Reporting the routing decision](#reporting-the-routing-decision)
- [Review checklist](#review-checklist)

## Routing principle

Personas are selected from evidence, never from habit and never from the fact that a specialist skill exists.

The route is determined by three things together:

1. the Jira ticket and its acceptance criteria;
2. the approved Stage 03 technical design, where one exists;
3. the actual source-code inspection.

A ticket that changes one layer runs one specialist. A ticket that changes four layers runs four. Every exclusion is a decision that appears in the report.

## Routing signals

| Evidence in the ticket, design, or code | Persona |
| --- | --- |
| Table, column, index, constraint, migration, seed or reference data, data backfill, query-performance obligation | DBA / Database Engineer |
| Service, controller, endpoint, domain rule, server-side validation, integration, scheduler, persistence mapping, backend configuration, error handling | Backend Developer |
| Web screen, component, form, client validation, state management, routing, API consumption from the browser, frontend error handling, accessibility of a web view | Frontend Developer |
| Android application flow, Kotlin implementation, mobile screen, offline behaviour, sync, device or platform constraint | Android / Kotlin Developer |
| New component, new contract, changed module ownership, cross-repository or cross-cutting change, changed integration boundary, security- or performance-material change, suspected deviation from the approved design | Technical Architect |
| Approved wireframe, workflow, or design-system rule that the user-visible change must honour | UX / UI Specialist |
| Any changed production behaviour | SDET / developer testing |

A signal that appears only in a document and is contradicted by the code is not a routing signal; it is a conflict to report.

## The personas

### Technical Architect — `review-implementation-architecture`

Runs **before** implementation for architecturally significant work, and again briefly after it when the change spans modules or repositories. During Stage 05 its purpose is conformance, not redesign: approved HLD and LLD, architecture patterns, module boundaries, API contracts, integration boundaries, and security and performance constraints.

It does not re-open an approved design. When the design cannot be implemented safely as written, it reports the discrepancy for design review.

### DBA / Database Engineer — `implement-database-change`

Owns schema changes, migrations, indexes, constraints, query impact, backward and forward migration considerations, and data compatibility. Authoritative schema changes live in `AMRIT-DB`. Respects any DBA-review requirement established during Stage 03; it never claims DBA approval.

Runs before the backend when the backend depends on the new schema.

### Backend Developer — `implement-backend-change`

Owns services, APIs, controllers, domain logic, integrations, server-side validation, persistence integration, error handling, and backend configuration in the affected API repository.

### Frontend Developer — `implement-frontend-change`

Owns the web UI: components, state management, API integration, forms, client-side validation, accessibility, and frontend error handling in the affected UI repository.

### Android / Kotlin Developer — `implement-android-change`

Owns the Android applications: Kotlin implementation, mobile flows, API integration, offline behaviour where applicable, and device or platform constraints.

### UX / UI Specialist — `validate-ux-implementation`

Validates the implemented UI against approved wireframes, workflow consistency, design-system adherence, accessibility, and interaction consistency. It is a validation persona, not an autonomous product-design persona: where approved UX exists, it conforms to it and reports gaps rather than inventing new design.

Runs after the user-visible change exists.

### SDET / developer testing — `write-unit-tests`

Owns code-level unit tests for changed behaviour: identifying changed behaviour and required coverage, adding or updating tests, covering success, failure, and boundary cases, mocking dependencies appropriately, running the relevant unit suites, and reporting real results.

Distinct from `draft-test-cases` and from Stage 07 QA execution.

## Route examples

Backend-only ticket:

```text
implement-jira-ticket
    └── implement-backend-change
        └── write-unit-tests
            └── verification
```

Backend plus database:

```text
implement-jira-ticket
    ├── implement-database-change      (first — establishes the schema contract)
    ├── implement-backend-change       (consumes the schema)
    └── write-unit-tests
```

Full-stack ticket:

```text
implement-jira-ticket
    ├── implement-backend-change       (establishes the API contract)
    ├── implement-frontend-change      (consumes the API contract)
    └── write-unit-tests
```

Android ticket:

```text
implement-jira-ticket
    ├── implement-android-change
    └── write-unit-tests
```

Architecturally significant cross-cutting change:

```text
implement-jira-ticket
    ├── review-implementation-architecture   (before implementation)
    ├── implement-database-change
    ├── implement-backend-change
    ├── implement-frontend-change
    ├── validate-ux-implementation
    └── write-unit-tests
```

## What to pass to a specialist

Pass a boundary and a contract, not a digest of the code:

- the Jira key and the acceptance criteria in scope for that persona;
- the repository and the modules it may change;
- the approved-design constraints it must honour;
- contracts it must produce, or contracts an upstream specialist already established;
- explicit exclusions — files, modules, repositories, and behaviours it must not change;
- the instruction to inspect its own code before editing;
- what it must report back: files changed, contracts produced, checks run with real results, and blockers.

Do not pass a summary in place of the code. Each specialist reads the code it owns; that is what prevents the orchestrator from becoming a lossy context bottleneck.

## Invoking a specialist

1. Use the host's skill-invocation mechanism when it exposes one.
2. Otherwise read the canonical specialist skill from `skills/<specialist-name>/SKILL.md` and follow it directly.
3. Otherwise apply the inline fallback below.

Record which mechanism was used for each specialist.

## When a specialist skill is unavailable

Each skill in this framework is independently installable, so an environment may have `implement-jira-ticket` without its specialists.

A missing specialist skill never removes the persona's obligations. When a selected persona's skill is not available:

1. Perform that persona's work inline, following the persona contract described above and the same non-negotiable boundaries.
2. Keep the layer's responsibilities intact — including the mandatory inspection of that layer's actual code, and unit tests for changed behaviour.
3. Do not skip the persona, and do not silently downgrade its scope.
4. Record in the report that the persona was applied inline because the specialist skill was unavailable.

Never claim that a specialist skill executed when the work was performed inline.

## Reporting the routing decision

The report states:

- personas selected, with the evidence for each;
- personas considered and excluded, with the reason;
- specialist skills actually executed;
- personas applied inline because their skill was unavailable.

## Review checklist

- every selected persona traces to evidence in the ticket, the approved design, or the code;
- no specialist ran by default;
- exclusions are stated with reasons;
- specialists received boundaries and contracts, not code summaries;
- each implementation specialist inspected its own code;
- unavailable specialists were applied inline, not skipped;
- the report distinguishes executed specialists from inline persona work.
