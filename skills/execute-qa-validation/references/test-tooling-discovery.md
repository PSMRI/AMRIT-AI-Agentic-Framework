# Test Tooling Discovery

## Contents

- [Scope of this document](#scope-of-this-document)
- [The discovery rule](#the-discovery-rule)
- [What to inspect](#what-to-inspect)
- [Tool-by-tool verification](#tool-by-tool-verification)
- [Environment and access verification](#environment-and-access-verification)
- [Recording the capability inventory](#recording-the-capability-inventory)
- [When nothing is available](#when-nothing-is-available)
- [What discovery must never do](#what-discovery-must-never-do)
- [Review checklist](#review-checklist)

## Scope of this document

Establishing, by inspection, what testing capability this environment genuinely provides before any execution claim is made.

## The discovery rule

> Do not claim a tool is available until you inspect the environment or repository and confirm it.

This framework's skills discover capabilities rather than hardcoding them, because host implementations differ. For QA execution the rule is stricter than elsewhere: a wrongly assumed tool does not merely degrade a report, it produces fabricated execution results.

Availability means all of:

1. the tool, suite, or capability is actually present;
2. it can actually be invoked here;
3. it can actually reach the build under test.

A dependency listed in a manifest is not a working suite. An automation framework installed with no reachable environment executes nothing.

## What to inspect

### Repository test infrastructure

- build files and package manifests — `pom.xml`, `build.gradle`, `package.json`, and their test dependencies and plugins;
- test source directories, and what layer each covers — unit, integration, contract, end-to-end;
- test runner configuration and scripts;
- CI workflow definitions, which reveal the commands the project actually runs and against what;
- contributor and QA documentation describing how to run each suite;
- fixtures, seed data, and environment configuration used by existing suites.

The commands come from these sources. Never assume a command exists.

### Existing automated suites

For each suite found, establish: what it covers, how it is invoked, what environment it needs, whether it runs against a deployed build or in isolation, and whether it is currently runnable here. A suite that needs a running database or a deployed API is only usable if that dependency is genuinely reachable.

### Host and environment capability

- host command execution;
- HTTP or API-call capability for API-level cases;
- browser or device automation, where one genuinely exists;
- filesystem access for reading configuration and writing evidence;
- log or observability access.

## Tool-by-tool verification

Each of these is usable only when verified. None may be assumed.

| Tool | Verify by | Usable when |
| --- | --- | --- |
| Existing project suites | Reading build files, scripts, and CI configuration | The command exists and its dependencies are reachable |
| Selenium | Finding it in project dependencies **and** confirming a driver and browser are available here | Both hold, and the target URL is reachable |
| Playwright | Finding it in project dependencies **and** confirming its browsers are installed | Both hold, and the target URL is reachable |
| Appium | Finding a configured server, driver, and a real or emulated device | All hold; otherwise device cases are infrastructure-blocked |
| Postman / Newman | Finding committed collections **and** a runner available here | Both hold, and the API is reachable |
| BrowserStack or another device cloud | Finding configuration **and** working credentials supplied by the environment | Both hold; never assume an account exists |
| Firebase | Finding configuration **and** access that this environment actually grants | Both hold |
| Direct API calls | Confirming an HTTP capability and a reachable, authenticated endpoint | Both hold |
| Browser capability of the host | Confirming the host exposes one and the URL is reachable | Both hold |
| Logs and observability | Confirming access to the actual log source for the build under test | Access is genuine, not assumed |

Credentials are supplied by the environment or by the user. This skill never requests, stores, prints, or embeds them in evidence, and never enters credentials into a system on the user's behalf beyond what the environment already provides for automated execution.

## Environment and access verification

Before classifying cases as executable, confirm:

- the QA environment URL resolves and responds;
- authentication succeeds for the roles the test cases require;
- the deployed build actually contains the change under test;
- required test data exists or can be created safely in that non-production environment;
- device, browser, or connectivity requirements named by the test cases are genuinely satisfiable.

Any of these failing moves affected cases to `BLOCKED` or `NOT EXECUTED — infrastructure`. It never moves them to `PASS`.

## Recording the capability inventory

The report states what was verified and what was absent, both explicitly:

```text
### Test capability verified in this environment

- Backend integration suite — available; `./mvnw verify -Pintegration`
  found in the build file and CI workflow, runs against the QA API
- Direct API calls — available; QA API reachable and authentication succeeded
- Playwright — not available; not present in any project dependency
- Appium — not available; no configured server or device
- BrowserStack — not available; no configuration and no credentials
- Application logs — not available; no log access from this environment
```

Absence is a finding, not a gap to paper over. It is what justifies each `NOT EXECUTED — infrastructure` verdict, and it tells the QA Lead what would need to be provided for a fuller run.

## When nothing is available

If no test capability and no reachable build exist, the run produces the blocked report:

```text
QA EXECUTION BLOCKED

Reason:
QA build/environment unavailable.

Test cases prepared:
42

Executed:
0

QA status:
NOT EXECUTED
```

Name precisely what was missing and what is required to unblock. Then stop. Do not review documentation, read the implementation, or reason about the design and present the result as validation — that is exactly the substitution this skill exists to prevent.

## What discovery must never do

- never install a testing framework, browser, driver, or device tooling to make a case runnable — report the absence instead;
- never point a suite at production, or at any environment the user did not identify as the test target;
- never create, modify, or delete production data;
- never weaken, skip, or modify an existing automated test to obtain a green run;
- never modify application code or configuration to make a suite pass;
- never fabricate a suite name, command, tool version, device, or credential;
- never claim a suite ran when its command failed to start.

## Review checklist

- every tool claimed available was verified in this environment, not inferred;
- suite commands came from build files, scripts, CI configuration, or documentation;
- the build under test was confirmed reachable and to contain the change;
- authentication was confirmed for the roles the cases need;
- absences are recorded explicitly and justify each non-execution verdict;
- nothing was installed, and no environment or application file was modified;
- no credential was requested, printed, or stored;
- a fully unavailable environment produced the blocked report and nothing more.
