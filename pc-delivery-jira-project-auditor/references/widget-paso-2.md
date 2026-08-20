# Widget chat-inline del PASO 2 — spec detallada

El output del PASO 2 es siempre un widget chat-inline vía `mcp__visualize__show_widget` (nunca texto plano markdown ni `create_artifact` en sidebar). El widget tiene 5 zonas obligatorias en este orden.

## Zona 0 — Scoring header (arriba de todo)

Antes de las stats cards, una fila con **2 cards de scoring** en grid de 2 columnas:

- **Card "Score general"** — muestra la letra (font-size grande, ~32px, weight 500) + el número (ej: `B / 78`) + sub-label con la fase detectada (`Ejecución`, `Sprint 0 — relevamiento`, o `Indeterminado`).
- **Card "Score sprint activo"** — misma estructura pero para el sprint en curso. Si la fase es Sprint 0, esta card muestra `Sprint 0 — relevamiento` con su score; si es Ejecución sin sprint activo (ej: entre sprints), muestra `Sin sprint activo` y deja la card en gris.

Color del badge de la letra según escala (ver `scoring.md`). Las cards usan `--color-background-secondary` con border-radius-lg, padding 1rem.

Debajo de las dos cards de scoring, dos botones en línea:

- **"Ver desglose por dimensión ▾"** — al click expande inline una tabla con cada dimensión, su score, y el peso.
- **"Ver histórico por sprint ↗"** — dispara `sendPrompt` para traer histórico on-demand (sólo aplica en fase Ejecución).

## Zona 1 — Sub-header + stats cards

3 cards en grid de 3 columnas usando `--color-background-secondary`:

- **Categorías limpias** (color `--color-text-success`) — formato `N / 6`.
- **Hallazgos accionables** (color `--color-text-warning` si > 0, sino `--color-text-success`) — sin contar la sub-categoría informativa "Posible mistype".
- **Cambios aplicados** — siempre `0` en PASO 2 (el skill no escribió nada todavía).

Sub-header arriba de las cards: `ProContacto · pc-delivery-jira-project-auditor · diagnóstico <PROJECT_KEY>` en `font-size: 12px; color: var(--color-text-secondary)`.

## Zona 2 — Tabla resumen por categoría

Una tabla con border-radius-lg y border 0.5px, mostrando las 6 categorías + (opcional) "Posible mistype" con badge de estado:

| Q | Categoría | Count | Estado |
|---|---|---|---|
| Q1 | Sin asignar | N | Limpio (`--color-background-success`) o Revisar (`--color-background-warning`) |

Si una categoría tiene 0, badge verde "Limpio". Si tiene >0, badge amarillo "Revisar". Si es N/A (ej: no hay issue type Artefacto), badge gris "No aplica".

## Zona 3 — Acciones globales (2-4 botones correctivos)

Grid de 2 columnas con botones que disparan `sendPrompt` para fixes bulk. Las acciones disponibles dependen del diagnóstico — el skill elige las 2-4 más relevantes:

