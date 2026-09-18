# Sample Confirmed RCA

This is a fictional example illustrating a Confirmed Root Cause outcome. All
ticket keys, repositories, classes, and system names are fictional and do not
describe real AMRIT architecture.

---

## Root Cause Analysis — DEMO-4521: Beneficiary update fails with HTTP 500 for mobile-registered records

### Incident Details

| Field | Value |
| --- | --- |
| Jira / Support Ticket | DEMO-4521 |
| Product / Module | HWC / Beneficiary Registration |
| Environment | Production |
| Affected Version | Release 3.2.1 |
| Reported Date | 2026-07-15 |
| Severity / Priority | Critical / P1 |

### Incident Summary

Health workers using the HWC web application encounter an HTTP 500 error when
attempting to update beneficiary records that were originally registered through
the mobile application. The failure affects approximately 12% of beneficiary
update attempts.

### Impact

Health workers cannot update demographic or visit data for beneficiaries
registered via mobile. Approximately 200 affected records per day across 15
facilities. Workaround: re-register the beneficiary through the web application,
which creates a duplicate record.

### Expected Behaviour

Beneficiary update should succeed regardless of the registration channel (web or
mobile).

### Observed Behaviour

Beneficiary update returns HTTP 500 with a NullPointerException in the server
logs when the beneficiary was registered through the mobile application.

### Reproduction / Failure Conditions

1. Register a beneficiary through the mobile application without selecting a
   district (the mobile form does not enforce district selection).
2. Sync the record to the server.
3. Attempt to update the beneficiary through the HWC web application.
4. The update fails with HTTP 500.

### Incident Timeline

| Date | Event |
| --- | --- |
| 2026-07-15 | Incident reported by field support |
| 2026-07-15 | DEMO-4521 created as P1 |
| 2026-07-16 | Initial investigation: NullPointerException identified in logs |
| 2026-07-17 | RCA investigation initiated |

### Evidence Reviewed

#### Jira / Support Evidence

- DEMO-4521: bug report with reproduction steps and affected facility list.
- Linked to DEMO-4100: original mobile registration feature story.
- No previous fix attempts.

#### Runtime / Logs / Screenshots

- Stack trace showing NullPointerException at
  `BeneficiaryUpdateService.validateDemographics()` line referencing
  `beneficiary.getDistrictId().getName()`.
- Log timestamp correlates with reported failure time.
- 47 occurrences in the last 7 days, all for mobile-registered beneficiaries.

#### Repository / Code Evidence

**Repository**: DEMO-HWC-API

- **File**: `src/main/java/com/demo/hwc/service/BeneficiaryUpdateService.java`
  - `validateDemographics()` calls `beneficiary.getDistrictId().getName()`
    without a null check. Confirmed in code.

- **File**: `src/main/java/com/demo/hwc/controller/WebRegistrationController.java`
  - `registerBeneficiary()` validates that `districtId` is non-null before
    persisting. Confirmed in code.

- **File**: `src/main/java/com/demo/hwc/controller/MobileRegistrationController.java`
  - `syncBeneficiary()` persists the record without validating `districtId`.
    Confirmed in code. The method was added in DEMO-4100 and does not replicate
    the validation from `WebRegistrationController`.

- **File**: `src/test/java/com/demo/hwc/service/BeneficiaryUpdateServiceTest.java`
  - All existing tests create beneficiaries with non-null `districtId`. No test
    covers the null-district case. Confirmed in code.

#### Confluence / Requirement Evidence

