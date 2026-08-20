---
name: pc-delivery-project-pulse
metadata:
  version: 1.0.0
  last_modified: 2026-07-11
description: >
  Genera un reporte diario del estado de todos los proyectos activos de ProContacto.
  Cruza Project__c de Salesforce con los proyectos Jira vía Project_Asset__c (soporta
  múltiples tableros Jira por proyecto SF) y presenta un semáforo de actividad:
  issues con movimiento esta semana, issues vencidas, sprint activo agregado.
  Renderiza SIEMPRE el resultado como widget chat-inline con mcp__visualize__show_widget
  — tabla filtrable con semáforo y accionables por fila.
  Activar SIEMPRE cuando el usuario diga "pulso de proyectos", "cómo van los proyectos",
  "dame el estado de los proyectos", "hay movimiento en los proyectos",
  "qué proyectos están estancados", "status de todos los proyectos",
  "reporte de proyectos", o cuando se ejecute como tarea programada diaria.
  También activar proactivamente si el usuario menciona querer un overview de todos
  sus proyectos activos.
---

# Skill: Project Pulse — Reporte diario de proyectos

Genera un panel compacto con el estado de movimiento de todos los proyectos activos.
El objetivo: "¿cuáles proyectos están vivos y cuáles parecen estancados?" sin abrir
Jira uno por uno. Un proyecto SF puede tener **uno o más tableros Jira** — el skill
los agrega en una sola fila con métricas combinadas.

> **Regla fuerte de UI**: TODA presentación de datos usa `mcp__visualize__show_widget`
> (widget chat-inline). Nunca texto plano, nunca `mcp__cowork__create_artifact`,
> nunca `AskUserQuestion`. Los widgets encadenan pasos vía `sendPrompt`.

> **Herramientas prohibidas**: NO usar `Claude in Chrome` (ni ninguna de sus tools
> `mcp__Claude_in_Chrome__*`) en ningún paso de este skill. Toda interacción con
> sistemas externos se hace exclusivamente vía los conectores MCP disponibles
> (Salesforce, Jira, Slack, etc.).

---

## Paso 1 — Recolectar datos base

Una sola query Salesforce. **La única condición para considerar un proyecto activo
es `Completion_Summary__c = null`** — es el único filtro de estado que se aplica.
No filtrar por `Stage__c` ni ningún otro campo de estado.
La subquery trae **todos** los tableros Jira vinculados, sin LIMIT.

```sql
SELECT Id, Name, Stage__c, Account__r.Name,
       OwnerId, Owner.Name, Owner.Email,
       Owner.Manager.Name, Owner.Manager.Email,
       JiraProjectKey__c,
       (SELECT Value__c FROM Project_Assets__r
        WHERE Type__c = 'JiraProjectKey')
FROM Project__c
WHERE Completion_Summary__c = null
ORDER BY Stage__c, Name
```

De cada proyecto extraer:
- `sfId`, `name`, `stage`, `account`
- `pmName` / `pmEmail` → `Owner.Name` / `Owner.Email`
- `managerName` / `managerEmail` → `Owner.Manager.Name` / `Owner.Manager.Email`
- `jiraKeys` → array de `Project_Assets__r[*].Value__c` (puede ser `[]`)
- `jiraKeyLegacy` → `JiraProjectKey__c` (campo deprecado, fallback para vinculación)

> **Regla estricta — owner del proyecto**: el responsable del proyecto se obtiene
> **siempre y únicamente** del campo estándar `Owner` de `Project__c`
> (`Owner.Name`, `Owner.Email`, `Owner.Manager.Name`, `Owner.Manager.Email`).
> Está **estrictamente prohibido** usar cualquier otro campo para identificar al
> dueño del proyecto (ej: `Project_Manager__c`, `PM__c`, `Responsible__c`, o
> cualquier campo custom). Si `Owner` no tiene el dato, reportar ausencia — nunca
> recurrir a campos alternativos.

**Clasificación post-query:**

| Caso | jiraKeys | jiraKeyLegacy | Estado |
|---|---|---|---|
| Vinculado (uno o más) | `[k1, ...]` | cualquiera | `linked` |
| Linkeable en masa | `[]` | ✅ | `linkeable` |
| Sin Jira | `[]` | null/vacío | `unlinked` |

---

## Paso 1b — Vinculación masiva (si hay proyectos `linkeable`)

Si hay proyectos `linkeable`, mostrar **antes del pulso** un widget con:

- Banner: "{N} proyecto(s) tienen clave Jira en el campo legacy pero sin
  Project_Asset__c vinculado."
