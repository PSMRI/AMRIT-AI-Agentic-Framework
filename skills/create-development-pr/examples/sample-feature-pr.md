# Fictional Sample Feature PR

This example is fictional. The Jira key, repository, branches, commit SHA, Pull Request URL, and CI state are invented and do not describe real AMRIT tickets, repositories, or Pull Requests. Use it only as a shape reference.

## Fictional input

```text
/create-development-pr DEMO-5140
```

Fictional Jira issue:

- Key: `DEMO-5140`
- Type: Story
- Summary: Add closure note to request completion
- Fix Version: `3.2.0`
- Component: Request Management
- Acceptance criteria:
  - AC1 — The completion request accepts an optional note of up to 500 characters.
  - AC2 — A note over 500 characters is rejected and the request keeps its prior status.
  - AC3 — The stored note is visible on the reopened request detail.
  - AC4 — Completing without a note behaves exactly as before.

Fictional repository state before the run:

- Repository root: `Demo-Request-API`
- Current branch: `release-3.2.0`
- Modified: four Java source files, one test file
- Untracked: `notes.txt`, `target/classes/DemoRequestCompletionService.class`
- Remote `release-*` branches: `release-3.1.4`, `release-3.2.0`

## Fictional decision trace

- **Release branch** — the ticket's Fix Version `3.2.0` matched the existing remote branch `release-3.2.0`. `release-3.1.4` was rejected because the Fix Version identified the target unambiguously. No question was needed.
- **Ancestry** — the work was uncommitted on `release-3.2.0` itself, so the development branch was created from the current state and the implementation carried over. No rebase, reset, or stash was used.
- **Branch name** — derived from the Jira summary: `feature/DEMO-5140-closure-note-on-completion`. No existing local or remote branch referenced `DEMO-5140`.
- **Change classification** — the four source files and the test file were ticket-related. `notes.txt` and the compiled class under `target/` were excluded: one is unrelated user work left untouched in the working tree, the other is an ignored build output.
- **Diff review** — one leftover `log.debug("note=" + note)` line was removed as a mechanical PR-preparation correction. No other code was changed.
- **Database** — no schema change; the `closure_note` column already existed.

## Fictional completion output

---

## Development PR Created

### Jira

DEMO-5140 — Add closure note to request completion

### Repository

Demo-Request-API (fictional)

### Branches

Base: `release-3.2.0`

Head: `feature/DEMO-5140-closure-note-on-completion`

### Commit

`a1b2c3d` — `DEMO-5140: Add optional closure note to request completion`

### Pull Request

Title: `DEMO-5140: Add optional closure note to request completion`

URL: https://github.com/example-org/demo-request-api/pull/412 (fictional)

### Verification

- Unit tests: PASS — `mvn -Dtest=DemoRequestCompletionServiceTest test`
- Module tests: PASS — `mvn -pl demo-request test`
- Lint: PASS — `mvn spotless:check`
- Static analysis: NOT RUN — the repository's Sonar check requires a server token that is not configured in this environment
- Build: PASS — `mvn -pl demo-request -am package -DskipTests`

### Database Impact

No schema changes.

### CI

CI: pending — 3 checks queued at PR creation.

### Remaining Stage 04 Requirements

- Code review by Senior Developer
- Required approval(s)
- Green CI if still pending
- Squash merge into `release-3.2.0`

---

**Development PR created. Awaiting code review.**

Not staged or committed: `notes.txt` (unrelated user work, left in the working tree) and `target/classes/DemoRequestCompletionService.class` (ignored build output). No Jira field was modified, and no approval or merge was performed or claimed.

## Fictional PR description that was submitted

```markdown
## Jira

DEMO-5140 — Add closure note to request completion

## Summary

Completion of a request can now carry an optional reviewer note, persisted with
the existing completion transaction and shown on the reopened request detail.

## Changes

- Mapped the existing `closure_note` column onto the request entity.
- Added the optional `closureNote` field to the completion request DTO with the
  module's existing 500-character constraint.
- Exposed `closureNote` additively on the detail response.
- Persisted the note inside the existing completion transaction; no transaction
  boundary or status-transition rule changed.
- Added unit tests for the note, the over-limit rejection, and the no-note path.

## Acceptance Criteria

- [x] AC1 — Optional 500-character note accepted on completion.
- [x] AC2 — Over-limit note rejected by the existing validation boundary; status unchanged.
- [x] AC3 — Stored note returned in the detail response and rendered on reopen.
- [x] AC4 — Completion without a note follows the prior path; covered by a regression test.

## Database Changes

No database schema changes. The `closure_note` column already exists with a
500-character limit; only entity mapping and application validation changed.

## Verification

- Unit tests: PASS — `mvn -Dtest=DemoRequestCompletionServiceTest test`
- Module tests: PASS — `mvn -pl demo-request test`
- Lint: PASS — `mvn spotless:check`
- Build: PASS — `mvn -pl demo-request -am package -DskipTests`
- Static analysis: NOT RUN — Sonar server token not configured in this environment

## Notes

The response change is additive, so existing clients are unaffected. Reviewer
attention is most useful on the transaction boundary in
`DemoRequestCompletionService`.
```
