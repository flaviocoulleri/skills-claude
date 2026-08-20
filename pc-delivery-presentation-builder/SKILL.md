---
name: pc-delivery-presentation-builder
metadata:
  version: 2.2.0
  last_modified: 2026-08-07
description: >
  Crea la presentación de DELIVERY de ProContacto **acá mismo**, como artefacto HTML navegable, y
  desde el chat la exporta a PDF, PowerPoint o imágenes — usa este skill aunque pidan "PowerPoint"
  o ".pptx": el .pptx sale exportado del mismo deck (no invoques la skill pptx/docx). Cubre kickoff,
  sprint review, steering, status, mid-project, cierre y retro. Parte de una base
  curada en Drive, captura el contexto del proyecto y barre conectores (Jira/Confluence/Slack/
  Calendar/ReadAI); sin placeholders. Delivery NO cotiza (sin slide de inversión). El entregable se
  sube a Drive y queda enganchado como issue Artifact del proyecto Jira. ACTIVAR con "quiero armar
  el kickoff", "presentación del proyecto", "presentación de status/weekly status", "steering",
  "carta de aceptación", "cierre de proyecto", "sprint review", "retro"; EN: "kickoff deck",
  "steering deck", "status deck". Si el pedido es comercial (propuesta, cotización, POC, first
  call), deriva al comercial. Proactivo con transcript de reunión. ES/EN.
---

# pc-delivery-presentation-builder

## Para qué existe este skill

Es el skill de la familia `presentation-builder` para las presentaciones **de delivery**: las que un PM/SM/DM arma sobre un proyecto activo (kickoff, steering, status, cierre, retros). **Construye el deck acá mismo** como artefacto HTML navegable siguiendo `_shared/deck-engine/deck-engine.md`, y desde el chat lo exporta a PDF, PowerPoint o imágenes. Ya no termina en un encargo para otra herramienta: termina en la presentación hecha (ver `_shared/references/common-rules.md` → "Salida del skill").

El valor: punto único para las presentaciones de proyecto, con **bases curadas en Drive** (mantenidas por PMO/Heads de Delivery), contexto real del proyecto tomado de Salesforce y conectores, y un prompt que nunca sale con huecos.

## Reglas comunes de la familia

**Antes de operar, lee `_shared/references/common-rules.md` — sus reglas aplican íntegras** (salida = artefacto HTML, secuencia canónica, consistencia visual con Patrones A–E, barrido sin picker, gate anti-placeholder, deck-craft, nomenclatura y trazabilidad, Drive y vinculación). Este archivo sólo documenta lo específico de delivery.

**Para construir el deck, lee `_shared/deck-engine/deck-engine.md`** (escenario fijo, kit de marca, verificación) y `_shared/deck-engine/export-formats.md` (formatos y cómo se generan).

**Antes del primer widget, lee `_shared/references/ui-patterns.md`** y llama a `mcp__visualize__read_me` (silencioso). Toda elección/input va por `mcp__visualize__show_widget`.

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

### Paso 0 — Red de seguridad de área

Este skill asume delivery. **Si el pedido es claramente comercial** (propuesta a cliente, cotización, orden de magnitud, POC de venta, first call deck), no sigas: deriva —transición invisible— a `pc-sales-presentation-builder` y avisa al usuario en lenguaje natural ("esto es una propuesta comercial, la armamos por el otro lado"). Si hay ambigüedad real, muestra el widget de área (Patrón A) y confirma antes de seguir. Con delivery confirmado, continúa.

### Paso 1B — Elegir base de delivery

1. **Lista las bases de delivery** combinando índice cacheado + Drive en runtime. Carpeta:
   - **ID:** `1Tdy-IVpVhDmMECODq_bhZBdIfS5wqu_F`
   - **URL:** https://drive.google.com/drive/folders/1Tdy-IVpVhDmMECODq_bhZBdIfS5wqu_F

   Sigue `references/base-index.md`: lee el índice primero, reconcilia contra Drive (`search_files` recursivo, todos los no-trashed). Si divergen, gana Drive y reescribes el índice.
2. **Muéstralas con el Patrón C** (selector de archivo de Drive): icono por tipo, nombre, meta (tipo · última modificación), botón "Ver en Drive" (`webViewLink`) y "Usar como base".
3. Si el usuario prefiere no partir de una base (o no hay ninguna que aplique al hito), sigue igual — el prompt se arma desde el contexto del proyecto y el arco de delivery de `_shared/references/deck-craft.md`.

### Paso 1B.2 — Capturar el contexto del proyecto

Renderiza el form con `assets/widgets/paso1b-proyecto.html` (Patrón B). **Autocompleta desde Salesforce** si tienes `Project__c` o la Account asociada (incluyendo `Account.Website`); el `PM/SM` default es el usuario actual.