- Tabla: Cliente, Proyecto, Clave detectada (editable), checkbox (todos marcados).
- Botón **"Vincular seleccionados ↗"** → sendPrompt con JSON de proyectos a vincular.
- Botón **"Saltar ↗"** → continúa con el pulso usando `jiraKeyLegacy` como clave
  temporal para las queries Jira.

Al confirmar, crear un `Project_Asset__c` por cada proyecto seleccionado:
```
Type__c = 'JiraProjectKey' | Value__c = {clave} | Project__c = {sfId}
```
Ejecutar con `createSobjectRecord`. Una falla no bloquea el resto.

---

## Paso 2 — Correr queries Jira y calcular métricas agregadas

Para cada proyecto, sus métricas se calculan **sobre todos sus tableros combinados**.
Cuando un proyecto tiene múltiples keys, usar JQL con `project IN (k1, k2, ...)` para
traer todo en una sola query — más eficiente que una query por tablero.

Los proyectos `linkeable` que saltaron el 1b usan `[jiraKeyLegacy]` como `jiraKeys`.

**Q1 — Actividad reciente**
```
project IN ({jiraKeys}) AND updated >= -7d
```
Fields: `key,project,status,updated`. `maxResults=50`.
→ `activityCount` = total de issues tocados. `activeKeys` = set de project.key con hits.

**Q2 — Issues vencidas**
```
project IN ({jiraKeys}) AND duedate < now() AND statusCategory != Done
```
Fields: `key,project,summary,assignee`. `maxResults=20`.
→ `overdueCount` = total. `overdueByKey` = mapa key→count para mostrar desglose.

**Q3 — Sprints activos** — solo si `activityCount > 0` (ahorra tokens en proyectos muertos)
```
project IN ({jiraKeys}) AND sprint in openSprints()
```
Fields: `key,project,status`. `maxResults=200`.
→ Por cada key activa: nombre del sprint + `%done`. Si hay múltiples sprints activos,
tomar el de mayor `%done` como representativo y registrar `sprintCount`.

### Lógica del semáforo (sobre métricas agregadas)

```
🔴 = unlinked
     OR (activityCount == 0 AND overdueCount > 0)
     OR overdueCount >= 10

🟡 = activityCount == 0 (sin movimiento, sin vencidas graves)
     OR (overdueCount >= 3 AND overdueCount < 10)

🟢 = activityCount > 0 AND overdueCount < 3
```

---

## Paso 3 — Renderizar el widget

### Header

- Título "Project Pulse" + fecha de hoy
- Chips de filtro: `Todos` / `🔴` / `🟡` / `🟢` / por Stage
- Buscador por nombre de proyecto o cuenta (JS cliente-side)
- Botón **"Actualizar ↗"** → `sendPrompt("Actualiza el pulso de proyectos")`

### Tabla — columnas

| Col | Fuente | Nota multi-tablero |
|---|---|---|
| Semáforo | Calculado | Sobre métricas agregadas |
| Cliente — Proyecto | SF | — |
| Stage | SF (badge por color) | — |
| PM | SF | — |
| Tableros | jiraKeys.length | "1 tablero" / "N tableros" como chip |
| Sprint | Jira Q3 | Sprint representativo + %done. Si N>1: "N sprints" |
| Mov. 7d | Jira Q1 | Total agregado |
| Vencidas | Jira Q2 | Total agregado (rojo si > 0) |
| Acciones | Botones | Varían según estado |

### Accionables por fila

**Proyectos `linked` o `linkeable` (tienen jiraKeys):**

1. **"Auditar ↗"**
   - 1 tablero → `sendPrompt("Audita el proyecto {account} — {name} (clave Jira: {jiraKeys[0]}). Avanza al PASO 1.3 con scope 'Todo el proyecto'.")`
   - N tableros → `sendPrompt("El proyecto {account} — {name} tiene {N} tableros Jira: {jiraKeys.join(', ')}. ¿Cuál quieres auditar? Mostrámelos como botones.")` — el skill muestra un picker y luego invoca el auditor.

2. **"Jira ↗"**
   - 1 tablero → link directo al tablero.
   - N tableros → dropdown o mini-widget con un link por tablero.

3. **"SF ↗"** → link al `Project__c`.

4. **"+ Tablero ↗"** → siempre visible en proyectos `linked`, para agregar un tablero adicional. `sendPrompt("Quiero agregar un tablero Jira adicional al proyecto {account} — {name} (SF Id: {sfId}). Ya tiene: {jiraKeys.join(', ')}. Arranca el flujo de vinculación.")` — arranca Paso 5.

