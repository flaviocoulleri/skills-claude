# JQL queries del PASO 2 — diagnóstico

Las 6 queries que ejecuta el skill en paralelo durante PASO 2, más el pre-step de detección de issue types recurrentes y los fallback en caso de orgs sin ScriptRunner.

## Pre-step — detectar el active sprint (afecta Q1-Q5)

Desde v1.13.2 las queries Q1-Q5 excluyen issues de sprints futuros por default. PC trabaja sprint a sprint — los issues planificados para sprints siguientes típicamente no tienen assignee/duedate/release y eso es esperable, no un hallazgo.

Antes de armar las queries, detectar el active sprint del proyecto:

```
GET /rest/agile/1.0/board/<BOARD_ID>/sprint?state=active
```

(El `BOARD_ID` se descubrió antes en el flow de creación de sprints — ver `sprint-planning.md`. Si no se descubrió todavía, hacerlo acá.)

Resultado posible:

- **Hay un active sprint** — usar su id como `<active_sprint_id>` y agregar a Q1-Q5: `AND (sprint = "<active_sprint_id>" OR sprint IS EMPTY)`. El "sprint IS EMPTY" incluye los issues del backlog sin sprint, que SÍ son hallazgos válidos (representan trabajo a refinar).
- **No hay active sprint** (proyecto en Sprint 0, entre sprints, o board sin sprints) — agregar a Q1-Q5: `AND sprint IS EMPTY`. Sólo backlog.
- **Toggle "Incluir sprints futuros" prendido por el PM en PASO 1.3** — omitir la cláusula completa. Las queries Q1-Q5 traen todo `statusCategory != Done`, incluyendo sprints futuros. Útil sólo en auditorías exhaustivas previas a un milestone.

Esta cláusula se inyecta en cada query Q1-Q5 antes del `ORDER BY` o final. Q6 (artefactos huérfanos) y Q7 (sin worklog) NO se ven afectadas — Q6 trabaja sobre el issue type y Q7 ya filtra a `statusCategory = "In Progress"` (issues en curso real).

## Pre-step — detectar issue types recurrentes (afecta Q3 y Q5)

Antes de correr Q3 y Q5, llamar `getJiraProjectIssueTypesMetadata` y construir el set `recurringTypes`: los issue types cuyo `name` matchea (case-insensitive) la regex `weekly|daily|status|recurring|standup`. Estos types existen para ritos de proyecto (ej: `Weekly Status`) y por su naturaleza no llevan `duedate` ni `fixVersion` — incluirlos en Q3/Q5 genera falsos positivos.

Si el set está vacío, Q3 y Q5 corren sin la cláusula extra. Si tiene uno o más types, se inyectan como `issuetype NOT IN (...)`.

> **Por qué este pre-step**: descubierto en el dry-run del proyecto AIREDSNS — un proyecto con issue type `Weekly Status` registraba 15 falsos positivos en Q3/Q5 porque las weeklies estaban como `Task` (mistype del usuario), pero la lección aplica al revés también: cuando el type **se usa correctamente**, igualmente no debería caer en Q3/Q5.

## Q1 — Sin asignar

```jql
project = "<KEY>" AND assignee IS EMPTY AND statusCategory != Done
```

## Q2 — Vencidas

```jql
project = "<KEY>" AND duedate < now() AND statusCategory != Done
```

## Q3 — Sin fecha

```jql
project = "<KEY>" AND duedate IS EMPTY
  AND issuetype IN (Story, Task, Bug, "Sub-task") AND statusCategory != Done
  [AND issuetype NOT IN (<recurringTypes>) -- sólo si el set no está vacío]
```

Excluye Epic intencionalmente (los Epics no siempre tienen fecha en el modelo PC) y los types recurrentes detectados en el pre-step.

### Q3.b — Posible mistype (sub-detección informativa)

