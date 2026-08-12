# answer-codebase-questions

`answer-codebase-questions` gives AMRIT Software Engineers a concise,
evidence-backed answer to implementation, ownership, data-flow, integration,
architecture, and design-rationale questions.

## Intended users

The primary users are Software Engineers, Technical Architects, and Open-Source contributors investigating AMRIT codebases.

## Inputs

The skill accepts questions about repositories, services, modules, classes,
functions, APIs, validation, persistence, data flow, integrations, current
behaviour, architecture, and documented design rationale.

It does not handle ticket status, assignments, sprints, backlog creation, or
Jira requirement analysis.

## Research capabilities

The skill uses read-only DeepWiki repository research first, Confluence for
needed architecture and workflow context second, and Graphify only as the
final fallback for unresolved cross-repository relationships. It never uses
Jira.

The repository MCP configuration supplies DeepWiki, Atlassian, and Graphify
server definitions for supported project clients. Tool names may vary by
client; use their equivalent read-only search and read capabilities.

## Output

The output leads with a direct answer and, where useful, provides precise
evidence, confidence, conflicts, and remaining gaps. Current implementation,
documented intent, inference, and unresolved points remain distinct.

## Use and distribution

Invoke `/answer-codebase-questions` from the repository root using a supported
coding agent. Configure local MCP credentials only where the selected client
requires them; never commit real tokens.

For a packaged installation, download `answer-codebase-questions.zip` from the
latest successful **Validate and package skills** GitHub Actions run and upload
or install it with the relevant client workflow. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
