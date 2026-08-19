# draft-test-cases

`draft-test-cases` is the **QA Test Analyst** specialist for Stage 03 — Analysis. It answers one question:

> What must QA test to prove that this requirement works?

**This skill produces a QA test specification.** It writes no test code, executes nothing, and touches no environment.

## Purpose

Read the Jira ticket and every acceptance criterion, retrieve the BRD, FRD, use cases, workflows, business rules, role requirements, approved technical design, and API contracts, then design functional QA test cases that prove the requirement — each one executable later without asking the author a question.

## Three different testing artifacts

| Skill | Stage | Artifact |
| --- | --- | --- |
| `draft-test-cases` | Stage 03 — Analysis | Functional QA test **specifications** |
| [`write-unit-tests`](../write-unit-tests/README.md) | Stage 05 — In Development | Executable developer-level **unit-test code** |
| [`execute-qa-validation`](../execute-qa-validation/README.md) | Stage 07 — In QA | QA **execution results and evidence** |

These are not three names for the same thing. This skill produces neither test code nor results.

## Relationship to `test-jira-ticket`

```text
test-jira-ticket
    └── Stage 03 — Analysis
        └── draft-test-cases        ← this skill
```

[`test-jira-ticket`](../test-jira-ticket/README.md) selects this skill when the ticket is at Analysis, or when the user explicitly asks for test-case design. The skill is independently installable and independently invocable; when it is not installed, the meta-skill applies the QA Test Analyst contract inline and says so.

## Test the requirement, not the implementation

Every expected result comes from an approved source — the acceptance criterion, the BRD or FRD, a business rule, the approved design, or a published API contract. None comes from observing what code currently returns.

```text
AC-3  Duplicate beneficiary mobile numbers must be rejected.
          ↓
TC-07  Attempt registration using an existing mobile number.
       Expected: duplicate validation shown, registration does not succeed.
```

If the implementation later returns HTTP 500 for that case, `TC-07` **fails**. The expected result is not rewritten to say `HTTP 500`. That independence is what makes the specification worth executing.

At Stage 03 the implementation usually does not exist yet. That is normal.

## Coverage

Applicable categories are covered and skipped ones are justified: positive, negative, boundary, role-based, validation rules, API behaviour, integration behaviour, workflow transitions, error handling, offline behaviour, sync behaviour, multilingual behaviour, device and platform constraints, and regression impact.

## Every test case is executable

| Field | | Field | |
| --- | --- | --- | --- |
| Test ID | Requirement / AC | Scenario | Preconditions |
| Test data | Steps | Expected result | Test type |
| Priority | Automation candidate | | |

A case a tester cannot execute without asking a question is not finished.

## Traceability

```text
BRD → FRD → JIRA Story → Acceptance Criterion → QA Test Case
```

Identifiers are preserved rather than matched by prose, so a defect raised from `TC-07` during Stage 07 is traceable back to `AC-3` and to the FRD requirement behind it. Existing test-case numbers are never reused or renumbered when a specification is revised.

## Gaps are reported, never invented

An acceptance criterion with no stated expected result is listed as ambiguous with the precise question, and its test case carries `TO BE CONFIRMED`. Conflicting sources are reported with both behaviours. Nothing is closed by inventing a rule.

## Read-only

Jira and Confluence are read-only. The skill never executes the application, calls a live API, touches a test or production environment, writes automated test code, or modifies any application source file. It never claims test-case approval, QA sign-off, execution, or a defect verdict.

## Required capabilities

Read access to Jira and Confluence, with DeepWiki, Graphify, OpenProject, and a configured test-management source used read-only where the environment provides them. Tool names are discovered, not hardcoded. If the Jira issue cannot be retrieved, the skill stops rather than inventing the requirement.

## Example invocation

```text
/draft-test-cases DEMO-4102
```

See [examples/sample-test-specification.md](examples/sample-test-specification.md) for a fictional end-to-end specification, including a reported ambiguity. The example is illustrative only and does not describe real AMRIT requirements.

## Use and distribution

Invoke `/draft-test-cases` from the repository root using a supported coding agent, or let `/test-jira-ticket` route to it. For a packaged installation, download `draft-test-cases.zip` from the latest release. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
