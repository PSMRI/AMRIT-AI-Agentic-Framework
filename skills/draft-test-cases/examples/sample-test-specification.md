# Fictional Sample QA Test Specification

This example is fictional. The ticket, acceptance criteria, business rules, and test cases below are invented to show the shape of the output. They do not describe real AMRIT requirements, workflows, or behaviour.

## Fictional input

```text
DEMO-4102 — Prevent duplicate beneficiary registration by mobile number

AC-1  A beneficiary can be registered with a mobile number that is not
      already registered to another active beneficiary.
AC-2  Registration is rejected when the mobile number already belongs to
      another active beneficiary.
AC-3  A mobile number belonging only to an inactive beneficiary may be
      reused.
AC-4  The rule applies to registration performed offline on the mobile
      application, once the record syncs.
```

Supporting fictional sources: `FRD-REQ-114` (duplicate prevention), an approved Stage 03 design describing a server-side uniqueness check, and a documented role matrix in which only `FIELD_WORKER` and `REGISTRATION_CLERK` may register a beneficiary.

## Fictional output

```markdown
## QA Test Specification

Jira: DEMO-4102 — Prevent duplicate beneficiary registration by mobile number
Lifecycle stage: Stage 03 — Analysis
Artifact: QA test specification (not unit tests, not execution results)

### Sources consulted

- Jira — DEMO-4102, four acceptance criteria read
- Confluence — FRD "Beneficiary Registration" (FRD-REQ-114); approved technical
  design "Registration duplicate prevention"; role matrix "Registration roles"
- API contract — `POST /beneficiary/register` documented request and response
- Existing test cases — "Beneficiary registration" suite, 18 existing cases
- DeepWiki — existing registration flow, to establish regression scope

### Acceptance criteria in scope

- AC-1 (FRD-REQ-114) — registration succeeds with an unused mobile number
- AC-2 (FRD-REQ-114) — registration is rejected for a duplicate active number
- AC-3 (FRD-REQ-114) — a number held only by an inactive beneficiary is reusable
- AC-4 (FRD-REQ-114) — the rule applies to offline registration on sync

### Test cases

#### TC-01

| Field | Value |
| --- | --- |
| Test ID | TC-01 |
| Requirement / AC | AC-1 (FRD-REQ-114) |
| Scenario | Registration succeeds with a mobile number not held by any beneficiary |
| Preconditions | Logged in as `FIELD_WORKER`; the chosen mobile number exists on no beneficiary record |
| Test data | A valid 10-digit Indian mobile number not present in the system |
| Steps | 1. Open the beneficiary registration form<br>2. Enter valid mandatory details and the unused mobile number<br>3. Submit |
| Expected result | The beneficiary is created, a success confirmation is shown, and the record is retrievable by the registered mobile number |
| Test type | Positive |
| Priority | P1 |
| Automation candidate | Yes — API |

#### TC-02

| Field | Value |
| --- | --- |
| Test ID | TC-02 |
| Requirement / AC | AC-2 (FRD-REQ-114) |
| Scenario | Registration is rejected when the mobile number already belongs to another active beneficiary |
| Preconditions | Logged in as `FIELD_WORKER`; an active beneficiary already holds the chosen mobile number |
| Test data | A mobile number registered to an existing active beneficiary |
| Steps | 1. Open the beneficiary registration form<br>2. Enter valid mandatory details and the duplicate mobile number<br>3. Submit |
| Expected result | Registration is rejected, the message "This mobile number is already registered" is shown against the mobile field, and no new beneficiary record is created |
| Test type | Negative |
| Priority | P1 |
| Automation candidate | Yes — API |

#### TC-03

| Field | Value |
| --- | --- |
| Test ID | TC-03 |
| Requirement / AC | AC-2 (FRD-REQ-114) |
| Scenario | The duplicate rule is enforced at the API, not only in the browser |
| Preconditions | A valid session token for `FIELD_WORKER`; an active beneficiary already holds the chosen mobile number |
| Test data | The same duplicate mobile number as TC-02 |
| Steps | 1. Send `POST /beneficiary/register` with valid mandatory fields and the duplicate mobile number, bypassing the web form |
| Expected result | The documented duplicate-rejection status code and error body are returned, and no new beneficiary record is created |
| Test type | API |
| Priority | P1 |
| Automation candidate | Yes — API |

#### TC-04

| Field | Value |
| --- | --- |
| Test ID | TC-04 |
| Requirement / AC | AC-3 (FRD-REQ-114) |
| Scenario | A mobile number held only by an inactive beneficiary can be reused |
| Preconditions | Logged in as `REGISTRATION_CLERK`; exactly one beneficiary holds the chosen number and that beneficiary is inactive |
| Test data | A mobile number held only by an inactive beneficiary |
| Steps | 1. Open the beneficiary registration form<br>2. Enter valid mandatory details and that mobile number<br>3. Submit |
| Expected result | The beneficiary is created successfully, and the inactive beneficiary record is unchanged |
| Test type | Boundary |
| Priority | P2 |
| Automation candidate | Yes — API |

#### TC-05

| Field | Value |
| --- | --- |
| Test ID | TC-05 |
| Requirement / AC | AC-2 (FRD-REQ-114) |
| Scenario | A role that may not register a beneficiary cannot bypass the flow |
| Preconditions | A valid session for a role outside `FIELD_WORKER` and `REGISTRATION_CLERK` |
| Test data | Any valid registration payload |
| Steps | 1. Attempt registration through the UI<br>2. Attempt `POST /beneficiary/register` directly |
| Expected result | Both attempts are refused with the documented authorization outcome, and no beneficiary record is created |
| Test type | Role-based |
| Priority | P1 |
| Automation candidate | Yes — API |

#### TC-06

| Field | Value |
| --- | --- |
| Test ID | TC-06 |
| Requirement / AC | AC-4 (FRD-REQ-114) |
| Scenario | A duplicate registered offline is rejected when the record syncs |
| Preconditions | Android application installed on a supported device, logged in as `FIELD_WORKER`, device offline; an active beneficiary already holds the chosen number |
| Test data | A mobile number registered to an existing active beneficiary |
| Steps | 1. With the device offline, register a beneficiary using the duplicate number<br>2. Confirm the record is queued locally<br>3. Restore connectivity and allow sync to run |
| Expected result | The queued record is rejected on sync, the rejection is surfaced to the user with the duplicate reason, the local record is not silently discarded without notice, and no new beneficiary exists on the server |
| Test type | Sync |
| Priority | P1 |
| Automation candidate | No — requires a physical device and controlled connectivity loss |

#### TC-07

| Field | Value |
| --- | --- |
| Test ID | TC-07 |
| Requirement / AC | Regression — existing registration flow, "Beneficiary registration" suite |
| Scenario | Registration with a valid unused number still completes for every previously supported mandatory-field combination |
| Preconditions | Logged in as `FIELD_WORKER` |
| Test data | Valid registration data for each documented mandatory-field combination |
| Steps | 1. Register a beneficiary for each documented combination |
| Expected result | Each registration completes as it did before the change, with no new validation error |
| Test type | Regression |
| Priority | P2 |
| Automation candidate | Yes — API |

### Traceability

| AC | Requirement source | Test cases | Coverage |
| --- | --- | --- | --- |
| AC-1 | FRD-REQ-114 | TC-01 | Covered |
| AC-2 | FRD-REQ-114 | TC-02, TC-03, TC-05 | Covered |
| AC-3 | FRD-REQ-114 | TC-04 | Covered |
| AC-4 | FRD-REQ-114 | TC-06 | Partially covered — the expected behaviour when the same duplicate is queued on two devices simultaneously is not stated by any source |
| — | Regression | TC-07 | Regression scope |

### Coverage categories

- Covered: Positive, Negative, Boundary, Role-based, API, Sync, Regression
- Not applicable: Multilingual — the change adds one message whose translations are handled by the existing string catalogue and are covered by the module's standing language checks; Offline capture — AC-4 concerns sync rejection, and offline capture itself is unchanged

### Regression scope

- Registration with a valid unused mobile number must still succeed for every documented mandatory-field combination — TC-07
- The inactive-beneficiary record must remain unchanged when its number is reused — TC-04

### Uncovered acceptance criteria

None fully uncovered.

### Ambiguous or conflicting requirements

- AC-4 — when the same duplicate number is registered offline on two devices and both sync, no approved source states whether the first record is accepted and the second rejected, or both are rejected. Question for the Product Manager: which record wins, and what does the losing device's user see?

### Manual versus automation

- Automation candidates: 6 — API layer
- Manual-only: 1 — TC-06 requires a physical device and controlled connectivity loss

### Not produced by this skill

- Unit-test code — `write-unit-tests`
- Execution results — `execute-qa-validation`

### Next

QA review of this specification, then Stage 07 execution by `execute-qa-validation`.
```

**QA test specification incomplete. Resolve the ambiguities above before QA review.**

## What this example demonstrates

**Expected results come from the requirement.** TC-02 expects a duplicate rejection with a validation message because AC-2 and `FRD-REQ-114` say so. If the implementation later returns HTTP 500, TC-02 fails — the specification does not change to expect a 500.

**No implementation existed.** This specification was written at Stage 03. Nothing in it depends on code being written yet.

**The ambiguity was reported, not invented.** The two-device sync collision has no approved answer, so AC-4 is `Partially covered` with the precise question, and the run ends with the incomplete line rather than a fabricated rule.

**Identifiers travel.** `AC-4 (FRD-REQ-114)` on TC-06 means a defect raised from TC-06 during Stage 07 is traceable back to the FRD requirement without prose matching.

**Automation candidacy is a recommendation.** TC-06 is marked manual because it needs a physical device and real connectivity loss — not because no automation tool happened to be connected.
