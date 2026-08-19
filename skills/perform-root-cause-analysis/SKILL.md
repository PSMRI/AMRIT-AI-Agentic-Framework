---
name: perform-root-cause-analysis
description: Investigate AMRIT production defects and support incidents using incident evidence and mandatory current source-code analysis, establish an evidence-backed root cause and CAPA recommendations, present the RCA for human confirmation, and publish the confirmed RCA to Confluence only after explicit authorization.
metadata:
  stage: Cross-lifecycle — Support & Quality
  category: Incident investigation and root-cause analysis
  primary_role: Senior Developer / Technical Lead / Support Engineer
  skill_type: Standalone
  knowledge_sources:
    - Jira
    - Confluence
    - Checked-out AMRIT repositories
    - Graphify
    - DeepWiki
  supported_inputs:
    - Jira defect or bug ticket
    - Support incident ticket
    - Reopened defect requiring investigation
    - Production incident reference
    - QA failure evidence from execute-qa-validation
  primary_input: Jira defect or support incident ticket
  primary_output: Evidence-backed RCA with CAPA recommendations, pending human confirmation
  upstream_skills:
    - create-product-backlog
    - execute-qa-validation
  downstream_skills:
    - implement-jira-ticket
---

# Perform Root Cause Analysis

Investigate an AMRIT production defect, support incident, reopened defect, or QA
failure. Establish an evidence-backed root cause using mandatory current
source-code inspection, propose corrective and preventive actions, present the
complete RCA for human confirmation, and publish the confirmed RCA to Confluence
only after explicit authorization.

## The current-code rule

**Current checked-out source code MUST be inspected for every software RCA.**

DeepWiki, Confluence, Graphify, previous RCA documents, Jira comments, and
architecture documentation may support the investigation but must not substitute
for direct inspection of the current implementation.

If current source evidence contradicts documentation, report the divergence. Do
not silently force the code to match the documentation in the RCA narrative.

If relevant source code cannot be inspected, do not claim a confirmed technical
root cause. Report `RCA BLOCKED — relevant current source code could not be
inspected` or `Root Cause Not Conclusively Established` depending on the
remaining evidence.

## Invocation

```text
/perform-root-cause-analysis AMRIT-1234
```

```text
Investigate the root cause of AMRIT-1234
```

If no ticket key is supplied, ask for one or for equivalent incident evidence
before beginning.

## Discover available capabilities

Use the connected tools' logical Jira issue-read, Confluence search/page-read,
DeepWiki repository search/read, and Graphify relationship-read capabilities.
Tool names vary by host: discover equivalent read-only operations rather than
assuming names.

Do not request write permissions or invoke write operations during investigation.
When a source is unavailable, continue on the remaining evidence and record the
limitation. Do not ask the user to install a tool during normal execution.

## Investigation workflow

Read and follow
[references/rca-investigation-workflow.md](references/rca-investigation-workflow.md)
for the full investigation sequence.

