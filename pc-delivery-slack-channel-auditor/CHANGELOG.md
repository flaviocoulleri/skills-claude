# Changelog — pc-delivery-slack-channel-auditor

Historial de versiones del skill. El runtime NO lee este archivo: vive acá
para no inflar el SKILL.md, que se carga entero en cada invocación.

---

2.16.0 (2026-06-29): Refactor estructural + estandarización de widgets. Sin
cambio funcional de runtime. Cambios:
(1) Changelog movido a este CHANGELOG.md (antes embebido en SKILL.md, ~345
    líneas que no aportaban al runtime). SKILL.md sólo deja un puntero.
(2) Nuevo `references/widget-shell.md`: shell canónico con HTML literal de
    bloques reutilizables (shell-root, header-card, kpi-grid, banner,
    data-table, checklist-block, button-row, badges) + todas las reglas de
    dark mode. Es la única fuente de verdad del markup de los 8 widgets.
(3) Las 8 fases (0, 3A, 5.2, 6, 7, 8, 9, 10) dejan de describir HTML en prosa
    y pasan a componer bloques del shell. Garantiza que widgets equivalentes se
    rendericen idénticos. La "🌓 REGLA DE TEMA" del SKILL.md queda como puntero
    corto al shell.
(4) Creado `references/dm-follow-up-template.md` (estaba citado 5x pero NO
    existía — referencia rota). Contiene templates single+multi de Fase 7,
    banned phrases, sugerencia por proyecto y catálogo de métricas por módulo,
    extraídos del SKILL.md.
(5) "Errores comunes" comprimido de lista plana (~165 líneas) a clusters
    temáticos, dedupeando entradas que sólo repetían una regla ya escrita en su
    sección dedicada (ahora apuntan a la sección/reference).
(6) Borrado `assets/audit-artifact.html` (deprecado desde v2.2.0).
(7) **Removido el single-project mode** (introducido en v2.14.0) — no funcionó
    bien en la práctica. Se eliminó: el input de threshold en Fase 0, el Paso
    7.1.5 (detección), el branching de Paso 7.2, el banner de Paso 7.6, el badge
    🎯 de la tabla de Fase 5.2, el template single en el reference y los campos
    `dm_compose_mode` / `focused_project_id` / `single_project_threshold_days`
    del objeto `audit`. Fase 7 ahora arma siempre el DM multi-proyecto clásico.
(8) **Widgets alineados con la plataforma `visualize`** (decisión del usuario):
    el shell pasa de dark forzado (variables `--color-*` propias) a **tema
    auto-adaptable** con tokens nativos (`--surface-*`, `--text-*`, `--bg-*`,
    `--border*`); los badges pasan de **emoji a íconos Tabler**; la tabla de
    Fase 5.2 usa **scroll horizontal**. El bloque `shell-root` (wrapper dark) se
    eliminó: los widgets arrancan directo. Los emoji se conservan solo en el
    texto de mensajes Slack (drafts de Fase 6/7/10), que no es HTML de widget.
    SKILL.md quedó en ~2180 líneas.

2.15.0 (2026-06-05): Dark mode forzado + sugerencias por proyecto en DM.
Dos cambios:

A) Dark forzado siempre — la "REGLA DE TEMA" v2.10 mandaba CSS variables
   que auto-adaptan. Ahora se refuerza: el widget se renderiza SIEMPRE
   en dark mode, sin importar la preferencia del host. Implementación:
   wrapper raíz con `color-scheme: dark` + override explícito de las
   CSS variables al stop dark (background primary -> zinc-900, secondary
   -> zinc-800, text primary -> zinc-50, etc.). Esto evita que un caller
   con chat en light vea un widget light cuando el equipo está
   estandarizado en dark.

