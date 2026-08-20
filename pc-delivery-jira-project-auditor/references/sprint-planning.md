# Creación de sprints — detalle

Acción del PASO 2 que crea sprints en el board del proyecto. Es la segunda excepción a la regla "no crear nada" del skill (la primera es "Trabajo invisible" que crea issues). Razón del relajamiento: crear sprints es estructural (no toca contenido del proyecto), recuperable (un sprint vacío se puede borrar) y resuelve un caso real frecuente — proyectos de Build sin cadencia armada.

## Cuándo aparece la acción

La nueva dimensión del scoring "Plan de sprints" (15% del peso en fase Ejecución) detecta tres escenarios donde el botón aparece:

1. **Sin ningún sprint creado** — proyecto en Build/UAT pero el board nunca tuvo sprints. Sub-score: 0.
2. **Sprints cerrados sin sprint activo ni siguiente** — la cadencia se rompió, el equipo trabaja sin sprints actuales. Sub-score: 30-40.
3. **Cadencia errática** — sprints anteriores con duraciones muy distintas (CV de duración > 0.2). El equipo arma sprints "cuando se acuerda". Sub-score: 50-60.

Cuando el sub-score baja de 60, suma el botón global **"Crear plan de sprints ↗"** al widget del PASO 2.

## Variante para fase Sprint 0

Si la fase es Sprint 0 (relevamiento) y la dimensión "Fecha objetivo de cierre Sprint 0" del scoring saca <60, en lugar del botón general aparece **"Planificar cierre de Sprint 0 ↗"** — variante simplificada que crea **1 solo sprint** con fecha de cierre del relevamiento.

## Detección del board del proyecto

La Agile API de Jira opera por `boardId`, no por `projectKey`. El skill descubre el board del proyecto:

```
GET /rest/agile/1.0/board?projectKeyOrId=<PROJECT_KEY>
```

Si devuelve >1 board (proyectos con kanban + scrum, o múltiples teams), el skill muestra al PM un widget de selección antes de armar el formulario.

Si devuelve 0 boards (proyecto kanban puro sin board scrum), no se puede crear sprints. El skill avisa y sugiere convertir a scrum desde la UI de Jira.

## Detección de la cadencia histórica

Para sugerir defaults inteligentes en el formulario, traer los últimos 5 sprints cerrados:

```
GET /rest/agile/1.0/board/<BOARD_ID>/sprint?state=closed
```

Calcular para cada uno: `duración = endDate - startDate`. La duración default propuesta en el formulario es la **mediana** de los últimos 5 (más robusta que el promedio frente a outliers). Si no hay sprints cerrados, default = 14 días.

Si el CV de duración > 0.2 (cadencia errática), el formulario muestra un banner warning:

> Detecté inconsistencias en la cadencia anterior (sprints de 7d, 14d, 21d, 10d, 14d). Usa esta duración como base y ajústala si quieres normalizar.

## Widget de PASO 3 para esta acción

Formulario chat-inline con campos pre-llenados:

```
Cantidad de sprints      [4]                          (default 4 = ~2 meses)
Duración por sprint      [14] días                    (default mediana histórica o 14)
Naming convention        [Sprint N — DD/MM]
Fecha primer sprint      [2026-05-04]                 (default próximo lunes)
Goal placeholder         [Definir en refinement]      (editable, opcional)
```

Debajo de los inputs, **tabla de preview en vivo** que recalcula al cambiar cualquier input:

```
N°  Nombre              startDate    endDate     Goal
1   Sprint 7 — 04/05    2026-05-04   2026-05-17  Definir en refinement
2   Sprint 8 — 18/05    2026-05-18   2026-05-31  Definir en refinement
3   Sprint 9 — 01/06    2026-06-01   2026-06-14  Definir en refinement
4   Sprint 10 — 15/06   2026-06-15   2026-06-28  Definir en refinement
```

Cada fila tiene:
- Inputs editables: nombre, startDate, endDate, goal
- Botón ✕ para descartar la fila

Footer: **"Crear N sprints ↗"** / **"Cancelar ↗"**.

### Variante Sprint 0 (cierre de relevamiento)

Sólo 1 sprint con campos:

```
Nombre        [Sprint 1 — Build kickoff]
startDate     [2026-05-04]                  (default = fecha de cierre objetivo de Sprint 0)
endDate       [2026-05-17]                  (default startDate + 14d)
Goal          [Build kickoff: arranque desarrollo de épicas X, Y]
```

