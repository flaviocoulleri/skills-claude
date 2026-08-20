# SLDS Component Blueprints — clases, estructura y densidad de los componentes Lightning

Capa **estructural** del design system: nombres de clase SLDS reales, anatomía de cada componente y las medidas densas características de Salesforce. Complementa `slds-design-tokens.md` (que define color, tipografía y spacing). Si los tokens dicen *qué color/tamaño*, esto dice *qué clase y qué estructura*.

> **Convención de nombres SLDS (respétala siempre):**
> - Prefijo de toda clase: **`slds-`**.
> - **Modificadores** con guion bajo: `slds-table_bordered`, `slds-table_fixed-layout`, `slds-form-element_stacked`.
> - **Estados** con `slds-is-`: `slds-is-selected`, `slds-is-sorted_asc`, `slds-is-edited`, `slds-is-resizable`.
> - Sub-partes con doble guion bajo BEM: `slds-card__header`, `slds-page-header__title`, `slds-cell-edit__button`.

> **Densidad (el "look" de Salesforce):** las medidas en px salen de los estilos computados (base 16px = 1rem). Las tablas son **densas e intencionalmente compactas**: header 32px alto / `font-size:13px` / `font-weight:700` / color `#444444`; celdas de body `padding:4px 8px`, alto ~30.75px, `font-size:13px`, color `#181818`, `line-height:19.5px`. No "esponjes" las tablas con padding grande: el aspecto compacto es parte de la fidelidad.

---

## Componentes de registro y listas

### Data Table (base de List Views)
Tabla de registros con columnas ordenables, seleccionables y editables.
- **Root:** `<table class="slds-table slds-table_bordered slds-table_fixed-layout slds-table_resizable-cols">`
- **Variantes:** bordered `slds-table_bordered` · striped `slds-table_striped` · column dividers `slds-table_col-bordered` · sin hover `slds-no-row-hover` · fixed layout `slds-table_fixed-layout` · resizable `slds-table_resizable-cols` · cell buffer `slds-table_cell-buffer`.
- **Header cell** `<th>`: clases `slds-is-resizable slds-is-sortable slds-cell_action-mode`, wrapper de acción `slds-th__action`; alto 32px, `font-size:13px`, `font-weight:700`, color `#444444`, padding 0.
- **Body row** `<tr class="slds-hint-parent">`; seleccionada → `slds-is-selected`.
- **Body cell** `<td class="slds-cell_action-mode">`: padding `4px 8px`, alto ~30.75px, `font-size:13px`, color `#181818`, `line-height:19.5px`.
- **Ordenamiento:** `slds-is-sortable` / `slds-is-sorted` / `slds-is-sorted_asc` / `slds-is-sorted_desc`.
- **Selección:** checkbox de fila `slds-checkbox slds-checkbox_faux slds-checkbox__label`; "seleccionar todo" en el header; fila seleccionada `slds-is-selected`; celda de número de fila `slds-row-number`.
- **Inline edit:** celda editable `slds-cell-edit`, botón `slds-cell-edit__button`, editada `slds-is-edited`, error `slds-cell-error`, popover `slds-popover slds-popover_edit`.
- **Utilidades de celda:** truncado `slds-truncate`, wrap `slds-cell-wrap`, line clamp `slds-line-clamp`, alinear der. `slds-text-align_right`, texto débil `slds-text-color_weak`, ícono `slds-icon_container`.

### Page Header (List View / Record Home)
Encabezado con título, contador de registros y acciones.
- **Root:** `slds-page-header`; fondo `#f3f3f3`, padding 16px, border-radius 4px, box-shadow `0 2px 2px 0 rgba(0,0,0,0.1)`.
- **Título:** `slds-page-header__title slds-truncate`.
- **Sub-partes:** name `slds-page-header__name` · name-title `slds-page-header__name-title` · meta `slds-page-header__meta-text` · controles `slds-page-header__controls` · fila `slds-page-header__row` · col de acciones `slds-page-header__col-actions` · detail row `slds-page-header__detail-row`.
- **Variantes:** `object-home` · `record-home` · `related-list` · `object-home-with-filters`.

### Card (secciones dentro de un registro, related lists)
- **Root:** `slds-card`; fondo `#ffffff`, borde `1px solid #c9c9c9`, border-radius 4px.
- **Sub-partes:** header `slds-card__header` · título `slds-card__header-title` · body `slds-card__body` · body inner `slds-card__body_inner` · footer `slds-card__footer`.

### Tile (registro compacto en listas tipo tarjeta / kanban)
- **Root:** `slds-tile slds-media`; `font-size:13px`.
- **Sub-partes:** título `slds-tile__title slds-truncate` · detalle `slds-tile__detail` · media body `slds-media__body`.
- **Variantes:** board (kanban) · with-icon · with-checkbox.