Sobre los resultados de Q3, aplicar regex `weekly|daily|status|recurring|standup` (case-insensitive) sobre `summary`. Los issues que matcheen y cuyo `issuetype` **no esté** en `recurringTypes` se flagean como **"posible mistype"** — son probablemente weeklies/dailies mal clasificadas como Task/Story.

No se propone fix automático: el cambio correcto es reclasificar el `issuetype`, y el skill nunca toca ese campo. Se reportan en una sub-categoría informativa con la sugerencia "reclasificar manualmente desde la UI".

## Q4 — Bloqueadas por algo abierto

```jql
project = "<KEY>" AND statusCategory != Done
  AND issueFunction IN linkedIssuesOf("statusCategory != Done", "is blocked by")
```

`issueFunction` requiere ScriptRunner en algunos orgs. Si la query falla con error de sintaxis, fallback: traer todos los issues abiertos con `searchJiraIssuesUsingJql` con `expand=issuelinks` y filtrar en memoria los que tienen `inwardIssue` con `type.name = "Blocks"` y status abierto. Más caro pero universal.

## Q5 — Sin release

```jql
project = "<KEY>" AND fixVersion IS EMPTY
  AND issuetype IN (Story, Task, Bug) AND statusCategory != Done
  [AND issuetype NOT IN (<recurringTypes>) -- sólo si el set no está vacío]
```

### Q5.b — Posible mistype (sub-detección informativa)

Misma lógica que Q3.b sobre los resultados de Q5. Issues que matcheen el regex en `summary` y no estén en un type recurrente se flagean como mistype informativo.

## Q7 — Sin worklog (en progreso sin tiempo cargado)

```jql
project = "<KEY>"
  AND statusCategory = "In Progress"
  AND timespent IS EMPTY
  AND assignee IS NOT EMPTY
  AND issuetype IN (Story, Task, Bug, "Sub-task")
  AND status CHANGED TO ("In Progress", "En curso", "En desarrollo") BEFORE -3d
```

**Por qué este filtro tan estricto**: queremos detectar issues que llevan trabajo real sin trazabilidad de tiempo. Las que entraron hoy a "In Progress" todavía pueden estar arrancando. Las que están en "To Do" todavía no se trabajan. El filtro de `>3 días en in-progress sin worklog` aísla el set genuinamente preocupante.

**Categoría asignada**: `no_worklog`. **Color del badge**: `c-amber` (mismo que `no_date`, son issues en zona gris).

**Cruce con "Seguimiento al equipo" de Slack**: este hallazgo se suma al contador de la categoría `team_followup_pending` (junto con `no_estimate` y `overdue`). El botón global "Mandar follow-up al equipo por Slack ↗" cubre las 3 razones — la plantilla de DM agrega la línea correspondiente según motivo. Detalle en `slack-integration.md`.

**Fix individual**: botón por fila "Pedir worklog ↗" que dispara DM al assignee pidiéndole que cargue las horas trabajadas hasta ahora.

## Q6 — Artefactos huérfanos

```jql
project = "<KEY>" AND issuetype = "Artifact"
```

Si el issue type "Artifact" no existe en el proyecto (verificar con `getJiraProjectIssueTypesMetadata`), saltar Q6 y avisar:
> "El proyecto no tiene issue type 'Artifact'. Salto la categoría."

Para los issues que sí vuelven, el URL del artefacto vive en **`customfield_10158` (Page Link, url)** y el tipo en **`customfield_10263` (Artifact Type, select)** — confirmado por introspección (`_shared/jira/fields-by-issuetype.md`). Fallback si el id difiere en el sitio: descubrirlo con `getJiraIssueTypeMetaWithFields` para "Artifact" (field tipo `url`). Cachear el `customfield_XXXXX` resultante.

Para cada artefacto, validar la URL contra los dominios permitidos (`drive.google.com` o `figma.com`) — ver reglas en SKILL.md sección "Reglas para sugerir fixes".
