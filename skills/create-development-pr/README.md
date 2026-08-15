# create-development-pr

`create-development-pr` supports the Pull Request portion of Stage 04 — In Development. It takes one implemented and locally verified AMRIT Jira ticket and turns the working implementation into a properly structured development Pull Request against the correct `release-X.Y.Z` branch.

**This skill performs Git and GitHub write operations.** It creates branches, commits, pushes, and opens Pull Requests. It does not perform substantive implementation.

## Purpose

Package an existing implementation into the correct Git and GitHub workflow: verify the working tree, determine the release branch, create a Jira-named branch, verify the change, commit, push, generate a traceable title and description, create the Pull Request, and report it honestly.

## Relationship to `implement-jira-ticket`

The two skills split Stage 04 cleanly:

| | `implement-jira-ticket` | `create-development-pr` |
| --- | --- | --- |
| Changes source code and unit tests | Yes | No |
| Creates branches, commits, pushes | No | Yes |
| Creates the Pull Request | No | Yes |
| Writes to Jira | No | No |
| Approves or merges | No | No |

`implement-jira-ticket` → orchestrates the Stage 04 engineering personas that change source code and unit tests. It routes to the specialist skills the ticket actually needs — `review-implementation-architecture`, `implement-database-change`, `implement-backend-change`, `implement-frontend-change`, `implement-android-change`, `validate-ux-implementation`, and `write-unit-tests` — none of which perform Git or Pull Request work either.

`create-development-pr` → packages an already implemented change into the correct Git/GitHub workflow.

The boundary is unchanged by that orchestration: everything upstream edits files, and this skill alone creates the branch, commit, push, and Pull Request. A change that legitimately spans an application repository and `AMRIT-DB` is still treated as separate Git repositories that may need separate Pull Requests.

This skill is normally used **after** `implement-jira-ticket` completes successfully, but invoking that skill is **not a hard dependency**. Each packaged skill remains independently installable, and this one works from the Jira ticket and the actual repository state. If the implementation is materially incomplete, the skill stops and sends the work back to implementation rather than quietly completing development work itself.

## When to use it

Use it when:

- a Jira Story, Task, or Bug has been implemented in a checked-out AMRIT repository;
- the implementation has been verified locally, or is ready to be verified;
- the next step is submitting the change for code review.

Do not use it to implement missing functionality, fix substantial defects, add missing unit tests, modify requirements, transition Jira, or review, approve, or merge a Pull Request.

## Intended users

Developers and Senior Developers. Code review by another engineer remains mandatory and is outside this skill.

## Supported Jira issue types

- Story
- Task
- Bug

## Expected invocation

```text
/create-development-pr AMRIT-1234
```

```text
Create the development PR for AMRIT-1234
```

If no ticket key is supplied, the skill asks for one before inspecting Git.

## Jira is strictly read-only

The skill reads the issue key, type, summary, description, acceptance criteria, parent Epic, linked issues, fix version or release information, sprint context, components, and labels. Jira supplies traceability and scope validation, nothing else.

It never transitions the issue, edits a field, assigns it, comments on it, creates a subtask, or changes acceptance criteria — including after the Pull Request is created successfully.

If the Jira issue cannot be retrieved, the skill does not fabricate its title, requirements, or acceptance criteria, and does not create a Pull Request: traceability cannot be established.

Confluence and DeepWiki are not required. Requirements and architecture research belong to the upstream skills.

## Release-branch discovery

AMRIT development targets a `release-X.Y.Z` branch. The skill does not default to `main`, `master`, or `develop` unless repository or project policy explicitly says otherwise for the ticket.

It weighs, in roughly this order: a user-supplied target branch, the ticket's release or fix-version information, authoritative sprint or release context, the actual remote `release-*` branches, documented repository conventions, and the current implementation context. Remote branch information is fetched when needed, and the chosen branch is validated as actually existing. A release branch is never invented.

When exactly one appropriate branch is identified confidently, it is used. When several plausible `release-X.Y.Z` branches exist and the evidence does not identify the right one, the skill stops and asks. The selected base and the evidence behind it appear in the final report.

Before creating a branch, the skill checks whether the implementation is actually based on the correct release branch instead of branching from whatever is checked out. It protects uncommitted work first and performs no automatic rebase, reset, force checkout, or destructive stash. If the work is on the wrong base and moving it safely is non-trivial, the skill stops and reports it rather than claiming the release-branch requirement is satisfied.

## Branch naming

The Jira key is always present in the branch name. Repository conventions come first; the fallback is `feature/ABC-123-short-description`, with `bugfix/ABC-123-short-description` used for bugs only where the repository explicitly distinguishes bug branches. The `bugfix/` prefix is not imposed on a repository that uses `feature/` for all development work.

The description derives from the Jira summary, normalized to lowercase hyphenated words with unnecessary punctuation removed and the name kept concise. `AMRIT-1234 Add beneficiary search filters` yields `feature/AMRIT-1234-beneficiary-search-filters`.

