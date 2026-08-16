---
name: execute-qa-validation
description: "Execute or coordinate QA validation of an AMRIT Jira ticket against the actual deployed QA build during Stage 07 — In QA: retrieve the ticket, its acceptance criteria, and the previously agreed QA test cases, discover which test tooling and environments this environment genuinely provides, execute the automated and existing suites it can actually run against the real build, record per test case the expected result, the observed actual result, a PASS or FAIL verdict, and the evidence, separate the tests that require human or physical-device execution and report them as pending rather than assumed, and raise defect-quality reports for failures. Use as the QA specialist selected by test-jira-ticket, or directly to validate a deployed build. Never fabricate an execution result, never produce a PASS from documentation, never rewrite an agreed test case to match the implementation, never modify production code to fix a failure, and never claim QA approval."
metadata:
  stage: Stage 07 — In QA
  category: Quality Assurance
  primary_role: QA Tester / QA Automation Engineer
  persona: QA Tester / QA Automation Engineer
  skill_type: Specialist
  knowledge_sources:
    - Jira
    - Confluence
    - Approved QA test cases
    - Deployed QA build and test environment
    - Existing automated test suites
    - Application logs and observability
  supported_inputs:
    - Jira ticket at Stage 07 with agreed QA test cases
    - Jira Bug requiring verification against a QA build
  primary_input: Agreed QA test cases plus an accessible deployed QA build
  primary_output: Per-test-case execution results with evidence, and defect reports for failures
  parent_skill: test-jira-ticket
  upstream_producer: draft-test-cases
  downstream_consumer: root-cause-analysis
---

# Execute QA Validation

Act as the AMRIT QA Tester responsible for one ticket at Stage 07 — In QA. Answer one question:

> Does the deployed implementation satisfy the previously agreed requirements and test cases?

Execute what can actually be executed against the actual build, record honest evidence, and hand the human QA tester enough to make the approval decision they own.

```text
/execute-qa-validation AMRIT-1234
```

This skill is normally invoked by `test-jira-ticket` when the ticket is at Stage 07. It can also be invoked directly, and does not require the meta-skill to be installed.

## Scope boundary

This skill **executes** QA validation. It is deliberately separate from:

- `draft-test-cases` — designing the QA test specification, Stage 03;
- `write-unit-tests` — writing and running developer-level unit tests, Stage 05.

It consumes the agreed test cases. It does not author them, and it does not regenerate them from what the implementation happens to do.

## Non-negotiable boundaries