| Cuando aparece | Texto del botón | Prompt que dispara |
|---|---|---|
| `unassigned > 0` | "Asignar por histórico a las N sin asignar ↗" | `Para los N issues sin asignar de <KEY>, deriva el assignee usando el histórico del Epic/Component (issues resueltos en los últimos 90 días). Muéstrame el preview en el widget chat-inline de PASO 3. Sin escribir hasta mi OK.` |
| `overdue > 0` o `no_date > 0` | "Aplicar duedate del active sprint a las N ↗" | `Para los N issues sin fecha o vencidos de <KEY>, propón duedate = endDate del sprint activo. Si no hay sprint, hoy + 7 días. Muéstrame el preview. Sin escribir hasta mi OK.` |
| `no_release > 0` | "Asignar fixVersion abierta a las N ↗" | `Para los N issues sin fixVersion de <KEY>, tráeme las releases abiertas del proyecto y propón cuál usar. Sin escribir hasta mi OK.` |
| `artifact_orphan > 0` | "Buscar matches en Drive/Figma para los N artefactos ↗" | `Para los N artefactos huérfanos de <KEY>, corre search_files en Drive y get_metadata en Figma con cada nombre, y arma el preview con top 3 matches por artefacto. Sin escribir hasta mi OK.` |
| `posible_mistype > 0` | "Reclasificar las N como `<RecurringType>` (manual) ↗" | `Las N issues flagadas como mistype tienen summary recurrente (weekly/daily/etc) pero están como Task/Story. Genera los pasos manuales para que el PM las reclasifique al issue type correcto desde la UI — el skill no toca issuetype. Sin escribir nada.` |
| `no_worklog > 0` (issues en progreso >3d sin tiempo) | (consolidado dentro de "Seguimiento al equipo") | — |
| `team_followup_pending > 0` (suma sin estimación + vencidas + sin worklog) | "Mandar follow-up al equipo por Slack ↗" | (ver `slack-integration.md`) |
| `analyze_worklog_only > 0` (sólo análisis, sin DM) | "Analizar tareas sin worklog ↗" | `Para los N issues de <KEY> en progreso desde hace >3d sin tiempo cargado, agrupa por assignee y muéstrame el desglose: cuántas tiene cada uno, cuánto tiempo lleva cada issue en in-progress, sugerencias de qué priorizar. Sin enviar nada — sólo análisis.` |
| `missing_scope = true` (no hay scope document detectado) | "Pedirme cargar el alcance ↗" | `El proyecto <KEY> no tiene un documento de alcance cargado (no se detectó Scope_Document_URL__c en Project__c, ni Project_Asset__c tipo SOW, ni página Confluence con keywords scope/alcance/SOW). Genera un draft de DM a mí (el caller del audit) con un recordatorio para cargarlo. Plantilla en slack-integration.md. Sin enviar hasta mi OK.` |
| **Siempre disponible al final** | "Postear resumen del diagnóstico al canal interno ↗" | `Genera un draft de mensaje para postear en el canal interno del proyecto <KEY> con: score general, fase, top 3 categorías con hallazgos, link a la conversación. Plantilla en slack-integration.md sección "Post-diagnóstico". Sin enviar hasta mi OK.` |
| **Siempre disponible al final** | "Generar weekly status ↗" | `Genera un weekly status para el proyecto <KEY> siguiendo el template ProContacto. Trae los datos de las queries por sección documentadas en weekly-status.md (sprint anterior, sprint actual, capacitaciones, acciones pendientes). Renderiza preview chat-inline editable antes de generar el doc en Drive. Sin crear el doc hasta mi OK.` |
| **Siempre disponible — meta-acción** | "Verificar actualizaciones del skill ↗" | `Compárame la versión instalada del skill (que estás leyendo del SKILL.md cargado en sesión) contra la latest publicada. Detalle de cómo y dónde buscar el latest en references/skill-self-update.md. Si hay diff, muéstrame el changelog acumulado entre las versiones y dame botón para descargar la nueva. No intentes recargarte a ti mismo en runtime — sólo infórmame del diff y el link de descarga.` |
| **Sólo si la carpeta de releases NO existe en Drive** | "Publicar esta versión en Drive para activar las actualizaciones ↗" | `Activa el sistema de verificación de actualizaciones la primera vez. Haz los 3 pasos descritos en references/skill-self-update.md sección "Bootstrap del registry": (1) crear carpeta `procontacto-claude/skills-releases/pc-delivery-jira-project-auditor/` si no existe, (2) subir el .skill actualmente instalado, (3) generar CHANGELOG.md extrayendo las entradas del frontmatter. Muéstrame preview de qué vas a hacer antes de tocar Drive. Sin escribir hasta mi OK.` |
| `slack_blockers_unregistered > 0` | "Crear issuelinks sugeridos desde Slack ↗" | (ver `slack-integration.md`) |
| `no_release > 0` y proyecto en Sprint 0 sin releases | "Marca los N sin release como `manual` ↗" | `Para los N issues sin fixVersion en <KEY>: el proyecto aún no tiene releases creadas. Marca esos hallazgos como manual y avísame que para resolverlos necesito que cree primero al menos una versión.` |

El skill prioriza por impacto: artefactos huérfanos > vencidas > sin asignar > sin fecha > sin release. Mostrar **máximo 4 botones correctivos** — si hay más categorías con hallazgos, dejar las menores para acciones por fila.

Las acciones derivadas del scoring (cuando una dimensión saca <60) se mezclan acá pero respetan el límite de 4 — ver `scoring.md` sección "Accionables derivados".

## Zona 3.5 — Cross-skill (separada visualmente)

