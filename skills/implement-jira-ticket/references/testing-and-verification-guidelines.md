# Testing and Verification Guidelines

## Contents

- [Unit tests are mandatory](#unit-tests-are-mandatory)
- [What to cover](#what-to-cover)
- [Follow the repository's test conventions](#follow-the-repositorys-test-conventions)
- [Test integrity rules](#test-integrity-rules)
- [Regression tests for defects](#regression-tests-for-defects)
- [Discover the verification commands](#discover-the-verification-commands)
- [Run checks narrowest first](#run-checks-narrowest-first)
- [Handling failures](#handling-failures)
- [Manual verification](#manual-verification)
- [Reporting verification honestly](#reporting-verification-honestly)

## Unit tests are mandatory

Add or update unit tests for every behaviour changed by the ticket. An implementation without tests for its changed behaviour is incomplete.

Write tests that verify observable behaviour. Do not write tests merely to increase a coverage number, and do not assert implementation details that would break on a harmless refactor.

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

## Test integrity rules

- Do not weaken or delete an existing valid test to make the new implementation pass.
- Do not relax an assertion, widen a tolerance, or add a skip or ignore annotation to get a green run.
- Do not change production behaviour simply to satisfy an incorrectly constructed new test; fix the test.
- Do not mock the unit under test.
- Do not introduce a security bypass, disabled check, or test-only backdoor in production code to make a test pass.
- Keep tests deterministic: no reliance on wall-clock timing, network access, execution order, or shared mutable state, unless the repository already provides a controlled mechanism for it.

When an existing test legitimately encodes behaviour the ticket changes, update it deliberately and state in the completion summary which test changed and why.

## Regression tests for defects

When fixing a defect, add a regression test that fails for the original bug when practical:

1. Reproduce the reported behaviour as a test.
2. Confirm the test fails against the unfixed behaviour where the repository makes that practical.
3. Apply the fix.
4. Confirm the test passes.

Name the test so a future reader can connect it to the defect's behaviour. When reproducing the original failure is impractical, say so in the summary rather than claiming a verified reproduction.

## Discover the verification commands

Discover the project's actual commands from the repository before running anything. Inspect build files, package manifests and scripts, CI configuration, contributor documentation, and existing tooling configuration.

Do not assume a command exists. Depending on the repository, verification may involve Maven, Gradle, npm, pnpm, yarn, Jest, Vitest, Karma, JUnit, ESLint, Prettier, Checkstyle, the TypeScript compiler, or Sonar-related checks — but confirm each one from the repository before invoking it.

## Run checks narrowest first

1. Run the specific tests covering the changed behaviour.
2. Run the module or package test suite.
3. Run lint.
4. Run the formatter or style check.
5. Run static analysis when the repository configures it.
6. Run type checking when applicable.
7. Run the build or compile step.
8. Run package verification when practical.

Broader checks are worth running when they are practical in the environment. When a check is not practical — it needs a service, a credential, or an environment the session does not have — record it as NOT RUN with the reason rather than skipping it silently.

## Handling failures

When a check fails:

1. Determine whether the failure was caused by this implementation.
2. Fix implementation-caused failures.
3. Rerun the relevant check.
4. Distinguish pre-existing failures and environmental failures from implementation failures, and evidence that distinction — for example, that the same test fails on the unmodified files.

Never suppress a failure by disabling a rule, deleting a test, or narrowing a check's scope.

## Manual verification

Perform manual verification when it is practical and the repository provides a safe local method, such as a documented local run, a fixture-driven script, or an existing developer harness.

Do not start destructive infrastructure, and do not manipulate production or shared environments. Do not create or modify data in a shared database to demonstrate a change.

## Reporting verification honestly

Report only what actually ran:

```markdown
### Tests

Added/updated:
- <test>

Executed:
- `<command>` — PASS
- `<command>` — PASS

### Verification

- Lint: PASS / NOT RUN / FAILED
- Unit tests: PASS / NOT RUN / FAILED
- Static analysis: PASS / NOT RUN / FAILED
- Build: PASS / NOT RUN / FAILED
```

Never claim a test passed unless it was executed successfully in this session. Use NOT RUN with a reason when a check was unavailable, and FAILED with the cause and current status when a check failed. A remaining failure means the implementation is incomplete.
