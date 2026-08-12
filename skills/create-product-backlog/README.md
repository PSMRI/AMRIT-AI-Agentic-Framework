# create-product-backlog

`create-product-backlog` supports AMRIT Product Managers at Stage 02 — Product Backlog Creation. It converts approved feature requirements or an L2-escalated production defect into a traceable, prioritized backlog draft.

## Intended users

The primary user and required reviewer is the Product Manager.

## Inputs

The feature path requires one of:

- a signed-off BRD or FRD;
- an approved Confluence requirement page;
- an uploaded approved requirement document.

The defect path accepts an L2-escalated bug, an existing Jira production defect, or supporting incident evidence. It does not require a BRD or FRD.

## Required MCP capability

An Atlassian MCP connection must provide relevant Confluence and Jira search and read capabilities. A cloned repository supplies the project-scoped server definition through `.mcp.json` for Claude Code, `.cursor/mcp.json` for Cursor, and `.agents/mcp_config.json` for Antigravity. These files intentionally contain the same `mcpServers` definitions at client-specific discovery paths. The skill uses these capabilities to retrieve source material, check related work and possible duplicates, and discover actual Jira hierarchy, fields, and project conventions.

Jira write capabilities are optional and used only for an explicitly authorized publication. No DeepWiki integration is required.

## Output

The default output is a Markdown backlog labelled:

- **Draft - Pending Product Manager Review**
- **Jira Publication Status: Not Published**

It may contain Epics, Stories, Tasks, or Subtasks with testable acceptance criteria, an INVEST review for each Story, priority rationale, source traceability, dependencies, risks, possible duplicates, and fields needing confirmation.

For a production defect, the skill preserves **Product defect - CAPA required at closure** and never invents root cause or CAPA findings.

## Human review and Jira guardrails

Drafting and refinement are Jira read-only. Jira publication requires both:

1. Explicit human approval or finalization of the specific backlog version.
2. A separate explicit request to create or publish that finalized backlog in Jira.

Approval alone is not publication permission. Before writing, the skill rechecks duplicates, discovers the target project's current fields and hierarchy, and shows a publication preview. It does not automatically transition issues, assign a sprint, replace a production-defect priority, or complete CAPA.

## Use and distribution

Invoke `/create-product-backlog` from the repository root using a supported
coding agent. After cloning, replace the token placeholders only in the
relevant local MCP file, open the repository in the chosen client, reload or
restart if required, and approve or trust the servers when prompted. Tokens
are not preconfigured. Never commit real Jira, Confluence, or OpenProject
tokens; confirm local credential changes are not staged or committed.

Claude Desktop does not use the repository MCP files and requires its own
user-level connector or configuration setup. Do not copy Claude Desktop-only
fields such as `coworkUserFilesPath` or `preferences` into repository MCP
files.

For a packaged installation, open the repository on GitHub, open
the **Actions** tab, select the latest successful
**Validate and package skills** workflow run on `main`, scroll to
**Artifacts**, and download `create-product-backlog.zip` directly. Upload or
install that ZIP using the relevant client workflow. It is the actual skill
package, so no additional archive extraction is required. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
