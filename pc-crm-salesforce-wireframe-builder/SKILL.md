---
name: pc-crm-salesforce-wireframe-builder
metadata:
  version: 1.9.0
  last_modified: 2026-08-07
  owner: ariel.tarsitano@procontacto.com.mx
description: Genera un SET completo de wireframes navegables de Salesforce Lightning Experience (Desktop 1280px + Salesforce Mobile) a partir de Historias de Usuario, como set HTML SLDS navegable publicado en el gestor de artefactos, o prompt para Claude Design si el usuario lo pide. Hace el análisis previo y descarta las HUs sin interfaz (integraciones, automatizaciones, permisos, data model, testing), arma el inventario reutilizando layouts (una plantilla de Record Page, List View y New/Edit para todos los objetos vía variantes) y clasifica el proyecto como CRM comercial o app operativa sobre objetos custom. Activar cuando el usuario diga "ármame los wireframes", "mockups del proyecto", "pantallas a partir de las HUs", "wireframes navegables", "maquetas de las historias", "build wireframes from user stories". También proactivamente cuando comparta un backlog de HUs (texto, Excel/Word/PDF, o link a Sheets/Docs/Confluence/Jira). Para UNA sola record page puntual usa pc-crm-salesforce-record-prototyper. ES/EN.
---

