# create-product-backlog

`create-product-backlog` supports the AMRIT Product Manager at SDLC Stage 02. It converts an approved BRD or FRD, or an L2-escalated production defect, into a traceable and prioritized backlog draft containing Epics, Stories, Tasks or Subtasks, acceptance criteria, and meaningful INVEST reviews.

## Supported inputs

- Signed-off BRD or FRD
- Approved Confluence requirement page
- Uploaded approved requirement document
- L2-escalated bug and supporting evidence
- Existing Jira production-defect issue

An already-connected Atlassian MCP must provide equivalent Confluence and Jira read capabilities. Jira write capabilities are needed only for an explicitly authorized publication.

## Two entry paths

### Approved feature requirements

The skill confirms approval, reads the full source, performs bounded Confluence and Jira research, checks for duplicates and project conventions, decomposes the scope, and presents a review-ready backlog.

### L2 escalation or production defect

The skill reads the existing defect and evidence, researches expected behavior and related issues, proposes classification and priority, and preserves **Product defect - CAPA required at closure**. It never invents root cause or CAPA findings.

## Human review and Jira safety

Drafting and refinement are Jira read-only. The default statuses are:

- **Draft - Pending Product Manager Review**
- **Jira Publication Status: Not Published**

Jira writes require both:

1. Explicit human approval or finalization of the specific backlog.
2. A separate explicit request to create or publish that finalized backlog in Jira.

Approval by itself is not publication permission. Before writing, the skill discovers the target project's actual fields and hierarchy, rechecks duplicates, and shows a publication preview. It does not automatically transition issues, assign a sprint, or complete CAPA.

## Example invocations

Invocation syntax depends on the client. In clients that expose skills as slash commands, prompts may look like:

```text
/create-product-backlog

Convert the attached signed-off BRD into a proposed product backlog.
Do not create Jira issues yet.
```

```text
/create-product-backlog

Review production defect AMRIT-123, classify it, propose priority and required follow-up work.
Do not modify Jira.
```

```text
/create-product-backlog

The backlog is approved and finalized.
Create the approved tickets in Jira project AMRIT.
```

Slash-command availability is client-dependent; selecting the installed skill and using the same natural-language request is equivalent.

## Package as a ZIP

From the repository's `amrit-sdlc-skills` directory in PowerShell:

```powershell
python .\scripts\package-skill.py create-product-backlog
```

The ZIP must contain one top-level `create-product-backlog` folder with `SKILL.md` directly inside it. Do not add repository-level files or external dependencies.

## Install in Claude Desktop

1. Download `create-product-backlog.zip`.
2. Open Claude Desktop's **Add Skills** flow.
3. Select and upload `create-product-backlog.zip`.
4. Confirm that the skill appears in Claude Desktop.
5. Ensure the organization-managed Atlassian MCP is already connected before using Confluence or Jira operations.

Claude Desktop requires a supported skill file such as `.zip`, `.skill`, or `.md`. Upload the ZIP directly; do not select the extracted folder.

Exact menu labels may vary by Claude Desktop version. Do not add Atlassian credentials, URLs, or configuration to the skill package.
