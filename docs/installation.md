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
6. Upload or install that ZIP using the relevant client workflow.

The three ZIPs are separate artifacts. There is no combined artifact, and no
additional archive extraction is required. The ZIP downloaded from GitHub
Actions is the actual skill package. Claude Desktop users can upload that ZIP
directly through the skill interface.

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
   packages and publishes the three individual ZIP artifacts.
4. A maintainer may also manually run the workflow against `main`.

The workflow runs tests, validates canonical skills and both bridge locations,
packages every canonical skill, and confirms all expected ZIPs exist. Pushes to
`main` and manual workflow runs publish the individual ZIP artifacts. Pull
requests perform all validation and packaging checks but do not publish
downloadable artifacts. Maintainers only need to merge canonical skill changes
into `main`; no release or version tag is required. GitHub Releases and version
tags are not currently used.

## MCP prerequisites

MCP connections and credentials are configured outside this repository.

- `create-brd` requires Atlassian MCP Confluence search and page-read
  capabilities.
- `create-product-backlog` requires Atlassian MCP Confluence and Jira read
  capabilities. Jira writes are only for a separately requested, explicitly
  approved publication.
- `create-technical-design` requires Jira and Confluence reads plus applicable
  architecture and Swagger/OpenAPI evidence. Official DeepWiki MCP repository
  research is optional.

Never add credentials, tokens, passwords, private MCP URLs, or
environment-specific configuration to a skill package.

For skill behavior and review gates, see the
[lifecycle mapping](lifecycle-mapping.md).
