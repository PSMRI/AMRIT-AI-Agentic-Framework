# Fictional Sample Story Input

This example is fictional. Names, keys, contracts, and architecture below are supplied evidence for the example only; they do not describe a real AMRIT deployment.

## Backlog approval

- Epic: `DEMO-4800` — Post-consultation continuity workflow
- Product Manager approval recorded: 14 July 2026
- Engineering Analysis authorized for Stories `DEMO-4821` and `DEMO-4822`

## Story DEMO-4821 — Schedule a beneficiary follow-up

As a Medical Officer, I want to schedule a follow-up while closing a teleconsultation case so that the care team can continue the advised care pathway.

### Acceptance criteria

1. An authorized Medical Officer can select a follow-up date and time from the case-closure screen.
2. Follow-up date and time must be later than the consultation completion time and no more than 30 days later.
3. A validation failure must not close the case or partially save the follow-up.
4. The saved follow-up is visible when the case is reopened.
5. The audit history records the actor, timestamp, case identifier, and change type without duplicating clinical notes.

## Story DEMO-4822 — Update a scheduled follow-up

As an authorized care-team user, I want to reschedule or clear a pending follow-up so that the case reflects the agreed next action.

### Acceptance criteria

1. Only users with the existing `CASE_FOLLOW_UP_MANAGE` permission can change the follow-up.
2. A completed or cancelled case cannot be rescheduled.
3. Two users updating the same case must not silently overwrite each other.
4. Existing integrations that read case details must remain compatible.

## Approved BRD/FRD evidence

`BRD-DEMO-17`, approved:

- Follow-up is optional.
- No new notification or outbound integration is in scope.
- Existing case access rules continue to apply.
- Reporting changes are outside this release.

`FRD-DEMO-17`, approved:

- Reuse the existing case-closure workflow.
- Store the follow-up timestamp against the case.
- Use the case's existing optimistic version for concurrent edits.
- Preserve existing case-detail consumers.

## Fictional Confluence evidence

`Case Management — Current Architecture`, version 6:

- The Case UI calls the Case API.
- The Case API delegates case lifecycle rules to the Case Application Service.
- The Case Repository owns writes to the `case_record` table.
- Audit events are recorded through the shared Audit Service.

`Case Closure Validation Standard`, version 3:

- The server remains the authoritative owner of lifecycle validation.
- The UI may repeat validation for immediate feedback.
- Validation conflicts use the platform's standard conflict error.

## Fictional OpenAPI evidence

`Case API`, version `1.8`:

- `PATCH /v1/cases/{caseId}` accepts optional `followUpAt` and required `version`.
- `GET /v1/cases/{caseId}` returns optional `followUpAt` and `version`.
- The patch operation documents `400`, `403`, `404`, and `409` responses.
- `followUpAt` is an ISO 8601 timestamp with offset.

## Fictional supplied repository evidence

This evidence is a supplied read-only export. The example does not assume DeepWiki availability.

- `case_record.follow_up_at` already exists and is nullable.
- `case_record.row_version` is used for optimistic concurrency.
- The case detail DTO and repository mapping already include `followUpAt`.
- The closure UI does not currently expose the field.
- The application service accepts the field but does not enforce the 30-day maximum.
- Existing audit infrastructure can record a `FOLLOW_UP_CHANGED` event type.

## Fictional Jira research

- `DEMO-3901` previously added `follow_up_at` for a pilot; status Done.
- `DEMO-4710` proposes SMS reminders; status Deferred and explicitly outside the current Epic.
- No duplicate active implementation Story was found after searches for follow-up, callback, reschedule, and `follow_up_at`.

## Explicit constraints

- No database schema change.
- No new endpoint.
- No SMS, email, queue, or scheduler.
- No implementation code is requested.
