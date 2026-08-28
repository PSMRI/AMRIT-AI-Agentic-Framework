---
name: prepare-release-notes
description: Prepare AMRIT release notes by deriving the current format from the latest applicable Mithun James-maintained Confluence release notes and populating release scope, bugs, enhancements, ticket details, statuses and other release metadata from Jira; present the draft for human confirmation and publish it to the correct Confluence hierarchy only after explicit authorization.
metadata:
  stage: Stage 12 — Release Documentation
  category: Release documentation and release-note preparation
  primary_role: Release Manager / Product Owner / Technical Lead
  skill_type: Standalone
  knowledge_sources:
    - Jira
    - Confluence
  supported_inputs:
    - Target release or version number
    - Jira Fix Version
    - Product or release family (AMRIT Web and API, FLW App)
    - User-supplied non-Jira release metadata
  primary_input: Target release version
  primary_output: Evidence-backed release-note draft, pending human confirmation
  upstream_skills:
    - execute-qa-validation
    - create-development-pr
  downstream_skills:
    - create-brd
---

# Prepare Release Notes

Prepare AMRIT release notes for a target release. Derive the **format** from the
latest applicable Confluence release-note pages. Derive the **content** from
Jira. Present the draft for human confirmation, and publish to Confluence only
after explicit authorization.

## Hard rules

These rules govern every invocation and override any convenience found in an
existing page.

> **Jira is the source of truth for the contents of the target release.**

> **Recent Mithun James-authored/maintained Confluence release notes are
> templates for structure and presentation, not evidence that their values apply
> to the new release.**

> **The skill must inspect the latest applicable release-note pages, including
> recent versions such as 3.7, 3.8.0 and 3.8.1 where applicable, before choosing
> a template.**

> **Bugs fixed, enhancements, features, statuses, ticket keys and summaries must
> be obtained from current Jira evidence for the target release.**

> **Never copy people, email IDs, bugs, dates, configuration, limitations,
> tickets or release metadata from a historical release unless current
> authoritative evidence independently establishes the same value.**

> **Jira is read-only.**

> **Confluence publication occurs only after human confirmation and explicit
> publication authorization.**

## The two-source rule

```text
Confluence
    ↓
Release-note TEMPLATE / FORMAT

Jira
    ↓
Actual RELEASE CONTENT / RELEASE DATA
```

Historical release notes answer *how should this release note be structured and
presented?*

Jira answers *what is actually in this release?*

A previous release can show where a field belongs. It can never prove the new
release has the same value. Never treat a previous Confluence release note as
the authoritative source for the contents of a new release.

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

If no version is supplied, ask for the target release before beginning. Do not
guess a version from recent activity.

## Discover available capabilities

Use the connected tools' logical Jira issue-read, Jira project and version-read,
and Confluence search, page-read, and page-children-read capabilities. Tool names
vary by host: discover equivalent read-only operations rather than assuming
names. Confluence write capability is used only for authorized publication.

Do not assume every Jira instance exposes every field. Discover the fields that
actually exist and use them; record the ones that do not.

If Confluence is unavailable, the skill cannot establish the current template and
must report that rather than inventing a format. If Jira is unavailable, the
skill cannot establish release content and must report that rather than reusing a
previous release's contents.

## Workflow

Read and follow
[references/release-notes-workflow.md](references/release-notes-workflow.md)
for the full sequence.

```text
User provides release/version
        ↓
Resolve target Jira version / Fix Version
        ↓
Read Jira release metadata
        ↓
Retrieve all release-member Jira issues
        ↓
Inspect issue type/status/resolution/details
        ↓
Classify bugs/features/enhancements/etc.
        ↓
Inspect latest applicable Mithun James
Confluence release notes
        ↓
Select current template
        ↓
Populate template using Jira evidence
        ↓
Validate completeness and traceability
        ↓
Produce release-note draft
        ↓
Human review / confirmation
        ↓
Explicit publication request
        ↓
Create/update correct Confluence page
        ↓
Read back and verify
```

## Template discovery and selection

Read and follow
[references/template-discovery-guidelines.md](references/template-discovery-guidelines.md).

The AMRIT release-note parent is:

```text
https://pmp.piramalswasthya.org/confluence/spaces/AMRIT/pages/46563852/Release+Notes
```

Inspect the actual current hierarchy through authenticated Confluence access. Do
not rely on public web indexing, and do not invent page IDs.

Locate and inspect the recent release notes the team named, at minimum:

```text
3.7
3.8.0
3.8.1
```

