# Installation and distribution

The repository supports two primary audiences:

- **Coding-agent users** use the committed project skills immediately after
  cloning.
- **Skill-package users** download prebuilt ZIP files from the latest GitHub
  Release.

Distribution has one official channel:

```text
Official/stable:            GitHub Releases
CI/debug build artifacts:   GitHub Actions
```

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
- `/review-implementation-architecture`
- `/implement-database-change`
- `/implement-backend-change`
- `/implement-frontend-change`
- `/implement-android-change`
- `/validate-ux-implementation`
- `/write-unit-tests`
- `/create-development-pr`
- `/answer-codebase-questions`

For ordinary Stage 05 work, `/implement-jira-ticket` is the only command
needed: it classifies the impacted personas and routes to the specialists
above. The specialists remain independently invocable for focused work.

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
ZIP packages. A packaged-skill user must use the MCP setup supported by the
client where the package is installed; for Claude Desktop, that is the
user-level setup described above.

## Install packaged skills

Each generated ZIP is published as an individual asset on a GitHub Release:

1. Open the repository on GitHub.
2. Open the **Releases** page and select the latest release, named
   **AMRIT SDLC Skills vX.Y.Z**.
3. Open its **Assets** section.
4. Download the required skill ZIP directly:
   - `create-brd.zip`
   - `create-product-backlog.zip`
   - `create-technical-design.zip`
   - `implement-jira-ticket.zip`
   - `review-implementation-architecture.zip`
   - `implement-database-change.zip`
   - `implement-backend-change.zip`
   - `implement-frontend-change.zip`
   - `implement-android-change.zip`
   - `validate-ux-implementation.zip`
   - `write-unit-tests.zip`
   - `create-development-pr.zip`
   - `answer-codebase-questions.zip`
5. Upload or install that ZIP using the relevant client workflow.

Every release carries all currently packaged skills, so newly added skills
appear as additional assets on the next release without any manual step.

For Stage 05, install `implement-jira-ticket` together with the specialist
packages relevant to the repositories in use. The orchestrator works alone —
it applies a missing persona's contract inline and reports that it did so — but
each installed specialist carries its own guidance and code-inspection
discipline.

The ZIPs are separate assets. There is no combined archive, and no additional
extraction is required. The ZIP downloaded from the release is the actual skill
package. Claude Desktop users can upload that ZIP directly through the skill
interface, but must configure the required user-level connectors separately
because Claude Desktop does not read the repository-scoped MCP files.

GitHub Actions artifacts from the **Validate and package skills** workflow are
kept for CI and build debugging only. Do not use them as an installation
source; install from a GitHub Release.

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

Preview the release tag the workflow would choose next, from the local tags:

```bash
python scripts/next-release-version.py
```

Generated files are written to `dist/`. The directory and all ZIP files are
ignored by Git. Release assets are generated build outputs and are never
committed.

Validation checks that each source skill has `SKILL.md`, every source has valid
bridges under both `.claude/skills/` and `.agents/skills/`, every bridge
resolves to its canonical skill, packaging succeeds with one top-level skill
directory per ZIP, and generated ZIPs are not tracked.

## Maintainer distribution workflow

1. Update the canonical skills under `skills/`.
2. Merge the changes into `main`.
3. The **Release Skills** workflow runs automatically and publishes one GitHub
   Release whose assets are the individual skill ZIPs.

Every successful merge to `main` automatically creates a patch release.
Maintainers do not tag or publish by hand. A change that reaches `main` is
considered release-worthy, so `main` always represents the latest officially
distributable state of the skills.

The **Release Skills** workflow runs on pushes to `main` only — never on pull
requests, feature branches, or tags. It runs the tests, validates canonical
skills and both bridge locations, packages every canonical skill, and verifies
the generated assets *before* it calculates a version or creates anything. It
holds `contents: write` for tag and release creation and uses the built-in
`GITHUB_TOKEN`; no personal access token or repository secret is involved. A
`skill-release` concurrency group serialises publication so two merges cannot
claim the same patch number, and a newer merge waits rather than cancelling an
in-progress release.

Pull requests and manual runs use the separate **Validate and package skills**
workflow, which performs all validation and packaging checks and uploads
Actions artifacts for CI inspection, but never creates a tag or a release.

If any check fails, the run publishes no tag, no release, and no assets. The
failed run stays visible in GitHub Actions for repair and re-run: a failed
release means publication failed, not that the commit should be skipped or that
some unrelated later state should be published in its place. Each release is
traceable to the commit SHA that triggered it, and the workflow never moves,
overwrites, or deletes an existing tag or release.

## Release versioning

Releases are tagged `vX.Y.Z`.

| Component | Controlled by | How it changes |
| --- | --- | --- |
| `X.Y` | Maintainers, in [`.release-version`](../.release-version) | Edited deliberately when moving the release line |
| `Z` | Automatic | One above the highest existing `vX.Y.Z` tag on that line, or `0` for a new line |

`.release-version` holds only the `X.Y` release line, never a patch number:

```text
1.0
```

Git tags are the source of truth for `Z`. The patch number is never stored in
`.release-version`, never derived from Actions run numbers, and never committed
back to the repository. Release lines are never inferred from commit messages,
PR labels, Conventional Commits, or semantic-release rules.

With `.release-version` set to `1.2`, consecutive merges to `main` produce:

```text
merge 1 → v1.2.0
merge 2 → v1.2.1
merge 3 → v1.2.2
```

Patch numbers need not be contiguous; the workflow always takes the highest
existing patch on the line, compared numerically, and adds one. So an existing
`v1.2.9` and `v1.2.10` yield `v1.2.11`.

To intentionally move the minor line, edit `.release-version`:

```diff
-1.2
+1.3
```

After that change reaches `main` the next release is `v1.3.0`, followed by
`v1.3.1`, `v1.3.2`, and so on. Moving `1.9` to `2.0` likewise makes the next
release `v2.0.0`. Tags on other lines, such as `v1.1.99` or `v2.0.0`, and
prerelease-like or unrelated tags, such as `v1.2.3-beta` or `foo-v1.2.100`,
never influence the calculation.

Release notes are generated automatically by GitHub from the changes since the
previous release; maintainers do not write notes for each patch release.

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
  repository research, and the host's repository-editing, command-execution, and
  skill-invocation capabilities. Graphify and OpenProject are used read-only
  where available and are not required. It writes only to source files, never to
  Jira or Confluence. Access to the actual checked-out source code is mandatory:
  the skill stops rather than implementing a ticket from documentation alone.
- The Stage 05 specialists — `review-implementation-architecture`,
  `implement-database-change`, `implement-backend-change`,
  `implement-frontend-change`, `implement-android-change`,
  `validate-ux-implementation`, and `write-unit-tests` — require Jira and
  Confluence reads, DeepWiki repository research where available, and access to
  the repositories they own. The four implementation specialists and
  `write-unit-tests` also need repository-editing and command-execution
  capabilities; `review-implementation-architecture` and
  `validate-ux-implementation` are read-only. `implement-database-change`
  additionally needs a checked-out `AMRIT-DB`, and creates no application-local
  substitute migration when it is unavailable.
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
