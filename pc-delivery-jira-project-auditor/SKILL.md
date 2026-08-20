---
name: pc-delivery-jira-project-auditor
metadata:
  version: 1.13.3
  last_modified: 2026-05-04
description: >
  Audita la higiene de un proyecto Jira y propone fixes en batch para Project
  Managers y Scrum Masters: issues sin asignar, vencidas, sin fecha,
  bloqueadas, sin release, y artefactos huérfanos (issue type Artefacto sin
  URL válida a Google Drive o Figma). Workflow obligatorio en 3 fases —
  diagnóstico read-only, propuesta con preview en widget chat-inline (máx 10 cambios),
  ejecución sólo con OK explícito del PM. Activar cuando el usuario diga
  "auditar el proyecto", "revisar la higiene del proyecto", "qué issues
  están sin asignar", "issues vencidas", "issues sin fecha", "qué artefactos
  faltan", "artefactos rotos", "muéstrame las dependencias bloqueadas",
  "issues sin release", "ordenar el backlog del proyecto", o cuando un PM/SM
  pide un health-check antes de un steering. NO se superpone con
  pc-delivery-jira-pending-tracker (External pendings del cliente) ni con
  pc-delivery-jira-worklog-tracker (carga de horas). Sólo PMs/SMs aprueban
  cambios. Funciona en español e inglés.
---

