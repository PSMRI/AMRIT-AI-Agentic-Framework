# Fictional Sample Database-Dependent PR

This example is fictional. The Jira key, repositories, branches, commit SHAs, Pull Request URLs, and CI states are invented and do not describe real AMRIT tickets, repositories, or Pull Requests. Use it only as a shape reference.

It shows two situations that the skill must handle differently:

1. a required `AMRIT-DB` change is **missing**, so no PR is created;
2. the change legitimately spans two repositories, so two Pull Requests are prepared.

## Scenario A — required schema change is missing

### Fictional input

```text
/create-development-pr DEMO-7310
```

Fictional Jira issue:

- Key: `DEMO-7310`
- Type: Story
- Summary: Store referral outcome against each referral
- Fix Version: `5.0.0`

Fictional repository state:

- Repository root: `Demo-Referral-API`
- Modified: entity, DTO, service, and test files that read and write a `referral_outcome` column
- The column does not exist in the schema
- The change set also contains `src/main/resources/db/migration/V42__add_referral_outcome.sql`, added in the application repository
- `AMRIT-DB` is checked out alongside and contains no corresponding change

### Fictional decision trace

- **Database classification** — a real schema change: a new column with a constraint.
- **Placement** — the migration was added inside the application repository. Authoritative AMRIT schema changes belong in `AMRIT-DB`. Committing the application-local migration would move schema ownership for convenience and produce a PR that implies a complete implementation.
- **Action** — stop. Nothing was staged, committed, or pushed. The application-local migration file was left untouched in the working tree for the developer to move; it was not deleted.

### Fictional completion output

---

## Development PR Not Created

### Jira

DEMO-7310 — Store referral outcome against each referral

### Repository

Demo-Referral-API (fictional)

### Reason

The implementation requires a new `demo_referral.referral_outcome` column. The
change set places that schema change in the application repository at
`src/main/resources/db/migration/V42__add_referral_outcome.sql`, and the
`AMRIT-DB` working copy contains no corresponding change.

Authoritative AMRIT schema changes belong in `AMRIT-DB`. Creating this PR would
imply a complete implementation that the schema does not support.

### What was done

- Jira issue read (read-only).
- Repository state and full diff inspected.
- Target release branch identified as `release-5.0.0` and confirmed on the remote.

### What was not done

- No branch created.
- No files staged.
- No commit.
- No push.
- No Pull Request.
- The application-local migration file was left in the working tree, untouched.

### Required before retrying

1. Implement the `referral_outcome` schema change in `AMRIT-DB`, following its
   existing migration conventions.
2. Remove the application-local migration from `Demo-Referral-API`.
3. Confirm the application persistence code matches the `AMRIT-DB` schema.

Run `implement-jira-ticket` again or resolve the implementation issues first.

---

**Development PR not created. Resolve the items above before retrying.**

## Scenario B — a legitimate two-repository change

### Fictional input

```text
/create-development-pr DEMO-7311
```

Fictional Jira issue:

- Key: `DEMO-7311`
- Type: Story
- Summary: Index referral search by facility
- Fix Version: `5.0.0`

Fictional repository state:

- `Demo-Referral-API` — modified query and repository classes plus tests, based on `release-5.0.0`
- `AMRIT-DB` — a new index migration following its own conventions, based on its own `release-5.0.0`
- Both repositories have a remote `release-5.0.0`

### Fictional ambiguity that required a question

Two repositories needed Pull Requests, and the deployment order mattered: the index must exist before the application query relies on it. Repository documentation did not state an ordering policy for paired PRs.

The run stopped and asked:

```text
DEMO-7311 requires Pull Requests in two separate repositories:

- AMRIT-DB — new index migration, base release-5.0.0
- Demo-Referral-API — query change that depends on that index, base release-5.0.0

These are separate Git repositories, so they cannot share one PR. The index must
exist before the application query relies on it, and the repository
documentation does not state an ordering policy for paired PRs.

How should this proceed?

  a) Create both PRs now and cross-reference the dependency in each description.
  b) Create only the AMRIT-DB PR now, and the application PR after it merges.
  c) Prepare both locally and let you open them.

Nothing has been staged, committed, or pushed in either repository.
```

The developer chose (a). The run then processed each repository independently.

### Fictional completion output

---

## Development PR Created

### Jira

DEMO-7311 — Index referral search by facility

### Repositories

Two Pull Requests were created, one per repository, at the developer's
direction. The repositories are independent, so their commits are not combined.

### AMRIT-DB

Base: `release-5.0.0`

Head: `feature/DEMO-7311-referral-facility-index`

Commit: `9c8b7a6` — `DEMO-7311: Add referral facility search index`

Pull Request: https://github.com/example-org/amrit-db/pull/74 (fictional)

### Demo-Referral-API

Base: `release-5.0.0`

Head: `feature/DEMO-7311-referral-facility-search`

Commit: `3d2e1f0` — `DEMO-7311: Use facility index for referral search`

Pull Request: https://github.com/example-org/demo-referral-api/pull/519 (fictional)

### Verification

`AMRIT-DB`:

- Migration lint: PASS — `python scripts/check_migrations.py`
- Unit tests: NOT RUN — the repository has no unit-test suite for migrations

`Demo-Referral-API`:

- Unit tests: PASS — `mvn -Dtest=ReferralSearchRepositoryTest test`
- Lint: PASS — `mvn spotless:check`
- Static analysis: NOT RUN — Sonar server token not configured in this environment
- Build: PASS — `mvn -pl referral -am package -DskipTests`

### Database Impact

`AMRIT-DB` changes are part of a separate repository and Pull Request.

Related PR: https://github.com/example-org/amrit-db/pull/74 (fictional)

- Added a composite index on `demo_referral(facility_id, referred_at)`.

### CI

`AMRIT-DB` — CI: 2/2 checks passed.

`Demo-Referral-API` — CI: pending, 4 checks queued at PR creation.

### Remaining Stage 04 Requirements

- Code review by Senior Developer on both Pull Requests
- Required approval(s) on both Pull Requests
- Green CI on `Demo-Referral-API` if still pending
- `AMRIT-DB` squash merge into its `release-5.0.0` before the application merge
- `Demo-Referral-API` squash merge into `release-5.0.0`

---

**Development PR created. Awaiting code review.**

The merge ordering above reflects the technical dependency, not an approval. No
Jira field was modified, and neither Pull Request was approved or merged.

### Fictional cross-references in the two descriptions

In the `Demo-Referral-API` description:

```markdown
## Database Changes

Schema changes required.

AMRIT-DB PR: https://github.com/example-org/amrit-db/pull/74

- Added a composite index on `demo_referral(facility_id, referred_at)`.

## Notes

This PR depends on the AMRIT-DB index above. The index must be merged and
applied before this query change is deployed.
```

In the `AMRIT-DB` description:

```markdown
## Notes

Supports DEMO-7311. The consuming application change is in
https://github.com/example-org/demo-referral-api/pull/519 and depends on this
index being applied first.
```

A related PR URL is written only after that Pull Request actually exists. It is never invented in advance.
