# Confluence research guidelines

Confluence research is mandatory before every BRD draft. Use the connected Atlassian MCP and search before asking detailed questions.

## Research practice

Use an iterative search-read-refine loop:

1. Generate several focused searches dynamically from the user's evidence. Use relevant combinations of the feature name and variations, AMRIT module, roles, workflow names, business terminology, validation terminology, notification terminology, audit terminology, report terminology, government programme names, and business process names.
2. Search Confluence and rank results by their likely relevance to the business need.
3. Read only the most relevant pages. Consider BRDs, FRDs, PRDs, workflows, module documents, validations, change requests, decisions, meeting notes, user guides, support processes, programme documents, and templates.
4. Record available title, type, space, version, created/updated date, status, relevance, and link or page reference.
5. While reading, capture newly discovered module names, workflows, business terms, validation rules, reports, downstream systems, related features, and related documents.
6. Turn material discoveries and unresolved evidence gaps into additional focused searches. For illustration, a newly discovered workflow name can be combined with its module, or a named report can be combined with the applicable programme. Treat these as illustrations, not fixed query patterns.
7. Maintain a search ledger of queries run and a source ledger of pages read. Deduplicate semantically equivalent queries and do not reread unchanged pages.
8. Repeat until no meaningful new information is found, remaining results are irrelevant, or sufficient evidence exists to draft the BRD. Use no more than three research rounds; record unresolved gaps after the final round.
9. Prefer reviewed, approved, newer, or explicitly current material only when metadata supports the choice. Newer is not automatically authoritative; approved is not automatically current.
10. Record conflicting and possibly outdated sources instead of silently resolving or discarding them.
11. Preserve returned links or page references. Never fabricate metadata.
12. Summarize relevant content; do not copy confidential pages at length.

If no relevant pages are found, state: **No sufficiently relevant Confluence documents were found for this request.**

If the MCP fails, state that research could not be completed, report the failure briefly, and ask whether to retry or proceed with a source-limited draft. Never claim success after a failure.

Confluence is read-only by default. Do not create or update a page, add a comment, or publish without explicit user instruction after the draft is shown. Never expose MCP credentials or endpoints.

## Source evidence classification

- **Confirmed:** Directly supported by the user's material or relevant Confluence content.
- **Assumption:** Reasonable but not confirmed.
- **Conflict:** Two or more sources disagree.
- **Missing:** Required information was not found.
- **Possibly Outdated:** Date, version, or status signals suggest the source may not reflect the current process.

For conflicts, record source titles, conflicting statements, why the difference matters, and the clarification needed. For possibly outdated content, record the title, available date/version, and reason for concern.
