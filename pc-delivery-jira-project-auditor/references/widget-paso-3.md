# Widget chat-inline del PASO 3 — preview de propuesta de fix

El preview de PASO 3 se renderiza con `mcp__visualize__show_widget` (chat-inline), NO con `mcp__cowork__create_artifact` (sidebar). Razón: cuando el PM toca un botón del widget de PASO 2 que dispara `sendPrompt`, el siguiente turno renderea otro widget chat-inline en el mismo hilo, manteniendo la continuidad del flujo. Si se abre un artifact en sidebar, el sendPrompt de confirmación del artifact no siempre se enrutea de vuelta al chat principal y el PM pierde el contexto del paso anterior.

## Estructura del widget

### Header

- Sub-header chico: `ProContacto · pc-delivery-jira-project-auditor · PASO 3 — preview` en `font-size: 12px; color: var(--color-text-secondary)`.
- Título: `Propuesta de <categoría> · <PROJECT_KEY>` en `font-size: 18px; font-weight: 500`.
- Una pill arriba a la derecha con `Batch X / Y · N issues` para que se vea cuántos batches quedan.

### Banner de confianza (si la confianza promedio es media o baja)

Banner con `background: var(--color-background-warning)`, texto `--color-text-warning`. Ejemplo:

> Confianza media — no hay issues resueltos en los últimos 90 días en este proyecto, los assignees se derivaron del issue padre. Revisa cada fila antes de confirmar.

Si la confianza es alta, el banner se omite.

### Tabla de filas editables (máximo 10)

Columnas: `Issue` (link a Jira en font-mono), `Summary` (truncado a 50 chars), `Tipo` (pill con color por type), `<campo a editar>` (input/select editable según categoría), `Transición` (select con las transiciones disponibles del issue, default "no transicionar"), `Confianza` (pill: alta verde / media amarilla / baja roja), `Fuente` (texto chico explicando de dónde salió la sugerencia, ej: `padre COLOM-994`), `Descartar` (botón ✕).

El campo editable depende de la categoría del fix:

- **Sin asignar** → `<input type="text">` con el nombre del assignee propuesto. Editable libre.
- **Vencidas / Sin fecha** → `<input type="date">` con la fecha propuesta.
- **Sin release** → `<select>` con las releases abiertas + opción `manual`.
- **Artefactos huérfanos** → `<select>` con top 3 matches de Drive/Figma + opción `manual`.

#### Columna "Transición" — opt-in granular (v1.9.0+)

Por cada fila, llamar `getTransitionsForJiraIssue` para ese issue específico (las transiciones varían por workflow del proyecto). Renderizar como `<select>`:

```html
<select>
  <option value="" selected>— no transicionar —</option>
  <option value="11">→ In Progress</option>
  <option value="21">→ In Review</option>
  <option value="31">→ Done</option>
</select>
```

Default: "no transicionar" (string vacío). Si el PM lo deja así, el PASO 4 sólo ejecuta `editJiraIssue` para ese issue. Si elige una transición, el PASO 4 ejecuta `editJiraIssue` **+** `transitionJiraIssue` con el id elegido.

**Optimización**: la llamada a `getTransitionsForJiraIssue` es una por issue (no se puede batch). Para no demorar el render del widget, hacer las llamadas en paralelo y mostrar el widget con loading indicators en la columna mientras se resuelven. Si un issue falla la consulta de transitions, dejar el select con la única opción "no transicionar" disponible.

**Cache**: las transiciones disponibles dependen del workflow + status actual del issue. Cache durante 5 minutos. Si el PM transiciona un issue en un batch, invalidar el cache de ese issue (porque el set de transiciones cambia con el status).

Cada fila tiene un botón ✕ "Descartar" que aplica una clase `discarded` (opacity 0.45, line-through) al `<tr>` y descuenta esa fila del payload de confirmación.

### Footer

Sticky al final con dos botones:

- **`Confirmar y aplicar (N) ↗`** — botón primario. Al click, dispara `sendPrompt` con un payload JSON que incluye sólo las filas no descartadas y los valores actuales de cada input. El prompt es algo como: `Aplica estos N cambios contra Jira en batch (PASO 4): [{issueKey, field, newValue}, ...]. Reporta éxito/falla por cada uno.`
- **`Cancelar ↗`** — al click, dispara `sendPrompt`: `Cancelé el preview del PASO 3 sin aplicar cambios. Vuelve al diagnóstico.`

### Sección "Batch siguiente" (si hay más de 10 hallazgos)

Debajo de la tabla, una sub-sección colapsada por default mostrando una lista compacta del próximo batch (issue key + summary + assignee tentativo) con texto: `Batch 2 — pendiente después de tu OK del batch 1`. No es interactiva — es un preview informativo de qué viene después.

## Reglas que se respetan en el widget

- Sin gradientes, sin shadows, fondos planos. CSS variables del host.
- Edición en el cliente — los cambios viven en estado JS hasta que se toca confirmar.
- El `sendPrompt` de confirmación es la **única** vía de aprobación. No aceptar "sí" tipeado en chat — el modelo debe insistir con que toque el botón. Esto preserva la trazabilidad (la JSON queda en el transcript).

## Variantes especiales

### Preview de "Seguimiento al equipo" (Slack DMs)

En lugar de tabla de cambios a Jira, muestra una tabla de **drafts de DM agrupados por assignee** — ver `slack-integration.md` para la estructura específica.

### Preview de "Bloqueos no registrados desde Slack"

Tabla con 4 columnas: issue / extracto del mensaje Slack (con timestamp) / link sugerido (`is blocked by` / `relates to` / `depends on` — el modelo decide según contexto) / botón ✕. Ver `slack-integration.md`.
