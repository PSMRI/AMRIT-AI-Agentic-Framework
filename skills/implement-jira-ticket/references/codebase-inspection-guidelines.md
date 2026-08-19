# Codebase Inspection and Knowledge Sources

## Contents

- [The rule](#the-rule)
- [Knowledge-source order](#knowledge-source-order)
- [DeepWiki](#deepwiki)
- [Confluence](#confluence)
- [Graphify](#graphify)
- [Jira and OpenProject](#jira-and-openproject)
- [Mandatory source-code inspection](#mandatory-source-code-inspection)
- [What to inspect](#what-to-inspect)
- [Reconciling documentation with code](#reconciling-documentation-with-code)
- [When source code is unavailable](#when-source-code-is-unavailable)
- [Review checklist](#review-checklist)

## The rule

Documentation answers **what the system is intended to do**.

The source code answers **what the system currently does, and where this change must actually be implemented**.

Both are required. Neither replaces the other. Where they disagree about current behaviour, the code is correct about the present and the approved documentation is authoritative about the intent — and the disagreement itself is reportable.

A ticket must never be implemented purely from documentation.

## Knowledge-source order

The framework's established order for technical and codebase knowledge, defined by the `answer-codebase-questions` skill, applies here:

1. **DeepWiki** — repository intelligence.
2. **Confluence** — intended architecture, workflows, design rationale.
3. **Graphify** — final fallback for unresolved cross-repository relationships.

Jira supplies the requirement. OpenProject, where configured, supplies delivery context. The checked-out repository is the implementation truth and is consulted in every route, regardless of which other sources answered.

Discover the connected tools' actual names and schemas. Do not hardcode MCP function names, bind to a particular local server name, or assume a host implementation. Use read operations only. When a source is unavailable, continue on the remaining evidence and record the limitation in the report; do not ask the user to install a tool during normal execution.

## DeepWiki

When DeepWiki is available for a repository, read the relevant documentation before implementation to understand:

- repository architecture;
- module responsibilities;
- major flows;
- important abstractions;
- integration boundaries;
- existing implementation patterns;
- API structure, models, and DTOs;
- frontend components and state management;
- configuration;
- test conventions;
- database-access and migration patterns.

Then verify every finding that will influence an edit against the actual source. DeepWiki is context; the repository is implementation truth.

Select repositories deliberately, using the current working directory, the ticket's components and Epic, the approved design, Confluence evidence, and [amrit-repository-map.md](amrit-repository-map.md). Do not research the whole AMRIT estate.

If DeepWiki is unavailable, inspect the checked-out repositories directly and record in the report that repository research was performed by direct inspection only. DeepWiki absence never justifies implementing without reading the code — it makes reading the code the only source.

## Confluence

Use Confluence for intended behaviour, approved requirements, approved technical design, workflows, wireframes, terminology, integration agreements, and historical design rationale. It is read-only.

Confluence describes intent. It does not establish that the code is currently built that way.

## Graphify

Use Graphify only when DeepWiki, Confluence, and direct inspection leave a relationship unresolved — typically cross-repository dependencies, service relationships, or impact spread across components. Treat it as the final research fallback, not the starting point, and validate what it returns against the code.

## Jira and OpenProject

Jira defines the requirement and the acceptance criteria and is strictly read-only. Where the environment exposes OpenProject and the work is tracked there, use it read-only for delivery context such as related work packages and dependencies. Neither system describes the implementation.

## Mandatory source-code inspection

Before any edit, in every route:

1. Confirm which repositories are actually checked out and accessible.
2. Read the real files that the change will touch, and their neighbours.
3. Confirm that the structures named in the ticket, the approved design, or DeepWiki actually exist, with the ownership the documentation claims.
4. Confirm the conventions the change must follow from the code itself.
5. Confirm the tests that already cover the behaviour.
6. Inspect `git status` so existing uncommitted user work is known and preserved.

Never change code solely because a pattern was inferred from documentation. Never assume a class, service, table, endpoint, component, or module exists because a document mentions it.

## What to inspect

Depending on the route:

- repository-level instructions, `CLAUDE.md`, and `AGENTS.md` when present;
- README and developer documentation;
- package, build, and dependency configuration;
- lint, formatting, and static-analysis configuration;
- the implementation files the change touches;
- nearby unit tests and the test conventions in use;
- API definitions and contracts consumed by other repositories;
- persistence code, entities, repositories or DAOs, and migration directories;
- frontend components, shared design-system components, and state management;
- Android modules, offline and sync behaviour, and platform configuration;
- relevant runtime and environment configuration.

Repository-specific conventions always take precedence over generic advice, including the advice in this framework's references.

## Reconciling documentation with code

For every material claim that will influence an edit, decide which of these it is:

- **Confirmed in code** — the file, symbol, contract, or schema object was read.
- **Documented intent** — an approved document states it; the code has not been shown to match.
- **Inferred** — strongly indicated by structure or convention, not directly confirmed.
- **Conflict** — documentation and code disagree materially.

Report a conflict rather than silently choosing a side when it affects business behaviour, API contracts, security, database ownership, data semantics, or module ownership. Where the approved Stage 03 design cannot be implemented as written, use the `IMPLEMENTATION BLOCKED` output defined in `SKILL.md`.

For ordinary engineering details that no requirement specifies, follow the existing codebase without asking.

## When source code is unavailable

If the relevant repository cannot be read or is not present in the environment:

1. Do not implement anything for that repository.
2. Do not substitute documentation, DeepWiki, Graphify, or previous knowledge for the code.
3. Complete only the parts of the ticket in repositories that are actually accessible, when they are safe on their own.
4. Report `IMPLEMENTATION BLOCKED` for the inaccessible repository, naming what is needed.
5. Finish with **Implementation incomplete. Resolve the items above before PR preparation.**

## Review checklist

- the actual source was inspected before any edit, in every route;
- no structure was assumed to exist because a document named it;
- DeepWiki findings that influenced an edit were verified against the code;
- unavailable sources are recorded as limitations, not silently ignored;
- documentation-versus-code conflicts are reported, not resolved silently;
- inaccessible source produced a blocked report rather than a documentation-driven implementation.