- Beneficiary Registration FRD (Confluence page "HWC Beneficiary Registration
  Requirements") states district is a mandatory field for all registration
  channels. Documented intent.

### Technical Investigation

The investigation traced the NullPointerException from the update endpoint
backward through the service layer to the persistence layer, then forward
through both registration pathways.

The web registration controller enforces district validation before persisting.
The mobile registration controller, added later for DEMO-4100, does not. Both
controllers use the same `BeneficiaryRepository.save()`, but the validation
gate exists only in the web pathway.

The update service assumes `districtId` is always non-null because the FRD
requires it. This assumption holds for web-registered records but fails for
mobile-registered records.

### Hypotheses Evaluated

#### Hypothesis 1: Database schema allows null districtId

- **Supporting evidence**: Mobile-registered records have null districtId in
  production.
- **Contradicting evidence**: None initially.
- **Verification**: Inspected entity definition and database schema. The column
  is nullable at the database level; the NOT NULL constraint is enforced only
  in the web controller, not at the schema level.
- **Result**: Confirmed as a contributing factor. The schema permits null, but
  the root cause is the missing validation in the mobile controller.

#### Hypothesis 2: Mobile registration controller missing district validation

- **Supporting evidence**: `MobileRegistrationController.syncBeneficiary()` has
  no district validation. The web controller does validate. The FRD requires
  district for all channels.
- **Contradicting evidence**: None.
- **Verification**: Both controllers inspected in the current source.
- **Result**: Confirmed as root cause.

### Causal Chain

```text
Beneficiary update returns HTTP 500 (Symptom)
      ↓
A mobile-registered beneficiary with null districtId is updated (Trigger)
      ↓
NullPointerException at validateDemographics() accessing districtId.getName()
on null (Immediate Technical Failure)
      ↓
Mobile registration persists records without districtId because
MobileRegistrationController.syncBeneficiary() does not validate it
(Underlying Condition)
      ↓
The district validation is enforced in WebRegistrationController but was not
replicated when MobileRegistrationController was added for DEMO-4100
(Root Cause)
```

### Root Cause

The required district validation is enforced in `WebRegistrationController` but
missing from `MobileRegistrationController`, which was added later for
DEMO-4100. This allows records that violate the beneficiary entity invariant
(non-null district) to be persisted through the mobile workflow. The update
service then fails on a null dereference because it assumes the invariant holds.

**Status**: Confirmed Root Cause

### Contributing Factors

1. The database schema does not enforce a NOT NULL constraint on `districtId`,
   allowing the persistence layer to accept the invalid state.
2. No regression test covers beneficiary records originating from the mobile
   registration workflow. The existing test suite only tests the web pathway.

### Corrective Action

Add district validation to `MobileRegistrationController.syncBeneficiary()` to
match the existing validation in `WebRegistrationController.registerBeneficiary()`.
This prevents records with null `districtId` from being persisted through the
mobile workflow.

Additionally, add a null-safety check in
`BeneficiaryUpdateService.validateDemographics()` to handle existing records
that already have null `districtId` gracefully rather than throwing an unhandled
NullPointerException.

**Status**: Proposed

### Preventive Action

1. Add unit tests for beneficiary creation through the mobile registration
   pathway, verifying that district validation is enforced.
2. Add an integration test that creates a beneficiary via the mobile endpoint
   and confirms that update operations succeed.
3. Consider adding a NOT NULL constraint on `districtId` in the database schema
   after backfilling existing null records, to prevent future persistence-layer
   bypasses.

**Status**: Proposed

### Validation Required

- Unit test for mobile registration district validation passes.
- Integration test confirms update succeeds for mobile-registered beneficiaries.
- No NullPointerException for `districtId` in production logs for 2 weeks after
  deployment.
- Existing null `districtId` records are identified and a data remediation plan
  is established.

### Regression Risk

- Mobile registration workflow: verify that the new validation does not reject
  legitimate records that omit optional fields.
- Beneficiary update workflow: verify that the null-safety check does not mask
  other validation failures.

### Related References

- DEMO-4521: incident ticket
- DEMO-4100: mobile registration feature story
- Confluence: HWC Beneficiary Registration Requirements

### Open Questions

- How many existing production records have null `districtId`? A data audit is
  needed before adding a database-level NOT NULL constraint.

### Status

| Status | Value |
| --- | --- |
| RCA Status | Draft — Pending Human Confirmation |
| CAPA Status | Proposed / Pending Implementation |
| Confluence Publication Status | Not Published |