B) Sugerencia por proyecto en el DM de Fase 7. Cada ítem listado en el
   DM (single-mode O multi-mode) suma debajo del bullet una línea
   "→ Sugerencia: <acción concreta>" generada por Haiku basada en el
   contexto del proyecto. Reglas:
   - Si hay `client_blocker != none`, la sugerencia es del estilo
     "haz push a <responsable del cliente>" con tono colaborativo:
     "hazle un push amigable a Juan Pérez para que entregue los
     mockups que están trabando el sprint".
   - Si hay externos involucrados (proveedor, consultor de terceros,
     área del cliente que no responde) el push se dirige a ellos por
     nombre o rol.
   - Si no hay blocker pero falta status, la sugerencia es accionable:
     "postear status hoy con avance del Sprint 4 + golive estimado".
   - Si `status_completeness = incomplete`, la sugerencia apunta a
     completar lo que faltó: "actualizar el status existente con la
     fecha de golive que decidiste el lunes".
   - Si `recent_golive = true`, la sugerencia incluye métricas:
     "comparte en el canal las métricas de adopción del primer mes:
     <métricas según módulo>".
   El extractor identifica nombres / roles del responsable del lado
   cliente desde los últimos 10 msgs del canal + el DM 1:1 (Fase 2.5).
   Si no hay nombre claro, usa "el referente del cliente".

2.14.0 (2026-06-05): Single-project mode en Fase 7 para >14d sin status.
Cuando algún proyecto auditado del PM lleva más de 14 días sin postear
status (threshold configurable, default 14), el DM follow-up se enfoca
EXCLUSIVAMENTE en ese proyecto y omite el resto. Si hay >1 proyecto con
>14d, se elige el más antiguo (mayor `last_pm_post_days`). Cambios:
(1) Nuevo Paso 7.1.5 — Detección de single-project mode. Calcula
    `mode = 'single' | 'multi'` y el `focused_project_id` antes de
    armar el draft.
(2) Paso 7.2 ramifica según mode: si `single`, ignora todos los demás
    items y construye una lista de 1 item. Si `multi`, comportamiento
    actual (multi-bloque delivery + support + finalizados).
(3) Paso 7.5 — nuevo template "Single-project DM" enfocado, sin
    listas largas, con cierre apropiado al tipo (delivery/support) y
    pidiendo módulo / golive / próximos pasos / sprint / horas /
    renovación según corresponda.
(4) Paso 7.6 — banner del widget cuando `mode = 'single'`:
    "🎯 Modo single-project: <Project Name> · <N días sin status>".
    El caller ve por qué el DM tiene formato distinto.
(5) Fase 0 — input nuevo "Threshold de single-project mode" (default 14
    días), separado del threshold R0 (que sigue siendo 7).
(6) Tabla Fase 5.2 — proyectos con `last_pm_post_days > 14` ganan badge
    🎯 en la columna days_inactive para señalar que entrarían en
    single-project mode.
(7) Si más de un proyecto tiene `last_pm_post_days > 14`, el resumen
    post-Fase 7 menciona los demás "quedan para próxima ronda" para
    que el caller sepa que se priorizó uno solo deliberadamente.

2.13.0 (2026-06-05): Lectura del DM 1:1 caller↔PM auditado. Los PMs
suelen escribirle al manager (caller) por DM privado cosas que no
pueden decir en el canal externo (problemas con el cliente, comentarios
sensibles sobre el comercial SF, etc.). El skill ahora también lee ese
DM para enriquecer la auditoría. Cambios:
(1) Nueva Fase 2.5 (entre Fase 2 y Fase 3): si `is_manager_audit = true`,
    levantar el canal DM 1:1 caller↔PM (slack_search_users → user.id →
    DM channel) y leer los últimos 30 días de mensajes. Default ON,
    apagable con toggle en Fase 0.
(2) Extracción por proyecto vía askClaude: para cada proyecto auditado,
    detectar si el PM lo mencionó en el DM, con extracto + fecha +
    clasificación (status, blocker, golive, decision, vent, otro).
(3) Nuevas fields en rows: `dm_mentions_in_window` (array),
    `latest_dm_mention_ts`, `has_dm_context` (bool).
(4) Tabla Fase 5.2: columna nueva 💬 DM con counter de menciones. Hover
    o click muestra los extractos en un mini-popover.
(5) Fase 7 integration: el DM follow-up acknowledgea lo que el PM ya
    dijo por DM en vez de repreguntarlo. Acknowledgements van como
    "Como me comentaste el otro día" + extracto corto, no como
    pregunta repetida.
(6) Fase 9 integration: el extractor de updates SF lee canal + DM como
    fuentes válidas. Source_excerpt marca claramente si vino de DM o
    de canal, y SF guarda solo el valor (no la fuente), así el extracto
    sensible del DM nunca termina en un campo SF visible.
