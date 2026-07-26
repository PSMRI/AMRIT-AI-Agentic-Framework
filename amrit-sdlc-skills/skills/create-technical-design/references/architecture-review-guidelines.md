# Architecture Review Guidelines

Use these guidelines to reason about the design and prepare it for human review. Do not use them as a scoring rubric that implies approval.

## Review posture

An experienced Architect first establishes what is true, then selects the smallest safe change. A polished diagram cannot compensate for missing evidence.

Apply this order:

1. Confirm the approved problem and acceptance criteria.
2. Reconstruct the relevant current state from reliable evidence.
3. Identify invariants and deliberate non-changes.
4. Locate reuse opportunities and constraints.
5. Compare viable approaches.
6. Recommend a design with explicit trade-offs.
7. Trace impacts, failure modes, rollout, and verification.

## Evidence hierarchy

No source is automatically authoritative. Evaluate scope, ownership, status, version, and consistency.

Prefer, when relevant:

1. current executable contract or implementation evidence;
2. approved and current architecture decisions or specifications;
3. current operational and deployment evidence;
4. linked requirements and recent completed implementation records;
5. historical documents and issue discussion.

Do not silently resolve disagreement. Record the conflicting claims, their sources, the architectural consequence, and the person or evidence needed to resolve them.

## Claim labels

Use labels at the claim, row, or subsection level:

- **Confirmed:** supported by a named source.
- **Assumed:** used to make progress but not verified.
- **Proposed:** introduced by this design for review.
- **Conflict:** credible sources disagree.
- **Unknown:** evidence is not available.

Do not label a whole document Confirmed when individual design choices are proposals.

## Architecture invariants

Identify what must remain stable, such as:

- public contract behavior used by current consumers;
- clinical or programme workflow semantics;
- data ownership and system-of-record boundaries;
- authentication and authorization model;
- audit requirements;
- deployment topology or supported runtime;
- backward compatibility during rollout;
- reporting and integration behavior outside approved scope.

Explain why each invariant matters and which source supports it.

## Decision quality

For each material decision, include:

| Field | Expectation |
|---|---|
| Decision | One precise choice |
| Status | Confirmed constraint or Proposed design |
| Driver | Requirement, risk, or constraint addressed |
| Evidence | Stable source references |
| Rationale | Why this choice fits the current system |
| Alternatives | At least credible alternatives; omit artificial options |
| Trade-offs | Benefits, costs, and limitations |
| Impact | Components, consumers, data, and operations affected |
| Validation | Review, spike, contract check, or evidence still required |

Do not use "industry best practice" as the sole rationale. Connect the choice to AMRIT evidence and the requested change.

## Proportionality checks

Challenge:

- new services when an existing owner can safely absorb the behavior;
- new datastores when no durable state is required;
- synchronous calls added to latency-sensitive paths;
- new queues where delivery semantics are undefined;
- framework or platform changes unrelated to acceptance criteria;
- duplicated validation, mapping, or integration logic;
- configuration proliferation;
- migrations for data that can remain derived;
- broad refactoring hidden inside a feature design.

If broader change is valuable but outside scope, record it as deferred work rather than embedding it.

## Cross-cutting review

Review:

- security boundaries, sensitive health information, and auditability;
- failure isolation, timeout, retry, idempotency, and recovery;
- transaction and consistency boundaries;
- compatibility and phased rollout;
- capacity, large datasets, pagination, and concurrency;
- observability sufficient to detect and diagnose failure;
- configuration ownership and safe defaults;
- deployment ordering and rollback;
- test seams and regression blast radius;
- operational ownership after release.

## Open-question threshold

Include an open question only if different answers produce meaningfully different architecture, contracts, data models, security controls, rollout, or scope.

For a conventional choice, recommend one and justify it. Examples:

- Recommend `409 Conflict` for a detected state conflict rather than asking for a status code.
- Recommend an existing AMRIT validation or logging convention when evidence shows it applies.
- Recommend additive contract evolution when current consumers require compatibility.

## Review readiness

The package is review-ready when:

- all supplied Stories and acceptance criteria are traced;
- current and proposed state are visibly separate;
- important claims have sources or labels;
- alternatives and trade-offs are credible;
- impacted and deliberately unchanged areas are explicit;
- API and database decisions are unambiguous;
- security, performance, observability, deployment, and rollback are addressed;
- risks have mitigations or validation actions;
- unresolved questions are architecture-material.

Review-ready is not approved. Finish only with the required **Ready for Architect Review** gate.
