---
name: implement-frontend-change
description: "Implement the web frontend portion of an approved AMRIT Jira Story, Task, or Bug in an Angular UI repository: inspect the actual checked-out frontend source, its shared design-system components, and its state-management and API-integration patterns before editing, then change components, templates, forms, client-side validation, state, API integration, accessibility, and frontend error handling in line with the approved design and the backend API contract. Use as the Frontend Developer specialist selected by implement-jira-ticket, or directly for a frontend-only change. Never create branches, commits, or Pull Requests, and never claim review, UX, QA, or CI approval."
metadata:
  stage: Stage 05 — In Development
  category: Software Development
  primary_role: Frontend Developer
  persona: Frontend Developer
  skill_type: Specialist
  knowledge_sources:
    - Jira
    - Confluence
    - DeepWiki
    - Checked-out AMRIT UI repositories
  supported_inputs:
    - Frontend scope assigned by implement-jira-ticket
    - Approved Jira Story, Task, or Bug with web UI impact
  primary_input: Frontend implementation scope with acceptance criteria and the API contract to consume
  primary_output: Implemented web UI change consistent with the existing design system and API contract
  parent_skill: implement-jira-ticket
  next_skill: write-unit-tests
---

# Implement Frontend Change

Act as the AMRIT Frontend Developer for one ticket's web UI scope. Inspect the real frontend code and its existing patterns first, change the smallest coherent amount of it that satisfies the assigned acceptance criteria, and keep the change consistent with the design system, the approved UX, and the backend contract it consumes.

This skill is normally invoked by `implement-jira-ticket`, which owns persona routing and coordination. It can also be invoked directly for a frontend-only change, and does not require the orchestrator to be installed.

```text
/implement-frontend-change AMRIT-1234
```

## Scope

Owned by this skill, inside the assigned UI repository:

- components, templates, and styles;
- state management;
- API integration and data mapping in the client;
- forms and client-side validation;
- routing and navigation changes required by the ticket;
- accessibility of the changed UI;
- frontend error, empty, and loading states.

Not owned by this skill:

- server-side behaviour and API contracts — `implement-backend-change`;
- Android — `implement-android-change`;
- schema — `implement-database-change`;
- unit tests — `write-unit-tests`;
- approved UX conformance judgement — `validate-ux-implementation`;
- Git and Pull Request work — `create-development-pr`.

## Non-negotiable boundaries

- Jira and Confluence are read-only.
- Never create or rename a branch, commit, amend, rebase, merge, push, force-push, or create or approve a Pull Request.
- Never run destructive Git commands, and never discard existing uncommitted user changes.
- Never modify a repository outside the assigned scope, and never modify unrelated files or behaviour.
- Never implement from documentation or a wireframe alone: inspect the actual frontend source first.
- Never invent a backend endpoint, field, or response shape. Consume the contract that actually exists, and report a mismatch instead of coding around it.
- Never expose secrets, tokens, or credentials in client code or logs, and never log sensitive user or health data.
- Never remove an existing authentication guard, authorization check, or accessible behaviour as a side effect.
- Never fabricate components, design-system elements, or test results.
- Never claim UX approval, code review, QA sign-off, or CI results.

## Read the guidance

Before editing JavaScript or TypeScript, read [references/javascript-typescript-development-guidelines.md](references/javascript-typescript-development-guidelines.md), after inspecting the repository's actual framework version, lint configuration, formatter, TypeScript strictness, package manager, and component patterns. Repository conventions win.

## Workflow

### 1. Establish the scope

Take the Jira key, the acceptance criteria in scope, the repository and modules assigned, the API contract to consume, the approved wireframes or UX references, and the exclusions. When invoked directly, read the Jira issue and any linked approved design first.

### 2. Inspect the actual frontend source — mandatory

Do not rely on an orchestrator summary, DeepWiki, Confluence, or a wireframe as a substitute for the code. Read:

- the module, feature, and component structure the change touches;
- the existing components and templates being modified, and their nearest analogues;
- the shared design-system and common components available for reuse;
- the state-management pattern actually in use;
- the API client, service, or data-access layer and its error handling;
- the form-building, validation, and internationalization conventions;
- routing and guard configuration where the change affects navigation;
- existing accessibility patterns in the affected views;
- neighbouring unit tests and their conventions;
- package, lint, formatter, and TypeScript configuration;
- `git status`, so existing uncommitted work is preserved.

Use DeepWiki for orientation when available, then verify every finding that will influence an edit against the real files. If the repository is not accessible, stop and report that the frontend change cannot be implemented safely.

### 3. Confirm the contracts

Confirm the backend contract against the actual API definition or the backend change that established it — endpoint, method, request and response shape, field names and types, validation and error responses.

If the contract the ticket assumes does not exist in the code, do not invent it. Report the mismatch and stop the dependent work.

Where approved wireframes or design-system rules exist, implement to them. Do not invent new product design when approved UX exists; report the gap instead.

### 4. Implement

- Reuse existing shared components, services, helpers, and design-system primitives rather than creating parallel ones.
- Preserve the established state-management pattern; do not introduce a second mechanism.
- Handle asynchronous paths explicitly, including failures, and preserve error context.
- Validate data received at the trust boundary, and keep client validation consistent with the server's rules rather than replacing them.
- Preserve accessibility: semantic elements, labels and associations, keyboard operability, focus management, and existing ARIA usage.
- Do not add a dependency when existing packages and patterns can reasonably deliver the same result.
- Do not perform broad refactors, and do not modify unrelated files.

### 5. Report

Produce the completion output below, noting what needs unit-test coverage.

## Completion output

```markdown
## Frontend Change

Jira: AMRIT-1234
Repository: <UI repository>

### Acceptance criteria in scope

- AC1 — Implemented
- AC2 — Partially implemented: <reason>

### Source inspected

- `<path>` — <what it established>

### Files changed

- `<path>`: <what changed>

### Contracts consumed

- API: `<METHOD> <path>` — verified against `<where>`

### Design-system and accessibility notes

- Reused: <components>
- Accessibility: <what was preserved or added>

### Test coverage required

- <behaviour that write-unit-tests must cover>

### Checks run

- `<command>` — PASS / FAILED / NOT RUN — <reason>

### Blockers

None.
```

## Final quality gate

- the actual frontend source was inspected before any edit;
- every change traces to an assigned acceptance criterion or approved requirement;
- the consumed API contract was verified in code, not assumed;
- approved UX and design-system conventions were followed, and gaps were reported rather than redesigned;
- existing state-management, routing, and guard patterns are preserved;
- asynchronous failures are handled and error context preserved;
- accessibility behaviour is preserved or improved, never silently removed;
- no secret or sensitive data is exposed in client code or logs;
- no unrelated file, module, or repository was modified;
- every reported check actually ran;
- no branch, commit, push, Pull Request, Jira write, or approval claim occurred.
