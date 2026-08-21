# Confluence Publishing Guidelines

Confluence is read-only for template discovery. It becomes writable only after
the user has both confirmed the draft and explicitly authorized publication.

## Publication is gated

The skill may research and draft freely. It must not write anything to Confluence
during template discovery, drafting, or revision.

Publication requires two conditions:

1. The user has confirmed or finalized the specific release-note draft.
2. The user has explicitly requested publication to Confluence.

Both must be met. Do not interpret vague approval as a write request.

### Examples

| User message | Condition 1 | Condition 2 | Action |
| --- | --- | --- | --- |
| `Looks good.` | Ambiguous | No | Do not publish. Acknowledge and ask whether to publish. |
| `Release notes confirmed.` | Yes | No | Confirm the draft is finalized. Ask whether to publish. |
| `Publish them.` | Ambiguous | Yes | Clarify that the content is confirmed before publishing. |
| `Release notes confirmed. Publish them to Confluence.` | Yes | Yes | Proceed with publication. |
| `Confirmed. Publish under FLW App releases.` | Yes | Yes | Proceed, using the specified area. |

A single clear statement may satisfy both conditions. Do not ask for redundant
confirmation once explicit authorization exists.

Revising the draft after a confirmation resets condition 1 for the changed
content. Re-present the revised draft; do not publish an older confirmation
against newer content.

## Resolve the publication target dynamically

Determine the target from the live Confluence hierarchy:

- normal AMRIT releases belong under the appropriate product area beneath
  `Release Notes`;
- FLW releases belong under `FLW App releases`;
- other product families belong under their own area, where one exists.

Resolve the parent page through the MCP. Do not hardcode an invented child page
ID, and do not create a new product area on your own initiative — if no
applicable area exists, report that and let the user decide where the page belongs.

If the user names a different target, use theirs.

## Publication plan

Before any write, show:

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

If Missing Required Metadata is non-empty and any listed field is genuinely
required by the selected template, ask the user to supply it or to confirm
publication without it. Do not fill it to make the plan look clean.

Publication is also blocked while either of these is unresolved:

- **an unconfirmed release date** — where the Jira `releaseDate` and another
  relevant current source disagree, publish only the value the user confirmed;
- **an unconfirmed format** — where the product family has no release-note
  precedent in Confluence, such as an mHWC release, publish only after the user
  confirms which template to use.

## Existing-page protection

Check whether a release-note page for the target version already exists in the
applicable area before creating anything.

### No existing page

Create it under the resolved parent, after authorization.

### Existing draft page

1. Read it first.
2. Compare the proposed content against the existing draft.
3. Do not silently overwrite material human-authored content.
4. Show the user what will change.
5. Publish the authorized revision.

### Existing published or final page

1. Do not overwrite it automatically.
2. Report that a published release-note page already exists, with its title, URL,
   and last-updated metadata.
3. Require explicit update intent before modifying it.
4. When updating, do not delete existing content without explicit instruction.
5. Where the current Jira Fix Version membership differs from what the page
   published, report the delta — the Fix Version is the current authoritative
   scope, the page is the previously published state — and require human
   confirmation of that delta before modifying the page. Never modify Jira to
   reconcile it.

A published release note is an organizational record. Treat replacing one as a
distinct decision from writing a new one.

## Content format

Render the body according to the template selected at runtime, per
[release-notes-template-guidelines.md](release-notes-template-guidelines.md).

Convert the draft into the format the Confluence MCP accepts — typically storage
format or wiki markup. Verify after writing that tables survived the conversion;
table-heavy release notes are the most common casualty of a format mismatch.

## Post-publication verification

After creating or updating the page:

1. read the page back through the MCP;
2. verify the title matches the intended page title;
3. verify the parent is the intended area;
4. verify the version stated in the body matches the target release;
5. verify the Jira issue tables persisted, with the expected ticket count and the
   real keys;
6. verify every required section of the selected template is present;
7. verify that no old-release values leaked in — check specifically for another
   version number, another release date, a previous release's ticket, a previous
   limitation, and any personal name or email address that current evidence did
   not establish;
8. report the actual page reference or URL.

Do not claim publication success because the write call returned without an
obvious error. Report any failure honestly, including a partial write.

## After publication

```text
Release Notes Status: Confirmed — Published to Confluence
Confluence Publication Status: Published
Page: <title and URL>
Verified: title, parent, version, ticket tables, required sections
```

If read-back verification fails, say so and do not report the release note as
published:

```text
Confluence Publication Status: Write attempted — read-back verification failed
```

## Boundaries during publication

Publication writes one Confluence page. It does not:

- modify Jira in any way;
- move, rename, restrict, or delete other Confluence pages;
- alter the parent area's own content;
- add labels or restrictions beyond the convention the recent pages show;
- tag a release, deploy anything, or execute any release procedure.