<!-- Changelog
1.13.3 (2026-07-13): Fix del bug de issuetype Artefacto→Artifact. La Q6 (artefactos huérfanos) filtraba `issuetype = "Artefacto"`, valor inexistente en la org (el work type real es `Artifact`, id 10209) → la JQL fallaba y la categoría nunca traía artefactos. Corregido a "Artifact" y nombrado el campo real del link (`customfield_10158` Page Link, url) + tipo (`customfield_10263` Artifact Type) con fallback a discovery. Fuente: introspección REST (`_shared/jira/fields-by-issuetype.md`).
1.13.2 (2026-05-04): Bug-fix del scoring y queries de hallazgos. PC trabaja sprint a sprint — los issues de sprints futuros no están asignados, fechados ni con release todavía, y eso es esperable, no un problema. Hasta v1.13.1 las queries Q1 (sin asignar), Q3 (sin fecha), Q4 (bloqueadas), Q5 (sin release) traían todo `statusCategory != Done` y mezclaban backlog real + sprint activo + sprints futuros, generando falsos positivos. Cambios: (1) Las queries Q1-Q5 ahora detectan el active sprint vía Agile API y agregan `AND (sprint = "<active_sprint_id>" OR sprint IS EMPTY)` para limitar el alcance al sprint activo + backlog sin sprint. Los issues de sprints futuros quedan fuera por default. Si no hay active sprint (Sprint 0 o entre sprints), filtran `AND sprint IS EMPTY` solo. (2) Las dimensiones del scoring de Ejecución (asignaciones, estimaciones, fechas, dependencias, epics, distribución de carga) quedan EXPLÍCITAMENTE sobre el sprint activo — antes algunas decían "sprint" ambiguo. (3) Toggle nuevo en el widget de PASO 1.3 "Incluir sprints futuros en el diagnóstico" (default: NO). Si el PM lo activa, la cláusula de exclusión se omite y vuelven los falsos positivos — útil sólo en auditorías exhaustivas previas a un milestone.
1.13.1 (2026-05-04): Dos ajustes. (1) Cambio de default en el PASO 1.3: el scope recomendado ahora es "Todo el proyecto" (antes era "Sólo issues abiertos"). El audit "completo" tiene más sentido como entrada por defecto — los PMs que querían el recorte chico ya saben elegirlo, mientras que los que entran por primera vez se benefician de ver el panorama completo. (2) Acción global nueva "Publicar esta versión en Drive para activar las actualizaciones ↗" que arranca el sistema de verificación de actualizaciones la primera vez (en términos técnicos: bootstrap del registry). El botón hace 3 cosas con un solo OK: crea la carpeta `procontacto-claude/skills-releases/pc-delivery-jira-project-auditor/` si no existe, sube el `.skill` actualmente instalado, y genera un `CHANGELOG.md` extrayendo las entradas del frontmatter. Después de correrlo una vez, todas las versiones futuras se publican ahí y el botón "Verificar actualizaciones del skill" ya tiene contra qué comparar. Si la carpeta ya existía, el botón sólo agrega la versión actual sin sobrescribir nada.
1.13.0 (2026-05-04): Acción meta de auto-update. Botón global nuevo "Verificar actualizaciones del skill ↗" siempre disponible al final de las acciones del PASO 2. Compara la versión instalada (leída del frontmatter del SKILL.md cargado en la sesión actual) contra la latest publicada en una ubicación de release de PC (default: carpeta Drive `procontacto-claude/skills-releases/pc-delivery-jira-project-auditor/`, fallback: cross-skill con `pc-meta-skill-manager` que mantiene el catálogo). Si hay diff, muestra widget chat-inline con el changelog acumulado entre versiones (extraído de los comments del frontmatter del .skill nuevo) y un botón "Descargar nueva versión ↗" con link directo al .skill. Limitación inherente: el skill NO puede recargarse a sí mismo en runtime — el modelo tiene cargada la versión instalada hasta que el PM reinstala manualmente. Después de reinstalar, el PM dispara cualquier audit de nuevo y la nueva versión queda activa. Detalle completo en references/skill-self-update.md.
1.12.0 (2026-04-30): Creación de sprints. Nueva dimensión del scoring "Plan de sprints" (en fase Ejecución, peso 15%) que evalúa: hay sprint activo (40% del sub-score), hay siguiente planeado (30%), cadencia consistente (30%). Si la dimensión saca <60, suma botón global "Crear plan de sprints ↗" al widget del PASO 2. El widget de PASO 3 muestra formulario con cantidad (default 4), duración (default 2 semanas heredada de cadencia histórica si existe), fecha de arranque (próximo lunes), naming (`Sprint N — DD/MM`), goal placeholder editable por sprint, y preview con tabla de los N sprints. Variante para Sprint 0: "Planificar cierre de Sprint 0 ↗" con widget más simple (1 sprint). Ejecución vía `POST /rest/agile/1.0/sprint` por cada sprint (la Agile API requiere boardId, no projectKey — el skill lo descubre vía `fetch` a `/rest/agile/1.0/board?projectKeyOrId=<KEY>`). Restricción ablandada: el skill ahora SÍ crea sprints (máximo 6 por batch, sólo con OK del PM, sólo si el caller tiene rol lead/admin del proyecto). Detalle completo en references/sprint-planning.md.
1.11.0 (2026-04-30): Generación de Weekly Status con branding ProContacto. Acción global nueva "Generar weekly status ↗" que arma un documento Google Docs siguiendo el template formal de PC (header del proyecto, tabla de avance con badges de estado, sprint anterior con issues completados, sprint actual con issues en curso, capacitaciones, roadmap, tabla de acciones pendientes, footer con logo). El estado del proyecto se deriva del scoring (A/B=ON-TRACK verde, C=AT-RISK amarillo, D/F=DEMORADO rojo). Los datos vienen de Jira (sprints + issues), Salesforce (Project__c data), Calendar (capacitaciones próximas) y External pendings via cross-skill con pc-delivery-jira-pending-tracker. Preview chat-inline antes de generar. El doc se guarda en la carpeta Drive del proyecto (detectada via Project_Asset__c tipo "Drive folder", o creada si falta con OK explícito). Detalle completo de estructura, queries por sección, branding y mapeos en references/weekly-status.md.
1.10.0 (2026-04-30): Comunicación al equipo + detección de alcance faltante. (1) Botones nuevos en el widget para postear al canal interno del proyecto: "Postear resumen del diagnóstico al canal ↗" (después de PASO 2) y "Postear resumen del batch aplicado al canal ↗" (después de PASO 4). Ambos abren preview editable del mensaje y requieren OK explícito antes de enviar — sin envío automático. (2) Detección "Falta alcance del proyecto": chequea Project__c.Scope_Document_URL__c, Project_Asset__c tipo "Scope document"/"SOW", y páginas Confluence con keywords scope/alcance/SOW. Si ninguna fuente tiene el alcance, suma botón global "Pedirme cargar el alcance ↗" que dispara DM al caller (quien corre el audit, no al PM dueño del proyecto — diseño pensado para Manager mode donde el caller hace follow-up con el PM después). Detalle de plantillas y queries en references/slack-integration.md.
1.9.0 (2026-04-30): Dos features. (1) Categoría nueva "Sin worklog": detecta issues en estado "In Progress" desde hace >3 días con assignee asignado pero sin tiempo cargado (`timespent IS EMPTY`). Es señal de trabajo en curso sin trazabilidad. Se integra con la categoría "Seguimiento al equipo" — el botón global de DMs ahora cubre 3 razones: sin estimación, vencidas, sin worklog. La plantilla de mensaje agrega la línea correspondiente cuando el motivo es worklog. (2) Status transitions opcionales en TODOS los widgets de PASO 3: cada fila editable suma una columna "Transición" con select de transiciones disponibles del issue (vía getTransitionsForJiraIssue, varían por workflow). Default: "no transicionar". Si el PM elige una transición explícitamente, el batch ejecuta editJiraIssue + transitionJiraIssue para ese issue. Ablanda la restricción "NUNCA cambiar status" — ahora es "NUNCA cambiar status por default; SÍ cambiar si el PM lo selecciona fila por fila".
1.8.0 (2026-04-30): Dos features grandes que se diseñaron juntas para evitar regresiones de latencia. (1) Categoría nueva "Trabajo invisible" que detecta tareas y compromisos en fuentes externas a Jira (ReadAI, Google Meet transcripts, Calendar, Confluence, Slack canales interno y externo, Gmail interno) y los propone para crear como Tasks/Stories. Es la primera y única categoría donde el skill ejecuta `createJiraIssue` — el resto del skill sigue con la regla "no crear nada". Máximo 10 issues nuevos por batch, todos en estado To Do, con description que incluye link a la fuente. Detalle completo en references/multi-source-detection.md (queries por fuente, dedup cross-source, schema del candidato, boundary con pc-delivery-jira-pending-tracker). (2) Estrategia de consultas en 3 niveles para minimizar latencia ahora que hay muchos conectores: Nivel 1 (Core, siempre — Jira + Salesforce, ~3s), Nivel 2 (Scoring contextual, default sólo en Sprint 0 / on-demand en Ejecución, ~+4s), Nivel 3 (Trabajo invisible, siempre on-demand vía botón, ~+12s). Suma fields mínimos por query Jira, time bounds fijos por fuente, cache durante sesión, conectores opcionales degradan silenciosamente, ejecución serial con orden de costo creciente en Nivel 3. Detalle completo en references/query-strategy.md.
1.7.1 (2026-04-30): Mantenimiento — sin cambios funcionales. Reorganización del SKILL.md para bajar de 736 líneas a ~280. El detalle largo se movió a archivos en references/ que el modelo lee sólo cuando los necesita: scoring.md (dimensiones por fase, escala, accionables derivados), jql-queries.md (las 6 queries del PASO 2 + sub-detecciones + fallback Q4), widget-paso-2.md (las 5 zonas del widget de diagnóstico + textos de sendPrompt), widget-paso-3.md (preview de propuesta + variantes), slack-integration.md (las 3 features de Slack — A1+A2, B1, B4). El SKILL.md queda como overview navegable con apuntadores explícitos. Hecho antes de v1.8.0 (crear sprints) para no llevar el archivo a 800+ líneas.
1.7.0 (2026-04-30): Tres incorporaciones grandes. (1) Eliminado el input libre de clave Jira en TODOS los fallbacks — el skill nunca pide tipear una clave. Cuando Salesforce no está disponible (o no devuelve PMs/proyectos para el caller), el PASO 1 ofrece dos rutas con botones: "Mis proyectos" (query Jira por actividad reciente del caller) y "Buscar todos" (widget con search-as-you-type cliente-side sobre los proyectos visibles). (2) Integración con Slack como destino: nueva categoría "Seguimiento al equipo" que detecta issues del sprint sin estimación o vencidos y propone drafts de DM agrupados por assignee — con preview editable y OK explícito antes de enviar. (3) Integración con Slack como fuente de contexto: detección de "bloqueos no registrados" (mensajes con keywords blocker/bloqueado/esperando que no tienen issuelink en Jira) baja el score de la dimensión Dependencias y suma botón "Crear issuelinks sugeridos"; detección de "requerimientos sin cargar" (mensajes del PO con keywords de nuevo feature) se reporta como sub-categoría informativa al lado de Posible mistype. Slack MCP pasa a obligatorio.
1.6.0 (2026-04-30): Unificación de toda la UI a chat-inline. El PASO 3 (preview de propuesta) dejó de usar mcp__cowork__create_artifact (panel lateral) y pasó a usar mcp__visualize__show_widget (chat-inline) — mismo mecanismo que ya usan los PASOS 1.1, 1.2 y 2. Razón: en una conversación con varios pasos encadenados via sendPrompt, abrir un artifact en sidebar rompe el flujo (el sendPrompt del sidebar no siempre se enrutea de vuelta al chat principal y el PM pierde el hilo). Mantener todo inline preserva la continuidad y hace que cada paso quede visible en la transcripción. Eliminada la dependencia de mcp__cowork__create_artifact y de assets/audit-artifact-template.html (ese archivo se mantiene en el directorio como referencia de diseño pero NO se carga por el skill — flagado como deprecated en su comment de cabecera).
1.5.0 (2026-04-30): Agregado scoring de salud del proyecto. El skill ahora detecta la fase (Sprint 0/relevamiento, Ejecución, Indeterminado) y calcula un score 0-100 con letra A-F sobre dimensiones específicas a la fase. Dimensiones de Sprint 0 evalúan plan de reuniones, diversidad de stakeholders, documentación inicial, roles definidos y fecha objetivo de cierre — usando todos los conectores disponibles (Calendar, Confluence, Slack, Gmail, Salesforce) para medir interacción real con cliente y equipo. Dimensiones de Ejecución evalúan historias cargadas, asignaciones, estimaciones, fechas, dependencias explícitas, agrupación por Epic y distribución de carga. El widget del PASO 2 ahora arranca con dos cards de scoring (general del proyecto + sprint activo) y un botón "Ver histórico ↗" on-demand para tendencia por sprint. Si la fase no se puede determinar, el skill cae a un set de dimensiones genéricas (asignaciones + fechas + releases). Cada dimensión floja agrega un botón accionable correspondiente (ej: "Arma la agenda de relevamiento" si plan de reuniones < 60).
1.4.0 (2026-04-30): Agregado accionable cross-skill en el widget del PASO 2: botón "Revisar pendientes del cliente" que dispara sendPrompt invocando pc-delivery-jira-pending-tracker con el proyecto Jira ya seleccionado, para que el PM pueda saltar de la higiene interna al trackeo de External pendings sin perder contexto. Aparece SIEMPRE (independiente del diagnóstico) porque es complementario, no correctivo. La regla del SKILL.md: este botón no cuenta dentro del límite de 4 acciones globales priorizadas — va separado en una fila inferior junto a otros cross-skill links que se sumen en el futuro.
1.3.0 (2026-04-30): Reescritura del output del PASO 2. Antes era un resumen en texto plano markdown; ahora es OBLIGATORIAMENTE un widget chat-inline (mcp__visualize__show_widget) con: (a) stats cards arriba (categorías limpias / hallazgos / cambios aplicados), (b) tabla resumen por categoría con badges de estado, (c) tabla detallada de hallazgos con un botón por fila que dispara sendPrompt con un prompt de fix individual, (d) sección "acciones globales" con 2-4 botones que disparan sendPrompts de fix bulk. El patrón se documentó en detalle con ejemplos de los textos de sendPrompt para cada categoría. Origen del cambio: feedback de Ariel — el skill instalado v1.2.0 mostraba el diagnóstico como texto plano y obligaba al PM a tipear las acciones; con widget interactivo el flow se vuelve un solo click → preview → batch.
1.2.0 (2026-04-30): Reescritura del PASO 1. En lugar de un AskUserQuestion único con campo libre para el proyecto, ahora se rompe en 3 sub-steps con widgets chat-inline (mcp__visualize__show_widget) y botones que disparan sendPrompt: 1.1 — elegir líder de proyecto (PMs con Project__c activos en Salesforce), 1.2 — elegir uno de los proyectos del PM seleccionado, 1.3 — scope + categorías. Salesforce MCP pasa de "opcional" a "obligatorio" (con fallback a campo libre cuando el conector no está disponible). El skill ahora también soporta uso por Managers que auditan proyectos de su equipo, no sólo PMs auditando sus propios proyectos.
1.1.0 (2026-04-30): Fix descubierto en el dry-run del proyecto AIREDSNS. Q3 (sin fecha) y Q5 (sin release) ahora excluyen issue types cuyo nombre matchea patrones recurrentes (weekly, daily, status, recurring, standup) — esos types naturalmente no llevan duedate ni fixVersion y antes generaban falsos positivos. Detección automática vía getJiraProjectIssueTypesMetadata. Además se agrega una sub-detección de "posible mistype": Tasks/Stories cuyo summary matchea esos mismos patrones se flagean como hallazgo informativo (no se ejecuta fix automático — el fix natural es reclasificar el issuetype, lo cual queda fuera del scope del skill).
1.0.0 (2026-04-28): Primera versión formal bajo la convención pc-[área]-[sistema]-[objeto]-[acción]. Reescrita desde un draft inicial llamado pc-delivery-jira-project-manager — el rename normaliza la "acción" (manager → auditor, coherente con pc-delivery-slack-channel-auditor).
-->

