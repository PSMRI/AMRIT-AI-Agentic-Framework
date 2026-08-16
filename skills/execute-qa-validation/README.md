# execute-qa-validation

`execute-qa-validation` is the **QA Tester / QA Automation Engineer** specialist for Stage 07 — In QA. It answers one question:

> Does the deployed implementation satisfy the previously agreed requirements and test cases?

**This skill executes tests against a real build.** It changes no production code, and it is never the QA approver.

## Purpose

Consume the QA test cases agreed at Stage 03, discover what test tooling this environment genuinely provides, execute what can actually be executed against the deployed QA build, record expected versus actual with evidence for every case, report everything that did not run, and raise defect-quality reports for failures.

## Three different testing artifacts

| Skill | Stage | Artifact |
| --- | --- | --- |
| [`draft-test-cases`](../draft-test-cases/README.md) | Stage 03 — Analysis | Functional QA test **specifications** |
| [`write-unit-tests`](../write-unit-tests/README.md) | Stage 05 — In Development | Executable developer-level **unit-test code** |
| `execute-qa-validation` | Stage 07 — In QA | QA **execution results and evidence** |

This skill consumes the specification. It does not author it, and it does not regenerate it from what the implementation happens to do.

## Relationship to `test-jira-ticket`

```text
test-jira-ticket
    └── Stage 07 — In QA
        └── execute-qa-validation        ← this skill
```

[`test-jira-ticket`](../test-jira-ticket/README.md) selects this skill when the ticket is at In QA and a build exists. The skill is independently installable and independently invocable; when it is not installed, the meta-skill applies the QA execution contract inline and says so.

## Execution against the real build is mandatory

Documentation cannot produce a PASS. Neither can source code, a technical design, a PR description, a green unit suite, or reasoning about what the code should do.

When the build or environment is unavailable, the run stops:

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

A blocked run is a legitimate outcome. A fabricated one is not.

## The agreed expected result never changes

If the specification expects a duplicate-validation rejection and the build returns HTTP 500, the verdict is `FAIL`. The expected result is not rewritten to say `HTTP 500`. Rewriting it would convert a defect into a documented feature.

Where the agreed expected result genuinely appears wrong, the case is recorded `BLOCKED — requirement question` and escalated to the QA Lead and Product Manager — never resolved by editing the case.

## Result model

```text
Test Case: TC-07
Acceptance Criterion: AC-3

Expected: Duplicate beneficiary is rejected.
Actual:   HTTP 500 returned.
Result:   FAIL

Evidence:
- API response
- application log reference
- screenshot where available

Severity: Major
Defect:   AMRIT-XXXX
```

Verdicts are `PASS`, `FAIL`, `BLOCKED`, or `NOT EXECUTED — <reason>`. There is no assumed pass.

## Automated versus manual is always explicit

```text
QA Execution Summary

Total test cases: 42

Automated/executable: 37
Passed:               35
Failed:                2
Manual-only:           5
Pending human QA:      5

Overall: QA VALIDATION INCOMPLETE
```

A ticket is never reported QA-approved, QA-complete, or Stage 08 ready while manual-required or infrastructure-blocked scenarios remain unverified. A high automated pass rate does not close that gap.

## Tooling is discovered, never assumed

Selenium, Playwright, Appium, Postman or Newman, BrowserStack, Firebase, and existing project suites are usable only when verified present, invocable, and able to reach the build. Absence is recorded explicitly, and is what justifies each `NOT EXECUTED — infrastructure` verdict. Nothing is installed to close a gap.

## Defects, not fixes

A failure produces a defect containing the failed test case, the acceptance criterion, expected and actual behaviour, deterministic reproduction steps, environment and build identity, evidence, severity, affected component, and reproducibility.

Jira is read-only by default. Defect creation is **draft only** unless the user explicitly asks for defects to be raised, in which case each defect is proposed for confirmation before creation. No defect key is ever fabricated, and the ticket under test is never transitioned or edited.

The skill never modifies production code, configuration, or a migration to make a test pass. A QA failure returns the work to the implementation flow.

## Prepared for root-cause analysis

A separate `root-cause-analysis` skill is expected later and is **not** implemented here. Failures are structured — preserved identifiers, separated expected and actual behaviour, deterministic steps, build identity, evidence references, reproducibility — so they would serve as clean inputs to that analysis without re-investigation.

## QA approval stays human

Stage 08 — QA Approved is a human accountability gate. This skill gives the human QA tester honest evidence to decide with. It never claims to be that approver, never records QA sign-off, and never states that a ticket has passed QA.

## Required capabilities

Read access to Jira and Confluence, access to the deployed QA build, host command execution and filesystem access, an HTTP capability for API cases, and browser, device, log, or observability capability where the environment genuinely provides it. A Jira write capability is used only for an explicitly authorized defect. Tool names are discovered, not hardcoded.

## Example invocation

```text
/execute-qa-validation DEMO-4102
```

See [examples/sample-qa-execution-report.md](examples/sample-qa-execution-report.md) for a fictional run with passes, failures, a drafted defect, and a pending device case, and [examples/sample-blocked-execution.md](examples/sample-blocked-execution.md) for the blocked and pending-manual outcomes. The examples are illustrative only and do not describe real AMRIT builds or defects.

## Use and distribution

Invoke `/execute-qa-validation` from the repository root using a supported coding agent, or let `/test-jira-ticket` route to it. For a packaged installation, download `execute-qa-validation.zip` from the latest release. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
