# Installation

This repository supports two installation flows:

- **Claude Code:** copy skills into user scope or project scope with `scripts/install-skill.py`.
- **Claude Desktop:** upload an individual ZIP from `skill-zips/` through the **Add Skills** interface.

Each skill is self-contained and can be installed without the other skills.

## Claude Code

Run all commands from the repository root.

### List available skills

```bash
python scripts/install-skill.py --list
```

The current skills are:

- `create-brd`
- `create-product-backlog`
- `create-technical-design`

### User scope

User scope is the default. Installed skills are available across projects at:

```text
~/.claude/skills/<skill-name>
```

Install one skill:

```bash
python scripts/install-skill.py create-brd
```

Install all skills:

```bash
python scripts/install-skill.py --all
```

Upgrade one skill or all skills by replacing the installed copy:

```bash
python scripts/install-skill.py create-brd --upgrade
python scripts/install-skill.py --all --upgrade
```

Uninstall one skill:

```bash
python scripts/install-skill.py --uninstall create-brd
```

`--force` is supported as a backward-compatible alias for `--upgrade`.

### Project scope

Project-scoped skills are available only within the target repository and are installed at:

```text
<repository>/.claude/skills/<skill-name>
```

When these commands are run from the repository root, that repository is the default project target.

Install one skill or all skills for the current project:

```bash
python scripts/install-skill.py create-brd --scope project
python scripts/install-skill.py --all --scope project
```

Upgrade project-scoped skills:

```bash
python scripts/install-skill.py create-brd --scope project --upgrade
python scripts/install-skill.py --all --scope project --upgrade
```

Uninstall one project-scoped skill:

```bash
python scripts/install-skill.py --uninstall create-brd --scope project
```

To target a different project directory, add `--project-path <path>` together with `--scope project`.

### PowerShell path style

The same commands can use PowerShell-style relative paths:

```powershell
python .\scripts\install-skill.py --list
python .\scripts\install-skill.py create-brd
python .\scripts\install-skill.py --all --scope project
```

### Use the installed skills

Invoke an installed skill in Claude Code with its slash command:

```text
/create-brd
/create-product-backlog
/create-technical-design
```

Keep the installed folder intact. `SKILL.md` must remain directly inside `<skill-name>/`.

## Claude Desktop

Current skill packages are:

- [`skill-zips/create-brd.zip`](../skill-zips/create-brd.zip)
- [`skill-zips/create-product-backlog.zip`](../skill-zips/create-product-backlog.zip)
- [`skill-zips/create-technical-design.zip`](../skill-zips/create-technical-design.zip)

Install one package:

1. Download the required skill ZIP.
2. Open Claude Desktop.
3. Open the **Add Skills** interface.
4. Upload the selected ZIP.
5. Confirm that the skill appears and that its required MCP connections are available.

The ZIP is the primary installation artifact for Claude Desktop. Cloning the repository or copying an extracted skill folder is an optional developer workflow, not a normal installation requirement.

Each package contains this structure:

```text
<skill-name>/
├── SKILL.md
├── README.md
├── references/
└── examples/
```

## Package a skill

Run the packaging command from the repository root:

```bash
python scripts/package-skill.py create-brd
```

PowerShell equivalent:

```powershell
python .\scripts\package-skill.py create-brd
```

The command writes:

```text
skill-zips/create-brd.zip
```

Substitute `create-product-backlog` or `create-technical-design` to package either of those skills. The script packages exactly one named skill per invocation and has no all-skills option.

## MCP prerequisites

MCP connections and credentials are configured outside this repository.

- `create-brd` requires Atlassian MCP Confluence search and page-read capabilities. It treats Confluence as read-only unless the user explicitly requests publication after reviewing the draft.
- `create-product-backlog` requires Atlassian MCP Confluence and Jira read capabilities. Jira write capabilities are needed only for an explicitly approved and separately requested publication.
- `create-technical-design` requires Jira and Confluence read capabilities plus applicable architecture and Swagger/OpenAPI evidence. Official DeepWiki MCP repository research is optional. The skill uses read operations only and never publishes a design.

If required research is unavailable, the skill reports the limitation rather than pretending that research succeeded. Never add credentials, tokens, passwords, private MCP URLs, or environment-specific configuration to a skill package.

For skill behavior and review gates, see the [lifecycle mapping](lifecycle-mapping.md).