Precedence:

```text
Newest applicable Mithun James release note
        ↓
Other recent Mithun James release notes
        ↓
Older AMRIT release notes only as fallback/reference
```

**Recency means page authoring recency, not the highest version number.** A
higher version number can belong to an older page. Compare the actual page
creation and update metadata, not the title.

Do not use older release notes such as 3.6.1, or the old contact-heavy
`AMRIT Release Notes Template` page, as the primary schema when newer Mithun
James pages exist.

Record internally which page was selected as the template. Do not publish that
internal selection note into the final Confluence page unless the current
convention calls for it.

## Product awareness

This is one skill, not separate Web and FLW skills. Template selection considers:

1. target product/application;
2. release family;
3. most recent applicable release note;
4. author/maintainer convention;
5. current Confluence hierarchy.

For a normal AMRIT Web/API release, use the newest applicable AMRIT Web and API
release-note pattern.

For FLW/mobile releases, inspect the dedicated FLW hierarchy:

```text
https://pmp.piramalswasthya.org/confluence/spaces/AMRIT/pages/96043199/FLW+App+releases
```

Use the latest applicable FLW structure. Do not force the Web/API format onto FLW
when the current FLW convention differs.

If the release belongs to a product family with no existing release notes, say so
and ask which convention to follow rather than assuming one. The mHWC mobile-app
release area was observed to hold no release notes, so there is currently no mHWC
template to derive. For an mHWC request:

```text
→ state that no mHWC release-note precedent/template was found in Confluence
→ ask the user which template/format should be used
→ do not automatically substitute the AMRIT Web/API or FLW format
→ do not publish until the format is confirmed
```

Re-check the area at runtime; it may have been populated since. Report the absence
as an observation about current Confluence content, not as evidence of an
organizational policy about mHWC releases.

## Template drift

Expect historical templates to differ. Use the **latest applicable convention**,
not the union of every historical field. Do not merge every field that ever
appeared into one giant format, and do not reintroduce a field simply because an
older template used it.

If one newer page is clearly a special-case release, derive the stable structure
from the newest comparable examples rather than blindly copying the anomaly.

## Jira release data

Read and follow
[references/jira-release-data-guidelines.md](references/jira-release-data-guidelines.md).

Resolve the target release to a real Jira version or Fix Version, then retrieve
the issues Jira actually assigns to it.

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

Release membership must be evidence-backed. A ticket must not appear because it
sounds related, was recently closed, appears in a previous release note, exists
in the same Jira project, or had recent code changes. If a ticket's membership is
ambiguous, flag it instead of silently including it.

Do not invent release membership from Git commits, Pull Requests, Confluence
text, or issue similarity.

The target Fix Version alone defines membership. Never compare the Jira issue set
against a historical or published Confluence ticket list in order to decide what
belongs in the release:

```text
Jira Fix Version = current authoritative scope
existing Confluence page = previously published state
```

A difference between the two is a publication-safety signal, not a membership
question. Report the delta and require human confirmation before modifying an
already-published page. Never modify Jira to reconcile the difference.

## Release content classification

Read and follow
[references/release-content-classification.md](references/release-content-classification.md).

Classify using actual Jira evidence — issue type, parent or epic, labels,
components, service-line field, release metadata, and issue description. Do not
classify an item as an enhancement or a bug merely because it sounds like one.

**Issue type governs presentation, never eligibility.**

```text
If an issue belongs to the target Jira Fix Version,
it must be considered release content regardless of issue type.
```

`Story`, `Task`, and `Bug` are the types observed in the historical release-note
samples. That is an observation, not a whitelist, and it must never become one.
Never silently drop an `Epic`, `Sub-task`, `Improvement`, or any other or
unfamiliar issue type because the historical samples did not contain it. Place an
unrecognized type using the best available evidence, state where it was placed,
and flag it for reviewer confirmation. A presentation-level rollup is acceptable
where the template calls for one; rolling up is not dropping — the issue stays
visible and stays in the ticket count.

For Service Line:

```text
explicit Jira Service Line
→ use it

Service Line unavailable and inferred from labels/components/context
→ mark the value as inferred and requiring reviewer confirmation
```

Never override an explicit Jira Service Line using a historical Confluence
categorization.

For bugs fixed, which the team specifically requires from Jira:

1. identify the Jira issues belonging to the release;
2. identify which of those Jira classifies as bugs or defects according to the
   actual issue type and project conventions;
