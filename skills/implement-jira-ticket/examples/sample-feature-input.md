# Fictional Sample Feature Input

This example is fictional. The keys, modules, classes, endpoints, and documents below are invented for illustration only and do not describe a real AMRIT deployment, repository, or architecture.

## Invocation

```text
/implement-jira-ticket DEMO-5140
```

## Fictional Jira issue DEMO-5140

- Type: Story
- Summary: Allow a reviewer to add a closure note when completing a demo request
- Parent Epic: `DEMO-5100` — Demo request closure workflow
- Components: Demo Request module
- Labels: `demo-closure`
- Status: Ready for Development
- Priority: Medium

### Description

Reviewers currently complete a demo request without recording why it was closed. The closure screen should accept an optional note, store it against the request, and display it when the request is reopened.

### Acceptance criteria

1. An authorized reviewer can enter an optional closure note of up to 500 characters when completing a demo request.
2. A note longer than 500 characters is rejected with a validation error and the request is not completed.
3. The stored note is returned with the request detail and shown when the request is reopened.
4. Completing a request without a note continues to work exactly as before.

### Linked issues

- `DEMO-5101` — Closure screen layout (Done)
- `DEMO-5139` — Reviewer permission model (Done)

### Comments carrying decisions

- Reviewer lead, 3 March 2026: "No new permission. The existing completion permission is sufficient."
- Architect, 5 March 2026: "The column already exists from the pilot; this is an application-side change only."

### Linked Confluence page

- `Demo Request Closure — Functional Specification` (fictional)

## Fictional Confluence evidence

`Demo Request Closure — Functional Specification`, version 4:

- The closure note is optional and free text.
- The note is not shown to the requester, only to reviewers.
- No notification is sent when a note is added.
- Existing completion validation rules are unchanged.

No BRD exists for this Story. The functional specification is the approved requirement evidence.

## Fictional repository evidence

Retrieved through repository research and confirmed by direct inspection of the checked-out source:

- `demo_request.closure_note` already exists and is nullable with a 500-character limit.
- The request entity and detail DTO do not currently map the column.
- The completion service validates status transitions and delegates persistence to the request repository.
- The closure screen posts to the existing completion endpoint.
- Unit tests for the completion service already exist and use the repository's established mocking helpers.

## Explicit constraints

- No new endpoint.
- No new permission.
- No database schema change — the column already exists.
- No notification, queue, or scheduler.
