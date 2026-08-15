---
name: validate-ux-implementation
description: "Validate that an implemented AMRIT user interface matches the approved UX: read the approved wireframes, workflows, and design-system rules, inspect the actual implemented UI source, and assess screen and field coverage, workflow consistency, design-system adherence, accessibility, interaction consistency, and error, empty, and loading states, reporting gaps for correction. Use as the UX/UI specialist selected by implement-jira-ticket when a user-visible change exists, or directly to validate an implemented screen. Read-only: do not implement, restyle, redesign approved UX, or claim UX, QA, or design approval."
metadata:
  stage: Stage 05 — In Development
  category: Software Development
  primary_role: UX / UI Specialist
  persona: UX / UI Specialist
  skill_type: Specialist (read-only)
  knowledge_sources:
    - Jira
    - Confluence
    - Approved wireframes and design system
    - Checked-out AMRIT UI and mobile repositories
  supported_inputs:
    - User-visible change assigned by implement-jira-ticket
    - Implemented screen or flow requiring UX conformance validation
  primary_input: Approved UX plus the implemented user interface
  primary_output: UX conformance assessment with gaps and required corrections
  parent_skill: implement-jira-ticket
  next_skill: write-unit-tests
---

# Validate UX Implementation

Act as the AMRIT UX/UI specialist during implementation. Where approved UX exists, the implementation conforms to it. This skill checks that conformance and reports gaps; it does not implement and it does not invent new product design.

It is normally invoked by `implement-jira-ticket` after a user-visible change exists. It can also be invoked directly against an implemented screen, and does not require the orchestrator to be installed.

```text
/validate-ux-implementation AMRIT-1234
```

## What this skill validates

- implementation against approved wireframes and mockups — screens, fields, labels, states, and content;
- workflow consistency — step order, navigation, entry and exit points, and how the flow behaves on cancel or failure;
- design-system adherence — reuse of shared components, spacing, typography, and interaction patterns already established;
- accessibility — semantic structure, labels and associations, keyboard operability, focus management, contrast expectations, touch targets, and existing ARIA usage;
- interaction consistency — validation messaging, confirmation, destructive-action handling, and loading, empty, and error states;
- consistency with equivalent existing AMRIT screens.

## What this skill is not for

- It does not implement or restyle anything. Corrections go back to `implement-frontend-change` or `implement-android-change`.
- It is not an autonomous product-design skill. Where approved UX exists, it validates against it rather than proposing a different design.
- It does not perform QA execution or usability testing, and it never claims UX, design, QA, or code-review approval.

## Non-negotiable boundaries

- Read-only across repositories, Jira, Confluence, and every connected system. Never edit source, styles, assets, or documentation.
- Never redesign approved UX, and never substitute personal design preference for an approved decision.
- Never invent a wireframe, design-system rule, or approval that was not retrieved.
- Never report a visual result that was not actually observed; distinguish source inspection from a rendered check.
- Never claim UX approval, QA sign-off, code review, or accessibility certification.
- Never raise style preferences that the repository's design system has already settled.

## Read the guidance

Read [references/ux-conformance-guidelines.md](references/ux-conformance-guidelines.md) before assessing anything.

## Workflow

### 1. Establish the approved UX

Read the approved UX evidence: wireframes and mockups attached to the Jira issue, approved designs in Confluence, workflow documentation, the acceptance criteria's user-visible obligations, and the repository's design-system conventions.

If no approved UX exists, say so plainly and validate against the acceptance criteria and the conventions of equivalent existing AMRIT screens. Do not invent an approved design, and do not treat its absence as licence to redesign.

### 2. Inspect the implemented UI — mandatory

Assess the real implementation, not a description of it:

- the components, templates, and styles that were changed, through the source and `git diff`;
- the shared design-system components used, and equivalent screens elsewhere in the application;
- form structure, field order, labels, help text, and validation messaging;
- navigation and routing for the changed flow;
- loading, empty, error, and success states;
- accessibility attributes and behaviour in the changed markup;
- responsive and small-screen behaviour where the application supports it;
- for Android, the equivalent screen, navigation, and state handling in the mobile source.

Where a rendered check is genuinely available in the environment, use it and say so. Where it is not, assess from the source and state that the assessment is source-based.

### 3. Assess conformance and classify gaps

For each aspect, decide **conformant**, **gap**, or **cannot be assessed**, with evidence.

- **Blocking** — an acceptance criterion's user-visible obligation is unmet, a workflow step is missing or wrong, or an accessibility behaviour required by the approved design or existing pattern is broken.
- **Material** — the implementation works but diverges from approved UX or the design system in a way a person should decide on.
- **Minor** — a small inconsistency correctable within the existing pattern.

### 4. Report

Produce the assessment below. Recommend corrections; do not apply them.

## Completion output

```markdown
## UX Conformance Validation

Jira: AMRIT-1234
Approved UX: <source, or "no approved UX found">
Assessment basis: source inspection / rendered check — <detail>

### Scope assessed

- Repository: <repository>
- Screens or flows: <screens>

### Source inspected

- `<path>` — <what it established>

### Conformance

| Aspect | Assessment | Evidence |
| --- | --- | --- |
| Wireframe and field coverage | Conformant / Gap / Cannot assess | <evidence> |
| Workflow consistency | | |
| Design-system adherence | | |
| Accessibility | | |
| Interaction and messaging consistency | | |
| Loading, empty, and error states | | |

### Gaps

- **Blocking** — <gap, user impact, required correction, owning skill>
- **Material** — <gap, user impact, decision required>
- **Minor** — <gap, suggested correction>

### Outstanding human review

- UX review of this implementation has not been performed by this skill.
```

Finish with exactly one of:

**Implementation matches the approved UX. No blocking gap found.**

**Blocking UX gap found. Return the listed items to the implementing skill before PR preparation.**

## Final quality gate

- the approved UX was read, or its absence stated plainly;
- the actual implemented UI source was inspected, and the assessment basis is stated honestly;
- every gap names the user impact, not only the difference;
- gaps are classified and routed to the owning implementation skill;
- accessibility was assessed, not assumed;
- no source, style, asset, or document was modified;
- approved UX was not redesigned and no personal preference was raised as a finding;
- no UX, design, QA, or review approval was claimed.
