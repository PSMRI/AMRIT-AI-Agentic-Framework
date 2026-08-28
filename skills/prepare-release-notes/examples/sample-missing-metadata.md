# Example C — missing release metadata

**Fictional.** Project key `DEMO`, version `9.5.0`, and every ticket and person
below are invented for illustration.

This example isolates the behaviour the AMRIT team specifically asked for: a
template field that current evidence cannot establish is **reported as missing**,
never filled from the previous release.

## Invocation

```text
/prepare-release-notes 9.5.0
```

## The situation

The selected template requires `Released By`. Jira does not hold it.

The previous release note for 9.4.0 has it filled in, along with a Product Owner
name and two email addresses. Copying those values would produce a document that
looks complete and is unverified.

## Wrong behaviour

```text
Released By: Piramal Swasthya          ← copied from the 9.4.0 page
Product Owner / Email ID: <name> / <email>   ← copied from an older layout
Quality Coordinator / Email ID: <name>       ← copied from an older layout
```

Three separate faults:

1. `Released By` was asserted without current evidence.
2. Contact fields were reintroduced even though the current template dropped them.
3. Real people were attributed to a release they may have had no part in.

## Correct behaviour

```text
Release Details
| Field | Details |
| Version | 9.5.0 |
| Project | AMRIT Web and API |
| Release Date | 2026-08-28 |
| Released By | MISSING — not established from Jira |
| Status | Released |
| Line of Business | 104, ECD |
```

The contact fields are absent, because the selected current template does not
have them. They are not reintroduced.

## Reported to the user

```text
Release Notes Status: Draft — Pending Human Confirmation
Confluence Publication Status: Not Published

Required template field not established from Jira/current evidence:
- Released By

The 9.4.0 release-note page carries a value for this field. It was not copied:
a previous release cannot establish who released this one.

The older 9.2.0 layout additionally carried Product Owner, Project Manager, and
Quality Coordinator fields with email addresses. The current template (9.4.0,
newest applicable) no longer has those fields, so they were not reintroduced and
no contact details were carried over.

Please supply "Released By" for 9.5.0, or confirm publication without it.
```

## The three possible resolutions

| User response | Skill behaviour |
| --- | --- |
| `Released By is Piramal Swasthya.` | Populate the field, record provenance as user-provided, re-present the draft. |
| `Publish without it.` | Leave the field explicitly marked missing in the published page. Do not fill it. Record that the user accepted the gap. |
| `The old template is what we use — add the Product Owner fields back.` | Add the fields, because the user has decided the convention. Populate them only from what the user supplies; still do not copy the values from an earlier page. |

In every case the value comes from Jira or the user. It never comes from a
previous release note.

## Other fields this applies to

The same rule governs, whenever the current template has the field and current
evidence does not establish the value:

- Released By
- Product Owner
- Project Manager
- Quality Coordinator
- any email ID
- Prepared by / Approved by
- Planned Release Date
- deployment or release method
- hardware and software configuration
- specific supporting-document links
- Line of Business, where no included ticket establishes a service line
- Revision History author or approver

## Configuration flagged rather than filled

Same principle, applied to a section rather than a field:

```text
Release Methods
FLAGGED FOR HUMAN COMPLETION — no current evidence in the Jira release scope
establishes the deployment method for 9.5.0.

The 9.4.0 page documents a server upload procedure and a software stack. That
describes 9.4.0. It was not copied forward.
```

`prepare-release-notes` documents the release. It does not own deployment
procedure, and it does not guess it.

## Known issues, honestly

With no evidence either way:

```text
Limitations
No known issues identified from the available Jira release evidence.
```

Not:

```text
Limitations
No known limitations for this release.
```

The first states what the evidence supports. The second is a claim about the
release that no evidence backs — and it is exactly the sentence most likely to be
copied from the previous page without thought.
