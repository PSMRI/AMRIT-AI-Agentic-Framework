# Kotlin and Android Development Guidelines

## Contents

- [Inspect before writing](#inspect-before-writing)
- [Architecture and structure](#architecture-and-structure)
- [Kotlin language use](#kotlin-language-use)
- [Concurrency and lifecycle](#concurrency-and-lifecycle)
- [UI and navigation](#ui-and-navigation)
- [Local persistence](#local-persistence)
- [Offline behaviour and synchronization](#offline-behaviour-and-synchronization)
- [Networking and API integration](#networking-and-api-integration)
- [Platform constraints](#platform-constraints)
- [Security and privacy](#security-and-privacy)
- [Performance and resource use](#performance-and-resource-use)
- [Dependencies](#dependencies)
- [Review checklist](#review-checklist)

## Inspect before writing

Before changing Android or Kotlin code, determine from the repository itself:

- the Kotlin, Gradle, and Android Gradle Plugin versions;
- the minimum, target, and compile SDK levels;
- the architecture actually in use — layering, view models, use cases, repositories;
- the UI toolkit in the affected screens and its component conventions;
- the dependency-injection approach;
- the coroutine, threading, and reactive conventions;
- the local database and its migration mechanism;
- the offline and synchronization mechanism;
- the networking stack, serialization, and error-handling patterns;
- lint, static-analysis, and formatting configuration;
- build variants and flavours that affect the change;
- the existing unit-test framework and conventions.

Repository-specific conventions take precedence over every general rule below. Where this document and the surrounding code disagree, follow the code.

## Architecture and structure

- Keep classes, view models, and functions focused on a single responsibility.
- Follow the app's existing layering; do not move logic across layers to make a change shorter.
- Keep business rules out of activities, fragments, and composables; place them where the app already puts them.
- Prefer extending an existing abstraction over adding a parallel one.
- Use the project's dependency-injection style rather than instantiating collaborators inline or reaching for a service locator.
- Avoid hidden global state and singletons introduced for convenience.

## Kotlin language use

- Prefer immutability: `val` over `var`, and immutable collections and data classes where the codebase already does.
- Handle nullability intentionally; do not use `!!` to silence the compiler.
- Use sealed classes or enums for closed state and result sets when that matches existing patterns.
- Keep extension functions discoverable and scoped; do not create a general dumping ground.
- Do not swallow exceptions; preserve the cause when wrapping, and follow the app's existing error model.

## Concurrency and lifecycle

- Use the project's coroutine scopes, dispatchers, and cancellation conventions; do not launch work in an unmanaged global scope.
- Respect lifecycle: cancel or scope work so it does not outlive its owner or leak a context.
- Handle configuration changes and process death as the surrounding code already does.
- Keep long-running or deferrable work in the mechanism the app already uses for background execution.
- Never block the main thread with disk, database, or network work.

## UI and navigation

- Reuse existing components, themes, styles, and layout conventions rather than introducing parallel primitives.
- Follow the existing navigation mechanism; do not add a second one.
- Preserve state restoration behaviour on rotation and return from background.
- Implement loading, empty, and error states consistently with neighbouring screens.
- Preserve accessibility: content descriptions, touch-target sizes, focus order, and text scaling.
- Follow approved wireframes and the design system where they exist; report gaps rather than inventing new product design.

## Local persistence

- Follow the existing local-database structure, DAO conventions, and type converters.
- Any change to the local schema requires a proper migration path for already-installed apps; never rely on destructive fallback migration for user data.
- Keep entity and mapping changes compatible with the data currently on devices.
- Do not store more personal or clinical data on the device than the requirement needs.

## Offline behaviour and synchronization

- Determine explicitly whether the changed flow must work without connectivity.
- Preserve the existing queueing, retry, backoff, and conflict-resolution behaviour; do not weaken it for convenience.
- Never silently drop a queued record, and never let a failed sync surface as success.
- Keep sync idempotent where the existing mechanism requires it, so a retry does not duplicate data.
- Make failure states visible to the user in the way the app already does.

## Networking and API integration

- Use the existing API client, serialization, and error-mapping layer.
- Consume the contract the backend actually exposes; verify it rather than assuming a field name or shape.
- Handle timeouts, connectivity loss, and non-success responses explicitly.
- Do not perform network calls from UI layers when the app routes them through a repository or use case.

## Platform constraints

- Respect the minimum supported API level and guard newer platform APIs as the repository already does.
- Request permissions using the app's existing flow, and handle denial without crashing or blocking unrelated features.
- Respect background-execution and battery restrictions rather than working around them.
- Consider low-connectivity, low-storage, and low-end-device conditions, which are ordinary conditions for AMRIT field use.

## Security and privacy

- Never hard-code credentials, API keys, or tokens in the application or its build configuration.
- Never log authentication data, personal data, or clinical data.
- Preserve existing encryption, secure-storage, and session-handling behaviour.
- Keep sensitive data out of exported components, logs, backups, and screenshots where the app already protects it.

## Performance and resource use

- Avoid unnecessary work in list binding, recomposition, and scroll paths.
- Avoid repeated network or database calls where the app already caches or shares data.
- Avoid unnecessary wake locks, polling, and background sync.
- Watch memory use with images and large result sets, following existing patterns.

## Dependencies

Do not add a library when existing dependencies and patterns can reasonably deliver the same result. When a new dependency is genuinely required, state what it is, why nothing existing suffices, where it was declared, and its effect on build configuration and minimum API level.

## Review checklist

Before considering the Android change complete:

- every change traces to an acceptance criterion or a supporting requirement;
- the change matches the app's actual architecture, DI, threading, and UI conventions;
- no unrelated file or behaviour was modified;
- lifecycle, cancellation, and configuration-change behaviour is correct;
- local schema changes carry a valid migration path for installed apps;
- offline, queueing, retry, and conflict behaviour is preserved and described;
- the consumed API contract was verified against the real backend definition;
- permissions, background execution, and API-level guards are handled;
- no secret is hard-coded and no sensitive data is logged;
- accessibility behaviour is preserved;
- lint, static analysis, and the repository's tests still pass.