<!-- Changelog
1.9.0 (2026-08-07): Se cablea la politica de publicacion en el gestor de artefactos de ProContacto: el entregable se publica ahi y no como artefacto de la conversacion, y publicar es siempre de dos pasos (listar_artefactos por titulo canonico -> publicar_version sobre la misma URL si ya existia, publicar_artefacto si no). Sin esa busqueda previa, una conversacion nueva republica de cero y el link ya compartido queda viejo en silencio. El titulo canonico va sin version ni fecha, el gestor-id queda en el trace del HTML, y el gate de vinculacion registra la URL del gestor.
1.8.0 (2026-08-06): Se suma el gate de continuidad de conversacion (_shared/session-continuity/) antes del Paso 0: si el proyecto ya tiene trabajo reciente, se le recomienda al usuario volver a la conversacion donde venia, en vez de rehacer el set sin el contexto. Nunca bloquea. Ademas se formaliza metadata.version en el frontmatter, que faltaba: hasta ahora la version solo vivia en este changelog y no habia forma de saber desde Cowork si el bundle subido era el nuevo o el viejo.
1.7.0 (2026-08-04): Se cablea al motor compartido. El set se materializa con el shell de _shared/wireframe-engine/ (selector de pantallas, zoom/ajustar, anotaciones numeradas con leyenda, encuadre resistente a contenedores que arrancan en 0x0) inyectando SLDS en el token de CSS: el chrome se comparte, la fidelidad SLDS no cambia. Nuevo Paso 2.9: se confirma la carpeta de Drive ANTES de materializar, para que cada iteracion del set suba sola sin volver a preguntar. Nuevo Paso 4.5: widget post-entrega para ajustar o exportar. El HTML liviano del set se sube a Drive y el gate de vinculacion registra el LINK DE DRIVE como Project_Asset__c (antes registraba el uuid del artefacto de Cowork, que apunta a una conversacion ajena). Claude Design pasa de opt-in a ultima opcion marcada en retiro.
1.6.0 (2026-07-17): Se invierte el output. Ahora el DEFAULT es el artefacto navegable en Cowork (HTML SLDS autocontenido con el design system de ProContacto); el prompt para Claude Design pasa a ser opción opt-in cuando el usuario quiere iterar el set en Claude Design. Alinea el skill con el catálogo canónico (pc-delivery-deliverable-orchestrator/references/artifact-catalog.md): wireframes v1 y v2 → artefacto Cowork; Claude Design queda para decks/presentaciones. El análisis (descartes + inventario) no cambia. El artefacto se registra como Project_Asset__c (Type__c='CoworkArtifactId').
1.5.0 (2026-06-08): Tercera ronda de fidelidad + dos módulos nuevos. List View: barra de íconos reforzada al extremo derecho (flex margin-left:auto). Record Page: "Guía para el éxito" en 2 columnas (Campos clave a la izquierda máx 5, texto a la derecha); tab "Relacionado" en panel derecho que agrupa TODAS las related lists incluido Historial de cambios como una related list más; sub-tabs de Actividad (Nueva tarea/Registrar llamada/Nuevo evento/Correo) cada una con su composer; secciones de Detalles con banda de encabezado gris de ancho completo. New/Edit: estado de validación con el patrón real (campo borde rojo + ícono ⊘ + mensaje debajo, popover "Encontramos un problema / Revise los siguientes campos" anclado a Guardar, ⊘ junto a Guardar), textos en español. Regla global de idioma (toda la UI en el idioma del proyecto, nada de inglés). Nuevos módulos condicionales con chrome propio y SIN versión mobile: Salesforce Maps (Layers/Routes/Schedule/List) y Planificador avanzado de visitas (wizard: segmentación con filtros, ventanas de visita por día, asignar usuarios, timeframe del plan, optimización en batches).
1.4.0 (2026-06-07): Segunda ronda de fidelidad tras prueba real. Home: dashboard/reportes en columna izquierda (ancha) y Actividades a la derecha (angosta), sin lista de registros al pie. List View: barra de íconos alineada a la derecha. New/Edit: mostrar siempre un campo en estado de error de validación (regla del backlog si existe, genérica si no) + recuadro de error de página. Record Page: tab "Relacionado" en panel derecho con related lists del objeto (default Archivos/Notas/Adjuntos + estándar del objeto + custom, o las que pidan las HUs), sub-tabs de Actividad todas con composer activo, encabezados de sección de Detalles con fondo gris claro. Lead Convert reducido a una sola pantalla con toggle crear/vincular por registro. Nuevo wireframe condicional Web-to-Lead (form público, estilo web neutro sin chrome SLDS). Pantalla de Solicitud de Aprobación reestructurada: datos como compact layout en header con Aprobar/Rechazar solo arriba, detalle del registro a la izquierda, Comentarios + Historial a la derecha.
1.3.0 (2026-06-06): Correcciones de fidelidad tras prueba real en Claude Design. Header global y mobile forzados a blanco (nunca navy) + logo nube de Salesforce por default. Home: 2-3 charts de dashboard de ejemplo y sin bloque de accesos rápidos de alta. List View: view switcher como dropdown (no tabs), panel "Filters" estándar, barra de íconos, caret por columna y meta "N items • Updated…". Record Page: "Guía para el éxito" en el Path, botón de etapa en línea con los chevrons, solo la tab "Relacionados" al panel derecho, secciones de Detalles ordenadas. Aprobaciones reescritas y condicionadas a que el backlog tenga HUs de aprobación (badge + banner solo-lectura + pantalla de Solicitud de Aprobación + notificación). Mobile siempre en sección separada del Desktop con patrones de la Salesforce Mobile App. Sumados blueprints de chrome/navegación/procesos en slds-component-blueprints.md y nota de header en slds-design-tokens.md.
1.2.0 (2026-06-06): Sumada la capa estructural del design system en references/slds-component-blueprints.md: clases SLDS reales (convención slds- / _ / slds-is-), anatomía de Data Table, Page Header, Card, Tile, Description List y Related List, patrones de layout (Record Home, List View, Split View) y la densidad compacta característica (tablas header 32px/13px/700, celdas 4×8px/13px). Cableado en wireframe-prompt-template.md (nueva sección "Clases y densidad SLDS") y referenciado desde los Pasos 3 y 5 del SKILL.
1.1.0 (2026-06-06): Sumados los design tokens oficiales del Salesforce Lightning Design System (color, tipografía, spacing, radios, sombras) en references/slds-design-tokens.md, con mapeo token→componente y CSS custom properties para el fallback. Cableados en wireframe-prompt-template.md (nueva sección "Design tokens SLDS" + reglas de fidelidad con valores exactos) y referenciados desde los Pasos 3 y 5 del SKILL. Fondo de página corregido a #f3f2f2 (warmGray-3, el valor real de LEX) en lugar de #f4f6f9.
1.0.0 (2026-06-05): Primera versión bajo la convención pc-[área]-[sistema]-[objeto]-[acción]. Convierte la "Plantilla reutilizable de wireframes Salesforce Lightning" de ProContacto en skill para Cowork y Code. Hermana mayor de pc-crm-salesforce-record-prototyper: el prototyper materializa UNA record page; este skill arma el SET completo navegable (Desktop + Mobile) a partir de un backlog de HUs, con descartes + inventario de reutilización. Output principal: prompt para Claude Design. Fallback: set HTML SLDS. La plantilla de fidelidad vive en references/wireframe-prompt-template.md.
-->

