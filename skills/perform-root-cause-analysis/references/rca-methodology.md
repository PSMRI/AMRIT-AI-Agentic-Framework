# RCA Methodology

## Causal chain taxonomy

Every RCA must distinguish these levels. Mislabelling any level as the root
cause produces an incomplete or misleading RCA.

### Symptom

What the user or system observed.

Example:

```text
Beneficiary update returned HTTP 500 on the production environment.
```

### Trigger

The condition or event that exposed the failure.

Example:

```text
A beneficiary record without a districtId value entered the update workflow.
```

### Immediate Technical Failure

Where and how execution failed.

Example:

```text
NullPointerException at BeneficiaryService.updateBeneficiary() when accessing
districtId.getName() on a null reference.
```

### Underlying Condition

Why the failing state could reach that execution path.

Example:

```text
Records created through the mobile registration workflow can persist districtId
as null because that workflow's save endpoint does not enforce the district
validation present in the web registration workflow.
```

### Root Cause

Why that invalid or dangerous condition was allowed to exist.

Example:

```text
The required district validation is enforced in the web registration controller
but missing from the mobile registration controller, allowing records that
violate the entity invariant to be persisted. The mobile registration endpoint
was added later and did not replicate the validation contract.
```

### Contributing Factors

Things that increased the probability, duration, or impact of the incident but
are not themselves the root cause.

Example:

```text
No regression test covered beneficiary records originating from the mobile
registration workflow. The existing test suite only tested the web pathway.
```

## Causal chain construction

Build a chain from symptom to root cause:

```text
Observed Failure (Symptom)
      ↓
Trigger
      ↓
Immediate Technical Failure
      ↓
Underlying Condition
      ↓
Why the condition was possible
      ↓
Root Cause
```

Use as many causal steps as evidence supports. You may use 5 Whys concepts
where they help structure the thinking, but do not force exactly five levels.
Evidence quality matters more than reaching a fixed number of questions.

Every link in the chain must be supported by evidence. A chain link supported
only by speculation must be labelled as such.

## Hypothesis evaluation protocol

When more than one plausible cause exists, the skill must not jump to the first
explanation. Form and evaluate hypotheses explicitly.

For each meaningful hypothesis:

```text
Hypothesis:
<Clear statement of the proposed cause>

Supporting evidence:
<What evidence points toward this hypothesis>

Contradicting evidence:
<What evidence argues against it>

Verification performed:
<What was inspected, queried, or traced to test the hypothesis>

Result:
Confirmed | Rejected | Unresolved
```

### Confirmed

The evidence establishes the causal relationship. This hypothesis (or a refined
version) becomes part of the root cause.

### Rejected

Evidence contradicts the hypothesis or a more strongly supported alternative
explains the same evidence. State why it was rejected.

### Unresolved

Evidence is insufficient to confirm or reject. State what additional evidence
would resolve it.

## Investigation approach

Prefer falsifiable investigation:

1. State a hypothesis.
2. Identify what evidence would confirm or refute it.
3. Inspect that evidence (code, logs, configuration, data state).
4. Record the result.

Example:

```text
Hypothesis:
The API failure is caused by a database schema mismatch after migration v42.

Supporting evidence:
The error log shows a SQL column-not-found exception. Migration v42 renamed the
column.

Contradicting evidence:
None initially.

Verification:
Inspected the current migration directory and the entity mapping in the
persistence layer.

Result:
Rejected. The migration correctly renamed both the column and the entity
mapping. The column-not-found exception occurs in a different query that
references a hardcoded column name in a native SQL string, not the renamed
column.
```

## Common mislabelling errors

Do not label any of the following as the final root cause without explaining the
causal chain behind it:

- `NullPointerException`
- `timeout`
- `null value`
- `SQL exception`
- `API error`
- `HTTP 500`
- `connection refused`
- `OutOfMemoryError`
- `deadlock`
- `race condition` (without identifying the specific unsynchronized access)

These are symptoms or immediate failures. The root cause explains **why** they
occurred.

## Multiple root causes

Some incidents have more than one root cause. When evidence supports it, report
each cause with its own causal chain and confidence level. Do not force a
single-cause narrative when the evidence shows compound causation.

## Reopened defects

When investigating a reopened defect, also consider:

- What was the original root cause and fix?
- Did the original fix address the actual root cause or only the symptom?
- Was the fix correctly implemented and verified?
- Has the system changed since the original fix in a way that reintroduced the
  issue?
- Are there related code paths that were not covered by the original fix?

Previous RCA documents may generate a hypothesis but are not proof for the
current incident.
