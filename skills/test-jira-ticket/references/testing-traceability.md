# Testing Traceability

## Contents

- [Scope of this document](#scope-of-this-document)
- [The full traceability chain](#the-full-traceability-chain)
- [Which skill owns which segment](#which-skill-owns-which-segment)
- [Preserve identifiers, not prose](#preserve-identifiers-not-prose)
- [What the meta-skill records](#what-the-meta-skill-records)
- [Reporting a broken chain](#reporting-a-broken-chain)
- [Three artifacts, never conflated](#three-artifacts-never-conflated)
- [Review checklist](#review-checklist)

## Scope of this document

Keeping the testing evidence for one ticket traceable across the three testing activities and the stages they occur in, so a result at any point can be traced back to the business requirement it came from.

## The full traceability chain

```text
Business Requirement
        ↓
FRD
        ↓
JIRA Story
        ↓
Acceptance Criterion
        ↓
QA Test Case
        ↓
Implementation
        ↓
Unit Tests
        ↓
QA Execution
        ↓
Evidence
        ↓
PASS / Defect
```

No single skill owns the whole chain. Each owns a segment and preserves the identifiers the next segment needs.

## Which skill owns which segment

| Segment | Owner | Stage |
| --- | --- | --- |
| Business Requirement → FRD → Jira Story → Acceptance Criterion | Upstream skills — `create-brd`, `create-product-backlog` | 01, 02 |
| Acceptance Criterion → QA Test Case | `draft-test-cases` | 03 |
| Acceptance Criterion → Implementation | `implement-jira-ticket` and its specialists | 05 |
| Implementation → Unit Tests | `write-unit-tests` | 05 |
| QA Test Case → QA Execution → Evidence → PASS / Defect | `execute-qa-validation` | 07 |
| Recording which segment this run produced, and which are missing | `test-jira-ticket` | Cross-stage |

`write-unit-tests` sits in this chain once, under both orchestration paths. `implement-jira-ticket` selects it during implementation; `test-jira-ticket` selects it when development-level testing is explicitly appropriate. Same specialist, same segment, no duplication.

## Preserve identifiers, not prose

Downstream skills match on identifiers. Prose matching fails the moment wording is edited.

| Level | Identifier | Rule |
| --- | --- | --- |
| BRD / FRD requirement | The source document's own identifier | Carry it verbatim |
| Jira ticket | `AMRIT-1234` | Verbatim |
| Acceptance criterion | The ticket's numbering, otherwise `AC-n` assigned at Stage 03 | Record when assigned |
| QA test case | `TC-nn` | Never reused, never renumbered |
| Unit test | Test class and case name | Recorded against the behaviour and criterion it covers |
| Execution result | `TC-nn` plus the build identifier | Anchored to a specific deployed state |
| Defect | The Jira defect key, once actually created | Never fabricated |

When passing work to a specialist, pass the identifiers rather than a paraphrase. When receiving output, keep the identifiers the specialist used.

## What the meta-skill records

The routing report is where the chain is visible for one run:

```text
### Traceability

AC-1 (FRD-REQ-112) → TC-01, TC-02        → executed: PASS, PASS
AC-2 (FRD-REQ-113) → TC-04               → executed: FAIL → defect drafted
AC-3 (FRD-REQ-114) → TC-06               → not executed: device unavailable
AC-4               → no test case         → gap: draft-test-cases required
```

Every row states which segment exists and which does not. A gap in the chain is a finding, not an omission from the report.

Record also which artifacts this run produced and which it consumed, so the next run knows what it inherits:

```text
Consumed: QA test specification for AMRIT-1234 (Stage 03, TC-01 to TC-07)
Produced: QA execution results against build 2.14.0-qa.37
```

## Reporting a broken chain

| Break | Report |
| --- | --- |
| An acceptance criterion has no test case | Gap — `draft-test-cases` required |
| A test case has no acceptance criterion | Either it covers regression, which must be stated, or it tests something nobody asked for — investigate and say which |
| Changed behaviour has no unit test | Gap — `write-unit-tests` required |
| A test case was never executed | Not executed, with the reason and the required action |
| An execution result names no build | The result is not evidence; re-run against an identified build |
| A failure has no defect | State whether it is drafted, proposed, or deliberately not raised |
| Existing QA test cases contradict the current acceptance criteria | Conflict — recommend a specification review; never prefer either silently |

Never close a gap by inventing the missing artifact. A ticket with no QA test cases at Stage 07 is a ticket whose QA scope was never agreed, and that is worth reporting.

## Three artifacts, never conflated

| Artifact | Produced by | Is not |
| --- | --- | --- |
| QA test specification | `draft-test-cases` | Test code; execution results |
| Unit-test code and its results | `write-unit-tests` | A QA specification; QA validation |
| QA execution results and evidence | `execute-qa-validation` | A specification; a unit-test run |

A green unit suite never satisfies a QA test case. A written QA specification never verifies anything. An execution result never redefines what was agreed.

Report each under its own heading with its own name. Do not merge them into one "tests" section, and do not call all three "test cases".

## Review checklist

- every produced artifact names the identifiers it consumed and the ones it produced;
- identifiers are carried verbatim, never paraphrased or renumbered;
- the traceability section shows each acceptance criterion's current position in the chain;
- gaps are reported with the skill that would close them;
- broken links are reported rather than closed by invention;
- execution results name the build they came from;
- the three artifacts are reported separately and never described interchangeably.
