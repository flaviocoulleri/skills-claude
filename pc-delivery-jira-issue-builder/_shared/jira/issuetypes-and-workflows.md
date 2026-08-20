<!-- AUTO-COPIADO desde _shared/jira/ — NO EDITAR ACÁ. Edita la fuente en _shared/jira/ y corre _shared/jira/sync.sh. -->

# Jira ProContacto — Issuetypes (Work Types) y sus Workflows

> Fuente de verdad canónica. La consumen todos los skills `pc-delivery-jira-*`.
> Ningún skill debe inventar issuetypes ni asumir workflows fuera de esta tabla.
> Última actualización: 2026-07-13 (inventario provisto por Ariel desde la config de Jira).
>
> ✅ Introspección completada (2026-07-13, REST). Campos + picklists + statuses por
> issuetype en `fields-by-issuetype.md`; screens en `screen-schemes.md`.
> Site `procontacto.atlassian.net`, cloudId `d041f87a-4f5e-40d1-b719-578536318f6a`.

## Tabla issuetype → workflow

| Issuetype (Work Type) | Workflow | Categoría |
|---|---|---|
| Incidente Seguridad Informatica | `Jira Workflow (jira)` (default) | Seguridad |
| Internal Pending | `Jira Workflow (jira)` (default) | Tracking interno |
| Acceptance Certificate | `0 - Implementation Acceptance Certificate v1` | Blueprint / cierre |
| Feedback Tracker | `0 - Implementation Feedback v1` | Gobierno |
| Bug | `0 - Implementation Workflow Bug v2` | Build |
| Change Control | `0 - Implementation Workflow Change Control v1` | Gobierno / control de cambios |
| Artifact | `0 - Implementation Workflow Deliverable v1` | Blueprint / entregables |
| Epic | `0 - Implementation Workflow Epic v2` | Build |
| Exploratory Testing | `0 - Implementation Workflow Exploratory Testing v1` | QA |
| External Pending | `0 - Implementation Workflow External Pending v2` | Tracking cliente |
| Opportunity for improvement | `0 - Implementation Workflow Opportunity for improvement v1` | Gobierno |
| Project Details | `0 - Implementation Workflow Project Details v3` | Blueprint / metadata proyecto |
| QAlity Test | `0 - Implementation Workflow QAlity v4` | QA |
| Story Bug | `0 - Implementation Workflow Story Bug v2` | Build |
| Task | `0 - Implementation Workflow Task v4` | Build |
| Sub-task | `0 - Implementation Workflow Task v4` (compartido) | Build |
| Story | `0 - Implementation Workflow User Story v5` | Build |
| Weekly Status | `0 - Implementation Workflow Weekly Status v1` | Blueprint / reporte |

La mayoría de los workflows son **shared by ~123-124 projects** → esquema estandarizado
a nivel org, no por-proyecto. Cambios de workflow impactan a toda la operación.

## Agrupación por dominio (para el ruteo de skills de escritura)

- **Build (backlog / sprint):** Epic, Story, Sub-task, Task, Bug, Story Bug
- **QA:** QAlity Test, Exploratory Testing
- **Tracking:** External Pending (cliente), Internal Pending (interno)
- **Blueprint / documentos:** Artifact (workflow "Deliverable"), Acceptance Certificate,
  Project Details, Weekly Status
- **Gobierno / cambios:** Change Control, Opportunity for improvement, Feedback Tracker
- **Seguridad:** Incidente Seguridad Informatica

## Mapa issuetype → skill responsable

| Issuetype | Skill que escribe |
|---|---|
| Epic, Story, Sub-task, Task, Bug, Story Bug | `pc-delivery-jira-issue-builder` (CRUD) + `pc-delivery-jira-backlog-builder` (desglose masivo) |
| Sprints (no es issuetype) | `pc-delivery-jira-sprint-manager` |
| fixVersions / releases (no es issuetype) | `pc-delivery-jira-release-manager` |
| External Pending | `pc-delivery-jira-pending-tracker` (ya existe) |
| Artifact | `pc-delivery-jira-project-auditor` / `pc-delivery-blueprint-guide` (ya existen) |
| QAlity Test, Exploratory Testing | (a decidir — ¿cubre issue-builder o skill QA aparte?) |
| Change Control, Opportunity for improvement, Feedback Tracker, Acceptance Certificate, Project Details, Weekly Status | (a decidir — issue-builder genérico vs skills dedicados) |
| Incidente Seguridad Informatica, Internal Pending | (a decidir) |

## ⚠️ Bug confirmado en vivo — `Artifact` (no `Artefacto`)

Introspección REST: el issuetype real es **`Artifact`** (id `10209`), su link vive en
`customfield_10158` (Page Link) y su tipo en `customfield_10263` (Artifact Type, cuyos
valores son los entregables del Blueprint). Las JQL que filtran `issuetype = "Artefacto"`
**fallan con error de validación** → `pc-delivery-jira-project-auditor` (Q6),
`pc-delivery-blueprint-guide` (context load) y a revisar `pc-delivery-sf-project-builder`
nunca encuentran los artefactos. Fix flagueado como tarea aparte. Detalle en `fields-by-issuetype.md`.