(7) Regla nueva "🔒 PRIVACIDAD DEL DM" — el contenido del DM jamás sale
    al canal externo (Fase 6 drafts) ni a artefactos públicos. Solo se
    surface en el widget de auditoría (que ve solo el caller) y en el
    DM de respuesta de Fase 7 (mismo PM, mismos interlocutores).

2.12.0 (2026-06-04): Verificar repo de código + commits recientes.
Nueva kebab action por fila "Verificar repo de código" que dispara la
Fase 10 (nueva). Lee `Project_Asset__c` con tipos de repo de código
aceptados (`BitbucketRepoSlug`, `BitbucketWorkspaceRepoSlug`,
`GitRepoUrl`, `CodeRepo`). Si existe, llama al conector Bitbucket
read-only para ver si hay commits en los últimos 7 días (threshold
configurable). Tres caminos:
(1) Sin asset registrado → widget que ofrece armar un DM al PM pidiendo
    que coordine con su team la creación del repo y el commit inicial
    de la metadata + código (con todas las reglas de tono v2.5+ y
    aprobación obligatoria).
(2) Asset registrado pero sin commits en N días → widget rojo "repo
    sin actividad reciente" con draft de DM al PM pidiendo que su team
    pushee metadata + código pendiente. Tono colaborativo (nunca reclamo).
(3) Asset registrado con commits recientes → widget verde resumen
    "✅ N commits en últimos 7 días por <autores>".
Fase 10 es READ-ONLY contra Bitbucket — no commitea, no crea, no
modifica nada en el repo. Solo lee y reporta, y eventualmente arma un
draft Slack para enviar (que sigue todas las reglas de Fase 7).

2.11.0 (2026-06-04): Acción global "Actualizar SF desde canales".
Nueva CTA global en Fase 5.2 (Sección D) y nueva acción en el kebab por
fila que dispara la Fase 9 (nueva): el skill barre los últimos 14 días
de posts del PM auditado en cada canal externo, extrae con askClaude la
info mapeable a campos de Salesforce (golive, status, completion,
priority, módulo si hay campo) y propone un batch de updates en un
widget checklist con diff (valor SF actual vs valor extraído por proyecto
y por campo). El caller destilda lo que no quiere y aprueba el resto.
La regla widget-first + REGLA DE SEGURIDAD aplica: NUNCA se llama
updateSobjectRecord sin un click explícito en "Aplicar N updates" del
widget. La ventana de 14 días es más amplia que el window de 10 msgs
estándar de Fase 3B (que era para señales de R0/blocker), porque para
updates SF queremos captar todo el contexto reciente. Si el PM no posteó
nada en 14 días, no se proponen updates y el skill avisa en el output.

2.10.0 (2026-06-04): Dark mode obligatorio en todos los widgets del skill.
El bug detectado: las filas de la tabla y las KPI cards renderizaban con
backgrounds hardcoded (blanco/crema) que se veían rotos cuando el host
está en dark mode (chat oscuro). Cambios:
(1) Nueva sección "🌓 REGLA DE TEMA — dark mode mandatory + CSS variables"
    cerca del comienzo del SKILL.
(2) Prohíbe todo color hardcoded en background, color, border-color:
    nada de #fff/#ffffff/white/#f0f0f0/rgb(...) ni nombres de color CSS.
    Único permitido: las CSS variables del design system Anthropic
    (--color-background-*, --color-text-*, --color-border-*) y las
    color ramps c-{gray,blue,red,amber,green,teal,purple,coral,pink}.
(3) Tabla de proyectos (Fase 5.2 Sección C): cada elemento mapeado a su
    variable correcta. Filas R0 rojas usan `var(--color-background-danger)`
    como tint sutil (no llenado pleno). Filas con badge ⚠ Incompleto usan
    `var(--color-background-warning)`. OK usa fondo transparente.
(4) KPI cards: `var(--color-background-secondary)` (no `--primary` que es
    blanco). Cards con valor crítico (>0) suman accent left-border con
    color semántico.
(5) Header card del widget: `var(--color-background-info)` (auto-adapta).
(6) Test mental obligatorio antes de pegar HTML al widget: "si el fondo
    fuera near-black, ¿se lee TODO?". Si la respuesta es no, el código
    está mal.

2.9.0 (2026-06-02): Recent go-live + métricas de adopción + módulo.
Cambios:
(1) Detección de "salió a producción": NO hay campo SF dedicado; el
    skill extrae con `askClaude` (Haiku) sobre los últimos 10 msgs del
    canal el `mentioned_golive_date` (la fecha de golive más reciente
    que el PM declaró en el canal). Si esa fecha está dentro de los
    últimos 30 días → `recent_golive = true`.
