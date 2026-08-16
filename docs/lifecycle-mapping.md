# AMRIT SDLC lifecycle mapping

## The AMRIT 12-stage lifecycle

The official lifecycle is the authority for stage numbering. Skills are mapped onto it; they do not define it.

| Stage | Official name | Skill coverage |
| --- | --- | --- |
| Stage 01 | BRD | [`create-brd`](../skills/create-brd/README.md) |
| Stage 02 | Open | [`create-product-backlog`](../skills/create-product-backlog/README.md) |
| Stage 03 | Analysis | [`create-technical-design`](../skills/create-technical-design/README.md) and [`draft-test-cases`](../skills/draft-test-cases/README.md) |
| Stage 04 | Ready for Development | **No skill yet — documented gap.** No testing specialist required |
| Stage 05 | In Development | [`implement-jira-ticket`](../skills/implement-jira-ticket/README.md) with its seven conditionally selected specialists, then [`create-development-pr`](../skills/create-development-pr/README.md) |
| Stage 06 | Pending QA | **No dedicated skill, deliberately.** Existing QA test cases may be reviewed through `draft-test-cases` |
| Stage 07 | In QA | [`execute-qa-validation`](../skills/execute-qa-validation/README.md) |
| Stage 08 | QA Approved | **Human gate, deliberately no skill** |
| Stage 09 | Closed | No skill yet |
| Stage 10 | Release UAT | No skill yet |
| Stage 11 | Release Approved | No skill yet |
| Stage 12 | Production Release | [`create-brd`](../skills/create-brd/README.md) also serves the Stage 12 feedback loop back into Business & Product |

Some skills carry a longer descriptive stage label in their metadata — for example `Stage 03 — Engineering Analysis` for the official `Stage 03 — Analysis`. The stage **number** is authoritative; the descriptive suffix only names the work.

## Skill mapping

The skills are independently installable. They align to consecutive lifecycle stages, with two meta-skills — one engineering, one testing — their conditionally selected specialists, and one Pull Request skill; `answer-codebase-questions` is available across the lifecycle. A downstream skill may consume an approved upstream output without requiring the upstream skill itself to be installed.

| Stage | Primary role | Skill | Review status |
| --- | --- | --- | --- |
| Stage 01/12 — Business & Product | Business Systems Analyst | [`create-brd`](../skills/create-brd/README.md) | Draft — Pending Human Review |
| Stage 02 — Product Backlog Creation | Product Manager | [`create-product-backlog`](../skills/create-product-backlog/README.md) | Draft - Pending Product Manager Review |
| Stage 03 — Engineering Analysis | Technical Architect / Senior Developer | [`create-technical-design`](../skills/create-technical-design/README.md) | Ready for Architect Review |
| Stage 03 — Analysis | QA Tester / Test Analyst | [`draft-test-cases`](../skills/draft-test-cases/README.md) | QA test specification drafted — Pending QA review |
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
| Stage 07 — In QA | QA Tester / QA Automation Engineer | [`execute-qa-validation`](../skills/execute-qa-validation/README.md) | Execution evidence produced — QA approval outstanding |
| Cross-stage — Testing orchestration | Testing orchestrator | [`test-jira-ticket`](../skills/test-jira-ticket/README.md) | Testing activity performed for the ticket's lifecycle position |
| Cross-lifecycle — Codebase knowledge | Software Engineer | [`answer-codebase-questions`](../skills/answer-codebase-questions/README.md) | Evidence-backed codebase answer |

## The two meta-skills

```text
                  AMRIT Jira Ticket
                         |
          ┌──────────────┴──────────────┐
          |                             |
          v                             v
 implement-jira-ticket             test-jira-ticket
   Engineering META                  Testing META
          |                             |
   persona routing              lifecycle routing
          |                             |
 Backend / Frontend              draft-test-cases
 Android / DB / etc.             write-unit-tests
          |                      execute-qa-validation
          |
   write-unit-tests
          |
 create-development-pr
```

`implement-jira-ticket` answers *implement this ticket*. `test-jira-ticket` answers *perform the appropriate testing activity for this ticket's lifecycle position*. They do not compete.

`write-unit-tests` participates in both paths as one specialist, never duplicated:

```text
implement-jira-ticket → write-unit-tests     (primary, Stage 05, unchanged)
test-jira-ticket      → write-unit-tests     (when development-level testing is
                                              explicitly appropriate)
```

## Testing architecture

Three testing responsibilities, three artifacts, three stages. They are deliberately not interchangeable, and documentation must not call all three "test cases".

```text
                         test-jira-ticket
                            META-SKILL

                    Stage 03 → draft-test-cases
                    Stage 05 → write-unit-tests when applicable
                    Stage 07 → execute-qa-validation
```