### Description List (campos clave-valor en el detalle)
- **Root:** `<dl>`.
- **Variantes:** horizontal `slds-list_horizontal` · stacked `slds-form-element_stacked` · grid vertical `slds-form-element_horizontal`.
- **Term (label):** `slds-item_label slds-text-color_weak`. **Definition (valor):** `slds-item_detail slds-truncate`.

### Related List
Lista relacionada dentro de un registro: normalmente **Card + Data Table** (o Tiles).
- **Patrón:** `slds-card > slds-card__header (título + count + acciones) > slds-card__body > slds-table | slds-tile-list`.

---

## Patrones de layout de registro

- **Record Home:** `slds-page-header` (variante `record-home`) + `slds-grid` de columnas → panel principal (`slds-col`) con `slds-tabs` / `slds-card`, y panel lateral (`slds-col`) con highlights y related lists.
- **List View:** `slds-page-header` (variante `object-home` con dropdown de vista, search, filtros y botones) + `slds-table` dentro de un contenedor con scroll.
- **Split View:** `slds-split-view` → lista a la izquierda (`slds-split-view__list`) + detalle a la derecha.

---

## Chrome, navegación y procesos (global header, view switcher, filtros, Path, aprobaciones, mobile)

### Global Header (barra superior)
- Fondo **blanco** `#ffffff` con borde inferior `#dddbda`. **Nunca navy/azul oscuro.**
- Izquierda: App Launcher (waffle) + **logo nube de Salesforce** (default) + nombre de la app. Centro: search global. Derecha: favoritos, ayuda, notificaciones (campana con badge), setup, avatar.
- Debajo, la nav bar de objetos con la tab activa subrayada en azul `#1b96ff`.

### List View — View Switcher (dropdown, NO tabs)
- Nombre de la vista en grande + caret. Al abrir: panel con buscador "Search lists…", grupo **"Recent List Views"** (✓ en la activa, ícono de pin para la fijada) y grupo **"All Other Lists"**.
- Meta bajo el nombre: "N items • Updated a minute ago".

### List View — Icon Bar
Orden estándar (derecha de la page-header): engranaje (List View Controls) · display selector (Tabla/Kanban/Split) · refresh · sort · editar (lápiz) · charts · embudo de filtros (abre el panel Filters).

### List View — Panel Filters
Panel a la derecha titulado "Filters" con botón cerrar (✕). Contenido: "Filter by Owner" (All/My), encabezado "Matching all of these filters", cada filtro como **card** con campo + operador + valor y un **ícono de tacho**; links "Add Filter", "Remove All" y "Add Filter Logic".

### Lightning Path + Guidance for Success
- Chevrons horizontales: completadas verde `#2e844a` con ✓, actual azul `#0176d3`, pendientes gris `#ecebea` texto `#706e6b`.
- Botón **"Marcar etapa como actual/completada" alineado a la derecha, EN LÍNEA con los chevrons** (misma fila), no debajo.
- Debajo del path: bloque **"Guía para el éxito"** en dos columnas — **IZQUIERDA: Campos clave** (label+valor, máx 5); **DERECHA: texto descriptivo** de la etapa.

### Tabs del registro (ubicación)
Tabs principales en el panel izquierdo: **Detalles, Actividad, Chatter** (+ custom). La tab **"Relacionado" va en el panel DERECHO** y agrupa TODAS las related lists del objeto, **incluido el "Historial de cambios" como una related list más** (no card suelta). Cada sección de Detalles abre con banda de encabezado gris `#f3f2f2` de ancho completo + borde `#dddbda`.

### Aprobaciones (sólo si hay HUs de aprobación)
- **Badge** "Pendiente de aprobación" junto al nombre del registro (pill warning `#dd7a01` / bg `#fff1ea`).
- **Banner de solo-lectura** (cuando bloqueado): franja superior amarilla con ícono, "Pendiente de aprobación de [proceso] · Enviado a [persona] el [fecha] · Este registro es de solo lectura", botón "Ver historial de aprobación", acciones principales en gris/disabled, badge "Solo lectura" con candado.
- **Pantalla de Solicitud de Aprobación:** **header con compact layout** (ícono + "Solicitud de Aprobación" + nombre del registro + badge PENDIENTE + datos Solicitante/Fecha/Aprobador actual/Asignado a/Estado/Proceso) con botones **Aprobar** (`#0176d3`) y **Rechazar** (`#ea001e`) **solo en el header, arriba a la derecha**. Columna izquierda (principal): detalle del registro (Approval Details). Columna derecha: Comentarios + Historial. Sin botones de acción dentro del bloque de Comentarios.
- **Notificación:** ítem en la campana "El usuario [X] ha solicitado la aprobación del siguiente registro: [nombre]" → linkea a la pantalla anterior.

