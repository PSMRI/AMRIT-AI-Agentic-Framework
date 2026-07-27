# AMRIT SDLC lifecycle mapping

## Stage 01/12 - BRD

- **Lifecycle area:** Business & Product
- **Role:** Business Systems Analyst
- **Primary skill:** `create-brd`

### Inputs

- Business need
- Feature request
- Field feedback
- Government guidelines
- Existing documents
- Confluence context

### Outputs

- Draft BRD
- Workflow information
- Functional requirement inputs
- Data mapping requirements where applicable

### Exit criterion

Human review and Product Manager sign-off.

`create-brd` prepares **Draft - Pending Human Review** and never claims that the exit criterion has been completed.

## Stage 02 - Product Backlog Creation

- **Lifecycle area:** Product Management
- **Role:** Product Manager
- **Primary skill:** `create-product-backlog`

### Inputs

- Signed-off BRD or FRD
- Approved Confluence requirement page or uploaded document
- L2-escalated bug or existing Jira production defect

### Outputs

- Proposed Epics, Stories, Tasks, or Subtasks
- Testable acceptance criteria and INVEST review
- Module and category mapping
- Priority recommendation, dependencies, risks, and source traceability
- Jira creation summary only after authorized publication

### Exit criterion

The human Product Manager has reviewed, finalized, and triaged the backlog with contextual priority so that tickets are ready for analysis.

`create-product-backlog` prepares **Draft - Pending Product Manager Review**. Jira remains read-only during drafting and refinement. Publication requires both explicit backlog approval or finalization and a separate explicit Jira creation request.

## Stage 03 - Engineering Analysis

- **Lifecycle area:** Engineering Analysis
- **Role:** Technical Architect / Senior Developer
- **Primary skill:** `create-technical-design`

### Inputs

- One or more approved Jira Stories with acceptance criteria
- Approved BRD and FRD
- Workflow and architecture diagrams
- Current Confluence architecture
- Swagger/OpenAPI specifications
- Optional repository, configuration, deployment, and operational evidence

### Outputs

- One review-ready technical design package
- Requirements traceability and cross-layer impact analysis
- High-level and low-level design with justified decisions
- API compatibility and database schema-change determination
- Security, performance, observability, deployment, and testability notes
- Implementation risks and architecture-material open questions
- Mermaid diagrams when useful and DBML only when a schema change exists
- Optional repository-grounded Existing Architecture Summary when official DeepWiki MCP or supplied repository evidence is available

### Exit criterion

The human Technical Architect has reviewed the design, resolved or accepted material risks and open questions, and authorized implementation to begin.

`create-technical-design` finishes with **Ready for Architect Review** and **No implementation should begin until the design is reviewed.** It is read-only, produces no implementation code, never modifies Jira or Confluence, and never claims that the exit criterion has been met.
