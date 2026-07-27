# AMRIT SDLC Skills

This repository contains three independently installable Claude skills for the AMRIT software development lifecycle.

## Available skills

| Skill | Lifecycle stage | What it produces |
| --- | --- | --- |
| [`create-brd`](skills/create-brd/README.md) | Stage 01/12 — Business & Product | A traceable AMRIT BRD labelled **Draft — Pending Human Review** after mandatory read-only Confluence research. |
| [`create-product-backlog`](skills/create-product-backlog/README.md) | Stage 02 — Product Backlog Creation | A review-ready backlog from an approved BRD/FRD or L2-escalated production defect, labelled **Draft - Pending Product Manager Review**. |
| [`create-technical-design`](skills/create-technical-design/README.md) | Stage 03 — Engineering Analysis | One evidence-based technical design package labelled **Ready for Architect Review**. |

The skills remain independently installable. `create-product-backlog` can consume an approved `create-brd` output, and `create-technical-design` can consume approved Stories from `create-product-backlog`, but neither depends on another skill at runtime.

## Repository structure

```text
AMRIT-AI-Agentic-Framework/
├── README.md
├── LICENSE
├── .gitignore
├── skills/
│   ├── create-brd/
│   ├── create-product-backlog/
│   └── create-technical-design/
├── scripts/
│   ├── install-skill.py
│   └── package-skill.py
├── docs/
│   ├── installation.md
│   └── lifecycle-mapping.md
└── skill-zips/
    ├── create-brd.zip
    ├── create-product-backlog.zip
    └── create-technical-design.zip
```

## Install for Claude Code

Run installer commands from the repository root.

List the available skills:

```bash
python scripts/install-skill.py --list
```

Install one skill or all skills at user scope:

```bash
python scripts/install-skill.py create-brd
python scripts/install-skill.py --all
```

Upgrade one installed skill or all installed skills:

```bash
python scripts/install-skill.py create-brd --upgrade
python scripts/install-skill.py --all --upgrade
```

Uninstall one user-scoped skill:

```bash
python scripts/install-skill.py --uninstall create-brd
```

Install for the current project instead:

```bash
python scripts/install-skill.py create-brd --scope project
python scripts/install-skill.py --all --scope project
```

Uninstall a project-scoped skill:

```bash
python scripts/install-skill.py --uninstall create-brd --scope project
```

User-scoped skills are copied to `~/.claude/skills/<skill-name>` and are available across projects. Project-scoped skills are copied to `<repository>/.claude/skills/<skill-name>` and are available only in that repository. With `--scope project`, the current working directory is the target unless `--project-path <path>` is supplied.

`--force` remains supported as a backward-compatible alias for `--upgrade`.

After installation, invoke the skills in Claude Code with:

```text
/create-brd
/create-product-backlog
/create-technical-design
```

See the [installation guide](docs/installation.md) for PowerShell examples and scope details.

## Install in Claude Desktop

Claude Desktop users install one skill package at a time:

1. Download the required ZIP from [`skill-zips/`](skill-zips/).
2. Open Claude Desktop.
3. Open the **Add Skills** interface.
4. Upload `create-brd.zip`, `create-product-backlog.zip`, or `create-technical-design.zip`.

Each archive contains one top-level skill folder with `SKILL.md` directly inside it. For Claude Desktop, cloning the repository is necessary only for development or repackaging, not for normal installation.

## Package a skill

From the repository root, regenerate one package by naming its skill:

```bash
python scripts/package-skill.py create-brd
```

The archive is written to `skill-zips/create-brd.zip`. The packaging script accepts one skill name per invocation; it does not provide an all-skills option.

## MCP requirements and guardrails

MCP services are externally managed; this repository stores no endpoints, credentials, tokens, or secrets.

- `create-brd` requires connected Atlassian MCP Confluence search and page-read capabilities. Confluence is read-only by default.
- `create-product-backlog` requires connected Atlassian MCP Confluence and Jira read capabilities. Jira publication is optional and requires both approval of the specific backlog and a separate explicit publication request.
- `create-technical-design` requires relevant Jira, Confluence, architecture, and Swagger/OpenAPI evidence. Official DeepWiki MCP repository research is optional and read-only.

All outputs require human review. No skill automatically approves or publishes content, and `create-technical-design` never modifies Jira, Confluence, repositories, or implementation files.

See the [lifecycle mapping](docs/lifecycle-mapping.md) for inputs, outputs, and review gates.
