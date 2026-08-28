# Example A — AMRIT Web/API release note draft

**Fictional.** Project key `DEMO`, version `9.4.0`, and every ticket below are
invented for illustration. They do not describe any real AMRIT release, ticket,
person, or schedule.

## Invocation

```text
/prepare-release-notes 9.4.0
```

## What the skill did first

```text
Resolved Jira version
  Project: DEMO
  Version name: 9.4.0
  Version id: 90400
  Released: false
  Start date: 2026-06-01
  Release date: 2026-07-15
  Description: Referral workflow enhancements; inventory reporting fixes

Retrieved release membership
  JQL: project = DEMO AND fixVersion = "9.4.0"
  Total reported: 9
  Total retrieved: 9

Template discovery
  Read the live Release Notes hierarchy and the Web and API product area.
  Inspected: 9.3.1 (newest, Dr Mithun James), 9.3.0, 9.2.0.
  Also inspected the older standing template page for comparison only.
  Selected: 9.3.1 — newest applicable Web and API convention.
  Noted: 9.2.0 uses an older contact-heavy layout with Product Owner and
  Quality Coordinator email fields. Not carried forward.
```

## Draft (rendered in the selected template)

### Release Details

| Field | Details |
| --- | --- |
| Version | 9.4.0 |
| Project | AMRIT Web and API |
| Release Date | 2026-07-15 |
| Released By | **MISSING — not established from Jira** |
| Status | Unreleased in Jira |
| Line of Business | HWC, Inventory, Common |

### Revision History

| S.No | Author | Description | Date |
| --- | --- | --- | --- |
| 1 | *pending — see Missing Required Metadata* | Release notes generated from Jira | 2026-07-15 |

### Release Description

Version 9.4.0 introduces referral-workflow enhancements for HWC, including a
referral reason picker and referral status visibility on the beneficiary record.
The release also adds an inventory consumption report export and resolves four
defects across HWC, Inventory, and common platform areas, including a duplicate
referral submission and an inventory report download failure.

### New Features/Enhancements

| S.No | Description | Work Item Type | Service Line | Status |
| --- | --- | --- | --- | --- |
| 1 | [DEMO-1401] Referral reason picker on the HWC referral screen | Story | HWC | Closed |
| 2 | [DEMO-1402] Show referral status on the beneficiary record | Story | HWC | Closed |
| 3 | [DEMO-1410] Inventory consumption report export | Task | Inventory | Closed |
| 4 | [DEMO-1414] Retain facility selection across the referral flow | Task | HWC | Closed |
| 5 | [DEMO-1420] Duplicate referral submitted when the save button is pressed twice | Bug | HWC | Closed |
| 6 | [DEMO-1421] Inventory consumption report download fails for large date ranges | Bug | Inventory | Closed |
| 7 | [DEMO-1422] Referral reason not persisted when the form is reopened | Bug | HWC | Closed |
| 8 | [DEMO-1423] Facility dropdown not sorted alphabetically | Bug | Common (inferred) | In QA |
| 9 | [DEMO-1419] Add export column headings (sub-task of DEMO-1410) | Sub-task | Inventory | Closed |

### Security Fixes

No security fixes in this release.

### Limitations

No known issues identified from the available Jira release evidence.

### Release Methods

**Flagged for human completion — not established from Jira.**

### Configuration

#### Hardware Requirements

No additional hardware requirements established from the release evidence.

#### Software Requirements

No additional software requirements established from the release evidence.

### Supporting Documents

| Artifact | Link | Source ticket |
| --- | --- | --- |
| Referral workflow technical design | *(Confluence link as held on the ticket)* | DEMO-1401 |

## Review summary

```text
Release Notes Status: Draft — Pending Human Confirmation
Confluence Publication Status: Not Published

Target Version: 9.4.0
Target Product / Release Family: AMRIT Web and API
Jira Fix Version: 9.4.0 (id 90400, project DEMO)
Jira Release Date: 2026-07-15 (version not yet marked released)
Template Source: 9.3.1 — newest applicable Web and API convention
Included Jira Ticket Count: 9 retrieved, 9 rendered
Release Date Provenance: Jira version 9.4.0 releaseDate. No other current source
  gives a different release date, so no confirmation was required.
Missing Required Metadata:
  - Released By
  - Revision History author
Inferred Values Requiring Reviewer Confirmation:
  - DEMO-1423 Service Line "Common" — no explicit Jira Service Line on the issue;
    inferred from the absence of a module label. Every other row uses the
    explicit Jira Service Line field.
Flagged Discrepancies:
  - DEMO-1423 is in the Fix Version but its current Jira status is "In QA",
    which is incompatible with release publication. Status rendered verbatim.
  - DEMO-1419 is a Sub-task, a type the historical 9.3.1 sample does not contain.
    It is in the Fix Version, so it is release content and is rendered with its
    real type; its parent DEMO-1410 is also listed. Placement flagged for
    reviewer confirmation. It was not dropped for being an unobserved type.
  - Jira version 9.4.0 is not marked released. Status rendered as
    "Unreleased in Jira" rather than "Released".
Publication Target (proposed):
  Space AMRIT → Release Notes → AMRIT Web and API releases → page titled "9.4.0"
```

## What the skill did not do

- It did not write to Confluence. The draft is presented for review only.
- It did not copy `Released By`, a Product Owner, a Quality Coordinator, or any
  email address from 9.3.1 or 9.2.0.
- It did not reproduce the contact fields that the older 9.2.0 layout carried.
- It did not carry 9.3.1's limitations or configuration stack forward.
- It did not convert DEMO-1423's `In QA` status to `Closed` to match the pattern
  in the historical examples.
- It did not inspect source code or Git history to establish membership.
- It did not compare the 9.3.1 page's ticket list against the Jira Fix Version to
  decide what belongs in 9.4.0.
- It did not drop DEMO-1419 because `Sub-task` does not appear in the historical
  release-note samples.
- It did not modify Jira, including DEMO-1423's status.
