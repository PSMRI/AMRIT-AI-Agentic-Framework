# Branch and Commit Guidelines

## Contents

- [Repository conventions come first](#repository-conventions-come-first)
- [Branch naming](#branch-naming)
- [Normalizing the description](#normalizing-the-description)
- [Bug branches](#bug-branches)
- [Checking for an existing branch](#checking-for-an-existing-branch)
- [Branches to never write to](#branches-to-never-write-to)
- [Commit message](#commit-message)
- [Commit hygiene](#commit-hygiene)
- [Multi-repository naming](#multi-repository-naming)

## Repository conventions come first

Inspect the repository before applying anything in this document:

- existing local and remote branch names;
- recent commit messages in the target release branch's history;
- `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, and developer documentation;
- any commit-message hook, template, or lint configuration such as commitlint.

Where the repository has an established convention, follow it. The formats below are fallbacks for when no convention is evident, not a standard to impose on a repository that already has one.

## Branch naming

The Jira issue key must be present in the branch name. It is the traceability link between the branch, the commit, the Pull Request, and the ticket.

Default format:

```text
feature/ABC-123-short-description
```

Example:

Jira `AMRIT-1234 Add beneficiary search filters` becomes:

```text
feature/AMRIT-1234-beneficiary-search-filters
```

Requirements:

- the Jira key appears exactly as Jira spells it, including its case;
- the description derives from the Jira summary, not from the diff or a guess;
- the name is short enough to read in a branch list and a PR header.

## Normalizing the description

From the Jira summary:

- lowercase the words;
- drop the Jira key from the description portion, since the prefix already carries it;
- replace spaces and underscores with single hyphens;
- remove punctuation that has no meaning in a ref name, including quotes, brackets, colons, commas, and slashes;
- drop filler words when the name would otherwise be unwieldy, keeping the distinctive terms;
- collapse repeated hyphens and trim leading and trailing hyphens;
- keep the whole branch name concise, typically well under 60 characters.

Never let normalization produce a name that no longer describes the change, and never abbreviate so aggressively that the branch becomes unrecognizable.

## Bug branches

Use the repository's established convention for bug work. Where the repository explicitly distinguishes bug branches:

```text
bugfix/ABC-123-short-description
```

Do not impose `bugfix/` on a repository that uses `feature/` for all development work, and do not invent a third prefix. When the repository shows no distinction, use the same prefix it uses for everything else.

## Checking for an existing branch

Before creating a branch, check whether:

- the intended branch name already exists locally;
- the intended branch name already exists on the remote;
- any other branch already references this Jira key.

If an appropriate branch exists, validate it before continuing on it:

- what base it was created from;
- whether it already contains this implementation or something else;
- whether it has an open Pull Request already;
- whether its remote state diverges from the local state.

Continue on a valid existing branch rather than creating a near-duplicate. If the existing remote branch contains unknown work, stop and ask rather than reusing or overwriting it.

## Branches to never write to

Never commit to, push to, or otherwise write directly to:

- `release-X.Y.Z`;
- `main`;
- `master`;
- `develop`;
- any other protected or shared integration branch.

These are Pull Request targets, not working branches.

## Commit message

Follow the repository's convention first. When none is evident, use:

```text
AMRIT-1234: Add beneficiary search filters
```

A good message:

- carries the Jira key for traceability;
- summarizes what the change does, in the imperative or the repository's prevailing style;
- describes the implemented change rather than restating the ticket;
- stays within the repository's subject-line length habit;
- adds a body only when the change genuinely needs context beyond the subject.

Do not:

- write empty messages such as `changes`, `fix`, `updates`, `wip`, or `final`;
- impose Conventional Commits (`feat:`, `fix:`) on a repository that does not use them;
- paste the full Jira description, the acceptance criteria, or the diff into the message;
- include a secret, token, credential, internal URL with embedded authentication, or personal data;
- claim review, approval, or merge status in the message.

## Commit hygiene

- Create one new commit for the staged, reviewed implementation. A second commit is acceptable only when the repository's convention clearly separates concerns such as schema and application code within the same repository.
- Do not amend a commit that already exists on the branch from other work.
- Do not rebase, reset, or otherwise rewrite history that has been pushed or that another developer may hold.
- Do not squash the branch's existing commits. Squashing belongs to the reviewer's merge step.
- Record the real resulting SHA for the report; never invent or approximate one.

## Multi-repository naming

When one ticket legitimately requires changes in an application repository and in `AMRIT-DB`:

- use the same Jira key in both branch names;
- keep each branch name descriptive of that repository's part of the change;
- determine each repository's own correct release branch independently;
- keep the commits in their own repositories, never combined.

Example shape, using a fictional key:

```text
AMRIT-API   feature/DEMO-5140-beneficiary-search-filters
AMRIT-DB    feature/DEMO-5140-beneficiary-search-index
```

Cross-reference the two Pull Requests in their descriptions once their real URLs exist. Never invent a related PR URL.
