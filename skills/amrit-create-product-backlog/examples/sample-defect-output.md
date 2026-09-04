# Product Defect Backlog Draft - AMRIT-123

## 1. Document status

- Status: **Draft - Pending Product Manager Review**
- Jira Publication Status: **Not Published**
- Existing issue: `AMRIT-123` (fictional)
- Source: L2 escalation and supplied fictional Jira issue details
- Research limitation: No live Jira issue, duplicate search, attachments, or Confluence pages were accessed for this example.

## 2. Classification

- Proposed classification: Product defect
- Application and module: Facility App
- Environment: Production
- Category: Proposed `Access Management`; confirm against actual Jira options
- Existing priority: Source not explicitly identified.
- Priority recommendation: Proposed High, subject to actual Jira options and evidence validation
- Closure requirement: **CAPA required at closure**
- Root cause: Not established; analysis required.

## 3. Impact and urgency

- Confirmed reported impact: Three users remained locked out after a reported successful reset.
- Operational impact: Service Desk intervention is required to restore access.
- Workaround: Manual account unlock; safety, effort, and scalability need confirmation.
- Urgency: Production access is affected. Report frequency, total affected population, and ongoing incident status are unresolved.
- Priority rationale: Live access failures with manual intervention justify elevated attention, but missing breadth, frequency, and Jira priority conventions prevent a final Jira value.

## 4. Proposed defect content

### Summary

Facility App users remain locked out after a reported successful password reset

### Expected behavior

Given an otherwise eligible user successfully resets a password, when the user signs in with the new password, then the account-lock state no longer prevents access unless a separate documented rule applies.

### Observed behavior

Three reported users received an account-locked message after completing the reset and using the new password.

### Evidence and reproduction

- Redacted screenshots and incident timestamps are reported as attached but were not inspected in this fictional example.
- Independent reproduction is pending.
- Capture account state before and after reset, reset outcome, sign-in result, environment, timestamp, and correlation evidence without exposing credentials or personal data.

## 5. Related Tasks

### TASK-01 - Reproduce and characterize post-reset lock behavior

- Purpose: Establish reproducibility, affected workflow states, and regression boundary.
- Expected result: Evidence-backed reproduction outcome and affected conditions without asserting a root cause.
- Parent: Link to `AMRIT-123` using the project's supported relationship after approval
- Module: Facility App
- Category: Proposed `Defect Analysis`; confirmation required
- Priority: Align with the approved defect priority

### TASK-02 - Verify expected lock-state behavior

- Purpose: Compare observed behavior with approved password-reset and account-lock rules.
- Expected result: Referenced expected behavior, conflicts, and clarification needs.
- Parent: Link to `AMRIT-123` using the project's supported relationship after approval
- Source: Related approved requirements or Confluence documentation; not yet retrieved

## 6. Possible duplicates

Not assessed in this fictional example. Search Jira by symptom, Facility App module, reset workflow, account-lock state, source incidents, and related labels before any update or new issue.

## 7. Open decisions

- Confirm the actual affected-user count, recurrence, and incident status.
- Inspect attachments and independently reproduce.
- Confirm whether successful reset is intended to clear the lock state in all cases.
- Confirm category, priority options, labels, and the Jira relationship for analysis Tasks.
- Decide whether the existing priority should change; do not overwrite it without human approval.

## 8. Product Manager review status

Pending review. `AMRIT-123` has not been updated, commented on, linked, moved, reprioritized, closed, or transitioned. CAPA has not been performed; **CAPA required at closure** remains recorded.