# SF Wireframe Set Builder

Esta skill toma un **backlog de Historias de Usuario** y produce un **set de wireframes navegables de Salesforce Lightning Experience** (Desktop 1280px + Salesforce Mobile App), indistinguibles de una implementación real de Lightning. El output principal es un **artefacto navegable en Cowork**: HTML SLDS autocontenido que aplica el design system SF de ProContacto; un consultor/admin Salesforce debe reconocer al instante Navigation Bar, Home, List Views, Record Pages, Path, Related Lists, Activities, Chatter, Files, Quick Actions, Approvals y Salesforce Mobile.

> **Regla de oro.** El valor de esta skill está en el *análisis* (qué HUs tienen interfaz, cómo se reutilizan los layouts) y en *materializar el set con alta fidelidad* usando los design tokens y blueprints SLDS de `references/`. No diseñes CRM genérico, dashboards SaaS modernos ni layouts inventados: sigue estrictamente el design system de ProContacto que vive en las referencias del skill.

---

## Diferencia con pc-crm-salesforce-record-prototyper

| | `record-prototyper` | `wireframe-builder` (este) |
|---|---|---|
| Alcance | UNA record page de un objeto | SET completo navegable de un proyecto |
| Input | Un objeto / un registro | Backlog de HUs (texto, adjunto o link) |
| Hace análisis de descartes + inventario | No | Sí (obligatorio) |
| Desktop + Mobile encadenados | Opcional | Sí, navegables entre sí |

Si el usuario sólo quiere mostrar una pantalla puntual, deriva al prototyper. Si quiere "las pantallas del proyecto" / "los wireframes de estas HUs", es este skill.

---

## Output: set HTML en el gestor (default) vs prompt Claude Design (última opción)

Por default genera el **set navegable HTML SLDS autocontenido y lo publica en el gestor de artefactos de ProContacto** (ver Paso 3.5). No se renderiza como artefacto de la conversación: el gestor es el único destino, porque es el que versiona sobre la misma URL. Sólo armas el prompt para Claude Design si el usuario lo pide explícitamente:

| Situación | Output |
|---|---|
| Default: set de wireframes de un proyecto | **HTML SLDS publicado en el gestor** |
| Está en **Claude Code** y quiere los `.html` en el repo | Set HTML SLDS (archivos en el working dir / outputs) |
| Lo necesita embebido (Confluence, Slack canvas) | Set HTML SLDS |
| El usuario dice "lo quiero iterar en Claude Design", "dame el prompt para Claude Design" | Prompt para Claude Design (última opción, en retiro) |

Este skill es el productor canónico de wireframes v1 (venta) y v2 (Anexo C del Sprint 0); ambos se publican en **el gestor de artefactos** según el catálogo (`pc-delivery-deliverable-orchestrator/references/artifact-catalog.md`). Claude Design **está en retiro** en ProContacto: no lo ofrezcas como default ni como equivalente; sólo si el usuario lo pide expresamente.

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

## Flujo de trabajo

### Paso 0 — Leer la fuente de HUs y clasificar el proyecto

Primero consigue las HUs. Según de dónde vengan:

- **Texto pegado** → léelo directo.
- **Adjunto** (Excel, Word, PDF, CSV) → lee el archivo. Si está en `/mnt/user-data/uploads` y no ves su contenido en contexto, sigue el skill `file-reading` para elegir la herramienta correcta (xlsx/docx/pdf). En Claude Code, abre el archivo del repo.
- **Link**:
  - Confluence / Jira → usa el conector **Atlassian** (`Atlassian:search`, `Atlassian:getConfluencePage`, `Atlassian:searchJiraIssuesUsingJql`).
  - Google Sheets / Docs / Drive → usa **Google Drive** (`Google Drive:search_files`, `Google Drive:read_file_content`).
