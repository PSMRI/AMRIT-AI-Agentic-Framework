# prepare-release-notes

`prepare-release-notes` prepares evidence-backed AMRIT release notes. It derives
the **format** from the latest applicable Confluence release-note pages and the
**content** from Jira, presents the draft for human confirmation, and publishes to
Confluence only after explicit authorization.

**Jira is read-only throughout.** The skill writes only to Confluence, and only
after the user has both confirmed the draft and explicitly requested publication.

## Purpose

Produce a release note whose structure matches the current organizational
convention and whose every factual claim traces to current Jira evidence for the
target release.

## The two-source rule

```text
Confluence
    ↓
Release-note TEMPLATE / FORMAT

Jira
    ↓
Actual RELEASE CONTENT / RELEASE DATA
```

Historical release notes answer *how should this be structured and presented?*
Jira answers *what is actually in this release?*

A previous release note shows where a field belongs. It never proves the new
release has the same value.

## Invocation

```text
/prepare-release-notes 3.8.2
```

```text
Prepare release notes for AMRIT 3.8.2
```

```text
Prepare FLW release notes for version 2.10
```

If no version is supplied, the skill asks for one. It does not guess a version
from recent activity.

## Execution architecture

```text
target release
→ Jira version/Fix Version
→ Jira release tickets/details
→ latest applicable Mithun James template
→ classify Jira content
→ generate release-note draft
→ human confirmation
→ explicit publish request
→ Confluence create/update
→ read-back verification
```

## Template selection

```text
Newest applicable Mithun James release note
        ↓
Other recent Mithun James release notes
        ↓
Older AMRIT release notes only as fallback/reference
```

**Recency means page recency, not the highest version number.** A page for a
higher version can be older than a page for a lower version, because releases are
documented retrospectively. The skill compares actual page creation and update
metadata, and inspects the recent pages the team named — including 3.7, 3.8.0, and
3.8.1 — before choosing.

The old contact-heavy standing template page and older release notes are not used
as the primary schema when newer Mithun James pages exist.

## Product awareness

One skill, two conventions — selected from the live hierarchy, not hardcoded:

| Release family | Confluence area | Convention |
| --- | --- | --- |
| AMRIT Web and API | the Web and API area beneath `Release Notes` | one combined ticket table plus a separate security section |
| FLW App | `FLW App releases` | a `Fixed Points` section grouped by priority band |

The FLW convention differs structurally, not cosmetically. The skill does not force
the Web/API format onto an FLW release.

The mHWC mobile-app release area was observed to hold no release notes, so no mHWC
template currently exists to derive. For an mHWC request the skill states that no
precedent was found, asks which format to use, does not substitute the Web/API or
FLW convention, and does not publish until the format is confirmed. That absence is
an observation about current Confluence content, not an organizational policy.

## What comes from Jira

| Category | Source |
| --- | --- |
| Release membership | Jira Fix Version |
| Bugs fixed | Jira issue type, key, summary, status, resolution |
| Features and enhancements | Jira issue type, epic, labels, components, description |
| Ticket keys and summaries | Jira, verbatim |
| Current statuses | Jira, verbatim |
| Version, release date, project, line of business | Jira release and issue metadata |
| Release description | synthesized from the included Jira tickets |

Release membership is never derived from Git commits, Pull Requests, Confluence
text, branch contents, or issue similarity, and it is never decided by comparing
the Jira issue set against a published Confluence ticket list — the Fix Version is
the current authoritative scope, an existing page is the previously published
state. A delta between them is reported and requires human confirmation before an
already-published page is modified.

Membership is also type-blind: every issue in the target Fix Version is release
content whatever its issue type. `Story`, `Task`, and `Bug` are what the
historical samples happen to contain, not a whitelist, so an `Epic`, `Sub-task`,
`Improvement`, or unfamiliar type is placed and flagged — never silently dropped.

Where an issue carries an explicit Jira Service Line, that value is used as-is and
is never overridden by historical Confluence categorization. Where it must be
inferred from labels or context, the value is marked as inferred and listed for
reviewer confirmation.

The Jira version `releaseDate` is the Jira-provided release date. Where another
relevant current source gives a different date, both values and their sources are
surfaced and the user is asked which should appear; the skill waits for that
confirmation rather than applying a precedence rule of its own.

## What is never copied forward

Bugs, ticket keys, summaries, enhancements, features, security fixes, limitations,
known issues, release dates, versions, statuses, line of business, released-by
information, Product Owner, Project Manager, Quality Coordinator, email IDs,
configuration changes, deployment details, and supporting-document links.

A field with no current evidence is reported as missing:

```text
Required template field not established from Jira/current evidence:
- Released By
```

Never a name, never an inferred email address, never the previous release's owner.

## No source-code inspection

Unlike `perform-root-cause-analysis`, this skill requires no source-code
inspection, and does not use DeepWiki or Graphify in normal operation. The release
note is a release-management artifact and Jira is the established source of truth
for release contents.

Source code may be consulted only when the user explicitly asks for technical
clarification and Jira evidence remains ambiguous. It never overrides Jira release
membership.

## Human confirmation and publication

The draft is always presented for review first:

```text
Release Notes Status: Draft — Pending Human Confirmation
Confluence Publication Status: Not Published
```

Publication requires both confirmation of the specific draft and an explicit
request to publish:

| Message | Publishes? |
| --- | --- |
| `Looks good.` | No |
| `Release notes confirmed.` | No — content confirmed, publication not requested |
| `Release notes confirmed. Publish them to Confluence.` | Yes |

Before writing, the skill shows a publication plan and checks whether a page for
the target version already exists. An existing published page is never overwritten
automatically. After writing, the page is read back and verified — title, parent,
version, ticket tables, required sections, and the absence of leaked old-release
values.

## Relationship to existing skills

```text
implement-jira-ticket → create-development-pr
        ↓
execute-qa-validation
        ↓
release contents completed and assigned a Jira Fix Version
        ↓
prepare-release-notes
```

The skill consumes completed lifecycle work. It does not replace
`implement-jira-ticket`, `create-development-pr`, `execute-qa-validation`,
`test-jira-ticket`, or `perform-root-cause-analysis`, and requires none of them at
runtime.

## Boundaries

The skill never:

- modifies Jira — no Fix Version changes, transitions, edits, comments, or new
  tickets;
- modifies product source code, branches, commits, pushes, or Pull Requests;
- deploys, tags a release, or executes any release procedure;
- writes to Confluence before confirmation and explicit authorization;
- claims publication success without read-back verification.

It documents the release. It does not perform the release.

## Required capabilities

Read-only Jira and Confluence access. Confluence write access is needed only for
authorized publication. No repository access, command execution, DeepWiki, or
Graphify capability is required.

## Completion status semantics

- **Release Notes Status: Draft — Pending Human Confirmation**
- **Release Notes Status: Confirmed — Published to Confluence**
- **RELEASE NOTES BLOCKED — target release could not be resolved from Jira**
- **RELEASE NOTES BLOCKED — current Confluence template could not be inspected**

## Examples

See [examples/](examples/) for three fictional illustrations: a Web/API release
draft, an FLW release draft showing the different template, and a missing-metadata
case. All ticket keys, versions, and people in the examples are invented.

## Use and distribution

Invoke `/prepare-release-notes` from the repository root using a supported coding
agent. Configure local MCP credentials only where the selected client requires
them; never commit real tokens.

For a packaged installation, download `prepare-release-notes.zip` from the latest
GitHub Release. See the [distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
