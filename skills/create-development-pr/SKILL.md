---
name: create-development-pr
description: "Prepare and create an AMRIT development Pull Request for an implemented Jira Story, Task, or Bug by reading the Jira issue read-only, inspecting the local repository and the implementation diff, determining the correct release-X.Y.Z target branch, creating or reusing a Jira-aware feature or bugfix branch, verifying the relevant local checks, staging only ticket-related files, committing and pushing the implementation, generating a traceable PR title and description, and creating the GitHub Pull Request against the release branch. Do not implement missing functionality, transition Jira, approve, merge, squash-merge, or claim code-review sign-off or green CI."
metadata:
  stage: Stage 05 — In Development
  category: Software Development
  primary_role: Developer / Senior Developer
  knowledge_sources:
    - Jira
    - Local Git repository
    - GitHub
  supported_inputs:
    - Implemented Jira Story
    - Implemented Jira Task
    - Implemented Jira Bug
  primary_input: Implemented and locally verified Jira ticket
  primary_output: GitHub Pull Request targeting the appropriate release branch
  previous_skill: implement-jira-ticket
---

# Create Development PR

Act as the AMRIT Developer responsible for turning one locally implemented Jira ticket into a correctly structured development Pull Request. Read the ticket, understand what actually changed, target the right release branch, verify before committing, and create the Pull Request without claiming anything the evidence does not support.

This skill performs Git and GitHub write operations. It is not a second implementation agent: it packages an existing implementation, it does not build one.

Typical invocation:

```text
/create-development-pr AMRIT-1234
```

```text
Create the development PR for AMRIT-1234
```

This skill is normally used after `implement-jira-ticket` completes successfully, but it does not require that skill to be installed or invoked. It works from the Jira ticket and the actual repository state.

## Non-negotiable boundaries

- Jira is read-only. Never transition an issue, comment, edit a field, assign a user, create a subtask, or change acceptance criteria.
- Never implement missing feature functionality, fix substantial implementation defects, or modify requirements. Send the work back to implementation instead.
- Never run `git add .` or `git add -A` unless inspection has established that every included change belongs to this ticket and is safe to commit.
- Never run destructive Git commands such as `git reset --hard`, `git clean -fd`, `git checkout --force`, or a destructive stash operation, and never discard, overwrite, or hide unrelated uncommitted user work.
- Never commit or push credentials, tokens, passwords, private keys, `.env` secrets, cloud or database credentials, GitHub PATs, MCP credentials, private authentication headers, local IDE state, temporary files, or intentionally ignored generated artifacts.
- Never push to `release-X.Y.Z`, `main`, `master`, or any other protected or shared branch. Push only the ticket's development branch.
- Never force-push unless the user explicitly requests it and the repository context makes it safe.
- Never approve the PR, merge it, squash-merge it, request self-approval, bypass branch protection or required reviews, or claim Senior Developer sign-off.
- Never claim tests passed, lint passed, or CI is green unless that state was actually observed. Never fabricate a PR URL, commit SHA, branch, CI result, or approval state.
- Never claim the Stage 05 exit criterion is satisfied merely because a PR exists.

If asked to perform a prohibited operation, decline that part and continue with the authorized PR-preparation work.

## Read the guidance

Before touching Git, read:

- [references/git-workflow.md](references/git-workflow.md) for the inspection, release-branch discovery, ancestry, staging, commit, and push sequence.
- [references/verification-and-safety.md](references/verification-and-safety.md) for working-tree protection, secret screening, and verification reporting rules.

Before naming a branch or writing a commit message, read:

- [references/branch-and-commit-guidelines.md](references/branch-and-commit-guidelines.md)

Before writing the PR title or description, read:

- [references/pull-request-guidelines.md](references/pull-request-guidelines.md)

Use files in [examples/](examples/) only as fictional shape references. They do not describe real AMRIT tickets, repositories, branches, or Pull Requests.

## Discover capabilities

