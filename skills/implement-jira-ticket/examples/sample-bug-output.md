# Fictional Sample Bug Output

This example is fictional. It shows the shape of the orchestration report for the fictional Bug in [sample-bug-input.md](sample-bug-input.md), routed as a backend-only change with a partially implemented criterion. The repository, paths, and classes are invented and do not describe real AMRIT architecture.

---

## Implementation Summary

Jira: DEMO-5288 — Status filter is ignored beyond the first page of the demo request list

### Repositories inspected

- Demo-Request-API (fictional) — query builder, list service, existing paging and sort tests
- Demo-Request-UI (fictional) — inspected only to confirm the client already sends the filter on every page request; no change required

### Knowledge sources consulted

- Jira — full issue, four acceptance criteria, the linked paging change `DEMO-5240`
- Confluence — no applicable page found for this defect
- DeepWiki — list and paging flow of the fictional request module
- Source code — the query builder, the count query path, and the existing paging tests

### Personas selected

- Backend Developer — the defect lives in the server-side query construction
- SDET — the defect requires a regression test and the changed behaviour needs coverage

Considered and excluded: Frontend (the client already sends the filter correctly; the defect is server-side), DBA (no schema object changes; the fix is in query construction), Android (the mobile applications do not use this list endpoint), Technical Architect (no contract, boundary, or ownership change), UX (no user-visible design change; the visible symptom is fixed by the backend correction).

### Specialist skills executed

- implement-backend-change
- write-unit-tests

### Requirements implemented

- AC1 — Implemented. The status predicate is applied to the list query for every page, not only the first.
- AC2 — Implemented. The count query now applies the same predicate, so the total reflects the filtered set.
- AC3 — Implemented. An empty filter continues to omit the predicate; covered by an added test.
- AC4 — Partially implemented: the existing sort behaviour is unchanged and covered by the existing sort tests, but the module's integration test suite that exercises sort-plus-filter across pages could not be executed in this environment because it requires a database container that is not available. The behaviour was verified at unit level only.

### Root cause

The fictional paging change in `DEMO-5240` moved predicate construction inside an offset check in the query builder, so the status predicate was applied only when the offset was zero. The count query never received the predicate.

### Files changed

Repository: Demo-Request-API (fictional)

- `src/main/java/org/example/demo/request/repository/DemoRequestQueryBuilder.java`: moved predicate construction out of the offset branch so filters apply to every page; the count query now uses the same predicate builder as the list query.
- `src/main/java/org/example/demo/request/service/DemoRequestListService.java`: passed the same filter object to the count call that the list call receives.

No UI change was required. No unrelated file was modified. No API contract changed.

### Database impact

No database schema changes required.

### Tests

Added/updated:
- `DemoRequestQueryBuilderTest#appliesStatusPredicateOnSecondPage` — regression test; confirmed failing against the unfixed builder before the change and passing after it.
- `DemoRequestQueryBuilderTest#countAppliesStatusPredicate`
- `DemoRequestListServiceTest#emptyFilterReturnsUnfilteredList`
- `DemoRequestListServiceTest#passesSameFilterToListAndCount`

No existing test was weakened or removed.

Executed:
- `mvn -Dtest=DemoRequestQueryBuilderTest test` — PASS
- `mvn -Dtest=DemoRequestListServiceTest test` — PASS
- `mvn -pl demo-request test` — PASS
- `mvn -pl demo-request checkstyle:check` — PASS

### Verification

- Unit tests: PASS
- Lint: PASS (Checkstyle)
- Static analysis: NOT RUN — the repository's static-analysis profile requires a Sonar token that is not configured in this environment.
- Build: PASS (`mvn -pl demo-request -am package -DskipTests`)
- Module integration tests: NOT RUN — require a database container unavailable in this environment.

### Architecture deviation

None.

### Remaining issues

- The sort-plus-filter integration test for AC4 must be run in an environment with the module's test database before PR review.

### Next skill

create-development-pr

---

**Implementation incomplete. Resolve the items above before PR preparation.**

No branch, commit, push, or Pull Request was created, the Jira issue was not modified, and no code-review, QA, or CI approval was claimed.