# Skill: Auditor de Proyectos Jira

## Descripción

Automatiza el health-check que un Project Manager o Scrum Master de ProContacto hace manualmente cuando quiere verificar que un proyecto Jira está en orden antes de un steering, una review interna o un cierre de sprint. Identifica seis tipos de hallazgo recurrentes:

1. **Issues sin asignar** — abiertos, sin `assignee`.
2. **Issues vencidas** — `duedate < hoy` y status abierto.
3. **Issues sin fecha** — abiertos, sin `duedate`, en tipos donde sí debería haberla (Story, Task, Bug — no Epic).
4. **Dependencias irresolutas** — issues abiertos bloqueados por otros que también están abiertos (link `is blocked by`).
5. **Issues sin release** — abiertos, sin `fixVersion`, en tipos donde sí debería haberla.
6. **Artefactos huérfanos** — issues tipo `Artefacto` (custom issue type del proyecto) sin URL, con URL rota, o con URL apuntando a un sistema que no es Google Drive ni Figma.

Para cada hallazgo, el skill propone un fix concreto y lo entrega en un widget chat-inline (mcp__visualize__show_widget) con preview editable. Sólo después de la confirmación explícita del PM aplica los cambios contra Jira, en batches de máximo 10 issues.

> **Regla fuerte de UI**: TODA interacción del skill con el PM se renderiza como widget chat-inline vía `mcp__visualize__show_widget`. Ningún paso usa `mcp__cowork__create_artifact` (sidebar) ni `AskUserQuestion`. Razón: el flow encadena varios pasos vía `sendPrompt`; abrir un artifact en sidebar o un dialogo modal de AskUserQuestion en el medio rompe la continuidad — el sendPrompt del sidebar/modal puede no enrutearse de vuelta al chat principal y el PM pierde contexto. Mantener todo inline preserva la transcripción completa y la trazabilidad del audit.

Adicionalmente, el skill calcula un **score de salud** del proyecto contra un estándar adaptado a la fase del proyecto. El score complementa los hallazgos: los hallazgos te dicen *qué arreglar mecánicamente*, el score te dice *qué tan bien planificado está el proyecto* — pueden no correlacionar (un proyecto sin issues sin asignar puede tener score bajo si nadie planificó las próximas reuniones).

