# Evidence and Confidence Guidelines

## Evidence classification

Classify every material statement in the RCA:

- **Observed** — directly witnessed in logs, error output, reproduction, or
  runtime behaviour.
- **Confirmed in code** — the file, symbol, contract, schema, or configuration
  was read in the current checked-out source.
- **Documented intent** — an approved document or specification states it; the
  code has not been shown to match.
- **Inferred** — strongly indicated by evidence or structure but not directly
  confirmed.
- **Hypothesis** — a proposed explanation under evaluation; not yet confirmed or
  rejected.
- **Unresolved** — evidence is unavailable, insufficient, incomplete, or
  conflicting.

Label inferred material explicitly. Do not present inferences as confirmed
facts.

## RCA confidence statuses

### Confirmed Root Cause

The available evidence establishes a defensible causal chain explaining the
incident:

- The symptom, trigger, and immediate failure are identified.
- The underlying condition is traced to its origin.
- The root cause explains why the condition exists.
- Every link in the causal chain has supporting evidence.
- No unresolved contradictory evidence exists.
- Current source code was inspected for the relevant execution path.

### Probable Root Cause

Strong evidence supports the cause but a meaningful verification gap remains:

- Most of the causal chain is evidence-backed.
- One or more links rely on inference or incomplete evidence.
- No contradictory evidence was found, but a gap prevents full confirmation.
- The gap is explicitly described: what was not verified and why.

Examples of gaps that produce Probable status:

- A repository in the causal chain was not accessible for inspection.
- Production-specific configuration could not be verified.
- The exact data state at failure time is not available.
- A downstream service could not be inspected.

### Root Cause Not Conclusively Established

Evidence is insufficient, conflicting, inaccessible, or multiple hypotheses
remain viable:

- The symptom is identified but the causal chain cannot be completed.
- Two or more hypotheses remain viable with no decisive evidence.
- Required source code is inaccessible.
- Available logs or reproduction evidence is insufficient.
- Contradictory evidence cannot be resolved.

This is a legitimate RCA outcome. Do not fabricate a conclusion to avoid it.

## What must not be fabricated

Never fabricate:

- logs or log excerpts;
- reproduction steps or results;
- affected versions or environments;
- code behaviour, functions, classes, or modules;
- repository names or file paths;
- service relationships or API contracts;
- ticket history, comments, or previous incidents;
- test results or test-case verdicts;
- deployment state or configuration values;
- root cause or causal chain links;
- CAPA completion or implementation status;
- approvals, sign-offs, or review outcomes.

## Evidence-backed language

Prefer precise language:

| Use | Instead of |
| --- | --- |
| Observed in logs | The system showed |
| Confirmed in code at `<file>` | The code does |
| Documented in `<page>` | The documentation says |
| Inferred from `<evidence>` | It appears that |
| Hypothesis — not yet verified | Probably |
| Not available — `<reason>` | Unknown |
| Rejected — contradicted by `<evidence>` | Unlikely |

## Handling conflicting evidence

When evidence conflicts:

1. Identify the conflict and name each source.
2. For claims about current runtime behaviour, prefer direct code evidence.
3. For claims about intended behaviour, prefer approved documentation.
4. Report the conflict explicitly in the RCA; do not silently choose a side.
5. If the conflict is material to the root cause, it may prevent Confirmed
   status.

## Evidence gaps

Every evidence gap must be:

1. Named — what is missing.
2. Explained — why it is missing (repository not accessible, logs not available,
   environment not reachable).
3. Assessed — what it prevents from being established.
4. Recorded — in the RCA under Open Questions or Evidence Gaps.

A gap does not invalidate the RCA. It determines the confidence level.
