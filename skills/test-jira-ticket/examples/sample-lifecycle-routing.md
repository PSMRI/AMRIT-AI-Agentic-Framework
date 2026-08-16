# Fictional Sample Lifecycle Routing

This example is fictional. The tickets, stages, repositories, and builds below are invented to show how the meta-skill routes different lifecycle positions. They do not describe real AMRIT tickets, builds, or architecture.

Routing is decided from the ticket status, the artifact inventory, and the user's intent — never from the fact that three testing specialists exist.

## Example 1 — Analysis

```text
/test-jira-ticket AMRIT-101

Ticket stage:
Analysis

Selected persona:
QA Test Analyst

Skill:
draft-test-cases

Output:
QA test specification
```

### Fictional routing report

```markdown
### Lifecycle assessment

- Jira status: Analysis
- Lifecycle stage: Stage 03 — Analysis
- Acceptance criteria: present — 4 criteria
- Approved technical design: present — "Registration duplicate prevention"
- Existing QA test cases: absent
- Implementation: absent — no branch or change found for this ticket
- Source code accessible: yes
- Existing unit tests: absent — nothing to cover
- Deployed QA build: not reachable — the change is not built
- User intent: not specified — routed from lifecycle

### Testing activity selected

- QA test design — the ticket is at Analysis with approved acceptance criteria
  and no existing QA test cases

Considered and excluded:
- write-unit-tests — no implementation exists; there is no changed behaviour to
  cover, and unit tests must never be invented for code that does not exist
- execute-qa-validation — no deployed build exists; QA execution would have
  nothing to test and could only produce a fabricated result

### Specialist invoked

- draft-test-cases — via the host skill mechanism
```

The implementation does not exist. That is normal at Stage 03, and it is exactly why the test cases can be written against the requirement rather than against the code.

## Example 2 — Development

```text
/test-jira-ticket AMRIT-102

Ticket stage:
In Development

Selected persona:
SDET

Skill:
write-unit-tests
```

### Fictional routing report

```markdown
### Lifecycle assessment

- Jira status: In Development
- Lifecycle stage: Stage 05 — In Development
- Acceptance criteria: present — 3 criteria
- Approved technical design: present
- Existing QA test cases: present — TC-01 to TC-09, agreed at Stage 03
- Implementation: present — DEMO-API, 4 changed files on the ticket branch
- Source code accessible: yes
- Existing unit tests: present — 2 cases touching the changed service, not
  covering the new behaviour
- Deployed QA build: not reachable — the change is not merged or deployed
- User intent: not specified — routed from lifecycle

### Testing activity selected

- Code-level unit testing — an implementation exists in DEMO-API with changed
  behaviour not covered by the existing tests

Considered and excluded:
- draft-test-cases — QA test cases already exist and were agreed at Stage 03;
  regenerating them now would risk replacing agreed scope with the
  implementation's behaviour
- execute-qa-validation — no deployed QA build; the change has not reached QA

### Specialist invoked

- write-unit-tests — via the host skill mechanism
```

Note what this route did **not** do. The Stage 05 relationship is unchanged: `implement-jira-ticket` still selects `write-unit-tests` during implementation, and this run reaches the same specialist by a different door. No unit-testing logic is duplicated in the meta-skill.

If the same ticket had **no** QA test cases, the report would additionally select `draft-test-cases` and note that a Stage 04 Definition of Ready artifact was missing.

## Example 3 — QA

```text
/test-jira-ticket AMRIT-103

Ticket stage:
In QA

Selected persona:
QA Tester

Skill:
execute-qa-validation
```

### Fictional routing report

```markdown
### Lifecycle assessment

- Jira status: In QA
- Lifecycle stage: Stage 07 — In QA
- Acceptance criteria: present — 4 criteria
- Approved technical design: present
- Existing QA test cases: present — TC-01 to TC-07, agreed at Stage 03
- Implementation: present — merged to release-2.14.0
- Source code accessible: yes
- Existing unit tests: present — executed green in CI on the merge commit
- Deployed QA build: reachable — QA, build 2.14.0-qa.37
- User intent: not specified — routed from lifecycle

### Testing activity selected

- QA execution — the ticket is In QA, agreed test cases exist, and a build
  carrying the change is reachable

Considered and excluded:
- draft-test-cases — an agreed specification already exists; regenerating it
  from the implementation would replace agreed QA scope with whatever the code
  does
- write-unit-tests — the implementation is complete and its unit tests ran
  green in CI; a green unit suite is not QA validation and does not substitute
  for it

### Specialist invoked

- execute-qa-validation — via the host skill mechanism
```

The agreed test cases are consumed as written. They are not regenerated, and no expected result is adjusted to match the build.

## Counter-example — what routing must never do

Given the same three tickets, this is the wrong behaviour:

```text
Wrong

/test-jira-ticket AMRIT-101   →  draft-test-cases
                              →  write-unit-tests        ← no implementation
                              →  execute-qa-validation   ← no build
```

Running all three produces invented unit tests for code that does not exist and a fabricated or vacuous QA result. The meta-skill is a router, not a pipeline.

```text
Wrong

/test-jira-ticket AMRIT-103   →  draft-test-cases regenerated from the
                                 implementation, then executed against it
```

Test cases derived from the implementation always pass. That is not validation; it is a description of the build with a PASS column attached.
