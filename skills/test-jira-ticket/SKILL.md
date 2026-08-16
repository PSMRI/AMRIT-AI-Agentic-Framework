---
name: test-jira-ticket
description: "Perform the testing activity that an AMRIT Jira ticket's lifecycle position actually calls for, acting as the testing orchestrator across Stage 03, Stage 05, and Stage 07: read the Jira issue, its status, acceptance criteria, linked requirements and approved design, then establish what testing evidence already exists — QA test cases, implemented code, unit tests, a deployed QA build — and route to exactly one or more of draft-test-cases for QA test design at Analysis, the existing write-unit-tests for code-level developer testing during Development, and execute-qa-validation for QA execution against a real build In QA. This is lifecycle-aware routing, not a pipeline that runs all three. Do not design QA test cases from an implementation, do not invent unit tests for code that does not exist, do not regenerate agreed test cases to match what was built, do not modify production code from a QA failure, and never claim QA approval."
metadata:
  stage: Cross-stage — Testing meta-skill (Stage 03, Stage 05, Stage 07)
  category: Quality Assurance
  primary_role: Testing orchestrator (QA Test Analyst / SDET / QA Tester)
  skill_type: Meta-skill / orchestrator
  knowledge_sources:
    - Jira
    - Confluence
    - DeepWiki
    - Graphify
    - OpenProject
    - Checked-out AMRIT repositories
    - Deployed QA build and test environment
  supported_inputs:
    - Jira Story at any testable lifecycle stage
    - Jira Task at any testable lifecycle stage
    - Jira Bug requiring test design, unit coverage, or QA verification
  primary_input: Jira ticket plus its lifecycle position and available artifacts
  primary_output: The testing deliverable appropriate to that lifecycle position, plus a routing report
  specialist_skills:
    - draft-test-cases
    - write-unit-tests
    - execute-qa-validation
  related_skills:
    - implement-jira-ticket
---

# Test Jira Ticket

Act as the AMRIT testing orchestrator for one Jira ticket. Work out **where the ticket actually is**, what testing evidence already exists, and which testing activity is genuinely appropriate — then run that activity through the right specialist and report what was done.

```text
/test-jira-ticket AMRIT-1234
```

```text
Test AMRIT-1234
```

Users do not select the testing specialist by hand. This skill routes the ticket.

## This is routing, not a pipeline

**Never run all three specialists by default.** The three testing activities answer different questions at different lifecycle positions, and running the wrong one produces actively harmful output:

| Wrong route | What it produces |
| --- | --- |
| QA test design derived from an implementation | A specification that ratifies whatever the code does, including its defects |
| Unit tests for a ticket with no implementation | Invented tests for code that does not exist |
| QA execution with no build | A fabricated pass, or a documentation review presented as validation |
| Regenerated test cases at Stage 07 | Agreed QA scope silently replaced by the implementation's behaviour |

Select the activity from evidence. State what was selected, what was excluded, and why.

## The three testing responsibilities

| Skill | Lifecycle | Question answered | Artifact |
| --- | --- | --- | --- |
| [`draft-test-cases`](../draft-test-cases/README.md) | Stage 03 — Analysis | What must QA test to prove this requirement works? | Functional QA test **specifications** |
| [`write-unit-tests`](../write-unit-tests/README.md) | Stage 05 — In Development | What code-level tests verify the changed code? | Executable **unit-test code** with real results |
| [`execute-qa-validation`](../execute-qa-validation/README.md) | Stage 07 — In QA | Does the deployed build satisfy the agreed requirements and test cases? | **Execution results and evidence** |

These are three different artifacts with three different owners. Never describe all three as "test cases".

## Relationship to `implement-jira-ticket`

Two meta-skills, two responsibilities, no competition:

```text
                  AMRIT Jira Ticket
                         |
          ┌──────────────┴──────────────┐
          |                             |
          v                             v
 implement-jira-ticket             test-jira-ticket
   Engineering META                  Testing META
          |                             |
   persona routing              lifecycle routing
          |                             |
 Backend / Frontend              draft-test-cases
 Android / DB / etc.             write-unit-tests
          |                      execute-qa-validation
          |
   write-unit-tests
          |
 create-development-pr
```

