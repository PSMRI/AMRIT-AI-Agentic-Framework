# Installation and distribution

The repository supports two primary audiences:

- **Coding-agent users** use the committed project skills immediately after
  cloning.
- **Skill-package users** download prebuilt ZIP files from GitHub Actions
  artifacts.

Every complete implementation lives only under `skills/`, which is the
canonical source.

## Project use

Clone the repository and launch a supported coding agent from its root:

```bash
git clone https://github.com/PSMRI/AMRIT-AI-Agentic-Framework.git
cd AMRIT-AI-Agentic-Framework
claude
```

There is no project installation step. Claude Code discovers:

```text
.claude/skills/<skill-name>/SKILL.md
```

Each `.claude/skills/<skill-name>/SKILL.md` is a small project bridge that
loads the canonical implementation from `skills/<skill-name>/SKILL.md`.

Cursor and Antigravity use the equivalent project bridges at:

```text
.agents/skills/<skill-name>/SKILL.md
```

Both bridge locations defer to the same authoritative canonical skill and
resolve references, examples, templates, scripts, and assets from its
`skills/<skill-name>/` directory. The bridges are ordinary directories and
files, so a normal Windows, Linux, or macOS clone does not require symbolic-link
configuration.

The available project skills are:

- `/create-brd`
- `/create-product-backlog`
- `/create-technical-design`
- `/implement-jira-ticket`
- `/create-development-pr`
- `/answer-codebase-questions`

## Project-scoped MCP setup

The cloned repository already contains project-level MCP configuration for the
three supported coding clients:

| Client | Project configuration |
| --- | --- |
| Claude Code | [`.mcp.json`](../.mcp.json) |
| Cursor | [`.cursor/mcp.json`](../.cursor/mcp.json) |
| Antigravity | [`.agents/mcp_config.json`](../.agents/mcp_config.json) |

All three files intentionally contain the same `mcpServers` definitions. The
copies live at different paths because each client expects project
configuration in a different location; users do not need to recreate the
server list in a global configuration.

To connect the project:

1. Clone the repository.
2. In the MCP file for the chosen client, replace each applicable
   `<put your token here>` placeholder with the user's Jira, Confluence, or
   OpenProject token.
3. Open the repository root in Claude Code, Cursor, or Antigravity.
4. Reload or restart the client if required for it to discover the project
   configuration.
5. Approve or trust the MCP servers when prompted by the client.

The committed files contain token placeholders, not configured credentials.
Never commit real Jira, Confluence, or OpenProject tokens. Replace placeholders
only in the local working copy, and confirm that accidental credential changes
are not staged or committed before sharing or pushing changes.

### Claude Desktop

Claude Desktop does not read the repository-scoped files above. It requires
its own user-level connector or configuration setup. Do not copy
Claude Desktop-only fields such as `coworkUserFilesPath` or `preferences` into
`.mcp.json`, `.cursor/mcp.json`, or `.agents/mcp_config.json`.

The repository-level MCP files are also not bundled inside the standalone skill
ZIP artifacts. A packaged-skill user must use the MCP setup supported by the
client where the package is installed; for Claude Desktop, that is the
user-level setup described above.

## Install packaged skills

Each generated ZIP is published as an individual GitHub Actions artifact:

1. Open the repository on GitHub.
2. Open the **Actions** tab.
3. Select the latest successful **Validate and package skills** workflow run on
   `main`.
4. Scroll to the **Artifacts** section.
5. Download the required skill ZIP directly:
   - `create-brd.zip`
   - `create-product-backlog.zip`
   - `create-technical-design.zip`
   - `implement-jira-ticket.zip`
   - `create-development-pr.zip`
   - `answer-codebase-questions.zip`
6. Upload or install that ZIP using the relevant client workflow.

The ZIPs are separate artifacts. There is no combined artifact, and no
additional archive extraction is required. The ZIP downloaded from GitHub
Actions is the actual skill package. Claude Desktop users can upload that ZIP
directly through the skill interface, but must configure the required
user-level connectors separately because Claude Desktop does not read the
repository-scoped MCP files.

Each package has exactly one top-level skill directory:

```text
<skill-name>/
├── SKILL.md
├── README.md
├── references/
└── examples/
```

Other source subdirectories such as templates, scripts, or assets are included
when a skill contains them.

## Local validation and packaging

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/validate-skills.py
python scripts/package-skills.py --all
```

Package only one skill:

```bash
python scripts/package-skills.py create-brd
```

Generated files are written to `dist/`. The directory and all ZIP files are
ignored by Git.

Validation checks that each source skill has `SKILL.md`, every source has valid
bridges under both `.claude/skills/` and `.agents/skills/`, every bridge
resolves to its canonical skill, packaging succeeds with one top-level skill
directory per ZIP, and generated ZIPs are not tracked.

## Maintainer distribution workflow

1. Update the canonical skills under `skills/`.
2. Merge the changes into `main`.
3. The **Validate and package skills** workflow runs automatically and
   packages and publishes the individual ZIP artifacts.
4. A maintainer may also manually run the workflow against `main`.

The workflow runs tests, validates canonical skills and both bridge locations,
packages every canonical skill, and confirms all expected ZIPs exist. Pushes to
`main` and manual workflow runs publish the individual ZIP artifacts. Pull
requests perform all validation and packaging checks but do not publish
downloadable artifacts. Maintainers only need to merge canonical skill changes
into `main`; no release or version tag is required. GitHub Releases and version
tags are not currently used.

## MCP prerequisites

For cloned-project use, the repository-provided MCP files define the
connections for Claude Code, Cursor, and Antigravity. Users supply only their
local token values and complete any client trust prompt as described in
[Project-scoped MCP setup](#project-scoped-mcp-setup).

- `create-brd` requires Atlassian MCP Confluence search and page-read
  capabilities.
- `create-product-backlog` requires Atlassian MCP Confluence and Jira read
  capabilities. Jira writes are only for a separately requested, explicitly
  approved publication.
- `create-technical-design` requires Jira and Confluence reads plus applicable
  architecture and Swagger/OpenAPI evidence. Official DeepWiki MCP repository
  research is optional.
- `implement-jira-ticket` requires Jira and Confluence reads, DeepWiki
  repository research, and the host's repository-editing and command-execution
  capabilities. It writes only to source files, never to Jira or Confluence, and
  does not require Graphify.
- `create-development-pr` requires Jira reads, local Git and repository access
  through the host's command execution, and a GitHub capability for remote
  branch inspection, Pull Request lookup, Pull Request creation, and check
  status where available. It never writes to Jira and does not require
  Confluence, DeepWiki, or Graphify. GitHub write access is **not** provided by
  the project-scoped MCP files; supply it through the host, such as a connected
  GitHub capability or an authenticated GitHub CLI in the local environment.
  Without it the skill performs safe local preparation only, fabricates no PR
  URL, and reports that PR creation could not be completed.
- `answer-codebase-questions` uses read-only DeepWiki first, then Confluence
  when needed, with Graphify as the final fallback. It never uses Jira.

Never add credentials, tokens, passwords, private MCP URLs, or
environment-specific configuration to a skill package. Never stage or commit
real Jira, Confluence, or OpenProject tokens from a local project MCP file.

For skill behavior and review gates, see the
[lifecycle mapping](lifecycle-mapping.md).
