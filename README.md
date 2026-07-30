# AMRIT SDLC Skills

This repository contains reusable Claude skills for the AMRIT software
development lifecycle. The source of truth is [`skills/`](skills/); project
discovery and release packages are generated from those same source
directories.

[Download the latest skill packages](../../releases/latest)

## Available skills

| Skill | Invocation | Lifecycle stage | What it produces |
| --- | --- | --- | --- |
| [`create-brd`](skills/create-brd/README.md) | `/create-brd` | Stage 01/12 — Business & Product | A traceable AMRIT BRD labelled **Draft — Pending Human Review** after mandatory read-only Confluence research. |
| [`create-product-backlog`](skills/create-product-backlog/README.md) | `/create-product-backlog` | Stage 02 — Product Backlog Creation | A review-ready backlog from an approved BRD/FRD or L2-escalated production defect, labelled **Draft - Pending Product Manager Review**. |
| [`create-technical-design`](skills/create-technical-design/README.md) | `/create-technical-design` | Stage 03 — Engineering Analysis | One evidence-based technical design package labelled **Ready for Architect Review**. |

The skills are independent. A downstream skill can consume an approved
upstream output without requiring the upstream skill at runtime.

## Claude Code: use the project skills immediately

Developers can clone the repository and start Claude Code from its root:

```bash
git clone https://github.com/PSMRI/AMRIT-AI-Agentic-Framework.git
cd AMRIT-AI-Agentic-Framework
claude
```

No project-level installation command is required. Claude Code discovers
project skills under `.claude/skills/`. Each project skill is a small,
Windows-safe `SKILL.md` bridge that loads its canonical implementation from
`skills/`:

```text
.claude/skills/create-brd/SKILL.md
    -> skills/create-brd/SKILL.md
.claude/skills/create-product-backlog/SKILL.md
    -> skills/create-product-backlog/SKILL.md
.claude/skills/create-technical-design/SKILL.md
    -> skills/create-technical-design/SKILL.md
```

Invoke a skill directly with `/create-brd`, `/create-product-backlog`, or
`/create-technical-design`. Claude may also load a skill automatically when a
request matches its description.

## Claude Desktop: download a release ZIP

Claude Desktop users do not need to clone the repository:

1. Open [the latest GitHub Release](../../releases/latest).
2. Download the ZIP for the desired skill.
3. Open Claude Desktop's skill interface.
4. Upload the downloaded ZIP.
5. Confirm that the skill and any required MCP connections are available.

Direct downloads:

- [Download Create BRD](../../releases/latest/download/create-brd.zip)
- [Download Create Product Backlog](../../releases/latest/download/create-product-backlog.zip)
- [Download Create Technical Design](../../releases/latest/download/create-technical-design.zip)

Each ZIP contains one top-level skill directory with `SKILL.md` and all of that
skill's references, examples, templates, scripts, and assets.

## Distribution architecture

```text
skills/                         Canonical source; edit skills here
├── create-brd/
├── create-product-backlog/
└── create-technical-design/

.claude/skills/                 Small project bridges to canonical skills/
scripts/package-skills.py       Deterministic ZIP packaging into dist/
scripts/validate-skills.py      Release and project-discovery checks
.github/workflows/
├── validate-skills.yml         PR/main validation and temporary artifacts
└── release-skills.yml          Tagged GitHub Release assets
```

Generated `dist/` content and all ZIP files are ignored by Git. GitHub Actions
creates packages from `skills/`; short-lived validation artifacts are for
maintainer inspection, while GitHub Releases are the permanent download
location for Claude Desktop users.

## Maintainer workflow

Run the complete local checks from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/validate-skills.py
python scripts/package-skills.py --all
```

Package one skill when needed:

```bash
python scripts/package-skills.py create-brd
```

Packages are written to ignored `dist/`.

When adding a new `skills/<name>/` source directory, also add the corresponding
small `.claude/skills/<name>/SKILL.md` bridge. Validation fails if a source or
bridge is missing; packaging discovers valid source directories automatically.

To publish a release, create and push a version tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The tag triggers tests, validation, packaging, GitHub Release creation (or
update), generated release notes for a new release, and upload of every skill
ZIP. The release workflow can also be started manually for an existing `v*`
tag.

## MCP requirements and guardrails

MCP services are externally managed; this repository stores no endpoints,
credentials, tokens, or secrets.

- `create-brd` requires connected Atlassian MCP Confluence search and page-read
  capabilities. Confluence is read-only by default.
- `create-product-backlog` requires connected Atlassian MCP Confluence and Jira
  read capabilities. Jira publication is optional and requires approval of the
  specific backlog plus a separate explicit publication request.
- `create-technical-design` requires relevant Jira, Confluence, architecture,
  and Swagger/OpenAPI evidence. Official DeepWiki MCP repository research is
  optional and read-only.

All outputs require human review. No skill automatically approves or publishes
content, and `create-technical-design` never modifies Jira, Confluence,
repositories, or implementation files.

See the [lifecycle mapping](docs/lifecycle-mapping.md) for inputs, outputs, and
review gates.
