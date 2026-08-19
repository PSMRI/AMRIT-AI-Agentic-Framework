# Test Design Guidelines

## Contents

- [Scope of this document](#scope-of-this-document)
- [The question this skill answers](#the-question-this-skill-answers)
- [Source research order](#source-research-order)
- [Implementation independence](#implementation-independence)
- [Deriving test conditions from an acceptance criterion](#deriving-test-conditions-from-an-acceptance-criterion)
- [Coverage categories](#coverage-categories)
- [Regression scope](#regression-scope)
- [Test data rules](#test-data-rules)
- [Priority](#priority)
- [Automation candidacy](#automation-candidacy)
- [Handling gaps, ambiguity, and conflict](#handling-gaps-ambiguity-and-conflict)
- [Review checklist](#review-checklist)

## Scope of this document

Designing functional QA test specifications from an agreed requirement. Executable developer-level unit-test code belongs to `write-unit-tests`. Execution against a deployed build belongs to `execute-qa-validation`. Keep the three separate; they are different artifacts with different owners.

## The question this skill answers

> What must QA test to prove that this requirement works?

Not *what does the code do*, and not *what tests exist*. The output is a specification that a human tester or an automated suite can execute later to decide whether the delivered system satisfies what was agreed.

## Source research order

1. **Jira** — the full issue and every acceptance criterion. This is the primary scope statement.
2. **Confluence** — BRD, FRD, use cases, workflows, business rules, validation rules, role and permission requirements, and the approved Stage 03 technical design.
3. **API contracts** — Swagger/OpenAPI definitions and documented request and response shapes, status codes, and error bodies.
4. **Existing test cases** — the configured test-management source or existing QA documentation for the same module or flow, so new cases extend rather than duplicate.
5. **DeepWiki** — existing product and repository behaviour, only to establish what the system already does so regression scope is real.
6. **Graphify** — final fallback for an unresolved cross-repository relationship that affects integration scope.

Every source is read-only. Record which sources answered which part of the design, and which were unavailable.

## Implementation independence

The expected result of a test case is the **agreed behaviour**, taken from an approved source. It is never taken from an implementation's observed output.

Legitimate sources for an expected result:

- the acceptance criterion;
- the BRD or FRD;
- a documented business or validation rule;
- the approved technical design;
- a published API contract;
- a documented role and permission matrix.

Not a source for an expected result:

- what an endpoint currently returns;
- what a screen currently renders;
- what a log currently contains;
- what a developer said the code does;
- what an existing failing test asserts.

```text
Wrong

Inspect implementation → endpoint returns 500 for a duplicate
                       → expected result: HTTP 500

Right

AC states duplicates must be rejected
                       → expected result: duplicate rejected with
                         validation message, no record created
                       → implementation returning 500 is a FAIL for
                         execute-qa-validation to record
```

At Stage 03 the implementation usually does not exist yet. Its absence is not a blocker and never justifies deferring test design.

## Deriving test conditions from an acceptance criterion

For each criterion, ask in order:

1. **What must happen** when the criterion is satisfied in the ordinary case?
2. **What must be rejected**, and with what user-visible outcome?
3. **What are the edges** — first, last, empty, maximum, minimum, expiry, and rollover values named or implied by the criterion?
4. **Who may do it** — which roles are permitted, and which are explicitly not?
5. **What state must exist first**, and what state must exist after?
6. **What can fail around it** — dependency unavailable, timeout, partial save, concurrent update?
7. **What already works that this must not break?**

A criterion that yields a single test case is usually under-analysed. A criterion that yields thirty is usually several criteria written as one; say so.

## Coverage categories

Apply every category that the requirement actually implies.

| Category | Design it when | Typical content |
| --- | --- | --- |
| Positive | Always | The criterion's main flow, with valid data and a permitted role |
| Negative | Any rejection, rule, or constraint exists | Invalid, missing, malformed, duplicate, or unauthorized input |
| Boundary | Any limit, range, length, count, or date window exists | Minimum, maximum, one below, one above, empty, and single-element cases |
| Role-based | More than one role can reach the feature | Permitted role succeeds; each non-permitted role is refused, and refusal is verified in the UI and at the API |
| Validation rules | Field-level rules exist | Format, mandatory, length, type, dependency between fields, and the exact user-facing message where one is specified |
| API behaviour | An endpoint is added or changed | Status codes, response shape, error body, required headers, authentication and authorization, idempotency where specified |
| Integration | The flow crosses a service, module, or external system | Contract honoured end to end, and behaviour when the far side is slow, failing, or returns an unexpected shape |
| Workflow transitions | A state machine or approval flow exists | Each permitted transition, each forbidden transition, and the resulting state and audit record |
| Error handling | Any failure path exists | The user-visible outcome, whether work is lost, and whether the system stays consistent |
| Offline | A mobile or field flow works without connectivity | What is captured offline, what is queued, what is blocked, and what the user sees |
| Sync | Offline data reaches the server later | Successful sync, retry, partial sync, duplicate prevention, and conflict resolution as specified |
| Multilingual | The change is user-visible and the product supports more than one language | Each supported language renders, and no string is untranslated, truncated, or overlapping |
| Device and platform | Android or a browser matrix is in scope | Supported OS and browser versions, screen sizes, and any documented low-end device constraint |
| Regression | Existing behaviour is adjacent to the change | The specific existing flows the change could break |

Skip a category only when the requirement genuinely has no such case, and record the skip with its reason. Padding a specification with hollow cases is worse than a stated gap.

## Regression scope

Regression scope is derived, not guessed. Identify it from:

- the modules and screens named in the ticket and the approved design;
- shared components, shared endpoints, and shared tables the change touches;
- flows that read or write the same data;
- existing test cases for the same module.

State each regression case as an existing behaviour that must still hold, not as a vague "regression testing of the module".

## Test data rules

- Never use real beneficiary, patient, worker, or citizen data, and never use production identifiers.
- Never embed credentials, tokens, API keys, or private URLs.
- Describe data by its characteristics — "a mobile number already registered to another active beneficiary" — so the tester can construct it in any environment.
- State any data that must pre-exist as a precondition, not as a step.
- Where a specific value matters — a boundary length, a specific date — give the value.

## Priority

| Priority | Assign when |
| --- | --- |
| P1 | The criterion's core behaviour, a data-integrity rule, an authorization rule, or a flow whose failure blocks the release |
| P2 | Important supporting behaviour, common error paths, and material regression risk |
| P3 | Cosmetic, rare, or low-impact scenarios |

Priority reflects business and release risk, not how difficult the test is.

## Automation candidacy

Mark each test case as an automation candidate or not, with the reason and the intended layer.

| Verdict | Typical case |
| --- | --- |
| Yes — API | Deterministic request and response behaviour, status codes, validation rules |
| Yes — Web UI | Stable, high-value flows with reliable selectors |
| Yes — Mobile | Repeatable device flows on a supported automation target |
| No — manual | Exploratory judgement, visual and layout assessment, physical-device behaviour, real network-loss behaviour, printing and hardware integration, and anything requiring a human decision |

This field is a recommendation for `execute-qa-validation`, not a promise that automation exists. Never mark a case automatable because automating it would be convenient.

## Handling gaps, ambiguity, and conflict

| Situation | Correct action |
| --- | --- |
| No approved source states the expected result | Write the case, mark the expected result `TO BE CONFIRMED — <question>`, list the criterion as ambiguous |
| Two approved sources disagree | Write both expected behaviours, state the conflict and both sources, list the criterion as conflicting |
| The criterion is untestable as written | List it as uncovered with the reason and the question that would make it testable |
| The criterion depends on a decision not yet taken | List it as uncovered, naming the decision and its owner |

Never invent behaviour to close a gap, and never mark an ambiguous criterion as covered.

## Review checklist

- every acceptance criterion was read and carries a stable identifier;
- every expected result traces to an approved requirement, not to an implementation;
- each criterion maps to at least one test case, or appears as uncovered with a reason;
- applicable coverage categories are present, and skipped categories are justified;
- regression scope names actual existing behaviour;
- every test case is executable without asking a question, or is explicitly marked `TO BE CONFIRMED`;
- test data contains no real personal data and no credentials;
- priority reflects business risk;
- automation candidacy is a reasoned recommendation, not an assumption of tooling;
- ambiguity and conflict are reported, not resolved by invention;
- no unit-test code was written, no application was executed, and no QA approval was claimed.
