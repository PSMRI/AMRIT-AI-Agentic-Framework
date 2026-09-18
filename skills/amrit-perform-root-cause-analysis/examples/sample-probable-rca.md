# Sample Probable RCA

This is a fictional example illustrating a Probable Root Cause outcome where
most evidence supports one cause but a meaningful verification gap remains. All
ticket keys, repositories, classes, and system names are fictional.

---

## Root Cause Analysis — DEMO-5810: Scheduled report generation fails intermittently in production

### Incident Details

| Field | Value |
| --- | --- |
| Jira / Support Ticket | DEMO-5810 |
| Product / Module | TM / Report Generation |
| Environment | Production |
| Affected Version | Release 4.1.0 |
| Reported Date | 2026-08-01 |
| Severity / Priority | Major / P2 |

### Incident Summary

The nightly scheduled report generation job fails intermittently, producing
incomplete CSV exports for approximately 3 of every 10 runs. The failure is not
deterministic and affects different report types on different nights.

### Impact

State-level health programme reports are delayed, requiring manual re-runs by
the operations team. Approximately 2 hours of operational effort per incident.

### Expected Behaviour

The scheduled report job should complete successfully every night, producing
complete CSV exports for all configured report types.

### Observed Behaviour

The job completes partially. Some report types generate successfully while
others fail with a database connection timeout. The specific reports that fail
vary between runs.

### Reproduction / Failure Conditions

Not reliably reproducible on demand. Failures correlate with report runs that
overlap with the nightly database backup window (02:00-03:00 IST).

### Incident Timeline

| Date | Event |
| --- | --- |
| 2026-08-01 | First failure reported by operations |
| 2026-08-02 | 3 more failures observed |
| 2026-08-05 | DEMO-5810 created |
| 2026-08-07 | RCA investigation initiated |

### Evidence Reviewed

#### Jira / Support Evidence

- DEMO-5810: intermittent failure report with partial log excerpts.
- No linked previous incidents.

#### Runtime / Logs / Screenshots

- Application logs show `ConnectionTimeoutException` during report query
  execution.
- Timeout occurs at varying points in the report generation sequence.
- Failures cluster between 02:15 and 02:45 IST.
- Successful runs outside the backup window show normal query times.

#### Repository / Code Evidence

**Repository**: DEMO-TM-API

- **File**: `src/main/java/com/demo/tm/scheduler/ReportScheduler.java`
  - The scheduled job is configured to run at 02:00 IST via a cron expression.
    Confirmed in code.
  - The job uses the default connection pool with no dedicated report connection
    configuration. Confirmed in code.

- **File**: `src/main/java/com/demo/tm/service/ReportGenerationService.java`
  - Report queries use the standard `JdbcTemplate` with default timeout
    settings. Confirmed in code.
  - No retry mechanism exists for failed queries. Confirmed in code.

- **File**: `src/main/resources/application.properties`
  - Connection pool max size is 10. Connection timeout is 30 seconds. Confirmed
    in code.
  - No separate datasource configuration for the report scheduler. Confirmed in
    code.

#### Confluence / Requirement Evidence

- Operations runbook (Confluence page "TM Nightly Jobs") documents the report
  schedule as 02:00 IST. Documented intent.
- Database backup schedule (Confluence page "Database Maintenance") documents
  backups at 02:00–03:00 IST. Documented intent.
- No documentation addresses the overlap.

### Technical Investigation

The investigation identified that the report scheduler and the database backup
window overlap completely. The report generation queries are long-running
(aggregate queries over large tables) and compete with the backup process for
database connections and I/O.

The application uses a single connection pool with a 30-second timeout. During
backup, database response times increase significantly. When a report query
exceeds the 30-second connection timeout, it fails with
`ConnectionTimeoutException`. Because there is no retry mechanism, the failure
is terminal for that report type.

The non-deterministic nature is explained by the variable ordering and duration
of individual report queries: reports that execute before the backup's heaviest
I/O phase succeed; those that coincide with it fail.

### Hypotheses Evaluated

#### Hypothesis 1: Report schedule overlaps with database backup window

- **Supporting evidence**: Scheduler cron runs at 02:00 IST. Backup window is
  02:00–03:00 IST. Failures cluster within this window.
