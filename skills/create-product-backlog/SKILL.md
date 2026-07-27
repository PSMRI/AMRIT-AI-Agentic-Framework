---
name: create-product-backlog
description: Convert a signed-off AMRIT BRD or FRD, or an L2-escalated production defect, into a traceable, prioritized, human-review-ready backlog of Epics, Stories, Tasks, or Subtasks with testable acceptance criteria and meaningful INVEST reviews. Use for AMRIT SDLC Stage 02 product backlog drafting, refinement, defect intake, duplicate research, Jira publication preparation, or publication of an explicitly finalized backlog after a separate explicit Jira creation request.
metadata:
  stage: Stage 02 - Product Backlog Creation
  category: Product Management
  primary_role: Product Manager
  knowledge_sources:
    - User-supplied information
    - Uploaded approved requirement documents
    - Confluence
    - Jira
  supported_inputs:
    - Signed-off BRD or FRD
    - Confluence page
    - Uploaded approved requirement document
    - L2-escalated bug
    - Existing Jira production defect
  primary_output: Product Backlog Draft - Pending Product Manager Review
  next_skill: stage-03-analysis
---

# Create Product Backlog

Prepare AMRIT SDLC Stage 02 backlog drafts in Markdown. Keep drafting human-led and Jira read-only until the strict publication gate is satisfied.

- Primary role: Product Manager
- Default status: **Draft - Pending Product Manager Review**
- Default Jira publication status: **Not Published**
- Normal destination after publication: Jira backlog, not active development

Never invent requirements, Jira keys, field IDs, field values, estimates, story points, root causes, CAPA findings, sources, citations, or approval.

## Read required resources

Read the references needed for the current path before drafting:

- Always read [references/backlog-structure.md](references/backlog-structure.md), [references/invest-guidelines.md](references/invest-guidelines.md), [references/acceptance-criteria-guidelines.md](references/acceptance-criteria-guidelines.md), [references/prioritization-guidelines.md](references/prioritization-guidelines.md), and [references/information-checklist.md](references/information-checklist.md).
- For any Jira publication request, also read [references/jira-publishing-guidelines.md](references/jira-publishing-guidelines.md).
- For an L2 escalation or production defect, also read [references/defect-intake-guidelines.md](references/defect-intake-guidelines.md).

Use [examples/sample-feature-input.md](examples/sample-feature-input.md) with [examples/sample-feature-output.md](examples/sample-feature-output.md), and [examples/sample-defect-input.md](examples/sample-defect-input.md) with [examples/sample-defect-output.md](examples/sample-defect-output.md), only as fictional patterns. All mandatory resources are inside this independently installable folder.

## Use the connected Atlassian MCP

Discover the installed Atlassian MCP's actual tool names and schemas. Do not assume exact function names.

During intake, research, drafting, and refinement, use only relevant read operations:

- Search and read full Confluence pages and related documentation.
- Search and read Jira issues, duplicates, backlog conventions, issue types, create fields, custom fields, valid options, priorities, labels, components, modules, categories, hierarchy, and boards.

Do not hardcode custom-field IDs or assume Jira projects share the same scheme. Do not run irrelevant searches merely to invoke a tool.

If required research is unavailable, explain what failed and ask whether to retry or proceed with a clearly labelled source-limited draft. Never imply that research succeeded.

## Run bounded iterative research

1. Generate focused searches from the feature, product area, module, roles, workflows, business terms, rules, reports, integrations, linked requirements, existing Epic names, labels, defect symptoms, and affected application.
2. Search, rank results, and read the most relevant material.
3. Record available titles, references, status, version, relevance, and conflicts without fabricating metadata.
4. Extract new terminology and relationships that could materially improve or challenge the backlog.
5. Refine and deduplicate searches, then repeat.
6. Stop when evidence is sufficient, no meaningful new information appears, or remaining results are irrelevant. Stop after three rounds and record any remaining gaps.

Separate findings into **Confirmed facts**, **Proposals**, **Assumptions**, **Conflicts**, and **Unresolved decisions**.

## Select an entry path

### Path A - Signed-off BRD or FRD