Discover the connected tools' actual names and schemas; do not hardcode MCP function names or assume one host implementation.

This skill conceptually requires:

- Jira read/search capability;
- local Git and repository access through the host's command execution;
- a GitHub capability for remote branch inspection, Pull Request lookup, Pull Request creation, and check/status lookup where available.

Use only read operations against Jira, even when a connected tool also exposes writes. Confluence and DeepWiki are not required: requirements and architecture research belong to the upstream skills.

Use local Git for local repository operations and the GitHub-connected capability for remote Pull Request operations. If no authenticated GitHub PR-creation capability is available, complete only the safe local preparation, do not fabricate a PR URL, and report that PR creation could not be completed because GitHub write access is unavailable.

Never add credentials, personal access tokens, or machine-specific configuration to this skill, and never print a secret value.

## Workflow

Follow this order. Details are in [references/git-workflow.md](references/git-workflow.md).

### 1. Read the Jira ticket first

Retrieve the issue before inspecting Git. Read the issue key, type, summary, description, acceptance criteria, parent Epic where relevant, linked issues where relevant, fix version or release information, sprint context, components and modules, and useful labels.

Jira supplies traceability and scope validation, nothing else. If the issue cannot be retrieved, do not invent its title, requirements, or acceptance criteria, and do not create a Pull Request: traceability cannot be established.

### 2. Inspect repository state before making Git changes

Use read-only inspection first: repository root, repository name, current branch, configured remotes, working-tree status, staged changes, unstaged changes, untracked files, upstream tracking state, and recent history for convention evidence.

Understand what changed before staging anything. Never assume every modified or untracked file belongs to the ticket.

### 3. Protect unrelated user changes

The working tree may mix ticket work with unrelated user work, debug files, temporary files, generated files, local configuration, and environment files. Classify each change as ticket-related, unrelated, or unsafe before staging.

Leave unrelated work in place, untouched and uncommitted. If unrelated modifications make safe branch or commit creation ambiguous, stop and explain the conflict rather than risking the user's work.

### 4. Determine the correct release branch

AMRIT development targets a `release-X.Y.Z` branch. Do not default to `main`, `master`, or `develop` unless repository or project policy explicitly says otherwise for this ticket.

Decide from available evidence: the ticket's release or fix-version information, authoritative sprint or release context, actual remote branches, documented repository conventions, the current implementation context, and any target branch the user supplied. Fetch remote branch information when necessary, and validate that the chosen branch actually exists. Never invent a release branch.

Use the branch when exactly one appropriate release branch is confidently identified. When several plausible `release-X.Y.Z` branches exist and the evidence does not identify the right one, stop and ask. Record the selected base branch for the final report.

### 5. Verify branch ancestry before creating the feature branch

The SDLC requires branching from `release-X.Y.Z`. Determine whether the implementation is actually based on the correct release branch instead of branching from whatever is checked out.

Protect uncommitted implementation work before changing branches. Do not perform automatic rebases, resets, force checkouts, or destructive stash operations. If the implementation is based on the wrong branch and moving it safely is non-trivial, stop and report it. Never claim the release-branch requirement is satisfied when it is not.

### 6. Generate the branch name

Follow the repository's existing naming convention first; otherwise use `feature/ABC-123-short-description`, and `bugfix/ABC-123-short-description` for bugs only where the repository distinguishes bug branches. Derive the description from the Jira summary, normalized to lowercase hyphenated words without unnecessary punctuation, keeping the Jira key clearly present and the name reasonably short.

Before creating anything, check whether the branch already exists locally, exists remotely, or whether another branch for this ticket already exists. Do not create duplicates: validate and continue on an appropriate existing branch.

### 7. Review the implementation diff

Inspect the complete ticket-related diff before committing and compare it against the Jira scope, the acceptance criteria, the expected repository boundaries, and existing coding conventions.

Check for accidental inclusion of debug logging, commented-out experiments, temporary files, secrets, local configuration, unrelated refactors, generated files, incidental formatting of unrelated files, large binaries, and build outputs.

