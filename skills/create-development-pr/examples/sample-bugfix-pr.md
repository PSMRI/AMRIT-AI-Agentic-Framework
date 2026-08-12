# Fictional Sample Bugfix PR

This example is fictional. The Jira key, repository, branches, commit SHA, Pull Request URL, and CI state are invented and do not describe real AMRIT tickets, repositories, or Pull Requests. Use it only as a shape reference.

It also shows a run that had to **stop and ask** before it could proceed, and then completed after the answer.

## Fictional input

```text
/create-development-pr DEMO-6021
```

Fictional Jira issue:

- Key: `DEMO-6021`
- Type: Bug
- Summary: Duplicate visit records created on double submit
- Fix Version: not set
- Sprint: Sprint 41
- Acceptance criteria:
  - AC1 — A repeated submit within the idempotency window does not create a second visit record.
  - AC2 — The caller receives the original visit identifier on the repeated submit.
  - AC3 — Existing single-submit behaviour is unchanged.

Fictional repository state before the run:

- Repository root: `Demo-Visit-API`
- Current branch: `feature/DEMO-6021-duplicate-visit-on-double-submit`, based on `release-4.1.2`
- Remote `release-*` branches: `release-4.1.2`, `release-4.2.0`
- Repository convention observed in history: bug work uses `bugfix/`, but this branch already existed with the `feature/` prefix
- Working tree: two modified source files, one modified test file, all ticket-related

## Fictional ambiguity that required a question

The Jira ticket had no Fix Version, and both `release-4.1.2` and `release-4.2.0` were plausible: the branch was based on `release-4.1.2`, but Sprint 41's other tickets targeted `release-4.2.0`. Nothing in Jira or the repository resolved it.

The run stopped and asked:

```text
Two release branches are plausible for DEMO-6021 and the evidence does not
identify one:

- release-4.1.2 — the current implementation branch is based on this branch
- release-4.2.0 — the newest release branch on the remote

DEMO-6021 has no Fix Version, and the repository documentation does not state a
default target for defect work.

Which release branch should this PR target?

Nothing has been staged, committed, or pushed. All local changes are intact.
```

The developer answered `release-4.1.2`, matching the existing branch base. The run then continued.

## Fictional decision trace

- **Release branch** — `release-4.1.2`, chosen by the developer after the question. Confirmed to exist on the remote.
- **Ancestry** — the existing branch's merge base was already `release-4.1.2`, so it satisfied the requirement with no history rewrite.
- **Branch name** — the existing `feature/DEMO-6021-duplicate-visit-on-double-submit` branch was reused rather than creating a near-duplicate `bugfix/` branch. Reusing a valid existing branch that already carries the implementation is preferred over renaming it, and the reuse is stated in the report.
- **Change classification** — all three modified files were ticket-related; nothing was excluded.
- **Diff review** — no debug statements, secrets, generated files, or unrelated refactors. No corrections needed.
- **Database** — no schema change; idempotency used an existing unique constraint.

## Fictional completion output

---

## Development PR Created

### Jira

DEMO-6021 — Duplicate visit records created on double submit

### Repository

Demo-Visit-API (fictional)

### Branches

Base: `release-4.1.2` — selected by the developer after the release-branch question

Head: `feature/DEMO-6021-duplicate-visit-on-double-submit` — pre-existing branch, reused

### Commit

`f7e6d5c` — `DEMO-6021: Prevent duplicate visit records on repeated submit`

### Pull Request

Title: `DEMO-6021: Prevent duplicate visit records on repeated submit`

URL: https://github.com/example-org/demo-visit-api/pull/188 (fictional)

### Verification

- Unit tests: PASS — `mvn -Dtest=VisitSubmissionServiceTest test`
- Regression test: PASS — `VisitSubmissionServiceTest#repeatedSubmitReturnsOriginalVisitId` fails against the pre-fix behaviour
- Lint: PASS — `mvn spotless:check`
- Static analysis: PASS — `mvn verify -Ppmd`
- Build: PASS — `mvn -pl visit -am package -DskipTests`

### Database Impact

No schema changes. Idempotency relies on the existing unique constraint on
`demo_visit(beneficiary_id, submitted_at_bucket)`.

### CI

CI: 4/4 checks passed.

### Remaining Stage 04 Requirements

- Code review by Senior Developer
- Required approval(s)
- Squash merge into `release-4.1.2`

---

**Development PR created. Awaiting code review.**

The branch kept its existing `feature/` prefix even though repository history shows `bugfix/` for defect work, because the branch already existed with the implementation on it and renaming a pushed branch was not warranted. Flagged here so the reviewer sees the deviation. No Jira field was modified, and no approval or merge was performed or claimed.

## Fictional PR description that was submitted

```markdown
## Jira

DEMO-6021 — Duplicate visit records created on double submit

## Summary

A repeated visit submission within the idempotency window no longer creates a
second record. The caller now receives the original visit identifier instead of
a new one.

## Changes

- Detected the existing visit inside the submission path before insert, using
  the existing unique constraint rather than a new lookup table.
- Returned the original visit identifier on a repeated submit.
- Added a regression test that fails against the pre-fix behaviour.

## Acceptance Criteria

- [x] AC1 — Repeated submit within the window creates no second record.
- [x] AC2 — Caller receives the original visit identifier.
- [x] AC3 — Single-submit behaviour unchanged; covered by the existing suite.

## Database Changes

No database schema changes.

## Verification

- Unit tests: PASS — `mvn -Dtest=VisitSubmissionServiceTest test`
- Lint: PASS — `mvn spotless:check`
- Static analysis: PASS — `mvn verify -Ppmd`
- Build: PASS — `mvn -pl visit -am package -DskipTests`

## Notes

Targets `release-4.1.2` rather than `release-4.2.0` at the developer's
direction; the ticket carried no Fix Version. The branch keeps its existing
`feature/` prefix although repository history uses `bugfix/` for defect work.
```
