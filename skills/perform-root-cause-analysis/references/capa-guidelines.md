# CAPA Guidelines

## RCA and CAPA are semantically separate

The AMRIT support process groups RCA and CAPA, but they serve different
purposes:

- **RCA** establishes what happened and why.
- **CAPA** proposes what to do about it.

Both appear in the same document because the organization treats them as paired
obligations. The skill produces both, but they must remain clearly separated.

## Corrective Action

Addresses the immediate defect or root cause. The corrective action should
directly fix or mitigate the specific failure identified in the RCA.

A corrective action must:

- Reference the specific root cause it addresses.
- Be concrete and actionable: name the repository, module, or configuration
  that needs to change.
- Be proportionate to the root cause: do not propose a system redesign for a
  missing validation.

Example:

```text
Corrective Action:
Add district validation to the mobile registration endpoint in
AMRIT-HWC-API/BeneficiaryController to match the existing validation in the web
registration endpoint. This prevents records with null districtId from being
persisted through the mobile workflow.

Status: Proposed
```

## Preventive Action

Reduces recurrence of the same **class** of failure, not just the specific
instance. Preventive actions address systemic gaps.

Examples:

- Adding regression tests that cover the failure scenario.
- Adding integration tests across the workflows that share a validation
  contract.
- Creating a shared validation service to prevent divergence between endpoints.
- Adding monitoring or alerting for the failure condition.
- Documenting the validation contract so future endpoints inherit it.

A preventive action must:

- Reference the contributing factors or systemic condition it addresses.
- Be concrete: name what type of test, what monitoring, or what process change.
- Not duplicate the corrective action with different wording.

Example:

```text
Preventive Action:
1. Add unit tests for beneficiary creation through the mobile registration
   pathway, verifying that district validation is enforced.
2. Add an integration test that creates a beneficiary via the mobile endpoint
   and confirms that update operations succeed without NullPointerException.
3. Document the beneficiary entity validation contract in the repository README
   or a shared validation reference so future registration endpoints apply it.

Status: Proposed
```

## CAPA status values

```text
Corrective Action: Proposed
Preventive Action: Proposed
CAPA Status: Pending implementation / validation
```

Do not use any of these statuses unless actual evidence supports them:

- `Corrective Action: Implemented` — only when the fix is verified in code.
- `Preventive Action: Implemented` — only when the prevention is verified.
- `CAPA Status: Complete` — only when both actions are implemented and
  validated.

The RCA skill proposes CAPA. It does not implement it.

## Implementation handoff

Corrective and preventive actions that require code changes should be
implemented through the appropriate development workflow:

```text
perform-root-cause-analysis
        ↓
confirmed corrective action
        ↓
implement-jira-ticket (or equivalent development workflow)
        ↓
create-development-pr
```

The RCA skill may recommend this handoff but does not execute it.

## CAPA scope

The skill proposes only CAPA that the evidence supports. Do not:

- Propose actions unrelated to the identified root cause or contributing
  factors.
- Propose organizational process changes without evidence that the process gap
  contributed to the incident.
- Propose actions so broad they are unactionable (for example, "improve testing"
  without specifying what tests).
- Claim CAPA is complete when only the RCA is complete.

## Validation required

For each proposed CAPA item, state what validation would confirm it is
effective:

```text
Validation Required:
- Unit test for mobile registration district validation passes.
- Integration test confirms update succeeds for mobile-registered beneficiaries.
- No NullPointerException for districtId in production logs for 2 weeks after
  deployment.
```
