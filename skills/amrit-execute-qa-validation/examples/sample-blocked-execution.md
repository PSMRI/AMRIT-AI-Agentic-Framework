# Fictional Sample Blocked QA Execution

This example is fictional. The ticket, environment, and conditions below are invented to show the two outcomes that must never be softened into a pass. They do not describe a real AMRIT build or environment.

## Case A — no QA build or environment

Fictional situation: `DEMO-4102` reaches Stage 07. The agreed QA test specification exists with 42 test cases. The QA environment URL does not resolve from this environment, and no deployed build identifier can be confirmed.

### Correct output

```text
QA EXECUTION BLOCKED

Reason:
QA build/environment unavailable.

Test cases prepared:
42

Executed:
0

QA status:
NOT EXECUTED
```

With the detail the QA Lead needs to unblock it:

```markdown
### What was unavailable

- QA environment https://qa.example.invalid — did not resolve from this
  environment
- Deployed build identifier — could not be confirmed
- Application logs — unreachable without the environment

### What was verified

- The agreed QA test specification for DEMO-4102, 42 test cases, was retrieved
  and read
- Test cases were classified: 34 executable given a reachable build, 5
  manual-only, 3 requiring a physical device

### Required to unblock

- A reachable QA environment with build 2.14.0 or later deployed
- Credentials for `FIELD_WORKER` and `REGISTRATION_CLERK`

### Human decision required

QA approval is a human decision. No validation evidence exists for this ticket.
```

**QA EXECUTION BLOCKED — QA build/environment unavailable. QA status: NOT EXECUTED.**

### What must not happen

The implementation exists in the repository, and its source could be read. That would prove nothing about the deployed build, so none of the following is acceptable:

- reading the source and reporting the criteria as satisfied;
- reading the approved technical design and reporting `PASS`;
- running the unit test suite and presenting a green result as QA validation;
- reasoning that the change "should" satisfy the criteria and recording an assumed pass;
- reporting a partial pass for the cases that "obviously" work.

`Executed: 0` is the honest outcome. A blocked run is a legitimate result; a fabricated one is not.

## Case B — build available, manual and device cases pending

Fictional situation: the QA build is reachable. Of 42 agreed test cases, 37 are executable here, 5 require human or physical-device execution.

### Correct output

```text
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
```

With the pending set named individually:

```markdown
### Not executed and why

- TC-18 — visual layout assessment across the supported language set; requires
  human judgement
- TC-21 — printed output legibility on the field printer; requires physical
  hardware
- TC-29 — behaviour during real intermittent connectivity in the field;
  requires a physical device and controlled network loss
- TC-33 — accessibility assessment with a screen reader; requires human
  execution
- TC-37 — supported low-end device performance; no device or device cloud
  available in this environment

### Acceptance criteria status

- AC-1, AC-2, AC-3, AC-5, AC-6 — Verified
- AC-4 — Not satisfied — TC-11 and TC-14 failed
- AC-7 — Partially verified — TC-30 passed, TC-29 pending device execution
- AC-8 — Unverified — TC-33 and TC-37 pending human and device execution

### Human decision required

QA approval is a human decision. This report provides evidence only.
```

**QA VALIDATION INCOMPLETE — 2 failed, 5 pending human or device execution.**

### What must not happen

35 of 37 executed cases passed — a 95% pass rate on what ran. None of the following is acceptable:

- reporting the ticket QA-approved or ready for Stage 08;
- describing the run as "QA complete with minor pending items";
- marking AC-8 verified because the related automated cases passed;
- inferring TC-29's result from TC-30's pass;
- recording a manual case as passed because the behaviour looks correct in a
  screenshot taken for a different case;
- omitting the pending cases from the summary so the totals reconcile.

Pending is pending. Two failures and five unverified scenarios mean the ticket is not QA-validated, and the skill says so plainly.

## The rule both cases share

This skill never claims to be the human QA approver, and never converts absence of evidence into evidence of correctness. Stage 08 — QA Approved is a human accountability gate; the job here is to give that human an honest picture, including everything that did not run.