Before creating anything, the skill checks for an existing local branch, an existing remote branch, and any other branch already referencing the Jira key. A suitable existing branch is validated and reused rather than duplicated. An existing remote branch containing unknown work is a stop-and-ask condition.

## Working-tree safety for unrelated local changes

Every uncommitted change is treated as the user's property. Each modified, added, deleted, and untracked path is classified as ticket-related, unrelated, or unsafe, and only ticket-related paths are staged.

- `git add .` and `git add -A` are not used unless inspection has established that every included path belongs to the ticket and is safe.
- Unrelated work stays in the working tree, uncommitted and unmodified.
- Destructive commands — `git reset --hard`, `git clean -fd`, `git checkout --force`, destructive stash operations — are never run.
- Wrong staging is corrected by unstaging, never by discarding content.
- Secrets, `.env` credentials, tokens, private keys, cloud and database credentials, GitHub PATs, MCP credentials, private authentication headers, local IDE state, temporary files, ignored generated artifacts, and unrelated modifications are never committed.

If ticket-related and unrelated changes are entangled such that safe staging cannot be determined, the skill stops and explains the conflict, naming the affected paths, rather than risking the user's work.

Before committing and again before pushing, the intended diff is screened for secrets. If one appears, the skill stops, commits and pushes nothing, and reports only the affected path and the remediation requirement — never the secret value.

## Diff review and scope discipline

The complete ticket-related diff is reviewed before commit against the Jira scope, the acceptance criteria, the expected repository boundaries, and the repository's coding conventions. It is screened for debug logging, commented-out experiments, temporary files, secrets, local configuration, unrelated refactors, generated files, incidental reformatting, large binaries, and build outputs.

Only clearly mechanical, low-risk PR-preparation corrections are permitted, such as removing an accidental debug statement or excluding a stray temporary file. Implementing a missing acceptance criterion, fixing a substantive defect, adding missing unit tests, or refactoring for style are all out of scope. When any of those is needed, the skill stops with:

**Implementation is not ready for PR preparation. Run `implement-jira-ticket` again or resolve the implementation issues first.**

## Verification before commit and PR

A previous agent's claim that tests passed is not verification. The skill discovers the repository's real commands — from build files, package scripts, lint and static-analysis configuration, the CI workflow, and developer documentation — and runs the relevant checks, narrowest first: unit tests, module tests, lint, formatting or checkstyle, type checking, static analysis, compilation, and build.

Results are reported as PASS only when the command actually ran and succeeded, FAILED with what failed, or `NOT RUN — <reason>` when an environmental limitation blocked it. Results are never aggregated into "all tests pass".

If a required check fails because of the implementation, the skill stops before creating the PR unless repository policy explicitly permits a draft PR for failing checks. It never weakens a test, relaxes an assertion, disables a lint rule, adds a suppression, skips static analysis, or edits CI configuration to make a check green.

## Commit behaviour

Only intended, explicitly staged paths are committed, after the staged diff has been reviewed. The commit message follows the repository's existing convention, inspected from recent history; the fallback is `AMRIT-1234: Add beneficiary search filters`. Conventional Commits are not imposed on a repository that does not use them, and meaningless messages such as `changes`, `fix`, `updates`, or `final` are not written. The message summarizes the implemented change rather than restating the ticket, and contains no secret.

The skill creates one new commit. It does not amend unrelated existing commits, rewrite shared history, or squash the branch's existing commits — the final squash merge is a repository and reviewer concern. The real commit SHA is recorded; one is never invented.

## Push behaviour

The development branch is pushed to the repository's appropriate GitHub remote, with upstream tracking set when required. Only that branch is pushed. The skill never pushes to `release-X.Y.Z`, `main`, `master`, `develop`, or another protected or shared branch, and never force-pushes unless the user explicitly requests it and the context makes it safe.

If authentication or authorization fails, the failure is reported. The skill does not embed tokens in remote URLs, does not persist credentials, does not attempt unauthenticated bypasses, and never prints a credential value.

## PR title generation

Repository conventions come first; the fallback is `AMRIT-1234: Add beneficiary search filters`. The Jira key is always present. The title is concise, descriptive, traceable, aligned with the Jira summary, and limited to what the diff actually implements. Status words such as "done", "approved", or "ready to merge" never appear.

## PR description generation

Before writing, the skill inspects the Jira issue, the acceptance criteria, the final committed diff, the checks actually run, the database impact, and any repository PR template such as `.github/pull_request_template.md`.

A repository template wins: its headings, ordering, and checklists are kept, its items are left unchecked when not genuinely satisfied, and its sections are not deleted. The generic fallback structure — Jira, Summary, Changes, Acceptance Criteria, Database Changes, Verification, Notes — is used only when no stronger repository template exists, and only the sections the evidence supports are included.

