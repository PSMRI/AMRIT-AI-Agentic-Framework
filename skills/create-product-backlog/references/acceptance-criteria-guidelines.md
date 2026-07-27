# Acceptance Criteria Guidelines

## Quality standard

Write criteria that are:

- tied to one Story and its source requirement;
- observable and testable;
- unambiguous about conditions and expected results;
- sufficient to cover important positive and negative behavior;
- free of architecture or implementation choices unless the approved source mandates them.

Use Given/When/Then where it improves clarity:

```text
Given an active user requested a password reset,
When the reset link has exceeded the configured expiry period,
Then the system rejects the link and prevents password modification.
```

## Scenario coverage

Select only source-supported scenarios:

- happy path and intended outcome;
- invalid, expired, missing, or duplicate input;
- boundary values and configured limits;
- permissions and role restrictions;
- state transitions and repeated actions;
- error behavior visible to the actor;
- audit, notification, report, or integration behavior when explicitly required.

For a production defect, include the expected behavior, evidence needed to reproduce, affected environment, and regression boundary without asserting a root cause.

## Avoid

- Vague terms such as "works correctly," "fast," "user-friendly," or "as needed."
- Implementation assumptions such as database tables, service names, APIs, frameworks, or algorithms absent from the approved source.
- Combining unrelated behaviors into one criterion.
- Restating the user story without a measurable result.
- Fabricated thresholds, timeouts, messages, permissions, or validation rules.

When a value is unresolved, write a visible placeholder such as `Reset-link expiry duration: Product Manager confirmation required` and mark the Story's Estimable or Testable result accordingly.

## Traceability

Associate criteria with source requirement IDs or sections where available. If a criterion is a proposal rather than a confirmed requirement, label it as a proposal and obtain human confirmation before finalization.
