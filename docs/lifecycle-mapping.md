# AMRIT SDLC lifecycle mapping

## The AMRIT 12-stage lifecycle

The official lifecycle is the authority for stage numbering. Skills are mapped onto it; they do not define it.

| Stage | Official name | Skill coverage |
| --- | --- | --- |
| Stage 01 | BRD | [`create-brd`](../skills/create-brd/README.md) |
| Stage 02 | Open | [`create-product-backlog`](../skills/create-product-backlog/README.md) |
| Stage 03 | Analysis | [`create-technical-design`](../skills/create-technical-design/README.md) |
| Stage 04 | Ready for Development | **No skill yet — documented gap** |
| Stage 05 | In Development | [`implement-jira-ticket`](../skills/implement-jira-ticket/README.md) with its seven conditionally selected specialists, then [`create-development-pr`](../skills/create-development-pr/README.md) |
| Stage 06 | Pending QA | No skill yet |
| Stage 07 | In QA | No skill yet |
| Stage 08 | QA Approved | No skill yet |
| Stage 09 | Closed | No skill yet |
| Stage 10 | Release UAT | No skill yet |
| Stage 11 | Release Approved | No skill yet |
| Stage 12 | Production Release | [`create-brd`](../skills/create-brd/README.md) also serves the Stage 12 feedback loop back into Business & Product |

Some skills carry a longer descriptive stage label in their metadata — for example `Stage 03 — Engineering Analysis` for the official `Stage 03 — Analysis`. The stage **number** is authoritative; the descriptive suffix only names the work.

## Skill mapping

The skills are independently installable. They align to consecutive lifecycle stages, with one orchestrator, seven conditionally selected specialists, and one Pull Request skill covering Stage 05; `answer-codebase-questions` is available across the lifecycle. A downstream skill may consume an approved upstream output without requiring the upstream skill itself to be installed.

