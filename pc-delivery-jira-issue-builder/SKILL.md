---
name: pc-delivery-jira-issue-builder
metadata:
  version: 0.3.0
  last_modified: 2026-08-06
  status: beta
description: >
  Crea y edita issues en Jira ProContacto respetando el issuetype y sus
  required/custom fields reales (Story, Task, Sub-task, Bug, Story Bug, Epic,
  Artifact, Change Control, Acceptance Certificate, etc.); linkea, comenta y
  transiciona de a un issue con OK explícito. NO es un formulario: ofrece revisar el contexto
  con conectores (Gmail, Calendar, Drive, Confluence, Slack, ReadAI, Salesforce), recomienda
  con el porqué y empuja a completar el proyecto. Es el núcleo de escritura de la
  familia pc-delivery-jira-*. Activar cuando el usuario diga "crea un issue",
  "carga una historia/tarea/bug en Jira", "edita el issue PROJ-123",
  "linkea estos issues", "comenta en el ticket", "cambia el estado de",
  "crear epic", "sube esta HU a Jira". NO borra issues ni hace transiciones
  masivas automáticas (eso queda en pc-delivery-jira-project-auditor, con OK
  fila por fila). Confirma por widget antes de cada escritura (gate pre/post-write,
  nunca sin OK). Orientado a PMs, Scrum Masters y devs. Funciona en español e inglés.
---

<!-- Changelog
0.2.0 (2026-07-13): Introspección REST completa → esquema real cableado (fields, picklists,
statuses por issuetype en _shared/jira/fields-by-issuetype.md). Bug Artifact confirmado (id 10209).
Widget de confirmación PASO 4 (assets/confirm-issue.html) construido y smoke-testeado en preview
(render, bloqueo de required, payload JSON con customfield_* correctos, cancelar). Sigue DRAFT:
faltan issue links, widget de handoff, ratificación meta + smoke test end-to-end real + .skill.
0.1.0 (2026-07-13): ESQUELETO / DRAFT — estructura y flujo sobre el inventario de
issuetypes+workflows de _shared/jira/; fields como TODO hasta la introspección.
-->

# Skill: Creación y edición de issues en Jira (núcleo de escritura)

## Descripción

CRUD conversacional de issues de Jira ProContacto para PMs, Scrum Masters y devs.
Es el **núcleo** del que dependen `pc-delivery-jira-backlog-builder` (desglose masivo),
`pc-delivery-jira-sprint-manager` y `pc-delivery-jira-release-manager`: todos delegan
acá la escritura de issues individuales.

Cubre:
1. **Crear** un issue de cualquier issuetype, respetando los required/custom fields de ese tipo.
2. **Editar** campos de un issue existente.
3. **Linkear** issues entre sí (blocks, relates, etc.) y a Epics (parent).
4. **Comentar**.
5. **Transicionar** un issue de a uno, con OK explícito (respetando su workflow).

> 🧪 **BETA — en pruebas con el equipo delivery.** Esquema real cableado y validado end-to-end; se está afinando el runtime. Reporta lo que encuentres. Ver TODO al final.

## Alcance y límites (decisión de diseño)

- **SÍ**: crear, editar, linkear, comentar, transicionar 1×1.
- **NO**: borrar issues (nunca).
- **NO**: transiciones/ediciones masivas automáticas → eso vive en `pc-delivery-jira-project-auditor` con OK fila por fila.
- **NO**: External pending del cliente → `pc-delivery-jira-pending-tracker` es el dueño de ese issuetype.
- **NO**: cargar horas/worklog → `pc-delivery-jira-worklog-tracker`.
- **NO**: crear/gestionar sprints ni releases → `sprint-manager` / `release-manager` (delegan acá para issues sueltos).

## Fuente de verdad del esquema

Este skill **NO inventa** issuetypes, fields ni transiciones. Lee:
- `_shared/jira/issuetypes-and-workflows.md` — issuetype ↔ workflow (18 tipos, IDs).
- `_shared/jira/fields-by-issuetype.md` — required + custom fields + picklists + statuses (introspectado en vivo 2026-07-13).
- `_shared/jira/screen-schemes.md` — screen scheme por issuetype.
- `references/issuetype-field-mapping.md` — obligaciones de negocio/convenciones que impone el skill por encima del schema.