### Scoring de salud del proyecto

El skill calcula un score 0-100 (letra A-F) que evalúa madurez del proyecto contra un estándar adaptado a la fase:

- **Sprint 0 / relevamiento** — evalúa plan de reuniones, nivel de interacción multi-conector, documentación inicial, roles definidos, fecha de cierre.
- **Ejecución** — evalúa historias cargadas, asignaciones, estimaciones, fechas, dependencias explícitas, agrupación por Epic, distribución de carga.
- **Indeterminado** — fallback con 3 dimensiones genéricas (asignaciones, fechas, releases).

Cuando una dimensión saca <60, suma un accionable correspondiente al widget del PASO 2 (ej: "Arma la agenda de relevamiento", "Pedir estimaciones al equipo", "Rebalancear el sprint"). El histórico por sprint se carga on-demand vía botón "Ver histórico ↗".

**Spec completa con dimensiones, pesos exactos, escala letra→número y prompts literales de cada accionable**: ver `references/scoring.md`. El modelo debe leer ese archivo antes de calcular el primer score en cada sesión.

### Boundary con otros skills

- **No es** `pc-delivery-jira-pending-tracker`: ese trackea compromisos del **cliente** (External pendings) extraídos de emails/transcripts. Este audita la higiene **interna** del proyecto.
- **No es** `pc-delivery-jira-worklog-tracker`: ese carga horas. Este no toca worklogs.
- **No es** `pc-delivery-slack-channel-auditor`: ese audita comunicación con el cliente. Este audita el tablero.

---

## Herramientas requeridas

- **Atlassian MCP**: `getAccessibleAtlassianResources`, `atlassianUserInfo`, `getVisibleJiraProjects`, `searchJiraIssuesUsingJql`, `getJiraIssue`, `getJiraIssueTypeMetaWithFields`, `getJiraProjectIssueTypesMetadata`, `editJiraIssue`, `createIssueLink`, `addCommentToJiraIssue`.
- **Salesforce MCP**: `soqlQuery` sobre `Project__c`, `Project_Asset__c` y `User`. Se usa en PASO 1 para listar PMs activos y mapear a sus proyectos Jira. Si el conector no está disponible, el flow degrada a un widget chat-inline con un campo de texto y botón "Auditar este proyecto" — pero la experiencia es claramente peor (sin auto-discovery de PMs/proyectos) y el skill avisa.
- **Google Drive MCP**: `search_files`, `get_file_metadata`. Para validar URLs y buscar artefactos huérfanos por nombre.
- **Figma MCP** (opcional): `get_metadata`. Para validar URLs de Figma. Si no está conectado, las URLs de Figma se aceptan como válidas si pasan el check de dominio pero no se valida el contenido.
- **Google Calendar MCP** (opcional, suma al scoring): `list_events` para detectar plan de reuniones y nivel de interacción con cliente/equipo en fase Sprint 0.
- **Atlassian Confluence** (parte del Atlassian MCP, opcional): `searchConfluenceUsingCql`, `getConfluencePage` para detectar documentación inicial del proyecto.
- **Slack MCP**: `slack_search_channels`, `slack_read_channel`, `slack_search_public_and_private`, `slack_search_users`, `slack_send_message_draft`. **Obligatorio** desde v1.7.0 — se usa para (a) sumar al scoring de interacción, (b) detectar bloqueos no registrados y requerimientos sin cargar (input), (c) generar drafts de DM al equipo del proyecto (output, A1/A2). Si Slack no está conectado, las features que dependen de él se omiten silenciosamente del widget de PASO 2 — el resto del skill sigue funcionando.
- **Gmail MCP** (opcional, suma al scoring): `search_threads` para detectar threads con dominio del cliente.
- **Visualize widgets**: `mcp__visualize__show_widget` (chat-inline, render seamless con la UI). **Es la única vía de UI del skill** — se usa en TODOS los pasos interactivos: PASO 1.1 (selección de PM), 1.2 (selección de proyecto), 2 (widget de diagnóstico con scoring + acciones), 3 (preview de propuesta de fix con tabla editable y botón de confirmación). NO se usa `mcp__cowork__create_artifact` — los artifacts de sidebar rompen la continuidad del flujo cuando hay sendPrompts encadenados entre pasos.

> Política sobre conectores opcionales del scoring: cuando un conector falta, su contribución al score se reparte proporcionalmente entre los disponibles (no se penaliza al proyecto por la falta del conector — se penaliza la falta de actividad detectada). Si **todos** los conectores de interacción están ausentes, las dimensiones que dependen de ellos se omiten y el scoring usa sólo lo derivable de Salesforce + Jira.

---

## Restricciones

- **NUNCA** escribir en Jira sin confirmación explícita del PM vía el widget chat-inline de PASO 3 (botón "Confirmar y aplicar"). Esto incluye `editJiraIssue`, `createIssueLink`, `addCommentToJiraIssue`.
- **NUNCA** actualizar más de 10 issues por batch. Si hay más hallazgos, ofrecer el siguiente batch — pero cada uno requiere su propio OK.
- **NUNCA** cambiar `status` ni `resolution` **por default**. El skill puede ejecutar `transitionJiraIssue` **sólo** si el PM seleccionó explícitamente una transición en la columna "Transición" del widget de PASO 3, fila por fila. Sin selección explícita, esa columna queda en "no transicionar" y el batch sólo edita los campos típicos (`assignee`, `duedate`, `fixVersion`, links, custom URL).
- **NO** inferir el proyecto Jira de forma automática. El PM lo elige siempre. La consecuencia de auditar el proyecto equivocado y empujar cambios es cara.
- **NO** crear issues nuevos, **EXCEPTO** en la categoría "Trabajo invisible" donde sí se crean Tasks/Stories — máximo 10 por batch, sólo con OK explícito vía widget de PASO 3, en estado `To Do`, con description conteniendo link a la fuente para trazabilidad. Para cualquier otra categoría que sugiera crear (ej: una release nueva), proponer al PM que lo haga manualmente.
- **SÍ crear sprints** (desde v1.12.0) — máximo 6 por batch, sólo con OK explícito vía widget de PASO 3, sólo en proyectos donde el caller tiene rol lead o admin (chequear con `getJiraProjectIssueTypesMetadata` la permission `CREATE_SPRINTS` o equivalente). Los sprints se crean vacíos (sin issues asignados) — la asignación es responsabilidad posterior del PM. Detalle de la lógica en `references/sprint-planning.md`.
- **Artefactos**: si la URL nueva no apunta a `drive.google.com` ni a `figma.com`, **rechazar el cambio**. No aceptar Dropbox, OneDrive, GitHub raw, etc.
- **Rol**: validar en PASO 0 que el `atlassianUserInfo` corresponde a alguien con rol PM/SM. Implementación operativa en `Notas de implementación` — si no se puede validar, asumir buena fe pero **dejar marca en el comentario de auditoría** ("ejecutado por X — rol no verificado").

