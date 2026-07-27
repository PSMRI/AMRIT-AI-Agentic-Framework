# API Design Guidelines

Base API analysis on the authoritative Swagger/OpenAPI contract and identified consumers. Do not invent paths, methods, schemas, headers, or status codes as current behavior.

## Decision sequence

Determine in this order:

1. Does the workflow require an API change?
2. Can a confirmed existing operation satisfy it without semantic distortion?
3. Can an existing operation be extended additively and compatibly?
4. Is a new operation justified?
5. Is a breaking change unavoidable?

Prefer reuse only when the operation's responsibility, authorization, semantics, and lifecycle genuinely match. Do not overload an unrelated endpoint to avoid adding a contract.

## Evidence record

For every affected operation record:

- specification title/version and retrieval source;
- path and method;
- operation identifier when present;
- provider and known consumers;
- authentication and authorization;
- request, response, and error schemas;
- deprecation or version signals;
- observed inconsistency between specification and implementation evidence.

Label absent or stale evidence.

## Change classification

Classify each operation:

- **Existing, unchanged**
- **Existing, reused**
- **Existing, additive modification**
- **Existing, breaking modification**
- **Proposed new endpoint**
- **Deprecated or replaced**
- **No API change**

Explain why the classification is correct.

Potential breaking changes include:

- removing or renaming fields or operations;
- changing field type, format, meaning, requiredness, or nullability;
- narrowing accepted values;
- changing status or error semantics;
- changing authentication, authorization, headers, or content type;
- changing pagination, sorting, default behavior, or idempotency;
- adding a required request field;
- making an optional response field unconditionally absent;
- changing date, time, locale, precision, or identifier representation.

An additive field can still break strict consumers. Identify consumer behavior rather than assuming compatibility.

## Contract specification

Describe, without implementation code:

### Request

- path, query, header, and body responsibilities;
- required and optional fields;
- types, formats, bounds, and cross-field rules;
- identity, tenant, programme, or location context where evidenced;
- idempotency or correlation behavior;
- sensitive-data classification.

### Response

- success status and semantics;
- response fields and nullability;
- pagination or continuation;
- stable identifiers and timestamps;
- compatibility expectations.

### Errors

Recommend conventional outcomes when current standards are unavailable:

- `400 Bad Request` for malformed or invalid input;
- `401 Unauthorized` when authentication is missing or invalid;
- `403 Forbidden` when identity is known but lacks permission;
- `404 Not Found` when the addressed resource is absent and disclosure is acceptable;
- `409 Conflict` for state, duplicate, or concurrency conflict;
- `422 Unprocessable Content` only when the established API convention distinguishes semantic validation from `400`;
- `429 Too Many Requests` for enforced rate limits;
- `503 Service Unavailable` for temporary inability to serve.

Fit recommendations to confirmed AMRIT conventions. Define safe error shape, stable error code, correlation reference, and retryability without exposing internals.

## Security and privacy

Identify:

- authentication mechanism from evidence;
- authorization rule and resource ownership;
- field-level sensitive information;
- over-posting and mass-assignment risk;
- enumeration and object-reference risk;
- payload and rate limits;
- audit requirements;
- log and trace redaction.

Use fictional values in examples.

## Reliability

For calls and callbacks define:

- timeout budget;
- retry owner and eligible failures;
- idempotency behavior;
- duplicate and ordering handling;
- circuit breaking or isolation only when consistent with the platform;
- reconciliation after ambiguous completion.

## Pagination and large results

Avoid unbounded collections. Define default and maximum page size, stable ordering, filters, continuation behavior, and consistency expectations. Do not invent numeric limits; mark them Proposed when not sourced.

## Versioning and rollout

Prefer additive compatibility where safe. When breaking change is required, explain:

- why compatibility cannot be preserved;
- version or parallel-operation strategy;
- consumer migration sequence;
- coexistence window;
- telemetry for old and new use;
- deprecation and rollback approach.

## Swagger/OpenAPI impact

List exact documentation changes:

- operation and schema additions or modifications;
- examples using fictional data;
- validation constraints;
- security requirements;
- error responses;
- deprecation markers;
- version metadata;
- consumer contract-test impact.

Do not output a full OpenAPI document unless separately requested and compatible with the no-code boundary; the design package should specify the change, not publish a contract.
