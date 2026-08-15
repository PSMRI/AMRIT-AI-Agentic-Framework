# JavaScript and TypeScript Development Guidelines

## Contents

- [Inspect before writing](#inspect-before-writing)
- [Structure and design](#structure-and-design)
- [Asynchronous behaviour and errors](#asynchronous-behaviour-and-errors)
- [Data handling and comparison](#data-handling-and-comparison)
- [TypeScript typing](#typescript-typing)
- [Frontend components and state](#frontend-components-and-state)
- [Performance](#performance)
- [Security and privacy](#security-and-privacy)
- [Accessibility](#accessibility)
- [Dependencies](#dependencies)
- [Review checklist](#review-checklist)

## Inspect before writing

Before changing JavaScript or TypeScript code, determine from the repository itself:

- the Node or runtime version;
- the framework and its version;
- the ESLint configuration and active rule set;
- the formatter configuration;
- the TypeScript configuration when present, including strictness flags;
- the package manager and lockfile in use;
- existing component and module patterns;
- state-management conventions;
- the existing unit-test framework and its configuration.

Repository-specific conventions take precedence over every general rule below. Where this document and the surrounding code disagree, follow the code.

## Structure and design

- Keep functions, modules, and components focused on one responsibility.
- Use meaningful names consistent with the module's existing vocabulary.
- Avoid duplicating business logic across components, services, or utilities; extend the existing owner instead.
- Prefer existing abstractions, services, helpers, and shared modules over new parallel ones.
- Avoid unnecessary mutation; prefer returning new values where the codebase already does so.
- Keep side effects out of pure helpers and rendering paths.

## Asynchronous behaviour and errors

- Handle asynchronous operations explicitly. Follow the repository's style — `async`/`await`, promise chains, or observables — rather than mixing them in one flow.
- Never silently ignore a rejected promise or a failed subscription; handle it or propagate it deliberately.
- Preserve error context when catching and rethrowing; do not replace an error with a bare string that loses the cause.
- Clean up subscriptions, timers, and listeners according to the framework's existing lifecycle conventions.

## Data handling and comparison

- Validate data received at trust boundaries: API responses, user input, route or query parameters, storage, and messages from other windows or workers.
- Avoid unsafe type coercion and implicit conversions in business logic.
- Use strict comparison (`===`, `!==`) unless the repository intentionally requires otherwise in a specific place.
- Guard against undefined and null explicitly where the data source can produce them.

## TypeScript typing

- Avoid weakening types with `any`. Use it only when genuinely necessary, and state why in a short comment.
- Prefer existing interfaces and types over introducing overlapping models of the same concept.
- Keep types close to the data's real shape rather than asserting a convenient one; avoid unchecked `as` casts across a trust boundary.
- Respect the project's strictness settings; do not disable a compiler or lint rule to make a change compile.

## Frontend components and state

- Preserve existing state-management patterns. Do not introduce a second state mechanism alongside the established one.
- Reuse the repository's existing design system and shared components rather than creating parallel UI primitives.
- Keep component inputs and outputs consistent with the surrounding component API style.
- Preserve existing routing, form-handling, and validation conventions.
- Preserve API compatibility for anything other modules consume, unless the requirement explicitly changes it.

## Performance

- Avoid unnecessary re-renders and repeated expensive computation in render or change-detection paths.
- Do not fetch the same data repeatedly when the codebase already caches or shares it.
- Keep list rendering, change detection, and subscription patterns consistent with what the module already uses.
- Do not add memoization or virtualization the ticket does not require and the evidence does not justify.

## Security and privacy

- Never expose secrets, API keys, tokens, or credentials in browser or client code, including build-time configuration bundled into the client.
- Never log sensitive user, health, or authentication data to the console or a telemetry sink.
- Preserve existing authentication and authorization checks and route guards.
- Avoid rendering untrusted content as raw HTML; follow the framework's sanitization conventions.

## Accessibility

Preserve accessibility patterns when modifying UI: semantic elements, labels and associations, keyboard operability, focus management, and existing ARIA usage. Do not remove an accessible name, role, or focus behaviour as an incidental side effect.

## Dependencies

Do not add a dependency when existing packages and patterns can reasonably deliver the same result. When a new dependency is genuinely required, state in the completion summary what it is, why nothing existing suffices, and where it was declared. Keep the lockfile consistent with the repository's package manager.

## Review checklist

Before considering the JavaScript or TypeScript change complete:

- every change traces to an acceptance criterion or a supporting requirement;
- the change matches the repository's framework, lint, formatting, and typing configuration;
- no unrelated file or behaviour was modified;
- asynchronous paths handle failure explicitly and preserve context;
- data crossing a trust boundary is validated;
- no `any`, cast, or disabled rule was introduced without justification;
- existing state-management and design-system patterns are preserved;
- no secret or sensitive data is exposed in client code or logs;
- accessibility behaviour is preserved;
- lint, type check, and tests defined by the repository still pass.