(2) Detección del módulo/producto entregado: el mismo extractor levanta
    `mentioned_module` (Sales Cloud, Service Cloud, Marketing Cloud,
    Consumer Goods Cloud, Field Service, Experience Cloud, CRM Custom,
    etc.) basado en lo que el PM dijo en el canal. No hay campo SF.
(3) Nuevo sub-bloque en DM (Bloque A · Delivery): "Recientemente en
    producción". Para cada proyecto con `recent_golive = true`, pedir
    métricas de adopción específicas al módulo detectado. Catálogo en
    references/metrics-by-module.md (embebido como tabla en el SKILL
    porque references/ no está bajo control del plugin).
(4) Cierre DELIVERY actualizado: SIEMPRE pide "¿qué módulo o producto se
    está entregando?" además de golive/pasos/sprint. Esto cierra el loop
    para los proyectos que aún no salieron a prod — la próxima ejecución
    podrá detectar el módulo desde el canal y aplicar el catálogo.
(5) Si `mentioned_module` es null pero `recent_golive = true`, el sub-bloque
    igual incluye al proyecto pero con métricas genéricas + pedido
    explícito "¿qué módulo entregaste?" en esa línea.
(6) Support no tiene "recent golive" en el DM — son contratos recurrentes,
    el momento "fresh production" no aplica (queda como Bloque B normal
    con su cierre de horas/renovación/issues).

2.8.0 (2026-06-02): Distinción Support vs Delivery. Cambios:
(1) SOQL de Fase 1 incluye RecordType.DeveloperName de Project__c.
    Proyectos con RecordType.DeveloperName='Support' se clasifican como
    soporte; el resto como delivery. Si no se puede leer RecordType, fallback
    a Delivery (conservador) y agregar nota en el output.
(2) `project_type` (Delivery | Support) se persiste en cada fila de
    audit.rows.
(3) Tabla de Fase 5.2 gana columna "Tipo" con badge 🚀 Delivery / 🛟 Support
    al lado del project name. Filtro inline nuevo: select "Tipo" además del
    de prioridad/bloqueo/status.
(4) Threshold de R0 se mantiene en 7 días para ambos tipos (decisión
    explícita — no diferenciar push).
(5) Fase 7 — cuerpo del DM dividido en dos sub-bloques: "Delivery" y
    "Soporte". Cada uno mantiene su orden interno (priority ASC,
    last_pm_post_days DESC). Account groups y client blockers cruzan
    ambos bloques (un Account puede tener delivery + support).
(6) Fase 7 — cierres separados:
    • Cierre Delivery (solo si hay items delivery): golive + próximos
      pasos + Sprint 0 o sprint actual.
    • Cierre Support (solo si hay items support): horas consumidas y
      restantes del contrato + próxima review / renovación del contrato
      + issues / pendings con el cliente.
    Si el DM solo tiene items de un tipo, solo aparece el cierre
    correspondiente.

2.7.1 (2026-06-02): Aclaración — canales compartidos por varios PMs.
Cuando un canal externo está linkeado vía Project_Asset__c a múltiples
Project__c con distintos `OwnerId`, `last_pm_post_days` y R0 se calculan
SOLO con mensajes cuyo autor coincide con el `Owner.Email` del proyecto
auditado en esa ejecución. Los mensajes de otros PMs sobre el mismo
canal NO cuentan como "el PM auditado posteó status". Comportamiento
ya correcto en el código de Fase 3B pero ahora explicitado como regla
prominente y agregado a Errores Comunes para evitar regresiones.

2.7.0 (2026-06-02): Prioridad, multi-proyecto por cliente, acciones de
tabla y Jira on-demand. Cambios:
(1) Schema: Project__c.Priority__c se incluye en la query SOQL de Fase 1.
    Número más chico = prioridad más alta. Default = 99 (sin prioridad
    asignada) para no priorizar lo no-priorizado.
(2) Orden en Fase 7 (DM): los ítems se ordenan ASC por priority primero,
    DESC por last_pm_post_days después. Ítems con priority <=2 (alta) van
    en una sección dedicada al tope del DM con tono más insistente
    ("este lo necesitamos puntualmente"), pero respetando la regla de
    "nunca reclamo". Ítems con priority >=10 (baja) quedan al fondo.