3. retrieve their real keys;
4. retrieve their real summaries;
5. retrieve their current statuses and resolutions;
6. populate the release note using the selected template's bug or fixed-point
   format.

Minor cleanup for readability is acceptable. Do not rewrite a Jira issue into a
materially different statement, and never fabricate a bug fix.

Follow the category naming found in the newest applicable template. Do not invent
categories before inspecting the templates.

## Ticket-table fidelity

Populate every ticket table from live Jira data using the columns the selected
template actually uses.

Use the current Jira status verbatim. If Jira says `Closed`, use `Closed`. If it
says something else, do not silently convert it because a historical example
showed `Closed`. If a current status appears incompatible with release
publication, flag it in the draft review summary. Do not modify Jira.

## Release details from Jira

Retrieve release metadata from Jira wherever Jira is authoritative — version,
project or product, release date, status, Fix Version, line of business or
component, release scope, and included tickets.

Do not copy these values from 3.7, 3.8.0, 3.8.1, or any other historical page.
Those pages supply the field layout, not the values.

The Jira version `releaseDate` is the Jira-provided release date and may be used
as such when no other current source contradicts it. State its provenance either
way.

Where another relevant current or existing source gives a different release date,
do not decide which is correct:

```text
Jira releaseDate = X
other relevant release-date value = Y
X != Y

→ surface the discrepancy
→ show both values and their sources
→ ask the user which Release Date should appear
→ wait for confirmation
→ use the confirmed value
```

There is no precedence rule between conflicting release dates. Do not invent one,
and never take a release date from an unrelated historical release. Apply the same
report-and-confirm handling to a disputed release scope.

## Missing metadata

Some template fields may not exist in Jira — for example released-by, product
owner, quality coordinator, project manager, email IDs, deployment method, or
specific supporting-document links.

If current Jira data does not establish such a value:

- do not copy it from an earlier release;
- do not infer an email address;
- do not infer a person because they owned the previous release.

Classify it as missing and report it during draft review:

```text
Required template field not established from Jira/current evidence:
- Released By
```

If the field is genuinely required for publication, request and accept
human-provided confirmation before publishing. If newer templates no longer
require the field, do not reintroduce it.

This resolves the older Product Owner and email-ID discrepancy explicitly:

```text
Newer template omits old contact fields
→ do not add them automatically.

Newer template requires a contact field
→ populate only from current authoritative evidence.

Current value unavailable
→ report it as missing.

Never copy a person's contact from an earlier release.
```

## Release description

If the selected template contains a Release Description, generate it from the
actual Jira release content. It may summarize major functionality introduced,
important enhancements, defects fixed, and affected service lines.

The description may be synthesized prose, but every factual claim must be
supported by the included Jira release scope. Do not invent business impact or
functionality absent from Jira.

## Known issues, limitations, configuration, and supporting documents

Include Known Issues or Limitations only when supported by current evidence: Jira
issues, unresolved issues explicitly associated with the release,
release-specific Jira metadata or comments, or explicit user-provided release
information. Never copy limitations from a previous release forward.

Do not claim `No known issues` unless the evidence reasonably establishes that.
Prefer:

```text
No known issues identified from the available Jira release evidence.
```

For configuration or deployment sections, obtain current values from Jira or
other explicitly authoritative current evidence. Do not copy deployment or
configuration instructions from an older release to fill the template. When
evidence is insufficient, flag the section for human completion. This skill is
not a deployment skill.

Supporting documents may include BRDs, technical designs, Confluence pages, Pull
Requests, test evidence, and other approved artifacts actually linked from the
release's Jira tickets. Preserve real links. Never fabricate a supporting-document
URL.

## Source code is not a release-membership source

Unlike `perform-root-cause-analysis`, this skill requires **no** source-code
inspection. The release note is a release-management and documentation artifact,
and Jira is the established source of truth for release contents.

Do not do:

```text
Git diff
→ guess included features
→ write release notes
```

Do not do:

```text
current source code
→ infer bugs fixed
→ write release notes
```

Source code may be consulted only when the user explicitly asks for additional
technical clarification and Jira evidence remains ambiguous. It must never
override Jira release membership.

DeepWiki and Graphify are not primary sources and are not required. Use them only
if the selected template requires architectural context, a Jira description
references a technical component that needs clarification, or the user explicitly
requests deeper technical explanation. Even then they must not determine whether
an issue belongs in the release.

## Draft output

Read and follow
[references/release-notes-template-guidelines.md](references/release-notes-template-guidelines.md).