Acceptance criteria are mapped against the actual implementation rather than copied from Jira. The description never states "all tests pass", "CI green", "reviewed", "approved", "ready to merge", or "code review complete" unless that state is genuinely established and within the skill's authority — which, for review and merge claims, it never is.

## GitHub PR creation

The Pull Request is created with the Jira-aware title, the generated description, the validated `release-X.Y.Z` base, and the ticket's development branch as head. Where practical, the skill first checks whether an open PR already exists for the same branch or Jira key, and reports an existing appropriate PR instead of creating a duplicate.

GitHub operations use whatever GitHub capability the host exposes; logical capabilities are discovered rather than hardcoded to fragile function names. Local Git is used for local repository operations. No credentials or machine-specific configuration are added to the skill.

If no authenticated GitHub PR-creation capability is available, the skill completes only the safe local preparation, does not fabricate a PR URL, reports the branch and commit that do exist, supplies the intended title and description for manual submission, and reports that PR creation could not be completed because GitHub write access is unavailable.

## AMRIT-DB and multi-repository handling

Authoritative AMRIT schema changes belong in `AMRIT-DB`. The skill never commits an application-local substitute migration to make a PR self-contained. If a required `AMRIT-DB` change is missing, it stops rather than creating a misleading application PR that implies a complete implementation, and reports that the work must return to implementation.

When a ticket legitimately spans an application repository and `AMRIT-DB`, those are separate Git repositories that may need separate Pull Requests. Commits from two repositories are never combined into one PR. Each repository is validated independently with its own release branch, the same Jira key appears in both branch names, and each description cross-references the dependency using only real URLs. If creating multiple PRs automatically would be unsafe, or the intended ordering and dependency handling is unclear, the skill stops after identifying the required PR set and asks how to proceed. Cross-repository dependency policy is never invented.

## CI reporting

After creation, GitHub checks or statuses are inspected when the capability supports it, and only observed state is reported — for example `CI: pending`, `CI: 5/5 checks passed`, `CI: 1 check failed — <name>`, or `CI: status unavailable`.

Creating the PR is the skill's primary responsibility, so it does not wait indefinitely for CI. CI success is never fabricated, and green CI is listed among the remaining Stage 04 requirements while it is still pending.

## Review and merge boundary

Senior Developer code review, reviewer approval, addressing substantive review feedback, the final squash merge, and release-branch merge confirmation are all outside this skill.

The skill never approves its own Pull Request, merges it, squash-merges it, requests a fake or self approval, bypasses branch protection or required reviews, claims code-review sign-off, or claims the Stage 04 exit criterion is satisfied merely because a PR exists.

The Stage 04 exit criteria remain: PR approved, code-review sign-off obtained, CI checks green, and the PR squash-merged into the appropriate release branch.

## Handling ambiguity

Ordinary details are resolved by inspecting Jira, repository conventions, Git history, remote branches, PR templates, and GitHub state. The skill stops and asks only when a material decision cannot be resolved safely: an ambiguous release branch, unrelated local changes that prevent safe staging, an existing conflicting branch containing unknown work, or an unclear multi-repository PR ordering. It never guesses through those situations.

## Success and failure semantics

Every invocation ends with exactly one of:

- **Development PR created. Awaiting code review.** — the Pull Request exists at a real URL, targeting the validated release branch, from a Jira-named branch carrying a real commit, with verification reported honestly.
- **Development PR not created. Resolve the items above before retrying.** — the PR was not created: the implementation was incomplete, a required check failed, a required `AMRIT-DB` change was missing, a secret was detected, GitHub write access was unavailable, or a material ambiguity stopped the run. The report states what was completed locally and what remains.

Neither line means the ticket is Done, approved, reviewed, merged, or code-review signed off. The skill never makes those claims.

## Example invocation

```text
/create-development-pr DEMO-5140
```

See [examples/](examples/) for fictional runs: a feature PR, a bugfix PR that had to stop and ask about an ambiguous release branch, and a database-dependent case covering both a missing `AMRIT-DB` change and a legitimate two-repository change set. The examples are illustrative only and do not describe real AMRIT tickets, repositories, branches, or Pull Requests.

## Required capabilities

The skill conceptually requires:

- Jira read access, for the ticket and its traceability;
- local Git and repository access through the host's command execution;
- a GitHub capability for remote branch inspection, Pull Request lookup, Pull Request creation, and check or status lookup where available.

Tool names vary by host, so capabilities are discovered rather than hardcoded. Jira writes are never requested or used. Confluence, DeepWiki, and Graphify are not required.

GitHub write access is not part of the repository's project-scoped MCP configuration. It comes from the host — a connected GitHub capability or an authenticated GitHub CLI in the developer's environment. Without it, the skill completes safe local preparation only and says so.

## Use and distribution

Invoke `/create-development-pr` from the repository root using a supported coding agent. Configure local MCP credentials only where the selected client requires them; never commit real tokens.

For a packaged installation, download `create-development-pr.zip` from the latest successful **Validate and package skills** GitHub Actions run and upload or install it with the relevant client workflow. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
