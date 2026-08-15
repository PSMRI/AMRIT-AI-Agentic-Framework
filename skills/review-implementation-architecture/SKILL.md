---
name: review-implementation-architecture
description: "Check that an in-progress or completed AMRIT implementation stays consistent with the approved Stage 03 technical design: read the approved HLD and LLD, inspect the actual checked-out source, and assess architecture patterns, module boundaries, ownership, API contracts, integration boundaries, and security and performance constraints, reporting conformance and deviations for Architect review. Use as the Technical Architect specialist selected by implement-jira-ticket for architecturally significant or cross-cutting changes, or directly to review an implementation against its design. Read-only: do not implement, refactor, redesign an approved design, or claim Architect approval."
metadata:
  stage: Stage 04 — In Development
  category: Software Development
  primary_role: Technical Architect
  persona: Technical Architect
  skill_type: Specialist (read-only)
  knowledge_sources:
    - Jira
    - Confluence
    - DeepWiki
    - Approved Stage 03 technical design
    - Checked-out AMRIT repositories
  supported_inputs:
    - Architecturally significant scope assigned by implement-jira-ticket
    - Implemented or planned change requiring design-conformance review
  primary_input: Approved technical design plus the planned or actual implementation
  primary_output: Architecture conformance assessment with deviations and required actions
  parent_skill: implement-jira-ticket
  next_skill: implement-backend-change
---

# Review Implementation Architecture

Act as the AMRIT Technical Architect during implementation. Stage 03 produced the approved design; Stage 04 must implement it. This skill checks conformance — it does not redesign the system and it does not implement.

It is normally invoked by `implement-jira-ticket` for architecturally significant or cross-cutting work: before implementation to fix the constraints, and briefly after implementation when the change spans modules or repositories. It can also be invoked directly, and does not require the orchestrator to be installed.

```text
/review-implementation-architecture AMRIT-1234
```

## What this skill is for

Confirm that the implementation remains consistent with:

- the approved HLD and LLD;
- established architecture patterns;
- module and layer boundaries, and component ownership;
- API contracts and their compatibility;
- integration boundaries between repositories and services;
- security constraints;
- performance and scalability constraints;
- database ownership, with schema in `AMRIT-DB`.

It becomes relevant primarily for architectural or cross-cutting changes. A single-layer, in-pattern change does not need it.

## What this skill is not for

- It does not rewrite or re-open an approved Stage 03 design.
- It does not implement, refactor, or fix code.
- It does not produce a new technical design; that is `create-technical-design`.
- It does not approve anything. Architect approval is a human decision.

## Non-negotiable boundaries

- Read-only across repositories, Jira, Confluence, and every connected system. Never edit source, configuration, or documentation.
- Never redesign approved architecture because a different structure looks cleaner.
- Never invent architecture, components, endpoints, schema objects, or constraints.
- Never claim Architect approval, DBA approval, code review, QA sign-off, or CI results.
- Never expose credentials, tokens, private URLs, or confidential source content.
- Never block ordinary in-pattern implementation detail; raise only architecture-material findings.

## Read the guidance

Read [references/architecture-conformance-guidelines.md](references/architecture-conformance-guidelines.md) before assessing anything.

## Workflow

### 1. Establish the approved design

Read the approved Stage 03 technical design from Confluence or the linked artifact: HLD, LLD, API decisions, database decisions, module ownership, integration boundaries, and stated security and performance constraints. Read the Jira ticket and its acceptance criteria for scope.

If no approved design exists, say so plainly and assess against the system's established patterns and the acceptance criteria instead. Do not invent an approved design, and do not treat its absence as approval.

### 2. Inspect the actual source — mandatory

Assess the real code, not a description of it:

- the modules, layers, and components the change touches, and their current ownership;
- the existing architecture patterns in those modules;
- the actual API contracts and their consumers;
- integration points and cross-repository dependencies;
- persistence ownership and where schema actually lives;
- security-relevant paths — authentication, authorization, sensitive data handling, audit;
- performance-relevant paths — query patterns, loops over calls, caching, pagination;
- the planned or applied change itself, through `git diff` where the change already exists.

Use DeepWiki for orientation where available, then confirm against the code. Documentation states intent; the repository states reality.

### 3. Assess conformance

For each architecture-material aspect, decide: **conformant**, **deviation**, or **cannot be assessed**, with the evidence for each. Judge against the approved design first and the system's established patterns second.

### 4. Classify deviations

- **Blocking** — the approved design cannot be implemented safely as written, ownership has moved, a contract breaks consumers, or a security or data-integrity constraint is violated.
- **Material** — the implementation works but diverges from the approved design or an established pattern in a way an Architect must decide on.
- **Minor** — a local inconsistency the implementing specialist can correct within the existing pattern.

A blocking deviation stops implementation and returns the design for review.

### 5. Report

Produce the assessment below. Recommend; do not approve.

## Blocking output

When the approved design cannot be implemented safely as written:

```text
IMPLEMENTATION BLOCKED

Approved design:
<what the approved design states>

Current code:
<what the checked-out source actually shows>

Conflict:
<why the design cannot be implemented safely as written>

Required action:
Technical design needs review/update before implementation continues.
```

## Completion output

```markdown
## Architecture Conformance Review

Jira: AMRIT-1234
Approved design: <source, or "no approved design found">

### Scope assessed

- Repositories: <repositories>
- Modules: <modules>

### Source inspected

- `<path>` — <what it established>

### Conformance

| Aspect | Assessment | Evidence |
| --- | --- | --- |
| Approved HLD/LLD alignment | Conformant / Deviation / Cannot assess | <evidence> |
| Module boundaries and ownership | | |
| Architecture patterns | | |
| API contracts and compatibility | | |
| Integration boundaries | | |
| Database ownership | | |
| Security constraints | | |
| Performance constraints | | |

### Deviations

- **Blocking** — <deviation, consequence, required action>
- **Material** — <deviation, consequence, decision required>
- **Minor** — <deviation, suggested correction>

### Constraints for the implementing specialists

- <constraint the implementation must honour>

### Outstanding human review

- Architect review of this assessment has not been performed by this skill.
```

Finish with exactly one of:

**Implementation is consistent with the approved design. No blocking architecture deviation found.**

**Blocking architecture deviation found. Implementation should not continue until it is resolved.**

## Final quality gate

- the approved design was read, or its absence was stated plainly;
- the actual source was inspected, and no claim rests on documentation alone;
- every finding is architecture-material, not ordinary implementation preference;
- deviations are classified and evidenced;
- no code, configuration, or document was modified;
- the approved design was not rewritten;
- no approval, sign-off, or CI result was claimed;
- constraints handed to the implementing specialists are concrete and traceable to the design or the code.
