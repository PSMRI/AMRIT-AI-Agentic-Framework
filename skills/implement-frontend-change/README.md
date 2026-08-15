# implement-frontend-change

`implement-frontend-change` is the **Frontend Developer** specialist for Stage 04 — In Development. It implements the web UI portion of one approved AMRIT Jira ticket in an Angular UI repository.

**This skill changes source files.**

## Purpose

Turn the frontend scope of an approved ticket into a minimal, convention-respecting change to components, state, API integration, forms, client validation, accessibility, and frontend error handling — after inspecting the actual frontend source and the shared design system.

## Relationship to `implement-jira-ticket`

`implement-jira-ticket` is the normal Stage 04 entry point. It routes to this skill only when the ticket actually changes the web UI.

```text
implement-jira-ticket
    ├── implement-backend-change     (establishes the API contract)
    └── implement-frontend-change    (consumes it)
        └── write-unit-tests
```

The skill is independently installable and independently invocable for a frontend-only change. It does not require the orchestrator at runtime, and when it is not installed the orchestrator applies the Frontend Developer persona inline.

## When to use it

Use it when the ticket changes web UI behaviour in an AMRIT UI repository — components, screens, forms, client validation, state management, API consumption in the browser, routing, accessibility, or frontend error handling.

Do not use it for server-side behaviour, Android, schema changes, unit-test authoring, UX conformance judgement, or Git and Pull Request work.

## It reads the code itself

The skill never implements from an orchestrator summary, a wireframe, DeepWiki, or Confluence alone. Before editing it inspects the feature and component structure, the components being changed and their nearest analogues, the shared design-system components, the state-management pattern, the API client layer, form and validation conventions, routing and guards, existing accessibility patterns, neighbouring tests, and the lint, formatter, and TypeScript configuration.

If the repository is not accessible, it stops rather than implementing from documentation.

## Contract discipline

The skill consumes the backend contract that actually exists in the code or the API definition. It never invents an endpoint, field, or response shape: a mismatch between the ticket's assumption and the real contract is reported and stops the dependent work.

Where approved wireframes and design-system rules exist, the implementation follows them. New product design is not invented in Stage 04; gaps are reported. `validate-ux-implementation` performs the separate conformance check.

## Git, Jira, and approval boundaries

The skill may inspect `git status`, `git diff`, and history. It never creates a branch, commit, push, or Pull Request, never writes to Jira or Confluence, and never claims UX approval, code review, QA sign-off, or CI results.

## Required capabilities

Read access to Jira, Confluence, and DeepWiki, plus the host's filesystem, repository-editing, and command-execution capabilities. Tool names are discovered, not hardcoded. If DeepWiki is unavailable the skill inspects the repository directly and says so.

## Use and distribution

Invoke `/implement-frontend-change` from the repository root using a supported coding agent, or let `/implement-jira-ticket` route to it. For a packaged installation, download `implement-frontend-change.zip` from the latest release. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
