# QA Execution Guidelines

## Contents

- [Scope of this document](#scope-of-this-document)
- [The question this skill answers](#the-question-this-skill-answers)
- [Execution is mandatory for a verdict](#execution-is-mandatory-for-a-verdict)
- [Identify the build under test](#identify-the-build-under-test)
- [Consume the agreed test cases](#consume-the-agreed-test-cases)
- [Classify before executing](#classify-before-executing)
- [Execution order](#execution-order)
- [Verdict rules](#verdict-rules)
- [The evidence standard](#the-evidence-standard)
- [Flaky, environmental, and test-data failures](#flaky-environmental-and-test-data-failures)
- [Acceptance-criterion status](#acceptance-criterion-status)
- [Completion semantics](#completion-semantics)
- [Safety in shared environments](#safety-in-shared-environments)
- [Review checklist](#review-checklist)

## Scope of this document

Executing or coordinating QA validation of one ticket against a deployed QA build at Stage 07 — In QA. Designing the test cases belongs to `draft-test-cases`. Developer-level unit testing belongs to `write-unit-tests`.

## The question this skill answers

> Does the deployed implementation satisfy the previously agreed requirements and test cases?

Not *is the code reasonable*, and not *what should this feature do*. The agreed test cases already settled what it should do. This is the run that finds out whether it does.

## Execution is mandatory for a verdict

A verdict comes from observing the actual system. Nothing else qualifies.

| Not execution | Why it produces no verdict |
| --- | --- |
| Reading the source code | Shows intent, not deployed behaviour |
| Reading the technical design | Describes what was planned |
| Reading the PR description | Describes what a developer believes they did |
| A green unit-test suite | Proves code-level behaviour in isolation, not that the build satisfies the criteria |
| Reasoning that it "should" work | Is an opinion |
| A previous run's result | Applies to a previous build |

When the build or environment is unavailable, the correct output is the blocked report with `Executed: 0` and `QA status: NOT EXECUTED`. A blocked run is a legitimate, useful outcome. A fabricated pass is not.

## Identify the build under test

Record before executing anything:

- environment name and URL;
- deployed version or build identifier;
- commit, tag, or release where discoverable;
- application configuration material to the tests — feature flags, enabled modules, language settings;
- the date of the run.

If the deployed version cannot be confirmed to include the change under test, say so. Testing an environment that does not have the change produces failures that are not defects, and passes that mean nothing.

## Consume the agreed test cases

Take the specification produced at Stage 03 by `draft-test-cases`, or the equivalent agreed test cases in Confluence or the configured test-management source.

- Preserve every identifier: `TC-07`, `AC-3`, and any FRD requirement identifier carried on the case.
- Execute the case as written — same preconditions, same data characteristics, same steps.
- Never edit the expected result. See [Verdict rules](#verdict-rules).

When no agreed test cases exist, state that plainly, validate against the acceptance criteria directly, label the run criteria-driven, and recommend `draft-test-cases` for a reviewed specification. Never invent a specification and present its results as agreed QA scope.

## Classify before executing

Classify every test case first, so the pending set is known up front rather than discovered by omission:

| Classification | Meaning | Report as |
| --- | --- | --- |
| Executable now — automated | An existing or runnable automated check covers it here | Executed, with verdict |
| Executable now — direct | Can be exercised directly against the build, for example an API call | Executed, with verdict |
| Manual-only | Needs human judgement, visual assessment, or exploratory work | `NOT EXECUTED — manual` |
| Infrastructure-blocked | Needs a physical device, browser matrix, connectivity control, or infrastructure this environment lacks | `NOT EXECUTED — infrastructure` |

A case is manual-only because of what it requires, not because automating it would take effort in this session. Be honest in both directions: do not label an executable case manual to avoid running it, and do not label a manual case automated to raise the executed count.

## Execution order

1. **Environment sanity** — confirm the build is reachable, the change is deployed, and a login or authenticated call succeeds. A failure here is `BLOCKED`, not a defect against the ticket.
2. **Existing automated suites** — trigger the suites the repositories already provide, where they are relevant and runnable, and record their real results.
3. **API-level cases** — deterministic, fast, and the clearest evidence.
4. **UI and flow cases** — where a genuine browser or device automation capability exists.
5. **Integration and workflow cases**.
6. **Regression cases** from the agreed specification.
7. **Record the pending set** — manual-only and infrastructure-blocked cases, each with its reason and the action required.

Stop and report if the environment sanity step fails; results gathered against a broken environment are noise.

## Verdict rules

| Verdict | Use when |
| --- | --- |
| `PASS` | The case ran against the identified build in this session and the actual result matched the agreed expected result |
| `FAIL` | The case ran and the actual result did not match the agreed expected result |
| `BLOCKED` | The case could not run to completion — a precondition could not be established, a dependency was down, or the environment failed mid-case |
| `BLOCKED — requirement question` | The agreed expected result appears to contradict an approved source or a changed requirement |
| `NOT EXECUTED — manual` | Requires human execution |
| `NOT EXECUTED — infrastructure` | Requires a device or infrastructure unavailable here |
| `NOT EXECUTED — <reason>` | Any other honest reason |

There is no "assumed pass", "likely pass", "pass by inspection", or "pass based on unit tests".

**The expected result is never edited to match the actual result.** If the specification expects a duplicate-validation message and the build returns HTTP 500, the verdict is `FAIL` and the expected result stands unchanged. Rewriting it would convert a defect into a documented feature and destroy the independence that makes the specification worth executing.

When the agreed expected result genuinely appears wrong — the requirement changed, or the case contradicts an approved source — record `BLOCKED — requirement question` with the precise question and escalate to the QA Lead and Product Manager. Resolving it is their decision, not this skill's.

A human-reported result may be recorded, attributed explicitly to that human and to when they reported it. It is never recorded as though the skill observed it.

## The evidence standard

Every executed case carries evidence proportional to its verdict. A `FAIL` needs enough for someone else to act without re-running it.

| Evidence | Capture for |
| --- | --- |
| Request and response — method, path, status, material body | Every API case |
| Command executed and its real output | Every automated suite run |
| Screenshot or recording | UI failures, and UI passes where a visual expectation exists |
| Application log reference — service, timestamp, correlation identifier | Every failure where logs are reachable |
| Database or state observation | Cases whose expected result includes a state change or the absence of one |
| Device, OS, browser, and version | Any device- or browser-specific case |
| Test data used, by characteristic | Every case |

Redact credentials, tokens, and real beneficiary or patient data from every piece of evidence before recording it. Evidence that cannot be captured is recorded as "evidence unavailable — <why>", never as a stronger claim than what exists.

## Flaky, environmental, and test-data failures

When a case fails, determine which kind of failure it is before reporting it:

| Kind | Signal | Report as |
| --- | --- | --- |
| Real defect | Reproducible against the build with correct preconditions | `FAIL` plus a defect |
| Environmental | A dependency, network, or environment fault unrelated to the change | `BLOCKED` with the environment fault named |
| Test data | Preconditions were not actually established | Fix the data, re-run, and report the final verdict with a note |
| Intermittent | Passes and fails across runs with identical inputs | `FAIL`, flagged as intermittent, with the observed run counts |

Investigate before classifying. Never retry a failing case until it happens to pass and then record `PASS` — record what actually happened, including the intermittency, because an intermittent failure is itself a defect worth raising.

## Acceptance-criterion status

Roll test-case verdicts up to the acceptance criteria, since that is what the ticket is judged on:

| Criterion status | Rule |
| --- | --- |
| Verified | Every test case covering it ran and passed |
| Not satisfied | Any covering test case failed |
| Partially verified | Some covering cases passed and others are pending |
| Unverified | No covering case ran |

A criterion is never `Verified` because most of its cases passed.

## Completion semantics

| Line | Permitted when |
| --- | --- |
| `QA VALIDATION COMPLETE — all agreed test cases executed and passed.` | Every agreed case actually ran and passed. Nothing pending, nothing blocked. |
| `QA VALIDATION INCOMPLETE — <n> failed, <n> pending human or device execution.` | Anything failed, is blocked, or is pending |
| `QA EXECUTION BLOCKED — <reason>. QA status: NOT EXECUTED.` | The build or environment was unavailable and nothing ran |

Every line ends with QA approval remaining a human decision. `COMPLETE` describes the execution, never the ticket's approval state.

## Safety in shared environments

- Never run a destructive operation against a shared QA environment — no bulk delete, no schema change, no truncation, no restart that would disrupt other testers.
- Never create, modify, or delete data in a production database, and never point a test run at a production environment.
- Create only the test data a case genuinely needs, in a non-production environment, and prefer data that is clearly identifiable as test data.
- Never modify application code, configuration, or a migration to make a case pass.
- Never disable a validation, authentication, or authorization check to get a test through.

## Review checklist

- the build under test is identified and confirmed to contain the change;
- the agreed test cases were consumed as written, identifiers preserved;
- no expected result was edited, relaxed, or reinterpreted;
- every claimed tool and command was verified to exist before use;
- every case has a verdict or an explicit non-execution reason;
- no PASS rests on documentation, code reading, unit tests, or reasoning;
- failures are classified as defect, environmental, test-data, or intermittent;
- every failure carries evidence sufficient to act on without re-running it;
- evidence contains no credentials and no real personal data;
- manual-only and infrastructure-blocked cases are reported as pending;
- acceptance-criterion status is rolled up correctly and no criterion is over-claimed;
- nothing in the report claims QA approval, sign-off, or Stage 08 readiness;
- no production code, configuration, shared data, or Jira field was modified.
