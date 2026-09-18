# Current Code Inspection Guidelines for RCA

## The rule

Current checked-out source code MUST be inspected for every software RCA.

Documentation answers **what the system is intended to do**.

The source code answers **what the system currently does and how the failure
actually occurs**.

Both are required. Neither replaces the other. Where they disagree about current
behaviour, the code is correct about the present and the approved documentation
is authoritative about the intent — and the disagreement itself is reportable.

An RCA must never establish a current technical root cause purely from
documentation, DeepWiki, Graphify, Jira comments, or previous RCA documents.

## What to inspect

Depending on the incident, inspect the appropriate areas in the execution path.
Do not blindly search the entire codebase. Start from the incident evidence and
trace the actual path.

Relevant areas include:

- controllers, routes, and request handling;
- services and domain or business logic;
- repositories, DAOs, and persistence code;
- validation and input handling;
- error handling and exception propagation;
- API clients and integration code;
- configuration and environment-dependent logic;
- database queries and schema assumptions;
- migrations and schema state;
- frontend components, state management, and API calls;
- Android flows, offline behaviour, and sync logic;
- async jobs, schedulers, and queue consumers;
- caching and cache-invalidation logic;
- authentication and authorization checks;
- serialization and deserialization;
- tests covering the affected behaviour;
- feature flags and conditional logic;
- build and dependency configuration.

## How to trace the execution path

1. Start from the reported symptom: the endpoint, screen, action, or process
   that failed.
2. Identify the entry point in code: the controller, route handler, scheduled
   job, event handler, or UI component.
3. Follow the call chain through service, domain, and persistence layers.
4. At each step, note what the code actually does, not what documentation says
   it should do.
5. Identify where the failure occurs and what condition leads to it.
6. Trace backward to find why that condition exists: missing validation, data
   inconsistency, incorrect logic, unhandled case, or configuration mismatch.

## Recording code evidence

For each material code finding, record:

- **Repository** — which AMRIT repository.
- **File** — the file path within the repository.
- **Class, function, or module** — the specific code unit.
- **Relevant behaviour** — what the code does that relates to the incident.
- **Relationship to incident** — how this code contributes to the failure chain.
- **Confidence** — Confirmed in code, Inferred from structure, or Not yet
  verified.

Avoid claiming specific line numbers unless the current tooling produces reliable
references and the line numbers are stable in context.

## When source code is unavailable

If the relevant repository cannot be read or is not present in the environment:

1. Do not fabricate a technical root cause for that repository.
2. Do not substitute documentation, DeepWiki, Graphify, or previous knowledge
   for the code.
3. Complete only the parts of the RCA that accessible evidence supports.
4. Report the evidence gap explicitly:
   `RCA BLOCKED — relevant current source code could not be inspected.`
   or include the gap in the RCA with `Root Cause Not Conclusively Established`.
5. Explain what repository and inspection would be needed to resolve it.

## Reconciling documentation with code

For every material claim in the RCA, classify it:

- **Confirmed in code** — the file, symbol, contract, or schema object was read.
- **Documented intent** — an approved document states it; the code has not been
  shown to match.
- **Inferred** — strongly indicated by structure or convention, not directly
  confirmed.
- **Conflict** — documentation and code disagree materially.

Report conflicts rather than silently choosing a side when they affect the RCA
conclusion.

## Multi-repository inspection

When the incident spans multiple repositories:

1. List every repository the causal chain plausibly touches.
2. Inspect each accessible repository along the failure path.
3. Trace cross-repository interactions: API calls, shared database tables, event
   flows, message queues, configuration dependencies.
4. For each inaccessible repository, state the evidence gap and what it prevents
   from being established.

## Review checklist

- The actual source was inspected before forming a technical hypothesis.
- No structure was assumed to exist because a document named it.
- DeepWiki findings that influenced the RCA were verified against the code.
- Unavailable sources are recorded as limitations, not silently ignored.
- Documentation-versus-code conflicts are reported, not resolved silently.
- Inaccessible source produced an evidence-gap report, not a
  documentation-driven root cause.
