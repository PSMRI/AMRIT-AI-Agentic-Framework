# Release-Notes Workflow

The full sequence for preparing AMRIT release notes. Jira supplies release
content; Confluence supplies the format.

## Step 0 — Establish the target release

Obtain the target version from the invocation:

```text
/prepare-release-notes 3.8.2
Prepare release notes for AMRIT 3.8.2
Prepare FLW release notes for version 2.10
```

If no version was supplied, ask for it. Do not guess a version from recent Jira
activity, recent commits, or the next number after the newest release note.

Establish the product / release family as well. The version alone is often
ambiguous — `2.9` can be an FLW App release while `3.8.1` is a Web and API
release. Where the invocation names the product ("FLW release notes"), use it.
Where it does not, resolve the family from the Jira project the version belongs
to, and state the conclusion in the draft.

## Step 1 — Resolve the Jira version / Fix Version

Resolve the target version to a real Jira version object in the correct project.
Record:

- Jira project key
- version name exactly as Jira spells it
- version id
- released flag
- start date, if present
- release date, if present
- version description, if present

Version names are not always what the user typed. `3.7` may exist in Jira as
`3.7.0`; `2.7.4 - hotfix` may be spelled differently from the page title
`2.7.4_Hotfix`. Match against the actual Jira version list rather than assuming.

If no matching Jira version exists, stop:

```text
RELEASE NOTES BLOCKED — target release could not be resolved from Jira
```

Report the candidate versions Jira does contain so the user can correct the
target. Do not proceed by inventing a Fix Version.

## Step 2 — Read Jira release metadata

From the resolved version, capture everything Jira provides about the release
itself, not its issues. See
[jira-release-data-guidelines.md](jira-release-data-guidelines.md).

## Step 3 — Retrieve release-member issues

Retrieve all issues Jira assigns to that Fix Version, paginating until the result
set is complete. Compare the number retrieved against the total the query
reports; a partial page is a common source of silently missing tickets.

Record the count. It is a published field in some templates and a review signal
in all of them.

## Step 4 — Inspect issue metadata

For every retrieved issue capture at least: key, issue type, summary, status,
resolution, priority, labels, components, service line, assignee, parent or epic,
and linked issues. Retrieve descriptions and comments where the template needs
narrative content or where classification is otherwise ambiguous.

## Step 5 — Classify release contents

Apply [release-content-classification.md](release-content-classification.md) to
sort issues into the categories the selected template actually uses. Classification
is evidence-driven; when evidence is contradictory, flag it rather than deciding
silently.

## Step 6 — Inspect the current Confluence template

Apply [template-discovery-guidelines.md](template-discovery-guidelines.md).
Inspect the live release-note hierarchy, identify the newest applicable
Mithun James-authored or maintained page for this product family, and compare it
against its recent neighbours to distinguish the stable structure from
release-specific variation.

Steps 3–5 and step 6 are independent. Either order is acceptable, and doing the
Jira work first avoids drafting a template that no Jira evidence can fill.

## Step 7 — Select the template

Record the selection internally:

```text
Template Source: <page title> (<page id>) — <author>, <created/updated date>
Compared Against: <other pages inspected>
Selection Reason: newest applicable <product family> release note
```

Keep this in the internal draft state and the review summary. Do not publish it
into the Confluence page body unless the current convention includes such a note.

## Step 8 — Populate the template

Fill each template field from Jira evidence, per
[release-notes-template-guidelines.md](release-notes-template-guidelines.md).

For every field, one of three outcomes applies:

1. **Populated from Jira** — record the field and its Jira source.
2. **Populated from explicit user-provided current evidence** — record that the
   user supplied it.
3. **Missing** — record it in Missing Required Metadata.

There is no fourth outcome. A field is never filled from a historical release
note.

## Step 9 — Validate

Run the traceability quality gate in `SKILL.md`. Additionally confirm:

- every ticket in every table appears in the Jira Fix Version result set;
- no ticket in the Jira result set is silently dropped from the draft — if a
  ticket is intentionally excluded, the exclusion and its reason are stated;
- the ticket count in the draft matches the ticket count retrieved from Jira, or
  the difference is explained;
- statuses in the draft match the statuses retrieved from Jira verbatim.

## Step 10 — Present the draft

Present the rendered release note, then the review summary:

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

## Step 11 — Apply revisions

The user may correct classification, supply missing metadata, add or remove a
ticket when Jira evidence is corrected, adjust wording, or clarify a service line.

When the user asks to add or remove a ticket, re-check Jira. If Jira still does
not place the ticket in the Fix Version, say so and record that the inclusion
rests on the user's instruction rather than Jira evidence. Apply the instruction;
do not silently present it as Jira-backed.

Re-present the revised draft with the same status block.

## Step 12 — Publish only when authorized

Apply [confluence-publishing-guidelines.md](confluence-publishing-guidelines.md).
Nothing is written to Confluence before both confirmation and explicit
publication authorization exist.

## Step 13 — Verify and report

After the write, read the page back and verify it. Report the actual page
reference or URL, and the final status.

## Blocking conditions

| Condition | Status |
| --- | --- |
| No Jira version matches the target | `RELEASE NOTES BLOCKED — target release could not be resolved from Jira` |
| Confluence hierarchy unreachable, no template establishable | `RELEASE NOTES BLOCKED — current Confluence template could not be inspected` |
| Jira version resolves but contains no issues | Not blocked. Report an empty release scope and ask whether the Fix Version is correct. Do not populate the release from another source. |
