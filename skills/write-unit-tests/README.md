# write-unit-tests

`write-unit-tests` is the **SDET / developer-testing** specialist for Stage 05 — In Development. It adds or updates code-level unit tests for an implemented AMRIT change and runs them.

**This skill changes source files** — test files, and never production code to make a test pass.

## Purpose

Read the actual production diff, identify what behaviour changed, cover success, failure, boundary, and regression cases with the repository's own test conventions, run the relevant suites, and report the real results.

## Relationship to `implement-jira-ticket`

`implement-jira-ticket` invokes this skill whenever production behaviour changed — effectively on every implementation route.

```text
implement-jira-ticket
    ├── implement-database-change / implement-backend-change /
    │   implement-frontend-change / implement-android-change
    └── write-unit-tests
        └── verification → create-development-pr
```

The skill is independently installable and independently invocable against an implemented change. When it is not installed, the orchestrator applies the developer-testing persona inline; unit tests are never skipped.

## Also reused by `test-jira-ticket`

The same specialist serves both AMRIT meta-skills:

```text
implement-jira-ticket → write-unit-tests     (primary, Stage 05)
test-jira-ticket      → write-unit-tests     (when development-level testing
                                              is explicitly appropriate)
```

[`test-jira-ticket`](../test-jira-ticket/README.md) routes here when a ticket is in development and code-level testing is what its lifecycle position calls for. Nothing about this skill's contract changes, and no unit-testing logic is duplicated into the testing meta-skill. One specialist can participate in more than one orchestration path.

## Not QA

This is developer, code-level testing — one of three distinct testing artifacts:

| Skill | Stage | Artifact |
| --- | --- | --- |
| [`draft-test-cases`](../draft-test-cases/README.md) | Stage 03 — Analysis | Functional QA test **specifications** |
| `write-unit-tests` | Stage 05 — In Development | Executable **unit-test code** with real results |
| [`execute-qa-validation`](../execute-qa-validation/README.md) | Stage 07 — In QA | QA **execution results and evidence** |

The skill never produces a QA test specification, never executes a QA cycle, and never claims QA sign-off. A green unit suite is not QA validation.

## It reads the diff itself

Coverage is derived from the real change: `git status` and `git diff`, the changed production code and its error paths, the acceptance criteria implemented, the contracts established or consumed, and the tests that already cover the touched code. A suite written from a summary tends to test the summary rather than the code.

## Test integrity

The skill never weakens, skips, or deletes a valid existing test, never changes production behaviour to satisfy a badly constructed test, never mocks the unit under test, and never introduces a test-only backdoor or security bypass. Tests stay deterministic and never touch shared or production systems.

When an existing test legitimately encodes behaviour the ticket changes, the update is deliberate and reported.

## Honest results

`PASS` means the command ran and succeeded in this session. Failures are reported with their cause and current status, and checks the environment cannot run are reported as `NOT RUN` with the reason. Nothing is claimed that was not observed.

## Git, Jira, and approval boundaries

The skill may inspect `git status`, `git diff`, and history. It never creates a branch, commit, push, or Pull Request, never writes to Jira, and never claims code review, QA sign-off, or CI results.

## Required capabilities

The host's filesystem, repository-editing, and command-execution capabilities, plus read access to Jira for traceability. Tool names are discovered, not hardcoded.

## Use and distribution

Invoke `/write-unit-tests` from the repository root using a supported coding agent, or let `/implement-jira-ticket` route to it. For a packaged installation, download `write-unit-tests.zip` from the latest release. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
