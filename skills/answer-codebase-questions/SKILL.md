---
name: answer-codebase-questions
description: Answer questions about AMRIT codebases by researching DeepWiki first, consulting Confluence for architecture and workflow context when needed, and using Graphify as the final fallback for cross-repository relationships. Do not use Jira.
metadata:
  stage: Cross-lifecycle
  category: Codebase knowledge
  primary_role: Software Engineer
  knowledge_sources:
    - DeepWiki
    - Confluence
    - Graphify
  supported_inputs:
    - Codebase implementation questions
    - Architecture questions
    - Component responsibility questions
    - Data flow and integration questions
    - Repository navigation questions
    - Historical design rationale questions
  primary_output: Evidence-backed codebase answer
---

# Answer Codebase Questions

Answer AMRIT implementation and architecture questions with concise, traceable,
read-only research. Lead with the answer, then provide only the evidence needed
to support it.

Never use Jira. Do not handle ticket status, assignments, sprints, backlog
creation, or Jira requirement analysis. Do not modify repositories, documents,
or connected systems.

## Discover available capabilities

Use the connected tools' logical DeepWiki repository search/read, Confluence
search/page-read, and Graphify search/relationship-read capabilities. Tool names
vary by host: discover equivalent read-only operations rather than assuming names.
Do not request write permissions or invoke write operations.

If a required source is unavailable, report that limitation when it prevents a
reliable answer. Do not fabricate a result or ask to install a tool during normal
execution.

## Research workflow

Maintain a compact research ledger of queries, sources read, findings,
conflicts, and unresolved gaps. Build focused queries from the user's terms and
each material discovery; deduplicate equivalent searches and do not reread an
unchanged source.

### 1. Research DeepWiki first

Always begin with DeepWiki. Use it for repository structure, files and
directories, symbols, functions, classes, APIs, services, dependencies,
implementation behaviour, and cross-repository code relationships.

Start with the most likely repository or symbol. Inspect the relevant source
context before making a claim. A loosely related page, symbol, or repository
result is not sufficient evidence for the actual question.

Assess whether the direct implementation evidence completely answers the
question. Continue to Confluence if it does not, or if context about intended
behaviour, architecture, workflow, terminology, integration, historical design
rationale, or implementation-to-design alignment is needed.

### 2. Consult Confluence when needed

Search and read the relevant Confluence pages when DeepWiki is incomplete or
the question requires architectural, product, workflow, design-rationale,
terminology, integration, or documented-design context.

Combine direct DeepWiki implementation evidence with Confluence context when
both are relevant; do not treat the sources as competing substitutes.

### 3. Use Graphify as the final fallback

Use Graphify only when DeepWiki and Confluence remain insufficient, or when
relationships across repositories, components, services, APIs, documents, or
concepts need additional investigation. Treat Graphify as the final research
fallback, not the starting point.

## Evidence and stopping rules

Stop only when the available evidence is direct, consistent, and complete
enough to answer responsibly. Do not stop merely because a search returned
some information.

Classify material statements as:

- **Verified implementation behaviour**: directly supported by code or
  implementation evidence.
- **Documented intended behaviour**: directly supported by approved
  documentation.
- **Evidence-backed inference**: strongly indicated by retrieved evidence but
  not directly stated.
- **Unresolved**: unsupported, unavailable, incomplete, or conflicting.

When evidence conflicts, identify the conflict and its sources. Prefer direct
code evidence for current runtime implementation and approved documentation for
intended architecture or business behaviour. Never silently choose one source.

Never invent repository names, files, symbols, APIs, database tables,
architecture decisions, service relationships, or implementation behaviour. If
the available sources cannot support a reliable answer, state that it could not
be verified and name the missing evidence.

## Answer format

Use this structure when it adds value; omit headings that would be trivial.
Mention only sources actually consulted and cite concrete evidence whenever it
is available.

```markdown
## Answer

<Direct response to the question>

## Evidence

- DeepWiki: <repository, file, symbol, or implementation evidence>
- Confluence: <architecture, workflow, or design evidence>
- Graphify: <relationship evidence>

## Confidence

High | Medium | Low

## Gaps

<Only include when something remains unresolved>
```

Use repository names, file paths, classes, functions, API routes, service
names, Confluence page titles, and Graphify entities or relationships where
retrieved. Keep citations precise, distinguish current implementation from
documented intent, and avoid a long narration of the research process.
