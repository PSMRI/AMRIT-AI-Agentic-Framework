# implement-jira-ticket

`implement-jira-ticket` is the **Stage 04 — In Development entry point** and the engineering orchestrator for that stage. It takes one approved AMRIT Jira ticket, researches the requirement and the affected architecture, inspects the actual source code, decides which engineering personas the change really needs, runs only those specialists, coordinates their dependencies, verifies the result, and reports the evidence.

**This skill changes source files**, directly or through the specialists it invokes. That makes it intentionally different from the read-only `create-technical-design` and `answer-codebase-questions` skills.

## Purpose

Turn an approved Jira ticket into a minimal, convention-respecting, locally verified code change with unit tests — implemented by the right engineering roles, in the right order, in the right repositories — ready for a separate skill to prepare the Pull Request.

## Invocation is unchanged

```text
/implement-jira-ticket AMRIT-1234
```

```text
Implement AMRIT-1234
```

Users do not select personas by hand. There is no need to invoke `/implement-backend-change`, `/implement-database-change`, or `/write-unit-tests` separately for ordinary ticket implementation: this skill routes the ticket. The specialists remain independently invocable for focused work.

If no ticket key is supplied, the skill asks for one before researching.

## Stage 04 architecture

```text
                       Jira ticket
                            │
                            ▼
                  implement-jira-ticket
                      (meta-skill)
                            │
        ┌───────────────────┴───────────────────┐
        ▼                                       ▼
  Knowledge research                    Source-code inspection
  (DeepWiki, Confluence,                (mandatory, always)
   Graphify, Jira)
        └───────────────────┬───────────────────┘
                            ▼
              Impact and persona classification
                            │
   ┌────────────┬───────────┼───────────┬────────────┐
   ▼            ▼           ▼           ▼            ▼
architecture  database   backend    frontend      android
  review                                          /kotlin
   └────────────┴───────────┼───────────┴────────────┘
                            ▼
                  UX implementation validation
                            │
                            ▼
                      write-unit-tests
                            │
                            ▼
                       verification
                            │
                            ▼
                   create-development-pr
```

Every specialist below the classification step is **conditionally selected**. Nothing runs unconditionally except unit tests when production behaviour changed.

## Specialist skills

| Persona | Skill | Selected when |
| --- | --- | --- |
| Technical Architect | [`review-implementation-architecture`](../review-implementation-architecture/README.md) | cross-cutting or cross-repository change, new component or contract, changed ownership or integration boundary, security- or performance-material change, suspected design deviation |
| DBA / Database Engineer | [`implement-database-change`](../implement-database-change/README.md) | a schema object, migration, index, constraint, or data-compatibility concern exists |
| Backend Developer | [`implement-backend-change`](../implement-backend-change/README.md) | services, APIs, controllers, domain logic, integrations, validation, persistence integration, error handling, or backend configuration change |
| Frontend Developer | [`implement-frontend-change`](../implement-frontend-change/README.md) | web UI, components, state, API integration, forms, client validation, accessibility, or frontend error handling change |
| Android / Kotlin Developer | [`implement-android-change`](../implement-android-change/README.md) | the Android applications change, including offline behaviour and platform constraints |
| UX / UI Specialist | [`validate-ux-implementation`](../validate-ux-implementation/README.md) | a user-visible change exists and approved UX or design-system rules apply |
| SDET / developer testing | [`write-unit-tests`](../write-unit-tests/README.md) | production behaviour changed — effectively always |

Each specialist inspects the code it owns before editing. The orchestrator passes boundaries and contracts, not a digest of the codebase, so it never becomes a lossy context bottleneck.

Every skill is independently installable. When a selected persona's specialist skill is not installed, the orchestrator applies that persona's contract inline and says so in the report; the persona is never skipped.

## Routing examples

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

See [examples/sample-persona-routing.md](examples/sample-persona-routing.md) for the full fictional walk-through, including both blocked cases.

## Research order

1. **Jira** — the full issue: type, summary, description, acceptance criteria, Epic, links, subtasks, dependencies, attachments, decision-bearing comments, priority, components, labels, and linked Confluence pages. Read-only.
2. **Confluence** — the approved Stage 03 technical design first, then BRD, FRD, functional specifications, workflows, wireframes, business rules, and API requirements. Read-only. A missing BRD does not stop implementation and is never fabricated.
3. **DeepWiki** — repository architecture, module responsibilities, major flows, abstractions, integration boundaries, and existing implementation patterns for the repositories the ticket plausibly touches.
4. **Graphify** — final fallback for unresolved cross-repository relationships.
5. **The checked-out repositories** — the implementation truth, consulted in every route.