Además, en runtime valida contra la org real con `getJiraIssueTypeMetaWithFields`
antes de crear (el esquema puede variar por proyecto; el archivo es la referencia, la org es la verdad).

## Principio rector (NO es un formulario)

Este skill implementa el contrato de familia `_shared/jira/context-and-completeness.md`:
actúa como un PM/BA senior que **ofrece revisar el contexto con conectores**, **recomienda con
el porqué** y **empuja la completitud del proyecto** — no solo escribe lo que el PM tipea.
Leer ese archivo es obligatorio antes de operar.

## Herramientas requeridas

- **Atlassian MCP**: `getAccessibleAtlassianResources`, `atlassianUserInfo`,
  `getVisibleJiraProjects`, `getJiraProjectIssueTypesMetadata`,
  `getJiraIssueTypeMetaWithFields`, `createJiraIssue`, `editJiraIssue`,
  `searchJiraIssuesUsingJql`, `addCommentToJiraIssue`, `getTransitionsForJiraIssue`,
  `transitionJiraIssue`, `getJiraIssue`. (Issue links vía `editJiraIssue`/REST según soporte del MCP.)
- **Widgets**: `mcp__visualize__show_widget` (revisión/confirmación chat-inline, patrón de la casa).
- **Conectores de contexto (opcionales, degradan en silencio)**: Gmail, Google Calendar,
  Drive, Confluence, Slack, ReadAI/Meet (transcripts), Salesforce (`Project__c`, Opportunity,
  Quote, `Project_Asset__c`) — para pre-llenar campos y detectar lo que el PM no cargó.

## Restricciones (gate de escritura — contrato de la casa)

- **NUNCA** escribir sin OK explícito del usuario vía widget de confirmación (gate pre-write).
- **NUNCA** crear un issue con required fields vacíos: gate pre-write valida required (técnicos + de negocio) contra `getJiraIssueTypeMetaWithFields`; si falta uno, se pide antes de escribir. (Regla transversal — ver contrato de escritura de skills.)
- **Verificación post-write**: releer el issue creado/editado (`getJiraIssue`) y confirmar que quedó como se esperaba antes de reportar éxito.
- **NO** inferir el proyecto automáticamente — el usuario lo elige siempre.
- **NO** transicionar por default; solo si el usuario elige la transición explícitamente.
- Escrituras **una por una** (no en paralelo) para poder reportar fallas individuales.

---

## Gate de continuidad — ¿este proyecto ya venía trabajándose en otra conversación? (ADVISORY)

> Runbook completo en `_shared/session-continuity/gate.md`. Corre **una sola vez**, en cuanto sabés de qué proyecto se trata y **antes de crear nada**. **Nunca bloquea.**

Cada conversación de Cowork arranca sin memoria de las anteriores. Si el usuario ya venía trabajando esto en otra, acá se re-pregunta todo y —peor— se puede terminar duplicar el trabajo y **partir el backlog en dos tandas** para el mismo alcance. Cowork **no expone** las conversaciones del usuario, así que no intentes detectarlas ni linkearlas: lo que sí podés es leer la **huella del trabajo previo** y recomendarle volver.

1. Buscá actividad reciente del proyecto (`Project__c` y sus `Project_Asset__c` activos), con `LastModifiedDate` y `LastModifiedBy`. Sumá la huella de **Jira** (issues creados/modificados en las últimas 72 h, sprint activo) y de la carpeta de **Drive** del proyecto — pero sólo con los conectores que el skill ya iba a usar igual.
2. **Dos señales fuertes** (modificado en las últimas 72 h · por el mismo usuario · backlog o assets tocados hoy · onboarding a medias) → mostrá el aviso. Actividad de más de 30 días no cuenta.
3. Mostrá **la evidencia concreta** (qué, cuándo, quién) y después la recomendación, siempre condicional: *"si venías trabajando este proyecto en otra conversación, seguí ahí — vas a tener el contexto; acá arranco sin esa memoria"*. **Nunca inventes un link a la conversación.**
4. Ofrecé: **(a)** continuar acá levantando el contexto *(default)* · **(b)** frenar para ir a buscar la otra conversación — no escribas nada · **(c)** es otro alcance, crear igual.