The high-level flow is:

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
```

This is intentionally different from the `answer-codebase-questions` research
order. RCA begins with incident evidence and current code, not with DeepWiki.

## Current-code inspection

Read and follow
[references/current-code-inspection-guidelines.md](references/current-code-inspection-guidelines.md)
for what to inspect and how to record code evidence.

Before forming any technical hypothesis:

1. Confirm which repositories are actually checked out and accessible.
2. Read the real files in the execution path implied by the incident.
3. Trace the actual behaviour from the reported symptom to the underlying code.
4. Record concrete code evidence: repository, file, class or function, relevant
   behaviour, and relationship to the incident.

Never establish a current technical root cause solely from DeepWiki, Confluence,
Graphify, Jira comments, or previous RCA documents.

## Root-cause methodology

Read and follow
[references/rca-methodology.md](references/rca-methodology.md)
for the full methodology.

The skill must distinguish:

- **Symptom** — what the user or system observed.
- **Trigger** — the condition or event that exposed the failure.
- **Immediate Technical Failure** — where and how execution failed.
- **Underlying Condition** — why the failing state could reach that path.
- **Root Cause** — why that condition was allowed to exist.
- **Contributing Factors** — things that increased probability, duration, or
  impact but are not themselves the root cause.

Never label a symptom, exception name, timeout, or error code as the final root
cause without explaining the causal chain behind it.

## Hypothesis-driven investigation

When more than one plausible cause exists, explicitly form and evaluate
hypotheses before concluding. For each hypothesis capture:

- Hypothesis statement
- Evidence supporting it
- Evidence contradicting it
- Verification performed
- Result: Confirmed, Rejected, or Unresolved

Prefer falsifiable investigation. Do not jump from evidence to the first
plausible explanation.

## Evidence and confidence

Read and follow
[references/evidence-and-confidence-guidelines.md](references/evidence-and-confidence-guidelines.md)
for classification rules.

Use these RCA statuses:

- **Confirmed Root Cause** — available evidence establishes a defensible causal
  chain explaining the incident.
- **Probable Root Cause** — strong evidence supports the cause but a meaningful
  verification gap remains.
- **Root Cause Not Conclusively Established** — evidence is insufficient,
  conflicting, inaccessible, or multiple hypotheses remain viable.

Never convert uncertainty into certainty to make the document look complete.

## CAPA

Read and follow
[references/capa-guidelines.md](references/capa-guidelines.md).

Corrective Action addresses the immediate defect or root cause. Preventive
Action reduces recurrence of the same class of failure.

Do not report CAPA as complete merely because the agent proposed actions. Use:

```text
Corrective Action: Proposed
Preventive Action: Proposed
CAPA Status: Pending implementation / validation
```

The skill does not implement CAPA. Implementation belongs to the appropriate
development workflow, typically `implement-jira-ticket`.

## RCA output

Read and follow
[references/rca-confluence-template.md](references/rca-confluence-template.md)
for the full output template.

At runtime, also inspect the actual AMRIT Confluence RCA/CAPA area to learn the
organizational format before drafting.

## Quality gate

Before presenting the RCA draft, verify internally:

- Real incident or support evidence was inspected.
- Relevant current source code was inspected.
- All materially involved repositories were considered.
- Expected and observed behaviour are distinguished.
- Symptom is not mislabelled as root cause.
- Trigger is not mislabelled as root cause.
- Immediate failure is not mislabelled as root cause.
- Competing hypotheses were considered where appropriate.
- Root-cause confidence is supported by evidence.
- Contributing factors are separated from root cause.
- Corrective action addresses the established cause.
- Preventive action addresses recurrence.
- CAPA is not falsely reported complete.
- Documentation and code conflicts are disclosed.
- Evidence gaps are disclosed.
- No external system was mutated.
- RCA remains pending human confirmation.
- Confluence has not been modified.

## Human confirmation gate

After producing the complete RCA, stop with:

```text
RCA Status: Draft — Pending Human Confirmation
Confluence Publication Status: Not Published
```

The user must review the exact RCA. They may correct findings, add incident
evidence, reject a hypothesis, modify CAPA, or request further investigation.
Revise the draft accordingly.

## Confluence publication

Read and follow
[references/confluence-publishing-guidelines.md](references/confluence-publishing-guidelines.md)
for the full publication contract.

Publication requires two conditions:

1. The user has confirmed or finalized the specific RCA.
2. The user has explicitly requested publication to Confluence.

Do not interpret vague approval as a write request.

- `Looks good.` — does not authorize publication.
- `RCA confirmed.` — confirms the RCA but does not request publication.
- `RCA confirmed. Publish it to Confluence.` — authorizes publication.

A single user message may satisfy both conditions when it clearly does so.
Do not repeatedly ask for redundant confirmation when explicit authorization
already exists.

Before writing, show a publication plan:

```text
Action: Create | Update
Space: AMRIT
Parent page: <resolved from Confluence>
Target page or title: <proposed>
Source ticket: <key>
RCA status: <status>
CAPA status: <status>
Known unresolved evidence: <if any>
```

After writing, read the page back, verify sections were persisted, and report
the actual page reference or URL. Do not claim success based only on the write
request returning without an obvious error.

## Read-only investigation boundary

Before publication authorization, all external-system interactions are
read-only. The skill must not:

- edit, transition, close, assign, comment on, or alter Jira;
- change source code, commit, push, create branches, or create PRs;
- alter databases, configuration, or production systems;
- restart services or deploy anything;
- mark tickets closed or claim QA, release, or implementation approval.

The skill performs investigation, analysis, and RCA/CAPA documentation with
authorized Confluence publication. It does not perform remediation.

## No production experiments

Do not alter production systems to test hypotheses. The skill may recommend a
validation experiment:

```text
Proposed validation:
Reproduce the issue in an approved non-production environment with condition X.

Expected observation if hypothesis is correct:
...
```

But it must not perform dangerous or unauthorized production mutations.

## Multi-repository incidents

RCA may span more than one repository. Identify all repositories materially
involved. Directly inspect current source in every repository required to
establish the causal chain. If a required repository cannot be inspected,
explicitly state the resulting evidence gap.

## Role of DeepWiki

DeepWiki is optional supporting context only. Use it for architecture context,
repository or module responsibilities, historical architectural understanding,
intended service boundaries, and large-system orientation.

Any DeepWiki statement that materially affects the RCA must be verified against
the current checked-out source where technically applicable. If DeepWiki and
current code conflict, the current checked-out implementation evidence wins for
claims about current behaviour. Report the divergence explicitly.

## Role of Graphify

Use Graphify when direct code inspection leaves unresolved relationship
questions, especially cross-repository relationships, caller and callee paths,
service-to-service relationships, API dependencies, impact propagation, and
flows spanning multiple AMRIT repositories. Do not query Graphify unnecessarily
when the causal chain is already established from code and incident evidence.

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

Also:

```text
execute-qa-validation
        ↓
QA failure requires root-cause investigation
        ↓
perform-root-cause-analysis
```

This skill investigates. It does not implement the corrective action. The skill
is independently executable; it recommends but does not require other skills at
runtime.

## Required capabilities

Read access to Jira, Confluence, and the host's filesystem and repository
access. DeepWiki and Graphify are used read-only where the environment provides
them; neither is required. Confluence write access is needed only for authorized
publication.

If Jira is unavailable, the skill can still investigate from user-supplied
incident evidence and current code. If the source code is unavailable, the skill
reports the limitation rather than fabricating a technical root cause.

## Completion status semantics

Every invocation ends with one of:

- **RCA Status: Draft — Pending Human Confirmation**
- **RCA Status: Confirmed — Published to Confluence** (only after authorization
  and verified publication)
- **RCA BLOCKED — relevant current source code could not be inspected**

The RCA is never automatically complete, approved, or published.
