# review-implementation-architecture

`review-implementation-architecture` is the **Technical Architect** specialist for Stage 05 — In Development. It checks that an implementation stays consistent with the approved Stage 03 technical design.

**This skill is read-only.** It never edits source, configuration, or documentation.

## Purpose

Stage 03 designs; Stage 05 implements. This skill exists to keep the implementation faithful to the approved design — HLD and LLD alignment, architecture patterns, module boundaries and ownership, API contracts, integration boundaries, database ownership, and security and performance constraints — and to surface deviations for Architect decision.

## Relationship to `implement-jira-ticket`

`implement-jira-ticket` selects this persona only for architecturally significant or cross-cutting work: before implementation to fix the constraints, and briefly after implementation when the change spans modules or repositories.

```text
implement-jira-ticket
    ├── review-implementation-architecture    (before implementation)
    ├── implement-database-change
    ├── implement-backend-change
    ├── implement-frontend-change
    └── write-unit-tests
```

The skill is independently installable and independently invocable. When it is not installed, the orchestrator applies the Architect conformance persona inline.

## When it is warranted

When the change spans repositories, crosses a module or service boundary, introduces a new component or contract, changes data or behaviour ownership, changes an integration boundary, affects authentication, authorization, sensitive health data, audit trails, or encryption, has material performance implications, or appears to deviate from the approved design.

Not warranted for a single-layer, in-pattern change that touches no contract, no boundary, and no security or performance constraint. Architecture review that raises ordinary preferences trains people to ignore it.

## What it does not do

- It does not rewrite or re-open an approved Stage 03 design.
- It does not implement, refactor, or fix code.
- It does not produce a new technical design; that is [`create-technical-design`](../create-technical-design/README.md).
- It does not approve anything. Architect approval is a human decision, reported as outstanding.

## It reads the code itself

Assessment is made against the real source: the modules and components the change touches and their current ownership, the actual API contracts and their consumers, integration points, persistence ownership, security-relevant paths, performance-relevant paths, and the diff where the change already exists. DeepWiki is used for orientation only.

If no approved design exists, the skill says so plainly and assesses against the system's established patterns and the acceptance criteria. It never invents an approved design, and never treats its absence as approval.

## Deviation classes

- **Blocking** — the approved design cannot be implemented safely as written; implementation stops and the design returns for review.
- **Material** — the implementation diverges in a way an Architect must decide on.
- **Minor** — a local inconsistency the implementing specialist can correct.

## Required capabilities

Read access to Jira, Confluence, and DeepWiki, plus read access to the checked-out repositories. Tool names are discovered, not hardcoded.

## Use and distribution

Invoke `/review-implementation-architecture` from the repository root using a supported coding agent, or let `/implement-jira-ticket` route to it. For a packaged installation, download `review-implementation-architecture.zip` from the latest release. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