5. **"Notificar ↗"** → arranca Paso 4.

**Proyectos `unlinked` (sin ninguna clave):**

1. ~~"Auditar"~~ → deshabilitado.
2. ~~"Jira"~~ → deshabilitado.
3. **"SF ↗"** → habilitado.
4. **"Vincular Jira ↗"** (botón destacado) → `sendPrompt("Ayúdame a vincular el proyecto Jira para: {account} — {name} (SF Id: {sfId}). JiraProjectKey__c: '{jiraKeyLegacy}'. No tiene tableros vinculados aún.")` — arranca Paso 5.
5. **"Notificar ↗"** → habilitado.

---

## Paso 4 — Flujo de notificación

### 4.1 — Recolectar datos de Slack para el proyecto

Ejecutar en paralelo:

1. `slack_search_users` con `pmEmail` → Slack ID del PM.
2. `slack_search_users` con `managerEmail` → Slack ID del Manager. Si no se encuentra, notificar solo al PM.
3. Leer los últimos DMs con el PM para entender el tono del último intercambio.
4. Buscar los canales Slack del proyecto en Salesforce:
   ```sql
   SELECT Type__c, Value__c FROM Project_Asset__c
   WHERE Project__c = '{sfId}'
     AND Type__c IN ('SlackProjectChannelId', 'SlackExternalProjectChannelId')
   ```
   Guardar como `slackChannels = [{type, channelId}]`.
   - `SlackProjectChannelId` → canal interno del equipo PC
   - `SlackExternalProjectChannelId` → canal externo con el cliente

   Si no hay canales registrados → omitir la sección de canales del mensaje silenciosamente.

### 4.2 — Primer mensaje del día

Revisar si ya hubo mensajes hoy en el DM con el PM.
- **Sin mensajes hoy** → arrancar con `"¿Cómo estás?"`.
- **Ya hubo mensajes hoy** → ir directo al cuerpo.

### 4.3 — Armar draft según semáforo

Los canales Slack del proyecto se incluyen al final del mensaje, **uno por línea**,
formateados como referencias Slack (`<#CHANNEL_ID>`) para que sean clicables
directamente desde el DM. Primero el canal interno, luego el externo (si existe).

**Template 🟡:**
```
[¿Cómo estás? — si es primer mensaje del día]

Te escribo por el proyecto [Nombre]. Esta semana no vi mucho movimiento en
Jira — ¿hay algo en vuelo que no esté reflejado ahí, o están con algo que
necesite atención?

[Si hay canales:]
Canales del proyecto:
<#CHANNEL_ID_INTERNO>
<#CHANNEL_ID_EXTERNO>
```

**Template 🔴:**
```
[¿Cómo estás? — si es primer mensaje del día]

Necesito un update del proyecto [Nombre]. Tiene [N] issues vencidas y no
registré actividad en los últimos 7 días. ¿Puedes contarme cómo está el
estado real? Quiero tener el panorama antes de que escale.

[Si hay canales:]
Canales del proyecto:
<#CHANNEL_ID_INTERNO>
<#CHANNEL_ID_EXTERNO>
```

Adaptar el tono al contexto del último DM: si fue hace varios días, reconocerlo
brevemente. Si hubo intercambio reciente, ir más directo.

**Draft para el Manager** (también incluye canales al final):
```
Hola [Manager], te paso un update: el proyecto [Nombre] de [Cuenta] tiene
señales de alerta en el pulso semanal ([N] vencidas / sin actividad).
Ya le escribe a [PM]. Solo te copio para que lo tengas en el radar.

[Si hay canales:]
Canales del proyecto:
<#CHANNEL_ID_INTERNO>
<#CHANNEL_ID_EXTERNO>
```

> **Formato de referencia Slack**: usar exactamente `<#CHANNEL_ID>` donde `CHANNEL_ID`
> es el valor de `Value__c` del `Project_Asset__c`. Slack renderiza esto como una
> mención clicable al canal. No usar el nombre del canal (`#nombre`) — solo funciona
> el ID para garantizar que el link abra el canal correcto.
> Si un canal no tiene `Value__c` o el valor está vacío, omitir esa línea.

### 4.4 — Widget de preview (`mcp__visualize__show_widget`)

- Pills editables de destinatarios (PM + Manager, cada uno con ✕)
- Textarea del mensaje al PM — editable
- Textarea del mensaje al Manager — colapsada por default, editable
- Botón **"Enviar ↗"** y **"Cancelar"**

**NUNCA enviar sin que el usuario confirme con "Enviar ↗".**

### 4.5 — Enviar DMs

`slack_send_message` por cada destinatario confirmado. Reportar resultado en chat.

