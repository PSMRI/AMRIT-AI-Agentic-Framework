# Sample Unresolved RCA

This is a fictional example illustrating a Root Cause Not Conclusively
Established outcome where evidence is insufficient to confirm a single root
cause. All ticket keys, repositories, classes, and system names are fictional.

---

## Root Cause Analysis — DEMO-6200: Intermittent sync failure on Android devices in field conditions

### Incident Details

| Field | Value |
| --- | --- |
| Jira / Support Ticket | DEMO-6200 |
| Product / Module | CHO App / Sync |
| Environment | Production (field devices) |
| Affected Version | Release 2.8.0 |
| Reported Date | 2026-07-20 |
| Severity / Priority | Major / P2 |

### Incident Summary

Community Health Officers report intermittent sync failures when attempting to
upload visit records from the Android application. The failures occur
unpredictably and do not produce user-visible error messages. Affected records
remain in local storage and are eventually synced on retry, but the delay
causes data gaps in the central dashboard.

### Impact

Visit data arrives 4–24 hours late for approximately 8% of CHOs across 3
states. The delay affects state-level daily reporting dashboards. No data loss
has been confirmed; records sync on subsequent attempts.

### Expected Behaviour

Visit records should sync to the server within the configured sync interval
(15 minutes) when the device has network connectivity.

### Observed Behaviour

Sync attempts fail silently for some records. The Android application logs show
`SyncException: unexpected response` but no further detail. The server-side
logs show no corresponding request for the failed sync attempts.

### Reproduction / Failure Conditions

Not reliably reproducible. Failures are reported from field conditions with
variable network quality. No reproduction has been achieved in a controlled
environment.

### Evidence Reviewed

#### Jira / Support Evidence

- DEMO-6200: support ticket with CHO reports from 3 states.
- No linked previous sync incidents.
- No attachments with device logs.

#### Runtime / Logs / Screenshots

- Android application log excerpt (user-supplied, partial): shows
  `SyncException: unexpected response` with no HTTP status code or response
  body.
- Server-side logs: no matching request entries for the reported failure
  timestamps.
- No device-level network logs available.
- No monitoring data for the sync API endpoint.

#### Repository / Code Evidence

**Repository**: DEMO-CHO-Android

- **File**: `app/src/main/java/com/demo/cho/sync/SyncManager.kt`
  - The sync process sends visit records as a batch POST request. Confirmed in
    code.
  - Error handling catches all exceptions and logs `SyncException: unexpected
    response` without preserving the HTTP status code or response body.
    Confirmed in code.
  - No retry differentiation between network errors and server errors.
    Confirmed in code.

- **File**: `app/src/main/java/com/demo/cho/sync/SyncApiClient.kt`
  - The HTTP client has a 30-second connection timeout and a 60-second read
    timeout. Confirmed in code.
  - No request logging or response interception beyond success and failure.
    Confirmed in code.

**Repository**: DEMO-CHO-API (server-side)

- RCA BLOCKED for this repository. The DEMO-CHO-API repository is not checked
  out in the current environment. The server-side sync endpoint, request
  validation, and error handling could not be inspected.

#### Confluence / Requirement Evidence

- Sync specification (Confluence page "CHO App Sync Architecture") documents
  the sync protocol. The specification does not mention error handling for
  partial network failures or request size limits. Documented intent.

### Technical Investigation

The investigation was limited by two evidence gaps:

1. The Android error handling discards the HTTP response detail, making it
   impossible to determine whether the server returned an error, a timeout
   occurred, or the network dropped the connection.
2. The server-side repository (DEMO-CHO-API) is not available for inspection,
   so the server-side sync endpoint behaviour could not be traced.

The absence of server-side log entries for the failed timestamps suggests
either:

- The request never reached the server (network-level failure), or
- The server rejected the request before application-level logging (for
  example, at a reverse proxy, load balancer, or request-size limit), or
- The server logged the request under different identifiers that were not
  correlated.

### Hypotheses Evaluated

#### Hypothesis 1: Network connectivity failure in field conditions

- **Supporting evidence**: Failures occur in field conditions with variable
  connectivity. No server-side log entry exists for failed sync attempts.
