# Release-Notes Template Guidelines

How to render the draft once the template is selected and the Jira evidence is
collected.

The authoritative structure is always the template selected at runtime from live
Confluence. The shapes recorded here are reference material describing conventions
observed in the AMRIT space; they are not a substitute for inspecting the real
pages, and they will drift.

## Internal draft state

Track at least this, regardless of which template was selected:

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

This state is what the review summary reports. It is not the published document —
the published document follows the selected template.

## Field provenance

Every rendered field has exactly one provenance:

| Provenance | Meaning |
| --- | --- |
| Jira | Derived from an explicit current Jira value for this release. |
| Inferred | Derived from Jira context — labels, components, product area — rather than an explicit Jira field. Marked as inferred and listed for reviewer confirmation. |
| User-provided | Supplied explicitly by the user for this release. |
| Missing | Not established. Reported, not filled. |

There is no "carried over from the previous release" provenance. If a value cannot
be established from Jira or the user, it is missing.

## Observed shape — AMRIT Web and API

A reference sketch of the convention seen in the recent Web and API pages. Verify
against the real pages before use.

```text
Release Details
---------------
| Field | Details |
| Version | <Jira version name> |
| Project | <product / release family> |
| Release Date | <Jira release date> |
| Released By | <current evidence, else Missing> |
| Status | <release status from current evidence> |
| Line of Business | <service lines established by the included tickets> |

Revision History
----------------
| S.No | Author | Description | Date |

Release Description
-------------------
<prose synthesized from the included Jira tickets>

New Features/Enhancements
-------------------------
| S.No | Description | Work Item Type | Service Line | Status |

Security Fixes
--------------
| S.No | Description | Work Item Type | Service Line | Status |

Limitations
-----------

Release Methods
---------------

Configuration
-------------
### Hardware Requirements
### Software Requirements

Supporting Documents
--------------------
```

Notes on this convention as observed:

- one combined ticket table covers features, enhancements, and fixes; the
  work-item type column carries the distinction;
- the description cell embeds the ticket key with its summary, so the key stays
  visible inside the text rather than in its own column;
- security fixes are separated out;
- empty sections are stated rather than deleted.

## Observed shape — FLW App

A reference sketch of the convention seen in the recent FLW pages. Verify against
the real pages before use.

```text
Release Details
---------------
| **Project Name:** | <product> |
| **Version** | <Jira version name> |
| **Description** | <release theme from Jira version metadata> |
| **Start Date:** | <Jira version start date, when present> |
| **Planned Release Date** | <current evidence> |
| **Actual Release Date** | <Jira release date> |
| **Total Tickets** | <count retrieved from Jira> |

Revision History
----------------
| **Version (x.y)** | **Date of Revision** | **Description of Change** |
| **Reason for Change** | **Affected Sections** | **Approved By** |

Release Description
-------------------

Fixed Points
------------
### <Priority band> – <kind of work>
| **Key** | **Summary** | **Assignee** | **Status** |
...

Limitations/Known Bugs
----------------------

Supporting Documents
--------------------
```

Notes on this convention as observed:

- the grouping axis is **priority band**, then kind of work, which is structurally
  different from the Web and API single-table layout;
- ticket key and summary are separate columns;
- an assignee column is present;
- a `Type` column appears in bands that mix work-item types;
- a total-ticket count is a published field, so the Jira retrieval count matters
  directly.

Do not force either shape onto the other family.

## Rendering rules

- Reproduce the selected template's headings, field labels, column names, casing,
  and order. Field labels are part of the convention.
- Reproduce its emphasis conventions — where the recent pages bold table headers
  or field labels, do the same.
- Keep the section order stable.
- Preserve every real link exactly as Jira holds it.
- Where the template numbers rows, number them consistently from one.
- Where the template has an empty-section phrase, use that phrase — unless it
  would assert certainty the evidence does not support, in which case use the
  honest form and flag it.

## Page title and parent

Follow the observed convention. In the AMRIT space the recent pages are titled
with the bare version number and filed under the product area — no prefix, no
suffix, no date.

Confirm the convention at runtime rather than applying this from memory, and
confirm the parent area matches the product family.

## Missing required metadata

Render the field with an explicit missing marker rather than a plausible
placeholder, and list it in the review summary:

```text
Required template field not established from Jira/current evidence:
- Released By
```

Do not write a name, an email address, or a department into the field to make the
document look finished. A visibly missing field prompts a human to supply the
right value; a plausible wrong value does not.

## Configuration and deployment sections

Populate only from Jira or other explicitly authoritative current evidence — for
example a Jira ticket that establishes a new dependency or a required credential.

Where the evidence is insufficient, flag the section for human completion. Do not
copy a hardware and software stack forward from an older page. This skill does not
own deployment procedure.

## Supporting documents

Include artifacts actually linked from the release's Jira tickets — BRDs,
technical designs, Confluence pages, Pull Requests, test evidence, and other
approved artifacts — where the template expects supporting documentation.

Preserve the real links. Never fabricate a URL, and never reuse a supporting-document
link from a previous release without current evidence that it applies.

## Review summary

Present after the rendered document:

```text
Release Notes Status: Draft — Pending Human Confirmation
Confluence Publication Status: Not Published

Target Version:
Target Product / Release Family:
Jira Fix Version:
Jira Release Date:
Template Source:
Included Jira Ticket Count:
Missing Required Metadata:
Flagged Discrepancies:
Publication Target (proposed):
```

Flagged discrepancies include Jira-versus-Confluence conflicts, tickets whose
current status is incompatible with publication, ambiguous membership, ambiguous
classification, and any template section that could not be filled from evidence.