- `implement-jira-ticket` — **implement this ticket.**
- `test-jira-ticket` — **perform the appropriate testing activity for this ticket's lifecycle position.**

`write-unit-tests` belongs to both paths. Its primary relationship remains the Stage 05 one: `implement-jira-ticket` selects it whenever production behaviour changed, and that is unchanged by this skill. `test-jira-ticket` routes to the same specialist when development-level testing is explicitly appropriate. One specialist, two orchestration paths, no duplicated logic.

Never re-implement a specialist's work inside this skill when the specialist is available.

## Non-negotiable boundaries

- Jira is read-only. Never transition an issue, comment, edit a field, assign a user, create a subtask, or change status. The only exception is an explicitly authorized defect raised by `execute-qa-validation` under its own rules.
- Confluence is read-only. Never create, edit, comment on, or publish a page.
- Never create or rename a branch, commit, push, or open a Pull Request.
- Never derive a QA expected result from an implementation's observed behaviour.
- Never invent unit tests for an implementation that does not exist.
- Never report a QA PASS that was not observed against a real build, and never substitute documentation, code reading, or a green unit suite for QA execution.
- Never regenerate or edit agreed QA test cases so that an implementation passes them.
- Never modify production code, configuration, or a migration in response to a QA failure.
- Never claim QA approval, QA sign-off, code review, CI results, or release approval.
- Never fabricate a ticket status, artifact, test result, tool, environment, or defect key.
- Never expose credentials, tokens, private URLs, or real beneficiary or patient data.

If asked to perform a prohibited operation, decline that part and continue with the authorized testing work.

## Read the guidance

Before routing, read:

- [references/testing-lifecycle-routing.md](references/testing-lifecycle-routing.md) for stage detection, the routing decision table, evidence gates, and every ambiguous case.
- [references/testing-orchestration-workflow.md](references/testing-orchestration-workflow.md) for the full assessment, invocation, and reporting sequence.

Before reporting, read:

- [references/testing-traceability.md](references/testing-traceability.md)

Use files in [examples/](examples/) only as fictional shape references. They do not describe real AMRIT tickets, builds, or defects.

## Discover capabilities

Discover the connected tools' actual names and schemas; do not hardcode MCP function names or assume one host implementation.

This skill conceptually requires:

- Jira read/search capability;
- Confluence read/search capability;
- repository-research capability such as DeepWiki, and Graphify only as a final fallback;
- delivery-context capability such as OpenProject, when the environment provides it;
- host filesystem and repository access, to establish whether an implementation exists;
- host command execution;
- access to a deployed QA build, when QA execution is the selected activity;
- the host's mechanism for invoking another skill.

Use read operations only. If a knowledge source is unavailable, continue on the remaining evidence and say so. If the Jira issue cannot be retrieved, stop and report that; never invent the ticket or its stage.

## Workflow

Details are in [references/testing-orchestration-workflow.md](references/testing-orchestration-workflow.md).

### 1. Read the Jira ticket

Read the full issue: type, summary, description, **status**, every acceptance criterion, parent Epic, linked issues, subtasks, dependencies, attachments, decision-bearing comments, components, labels, fix version, sprint, and linked Confluence pages.

The status is the primary lifecycle signal, but it is not the only one. Verify it against the artifacts that actually exist.

### 2. Establish the lifecycle position

Determine, from evidence rather than assumption:

- the ticket's current status and its mapped lifecycle stage;
- whether requirements and acceptance criteria exist;
- whether an approved Stage 03 technical design exists;
- whether QA test cases already exist;
- whether an implementation exists, in the checked-out repositories;
- whether the source code is accessible;
- whether unit tests exist for the changed behaviour;
- whether a deployed QA or test build exists and is reachable;
- what the user actually asked for.