- Si no puedes acceder al link/adjunto, avisa y pide que peguen el contenido como texto. No inventes las HUs.

Luego **clasifica el proyecto** (define qué patrones entran):

- **CRM comercial** (hay Leads, Oportunidades, Cotizaciones, Pedidos, forecast, Home de vendedor): habilita Home Lightning, List Views de objetos estándar, Record Pages, Path, Lead Convert, Kanban + Forecast, Approvals.
- **Integración / app operativa** sobre objetos custom o un objeto eje (LWCs, wizards, record pages de un objeto específico): NO metas Home de vendedor, Leads, Oportunidades, Cotizaciones ni Forecast salvo que una HU lo pida. Centrá el set en la(s) Record Page(s) del/los objeto(s) eje y en los LWCs/Quick Actions descriptos.

Incluye cada patrón **sólo si alguna HU lo requiere**. No fuerces secciones que el alcance no tiene.

### Paso 1 — Historias descartadas para diseño (genera esta sección primero)

Descarta las HUs que **no tienen interfaz**: integraciones, automatizaciones, flujos backend, batch/cron, reglas de negocio, validaciones, permisos/Sharing Rules, Permission Sets, CMTs, data model/campos, testing y config técnica.

Presenta una **tabla**: `ID | Nombre | Motivo del descarte`. Si hay muchas HUs (>40), agrupa los descartes por épica/módulo con el motivo, aclarando qué HUs de esa épica SÍ van a diseño.

### Paso 2 — Inventario de Wireframes con reutilización (genera esta sección segundo)

Detecta historias similares, agrúpalas y reutiliza layouts/componentes. Reglas de eficiencia (obligatorias):

1. Minimiza la cantidad de wireframes; maximiza la reutilización.
2. **Una sola** plantilla de Record Page se reutiliza para TODOS los objetos (cambian compact layout, Path, tabs y related lists). Lo mismo con List View y con el formulario New/Edit.
3. Agrupa historias similares en un mismo wireframe usando **variantes**, no pantallas nuevas.
4. Wireframe nuevo SÓLO si hay diferencia funcional significativa.

Presenta una **tabla**: `Wireframe | HUs cubiertas | Variantes | Componentes reutilizados`.

### Paso 2.9 — Confirmar la carpeta de Drive (antes de materializar)

Corré el gate de `_shared/drive-upload/drive-upload.md` con el widget `subir-a-drive.html`
(`{{AREA_LABEL}}` = "Delivery"), **una sola vez y antes de armar el set**. Ruta:
**`J - Delivery / B - Proyectos / {Cliente} / {Proyecto}`**. Confirmarla acá es lo que permite que
cada iteración del set suba sola, sin interrumpir al PM en cada corrección.

### Paso 3 — Materializar el set (HTML SLDS, default)

Usá el shell `_shared/wireframe-engine/assets/wireframe-shell-template.html`: ya trae **selector de
pantallas, zoom/ajustar y anotaciones numeradas** con su leyenda, más el encuadre resistente a
contenedores que arrancan en 0×0. No improvises ese chrome.

Tokens del shell: `WF TITLE`, `WF TRACE`, `WF CSS` (acá va el design system **SLDS**, no el kit gris
de baja fidelidad del shell), `WF SCREENS` (una `<section class="wf-screen" data-nombre="…">` por
pantalla) y `WF NOTAS` (el JSON de anotaciones por pantalla).

> **Las anotaciones no son decorado.** Un set de wireframes sin las preguntas abiertas anotadas
> ("falta definir si el supervisor ve el consolidado acá o en Cobertura") es un dibujo; con ellas es
> un instrumento de revisión. Anotá lo que quedó sin decidir, no lo que ya es obvio en la pantalla.

Genera el set como HTML SLDS autocontenido, aplicando el design system con alta fidelidad. Lee `references/wireframe-prompt-template.md` para las reglas de fidelidad, `references/slds-design-tokens.md` para los valores exactos (define los tokens como CSS custom properties `:root { --slds-... }` y referéncialos; no hardcodees hex sueltos) y `references/slds-component-blueprints.md` para las clases SLDS, la estructura de cada componente y la densidad compacta de tablas (header 32px/13px/700, celdas padding 4×8px/13px).