(3) Agrupación por cuenta en el DM: si el PM tiene más de un proyecto
    vigente para el mismo Account__c, los canales se agrupan bajo el
    header de la cuenta: "Para <Account>, status de los N proyectos
    activos: <#A> <#B> <#C>". El cierre pide golive+pasos por cada uno.
(4) Tabla de Fase 5 (Sección C) — multi-select por fila + kebab por fila:
    nueva columna "☐" al inicio (checkbox para multi-select), nueva columna
    "⋮" al final (kebab menu). Action bar al pie de la tabla con acciones
    globales sobre las filas tildadas: [Marcar como Completed]
    [Cambiar Status a Ongoing] [Cambiar Status a Stopped]. Kebab por fila
    con las mismas acciones individuales + nueva acción "Cross-check Jira".
(5) Nueva Fase 8 — Jira cross-check on demand. Se dispara EXCLUSIVAMENTE
    desde el kebab "Cross-check Jira" de una fila puntual. Lee tasks,
    sprints activos, releases y issues pendientes del board Jira del
    proyecto y los compara con lo que el PM dijo en los últimos 10 msgs
    del canal externo. Reporta discrepancias en un widget separado.
(6) Toda consulta a Jira queda detrás de pedido explícito del caller. La
    detección automática de Sprint 0 / sprint actual que estaba en Paso
    7.5 (v2.5.0) se REMUEVE. El cierre del DM ahora usa siempre el
    pedido genérico "fin de Sprint 0 si aplica / fin de sprint actual si
    aplica". El conector Atlassian pasa de "opcional para Fase 7" a
    "obligatorio solo si se invoca Fase 8".

2.6.0 (2026-05-28): Patrón checklist para mensajes propuestos. Cuando el
skill propone uno o más ítems para mandar (canales sin update, status
incompletos, bloqueos del cliente, proyectos finalizados, drafts de
status), el widget los muestra como **lista con checkboxes**. Todos
arrancan tildados; el caller deselecciona los que no quiere incluir.
El draft final se rearma en vivo (preview pane) cada vez que cambia un
checkbox. El botón final dice "Aprobar y enviar DM con N items" y queda
deshabilitado si N=0. Aplica a: Paso 7.6 (widget de aprobación del DM
follow-up) y Fase 6 (lista de drafts de status). Nueva sección "REGLA DE
UX — checklist para mensajes propuestos" que documenta el patrón para
futuras fases. Este patrón NO viola la regla de seguridad: cada checkbox
es una micro-aprobación explícita del ítem, y el botón de enviar sigue
requiriendo click final (la fricción se mueve del "una aprobación por
mensaje" al "una aprobación batch sobre el set explícitamente revisado
ítem por ítem", lo cual mantiene la trazabilidad y baja la fricción
cuando los ítems son granulares dentro de un solo DM).

2.5.0 (2026-05-26): Nueva Fase 7 — "DM follow-up al PM auditado". Cuando
Ariel (u otro manager) audita los proyectos de un PM de su equipo, después
del widget de output puede generar un draft de Slack DM al PM auditado con
tono conversacional (no automático). El draft:
(1) Excluye canales con status posteado hace <7 días.
(2) Ordena descendente por días sin status; status incompletos (sin golive
    ni próximos pasos) primero.
(3) Lista canales uno por línea con notación <#CHANNEL_ID> y contador de
    días sin update.
(4) Si es el primer DM del día con esa persona, abre con "¿Cómo estás?".
    Si no, va directo al pedido sin saludo redundante.
(5) Prohíbe frases tipo "arrancamos esta semana", "te pedí ayer", "te pide
    varias veces", "como te dije" — siempre tono de pedido de ayuda, nunca
    reclamo.
(6) Detecta bloqueos del cliente por canal (no vino a meet, no responde,
    no termina de definir temas, no entrega pendientes) y los menciona.
(7) Para los proyectos con pendientes del cliente, calcula la fecha
    hipotética de golive si el cliente entregara, y la incluye en el draft.
(8) Lista aparte proyectos finalizados recientemente (Completion_Summary
    != null) para que el PM los cierre / mueva fuera del seguimiento.
