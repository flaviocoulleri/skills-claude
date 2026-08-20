<!-- AUTO-COPIADO desde _shared/jira/ — NO EDITAR ACÁ. Edita la fuente en _shared/jira/ y corre _shared/jira/sync.sh. -->

# Jira ProContacto — Campos, picklists y statuses por issuetype

> Fuente de verdad canónica para la familia `pc-delivery-jira-*`. Introspección REST
> en vivo (site `procontacto.atlassian.net`, cloudId `d041f87a-4f5e-40d1-b719-578536318f6a`),
> proyecto muestra **AA200** (classic, usa los schemes org-wide compartidos por ~116-124
> proyectos). Fecha: 2026-07-13.
>
> Complementa: `issuetypes-and-workflows.md` (workflows) y `screen-schemes.md` (screens).
>
> ⚠️ En runtime los skills usan el **conector Atlassian MCP** (no este token). Igual deben
> revalidar contra la org con `getJiraIssueTypeMetaWithFields` antes de crear — el esquema
> puede variar por proyecto; este archivo es la referencia, la org es la verdad.

## Reglas generales (confirmadas)

- **Required de sistema en TODOS los issuetypes**: `Summary` (string), `Project`, `Issue Type`.
- **`Parent` (issuelink) required** SOLO en los issuetypes de tipo subtask:
  **Sub-task (10003)**, **Story Bug (10506)**, **Opportunity for improvement (10539)**.
- Jira `createmeta` **NO marca required** los custom fields aunque el equipo los trate como
  obligatorios → las obligaciones de negocio de PC (ej: Story sin Como/Quiero/Para) las
  impone el skill, no vienen del schema.
- **Custom fields comunes**: `Sprint` = `customfield_10020` (gh-sprint); `Story point estimate`
  = `customfield_10016` (jsw-story-points).
- **Security Level** (campo de sistema `security`) presente en varios: `0 - Internal` / `1 - External`.
- **Story Bug** y **Opportunity for improvement** son **subtasks** (requieren Parent) — no confundir con Bug/tarea suelta.

## IDs de issuetype (proyecto AA200; estables en los proyectos que comparten el scheme)

| id | Issuetype | subtask |
|---|---|---|
| 10000 | Epic | no |
| 10001 | Story | no |
| 10002 | Task | no |
| 10003 | Sub-task | **sí** |
| 10004 | Bug | no |
| 10506 | Story Bug | **sí** |
| 10209 | Artifact | no |
| 10107 | Change Control | no |
| 10243 | Acceptance Certificate | no |
| 10440 | Project Details | no |
| 10109 | Weekly Status | no |
| 10144 | External Pending | no |
| 10308 | Internal Pending | no (JSM) |
| 10143 | Feedback Tracker | no |
| 10539 | Opportunity for improvement | **sí** |
| 10275 | QAlity Test | no |
| 10473 | Exploratory Testing | no |
| 10717 | Incidente Seguridad Informatica | no (JSM) |

---

## Nota: create rápido (compacto) vs formulario completo
El modal compacto de crear muestra solo un **subset "rápido"** de campos fijado por tipo (abajo,
"quick-create"); el formulario completo/edición expone el resto (todo el set está en createmeta).
Validado contra pantallas reales (IMPNTR, 2026-07-13).

## Quick-create por issuetype (validado en pantalla, IMPNTR 2026-07-13)
Todos llevan Title(summary)+Description salvo aclaración. "Set común de acción" = Due date, Assignee
(Automatic), Priority (Medium), Parent, Labels.

| Issuetype | Campos rápidos del create | Status inicial (si confirmado) |
|---|---|---|
| Story | form completo: Como/Quiero/Para/Criterios, Priority, Assignee, Parent, Sprint, Reporter*, Components, Fix versions, Labels, Linked, Due date | **ESPERANDO REFINAMIENTO** |
| Epic | form completo: Parent, Components, Reporter*, Fix versions, Priority, **Team**, Labels, Linked, Assignee, Sprint | **TAREAS POR HACER** |
| Task | set común de acción | — |
| Bug | set común de acción | — |
| Change Control | set común de acción | — |
| Internal Pending | Assignee, Due date, Priority, Labels, Parent | — |
| Incidente Seguridad Inf. | Assignee, Due date, Priority, Labels, Parent | — |
| Feedback Tracker | Due date, Assignee, Priority, Parent, Labels | — |
| External Pending | Sprint, **Owner**, Due date, Assignee, Priority | — |
| Artifact | **Artifact Type**, Parent, Labels, Sprint (Page Link en edición) | — |
| Acceptance Certificate | Sprint, Priority (resto en edición) | — |
| Project Details | **GoLive**, Priority, Labels | — |
| Weekly Status | Sprint, Project Status Report, Risk Level, GoLive, Project End Date | — |
| QAlity Test | Original estimate, Due date, Assignee, Priority, Parent, Labels | **FINALIZADO** |
| Exploratory Testing | Priority, Labels, Due date (mínimo) | — |
| Sub-task / Story Bug / Opportunity for improvement | (subtasks — requieren Parent; ver createmeta) | — |

