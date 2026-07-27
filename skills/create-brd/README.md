# create-brd

`create-brd` prepares a business-focused AMRIT BRD in Markdown from a short request or supplied sources. Every result is labelled **Draft — Pending Human Review**.

## What it does

- Inspects business needs, feedback, notes, guidelines, workflows, screenshots, and existing documents.
- Performs mandatory, iterative, read-only Confluence research through an already-connected Atlassian MCP.
- Consolidates confirmed, assumed, missing, conflicting, and possibly outdated evidence.
- Produces stable business and functional requirement identifiers, acceptance criteria, source references, and unresolved questions.

## What it does not do

It does not perform an automated Business Analyst review, score or certify completeness, approve or sign off a BRD, create an FRD, design implementation, modify Jira, or publish automatically.

## Why Confluence research is mandatory

AMRIT requirements depend on existing workflows, terminology, validation rules, prior decisions, and related documents. The skill generates focused searches from the request, reads relevant pages, and uses newly discovered terminology and relationships to refine later searches. It stops when evidence is sufficient or no material leads remain, with a fixed research-round limit to prevent loops. It records source metadata when available and never fabricates missing details.

## Modes and evidence

- **Interactive mode:** Research first, then ask small groups of questions only for critical remaining gaps.
- **Source-based mode:** Treat supplied material as primary, research related Confluence content, and preserve supported terminology.

Conflicts are not silently reconciled; the draft records both statements, their sources, impact, and clarification needed. Missing information remains visible as assumptions, open questions, or information requiring human confirmation. If Confluence is unavailable, the skill reports the limitation and asks whether to retry or proceed with a source-limited draft.

## Optional Confluence publishing

Confluence is read-only by default. After the full draft is shown, the skill may create or update a page only when the user explicitly requests it and the destination is clear. It never marks the page approved.

## Human review

Business Systems Analyst, Product Manager, and relevant stakeholder review remain mandatory. Product Manager sign-off is a lifecycle exit criterion, not an action or claim made by this skill.

## Example invocations

- `Create a BRD for enabling username editing in Employee Master.`
- `Create a BRD from these meeting notes.`
- `Create a BRD from these programme guidelines and related Confluence documents.`
- `Draft the BRD first, then publish it to the Product Requirements space after I approve it.`

## Independent installation

Download or copy this `create-brd` folder and add it through Claude Desktop's Add Skills flow. `SKILL.md` must be directly inside the selected folder. The folder is self-contained and does not depend on repository-level files. An already-connected Atlassian MCP with Confluence search and page-read capabilities is required.