| Campo | Requerido | Notas |
|---|---|---|
| Proyecto | sí | idealmente el `Name` del `Project__c` |
| Cliente | sí | Account asociada |
| Audiencia del deck | sí | sponsor del cliente, equipo, comité interno, retro |
| Hito del proyecto | sí | Kickoff / Sprint review / Steering / Status / Mid-project / Cierre-Aceptación / Retro / Otro |
| PM/SM responsable | no (default usuario) | |
| Período cubierto | no | útil para status/steering |
| Web del cliente | no — recomendado | dispara el fetch (Paso 2.5) |
| Idioma del deck | sí (default ES) | |

### Paso 2.5 — Fetch del sitio del cliente (si se proporcionó la web)

Si el form trae web (o viene de `Account.Website`), corre el fetch automático: home + hasta 3 páginas clave (`/about`|`/nosotros`, `/servicios`|`/productos`, `/clientes`|`/casos`) con `WebFetch` (escala a Claude in Chrome sólo la home si viene client-rendered). Extrae lenguaje propio del cliente, a quién le vende, qué vende, casos y tono — **sólo lo textual, no inventes**. Resume 5-8 señales en un widget (Patrón D abreviado) y deja que el usuario deseleccione. Máx 4 páginas; si falla todo, avisa en una línea y sigue.

### Paso 3 — Enriquecer con conectores (opcional, recomendado)

Pregunta con Patrón A ("Sí, barre todo" / "No, seguimos"). **Sin picker** — usa todo lo conectado. En delivery la **fuente primaria es Jira/Confluence** del proyecto: issues cerrados en el período, blockers abiertos, hitos/epics cumplidos, riesgos próximos; más el canal de Slack del proyecto y transcripts recientes (ReadAI/Calendar). Ver `_shared/references/connector-sweep.md`. Resume en un widget con checkboxes (Patrón D) y deja que el usuario marque qué sumar; cita la fuente de cada señal.

### Paso 4 — (no aplica personalización por industria)

En delivery el lenguaje lo aportan la base elegida + el hito + las señales del proyecto. No hay banco de industrias ni pricing.

### Paso 4.7 — Chequeo de completitud (gate bloqueante)

Corre el gate anti-placeholder de `_shared/references/common-rules.md`. Requeridos en delivery: Proyecto, Cliente, Audiencia, Hito, Idioma. Opcionales (preguntar incluir/omitir): Período cubierto, PM/SM específico, señales de conectores. Nada de `[A completar]`.

### Paso 4.8 — Confirmar la carpeta de Drive (antes de construir)

Corré el gate de `_shared/drive-upload/drive-upload.md` con el widget `subir-a-drive.html`
(`{{AREA_LABEL}}` = "Delivery"), **una sola vez y antes de armar el deck**. Ruta de
`references/drive-structure.md`:

**`J - Delivery / B - Proyectos / {Cliente} / {Proyecto}`** — sin nivel de país.

Nunca uses la carpeta de bases de delivery como destino. Confirmarla acá y no al final es lo que
permite que **cada corrección suba sola**, sin interrumpir al PM en cada iteración.

### Paso 5 — Construir el deck y subirlo

Seguí `_shared/deck-engine/deck-engine.md`, con el **arco narrativo de delivery** de
`_shared/references/deck-craft.md`: dónde estamos → qué logramos con evidencia → qué cambió o
aprendimos → qué viene → el pedido o cierre. Divisores de sección, ilustraciones materializadas,
cero placeholders.

Adaptaciones de delivery:

- "Tipo de presentación" → **hito del proyecto**.
- "Cliente" → **cliente del proyecto + sponsor/audiencia**.
- **"Inversión" se omite entera** — delivery no cotiza.
- "Señales relevantes" → issues cerrados, blockers, hitos cumplidos, riesgos.
- Si se partió de una base, la estructura se deriva de la base extraída (sólo contenido), personalizada al proyecto.

**Antes de publicar, corré la verificación del motor** (§6 de `deck-engine.md`). Publicado el
artefacto, **subí el HTML liviano** a la carpeta del Paso 4.8 y presentá el deck **junto con su link
de Drive**.

### Paso 6 — Ofrecer corregir o descargar

Mostrá `_shared/assets/exportar-deck.html` (`show_widget`). El primer botón es **ajustar**. Si el PM
pide cambios: corregí, subí la versión, **volvé a subir el HTML a Drive avisando con el link** y
mostrá el widget de nuevo. La carpeta ya está confirmada — no se vuelve a preguntar.

### Paso 7 — Generar el formato elegido

Generá el archivo con `_shared/deck-engine/scripts/export-deck.mjs` y **entregalo en el chat**. A
Drive no sube: el original ya está ahí desde el Paso 5. Verificá que la cantidad de páginas o
imágenes coincida con la de slides.

### Paso 8 — Enganchar al proyecto Jira

Corré el gate de `_shared/artifact-linkage/artifact-linkage.md`: el **link de Drive** queda como
issue **`Artifact`** (workflow "Deliverable") del proyecto Jira, del tipo que corresponda al
entregable según el metadata del proyecto —que varía por proyecto: leelo, no lo asumas—. El proyecto
se busca primero en el `Project_Asset__c` del `Project__c` y, si no está, en Jira por nombre. **Un
proyecto Jira no se crea** para guardar un entregable: eso es decisión de PMO.