> Status inicial confirmado solo donde el form lo mostró (Story/Epic/QAlity). Regla de familia:
> **no setear status en el create** — cada issue nace en el inicial de su workflow.

## Detalle por issuetype

### Story (10001) — build
- Custom fields (convención PC, NO required de sistema pero SÍ de negocio):
  - `customfield_10043` **Como: <Rol/Perfil Usuario>** (textarea)
  - `customfield_10044` **Quiero: <Objetivo>** (textarea)
  - `customfield_10045` **Para: <Beneficio>** (textarea)
  - `customfield_10155` **Criterios de Aceptacion** (textarea) — formato DADO/CUANDO/ENTONCES
  - `customfield_10020` Sprint (gh-sprint)
- Statuses: TAREAS POR HACER, EN REFINAMIENTO, ESPERANDO REFINAMIENTO, TAREA EN CURSO, Testing, TESTING FINALIZADO, EN VALIDACIÓN DEL CLIENTE, EN REVISIÓN DEL CLIENTE, OBSERVACIONES DETECTADAS, FINALIZADO, DEPRECADO.
  **Status inicial al crear = `ESPERANDO REFINAMIENTO`** (validado en pantalla real IMPNTR). Regla general
  de la familia: NO setear status en el create — cada issue nace en el estado inicial de su workflow.
- Campos en pantalla de crear (orden real): Title, Description, Como/Quiero/Para/Criterios, Priority
  (default Medium), Assignee (default Automatic), Parent, Sprint, Reporter*(req), Components, Fix versions,
  Labels, Linked work items (dependencias), Due date, Attachment.

### Task (10002) — build
- Custom: `customfield_10016` Story point estimate, `customfield_10020` Sprint.
- Statuses: TAREAS POR HACER, TAREA EN CURSO, FINALIZADO, DEPRECADO.

### Sub-task (10003) — build · SUBTASK
- Required extra: **Parent**.
- Custom: `customfield_10016` Story point estimate, `customfield_10020` Sprint.
- Statuses: TAREAS POR HACER, TAREA EN CURSO, FINALIZADO, DEPRECADO.

### Bug (10004) — build
- Custom: `customfield_10016` Story point estimate, `customfield_10020` Sprint.
- Statuses: TAREAS POR HACER, En análisis, TAREA EN CURSO, Testing, FINALIZADO, DEPRECADO.

### Story Bug (10506) — build · SUBTASK
- Required extra: **Parent**.
- Custom: `customfield_10020` Sprint.
- Statuses: TAREAS POR HACER, En análisis, TAREA EN CURSO, Testing, FINALIZADO, DEPRECADO.

### Epic (10000) — build
- Custom: `customfield_10001` Team (atlassian-team), `customfield_10020` Sprint.
- Statuses: TAREAS POR HACER, TAREA EN CURSO, Change Control Approval, FINALIZADO, DEPRECADO.

### Artifact (10209) — blueprint/entregables  ✅ (era el "Artefacto")
- Quick-create: Description, **Artifact Type**, Parent, Labels, Sprint. ⚠️ **`Page Link` NO está en el create rápido** → se carga en edición (pero el skill igual debe pedirlo: es lo central del entregable).
- `customfield_10158` **Page Link** (url) ← el link al Drive/Figma/Confluence del entregable.
- `customfield_10263` **Artifact Type** (select) — valores = **entregables del Blueprint**:
  `SOW Comercial`, `Presentación de Equipos`, `Cronograma Pre Sprint 0`, `User Story Mapping`,
  `Diccionario de Datos`, `SOW Refinado`, `Documento Técnico`,
  `Roles y Permissions Set Groups (ex Perfiles)`, `Cronograma Post Sprint 0`,
  `Checklist Pasaje a Producción`.
