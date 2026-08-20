# Mapeo issuetype → fields + convenciones (issue-builder)

> El esquema real (fields, `customfield_*` ids, picklists, statuses) es canónico y vive en
> **`_shared/jira/fields-by-issuetype.md`** — leerlo ahí, no duplicar. En runtime revalidar
> con `getJiraIssueTypeMetaWithFields` (la org es la verdad).
>
> Este archivo solo agrega las **obligaciones de negocio y convenciones de contenido** que el
> issue-builder impone por encima de los required de sistema de Jira.

## Required de sistema (recordatorio)
Solo `Summary` + `Project` + `Issue Type` en todos; **`Parent`** además en subtasks:
Sub-task, Story Bug, Opportunity for improvement.

## Obligaciones de NEGOCIO por issuetype (las impone el skill, no el schema)

### Story (10001) — validado contra la pantalla real (IMPNTR, 2026-07-13)
**Orden canónico de la pantalla de crear** (el widget arma `fields` en ESTE orden):
1. `summary` (Title) *req* · 2. `description` (ADF, opcional) · 3. `customfield_10043` Como *
· 4. `customfield_10044` Quiero * · 5. `customfield_10045` Para * · 6. `customfield_10155` Criterios *
(ADF rich text, DADO/CUANDO/ENTONCES) · 7. `priority` (default **Medium**) · 8. `assignee`
(default **Automatic**) · 9. `parent` (Epic) · 10. `customfield_10020` Sprint · 11. `reporter`
**REQUIRED** (default=usuario) · 12. `components` (módulos) · 13. `fixVersions` · 14. `labels`
· 15. `issuelinks` (dependencias) · 16. `duedate`.
- (* = obligación de NEGOCIO: pedir Como/Quiero/Para/Criterios aunque Jira no los marque required.)
- **Status inicial al crear = `ESPERANDO REFINAMIENTO`** (NO "To Do"): no setear status en el create;
  nace ahí por el workflow User Story v5. (En ZCLAUDE salía "To Do" por tener el workflow default.)
- Alinear contenido con `pc-crm-userstory-generator`. Summary = título imperativo corto.

### Artifact (10209)
- Quick-create real: Description, Artifact Type, Parent, Labels, Sprint.
- `customfield_10158` Page Link (url) — OBLIGATORIO de negocio (un Artifact sin link no sirve).
  ⚠️ En Jira nativo NO está en el create rápido (se carga en edición); el skill lo pide igual en el mismo paso — es una MEJORA sobre el flujo manual, no una desviación.
- `customfield_10263` Artifact Type (select) — OBLIGATORIO; elegir de los 10 valores del Blueprint
  (SOW Comercial, User Story Mapping, Diccionario de Datos, SOW Refinado, Documento Técnico,
  Roles y Permissions Set Groups, Cronograma Pre/Post Sprint 0, Presentación de Equipos,
  Checklist Pasaje a Producción). Ver valores exactos en el shared.
- Handoff natural a/desde `pc-delivery-blueprint-guide`.

### Acceptance Certificate (10243)
- Page Link (10158) + Environment (10264); `Signed` (10230) solo al aprobar.

### Bug / Story Bug (10004 / 10506)
- Description con pasos para reproducir + esperado vs actual. Story Bug requiere Parent (la Story afectada).

### Sub-task (10003)
- Requiere Parent. Heredar Sprint del padre salvo indicación contraria.

### Epic (10000) / Task (10002)
- Sin obligaciones extra más allá del summary claro.

### Módulos = Epics (no Components) — recomendación de estructura
- En PC los **módulos del sistema son Epics** (`Gestión de <Dominio>`), no Components. Recomendar que
  cada Story cuelgue (parent) de su Epic-módulo. Los **Artifacts** cuelgan del Epic `Artefactos - <proyecto>`.
- **Components** existe en Story/Epic pero casi no se usa → eje secundario; ofrecerlo solo si el PM ya lo usa.
- Detalle y ejemplo de módulos en `_shared/jira/fields-by-issuetype.md`.

## Fuera de alcance del issue-builder (derivar)
- **External Pending** → `pc-delivery-jira-pending-tracker`.
- **Weekly Status** → `pc-delivery-jira-project-auditor` (lo genera él).
- **Internal Pending / Incidente Seguridad Informatica** → colas JSM de soporte/seguridad (no delivery).
- Horas/worklog → `pc-delivery-jira-worklog-tracker`.