This matches the knowledge-source philosophy of [`answer-codebase-questions`](../answer-codebase-questions/README.md).

## Actual code inspection is mandatory

Documentation answers *what the system is intended to do*. The source code answers *what the system currently does and where the change must actually be made*.

The skill never implements a ticket purely from Jira, Confluence, DeepWiki, Graphify, architecture documentation, or previous knowledge. Findings that influence an edit are verified against the checked-out source, and material documentation-versus-code conflicts are reported rather than resolved silently.

If the relevant repository or source code cannot be accessed, the skill stops and reports that implementation cannot safely proceed.

## Respecting the approved Stage 03 design

Stage 04 implements the approved design; it does not replace it. When source inspection shows the approved design cannot be implemented safely as written — for example when ownership of the data has moved to another service — the skill stops and surfaces the discrepancy for design review instead of deviating silently.

## Repository boundaries

A ticket may affect more than one repository. The skill names each affected repository and the modules inside it, states which candidate repositories require no change, and never modifies an unrelated repository because a persona exists for it. Application repositories and `AMRIT-DB` remain separate Git repositories.

## AMRIT-DB schema ownership rule

Every change is classified explicitly as **no database change**, **application model/query change only**, or **database schema change**.

Any actual schema change is implemented in `AMRIT-DB` by `implement-database-change`, never in an application repository for convenience. If `AMRIT-DB` is unavailable, no local substitute migration is created; the required change is stated, the dependent work stops, and the implementation is reported incomplete.

## Test and verification behaviour

Unit tests are mandatory for changed behaviour and are owned by `write-unit-tests` — developer, code-level testing, kept conceptually separate from `draft-test-cases` and Stage 07 QA execution.

Verification commands are discovered from each changed repository, never assumed, and run narrowest first. A check is reported as PASS only when it actually ran successfully; otherwise it is `FAILED` with the cause or `NOT RUN` with the reason.

## Human accountability

The skill implements and verifies. It never produces, implies, or assumes architecture approval, DBA approval, code-review approval, QA approval, release approval, CI results, or test results it did not observe. Absent approvals are reported as absent.

## Git and Pull Request boundaries

The skill **may** inspect `git status`, `git diff`, and history.

The skill and its specialists **must not** create or rename a branch, commit, amend, squash, rebase, merge, push, force-push, create, merge, or approve a Pull Request, or claim code-review sign-off. Jira and Confluence are never written to, and destructive Git commands are never run.

Branch creation, Git operations, PR title and description, PR creation, and review preparation belong to the downstream [`create-development-pr`](../create-development-pr/README.md) skill. That skill is independently installable; this one completes without it.

## Completion status semantics

Every invocation ends with exactly one of:

- **Implementation complete and locally verified. Ready for PR preparation.**
- **Implementation incomplete. Resolve the items above before PR preparation.**

Neither line means the ticket is Done, approved, merged, or code-review signed off.

## Required capabilities

Read access to Jira, Confluence, and DeepWiki, with Graphify and OpenProject used where the environment provides them, plus the host's filesystem, repository-editing, command-execution, and skill-invocation capabilities. Tool names vary by host, so capabilities are discovered rather than hardcoded. Jira and Confluence writes are never requested or used.

If DeepWiki is unavailable, the skill falls back to direct repository inspection and says so. If the Jira issue cannot be retrieved, it stops rather than inventing requirements. If the source code is unavailable, it stops rather than implementing from documentation.

## Example invocation

```text
/implement-jira-ticket DEMO-5140
```

See [examples/](examples/) for fictional inputs and outputs, including a full-stack feature, a backend-only bug with a partially implemented criterion, a database change under both available and unavailable `AMRIT-DB` conditions, and the persona-routing walk-through. The examples are illustrative only and do not describe real AMRIT architecture.

## Use and distribution

Invoke `/implement-jira-ticket` from the repository root using a supported coding agent. Configure local MCP credentials only where the selected client requires them; never commit real tokens.

For a packaged installation, download `implement-jira-ticket.zip` from the latest GitHub Release, together with the specialist packages you want available. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
