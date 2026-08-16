# Test Case Structure

## Contents

- [Scope of this document](#scope-of-this-document)
- [Required fields](#required-fields)
- [Identifier rules](#identifier-rules)
- [Writing each field](#writing-each-field)
- [The executability test](#the-executability-test)
- [Specification layout](#specification-layout)
- [What never belongs in a test case](#what-never-belongs-in-a-test-case)
- [Review checklist](#review-checklist)

## Scope of this document

The shape of one QA test case and of the specification that contains it. Every test case must carry enough structure to be executed later by a human tester or by `execute-qa-validation` without returning to the author.

## Required fields

| Field | Required | Purpose |
| --- | --- | --- |
| Test ID | Always | Stable identifier used by execution, defects, and traceability |
| Requirement / AC | Always | The acceptance criterion or approved requirement the case proves |
| Scenario | Always | What is being proven, in one sentence |
| Preconditions | Always | The state that must exist before step 1 |
| Test data | Always | The data characteristics the case needs |
| Steps | Always | Numbered, unambiguous actions |
| Expected result | Always | The agreed outcome, from the requirement |
| Test type | Always | The coverage category |
| Priority | Always | P1 / P2 / P3 |
| Automation candidate | Always | Yes with layer, or No with reason |
| Environment constraint | When one exists | Device, browser, connectivity, or configuration the case requires |
| Related test cases | When one exists | Cases that must run before, or that share setup |

A case missing a required field is not finished.

## Identifier rules

Identifiers are the backbone of traceability. Preserve them rather than relying on prose matching.

- Test cases: `TC-01`, `TC-02`, … zero-padded, unique within the ticket's specification.
- Acceptance criteria: use the ticket's own numbering. If the ticket does not number them, assign `AC-1`, `AC-2`, … and state in the report that you assigned them.
- When a specification is revised at Stage 06, **never renumber an existing test case**. Add new cases with the next free number, and mark retired cases as retired with the reason.
- When a test case is derived from a requirement identifier that already exists — an FRD requirement number, a business-rule identifier — carry that identifier in the Requirement / AC field alongside the acceptance criterion.

An identifier reused for different behaviour breaks every downstream defect and execution record that referenced it.

## Writing each field

### Scenario

One sentence naming the behaviour under test and the condition that makes this case distinct.

```text
Good  Registration is rejected when the mobile number already belongs
      to another active beneficiary.
Poor  Test duplicate mobile number.
```

### Preconditions

State, not actions. Everything that must already be true: the role logged in, the records that must exist, the configuration or feature flag state, the connectivity state, and the starting workflow state.

If a precondition requires work, it is still a precondition — the tester needs it before step 1, and `execute-qa-validation` needs it to decide whether the case is runnable in the available environment.

### Test data

Describe by characteristic so the case works in any environment, and give specific values only where the value itself is the point.

```text
Good  A mobile number already registered to another active beneficiary.
Good  A name field containing exactly 51 characters (limit is 50).
Poor  Use beneficiary 9876543210.
```

Never real personal data, never credentials.

### Steps

Numbered, one action each, in the order performed. Each step names where the tester is and what they do. A step that contains an assertion belongs in the expected result instead, unless the case genuinely has intermediate checkpoints — in which case number them and state the intermediate expectation explicitly.

For an API case, a step states the method, path, and the material request content, not a code snippet.

### Expected result

The agreed outcome, complete enough to decide PASS or FAIL without judgement:

- what the user sees, including the specific message where one is specified;
- what the system state becomes, including what must **not** have been created or changed;
- for an API case, the status code and the material response content;
- for an offline or sync case, what is queued and what reaches the server.

```text
Good  Registration is rejected, the message "This mobile number is already
      registered" is shown against the mobile field, and no new beneficiary
      record is created.
Poor  Error is shown.
```

Where no approved source states the outcome, write `TO BE CONFIRMED — <the precise question>` and list the criterion as ambiguous. Never guess.

### Test type

One of: Positive, Negative, Boundary, Role-based, Validation, API, Integration, Workflow, Error handling, Offline, Sync, Multilingual, Device, Regression. Where a case genuinely spans two, name the primary type and mention the secondary in the scenario.

### Priority

P1, P2, or P3 by business and release risk.

### Automation candidate

`Yes — API`, `Yes — Web UI`, `Yes — Mobile`, or `No — <reason>`. A recommendation, never an assertion that a suite exists.

## The executability test

Before finishing a case, read it as a tester who has never seen the ticket:

1. Do I know what state to set up? — preconditions
2. Do I know what data to use? — test data
3. Do I know exactly what to do? — steps
4. Can I decide PASS or FAIL without asking anyone? — expected result
5. Do I know whether I need a device, browser, or offline condition? — environment constraint

If any answer is no, the case is not finished.

## Specification layout

```text
QA Test Specification — <Jira key>

Sources consulted
Acceptance criteria in scope       AC-1 … AC-n
Test cases                         TC-01 … TC-nn, grouped by AC
Traceability matrix                AC → TC, TC → AC
Coverage categories                covered and not applicable
Regression scope
Uncovered acceptance criteria
Ambiguous or conflicting requirements
Manual versus automation summary
```

Group test cases by acceptance criterion so a reviewer can judge coverage per criterion, and keep the traceability matrix as a separate section so it stays readable on its own.

## What never belongs in a test case

- executable test code in any framework;
- an expected result copied from an implementation's observed behaviour;
- a PASS, FAIL, or execution timestamp — this skill executes nothing;
- a defect identifier — defects come from execution;
- real beneficiary or patient data, credentials, tokens, or private URLs;
- a step that says "verify it works";
- an implementation instruction to a developer.

## Review checklist

- every case carries all required fields;
- identifiers are stable, unique, and never reused for different behaviour;
- preconditions are state, and steps are actions;
- every expected result is decidable without judgement, or is explicitly `TO BE CONFIRMED`;
- test data is described by characteristic and contains nothing real or secret;
- the case passes the executability test;
- cases are grouped by acceptance criterion and the traceability matrix is present;
- nothing in the specification claims execution, approval, or a defect.
