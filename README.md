# AMRIT SDLC Skills

This repository contains reusable agent skills for the AMRIT software
development lifecycle. The source of truth is [`skills/`](skills/); project
discovery bridges and installable packages are generated from those same
source directories.

[Download skill packages from the latest GitHub Release](../../releases/latest)

## Available skills

| Skill | Invocation | Lifecycle stage | What it produces |
| --- | --- | --- | --- |
| [`create-brd`](skills/create-brd/README.md) | `/create-brd` | Stage 01/12 — Business & Product | A traceable AMRIT BRD labelled **Draft — Pending Human Review** after mandatory read-only Confluence research. |
| [`create-product-backlog`](skills/create-product-backlog/README.md) | `/create-product-backlog` | Stage 02 — Product Backlog Creation | A review-ready backlog from an approved BRD/FRD or L2-escalated production defect, labelled **Draft - Pending Product Manager Review**. |
| [`create-technical-design`](skills/create-technical-design/README.md) | `/create-technical-design` | Stage 03 — Engineering Analysis | One evidence-based technical design package labelled **Ready for Architect Review**. |
| [`implement-jira-ticket`](skills/implement-jira-ticket/README.md) | `/implement-jira-ticket` | Stage 04 — In Development | Implemented and locally verified code with unit tests, with any schema change placed in `AMRIT-DB`, ready for PR preparation. |
| [`create-development-pr`](skills/create-development-pr/README.md) | `/create-development-pr` | Stage 04 — In Development | A GitHub Pull Request for an implemented Jira ticket, from a Jira-named branch against the correct `release-X.Y.Z` branch, labelled **Awaiting code review**. |
| [`answer-codebase-questions`](skills/answer-codebase-questions/README.md) | `/answer-codebase-questions` | Cross-lifecycle — Codebase knowledge | A concise, evidence-backed AMRIT codebase answer from DeepWiki, Confluence, and Graphify; never Jira. |

`implement-jira-ticket` is the implementation and source-editing skill.
`create-development-pr` performs Git and GitHub write operations — branch,
commit, push, and Pull Request creation — but no substantive implementation. The
other three skills are read-only.

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

Both bridge locations contain every available skill:

```text
<bridge-root>/create-brd/SKILL.md
    -> skills/create-brd/SKILL.md
<bridge-root>/create-product-backlog/SKILL.md
    -> skills/create-product-backlog/SKILL.md
<bridge-root>/create-technical-design/SKILL.md
    -> skills/create-technical-design/SKILL.md
<bridge-root>/implement-jira-ticket/SKILL.md
    -> skills/implement-jira-ticket/SKILL.md
<bridge-root>/create-development-pr/SKILL.md
    -> skills/create-development-pr/SKILL.md
<bridge-root>/answer-codebase-questions/SKILL.md
    -> skills/answer-codebase-questions/SKILL.md
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

## Install skill packages from GitHub Releases

GitHub Releases are the official distribution channel. To install a skill:

1. Open the repository on GitHub.
2. Open the **Releases** page and select the latest release, named
   **AMRIT SDLC Skills vX.Y.Z**.
3. Open its **Assets** section.
4. Download the required skill ZIP directly:
   - `create-brd.zip`
   - `create-product-backlog.zip`
   - `create-technical-design.zip`
   - `implement-jira-ticket.zip`
   - `create-development-pr.zip`
   - `answer-codebase-questions.zip`
5. Upload or install that ZIP using the relevant client workflow.

Every release contains all currently packaged skills as individual assets, so
the asset list above grows automatically as skills are added. The packages are
separate assets, not a combined archive, and no additional extraction is
required: the ZIP downloaded from the release is the actual skill package. Each
ZIP contains one top-level skill directory with `SKILL.md` and all of that
skill's references, examples, templates, scripts, and assets.

GitHub Actions artifacts from the **Validate and package skills** workflow
remain available for CI inspection and debugging. They are not the installation
path; ordinary users should always install from a release.

## Distribution architecture

```text
skills/                         Canonical source; edit skills here
├── create-brd/
├── create-product-backlog/
├── create-technical-design/
├── implement-jira-ticket/
├── create-development-pr/
└── answer-codebase-questions/