## Numeración de sprints

Si el proyecto ya tiene sprints anteriores, el primer sprint nuevo arranca en `<último_número> + 1`. Ejemplo: si el último sprint cerrado fue "Sprint 6", los nuevos arrancan en "Sprint 7".

Si no hay sprints anteriores, arrancar en "Sprint 1". Si la fase es Sprint 0 y se crea el primer sprint formal, también arrancar en "Sprint 1" (por convención PC, Sprint 0 es el relevamiento, no cuenta como sprint productivo).

## Naming convention

Default: `Sprint N — DD/MM` (ej: `Sprint 7 — 04/05`). El DD/MM corresponde a la fecha de inicio. El PM puede cambiar la convention en el formulario — el cambio se aplica a todas las filas en vivo.

Convenciones alternativas que el PM puede tipear:
- `Sprint N` — sin fecha, para proyectos donde el N es suficiente
- `Sprint N — Nombre del Goal` — si el PM quiere goals visibles desde el board
- `Cliente · Sprint N` — para teams que comparten board entre clientes

## Ejecución

Por cada sprint en el subset aprobado, **una llamada por sprint** (la API no soporta batch):

```
POST /rest/agile/1.0/sprint
{
  "name": "Sprint 7 — 04/05",
  "startDate": "2026-05-04T00:00:00.000-03:00",
  "endDate": "2026-05-17T23:59:59.999-03:00",
  "originBoardId": <BOARD_ID>,
  "goal": "Definir en refinement"
}
```

Se ejecuta vía la tool `fetch` del MCP Atlassian (la Agile API no está expuesta como tool dedicado). El skill arma la URL completa con el cloudId:

```
https://api.atlassian.com/ex/jira/<CLOUD_ID>/rest/agile/1.0/sprint
```

**Una por una** (no paralelo) — la API responde rápido y queremos detectar fallas individuales sin que arrastren al resto. Si una falla (ej: nombre duplicado, permisos), reportar el error específico y seguir con los siguientes.

## Trazabilidad post-creación

Después de crear los sprints exitosamente:

1. Reportar en chat con widget chat-inline mostrando los sprints creados con sus fechas y links a Jira.
2. Si Salesforce está conectado, agregar comentario al `Project__c`:

   > "Plan de sprints actualizado el `<fecha>`. Sprints creados: Sprint 7 (04/05-17/05), Sprint 8 (18/05-31/05), Sprint 9 (01/06-14/06), Sprint 10 (15/06-28/06). Ejecutado por `<email del caller>`."

3. Ofrecer dos próximos pasos como botones:
   - **"Postear plan al canal interno ↗"** — reusa el flow de notificaciones (ver `slack-integration.md`). El mensaje al canal lista los sprints con sus fechas.
   - **"Pedir al equipo que carguen issues a Sprint 7 ↗"** — DM al equipo o post al canal pidiendo que el próximo refinement priorice cargar el sprint nuevo.

## Restricciones específicas

- **Máximo 6 sprints por batch** — más sprints planificados de una son ruido (proyectos PC raramente proyectan >3 meses).
- **Permisos del caller** — antes de crear, chequear que el caller tiene permiso de admin/lead en el proyecto. Si no, abortar con mensaje al PM real del proyecto sugiriendo que él lo haga.
- **Validación de fechas** — no permitir startDate < hoy. No permitir endDate < startDate. Detectar overlap con sprints existentes y avisar (no bloquear, pero pedir confirmación).
- **Nombres únicos** — la API rechaza nombres duplicados. Si el formulario propone un nombre que ya existe (ej: "Sprint 7" pero ya hubo un Sprint 7 cerrado), agregar sufijo numérico o avisar.
- **Sprints vacíos por default** — el skill NO asigna issues a los sprints recién creados. La asignación queda al refinement humano. Los sprints arrancan vacíos.

## Casos donde NO crear sprints

- El proyecto está en Hypercare (la fase Hypercare no usa sprints, sólo backlog reactivo).
- El proyecto cerró (`Project__c.Stage__c = 'Finished'`).
- El board es kanban puro (no soporta sprints).
- El caller no tiene permisos.

En todos estos casos, el botón global no aparece — la dimensión "Plan de sprints" se omite del scoring (no penaliza).