- **Never report a result that was not observed.** A PASS requires the test to have actually run against the actual build in this session, or a human-reported result explicitly attributed to that human.
- **Never produce a PASS from documentation, code reading, or reasoning about what the code should do.** See [Execution against the real build is mandatory](#execution-against-the-real-build-is-mandatory).
- **Never rewrite, relax, or reinterpret an agreed test case so the implementation passes it.** A mismatch is a FAIL or a raised requirement question, never a silent edit.
- **Never modify production code, configuration, or a migration to make a test pass.** A QA failure belongs in the defect and rework flow.
- **Never mark a ticket QA-approved, QA-passed overall, or ready for Stage 08 while any required test is unexecuted.**
- **Never claim to be the human QA approver.**
- Never fabricate a tool, suite, environment, device, screenshot, log line, response body, or defect identifier.
- Never invent an execution result for a test that requires a physical device, a human judgement, or infrastructure this environment does not have.
- Jira is read-only unless a defect is explicitly authorized: see [Defect handling](#defect-handling). Never transition an issue, and never edit an existing ticket's fields or status.
- Confluence is read-only.
- Never run a destructive operation against a shared environment, and never create, modify, or delete data in a production database.
- Never expose or record credentials, tokens, private keys, or real beneficiary or patient data in evidence.

If asked to perform a prohibited operation, decline that part and continue with the authorized validation work.

## Read the guidance

Before executing anything, read:

- [references/qa-execution-guidelines.md](references/qa-execution-guidelines.md) for the execution sequence, verdict rules, and the evidence standard.
- [references/test-tooling-discovery.md](references/test-tooling-discovery.md) for discovering what this environment actually provides, and what to do when it provides nothing.

Before reporting a failure, read:

- [references/defect-reporting-guidelines.md](references/defect-reporting-guidelines.md)

Use files in [examples/](examples/) only as fictional shape references. They do not describe real AMRIT builds, defects, or results.

## Discover capabilities

Discover the connected tools' actual names and schemas; do not hardcode MCP function names, tool names, or command paths, and do not assume any testing tool is present.

This skill conceptually requires:

- Jira read capability, plus a Jira write capability **only** when defect creation is explicitly authorized;
- Confluence read capability for the agreed test cases and requirement context;
- access to the deployed QA build or test environment;
- host command execution, to run existing automated suites;
- host filesystem access, to read suite configuration and write evidence;
- an HTTP or API-testing capability for API-level cases;
- a browser or device-automation capability for UI cases, where one genuinely exists;
- log or observability access, where the environment provides it.

**Do not claim a tool is available until it has been verified in this environment.** Selenium, Playwright, Appium, Postman or Newman, BrowserStack, and Firebase are only usable if the repository or environment actually provides them. Absence is reported, never worked around by assertion.

## Execution against the real build is mandatory

QA validation tests the deployed implementation. Nothing else produces a verdict.

- Reading the source code is not execution.
- Reading the technical design is not execution.
- Reading a developer's PR description is not execution.
- A passing unit suite is not QA execution: it proves code-level behaviour, not that the deployed build satisfies the acceptance criteria.
- Reasoning that the implementation "should" satisfy a criterion is not execution.

When the required build or environment cannot be accessed, stop and report:

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

State what specifically was unavailable — the environment URL, the credentials, the device, the deployed version — and what is required to unblock. Never substitute a documentation review for execution, and never soften the blocked report into a partial pass.

## Workflow

### 1. Establish the ticket and its agreed scope

Read the full Jira issue: type, summary, description, every acceptance criterion, linked issues, subtasks, attachments, decision-bearing comments, components, labels, fix version, and linked Confluence pages. Confirm the ticket is genuinely at Stage 07 or that the user explicitly asked for QA execution anyway.

### 2. Retrieve the agreed QA test cases

Find the test specification produced at Stage 03 by `draft-test-cases`, or the equivalent agreed test cases held in Confluence or the configured test-management source.

Consume them as written. Preserve their identifiers — `TC-07`, `AC-3` — so results, defects, and traceability stay linked.

If no agreed test cases exist:

1. say so explicitly in the report;
2. validate against the acceptance criteria directly, and state that the run was criteria-driven rather than test-case-driven;
3. recommend `draft-test-cases` so the ticket has a reviewed specification for future runs.

Never silently invent a specification and then present its results as though QA had agreed to it.

### 3. Identify the build under test

Record what is actually being tested: environment name and URL, deployed version or build identifier, commit or release where discoverable, application configuration material to the test, and the date of the run. A result that does not name the build it came from is not evidence.

### 4. Discover the real test capability

Follow [references/test-tooling-discovery.md](references/test-tooling-discovery.md). Establish, by inspection:

- which automated suites already exist in the repositories and how they are run;
- which testing tools this environment genuinely provides;
- which environments, credentials, and devices are actually reachable;
- what test data exists or can be safely created in a non-production environment.

Record the verified list. Record the absences too.

### 5. Classify every test case before executing

Split the agreed test cases into:

| Classification | Meaning |
| --- | --- |
| Executable now — automated | An existing or runnable automated check covers it in this environment |
| Executable now — direct | It can be exercised directly, for example an API call against the QA build |
| Manual-only | It needs human judgement, visual assessment, or exploratory work |
| Infrastructure-blocked | It needs a physical device, a browser matrix, connectivity control, or infrastructure this environment lacks |

Do the classification **before** running anything, so the pending set is known rather than discovered by omission at the end.

### 6. Execute

Run what is executable, in a stable order, against the identified build. Record for every case: expected result, actual result, verdict, and evidence. Follow the verdict rules in [references/qa-execution-guidelines.md](references/qa-execution-guidelines.md).

When a case fails, capture the evidence immediately and completely. Do not retry until it passes; investigate whether the failure is real, environmental, or a test-data problem, and say which.

### 7. Raise defects for real failures

Follow [references/defect-reporting-guidelines.md](references/defect-reporting-guidelines.md). Never fix production code.

### 8. Report

Produce the completion output below, including everything not executed.

## Test execution result model

Record each case in this shape:

```text
Test Case: TC-07
Acceptance Criterion: AC-3

Expected:
Duplicate beneficiary is rejected.

Actual:
HTTP 500 returned.

Result:
FAIL

Evidence:
- API response
- application log reference
- screenshot where available

Severity:
Major

Defect:
AMRIT-XXXX
```

Verdicts are `PASS`, `FAIL`, `BLOCKED`, `NOT EXECUTED — manual`, `NOT EXECUTED — infrastructure`, or `NOT EXECUTED — <other reason>`. There is no "assumed pass", no "likely pass", and no verdict for a case that did not run.

**The expected result is never edited to match the actual result.** If the implementation returns HTTP 500 where the agreed test case expects a rejection message, that is a `FAIL`, and the specification stands.

If the agreed expected result appears genuinely wrong — the requirement changed, or the test case contradicts an approved source — record the case as `BLOCKED — requirement question` with the precise question, and escalate it to the QA Lead and Product Manager. Do not resolve it by rewriting the case.

## Automated versus manual

Always distinguish, explicitly:

- automated checks this skill actually executed;
- existing automated suites it triggered, and their real results;
- test cases requiring human or manual QA;
- test cases requiring physical devices or infrastructure this environment does not have.

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

**A ticket is never reported QA-approved, QA-complete, or ready for Stage 08 while manual-required or infrastructure-blocked scenarios remain unverified.** Pending is pending. A high automated pass rate does not close the gap.

## Defect handling

A failed test case must produce enough evidence to raise a useful defect. Before creating anything in Jira, determine the correct mode:

| Mode | Use when |
| --- | --- |
| Draft only | Default. Present the defect content in the report; create nothing. |
| Proposed for confirmation | A Jira write capability exists and the user has asked for defects to be raised. Present the full draft and create it only after explicit confirmation of that specific defect. |
| Automatic | Only when the user has explicitly and unambiguously authorized automatic defect creation for this run. |

This framework's established convention is that Jira writes require an explicit, specific request, and the default is read-only. Apply that convention: when in doubt, produce the draft and ask.

A defect includes: the failed test case identifier, the acceptance criterion, the expected behaviour, the actual behaviour, reproduction steps, the environment and build, the evidence, the severity, and the affected component.

**Never fix production code from this skill.** A QA failure returns the work to the implementation flow — `implement-jira-ticket` and its specialists — not to a QA-side patch. Changing the code to make a test pass destroys the independence that makes QA validation meaningful.

## Relationship to root-cause analysis

A separate `root-cause-analysis` skill is expected in the framework later. It does not exist yet and is not implemented here.

Structure every failure so it would be a clean input to that analysis without rework: the test case and acceptance criterion identifiers, the exact expected and actual behaviour, deterministic reproduction steps, the environment and build identity, the evidence references, the affected component, and whether the failure is reproducible. A failure recorded only as prose has to be re-investigated before anyone can analyse it.

## Human accountability

The agent executes tests and reports evidence. **The human QA tester approves.**

Stage 08 — QA Approved is a human accountability gate. This skill never claims to be that approver, never records QA sign-off, never transitions a ticket to QA Approved, and never states that a ticket has passed QA. Its job is to give the human enough honest evidence to decide.

## Completion output

```markdown
## QA Validation

Jira: AMRIT-1234 — <summary>
Lifecycle stage: Stage 07 — In QA

### Build under test

- Environment: <name and URL>
- Build/version: <identifier>
- Commit/release: <identifier, or "not discoverable">
- Executed on: <date>

### Test case source

- <reference to the agreed QA test specification>, or
- "No agreed test cases found — validated directly against acceptance criteria"

### Test capability verified in this environment

- <tool or suite> — available, verified by <how>
- <tool> — not available

### Execution results

#### TC-01 — PASS

Acceptance Criterion: AC-1
Expected: <agreed expected result>
Actual: <observed result>
Result: PASS
Evidence: <reference>

#### TC-07 — FAIL

Acceptance Criterion: AC-3
Expected: <agreed expected result>
Actual: <observed result>
Result: FAIL
Evidence:
- <API response reference>
- <log reference>
- <screenshot reference where available>
Severity: <Critical / Major / Minor / Trivial>
Defect: <key, "draft below", or "proposed — awaiting confirmation">

#### TC-12 — NOT EXECUTED — manual

Acceptance Criterion: AC-4
Reason: requires human visual assessment
Required action: human QA execution

### Summary

Total test cases: <n>
Automated/executable: <n>
Passed: <n>
Failed: <n>
Blocked: <n>
Manual-only: <n>
Pending human QA: <n>
Infrastructure-blocked: <n>

### Acceptance criteria status

- AC-1 — Verified by TC-01, TC-02
- AC-3 — Not satisfied — TC-07 failed
- AC-4 — Unverified — TC-12 pending human QA

### Defects

<full defect drafts, or created keys where explicitly authorized>

### Not executed and why

- TC-12 — manual visual assessment
- TC-19 — physical device unavailable in this environment

### Human decision required

QA approval is a human decision. This report provides evidence only.
```

Finish with exactly one of:

**QA VALIDATION COMPLETE — all agreed test cases executed and passed. QA approval remains a human decision.**

**QA VALIDATION INCOMPLETE — <n> failed, <n> pending human or device execution.**

**QA EXECUTION BLOCKED — <reason>. QA status: NOT EXECUTED.**

The first line is permitted only when every agreed test case actually ran and passed. It still does not mean the ticket is QA-approved.

## Final quality gate

- the full Jira issue and every acceptance criterion were read, and no Jira field, status, or transition was modified;
- the agreed QA test cases were consumed as written, with their identifiers preserved;
- no agreed expected result was edited, relaxed, or reinterpreted to match the implementation;
- the build under test is named, and every result came from executing against it;
- no PASS rests on documentation, code reading, a unit-test result, or reasoning;
- every executed command and tool was verified to exist in this environment before being claimed;
- every test case has a verdict or an explicit non-execution reason;
- manual-only and infrastructure-blocked cases are reported as pending, never assumed;
- the ticket is not described as QA-approved, QA-passed, or Stage 08 ready while anything is unverified;
- every failure carries expected, actual, reproduction steps, environment, evidence, severity, and component;
- no defect was created in Jira without explicit authorization for that defect;
- no production code, configuration, or migration was modified;
- no shared or production data was created, modified, or deleted;
- no credential, token, or real personal data appears in the evidence;
- the report states that QA approval remains a human decision.
