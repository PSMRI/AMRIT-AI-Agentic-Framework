# Git Workflow

## Contents

- [Purpose](#purpose)
- [Step 1: Read the Jira ticket](#step-1-read-the-jira-ticket)
- [Step 2: Inspect the repository read-only](#step-2-inspect-the-repository-read-only)
- [Step 3: Classify every working-tree change](#step-3-classify-every-working-tree-change)
- [Step 4: Determine the release branch](#step-4-determine-the-release-branch)
- [Step 5: Verify branch ancestry](#step-5-verify-branch-ancestry)
- [Step 6: Create or reuse the development branch](#step-6-create-or-reuse-the-development-branch)
- [Step 7: Review the implementation diff](#step-7-review-the-implementation-diff)
- [Step 8: Place database changes](#step-8-place-database-changes)
- [Step 9: Verify before committing](#step-9-verify-before-committing)
- [Step 10: Stage only intended files](#step-10-stage-only-intended-files)
- [Step 11: Commit](#step-11-commit)
- [Step 12: Push](#step-12-push)
- [Step 13: Create the Pull Request](#step-13-create-the-pull-request)
- [Step 14: Report CI and finish](#step-14-report-ci-and-finish)
- [Preparation ledger](#preparation-ledger)

## Purpose

Sequence the work so that traceability is established before Git changes, the target branch is proven before branching, the diff is understood before staging, and verification happens before the commit. Every step up to Step 10 is read-only against the repository.

Jira is read-only throughout. No step in this workflow transitions, comments on, or edits an issue.

## Step 1: Read the Jira ticket

Accept the ticket key from the invocation, for example `/create-development-pr AMRIT-1234`. If no key is supplied, ask for one before inspecting Git.

Retrieve the issue through the connected Jira read capability and read:

- issue key;
- issue type — Story, Task, or Bug;
- summary;
- description;
- acceptance criteria;
- parent Epic where relevant;
- linked issues where relevant;
- fix version, release, or target-version fields;
- sprint or release context where authoritative;
- components and modules;
- labels where useful.

The summary drives the branch name, commit message, and PR title. The acceptance criteria drive the PR description's completeness mapping. The release information is the first evidence for the target branch.

If the issue cannot be retrieved, stop. Do not reconstruct the summary from the branch name, the diff, or memory, and do not create a Pull Request without traceability.

## Step 2: Inspect the repository read-only

Determine, before changing anything:

- repository root;
- repository name and the owning GitHub organization;
- current branch;
- configured remotes and their URLs;
- working-tree status;
- staged changes;
- unstaged changes;
- untracked files;
- upstream and tracking state;
- recent history, for commit-message and branch conventions;
- local and remote branches relevant to the ticket;
- repository instructions such as `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, and developer documentation;
- any PR template under `.github/`.

Typical read-only inspection includes commands of this kind, chosen as the situation requires rather than executed mechanically:

```text
git status
git branch --show-current
git remote -v
git diff
git diff --staged
git log --oneline -20
git branch -a
```

Fetch remote refs when remote branch information is needed. Prefer a plain fetch over any operation that moves local refs.

## Step 3: Classify every working-tree change

Before staging anything, classify each modified, added, deleted, and untracked path as one of:

1. **ticket-related** — part of the implementation for this Jira ticket;
2. **unrelated** — other user work, experiments, or changes belonging to a different ticket;
3. **unsafe** — secrets, environment files, local configuration, IDE state, temporary files, build outputs, or generated artifacts the repository intentionally ignores.

Only category 1 may be staged. Category 2 stays in the working tree, untouched. Category 3 is never committed, even when it looks incidental.

Never run `git add .` or `git add -A` unless inspection has established that every included path is category 1.

Never discard, revert, stash destructively, or hide category 2 work to simplify the tree. If ticket-related and unrelated changes are entangled inside the same files such that safe staging cannot be determined, stop and explain the conflict.

## Step 4: Determine the release branch

AMRIT development work targets `release-X.Y.Z`. Do not default to `main`, `master`, or `develop` unless repository or project policy explicitly says otherwise for this ticket.

Weigh evidence in roughly this order:

1. an explicit target branch supplied by the user;
2. the Jira ticket's release or fix-version information;
3. authoritative Jira sprint or release context;
4. actual remote `release-*` branches in the repository;
5. documented repository development conventions;
6. the current implementation context, including the branch the work was based on.

Then:

- validate that the chosen branch actually exists on the remote;
- never invent a release branch or assume the next version number;
- record the branch and the evidence that selected it.

Stop and ask when more than one plausible `release-X.Y.Z` branch exists and no evidence identifies the correct one. This is a material ambiguity, not a detail to guess.

## Step 5: Verify branch ancestry

Branching from the correct release branch is a requirement, not a formality. Determine whether the implementation is actually based on the selected release branch, for example by comparing the current branch's merge base against the release ref.

Before changing branches, protect uncommitted implementation work. Do not rebase, reset, force-checkout, or run a destructive stash operation automatically.

Outcomes:

- **Already based on the correct release branch** — continue.
- **On the release branch itself with uncommitted work** — create the development branch from the current state so the work carries over, then continue.
- **Based on the wrong branch and transferring the work is non-trivial** — stop and report it, describing what is on the wrong base and what the developer must decide.

Never state that the release-branch requirement is satisfied when the ancestry does not support it.

## Step 6: Create or reuse the development branch

Apply [branch-and-commit-guidelines.md](branch-and-commit-guidelines.md) to derive the name.

Before creating anything, check whether:

- the intended branch already exists locally;
- the intended branch already exists on the remote;
- another branch already exists for this Jira key.

If an appropriate branch exists, validate it — its base, its contents, and whether it already carries the implementation — and continue on it instead of creating a duplicate. If an existing remote branch for the ticket contains unknown work that would be unsafe to reuse or overwrite, stop and ask.

Create the branch from the validated release base when no suitable branch exists.

## Step 7: Review the implementation diff

Inspect the full ticket-related diff and compare it against:

- the Jira scope and acceptance criteria;
- the expected repository and module boundaries;
- the repository's existing coding conventions.

Screen specifically for:

- debug logging and temporary print statements;
- commented-out experimental code;
- temporary files;
- secrets and credentials;
- local or machine-specific configuration;
- unrelated refactors;
- generated files and build outputs;
- incidental reformatting of unrelated files;
- large binary artifacts.

Small, clearly mechanical, low-risk PR-preparation corrections are allowed, such as removing an accidental debug statement or an obviously stray temporary file from the change set.

If substantive code changes are needed — a missing acceptance criterion, a defect in the implementation, absent unit tests for changed behaviour, or a design problem — stop and report:

**Implementation is not ready for PR preparation. Run `implement-jira-ticket` again or resolve the implementation issues first.**

Do not become a second implementation agent.

## Step 8: Place database changes

Determine whether the implementation involves a database schema change. Authoritative AMRIT schema changes belong in the `AMRIT-DB` repository.

- If the diff contains an application-local substitute for an `AMRIT-DB` schema change, stop. Do not commit it to make the PR self-contained.
- If a required `AMRIT-DB` change is missing, stop and report that the work must return to implementation. Do not create an application PR that implies a complete implementation.
- If the change legitimately spans an application repository and `AMRIT-DB`, treat them as separate Git repositories with separate Pull Requests. Never attempt to combine commits from two repositories into one PR.

For a multi-repository change set, validate each repository independently, determine each repository's own release branch, keep the same Jira key in both branch names, and cross-reference the dependency in both descriptions. If creating both PRs automatically would be unsafe, or the intended ordering and dependency policy is unclear, stop after identifying the required PR set and ask how to proceed. Do not invent cross-repository dependency policy.

## Step 9: Verify before committing

Apply [verification-and-safety.md](verification-and-safety.md). Discover the repository's real commands; do not assume them. Run the narrowest relevant checks first, then broader checks where practical.

A previous agent's claim that tests passed is not verification. Report PASS only for a command that actually ran successfully in this session, and `NOT RUN — <reason>` otherwise.

If a required check fails because of the implementation, stop before creating the PR unless repository policy explicitly permits a draft PR for failing checks. Never weaken a test, disable a lint rule, skip static analysis, or edit CI configuration to make a check pass.

## Step 10: Stage only intended files

Stage the category 1 paths explicitly. Prefer naming paths over pattern-based bulk staging.

Then inspect the staged diff and confirm it:

- belongs entirely to the Jira ticket;
- contains no secret or credential;
- contains no unrelated user work;
- contains no unintended generated artifact.

If the staged content is wrong, correct the staging with non-destructive operations that leave the working tree intact. Unstaging a path is acceptable; discarding its content is not.

## Step 11: Commit

Commit only after all of the following hold:

- Jira traceability is confirmed;
- the release target is confirmed and validated;
- the branch is correct and its ancestry is understood;
- only intended files are staged;
- the staged diff was reviewed;
- relevant local checks completed satisfactorily, or their permitted limitations are explicitly understood and will be reported.

Use the message produced by [branch-and-commit-guidelines.md](branch-and-commit-guidelines.md). Create one new commit; do not amend an unrelated existing commit, rewrite shared history, or squash the branch's existing commits. The final squash merge is the reviewer's and repository's concern.

Record the resulting commit SHA for the report; never invent one.

## Step 12: Push

Push the development branch to the repository's appropriate GitHub remote, setting upstream tracking when required.

- Push only the development branch.
- Never push to `release-X.Y.Z`, `main`, `master`, or another protected or shared branch.
- Never force-push unless the user explicitly requests it and the repository context makes it safe.
- If authentication or authorization fails, report the failure. Do not attempt credential workarounds, do not modify remote URLs to embed tokens, and never print credentials.

Re-screen the outgoing commit for secrets before pushing, as described in [verification-and-safety.md](verification-and-safety.md).

## Step 13: Create the Pull Request

Use the discovered GitHub capability to create the Pull Request with:

- the Jira-aware title;
- the generated description;
- the validated `release-X.Y.Z` base branch;
- the ticket's development branch as head.

Check first, where practical, whether an open PR already exists for the same head branch or Jira key. Report an existing appropriate PR instead of creating a duplicate.

If no authenticated GitHub PR-creation capability is available, stop after the safe local preparation, do not fabricate a PR URL, and report that PR creation could not be completed because GitHub write access is unavailable.

Do not merge, approve, self-approve, request a fake approval, bypass branch protection or required reviews, or claim Senior Developer sign-off.

## Step 14: Report CI and finish

Inspect GitHub checks or statuses for the new PR when the capability supports it, and report only what was observed:

```text
CI: pending
CI: 5/5 checks passed
CI: 1 check failed — <name>
CI: status unavailable
```

Do not wait indefinitely for CI; creating the PR is the primary responsibility. Never fabricate CI success.

Produce the completion output defined in `SKILL.md`, then finish with exactly one of:

**Development PR created. Awaiting code review.**

**Development PR not created. Resolve the items above before retrying.**

## Preparation ledger

Keep a compact ledger through the run containing: the Jira evidence read, the release-branch candidates and the evidence that selected one, the classification decision for each changed path, the checks executed and their real results, the staged path list, the commit SHA, the push result, the PR URL, and the observed CI state.

Use it to build an honest report and to avoid claiming any state that was not actually observed.