### Home Lightning (layout)
Dos columnas: **izquierda ancha = dashboard con 2-3 charts/reportes** (título + gráfico + "Ver reporte" + "As of Today at HH:MM"); **derecha angosta = Actividades** (composer Nueva tarea/Llamada/Evento/Email + Tareas pendientes + Próximos eventos). Sin accesos rápidos de alta ni lista de registros al pie.

### Tab Actividad (composers)
Sub-tabs **Nueva tarea / Registrar llamada / Nuevo evento / Correo**. **Al seleccionar CUALQUIERA se muestra SU propio composer** (no solo Nueva tarea); ninguna queda vacía/muerta. Debajo, timeline de actividad.

### Estado de error de validación (New/Edit)
- Campo inválido: borde rojo `#ea001e`, **ícono ⊘ (prohibido)** en el campo, **mensaje en rojo debajo** ("Debe completar este campo para continuar" — en español).
- Asterisco rojo en requeridos.
- Error de página = **popover anclado al botón Guardar**: encabezado rojo "Encontramos un problema" + ✕, "Revise los siguientes campos" con campos en error como **links**. Ícono ⊘ rojo al lado de Guardar.
- Mostrar SIEMPRE al menos un campo en este estado, textos en español.

### Lead Convert (una pantalla)
Tres columnas (Cuenta / Contacto / Oportunidad), cada una con toggle **Crear nuevo / Vincular existente** en la misma vista. No dos pantallas separadas.

### Web-to-Lead (form público)
**Sin chrome SLDS** — estilo web neutro/genérico. Campos según HUs + botón Enviar + estado de confirmación post-envío.

### Salesforce Maps (chrome propio, sin mobile)
Header azul "Salesforce Maps" + tabs **Layers · Routes · Schedule · List** + toolbar de íconos + search. Todo en español.
- **Layers:** mapa + panel de capas (Recientes/Guardadas/En el mapa). Markers = registros (con color), boundaries/polígonos por país/región. Card de capa "Registros: N", geocodificados, markers visibles.
- **Routes:** Nombre de ruta, botón **Optimizar**, toggle "Bloquear orden de paradas", **paradas numeradas** (dirección + tiempo/distancia), footer "1 h 4 min con tráfico · 30.6 km · 43 paradas · Agregar parada"; ruta dibujada en el mapa.
- **Schedule:** calendario por día con franjas horarias + panel "Sin programar" (markers + empty state), drag&drop al calendario, selector fecha/Hoy.
- **List:** lista de los registros del mapa.

### Planificador avanzado de visitas (wizard, chrome propio, sin mobile)
Wizard con stepper de círculos + Anterior / Guardar y siguiente. Todo en español. Pasos:
- **Segmentación:** Mapeo de campo de usuario asignado + tabla "Filtros de campo" (Campo/Operador/Valor) con "Agregar fila" y "Agregar lógica de filtros".
- **Ventanas de visita:** tabla por día (Dom→Sáb), "Agregar ventana de visita" (1/2), "Aplicar a todos los días"; frecuencia diaria/semanal/mensual/cuatrimestral + días + franja horaria.
- **Asignar usuarios:** tabla Usuarios (Nombre/Perfil/Rol/Manager) con checkboxes + buscador + "N usuarios asignados".
- **Configuración del plan:** fecha inicio/fin, "Reiniciar el plan al finalizar", cantidad de datos de ruta tras optimización.
- **Optimización:** "Programar lotes de optimización" — frecuencia (cada N semanas), hora, días de la semana (checkboxes).

> **Maps y Planificador: condicionales (solo si las HUs los piden), chrome propio (NO Lightning estándar) y SIN versión mobile.**


### Mobile shell (Salesforce Mobile App) — SIEMPRE en sección separada
- **Header blanco** con "‹ Atrás"/título a la izquierda + íconos (compartir, estrella, buscar, campana) en azul. Sin status-bar falsa.
- **Bottom tab bar fija** de 5 ítems, activa en azul.
- **Record:** tarjeta ícono+tipo+nombre, campos clave-valor, acciones rápidas como **botones circulares** arriba, secciones colapsables "Relacionado"/"Detalles" con chevron ›, **Path compacto horizontal** + "Estado: X" + botón "Marcar Estado como completado(a)", "Seguir", "Actividad reciente".
- **List View:** buscador, grupos Listas/recientes, vista con caret, **Filtrar/Ordenar como botones circulares**, registros en **tarjetas apiladas clave-valor**.
- **Eventos:** calendario mensual con el día actual resaltado.



