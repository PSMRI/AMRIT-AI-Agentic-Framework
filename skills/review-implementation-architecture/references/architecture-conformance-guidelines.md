# Architecture Conformance Guidelines

## Contents

- [Stage 04 posture](#stage-04-posture)
- [When this review is warranted](#when-this-review-is-warranted)
- [Evidence discipline](#evidence-discipline)
- [What to assess](#what-to-assess)
- [Deviation classification](#deviation-classification)
- [Design-versus-code conflicts](#design-versus-code-conflicts)
- [What not to raise](#what-not-to-raise)
- [Handing constraints to specialists](#handing-constraints-to-specialists)
- [Review checklist](#review-checklist)

## Stage 04 posture

Stage 03 designs. Stage 04 implements. This review exists to keep the implementation faithful to the approved design, not to improve the design during implementation.

Three rules follow:

1. An approved design is a constraint, not a starting suggestion.
2. A disagreement with the approved design is raised for Architect decision, never resolved unilaterally in code.
3. Absence of an approved design is stated, never substituted with an invented one.

## When this review is warranted

Warranted when the change:

- spans repositories or crosses a module or service boundary;
- introduces a new component, service, table, queue, or cross-cutting pattern;
- changes an API contract that other repositories consume;
- changes ownership of data or behaviour;
- changes an integration boundary or external dependency;
- affects authentication, authorization, sensitive health data, audit trails, or encryption;
- has material performance or scalability implications;
- appears to deviate from the approved design.

Not warranted for a single-layer, in-pattern change that touches no contract, no boundary, and no security or performance constraint. Running this review on ordinary work adds ceremony without value.

## Evidence discipline

Label every material statement:

- **Confirmed in code** — the file, symbol, contract, or object was read.
- **Documented intent** — the approved design or an approved document states it.
- **Inferred** — strongly indicated by structure or convention, not directly confirmed.
- **Cannot assess** — evidence is unavailable; say what is missing.

Never present inferred structure as confirmed. Never cite a file, class, endpoint, or table that was not retrieved. Treat source evidence as authoritative for current behaviour and approved documents as authoritative for intended architecture.

## What to assess

### Approved design alignment

Does the implementation do what the approved HLD and LLD say, in the components they name, with the responsibilities they assign?

### Module boundaries and ownership

Does each piece of behaviour live where the architecture says it belongs? Watch for logic leaking into controllers, UI, or utilities; for a module reaching into another module's internals; and for data ownership drifting between services.

### Architecture patterns

Does the change follow the patterns already established in those modules — layering, dependency direction, error model, transaction handling, configuration, and dependency injection — rather than introducing a parallel structure?

### API contracts and compatibility

Is the contract the design specified the one that was built? Is the change additive, and if not, are the affected consumers identified? Are error semantics, status codes, and field types consistent with the module's conventions?

### Integration boundaries

Are cross-repository and external dependencies the ones the design intended? Has any new coupling appeared? Is failure of a dependency handled at the boundary the architecture defines?

### Database ownership

Does schema live in `AMRIT-DB`, with the application holding only application-side persistence code? Does the application depend on any object that no migration creates?

### Security constraints

Are authentication and authorization checks intact on every changed path? Is sensitive personal and clinical data handled, logged, and stored as the architecture requires? Are audit obligations preserved? Are trust boundaries validated?

### Performance constraints

Do the changed paths avoid N+1 access, repeated remote calls in loops, unbounded result sets, and missing pagination? Are caching and indexing decisions consistent with the design's stated expectations?

## Deviation classification

| Class | Meaning | Action |
| --- | --- | --- |
| **Blocking** | The approved design cannot be implemented safely as written, ownership has moved, a contract breaks consumers, or a security or data-integrity constraint is violated | Stop implementation; return the design for Architect review |
| **Material** | The implementation works but diverges from the approved design or an established pattern in a way an Architect must decide on | Report for decision; implementation may continue only where independent and safe |
| **Minor** | A local inconsistency correctable inside the existing pattern | Hand to the implementing specialist |

Every deviation states the consequence, not only the difference. "This differs from the design" is an observation; "this moves ownership of beneficiary data into a service that does not own it, so two writers can diverge" is a finding.

## Design-versus-code conflicts

When the approved design and the actual code disagree materially:

1. Preserve both claims with their sources.
2. Identify which represents current implementation and which represents intended direction.
3. State the architectural consequence of following each.
4. Do not silently overwrite intended architecture with an accidental implementation pattern, and do not misdescribe current behaviour because a document says it should differ.
5. Use the `IMPLEMENTATION BLOCKED` output when the design cannot be implemented safely as written.

## What not to raise

- Naming, formatting, and style preferences already settled by the repository.
- Refactors that would improve the codebase but are outside the ticket.
- Alternative designs that do not address a real risk in the approved one.
- Anything the implementing specialist's own guidelines already cover at code level.

Architecture review that raises ordinary preferences trains people to ignore it.

## Handing constraints to specialists

Constraints passed to the implementing specialists must be concrete and traceable:

- the component or module that must own the behaviour;
- the contract shape that must be produced or consumed;
- the boundary that must not be crossed;
- the security or performance obligation that must hold;
- the evidence — design section or source path — behind each.

## Review checklist

- the approved design was read, or its absence stated;
- the actual source was inspected before any assessment;
- every finding is architecture-material and evidenced;
- deviations are classified with consequences and required actions;
- design-versus-code conflicts preserve both sources;
- nothing was edited, and no approval was claimed;
- constraints handed downstream are concrete and traceable.
