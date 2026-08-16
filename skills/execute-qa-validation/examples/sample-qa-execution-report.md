# Fictional Sample QA Execution Report

This example is fictional. The ticket, build, environment, results, defect, and evidence below are invented to show the shape of the output. They do not describe a real AMRIT build, defect, or QA run.

It continues the fictional `DEMO-4102` specification from
[`draft-test-cases/examples/sample-test-specification.md`](../../draft-test-cases/examples/sample-test-specification.md), executed at Stage 07 against a deployed QA build.

## Fictional output

```markdown
## QA Validation

Jira: DEMO-4102 — Prevent duplicate beneficiary registration by mobile number
Lifecycle stage: Stage 07 — In QA

### Build under test

- Environment: QA — https://qa.example.invalid
- Build/version: 2.14.0-qa.37
- Commit/release: release-2.14.0 @ a1b2c3d
- Executed on: 2026-08-16

### Test case source

QA test specification for DEMO-4102, TC-01 to TC-07, agreed at Stage 03.
Consumed as written; no expected result was modified.

### Test capability verified in this environment

- Direct API calls — available; QA API reachable, authentication succeeded for
  `FIELD_WORKER` and `REGISTRATION_CLERK`
- Backend integration suite — available; `./mvnw verify -Pintegration` found in
  the build file and CI workflow, runs against the QA API
- Application logs — available; QA service logs reachable by correlation id
- Playwright — not available; not present in any project dependency
- Appium — not available; no configured server and no device
- BrowserStack — not available; no configuration and no credentials

### Execution results

#### TC-01 — PASS

Acceptance Criterion: AC-1 (FRD-REQ-114)
Expected: The beneficiary is created, a success confirmation is shown, and the
record is retrievable by the registered mobile number.
Actual: Beneficiary created; `201` returned; the record was retrieved by the
registered number.
Result: PASS
Evidence: `POST /beneficiary/register` request and response captured;
retrieval response captured.

#### TC-02 — FAIL

Acceptance Criterion: AC-2 (FRD-REQ-114)
Expected: Registration is rejected, the message "This mobile number is already
registered" is shown against the mobile field, and no new beneficiary record is
created.
Actual: The request failed with HTTP 500 and a generic server-error body. The
web form displayed "Something went wrong". No duplicate record was created.
Result: FAIL
Evidence:
- `POST /beneficiary/register` response — HTTP 500, generic error body
- QA service log, correlation id `c-88213`, constraint-violation stack trace
- Screenshot of the generic error on the registration form
Severity: Major
Defect: draft below

#### TC-03 — FAIL

Acceptance Criterion: AC-2 (FRD-REQ-114)
Expected: The documented duplicate-rejection status code and error body are
returned, and no new beneficiary record is created.
Actual: HTTP 500 with a generic server-error body. No duplicate record created.
Result: FAIL
Evidence: direct API response captured; same correlation id family as TC-02.
Severity: Major
Defect: same defect as TC-02

#### TC-04 — PASS

Acceptance Criterion: AC-3 (FRD-REQ-114)
Expected: The beneficiary is created successfully, and the inactive beneficiary
record is unchanged.
Actual: Beneficiary created; the inactive record was re-read after the run and
was unchanged.
Result: PASS
Evidence: registration response; before-and-after retrieval of the inactive
record.

#### TC-05 — PASS

Acceptance Criterion: AC-2 (FRD-REQ-114)
Expected: Both attempts are refused with the documented authorization outcome,
and no beneficiary record is created.
Actual: UI navigation refused; direct API call returned the documented
authorization failure. No record created.
Result: PASS
Evidence: API response captured; no new record found on verification query.

#### TC-06 — NOT EXECUTED — infrastructure

Acceptance Criterion: AC-4 (FRD-REQ-114)
Reason: requires a physical Android device and controlled connectivity loss.
No device automation, device cloud, or physical device is available in this
environment.
Required action: human QA execution on a supported device.

#### TC-07 — PASS

Acceptance Criterion: Regression — existing registration flow
Expected: Each registration completes as it did before the change, with no new
validation error.
Actual: All six documented mandatory-field combinations registered successfully.
Result: PASS
Evidence: six request and response pairs captured;
`./mvnw verify -Pintegration` — 142 tests, 0 failures.

### Summary

Total test cases: 7
Automated/executable: 6
Passed: 4
Failed: 2
Blocked: 0
Manual-only: 0
Pending human QA: 1
Infrastructure-blocked: 1

### Acceptance criteria status

- AC-1 — Verified by TC-01
- AC-2 — Not satisfied — TC-02 and TC-03 failed
- AC-3 — Verified by TC-04
- AC-4 — Unverified — TC-06 pending device execution

### Defects

**Draft defect — not created in Jira**

| Field | Value |
| --- | --- |
| Summary | Duplicate beneficiary registration returns HTTP 500 instead of the agreed duplicate-validation rejection |
| Failed test case | TC-02, TC-03 |
| Acceptance criterion | AC-2 (FRD-REQ-114) |
| Source ticket | DEMO-4102 |
| Expected behaviour | Registration is rejected with "This mobile number is already registered" against the mobile field, and no new record is created |
| Actual behaviour | HTTP 500 with a generic server-error body; the form shows "Something went wrong"; no duplicate record is created |
| Reproduction steps | 1. Log in to QA as `FIELD_WORKER`<br>2. Identify a mobile number held by an active beneficiary<br>3. Submit registration with valid mandatory details and that number<br>4. Observe the response |
| Environment | QA — https://qa.example.invalid, build 2.14.0-qa.37, release-2.14.0 @ a1b2c3d, 2026-08-16 |
| Test data | A mobile number registered to an existing active beneficiary |
| Evidence | API response (HTTP 500); QA service log correlation id `c-88213` with a constraint-violation stack trace; screenshot of the generic form error |
| Severity | Major — an acceptance criterion is not satisfied and the user is given no actionable message |
| Affected component | Beneficiary registration API, server-side duplicate handling |
| Reproducibility | Always — 3 of 3 runs |
| Regression | Not a regression; the duplicate rule is new in this ticket |

No defect was created in Jira. Confirm to raise it.

### Not executed and why

- TC-06 — physical Android device and controlled connectivity loss unavailable
  in this environment

### Human decision required

QA approval is a human decision. This report provides evidence only.
```

**QA VALIDATION INCOMPLETE — 2 failed, 1 pending human or device execution.**

## What this example demonstrates

**The agreed expected result was not edited.** TC-02 expected a duplicate-validation rejection. The build returned HTTP 500. That is a `FAIL` — the specification was not rewritten to expect a 500, even though the duplicate record was in fact prevented. Preventing the record is not the agreed behaviour; rejecting it with an actionable message is.

**Nothing was fixed.** The constraint-violation stack trace makes the likely cause visible. This skill still changed no code. The defect returns the work to the implementation flow.

**Absent tooling was reported as absent.** Playwright, Appium, and BrowserStack were checked and are not present, which is exactly what justifies TC-06's `NOT EXECUTED — infrastructure`.

**The pending case blocks completion.** Four of six executed cases passed, but AC-4 is unverified, so the run ends `INCOMPLETE`. A high pass rate does not close a pending case.

**The defect was drafted, not created.** Jira stayed read-only. The draft carries the test case, criterion, expected and actual behaviour, deterministic steps, build identity, evidence, severity, component, and reproducibility — enough for a future `root-cause-analysis` skill to start from without re-investigation.
