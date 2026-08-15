# validate-ux-implementation

`validate-ux-implementation` is the **UX / UI specialist** for Stage 05 — In Development. It validates that an implemented AMRIT user interface matches the approved UX.

**This skill is read-only.** Corrections go back to the implementing skill.

## Purpose

Check the implemented UI against approved wireframes and workflows, the design system, accessibility expectations, and interaction conventions, and report gaps with their user impact.

## Relationship to `implement-jira-ticket`

`implement-jira-ticket` selects this persona only when a user-visible change exists, and runs it after the change has been implemented.

```text
implement-jira-ticket
    ├── implement-frontend-change / implement-android-change
    ├── validate-ux-implementation      (after the user-visible change exists)
    └── write-unit-tests
```

The skill is independently installable and independently invocable against an implemented screen. When it is not installed, the orchestrator applies the UX conformance persona inline.

## Not autonomous product design

Where approved UX exists, the implementation conforms to it. The skill validates against the approved design rather than proposing a different one, and it never restyles or implements anything.

If no approved UX exists, it says so plainly and validates against the acceptance criteria and the conventions of equivalent existing AMRIT screens. It never invents an approved design and never treats its absence as licence to redesign.

## What it assesses

Wireframe and field coverage, workflow consistency, design-system adherence, interaction and messaging consistency, loading, empty and error states, accessibility, and consistency with equivalent existing screens.

Accessibility is assessed rather than assumed: semantic structure, label associations, accessible names, keyboard operability, focus management, error announcement, contrast and text-scaling expectations, and touch-target size. An accessibility behaviour removed as a side effect is a blocking gap.

## Honest assessment basis

The report states whether the assessment came from **source inspection** or from an actual **rendered check**. The skill never describes a visual result it did not observe.

## Gap classes and routing

- **Blocking** — an acceptance criterion's user-visible obligation is unmet, a workflow step is wrong, or a required accessibility behaviour is broken.
- **Material** — a divergence a person should decide on.
- **Minor** — a local inconsistency.

Each gap names the owning skill: `implement-frontend-change`, `implement-android-change`, or `implement-backend-change` for backend-driven content. UX review and approval remain human responsibilities and are reported as outstanding.

## Required capabilities

Read access to Jira, Confluence, and the checked-out UI or mobile repositories. Tool names are discovered, not hardcoded. A rendered check is used only where the environment genuinely provides one.

## Use and distribution

Invoke `/validate-ux-implementation` from the repository root using a supported coding agent, or let `/implement-jira-ticket` route to it. For a packaged installation, download `validate-ux-implementation.zip` from the latest release. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
