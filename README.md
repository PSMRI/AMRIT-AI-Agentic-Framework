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
| [`implement-jira-ticket`](skills/implement-jira-ticket/README.md) | `/implement-jira-ticket` | Stage 05 — In Development | The Stage 05 entry point and engineering orchestrator: implemented and locally verified code with unit tests, produced by the specialist personas the ticket actually needs, with any schema change placed in `AMRIT-DB`. |
| [`review-implementation-architecture`](skills/review-implementation-architecture/README.md) | `/review-implementation-architecture` | Stage 05 — In Development | A read-only architecture conformance assessment of an implementation against the approved Stage 03 design. |
| [`implement-database-change`](skills/implement-database-change/README.md) | `/implement-database-change` | Stage 05 — In Development | The `AMRIT-DB` migration for a ticket, plus the schema contract the application implements against. |
| [`implement-backend-change`](skills/implement-backend-change/README.md) | `/implement-backend-change` | Stage 05 — In Development | The server-side change in a Spring Boot API repository, plus the API and persistence contracts it establishes. |
| [`implement-frontend-change`](skills/implement-frontend-change/README.md) | `/implement-frontend-change` | Stage 05 — In Development | The web UI change in an Angular repository, consistent with the design system and the real API contract. |
| [`implement-android-change`](skills/implement-android-change/README.md) | `/implement-android-change` | Stage 05 — In Development | The Kotlin/Android change, consistent with the app architecture, offline behaviour, and platform constraints. |
| [`validate-ux-implementation`](skills/validate-ux-implementation/README.md) | `/validate-ux-implementation` | Stage 05 — In Development | A read-only UX conformance assessment of an implemented interface against approved wireframes, the design system, and accessibility expectations. |
| [`write-unit-tests`](skills/write-unit-tests/README.md) | `/write-unit-tests` | Stage 05 — In Development | Code-level unit tests for an implemented change, with executed results; separate from `draft-test-cases` and Stage 07 QA. |
| [`create-development-pr`](skills/create-development-pr/README.md) | `/create-development-pr` | Stage 05 — In Development | A GitHub Pull Request for an implemented Jira ticket, from a Jira-named branch against the correct `release-X.Y.Z` branch, labelled **Awaiting code review**. |
| [`answer-codebase-questions`](skills/answer-codebase-questions/README.md) | `/answer-codebase-questions` | Cross-lifecycle — Codebase knowledge | A concise, evidence-backed AMRIT codebase answer from DeepWiki, Confluence, and Graphify; never Jira. |

`implement-jira-ticket` is the Stage 05 entry point. It inspects the Jira
ticket, the knowledge sources, and the actual source code, classifies which
engineering personas the change requires, and invokes only those specialist
skills — `review-implementation-architecture`, `implement-database-change`,
`implement-backend-change`, `implement-frontend-change`,
`implement-android-change`, `validate-ux-implementation`, and
`write-unit-tests` — in dependency order before handing off to
`create-development-pr`. The specialists are **conditionally selected**, never
an unconditional sequence.

`create-development-pr` performs Git and GitHub write operations — branch,
commit, push, and Pull Request creation — but no substantive implementation.
`create-brd`, `create-product-backlog`, `create-technical-design`,
`answer-codebase-questions`, `review-implementation-architecture`, and
`validate-ux-implementation` are read-only.

The skills are independent. A downstream skill can consume an approved
upstream output without requiring the upstream skill at runtime, and
`implement-jira-ticket` applies a persona's contract inline when that
persona's specialist skill is not installed.

## Stage 05 — In Development

Stage 05 is entered through one skill. `implement-jira-ticket` orchestrates the
engineering personas the ticket actually requires and hands off to
`create-development-pr`:

```text
Stage 03 — Analysis
        ↓
Stage 04 — Ready for Development      (no skill; human Definition of Ready)
        ↓
Stage 05 — In Development

implement-jira-ticket
        |
        |-- review-implementation-architecture   (architecturally significant change)
        |-- implement-database-change            (schema, migrations, indexes)
        |-- implement-backend-change             (services, APIs, domain logic)
        |-- implement-frontend-change            (web UI, state, forms)
        |-- implement-android-change             (Kotlin, mobile flows, offline)
        |-- validate-ux-implementation           (user-visible change vs approved UX)
        `-- write-unit-tests                     (code-level tests for what changed)
                 |
                 v
        create-development-pr
        ↓
