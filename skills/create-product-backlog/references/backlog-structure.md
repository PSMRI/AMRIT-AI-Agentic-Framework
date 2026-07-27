# Backlog Structure

## Issue-type decisions

| Type | Use when | Avoid when |
|---|---|---|
| Epic | A coherent business outcome needs multiple Stories and spans a meaningful body of work. | The scope is one independently deliverable behavior. |
| Story | A user or stakeholder receives a testable unit of value that can be discussed and delivered. | The item only describes internal activity or is too broad to validate. |
| Task | Analysis, configuration, migration, documentation, implementation support, or operational work has a concrete result but is not naturally a user story. | The Jira project requires the work to be represented as a Subtask. |
| Subtask | The configured Jira hierarchy supports it and a small piece of work must sit beneath a Story or Task. | The parent relationship or project scheme is unknown. |

Discover the target Jira project's actual issue types and hierarchy before publication. Do not assume that a Task can be a child of a Story or that every project enables Subtasks.

## Suggested hierarchy

```text
Epic: coherent business objective
|- Story: independently testable user value
|  |- Subtask: supported, necessary child work
|- Story: another independently testable value slice
|- Task: non-story work linked through the project's supported model
```

Use `EPIC-01`, `STORY-01`, and `TASK-01` while drafting. Replace them only with keys returned by Jira.

## Decomposition method

1. Anchor each Epic to a business objective and approved scope.
2. Slice Stories vertically by observable user outcome, workflow step, business rule, role, or scenario.
3. Keep acceptance criteria within one coherent behavior.
4. Create Tasks only for work with a clear purpose and expected result.
5. Preserve source IDs and dependencies on every important item.
6. Run INVEST review after decomposition and revise weak Stories.

## Common mistakes

- **Epic as a document dump:** Split by coherent objectives, not BRD sections alone.
- **Story as a project phase:** "Build backend" and "test feature" lack standalone user value; slice end-to-end behavior instead.
- **Oversized Story:** Split by role, workflow state, rule, channel, or positive/negative scenario while preserving value.
- **Microscopic Story:** Combine items that cannot deliver or be tested meaningfully alone.
- **Task disguised as Story:** Use a Task for migrations, research, configuration, or documentation when the user-story form is unnatural.
- **Unsupported hierarchy:** Mark the relationship as proposed until Jira configuration is discovered.
- **Invented scope:** Keep unclear behavior in open decisions rather than turning it into tickets.

## Size checks

Do not invent estimates or story points. Treat a Story as probably too large when it contains several independent outcomes, many unrelated rules, multiple roles with different goals, or acceptance criteria that could be released separately. Split it or record a Product Manager decision.