Arma un set navegable entre pantallas (siguiendo el patrón Home → tab del Objeto → List View → Registro → Editar → procesos), con Desktop 1280px + Salesforce Mobile y datos de muestra coherentes (mismo registro a lo largo del flujo). Según el entorno:

- **Cowork**: renderiza el artefacto con `mcp__visualize__show_widget` (un único HTML autocontenido con navegación interna entre pantallas; evita `display:none` durante el streaming) y/o guarda el `.html` en outputs.
- **Claude Code**: escribe los `.html` navegables entre sí en el repo / working dir.

### Paso 3.5 — Publicar el set en el gestor (antes de entregar)

**El entregable se publica en el gestor de artefactos de ProContacto — nunca como artefacto de la
conversación.** Lee `_shared/artifact-publish/artifact-publish.md` y aplica su procedimiento, que es
de dos pasos y no de uno:

1. `listar_artefactos` y busca por título canónico `{Cliente} · {Entregable} · {Tipo}` (sin versión
   ni fecha en el título — la versión vive adentro del artefacto).
2. Si ya existía → `publicar_version` sobre la misma URL, con un `message` que diga qué cambió.
   Si no → `publicar_artefacto`, y anota el `id`.

Nunca publiques sin haber buscado primero, aunque estés seguro de que es nuevo: una segunda
publicación del mismo entregable deja al cliente con un link que quedó viejo sin que nadie se entere.
Escribe el link del gestor en el chat — publicar sin mostrar el link es no publicar — y deja el `id`
en el comentario de trazabilidad del HTML.

Exportar a PDF u otro formato **exige que el artefacto ya esté publicado**: sin eso, el archivo que
circula no tiene original identificable detrás.

El link del gestor es lo que entregás en el Paso 4 y lo que se registra en el gate de vinculación.

### Paso 4 — Entregar el link y subirlo a Drive

Devuelve en orden: **(1)** la tabla de descartes, **(2)** la tabla del inventario, **(3)** el **link del gestor** del Paso 3.5 (el link es el entregable: no adjuntes el HTML ni lo rendericies como artefacto de conversación), **(4)** el **gate de vinculación** (ver `_shared/artifact-linkage/artifact-linkage.md`): el wireframe es `Type__c='WireframeId'` — si es de un deal se registra como `Project_Asset__c` en SF, y si es de un proyecto Blueprint como issue `Artifact` en Jira (los wireframes v1→v2 suelen ir en **ambos**). Como el set se publicó en el gestor (Paso 3.5), dejá **además** el asset `Type__c='ProContactoArtifactId'` con el **uuid** de `artifacts.procontacto.com.mx/a/<uuid>` en `Value__c` y la `Description__c` diciendo qué set es (`Wireframes v2 — 14 pantallas de la consola de ventas`): cada id va en el tipo que corresponde a su sistema, porque `Link__c` deriva la URL del `Type__c`. Ofrece y crea **solo con OK**; si falta el contexto, déjalo pendiente sin bloquear. Si el skill corre dentro de un flujo de delivery, devuelve el control al orchestrator para el registro.

### Paso 4.5 — Ofrecer corregir o exportar

Mostrá el widget post-entrega con las opciones de ajustar el set o llevárselo en PDF/imágenes. Si el
PM pide cambios: corregí y **publicá la versión nueva con `publicar_version` sobre el mismo `id`** —
la URL no cambia, así que el link que el PM ya tiene muestra lo corregido sin reenviar nada. Después
volvé a subir el HTML a Drive avisando con el link y mostrá el widget de nuevo. La carpeta ya está
confirmada — no se vuelve a preguntar.

### Paso 5 — Opción Claude Design (última opción, en retiro)