Después de los botones correctivos, sub-sección con borde superior 0.5px que dice "Otros skills" en `font-size: 12px; color: var(--color-text-secondary)` y debajo botones que invocan a otros skills del catálogo PC con el contexto del proyecto ya cargado. Estos botones aparecen **siempre** (independiente del diagnóstico) porque son **complementarios**, no correctivos:

| Skill destino | Texto del botón | Prompt que dispara |
|---|---|---|
| `pc-delivery-jira-pending-tracker` | "Revisar pendientes del cliente ↗" | `Activa el skill pc-delivery-jira-pending-tracker para el proyecto Jira <KEY>. Sáltate el paso de elegir proyecto (ya está elegido). Pediime el período (default: últimos 15 días) y el cliente, después revisa Gmail, Confluence y otras fuentes para extraer External pendings y ármame el widget chat-inline de revisión.` |

Cuando se sumen otros skills cross-relevantes a futuro, se agregan a esta misma sub-sección sin contar contra el límite de 4 acciones correctivas.

## Zona 4 — Tabla de hallazgos individuales con botón por fila

Tabla con border-radius-lg listando hasta 30 hallazgos (paginar si hay más). Columnas:

- **Issue** — link a Jira (`<a href="https://procontacto.atlassian.net/browse/<KEY>">`) en `font-mono`, `--color-text-info`.
- **Summary** — truncado a 60 chars.
- **Categoría** — badge con `c-{ramp}` según categoría: unassigned `c-blue`, overdue `c-red`, no_date `c-amber`, blocked `c-purple`, no_release `c-green`, artifact_orphan `c-coral`, posible_mistype `c-pink`, no_worklog `c-amber`.
- **Acción sugerida** — botón compacto que dispara `sendPrompt` con un prompt **específico al issue**.

Texto del prompt por categoría (sustituir `<KEY>` y `<SUMMARY>`):

| Categoría | Texto del prompt |
|---|---|
| `unassigned` | `Asigna <KEY> usando histórico del epic. Muéstrame el match propuesto y el preview. Sin escribir hasta mi OK.` |
| `overdue` / `no_date` | `Propón duedate para <KEY> usando el active sprint del proyecto. Muéstrame preview. Sin escribir hasta mi OK.` |
| `no_release` | `Asigna fixVersion a <KEY>. Lístame las releases abiertas y propón cuál usar. Sin escribir hasta mi OK.` |
| `blocked` | `Muéstrame la cadena de bloqueo de <KEY> (qué issues lo bloquean y su status). Es informativo — no se ejecuta fix.` |
| `artifact_orphan` | `Para <KEY>, corre search_files en Drive y get_metadata en Figma con el nombre "<SUMMARY>". Muéstrame top 3 matches. Sin escribir hasta mi OK.` |
| `posible_mistype` | `Reclasificame <KEY> ("<SUMMARY>") al issue type recurrente correspondiente. Génerame pasos manuales — el skill no toca issuetype.` |
| `no_worklog` | `Para <KEY> ("<SUMMARY>") en in-progress sin tiempo cargado, muéstrame cuándo entró a in-progress y ármame draft de DM al assignee pidiendo que cargue las horas. Sin enviar hasta mi OK.` |

**Después del widget**, en chat, una sola línea de prosa cerrando: "Toca cualquier botón para arrancar el preview de ese fix — nada se aplica hasta tu OK explícito en el PASO 3." Ningún resumen narrativo previo: el widget habla por sí solo.

## Caso especial: proyecto en Sprint 0 sin releases

Si en el diagnóstico se detecta que `Q5 (sin release) > 0` **y** el proyecto no tiene `fixVersions` creadas, agregar al inicio del widget un **callout informativo** con `--color-background-info`:

> Contexto: el proyecto está en Sprint 0 y aún no tiene releases creadas en Jira. Para los fixes de release, vas a necesitar crear al menos una versión en el proyecto (no es algo que el skill haga — el PM lo hace desde la UI), o marcarlos como `manual`.

El callout no reemplaza el widget — va arriba como banner.

## Sub-categoría informativa "Posible mistype"

Si Q3.b/Q5.b detectan posibles mistypes, aparece como una fila más en la tabla resumen (con badge gris claro "informativo") y los issues correspondientes en la tabla detallada con su categoría `posible_mistype`. **No se cuentan en "Hallazgos accionables"** ni en las acciones globales — sólo aparecen en el botón global de reclasificación manual y en el botón por fila.