---

## Flujo completo paso a paso

### PASO 0 — Validar conectores y usuario

Antes de cualquier query:

1. `getAccessibleAtlassianResources` → si falla, decirle al PM:
   > "Necesitas el conector de Atlassian activo. Actívalo en Configuración → Conectores."
   → **Fin del flujo.**
2. `atlassianUserInfo` → capturar `email` + `accountId`. Se usa para firmar comentarios y para el check de rol.
3. Validar Drive con un `search_files` trivial (`pageSize=1`). Si falla, avisar:
   > "Sin Google Drive no puedo validar artefactos. Puedo seguir con las otras 5 categorías de hallazgo — ¿avanzo?"
   El PM decide si continuar o conectar Drive.
4. Validar Figma de la misma forma. Si falla, marcar internamente `figma_disponible = false` — afecta sólo la sub-validación de artefactos Figma.

Si todo OK → PASO 1.

---

### PASO 1 — Elegir PM, proyecto y scope (3 sub-steps)

Este paso ahora se rompe en tres widgets chat-inline encadenados. Cada widget muestra opciones como **botones** que disparan `sendPrompt` con un texto que arranca el siguiente sub-step. El patrón se eligió porque (a) el usuario no tiene que tipear claves Jira de memoria, (b) el flow soporta tanto al PM auditando su propio proyecto como al Manager auditando proyectos de su equipo, y (c) los botones se ven seamless con la UI del chat.

#### PASO 1.1 — Elegir líder de proyecto

Query Salesforce:

```sql
SELECT OwnerId, Owner.Name, Owner.Email, COUNT_DISTINCT(Id) activeProjects
FROM Project__c
WHERE Stage__c IN ('Discovery', 'Build', 'UAT', 'Hypercare')
  AND Id IN (SELECT Project__c FROM Project_Asset__c WHERE Type__c = 'Jira project')
GROUP BY OwnerId, Owner.Name, Owner.Email
ORDER BY COUNT_DISTINCT(Id) DESC
```

Renderizar como `mcp__visualize__show_widget` con un grid 2-columnas de botones: avatar circular con iniciales (color `--color-background-info` + texto `--color-text-info`), nombre del PM, count de proyectos activos. Al final un botón secundario "Buscar otro proyecto por clave Jira" como escape hatch.

Cada botón ejecuta:
```javascript
sendPrompt(`Quiero auditar los proyectos de <Nombre PM>. Lístame sus Project__c activos
con Project_Asset__c tipo Jira project y muéstrame los proyectos como botones
chat-inline para que elija uno.`)
```

**Auto-selección si el caller es un PM con proyectos**: si `atlassianUserInfo.email` matchea el `Owner.Email` de algún PM en la lista **y** ese PM tiene proyectos activos, saltar 1.1 y entrar directo a 1.2 con su selección. El usuario debería ver el sub-step 1.1 sólo si es un Manager o si el PM no tiene proyectos a su nombre.

#### PASO 1.2 — Elegir proyecto del PM

Query Salesforce:

```sql
SELECT Id, Name, Stage__c, Account__r.Name,
       (SELECT Value__c FROM Project_Assets__r WHERE Type__c = 'Jira project' LIMIT 1)
FROM Project__c
WHERE OwnerId = :pmId
  AND Stage__c IN ('Discovery', 'Build', 'UAT', 'Hypercare')
ORDER BY Stage__c, Name
```

Renderizar el segundo widget chat-inline: un grid de botones, uno por proyecto, mostrando `Account.Name — Project.Name` como título y el `jira_project_key` extraído de `Project_Asset__c.Value__c` como subtítulo en `font-mono`. Color del badge según Stage (Discovery → `c-purple`, Build → `c-blue`, UAT → `c-amber`, Hypercare → `c-green`).

Cada botón ejecuta:
```javascript
sendPrompt(`Audita el proyecto <Account.Name — Project.Name> (clave Jira:
<JIRA_KEY>). Avanza al PASO 1.3 para que elija scope y categorías.`)
```

#### PASO 1.3 — Scope y categorías

Widget chat-inline con dos secciones:

1. **Scope** — radio buttons: "Todo el proyecto" / "Sólo issues abiertos" / "Sólo el sprint activo" / "Sólo la próxima release". **Default seleccionado y recomendado: "Todo el proyecto"** — un audit completo da el panorama más útil de entrada. Los PMs que prefieren el recorte chico saben elegirlo manualmente; los que entran por primera vez se benefician de ver todo.

   **Sub-toggle (desde v1.13.2)** — "Incluir sprints futuros en el diagnóstico". **Default: NO marcado**. PC trabaja sprint a sprint, entonces los issues de sprints futuros típicamente no tienen assignee/duedate/release todavía y eso es esperable, no un problema. Por default las queries Q1-Q5 excluyen sprints futuros para evitar falsos positivos. El toggle sólo se prende cuando se hace una auditoría exhaustiva previa a un milestone donde sí importa que los próximos sprints tengan todo cargado.
2. **Categorías** — checkboxes multi-select de las 6 categorías. Todas marcadas por default.

Footer del widget: un solo botón "Empezar diagnóstico ↗" que dispara `sendPrompt` con el JSON del scope + categorías elegidos. Al click → arranca PASO 2.

**No avanzar** a PASO 2 sin que el PM toque el botón. El sendPrompt es la única vía válida — no aceptar respuesta tipeada en chat.

#### Fallback: Salesforce no disponible o sin PMs/proyectos relevantes

**Regla fuerte**: el skill NUNCA pide tipear la clave Jira de un proyecto. Tipear texto libre rompe el patrón del catálogo PC y obliga al usuario a recordar claves de memoria. Si Salesforce no está disponible, el flow se degrada pero sigue siendo todo botones.

Renderizar un widget de **selector de proyecto sin Salesforce** con dos rutas grandes (botones), sin input libre:

**Ruta A — "Mis proyectos"** (botón primario)

Query a Jira para detectar proyectos donde el caller tiene actividad reciente:

```jql
project IN projectsLeadByUser() OR (
  assignee = currentUser() AND updated > -30d
) OR (
  reporter = currentUser() AND updated > -30d
)
```

Agrupar por `project.key` y contar issues. Mostrar los proyectos resultantes como botones (mismo patrón visual que PASO 1.2 — Account/Project/Stage badge). Esto típicamente reduce 320 proyectos visibles a 5-15 relevantes.

