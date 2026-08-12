# AMRIT Repository Catalog

## Contents

- [Catalog authority and naming](#catalog-authority-and-naming)
- [UI repositories](#ui-repositories)
- [API repositories](#api-repositories)
- [Mobile application repositories](#mobile-application-repositories)
- [Infrastructure and tooling repositories](#infrastructure-and-tooling-repositories)
- [Repository relationships](#repository-relationships)
- [Repository shortlist guidance](#repository-shortlist-guidance)
- [Catalog maintenance](#catalog-maintenance)

## Catalog authority and naming

- **GitHub organization/owner:** PSMRI
- **Platform:** AMRIT
- **DeepWiki repository identifier format:** `PSMRI/<repository-name>`
- **Catalog source of truth:** [Central PSMRI/AMRIT README](https://github.com/PSMRI/AMRIT/blob/main/README.md)

This catalog reflects the AMRIT repository list from the central `PSMRI/AMRIT` README. Use every repository name with its exact GitHub capitalization. Treat the catalog as repository-discovery metadata, not evidence of a repository's internal architecture. Confirm internal components through retrieved repository evidence before labelling them Confirmed.

## UI repositories

All UI repositories are Angular applications.

| Repository | Domain / responsibility | Primary paired API | Technology | Architecture keywords | Local development port |
|---|---|---|---|---|---|
| `Inventory-UI` | Inventory management | `Inventory-API` | Angular | inventory, stock, medicine, dispensing, prescription, pharmacy | 4201 |
| `Common-UI` | Shared UI components used across service lines | Multiple AMRIT APIs | Angular | shared components, common UI, forms, authentication, reusable controls | - |
| `MMU-UI` | Mobile Medical Unit | `MMU-API` | Angular | MMU, beneficiary, consultation, examination, sync, mobile medical unit | 4202 |
| `TM-UI` | Telemedicine centres | `TM-API` | Angular | telemedicine, specialist, consultation, video consultation | 4203 |
| `HWC-UI` | Health and Wellness Centre | `HWC-API` | Angular | HWC, consultation, doctor, nurse, lab, pharmacist | 4204 |
| `ADMIN-UI` | Deployment configuration management for administrators | `Admin-API` | Angular | admin, configuration, master data, users, deployment settings | 4205 |
| `HWC-Scheduler-UI` | Appointment schedule management for HWC | `Scheduler-API` | Angular | HWC, appointment, schedule, slot, calendar | 4206 |
| `HWC-Inventory-UI` | HWC inventory management | `Inventory-API` | Angular | HWC, inventory, pharmacy, medicine, stock | 4207 |
| `Scheduler-UI` | Appointment schedule management | `Scheduler-API` | Angular | appointment, schedule, slot, calendar, specialist | 4208 |
| `ECD-UI` | Early Childhood Development application | `ECD-API` | Angular | ECD, early childhood development, call centre, sync, child | 4209 |
| `Helpline1097-UI` | 1097 health information helpline | `Helpline1097-API` | Angular | 1097, HIV, AIDS, helpline, call centre, telephony | 4210 |
| `Helpline104-UI` | 104 health information helpline | `Helpline104-API` | Angular | 104, health helpline, call centre, telephony | 4211 |

## API repositories

All API repositories are Spring Boot services.

| Repository | Domain / responsibility | Technology | Architecture keywords | Local development port |
|---|---|---|---|---|
| `FLW-API` | REST APIs for the FLW mobile application | Spring Boot | FLW, frontline worker, ASHA, pregnancy, mother, newborn, mobile | 8081 |
| `Admin-API` | Configuration management for AMRIT deployments | Spring Boot | admin, configuration, master data, deployment, users | 8082 |
| `Common-API` | Shared AMRIT services and integrations | Spring Boot | common services, shared integrations, DMS, call centre integration | 8083 |
| `ECD-API` | Early Childhood Development call-centre services and ECD UI backend | Spring Boot | ECD, early childhood development, call centre, child, sync | 8084 |
| `HWC-API` | Health and Wellness Centre backend services | Spring Boot | HWC, consultation, doctor, nurse, lab, pharmacist | 8085 |
| `Inventory-API` | Medicine inventory and dispensing | Spring Boot | inventory, medicine, stock, prescription, dispensing, pharmacy | 8086 |
| `MMU-API` | REST APIs for Mobile Medical Unit deployments and UI | Spring Boot | MMU, beneficiary, consultation, examination, sync | 8087 |
| `Scheduler-API` | Specialist consultation appointment scheduling | Spring Boot | schedule, appointment, specialist, slot, cancellation, day view | 8088 |
| `TM-API` | Telemedicine backend services | Spring Boot | telemedicine, specialist, consultation, video consultation | 8089 |
| `Helpline1097-API` | 1097 AIDS health information helpline | Spring Boot | 1097, HIV, AIDS, helpline, telephony | 8090 |
| `Helpline104-API` | 104 health information helpline | Spring Boot | 104, health helpline, call centre, telephony | 8091 |
| `BeneficiaryID-Generation-API` | Generation and management of unique beneficiary IDs | Spring Boot | beneficiary ID, identifier, identity, generation | 8092 |
| `FHIR-API` | Healthcare interoperability using the FHIR standard | Spring Boot | FHIR, interoperability, health information exchange, standards | 8093 |
| `Identity-API` | Beneficiary creation and identity management | Spring Boot | beneficiary, identity, profile, demographic data | 8094 |
| `Identity-1097-API` | Beneficiary identity management for the 1097 service | Spring Boot | 1097, beneficiary, identity, profile | 8095 |

## Mobile application repositories

The mobile applications are built with Kotlin and use AMRIT REST APIs.

| Repository | Domain / responsibility | Technology | Architecture keywords |
|---|---|---|---|
| `FLW-Mobile-App` | Frontline worker Android application for healthcare programs and consultations delivered by ASHAs | Kotlin / Android | FLW, ASHA, pregnancy, mothers, newborns, offline, sync, mobile |
| `HWC-Mobile-App` | HWC mobile workflows for CHOs, doctors, nurses, lab technicians and pharmacists | Kotlin / Android | HWC, CHO, doctor, nurse, lab, pharmacist, offline, sync |

## Infrastructure and tooling repositories

| Repository | Purpose | When the technical-design skill should inspect it | Architecture keywords |
|---|---|---|---|
| `AMRIT-Docs` | AMRIT developer documentation synchronized with GitBook | Architecture guidance, development conventions, or system documentation is required | documentation, architecture, development guide, GitBook |
| `AMRIT-DB` | Database schema management through Flyway migrations | The ticket may change tables, columns, indexes, constraints, migrations, or seed data | Flyway, schema, migration, DDL, database, index, constraint |
| `AMRIT-Website` | Public AMRIT website | The ticket specifically affects the AMRIT public website | website, public portal, content |
| `AMRIT-DevOps` | AMRIT deployment, infrastructure, and DevOps configuration | Deployment, environment variables, containers, CI/CD, infrastructure, or operational configuration may change | DevOps, deployment, Docker, CI/CD, infrastructure, configuration |
| `AMRIT` | Central AMRIT repository, issue-tracking hub, and repository catalog | Repository relationships, central project context, or contribution guidance is required | issue tracking, repository catalog, contributor guidance, platform overview |

## Repository relationships

Common UI/API pairs:

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

`Common-UI` and `Common-API` may be shared dependencies across multiple service lines. Include them only when the requested behavior uses shared components or integrations.

Consider `AMRIT-DB` when database persistence may change. Consider `AMRIT-DevOps` only when deployment, infrastructure, environment, or configuration impact exists.

## Repository shortlist guidance

Build the shortlist from:

- the service line or product named in Jira;
- acceptance-criteria terminology;
- BRD and FRD terminology;
- Confluence findings;
- API names;
- module names;
- domain and database entities;
- UI screens;
- integration names.

Never search every catalog repository by default.

1. Start with the primary UI/API pair.
2. Add `Common-UI` or `Common-API` only when shared behavior or integrations are relevant.
3. Add `AMRIT-DB` only when schema or persistence impact is plausible.
4. Add `AMRIT-DevOps` only when deployment or configuration impact is plausible.
5. Add identity, FHIR, or beneficiary-ID services only when the business domain requires them.
6. Start with no more than three primary repositories where practical.
7. Expand the shortlist only when repository evidence reveals a material dependency.

Document why each repository entered the shortlist and why adjacent repositories were excluded. Catalog keywords help discovery; they do not prove impact.

## Catalog maintenance

Review this catalog when the central `PSMRI/AMRIT` README adds, renames, or retires repositories. Reconfirm exact capitalization, relationships, technologies, and ports against that source before updating this file.
