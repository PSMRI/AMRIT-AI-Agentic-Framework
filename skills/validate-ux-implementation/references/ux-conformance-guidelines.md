# UX Conformance Guidelines

## Contents

- [Stage 04 posture](#stage-04-posture)
- [When this validation is warranted](#when-this-validation-is-warranted)
- [Establishing the approved UX](#establishing-the-approved-ux)
- [Assessment basis and honesty](#assessment-basis-and-honesty)
- [What to assess](#what-to-assess)
- [Accessibility baseline](#accessibility-baseline)
- [Gap classification](#gap-classification)
- [What not to raise](#what-not-to-raise)
- [Routing corrections](#routing-corrections)
- [Review checklist](#review-checklist)

## Stage 04 posture

Where approved UX exists, the implementation conforms to it. This validation checks conformance and reports gaps. It does not restyle, does not implement, and does not replace an approved design with a preferred one.

AMRIT screens are used by frontline health workers, often on constrained devices and in low-connectivity conditions. Consistency with the existing product and with the approved workflow matters more than novelty.

## When this validation is warranted

Warranted when a user-visible change exists and any of these apply:

- approved wireframes, mockups, or workflow documentation exist for the change;
- the change adds or modifies a screen, form, field, or navigation step;
- the change affects validation messaging, confirmation, or destructive actions;
- the change affects loading, empty, or error states;
- the change touches accessibility behaviour.

Not warranted for a change with no user-visible effect.

## Establishing the approved UX

Gather, in this order:

1. wireframes and mockups attached to the Jira issue;
2. approved UX and workflow pages in Confluence;
3. the user-visible obligations stated in the acceptance criteria;
4. the repository's design system and equivalent existing screens.

When no approved UX exists, say so plainly and validate against the acceptance criteria and existing conventions. Never invent an approved design, and never treat its absence as licence to redesign.

## Assessment basis and honesty

State how the assessment was made:

- **Source inspection** — the implementation was read in the code.
- **Rendered check** — the UI was actually rendered and observed in this environment.

Do not describe a visual result that was not observed. A source-based assessment is legitimate and useful; claiming to have seen a rendered screen that was never rendered is not.

## What to assess

### Wireframe and field coverage

Every screen, section, field, label, help text, action, and state the approved design specifies is present, and nothing user-visible was invented beyond it. Field order, grouping, and labelling match the approved design and the module's existing vocabulary.

### Workflow consistency

Step order, entry and exit points, navigation, and back and cancel behaviour follow the approved workflow. The flow behaves sensibly when a step fails, when data is missing, and when the user leaves and returns.

### Design-system adherence

Shared components are reused rather than reimplemented. Spacing, typography, iconography, button hierarchy, and interaction patterns follow what the application already establishes. New one-off primitives are a finding, not a shortcut.

### Interaction and messaging consistency

Validation messages appear where and how the application already shows them, in consistent tone and wording. Confirmations, destructive-action guards, and success feedback follow existing conventions. Error text is actionable and never exposes internal detail or sensitive data.

### Loading, empty, and error states

Every asynchronous view has a defined loading state, an empty state, and an error state consistent with equivalent screens. A screen that silently shows nothing on failure is a gap.

### Consistency with equivalent screens

The change looks and behaves like the rest of the application. Divergence is a finding unless the approved design deliberately requires it.

## Accessibility baseline

Assess, at minimum:

- semantic structure and heading order;
- form labels programmatically associated with their controls;
- accessible names for interactive elements, including icon-only controls;
- keyboard operability and a sensible focus order;
- visible focus indication and focus management on dialogs, navigation, and validation errors;
- error messages announced and associated with the field;
- contrast and text-scaling expectations set by the design system;
- touch-target size on mobile screens;
- preservation of existing ARIA usage and accessible behaviour.

An accessibility behaviour removed as a side effect of a change is a blocking gap, not a preference.

## Gap classification

| Class | Meaning | Action |
| --- | --- | --- |
| **Blocking** | An acceptance criterion's user-visible obligation is unmet, a workflow step is missing or wrong, or a required accessibility behaviour is broken | Return to the implementing skill before PR preparation |
| **Material** | The implementation works but diverges from approved UX or the design system in a way a person should decide on | Report for decision |
| **Minor** | A small inconsistency correctable inside the existing pattern | Hand to the implementing specialist |

Every gap states the user impact, not only the difference. "Spacing differs from the mockup" is an observation; "the validation message is not associated with the field, so screen-reader users receive no error" is a finding.

## What not to raise

- Personal aesthetic preference where the design system has already decided.
- Redesign proposals for approved UX.
- Product-scope suggestions beyond the ticket.
- Code-level style issues the frontend or Android guidelines already cover.

## Routing corrections

Each gap names the skill that owns the fix:

- web UI corrections → `implement-frontend-change`;
- Android corrections → `implement-android-change`;
- backend-driven content, field, or error-message corrections → `implement-backend-change`;
- unclear or missing approved UX → back to the requirement owner, not resolved by inventing design.

This skill never applies the correction itself.

## Review checklist

- the approved UX was read, or its absence stated;
- the implemented UI source was inspected and the assessment basis stated honestly;
- coverage, workflow, design-system, interaction, state, and accessibility aspects were all assessed;
- every gap names user impact and the owning skill;
- no source, style, or asset was modified;
- approved UX was not redesigned and no settled preference was raised;
- no UX, design, QA, or review approval was claimed.