**Ruta B — "Buscar todos"** (botón secundario)

Renderizar un widget con search-as-you-type cliente-side. El skill llama a `getVisibleJiraProjects` con `maxResults=50` y paginación, acumula la lista completa, la pasa al widget, y el widget hace filtrado cliente-side mientras el PM tipea. Cada match se muestra como botón clickeable (key + name) que al click dispara `sendPrompt` con la elección.

```html
<input type="text" placeholder="Tipea clave o nombre — AIRE, Avellaneda…"
       oninput="filterProjects(this.value)" />
<div id="results"></div>
```

El listado completo de proyectos vive en una variable JS dentro del widget — el filtrado no requiere round-trip al modelo. Sólo cuando el PM **toca un botón** se dispara el sendPrompt para arrancar PASO 1.3.

**Banner del widget**: aviso warning explicando "Salesforce no está conectado — sin él no puedo auto-descubrir tus PMs ni cruzar con Project__c. El resto del diagnóstico funciona normal."

**Condición de invocación de este fallback**: se usa también cuando Salesforce SÍ está conectado pero el caller no tiene Project__c activos a su nombre (caso típico: alguien del equipo que no es PM pero quiere auditar un proyecto). En ese caso, el banner se ajusta: "No encontré proyectos a tu nombre en Salesforce — audita uno de los que tienes actividad en Jira o busca entre todos los visibles."

---

### Estrategia de consultas en 3 niveles

A partir de v1.8.0 el PASO 2 NO ejecuta todas las consultas posibles de una. Se organizan en 3 niveles para mantener el audit típico bajo 5s:

- **Nivel 1 (Core)** — siempre, automático. Jira Q1-Q6 con fields mínimos + Salesforce 1 query para fase + `getJiraProjectIssueTypesMetadata`. ~2-4s.
- **Nivel 2 (Scoring contextual)** — default sólo si la fase es **Sprint 0** (porque el scoring de relevamiento depende de Calendar/Confluence/Slack para tener sentido). En fase Ejecución, queda on-demand vía botón "Calcular scoring completo ↗" en el widget. ~+3-5s.
- **Nivel 3 (Trabajo invisible multi-fuente)** — siempre on-demand vía botón "Buscar trabajo invisible ↗". Nunca por default. Ejecución serial con orden de costo creciente. ~+8-15s.

Reglas de optimización adicionales (fields mínimos por query, time bounds fijos por fuente, cache durante sesión, conectores opcionales que degradan silenciosamente): ver `references/query-strategy.md`. El modelo debe leer ese archivo antes de la primera consulta de cada sesión.

### PASO 2 — Diagnóstico (read-only)

Ejecutar las queries en paralelo. Todas filtran por el proyecto y scope elegidos.

#### Queries Q1 a Q6 + sub-detecciones

El skill ejecuta 6 queries JQL en paralelo (sin asignar, vencidas, sin fecha, bloqueadas, sin release, artefactos huérfanos) más un pre-step que detecta issue types recurrentes para excluirlos de Q3/Q5, y dos sub-detecciones informativas (Q3.b y Q5.b) para flagear posibles mistypes.

**Spec completa con queries literales, fallback de Q4 sin ScriptRunner y descubrimiento del custom field de URL**: ver `references/jql-queries.md`. El modelo debe leer ese archivo antes de armar el primer diagnóstico en cada sesión.

#### Output del PASO 2 — widget chat-inline con accionables

**Regla fuerte**: el output del PASO 2 NO se renderiza como texto plano markdown en chat. Se renderiza como widget chat-inline vía `mcp__visualize__show_widget` con 5 zonas:

0. **Scoring header** — 2 cards (general + sprint activo) con letra A-F y botones colapsables.
1. **Stats cards** — categorías limpias / hallazgos / cambios aplicados.
2. **Tabla resumen** por categoría con badges de estado.
3. **Acciones globales** — máximo 4 botones correctivos priorizados + sub-sección "Otros skills" para invocar cross-skill (`pc-delivery-jira-pending-tracker`).
4. **Tabla detallada** de hallazgos con botón por fila que dispara `sendPrompt` específico al issue.

**Spec completa de las 5 zonas con prompts literales por categoría, paleta de colores, casos especiales (Sprint 0 sin releases, sub-categoría "Posible mistype"), y reglas de priorización de botones**: ver `references/widget-paso-2.md`. El modelo debe leer ese archivo antes de renderizar el primer widget en cada sesión.

---

### PASO 3 — Armar propuestas de fix

Si el PM dice SÍ, para cada hallazgo derivar un fix concreto. Detalles operativos en `Reglas para sugerir fixes`. Resumen:

| Categoría | Fix sugerido |
|---|---|
| Sin asignar | Histórico del Epic/Component → assignee con más issues resueltos en los últimos 90 días. Si no hay histórico → marcar `manual`. |
| Vencidas | Active sprint del proyecto (vía sprint endpoint) si el issue está en uno; si no, +7 días desde hoy. |
| Sin fecha | Misma lógica que vencidas. |
| Bloqueadas | Sólo reportar la cadena de bloqueo — **no** se auto-resuelve. El fix es informativo. |
| Sin release | Próxima `fixVersion` no released del proyecto, ordenada por `releaseDate` ASC. Si no hay → marcar `manual`. |
| Artefactos huérfanos | `search_files` en Drive + `get_metadata` en Figma por nombre del issue. Top 3 matches con score de similitud. |

**Tomar como máximo 10 hallazgos por batch.** Priorizar en este orden: artefactos huérfanos > bloqueadas > vencidas > sin asignar > sin fecha > sin release. La idea es que lo que más friega visibilidad y trazabilidad sale primero.

#### Render del preview — chat-inline (NO sidebar)

El preview se renderiza con `mcp__visualize__show_widget` (chat-inline), nunca con `mcp__cowork__create_artifact` (sidebar). Estructura: header con título + pill de batch, banner de confianza si aplica, tabla con filas editables (máximo 10) con campo editable según categoría, footer sticky con botones "Confirmar y aplicar (N) ↗" / "Cancelar ↗", y sección colapsable de "Batch siguiente" si hay más de 10 hallazgos.

**Spec completa de columnas, tipos de input por categoría, banner de confianza y variantes especiales (Slack DMs, bloqueos)**: ver `references/widget-paso-3.md`.

---

### PASO 4 — Ejecutar el batch

Sólo cuando el widget de PASO 3 dispara su `sendPrompt` de confirmación con un subset:

Para cada cambio en el subset:

- **Sin asignar** → `editJiraIssue` con `assignee.accountId`.
- **Vencidas / Sin fecha** → `editJiraIssue` con `duedate` (formato `YYYY-MM-DD`).
- **Sin release** → `editJiraIssue` con `fixVersions: [{name: "<release>"}]`.
- **Artefacto huérfano** → `editJiraIssue` actualizando el `customfield_XXXXX` cacheado en PASO 2 con la URL elegida. Antes de escribir, **revalidar** que la URL apunta a `drive.google.com` o `figma.com` — si no, abortar ese cambio individual y reportar.
- **Bloqueadas** → no se ejecuta. Es informativo.

Llamar **una por una** (no paralelo) — Jira responde rápido y queremos ver fallas individuales sin que arrastren al resto. Después de cada éxito, `addCommentToJiraIssue`:

> "Auditoría automática (`pc-delivery-jira-project-auditor` v1.0.0) — campo `<X>` actualizado de `<Y>` a `<Z>`. Ejecutado por `<email del PM>`."

Reportar en chat al final:

```
✅ 9/10 aplicados.
   - MYPROJ-102 → assignee: juan.perez ✅
   - MYPROJ-105 → duedate: 2026-05-15 ✅
   - MYPROJ-200 → URL: https://figma.com/design/abc... ✅
   ...
   - MYPROJ-210 → ❌ falló: el custom field "Artifact URL" requiere un format específico. Saltado.

Quedan 30 hallazgos sin tratar. ¿Sigo con el próximo batch? [SÍ / NO]
```

Si el PM dice SÍ → vuelve al PASO 3 con los próximos 10. Si dice NO → fin.

---

## Reglas para sugerir fixes (detalle)

### Asignado por histórico

Para un issue `X` en epic `E` o component `C`:

```jql
project = "<KEY>"
  AND statusCategory = Done
  AND resolutiondate > -90d
  AND ("Epic Link" = E OR component = C)
ORDER BY resolutiondate DESC
```

Agrupar resultados por `assignee`, contar issues. El sugerido es el de mayor count. Si el top 1 tiene menos de 3 issues, marcar `confianza: baja` y dejar el fix como `manual`.

### Fecha por active sprint

Si el issue tiene `Sprint` asignado y el sprint es `active`, usar el `endDate` del sprint como duedate. Si no, traer el active sprint del proyecto (vía agile API o JQL `sprint in openSprints()`); si tampoco hay, usar `today + 7 días`.

### Release abierta más cercana

Listar `fixVersions` del proyecto donde `released = false` y `archived = false`, ordenar por `releaseDate` ASC. Tomar la primera. Si todas están sin fecha, tomar la creada más recientemente.

### Validación de artefactos

Para una URL `U` asociada a un issue `Artefacto` con título `T`:

1. **Check de dominio**: parsear el host. Aceptado sólo si `host` termina en `drive.google.com` o `figma.com`. Otro host → marcar `huérfano: dominio inválido`.
2. **Check de existencia (Drive)**: extraer el `fileId` del path (`/file/d/<ID>/` o `/document/d/<ID>/`). Llamar `mcp__...__get_file_metadata` con ese ID. Si responde con metadata → válido. Si responde 404 / sin permiso → `huérfano: URL rota`.
3. **Check de existencia (Figma)**: extraer el `fileKey` del path (`/design/<KEY>/...` o `/file/<KEY>/...`). Llamar `mcp__Figma__get_metadata` con ese key. Mismo criterio. Si Figma MCP no está conectado, aceptar la URL si pasa el check de dominio pero anotar `validación parcial`.
4. **Búsqueda de match (cuando falta o está rota)**: para Drive, `search_files` con query `name contains "<T normalizado>"`. Para Figma, no hay `search` nativo en el MCP — sólo es posible si el PM provee una URL candidata. Para Drive, devolver top 3 matches ordenados por similitud (Levenshtein normalizado o token-set ratio sobre el nombre).

**No usar HEAD HTTP requests.** El skill no tiene cliente HTTP libre, sólo MCP. Las verificaciones se hacen vía las tools de cada conector.

---

## Integración con Slack

Slack entra al skill como **destino** (drafts de DM al equipo) y como **fuente** (análisis de canales para descubrir gaps con Jira). Las integraciones son aditivas — si Slack MCP no está conectado, todas las features se omiten silenciosamente del widget de PASO 2 y el resto del skill sigue funcionando.

Tres features:

- **Seguimiento al equipo** (A1+A2 unificadas) — botón global que dispara drafts de DM agrupados por assignee a issues sin estimar o vencidos.
- **Bloqueos no registrados** (B1) — sub-score que detecta keywords de bloqueo en canal interno y los cruza con `issuelinks` de Jira para sugerir links faltantes.
- **Requerimientos sin cargar** (B4) — sub-categoría informativa que detecta mensajes del PO/cliente sobre nuevas features sin issue asociado.

**Spec completa con detección del canal interno, keywords exactas, plantilla de DM, lógica de correlación y restricciones de envío**: ver `references/slack-integration.md`. El modelo debe leer ese archivo antes de activar cualquier feature de Slack.

---

## Categoría "Trabajo invisible" (multi-fuente)

Detección on-demand de tareas, compromisos y requerimientos que viven en otras fuentes (ReadAI, Google Meet transcripts, Calendar, Confluence, Slack canales interno y externo, Gmail interno) pero **no están cargados como issues en Jira**. Es la única categoría donde el skill ejecuta `createJiraIssue` (resto del skill sólo modifica issues existentes).

Activación: el PM toca el botón global "Buscar trabajo invisible ↗" en el widget del PASO 2. Eso dispara las consultas del Nivel 3 (multi-fuente serial con orden de costo creciente). Las stats card "Trabajo invisible" del widget arranca en `?` hasta que se ejecute.

Cada fuente devuelve "candidatos" con campos comunes (`extract`, `source_url`, `timestamp`, `author`, `confidence`). Después de juntarlos, se deduplica cross-fuente por similitud de texto > 80% — si el mismo compromiso aparece en Slack y Calendar, se consolida en una sola fila con badges de las dos fuentes.

El widget de PASO 3 para esta categoría es una variante: tabla con `Fuente` (badge por color), `Extracto` (max 100 chars + link al origen), `Issue propuesto` (input editable: type + summary), `Assignee tentativo`, `Confianza`, `✕`. Footer "Crear N issues ↗" / "Cancelar ↗". Los issues se crean en `To Do` con description que incluye link a la fuente.

**Boundary con `pc-delivery-jira-pending-tracker`**: ese skill carga External pendings del **cliente**. Esta categoría carga trabajo del **equipo** + requerimientos del cliente sin Story. Si los dos detectan el mismo extracto, gana el más específico según las reglas en `references/multi-source-detection.md`.

