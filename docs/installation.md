# Installation and distribution

The repository supports two primary audiences:

- **Claude Code developers** use the committed project skills immediately
  after cloning.
- **Claude Desktop users** download prebuilt ZIP files from GitHub Releases.

Every complete implementation lives only under `skills/`.

## Claude Code project use

Clone the repository and launch Claude Code from its root:

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
loads the canonical implementation from `skills/<skill-name>/SKILL.md`. These
are ordinary directories and files, so a normal Windows, Linux, or macOS clone
does not require symbolic-link configuration.

The available project skills are:

- `/create-brd`
- `/create-product-backlog`
- `/create-technical-design`

## Claude Desktop

[Download the latest skill packages](../../releases/latest)

Install one package:

1. Open the repository's latest GitHub Release.
2. Download the ZIP for the desired skill.
3. Open Claude Desktop.
4. Open the skill interface and upload the ZIP.
5. Confirm that the skill appears and its required MCP connections are
   available.

Direct release assets:

- [Create BRD](../../releases/latest/download/create-brd.zip)
- [Create Product Backlog](../../releases/latest/download/create-product-backlog.zip)
- [Create Technical Design](../../releases/latest/download/create-technical-design.zip)

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

Validation checks that each source skill has `SKILL.md`, every project bridge
resolves to its canonical skill, packaging succeeds with one top-level skill
directory per ZIP, and generated ZIPs are not tracked.

## Publishing a release

Create and push a tag following the `v*` convention:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The release workflow checks out that exact tag, runs tests and validation,
packages every skill, creates or updates the corresponding GitHub Release, and
uploads all ZIP assets. New releases receive generated release notes.

The validation workflow runs separately for pull requests, pushes to `main`,
and manual dispatch. Its uploaded packages are temporary inspection artifacts,
not the permanent user download location.

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
