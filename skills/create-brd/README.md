# create-brd

`create-brd` prepares a traceable AMRIT Business Requirements Document in Markdown for Stage 01/12 — Business & Product. Every result is labelled **Draft — Pending Human Review**.

## Intended users

The primary user is a Business Systems Analyst. Product Managers and relevant stakeholders remain required human reviewers.

## Inputs

The skill supports interactive creation from a short business need or feature request and source-based creation from supplied material, including:

- field or stakeholder feedback;
- government programme guidelines;
- workflows, screenshots, and meeting notes;
- PDFs, existing BRDs or FRDs, and product documents;
- relevant Confluence pages.

Historical Jira material may be supplied as evidence, but the skill does not search or modify Jira.

## Required MCP capability

An already-connected Atlassian MCP must provide Confluence search and page-read capabilities. Focused, iterative Confluence research is mandatory before every BRD draft and is read-only by default.

If Confluence research fails, the skill reports the limitation and asks whether to retry or proceed with a clearly source-limited draft. It never implies that unavailable research succeeded.

Confluence page creation or update is optional. The skill may publish only after showing the full draft and receiving an explicit publication request with a clear destination.

## Output

The skill produces one Markdown BRD with:

- stable business and functional requirement identifiers;
- traceable acceptance criteria and source references;
- confirmed information, assumptions, gaps, conflicts, and possibly outdated evidence;
- unresolved questions and review status.

It does not create an FRD or technical design.

## Human review and publishing guardrails

The skill never scores, certifies, approves, rejects, signs off, or automatically publishes a BRD. Optional Confluence publishing does not mark the document approved. Business Systems Analyst, Product Manager, and relevant stakeholder review remain mandatory.

## Use and distribution

Invoke `/create-brd` in Claude Code from the repository root. Claude Desktop
users can download [create-brd.zip](../../releases/latest/download/create-brd.zip).
See the [distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
