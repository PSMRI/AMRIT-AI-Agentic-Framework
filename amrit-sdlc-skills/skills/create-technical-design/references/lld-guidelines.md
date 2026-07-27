# Low-Level Design Guidelines

The LLD gives implementers enough behavioral precision to estimate and implement after review without generating code.

## Evidence-aware detail

Use real class, service, repository, controller, DTO, validator, and configuration names only when found in current evidence.

For a new element:

- prefix its first mention with **Proposed**;
- use a responsibility-oriented name;
- do not imply a language, framework, annotation, library, or package unless confirmed;
- treat signatures and fields as design contracts, not source code.

When DeepWiki research is available, distinguish:

- **Confirmed existing components** — exact names or locations supported by retrieved evidence;
- **Inferred components or conventions** — strongly indicated but not directly verified;
- **Likely impacted modules/files** — include only with evidence and classification;
- **Proposed new components** — recommendations requiring Architect approval;
- **Repository verification still required** — unresolved implementation detail.

Record implementation conventions discovered through DeepWiki, including layering, naming, validation, exception, transaction, security, logging, migration, and testing patterns. Never derive an exact class, path, or package from the repository catalog alone.

## Element specification

For each affected or proposed element include only useful fields:

| Element | Status | Responsibility | Inputs | Outputs | Collaborators | Rules | Failure behavior |
|---|---|---|---|---|---|---|---|

Cover:

- controllers or entry adapters;
- application or orchestration services;
- domain services and rules;
- validators;
- repositories or integration adapters;
- DTOs, commands, events, and result models;
- mapping responsibilities;
- configuration and feature controls.

Avoid class-by-class ceremony for unchanged or irrelevant code.

## Detailed processing flow

Describe the main path in numbered steps:

1. entry and identity context;
2. syntactic validation;
3. authorization;
4. business validation;
5. data retrieval;
6. state conflict or duplicate detection;
7. mutation or integration;
8. transaction completion;
9. response or event;
10. audit and observability.

Then describe meaningful alternate and failure paths. Keep acceptance-criteria traceability visible.

## Validation

Separate:

- transport or shape validation;
- required and format validation;
- reference or master-data validation;
- authorization and ownership checks;
- domain invariants;
- state-transition rules;
- duplicate and idempotency checks;
- cross-field and temporal rules.

State where each validation runs and how failure is represented. Reuse a confirmed validation owner instead of duplicating rules across UI and service layers.

## Exception handling

Define categories, not language-specific exception classes unless confirmed:

- invalid request;
- unauthenticated or unauthorized;
- resource not found;
- state conflict;
- downstream unavailable or timeout;
- persistence or concurrency failure;
- unexpected internal failure.

For each category, define external outcome, safe diagnostic behavior, retryability, audit needs, and correlation. Do not expose internals or sensitive information.

## Retry and idempotency

Retry only transient failures. Define:

- retry owner;
- eligible operations and failure categories;
- maximum attempts or elapsed budget when known;
- backoff and jitter as a recommendation when convention is absent;
- idempotency key or duplicate-detection strategy;
- behavior after exhaustion;
- metrics and alerts.

Do not retry validation, authorization, deterministic conflict, or other permanent failures.

## Transaction boundaries

State:

- operations inside one transaction;
- operations intentionally outside it;
- isolation or locking expectation when material;
- behavior on partial failure;
- consistency model across external calls;
- compensation or reconciliation where atomicity is impossible.

Avoid holding a database transaction open across a remote network call unless confirmed constraints make it unavoidable and the risk is justified.

## Concurrency

Consider:

- simultaneous edits;
- duplicate requests;
- stale reads and lost updates;
- optimistic or pessimistic concurrency;
- event ordering;
- scheduler overlap;
- multi-instance behavior;
- cache invalidation.

Recommend a conflict outcome rather than leaving behavior undefined.

## Configuration

For each proposed key identify:

- purpose and owner;
- type, range, and validation;
- secure or non-secure classification;
- default and environment scope;
- dynamic reload or restart requirement;
- fallback behavior;
- deployment and rollback impact.

Never put secrets or environment-specific values in the design.

## State model

Use a state diagram only when the Story introduces or changes a lifecycle with guarded transitions. Define:

- valid states;
- allowed transitions and actor;
- guard conditions;
- terminal states;
- rejection of invalid transitions;
- audit event.

## LLD completion check

Confirm that:

- the main, alternate, and failure flows are implementable;
- validation ownership is unambiguous;
- exception mapping is safe and consistent;
- retries are bounded and idempotent;
- transactions and concurrency are explicit;
- configuration is operable;
- details do not claim unsupported implementation facts;
- repository-grounded names and conventions have correct evidence classification;
- no source code has been generated.
