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