- `customfield_10020` Sprint. Security Level: 0-Internal/1-External.
- Statuses: TAREAS POR HACER, TAREA EN CURSO, EN VALIDACIÓN DEL CLIENTE, FINALIZADO, DEPRECADO.
- 🔗 Fuerte acople con `pc-delivery-blueprint-guide`: cada Artifact Type = un entregable de la metodología.

### Acceptance Certificate (10243) — blueprint/cierre
- Quick-create: Sprint, Priority (mínimo). `Page Link`/`Signed`/`Environment` son de edición.
- `customfield_10158` Page Link (url), `customfield_10230` **Signed** (multicheckboxes, valor `Yes`),
  `customfield_10264` Environment (textfield), `customfield_10020` Sprint.
- Statuses: Pendiente, ENVIADO, APROBADO.

### Project Details (10440) — metadata del proyecto
- Quick-create: Description, **GoLive**, Priority, Labels. `Actual end` es de edición.
- `customfield_10009` Actual end (datetime), `customfield_10161` GoLive (datepicker).
- Statuses: Sprint 0, Ejecucion, HYPERCARE, LISTO PARA ENTREGAR, FINALIZADO.

### Weekly Status (10109) — reporte (lo genera el project-auditor)
- Quick-create: Sprint, Project Status Report, Risk Level, GoLive, Project End Date. `Page Link`/`Notes` en edición.
- `customfield_10158` Page Link (url), `customfield_10159` **Project Status Report** (select:
  `RETRASADO`, `EN RIESGO`, `ON TRACK`), `customfield_10160` **Risk Level** (select: `ALTO`,
  `MEDIO`, `BAJO`), `customfield_10161` GoLive, `customfield_10162` Project End Date,
  `customfield_10163` Notes (textarea), `customfield_10020` Sprint.
- Statuses: FINALIZADO.

### External Pending (10144) — tracking cliente (dueño: pc-delivery-jira-pending-tracker)
- `customfield_10197` **Owner** (select: `ProContacto`, `Customer`, `ProContacto and Customer`),
  `customfield_10020` Sprint.
- Statuses: TAREAS POR HACER, TAREA EN CURSO, EN VALIDACIÓN DEL CLIENTE, FINALIZADO, DEPRECADO.

### Feedback Tracker (10143) — gobierno
- Quick-create: Description, Due date, Assignee (Automatic), Priority, Parent, Labels (se usa como tarea con padre).
- Custom: `customfield_10016` Story point estimate, `customfield_10020` Sprint.
- Statuses (muchos): Abierto, En análisis, En curso, Listo en dev, EN TESTING, Listo para testing/pruebas,
  OBSERVACIONES DETECTADAS, En espera de información, En pausa, Resuelto, Limitante Salesforce, Futura Fase, Desestimado.

### Change Control (10107) — control de cambios (workflow tipo JSM)
- Custom: `customfield_10016` Story point estimate, `customfield_10020` Sprint.
- Statuses: TODO, En curso, Resolved, Reopened, Closed.

### Opportunity for improvement (10539) — gobierno · SUBTASK
- Required extra: **Parent**. `customfield_10165` Fecha de vencimiento (datepicker).
- Statuses: TAREAS POR HACER, TAREA EN CURSO, FINALIZADO, DEPRECADO.

### QAlity Test (10275) / Exploratory Testing (10473) — QA
- QAlity: `customfield_10020` Sprint; statuses: FINALIZADO (mínimo).
- Exploratory: sin custom fields propios; statuses: TAREAS POR HACER, TAREA EN CURSO, FINALIZADO.

### Internal Pending (10308) / Incidente Seguridad Informatica (10717) — JSM (service desk)
- Usan campos de Jira Service Management: Organizations, Approvers, Request Type, Request participants,
  Satisfaction, Approver groups, Request language, Sprint.
- Statuses: TODO, En curso, Resolved, Reopened, Closed.
- ⚠️ Son colas de servicio/soporte — probablemente FUERA del alcance del issue-builder de delivery.

---

## Módulos del sistema = **Epics** (mecanismo real en PC) · Components = secundario

