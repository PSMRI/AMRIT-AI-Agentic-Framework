# Sample input

## Title

Enable Editing of Employee Login Username

## Context

AMRIT currently uses an employee's contact number as the login username. Employees may change contact numbers. Support teams currently depend on developers to update multiple records manually.

## Requested change

Allow authorized Support Admin users to edit the username from Employee Master.

## Known requirements

- Only Username is editable.
- Employee ID, Date of Joining, and Password remain read-only.
- Existing employee data must not be overwritten.
- Duplicate usernames must be rejected.
- Blank usernames must be rejected.
- Successful changes must be audit logged.
- The employee should receive an SMS.
- The new username should work immediately.

## Known open questions

- Should active sessions be terminated?
- Should the old username stop working immediately?
- What is the existing username format validation?

## Required live research

Before drafting, the skill must search Confluence for related documentation about:

- Employee Master
- Username or user name
- Login ID
- Credential changes
- Username validation
- Audit logging
- SMS notification
- Support Admin
- Employee login
