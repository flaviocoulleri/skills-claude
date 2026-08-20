---
name: pc-meta-mermaid-diagram-builder
metadata:
  version: 1.5.0
  last_modified: 2026-08-06
description: >
  Genera diagramas técnicos como artefactos interactivos de Cowork usando exclusivamente
  mermaid (flowchart, sequence, ER, state, class, gantt, C4, mindmap, timeline, journey,
  architecture y más). Al pedir "un diagrama" o "un diagrama de X" muestra un selector para
  elegir el tipo —guiado por la metodología ProContacto o por desplegable—, arma el mermaid y
  lo publica en un shell HTML con desplazamiento, zoom, pantalla completa, minimapa, búsqueda de
  nodos, anotación (láser, dibujo y resaltador), exportar SVG/PNG y guía de uso. Activar con
  "hacé/armá un diagrama", "diagrama de flujo/proceso/secuencia/estados/ERD", "diagrama de
  arquitectura o integraciones", "quiero visualizar este proceso", "make a diagram",
  "flowchart/sequence/ER diagram". NO hace BPMN formal con pools y carriles (deriva a
  draw.io/bpmn-js), ni wireframes ni presentaciones. No requiere instalar nada: el render de
  mermaid es nativo del runtime de artefactos. Funciona en español e inglés.
---

# pc-meta-mermaid-diagram-builder — Diagramas técnicos en mermaid

## Propósito

Estandarizar la creación de diagramas técnicos de ProContacto sobre **un solo motor:
mermaid**. El usuario pide "un diagrama", el skill lo ayuda a elegir el tipo adecuado
(guiado por la metodología o por desplegable), arma el código mermaid y lo entrega como
**artefacto interactivo de Cowork** con una barra de controles rica.

Es una utilidad **transversal** (no atada a un sistema de negocio). Convive con otros
skills de visualización delegándoles lo que no le corresponde (ver Paso 0).

## Sobre mermaid: no se instala nada

