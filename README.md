# AMRIT SDLC Skills

This repository contains reusable agent skills for the AMRIT software
development lifecycle. The source of truth is [`skills/`](skills/); project
discovery bridges and installable packages are generated from those same
source directories.

[Download skill packages from GitHub Actions](../../actions/workflows/validate-skills.yml)

## Available skills

| Skill | Invocation | Lifecycle stage | What it produces |
| --- | --- | --- | --- |
| [`create-brd`](skills/create-brd/README.md) | `/create-brd` | Stage 01/12 — Business & Product | A traceable AMRIT BRD labelled **Draft — Pending Human Review** after mandatory read-only Confluence research. |
| [`create-product-backlog`](skills/create-product-backlog/README.md) | `/create-product-backlog` | Stage 02 — Product Backlog Creation | A review-ready backlog from an approved BRD/FRD or L2-escalated production defect, labelled **Draft - Pending Product Manager Review**. |
| [`create-technical-design`](skills/create-technical-design/README.md) | `/create-technical-design` | Stage 03 — Engineering Analysis | One evidence-based technical design package labelled **Ready for Architect Review**. |

The skills are independent. A downstream skill can consume an approved
upstream output without requiring the upstream skill at runtime.

## Project use: discover skills immediately

Developers can clone the repository and use a supported coding agent from its
root:

```bash
git clone https://github.com/PSMRI/AMRIT-AI-Agentic-Framework.git
cd AMRIT-AI-Agentic-Framework
```

No project-level installation command is required. Claude Code discovers
project skills under `.claude/skills/`. Cursor and Antigravity discover project
skills under `.agents/skills/`. Each project skill is a small, Windows-safe
`SKILL.md` bridge that loads its canonical implementation from `skills/`.

Both bridge locations contain all three skills:

```text
<bridge-root>/create-brd/SKILL.md
    -> skills/create-brd/SKILL.md
<bridge-root>/create-product-backlog/SKILL.md
    -> skills/create-product-backlog/SKILL.md
<bridge-root>/create-technical-design/SKILL.md
    -> skills/create-technical-design/SKILL.md
```

Invoke a skill using the supported client workflow. Clients may also load a
skill automatically when a request matches its description.

### Project-scoped MCP setup

The repository includes project-scoped MCP configuration for every supported
coding client:

| Client | Project configuration |
| --- | --- |
| Claude Code | [`.mcp.json`](.mcp.json) |
| Cursor | [`.cursor/mcp.json`](.cursor/mcp.json) |
| Antigravity | [`.agents/mcp_config.json`](.agents/mcp_config.json) |

These files intentionally contain the same `mcpServers` definitions. They are
stored at different paths only because each client discovers project MCP
configuration at a different location.

After cloning:

1. Open the MCP file for the client you intend to use.
2. Replace each applicable `<put your token here>` placeholder in your local
   working copy with your Jira, Confluence, or OpenProject token.
3. Open the repository root in Claude Code, Cursor, or Antigravity.
4. Reload or restart the client if it does not detect the configuration
   immediately.
5. Approve or trust the configured MCP servers when the client prompts you.

The committed files contain placeholders; tokens are not preconfigured.
Never commit real Jira, Confluence, or OpenProject tokens. Make credential
changes only in your local working copy, and check that they are not staged or
committed before sharing or pushing changes.

### Obtaining required API tokens

The committed MCP configuration files contain token placeholders. Before using
the Atlassian or OpenProject MCP servers, generate your own personal access
tokens and replace the placeholders in your local working copy.

#### Jira

1. Log in to Jira.
2. Open your account settings.
3. Navigate to **API Tokens** or **Personal Access Tokens**.
4. Create a new token.
5. Copy and securely store the token.
6. Replace the Jira placeholder in your local MCP configuration.

#### Confluence

1. Log in to https://pmp.piramalswasthya.org/confluence.
2. Open your account settings.
3. Navigate to **Personal Access Tokens**.
4. Create a new token.
5. Copy and securely store the token.
6. Replace the Confluence placeholder in your local MCP configuration.

#### OpenProject

1. Log in to https://openproject.piramalswasthya.org/.
2. Click your profile avatar in the upper-right corner.
3. Open **My Account**.
4. Navigate to **Access Tokens** or **API Tokens**.
5. Generate a new API token.
6. Copy and securely store the token.
7. Replace the OpenProject placeholder in your local MCP configuration.

Never commit real tokens to the repository. Keep credentials only in your local
working copy.


Claude Desktop does not use these project-scoped files. It still requires its
own user-level connector or configuration setup. Keep Claude Desktop-only
fields such as `coworkUserFilesPath` and `preferences` out of `.mcp.json`,
`.cursor/mcp.json`, and `.agents/mcp_config.json`.

## Install skill packages from GitHub Actions

Each skill is published as an individual GitHub Actions artifact. To install
one:

1. Open the repository on GitHub.
2. Open the **Actions** tab.
3. Select the latest successful **Validate and package skills** workflow run on
   `main`.
4. Scroll to the **Artifacts** section.
5. Download the required skill ZIP directly:
   - `create-brd.zip`
   - `create-product-backlog.zip`
   - `create-technical-design.zip`
6. Upload or install that ZIP using the relevant client workflow.

The packages are separate artifacts, not a combined artifact. No additional
archive extraction is required: the ZIP downloaded from GitHub Actions is the
actual skill package. Each ZIP contains one top-level skill directory with
`SKILL.md` and all of that skill's references, examples, templates, scripts,
and assets.

## Distribution architecture

```text
skills/                         Canonical source; edit skills here
├── create-brd/
├── create-product-backlog/
└── create-technical-design/

.claude/skills/                 Claude project bridges
.agents/skills/                 Cursor and Antigravity project bridges
scripts/package-skills.py       Deterministic ZIP packaging into dist/
scripts/validate-skills.py      Packaging and project-discovery checks
.github/workflows/
└── validate-skills.yml         PR/main validation and Actions artifacts
```

Generated `dist/` content and all ZIP files are ignored by Git. GitHub Actions
creates packages from `skills/` and publishes each ZIP as an individual
artifact. GitHub Releases and version tags are not currently used.

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

When adding a new `skills/<name>/` source directory, also add corresponding
small bridges at `.claude/skills/<name>/SKILL.md` and
`.agents/skills/<name>/SKILL.md`. Validation fails if a source or either bridge
is missing; packaging discovers valid source directories automatically.

To distribute updates:

1. Update the canonical skills under `skills/`.
2. Merge the changes into `main`.
3. The **Validate and package skills** workflow runs automatically and
   packages and publishes the three individual ZIP artifacts.
4. A maintainer may also run the workflow manually against `main`.

Pushes to `main` and manual workflow runs publish the individual ZIP artifacts.
Pull requests run the same tests, validation, packaging, and package-existence
checks but do not publish downloadable artifacts. Maintainers do not need to
create a release or version tag.

## MCP requirements and guardrails

The project-scoped files described above provide the server definitions and
endpoints needed by Claude Code, Cursor, and Antigravity. Their committed token
values remain placeholders and must be replaced only in each user's local
working copy.

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
