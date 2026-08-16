# Unit Testing Guidelines

## Contents

- [Scope of this document](#scope-of-this-document)
- [Unit tests are mandatory](#unit-tests-are-mandatory)
- [Identify the changed behaviour first](#identify-the-changed-behaviour-first)
- [What to cover](#what-to-cover)
- [Follow the repository's test conventions](#follow-the-repositorys-test-conventions)
- [Mocking](#mocking)
- [Test integrity rules](#test-integrity-rules)
- [Regression tests for defects](#regression-tests-for-defects)
- [Layer-specific notes](#layer-specific-notes)
- [Discover and run the test commands](#discover-and-run-the-test-commands)
- [Handling failures](#handling-failures)
- [Reporting results honestly](#reporting-results-honestly)
- [Review checklist](#review-checklist)

## Scope of this document

Code-level unit testing of an implemented change. Broader verification — lint, formatting, static analysis, type checking, build, and packaging — is coordinated by `implement-jira-ticket`. QA test-specification design belongs to `draft-test-cases` at Stage 03, and QA execution against a deployed build belongs to `execute-qa-validation` at Stage 07. Keep these three separate: they are different artifacts with different owners.

## Unit tests are mandatory

Add or update unit tests for every behaviour changed by the ticket. An implementation without tests for its changed behaviour is incomplete.

Write tests that verify observable behaviour. Do not write tests merely to increase a coverage number, and do not assert implementation details that would break on a harmless refactor.

## Identify the changed behaviour first

Read the actual production diff and the changed code, not a description of it. For each change, establish:

- what behaviour is new or different;
- which inputs now produce different outputs or side effects;
- which collaborators are involved and how they fail;
- which existing behaviour could plausibly break;
- which acceptance criterion the behaviour serves;
- which tests already cover the touched code.

A test suite written from a summary tends to test the summary rather than the code.

## What to cover

Cover the behaviour the ticket actually specifies:

- **happy path** — the acceptance criterion's main flow;
- **validation behaviour** — rejected input, required fields, and rule violations;
- **error behaviour** — failures from collaborators, integrations, and persistence;
- **boundary cases** — limits, empty and maximum values, first and last elements, and time or range edges named in the criteria;
- **regression behaviour** — the specific behaviour the change could plausibly break.

Skip a category when the ticket genuinely has no such case, and say so rather than writing a hollow test.

## Follow the repository's test conventions

Reuse what the repository already has:

- the existing test framework and runner;
- existing fixtures, factories, builders, and test data helpers;
- existing mocking or stubbing approach;
- existing naming conventions for test classes, files, and cases;
- existing directory organization and file placement;
- existing assertions library and style.

Do not introduce a second test framework, a parallel fixture mechanism, or a different assertion style alongside the established one.

## Mocking

- Mock at the boundary the repository already mocks, and no deeper.
- Never mock the unit under test.
- Prefer the repository's existing test doubles and helpers over ad-hoc stubs.
- Assert on behaviour and outcomes rather than on every internal interaction, unless the interaction is the contract being tested.
- Keep mocks honest: a mock that returns a shape the real collaborator cannot produce proves nothing.

## Test integrity rules

- Do not weaken or delete an existing valid test to make the new implementation pass.
- Do not relax an assertion, widen a tolerance, or add a skip or ignore annotation to get a green run.
- Do not change production behaviour simply to satisfy an incorrectly constructed new test; fix the test.
- Do not introduce a security bypass, disabled check, or test-only backdoor in production code to make a test pass.
- Keep tests deterministic: no reliance on wall-clock timing, network access, execution order, or shared mutable state, unless the repository already provides a controlled mechanism for it.
- Do not create or modify data in a shared or production database to make a test work.

When an existing test legitimately encodes behaviour the ticket changes, update it deliberately and state which test changed and why.

## Regression tests for defects

When fixing a defect, add a regression test that fails for the original bug when practical:

1. Reproduce the reported behaviour as a test.
2. Confirm the test fails against the unfixed behaviour where the repository makes that practical.
3. Apply or confirm the fix.
4. Confirm the test passes.

Name the test so a future reader can connect it to the defect's behaviour. When reproducing the original failure is impractical, say so rather than claiming a verified reproduction.

## Layer-specific notes

- **Backend** — cover domain rules, validation, error mapping, and persistence interaction at the layer the repository already tests. Preserve transaction expectations rather than asserting them into a different shape.
- **Frontend** — cover component behaviour, form validation, state transitions, and error and empty states using the repository's existing component-testing approach.
- **Android** — cover view models, use cases, mappers, and offline or sync logic with the project's existing unit-test approach. Instrumented tests may not be runnable in every environment; report them as `NOT RUN` with the reason rather than claiming them.
- **Database-dependent code** — test the application logic against the schema contract; do not stand up shared infrastructure to prove a migration.

## Discover and run the test commands

Discover the project's actual commands from build files, package manifests and scripts, CI configuration, contributor documentation, and existing tooling configuration. Do not assume a command exists.

Run narrowest first:

1. the specific new and updated tests;
2. the class, module, or package suite covering the changed code;
3. the broader repository suite when practical in the environment.

Run the relevant suite in every repository that changed.

## Handling failures

When a test fails:

1. Determine whether the production change or the test is wrong.
2. Fix the correct one — never the convenient one.
3. Rerun the relevant test.
4. Distinguish pre-existing failures and environmental failures from failures caused by this change, and evidence that distinction — for example, that the same test fails on the unmodified files.

Never suppress a failure by disabling a rule, deleting a test, or narrowing a check's scope.

## Reporting results honestly

Report only what actually ran:

```markdown
### Tests

Added/updated:
- <test>

Executed:
- `<command>` — PASS
- `<command>` — FAILED — <cause and current status>
- `<command>` — NOT RUN — <reason>
```

Never claim a test passed unless it was executed successfully in this session. A remaining failure means the implementation is incomplete.

## Review checklist

- the actual production diff was inspected before writing tests;
- every changed behaviour is covered or listed as a gap with a reason;
- success, failure, and boundary cases are covered where they exist;
- a defect fix carries a regression test, or the impracticality is stated;
- the repository's framework, fixtures, mocks, naming, and organization were reused;
- no existing valid test was weakened, skipped, or deleted;
- no production behaviour was changed to make a test pass;
- tests are deterministic and touch no shared or production system;
- every reported command actually ran, with honest `FAILED` and `NOT RUN` reasons.