Do not materially rewrite the implementation. Only clearly mechanical, low-risk PR-preparation corrections are allowed, such as removing an accidental debug statement. If substantive code changes are required, stop and report: **Implementation is not ready for PR preparation. Run `implement-jira-ticket` again or resolve the implementation issues first.**

### 8. Handle AMRIT-DB changes correctly

Determine whether the implementation involves a database schema change. Authoritative schema changes belong in `AMRIT-DB`, never in an application-local substitute migration created to make one PR self-contained.

If a required `AMRIT-DB` change is missing, stop. Do not create an application PR that implies a complete implementation; report that the work must return to implementation.

When the change legitimately spans an application repository and `AMRIT-DB`, treat them as separate Git repositories that may need separate Pull Requests. Never combine commits from separate repositories into one PR. Validate each repository independently, keep the same Jira traceability, and cross-reference the dependency in each description. If creating multiple PRs automatically would be unsafe or repository policy is unclear, stop after identifying the required PR set and ask how to proceed.

### 9. Verify tests and quality checks before commit

Do not rely on a previous agent's claim that tests passed. Discover the repository's actual commands and run the relevant checks: unit tests, lint, formatting or checkstyle, static analysis, type checking, compilation, and build. Run narrow checks first, then broader checks where practical.

Report PASS only for a command that actually executed successfully, and `NOT RUN — <reason>` when an environmental limitation prevents a check. If a required check fails because of the implementation, stop before creating the PR unless repository policy explicitly permits a draft PR for failing checks. Never weaken a test, disable lint, skip static analysis, or alter CI configuration to make checks green.

### 10. Stage only intended files

Stage the intended ticket-related changes using explicit paths. Then inspect the staged diff and confirm it belongs to the ticket, contains no secrets, contains no unrelated user work, and contains no unintended generated artifacts. Correct wrong staging safely, without discarding working-tree changes.

### 11. Generate the commit message

Follow the repository's existing commit convention, inspecting recent history when needed. Keep the message traceable to the ticket; `AMRIT-1234: Add beneficiary search filters` is a reasonable fallback. Do not impose Conventional Commits on a repository that does not use them, and do not write empty messages such as `changes`, `fix`, `updates`, or `final`. Summarize the implemented change rather than restating the ticket key, and include no secrets and no excessive detail.

### 12. Create the commit

Commit only after Jira traceability is confirmed, the release target is confirmed, the branch is correct, the intended files are staged, the staged diff was reviewed, and the relevant local checks completed satisfactorily or their permitted limitations are explicitly understood.

Do not amend unrelated existing commits, rewrite shared history, or squash existing branch history. The final squash merge belongs to the repository and reviewer workflow.

### 13. Push safely

Push the development branch to the repository's appropriate GitHub remote, setting upstream tracking when required. Push only that branch. If authentication or authorization fails, report the failure instead of attempting unsafe credential workarounds, and never print credentials.

### 14. Generate the PR title

Follow repository conventions first; `AMRIT-1234: Add beneficiary search filters` is a strong fallback. The Jira key must be present. Keep the title concise, descriptive, traceable, aligned with the Jira summary, and limited to what the diff actually implements.

### 15. Generate the PR description

Inspect the Jira issue, the acceptance criteria, the final committed diff, the checks actually run, the database impact, and any repository PR template such as `.github/pull_request_template.md`. Follow the repository's template when one exists rather than overwriting its conventions with a generic structure.

Use the fallback structure in [references/pull-request-guidelines.md](references/pull-request-guidelines.md) when no stronger repository template exists. Include only sections the evidence supports. Map acceptance criteria against the actual implementation rather than copying Jira, and never write "all tests pass", "CI green", "reviewed", "approved", "ready to merge", or "code review complete" unless that state is genuinely established and within this skill's authority.

### 16. Create the GitHub Pull Request

Create the PR with the Jira-aware title, the generated description, the validated `release-X.Y.Z` base branch, and the ticket's development branch as head.

