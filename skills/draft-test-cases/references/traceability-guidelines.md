# Traceability Guidelines

## Contents

- [Scope of this document](#scope-of-this-document)
- [The AMRIT testing traceability chain](#the-amrit-testing-traceability-chain)
- [Preserve identifiers, not prose](#preserve-identifiers-not-prose)
- [The traceability matrix](#the-traceability-matrix)
- [Coverage verdicts](#coverage-verdicts)
- [Bidirectional checks](#bidirectional-checks)
- [Handing traceability downstream](#handing-traceability-downstream)
- [Revising a specification later](#revising-a-specification-later)
- [Review checklist](#review-checklist)

## Scope of this document

Keeping a QA test specification traceable from the business requirement down to the individual test case, and keeping those identifiers usable by the skills that run later.

## The AMRIT testing traceability chain

```text
Business Requirement          BRD reference
        ↓
FRD                           FRD requirement identifier
        ↓
JIRA Story                    AMRIT-1234
        ↓
Acceptance Criterion          AC-3
        ↓
QA Test Case                  TC-07                 ← draft-test-cases produces this
        ↓
Implementation                changed code
        ↓
Unit Tests                    write-unit-tests
        ↓
QA Execution                  execute-qa-validation
        ↓
Evidence                      response, log, screenshot
        ↓
PASS / Defect                 AMRIT-XXXX
```

`draft-test-cases` owns the segment from the business requirement to the test case. Everything below the test case is produced later by other skills, and it can only be linked back if the identifiers this skill assigns are stable.

## Preserve identifiers, not prose

Downstream skills match on identifiers. Prose matching fails as soon as wording is edited.

| Level | Identifier | Rule |
| --- | --- | --- |
| BRD / FRD requirement | The source document's own identifier | Carry it verbatim; never renumber |
| Jira ticket | `AMRIT-1234` | Verbatim |
| Acceptance criterion | The ticket's own numbering, otherwise `AC-n` assigned here | State when you assigned it |
| Test case | `TC-nn` | Unique within the ticket's specification, never reused |

When an acceptance criterion derives from a numbered FRD requirement, record both in the test case's Requirement / AC field:

```text
Requirement / AC: AC-3 (FRD-REQ-114)
```

That single line lets a reviewer trace a failing test case back to the business requirement without re-reading the source documents.

## The traceability matrix

Every specification carries the matrix as its own section:

| AC | Requirement source | Test cases | Coverage |
| --- | --- | --- | --- |
| AC-1 | FRD-REQ-112 | TC-01, TC-02, TC-03 | Covered |
| AC-2 | FRD-REQ-113 | TC-04, TC-05 | Covered |
| AC-3 | FRD-REQ-114 | TC-06 | Partially covered — <what is not proven> |
| AC-4 | — | — | Not covered — <reason> |

Keep it separate from the test cases themselves so a reviewer can judge coverage at a glance.

## Coverage verdicts

| Verdict | Use when |
| --- | --- |
| Covered | Every condition the criterion states is proven by at least one test case |
| Partially covered | Some conditions are proven and a named condition is not |
| Not covered | No executable test case could be designed |
| Ambiguous | The criterion does not state enough to define an expected result |
| Conflicting | Two approved sources state different expected behaviour |

`Partially covered`, `Not covered`, `Ambiguous`, and `Conflicting` must each name the specific missing condition or the precise question. "Needs clarification" on its own is not a report.

Never record `Covered` for a criterion whose expected result is `TO BE CONFIRMED`.

## Bidirectional checks

Run both directions before finishing:

**Forward — every criterion is covered.** Walk the acceptance criteria; each has test cases or an explicit non-coverage verdict. A criterion silently absent from the matrix is a defect in the specification.

**Backward — every test case is justified.** Walk the test cases; each names the criterion or approved requirement it proves. A test case with no requirement behind it is either testing the implementation, testing something out of scope, or proving a requirement nobody wrote down. Investigate which, and either link it or remove it.

A case that legitimately covers general regression rather than a specific criterion records `Requirement / AC: Regression — <the existing behaviour and its source>`.

## Handing traceability downstream

`execute-qa-validation` consumes this specification and records, per test case, the expected result, the actual result, the verdict, and the evidence. It can only do that if:

- test case identifiers are stable;
- the acceptance criterion identifier travels with the test case;
- the expected result is decidable without asking the author;
- environment constraints are stated so unrunnable cases are identified as unrunnable rather than guessed.

A defect raised later carries `TC-07` and `AC-3`, which is what makes the failure traceable back to the business requirement, and what will make a future `root-cause-analysis` skill able to start from a clean input rather than from prose.

## Revising a specification later

The canonical creation point is Stage 03. A specification may be reviewed and refined at Stage 06 — Pending QA, or when a requirement legitimately changes.

When revising:

- never renumber an existing test case;
- add new cases with the next free number;
- mark a superseded case `Retired — <reason>` rather than deleting it, so historical execution records stay meaningful;
- record what changed and why in a revision section;
- re-run both bidirectional checks.

Never revise a test case's expected result to match an implementation that failed it. If the requirement genuinely changed, the change comes from the approved requirement, is stated as such, and names the source.

## Review checklist

- the chain from requirement source to test case is recorded for every case;
- identifiers are stable, unique, and carried verbatim from their sources;
- assigned acceptance-criterion identifiers are declared as assigned;
- the traceability matrix is present as its own section;
- the forward check passes: every criterion has a coverage verdict;
- the backward check passes: every test case names its requirement;
- non-coverage verdicts name the specific missing condition or question;
- no `Covered` verdict rests on a `TO BE CONFIRMED` expected result;
- a revision preserved existing identifiers and recorded what changed;
- no expected result was revised to match an implementation.