| Skill | Stage | Persona | Question answered | Artifact |
| --- | --- | --- | --- | --- |
| [`draft-test-cases`](../skills/draft-test-cases/README.md) | Stage 03 — Analysis | QA Tester / Test Analyst | What must QA test to prove this requirement works? | Functional QA test **specifications** |
| [`write-unit-tests`](../skills/write-unit-tests/README.md) | Stage 05 — In Development | SDET / Developer testing | What code-level tests verify the changed code? | Executable **unit-test code** with real results |
| [`execute-qa-validation`](../skills/execute-qa-validation/README.md) | Stage 07 — In QA | QA Tester / QA Automation Engineer | Does the deployed build satisfy the agreed requirements and test cases? | QA **execution results and evidence** |

`test-jira-ticket` routes; it is not a pipeline that runs all three. It establishes the ticket's status, the artifacts that actually exist — requirements, approved design, QA test cases, implementation, unit tests, deployed build — and the user's intent, then selects only the activities the evidence supports and states every exclusion with its reason.

Each activity has an evidence gate that a stage alone never satisfies:

| Activity | Prerequisite | If absent |
| --- | --- | --- |
| `draft-test-cases` | Acceptance criteria or an approved requirement set | Stop and report; never invent a requirement |
| `write-unit-tests` | An implementation exists and its source is accessible | Do not route; never invent tests for code that does not exist |
| `execute-qa-validation` | A reachable deployed build | Blocked report with `Executed: 0`; never a PASS from documentation |

### Testing traceability

```text
Business Requirement
        ↓
FRD
        ↓
JIRA Story
        ↓
Acceptance Criterion
        ↓
QA Test Case                  draft-test-cases
        ↓
Implementation                implement-jira-ticket
        ↓
Unit Tests                    write-unit-tests
        ↓
QA Execution                  execute-qa-validation
        ↓
Evidence
        ↓
PASS / Defect
```

Identifiers — the FRD requirement number, `AMRIT-1234`, `AC-3`, `TC-07`, the build version — are preserved verbatim rather than matched by prose, so a defect raised at Stage 07 traces back to the business requirement without re-investigation. Existing test-case numbers are never reused or renumbered.

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

### QA test design at Stage 03

Stage 03 has two parallel responsibilities. Alongside the technical design, `draft-test-cases` answers the QA question: **what must QA test to prove that this requirement works?**

```text
Stage 03 — Analysis
    create-technical-design      Technical Architect
    draft-test-cases             QA Tester / Test Analyst
```

#### Inputs

- Jira Story or Task with acceptance criteria
- BRD and FRD
- Use cases, workflow diagrams, and business rules
- Role and permission requirements
- Approved technical design
- API contracts and data mappings
- Existing related test cases

#### Outputs

- Functional QA test specification covering the applicable categories — positive, negative, boundary, role-based, validation, API, integration, workflow, error handling, offline, sync, multilingual, device, and regression
- Each test case with Test ID, Requirement / AC, Scenario, Preconditions, Test data, Steps, Expected result, Test type, Priority, and Automation candidate
- A traceability matrix from acceptance criterion to test case
- Uncovered, ambiguous, and conflicting acceptance criteria, reported rather than resolved by invention

#### Exit criterion

QA and the Product Manager have reviewed the specification and agreed it as the QA scope for the ticket.

`draft-test-cases` finishes with **QA test specification drafted. Pending QA review.** or **QA test specification incomplete. Resolve the ambiguities above before QA review.**

The specification is **implementation-independent**. Every expected result comes from an approved requirement, never from what code happens to do. The implementation usually does not exist at Stage 03, which is exactly what makes the specification worth executing later. The skill writes no test code, executes nothing, and touches no environment.

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

**No skill covers Stage 04 today, and no testing specialist is required here.** This is a documented gap, not an omission from this mapping: the readiness checks above are performed by humans — Product Manager, Scrum Master, or Tech Lead — during backlog refinement and sprint planning.

A future `check-definition-of-ready` skill could verify linked artifacts and dependency readiness read-only, but none exists in this repository and none is implied by the Stage 05 skills. `implement-jira-ticket` assumes the ticket already reached Stage 05; it does not perform the Stage 04 readiness check and never claims a ticket is sprint-ready.

QA test cases are a Definition of Ready artifact. `test-jira-ticket` performs no activity at Stage 04, but when a ticket reaches it without agreed QA test cases, that absence is reported as a readiness gap and `draft-test-cases` is recommended.

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

