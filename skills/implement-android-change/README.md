# implement-android-change

`implement-android-change` is the **Android / Kotlin Developer** specialist for Stage 05 — In Development. It implements the mobile portion of one approved AMRIT Jira ticket in a Kotlin Android repository such as `FLW-Mobile-App` or `HWC-Mobile-App`.

**This skill changes source files.**

## Purpose

Turn the Android scope of an approved ticket into a minimal, convention-respecting Kotlin change to screens, mobile flows, local persistence, API integration, and offline behaviour — after inspecting the actual Android source, its architecture, and its synchronization mechanism.

## Relationship to `implement-jira-ticket`

`implement-jira-ticket` routes to this skill only when the Android application is actually in scope.

```text
implement-jira-ticket
    ├── implement-android-change
    └── write-unit-tests
```

The skill is independently installable and independently invocable for an Android-only change. When it is not installed, the orchestrator applies the Android persona inline.

## When to use it

Use it when the ticket changes the AMRIT Android applications — mobile screens and flows, Kotlin implementation, local persistence, offline behaviour and sync, API integration on the device, or platform-constrained behaviour.

Do not use it for server-side behaviour, web UI, `AMRIT-DB` schema, unit-test authoring, or Git and Pull Request work.

## It reads the code itself

Before editing, the skill inspects the module structure and architecture in use, the affected screens and navigation, the UI conventions, the local database and its migration approach, the offline and synchronization mechanism, the network layer and error handling, dependency injection and coroutine conventions, permission and lifecycle patterns, Gradle configuration and API levels, and neighbouring tests.

If the repository is not accessible, it stops rather than implementing from documentation.

## Offline and device constraints

AMRIT mobile applications are used in low-connectivity field conditions. The skill establishes explicitly whether the changed flow must work offline, what is queued, when it syncs, and how conflicts and failures surface — and it never weakens existing queueing, retry, or conflict handling as a side effect. A local schema change always carries a migration path for already-installed apps.

## Contract discipline

The skill consumes the backend contract that actually exists, verified against the API definition or the backend change that established it. It never invents an endpoint, field, or response shape; a mismatch is reported and stops the dependent work.

## Git, Jira, and approval boundaries

The skill may inspect `git status`, `git diff`, and history. It never creates a branch, commit, push, or Pull Request, never writes to Jira or Confluence, and never claims code review, QA sign-off, or CI results.

## Required capabilities

Read access to Jira, Confluence, and DeepWiki, plus the host's filesystem, repository-editing, and command-execution capabilities. Tool names are discovered, not hardcoded. Android builds and instrumentation may not be runnable in every environment; unavailable checks are reported as `NOT RUN` with the reason, never as passing.

## Use and distribution

Invoke `/implement-android-change` from the repository root using a supported coding agent, or let `/implement-jira-ticket` route to it. For a packaged installation, download `implement-android-change.zip` from the latest release. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
