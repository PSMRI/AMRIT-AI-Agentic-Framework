# Defect Reporting Guidelines

## Contents

- [Scope of this document](#scope-of-this-document)
- [A QA failure never becomes a code fix](#a-qa-failure-never-becomes-a-code-fix)
- [Before raising anything, classify the failure](#before-raising-anything-classify-the-failure)
- [Defect creation modes](#defect-creation-modes)
- [Required defect content](#required-defect-content)
- [Severity](#severity)
- [Reproduction steps](#reproduction-steps)
- [Duplicates and existing defects](#duplicates-and-existing-defects)
- [Preparing clean inputs for root-cause analysis](#preparing-clean-inputs-for-root-cause-analysis)
- [Review checklist](#review-checklist)

## Scope of this document

Turning a failed QA test case into a defect report that someone else can act on, under this framework's write-safety conventions.

## A QA failure never becomes a code fix

When a test fails, this skill records the failure and raises the defect. It does not repair the system.

- Never modify production code, configuration, a migration, or a build file to make a case pass.
- Never disable a validation, authentication, or authorization check to get a test through.
- Never edit, relax, or reinterpret the agreed test case so the implementation satisfies it.
- Never weaken or skip an existing automated test.

A QA failure returns the work to the implementation flow — `implement-jira-ticket` and its Stage 05 specialists — through the defect and rework path. QA that fixes the code it is testing is no longer independent, and its subsequent passes mean nothing.

## Before raising anything, classify the failure

| Classification | Signal | Action |
| --- | --- | --- |
| Real defect | Reproducible against the identified build with correct preconditions | Raise a defect |
| Environmental | A dependency, network, or environment fault unrelated to the change | Report as `BLOCKED` with the fault named; no defect against the ticket |
| Test data | Preconditions were not actually established | Correct the data, re-run, report the final verdict with a note |
| Test case error | The case contradicts an approved source, or the requirement changed | `BLOCKED — requirement question`; escalate to QA Lead and Product Manager, do not edit the case |
| Intermittent | Passes and fails across runs with identical inputs | Raise a defect, flagged intermittent, with the observed run counts |

Classify before reporting. A defect raised for an environment fault wastes a developer's time; an environment fault recorded for a real defect hides a release risk.

An intermittent failure is a defect, not a reason to keep re-running until it passes.

## Defect creation modes

Jira is read-only by default across this framework, and writes require an explicit, specific request. Apply the same convention here.

| Mode | Use when | Behaviour |
| --- | --- | --- |
| **Draft only** | Default, and whenever there is any doubt | Present the complete defect content in the report. Create nothing in Jira. |
| **Proposed for confirmation** | A Jira write capability exists and the user asked for defects to be raised | Present the complete draft, then create it only after explicit confirmation of that specific defect |
| **Automatic** | The user explicitly and unambiguously authorized automatic defect creation for this run | Create it, then report exactly what was created |

Rules that hold in every mode:

- Never transition, reopen, or edit the fields or status of the ticket under test.
- Never link, assign, or comment beyond what the authorized defect creation itself requires.
- Never fabricate a defect key. A defect that was not created is reported as `draft below` or `proposed — awaiting confirmation`, never as `AMRIT-XXXX` presented as real.
- Confirmation for one defect is not confirmation for the next.

## Required defect content

Every defect, whether draft or created, contains:

| Field | Content |
| --- | --- |
| Summary | The observable failure in one line, naming the behaviour and the condition |
| Failed test case | `TC-07` |
| Acceptance criterion | `AC-3`, plus any FRD requirement identifier carried on the case |
| Source ticket | The ticket under validation |
| Expected behaviour | The agreed expected result, verbatim from the specification |
| Actual behaviour | Exactly what was observed, with the concrete result — status code, message, state |
| Reproduction steps | Numbered, deterministic, from a stated starting state |
| Environment | Environment name and URL, build or version, commit or release, date |
| Test data | Described by characteristic, with no real personal data |
| Evidence | Response bodies, command output, log references, screenshots where available |
| Severity | Critical / Major / Minor / Trivial, with the reason |
| Affected component | The module, service, screen, or repository, where identifiable from the observed behaviour |
| Reproducibility | Always / Intermittent (`n` of `m` runs) / Once |
| Regression | Whether this behaviour previously worked, where that is known |

Do not diagnose the cause in the defect. "Duplicate check missing in the service layer" is a hypothesis; "the API returns HTTP 500 where the agreed expected result is a duplicate-validation rejection" is an observation. Report the observation, and name the affected component only as far as the evidence supports.

## Severity

| Severity | Use when |
| --- | --- |
| Critical | Data loss or corruption, a security or authorization failure, a core flow entirely blocked, or a failure affecting patient or beneficiary safety |
| Major | An acceptance criterion is not satisfied, a significant flow is broken, or a documented rule is not enforced |
| Minor | A limited or cosmetic-plus failure with an available workaround |
| Trivial | Cosmetic only, with no functional impact |

Severity is the observed impact. It is not the priority — priority is a triage decision the Product Manager and QA Lead own, and this skill does not set it.

A failure that lets invalid data into the system, or that lets a user act beyond their role, is at least Major regardless of how small the reproduction looks.

## Reproduction steps

Steps must let someone reproduce the failure without contacting the tester:

1. start from an explicitly stated state — role, environment, and any pre-existing records;
2. one action per step, in order;
3. name the exact data characteristics used;
4. end at the point where the actual result is observable;
5. state the actual result and the agreed expected result separately.

If the failure could not be reproduced on a second attempt, say so and record it as intermittent with the run counts. Never present a single unreproducible observation as a reliably reproducible defect.

## Duplicates and existing defects

Before drafting, search Jira read-only for an existing defect describing the same behaviour on the same build or component. If one exists:

- reference it rather than drafting a new defect;
- add the new evidence to the report, noting that the existing defect covers it;
- never edit or comment on the existing defect without explicit authorization.

## Preparing clean inputs for root-cause analysis

A separate `root-cause-analysis` skill is expected in this framework later. It does not exist yet and is not implemented here. Structure every defect so it would be usable as a clean input without re-investigation:

- test case and acceptance-criterion identifiers, preserved verbatim;
- expected and actual behaviour stated separately and concretely;
- deterministic reproduction steps;
- environment and build identity, so the failure is anchored to a specific deployed state;
- evidence references — responses, logs, screenshots — rather than prose descriptions of them;
- affected component as far as evidence supports, with hypotheses clearly marked as hypotheses;
- reproducibility and, where known, whether this is a regression.

A failure recorded only as prose has to be re-investigated before anyone can analyse it, which is the cost this structure avoids.

## Review checklist

- the failure was classified before it was reported;
- no production code, configuration, migration, or existing test was modified;
- no agreed test case was edited to match the implementation;
- the defect creation mode matches the authorization actually given;
- no defect key was fabricated, and nothing was created without explicit authorization;
- the ticket under test was not transitioned, edited, or commented on;
- every required defect field is present;
- expected and actual behaviour are separate, concrete, and evidence-backed;
- reproduction steps are deterministic and start from a stated state;
- severity reflects observed impact, and priority was not assumed;
- evidence contains no credentials and no real personal data;
- a duplicate search was performed and an existing defect was referenced rather than duplicated;
- the defect would serve as a clean input to root-cause analysis without rework.
