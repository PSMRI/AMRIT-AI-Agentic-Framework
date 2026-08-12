# Sample Feature Input

> Fictional example; no live Jira or Confluence data.

## Source

- Document: BRD - Registered Email Password Reset
- Version: 1.0
- Status: Signed off by Product Manager
- Application: Facility App

## Approved requirements

- `BR-001`: Allow an active Facility App user to request a password reset using the email registered to the account.
- `FR-001`: Send a single-use reset link when the submitted email belongs to an eligible active account.
- `FR-002`: Make reset-link expiry configurable by an authorized administrator.
- `FR-003`: Reject expired or previously used reset links.
- `FR-004`: Do not disclose whether an entered email is registered.
- `FR-005`: After a successful reset, allow the user to sign in with the new password.

## Known constraints

- The configured expiry duration is not stated in the BRD.
- Email delivery and security implementation are outside the business requirements.
- Jira project field values have not yet been researched.

## Requested action

Create a proposed product backlog for Product Manager review. Do not create Jira issues.