## Estructura del skill

```
pc-delivery-presentation-builder/
├── SKILL.md                          ← este archivo (flujo específico de delivery)
├── references/
│   ├── base-index.md                 ← caché de bases de delivery (Drive = fuente de verdad)
│   └── drive-structure.md            ← ruta destino J-Delivery/B-Proyectos
├── assets/widgets/
│   └── paso1b-proyecto.html          ← form de contexto de proyecto (Patrón B)
├── _shared/                          ← AUTO-COPIADO de _shared/presentation-builder/ (no editar acá)
│   ├── references/{common-rules, ui-patterns, deck-craft, connector-sweep}.md
│   ├── deck-engine/                  ← motor del artefacto (shell, fuente, exportador)
│   ├── drive-upload/                 ← gate de subida a Drive
│   ├── artifact-linkage/             ← gate de vinculación
│   └── assets/{exportar-deck.html, prompt-skeleton.md, drive-folder-path.html, slides/}
└── evals/evals.json
```

> El contenido de `_shared/` se edita en `_shared/presentation-builder/` (raíz del repo) y se propaga con `sync.sh`. No lo edites acá.

## Integración con la cadena de delivery

- `pc-delivery-sf-project-builder` / `pc-delivery-project-pulse` — fuentes de estado del proyecto; este skill lee `Project__c` y conectores pero no escribe.
- `pc-sales-presentation-builder` — a donde deriva si el pedido resulta ser comercial.
- `pc-meta-presentation-builder` — el router que puede haber derivado hacia acá.

## Publicación en el gestor (antes de vincular)

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

**Recién después** corre el gate de vinculación: lo que se registra es la URL del gestor.

## Gate de vinculación del entregable (cierre)

Ver `_shared/artifact-linkage/artifact-linkage.md`. Destino de delivery: issue **`Artifact`** en el proyecto Jira (workflow "Deliverable", NO `Artefacto`). Verificá el issuetype real con el metadata, buscá duplicado por summary, y creálo con **el link de Drive** del entregable, **sólo con OK**. Se registra el archivo de Drive, no el artefacto de la conversación. Si corres dentro del flujo de `pc-delivery-deliverable-orchestrator`, podés devolverle el control para el registro.

## Changelog

- **2.2.0 (2026-08-07)** — **Todo entregable termina en el gestor.** Se publica en el gestor de artefactos de ProContacto y **no** como artefacto de la conversación, y publicar es siempre de dos pasos: `listar_artefactos` por título canónico y `publicar_version` sobre la misma URL si ya existía, `publicar_artefacto` sólo si no. Sin esa búsqueda previa, una conversación nueva republica de cero y el link que el cliente ya tiene queda viejo sin que nadie se entere. El título canónico va sin versión ni fecha, el `gestor-id` queda en el trace del HTML para que lo encuentre la conversación siguiente, y el gate de vinculación registra la URL del gestor. Ver `_shared/artifact-publish/artifact-publish.md`.
- **2.0.0 (2026-08-03)** — **El deck se construye acá.** Deja de terminar en un prompt para Claude Design —que ProContacto está discontinuando— y pasa a **materializar la presentación como artefacto HTML** con el motor compartido `_shared/deck-engine/`. Secuencia: confirmar la carpeta de Drive → crear el artefacto y subir el HTML → ofrecer corregir o descargar → generar el formato → enganchar el link como issue `Artifact` del proyecto Jira. Cambios concretos: (1) el Paso 4.8 pasa a **confirmar la carpeta antes de construir**, para que cada corrección suba sola; (2) los Pasos 5-8 reemplazan al ensamble y entrega del prompt; (3) la exportación se ofrece **en el chat** con `exportar-deck.html`, nunca dentro del artefacto — el contenedor bloquea descargas y no expone `sendPrompt`; (4) a Drive va **sólo el HTML liviano**, el original re-editable, y los formatos exportados se entregan en el chat; (5) el gate de vinculación registra el **link de Drive** y busca el proyecto Jira en vez de dejar pendiente; (6) el prompt para Claude Design sobrevive como **última opción del widget, marcada "En retiro"**. Sin cambios en el arco de delivery, las bases de Drive ni el barrido de conectores.
- **1.1.0 (2026-07-24)** — **Calidad del deck** (núcleo compartido `_shared/presentation-builder/`): **divisores de sección obligatorios** entre bloques del arco; **ilustraciones materializadas en slides clave** (portada, divisores, cierre) con **prohibición explícita de placeholders de imagen**. Las palancas de precio (ancla/descuento, calendario de pagos) son comerciales — no aplican a delivery.
- **1.0.0 (2026-07-06)** — Nace del split de `pc-sales-presentation-builder`: se separa la mitad de delivery en su propio skill (plugin `procontacto-delivery`) para que los PMs no dependan del plugin comercial. Núcleo común canónico en `_shared/presentation-builder/` propagado vía `sync.sh`. Sin pricing ni industria; arco narrativo de delivery; fuente primaria de conectores = Jira/Confluence.

<!-- owner: ariel.tarsitano -->
---