| Stage | Primary role | Skill | Review status |
| --- | --- | --- | --- |
| Stage 01/12 — Business & Product | Business Systems Analyst | [`create-brd`](../skills/create-brd/README.md) | Draft — Pending Human Review |
| Stage 02 — Product Backlog Creation | Product Manager | [`create-product-backlog`](../skills/create-product-backlog/README.md) | Draft - Pending Product Manager Review |
| Stage 03 — Engineering Analysis | Technical Architect / Senior Developer | [`create-technical-design`](../skills/create-technical-design/README.md) | Ready for Architect Review |
| Stage 04 — Ready for Development | Product Manager / Scrum Master / Tech Lead | *No skill yet — see [Stage 04](#stage-04--ready-for-development)* | Definition of Ready verified by humans |
| Stage 05 — In Development | Developer / Senior Developer (orchestration) | [`implement-jira-ticket`](../skills/implement-jira-ticket/README.md) | Ready for PR preparation |
| Stage 05 — In Development | Technical Architect | [`review-implementation-architecture`](../skills/review-implementation-architecture/README.md) | Conformance assessed — Architect review outstanding |
| Stage 05 — In Development | DBA / Database Engineer | [`implement-database-change`](../skills/implement-database-change/README.md) | Migration implemented — DBA review outstanding |
| Stage 05 — In Development | Backend Developer | [`implement-backend-change`](../skills/implement-backend-change/README.md) | Backend implemented |
| Stage 05 — In Development | Frontend Developer | [`implement-frontend-change`](../skills/implement-frontend-change/README.md) | Frontend implemented |
| Stage 05 — In Development | Android / Kotlin Developer | [`implement-android-change`](../skills/implement-android-change/README.md) | Android implemented |
| Stage 05 — In Development | UX / UI Specialist | [`validate-ux-implementation`](../skills/validate-ux-implementation/README.md) | UX conformance assessed — UX review outstanding |
| Stage 05 — In Development | SDET / Developer testing | [`write-unit-tests`](../skills/write-unit-tests/README.md) | Unit tests executed |
| Stage 05 — In Development | Developer / Senior Developer | [`create-development-pr`](../skills/create-development-pr/README.md) | Awaiting code review |
| Cross-lifecycle — Codebase knowledge | Software Engineer | [`answer-codebase-questions`](../skills/answer-codebase-questions/README.md) | Evidence-backed codebase answer |

## Stage 01/12 — BRD

### Inputs

- Business need or feature request
- Field or stakeholder feedback
- Government programme guidelines
- Workflows, screenshots, meeting notes, and existing documents
- Relevant Confluence context

### Outputs

- Traceable draft BRD
- Business workflows and functional requirements
- Acceptance criteria and source references
- Data-mapping requirements where applicable
- Assumptions, conflicts, missing information, and open questions

### Exit criterion

Business Systems Analyst, Product Manager, and relevant stakeholder review, followed by Product Manager sign-off.

`create-brd` prepares **Draft — Pending Human Review**. Mandatory Confluence research is read-only by default, publishing requires an explicit request after the draft is shown, and the skill never claims that the exit criterion has been met.

## Stage 02 — Product Backlog Creation

### Inputs

- Signed-off BRD or FRD
- Approved Confluence requirement page or uploaded approved document
- L2-escalated bug or existing Jira production defect

### Outputs

- Proposed Epics, Stories, Tasks, or Subtasks
- Testable acceptance criteria and INVEST review
- Module and category mapping
- Priority recommendation, dependencies, risks, and source traceability
- Jira creation summary only after authorized publication

### Exit criterion

The Product Manager has reviewed, finalized, and triaged the backlog with contextual priority so that tickets are ready for Engineering Analysis.

`create-product-backlog` prepares **Draft - Pending Product Manager Review**. Jira remains read-only during drafting and refinement. Publication requires approval or finalization of the specific backlog and a separate explicit Jira creation request.

## Stage 03 — Engineering Analysis

### Inputs

- One or more approved Jira Stories with acceptance criteria
- Approved BRD and FRD
- Workflow and architecture diagrams
- Current Confluence architecture
- Applicable Swagger/OpenAPI specifications
- Optional repository, configuration, deployment, and operational evidence

### Outputs

- One review-ready technical design package
- Requirements traceability and cross-layer impact analysis
- High-level and low-level design with justified decisions
- API compatibility and database schema-change determination
- Security, performance, observability, deployment, and testability notes
- Implementation risks and architecture-material open questions
- Mermaid diagrams when useful and DBML only when a schema change exists
- Repository-grounded Existing Architecture Summary when official DeepWiki MCP or supplied repository evidence is available

### Exit criterion

The Technical Architect has reviewed the design, resolved or accepted material risks and open questions, and authorized implementation to begin.

`create-technical-design` finishes with **Ready for Architect Review** and **No implementation should begin until the design is reviewed.** It is read-only, produces no implementation code, never modifies or publishes to Jira or Confluence, and never claims that the exit criterion has been met.

## Stage 04 — Ready for Development

The readiness holding state between Analysis and In Development. A ticket has completed analysis, design, and test-case preparation, and is waiting to be pulled into a sprint.

```text
Stage 03 — Analysis
        ↓
Stage 04 — Ready for Development
        ↓
Stage 05 — In Development
```

### Typical responsibilities

- verify Definition of Ready artifacts
- ensure FRD, HLD, LLD, and QA test cases are linked
- confirm dependencies
- estimate story points
- prioritize within the release
- assign or pull into a sprint

### Inputs

- Design-complete ticket
- Test cases
- Release plan
- Sprint capacity

### Outputs

- Sprint-ready ticket

### Exit criterion

The ticket is pulled into a sprint with an assignee set.

### Skill coverage

**No skill covers Stage 04 today.** This is a documented gap, not an omission from this mapping: the readiness checks above are performed by humans — Product Manager, Scrum Master, or Tech Lead — during backlog refinement and sprint planning.

A future `check-definition-of-ready` skill could verify linked artifacts and dependency readiness read-only, but none exists in this repository and none is implied by the Stage 05 skills. `implement-jira-ticket` assumes the ticket already reached Stage 05; it does not perform the Stage 04 readiness check and never claims a ticket is sprint-ready.

## Stage 05 — In Development

`implement-jira-ticket` is the single entry point. It orchestrates the engineering personas the ticket actually requires and hands off to `create-development-pr`:

```text
Stage 03 — Analysis
        ↓
Stage 04 — Ready for Development
        ↓
Stage 05 — In Development

implement-jira-ticket
        |
        |-- review-implementation-architecture   (architecturally significant change)
        |-- implement-database-change            (schema, migrations, indexes)
        |-- implement-backend-change             (services, APIs, domain logic)
        |-- implement-frontend-change            (web UI, state, forms)
        |-- implement-android-change             (Kotlin, mobile flows, offline)
        |-- validate-ux-implementation           (user-visible change vs approved UX)
        `-- write-unit-tests                     (code-level tests for what changed)
                 |
                 v
        create-development-pr
                 |
                 v
        Senior Developer review
                 |
                 v
        CI green + approval + squash merge
        ↓
Stage 06 — Pending QA
```

The specialists are **conditionally selected, not an unconditional sequence**. The route comes from the Jira ticket, the approved Stage 03 technical design where one exists, and mandatory inspection of the actual source code.

### Persona routing

| Persona | Skill | Selected when |
| --- | --- | --- |
| Technical Architect | `review-implementation-architecture` | cross-cutting or cross-repository change, new component or contract, changed ownership or integration boundary, security- or performance-material change, suspected design deviation |
| DBA / Database Engineer | `implement-database-change` | a schema object, migration, index, constraint, or data-compatibility concern exists |
| Backend Developer | `implement-backend-change` | services, APIs, controllers, domain logic, integrations, validation, persistence integration, error handling, or backend configuration change |
| Frontend Developer | `implement-frontend-change` | web UI, components, state, API integration, forms, client validation, accessibility, or frontend error handling change |
| Android / Kotlin Developer | `implement-android-change` | the Android applications change, including offline behaviour and platform constraints |
| UX / UI Specialist | `validate-ux-implementation` | a user-visible change exists and approved UX or design-system rules apply |
| SDET / developer testing | `write-unit-tests` | production behaviour changed — effectively always |

Representative routes:

```text
Backend-only        implement-backend-change → write-unit-tests → verification
Backend + database  implement-database-change → implement-backend-change → write-unit-tests
Full stack          implement-backend-change → implement-frontend-change
                    → validate-ux-implementation → write-unit-tests
Android             implement-android-change → write-unit-tests
Cross-cutting       review-implementation-architecture → implement-database-change
architectural       → implement-backend-change → implement-frontend-change
change              → validate-ux-implementation → write-unit-tests
```

Execution follows the dependency chain: architecture review before implementation, schema before the backend that consumes it, the API contract before the frontend or Android that consumes it, UX validation after the user-visible change exists, unit tests over everything that changed.

### Mandatory source-code inspection

Every Stage 05 skill inspects the actual checked-out code before changing or assessing it. Jira, Confluence, DeepWiki, Graphify, the approved design, and previous knowledge establish intent; the repository establishes what the system currently does and where the change belongs. A ticket is never implemented from documentation alone, and an inaccessible repository stops the work with a blocked report rather than producing a documentation-driven change.

Where the approved Stage 03 design cannot be implemented safely as written, the work stops and the discrepancy is surfaced for design review instead of a silent deviation.

### Inputs

- Sprint-ready Jira ticket with acceptance criteria, pulled into a sprint at Stage 04
- Approved Stage 03 technical design where available
- Functional specification or BRD where available
- Wireframes and approved UX where applicable
- The relevant application repositories, actually checked out
- `AMRIT-DB` when schema changes are required

### Outputs

- Persona classification and orchestration report — `implement-jira-ticket`
- Architecture conformance assessment — `review-implementation-architecture`
- `AMRIT-DB` migration and schema contract — `implement-database-change`
- Backend, frontend, and Android code changes — the implementation specialists
- UX conformance assessment — `validate-ux-implementation`
- Code-level unit tests with executed results — `write-unit-tests`
- Local verification results — `implement-jira-ticket` and `create-development-pr`
- Pull Request targeting the appropriate `release-X.Y.Z` branch — `create-development-pr`
- Architecture, DBA, UX, and code review sign-off — human review, never claimed by any skill

### Exit criterion

The Pull Request is approved with code-review sign-off, CI is green, and the change is squash-merged to the appropriate release branch. The ticket then moves to Stage 06 — Pending QA, which no skill in this repository covers.

`implement-jira-ticket` finishes with either **Implementation complete and locally verified. Ready for PR preparation.** or **Implementation incomplete. Resolve the items above before PR preparation.**

`create-development-pr` finishes with either **Development PR created. Awaiting code review.** or **Development PR not created. Resolve the items above before retrying.**

Together the Stage 05 skills contribute to the phase but do not satisfy the full phase exit criteria by themselves. The actual phase exit still requires:

- PR approval;
- code-review sign-off;
- green CI;
- squash merge to the appropriate release branch.

Those responsibilities belong to human review and the repository's merge workflow rather than to any skill. Every Stage 05 skill is independently installable, and none requires another at runtime. When a selected persona's specialist skill is not installed, `implement-jira-ticket` applies that persona's contract inline and reports that it did so; the persona is never skipped.

`implement-jira-ticket` is the Stage 05 orchestrator and the entry point. It reads the ticket, researches the knowledge sources, inspects the actual source code, classifies the impacted repositories and personas, invokes only the relevant specialists in dependency order, coordinates the contracts between them, verifies the result, and reports the evidence. Jira and Confluence remain read-only, and it never creates a branch, commit, push, or Pull Request, never transitions a Jira issue, and never claims that the exit criterion has been met. Any actual database schema change is implemented in `AMRIT-DB`, never in an application repository.

The specialists own their layers. `implement-backend-change`, `implement-frontend-change`, `implement-android-change`, and `implement-database-change` edit code, each inspecting the code it owns before changing it. `write-unit-tests` writes and runs code-level unit tests — developer testing, kept separate from `draft-test-cases` and Stage 07 QA execution. `review-implementation-architecture` and `validate-ux-implementation` are read-only assessments that report deviations and gaps for human decision. No specialist performs Git or Pull Request work, and none claims architecture, DBA, UX, code-review, QA, CI, or release approval; absent approvals are reported as absent.

`create-development-pr` performs the Git and GitHub write operations — branch, commit, push, and Pull Request creation against a validated `release-X.Y.Z` branch — but performs no substantive implementation. Jira remains strictly read-only. It never approves, merges, or squash-merges a Pull Request, never claims code-review sign-off or green CI it did not observe, and stops and returns the work to implementation when the change is materially incomplete or a required `AMRIT-DB` change is missing.

## Cross-lifecycle — Codebase knowledge

### Inputs

- Questions about AMRIT repositories, services, APIs, modules, data flows, integrations, implementation behaviour, or architecture rationale

### Outputs

- Direct, evidence-backed codebase answer
- Concrete implementation and documentation references when available
- Confidence, conflicts, and unresolved evidence gaps when relevant

### Research order

`answer-codebase-questions` researches DeepWiki first, Confluence when
implementation evidence does not fully answer the question or design context is
needed, and Graphify only as the final fallback for unresolved relationships.
It is read-only and never uses Jira.

See the [installation guide](installation.md) for Claude Code and Claude Desktop setup.
