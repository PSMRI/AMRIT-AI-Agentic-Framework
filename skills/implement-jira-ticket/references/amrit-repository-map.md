# AMRIT Repository Map for Implementation Routing

## Contents

- [Purpose and authority](#purpose-and-authority)
- [UI repositories — frontend persona](#ui-repositories--frontend-persona)
- [API repositories — backend persona](#api-repositories--backend-persona)
- [Mobile repositories — Android persona](#mobile-repositories--android-persona)
- [Infrastructure and tooling repositories](#infrastructure-and-tooling-repositories)
- [Repository pairs](#repository-pairs)
- [Building the impact shortlist](#building-the-impact-shortlist)
- [Repository boundary rules](#repository-boundary-rules)
- [Catalog maintenance](#catalog-maintenance)

## Purpose and authority

Use this map to identify which repositories a ticket plausibly touches and which persona owns each one. It is discovery metadata, not evidence of impact and not evidence of a repository's internal architecture. Impact is confirmed by reading the ticket, the approved design, and the actual source code.

- **GitHub organization/owner:** PSMRI
- **DeepWiki repository identifier format:** `PSMRI/<repository-name>`
- **Catalog source of truth:** the central [PSMRI/AMRIT README](https://github.com/PSMRI/AMRIT/blob/main/README.md)

Use each repository name with its exact GitHub capitalization.

## UI repositories — frontend persona

All UI repositories are Angular applications and route to `implement-frontend-change`.

| Repository | Domain | Paired API |
|---|---|---|
| `Inventory-UI` | Inventory management | `Inventory-API` |
| `Common-UI` | Shared UI components across service lines | Multiple |
| `MMU-UI` | Mobile Medical Unit | `MMU-API` |
| `TM-UI` | Telemedicine centres | `TM-API` |
| `HWC-UI` | Health and Wellness Centre | `HWC-API` |
| `ADMIN-UI` | Deployment configuration management | `Admin-API` |
| `HWC-Scheduler-UI` | HWC appointment scheduling | `Scheduler-API` |
| `HWC-Inventory-UI` | HWC inventory management | `Inventory-API` |
| `Scheduler-UI` | Appointment scheduling | `Scheduler-API` |
| `ECD-UI` | Early Childhood Development | `ECD-API` |
| `Helpline1097-UI` | 1097 helpline | `Helpline1097-API` |
| `Helpline104-UI` | 104 helpline | `Helpline104-API` |

## API repositories — backend persona

All API repositories are Spring Boot services and route to `implement-backend-change`.

| Repository | Domain |
|---|---|
| `FLW-API` | REST APIs for the FLW mobile application |
| `Admin-API` | Configuration management for AMRIT deployments |
| `Common-API` | Shared AMRIT services and integrations |
| `ECD-API` | Early Childhood Development services |
| `HWC-API` | Health and Wellness Centre services |
| `Inventory-API` | Medicine inventory and dispensing |
| `MMU-API` | Mobile Medical Unit services |
| `Scheduler-API` | Specialist consultation appointment scheduling |
| `TM-API` | Telemedicine services |
| `Helpline1097-API` | 1097 AIDS health information helpline |
| `Helpline104-API` | 104 health information helpline |
| `BeneficiaryID-Generation-API` | Unique beneficiary ID generation |
| `FHIR-API` | FHIR interoperability |
| `Identity-API` | Beneficiary creation and identity management |
| `Identity-1097-API` | Beneficiary identity for the 1097 service |

## Mobile repositories — Android persona

Kotlin Android applications consuming AMRIT REST APIs. They route to `implement-android-change`.

| Repository | Domain |
|---|---|
| `FLW-Mobile-App` | Frontline worker application for ASHA programmes and consultations |
| `HWC-Mobile-App` | HWC workflows for CHOs, doctors, nurses, lab technicians, and pharmacists |

## Infrastructure and tooling repositories

| Repository | Purpose | Persona |
|---|---|---|
| `AMRIT-DB` | Database schema management through Flyway migrations | `implement-database-change` |
| `AMRIT-Docs` | Developer documentation synchronized with GitBook | Research only |
| `AMRIT-DevOps` | Deployment, infrastructure, and DevOps configuration | Out of Stage 05 implementation scope unless the ticket explicitly requires it |
| `AMRIT-Website` | Public AMRIT website | Only when the ticket affects the public website |
| `AMRIT` | Central repository, issue hub, and repository catalog | Research only |

`AMRIT-DB` is the only authoritative home for schema DDL and migrations. No application repository may own them.

## Repository pairs

- `Inventory-UI` ↔ `Inventory-API`
- `MMU-UI` ↔ `MMU-API`
- `TM-UI` ↔ `TM-API`
- `HWC-UI` ↔ `HWC-API`
- `ADMIN-UI` ↔ `Admin-API`
- `HWC-Scheduler-UI` ↔ `Scheduler-API`
- `Scheduler-UI` ↔ `Scheduler-API`
- `HWC-Inventory-UI` ↔ `Inventory-API`
- `ECD-UI` ↔ `ECD-API`
- `Helpline1097-UI` ↔ `Helpline1097-API`
- `Helpline104-UI` ↔ `Helpline104-API`

`Common-UI` and `Common-API` are shared dependencies. Include them only when the requested behaviour actually uses the shared component or integration.

## Building the impact shortlist

1. Start from the repository actually checked out in the working directory.
2. Add the paired UI or API repository when the change crosses that boundary.
3. Add `AMRIT-DB` only when a schema object may change.
4. Add a mobile repository only when the Android application is in scope.
5. Add `Common-UI` or `Common-API` only when shared behaviour is involved.
6. Add identity, FHIR, or beneficiary-ID services only when the business domain requires them.
7. Start with no more than three primary repositories where practical, and expand only when discovered evidence identifies a material dependency.

Record why each repository entered the shortlist and why adjacent repositories were excluded.

## Repository boundary rules

- A repository is in scope only when the ticket, the approved design, or the source evidence puts it there.
- Never modify a repository because a persona exists for it.
- Never modify a repository that is not checked out; report it as inaccessible instead.
- Report changes per repository, and state explicitly which candidate repositories required no change.

## Catalog maintenance

Review this map when the central `PSMRI/AMRIT` README adds, renames, or retires repositories. Reconfirm exact capitalization, pairing, and technology against that source before updating this file.
