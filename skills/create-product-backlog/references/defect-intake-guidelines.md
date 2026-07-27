# Defect Intake Guidelines

## Entry path

Accept an L2-escalated IHD Service Desk bug, an existing Jira production-defect issue, or user-supplied incident evidence without requiring a BRD. Retrieve an existing Jira issue in read-only mode and preserve its key.

## Minimum evidence

Capture when available:

- reported and expected behavior;
- affected application, module, environment, users, sites, services, or workflows;
- first observed time and recurrence;
- reproduction steps and observed result;
- impact, urgency, and operational consequence;
- workaround and its safety or cost;
- logs, screenshots, incident references, attachments, and linked documentation;
- current status, severity, priority, labels, category, and related issues.

Do not invent missing evidence. Separate observed facts from reporter hypotheses.

## Research and classification

1. Read the existing defect and linked evidence.
2. Research expected behavior, rules, workflows, and prior fixes in Confluence.
3. Search Jira for similar symptoms, source links, modules, and business intent.
4. Show possible duplicates before proposing a new issue.
5. Classify a confirmed production bug as a product defect using the project's actual field conventions.
6. Preserve this closure requirement verbatim: **CAPA required at closure**.

CAPA is a later closure obligation. Do not claim CAPA is performed, propose fabricated findings, or close the defect.

## Backlog output

Provide:

- existing key, if supplied and verified;
- classification and evidence;
- affected users or services;
- impact and urgency;
- environment and reproduction information;
- expected versus observed behavior;
- workaround status;
- proposed module, category, priority, and rationale;
- related or duplicate issues;
- useful analysis Tasks, each with purpose and expected result;
- assumptions, missing evidence, and unresolved decisions;
- **CAPA required at closure**;
- `Jira Publication Status: Not Published`.

Never assert root cause. Use language such as `Root cause not established; analysis required.`

## Write restrictions

Do not create, update, comment on, link, move, reprioritize, close, or transition the issue during intake or refinement. Apply the two-part approval-plus-publication gate in `jira-publishing-guidelines.md` before any write.
