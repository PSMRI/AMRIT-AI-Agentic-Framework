# Installation

## Install from the complete repository

1. Clone the repository with Git or download its archive.
2. Locate `skills/create-brd`.
3. In Claude Desktop, open the Add Skills flow and select the `create-brd` folder.
4. Confirm the skill appears and that the Atlassian MCP connection is available.

## Download only the skill

Download or export only `skills/create-brd` while preserving its contents. The folder is independently installable and has no mandatory dependency on repository-level files.

The required layout is:

```text
create-brd/
├── SKILL.md
├── README.md
├── references/
└── examples/
```

`SKILL.md` must be directly inside the installed folder. This nested layout is incorrect:

```text
create-brd/
└── create-brd/
    └── SKILL.md
```

The Claude Desktop Add Skills interface is the preferred installation method. Exact local skill-directory paths may vary by client version and operating system; do not rely on one hardcoded path.

## Atlassian MCP prerequisite

Before using the skill, confirm in Claude Desktop's connectors or tool availability that the organization-managed Atlassian MCP is connected and exposes equivalent Confluence search and page-read capabilities. Exact MCP setup and hosting are managed externally and are not stored in this repository.

The skill cannot complete mandatory Confluence research when the Atlassian MCP is unavailable. In that case, it must report the failure and ask whether to retry or proceed with a source-limited draft; it must never pretend research succeeded.

Credentials, tokens, passwords, and MCP URLs must not be added to this repository or skill folder.