(9) Pide golive + próximos 2-3 pasos por cada proyecto al final. Además,
    si el proyecto está en Sprint 0 pide la fecha de finalización del
    Sprint 0; si ya está en sprint posterior, pide la fecha de cierre del
    sprint actual. Detección automática del sprint vía conector Atlassian
    (board del Project_Asset__c JiraBoardId) — si falla, queda genérico.
(10) Aprobación EXPLÍCITA en widget [Aprobar y enviar] / [Editar] /
     [Cancelar] — nunca se envía sin click. Si Ariel se audita a sí mismo
     este flow no aplica (no tiene sentido auto-DM-arse).
Nuevo CTA `dm_follow_up` en Fase 5.2 (visible cuando pm_email != caller_email
y filtered_r0 > 0). Nuevo `references/dm-follow-up-template.md` con los
ejemplos completos. Banned-phrases list movida a este reference para
trazabilidad.

2.4.0 (2026-05-15): Formato de referencias a canales Slack. Nueva sección
"REGLA DE FORMATO" (ver más abajo): (1) todo canal con channel_id conocido
se referencia como <#CHANNEL_ID> en mensajes de Slack (clickeable al pegar);
(2) múltiples canales van uno por línea, nunca inline separados por comas;
(3) en widgets HTML, la columna Canal usa <a href="slack://channel?id=...">
para que el PM entre con un click.

2.3.0 (2026-05-12): Bug crítico resuelto — el skill confundía "sin asset
en SF" con "sin canal en Slack". Repuestos Boston (y otros) tenían el
canal `cc-repuestosboston` ya creado en Slack pero sin Project_Asset__c
en SF, y el skill iba a crear un canal duplicado. Cambios:
(1) Nuevo Paso 3A.0 — antes de cualquier intento de crear canal, busca en
Slack con `slack_search_channels` usando account slug + project slug + alias
("cc-", "proy-", "ext-") y muestra candidatos al PM vía widget para que
linkee el existente en vez de crear nuevo.
(2) Nuevo CTA `link_existing` en el widget de output (Fase 5.2), visible
cuando `missing_asset > 0`, que dispara el barrido masivo de búsqueda y
proposición de linkeos para todos los proyectos sin asset.
(3) Hardening: aunque el PM diga "crear nuevo", el skill vuelve a verificar
el nombre exacto propuesto antes de invocar la API de creación. Si hay
colisión exacta, frena y obliga a re-elegir.

2.2.0 (2026-05-12): Output reemplazado de artifact HTML a widget único.
El skill ya no crea `mcp__cowork__create_artifact` ni depende de
`assets/audit-artifact.html` (que producía bullets inertes en corridas
automáticas). Toda la salida — KPIs, tabla completa de proyectos auditados
y bloque de CTAs — se renderiza vía `mcp__visualize__show_widget` en una
sola llamada al final de Fase 5. El widget incluye filtros, ordenamiento
inline y botones de acción condicionales que disparan `sendPrompt(...)`.
Esto resuelve el bug recurrente de "recomendaciones de texto en vez de
accionables" en corridas headless / scheduled tasks.

2.1.0 (2026-05-12): Regla widget-first reforzada. Se agrega regla de UX
inflexible: TODA opción, CTA o "próximo paso" que el skill le ofrezca al PM
debe renderizarse vía mcp__visualize__show_widget — prohibido enumerar
opciones como bullets de texto en chat. Fase 5.3 reescrita: el resumen post
auditoría ya no muestra "Próximos pasos:" en texto plano, ahora dispara un
widget con botones (onboarding faltantes / drafts R0 / invitar comercial SF /
ver artefacto). Se documenta el helper `sendPrompt(...)` para todos los CTAs.

2.0.0 (2026-05-05): Reorientación completa. La audiencia del status pasa a ser
el comercial de Salesforce (partner seller), no el cliente final — el cliente
NO está en el canal externo. Nueva regla R0 primaria: PM en silencio +7d. Las
4 reglas históricas de pendientes del cliente quedan como vista secundaria.
Onboarding ampliado: crear canal privado + invitar Owner (PM) + Manager del
PM + comercial SF (mail tipeado). Todos los AskUserQuestion reemplazados por
mcp__visualize__show_widget. Threshold default unificado en 7 días.

1.0.0 (2026-04-25): Primera versión formal bajo la convención
pc-[área]-[sistema]-[objeto]-[acción]. Renombrado desde
`slack-external-channel-auditor`.