Stage 06 — Pending QA
```

Stage 05 begins with a ticket that Stage 04 — Ready for Development has already
made sprint-ready. That readiness check is performed by humans; no skill in this
repository covers Stage 04. See the
[lifecycle mapping](docs/lifecycle-mapping.md#stage-04--ready-for-development).

The specialists are **conditionally selected from the ticket, the approved
Stage 03 design, and the actual source code** — not an unconditional sequence.
A backend-only defect runs `implement-backend-change` and `write-unit-tests`;
an Android ticket runs `implement-android-change` and `write-unit-tests`. Only
unit tests are effectively always required, because production behaviour
changed.

Ordinary use needs one command:

```bash
/implement-jira-ticket AMRIT-1234
```

Actual source-code inspection is mandatory in every route, for the orchestrator
and for each specialist. Documentation, DeepWiki, Confluence, Graphify, and the
approved design describe intent; the checked-out repository decides what the
code does and where the change belongs. When the source is inaccessible, the
skills stop instead of implementing from documentation.

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
<bridge-root>/review-implementation-architecture/SKILL.md
    -> skills/review-implementation-architecture/SKILL.md
<bridge-root>/implement-database-change/SKILL.md
    -> skills/implement-database-change/SKILL.md
<bridge-root>/implement-backend-change/SKILL.md
    -> skills/implement-backend-change/SKILL.md
<bridge-root>/implement-frontend-change/SKILL.md
    -> skills/implement-frontend-change/SKILL.md
<bridge-root>/implement-android-change/SKILL.md
    -> skills/implement-android-change/SKILL.md
<bridge-root>/validate-ux-implementation/SKILL.md
    -> skills/validate-ux-implementation/SKILL.md
<bridge-root>/write-unit-tests/SKILL.md
    -> skills/write-unit-tests/SKILL.md
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

For Stage 05, install `implement-jira-ticket` together with the specialist
packages relevant to the repositories you work in. The orchestrator still works
alone — it applies a missing persona's contract inline — but each installed
specialist keeps its own guidance and code-inspection discipline.

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
├── implement-jira-ticket/              Stage 05 orchestrator
├── review-implementation-architecture/ Stage 05 specialist
├── implement-database-change/          Stage 05 specialist
├── implement-backend-change/           Stage 05 specialist
├── implement-frontend-change/          Stage 05 specialist
├── implement-android-change/           Stage 05 specialist
├── validate-ux-implementation/         Stage 05 specialist
├── write-unit-tests/                   Stage 05 specialist
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
  DeepWiki repository research, and the host's repository-editing,
  command-execution, and skill-invocation capabilities. Graphify and OpenProject
  are used read-only where the environment provides them, and neither is
  required. Jira and Confluence are never written to. Access to the actual
  checked-out source code is mandatory: the skill stops rather than implementing
  a ticket from documentation alone.
- The Stage 05 specialists — `review-implementation-architecture`,
  `implement-database-change`, `implement-backend-change`,
  `implement-frontend-change`, `implement-android-change`,
  `validate-ux-implementation`, and `write-unit-tests` — require read-only Jira
  and Confluence, DeepWiki repository research where available, and the host's
  repository access. The four implementation specialists and `write-unit-tests`
  also require repository-editing and command-execution capabilities;
  `review-implementation-architecture` and `validate-ux-implementation` are
  read-only. Each specialist inspects the code it owns before editing, and
  stops when that code is inaccessible.
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

`implement-jira-ticket` and its Stage 05 specialists edit source files by
design. They still never write to Jira or Confluence, never create a branch,
commit, push, or Pull Request, and never claim architecture, DBA, code-review,
QA, CI, or release approval; Git and Pull Request operations belong to the
downstream `create-development-pr` skill, and every approval remains a human
decision.

`create-development-pr` creates branches, commits, pushes, and Pull Requests by
design. It still never writes to Jira, never implements missing functionality,
never stages unrelated user work or secrets, never pushes to a protected branch,
and never approves, merges, or squash-merges a Pull Request or claims
code-review sign-off or green CI it did not observe. Every Stage 05 skill is
independently installable; none requires another at runtime.

See the [lifecycle mapping](docs/lifecycle-mapping.md) for inputs, outputs, and
review gates.
