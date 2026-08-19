# RCA Investigation Workflow

## Investigation sequence

This is the mandatory sequence for every RCA. Steps are not interchangeable.

### 1. Gather incident evidence from Jira or support ticket

Read the issue in read-only mode. Collect whatever is available:

- issue key, type, summary, and description;
- expected behaviour and observed behaviour;
- environment, affected module, product, and version;
- severity, priority, and impact;
- reproduction steps;
- timestamps, comments, and decision-bearing discussion;
- attachments, screenshots, and logs;
- linked defects, incidents, stories, and features;
- previous attempted fixes;
- reopen history and resolution history;
- CAPA or RCA requirement indicators;
- affected release or version.

Do not fabricate missing incident evidence. Separate observed facts from reporter
hypotheses.

Do not mutate Jira. Do not transition, close, edit, reprioritize, assign, or
comment on the ticket.

### 2. Incorporate user-supplied runtime evidence

Accept and integrate any evidence the user provides:

- application logs or log excerpts;
- stack traces or error messages;
- screenshots or screen recordings;
- database query results;
- API request and response traces;
- monitoring or alerting output;
- deployment or configuration state;
- reproduction steps and results.

Runtime and log evidence should be integrated throughout the investigation
whenever the user supplies it, not treated as a one-time fixed step.

### 3. Identify affected repositories

From the incident evidence, determine which AMRIT repositories are materially
involved. Use:

- the Jira ticket's component, module, and product fields;
- the error location from logs or stack traces;
- the application, service, or API identified in the incident;
- the AMRIT repository map if available in the working environment.

RCA may span more than one repository. List every repository that the causal
chain plausibly touches.

### 4. Inspect current source code — MANDATORY

This step is not optional and cannot be replaced by documentation.

For every materially involved repository that is checked out and accessible:

1. Confirm the repository is present and accessible.
2. Read the files in the execution path implied by the incident.
3. Trace the actual behaviour: controllers, services, domain logic, persistence,
   validation, error handling, API clients, integrations, configuration,
   frontend state, Android flows, or whatever the incident path requires.
4. Record concrete code evidence following the guidelines in
   [current-code-inspection-guidelines.md](current-code-inspection-guidelines.md).

Do not blindly search the entire codebase. Start from incident evidence and
trace the actual execution path.

If a materially involved repository is not accessible, state the evidence gap
explicitly. Do not infer current implementation behaviour from documentation.

### 5. Research Confluence for intended behaviour

Search and read relevant Confluence pages for:

- requirements and expected behaviour;
- approved functional and business rules;
- workflow and integration documentation;
- API contracts and data specifications;
- historical design rationale;
- previous RCA or CAPA documentation in the Support Tickets — RCA and CAPA
  area.

Confluence describes intent and approved behaviour. It does not establish what
the code currently does.

When investigating, also inspect the AMRIT RCA/CAPA Confluence area to learn the
organizational RCA format:

```text
Support Tickets - RCA and CAPA
https://pmp.piramalswasthya.org/confluence/spaces/AMRIT/pages/76546642/Support+Tickets+-+RCA+and+CAPA
```

Read representative existing RCA pages to learn:

- expected structure and headings;
- table layout and terminology;
- naming conventions;
- RCA and CAPA fields;
- page hierarchy;
- ownership metadata.

Historical RCA pages are format and reference evidence only. Never assume that a
similar symptom in a previous RCA means the same root cause for the current
incident.

### 6. Use Graphify when relationships remain unclear

Use Graphify only when direct code inspection and Confluence leave cross-component
relationships unresolved:

- cross-repository dependencies;
- caller and callee paths;
- service-to-service relationships;
- API dependencies;
- impact propagation;
- flows spanning multiple AMRIT repositories.

Do not query Graphify when the causal chain is already established.

### 7. Use DeepWiki for architecture context when useful

DeepWiki is optional. Use it only when architecture context, module
responsibilities, or intended service boundaries would help orient the
investigation in a large system.

Any DeepWiki statement that materially affects the RCA must be verified against
the current checked-out source. If DeepWiki and current code conflict, the
current code wins for claims about current behaviour. Report the divergence.

### 8. Form and evaluate hypotheses

When more than one plausible cause exists, explicitly form hypotheses and
evaluate them against the evidence. See
[rca-methodology.md](rca-methodology.md) for the hypothesis evaluation protocol.

### 9. Construct the causal chain

Build the chain from symptom through trigger, immediate failure, underlying
condition, and root cause. See
[rca-methodology.md](rca-methodology.md) for the causal chain structure.

### 10. Draft the RCA with CAPA recommendations

Produce the RCA using the template in
[rca-confluence-template.md](rca-confluence-template.md), adapted to the
organizational format discovered from Confluence.

Apply the quality gate from `SKILL.md` before presenting the draft.

### 11. Present for human confirmation

Present the complete RCA draft and stop:

```text
RCA Status: Draft — Pending Human Confirmation
Confluence Publication Status: Not Published
```

### 12. Revise as directed

Incorporate corrections, additional evidence, hypothesis rejections, CAPA
modifications, or further investigation results from the user.

### 13. Publish to Confluence only after explicit authorization

Follow the publication contract in
[confluence-publishing-guidelines.md](confluence-publishing-guidelines.md).

## What this workflow does NOT do

- Mutate Jira in any way.
- Implement corrective or preventive actions.
- Commit, push, or create branches or PRs.
- Alter production systems, databases, configuration, or deployments.
- Claim approvals, sign-offs, or CAPA completion.
- Fabricate evidence, root causes, or conclusions.
