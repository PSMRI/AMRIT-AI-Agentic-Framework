# Product Backlog Draft - Registered Email Password Reset

## 1. Document status

- Status: **Draft - Pending Product Manager Review**
- Jira Publication Status: **Not Published**
- Source: `BRD - Registered Email Password Reset`, version 1.0
- Source approval: Signed off, as stated in the supplied sample
- Research limitation: This fictional example contains no live Confluence or Jira research.

## 2. Backlog summary

One Epic, three Stories, and one configuration Task are proposed. Module is supported by the source. Category, Jira field options, and hierarchy require project research before publication.

## 3. Proposed hierarchy

- `EPIC-01` - Restore Facility App access through registered-email password reset
  - `STORY-01` - Request a password-reset link
  - `STORY-02` - Reject invalid reset links
  - `STORY-03` - Complete reset and regain access
  - `TASK-01` - Configure reset-link expiry

## 4. Epic

### EPIC-01 - Restore Facility App access through registered-email password reset

- Business objective: Enable eligible users to regain access without disclosing account registration.
- Scope: `BR-001`, `FR-001` through `FR-005`
- Module: Facility App
- Category: Proposed `Access Management`; confirm against Jira options
- Priority recommendation: Proposed High
- Rationale: Account access is affected and the capability reduces service-desk dependency; production status, affected-user volume, deadline, and workaround are not identified.
- Dependencies: Registered email data; outbound email capability
- Risks: Undecided expiry duration; current Jira conventions unknown

## 5. Stories

### STORY-01 - Request a password-reset link

As an active Facility App user, I want to request a password-reset link using my registered email so that I can begin recovering access without service-desk intervention.

- Business value: Starts self-service account recovery while avoiding account enumeration.
- Module: Facility App
- Category: Proposed `Access Management`; confirmation required
- Priority recommendation: Proposed High
- Priority rationale: This is the core entry point for the approved recovery capability.
- Source: `BR-001`, `FR-001`, `FR-004`
- Dependencies: Outbound email capability
- Assumptions or unresolved decisions: Eligibility rules beyond active-account status are not identified.

Acceptance criteria:

1. Given an eligible active account has the submitted registered email, when a reset is requested, then the system sends a single-use reset link to that email.
2. Given any email is submitted, when the request is accepted, then the response does not disclose whether the email is registered.

INVEST Review:

- Independent: Pass - produces the request outcome independently of completing the reset.
- Negotiable: Pass - states behavior without choosing architecture.
- Valuable: Pass - enables self-service recovery.
- Estimable: Pass - the stated behavior is bounded; technical estimation remains a later activity.
- Small: Pass - covers one workflow step.
- Testable: Pass - success and privacy behavior are observable.

### STORY-02 - Reject invalid reset links

As a Facility App user, I want invalid reset links to be rejected so that an expired or consumed link cannot change my password.

- Business value: Enforces the approved validity rules.
- Module: Facility App
- Category: Proposed `Access Management`; confirmation required
- Priority recommendation: Proposed High
- Priority rationale: Invalid-link rejection protects the approved reset workflow.
- Source: `FR-002`, `FR-003`
- Dependency: Configured expiry duration
- Assumptions or unresolved decisions: Expiry duration and the authorized configuration role require confirmation.

Acceptance criteria:

1. Given a reset link has exceeded the configured expiry period, when it is submitted, then the system rejects it and prevents password modification.
2. Given a reset link has already been used, when it is submitted again, then the system rejects it and prevents password modification.

INVEST Review:

- Independent: Pass - validity behavior can be accepted separately.
- Negotiable: Pass - no implementation is prescribed.
- Valuable: Pass - prevents invalid password changes.
- Estimable: Needs clarification - the expiry duration and authorized configurator remain unresolved.
- Small: Pass - covers reset-link validity.
- Testable: Pass - expired and reused outcomes are explicit.

### STORY-03 - Complete reset and regain access

As an eligible Facility App user, I want to set a new password through a valid reset link so that I can sign in again.

- Business value: Completes account recovery.
- Module: Facility App
- Category: Proposed `Access Management`; confirmation required
- Priority recommendation: Proposed High
- Priority rationale: This Story completes the approved recovery outcome.
- Source: `BR-001`, `FR-005`
- Dependency: Valid reset link
- Assumptions or unresolved decisions: Normal account-eligibility rules are referenced but not enumerated in the source.

Acceptance criteria:

1. Given an eligible user has a valid unused reset link, when the user successfully sets a new password, then the link becomes unusable.
2. Given the password reset succeeded, when the user signs in with the new password, then access is permitted subject to normal account eligibility.

INVEST Review:

- Independent: Pass - expresses the completion outcome with an explicit link dependency.
- Negotiable: Pass - leaves implementation open.
- Valuable: Pass - restores access.
- Estimable: Pass - the outcome is bounded by supplied requirements.
- Small: Pass - covers completion and immediate user outcome.
- Testable: Pass - link consumption and sign-in are observable.

## 6. Task

### TASK-01 - Configure reset-link expiry

- Purpose: Make reset-link expiry configurable by an authorized administrator.
- Expected result: The approved expiry setting can be managed by an authorized role and is applied to new reset links.
- Proposed parent: `EPIC-01`; validate Jira hierarchy
- Source: `FR-002`
- Module: Proposed Admin Portal; source confirmation required
- Category: Proposed `Configuration`; Jira confirmation required
- Priority: Proposed High because `STORY-02` depends on it
- Notes: Confirm the authorized role, target module, and Jira-supported relationship before publication.

## 7. Traceability

| Source | Backlog items |
|---|---|
| BR-001 | EPIC-01, STORY-01, STORY-03 |
| FR-001 | STORY-01 |
| FR-002 | STORY-02, TASK-01 |
| FR-003 | STORY-02 |
| FR-004 | STORY-01 |
| FR-005 | STORY-03 |

## 8. Possible duplicates

Not assessed in this fictional example. Jira duplicate research is required before publication.

## 9. Open decisions

- Confirm the reset-link expiry duration or ownership of that business decision.
- Confirm which authorized role changes expiry and in which module.
- Confirm category, priority options, labels, and supported Jira hierarchy.
- Confirm production impact, affected-user volume, and workaround.

## 10. Product Manager review status

Pending review. No Jira issues have been created or updated.