- El **runtime de artefactos de Cowork renderiza mermaid nativamente** (`<pre class="mermaid">`
  en HTML, ` ```mermaid ` en markdown). Ni el usuario ni el skill instalan nada.
- El artefacto corre con **CSP estricta que bloquea todo host externo**: NO cargar mermaid
  (ni ninguna librería) desde un CDN. Se depende del render nativo del host. Es correcto y
  es la vía de cero dependencias.
- **Nunca** intentar `npm install`, bajar binarios ni tocar el sistema.

---

## Gate de continuidad — ¿este entregable ya venía trabajándose en otra conversación? (ADVISORY)

> Runbook completo en `_shared/session-continuity/gate.md`. Corre **una sola vez**, en cuanto sabés de qué entregable se trata y **antes de crear nada**. **Nunca bloquea.**

Cada conversación de Cowork arranca sin memoria de las anteriores. Si el usuario ya venía trabajando esto en otra, acá se re-pregunta todo y —peor— se puede terminar generar un segundo entregable que compite con el que ya existe. Cowork **no expone** las conversaciones del usuario, así que no intentes detectarlas ni linkearlas: lo que sí podés es leer la **huella del trabajo previo** y recomendarle volver.

1. Buscá actividad reciente del entregable (`Project__c` y sus `Project_Asset__c` activos), con `LastModifiedDate` y `LastModifiedBy`. Buscá `Project_Asset__c` activos del cliente/proyecto (`ProContactoArtifactId` —leé su `Description__c`, que dice de qué documento se trata—, `WireframeId`, `BlueprintId`, y `CoworkArtifactId` en registros viejos) y archivos tocados hoy en Drive.
2. **Dos señales fuertes** (modificado en las últimas 72 h · por el mismo usuario · backlog o assets tocados hoy · onboarding a medias) → mostrá el aviso. Actividad de más de 30 días no cuenta.
3. Mostrá **la evidencia concreta** (qué, cuándo, quién) y después la recomendación, siempre condicional: *"si venías trabajando este entregable en otra conversación, seguí ahí — vas a tener el contexto; acá arranco sin esa memoria"*. **Nunca inventes un link a la conversación.**
4. Ofrecé: **(a)** continuar acá levantando el contexto *(default)* · **(b)** frenar para ir a buscar la otra conversación — no escribas nada · **(c)** es otro alcance, crear igual.

**Salteá este paso** si el skill fue invocado encadenado desde otro skill en la misma conversación.

---

## Paso 0 — Desambiguación al inicio (Q04)

Este skill se parece a otros. Antes de arrancar, confirmar que el pedido es un **diagrama
técnico mermaid** y no:

- **Diagrama de actividad / proceso con carriles** (swimlanes tipo "Experience Cloud /
  Salesforce / Servicios externos") → **modo swimlane nativo** (ver Paso 4), no `subgraph` de mermaid.
- **BPMN 2.0 formal** (pools + gateways tipados XOR/AND/OR + eventos de mensaje/temporizador +
  message flows): ni mermaid ni el swimlane nativo lo cubren con fidelidad → **derivar a draw.io / bpmn-js**.
- **Wireframe / mockup de UI** → derivar a `pc-crm-salesforce-wireframe-builder`.
- **Presentación / deck** → derivar a `pc-sales-presentation-builder` o `pc-delivery-presentation-builder`.

Si hay duda, preguntar en una línea antes de seguir.

---

## Paso 1 — Mostrar el selector de tipo (Q05)

Renderizar el selector con `mcp__visualize__show_widget` usando el markup de
`assets/selector-widget.html` (no improvisar el markup). Ofrece las dos vías que el
usuario espera:

1. **Guiado por metodología** — tarjetas que mapean la intención (proceso AS-IS/TO-BE,
   modelo de datos, integración, arquitectura, estados, cronograma) a su tipo mermaid.
2. **Desplegable** — lista completa de tipos para quien ya sabe cuál quiere.

Cada opción dispara (`sendPrompt`) la continuación del flujo con el tipo ya elegido.
El selector incluye el guardarraíl de BPMN (deriva a draw.io/bpmn-js).

> Si del contexto ya se deduce el tipo y el contenido (p. ej. el usuario pegó un proceso
> y pidió "diagrama de flujo de esto"), se puede saltar el selector y proponer directamente
> el tipo, confirmando en una línea. Inferir antes de preguntar.

---

## Paso 2 — Capturar el contenido

Según el tipo, pedir lo mínimo necesario (o tomarlo de un transcript / brief / esquema
que el usuario haya pasado):

- **flowchart**: pasos, decisiones (con sus ramas etiquetadas), actores/lanes.
- **erDiagram**: entidades, atributos clave, cardinalidades.
- **sequenceDiagram**: participantes y orden de mensajes.
- **stateDiagram-v2**: estados y transiciones.
- **gantt / timeline**: tareas/hitos y fechas.
- resto: ver `references/diagram-types.md`.

Trabajar en **pasos cortos** (Q03), confirmando lo capturado antes de generar.

---

## Paso 3 — Generar el código mermaid

- Elegir la sintaxis del tipo elegido según `references/diagram-types.md`.
- **Español neutro** en las etiquetas (Q09), salvo dialecto pedido por el cliente.
- Saltos de línea en nodos: `<br/>` (y `&lt;br/&gt;` al embeberlo en el shell).
- Color por categoría con `classDef` (2-3 familias, no arcoíris).
- Ramas de decisión siempre etiquetadas.
- **Evitar cruces de flechas** en flowcharts/diagramas con carriles: usar el layout **ELK**
  (`--- config: layout: elk ---`) que minimiza cruces, más el orden de declaración y las
  reglas de `references/diagram-types.md` (sección "Reducir cruces de flechas").

---

## Paso 4 — Publicar el artefacto interactivo (Q01)

Tomar `assets/diagram-shell-template.html` (no improvisar el HTML) y reemplazar los tokens:

- `__MERMAID_SOURCE__` → el código mermaid del Paso 3 (con los `<br/>` escapados a `&lt;br/&gt;`).
- `__DIAGRAM_TITLE__` → título descriptivo del diagrama.

Publicar con la herramienta de artefactos (`.html`). El shell ya trae:

- Desplazamiento (arrastre, scroll/trackpad, espacio+arrastrar, flechas, inercia),
  zoom (botones, Cmd/Ctrl+rueda, teclas), Ajustar y Reset.
- Pantalla completa, minimapa, búsqueda de nodos, color de lienzo y de tinta.
- Anotación: puntero láser, dibujo y resaltador (efímeros o permanentes), deshacer, limpiar.
- Exportar SVG/PNG (con aplanado de `foreignObject`) y copiar el código mermaid.
- Tooltips en cada control y guía de uso paso a paso (botón `?`).
- **Escala temporal (solo Gantt)**: si el `MERMAID_SRC` es un `gantt`, el shell muestra
  un control extra que estira/comprime la línea de tiempo en el eje X (útil para leer
  cronogramas largos). En el resto de los tipos el control queda oculto.

**Default = artefacto de Cowork** (render nativo de mermaid, cero instalación, sin CDN).

### Gantt: modo NATIVO (no mermaid)

El Gantt de mermaid es limitado (texto que se deforma al escalar, poco control). Para
cronogramas el skill usa un **renderer SVG propio** en `assets/gantt-native-template.html`,
que NO usa mermaid: texto siempre nítido, dependencias, hitos, releases, filtros
(etapa/responsable/estado), drill-in colapsable, y **escala temporal por `px/día` que
re-renderiza** (nunca estira). En vez de código mermaid, este modo se alimenta con un
**modelo de datos JSON** (`PLAN`) que reemplaza el token `__PLAN_JSON__`; el esquema está en
`references/diagram-types.md` (sección "Modo Gantt nativo"). Exporta SVG/PNG sin `foreignObject`
(rasteriza limpio). El Gantt de mermaid queda solo como fallback rápido.

### Diagrama de actividad / swimlane: modo NATIVO (no mermaid)

Mermaid no dibuja **carriles como tabla** (columnas parejas con encabezado y bandas de
color); sus `subgraph` son cajas sueltas. Para procesos con carriles el skill usa otro
renderer SVG propio en `assets/swimlane-native-template.html`: columnas por carril con fila
de encabezado y banda de color, un nodo por fila, tipos (inicio/fin, tarea, gateway, fin de
error, "identidad validada"), conectores ortogonales y **loops por canal lateral** para no
cruzar cajas. Etiqueta del gateway **al costado** del rombo y líneas de texto **truncadas al
ancho de la caja** (nada de texto salido de las formas). Se alimenta con un JSON que
reemplaza `__SWIMLANE_JSON__` (esquema en `references/diagram-types.md`, sección "Modo
swimlane nativo"). Chrome DS + export SVG.

Cuándo usarlo vs otras salidas:
- **Proceso/actividad con carriles** (actores tipo "Experience Cloud / Salesforce / Servicios
  externos") → modo swimlane nativo.
- **Flowchart sin carriles** → mermaid (`flowchart`, con ELK si hay muchos cruces).
- **BPMN 2.0 formal** (pools + gateways tipados XOR/AND + message flows) → draw.io/bpmn-js.

### Design System, lienzo y codificación

- **Chrome con el Design System de ProContacto**: barra/paneles en superficie de marca
  (oscuro `#1F1F1F`, borde `rgba(255,255,255,.10)`), acento azul `#0062FF`, tipografía
  `Open Sans` con fallback del sistema. Nota: en el artefacto la CSP estricta **bloquea
  CDNs**, así que Open Sans y los íconos Lucide del DS no se cargan por red — se usa Open
  Sans si está en el sistema (si no, la fuente del sistema) y glyphs en la barra.
- **Lienzo del diagrama por default en gris** (`#E9EDF0`); el usuario puede cambiarlo a
  blanco, oscuro de marca o azul desde el grupo "Lienzo".
- **Charset UTF-8 (falla en Windows)**: el template arranca con `<meta charset="utf-8">`
  como primera línea y los exports declaran `encoding="UTF-8"`. Al escribir el `.html`
  (o la variante portable) **guardar siempre en UTF-8**; sin el meta o con otra
  codificación, en Windows los acentos/íconos se rompen (mojibake).

### Variante secundaria — HTML portable (opcional)

Solo si el usuario necesita un `.html` que abra en cualquier navegador **sin internet y
fuera de Cowork**: generar una variante **autocontenida** con `mermaid.min.js` embebido
en el propio archivo (no por CDN). Pesa ~1 MB; ofrecerla como opción explícita, nunca por
default. Esta variante DEBE llevar `<!DOCTYPE html><html><head><meta charset="utf-8">…`
y guardarse en UTF-8 (si no, falla en Windows).

---

## Paso 5 — Prueba de humo de interactividad (Q08)

Antes de dar por bueno el shell, renderizarlo, stubear `sendPrompt` y **clickear cada
control** confirmando efecto observable sin errores de consola. Los botones ya están
cableados a listeners locales / `sendPrompt` en el template (no en placeholders); los
tokens solo inyectan datos.

> Nota de entorno: el motor de mermaid lo inyecta el host de artefactos, así que la prueba
> de humo se hace en el visor de artefactos de Cowork, no abriendo el `.html` suelto.

---

## Reglas de diseño aplicadas

- **Q01** — HTML en `assets/diagram-shell-template.html` y selector en
  `assets/selector-widget.html`; no se improvisa markup por corrida.
- **Q02** — el shell y el selector se aprueban pantalla-por-pantalla con el gestor antes de
  publicar cambios al template.
- **Q04** — desambiguación al inicio (Paso 0).
- **Q05** — inputs seleccionables reales (selector con el catálogo de tipos).
- **Q06** — no se referencia por nombre ningún skill de BPMN inexistente; se deriva
  genéricamente a draw.io/bpmn-js.
- **Q07** — N/A: el skill no crea ni actualiza registros en sistemas externos.
- **Q08** — controles del shell cableados y probados (Paso 5).
- **Q09** — prosa y salida en español neutro.

## Estructura del skill

```
pc-meta-mermaid-diagram-builder/
├── SKILL.md                          ← este archivo (workflow)
├── assets/
│   ├── selector-widget.html          ← markup del selector (show_widget) — Q05
│   └── diagram-shell-template.html    ← shell interactivo con tokens __MERMAID_SOURCE__ / __DIAGRAM_TITLE__ — Q01/Q08
└── references/
    └── diagram-types.md               ← catálogo mermaid + mapeo por metodología + cuándo NO es mermaid
```

## Publicación en el gestor (regla dura)

**Todo entregable de este skill se publica en el gestor de artefactos de ProContacto — nunca como
artefacto de la conversación, y nunca solamente como archivo.** Lee
`_shared/artifact-publish/artifact-publish.md` y aplicá su procedimiento completo. Tres partes que no
son opcionales:

1. **Gate del conector, antes de construir.** Una llamada a `listar_artefactos` comprueba que el
   gestor responde. Si no está disponible, **el skill se detiene y le pide a la persona que lo
   active**: no construye "por las dudas", no deja el entregable en la conversación y no ofrece
   mandar el archivo en su lugar.
2. **Anti-duplicado de dos pasos.** `listar_artefactos` por título canónico
   `{Cliente} · {Entregable} · {Tipo}` (sin versión ni fecha) → `publicar_version` sobre la misma URL
   si ya existía, `publicar_artefacto` si no. Anotá el `id` y dejalo en el trace del HTML.
3. **El link va escrito en el chat.** Publicar sin mostrar el link es no publicar.

El diagrama deja de terminar como artefacto de la conversación: se publica en el gestor.

> **Restricción del motor.** El gestor **no inyecta mermaid** (eso lo hace el host de Cowork), así que un `<pre class="mermaid">` suelto no renderiza allá. Como el gestor **no tiene CSP** (verificado 4-ago-2026: es la razón por la que la tipografía carga por `<link>`), el shell publicado carga mermaid desde CDN con la versión pineada. Verificalo en el render antes de dar el diagrama por entregado: si el nodo no dibuja, no publiques.

**Exportar exige haber publicado.** Cualquier formato (`.docx`, `.xlsx`, `.pdf`, `.pptx`, texto) se
ofrece en el chat **después** de que el artefacto existe, y sale del mismo original. Que la persona
pida un formato no es permiso para saltear la publicación.