Record each as **present**, **absent**, or **unknown — could not verify**. Never record an artifact as present because a stage implies it should be.

### 3. Apply user intent

An explicit request overrides stage inference — but never overrides a missing prerequisite.

```text
"Write unit tests for AMRIT-1234"   → write-unit-tests, if an implementation exists
"Draft QA test cases for AMRIT-1234" → draft-test-cases
"Run QA on AMRIT-1234"               → execute-qa-validation, if a build is reachable
"Test AMRIT-1234"                    → route from the lifecycle position
```

When intent conflicts with the evidence — QA execution requested with no build, unit tests requested with no implementation — report the gap and offer the activity that is genuinely possible. Do not fabricate the prerequisite.

### 4. Select the testing activity

Apply the routing table below and in [references/testing-lifecycle-routing.md](references/testing-lifecycle-routing.md). Selecting more than one activity is legitimate when the evidence supports each independently; selecting all three by habit is not.

### 5. Invoke the specialist

Invoke through the host's skill mechanism, passing the ticket key, the acceptance criteria in scope, the artifacts located and their references, the boundaries, and what must be reported back.

When the specialist skill is not installed, read its canonical `SKILL.md` from `skills/<specialist-name>/SKILL.md` and follow it, or apply its contract inline — and record which mechanism was used. Never claim a specialist ran when the work was done inline.

### 6. Report

Produce the routing and testing report below, built from what actually happened.

## Lifecycle routing

```text
                         test-jira-ticket
                            META-SKILL
                                |
              lifecycle-aware test orchestration
                                |
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
     draft-test-cases     write-unit-tests    execute-qa-validation
       QA test design       code-level         QA execution
                            unit testing
            │                   │                   │
      Stage 03              Stage 05             Stage 07
       Analysis          In Development           In QA
```

| Lifecycle position | Activity | Specialist | Required evidence |
| --- | --- | --- | --- |
| Stage 03 — Analysis | QA test design | `draft-test-cases` | Acceptance criteria or an approved requirement set |
| Stage 04 — Ready for Development | Usually none | — | QA test cases are a Definition of Ready artifact; draft them if missing |
| Stage 05 — In Development | Code-level unit testing | `write-unit-tests` | An implementation exists and the source is accessible |
| Stage 06 — Pending QA | Usually none | — | Existing QA test cases may be reviewed or refined by `draft-test-cases` |
| Stage 07 — In QA | QA execution | `execute-qa-validation` | Agreed QA test cases **and** a reachable deployed build |
| Stage 08 — QA Approved | None | — | Human accountability gate |

### Stage 03 — Analysis

```text
test-jira-ticket
      |
      v
draft-test-cases
```

The implementation may not exist yet, and that is normal. Do **not** attempt QA execution. Do **not** invent unit-test code for an implementation that does not exist.

### Stage 05 — In Development

Unit testing remains primarily part of the implementation flow:

```text
implement-jira-ticket
      |
      v
write-unit-tests
```

When `test-jira-ticket` is invoked for development-level testing — the ticket is in development, or the user explicitly asked for unit tests — it routes to the same existing specialist:

```text
test-jira-ticket
      |
      v
write-unit-tests
```

Do not duplicate unit-testing logic here, and do not change how `implement-jira-ticket` selects it.

If the ticket is in development and no QA test cases exist, say so and offer `draft-test-cases`: QA test cases are a Stage 04 Definition of Ready artifact, and their absence is a real gap worth reporting.

### Stage 07 — In QA

```text
test-jira-ticket
      |
      v
execute-qa-validation
```

Consume the previously agreed QA test cases. **Do not silently regenerate them based on what the implementation happens to do.** If none exist, say so, execute against the acceptance criteria directly, label the run criteria-driven, and recommend `draft-test-cases` for a reviewed specification.

If no build is reachable, the run is blocked and reports `Executed: 0`. Never substitute documentation for execution.

## Evidence gates

A stage never authorizes an activity on its own. Each activity has a prerequisite that must be verified:

