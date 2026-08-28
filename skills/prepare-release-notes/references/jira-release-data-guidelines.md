# Jira Release Data Guidelines

Jira is the authoritative source for what is in a release and for the release
metadata Jira actually holds. Every interaction described here is read-only.

## Resolve the Fix Version first

Everything else depends on this step.

```text
Target version
    ↓
Resolve Jira Fix Version
    ↓
Retrieve all issues assigned to that Fix Version
    ↓
Inspect issue metadata/content
    ↓
Classify release contents
```

Read the project's version list and match the target against it. Record the exact
Jira spelling, the version id, the released flag, and any start date, release
date, and description.

Matching notes:

- the spoken version may be shorter than the Jira name (`3.7` → `3.7.0`);
- hotfix naming varies (`2.7.4 - hotfix` in Jira vs `2.7.4_Hotfix` as a page
  title);
- more than one project can contain a similar version number, so confirm the
  project as well as the name;
- an unreleased version is a legitimate target. A release note may be prepared
  before the release is marked released in Jira. Report the released flag rather
  than treating unreleased as an error.

If nothing matches, stop with
`RELEASE NOTES BLOCKED — target release could not be resolved from Jira` and list
the versions Jira does contain.

## Release metadata to collect

Collect whatever Jira actually provides. Depending on instance and project, that
may include:

- Fix Version name and id
- version description
- release date and start date
- released and archived flags
- Jira project key and name
- the set of issues assigned to the version

Discover which of these exist rather than assuming. Record the ones that do not
so they can be reported as missing rather than guessed.

## Issue data to collect

For each release-member issue, collect what Jira exposes:

- issue key
- issue type
- summary
- description
- current status
- resolution
- priority
- labels
- components
- service line or product field, where the instance defines one
- assignee
- reporter
- parent, epic, or epic link
- linked issues
- acceptance criteria, where the project captures them and the template needs them
- release-related custom fields
- comments, only when necessary for classification or narrative content
- attachments and remote links, when the template expects supporting documents

Do not assume every Jira instance exposes every field. Discover the available
fields, use what exists, and record what does not.

Retrieve descriptions and comments selectively. A release with two hundred tickets
does not need every description read; retrieve them where the template requires
narrative content or where classification is genuinely ambiguous.

## Completeness

Retrieve the full membership, not the first page. Compare the number of issues
retrieved against the total the query reports and paginate until they agree.

Record the final count. Some templates publish a total-tickets field, and every
review summary should carry the count so a reviewer can spot a truncated result
set.

If pagination cannot be completed, report the shortfall explicitly rather than
presenting a partial release as complete.

## Membership must be evidence-backed

A ticket belongs in the release note when Jira places it in the release —
normally through the Fix Version.

A ticket must **not** appear because:

- it sounds related to the release theme;
- it was recently closed;
- it appears in a previous release note;
- it exists in the same Jira project;
- its code was recently changed;
- its epic contains other tickets that are in the release;
- a Pull Request referencing it was merged near the release date.

Never derive membership from Git commits, Pull Requests, Confluence text, branch
contents, or issue similarity.

Membership is type-blind. Every issue in the target Fix Version is release
content, whatever its issue type — `Story`, `Task`, `Bug`, `Epic`, `Sub-task`,
`Improvement`, or a type this guidance has never seen. The types that appear in
the historical release-note samples are an observation about those samples, not an
eligibility filter, and must never be treated as a whitelist.

## Ambiguous membership

Flag rather than decide silently. Common ambiguities:

| Situation | Handling |
| --- | --- |
| Issue carries several Fix Versions including the target | Include it, and note the multiple versions. |
| Issue is in the Fix Version but not in a Done status | Include it with its real status and flag the status as incompatible with publication. |
| Issue is a sub-task whose parent is also in the version | Both are release content. Present them per the template convention — a parent-with-children rollup is acceptable — but the sub-task stays visible and stays in the ticket count. State the convention applied. |
| Issue is an Epic whose children are listed individually | All are release content. Present per the template convention without double-counting, and keep the Epic visible rather than omitting it. |
| Issue has an unfamiliar or newly introduced issue type | Include it. Place it using the best available evidence and flag the placement for reviewer confirmation. Never drop it for being unfamiliar. |
| Issue was clearly delivered but has no Fix Version | Do not include it on that basis. Report it as a candidate the user can confirm. |
| Fix Version contains a release-management or ticket-tracking task | It is release content. Present it per the convention the recent pages show and state the placement; do not silently drop it. |

Where the user directs an inclusion or exclusion that Jira does not support,
apply the instruction and record that it rests on the user's instruction rather
than Jira evidence.

## The stale-page problem

A Fix Version keeps changing after its release note is published. Tickets are
added, statuses move, summaries are edited.

This means a previously published release note and the current Jira Fix Version
routinely disagree, and the Jira state is the current evidence. When preparing or
updating a release note:

- derive the ticket list from Jira at the time of preparation;
- never reconcile against the published page by dropping tickets Jira now
  includes;
- when the difference is material — a page lists eighteen tickets and Jira now
  returns nineteen — report the delta in the review summary.

```text
Jira Fix Version = current authoritative scope
existing Confluence page = previously published state
```

The delta is never an input to membership: do not compare the two lists to decide
what belongs in the release. It is a publication-safety signal. Require human
confirmation of the delta before modifying an already-published page, and never
modify Jira to make the two agree.

## Discrepancies between Jira and Confluence

Report, do not resolve. Typical cases:

- Jira's release date differs from the date on an existing release-note page;
- Jira's version description differs from the published release description;
- Jira's ticket set differs from the published ticket list;
- a ticket's current Jira status differs from the status published earlier.

State both values and their sources, and let the human decide:

```text
Discrepancy — Release Date
  Jira (Fix Version 3.7.0) releaseDate: 2025-07-17
  Existing Confluence page 3.7.0:       2026-05-18

Not resolved. Which Release Date should appear in the release note?
```

For a release date this is a blocking question, not a footnote. Surface both
values with their sources, ask which should appear, wait for the answer, and use
the confirmed value. There is no precedence rule between them: do not invent one,
do not pick the more plausible value, do not average or reinterpret, and never
substitute a date from an unrelated historical release.

Where no conflicting value exists, the Jira version `releaseDate` is the
Jira-provided release date and may be used, with its provenance stated.

Do not silently pick the more plausible value for any other conflicting field
either, and do not edit Jira to make the sources agree.

## Jira is read-only

The skill must never:

- change a Fix Version or version metadata;
- transition, close, or reopen issues;
- edit summaries or descriptions;
- add or edit comments;
- change statuses, resolutions, priorities, or release dates;
- create, delete, or link issues;
- assign or reassign issues.

If Jira data appears incorrect, report the discrepancy. Repairing Jira is a
separate human decision and is not this skill's responsibility.