**Salteá este paso** si el skill fue invocado encadenado desde otro skill en la misma conversación.

---

## Flujo paso a paso

### PASO 0 — Preflight de conectores e identidad
1. `getAccessibleAtlassianResources` → si falla: "Necesitas el conector de Atlassian activo. Actívalo en Configuración → Conectores." → **fin**.
2. `atlassianUserInfo` → capturar email + accountId (reporter / asignaciones).
3. Detectar `cloudId` dinámicamente (no hardcodear).

### PASO 1 — Intención y proyecto
Detectar la operación (crear / editar / linkear / comentar / transicionar) del pedido del usuario.
Resolver el **proyecto Jira** destino: si el usuario ya nombró un issue key (`PROJ-123`) se deriva de ahí; si va a crear, elegir proyecto vía `getVisibleJiraProjects` (typeahead si hay muchos). No avanzar sin proyecto.

### PASO 1.5 — Recomendaciones + oferta de contexto (OPT-IN, sin barrido por defecto)
Aplicar el contrato de `_shared/jira/context-and-completeness.md`. **Clave de performance: NO
barrer conectores por defecto** (encarece la latencia). El camino normal es rápido:
1. **Recomendar** con lo que ya se tiene (pedido del PM + Jira): calidad de la historia (Como/Quiero/
   Para, criterios DADO/CUANDO/ENTONCES), Epic padre, estimación, campos de negocio vacíos, issuetype
   correcto — cada una con su porqué. Esto NO requiere conectores.
2. **Ofrecer** (sin ejecutar) revisar el contexto con conectores (Gmail, Calendar, ReadAI/Meet, Drive,
   Confluence, Slack, Salesforce) para pre-llenar y detectar lo no cargado. Se dispara SOLO si el PM lo
   pide (botón "Revisar el contexto del proyecto" del widget). Al aceptar: consulta **lazy y acotada**
   (solo fuentes pertinentes, con límites), y decir qué se miró y qué no.
3. Recomendaciones y oferta se muestran en el widget del PASO 4 (sección "Recomendaciones" + botón de
   contexto). Nunca se escribe ni se barre nada solo: son propuestas.

### PASO 2 — Resolver issuetype + su esquema de fields
1. `getJiraProjectIssueTypesMetadata` sobre el proyecto → issuetypes disponibles (validar contra `_shared/jira/issuetypes-and-workflows.md`).
2. Elegir el issuetype (del pedido o preguntando).
3. `getJiraIssueTypeMetaWithFields` → required + opcionales + allowedValues de picklists. Cruzar con `references/issuetype-field-mapping.md` para defaults/convenciones de PC.
4. ⚠️ **Verificar el nombre real del issuetype** (ej: `Artifact` vs `Artefacto`) — usar el `id`/`name` que devuelve la org, no el string en español.

### PASO 3 — Juntar los datos del issue
Reunir del pedido del usuario los valores para cada field. Los **required** que falten se piden explícitamente (AskUserQuestion o widget). Convenciones de contenido por issuetype (formato de summary, criterios de aceptación DADO/CUANDO/ENTONCES para Story, etc.) en `references/issuetype-field-mapping.md`.

### PASO 4 — Revisión y confirmación (widget, gate pre-write)
Cargar `assets/confirm-issue.html` y pasarlo como `widget_code` a `mcp__visualize__show_widget`,
reemplazando SOLO el objeto `const ISSUE = ...` (anclar en esa línea y su marcador de fin, NO en
el comentario de cabecera) con el issue armado: `{mode, projectKey, projectName, issuetype,
issueKey, fields:[{key,label,type,value,required,options?}]}`. Tipos: string/textarea/url/date/number/select.
El widget valida los required en cliente y, al confirmar, devuelve por `sendPrompt` los valores
finales como `CONFIRMO: ... Datos finales (JSON): {...}`. **Nada se escribe antes de ese OK.**

