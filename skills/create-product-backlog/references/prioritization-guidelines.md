# Prioritization Guidelines

Recommend priority only from evidence and explain the rationale. Do not map words such as "urgent" or "critical" directly to a Jira priority.

## Assess

- **Impact:** What service, workflow, data, or outcome is affected?
- **Affected population:** Which users, roles, sites, programmes, or integrations are affected, and how broadly?
- **Urgency:** What deadline, operational window, escalation, or accumulating harm exists?
- **Production impact:** Is live use blocked, degraded, or unaffected?
- **Regulatory importance:** Is a documented statutory, government-programme, privacy, safety, or audit obligation involved?
- **Dependency pressure:** Does the item block other approved work or a committed release?
- **Workaround:** Is a safe, practical workaround available and at what operational cost?
- **Evidence strength:** Which source supports each factor?

## Produce a recommendation

```text
Priority recommendation: <actual Jira option if discovered, otherwise proposed level>
Rationale: <affected users and impact>; <urgency or deadline>; <production/regulatory/dependency context>; <workaround status>.
Evidence: <source references>
Confirmation needed: <field option or missing fact, if any>
```

Use the target project's actual priority options for publication. If options are not yet known, describe relative priority as a proposal and do not invent a Jira value.

## Defect-specific rules

- Distinguish severity or technical impact from business priority.
- Preserve an existing production-defect priority until a human explicitly approves a change.
- Capture whether the incident is ongoing and whether the workaround is safe.
- Do not infer frequency, affected-user count, regulatory impact, or data loss without evidence.

## Feature-specific rules

Consider approved business value, beneficiary reach, obligations, dependencies, and timing. Do not treat document order as priority and do not invent dates or commitments.
