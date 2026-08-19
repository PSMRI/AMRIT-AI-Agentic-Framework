# Confluence Publishing Guidelines

## Publication is gated

The skill may automatically research and draft the RCA. It must not write
anything to Confluence during the investigation or draft phase.

Publication requires two conditions:

1. The user has confirmed or finalized the specific RCA.
2. The user has explicitly requested publication to Confluence.

Both conditions must be met. Do not interpret vague approval as a write request.

### Examples

| User message | Condition 1 | Condition 2 | Action |
| --- | --- | --- | --- |
| `Looks good.` | Ambiguous | No | Do not publish. Acknowledge and ask if they want to publish. |
| `RCA confirmed.` | Yes | No | Confirm the RCA is finalized. Ask if they want to publish. |
| `Publish it.` | Ambiguous | Yes | Clarify whether the RCA content is confirmed before publishing. |
| `RCA confirmed. Publish it to Confluence.` | Yes | Yes | Proceed with publication. |
| `RCA confirmed. Publish it to the Support Tickets - RCA and CAPA area.` | Yes | Yes | Proceed with publication to the specified area. |

A single user message may satisfy both conditions when it clearly does so.
Do not repeatedly ask for redundant confirmation when explicit authorization
already exists.

## Publication target

The primary AMRIT RCA/CAPA documentation area is:

```text
Support Tickets - RCA and CAPA
https://pmp.piramalswasthya.org/confluence/spaces/AMRIT/pages/76546642/Support+Tickets+-+RCA+and+CAPA
```

At runtime, resolve the actual parent page and hierarchy through the configured
Confluence MCP. Do not hardcode a page ID. Use the actual Confluence hierarchy
discovered through the MCP.

If the user specifies a different publication target, use that instead.

## Publication preview

Before performing a Confluence write, show a publication plan:

```text
Action: Create | Update
Space: AMRIT
Parent page: <actual page title resolved from Confluence>
Target page or title: <proposed page title>
Source ticket: <Jira key>
RCA status: <Confirmed Root Cause | Probable Root Cause | ...>
CAPA status: <Proposed | Pending Implementation | ...>
Known unresolved evidence: <if any, otherwise "None">
```

## Create vs update safety

### No existing RCA page

Create the page under the correct parent only after authorization.

### Existing draft RCA page

1. Read it first.
2. Compare the proposed new RCA with the existing draft.
3. Do not silently overwrite material human-authored content.
4. Show the user what will change.
5. Publish the authorized revision.

### Existing approved or final RCA page

1. Do not automatically overwrite it.
2. Report that an approved or final RCA already exists.
3. Require explicit instruction for modifying it.
4. Preserve traceability: if updating, do not delete the original findings
   without explicit instruction.

## Post-write verification

After creating or updating a Confluence page:

1. Read the resulting page back through the MCP.
2. Verify that required sections and content were persisted.
3. Verify the title and parent page.
4. Report the actual page reference or URL returned by the system.
5. Report any publication failure honestly.

Do not claim success based only on the write request returning without an
obvious error.

## Page naming convention

At runtime, inspect existing RCA pages to learn the naming convention. A
reasonable default when no convention is discovered:

```text
RCA — <Ticket Key>: <Brief Summary>
```

Example:

```text
RCA — AMRIT-1234: Beneficiary update fails with HTTP 500
```

Adapt to the actual naming convention discovered from the Confluence area.

## Content format

Use the RCA template from
[rca-confluence-template.md](rca-confluence-template.md), adapted to the
actual organizational format discovered from existing Confluence RCA pages.

When publishing, convert the markdown RCA to the format the Confluence MCP
supports (typically Confluence storage format or wiki markup, depending on the
MCP capabilities).

## After publication

Update the RCA status:

```text
RCA Status: Confirmed — Published to Confluence
Confluence Publication Status: Published
Page: <title and URL or reference>
```
