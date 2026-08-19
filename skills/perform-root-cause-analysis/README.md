# perform-root-cause-analysis

`perform-root-cause-analysis` investigates AMRIT production defects, support
incidents, reopened defects, and QA failures to establish an evidence-backed root
cause, propose corrective and preventive actions (CAPA), and publish the
confirmed RCA to Confluence after explicit authorization.

**This skill is read-only** against Jira, source code, and all knowledge sources
during investigation. It writes only to Confluence, and only after the user has
both confirmed the RCA and explicitly requested publication.

## Purpose

Produce a defensible, evidence-backed Root Cause Analysis for an AMRIT incident,
grounded in mandatory inspection of the current source code, with clear
separation of symptom, trigger, immediate failure, underlying condition, and root
cause.

## Invocation

```text
/perform-root-cause-analysis AMRIT-1234
```

```text
Investigate the root cause of AMRIT-1234
```

If no ticket key is supplied, the skill asks for one or for equivalent incident
evidence before beginning.

## Investigation architecture

```text
Jira / support incident evidence
        ↓
User-supplied logs, screenshots, runtime evidence
        ↓
Identify affected repository or repositories
        ↓
MANDATORY current source-code inspection
        ↓
Trace actual execution and data path
        ↓
Relevant Confluence requirements and intended behaviour
        ↓
Graphify when cross-component relationships remain unclear
        ↓
DeepWiki only when architecture context is additionally useful
        ↓
Hypothesis formation and evaluation
        ↓
Causal chain construction
        ↓
RCA draft with CAPA recommendations
        ↓
Human confirmation gate
        ↓
Confluence publication only after explicit authorization
        ↓
Read-back verification
```

## The current-code rule

Current checked-out source code MUST be inspected for every software RCA.
DeepWiki, Confluence, Graphify, previous RCA documents, Jira comments, and
architecture documentation may support the investigation but must not substitute
for direct inspection of the current implementation.

This is intentionally different from the `answer-codebase-questions` research
order. RCA begins with incident evidence and current code, not with DeepWiki.

## Root-cause methodology

The skill distinguishes:

| Level | Example |
| --- | --- |
| Symptom | Beneficiary update returned HTTP 500 |
| Trigger | A record without districtId entered the workflow |
| Immediate Technical Failure | NullPointerException in the update service |
| Underlying Condition | Mobile registration can persist null districtId |
| Root Cause | District validation missing from the mobile controller |
| Contributing Factor | No regression test for mobile-registered records |

The skill never labels a symptom, exception name, or error code as the final
root cause.

## Hypothesis-driven investigation

When more than one plausible cause exists, the skill explicitly forms and
evaluates hypotheses before concluding:

- Hypothesis statement
- Supporting evidence
- Contradicting evidence
- Verification performed
- Result: Confirmed, Rejected, or Unresolved

## RCA confidence levels

| Status | Meaning |
| --- | --- |
| Confirmed Root Cause | Evidence establishes a defensible causal chain |
| Probable Root Cause | Strong evidence with a meaningful verification gap |
| Root Cause Not Conclusively Established | Evidence insufficient, conflicting, or inaccessible |

The skill never converts uncertainty into certainty to make the document look
complete.

## CAPA

The skill produces RCA and proposed CAPA because the AMRIT support process
groups them. They remain semantically separate:

- **Corrective Action** — addresses the immediate defect or root cause.
- **Preventive Action** — reduces recurrence of the same class of failure.

CAPA is proposed, not implemented. Implementation belongs to the appropriate
development workflow, typically `implement-jira-ticket`.

## Human confirmation and Confluence publication

The RCA draft is always presented for human confirmation before any Confluence
write:

```text
RCA Status: Draft — Pending Human Confirmation
Confluence Publication Status: Not Published
```

Publication requires the user to both confirm the RCA and explicitly request
publication. The skill publishes to the AMRIT RCA/CAPA Confluence area, reads
the page back, and verifies the result.

## Relationship to existing skills

```text
create-product-backlog
        ↓
production or support defect requires investigation
        ↓
perform-root-cause-analysis
        ↓
confirmed corrective action requires code change
        ↓
implement-jira-ticket
        ↓
create-development-pr
```

```text
execute-qa-validation
        ↓
QA failure requires root-cause investigation
        ↓
perform-root-cause-analysis
```

The skill investigates. It does not implement corrective actions, transition
Jira tickets, or claim any approval.

## Read-only boundaries

During investigation, the skill does not:

- edit, transition, or comment on Jira;
- change source code, commit, push, or create PRs;
- alter databases, configuration, or production systems;
- claim approvals, sign-offs, or CAPA completion.

## Required capabilities

Read access to Jira, Confluence, and the host's filesystem. DeepWiki and
Graphify are used read-only where available; neither is required. Confluence
write access is needed only for authorized publication.

## Example invocation

```text
/perform-root-cause-analysis DEMO-4521
```

See [examples/](examples/) for fictional RCA outputs illustrating all three
confidence levels: confirmed root cause, probable root cause, and root cause
not conclusively established. The examples are illustrative only and do not
describe real AMRIT architecture.

## Confluence publication example

After the user confirms the RCA:

```text
User: RCA confirmed. Publish it to the Support Tickets - RCA and CAPA area.

Agent:
1. Resolves the actual Confluence target page.
2. Verifies whether an RCA page already exists for this ticket.
3. Shows the publication plan (action, space, parent, title).
4. Creates or updates the page.
5. Reads the page back and verifies content.
6. Reports the resulting page URL.

RCA Status: Confirmed — Published to Confluence
Confluence Publication Status: Published
Page: <title and URL>
```

## Use and distribution

Invoke `/perform-root-cause-analysis` from the repository root using a
supported coding agent. Configure local MCP credentials only where the selected
client requires them; never commit real tokens.

For a packaged installation, download `perform-root-cause-analysis.zip` from
the latest GitHub Release. See the
[distribution guide](../../docs/installation.md) and
[lifecycle mapping](../../docs/lifecycle-mapping.md).
