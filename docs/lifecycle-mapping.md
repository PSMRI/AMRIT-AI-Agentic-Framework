# AMRIT SDLC lifecycle mapping

The skills are independently installable. The first five align to consecutive lifecycle stages, with two skills covering Stage 04; `answer-codebase-questions` is available across the lifecycle. A downstream skill may consume an approved upstream output without requiring the upstream skill itself to be installed.

| Stage | Primary role | Skill | Review status |
| --- | --- | --- | --- |
| Stage 01/12 — Business & Product | Business Systems Analyst | [`create-brd`](../skills/create-brd/README.md) | Draft — Pending Human Review |
| Stage 02 — Product Backlog Creation | Product Manager | [`create-product-backlog`](../skills/create-product-backlog/README.md) | Draft - Pending Product Manager Review |
| Stage 03 — Engineering Analysis | Technical Architect / Senior Developer | [`create-technical-design`](../skills/create-technical-design/README.md) | Ready for Architect Review |
| Stage 04 — In Development | Developer / Senior Developer | [`implement-jira-ticket`](../skills/implement-jira-ticket/README.md) | Ready for PR preparation |
| Stage 04 — In Development | Developer / Senior Developer | [`create-development-pr`](../skills/create-development-pr/README.md) | Awaiting code review |
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

## Stage 04 — In Development

Two skills cover this stage in sequence:

```text
Stage 04 — In Development

implement-jira-ticket
    ↓
create-development-pr
    ↓
Senior Developer review
    ↓
CI green + approval + squash merge
```

### Inputs

- Sprint-ready Jira ticket with acceptance criteria
- Functional specification or BRD where available
- Wireframes where applicable
- Approved technical-design or architecture context where available
- The relevant application repository
- `AMRIT-DB` when schema changes are required

### Outputs

- Code and unit tests — `implement-jira-ticket`
- Required `AMRIT-DB` schema changes — `implement-jira-ticket`
- Local verification results — both skills
- Pull Request targeting the appropriate `release-X.Y.Z` branch — `create-development-pr`
- Code review sign-off — Senior Developer / human review

### Exit criterion

The Pull Request is approved with code-review sign-off, CI is green, and the change is squash-merged to the appropriate release branch.

`implement-jira-ticket` finishes with either **Implementation complete and locally verified. Ready for PR preparation.** or **Implementation incomplete. Resolve the items above before PR preparation.**

`create-development-pr` finishes with either **Development PR created. Awaiting code review.** or **Development PR not created. Resolve the items above before retrying.**

Together the two skills contribute to the phase but do not satisfy the full phase exit criteria by themselves. The actual phase exit still requires:

- PR approval;
- code-review sign-off;
- green CI;
- squash merge to the appropriate release branch.

Those responsibilities belong to human review and the repository's merge workflow rather than to either skill. Both skills are independently installable, and neither requires the other at runtime.

`implement-jira-ticket` is the implementation and source-editing skill. Jira and Confluence remain read-only, and it never creates a branch, commit, push, or Pull Request, never transitions a Jira issue, and never claims that the exit criterion has been met. Any actual database schema change is implemented in `AMRIT-DB`, never in an application repository.

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
