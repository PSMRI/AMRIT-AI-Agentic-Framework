# Java Development Guidelines

## Contents

- [Inspect before writing](#inspect-before-writing)
- [Structure and design](#structure-and-design)
- [Naming and API surface](#naming-and-api-surface)
- [Nullability and validation](#nullability-and-validation)
- [Exceptions and error handling](#exceptions-and-error-handling)
- [Logging](#logging)
- [Data access and performance](#data-access-and-performance)
- [Concurrency and state](#concurrency-and-state)
- [Spring and Spring Boot](#spring-and-spring-boot)
- [Dependencies](#dependencies)
- [Comments and documentation](#comments-and-documentation)
- [Review checklist](#review-checklist)

## Inspect before writing

Before changing Java code, determine from the repository itself:

- the Java language and runtime version;
- the framework and its version;
- the architectural layering actually in use;
- build tooling and module layout;
- formatting configuration;
- Checkstyle, SpotBugs, PMD, SonarQube, or other static-analysis configuration;
- existing coding conventions in the files being changed and their neighbours.

Repository-specific conventions take precedence over every general rule below. Where this document and the surrounding code disagree, follow the code and note the deviation only if it is material.

## Structure and design

- Keep classes and methods focused on a single responsibility.
- Preserve the existing separation of concerns; do not move logic across layers to make a change shorter.
- Prefer an existing abstraction over a new duplicate one.
- Avoid unnecessary inheritance; prefer composition unless the codebase already models the case with a hierarchy.
- Use dependency injection consistently with the project rather than instantiating collaborators inline.
- Avoid hidden global state, static mutable fields, and singletons introduced for convenience.
- Use constants, enums, or value objects where that matches existing project patterns instead of scattering literals.
- Reuse an existing utility only when it is semantically appropriate, not merely because its signature fits.
- Do not create a generic `Utils` dumping ground; place behaviour with the concept that owns it.

## Naming and API surface

- Use meaningful, domain-oriented names that match the vocabulary already used in the module and in the Jira ticket.
- Keep public API compatibility unless the requirement explicitly changes the contract. Additive change is preferred to breaking change.
- When a contract must change, identify the consumers affected and state the compatibility impact in the completion summary.

## Nullability and validation

- Handle nullability intentionally. Follow the repository's existing approach — annotations, `Optional`, defensive checks, or explicit contracts — rather than mixing styles.
- Validate external input at the appropriate boundary: request payloads, integration responses, file or message content, and configuration.
- Do not repeat the same validation at every layer when the codebase already establishes one owner for it.
- Keep validation messages free of sensitive data.

## Exceptions and error handling

- Do not swallow exceptions. An empty or log-only catch block that hides a real failure is a defect.
- Avoid broad `catch (Exception)` unless the surrounding repository has a justified boundary-level pattern, such as a controller advice or a scheduled-job wrapper.
- Preserve useful causes: pass the original exception when wrapping.
- Use the repository's existing domain or application exception conventions rather than introducing a parallel hierarchy.
- Do not use exceptions for ordinary control flow.
- Fail with a message that helps diagnosis without disclosing secrets, credentials, tokens, or personal or clinical data.

## Logging

- Use the repository's logging framework and existing patterns.
- Never log passwords, API tokens, private keys, authentication headers, full request payloads containing personal or clinical data, or secret configuration values.
- Use appropriate levels: `error` for failures needing attention, `warn` for recoverable anomalies, `info` for meaningful lifecycle events, `debug` for diagnostic detail.
- Do not add high-volume logging inside hot paths or per-row loops.

## Data access and performance

- Avoid unnecessary repeated database or network calls, especially inside loops.
- Avoid N+1 query patterns; use the repository's existing fetching or batching approach.
- Preserve existing transaction boundaries. Do not widen a transaction to include external calls, and do not split one that guarantees atomicity required by the requirement.
- Keep query changes consistent with the repository's persistence style, whether that is JPA, an ORM mapping, or explicit SQL.
- Do not add caching, indexes, or asynchronous behaviour that the ticket does not require and the evidence does not justify.

## Concurrency and state

- Preserve existing concurrency and thread-safety expectations of the classes being changed.
- Avoid introducing mutable shared state unnecessarily; prefer immutable data and local state.
- When concurrent updates are in scope, use the mechanism the codebase already uses — optimistic version, lock, or database constraint — instead of inventing a new one.

## Spring and Spring Boot

- Respect the repository's existing layering and patterns. Do not impose an arbitrary Controller-Service-Repository structure on a codebase organized differently.
- Follow existing conventions for component registration, configuration properties, profiles, transaction management, validation, exception handling, and security configuration.
- Prefer constructor injection when the repository already uses it.
- Do not change bean scope, transaction propagation, or security configuration as an incidental side effect of a feature change.

## Dependencies

Do not add a new framework or library when the same result can reasonably be achieved with dependencies and patterns already present. When a new dependency is genuinely required, state in the completion summary what it is, why nothing existing suffices, and where it was declared.

## Comments and documentation

Document only non-obvious decisions: a constraint, a workaround, a non-intuitive ordering, or a rule that comes from the requirement rather than the code. Do not narrate straightforward code, and do not leave commented-out code behind.

## Review checklist

Before considering the Java change complete:

- every change traces to an acceptance criterion or a supporting requirement;
- the change matches the repository's actual conventions and layering;
- no unrelated file or behaviour was modified;
- nullability, validation, and error handling are intentional;
- no exception is swallowed and no cause is lost;
- no secret or sensitive payload is logged;
- no new N+1 or redundant call was introduced;
- transaction and concurrency behaviour is preserved;
- public API compatibility is preserved or the break is explicitly required and reported;
- formatting, lint, and static-analysis configuration in the repository still pass.
