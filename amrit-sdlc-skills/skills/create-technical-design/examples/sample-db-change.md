# Fictional Database-Change Example

This is a focused example of the Database Analysis section for a healthcare referral workflow. It is not a complete technical design and does not describe a real AMRIT schema.

## Decision

**Confirmed requirement:** A referral may have multiple time-ordered escalation attempts, each with an outcome and audit timestamp. History must remain available after the referral returns to normal processing.

**Confirmed current evidence:** The fictional `referral` table stores only the referral's current state. The repository and schema research found no child entity or audit record capable of representing multiple escalation attempts.

**Proposed:** Add a child table for escalation attempts. A schema change is required because the approved history cannot be represented without overwriting prior attempts.

## Schema impact

| Item | Proposed change | Rationale | Compatibility |
|---|---|---|---|
| `referral_escalation_attempt` | New child table | Preserve one-to-many attempt history | Additive |
| `referral_id` | Required foreign key | Keep referral as aggregate owner | Additive |
| `attempt_number` | Required positive integer | Stable ordering within referral | Additive |
| `outcome_code` | Required bounded code | Avoid free-text outcome semantics | Additive |
| `attempted_at` | Required offset-aware timestamp | Preserve event time | Additive |
| Unique constraint | `(referral_id, attempt_number)` | Prevent duplicate ordinal under concurrency | Additive |
| Query index | `(referral_id, attempted_at)` | Support ordered referral-history retrieval | Write/storage cost to review |

The design does not store beneficiary name, contact detail, or clinical narrative in the new table. The referral remains the owner of access control and retention.

## Relationships and constraints

- One referral has zero or more escalation attempts.
- An attempt belongs to exactly one referral.
- Deletion behavior must follow the confirmed referral-retention policy; do not select cascade behavior until that policy is verified.
- `attempt_number` must be positive.
- `outcome_code` values must come from the approved bounded domain; the physical enforcement mechanism depends on the confirmed database convention.

## DBML

```dbml
Table referral {
  id bigint [pk, note: 'Existing fictional table']
  status varchar(30) [not null, note: 'Existing fictional column']
}

Table referral_escalation_attempt {
  id bigint [pk, increment, note: 'Proposed']
  referral_id bigint [not null, ref: > referral.id]
  attempt_number int [not null, note: 'Must be greater than zero']
  outcome_code varchar(30) [not null]
  attempted_at timestamp [not null]
  created_by varchar(100) [not null, note: 'Actor identifier; no beneficiary data']
  created_at timestamp [not null]

  Indexes {
    (referral_id, attempt_number) [unique]
    (referral_id, attempted_at)
  }
}
```

## Migration and deployment notes

1. Apply the additive table before deploying writers.
2. No backfill is proposed because the approved source states that historical attempt detail was not previously captured. Confirm this with the data owner.
3. Deploy reads that tolerate zero attempts before enabling writes.
4. Monitor constraint violations and insert latency.
5. Add retention, masking, and access controls using confirmed referral policy.

## Rollback considerations

Application rollback can stop new writes while leaving the additive table in place. Dropping the table is not a safe rollback after production attempts exist because it would destroy history. Prefer a forward fix or disable the new workflow, then retain data until an approved data disposition is available.

## Review points

- Confirm the physical database engine and type conventions.
- Confirm referral retention and delete behavior.
- Confirm the actor-identifier format and privacy classification.
- Confirm whether outcome codes use a check constraint, reference table, or application-owned validation.
- Confirm online DDL and deployment sequencing with the DBA or data owner.
