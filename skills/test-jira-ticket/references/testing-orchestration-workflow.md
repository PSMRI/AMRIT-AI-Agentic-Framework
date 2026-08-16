# Testing Orchestration Workflow

## Contents

- [Scope of this document](#scope-of-this-document)
- [Step 1: Read the Jira ticket](#step-1-read-the-jira-ticket)
- [Step 2: Locate the requirement set](#step-2-locate-the-requirement-set)
- [Step 3: Take the artifact inventory](#step-3-take-the-artifact-inventory)
- [Step 4: Establish the lifecycle position](#step-4-establish-the-lifecycle-position)
- [Step 5: Apply user intent](#step-5-apply-user-intent)
- [Step 6: Select the testing activity](#step-6-select-the-testing-activity)
- [Step 7: Invoke the specialist](#step-7-invoke-the-specialist)
- [Step 8: Coordinate a multi-activity run](#step-8-coordinate-a-multi-activity-run)
- [Step 9: Report](#step-9-report)
- [When a specialist skill is unavailable](#when-a-specialist-skill-is-unavailable)
- [What this skill never does itself](#what-this-skill-never-does-itself)
- [Research ledger](#research-ledger)
- [Review checklist](#review-checklist)

## Scope of this document

The full sequence this meta-skill follows from receiving a ticket key to producing the routing and testing report. Routing rules themselves are in [testing-lifecycle-routing.md](testing-lifecycle-routing.md).

## Step 1: Read the Jira ticket

Read the full issue, not the title: issue type, summary, description, **status**, every acceptance criterion, parent Epic, linked issues, subtasks, dependencies, attachments, decision-bearing comments, components and modules, labels, fix version, sprint, and linked Confluence pages.

Number the acceptance criteria as the ticket numbers them; where it does not number them, assign `AC-1`, `AC-2`, … and record that you assigned them so downstream identifiers stay stable.

If the issue cannot be retrieved, stop and report that. Never invent the ticket, its status, or its criteria.

Jira is read-only throughout. The only permitted write anywhere in this architecture is a defect explicitly authorized under `execute-qa-validation`'s own rules.

## Step 2: Locate the requirement set

Follow any Confluence page linked from Jira first, then search focused terms derived from the Jira key, feature name, Epic, module, service, or business capability.

Look for the BRD, FRD, use cases, workflows, business rules, validation rules, role and permission requirements, the approved Stage 03 technical design, and API contracts. Record what was found and what was not. A missing document does not stop routing; it is recorded and, where it matters, reported as a gap.

## Step 3: Take the artifact inventory

Establish each item by inspection, and record it as **present**, **absent**, or **unknown — could not verify**:

| Artifact | Establish by |
| --- | --- |
| Acceptance criteria | The Jira issue |
| Requirement set | Confluence |
| Approved technical design | Confluence |
| Existing QA test cases | Confluence, the configured test-management source, or a prior `draft-test-cases` output |
| Implementation | `git status`, `git diff`, branch and file inspection in the checked-out repositories |
| Source code accessible | Whether those repositories exist in this environment at all |
| Existing unit tests | Test directories covering the changed behaviour |
| Deployed QA build | An environment that actually responds, with a confirmable version |

Two rules:

- **Never record an artifact as present because the stage implies it.** A ticket at Stage 07 does not prove a build exists.
- **Never guess at a repository's state.** If the repository is not checked out here, the implementation is `unknown — could not verify`, not `absent`.

This step is inspection, not a full code review. Establishing that an implementation exists and where it lives is enough; the specialist reads its own code in depth.

## Step 4: Establish the lifecycle position

Map the Jira status to a lifecycle stage, then reconcile it with the inventory.

Where they agree, route normally. Where they disagree, **the artifacts decide what is possible**, and the disagreement appears in the report:

```text
Jira status:        In QA (Stage 07)
Deployed build:     not reachable from this environment
Consequence:        QA execution cannot produce a verdict
```

In Development is **Stage 05**. Never label it Stage 04.

## Step 5: Apply user intent

An explicit request overrides stage inference; it never overrides a missing prerequisite.

When intent and evidence conflict, report the conflict, state what is genuinely possible now, and state what would unblock the requested activity. Never fabricate the prerequisite, and never silently substitute a different activity.

## Step 6: Select the testing activity

Apply the routing decision table and the evidence gates in [testing-lifecycle-routing.md](testing-lifecycle-routing.md).

For each activity, record the evidence that selected it. For each activity not selected, record the reason. An exclusion without a reason is not a decision.

Do not run all three specialists by default. Do not run an activity because it "seems thorough".

## Step 7: Invoke the specialist

Pass a boundary and a set of references, not a digest of the work:

- the Jira key and the acceptance criteria in scope;
- references to the artifacts located — the requirement pages, the approved design, the existing QA test specification, the repositories, the environment;
- the lifecycle position and why this activity was selected;
- explicit exclusions — what it must not do;
- what it must report back.

Invocation order of preference:

1. the host's skill-invocation mechanism;
2. otherwise, read the canonical specialist skill from `skills/<specialist-name>/SKILL.md` and follow it directly;
3. otherwise, apply its contract inline.

Record which mechanism was used for each specialist. Never claim a specialist ran when the work was performed inline.

Do not summarize the artifacts in place of the references. Each specialist reads its own sources — `draft-test-cases` reads the requirements, `write-unit-tests` reads the real diff, `execute-qa-validation` reads the agreed test cases and executes against the real build. That is what stops this orchestrator becoming a lossy context bottleneck, and what stops a QA specification being written from a summary of a summary.

## Step 8: Coordinate a multi-activity run

When more than one activity is genuinely supported, order by dependency:

```text
draft-test-cases          before   execute-qa-validation
implementation exists     before   write-unit-tests
```

Never run an activity merely because another one ran. If one activity is blocked, complete the others and state exactly what was left out and why.

Each specialist's output is reported in full and unmodified. Do not merge three different artifacts into one section, and do not describe them all as "test cases".

## Step 9: Report

Produce the routing and testing report defined in `SKILL.md`, built from the ledger and the specialist results. Every line must correspond to something that actually happened.

Include, always:

- the lifecycle assessment and the full artifact inventory;
- the selected activities with their evidence, and the excluded ones with their reasons;
- the specialist invoked and the mechanism used;
- the specialist's own completion report, unmodified;
- traceability from acceptance criteria to the produced artifact;
- gaps found and the skill that would close each one;
- what a human must decide.

Finish with exactly one of the three completion lines. None of them means the ticket is QA-approved, verified, or Done.

## When a specialist skill is unavailable

Every skill in this framework is independently installable, so an environment may have `test-jira-ticket` without its specialists.

A missing specialist never removes the activity's obligations, and never lowers its standards:

1. perform the activity inline, following that specialist's canonical contract and the same non-negotiable boundaries;
2. keep the discipline intact — implementation-independent expected results for test design; the real diff for unit tests; a real build for QA execution;
3. do not skip the activity, and do not silently downgrade its scope;
4. record in the report that the activity was applied inline because the specialist skill was unavailable.

Never claim a specialist skill executed when the work was performed inline.

## What this skill never does itself

- It never writes QA test cases when `draft-test-cases` is available.
- It never writes unit-test code when `write-unit-tests` is available.
- It never executes QA validation when `execute-qa-validation` is available.
- It never duplicates a specialist's logic into its own instructions.
- It never modifies production code, in any route.
- It never creates a branch, commit, push, or Pull Request.
- It never transitions a Jira issue or claims QA approval.

The value of the meta-skill is the routing decision and the honest report around it, not a second implementation of the specialists.

## Research ledger

Keep a compact ledger through the run: queries executed, sources read, artifacts located with their references, artifacts confirmed absent, environment and repository checks with their outcomes, the routing decision and its evidence, the specialist invoked and how, and unresolved gaps.

Use it to build the report's traceability and to state exactly which evidence supported the routing decision. A route that cannot be justified from the ledger was a guess.

## Review checklist

- the full Jira issue and status were read, and Jira was not modified;
- the requirement set was researched read-only;
- the artifact inventory was taken by inspection before routing;
- unverifiable artifacts were marked unverifiable, not absent;
- the lifecycle position reconciles status with artifacts, and conflicts are reported;
- user intent was honoured except where a prerequisite was genuinely missing;
- every selected activity passed its evidence gate and carries its evidence;
- every exclusion carries a reason;
- specialists received references and boundaries, not digests;
- the invocation mechanism is recorded for each specialist, and inline work is not reported as a specialist run;
- multi-activity runs are dependency-ordered, and blocked activities are stated;
- each specialist's output is reported unmodified and not conflated with another artifact;
- no production code, branch, commit, Pull Request, or unauthorized Jira write occurred;
- no approval or QA sign-off was claimed;
- the report ends with the correct completion line.
