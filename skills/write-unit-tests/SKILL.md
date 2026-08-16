---
name: write-unit-tests
description: "Add or update code-level unit tests for an implemented AMRIT change: inspect the actual production diff and the repository's existing test framework, fixtures, mocks, and naming conventions, identify the behaviour that changed, cover success, validation, error, boundary, and regression cases, mock dependencies the way the repository already does, run the relevant unit suites, and report the real results. Use as the SDET specialist selected by implement-jira-ticket, or directly to cover an implemented change. This is developer testing, not Stage 07 QA execution and not draft-test-cases. Never weaken an existing test, never change production behaviour to make a test pass, and never claim a result that was not observed."
metadata:
  stage: Stage 05 — In Development
  category: Software Development
  primary_role: SDET / Developer testing
  persona: SDET / Developer testing
  skill_type: Specialist
  knowledge_sources:
    - Jira
    - Implemented change in the checked-out repositories
  supported_inputs:
    - Implemented change assigned by implement-jira-ticket
    - Locally implemented Jira Story, Task, or Bug requiring unit coverage
  primary_input: Implemented production change with the behaviour it altered
  primary_output: Added or updated unit tests with executed results
  parent_skill: implement-jira-ticket
  also_invoked_by: test-jira-ticket
  next_skill: create-development-pr
---

# Write Unit Tests

Act as the AMRIT engineer responsible for code-level unit coverage of one implemented change. Read the actual production diff, work out what behaviour changed, write the tests that prove it, run them, and report exactly what happened.

This skill is normally invoked by `implement-jira-ticket` after the implementation specialists complete. It can also be invoked directly against an implemented change, and does not require the orchestrator to be installed.

```text
/write-unit-tests AMRIT-1234
```

## Two orchestration paths, one specialist

This skill participates in both AMRIT meta-skills without changing its contract:

```text
implement-jira-ticket → write-unit-tests     (primary, Stage 05)
test-jira-ticket      → write-unit-tests     (when development-level testing
                                              is explicitly appropriate)
```

The Stage 05 relationship is unchanged: `implement-jira-ticket` selects this skill whenever production behaviour changed, ahead of `create-development-pr`. `test-jira-ticket` reaches the same skill by a different door. The work performed is identical either way.

## Scope boundary

This is **developer, code-level testing**. It is deliberately separate from:

- `draft-test-cases` — QA test-specification design at Stage 03 — Analysis;
- `execute-qa-validation` — Stage 07 QA execution against a deployed build.

This skill writes and runs unit tests in the repositories that changed. It does not produce a QA test specification, does not execute a QA cycle, and does not claim QA sign-off. A green unit suite is not QA validation.

## Non-negotiable boundaries

- Never weaken, delete, skip, or relax an existing valid test to obtain a green run.
- Never change production behaviour to satisfy an incorrectly constructed test; fix the test.
- Never introduce a security bypass, disabled check, or test-only backdoor in production code.
- Never mock the unit under test.
- Never introduce a second test framework, fixture mechanism, or assertion style alongside the established one.
- Never write a hollow test purely to raise a coverage number.
- Never report a test as passing unless it actually ran and passed in this session.
- Never create a branch, commit, push, or Pull Request, and never write to Jira.
- Never claim QA sign-off, code review, or CI results.
- Never start destructive infrastructure, and never create or modify data in a shared or production database to make a test work.

## Read the guidance

Read [references/unit-testing-guidelines.md](references/unit-testing-guidelines.md) before writing or running anything.

## Workflow

### 1. Establish what changed — mandatory inspection

Do not work from a description of the change. Read the real diff and the real code:

- `git status` and `git diff` for the changed files in each repository;
- the changed production code itself, including its collaborators and error paths;
- the acceptance criteria the change implements;
- any contract the change established or consumed — API shape, schema, component inputs and outputs;
- the existing tests that already cover the touched code.

From that, list the behaviours that changed and the behaviours that could plausibly break.

### 2. Adopt the repository's test conventions

Inspect and reuse:

- the existing test framework and runner;
- existing fixtures, factories, builders, and test-data helpers;
- the existing mocking or stubbing approach;
- naming conventions for test classes, files, and cases;
- directory organization and file placement;
- the assertions library and style.

Discover the test commands from build files, package manifests and scripts, CI configuration, and contributor documentation. Do not assume a command exists.

### 3. Determine the required coverage

For each changed behaviour, cover what the ticket actually specifies:

- **success cases** — the acceptance criterion's main flow;
- **failure cases** — rejected input, rule violations, and failures from collaborators, integrations, and persistence;
- **boundary cases** — limits, empty and maximum values, first and last elements, and time or range edges named in the criteria;
- **regression cases** — the specific behaviour the change could plausibly break.

Skip a category only when the change genuinely has no such case, and say so rather than writing a hollow test.

When fixing a defect, add a regression test that fails against the original behaviour where the repository makes that practical.

### 4. Write the tests

- Test observable behaviour, not implementation details that a harmless refactor would break.
- Mock dependencies at the boundary the repository already mocks, and no deeper.
- Keep tests deterministic: no reliance on wall-clock timing, network access, execution order, or shared mutable state unless the repository provides a controlled mechanism.
- When an existing test legitimately encodes behaviour the ticket changes, update it deliberately and state which test changed and why.

### 5. Run the relevant suites

Run narrowest first: the new and updated tests, then the module or package suite for each repository that changed. Run the broader suite when practical.

When a test fails, determine whether the production change or the test is wrong, fix the correct one, and rerun. Distinguish pre-existing and environmental failures from failures caused by this change, with evidence.

### 6. Report

Produce the completion output below with real commands and real results.

## Completion output

```markdown
## Unit Tests

Jira: AMRIT-1234
Repositories: <repository>, <repository>

### Changed behaviour identified

- <behaviour> — from `<file>`

### Tests added or updated

- `<TestClass#case>` — success
- `<TestClass#case>` — validation failure
- `<TestClass#case>` — boundary
- `<TestClass#case>` — regression for <defect behaviour>

### Existing tests deliberately updated

- `<test>` — <why the expected behaviour legitimately changed>

### Coverage gaps

- <behaviour not covered and why, or "None">

### Executed

- `<command>` — PASS
- `<command>` — FAILED — <cause and current status>
- `<command>` — NOT RUN — <reason>

### Blockers

None.
```

## Final quality gate

- the actual production diff was inspected, not a description of it;
- every changed behaviour is either covered or listed as a gap with a reason;
- success, failure, and boundary cases are covered where they exist;
- a defect fix carries a regression test, or the impracticality is stated;
- the repository's existing framework, fixtures, mocks, naming, and organization were reused;
- no existing valid test was weakened, skipped, or deleted;
- no production behaviour was changed to make a test pass;
- no test-only backdoor or security bypass was introduced;
- tests are deterministic and do not touch shared or production systems;
- every reported command actually ran, with honest `FAILED` and `NOT RUN` reasons;
- no branch, commit, push, Pull Request, Jira write, or QA sign-off claim occurred.
