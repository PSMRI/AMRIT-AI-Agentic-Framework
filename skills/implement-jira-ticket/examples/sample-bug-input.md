# Fictional Sample Bug Input

This example is fictional. The keys, modules, classes, and behaviour below are invented for illustration only and do not describe a real AMRIT deployment, repository, or architecture.

## Invocation

```text
Implement DEMO-5288
```

## Fictional Jira issue DEMO-5288

- Type: Bug
- Summary: Demo request list ignores the status filter after paging past the first page
- Parent Epic: `DEMO-5200` — Demo request listing improvements
- Components: Demo Request module
- Labels: `defect`, `l2-escalated`
- Status: Ready for Development
- Priority: High

### Description

A reviewer filters the demo request list by status, then moves to page 2. The second page returns requests of every status. Returning to page 1 shows the filter applied again.

### Steps to reproduce

1. Open the demo request list.
2. Filter by status `PENDING`.
3. Confirm page 1 shows only pending requests.
4. Move to page 2.
5. Page 2 contains requests with other statuses.

### Expected behaviour

Every page of a filtered list contains only requests matching the selected status, and the total count reflects the filter.

### Acceptance criteria

1. The status filter is applied to every page of the result set.
2. The reported total count reflects the filtered result set, not the unfiltered one.
3. Clearing the filter returns the full unfiltered list.
4. Existing sort behaviour is unchanged.

### Comments carrying decisions

- Reviewer lead, 18 March 2026: "Filter values are unchanged; this is only about paging."
- Architect, 19 March 2026: "Server-side defect. Do not work around it in the UI."

### Linked issues

- `DEMO-5240` — Added server-side paging to the demo request list (Done)

## Fictional Confluence evidence

No BRD or FRD exists for this defect. The Epic page `Demo Request Listing` (fictional, version 2) documents that filtering and paging are both server-side responsibilities and that the list endpoint returns a filtered total count.

## Fictional repository evidence

Retrieved through repository research and confirmed by direct inspection of the checked-out source:

- The list query builder applies the status predicate only when the page offset is zero, introduced by the fictional paging change in `DEMO-5240`.
- The count query does not apply the status predicate at all.
- The list service already has unit tests using the repository's established query-builder test helpers.
- The UI passes the filter on every page request, so no UI change is required.

## Explicit constraints

- No database schema change.
- No API contract change.
- No UI workaround.
- The fix must include a regression test that fails against the unfixed behaviour.
