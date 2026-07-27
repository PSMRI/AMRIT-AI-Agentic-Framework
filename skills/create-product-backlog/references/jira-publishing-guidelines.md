# Jira Publishing Guidelines

## Non-negotiable write gate

Keep Jira read-only unless both statements are established:

1. The human explicitly approved or finalized the specific backlog version.
2. The human separately and explicitly requested creation or publication of that finalized backlog in Jira.

Approval alone is insufficient. A publication request for an unfinalized or materially changed draft is insufficient. If either condition is uncertain, do not write and ask one focused confirmation question.

Any material revision after approval returns the changed items to **Draft - Pending Product Manager Review** unless the human explicitly approves the revised version.

## Discover before writing

Use actual available Atlassian MCP schemas to discover:

- target project and permissions;
- issue types and supported parent-child hierarchy;
- required create fields;
- field names, current custom-field IDs, and valid options;
- priority, module, category, component, and label conventions;
- similar existing issues and source-linked duplicates.

Never hardcode custom-field IDs or assume another project's configuration applies.

## Duplicate check

Compare proposed items with Jira by summary, business intent, module, source IDs or links, labels, and relationships. Present likely duplicates and recommend create versus update. Never update or duplicate an issue without explicit instruction.

## Pre-publish preview

Show:

- target project;
- counts of Epics, Stories, Tasks, and Subtasks;
- issue types and hierarchy;
- modules, categories, priorities, and labels;
- each parent-child relationship;
- existing issues proposed for update;
- new issues proposed for creation;
- unresolved or missing fields;
- whether production-defect CAPA-required tagging applies.

Resolve ambiguous project, hierarchy, issue type, required field, or update behavior before writing.

## Safe creation order

1. Create one Epic and capture the returned key.
2. Create its Stories with supported relationships and capture returned keys.
3. Create Tasks or Subtasks with valid parents.
4. Add only approved links, comments, or updates.
5. Repeat for later Epics.
6. Read back created or updated issues and verify summaries, fields, relationships, and status.
7. Report only Jira-returned keys and links.

Use batch creation only when ordering, required fields, and relationships remain safe. Do not perform blind bulk creation.

## Boundaries

- Keep newly created work in the backlog.
- Do not transition to active development, assign a sprint, change a production-defect priority, comment, move, or link unless the user's explicit authorization covers that action.
- Do not publish items with missing required information.
- Set `Jira Publication Status: Published` only for verified successful writes; report partial failures precisely.
