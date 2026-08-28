# Example B — FLW release note draft

**Fictional.** Project key `DEMOAPP`, version `7.3`, and every ticket and person
below are invented for illustration. They do not describe any real FLW release,
ticket, person, or schedule.

This example shows product detection changing the template, and therefore the
whole document shape — not just its cover fields.

## Invocation

```text
Prepare FLW release notes for version 7.3
```

## Product detection

```text
Signal 1: the invocation names FLW.
Signal 2: version 7.3 resolves in the DEMOAPP project, the mobile app project,
          not the web and API project.
Conclusion: FLW / mobile release family.
Consequence: use the FLW release-note convention, not the Web and API convention.
```

## What the skill did first

```text
Resolved Jira version
  Project: DEMOAPP
  Version name: 7.3
  Version id: 70300
  Released: true
  Start date: 2026-04-06
  Release date: 2026-07-10
  Description: Supervisor verification queue; sync and localization fixes

Retrieved release membership
  JQL: project = DEMOAPP AND fixVersion = "7.3"
  Total reported: 12
  Total retrieved: 12

Template discovery
  Read the live Release Notes hierarchy and the FLW App releases area.
  Inspected: 7.2 (newest, Dr Mithun James), 7.1, 7.0.
  Selected: 7.2 — newest applicable FLW convention.
  Noted: the FLW convention groups a "Fixed Points" section by priority band,
  which differs structurally from the Web and API single-table layout. The Web
  and API format was NOT applied.
```

## Draft (rendered in the selected FLW template)

### Release Details

|  |  |
| --- | --- |
| **Project Name:** | FLW Mobile App |
| **Version** | 7.3 |
| **Description** | Supervisor verification queue; sync and localization fixes |
| **Start Date:** | 2026-04-06 |
| **Planned Release Date** | **MISSING — not established from Jira** |
| **Actual Release Date** | 2026-07-10 |
| **Total Tickets** | 12 (11 Closed, 1 In QA) |

### Revision History

| **Version (x.y)** | **Date of Revision** | **Description of Change** | **Reason for Change** | **Affected Sections** | **Approved By** |
| --- | --- | --- | --- | --- | --- |
| 7.3 | 2026-07-10 | Release notes generated from Jira | Initial release notes creation | All | *pending* |

### Release Description

Release 7.3 of the FLW Mobile App adds a supervisor verification queue, allowing
supervisors to review and act on submitted activity records with a monthly view
and per-record approval. The release also resolves offline sync failures after
app upgrade, restores missing Hindi labels in the household module, and corrects
several form-validation defects in the maternal health and immunization flows.

### Fixed Points

#### Blocker – Critical Production Fixes

| **Key** | **Summary** | **Assignee** | **Status** |
| --- | --- | --- | --- |
| DEMOAPP-812 | Sync fails silently after upgrading from 7.1 to 7.2 | Fictional Assignee A | Closed |
| DEMOAPP-814 | App closes when opening the household list on low-memory devices | Fictional Assignee B | Closed |

#### Highest Priority – Critical Fixes

| **Key** | **Summary** | **Assignee** | **Status** |
| --- | --- | --- | --- |
| DEMOAPP-820 | Submitted records not appearing in the supervisor queue | Fictional Assignee A | Closed |
| DEMOAPP-821 | Login fails in offline mode after a password change | Fictional Assignee C | Closed |

#### High Priority – Features & Enhancements

| **Key** | **Summary** | **Type** | **Assignee** | **Status** |
| --- | --- | --- | --- | --- |
| DEMOAPP-780 | Supervisor Verification Queue | Epic | Fictional Assignee B | Closed |
| DEMOAPP-781 | Monthly overview for supervisors | Story | Fictional Assignee B | Closed |
| DEMOAPP-782 | Per-record approve and return-for-correction actions | Story | Fictional Assignee B | Closed |
| DEMOAPP-790 | Retain the selected month when navigating back to the queue | Task | Fictional Assignee A | Closed |

#### High Priority – Bug Fixes

| **Key** | **Summary** | **Assignee** | **Status** |
| --- | --- | --- | --- |
| DEMOAPP-830 | Hindi labels missing in the household member form | Fictional Assignee A | Closed |
| DEMOAPP-831 | Immunization due date not recalculated after editing the birth date | Fictional Assignee C | Closed |
| DEMOAPP-832 | Validation error persists after the mandatory field is filled | Fictional Assignee A | Closed |

#### Medium Priority – Bug Fixes

| **Key** | **Summary** | **Assignee** | **Status** |
| --- | --- | --- | --- |
| DEMOAPP-840 | Sort order not retained on the beneficiary list | Fictional Assignee C | In QA |

### Limitations/Known Bugs

No known issues identified from the available Jira release evidence.

### Supporting Documents

|  |  |  |  |
| --- | --- | --- | --- |
| **Prepared by/ Date:****E-mail ID:** | *pending* | **Approved by/ Date:****E-mail ID:** | *pending* |

## Review summary

```text
Release Notes Status: Draft — Pending Human Confirmation
Confluence Publication Status: Not Published

Target Version: 7.3
Target Product / Release Family: FLW Mobile App
Jira Fix Version: 7.3 (id 70300, project DEMOAPP)
Jira Release Date: 2026-07-10
Template Source: FLW 7.2 — newest applicable FLW convention
Included Jira Ticket Count: 12 retrieved, 12 rendered
Missing Required Metadata:
  - Planned Release Date
  - Revision History "Approved By"
  - Supporting Documents "Prepared by" and "Approved by"
Flagged Discrepancies:
  - DEMOAPP-840 is in the Fix Version but its current status is "In QA".
    Status rendered verbatim and reflected in the Total Tickets breakdown.
  - Priority band placement for DEMOAPP-790 rests on its Jira priority (High)
    and its Task type; no epic link is set.
Publication Target (proposed):
  Space AMRIT → Release Notes → FLW App releases → page titled "7.3"
```

## What the skill did not do

- It did not apply the Web and API single-table layout to an FLW release.
- It did not invent `Planned Release Date` from the start date, the actual release
  date, or the previous release's planned date.
- It did not fill the Prepared-by and Approved-by contact cells with the names
  that appear on FLW 7.2.
- It did not carry 7.2's limitations forward.
- It did not write to Confluence.
- It did not modify Jira.