### PASO 5 — Ejecutar la escritura
> ⚠️ **ADF**: `description` y los custom `textarea` (Story Como/Quiero/Para/Criterios,
> Weekly Status Notes, etc.) deben ir en Atlassian Document Format, no como string plano
> (`{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":"..."}]}]}`),
> un `paragraph` por línea. Detalle en `_shared/jira/fields-by-issuetype.md`. Los `select`/`url`/`date` van planos.
- Crear: `createJiraIssue` (reporter = usuario del PASO 0).
- Editar: `editJiraIssue` sobre el issue key.
- Parent (jerarquía Epic←Story←Sub-task): campo `parent` en el create.
- Dependencias/relaciones (campo `issuelinks`): crear con `POST /rest/api/3/issueLink`
  (vía `fetch` si el MCP no expone tool de links). Tipos reales en `_shared/jira/fields-by-issuetype.md`
  — para "necesita X primero" usar **`Dependencia`**, para bloqueo **`Blocks`**. No inventar tipos.
- Comentar: `addCommentToJiraIssue`.
- Transicionar (solo si el usuario eligió una): `getTransitionsForJiraIssue` → `transitionJiraIssue`.
Una llamada por vez.

### PASO 6 — Verificación post-write y reporte
`getJiraIssue` sobre lo escrito → confirmar. Reportar en chat con link(s) directo(s) al/los issue(s).

### PASO 7 — Handoff (opcional)
Ofrecer próximo paso según contexto (ej: "¿lo sumo al sprint activo?" → `sprint-manager`; "¿le asigno release?" → `release-manager`), patrón de widget de próximo paso de la casa.

---

## Reglas de negocio / no obvias
- El esquema de fields **varía por issuetype**; nunca asumir un set fijo. La org es la verdad; el archivo de mapeo es la referencia.
- **Idempotencia razonable**: antes de crear, buscar por summary similar en el proyecto (`searchJiraIssuesUsingJql`) y avisar si parece duplicado.
- Zona horaria de input: `America/Argentina/Buenos_Aires`; convertir a UTC hacia Atlassian.
- Los issuetypes con dueño en otro skill (External pending, worklog) se derivan, no se crean acá.

---

## Archivos referenciados
| Archivo | Cuándo leerlo | Estado |
|---|---|---|
| `_shared/jira/issuetypes-and-workflows.md` | PASO 2 — inventario + IDs | ✅ listo |
| `_shared/jira/fields-by-issuetype.md` | PASO 2-3 — fields, picklists, statuses reales | ✅ listo |
| `_shared/jira/screen-schemes.md` | PASO 2 — screen por issuetype | ✅ listo |
| `_shared/jira/context-and-completeness.md` | PASO 1.5 — contrato asistente proactivo (contexto+recomendaciones+completitud) | ✅ listo |
| `references/issuetype-field-mapping.md` | PASO 3 — obligaciones de negocio/convenciones | ✅ listo |
| `assets/confirm-issue.html` | PASO 4 — widget de confirmación (gate pre-write) | ✅ listo (smoke test OK) |

## TODO antes de pasar de DRAFT a 1.0.0
1. ~~Introspección de fields + statuses~~ ✅ hecho (2026-07-13).
2. ~~Confirmar `name`/`id` real de `Artifact`~~ ✅ `Artifact` id 10209 (bug flagueado aparte).
3. ~~Widget de confirmación PASO 4~~ ✅ `assets/confirm-issue.html` (smoke test en preview: render, required-block, payload JSON, cancel).
4. ~~Issue links~~ ✅ validado end-to-end vía REST: `POST /rest/api/3/issueLink` con `Dependencia` funcionó (ZCLAUDE-12 ←req— ZCLAUDE-10). 10 tipos; `Dependencia`/`Blocks` canónicos.
5. ~~Smoke test end-to-end real~~ ✅ (2026-07-13, sandbox ZCLAUDE): Epic-módulo ZCLAUDE-9 → Story ZCLAUDE-10 (parent + Como/Quiero/Para/Criterios en ADF) → Sub-task ZCLAUDE-11; + dependencia + versión MVP 1 asignada. Confirma issue-builder + jerarquía + dependencias + release contra el esquema real.
6. Widget de handoff PASO 7: reusar `_shared/handoff/` (no requiere widget propio).
7. Ratificar nombre + distribución con `pc-meta-skill-manager` + tarea PROCSKILLS (necesita Atlassian MCP). Naming ya validado contra la convención pc-[delivery]-[jira]-[objeto]-[acción].
8. Generar `.skill` + deploy a Cowork (tras ratificación; hoy DRAFT no deployable).