**Spec completa con queries por fuente, filtros de keywords, lógica de correlación con Jira, deduplicación cross-fuente y schema del candidato**: ver `references/multi-source-detection.md`. El modelo debe leer ese archivo antes de la primera ejecución del Nivel 3 en cada sesión.

---

## Reglas de negocio / no obvias

- **El skill es read-mostly.** El 80% de las invocaciones espera quedarse en PASO 2 (sólo diagnóstico). Si el PM no avanza después del reporte, eso es un éxito — significa que vio el panorama y decidió actuar manualmente. No empujar.
- **Tolerancia a falsos positivos.** Es preferible reportar un hallazgo dudoso (ej: un Epic que en algunos proyectos PC sí lleva fecha) y que el PM lo descarte, que filtrar por reglas tan estrictas que se pierdan casos reales.
- **Idempotencia.** Correr el skill dos veces seguidas sobre el mismo proyecto debe dar el mismo diagnóstico (asumiendo que nadie tocó Jira en el medio) y no crear cambios duplicados — los `addCommentToJiraIssue` son los únicos efectos persistentes y no son problemáticos si se acumulan.
- **El custom field de URL del artefacto puede llamarse distinto en cada proyecto.** No hardcodear nombre. Resolverlo cada vez vía `getJiraIssueTypeMetaWithFields` y cachear sólo durante la sesión.
- **No agresivo con dependencias.** El skill detecta bloqueos, pero **no** propone resolverlos automáticamente — la causa raíz casi nunca está en el campo de link, está en el trabajo subyacente.
- **Una falla individual no detiene el batch.** Si `MYPROJ-210` falla, seguir con los otros 9 y reportar la falla al final.

---

## Ejemplo de conversación esperada

```
PM: haz un health-check del proyecto AVELLANEDA antes del steering del jueves

Claude: [PASO 0: valida Atlassian, Drive OK, Figma no conectado]
        ⚠ Sin Figma no valido contenido de URLs Figma — sigo con el resto.
        [PASO 1.1: show_widget con grilla de PMs — Andrea, Ignacio, Mariana, Diego]

PM: [toca botón "Andrea Casanova"] → sendPrompt automático

Claude: [PASO 1.2: show_widget con proyectos de Andrea — AVELLANEDA aparece en Build]

PM: [toca botón "AVELLANEDA"] → sendPrompt automático

Claude: [PASO 1.3: show_widget con scope (issues abiertos por default) + categorías]

PM: [toca "Empezar diagnóstico ↗"] → sendPrompt automático

Claude: [PASO 2: corre Q1-Q6 en paralelo + scoring]
        [show_widget de diagnóstico chat-inline con:
          • 2 cards de scoring (general: B/78, sprint activo: B/80, fase Ejecución)
          • 3 stats cards (4/6 limpias, 36 hallazgos, 0 cambios)
          • Tabla resumen por categoría con badges
          • 4 botones globales: artefactos, vencidas, asignar, fixVersion
          • Tabla de hallazgos individuales con botón "Reclasificar/Asignar/etc" por fila
          • Sub-sección "Otros skills" con botón "Revisar pendientes del cliente ↗"]

PM: [toca botón global "Buscar matches en Drive/Figma para los 4 artefactos ↗"]
    → sendPrompt automático

Claude: [PASO 3: corre search en Drive, arma payload de 4 fixes]
        [show_widget chat-inline con:
          • Header con badge "Batch 1/2 · 4 issues"
          • Banner: "Confianza alta — todos los matches > 90% similitud"
          • Tabla con 4 filas: Issue / Summary / URL match (dropdown con top 3) /
            Confianza / Fuente / Botón ✕ Descartar
          • Footer: botón "Confirmar y aplicar (4) ↗" + "Cancelar ↗"]

PM: [edita una URL, descarta una fila, toca "Confirmar y aplicar (3) ↗"]
    → sendPrompt con JSON del subset aprobado

Claude: [PASO 4: editJiraIssue x3 en serie, agrega comentarios de auditoría]
        ✅ 3/3 aplicados.
        Quedan 33 hallazgos. ¿Volvemos al diagnóstico para el próximo batch?
        [show_widget chico con botón "Continuar con próximos 10 ↗" + "Cerrar auditoría ↗"]

PM: [toca "Cerrar auditoría ↗"]
    → sendPrompt: "El resto lo veo con el equipo en la daily. Cerramos."
```

**Nota sobre el ejemplo**: cada interacción del PM se hace tocando un botón de un widget (no tipeando texto), salvo cuando explícitamente edita un input editable dentro del widget. Esto es deliberado: garantiza trazabilidad (cada `sendPrompt` queda en el transcript) y evita ambigüedad de interpretación.

---

## Notas de implementación

- **cloudId Atlassian**: detectar dinámicamente en PASO 0 vía `getAccessibleAtlassianResources`. No hardcodear.
- **Validación de rol PM/SM**: enfoque pragmático. Si el `email` del `atlassianUserInfo` está en una lista mantenida en `references/role-allowlist.md` (mantenida por Ariel), aceptar. Si no, dejar el comentario de auditoría con la marca "rol no verificado" y seguir — pero **no** bloquear; bloquear por una lista desactualizada genera más fricción que valor. La auditoría queda en el comentario y eso es suficiente trazabilidad.
- **`issueFunction` (Q4)**: requiere ScriptRunner. Si la query falla con error de parsing, hacer fallback: traer todos los issues abiertos con `expand=issuelinks` y filtrar en memoria los que tienen `inwardIssue` con `type.name = "Blocks"` y status abierto. Más caro pero universal.
- **Active sprint**: la API Agile de Jira da el sprint activo de un board. Si el proyecto no tiene board (ej: kanban sin sprints), saltar la sub-regla y caer al fallback de `+7 días`.
- **Zona horaria**: trabajar en `America/Argentina/Buenos_Aires` para inputs de fecha; convertir a `YYYY-MM-DD` (sin hora) al hablar con Jira.
- **Logging**: cada cambio aplicado deja un comentario en el issue con el nombre+versión del skill. Esto reemplaza un log centralizado.
- **Rate**: Jira Cloud permite ~10 req/seg sostenido. El skill aplica de a uno y no satura. No inventar throttling adicional.

---

## Roadmap futuro

- Confluence: dejar nota en la página del proyecto resumiendo el diagnóstico y los fixes aplicados.
- Schedule: correr el diagnóstico cada lunes a la mañana sobre todos los `Project__c` activos del PM y mandar un DM con el resumen — sin propuesta automática, sólo el headline. Ver `anthropic-skills:schedule`.
- Detección de Epics sin children y sub-tasks huérfanas — categorías 7 y 8.