.claude/skills/                 Claude project bridges
.agents/skills/                 Cursor and Antigravity project bridges
scripts/package-skills.py       Deterministic ZIP packaging into dist/
scripts/validate-skills.py      Packaging and project-discovery checks
scripts/next-release-version.py Next vX.Y.Z tag from .release-version and tags
.release-version                Manually controlled X.Y release line
.github/workflows/
├── validate-skills.yml         PR/main validation and CI build artifacts
└── release-skills.yml          Official GitHub Release publication from main
```

Generated `dist/` content and all ZIP files are ignored by Git; release assets
are build outputs, never repository sources. Official, stable distribution is
GitHub Releases. GitHub Actions artifacts are retained only for CI and build
debugging.

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

Check the next release tag the workflow would choose, using the local tags:

```bash
python scripts/next-release-version.py
```

To distribute updates:

1. Update the canonical skills under `skills/`.
2. Merge the changes into `main`.
3. The **Release Skills** workflow runs automatically, verifies the repository,
   packages every skill, and publishes one GitHub Release whose assets are the
   individual skill ZIPs.

Every successful merge to `main` automatically creates a patch release. A
change that reaches `main` is considered release-worthy, so `main` always
represents the latest officially distributable state of the skills.

Pull requests run the **Validate and package skills** workflow only: the same
tests, validation, packaging, and package-existence checks, with no release and
no tag. That workflow also continues to upload Actions artifacts on `main` and
on manual runs for CI and build inspection.

## Release versioning

Releases are tagged `vX.Y.Z`:

- `X.Y` is human-controlled in [`.release-version`](.release-version).
- `Z` is automatic, one above the highest existing `vX.Y.Z` tag on that release
  line, or `0` when the line has no tags yet.
- Git tags are the source of truth for `Z`. No patch number is stored in
  `.release-version` and no version bump is ever committed back to the
  repository.
- Release lines are never inferred from commit messages, PR labels,
  Conventional Commits, or semantic-release rules.

With `.release-version` set to `1.2`, consecutive merges to `main` produce:

```text
merge 1 → v1.2.0
merge 2 → v1.2.1
merge 3 → v1.2.2
```

To deliberately move the minor line, a maintainer edits `.release-version`:

```diff
-1.2
+1.3
```

Once that change reaches `main`, the next release is `v1.3.0`, then `v1.3.1`,
`v1.3.2`, and so on. Moving `1.9` to `2.0` likewise makes the next release
`v2.0.0`. Change this file only when deliberately moving the major/minor
release line.

The release workflow runs tests, validation, and packaging **before** it
calculates a version or creates anything. A failed run publishes no tag, no
release, and no assets; the failed run stays visible in GitHub Actions so
maintainers can repair the problem and re-run. A failed release means
publication failed — not that the commit should be skipped. Releases are
always traceable to the commit SHA that triggered them, and the workflow never
moves, overwrites, or deletes an existing tag or release.

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
- `implement-jira-ticket` requires read-only Jira and Confluence capabilities,
  DeepWiki repository research, and the host's repository-editing and
  command-execution capabilities. Jira and Confluence are never written to, and
  Graphify is not required.
- `create-development-pr` requires a read-only Jira capability, local Git and
  repository access through the host, and a GitHub capability for remote branch
  inspection, Pull Request lookup, Pull Request creation, and check status where
  available. Jira is never written to. Confluence, DeepWiki, and Graphify are not
  required. GitHub write access is not part of the project-scoped MCP files
  above; it comes from the host, such as a connected GitHub capability or an
  authenticated GitHub CLI. Without it the skill performs safe local preparation
  only and reports that PR creation could not be completed.
- `answer-codebase-questions` uses read-only DeepWiki first, then Confluence
  when needed, with Graphify as the final fallback. It never uses Jira.

All outputs require human review. No skill automatically approves or publishes
content, and `create-technical-design` never modifies Jira, Confluence,
repositories, or implementation files.

`implement-jira-ticket` edits source files by design. It still never writes to
Jira or Confluence, never creates a branch, commit, push, or Pull Request, and
never claims code-review sign-off; those operations belong to the downstream
`create-development-pr` skill.

`create-development-pr` creates branches, commits, pushes, and Pull Requests by
design. It still never writes to Jira, never implements missing functionality,
never stages unrelated user work or secrets, never pushes to a protected branch,
and never approves, merges, or squash-merges a Pull Request or claims
code-review sign-off or green CI it did not observe. The two Stage 04 skills are
independently installable; neither requires the other at runtime.

See the [lifecycle mapping](docs/lifecycle-mapping.md) for inputs, outputs, and
review gates.