The Pull Request is approved with code-review sign-off, CI is green, and the change is squash-merged to the appropriate release branch. The ticket then moves to [Stage 06 — Pending QA](#stage-06--pending-qa), which deliberately carries no dedicated skill, and on to [Stage 07 — In QA](#stage-07--in-qa), where `execute-qa-validation` performs QA execution.

`implement-jira-ticket` finishes with either **Implementation complete and locally verified. Ready for PR preparation.** or **Implementation incomplete. Resolve the items above before PR preparation.**

`create-development-pr` finishes with either **Development PR created. Awaiting code review.** or **Development PR not created. Resolve the items above before retrying.**

Together the Stage 05 skills contribute to the phase but do not satisfy the full phase exit criteria by themselves. The actual phase exit still requires:

- PR approval;
- code-review sign-off;
- green CI;
- squash merge to the appropriate release branch.

Those responsibilities belong to human review and the repository's merge workflow rather than to any skill. Every Stage 05 skill is independently installable, and none requires another at runtime. When a selected persona's specialist skill is not installed, `implement-jira-ticket` applies that persona's contract inline and reports that it did so; the persona is never skipped.

`implement-jira-ticket` is the Stage 05 orchestrator and the entry point. It reads the ticket, researches the knowledge sources, inspects the actual source code, classifies the impacted repositories and personas, invokes only the relevant specialists in dependency order, coordinates the contracts between them, verifies the result, and reports the evidence. Jira and Confluence remain read-only, and it never creates a branch, commit, push, or Pull Request, never transitions a Jira issue, and never claims that the exit criterion has been met. Any actual database schema change is implemented in `AMRIT-DB`, never in an application repository.

The specialists own their layers. `implement-backend-change`, `implement-frontend-change`, `implement-android-change`, and `implement-database-change` edit code, each inspecting the code it owns before changing it. `write-unit-tests` writes and runs code-level unit tests — developer testing, kept separate from `draft-test-cases` at Stage 03 and `execute-qa-validation` at Stage 07. `review-implementation-architecture` and `validate-ux-implementation` are read-only assessments that report deviations and gaps for human decision. No specialist performs Git or Pull Request work, and none claims architecture, DBA, UX, code-review, QA, CI, or release approval; absent approvals are reported as absent.

`write-unit-tests` is also reachable through the testing meta-skill. `test-jira-ticket` routes to the same specialist when a ticket is in development and development-level testing is explicitly appropriate. The Stage 05 relationship above is unchanged, and no unit-testing logic is duplicated:

```text
implement-jira-ticket → write-unit-tests     (primary, Stage 05)
test-jira-ticket      → write-unit-tests     (development-level testing)
```

`create-development-pr` performs the Git and GitHub write operations — branch, commit, push, and Pull Request creation against a validated `release-X.Y.Z` branch — but performs no substantive implementation. Jira remains strictly read-only. It never approves, merges, or squash-merges a Pull Request, never claims code-review sign-off or green CI it did not observe, and stops and returns the work to implementation when the change is materially incomplete or a required `AMRIT-DB` change is missing.

## Stage 06 — Pending QA

The queue state between a merged implementation and active QA. The change is merged and awaiting deployment to the QA environment and QA capacity.

```text
Stage 05 — In Development
        ↓
Stage 06 — Pending QA
        ↓
Stage 07 — In QA
```

### Inputs

- Merged implementation on the release branch
- Agreed QA test cases from Stage 03
- Deployment to the QA environment

### Outputs

- A ticket ready for QA execution, with agreed test cases in place

### Exit criterion

The change is deployed to the QA environment and QA begins execution.

### Skill coverage

**No dedicated skill covers Stage 06, deliberately.** Stage 06 is primarily a lifecycle and queue state; it does not justify an agent skill merely because the lifecycle has a stage. There is no `prepare-qa-handoff` skill and none is wanted.

Existing QA test cases may legitimately be reviewed or refined here through `draft-test-cases`, whose canonical creation point remains Stage 03. When it is re-run for a review, it states which test cases were added, changed, or retired, and never renumbers an existing one.

## Stage 07 — In QA

`execute-qa-validation` is the QA execution skill. It answers: **does the deployed implementation satisfy the previously agreed requirements and test cases?**

```text
Stage 06 — Pending QA
        ↓
Stage 07 — In QA

test-jira-ticket
        |
        v
execute-qa-validation
        |
        ├── PASS with evidence
        └── FAIL → defect → back to the implementation flow
        ↓
Stage 08 — QA Approved      (human gate)
```

### Inputs

- Jira ticket and its acceptance criteria
- The QA test cases agreed at Stage 03
- A deployed, reachable QA or test build
- Existing automated suites and the regression suite
- API specifications and relevant application configuration
- Test data and whatever test infrastructure the environment genuinely provides

### Outputs

- Per test case: expected result, actual result, verdict, and evidence
- An explicit split between automated, manual-required, and infrastructure-blocked cases
- Acceptance-criterion status rolled up from the test-case verdicts
- Defect reports for failures, drafted by default
- A named build under test, so every result is anchored to a deployed state

### Exit criterion

The human QA tester reviews the evidence and decides whether the ticket is QA approved.

### Execution is mandatory

Documentation cannot produce a PASS. Neither can source code, a technical design, a PR description, a green unit suite, or reasoning about what the code should do. When the build or environment is unavailable, the run stops:

```text
QA EXECUTION BLOCKED

Reason:
QA build/environment unavailable.

Test cases prepared:
42

Executed:
0

QA status:
NOT EXECUTED
```

A blocked run is a legitimate outcome. A fabricated one is not.

### The agreed test cases are not rewritten

`execute-qa-validation` consumes the Stage 03 specification as written. It does not regenerate it from the implementation, and it never edits an expected result so the build passes. If the specification expects a duplicate-validation rejection and the build returns HTTP 500, the verdict is `FAIL`.

Where the agreed expected result genuinely appears wrong, the case is recorded `BLOCKED — requirement question` and escalated to the QA Lead and Product Manager rather than edited.

### Manual and device tests cannot be assumed

Automated and manual coverage is always reported separately, and pending cases are named individually. A ticket is never reported QA-approved, QA-complete, or Stage 08 ready while manual-required or infrastructure-blocked scenarios remain unverified. A high automated pass rate does not close that gap.

### Failures produce defects, not fixes

`execute-qa-validation` never modifies production code, configuration, or a migration to make a test pass. A QA failure returns the work to the implementation flow through the defect and rework path. Jira is read-only by default: defects are drafted, and are created only when the user explicitly authorizes that specific defect. No defect key is ever fabricated.

Failures are structured — preserved `TC` and `AC` identifiers, separated expected and actual behaviour, deterministic reproduction steps, build identity, evidence references, and reproducibility — so they would serve as clean inputs to a future `root-cause-analysis` skill. That skill does not exist in this repository and is not implied by these skills.

`execute-qa-validation` finishes with exactly one of **QA VALIDATION COMPLETE — all agreed test cases executed and passed. QA approval remains a human decision.**, **QA VALIDATION INCOMPLETE — <n> failed, <n> pending human or device execution.**, or **QA EXECUTION BLOCKED — <reason>. QA status: NOT EXECUTED.**

## Stage 08 — QA Approved

The QA sign-off state. QA has reviewed the execution evidence and accepted the change.

### Inputs

- QA execution evidence from Stage 07
- Defect status for every failure raised

### Outputs

- A QA-approved ticket

### Exit criterion

The QA tester approves the ticket.

### Skill coverage

**No skill covers Stage 08, deliberately.** QA approval is a human accountability gate. There is no `check-qa-approval-readiness` skill and none is wanted.

`execute-qa-validation` provides the evidence the human QA tester needs to make that decision — including everything that did not run — and never claims to be that approver, never records QA sign-off, and never transitions a ticket to QA Approved.

## Stage 09 — Closed

**No skill covers Stage 09, deliberately.** Ticket closure is a lifecycle and project-management action and does not justify a separate agent skill in the current architecture. There is no `prepare-ticket-closure` skill and none is wanted.

## Cross-stage — Testing orchestration

`test-jira-ticket` is the testing entry point across Stage 03, Stage 05, and Stage 07.

```text
                         test-jira-ticket
                            META-SKILL
                                |
              lifecycle-aware test orchestration
                                |
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
     draft-test-cases     write-unit-tests    execute-qa-validation
       QA test design       code-level         QA execution
                            unit testing
            │                   │                   │
      Stage 03              Stage 05             Stage 07
       Analysis          In Development           In QA
```

### Inputs

- A Jira ticket at any testable lifecycle position
- The artifact inventory: acceptance criteria, requirement set, approved design, existing QA test cases, implementation, source access, existing unit tests, deployed build
- The user's explicit intent, where they stated one

### Outputs

- The testing deliverable appropriate to that lifecycle position, produced by the specialist
- A routing report: lifecycle assessment, artifact inventory, activity selected with its evidence, activities excluded with their reasons, and the invocation mechanism used
- Traceability from acceptance criteria to the produced artifact, and the gaps that remain

### Routing

```text
Stage 03 → draft-test-cases
Stage 05 → write-unit-tests when applicable
Stage 07 → execute-qa-validation
```

It is **not a pipeline**. Running all three by default would design QA test cases from an implementation, invent unit tests for code that does not exist, and fabricate QA results with no build. Activities are selected from evidence, and every exclusion is stated with its reason.

Stage 04, 06, 08, and 09 carry no testing activity. An activity is never invented because the lifecycle has a stage.

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
