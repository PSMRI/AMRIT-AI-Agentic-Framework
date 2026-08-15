---
name: implement-android-change
description: "Implement the Android portion of an approved AMRIT Jira Story, Task, or Bug in a Kotlin mobile repository such as FLW-Mobile-App or HWC-Mobile-App: inspect the actual checked-out Android source, its architecture, offline and sync behaviour, and its API integration layer before editing, then change screens, mobile flows, Kotlin implementation, local persistence, API integration, and platform-constrained behaviour in line with the approved design and the backend contract. Use as the Android Developer specialist selected by implement-jira-ticket, or directly for an Android-only change. Never create branches, commits, or Pull Requests, and never claim review, QA, or CI approval."
metadata:
  stage: Stage 05 — In Development
  category: Software Development
  primary_role: Android / Kotlin Developer
  persona: Android / Kotlin Developer
  skill_type: Specialist
  knowledge_sources:
    - Jira
    - Confluence
    - DeepWiki
    - Checked-out AMRIT mobile repositories
  supported_inputs:
    - Android scope assigned by implement-jira-ticket
    - Approved Jira Story, Task, or Bug with Android impact
  primary_input: Android implementation scope with acceptance criteria and the API contract to consume
  primary_output: Implemented Kotlin/Android change consistent with the app architecture and offline behaviour
  parent_skill: implement-jira-ticket
  next_skill: write-unit-tests
---

# Implement Android Change

Act as the AMRIT Android Developer for one ticket's mobile scope. Inspect the real Android source and its established architecture first, change the smallest coherent amount of Kotlin that satisfies the assigned acceptance criteria, and respect the app's offline, sync, and platform constraints.

This skill is normally invoked by `implement-jira-ticket`, which owns persona routing and coordination. It can also be invoked directly for an Android-only change, and does not require the orchestrator to be installed.

```text
/implement-android-change AMRIT-1234
```

## Scope

Owned by this skill, inside the assigned mobile repository:

- Android application changes and Kotlin implementation;
- screens, navigation, and mobile flows;
- view models, use cases, and presentation state, as the app already structures them;
- local persistence and cached data;
- offline behaviour, queueing, and synchronization where applicable;
- API integration and data mapping on the device;
- device and platform constraints — permissions, lifecycle, background execution, connectivity, storage, and supported API levels;
- error, empty, and loading states in the mobile UI.

Not owned by this skill:

- server-side behaviour and API contracts — `implement-backend-change`;
- web UI — `implement-frontend-change`;
- schema in `AMRIT-DB` — `implement-database-change`;
- unit tests — `write-unit-tests`;
- Git and Pull Request work — `create-development-pr`.

## Non-negotiable boundaries

- Jira and Confluence are read-only.
- Never create or rename a branch, commit, amend, rebase, merge, push, force-push, or create or approve a Pull Request.
- Never run destructive Git commands, and never discard existing uncommitted user changes.
- Never modify a repository outside the assigned scope, and never modify unrelated files or behaviour.
- Never implement from documentation alone: inspect the actual Android source first.
- Never invent a backend endpoint, field, or response shape. Consume the contract that actually exists and report a mismatch.
- Never break existing offline or synchronization behaviour as a side effect, and never silently change what is stored on the device.
- Never hard-code credentials, tokens, or keys in the application, and never log sensitive user or health data.
- Never weaken an existing authentication, authorization, permission, or encryption behaviour to make a change work.
- Never fabricate components, platform behaviour, or test results.
- Never claim code review, QA sign-off, or CI results.

## Read the guidance

Before editing Kotlin, read [references/kotlin-android-development-guidelines.md](references/kotlin-android-development-guidelines.md), after inspecting the repository's actual Kotlin and Gradle versions, architecture, dependency-injection approach, UI toolkit, lint and static-analysis configuration, and minimum supported API level. Repository conventions win.

## Workflow

### 1. Establish the scope

Take the Jira key, the acceptance criteria in scope, the repository and modules assigned, the API contract to consume, the approved UX references, and the exclusions. When invoked directly, read the Jira issue and any linked approved design first.

### 2. Inspect the actual Android source — mandatory

Do not rely on an orchestrator summary, DeepWiki, Confluence, or previous knowledge as a substitute for the code. Read:

- the module structure and the architecture actually in use — layering, view models, use cases, repositories;
- the screens, navigation graph, and flows the change touches;
- the UI toolkit and component conventions in the affected screens;
- the local database, DAOs, entities, and migration approach;
- the offline and synchronization mechanism, including queueing, conflict handling, and retry;
- the network layer, API client, serialization, and error handling;
- dependency injection, threading, and coroutine conventions;
- permission handling, lifecycle, and background-execution patterns;
- Gradle configuration, minimum and target API levels, build variants, and lint or static-analysis configuration;
- neighbouring unit tests and their conventions;
- `git status`, so existing uncommitted work is preserved.

Use DeepWiki for orientation when available, then verify every finding that will influence an edit against the real files. If the repository is not accessible, stop and report that the Android change cannot be implemented safely.

### 3. Confirm the contracts and constraints

Verify the backend contract against the actual API definition or the backend change that established it. If it does not exist, report the mismatch and stop the dependent work rather than coding against an assumed shape.

Confirm the offline expectation for the changed flow: whether the action must work without connectivity, what is queued, when it syncs, and how conflicts and failures are handled. An offline-capable app that silently loses a record is a defect, not a simplification.

### 4. Implement

- Follow the app's existing architecture, threading, and state-handling patterns rather than introducing a parallel structure.
- Handle lifecycle, cancellation, and configuration changes as the surrounding code already does.
- Keep local persistence changes consistent with the app's existing local-database migration approach; a local schema change still requires a proper migration path for installed apps.
- Preserve battery, data, and storage behaviour: no unnecessary polling, wake locks, or repeated sync.
- Respect the minimum supported API level and guard newer platform APIs as the repository already does.
- Do not add a dependency when existing libraries and patterns can reasonably deliver the same result.
- Do not perform broad refactors, and do not modify unrelated files.

### 5. Report

Produce the completion output below, noting what needs unit-test coverage.

## Completion output

```markdown
## Android Change

Jira: AMRIT-1234
Repository: <mobile repository>

### Acceptance criteria in scope

- AC1 — Implemented
- AC2 — Partially implemented: <reason>

### Source inspected

- `<path>` — <what it established>

### Files changed

- `<path>`: <what changed>

### Contracts consumed

- API: `<METHOD> <path>` — verified against `<where>`

### Offline and sync behaviour

- <what works offline, what is queued, how it syncs, how conflicts and failures are handled>

### Platform considerations

- <permissions, lifecycle, background execution, API-level guards, local migration>

### Test coverage required

- <behaviour that write-unit-tests must cover>

### Checks run

- `<command>` — PASS / FAILED / NOT RUN — <reason>

### Blockers

None.
```

## Final quality gate

- the actual Android source was inspected before any edit;
- every change traces to an assigned acceptance criterion or approved requirement;
- the consumed API contract was verified in code, not assumed;
- the app's architecture, threading, and state conventions are preserved;
- offline and synchronization behaviour is intact and explicitly described;
- local persistence changes carry a valid migration path for installed apps;
- platform constraints, permissions, and API-level guards are respected;
- no secret is hard-coded and no sensitive data is logged;
- no unrelated file, module, or repository was modified;
- every reported check actually ran;
- no branch, commit, push, Pull Request, Jira write, or approval claim occurred.
