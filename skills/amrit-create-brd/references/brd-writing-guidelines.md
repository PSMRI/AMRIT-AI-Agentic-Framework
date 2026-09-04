# BRD writing guidelines

- Use clear, professional business language focused on what the business needs.
- Avoid detailed technical design.
- Preserve source-supported AMRIT terminology, module names, and role names.
- Use “shall” for mandatory requirements and “should” only for recommendations.
- Clearly distinguish confirmed information from assumptions.
- Never hide missing information, fabricate approval, mark the document final, or use “approved” without explicit evidence.
- Keep requirement identifiers stable, avoid duplicates, and give unrelated requirements separate identifiers.
- Make each requirement reasonably testable when evidence is sufficient.
- Use tables only when they improve clarity.
- Mention the relevant screen, module, workflow, page, or role when supplied.
- Treat screenshots as supporting references, not the sole definition of behaviour.
- Summarize and adapt relevant source material; do not copy large passages from Confluence.
- Make every important Business Requirement and Functional Requirement traceable to one or more evidence sources whenever possible. Evidence may include user-supplied information, uploaded documents, meeting notes, government guidelines, and Confluence pages.
- Name the source precisely enough to locate it and include its section or heading when available. Do not fabricate citations or source metadata.
- If a requirement's origin cannot be identified, write `Not explicitly identified` in its Source field.
- Use confidence only to communicate evidence strength, never correctness: **High** for direct support from user input or Confluence, **Medium** for indirect support from multiple related documents, and **Low** for an explicitly stated assumption.
- Do not infer or invent confidence. If confidence cannot reasonably be determined, omit the value.
- Retain uncertainty under assumptions, open questions, conflicts, or human confirmation.
- Do not invent implementation detail.

Label technical suggestions exactly:

> **Implementation consideration — not a business requirement**

Do not present API design, database tables or columns, frameworks, code classes, deployment architecture, queues, infrastructure, or internal service boundaries as confirmed business requirements unless explicitly supplied.
