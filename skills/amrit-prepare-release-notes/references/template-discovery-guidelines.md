# Template Discovery Guidelines

How to find and choose the current AMRIT release-note format. This is the only
purpose Confluence release notes serve in this skill: they supply structure and
presentation, never release content.

## Discover the live hierarchy

The AMRIT release-note parent is:

```text
Release Notes
https://pmp.piramalswasthya.org/confluence/spaces/AMRIT/pages/46563852/Release+Notes
```

Use authenticated Confluence access to read the actual current hierarchy at
runtime. Do not rely on public web indexing, cached knowledge of the space, or
page IDs written into this file.

The parent page has organized child areas per product. Read the children of the
parent, then the children of the relevant product area, rather than assuming
which versions exist. Areas are added and reorganized over time.

Page IDs in this file are illustrative context, not addresses to hardcode. Always
resolve the current hierarchy through the MCP.

## Identify the product family

Match the target release to a product area:

| Release family | Confluence area |
| --- | --- |
| AMRIT Web and API releases | the Web and API area beneath `Release Notes` |
| FLW App releases | `FLW App releases` |
| Other mobile or product areas | the corresponding area, if one exists |

An area can exist and be empty. If the applicable product area contains no
release notes, there is no current template to derive for that family. Say so,
and ask which convention to follow — do not silently borrow another product's
format and present it as the organizational standard.

The mHWC mobile-app release area was observed to contain no release notes, so
there is currently no mHWC release-note precedent or template in Confluence to
derive from. For an mHWC request:

```text
→ state that no mHWC release-note precedent/template was found in Confluence
→ ask the user which template/format should be used
→ do not automatically substitute the AMRIT Web/API or FLW format
→ do not publish until the format is confirmed
```

Re-check the area at runtime; it may have been populated since. Report the absence
as an observation about current Confluence content, and do not describe it as an
organizational policy about mHWC releases beyond what was actually observed.

## Inspect the recent pages

Within the applicable area, read the actual pages. At minimum, for AMRIT Web and
API releases, locate and inspect the versions the team named:

```text
3.7
3.8.0
3.8.1
```

Note that a page title may differ from how the version is spoken — `3.7` may be
titled `3.7.0`. Match against the real page titles in the hierarchy.

For each page, capture the metadata as well as the body:

- page title
- page id
- author
- created date
- last updated date
- version number of the page

The metadata is what makes precedence decidable. The body alone cannot tell you
which schema is current.

## Precedence

```text
Newest applicable Mithun James release note
        ↓
Other recent Mithun James release notes
        ↓
Older AMRIT release notes only as fallback/reference
```

## Recency means page recency, not version number

This is the single most important discovery rule, and the easiest to get wrong.

A page for a **higher version number can be older** than a page for a lower
version number. Releases are documented retrospectively, and back-filled pages
for earlier versions can be written after later versions were published.

Therefore:

- do not assume the highest version number carries the newest schema;
- compare `created` and `updated` metadata across the candidate pages;
- when several pages were authored in the same batch and share one schema, that
  shared schema is the current convention;
- when an older page uses a different schema, treat it as superseded.

Worked illustration of the reasoning pattern, using the versions the team named:
if `3.8.0` was authored months before `3.6.2`, `3.7.0`, and `3.8.1`, and those
three later pages share one clean schema while `3.8.0` carries an older
contact-heavy layout, then the current convention is the schema of the three
later pages — even though `3.8.0` has a higher version number than two of them.
Verify this at runtime against the actual metadata; do not assume it still holds.

## Do not use these as the primary schema

- the standing `AMRIT Release Notes Template` page, when it predates the recent
  release notes — it can carry a superseded layout and real personal contact
  details;
- older release notes such as `3.6.1` or earlier, when newer Mithun James pages
  exist;
- any page whose schema is not reflected in the recent batch.

They remain useful as fallback reference when nothing newer exists, and as
evidence of what changed.

## Derive the stable structure

Compare the recent applicable pages against each other and record:

- **common/stable sections** — present in every recent page, in the same order;
- **field names** — the exact labels used, including punctuation and casing;
- **release-details table structure** — column layout and row set;
- **ticket table structure** — the exact columns and their order;
- **category structure** — how tickets are grouped into sections;
- **optional sections** — present in some recent pages and absent in others;
- **revision-history conventions** — columns and how the first row is worded;
- **status terminology** — the exact vocabulary used for release and ticket status;
- **formatting conventions** — heading levels, table emphasis, how ticket keys are
  embedded in text;
- **page-title convention** — for example a bare version number with no prefix;
- **parent-page convention** — which area the page is filed under;
- **product-specific differences** — where the families genuinely diverge.

A field that appears in exactly one recent page is release-specific, not part of
the stable schema. Include it only when the target release has evidence that
calls for it.

## Handling anomalies

If one newer page is clearly a special-case release — a hotfix with a truncated
structure, a page with an obvious paste or macro artifact, a page mid-revision —
derive the stable structure from the newest comparable examples instead of copying
the anomaly.

Record the anomaly in the review summary rather than silently smoothing it over.
Rendering artifacts in a source page are a signal about the page, not a format to
reproduce.

## Do not merge every historical field

Use:

```text
latest applicable convention
```

not:

```text
union of every historical field
```

If the recent pages show incremental evolution, prefer the newest stable
structure. A field the current convention dropped stays dropped. Reintroducing it
"for completeness" produces a document that matches no convention and invites the
exact contact-detail copying this skill forbids.

## Record the selection

Keep this in internal draft state and surface it in the review summary:

```text
Template Source: <page title> (<page id>) — <author>, created <date>
Compared Against: <other pages inspected, with dates>
Selection Reason: <why this page is the newest applicable convention>
Anomalies Noted: <if any>
```

Do not publish this selection note into the Confluence page body unless the
current convention includes such a note.

## When template discovery fails

If the Confluence hierarchy cannot be read, or no applicable page can be
retrieved, stop:

```text
RELEASE NOTES BLOCKED — current Confluence template could not be inspected
```

Report which pages were attempted and what the access result was. Never claim a
page was inspected if the request did not actually return it, and never
reconstruct a format from memory and present it as the current organizational
template.
