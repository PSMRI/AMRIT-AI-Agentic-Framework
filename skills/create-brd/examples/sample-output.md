# Enable Editing of Employee Login Username

**Document Status:** Draft — Pending Human Review

> This condensed fictional example demonstrates output structure. Confluence research would be performed during live skill execution; the illustrative references below are not real pages or links.

## Document Control

| Field | Value |
|---|---|
| Date | [Date] |
| Version Number | 0.1 |
| Author | Pending |
| Reviewed By | Pending |
| Approved By | Pending |
| Document Change Reference | Not supplied |

## 1. Executive Summary

This draft proposes allowing authorized Support Admin users to edit an employee's login username in Employee Master. It aims to remove reliance on developers when contact numbers change while protecting other employee information.

## 2. Background and Current Process

AMRIT uses an employee's contact number as the login username. When it changes, support teams depend on developers to update multiple records manually. The exact current workflow and records involved require confirmation.

## 3. Problem Statement

The current process creates operational dependency on developers and does not provide Support Admin users with a controlled business workflow for username changes.

## 4. Objectives

- Enable an authorized Support Admin to change Username in Employee Master.
- Prevent invalid or duplicate usernames.
- preserve existing employee data.
- Provide traceability and employee notification.
- Make the new username usable immediately after a successful change.

## 5. Stakeholders and Affected Users

- Support Admin users
- Employees whose usernames are changed
- Support team
- Business Systems Analyst, Product Manager, and relevant stakeholders as reviewers

## 6. Scope

### 6.1 In Scope

- Editing Username in Employee Master by an authorized Support Admin.
- Blank and duplicate validation.
- Audit logging and SMS notification.
- Immediate use of the new username.

### 6.2 Out of Scope

- Editing Employee ID, Date of Joining, or Password.
- Overwriting unrelated employee data.
- Decisions about active-session termination, old-username behaviour, or username format until confirmed.

## 7. Proposed Business Process

An authorized Support Admin opens an employee record, edits Username, and submits it. The system validates authorization, non-blank input, uniqueness, and any existing format rule once confirmed. On success, it retains other employee data, records an audit entry, sends an SMS, and permits login with the new username immediately.

## 8. Business Requirements

| Identifier | Requirement | Rationale | Source | Source Section (when available) | Confidence | Priority (only if supplied) | Notes |
|---|---|---|---|---|---|---|---|
| BR-001 | Authorized Support Admin users shall be able to change an employee Username from Employee Master. | Remove routine developer dependency. | Fictional user input | Business need | High |  |  |
| BR-002 | A username change shall not overwrite other employee data. | Protect employee records. | Fictional user input | In scope | High |  |  |
| BR-003 | A successful username change shall be traceable and communicated to the employee by SMS. | Support accountability and awareness. | Fictional user input | In scope | High |  |  |
| BR-004 | The new username shall work immediately after a successful change. | Avoid access delay. | Fictional user input | In scope | High |  |  |

## 9. Functional Requirements

| Identifier | Requirement | Source | Source Section | Confidence | Notes |
|---|---|---|---|---|---|
| FR-001 | Employee Master shall make only Username editable in this change workflow. | Fictional user input | In scope | High |  |
| FR-002 | Employee ID, Date of Joining, and Password shall remain read-only. | Fictional user input | Out of scope | High |  |
| FR-003 | The system shall reject blank or duplicate usernames and shall not save the change. | Fictional user input | Validation rules | High |  |
| FR-004 | The system shall audit-log each successful username change. | Fictional user input | Audit | High |  |
| FR-005 | The system shall send an SMS to the affected employee after a successful change. | Fictional user input | Notification | High |  |
| FR-006 | The system shall permit immediate login with the new username after a successful change. | Fictional user input | In scope | High |  |

## 10. Validation and Business Rules

- Username shall not be blank.
- Username shall be unique.
- Existing username format validation remains an open question and shall not be invented.
- Only an authorized Support Admin shall perform the change.

## 12. Non-Functional Business Requirements

- **Security and authorization:** Only authorized Support Admin users shall access the edit action.
- **Auditability:** A successful change shall produce an audit record; required audit fields need confirmation.
- **Data integrity:** Unrelated employee data shall remain unchanged.

## 14. Assumptions Requiring Confirmation

- The SMS destination and content are not supplied.
- The exact authorization rule and audit fields are not supplied.

## 15. Acceptance Criteria

| ID | Traces to | Criterion |
|---|---|---|
| AC-001 | BR-001, FR-001, FR-002 | **Given** an authorized Support Admin is viewing an employee in Employee Master, **when** the user enters a valid unique Username and submits, **then** the Username is changed and Employee ID, Date of Joining, and Password remain read-only. |
| AC-002 | FR-003 | **Given** a blank or duplicate Username, **when** the change is submitted, **then** the system rejects it and does not save the change. |
| AC-003 | BR-002 | **Given** a valid username change, **when** it succeeds, **then** unrelated employee data is unchanged. |
| AC-004 | BR-003, FR-004, FR-005 | **Given** a successful change, **when** processing completes, **then** an audit entry is recorded and an SMS is sent to the employee. |
| AC-005 | BR-004, FR-006 | **Given** a successful change, **when** the employee authenticates with the new username, **then** the new username works immediately. |

## 17. Information Still Requiring Human Confirmation

- Existing username format validation
- Authorization rule for Support Admin
- Audit fields and retention
- SMS destination, template, and failure handling

## 18. Open Questions

1. Should active sessions be terminated?
2. Should the old username stop working immediately?
3. What username format validation currently applies?

## 19. Reference Documents

| Page title | Document type | Status | Relevance | Reference |
|---|---|---|---|---|
| Example Employee Master Overview | Fictional module document | Example only | Illustrates the type of module context sought | No real link |
| Example Credential Change Rules | Fictional rules document | Example only | Illustrates validation and audit research | No real link |

Confluence research would be performed during live skill execution.

## 20. Human Review and Sign-Off

| Review | Status |
|---|---|
| Business Systems Analyst Review | Pending |
| Product Manager Review | Pending |
| Stakeholder Review | Pending |
| Final Approval | Pending |

## 21. Revision History

| Date | Version | Change | Author |
|---|---|---|---|
| [Date] | 0.1 | Initial draft example | Pending |
