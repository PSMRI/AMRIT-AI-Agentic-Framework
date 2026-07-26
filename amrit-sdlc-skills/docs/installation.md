# Installation

## Install from the complete repository

1. Clone the repository or download its archive.
2. Locate `skills/create-brd`, `skills/create-product-backlog`, or `skills/create-technical-design`.
3. In Claude Desktop, open the Add Skills flow and select the required skill folder.
4. Confirm the skill appears and the Atlassian MCP connection is available.

## Download only one skill

Download or export only the required folder from `skills/` while preserving its contents. Each folder is independently installable and has no mandatory dependency on repository-level files or another skill.

The required Stage 01 layout is:

```text
create-brd/
|- SKILL.md
|- README.md
|- references/
`- examples/
```

The Stage 02 skill uses the same convention:

```text
create-product-backlog/
|- SKILL.md
|- README.md
|- references/
`- examples/
```

The Stage 03 skill uses the same convention:

```text
create-technical-design/
|- SKILL.md
|- README.md
|- references/
`- examples/
```

`SKILL.md` must be directly inside the installed folder. A duplicated nested folder is incorrect.

The Claude Desktop Add Skills interface is the preferred installation method. It may accept a ZIP directly; otherwise extract the archive and select its top-level skill folder. Exact menu labels and local skill-directory paths may vary by client version and operating system.

## Package a skill

From the `amrit-sdlc-skills` directory in PowerShell:

```powershell
python .\scripts\package-skill.py create-technical-design
```

The resulting ZIP contains one top-level folder named for the selected skill and no dependency on the rest of the repository.

## Atlassian MCP prerequisite

Before using a skill, confirm in Claude Desktop's connectors or tool availability that the organization-managed Atlassian MCP is connected:

- `create-brd` requires equivalent Confluence search and page-read capabilities.
- `create-product-backlog` requires Confluence and Jira read capabilities for research. Jira write capabilities are needed only for explicitly approved publication.
- `create-technical-design` requires Confluence and Jira read capabilities, relevant Swagger/OpenAPI evidence, and access to current architecture or repository evidence. It never uses Jira or Confluence write operations.

Exact MCP setup and hosting are managed externally and are not stored in this repository. If required research is unavailable, the skill reports the limitation and asks whether to retry or proceed with a source-limited draft; it never pretends research succeeded.

Credentials, tokens, passwords, and MCP URLs must not be added to this repository or a skill folder.
