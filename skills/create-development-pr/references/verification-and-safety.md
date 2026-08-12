# Verification and Safety

## Contents

- [Purpose](#purpose)
- [Protecting the working tree](#protecting-the-working-tree)
- [Commands that are never run](#commands-that-are-never-run)
- [Discovering verification commands](#discovering-verification-commands)
- [Running checks](#running-checks)
- [Reporting check results](#reporting-check-results)
- [Failing checks](#failing-checks)
- [Secret screening](#secret-screening)
- [Files that must never be committed](#files-that-must-never-be-committed)
- [Push safety](#push-safety)
- [Authentication failures](#authentication-failures)
- [Scope discipline](#scope-discipline)
- [Stop conditions](#stop-conditions)

## Purpose

Guarantee that nothing is committed that should not be, nothing is lost that belongs to the user, and nothing is claimed that was not observed.

## Protecting the working tree

The repository may contain the ticket's implementation alongside unrelated user work, debug files, temporary files, generated files, local configuration, environment files, and secrets. Treat every uncommitted change as the user's property.

- Inspect and classify before staging. See Step 3 of [git-workflow.md](git-workflow.md).
- Stage explicit paths. Do not use `git add .` or `git add -A` unless every included path has been established as ticket-related and safe.
- Leave unrelated work uncommitted and unmodified.
- Correct wrong staging by unstaging, never by discarding content.
- Never delete, revert, or overwrite a file to make the tree simpler.
- Never hide unrelated work in a stash the user did not ask for.

If ticket-related and unrelated changes are entangled such that safe staging cannot be determined, stop and describe the conflict, naming the affected paths.

## Commands that are never run

Do not run these to simplify the working tree, resolve a conflict, or make a check pass:

```text
git reset --hard
git clean -fd
git checkout --force
git stash drop
git push --force
```

`git push --force` is permitted only when the user explicitly requests it and the repository context makes it safe. The others are never appropriate in this skill.

## Discovering verification commands

Discover the repository's real commands rather than assuming them. Inspect:

- `pom.xml`, `build.gradle`, or `build.gradle.kts` for Java projects;
- `package.json` scripts for JavaScript and TypeScript projects;
- `Makefile` or equivalent task runners;
- lint, formatting, checkstyle, and static-analysis configuration;
- CI workflow files under `.github/workflows/`, which show what the repository will run against the PR;
- `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, and developer documentation.

The repository's CI workflow is the best predictor of which checks matter for this PR.

## Running checks

Run the narrowest relevant checks first, then broaden where practical:

1. unit tests for the changed modules or files;
2. wider module or package tests;
3. lint;
4. formatting or checkstyle;
5. type checking;
6. static analysis;
7. compilation or build;
8. package verification.

Do not start destructive infrastructure, and never touch production or shared environments to run a check.

## Reporting check results

Use exactly these outcomes:

- **PASS** — the command actually ran in this session and succeeded. Always name the command.
- **FAILED** — the command ran and failed. State what failed.
- **NOT RUN — `<reason>`** — the check could not run because of an environmental limitation, a missing token, a missing service, or an unavailable toolchain.

A previous agent's statement that tests passed is not verification. Do not carry it forward as PASS.

Never aggregate results into "all tests pass", and never report a check that was not executed.

## Failing checks

When a check fails, first determine the cause:

- **caused by the implementation** — this is an implementation problem. Stop before creating the PR and report it, unless repository policy explicitly permits a draft PR for failing checks. Return the work to implementation.
- **pre-existing on the release base** — verify it against the base where practical, report it as pre-existing, and continue.
- **environmental** — report it as `NOT RUN — <reason>` or as a failure with its environmental cause, and continue only if the check is not a required gate.

Never weaken or delete a test, relax an assertion, disable a lint rule, add a suppression, skip static analysis, or edit CI configuration to turn a check green. Any of those is an out-of-scope change and a misrepresentation of the implementation's state.

## Secret screening

Screen the intended diff for secrets twice: before committing, and again before pushing.

Look for:

- `.env` files and environment credential values;
- API keys, access tokens, and bearer tokens;
- passwords, including database passwords;
- private keys, certificates, and keystores;
- cloud provider credentials;
- GitHub personal access tokens;
- MCP credentials and private authentication headers;
- connection strings with embedded credentials;
- hardcoded credentials introduced into source or configuration;
- credential values in test fixtures, logs, or committed sample files.

If a secret appears to have been introduced into the intended diff:

- stop;
- do not commit or push it;
- report only the affected file path and the remediation requirement;
- never repeat the secret value in the report, a log, a commit message, or the PR description;
- state that the credential should be treated as exposed if it was already committed earlier in the branch's history, and leave remediation to the developer.

## Files that must never be committed

- `.env` and other environment credential files;
- IDE and editor state, such as `.idea/` and `.vscode/`;
- OS artifacts, such as `.DS_Store` and `Thumbs.db`;
- temporary and scratch files;
- build outputs and generated artifacts the repository intentionally ignores;
- dependency directories such as `node_modules/` or `target/`;
- large binary artifacts;
- local configuration overrides specific to one machine;
- anything unrelated to the ticket.

If one of these appears in the change set, exclude it from staging. Do not delete it from the user's working tree.

## Push safety

Before pushing:

- confirm the branch being pushed is the ticket's development branch;
- confirm the remote is the repository's intended GitHub remote;
- re-screen the outgoing commit for secrets;
- set upstream tracking when required.

Never push to `release-X.Y.Z`, `main`, `master`, `develop`, or another protected or shared branch. Never force-push without explicit user instruction and a safe context.

## Authentication failures

If Git or GitHub authentication or authorization fails:

- report the failure and the operation it blocked;
- do not modify remote URLs to embed a token;
- do not write credentials to a file, a Git config, or an environment variable that persists;
- do not print any credential value, even a partial one;
- do not attempt an alternative unauthenticated route that bypasses repository policy.

Report what completed locally and what the developer must authorize.

## Scope discipline

This skill packages an implementation. It does not build one.

Permitted PR-preparation corrections are only those that are clearly mechanical and low risk:

- removing an accidental debug or print statement;
- removing an obviously stray temporary file from the change set;
- excluding an unintended generated artifact from staging.

Not permitted:

- implementing a missing acceptance criterion;
- fixing a substantive defect;
- adding missing unit tests for changed behaviour;
- refactoring for style;
- changing requirements or acceptance criteria;
- modifying Jira in any way.

When any of those is needed, stop and report:

**Implementation is not ready for PR preparation. Run `implement-jira-ticket` again or resolve the implementation issues first.**

## Stop conditions

Stop and report, or stop and ask, when:

- the Jira issue cannot be retrieved, so traceability cannot be established;
- several plausible `release-X.Y.Z` branches exist and no evidence identifies the right one;
- the selected release branch does not exist on the remote;
- the implementation is based on the wrong branch and moving it safely is non-trivial;
- unrelated changes are entangled with ticket work and safe staging cannot be determined;
- an existing remote branch for the ticket contains unknown work;
- the implementation is materially incomplete or defective;
- a required `AMRIT-DB` schema change is missing;
- an application plus `AMRIT-DB` change set needs multiple PRs and the intended ordering or dependency handling is unclear;
- a required local check fails because of the implementation;
- a secret appears in the intended diff;
- no authenticated GitHub PR-creation capability is available.

In every case, complete the safe work that does not depend on the unresolved question, state exactly what was and was not done, and never guess through the decision.