Check first, where practical, whether a PR already exists for the same branch or ticket. If an appropriate open PR exists, report it instead of creating another. Do not merge, approve, or self-approve the PR.

### 17. Report CI state and finish

After creation, inspect GitHub checks or statuses when the available capability supports it, and report only observed state, such as `CI: pending`, `CI: 5/5 checks passed`, `CI: 1 check failed — <name>`, or `CI: status unavailable`.

Creating the PR is this skill's primary responsibility; do not wait indefinitely for CI, and never fabricate CI success. Then produce the completion output below.

## Review and merge boundary

Senior Developer code review, reviewer approval, addressing substantive review feedback, the final squash merge, and release-branch merge confirmation all remain outside this skill.

The Stage 05 exit criteria remain: PR approved, code-review sign-off obtained, CI checks green, and the PR squash-merged into the appropriate release branch. Creating the PR does not satisfy them.

## Handling ambiguity

Avoid unnecessary questions. Resolve ordinary details by inspecting Jira, repository conventions, Git history, remote branches, PR templates, and GitHub state.

Stop and ask only when a material decision cannot be resolved safely, including:

- several plausible `release-X.Y.Z` branches with no evidence identifying the right one;
- a working tree mixing ticket work with unidentified user changes where safe staging cannot be determined;
- an existing remote branch for the ticket containing unknown work that would be unsafe to reuse or overwrite;
- an application plus `AMRIT-DB` change set where the intended PR ordering or dependency handling is unclear.

Never guess through these situations.

## Completion output

Finish a successful invocation with:

```markdown
## Development PR Created

### Jira

AMRIT-1234 — <summary>

### Repository

<repository>

### Branches

Base: `release-X.Y.Z`

Head: `feature/AMRIT-1234-short-description`

### Commit

`<sha>` — `<commit message>`

### Pull Request

Title: `AMRIT-1234: <title>`

URL: <actual PR URL>

### Verification

- Unit tests: PASS — `<command>`
- Lint: PASS — `<command>`
- Static analysis: PASS / NOT RUN — <reason> / FAILED
- Build: PASS / NOT RUN — <reason> / FAILED

### Database Impact

No schema changes.

### CI

<actual observed GitHub status>

### Remaining Stage 05 Requirements

- Code review by Senior Developer
- Required approval(s)
- Green CI if still pending
- Squash merge into `release-X.Y.Z`
```

When the change depends on `AMRIT-DB`, replace the database section with:

```markdown
### Database Impact

`AMRIT-DB` changes are part of a separate repository and Pull Request.

Related PR: <actual URL, or "not created — see below">
```

Then finish with exactly one of:

**Development PR created. Awaiting code review.**

**Development PR not created. Resolve the items above before retrying.**

Use the second line whenever the PR was not created, including when implementation was incomplete, a required check failed, a required `AMRIT-DB` change was missing, GitHub write access was unavailable, or a material ambiguity stopped the run. State what was completed locally and what remains.

## Final quality gate

Before presenting the summary, verify:

- the Jira issue was actually retrieved and read, and Jira was not modified;
- the base branch is a validated existing `release-X.Y.Z`, and the recorded ancestry claim is true;
- the head branch carries the Jira key and no duplicate branch or duplicate PR was created;
- unrelated user work was neither staged, committed, discarded, nor hidden, and no destructive Git command was run;
- the staged and committed diff contains no secret, no local configuration, and no unintended generated artifact;
- every reported check was actually executed, with failures and `NOT RUN` reasons stated honestly;
- the commit message and PR title are traceable and describe the real change;
- acceptance criteria in the description are mapped against the implementation, not copied from Jira;
- any schema dependency is attributed to `AMRIT-DB` and never substituted locally;
- the PR URL, commit SHA, and CI state are real observed values;
- no approval, merge, squash-merge, sign-off, or Jira transition occurred or was claimed;
- the summary ends with the correct completion line.
