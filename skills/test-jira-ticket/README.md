# test-jira-ticket

`test-jira-ticket` is the **testing meta-skill** and the entry point for testing work across the AMRIT lifecycle. It takes one Jira ticket, works out where it actually is, establishes what testing evidence already exists, and runs the testing activity that position genuinely calls for.

**This skill routes. It does not implement the specialists' work.**

## Purpose

Answer one question per ticket:

> What testing activity is appropriate for this ticket right now, and what does it produce?

## Invocation

```text
/test-jira-ticket AMRIT-1234
```

```text
Test AMRIT-1234
```

Users do not select the testing specialist by hand. If no ticket key is supplied, the skill asks for one before researching.

## Testing architecture

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

## This is routing, not a pipeline

The three activities answer different questions. Running all three by default produces harmful output, not thorough output:

| Wrong route | What it produces |
| --- | --- |
| QA test design derived from an implementation | A specification that ratifies whatever the code does, defects included |
| Unit tests for a ticket with no implementation | Invented tests for code that does not exist |
| QA execution with no build | A fabricated pass, or a documentation review dressed as validation |
| Regenerated test cases at Stage 07 | Agreed QA scope silently replaced by the build's behaviour |

## Three different testing artifacts

| Skill | Stage | Question | Artifact |
| --- | --- | --- | --- |
| [`draft-test-cases`](../draft-test-cases/README.md) | Stage 03 — Analysis | What must QA test to prove this requirement works? | Functional QA test **specifications** |
| [`write-unit-tests`](../write-unit-tests/README.md) | Stage 05 — In Development | What code-level tests verify the changed code? | Executable **unit-test code** with real results |
| [`execute-qa-validation`](../execute-qa-validation/README.md) | Stage 07 — In QA | Does the deployed build satisfy the agreed requirements and test cases? | **Execution results and evidence** |

Three artifacts, three owners. They are never all called "test cases".

## Lifecycle routing

| Lifecycle position | Activity | Specialist | Required evidence |
| --- | --- | --- | --- |
| Stage 03 — Analysis | QA test design | `draft-test-cases` | Acceptance criteria or an approved requirement set |
| Stage 04 — Ready for Development | Usually none | — | Missing QA test cases are reported as a readiness gap |
| Stage 05 — In Development | Code-level unit testing | `write-unit-tests` | An implementation exists and the source is accessible |
| Stage 06 — Pending QA | Usually none | — | Existing test cases may be reviewed through `draft-test-cases` |
| Stage 07 — In QA | QA execution | `execute-qa-validation` | Agreed QA test cases **and** a reachable deployed build |
| Stage 08 — QA Approved | None | — | Human accountability gate |

In Development is **Stage 05**, never Stage 04.

## Evidence gates

A stage never authorizes an activity on its own:

| Activity | Prerequisite | If absent |
| --- | --- | --- |
| `draft-test-cases` | Acceptance criteria or an approved requirement set | Stop and report; never invent a requirement |
| `write-unit-tests` | An implementation exists and its source is accessible | Do not route; report that there is nothing to test yet |
| `execute-qa-validation` | A reachable deployed build | Blocked report with `Executed: 0`; never a PASS |

## Relationship to `implement-jira-ticket`

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

- [`implement-jira-ticket`](../implement-jira-ticket/README.md) — **implement this ticket.**
- `test-jira-ticket` — **perform the appropriate testing activity for this ticket's lifecycle position.**

They do not compete.

## `write-unit-tests` is reused, never duplicated

`write-unit-tests` participates in both orchestration paths:

```text
implement-jira-ticket → write-unit-tests     (primary, Stage 05, unchanged)
test-jira-ticket      → write-unit-tests     (when development-level testing is
                                              explicitly appropriate)
```

One specialist, two doors. Its Stage 05 relationship with `implement-jira-ticket` — selected whenever production behaviour changed, ahead of `create-development-pr` — is unchanged by this skill, and no unit-testing logic is copied into the meta-skill.

## Lifecycle exclusions

No skill exists for, and none is wanted for:

- **Stage 06 — Pending QA** — a lifecycle and queue state. Existing test cases may be reviewed through `draft-test-cases`; there is no `prepare-qa-handoff`.
- **Stage 08 — QA Approved** — a human accountability gate. There is no `check-qa-approval-readiness`, and this skill never claims to be the QA approver.
- **Stage 09 — Closed** — a project-management action. There is no `prepare-ticket-closure`.

An activity is never invented because the lifecycle has a stage.

## Traceability

```text
Business Requirement → FRD → JIRA Story → Acceptance Criterion → QA Test Case
    → Implementation → Unit Tests → QA Execution → Evidence → PASS / Defect
```

Identifiers are preserved rather than matched by prose. The routing report shows each acceptance criterion's current position in that chain and names the skill that would close each gap.

## Boundaries

Jira and Confluence are read-only — the only exception being a defect explicitly authorized under `execute-qa-validation`'s own rules. No branch, commit, push, or Pull Request. No production code is modified in response to a QA failure. No QA approval, code review, CI result, or release approval is ever claimed.

## Human accountability

The agent designs, writes, and executes tests and reports evidence. Humans approve. QA approval remains a human decision at Stage 08, and this skill never claims to be that approver.

## Required capabilities

Read access to Jira and Confluence, DeepWiki and Graphify where available, OpenProject where the environment provides it, host filesystem and repository access to establish whether an implementation exists, host command execution, access to a deployed QA build when QA execution is selected, and the host's skill-invocation mechanism. Tool names are discovered, not hardcoded.

Every specialist is independently installable. When one is not installed, the meta-skill applies its contract inline, at the same standard, and says that it did so.

## Examples

```text
/test-jira-ticket AMRIT-101    Analysis        → draft-test-cases
/test-jira-ticket AMRIT-102    In Development  → write-unit-tests
/test-jira-ticket AMRIT-103    In QA           → execute-qa-validation
```

See [examples/sample-lifecycle-routing.md](examples/sample-lifecycle-routing.md) for the three routing walk-throughs with full artifact inventories, and [examples/sample-qa-outcomes.md](examples/sample-qa-outcomes.md) for a QA run with manual tests outstanding and a QA failure producing a defect without any code being changed. The examples are illustrative only and do not describe real AMRIT tickets, builds, or defects.

## Use and distribution

Invoke `/test-jira-ticket` from the repository root using a supported coding agent. For a packaged installation, download `test-jira-ticket.zip` from the latest release, together with the testing specialist packages you want available. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
