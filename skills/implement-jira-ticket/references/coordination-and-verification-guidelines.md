# Coordination and Verification Guidelines

## Contents

- [Why coordination matters](#why-coordination-matters)
- [Establish contracts before implementation](#establish-contracts-before-implementation)
- [Execution order](#execution-order)
- [Checkpoints between specialists](#checkpoints-between-specialists)
- [Handling a specialist blocker](#handling-a-specialist-blocker)
- [Multi-repository coordination](#multi-repository-coordination)
- [Verification](#verification)
- [Evidence honesty](#evidence-honesty)
- [Human accountability](#human-accountability)
- [Review checklist](#review-checklist)

## Why coordination matters

Specialists are not independent agents editing unrelated pieces. A schema change that the backend does not map, an API contract the frontend does not consume, or a model change with no test is a broken implementation assembled from correct-looking parts.

The orchestrator establishes affected components, dependencies, execution order, contracts, and verification requirements **before** implementation begins, and re-checks them between specialists.

## Establish contracts before implementation

For each boundary the change crosses, write down the contract before the first edit:

| Boundary | Contract to fix in advance |
| --- | --- |
| Database → backend | table and column names, types, nullability, constraints, indexes, migration ordering |
| Backend → backend | service and method responsibilities, transaction boundaries, error semantics |
| Backend → frontend or Android | endpoint path and method, request and response shape, field names and types, validation and error responses, compatibility expectations |
| Frontend or Android → user | approved wireframe, workflow, design-system component, accessibility behaviour |
| Any change → tests | the behaviours that must be covered and the cases that prove them |

A contract that cannot be stated before implementation is a design gap. Resolve it — from the approved design, from the code, or by reporting a blocker — before delegating.

## Execution order

The dependency chain, applied only to the personas actually selected:

```text
review-implementation-architecture     (before implementation, when selected)
        ↓
implement-database-change              (schema first — it constrains everything above it)
        ↓
implement-backend-change               (models, then persistence, then API)
        ↓
implement-frontend-change / implement-android-change   (consume the API contract)
        ↓
validate-ux-implementation             (after the user-visible change exists)
        ↓
write-unit-tests                       (covers everything that changed)
        ↓
verification
        ↓
create-development-pr
```

Frontend and Android work are independent of each other and may run in either order once the API contract exists. Never start a consumer before its producer's contract is real in the code.

## Checkpoints between specialists

After each specialist completes:

1. Confirm what actually changed in the repository, not what the specialist described.
2. Re-check the contract the next specialist depends on against the real code.
3. Confirm the change stayed inside its declared repository and module boundary.
4. Confirm no unrelated file or behaviour was modified.
5. Confirm no Git operation, Jira write, or approval claim occurred.
6. Update the plan when the discovered reality differs from the assumption.

## Handling a specialist blocker

When a specialist reports a blocker:

1. Stop the work that depends on it. Do not implement against a contract that does not exist.
2. Complete the independent work that remains safe.
3. Keep the partial implementation coherent: do not leave code referencing a schema object, endpoint, or component that was never created.
4. Report the blocker, the dependent work not performed, and what is required to unblock it.
5. Finish with **Implementation incomplete. Resolve the items above before PR preparation.**

## Multi-repository coordination

- Every repository touched must be identified before implementation and reported separately.
- Application repositories and `AMRIT-DB` are separate Git repositories with separate histories.
- Keep the application change compatible with the schema after the migration is applied, and state the required deployment ordering when it matters.
- Never create an application-local substitute for a schema change.
- Never modify a repository outside the identified impact.
- This skill edits repositories. It never commits in any of them; downstream `create-development-pr` decides how the change set becomes one or more Pull Requests.

## Verification

Discover the repository's actual commands from build files, package manifests and scripts, CI configuration, contributor documentation, and existing tooling configuration. Do not assume a command exists.

Run narrowest first, per repository that changed:

1. the specific unit tests covering the changed behaviour;
2. the module or package test suite;
3. lint;
4. formatter, checkstyle, or style check;
5. static analysis where the repository configures it;
6. type checking where applicable;
7. build or compile;
8. migration or schema validation where the database repository provides one;
9. package verification when practical.

When a check fails, determine whether this implementation caused it, fix implementation-caused failures, rerun, and distinguish pre-existing or environmental failures with evidence. Never suppress a failure by disabling a rule, deleting or weakening a test, or narrowing a check's scope.

Do not start destructive infrastructure, and do not touch production or shared environments.

## Evidence honesty

- `PASS` means the command actually ran and succeeded in this session.
- `FAILED` means it ran and failed; state the cause and the current status.
- `NOT RUN — <reason>` means it did not run; state why.
- Files changed are reported from the actual working tree.
- A specialist that was applied inline is reported as inline persona work, not as an executed skill.
- A knowledge source that was unavailable is reported as unavailable, not silently omitted.

Never report a check that did not run. Never report a result you did not observe.

## Human accountability

The agent implements and verifies. It never produces, implies, or assumes:

- architecture approval;
- DBA approval;
- code-review approval;
- QA approval;
- release approval;
- CI results;
- test results it did not observe.

When a required approval is absent — for example a Stage 03 DBA review that has not happened — report it as absent and continue only with the implementation work that is safe without it.

## Review checklist

- contracts were established before implementation;
- specialists ran in dependency order;
- each contract was re-checked against the real code between specialists;
- a blocker stopped its dependent work instead of producing incoherent code;
- every changed repository was verified with its own commands;
- every reported check actually ran, with honest `FAILED` and `NOT RUN` reasons;
- no approval, sign-off, or CI state was fabricated;
- the report matches the actual working tree.