**CORRECCIÓN validada en pantalla (IMPNTR/proy-nutracom, 2026-07-13):** en PC los **módulos del
sistema se modelan como Epics**, NO como Components. Ejemplo real de Epics = módulos:
`Gestión de Leads`, `Gestión de Cuentas (B2B)`, `Gestión de Contactos`, `Visualización de Productos`,
`Gestión de Listas de Precios`, `Gestión de Cartera y Productividad del Ejecutivo`,
`Reportes y Dashboards Operativos`, `Gestión de Oportunidades`, `Gestión de Cotizaciones`,
`Gestión de Pedidos`… + un Epic **`Artefactos - <proyecto>`** que agrupa los issues `Artifact`.
- **Convención de naming de Epic-módulo**: `Gestión de <Dominio>` (dominios CRM típicos arriba).
- Los **Artifacts** cuelgan (parent) del Epic `Artefactos - <proyecto>`.
- Implicancia para los skills: el nivel Epic del backlog-builder = los módulos; la Story se asocia al
  módulo vía su `parent` (Epic), no vía Components.

**Components** (campo `components`, en pantalla de Story y Epic): existe pero **adopción casi nula**
(barrido 2026-07-13: 1/40 proyectos — BER). Es un eje **secundario/opcional**; NO empujarlo como el
mecanismo de módulos (eso lo cubren los Epics). Ofrecerlo solo si el PM ya lo usa o lo pide.
API si aplica: `GET /rest/api/3/project/{key}/components`, `POST /rest/api/3/component`,
asignar `components:[{name}]`.

## Dependencias entre issues (issue links) + jerarquía

Dos cosas distintas:
- **Jerarquía**: `parent` (issuelink field) — Epic←Story, Story←Sub-task. Es el `parent` del create, NO un issue link.
- **Dependencias / relaciones**: campo `issuelinks` ("Linked Issues", en la pantalla de Story/Epic, opcional).
  Se crean con `POST /rest/api/3/issueLink` `{type:{name:"<tipo>"}, inwardIssue:{key}, outwardIssue:{key}}`
  (si el MCP no expone un tool de links, usar `fetch` a ese endpoint, como con la Agile API).

**10 tipos de link definidos en la org** (name → outward / inward):
| Tipo | outward | inward | Uso en PC |
|---|---|---|---|
| **Dependencia** | Es requerido para los siguientes issues | Se requiere primero | **dependencia funcional canónica (PC, en español)** |
| **Blocks** | blocks | is blocked by | bloqueo duro |
| **QAlity Test** | tests | is tested by | ata QAlity Test / Exploratory Testing → Story |
| Relates | relates to | relates to | relación genérica |
| Duplicate | duplicates | is duplicated by | dedup |
| Cloners | clones | is cloned by | — |
| Problem/Incident | causes | is caused by | incidentes |
| Post-Incident Reviews | reviews | is reviewed by | incidentes |
| Work item split | split to | split from | partición |
| Polaris work item link | implements | is implemented by | Polaris |

Guía para las skills: para "A necesita que B esté primero" usar **`Dependencia`** (A inward "Se requiere primero" B),
o **`Blocks`** para bloqueo. No inventar tipos; elegir de esta tabla.

## Notas de uso para los skills
- **⚠️ ADF obligatorio**: los campos de texto largo — `description` (sistema) y TODOS los custom
  `textarea` (ej. Story: Como/Quiero/Para/Criterios cf_10043/44/45/155; Weekly Status Notes cf_10163)
  — deben enviarse en **Atlassian Document Format** (`{"type":"doc","version":1,"content":[...]}`),
  NO como string plano (la API v3 rechaza con "not valid ADF content"). Multilínea = un `paragraph`
  por línea (ADF no admite `\n` dentro de `text`). Verificado en smoke test 2026-07-13 (ZCLAUDE-8).
  El `customfield_*` de tipo `select`/`url`/`date`/`number` sí acepta valor plano.
- **Transiciones**: los statuses de acá son los estados del workflow; las transiciones concretas
  (y sus ids) se obtienen en runtime con `getTransitionsForJiraIssue` sobre un issue real.
- **Picklists**: NUNCA inventar valores; usar los de este archivo y revalidar con
  `getJiraIssueTypeMetaWithFields` (allowedValues) por si cambian.
- **Owned por otros skills**: External Pending → pending-tracker; Weekly Status → project-auditor;
  horas/worklog → worklog-tracker.
