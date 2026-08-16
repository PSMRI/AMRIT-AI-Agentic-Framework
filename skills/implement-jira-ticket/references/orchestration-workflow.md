# Orchestration Workflow

## Contents

- [Purpose](#purpose)
- [Step 1: Read the Jira ticket](#step-1-read-the-jira-ticket)
- [Step 2: Read linked requirements and approved design](#step-2-read-linked-requirements-and-approved-design)
- [Step 3: Research the technical knowledge](#step-3-research-the-technical-knowledge)
- [Step 4: Inspect the actual source code](#step-4-inspect-the-actual-source-code)
- [Step 5: Determine impacted repositories and modules](#step-5-determine-impacted-repositories-and-modules)
- [Step 6: Classify the required personas](#step-6-classify-the-required-personas)
- [Step 7: Build the implementation plan](#step-7-build-the-implementation-plan)
- [Step 8: Invoke the selected specialists](#step-8-invoke-the-selected-specialists)
- [Step 9: Coordinate dependencies](#step-9-coordinate-dependencies)
- [Step 10: Ensure unit tests exist](#step-10-ensure-unit-tests-exist)
- [Step 11: Verify](#step-11-verify)
- [Step 12: Summarize the evidence](#step-12-summarize-the-evidence)
- [Step 13: Hand off](#step-13-hand-off)
- [Research ledger](#research-ledger)

## Purpose

Sequence the work so that requirements are understood before architecture, architecture before code, code before delegation, and delegation before verification. Skipping forward produces changes that satisfy a title rather than a ticket, and produces personas that run because they exist rather than because the ticket needs them.

Steps 1 to 7 are read-only. Editing begins in Step 8, inside the specialists. Jira, Confluence, OpenProject, DeepWiki, and Graphify remain read-only throughout.

## Step 1: Read the Jira ticket

Accept the ticket key from the invocation, for example `/implement-jira-ticket AMRIT-1234` or `Implement AMRIT-1234`. If no key is supplied, ask for one before researching.

Retrieve the issue through the connected Jira read capability and read it in full:

- issue type — Story, Task, or Bug;
- summary;
- description;
- acceptance criteria;
- parent Epic;
- linked issues and their relationship type;
- subtasks;
- dependencies and blockers;
- attachments, including wireframes and mockups;
- comments that carry requirement or design decisions;
- priority where it affects scope or sequencing;
- components and modules;
- labels;
- linked Confluence pages;
- referenced technical-design material.

The acceptance criteria define scope. Where a ticket has no explicit acceptance criteria, derive the intended behaviour from the description and supporting documents, and state in the report which criteria were inferred.

Do not transition the issue, comment, edit fields, assign users, create subtasks, or change status at any point, including after implementation succeeds.

If the issue cannot be retrieved, stop and report the retrieval failure. Never reconstruct requirements from the key, the branch name, or memory.

Where the environment also exposes OpenProject and the work is tracked there, read the corresponding work package for delivery context only. It does not replace the Jira acceptance criteria, and it is read-only.

## Step 2: Read linked requirements and approved design

Follow any Confluence page linked directly from the Jira issue first. Then search focused terms derived from the Jira key, feature name, Epic, module, service, and business capability.

Look for:

- the approved Stage 03 technical design — HLD, LLD, API decisions, and database decisions;
- BRD and FRD;
- functional specifications;
- workflows;
- wireframes and approved UX;
- acceptance rules and business rules;
- API requirements;
- architecture documents;
- related feature documentation.

Use a bounded search-read-refine loop. Deduplicate queries and pages, and stop when the evidence is sufficient, when no material new information appears, or after three rounds.

An approved technical design is consumed, not rewritten. Record the design constraints each specialist must honour: module ownership, API contracts, schema decisions, integration boundaries, and security or performance constraints.

A BRD may not exist for every ticket. Read one when it does, continue on the remaining approved evidence when there is none, never fabricate one, and never stop merely because it is absent. Confluence is read-only.

Keep four categories distinct when reasoning and reporting:

1. Jira acceptance criteria.
2. Documented business or functional requirements.
3. Approved architectural guidance.
4. Assumption or inferred behaviour.

## Step 3: Research the technical knowledge

Follow the knowledge-source order in [codebase-inspection-guidelines.md](codebase-inspection-guidelines.md): DeepWiki first, Confluence for intended architecture and rationale, Graphify only as the final fallback for unresolved cross-repository relationships.

Research only the repositories the ticket plausibly touches, identified from the current working directory, the ticket's components and Epic, the approved design, Confluence evidence, and [amrit-repository-map.md](amrit-repository-map.md). Start with no more than three repositories where practical.

Record what each source contributed. It is used both for routing and for the report.

## Step 4: Inspect the actual source code

Mandatory in every route. Follow [codebase-inspection-guidelines.md](codebase-inspection-guidelines.md).

The orchestrator inspects enough of the real code to determine impact, ownership, dependencies, and contracts. Each specialist then performs its own deeper inspection of the layer it owns; the orchestrator does not attempt to pre-digest the codebase for them.

If the relevant source code is not accessible, stop and report `IMPLEMENTATION BLOCKED` as defined in `SKILL.md`.

## Step 5: Determine impacted repositories and modules

Produce an explicit impact statement before routing:

- each affected repository and what changes inside it;
- the modules, packages, services, components, or migration areas inside each;
- adjacent repositories deliberately not changed, with the reason;
- shared or common repositories, included only when the behaviour actually uses them;
- `AMRIT-DB`, included only when a schema object may change.

Never expand the change into a repository because a persona exists for it. Never modify an unrelated repository.

When one ticket legitimately spans repositories, keep the changes traceable per repository. They are separate Git repositories and may need separate Pull Requests downstream; that is `create-development-pr`'s decision, not this skill's.

## Step 6: Classify the required personas

Apply [persona-routing-guidelines.md](persona-routing-guidelines.md). Select each persona from evidence in the ticket, the approved design, and the source inspection.

Record, for the report:

- the personas selected and the evidence for each;
- the personas considered and excluded and why;
- whether each selected persona's specialist skill is available in this environment.

## Step 7: Build the implementation plan

Before any edit, establish:

- which acceptance criteria are being implemented;
- affected components per repository;
- the dependencies between the specialist changes;
- the execution order;
- the contracts between components — schema shape, API request and response, DTO and model fields, component inputs and outputs, error semantics;
- the verification each change requires;
- backward-compatibility impact;
- potential regression areas;
- what must deliberately not change.

Trace every material code change to a Jira acceptance criterion, a supporting approved requirement or design, or a necessary engineering change required to support them. A change that traces to none of these does not belong in this ticket. Do not add speculative features or implement future requirements outside the ticket.

## Step 8: Invoke the selected specialists

For each selected specialist, in the planned order, pass a boundary rather than a code summary:

- the Jira key and the acceptance criteria in scope for that persona;
- the repository or repositories and the modules it may change;
- the approved-design constraints it must honour;
- the contracts it must produce or consume, including anything an upstream specialist has already established;
- explicit exclusions — files, modules, repositories, and behaviours it must not change;
- the requirement to inspect its own code before editing;
- the requirement to report files changed, contracts produced, checks run, and blockers.

Use the host's skill-invocation mechanism. When it is unavailable, read the canonical specialist skill directly from `skills/<specialist-name>/SKILL.md`. When neither is possible, apply the persona contract inline as described in [persona-routing-guidelines.md](persona-routing-guidelines.md) and state that in the report.

Never claim a specialist ran when it did not.

## Step 9: Coordinate dependencies

Apply [coordination-and-verification-guidelines.md](coordination-and-verification-guidelines.md).

After each specialist completes, re-check the contract the next one depends on against the actual code, not against the previous specialist's description of it. If a specialist reports a blocker, stop the dependent work rather than implementing against a contract that does not exist, and complete only the independent work that remains safe.

## Step 10: Ensure unit tests exist

Whenever production behaviour changed, `write-unit-tests` runs and covers the changed behaviour: happy path, validation, error behaviour, boundary cases, and regression risk, with dependencies mocked as the repository already does.

This is developer, code-level testing. It is not `execute-qa-validation` at Stage 07 and it is not `draft-test-cases` at Stage 03.

## Step 11: Verify

Discover the repository's actual commands from build files, package manifests, CI configuration, and contributor documentation. Run narrow checks first, then broader checks where practical, for every repository that changed.

Report only what ran. `PASS` requires successful execution in this session; use `FAILED` with the cause, or `NOT RUN — <reason>` when the environment prevents it. Never weaken a test, disable a lint rule, or narrow a check to obtain a green result.

## Step 12: Summarize the evidence

Produce the orchestration report defined in `SKILL.md`, built from the research ledger and the specialist results. Every line must correspond to something that actually happened.

## Step 13: Hand off

Name `create-development-pr` as the next skill and finish with exactly one of:

**Implementation complete and locally verified. Ready for PR preparation.**

**Implementation incomplete. Resolve the items above before PR preparation.**

Never state that the ticket is Done, approved, merged, or code-review signed off. Never create a branch, commit, push, or Pull Request, and never transition the Jira issue.

## Research ledger

Keep a compact ledger through the run containing queries executed, sources read, files inspected, findings that changed the plan, routing decisions, contracts established, specialist results, conflicts, and unresolved gaps. Use it to avoid repeating research, to build the traceability in the report, and to state exactly which evidence supported the implementation.