The exact published structure comes from the selected current template.
Internally, the draft process tracks at least:

```text
Target Version
Target Product / Release Family
Jira Fix Version
Jira Release Date
Template Source
Included Jira Issues
Features / Enhancements
Bug / Fixed Points
Known Issues / Limitations
Missing Required Metadata
Publication Target
```

Then render the release note according to the selected Confluence template.

## Traceability quality gate

Before presenting the draft, verify internally:

```text
[ ] Target Jira version/Fix Version resolved
[ ] Every included Jira ticket belongs to the target release
[ ] Ticket keys are real
[ ] Summaries come from Jira
[ ] Current statuses come from Jira
[ ] Bug/fix classification is supported by Jira
[ ] Feature/enhancement classification is supported by Jira
[ ] Release date/version are current
[ ] Latest applicable Mithun James template was inspected
[ ] 3.7 / 3.8.0 / 3.8.1 were considered where applicable
[ ] FLW-specific template considered for FLW releases
[ ] No people/email IDs copied from an older release
[ ] No old bug list copied forward
[ ] No old known issues copied forward
[ ] No old configuration copied forward
[ ] Missing required fields are identified explicitly
[ ] Jira has not been modified
[ ] Confluence has not yet been modified
```

## Human review gate

Release notes are always produced as a draft first. After generating the draft,
stop with:

```text
Release Notes Status: Draft — Pending Human Confirmation
Confluence Publication Status: Not Published
```

The user may correct classification, provide missing release metadata, add or
remove a ticket when Jira evidence is corrected, adjust wording, clarify a
service line, or provide required non-Jira metadata. Apply revisions to the
draft.

Do not publish merely because the draft was generated successfully.

## Confluence publication

Read and follow
[references/confluence-publishing-guidelines.md](references/confluence-publishing-guidelines.md).

Publication requires two conditions:

1. The user has confirmed or finalized the specific release-note draft.
2. The user has explicitly requested publication to Confluence.

- `Looks good.` — does not authorize publication.
- `Release notes confirmed.` — confirms content but does not request publication.
- `Release notes confirmed. Publish them to Confluence.` — authorizes publication.

A single clear statement may satisfy both conditions. Do not ask redundant
confirmation once explicit authorization exists.

Determine the publication target dynamically from Confluence. Normal AMRIT
releases belong under the appropriate hierarchy beneath `Release Notes`; FLW
releases belong under `FLW App releases`. Do not hardcode an invented child page
ID.

Before mutation, establish and show:

```text
Action: Create | Update
Space: AMRIT
Parent:
Target Version:
Target Page Title:
Template Used:
Jira Fix Version:
Included Jira Ticket Count:
Missing Required Metadata:
```

Check whether a release-note page for the target version already exists. If none
exists, create it after authorization. If a draft page exists, read it first and
do not silently overwrite human-authored content. If a published or final page
exists, do not overwrite it automatically — report it and require explicit update
intent.

After the write, read the page back and verify the title, parent, version, Jira
issue tables, and required sections, and confirm that no old-release values
leaked into the page. Report the actual page reference or URL. Do not claim
publication success without read-back verification.

## Read-only and scope boundaries

Jira is read-only at all times. The skill must never change a Fix Version,
transition or close issues, edit summaries or descriptions, add comments, change
statuses or release dates, or create tickets. If Jira data appears incorrect,
report the discrepancy; do not repair Jira from this skill.

The skill has no Git or deployment responsibility. It must not modify product
source code, create branches, commit, push, create Pull Requests, deploy, update
production, tag releases, or execute release procedures.

It documents the release. It does not perform the release.

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

Release-note preparation consumes completed work from the development, QA, and
release lifecycle. It does not replace `implement-jira-ticket`,
`create-development-pr`, `execute-qa-validation`, `test-jira-ticket`, or
`perform-root-cause-analysis`. The skill is independently executable and requires
none of them at runtime.

## Required capabilities

Read-only Jira and Confluence access. Confluence write access is needed only for
authorized publication. No repository access, command execution, DeepWiki, or
Graphify capability is required.

## Completion status semantics

Every invocation ends with one of:

- **Release Notes Status: Draft — Pending Human Confirmation**
- **Release Notes Status: Confirmed — Published to Confluence** (only after
  authorization and verified publication)
- **RELEASE NOTES BLOCKED — target release could not be resolved from Jira**
- **RELEASE NOTES BLOCKED — current Confluence template could not be inspected**

Release notes are never automatically complete, approved, or published.