**ProContacto está discontinuando el uso de Claude Design.** Va como **última opción** y no
recomendada: si el usuario lo pide, decí en una línea que el set ya está hecho acá y que lo que arme
allá arranca de cero y no se exporta desde acá; si insiste, hacelo sin fricción. Si el usuario quiere iterar el set en Claude Design, ensambla el prompt: lee `references/wireframe-prompt-template.md` y completa sus placeholders con lo resuelto en Pasos 0–2. El prompt debe llevar baked-in: la orden de usar el design system del proyecto, los **design tokens SLDS** y las **clases y densidad SLDS** (ambos resúmenes ya embebidos en la plantilla; fuentes completas en `references/slds-design-tokens.md` y `references/slds-component-blueprints.md`), el inventario ya resuelto, el detalle de las HUs por wireframe, las reglas de fidelidad y el requerimiento Desktop + Mobile. No mandes el prompt con placeholders `{{ }}` sin resolver, y no abrevies datos con "etc." (Claude Design no ve esta conversación). Entregá el prompt en un fenced code block copiable + las instrucciones de "Cómo y dónde pegar el prompt" (abajo).

---

## Cómo y dónde pegar el prompt (solo camino opt-in Claude Design)

Aplica únicamente cuando el usuario pidió el prompt para Claude Design (Paso 5). Después del bloque del prompt, incluye siempre estas instrucciones (no muestres el ID ni el URL directo del proyecto — confunde si el usuario no tiene acceso):

> **Para materializar los wireframes:**
>
> 1. Ve a **claude.ai/design** y entrá al proyecto **"ProContacto · Salesforce Design System"** desde tu lista de proyectos. Si no lo ves, pídele acceso a Ariel Tarsitano.
> 2. Dentro del proyecto, abre una **nueva conversación**. Es importante que sea dentro del proyecto: fuera no tiene el design system cargado.
> 3. Pega el prompt completo de arriba como primer mensaje.
> 4. Claude Design genera el set aplicando el design system. Iterá libre ("suma el tab Files", "agrega la variante de List View de Cases", "arma la versión mobile del wizard").
> 5. Cuando esté listo, descarga el HTML o toma las capturas para el deck / HU / demo.
>
> Si Claude Design no toma el design system, repítele en la primera línea: *"Usa estrictamente el design system de este proyecto, no inventes tokens"*.

El ID del proyecto Claude Design (`9bfeb33a-bf39-4769-8f96-aa0a79b94122`) es referencia interna tuya, no para el usuario.

---

## Ejemplos de uso

### Ejemplo 1 — Backlog en Confluence, CRM comercial
**Usuario:** "Ármame los wireframes a partir de las HUs de este Confluence: [link]."
**Claude:** abre el page vía conector Atlassian → clasifica como CRM comercial → tabla de descartes (deja afuera integraciones, validaciones, permisos) → inventario reutilizando Record Page/List View/New-Edit + Lead Convert + Kanban+Forecast + Approvals → materializa el set como artefacto Cowork (HTML SLDS navegable) con el detalle de cada HU → lo renderiza con show_widget y explica cómo registrarlo como Project_Asset__c.

### Ejemplo 2 — App operativa sobre objeto custom, Excel adjunto
**Usuario:** "Estas son las HUs (adjunto .xlsx). Haz las pantallas." (objeto eje `Visit_Job__c`, hay un wizard LWC)
**Claude:** lee el xlsx (skill `file-reading`) → clasifica como app operativa (NO mete Home/Leads/Forecast) → descarta backend → inventario centrado en la Record Page de `Visit_Job__c` + el wizard multi-paso + Quick Actions → materializa el set Cowork con el wizard descripto paso a paso → entrega el artefacto.

### Ejemplo 3 — Set HTML en Claude Code
**Usuario (en Code):** "Pásame el set en HTML, lo quiero en el repo."
**Claude:** hace descartes + inventario igual → genera los `.html` navegables siguiendo las reglas de fidelidad del reference → los escribe en el working dir/outputs.

### Ejemplo 4 — Opt-in Claude Design
**Usuario:** "Ármame los wireframes pero dame el prompt, lo quiero iterar en Claude Design."
**Claude:** hace descartes + inventario igual → ensambla el prompt (Paso 5) con la plantilla resuelta → entrega el prompt en un bloque copiable + las instrucciones de dónde pegarlo.