---

## Paso 5 — Flujo de vinculación / agregar tablero

Se activa tanto desde "Vincular Jira ↗" (proyecto sin tableros) como desde
"+ Tablero ↗" (proyecto que ya tiene tableros y quiere agregar otro).

### 5.1 — Verificar campo deprecado

```sql
SELECT JiraProjectKey__c FROM Project__c WHERE Id = '{sfId}' LIMIT 1
```
- Con valor y el proyecto es `unlinked` → pre-cargar en Zona A.
- El proyecto ya tiene `jiraKeys` → ignorar el campo legacy (ya fue migrado).

### 5.2 — Buscar candidatos en Jira

`getVisibleJiraProjects` → filtrar por similitud con `{name}` y `{account}`:
1. Normalizar: quitar prefijos `proy-`, `support-`, `cc-`; tokenizar por `-`.
2. Excluir keys que ya están en `jiraKeys` del proyecto (ya vinculados).
3. Rankear por tokens que coinciden. Top 5 candidatos.

### 5.3 — Widget de selección (`mcp__visualize__show_widget`)

**Contexto de la acción** (siempre visible arriba):
- Si es `unlinked`: "Vinculando Jira para: {account} — {name}"
- Si ya tiene tableros: "Agregando tablero adicional a: {account} — {name}
  (ya tiene: {jiraKeys.join(', ')})"

**Zona A — Campo legacy** (solo si `unlinked` y `JiraProjectKey__c` tiene valor):
- Card: "El campo JiraProjectKey__c tiene `{valor}`" + botón **"Usar esta clave ↗"**.

**Zona B — Candidatos en Jira** (puede estar vacía):
- Tabla con **checkboxes de multi-selección**: Clave, Nombre del proyecto en Jira,
  Score de similitud, checkbox (ninguno marcado por default — el usuario decide cuáles
  son correctos).
- Botón **"Vincular seleccionados ↗"** habilitado cuando al menos un checkbox está marcado.
- Si vacía: "No encontré proyectos similares en Jira."
- El usuario puede marcar varios si el proyecto SF realmente usa múltiples tableros Jira.

**Zona C — Entrada manual:**
- Input: "Ingresa la clave Jira (ej: AVELLANEDA)" + botón **"Agregar a selección ↗"**
  que suma esa clave a la selección de Zona B antes de confirmar (no vincula de
  inmediato — permite revisar junto con los candidatos).
- Botón **"Este proyecto no tiene tablero en Jira"** (solo para `unlinked`) → cierra el
  flujo sin crear Asset. Registrar en chat.

### 5.4 — Validar y crear `Project_Asset__c` (soporta múltiples claves)

Cuando el usuario confirma la selección (puede ser 1 o N claves):

1. Para cada clave seleccionada, verificar que no esté ya vinculada (`jiraKeys` del
   proyecto). Si ya está → saltar esa clave con nota "ya vinculada".

2. Verificar que cada clave existe en Jira con `searchJiraIssuesUsingJql`:
   `project = {clave} ORDER BY created DESC` con `maxResults=1`.
   Si falla → saltar esa clave con error "no existe o sin acceso". No crear Asset.

3. Crear un `Project_Asset__c` por cada clave válida:
   ```
   Type__c    = 'JiraProjectKey'
   Value__c   = {clave en mayúsculas}
   Project__c = {sfId}
   ```
   Ejecutar de a uno. Una falla no bloquea el resto.

4. Reportar resumen: "✅ {N} tablero(s) vinculados a {name}: {claves unidas por ', '}.
   [clave fallida si hubo: ❌ {clave} — {motivo}]"

5. Ofrecer: **"Ver el pulso actualizado ↗"** → `sendPrompt("Actualiza el pulso de proyectos")`.

---

## Notas de implementación

- **Sin Manager en SF**: `Owner.Manager` puede ser null → omitir silenciosamente del flujo de notificación.
- **Zona horaria**: `America/Argentina/Buenos_Aires`.
- **Widget stateless**: datos calculados en cada ejecución, embebidos en el HTML. "Actualizar ↗" re-invoca el skill completo.
- **Sprints múltiples**: si un proyecto tiene N tableros con sprints activos, mostrar el de mayor %done como representativo y agregar un chip "N sprints activos" colapsable.
- **Auditar con múltiples tableros**: el picker de auditoría muestra cada tablero como botón con su key y nombre de sprint activo si tiene.
- **Scheduleable**: después de la primera ejecución ofrecer: "¿Quieres que ejecute esto automáticamente cada mañana? Puedo configurarlo."
