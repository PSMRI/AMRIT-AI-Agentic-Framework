# Pull Request Guidelines

## Contents

- [Inspect before writing](#inspect-before-writing)
- [Repository PR templates win](#repository-pr-templates-win)
- [PR title](#pr-title)
- [Fallback description structure](#fallback-description-structure)
- [Acceptance criteria mapping](#acceptance-criteria-mapping)
- [Database changes section](#database-changes-section)
- [Verification section](#verification-section)
- [Notes section](#notes-section)
- [Claims that are not permitted](#claims-that-are-not-permitted)
- [Base and head branches](#base-and-head-branches)
- [Duplicate Pull Requests](#duplicate-pull-requests)
- [When GitHub write access is unavailable](#when-github-write-access-is-unavailable)
- [CI reporting](#ci-reporting)

## Inspect before writing

Before drafting the title or description, inspect:

- the Jira issue, including its summary, description, and acceptance criteria;
- the final committed diff, not the intended change;
- the checks that were actually executed and their real results;
- the database impact and any `AMRIT-DB` dependency;
- any repository PR template, label convention, reviewer convention, or checklist under `.github/`.

Every statement in the description must be supported by one of these.

## Repository PR templates win

If the repository contains `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`, or a template directory such as `.github/PULL_REQUEST_TEMPLATE/`, follow it.

- Fill the template's own sections with evidence-backed content.
- Keep its headings, ordering, and checklists.
- Leave a checklist item unchecked when it is not genuinely satisfied, and say why if the template expects an explanation.
- Do not delete template sections that the repository intends reviewers to see. Mark a section not applicable rather than removing it.
- Add a section beyond the template only when it carries information reviewers need and the template has nowhere to put it.

Do not replace a repository's PR conventions with the generic structure below.

## PR title

Follow the repository's title convention first. When none is evident:

```text
AMRIT-1234: Add beneficiary search filters
```

Requirements:

- the Jira key is present;
- the title is concise and descriptive;
- it aligns with the Jira summary;
- it reflects what the diff actually implements, and claims nothing beyond it;
- it does not include status words such as "done", "final", "approved", or "ready to merge".

## Fallback description structure

Use this only when no stronger repository template exists. Include a section only when the evidence supports it, and delete a section that would be empty.

```markdown
## Jira

AMRIT-1234 — Add beneficiary search filters

## Summary

Briefly explain what changed and why.

## Changes

- Added ...
- Updated ...
- Added/updated unit tests for ...

## Acceptance Criteria

- [x] AC1 — ...
- [x] AC2 — ...
- [ ] AC3 — ... <only if genuinely incomplete>

## Database Changes

No database schema changes.

## Verification

- Unit tests: PASS — `<actual command>`
- Lint: PASS — `<actual command>`
- Build: PASS — `<actual command>`
- Static analysis: NOT RUN — <reason>

## Notes

Any compatibility, rollout, dependency, reviewer, or environment notes that are actually relevant.
```

Keep the description reviewable: a reviewer should learn what changed, what proves it, and what to watch for, without reading the diff first.

## Acceptance criteria mapping

Map each criterion against the actual implementation, not against Jira's list:

- check a criterion only when the committed diff genuinely satisfies it;
- leave a criterion unchecked and explain the gap when it is only partly implemented;
- note explicitly when a criterion was inferred because the ticket had no formal criteria;
- state when a criterion is satisfied by another repository's Pull Request, and reference that PR only when its real URL exists.

If a material criterion is unimplemented, the correct action is to stop and return to implementation, not to open a PR with an unchecked box.

## Database changes section

When there is no schema change:

```markdown
## Database Changes

No database schema changes.
```

When the change depends on `AMRIT-DB`:

```markdown
## Database Changes

Schema changes required.

AMRIT-DB PR: <link if available>

- Added ...
- Updated ...
```

Never describe an application-local migration as the authoritative schema change, and never invent a link for the `AMRIT-DB` Pull Request. If the related PR does not exist yet, say so plainly and state the dependency.

## Verification section

List only commands that actually ran, with their real outcome:

```text
- Unit tests: PASS — `mvn -Dtest=BeneficiarySearchServiceTest test`
- Lint: PASS — `npm run lint`
- Build: PASS — `mvn -pl beneficiary -am package -DskipTests`
- Static analysis: NOT RUN — repository Sonar check requires a server token that is not configured in this environment
```

Rules:

- PASS requires an actual successful execution;
- FAILED must state what failed and why the PR is still appropriate, which normally means only a draft PR under an explicit repository policy;
- `NOT RUN — <reason>` is the honest answer for any check blocked by the environment;
- never aggregate into "all tests pass";
- never present a previous agent's claim as an executed check.

## Notes section

Include only genuinely relevant notes, such as:

- backward-compatibility impact and API contract changes;
- configuration or feature-flag requirements;
- deployment ordering, especially against an `AMRIT-DB` dependency;
- data migration or backfill considerations;
- specific areas where reviewer attention is most valuable;
- known limitations that are in scope for a follow-up ticket.

Omit the section when there is nothing real to say.

## Claims that are not permitted

Never write, in the title, description, or report:

- "all tests pass" unless every listed check actually ran and passed;
- "CI green" or "CI passing" unless that state was retrieved from GitHub;
- "reviewed", "code review complete", or any reviewer name as an approver;
- "approved" or "self-approved";
- "ready to merge", "merged", or "squash-merged";
- "Sr Dev sign-off obtained";
- "Jira moved to Done" or any other Jira state change.

The skill has no authority over any of these.

## Base and head branches

- Base is the validated `release-X.Y.Z` branch determined earlier. Never open the PR against `main`, `master`, or `develop` unless repository policy explicitly requires it for this ticket.
- Head is the Jira-specific development branch that was pushed.
- Confirm both refs exist on the remote before creating the PR.
- Record both in the completion report.

## Duplicate Pull Requests

Before creating a PR, check where practical whether one already exists for the same head branch or the same Jira key. If an appropriate open PR exists:

- report its URL, title, base, and head;
- state that the new commit has been pushed to the existing PR's branch when that is what happened;
- do not create a second PR for the same change.

## When GitHub write access is unavailable

If no authenticated GitHub PR-creation capability is available:

- complete only the safe local preparation that has already been justified;
- do not fabricate a PR URL, PR number, or CI state;
- report exactly what exists locally and remotely, including the branch and commit;
- provide the intended title and description so the developer can open the PR manually;
- finish with **Development PR not created. Resolve the items above before retrying.**

## CI reporting

After creation, inspect checks or statuses when the capability supports it, and report only observed state:

```text
CI: pending
CI: 5/5 checks passed
CI: 1 check failed — <name>
CI: status unavailable
```

The Stage 05 exit criterion requires green CI, but this skill does not wait indefinitely for it. Report the observed state and list green CI among the remaining requirements when it is still pending.
