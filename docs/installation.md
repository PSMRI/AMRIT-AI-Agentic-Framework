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

Generated ZIP files are distributed through the **skill-packages** GitHub
Actions artifact:

1. Open the GitHub repository.
2. Open the **Actions** tab.
3. Select **Validate and package skills**.
4. Open the latest successful run for `main`.
5. Download the **skill-packages** artifact.
6. Extract the outer artifact archive.
7. Select the required individual skill ZIP.
8. Install or upload that ZIP using the supported client workflow.

The artifact contains:

- `create-brd.zip`
- `create-product-backlog.zip`
- `create-technical-design.zip`

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
   generates updated packages.
4. A maintainer may also manually run the workflow against `main`.

The workflow runs tests, validates canonical skills and both bridge locations,
packages every canonical skill, confirms all expected ZIPs exist, and uploads
`skill-packages` on pushes to `main` and manual runs. Pull requests perform all
validation and packaging checks but do not upload an artifact. GitHub Releases
and version tags are not currently used.

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
