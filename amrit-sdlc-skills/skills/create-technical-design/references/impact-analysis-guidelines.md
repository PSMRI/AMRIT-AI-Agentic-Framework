# Impact Analysis Guidelines

Impact analysis defines the blast radius of the approved change. Assess every category; do not infer "no impact" from silence.

## Method

For each category:

1. Record the current element only when supported by evidence.
2. Describe the proposed change or state that no impact was identified.
3. Explain why.
4. Identify direct and downstream consumers.
5. Note compatibility, rollout, testing, and operational consequences.
6. Cite the source or label the conclusion Assumed or Proposed.

Use a table such as:

| Area | Current evidence | Proposed impact | Why | Downstream effect | Status/source |
|---|---|---|---|---|---|

Write **No impact identified from available evidence** when research found no impact. This means "not found," not a proof that impact is impossible.

## Required areas

### Modules

- owning module and adjacent modules;
- changed responsibility or boundary;
- reuse versus duplication;
- dependency direction and cyclic-dependency risk.

### Services

- service ownership and interface;
- orchestration, synchronous calls, messages, or scheduled work;
- latency, timeout, retry, idempotency, and failure isolation;
- version and deployment coupling.

### Repositories and persistence adapters

- entities and queries involved;
- read/write behavior and transaction participation;
- query-volume, locking, and compatibility impact;
- ownership of database access.

### Controllers and entry points

- HTTP, event, batch, UI, or integration entry points;
- validation and authorization boundary;
- contract or routing changes;
- error mapping.

### UI

- affected roles, screens, workflow, validation, accessibility, and localization;
- loading, empty, partial-failure, retry, and conflict states;
- backward compatibility during phased backend/frontend rollout.

### Database

- schema, query, migration, backfill, index, constraint, retention, and rollback impact;
- sensitive-data classification;
- whether the change only reuses existing persisted data.

Follow the database guidelines and make one explicit schema-change determination.

### APIs

- provider and consumers;
- existing reuse, additive modification, breaking modification, or new endpoint;
- contract, security, error, version, and OpenAPI impact;
- rollout coordination.

### Infrastructure

- compute, network, gateway, storage, queue, cache, secrets, certificates, scheduled jobs, and capacity;
- topology, availability, disaster recovery, and cost implications;
- avoid inventing a platform component.

### External integrations

- owner, purpose, protocol, contract, authentication, data classification, availability, and rate limits;
- timeout, retry, duplicate delivery, reconciliation, and support responsibility;
- sandbox or certification needs.

### Configuration

- key, owner, scope, default, allowed values, validation, secrets handling, and reload behavior;
- environment parity and rollback;
- prefer existing configuration mechanisms.

### Security

- authentication, authorization, privilege boundary, input handling, sensitive data, audit, misuse, and threat surface;
- security-review or privacy-review dependency.

### Performance

- changed request volume, payload, query count, dataset size, latency path, concurrency, caching, pagination, and capacity;
- measurable targets only when sourced; otherwise mark them Proposed.

### Logging

- diagnostic events and correlation;
- safe fields and redaction;
- prohibited clinical, personal, credential, or token content;
- log-level and volume impact.

### Monitoring

- service-level indicators, business-flow metrics, traces, alerts, dashboard, synthetic check, and failure visibility;
- alert owner and actionable threshold where known.

### Deployment

- build artifacts, order, compatibility window, feature control, migration sequence, health checks, smoke verification, rollback, and operational communications;
- zero-downtime or maintenance-window assumptions.

## Dependency graph

When three or more affected elements have meaningful dependency direction, add a small Mermaid component or flow diagram. Show:

- entry point;
- owning component;
- dependencies;
- data store or external systems;
- changed and unchanged boundaries.

Do not add a diagram for a linear relationship already clear in one sentence.

## Indirect and negative impact

Specifically look for:

- reports and exports reading changed data;
- downstream consumers relying on undocumented behavior;
- shared validation or master data;
- batch and reconciliation jobs;
- permissions inherited through roles;
- caches invalidated by writes;
- historical records and in-flight workflows;
- deployment skew between producers and consumers;
- support and audit processes.

State what should not change. Negative-scope clarity is part of impact analysis.
