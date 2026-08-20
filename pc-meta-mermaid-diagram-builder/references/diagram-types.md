# Catálogo de tipos de diagrama mermaid + mapeo a la metodología ProContacto

Fuente única de verdad de qué tipos soporta mermaid, para qué sirve cada uno y qué
tipo elegir según lo que el usuario quiere representar. El skill **no inventa** tipos:
usa esta tabla.

## Regla dura

Este skill es **mermaid-only**. Si el pedido es un **BPMN formal** (pools, carriles /
swimlanes, gateways tipados XOR/AND/OR, eventos con semántica, flujos de mensaje entre
pools), mermaid **no lo cubre con fidelidad** → no forzarlo. Avisar y derivar a
**draw.io / bpmn-js** (XML BPMN 2.0). Ver "Cuándo NO es mermaid" abajo.

## Mapeo por intención (guiado por metodología)

Cuando el usuario describe qué quiere representar, elegir el tipo así:

| El usuario quiere… | Tipo mermaid | Palabra clave |
|---|---|---|
| Proceso de negocio AS-IS / TO-BE, flujo con decisiones o aprobaciones | Flowchart | `flowchart` |
| Modelo de datos / objetos y relaciones (ej. objetos Salesforce) | Entidad-relación | `erDiagram` |
| Integración entre sistemas, orden de mensajes en el tiempo | Secuencia | `sequenceDiagram` |
| Arquitectura de componentes / servicios / integraciones | Arquitectura | `architecture-beta` (o `C4Context`) |
| Estados y transiciones de un registro (ej. Opportunity, Ticket) | Estados | `stateDiagram-v2` |
| Cronograma / plan (Sprint 0, fases del proyecto) | Gantt | `gantt` |
| Roadmap / línea de tiempo de hitos | Timeline | `timeline` |
| Estructura jerárquica / lluvia de ideas | Mapa mental | `mindmap` |
| Recorrido / experiencia del usuario por etapas | Journey | `journey` |
| Estructura de clases (UML) | Clases | `classDiagram` |

El **default recomendado** ante un pedido genérico de "un diagrama" es `flowchart`
(es el pedido más frecuente). Igual, siempre ofrecer el selector para confirmar.

## Catálogo completo (para el desplegable)

Estables: `flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`,
`erDiagram`, `journey`, `gantt`, `pie`, `quadrantChart`, `requirementDiagram`,
`gitGraph`, `mindmap`, `timeline`, `C4Context` (familia C4).

Beta / más nuevos: `sankey-beta`, `xychart-beta`, `block-beta`, `packet-beta`,
`kanban`, `architecture-beta`, `radar-beta`, `treemap-beta`, `zenuml`.

Los `-beta` pueden variar de sintaxis entre versiones de mermaid; si el runtime de
artefactos no los renderiza, caer a un tipo estable equivalente y avisar.

## Cuándo NO es mermaid (derivar, no forzar)

- **BPMN 2.0 formal** (pools, swimlanes, gateways tipados, eventos de mensaje/temporizador,
  message flows): mermaid solo aproxima con `flowchart` + `subgraph`, perdiendo la
  notación. Derivar a **draw.io / bpmn-js** (XML BPMN 2.0), que sí es interoperable con
  Camunda / Signavio / draw.io.
- **Wireframes / mockups de UI**: no es diagramación técnica → `pc-crm-salesforce-wireframe-builder`.
- **Presentaciones / decks**: → `pc-sales-presentation-builder` o `pc-delivery-presentation-builder`.

> Nota Q06: no referir por nombre a ningún skill de BPMN que no exista en el catálogo;
> derivar genéricamente a "draw.io / bpmn-js".

## Convenciones de estilo del mermaid generado

- Etiquetas en **español neutro** (Q09), salvo dialecto pedido por el cliente.
- Para saltos de línea en nodos usar `<br/>`. En el shell HTML (`<pre class="mermaid">`)
  escribir `&lt;br/&gt;` para que el runtime lo interprete como salto y no lo coma el parser.
- Colores por categoría vía `classDef` (no arcoíris): 2-3 familias, no 6+.
- Ramas de gateway/decisión siempre etiquetadas (Sí/No o los valores del negocio).

### Gantt: SIEMPRE con fechas

Un `gantt` **siempre** lleva eje de fechas — nunca un cronograma sin fechas:

- Declarar `dateFormat YYYY-MM-DD` y un `axisFormat` legible (ej. `%d/%m` o `%d %b`).
- Cada tarea tiene fecha de inicio real (o `after <id>`) **y** duración (`5d`) o fecha de fin.
- Si el usuario no da fechas concretas, pedirlas (fecha de arranque + duraciones) o proponer
  fechas tentativas y confirmarlas — pero el diagrama entregado debe mostrar fechas en el eje.
- Usar `section` para agrupar fases y `milestone` para los hitos (ej. Go-live).

## Modo Gantt NATIVO (no mermaid) — `assets/gantt-native-template.html`

Para cronogramas, el modo por default NO es mermaid sino un renderer SVG propio (texto
nítido, dependencias, hitos, releases, filtros, drill-in, escala por `px/día`). Se alimenta
con un JSON `PLAN` que reemplaza el token `__PLAN_JSON__`:

```jsonc
{
  "start": "2026-08-01",
  "stages":   [{ "id": "s0", "name": "Sprint 0" }, { "id": "cfg", "name": "Configuración" }],
  "tasks": [
    { "id": "t1", "stage": "s0", "owner": "PM", "name": "Kickoff", "start": "2026-08-01", "days": 3, "status": "done" },
    { "id": "t2", "stage": "s0", "owner": "Consultor", "name": "Relevamiento", "start": "2026-08-04", "days": 5,
      "status": "active", "deps": ["t1"] },
    { "id": "cfg1", "stage": "cfg", "owner": "Dev", "name": "Configuración", "start": "2026-08-18", "days": 18,
      "status": "pendiente", "deps": ["t2"], "release": "R1",
      "children": [
        { "id": "cfg1a", "stage": "cfg", "owner": "Dev", "name": "Modelo de datos", "start": "2026-08-18", "days": 6, "status": "pendiente" }
      ] }
  ],
  "milestones": [{ "id": "gl", "name": "Go-live", "date": "2026-09-12", "crit": true }],
  "releases":   [{ "id": "R1", "name": "R1", "date": "2026-09-12" }]
}
```

Reglas del modelo:
- `status`: `done` | `active` | `pendiente`. Los nodos con `children` **calculan** su estado
  y su rango (rollup); no se les pone `start`/`days`.
- Toda tarea hoja lleva `start` (YYYY-MM-DD) y `days` (duración) — SIEMPRE fechas.
- `deps` (array de ids) dibuja flechas de dependencia; `milestones`/`releases` son líneas verticales.
- `owner` alimenta el filtro de responsable. La escala temporal se cambia con el control
  (px/día) y re-renderiza nítido — no estira.

## Modo swimlane NATIVO (no mermaid) — `assets/swimlane-native-template.html`

Para diagramas de actividad con carriles (columnas-tabla con encabezado y bandas). Se alimenta
con un JSON `model` que reemplaza el token `__SWIMLANE_JSON__`:

```jsonc
{
  "lanes": [
    { "id": "ec",  "name": "Experience Cloud (Pantallas)",     "band": "rgba(63,81,181,0.08)", "fill": "#EAF1FB", "stroke": "#3f51b5", "tx": "#1a237e" },
    { "id": "sf",  "name": "Salesforce (Creación de objetos)", "band": "rgba(46,125,50,0.08)", "fill": "#E3F2E9", "stroke": "#2e7d32", "tx": "#1b5e20" },
    { "id": "ext", "name": "Servicios externos",               "band": "rgba(106,27,154,0.08)","fill": "#F3E5F5", "stroke": "#6a1b9a", "tx": "#4a148c" }
  ],
  "nodes": [
    { "id": "ini",  "lane": "ec", "row": 0, "type": "start", "text": "Inicio" },
    { "id": "p1",   "lane": "ec", "row": 1, "type": "task",  "text": "Pantalla:\nDatos iniciales" },
    { "id": "g1",   "lane": "sf", "row": 2, "type": "gw",    "text": "¿Empresa existe\ny RL asociado?" },
    { "id": "idOk", "lane": "sf", "row": 3, "type": "idok",  "text": "Identidad validada" },
    { "id": "ko",   "lane": "ec", "row": 4, "type": "endko", "text": "No se puede atender\ntu consulta" },
    { "id": "fin",  "lane": "sf", "row": 5, "type": "end",   "text": "Fin" }
  ],
  "edges": [
    { "from": "ini", "to": "p1" },
    { "from": "p1",  "to": "g1" },
    { "from": "g1",  "to": "idOk", "label": "Sí" },
    { "from": "g1",  "to": "ko",   "label": "No" },
    { "from": "idOk","to": "fin" }
  ]
}
```

Reglas del modelo:
- `lanes`: columnas de izquierda a derecha; `band`/`fill`/`stroke`/`tx` son los colores del carril
  (usar la paleta del DS por dominio: pantallas azul, Salesforce verde, externos violeta).
- `nodes[].type`: `start` | `end` | `endko` (fin de error, círculo rojo) | `task` | `gw` (gateway
  rombo, etiqueta al costado) | `idok` (píldora azul, ej. "Identidad validada").
- `nodes[].row`: entero; **un nodo por fila** (top→down). Dos nodos pueden compartir fila si están
  en carriles distintos (ej. las dos ramas de un gateway).
- Texto: `\n` separa líneas; el renderer trunca al ancho de la caja (nunca se sale de la forma).
- `edges[].label` (Sí/No/…) y `dashed` (retornos async). Adyacentes van directos; los loops hacia
  atrás se rutean por un canal lateral para no cruzar cajas.

Layout: para minimizar líneas largas, agrupá filas contiguas del mismo actor cuando el flujo lo permita.

## Reducir cruces de flechas (flowcharts / carriles)

Los diagramas con carriles y muchos saltos entre carriles cruzan flechas por el auto-layout
(dagre). Para minimizarlo:

1. **Usar el layout ELK** (Eclipse Layout Kernel), que minimiza cruces mucho mejor que dagre:
   ```
   ---
   config:
     layout: elk
   ---
   flowchart TB
     ...
   ```
   Nota: si el runtime del artefacto no tiene ELK registrado, mermaid cae a dagre en silencio
   (no rompe, pero no mejora); verificar en el render.
2. **Orden de declaración**: dagre/ELK respetan el orden — declarar nodos y aristas en el
   orden del flujo real reduce cruces.
3. **Minimizar saltos entre carriles**: agrupar en un carril los pasos consecutivos del mismo
   actor; cada ida y vuelta entre carriles es un cruce potencial.
4. **Dirección consistente** (`TB` o `LR`, no mezclar) y evitar back-edges innecesarios
   (los loops de reintento van etiquetados y, si se puede, por un solo lado).
5. Si aun así cruza y el diagrama es un **proceso con carriles/pools tipo BPMN**, es señal de
   que mermaid no es la herramienta: derivar a draw.io/bpmn-js.