1. Confirm that the source is signed off or explicitly approved for decomposition. If not, stop and request an approved source or explicit direction to produce a provisional draft.
2. Read the complete supplied document or retrieve the full Confluence page.
3. Research related Confluence material and Jira conventions or possible duplicates in read-only mode.
4. Extract source requirement IDs, actors, business value, workflows, rules, validations, reports, integrations, modules, categories, dependencies, risks, and known limitations.
5. Decompose the approved scope into Epics, Stories, and only useful Tasks or supported Subtasks.
6. Draft testable acceptance criteria.
7. Assess every Story against each INVEST criterion; rewrite, split, or flag weak Stories.
8. Propose module, category, priority, labels, dependencies, and traceability from evidence. Mark unavailable field values for confirmation.
9. Present the complete backlog for Product Manager review and revise iteratively without writing to Jira.

### Path B - L2-escalated or production defect

1. Read supplied defect evidence. Retrieve a supplied Jira issue in read-only mode and preserve its real key.
2. Inspect the description, impact, affected users or services, environment, severity, reproduction details, workaround, attachments or linked evidence, incidents, labels, and classification.
3. Research expected behavior and business rules in Confluence and search Jira for duplicates or related defects.
4. Classify the item using actual Jira conventions. For a production bug, preserve **Product defect - CAPA required at closure**.
5. Propose priority with impact and urgency context. Never overwrite an existing priority without human approval.
6. Improve the defect backlog item and add analysis Tasks only when useful.
7. Present the proposed defect and related work for Product Manager review without creating, updating, commenting on, linking, moving, closing, or transitioning any Jira issue.

Never invent a root cause or say CAPA is complete.

## Draft the backlog

Use draft identifiers such as `EPIC-01`, `STORY-01`, and `TASK-01`; never fabricate Jira keys.

Include:

1. Document status
2. Source and source approval status
3. Backlog summary and proposed hierarchy
4. Epic details: summary, objective, scope, source, module, category, priority and rationale, dependencies, risks
5. Story details: title, user story where natural, business value, acceptance criteria, source requirement IDs, module, category, priority and rationale, dependencies, assumptions, unresolved decisions, INVEST review
6. Task or Subtask details: purpose, expected result, parent, source, module, category, priority, notes
7. Traceability, possible duplicates, open decisions, and fields needing confirmation
8. Product Manager review status
9. `Jira Publication Status: Not Published`

Use `As a [role], I want [capability], so that [value]` for genuine user-facing Stories. Do not force it onto defects, migrations, configuration, documentation, technical, or operational work.

Write `Source not explicitly identified.` when origin cannot be established.

## Apply the strict Jira write gate

Treat finalization and publication as separate actions. Permit any Jira write only when both conditions are true:

1. A human has explicitly finalized or approved the specific backlog version.
2. A human has explicitly requested that finalized backlog be created or published in Jira.

Approval alone does not authorize a write. Phrases such as "approved," "finalized," "looks good," "ready for review," or "show the final version" do not authorize publication unless the user also explicitly requests Jira creation or publication. If authorization is ambiguous, ask one focused question.

Before any write:

1. Recheck possible duplicates.
2. Discover the target project's current issue types, required create fields, hierarchy, valid field options, and priority values.
3. Show a publication preview with target project; counts and types; modules; categories; priorities; labels; parent-child relationships; proposed creates and updates; unresolved fields; and CAPA-required tagging.
4. Obtain clarification when the project, issue type, hierarchy, required field, or update behavior is unresolved. Do not create incomplete issues.

After the two-part gate is satisfied, use the safest available write operations:

1. Create the Epic and capture its returned key.
2. Create Stories with the correct Epic relationship and capture returned keys.
3. Create Tasks or Subtasks with supported parents.
4. Add only necessary links or approved updates.
5. Keep issues in the backlog unless the user explicitly requests a permitted transition.
6. Verify every created or updated issue by reading it back.
7. Report only returned Jira keys and links, and set `Jira Publication Status: Published` only for successful writes.

Avoid blind bulk creation. Use batch creation only when required fields and relationships remain safe. Never update a possible duplicate, replace a production-defect priority, comment, transition, link, move, or assign to a sprint without explicit authorization covering that action.

## Protect information

Never reveal or store MCP URLs, tokens, passwords, credentials, or private organizational secrets. Summarize relevant source material rather than reproducing confidential pages at length.
