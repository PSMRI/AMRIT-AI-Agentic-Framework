# Implementation Workflow

## Contents

- [Purpose](#purpose)
- [Step 1: Read the Jira ticket](#step-1-read-the-jira-ticket)
- [Step 2: Research supporting requirements in Confluence](#step-2-research-supporting-requirements-in-confluence)
- [Step 3: Research architecture in DeepWiki](#step-3-research-architecture-in-deepwiki)
- [Step 4: Inspect the checked-out repository](#step-4-inspect-the-checked-out-repository)
- [Step 5: Build the implementation plan](#step-5-build-the-implementation-plan)
- [Step 6: Implement the change](#step-6-implement-the-change)
- [Step 7: Handle conflicting evidence](#step-7-handle-conflicting-evidence)
- [Step 8: Handle ambiguity](#step-8-handle-ambiguity)
- [Step 9: Report completion](#step-9-report-completion)
- [Research ledger](#research-ledger)

## Purpose

Sequence the work so that requirements are understood before architecture, architecture before code, and code before verification. Skipping forward produces changes that satisfy a title rather than a ticket.

Each step is read-only until Step 6. Jira and Confluence remain read-only throughout.

## Step 1: Read the Jira ticket

Accept the ticket key from the invocation, for example `/implement-jira-ticket AMRIT-1234` or `Implement AMRIT-1234`. If no key is supplied, ask for one before researching.

Retrieve the issue through the connected Jira read capability and read it in full:

- issue type — Story, Task, or Bug;
- summary;
- description;
- acceptance criteria;
- parent Epic;
- linked issues and their relationship type;
- subtasks;
- dependencies and blockers;
- attachments;
- comments that carry requirement or design decisions;
- priority where it affects scope or sequencing;
- components and modules;
- labels;
- linked Confluence pages;
- referenced technical-design material.

The acceptance criteria define scope. Where a ticket has no explicit acceptance criteria, derive the intended behaviour from the description and supporting documents, and state in the summary which criteria were inferred.

Do not transition the issue, comment, edit fields, assign users, create subtasks, or change status at any point, including after implementation succeeds.

If the issue cannot be retrieved, stop and report the retrieval failure. Never reconstruct requirements from the key, the branch name, or memory.

## Step 2: Research supporting requirements in Confluence

Follow any Confluence page linked directly from the Jira issue first. Then search focused terms derived from the Jira key, feature name, Epic, module, service, and business capability.

Look for:

- BRD;
- FRD;
- functional specifications;
- workflows;
- wireframes;
- acceptance rules;
- business rules;
- API requirements;
- architecture documents;
- approved technical design;
- related feature documentation.

Use a bounded search-read-refine loop. Deduplicate queries and pages, and stop when the evidence is sufficient, when no material new information appears, or after three rounds.

A BRD may not exist for every ticket:

- read an applicable BRD when one exists;
- continue on the remaining approved requirement evidence when there is none;
- never fabricate a BRD or cite a page that was not read;
- never stop implementation merely because no BRD exists.

Confluence is read-only. Do not create, edit, comment on, or publish a page.

Keep four categories distinct when reasoning and reporting:

1. Jira acceptance criteria.
2. Documented business or functional requirements.
3. Architectural guidance.
4. Assumption or inferred behaviour.

## Step 3: Research architecture in DeepWiki

Research the affected repository before editing application code. Use DeepWiki as the primary repository-intelligence source for:

- repository architecture;
- module responsibilities;
- existing implementation patterns;
- classes, services, controllers, repositories and DAOs;
- APIs;
- DTOs and models;
- frontend components;
- state management;
- utilities;
- configuration;
- dependency relationships;
- test conventions;
- relevant data flow;
- integration points;
- error-handling patterns;
- database-access patterns.

Discover the host's available repository-research capability rather than hardcoding a tool function name or binding to a particular local server name. Use only read-oriented operations.

### Selecting repositories

Do not search blindly across every AMRIT repository. Identify likely affected repositories from, in order:

1. the current working directory and the repository actually checked out;
2. the Jira ticket's components, module, service line, and Epic;
3. Confluence architecture evidence;
4. a repository catalog when the environment provides one.

AMRIT repositories are owned by the `PSMRI` GitHub organization and are typically paired as a UI repository and its API repository. Add `AMRIT-DB` when persistence may change, and add another repository only when discovered evidence identifies a material dependency. Start with no more than three repositories where practical.

### Fallback

If DeepWiki is unavailable, skip the phase and inspect the checked-out repository directly. Record in the summary that repository research was performed by direct inspection only.

DeepWiki assists understanding; the checked-out source tree is the final implementation truth. Never modify code solely because an architectural pattern was inferred from documentation without validating it against the actual repository.

## Step 4: Inspect the checked-out repository

Once likely impacted files and modules are identified, read them directly:

- repository-level instructions;
- `CLAUDE.md` when present;
- `AGENTS.md` when present;
- README and developer documentation;
- package and build configuration;
- lint configuration;
- formatting configuration;
- the relevant implementation files;
- nearby unit tests;
- relevant API definitions;
- relevant database-access code;
- relevant configuration;
- repository-specific development conventions.

Repository-specific conventions always take precedence over generic advice, including the advice in this skill's language references.

Also inspect `git status` before editing to know which files already carry uncommitted work. Never discard or overwrite existing uncommitted user changes, and never use destructive Git commands such as `git reset --hard` or `git clean -fd` to simplify implementation.

## Step 5: Build the implementation plan

Before editing, determine:

- which acceptance criteria are being implemented;
- affected modules and files;
- business rules involved;
- expected API changes;
- expected data-model changes;
- expected database changes;
- backward-compatibility impact;
- tests required;
- potential regression areas.

Trace every material code change back to one of:

- a Jira acceptance criterion;
- a supporting approved requirement or design;
- a necessary engineering change required to support those requirements.

A change that traces to none of these does not belong in this ticket. Do not add speculative features and do not implement future requirements outside the ticket.

## Step 6: Implement the change

Target the smallest coherent change that completely satisfies the ticket and its acceptance criteria.

- Preserve unrelated behaviour.
- Do not modify unrelated files.
- Do not perform broad refactors merely because a different architecture might look cleaner.
- Prefer extending an existing abstraction over introducing a parallel one.
- Do not introduce a new framework or library when the same result is reasonably achievable with dependencies and patterns already present.

Apply the language-specific reference for each file being changed, and the database reference whenever persistence is involved.

When the change spans an application repository and `AMRIT-DB`, keep the two compatible and track the changes separately for the completion summary.

## Step 7: Handle conflicting evidence

When Jira, Confluence, and the repository disagree, preserve both claims and their sources rather than silently selecting one.

Treat source code as the stronger evidence of current behaviour and approved documentation as the stronger evidence of intended behaviour.

Report the conflict before implementing when it materially affects:

- business behaviour;
- API contracts;
- security;
- database ownership;
- data semantics.

For ordinary engineering details that no requirement specifies, follow the existing codebase architecture and conventions without asking.

## Step 8: Handle ambiguity

Do not ask unnecessary questions. Inspect the codebase and make the choice most consistent with existing architecture.

Stop implementation only when choosing incorrectly could materially affect business behaviour, acceptance criteria, public API contracts, database schema or data semantics, security or privacy, destructive migration behaviour, or compatibility with another system.

When blocked, state:

1. what is known;
2. what conflicts or is missing;
3. why making an assumption would be unsafe;
4. the precise decision or evidence required.

Complete every independent part of the ticket that is safe to complete before stopping, and say explicitly what was left out.

Never invent missing requirements.

## Step 9: Report completion

Produce the completion summary defined in `SKILL.md`, then finish with exactly one of:

**Implementation complete and locally verified. Ready for PR preparation.**

**Implementation incomplete. Resolve the items above before PR preparation.**

Never state that the ticket is Done, approved, merged, or code-review signed off. Never create a branch, commit, push, or Pull Request, and never transition the Jira issue.

## Research ledger

Keep a compact ledger through the run containing queries executed, sources read, findings that changed the plan, conflicts, and unresolved gaps. Use it to avoid repeating searches, to build the traceability in the summary, and to report exactly which evidence supported the implementation.