- **Contradicting evidence**: None from available evidence.
- **Verification**: Scheduler configuration confirmed in code. Backup schedule
  confirmed in Confluence documentation. Log timestamps confirm the overlap.
- **Result**: Confirmed as the trigger.

#### Hypothesis 2: Connection pool exhaustion under backup load

- **Supporting evidence**: Connection pool is 10 connections with 30-second
  timeout. No separate report datasource. Report queries are long-running
  aggregates.
- **Contradicting evidence**: None from available evidence.
- **Verification**: Connection pool configuration confirmed in code. Query
  patterns confirmed in the service layer. Absence of retry mechanism confirmed
  in code.
- **Result**: Confirmed as the immediate technical failure mechanism.

#### Hypothesis 3: Production database I/O degradation during backup

- **Supporting evidence**: Log timestamps correlate with backup window. Reports
  that run outside the window succeed.
- **Contradicting evidence**: None.
- **Verification**: Production database performance metrics during backup were
  not available for inspection. The database server configuration and backup
  mechanism are not accessible in the checked-out source.
- **Result**: Unresolved. Strong circumstantial evidence supports this, but
  direct verification of database I/O contention requires production
  infrastructure access not available during this investigation.

### Causal Chain

```text
Reports fail intermittently with incomplete CSV output (Symptom)
      ↓
Report generation queries execute during the database backup window
02:00-03:00 IST (Trigger)
      ↓
ConnectionTimeoutException — database queries exceed the 30-second pool
timeout under backup load (Immediate Technical Failure)
      ↓
The report scheduler runs at 02:00 IST, fully overlapping the backup window,
using a shared connection pool with no retry mechanism (Underlying Condition)
      ↓
The report schedule was set to 02:00 IST without accounting for the database
backup window, and the connection pool and timeout configuration does not
accommodate degraded database performance (Root Cause — Probable)
```

### Root Cause

The report scheduler is configured to run at 02:00 IST, fully overlapping the
database backup window (02:00–03:00 IST). The application uses a shared
connection pool with a 30-second timeout and no retry mechanism. Under
backup-induced I/O contention, report queries exceed the timeout and fail
non-deterministically depending on which queries coincide with the heaviest
backup I/O.

**Status**: Probable Root Cause

**Verification gap**: Production database performance metrics during the backup
window were not available for direct inspection. The hypothesis that backup
causes I/O contention sufficient to exceed the 30-second timeout is strongly
supported by log correlation but not directly measured. Confirming this requires
database-level monitoring data from the production environment during a backup
run.

### Contributing Factors

1. No monitoring or alerting is configured for the report job's success or
   failure rate.
2. The operations runbook does not document the schedule overlap or its risk.

### Corrective Action

Reschedule the report generation job to run outside the database backup window.
For example, move the cron schedule from 02:00 IST to 04:00 IST.

**Status**: Proposed

### Preventive Action

1. Add a retry mechanism with exponential backoff to the report generation
   service for transient database connection failures.
2. Configure a separate datasource or connection pool for scheduled report
   queries with a longer timeout appropriate for aggregate reporting queries.
3. Add monitoring and alerting for scheduled job completion status.
4. Document infrastructure scheduling constraints (backup windows, maintenance
   windows) in the operations runbook alongside application job schedules.

**Status**: Proposed

### Validation Required

- Report generation succeeds consistently for 2 weeks after the schedule change.
- No `ConnectionTimeoutException` in report job logs after the schedule change.

### Regression Risk

- Rescheduling the report job may affect downstream consumers that expect
  reports at a specific time. Verify with the operations team.

### Related References

- DEMO-5810: incident ticket
- Confluence: TM Nightly Jobs, Database Maintenance

### Open Questions

- What are the actual database I/O metrics during the backup window? This would
  confirm or reject the backup-contention hypothesis.
- Are there other scheduled jobs that overlap with the backup window?

### Status

| Status | Value |
| --- | --- |
| RCA Status | Probable Root Cause — Pending Human Confirmation |
| CAPA Status | Proposed / Pending Implementation |
| Confluence Publication Status | Not Published |