- **Contradicting evidence**: Devices have connectivity (other app functions
  work). The sync protocol retries and eventually succeeds.
- **Verification**: No device-level network logs available. No network
  monitoring data available.
- **Result**: Unresolved. Plausible but cannot be confirmed or rejected without
  device-level network diagnostics.

#### Hypothesis 2: Server-side request rejection (size limit or validation)

- **Supporting evidence**: No server-side log entry for failed attempts could
  indicate rejection before application logging. Batch sync sends variable-size
  payloads.
- **Contradicting evidence**: No direct evidence of a size limit. Records
  eventually sync, suggesting the payload is valid.
- **Verification**: Server-side code (DEMO-CHO-API) not available for
  inspection. Reverse proxy and load balancer configuration not accessible.
- **Result**: Unresolved. Cannot confirm or reject without server-side code
  inspection and infrastructure configuration review.

#### Hypothesis 3: Android HTTP client timeout under slow network

- **Supporting evidence**: 30-second connection timeout and 60-second read
  timeout are configured. Field networks may be slow.
- **Contradicting evidence**: The error message says "unexpected response", not
  "timeout", but the error handling discards the actual exception type.
- **Verification**: Error handling code confirmed to discard exception detail.
  Cannot distinguish timeout from other failures.
- **Result**: Unresolved. Plausible but the error handling code prevents
  differentiation.

### Causal Chain

```text
Visit records sync 4-24 hours late for some CHOs (Symptom)
      ↓
Sync attempt fails silently on the Android device (Trigger — observed)
      ↓
SyncException: unexpected response — actual failure type unknown because
error handling discards the HTTP status and response detail
(Immediate Technical Failure — confirmed in code)
      ↓
<gap — multiple viable causes, none confirmed>
      ↓
Root Cause Not Conclusively Established
```

### Root Cause

**Status**: Root Cause Not Conclusively Established

Three hypotheses remain viable: network failure, server-side rejection, and
HTTP client timeout. The investigation cannot distinguish between them because:

1. The Android error handling discards the failure detail needed to
   differentiate the causes.
2. The server-side repository is not available for inspection.
3. No device-level network diagnostics or server-side infrastructure
   configuration is accessible.

### Contributing Factors

1. The Android sync error handling catches all exceptions with a single generic
   message, discarding the HTTP status code, response body, and exception type.
   This is confirmed in code and directly prevents diagnosis.
2. No sync-specific monitoring or alerting exists on either the client or server
   side.

### Corrective Action

Improve the Android sync error handling to preserve and log the HTTP status
code, response body (truncated), exception type, and network state at the time
of failure. This does not fix the underlying sync failure but enables diagnosis
of the root cause when it recurs.

**Status**: Proposed

### Preventive Action

1. Add structured error logging to `SyncManager.kt` that distinguishes network
   errors, timeouts, HTTP 4xx, HTTP 5xx, and unexpected responses.
2. Add server-side request logging and monitoring for the sync endpoint.
3. Add sync success and failure rate monitoring with alerting thresholds.

**Status**: Proposed

### Validation Required

- After deploying improved error logging, reproduce or wait for the next sync
  failure and use the detailed error information to identify the actual cause.
- Server-side sync endpoint inspection (DEMO-CHO-API) once the repository is
  accessible.

### Regression Risk

- Error handling changes in `SyncManager.kt` should not affect sync behaviour,
  only logging. Verify that the retry mechanism still functions correctly.

### Related References

- DEMO-6200: incident ticket
- Confluence: CHO App Sync Architecture

### Open Questions

1. What does the DEMO-CHO-API sync endpoint do when it receives requests during
   high load? Server-side code inspection is needed.
2. Is there a reverse proxy or load balancer request-size limit that could
   reject large batch payloads before they reach the application?
3. What are the actual network conditions (latency, packet loss, bandwidth) at
   the field sites reporting failures?
4. Does the Android application correctly report network availability before
   attempting sync?

### Status

| Status | Value |
| --- | --- |
| RCA Status | Root Cause Not Conclusively Established — Pending Human Confirmation |
| CAPA Status | Proposed / Pending Implementation |
| Confluence Publication Status | Not Published |
