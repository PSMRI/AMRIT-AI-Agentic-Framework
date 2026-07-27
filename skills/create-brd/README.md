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

## Install for Claude Code

From the repository root:

```bash
python scripts/install-skill.py create-brd
```

Use `--scope project` to install only for the current repository. After installation, invoke the skill with:

```text
/create-brd
```

Example:

```text
/create-brd

Create a BRD from these programme guidelines and related Confluence documents.
Keep it as a draft for human review.
```

## Install in Claude Desktop

1. Download [`skill-zips/create-brd.zip`](../../skill-zips/create-brd.zip).
2. Open Claude Desktop.
3. Open the **Add Skills** interface.
4. Upload `create-brd.zip`.
5. Confirm that the skill appears and the required Atlassian MCP connection is available.

## Generate the skill package

From the repository root:

```bash
python scripts/package-skill.py create-brd
```

The generated archive is written to `skill-zips/create-brd.zip`.

For all installer options, see the [repository installation guide](../../docs/installation.md). For lifecycle inputs and review gates, see the [lifecycle mapping](../../docs/lifecycle-mapping.md).
