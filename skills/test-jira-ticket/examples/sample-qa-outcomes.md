# Fictional Sample QA Outcomes

This example is fictional. The tickets, builds, results, and defects below are invented to show the two QA outcomes that must never be softened. They do not describe real AMRIT builds, defects, or QA runs.

Both continue Example 3 from [sample-lifecycle-routing.md](sample-lifecycle-routing.md): a ticket routed to `execute-qa-validation` at Stage 07.

## Example 4 — QA with manual tests outstanding

Fictional situation: `AMRIT-104` is In QA. The build is reachable. Of 42 agreed test cases, 37 are executable in this environment and 5 require human or physical-device execution. 35 of the 37 pass.

### Fictional output

```markdown
### Testing activity selected

- QA execution — In QA, agreed test cases exist, build 3.2.0-qa.11 reachable

### Specialist output

QA Execution Summary

Total test cases: 42

Automated/executable:
37

Passed:
35

Failed:
2

Manual-only:
5

Pending human QA:
5

Overall:
QA VALIDATION INCOMPLETE

Not executed and why:
- TC-18 — visual layout assessment across the supported language set;
  requires human judgement
- TC-21 — printed output legibility on the field printer; requires physical
  hardware
- TC-29 — behaviour during real intermittent connectivity; requires a physical
  device and controlled network loss
- TC-33 — accessibility assessment with a screen reader; requires human
  execution
- TC-37 — supported low-end device performance; no device or device cloud
  available in this environment

Acceptance criteria status:
- AC-1, AC-2, AC-3, AC-5, AC-6 — Verified
- AC-4 — Not satisfied — TC-11 and TC-14 failed
- AC-7 — Partially verified — TC-30 passed, TC-29 pending device execution
- AC-8 — Unverified — TC-33 and TC-37 pending human and device execution

### Human decision required

QA approval is a human decision. Five scenarios require human or physical-device
execution and two executed cases failed. This report provides evidence only.
```

**Testing activity incomplete: QA execution. QA VALIDATION INCOMPLETE — 2 failed, 5 pending human or device execution.**

### What must not happen

A 95% pass rate on what ran is not QA completion. None of the following is acceptable:

- reporting the ticket QA-approved or ready for Stage 08;
- describing the run as "QA complete with minor pending items";
- marking AC-8 verified because related automated cases passed;
- inferring TC-29's result from TC-30's pass;
- recording a manual case as passed because the behaviour "looks correct";
- omitting the pending cases so the totals reconcile.

Pending is pending. The manual and device scenarios are unverified, and the report says so plainly.

## Example 5 — QA failure producing a defect

Fictional situation: `AMRIT-105` is In QA with a reachable build. `TC-07` fails.

```text
Test case
    ↓
FAIL
    ↓
Evidence
    ↓
Defect
```

### Fictional output

```markdown
### Specialist output

#### TC-07 — FAIL

Acceptance Criterion: AC-3 (FRD-REQ-114)

Expected:
Registration is rejected, the message "This mobile number is already
registered" is shown against the mobile field, and no new beneficiary record
is created.

Actual:
HTTP 500 returned with a generic server-error body; the form shows
"Something went wrong"; no duplicate record was created.

Result:
FAIL

Evidence:
- POST /beneficiary/register response — HTTP 500, generic error body
- QA service log, correlation id c-88213, constraint-violation stack trace
- Screenshot of the generic error on the registration form

Severity:
Major

Defect:
draft below — not created in Jira

### Defects

**Draft defect — not created in Jira**

Summary: Duplicate beneficiary registration returns HTTP 500 instead of the
agreed duplicate-validation rejection
Failed test case: TC-07
Acceptance criterion: AC-3 (FRD-REQ-114)
Source ticket: AMRIT-105
Expected behaviour: duplicate rejection with the documented message; no record
created
Actual behaviour: HTTP 500 with a generic error body; no record created
Reproduction steps:
  1. Log in to QA as FIELD_WORKER
  2. Identify a mobile number held by an active beneficiary
  3. Submit registration with valid mandatory details and that number
  4. Observe the response
Environment: QA, build 3.2.0-qa.11, release-3.2.0 @ e5f6a7b, 2026-08-16
Evidence: API response; log correlation id c-88213; screenshot
Severity: Major — an acceptance criterion is not satisfied and the user is
given no actionable message
Affected component: Beneficiary registration API, server-side duplicate
handling
Reproducibility: Always — 3 of 3 runs
Regression: not a regression; the rule is new in this ticket

No defect was created in Jira. Confirm to raise it.

### Gaps and recommendations

- AC-3 is not satisfied. The work returns to the implementation flow —
  implement-jira-ticket and its specialists — through the defect and rework
  path.

### Human decision required

QA approval is a human decision. Confirm whether the drafted defect should be
raised in Jira.
```

**Testing activity incomplete: QA execution. QA VALIDATION INCOMPLETE — 1 failed, 0 pending human or device execution.**

### What must not happen

The log makes the likely cause visible — a database constraint violation surfacing as an unhandled 500. None of the following is acceptable:

- **editing the application code** to catch the constraint violation and return the correct rejection;
- **editing the expected result** to say `HTTP 500` because "the duplicate is prevented anyway";
- **passing the case** because no duplicate record was created;
- **fabricating a defect key** such as `AMRIT-9999` to fill the Defect field;
- **transitioning the ticket** to Failed QA or Reopened;
- **diagnosing the root cause** as fact in the defect rather than reporting the observation.

Preventing the record is not the agreed behaviour; rejecting it with an actionable message is. QA that fixes the code it is testing is no longer independent, and every later pass from it means nothing.

### Prepared for root-cause analysis

A separate `root-cause-analysis` skill is expected in the framework later and is **not** implemented here. The defect above is already shaped as a clean input to it: preserved `TC-07` and `AC-3` identifiers, separated expected and actual behaviour, deterministic reproduction steps, build identity, evidence references, affected component, and reproducibility. Nothing would need re-investigation before that analysis could start.
