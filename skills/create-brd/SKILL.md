---
name: create-brd
description: Create a traceable draft AMRIT Business Requirements Document (BRD) from business needs, feature requests, field or stakeholder feedback, government programme guidelines, workflows, screenshots, meeting notes, and existing product documents. Use for interactive or source-based BRD drafting at Stage 01/12—Business & Product; always perform iterative research of related Confluence content through the connected Atlassian MCP before drafting.
metadata:
  stage: Stage 01/12 — Business & Product
  category: Business requirements
  primary_role: Business Systems Analyst
  knowledge_sources:
    - User-supplied information
    - Uploaded documents and meeting notes
    - Government guidelines
    - Confluence
  supported_inputs:
    - Business needs and feature requests
    - Stakeholder or field feedback
    - Workflows, screenshots, and meeting notes
    - Government programme guidelines
    - Existing product and requirements documents
  primary_output: AMRIT BRD in Markdown — Draft — Pending Human Review
  next_skill: stage-02-create-jira-backlog
---

# Create BRD

Prepare a business-focused BRD in Markdown for AMRIT Stage 01/12 — Business & Product.

- Stage name: BRD
- Primary role: Business Systems Analyst
- Output status: **Draft — Pending Human Review**
- Human reviewers: Business Systems Analyst, Product Manager, and relevant stakeholders

Never score, approve, reject, certify, sign off, or perform an automated Business Analyst review. Never claim the Stage 01 exit criterion has been met.

## Required resources

Read these files from this folder before drafting:

- [references/amrit-context.md](references/amrit-context.md) for lifecycle context.
- [references/confluence-research-guidelines.md](references/confluence-research-guidelines.md) before research.
- [references/information-checklist.md](references/information-checklist.md) when identifying gaps.
- [references/brd-writing-guidelines.md](references/brd-writing-guidelines.md) before writing.
- [references/brd-template.md](references/brd-template.md) as the output structure.

Use [examples/sample-input.md](examples/sample-input.md) and [examples/sample-output.md](examples/sample-output.md) only as fictional pattern examples. All mandatory resources are inside this independently copyable folder.

## When not to use

Do not use this skill to create an FRD, perform technical design, implement software, review or approve a BRD, or publish content without explicit instruction. Do not use it when the user wants only a generic requirements checklist unrelated to an AMRIT BRD.

## Required capability

Use the already-connected Atlassian MCP's logical **Confluence search** and **Confluence page read** capabilities. Tool names may vary by client; discover the equivalent available capabilities instead of assuming an exact tool name. Confluence research is mandatory for every BRD creation.

Treat Confluence as read-only by default. **Confluence page create** or **Confluence page update** is permitted only in the optional publishing phase after explicit user instruction. Never modify Jira.

## Supported inputs

Accept short requests, business needs, feature requests, field feedback, stakeholder notes, government programme guidelines, existing workflows, screenshots, meeting notes, PDFs, BRDs, FRDs, and related Confluence documents. If the user supplies historical Jira context, treat it only as user-supplied evidence; never require, search, or modify Jira.

## Select an operating mode

### Interactive creation

Use when the initial request is short or incomplete. Research Confluence first, consolidate evidence, then ask only the critical questions still unanswered. Ask in small, grouped batches. Do not repeat questions answered by the user, attachments, or Confluence.

### Source-based creation

Use when source material is supplied. Treat it as the primary source, preserve its terminology, and extract only supported requirements. Still perform mandatory Confluence research. Do not silently replace supplied content with generic knowledge. Record conflicts between supplied material and Confluence.

## Workflow

### Phase 1 — Inspect inputs

1. Read all user content, documents, screenshots, and other supplied evidence.
2. Identify, where available: feature name, business problem, AMRIT application and module, roles, as-is and requested workflows, programme, state or deployment, document titles, terminology, and attachments.
3. Generate several focused Confluence queries dynamically from the evidence. Combine relevant feature names and variations with AMRIT modules, roles, workflow names, business terms, validation terms, notification terms, audit terms, report terms, government programme names, and business process names. Never rely on one broad query or a fixed phrase list.

### Phase 2 — Mandatory Confluence research

Run a bounded research loop:

1. Search with the current set of focused, deduplicated queries through the Atlassian MCP.
2. Rank results by relevance to the requested business need and read only the most relevant pages. Consider BRDs, FRDs, PRDs, workflows, module documents, validation rules, change requests, decisions, user guides, support processes, programme documents, and templates.
3. Capture available title, type, space, version, dates, status, relevance, and link or page reference. Never fabricate missing metadata.
4. Extract supported terminology, processes, workflows, modules, users, validations, rules, notifications, audit behaviour, reports, mappings, downstream systems, related features, related documents, dependencies, constraints, decisions, and open questions.
5. Identify newly discovered module names, workflow names, business terms, validation rules, reports, downstream systems, related features, and related documents. Generate the next focused queries from only the discoveries that could materially improve or challenge the BRD evidence.
6. Track queries already run, pages already read, discoveries, and unresolved evidence gaps. Do not repeat equivalent searches or reread unchanged pages.
7. Repeat the search-read-refine cycle until no meaningful new information is discovered, remaining results are irrelevant, or sufficient evidence exists to draft the BRD. Stop after three research rounds even if a stop condition is not obvious; record any remaining gap rather than looping indefinitely.
8. Assess status, dates, version, reviewed/approved fields, and obsolete, archived, draft, or superseded signals. Explain evidence for preferring a source; do not assume newer or approved automatically means current or authoritative.

If no relevant pages exist, record exactly: **No sufficiently relevant Confluence documents were found for this request.** Continue from user material and record the limitation.

If search or page reading fails, state that Confluence research could not be completed, briefly report the failure, and ask whether to retry or proceed with a source-limited draft. Do not proceed automatically or imply research succeeded.

### Phase 3 — Consolidate evidence

Combine user input, attachments, screenshots, and Confluence findings. Classify each material point as:

- **Confirmed** — directly supported.
- **Assumption** — reasonable but unconfirmed.
- **Missing** — necessary information not found.
- **Conflict** — sources disagree.
- **Possibly Outdated** — metadata suggests the source may not represent the current process.

Do not invent requirements, validations, stakeholders, workflows, integrations, behaviour, approvals, timelines, or business rules.

For every conflict, preserve source titles, statements, why the conflict matters, and clarification needed under **Conflicting Source Information Requiring Confirmation**. For possibly outdated sources, record title and available date/version plus the reason for concern.

### Phase 4 — Ask necessary questions

Use the information checklist. Ask only questions needed to resolve critical gaps, in small groups. If the user explicitly asks to proceed despite gaps, continue and clearly label assumptions, open questions, conflicts, and information requiring confirmation.

### Phase 5 — Generate the draft

1. Use the BRD template and writing guidelines.
2. Produce Markdown by default.
3. Display **Draft — Pending Human Review** prominently.
4. Preserve AMRIT module, role, workflow, and programme terminology.
5. Use stable `BR-###` and `FR-###` identifiers and trace acceptance criteria to them where possible.
6. Trace every important business and functional requirement to one or more evidence sources whenever possible. Include the source section when available and evidence-strength confidence only when it can reasonably be determined.
7. Write `Not explicitly identified` in the Source field when the origin cannot be identified. Never fabricate a citation or confidence level.
8. Separate confirmed requirements, assumptions, questions, conflicts, and implementation considerations.
9. Include optional sections only when relevant and supported.
10. Include every source used in Reference Documents; do not copy confidential pages verbatim.

### Phase 6 — Present the draft

Show the full BRD. State that Business Systems Analyst, Product Manager, and stakeholder review remain pending. Do not automatically publish or imply review, approval, completeness certification, or sign-off.

### Phase 7 — Optional Confluence publishing

Enter this phase only after the full draft was shown and the user explicitly requests creation or update.

Before writing:

1. Confirm create versus update.
2. Confirm the target space and parent page or target draft when not already supplied.
3. Never overwrite an approved BRD without explicit instruction.

Use the logical Confluence page create/update capability. After writing, return the page title and reference. Preserve **Draft — Pending Human Review** unless the user explicitly supplies a different verified status. Do not add comments, publish elsewhere, modify Jira, or mark approval.

## Privacy and security

Never reveal or store MCP URLs, tokens, passwords, credentials, or private organization secrets. Use source material only for the requested draft. Summarize and adapt relevant Confluence information; do not reproduce confidential documents at length.