| Activity | Prerequisite | If absent |
| --- | --- | --- |
| `draft-test-cases` | Acceptance criteria or an approved requirement set | Stop; report that the requirement is missing. Never invent it. |
| `write-unit-tests` | An implementation exists and the source is accessible | Do not route. Report that there is nothing to test yet. |
| `execute-qa-validation` | A reachable deployed build | Route so it produces the blocked report, or report the gap directly. Never a PASS. |

## Lifecycle exclusions

This skill deliberately covers **no** activity at:

- **Stage 06 — Pending QA** — a lifecycle and queue state. Existing QA test cases may be reviewed or refined through `draft-test-cases`, but no dedicated handoff skill exists and none is wanted.
- **Stage 08 — QA Approved** — a human accountability gate. `execute-qa-validation` supplies the evidence; the human QA tester decides. This skill never claims to be that approver.
- **Stage 09 — Closed** — lifecycle and project-management action, not an agent skill.

Never invent an activity because the lifecycle has a stage.

## Human accountability

The agent designs, writes, and executes tests, and reports evidence. Humans approve.

QA test-case approval, code review, QA sign-off, CI results, and release approval are never produced, implied, or assumed. When a required approval is absent, report it as absent.

## Handling ambiguity

Do not ask unnecessary questions. For ordinary routing decisions, read the ticket and the artifacts and choose the activity the evidence supports.

Stop and ask only when the evidence genuinely cannot settle it — for example when the ticket status and the actual artifacts contradict each other in a way that changes which activity is correct, or when QA execution is requested and it is unclear which environment is the intended build under test. State what is known, what conflicts, and the precise decision required.

## Completion output

```markdown
## Testing Orchestration

Jira: AMRIT-1234 — <summary>

### Lifecycle assessment

- Jira status: <status>
- Lifecycle stage: Stage <nn> — <name>
- Acceptance criteria: present / absent
- Approved technical design: present — <ref> / absent
- Existing QA test cases: present — <ref> / absent
- Implementation: present — <repositories> / absent
- Source code accessible: yes / no
- Existing unit tests: present / absent
- Deployed QA build: reachable — <environment and version> / not reachable
- User intent: <explicit request, or "not specified — routed from lifecycle">

### Testing activity selected

- <activity> — <the evidence that selected it>

Considered and excluded:
- <activity> — <why the evidence excluded it>
- <activity> — <why the evidence excluded it>

### Specialist invoked

- <skill> — via <host skill mechanism / canonical SKILL.md / applied inline>

### Specialist output

<the specialist's own completion report, unmodified>

### Traceability

Acceptance criteria → test cases → <unit tests / execution evidence>

### Gaps and recommendations

- <missing artifact and the skill that would produce it, or "None">

### Human decision required

<what a human must decide, or "None beyond ordinary review">
```

Finish with exactly one of:

**Testing activity complete: <activity>. <specialist completion line>**

**Testing activity incomplete: <activity>. Resolve the items above.**

**Testing not started — <reason>. Required action: <what would unblock it>.**

None of these means the ticket is QA-approved, verified, or Done.

## Final quality gate

- the full Jira issue and its status were read, and Jira was not modified;
- the lifecycle position was established from evidence, not from status alone;
- every artifact was recorded as present, absent, or unverifiable — never assumed from the stage;
- exactly the activities the evidence supports were selected, and every exclusion is stated with its reason;
- no activity ran without its prerequisite;
- QA test design was not derived from an implementation;
- no unit tests were invented for an implementation that does not exist;
- agreed QA test cases were consumed as written and not regenerated;
- no QA PASS rests on documentation, code reading, or a unit-test result;
- no production code was modified in response to a QA failure;
- the specialist was invoked rather than re-implemented, and the invocation mechanism is recorded;
- no skill was claimed to have run when the work was performed inline;
- no activity was invented for Stage 06, Stage 08, or Stage 09;
- no approval, sign-off, or CI result was fabricated or implied;
- no branch, commit, push, Pull Request, or unauthorized Jira write occurred;
- the report ends with the correct completion line.
