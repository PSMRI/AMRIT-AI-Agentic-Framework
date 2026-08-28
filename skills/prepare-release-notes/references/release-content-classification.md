# Release Content Classification

How to sort release-member Jira issues into the categories the selected template
uses. Classification is an evidence exercise, not a naming exercise.

## Categories come from the template

Do not invent categories. Inspect the selected template first and use its actual
section names and grouping axis.

The current conventions differ by product family, and the difference is
structural, not cosmetic:

| Family | Grouping axis observed in recent pages |
| --- | --- |
| AMRIT Web and API | one combined table of features, enhancements, and fixes, plus a separate security section |
| FLW App | a `Fixed Points` section subdivided by **priority** and then by kind |

Verify the current axis at runtime. If the newest applicable pages group by
priority, group by priority. If they group by work-item type, group by type. Do
not translate one convention into the other.

Only use category names such as `Enhancements`, `Fixed Points`, `Bug Fixes`,
`Security Fixes`, or `Known Issues` when the selected template actually uses them.

## Every issue type is release content

Classification decides **where** an issue appears. It never decides **whether** it
appears.

```text
If an issue belongs to the target Jira Fix Version,
it must be considered release content regardless of issue type.
```

The recent AMRIT release-note samples happen to contain `Story`, `Task`, and
`Bug`. That is an observation about those samples. It is not a whitelist and must
never become one.

Never silently drop `Epic`, `Sub-task`, `Improvement`, or any other or unfamiliar
issue type because the historical samples did not contain it. When a type has no
obvious home in the selected structure:

- place it using the best available evidence;
- state where it was placed and why;
- flag it for reviewer confirmation.

A presentation-level rollup is acceptable where the template calls for one — for
example listing a parent with its children beneath it. Rolling up is not dropping:
the rolled-up issue stays visible and stays in the ticket count.

## Evidence for classification

Classify from actual Jira evidence:

1. **Issue type** — the primary placement signal. `Bug` is a defect; `Story` and
   `Task` are normally delivery work. Placement only: issue type is never an
   eligibility test.
2. **Parent, epic, or epic link** — places work in a feature context.
3. **Labels** — for example a security or VAPT label marking a security fix.
4. **Components** — where the project uses them.
5. **Service line or product field** — where the instance defines one.
6. **Priority** — required when the template groups by priority.
7. **Jira release metadata** — the version description often names the release theme.
8. **Issue description** — used to disambiguate, not to override the issue type.

Never classify an item from its summary wording alone. A summary reading "improve
sync performance" does not make a `Bug` an enhancement, and "fix the incentive
screen" does not make a `Story` a defect.

## Issue type is not always decisive

Real AMRIT projects carry defect-shaped work as `Task` and delivery work as `Bug`.
Both happen.

When the issue type and the other evidence disagree:

- prefer the issue type as the default;
- allow the combined evidence to place the item elsewhere when it is clear —
  for example a `Bug` carrying a security label belongs in the security section
  when the template has one;
- record the reasoning where the placement was not straightforward;
- flag the item in the review summary when the evidence remains genuinely split,
  so a human can move it.

Do not silently reclassify to make a section look better balanced.

## Bugs fixed

The team specifically requires bugs fixed to come from Jira. For the target
release:

1. take the release-member issue set;
2. identify which issues Jira classifies as bugs or defects, using the actual
   issue type and the project's conventions;
3. take their real keys from Jira;
4. take their real summaries from Jira;
5. take their current statuses and resolutions from Jira;
6. render them in the selected template's bug or fixed-point format.

Rules:

- never fabricate a bug fix;
- never copy a bug list from a previous release note;
- never restate a defect as a different defect;
- minor cleanup for readability is acceptable — trimming an environment prefix,
  fixing capitalization, expanding an abbreviation — but the meaning must survive
  intact;
- a Jira summary that is uninformative stays uninformative. Do not invent detail
  to improve it; if the reviewer needs better wording, they can supply it.

## Features and enhancements

Obtain these from Jira as well, classified from issue type, parent or epic,
labels, components, release metadata, and description.

Do not classify an item as an enhancement solely because it sounds like one, and
do not promote a small task into a headline feature because the release needs one.

Where the template distinguishes features from enhancements, apply the distinction
the recent pages actually draw. Where the template combines them in one section —
as the current Web and API convention does — do not split them.

## Security fixes

Where the template has a security section, populate it from evidence: a security
or vulnerability-assessment label, a security component, or an unambiguous
security subject in the issue itself.

Where the template has the section and the release has no such issues, follow the
template's own convention for an empty section rather than deleting the heading.

## Known issues and limitations

Include only when supported by current evidence:

- Jira issues explicitly associated with the release as known issues;
- unresolved issues carrying the release's Fix Version;
- release-specific Jira metadata or comments identifying a limitation;
- explicit user-provided release information.

Never carry limitations forward from the previous release. A limitation on the
previous page is evidence about the previous release only.

Do not assert `No known issues` unless the evidence reasonably establishes it.
Prefer the honest form:

```text
No known issues identified from the available Jira release evidence.
```

Where the template's own convention for an empty section is a fixed phrase, use
that phrase — but never in a way that asserts more certainty than the evidence
supports.

## Release description

Synthesize it from the classified release content. It may summarize major
functionality introduced, important enhancements, defects fixed, and affected
service lines.

Every factual claim must be traceable to an included Jira ticket. Specifically:

- do not claim a feature the release does not contain;
- do not claim business impact, adoption, or performance improvement that no
  ticket establishes;
- do not name a state, deployment, or programme unless the tickets or Jira release
  metadata name it;
- the version description from Jira is legitimate evidence for the release theme.

Prose is expected. Invention is not.

## Service line and line of business

Where the template has a service-line column or a line-of-business field:

```text
explicit Jira Service Line field
→ use it as-is

Service Line unavailable, value inferred from labels/components/product context
→ mark it as inferred and requiring reviewer confirmation
```

An explicit Jira Service Line is never overridden by how a historical Confluence
release note categorized the same module, area, or ticket.

Mark inferred values visibly so a reviewer can tell evidence from judgement — for
example `Admin (inferred)` — and list them in the review summary for confirmation.

Where no evidence establishes a service line for an item, use the template's
convention for unclassified or common work rather than guessing a programme, and
mark it as unestablished. The line-of-business field for the release as a whole is
the set of service lines the included tickets actually establish, not the set the
previous release listed.

## Statuses

Take every status from Jira verbatim. Do not normalize, translate, or tidy. If
Jira says `Closed`, write `Closed`. If it says `In QA`, write `In QA` — and flag
it, because a release note listing a ticket that is not done is a signal worth
raising.

Never copy a status from a historical release note.

## Ordering

Follow the ordering the recent pages show — commonly by work-item type then key
for the Web and API convention, and by priority band for the FLW convention.
Where no ordering is evident, order deterministically by issue type and then key,
and state the choice.

## No Fix Version issue disappears

Every issue in the target Fix Version is accounted for in the draft. A
presentation-level rollup is allowed where the template calls for one, but the
issue stays visible and stays in the ticket count:

```text
Presentation note:
- DEMO-9999 (Sub-task) is listed beneath its parent DEMO-9998 per the current
  template convention. Both remain in the ticket tables and the ticket count.
```

If the user directs an exclusion, apply it and record that it rests on their
instruction rather than on Jira evidence:

```text
Excluded on user instruction:
- DEMO-9997 — excluded at the user's request; Jira still places it in the target
  Fix Version.
```

A silent omission is indistinguishable from an error, and an issue dropped because
its type was unfamiliar is a defect in the release note.
