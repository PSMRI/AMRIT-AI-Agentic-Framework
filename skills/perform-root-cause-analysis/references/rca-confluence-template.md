# RCA Confluence Template

## Usage

This template provides the logical information model for an RCA document. At
runtime, also inspect the actual AMRIT Confluence RCA/CAPA area to learn the
organizational format before drafting:

```text
Support Tickets - RCA and CAPA
https://pmp.piramalswasthya.org/confluence/spaces/AMRIT/pages/76546642/Support+Tickets+-+RCA+and+CAPA
```

Read representative existing RCA pages to learn the actual headings, table
layout, terminology, naming conventions, and page hierarchy. Adapt the template
below to match the discovered organizational format. Do not force fields that do
not exist in the actual format without good reason, and do not omit fields that
the organization expects.

## Template

```markdown
# Root Cause Analysis — <Ticket Key>: <Summary>

## Incident Details

| Field | Value |
| --- | --- |
| Jira / Support Ticket | <key and link> |
| Product / Module | <affected product and module> |
| Environment | <production, staging, or other> |
| Affected Version | <release or build version> |
| Reported Date | <date> |
| Severity / Priority | <severity and priority> |

## Incident Summary

<Brief summary of the incident in 2-4 sentences.>

## Impact

<Who or what was affected, how many users or transactions, operational
consequence, and any workaround in place.>

## Expected Behaviour

<What should have happened according to approved requirements.>

## Observed Behaviour

<What actually happened, based on incident evidence.>

## Reproduction / Failure Conditions

<Steps or conditions under which the failure occurs. If reproduction was not
performed, state why.>

## Incident Timeline

<Chronological sequence of relevant events: when reported, when triaged, when
investigated, previous fix attempts, reopens.>

## Evidence Reviewed

### Jira / Support Evidence

<Ticket details, linked issues, comments, attachments, reopen history.>

### Runtime / Logs / Screenshots

<Application logs, error output, stack traces, screenshots, monitoring data.
State what was available and what was not.>

### Repository / Code Evidence

<For each materially involved repository: repository name, files inspected,
relevant behaviour found, relationship to the incident. Follow the recording
format in current-code-inspection-guidelines.md.>

### Confluence / Requirement Evidence

<Relevant requirements, specifications, approved behaviour, previous RCA
documents consulted.>

### Graph / Architecture Evidence

<Graphify or architecture evidence, if used. Omit this section if Graphify was
not consulted.>

## Technical Investigation

<Narrative of the investigation: what was traced, what was found, how the
execution path was followed through the code. This section tells the story of
the investigation for a human reader.>

## Hypotheses Evaluated

### Hypothesis 1: <brief label>

- **Supporting evidence**: <what supports this hypothesis>
- **Contradicting evidence**: <what argues against it>
- **Verification**: <what was inspected or tested>
- **Result**: Confirmed | Rejected | Unresolved

### Hypothesis 2: <brief label>

<Same structure. Include as many as were meaningfully evaluated. Omit this
section if only one plausible cause existed.>

## Causal Chain

```text
Observed Failure
      ↓
<Trigger>
      ↓
<Immediate Technical Failure>
      ↓
<Underlying Condition>
      ↓
<Why the condition was possible>
      ↓
<Root Cause>
```

## Root Cause

<Clear statement of the root cause.>

**Status**: Confirmed Root Cause | Probable Root Cause | Root Cause Not
Conclusively Established

<If Probable or Not Conclusively Established, state the specific evidence gap.>

## Contributing Factors

<Factors that increased probability, duration, or impact but are not themselves
the root cause. Omit if none were identified.>

## Corrective Action

<Specific proposed fix addressing the root cause.>

**Status**: Proposed

## Preventive Action

<Proposed actions to prevent recurrence of this class of failure.>

**Status**: Proposed

## Validation Required

<What validation would confirm the corrective and preventive actions are
effective.>

## Regression Risk

<Areas that could be affected by the proposed corrective action and should be
regression-tested.>

## Related References

<Links to related Jira issues, Confluence pages, previous RCA documents,
architecture documentation, or other relevant references.>

## Open Questions

<Anything that remains unresolved, requires further investigation, or depends
on information not available during this analysis.>

## Status

| Status | Value |
| --- | --- |
| RCA Status | Draft — Pending Human Confirmation |
| CAPA Status | Proposed / Pending Implementation |
| Confluence Publication Status | Not Published |
```

## Adaptation rules

- If the actual Confluence RCA pages use different headings, use those headings.
- If the organization uses a table-based format rather than headings, use
  tables.
- If the organization expects additional fields, include them.
- If a template field has no applicable content, include it with a clear
  statement that it does not apply or was not available, rather than omitting
  it silently.
- The Status section at the end is mandatory regardless of organizational
  format.
