# Testing Lifecycle Routing

## Contents

- [Scope of this document](#scope-of-this-document)
- [Routing principle](#routing-principle)
- [The AMRIT lifecycle and its testing coverage](#the-amrit-lifecycle-and-its-testing-coverage)
- [Establishing the lifecycle position](#establishing-the-lifecycle-position)
- [The artifact inventory](#the-artifact-inventory)
- [The routing decision table](#the-routing-decision-table)
- [Evidence gates](#evidence-gates)
- [User intent](#user-intent)
- [Ambiguous and conflicting cases](#ambiguous-and-conflicting-cases)
- [Multiple activities in one run](#multiple-activities-in-one-run)
- [Stages with no testing activity](#stages-with-no-testing-activity)
- [Reporting the routing decision](#reporting-the-routing-decision)
- [Review checklist](#review-checklist)

## Scope of this document

Deciding which testing activity a ticket actually needs, from its lifecycle position, its available artifacts, and the user's intent.

## Routing principle

The testing activity is selected from evidence, never from habit and never from the fact that a specialist skill exists.

The route is determined by four things together:

1. the Jira ticket, its status, and its acceptance criteria;
2. the artifacts that actually exist — requirements, approved design, QA test cases, implementation, unit tests, deployed build;
3. what can actually be accessed from this environment;
4. the user's explicit intent, where they stated one.

**This is not a pipeline.** A ticket at Analysis gets test design. A ticket in Development gets unit testing. A ticket in QA gets execution. Running all three by default produces harmful output, not thorough output.

## The AMRIT lifecycle and its testing coverage

The authoritative stage numbering:

```text
Stage 03 — Analysis                  draft-test-cases
Stage 04 — Ready for Development     no testing specialist required
Stage 05 — In Development            write-unit-tests
Stage 06 — Pending QA                no dedicated skill
Stage 07 — In QA                     execute-qa-validation
Stage 08 — QA Approved               human gate
```

In Development is **Stage 05**, not Stage 04. Stage 04 is the Ready for Development readiness state.

## Establishing the lifecycle position

The Jira status is the primary signal. It is not sufficient on its own, because a ticket's status and its actual state routinely diverge: a ticket can sit In Development with no code written, or In QA with nothing deployed.

Establish the position by:

1. reading the Jira status and mapping it to a lifecycle stage;
2. taking the artifact inventory below;
3. reconciling the two.

Where the status and the artifacts disagree, **the artifacts decide what is possible** and the disagreement is reported. A ticket marked In QA with no reachable build cannot be QA-executed no matter what the status says.

## The artifact inventory

Record each item as **present**, **absent**, or **unknown — could not verify**. Never record an artifact as present because the stage implies it should exist.

| Artifact | How to establish it | Why it matters |
| --- | --- | --- |
| Acceptance criteria | The Jira issue | Prerequisite for all three activities |
| Requirement set — BRD, FRD, business rules | Confluence, linked from Jira | Source of agreed expected results |
| Approved Stage 03 technical design | Confluence | Informs test design and integration scope |
| Existing QA test cases | Confluence, the configured test-management source, or a prior `draft-test-cases` output | Decides design versus execution, and whether execution has agreed scope |
| Implementation | The checked-out repositories — `git status`, `git diff`, branch and file inspection | Prerequisite for unit testing |
| Source code accessible | Whether the repositories are actually checked out here | A missing repository blocks unit testing |
| Existing unit tests | Test directories covering the changed behaviour | Decides whether coverage must be added or extended |
| Deployed QA build | The environment actually responding, with a confirmable version | Prerequisite for QA execution |

The inventory is the routing input. Take it before deciding anything.

## The routing decision table

| Stage | Implementation | QA test cases | Build reachable | Route |
| --- | --- | --- | --- | --- |
| 03 — Analysis | absent | absent | — | `draft-test-cases` |
| 03 — Analysis | absent | present | — | `draft-test-cases` to review and extend, or report the specification as already complete |
| 04 — Ready for Development | absent | present | — | No activity; report the ticket as test-ready |
| 04 — Ready for Development | absent | absent | — | `draft-test-cases` — a Definition of Ready artifact is missing |
| 05 — In Development | present | — | — | `write-unit-tests`; report a missing QA specification as a gap |
| 05 — In Development | absent | — | — | No unit testing is possible; report that there is nothing to test yet |
| 06 — Pending QA | present | present | — | No activity; the specification may be reviewed through `draft-test-cases` on request |
| 06 — Pending QA | present | absent | — | `draft-test-cases` — QA has no agreed scope to execute |
| 07 — In QA | present | present | yes | `execute-qa-validation` |
| 07 — In QA | present | present | no | `execute-qa-validation` producing its blocked report, or report the gap directly. Never a PASS |
| 07 — In QA | present | absent | yes | `execute-qa-validation` criteria-driven, and recommend `draft-test-cases` |
| 08 — QA Approved | — | — | — | No activity; human gate |

A dash means the column does not affect that row's decision.

## Evidence gates

A stage never authorizes an activity by itself. Each activity has a prerequisite that must be verified before routing:

| Activity | Prerequisite | When the prerequisite is absent |
| --- | --- | --- |
| `draft-test-cases` | Acceptance criteria or an approved requirement set | Stop. Report that the requirement is missing and name what is needed. Never invent a requirement to have something to test. |
| `write-unit-tests` | An implementation exists and its source is accessible | Do not route. Report that there is nothing to test yet. Never invent tests for code that does not exist, and never write tests against a documented design. |
| `execute-qa-validation` | A reachable deployed build | Route so the specialist produces its blocked report with `Executed: 0`, or report the gap directly. Never a PASS, and never a documentation review presented as validation. |

An absent prerequisite is a finding to report, not an obstacle to work around.

## User intent

An explicit request overrides stage inference. It never overrides a missing prerequisite.

| The user says | Route |
| --- | --- |
| "Test AMRIT-1234" | From the lifecycle position |
| "Draft QA test cases for AMRIT-1234" | `draft-test-cases` |
| "Write unit tests for AMRIT-1234" | `write-unit-tests`, if an implementation exists |
| "Run QA on AMRIT-1234" | `execute-qa-validation`, if a build is reachable |
| "Has AMRIT-1234 been tested?" | No activity — take the inventory and report the testing state |

When intent conflicts with the evidence, report the conflict and offer what is genuinely possible:

```text
QA execution was requested for AMRIT-1234, but no QA build is reachable
from this environment.

What is possible now:
- draft-test-cases — the ticket has acceptance criteria and no agreed QA
  test cases

Required to run QA execution:
- a reachable QA environment with the change deployed
```

Never fabricate a prerequisite, and never quietly substitute a different activity without saying so.

## Ambiguous and conflicting cases

| Situation | Correct action |
| --- | --- |
| Status says In QA, no build is reachable | Report the conflict; produce the blocked outcome, never a PASS |
| Status says In Development, no code exists | Report it; offer `draft-test-cases` if QA test cases are missing |
| Status says Analysis, an implementation already exists | Still route to `draft-test-cases`, and design from the requirement — never from the implementation. Note the divergence |
| QA test cases exist but contradict the current acceptance criteria | Report the conflict; do not silently prefer either. Recommend a specification review |
| The ticket is a Bug with no acceptance criteria | Treat the reported defect behaviour and its expected behaviour as the criterion, and say that you did |
| The ticket has no status this framework maps | Route from the artifacts alone and state that the status was unmapped |
| The Jira issue cannot be retrieved | Stop. Never invent the ticket, its status, or its criteria |

## Multiple activities in one run

Selecting more than one activity is legitimate when each is independently supported by evidence — for example, a ticket in Development whose implementation exists and which never received QA test cases:

```text
Selected:
- write-unit-tests    — implementation exists in <repository>
- draft-test-cases    — no QA test cases exist; a Stage 04 Definition of
                        Ready artifact is missing

Excluded:
- execute-qa-validation — no deployed build; the change is not released to QA
```

When two activities run, order them by dependency: test design before execution, implementation before unit tests. Never run an activity merely because another one ran.

Selecting all three at once is almost always a routing error. If the evidence genuinely supports all three, state the evidence for each separately.

## Stages with no testing activity

| Stage | Why no skill | What may still happen |
| --- | --- | --- |
| Stage 04 — Ready for Development | A human Definition of Ready check | Report missing QA test cases as a readiness gap |
| Stage 06 — Pending QA | A lifecycle and queue state | Existing QA test cases may be reviewed or refined through `draft-test-cases` on request |
| Stage 08 — QA Approved | A human accountability gate | `execute-qa-validation` supplies evidence; the human decides |
| Stage 09 — Closed | A project-management action | Nothing |

No `prepare-qa-handoff`, `check-qa-approval-readiness`, or `prepare-ticket-closure` skill exists, and none is wanted. Never invent an activity because the lifecycle has a stage.

## Reporting the routing decision

The report always states:

- the Jira status and the mapped lifecycle stage;
- the full artifact inventory, with unverifiable items marked as such;
- the activity or activities selected, each with the evidence that selected it;
- the activities considered and excluded, each with its reason;
- the specialist invoked and the invocation mechanism used;
- gaps found, and the skill that would close each one.

An exclusion without a reason is not a routing decision, and a stage-based route with no artifact inventory behind it is a guess.

## Review checklist

- the ticket status was read and mapped to the correct stage number;
- In Development was treated as Stage 05, never Stage 04;
- the artifact inventory was taken before routing;
- no artifact was assumed present because the stage implies it;
- status-versus-artifact conflicts were reported, and the artifacts decided what was possible;
- every selected activity passed its evidence gate;
- every exclusion carries a reason;
- explicit user intent was honoured, except where a prerequisite was genuinely missing;
- no activity was invented for Stage 04, 06, 08, or 09;
- no prerequisite was fabricated to enable an activity.