```json
{
  "recordAndListComponents": {
    "dataTable": {
      "rootElement": "table",
      "rootClasses": ["slds-table", "slds-table_bordered", "slds-table_fixed-layout", "slds-table_resizable-cols"],
      "variants": { "bordered": "slds-table_bordered", "stripedRows": "slds-table_striped", "columnDividers": "slds-table_col-bordered", "noRowHover": "slds-no-row-hover", "fixedLayout": "slds-table_fixed-layout", "resizableCols": "slds-table_resizable-cols", "cellBuffer": "slds-table_cell-buffer" },
      "headerCell": { "element": "th", "classes": ["slds-is-resizable", "slds-is-sortable", "slds-cell_action-mode"], "actionWrapper": "slds-th__action", "height": "32px", "fontSize": "13px", "fontWeight": "700", "color": "#444444", "padding": "0" },
      "bodyRow": { "element": "tr", "classes": ["slds-hint-parent"], "selectedClass": "slds-is-selected" },
      "bodyCell": { "element": "td", "classes": ["slds-cell_action-mode"], "padding": "4px 8px", "height": "30.75px", "fontSize": "13px", "color": "#181818", "lineHeight": "19.5px" },
      "sortingClasses": { "sortable": "slds-is-sortable", "sorted": "slds-is-sorted", "ascending": "slds-is-sorted_asc", "descending": "slds-is-sorted_desc" },
      "selection": { "rowCheckbox": ["slds-checkbox", "slds-checkbox_faux", "slds-checkbox__label"], "selectAllInHeader": true, "selectedRow": "slds-is-selected", "rowNumberCell": "slds-row-number" },
      "inlineEdit": { "editableCell": "slds-cell-edit", "editButton": "slds-cell-edit__button", "editedCell": "slds-is-edited", "errorCell": "slds-cell-error", "editPopover": ["slds-popover", "slds-popover_edit"] },
      "utilityCellClasses": { "truncate": "slds-truncate", "wrap": "slds-cell-wrap", "lineClamp": "slds-line-clamp", "alignRight": "slds-text-align_right", "weakText": "slds-text-color_weak", "iconContainer": "slds-icon_container" }
    },
    "pageHeader": {
      "rootClasses": ["slds-page-header"], "background": "#f3f3f3", "padding": "16px", "borderRadius": "4px", "boxShadow": "0 2px 2px 0 rgba(0,0,0,0.1)",
      "titleClasses": ["slds-page-header__title", "slds-truncate"],
      "subParts": { "title": "slds-page-header__title", "name": "slds-page-header__name", "nameTitle": "slds-page-header__name-title", "meta": "slds-page-header__meta-text", "controls": "slds-page-header__controls", "row": "slds-page-header__row", "col": "slds-page-header__col-actions", "detailRow": "slds-page-header__detail-row" },
      "variants": ["object-home", "record-home", "related-list", "object-home-with-filters"]
    },
    "card": {
      "rootClasses": ["slds-card"], "background": "#ffffff", "border": "1px solid #c9c9c9", "borderRadius": "4px",
      "subParts": { "header": "slds-card__header", "headerTitle": "slds-card__header-title", "body": "slds-card__body", "bodyInner": "slds-card__body_inner", "footer": "slds-card__footer" }
    },
    "tile": {
      "rootClasses": ["slds-tile", "slds-media"], "fontSize": "13px",
      "subParts": { "title": ["slds-tile__title", "slds-truncate"], "detail": "slds-tile__detail", "mediaBody": "slds-media__body" },
      "variants": ["board (kanban)", "with-icon", "with-checkbox"]
    },
    "descriptionList": {
      "rootElement": "dl",
      "variants": { "horizontal": "slds-list_horizontal", "stacked": "slds-form-element_stacked", "verticalGrid": "slds-form-element_horizontal" },
      "term": ["slds-item_label", "slds-text-color_weak"], "definition": ["slds-item_detail", "slds-truncate"]
    },
    "relatedList": { "pattern": "slds-card > slds-card__header (titulo + count + acciones) > slds-card__body > slds-table | slds-tile-list" }
  },
  "recordLayoutPatterns": {
    "recordHome": "slds-page-header (record-home) + slds-grid de columnas: panel principal (slds-col) con slds-tabs / slds-card, y panel lateral (slds-col) con highlights y related lists.",
    "listView": "slds-page-header (object-home con dropdown de vista, search, filtros y botones) + slds-table dentro de un contenedor con scroll.",
    "splitView": "slds-split-view: lista a la izquierda (slds-split-view__list) + detalle a la derecha."
  }
}
```
