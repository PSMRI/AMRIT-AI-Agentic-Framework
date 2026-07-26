# INVEST Guidelines

Assess every proposed Story against all six criteria. Do not merely add an INVEST label.

| Criterion | Pass signal | Failure signal | Repair |
|---|---|---|---|
| Independent | Can be prioritized and delivered with limited coupling. | Requires another draft Story merely to be usable or testable. | Re-slice by outcome, combine inseparable items, or state the dependency. |
| Negotiable | Describes desired value and boundaries without prescribing unnecessary implementation. | Reads as a fixed technical solution unsupported by the source. | Restate the outcome and move genuine constraints to acceptance criteria. |
| Valuable | Names a clear benefit to a user, stakeholder, operation, or obligation. | Describes activity with no business value. | Clarify the beneficiary and outcome, or convert it to a Task. |
| Estimable | Scope, rules, and dependencies are sufficiently understood for later estimation. | Critical decisions, data, integrations, or rules are unknown. | Ask a focused question or flag `Needs clarification`; never invent an estimate. |
| Small | Represents one coherent outcome likely to fit normal delivery boundaries. | Contains multiple releasable behaviors, roles, or workflows. | Split vertically while retaining independent value. |
| Testable | Has observable, unambiguous pass/fail conditions. | Uses vague terms or omits expected outcomes. | Rewrite acceptance criteria with explicit conditions and results. |

## Required review format

```text
INVEST Review:
- Independent: Pass - <brief evidence>
- Negotiable: Pass - <brief evidence>
- Valuable: Pass - <brief evidence>
- Estimable: Needs clarification - <missing decision>
- Small: Fail - <split recommendation>
- Testable: Pass - <brief evidence>
```

Use `Pass`, `Fail`, or `Needs clarification` with a concise reason. A Story that fails should be rewritten, split, converted to a Task, or explicitly held for Product Manager decision.

## Examples

### Weak

> As a user, I want the whole account platform rebuilt so that it is better.

Problems: unclear role and value, multiple outcomes, unbounded scope, no testable result, and an implementation assumption.

### Improved

> As a registered Facility App user, I want to request a password-reset link using my registered email so that I can regain access without service-desk intervention.

This may pass when source evidence defines eligibility, response behavior, expiry configuration, permissions, and measurable acceptance criteria.

## Guardrails

- Do not declare `Estimable: Pass` when a critical business rule is unresolved.
- Do not treat dependency-free as the only meaning of Independent; identify manageable dependencies honestly.
- Do not split Stories into technical layers that provide no independently testable value.
- Do not invent delivery duration, estimates, or story points.
