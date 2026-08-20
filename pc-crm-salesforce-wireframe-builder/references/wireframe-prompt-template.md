# Plantilla del prompt para Claude Design — Set de wireframes Salesforce Lightning

Esta es la plantilla que ensamblas en el Paso 3 del SKILL. Sustituye todo lo que está entre `{{ }}` con lo resuelto en los Pasos 0–2 (clasificación, descartes, inventario, detalle de HUs). **No mandes el prompt con placeholders sin resolver ni abrevies datos con "etc."** — Claude Design no ve la conversación.

La misma plantilla sirve como **especificación de fidelidad** para el fallback HTML (Paso 5): si generas el set tú mismo, respeta el catálogo de componentes y las reglas de fidelidad de abajo. Los valores exactos de color, tipografía y spacing viven en `references/slds-design-tokens.md`, y las clases SLDS + estructura + densidad de cada componente en `references/slds-component-blueprints.md` (ambos también van resumidos en esta plantilla, secciones "Design tokens SLDS" y "Clases y densidad SLDS").

---

## PLANTILLA (copia desde acá, resolviendo los `{{ }}`)

````markdown
# Set de wireframes Salesforce Lightning — {{Nombre del proyecto}}

Aplica ESTRICTAMENTE el design system de este proyecto (ProContacto · Salesforce Design System): tokens de color, tipografía Salesforce Sans, spacing, íconos de objeto Lightning y componentes (nav bar, record header, highlights panel, Path, tabs, secciones colapsables, related lists, modales, toasts, edición inline). No inventes colores, sombras ni layouts fuera del sistema. Si no tomas el design system, repite en la primera línea: "usa estrictamente el design system de este proyecto".

## Design tokens SLDS (valores exactos — úsalos tal cual)
Estos son los tokens oficiales del Salesforce Lightning Design System. Aplícalos literalmente; no inventes ni aproximes hex, spacing ni tamaños de fuente.
- **Fondo de página:** `#f3f2f2`. **Cards / header / secciones:** `#ffffff`. **Bordes** (cards, tablas, inputs): `#dddbda`, 1px. **Hover de fila:** `#fafaf9`.
- **Azul de marca / botón primario:** `#1b96ff`, hover/active `#0176d3`, dark `#014486`. **Links:** `#0b5cab` (active `#014486`). **Focus ring:** `0 0 2px #0176d3`.
- **Texto:** principal `#2b2826`, secundario/labels `#706e6b`, deshabilitado/placeholder `#b0adab`.
- **Estados** (texto / fondo suave): success `#2e844a` / `#ebf7e6` · warning `#dd7a01` / `#fff1ea` · error y asterisco de requerido `#ea001e` / `#fef1ee` · info `#0176d3` / `#eef4ff`.
- **Path:** etapa actual `#0176d3`, completadas `#2e844a`, pendientes fondo `#ecebea` texto `#706e6b`.
- **Tipografía:** stack `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`. Label de campo `0.75rem`, valor/body `0.875rem`, título de sección `1rem`, nombre de registro en el header `1.5rem` bold, line-height texto `1.5` / heading `1.25`.
- **Spacing (rem):** xSmall `0.5` · small `0.75` · medium `1` · large `1.5`. Padding de card/sección `1`–`1.5rem`, gap entre campos `0.75rem`, padding de celda `0.5`–`0.75rem`.
- **Forma:** border-radius `0.25rem` (cards/inputs/botones), pill `15rem` (badges/toggles), avatar circle. Sombra de dropdown/menú `0 2px 3px 0 rgba(0,0,0,0.16)`.
- **Íconos de objeto:** color Lightning propio de cada objeto estándar (Account turquesa, Contact azul, Opportunity dorado, Lead naranja, Case rojo-naranja…). Nunca emojis.

## Clases y densidad SLDS (estructura del markup)
Usa las clases SLDS reales y la densidad compacta característica de Salesforce. Convención: prefijo `slds-`, modificadores con guion bajo (`slds-table_bordered`), estados con `slds-is-` (`slds-is-selected`, `slds-is-sorted_asc`), sub-partes BEM (`slds-card__header`, `slds-page-header__title`).
- **Tablas / List Views (densas, NO esponjosas):** `table.slds-table.slds-table_bordered.slds-table_fixed-layout`. Header `th` 32px alto, `13px`/`700`, color `#444444`. Celdas `td` padding `4px 8px`, alto ~30.75px, `13px`, color `#181818`, line-height `19.5px`. Ordenable `slds-is-sortable`/`slds-is-sorted_asc`; fila seleccionada `slds-is-selected`; checkbox `slds-checkbox_faux`; inline edit `slds-cell-edit` + popover `slds-popover_edit`; truncado `slds-truncate`.
- **Page Header** (List View y Record Home): `slds-page-header`, fondo `#f3f3f3`, padding 16px, radius 4px, sombra `0 2px 2px 0 rgba(0,0,0,0.1)`; título `slds-page-header__title slds-truncate`, contador en `slds-page-header__meta-text`, acciones en `slds-page-header__controls`. Variantes object-home / record-home / related-list.
- **Card** (secciones y related lists): `slds-card`, fondo blanco, borde `1px solid #c9c9c9`, radius 4px; `slds-card__header` (título + count + acciones) → `slds-card__body`.
- **Detalle clave-valor:** `<dl>` con term `slds-item_label slds-text-color_weak` y value `slds-item_detail slds-truncate`.
- **Related List:** Card + Data Table → `slds-card > slds-card__header (título+count+acciones) > slds-card__body > slds-table`.
- **Layouts:** Record Home = `slds-page-header (record-home)` + `slds-grid` (panel principal `slds-col` con `slds-tabs`/`slds-card` + panel lateral `slds-col` con highlights y related lists). List View = page-header object-home + `slds-table` en contenedor con scroll. Split View = `slds-split-view` (lista `slds-split-view__list` + detalle).
- Detalle estructural completo de cada componente en `references/slds-component-blueprints.md`.

## Objetivo
Genera un set de wireframes navegables, en alta fidelidad, INDISTINGUIBLES de una implementación real de Salesforce Lightning Experience. El usuario final es un consultor/admin Salesforce: debe reconocer al instante Navigation Bar, Home, List Views, Record Pages, Path, Related Lists, Activities, Chatter, Files, Quick Actions, Notifications, Approvals y Salesforce Mobile. NO diseñes CRM genérico, dashboards SaaS modernos ni layouts inventados. Genera Desktop (1280px) y Mobile (Salesforce Mobile App).

## Tipo de proyecto
{{CRM comercial | App operativa / integración sobre objeto(s) custom}}. {{Si es app operativa: NO incluyas Home de vendedor, Leads, Oportunidades, Cotizaciones ni Forecast. Centrá el set en la(s) Record Page(s) del/los objeto(s) eje y en los LWCs/Quick Actions.}}

## Inventario de wireframes a generar (ya resuelto)
{{Pega acá la tabla del inventario: Wireframe | HUs cubiertas | Variantes | Componentes reutilizados. Genera los wireframes en este orden.}}

## Detalle por wireframe
{{Por cada wireframe del inventario, da el detalle concreto: objeto/s, compact layout (3-5 campos), etapas del Path, tabs visibles, related lists, quick actions, campos por sección con su tipo (text, picklist con opciones, date, currency, lookup, checkbox, read-only), y datos de muestra realistas y COHERENTES entre pantallas (mismo registro a lo largo del flujo).}}

## Componentes y patrones (incluye cada uno SÓLO si el inventario lo tiene)

### Navigation Bar (en TODOS los Desktop)
Barra Lightning **blanca** (`#ffffff`, NO azul oscuro/navy): App Launcher (waffle), **logo = nube de Salesforce por default** (cloudBlue `#00a1e0`; usa un logo/branding propio SOLO si el proyecto lo indica explícitamente), nombre de la app, tabs de los objetos en alcance, búsqueda global centrada, favoritos (estrella), ayuda (?), campana de notificaciones con badge, setup (engranaje), avatar. Tab activa con subrayado azul `#1b96ff`. El header global NUNCA es una franja azul oscura.

### Home Page Lightning [sólo si el alcance la tiene]
Layout de dos columnas. **Columna izquierda (principal, ancha): dashboard con 2-3 charts/reportes de ejemplo** coherentes con los objetos del proyecto (ej: "Prospectos por Estatus" en barras, "Prospectos por Clasificación" en torta, "Prospectos por Vendedor"), cada uno con título, gráfico simple, "Ver reporte" y "As of Today at HH:MM". **Columna derecha (más angosta): Actividades** (composer Nueva tarea / Llamada / Evento / Email, Tareas pendientes, Próximos eventos) y, si aplica, "Mis aprobaciones pendientes".
**NO incluyas** un bloque de "Accesos rápidos" con botones de alta, **ni una lista de registros** ("Mis Prospectos" / "Todos los prospectos") al pie de la Home: eso vive en la List View, no en la Home. La Home estándar es **dashboard/reportes + actividades, y nada más.**

### Patrón de navegación (encadenar todas las pantallas)
Home -> tab del Objeto -> List View -> Registro -> Editar -> procesos relacionados. NUNCA navegar de Home directo al registro.

### List View (plantilla única, una por objeto vía variantes)
- **Selector de vistas = DROPDOWN, no tabs.** Muestra el nombre de la vista activa en grande con un caret; al abrir, un panel con buscador "Search lists…" y dos grupos: **"Recent List Views"** (con check ✓ en la activa y la vista fijada/pin) y **"All Other Lists"**. Nunca pongas las vistas como botones/tabs horizontales (Todos · Recientes · Activos).
- **Meta de la vista:** debajo del nombre, "N items • Updated a minute ago".
- **Barra de íconos — OBLIGATORIAMENTE alineada a la DERECHA.** Es una fila con dos extremos: a la **izquierda** queda solo el nombre de la vista + meta; **TODO el cluster de íconos se empuja al extremo derecho** (flex con `margin-left:auto` / `justify-content:flex-end`), alineado con los botones Nuevo/Importar/Exportar de arriba. NUNCA pegados a la izquierda debajo del nombre. Orden del cluster: engranaje (List View Controls), selector de display (Tabla/Kanban/Split View), refresh, sort, editar (lápiz), charts, embudo de filtros.
- **Filtros = panel "Filters" a la derecha** (se abre con el embudo): arriba "Filter by Owner" (All / My), luego "Matching all of these filters", cada filtro como **card con Campo + operador + valor y un ícono de tacho** para borrar, y links **"Add Filter"**, **"Remove All"** y **"Add Filter Logic"**. NO un sidebar de filtros inventado.
- **Tabla:** densa SLDS; cada **columna con su caret** (ordenar asc/desc, redimensionar, mostrar/ocultar). Checkboxes de fila + "seleccionar todo", acciones masivas, paginación. Botones de la page-header: Nuevo, Importar/Exportar, etc. (cuando apliquen). Las columnas cambian por objeto.

### Record Page (plantilla maestra — misma estructura para todos los objetos)
- Record Header: ícono del objeto (color Lightning correspondiente), nombre en bold grande, badge(s) de estado, compact layout. Fondo BLANCO (nunca azul Classic).
- Compact Layout: 3-5 campos destacados, distintos por objeto.
- Action Bar / Quick Actions (arriba derecha): Editar, Clonar, Compartir, Eliminar + acciones específicas (Convertir, Enviar a aprobación, Generar PDF, Reintentar, etc.) — sólo las que pidan las HUs, con visibility por estado/permiso cuando corresponda.
- Path (Lightning Path) cuando el objeto tiene proceso/estados: chevrons reales (actual `#0176d3`, completadas `#2e844a` con ✓, pendientes gris). El botón **"Marcar etapa como actual/completada" va a la MISMA ALTURA que los chevrons** (alineado a la derecha, en línea con el path), nunca en una fila separada debajo. Debajo del path, el bloque **"Guía para el éxito" (Guidance for Success)** en dos columnas: a la **IZQUIERDA los Campos clave** (label + valor, **hasta 5 como máximo**) y a la **DERECHA el texto descriptivo** de la etapa actual. Las etapas salen de las HUs del proceso.
- **Tabs principales (panel izquierdo): Detalles, Actividad, Chatter** (+ tabs custom: Notas, Archivos según el objeto). La tab **"Relacionado/Relacionados" NO va acá: va en el panel DERECHO**. El resto de las tabs quedan a la izquierda.
- Tab Detalles: **secciones bien ordenadas y agrupadas lógicamente** (Información general, Contacto, Información comercial, etc.) con campos en orden coherente; **cada sección abre con una banda de encabezado de ancho completo en gris claro `#f3f2f2` con borde inferior `#dddbda`** (debe leerse claramente como "una sección"; la tipografía y su color ya están bien). Secciones colapsables, campos side-by-side (label izq. ~38%, valor der.), ícono editar en hover; respeta el tipo de cada campo.
- **Panel derecho — tab "Relacionado" que agrupa TODAS las Related Lists del objeto** (cada una como card SLDS: tabla con encabezado + contador + [Ver Todos], NO tarjetas modernas). **El "Historial de cambios" va DENTRO de esta tab como una related list más, junto a las demás** — nunca como card suelta aparte. Además, paneles auxiliares (ej: Ubicación/mapa) según las HUs. Qué related lists mostrar:
  - Si las HUs **NO especifican**: pon siempre **Archivos, Notas y Adjuntos** + las **related lists estándar del objeto** (ej: Cuenta → Contactos, Oportunidades, Casos; Oportunidad → Productos, Contactos; etc.) + Historial de cambios.
  - Si hay HUs que **sí especifican** related lists: pon esas (más Historial de cambios).
  - Incluye también los **objetos custom** relacionados que aparezcan en el modelo/HUs.
- Tab Actividad: barra de sub-tabs **Nueva tarea / Registrar llamada / Nuevo evento / Correo**. **Al seleccionar CUALQUIERA de ellas se muestra SU propio composer** (campo de descripción/asunto + botón Guardar para tarea; registro de llamada; nuevo evento con fecha/hora; redactar correo) — ninguna sub-tab puede quedar vacía o muerta. Debajo, timeline con Tareas, Correos, Eventos, Llamadas (+ WhatsApp si aplica).
- Tab Chatter: publicaciones, comentarios, menciones, archivos compartidos.
- Files: área de carga (arrastrar/seleccionar/nueva versión) + lista (Nombre, Tipo, Fecha, Propietario) con Vista previa/Descargar/Eliminar.
- Una variante de Record Page por cada objeto en alcance (compact layout, Path, tabs y related lists propios).

### New/Edit Form (plantilla única)
Modal estándar Salesforce: secciones, campos según tipo, obligatorios con **asterisco rojo**; botones Guardar / Guardar y Nuevo / Cancelar. Mismo layout para Crear y Editar (variantes).
**Muestra SIEMPRE (obligatorio, no opcional) al menos un campo en estado de error de validación**, replicando el patrón real de Salesforce:
- **Campo inválido:** borde rojo `#ea001e`, **ícono circular de "prohibido" (⊘)** dentro/al inicio del campo, y **mensaje en rojo debajo** del campo.
- **Error a nivel página = popover anclado al botón Guardar** (no un recuadro arriba del form): encabezado rojo **"Encontramos un problema"** con ✕, y debajo **"Revise los siguientes campos"** con la **lista de campos en error como links** (ej: Nombre del prospecto, External ID). Suma un **ícono ⊘ rojo al lado del botón Guardar** indicando que el guardado está bloqueado.
- **Textos en español** (igual que toda la UI): mensaje del campo "Debe completar este campo para continuar" (o la regla de negocio de la HU si existe, ej: RUT/RFC inválido, monto > 0). Nunca dejes los textos en inglés.

### Line Item Editor [sólo si hay objetos con líneas: Opp/Quote/Order]
Selector de Lista de Precios, grilla de líneas (cantidad, precio dentro de piso/techo, descuento %, total), recálculo automático de totales, validación de precio/descuento.

### Lead Convert [sólo si hay Leads]
**Una sola pantalla** de conversión (no dos). Tres columnas — Cuenta, Contacto, Oportunidad — y en cada una, dentro de la misma vista, el toggle **"Crear nuevo" vs "Vincular a uno existente"** (buscar/seleccionar registro existente o crear uno nuevo con mapeo de campos). Valida obligatorios faltantes. No separes "crear nuevos" y "vincular existentes" en pantallas distintas.

### Web-to-Lead [sólo si hay HUs de Web-to-Lead]
Wireframe del **formulario web público** tal como lo vería el visitante, embebido en una página web. **Estilo web neutro/genérico — SIN el chrome de Salesforce ni el design system Lightning** (no nav bar, no íconos de objeto). Campos que captura el form según las HUs (Nombre, Empresa, Email, Teléfono, etc.), botón Enviar y un estado de confirmación/"gracias" post-envío.

### Salesforce Maps [sólo si hay HUs de Salesforce Maps] — chrome propio, SIN versión mobile
Módulo aparte con su **propio chrome** (NO el Lightning estándar): header azul "Salesforce Maps" con tabs **Layers · Routes · Schedule · List**, barra de herramientas de íconos a la derecha y buscador. Todo en español. Genera las vistas que pidan las HUs:
- **Layers:** mapa grande a la derecha + panel de capas a la izquierda (tabs Recientes/Guardadas/En el mapa). **Pins/markers** que representan registros (ej: clientes/tiendas) con su color, y **boundaries/polígonos por país o región** (las formas dependen del país, ej: provincias). Card de capa con "Registros: N", geocodificados y markers visibles.
- **Routes:** armado de **rutas**. Panel izquierdo con Nombre de ruta, botón **Optimizar**, toggle "Bloquear orden de paradas", **lista de paradas numeradas** (dirección + tiempo/distancia entre paradas), footer "1 h 4 min con tráfico · 30.6 km · 43 paradas · Agregar parada". En el mapa, la **ruta dibujada** con los stops numerados.
- **Schedule (programar visitas):** calendario por día con franjas horarias a la izquierda + panel "Sin programar" a la derecha (markers sin agendar con su empty state), **drag&drop de markers al calendario**, selector de fecha / Hoy.
- **List:** vista de lista de los registros del mapa.

### Planificador avanzado de visitas [sólo si hay HUs de Advanced Visit Planning] — chrome propio (wizard), SIN versión mobile
**Wizard multi-paso** con stepper de círculos (Asignar usuarios → Definir configuración del plan → Opciones adicionales → Confirmar y guardar), botones **Anterior / Guardar y siguiente** abajo y progress indicator. Todo en español. Pasos (incluye los que pidan las HUs):
- **Segmentación de clientes:** "Mapeo de campo de usuario asignado" + tabla **Filtros de campo** (Campo / Operador / Valor) con "Agregar fila" y "Agregar lógica de filtros" — define qué clientes entran al plan.
- **Ventanas de visita:** tabla por **día de la semana** (Domingo→Sábado) con "Agregar ventana de visita" (Ventana 1 / 2) y "Aplicar a todos los días"; acá se define **frecuencia (diaria/semanal/mensual/cuatrimestral), días y franja horaria**.
- **Asignar usuarios:** tabla de Usuarios (Nombre / Perfil / Rol / Manager) con checkboxes, buscador y contador "N usuarios asignados" — a qué vendedores se les planifica.
- **Configuración del plan:** **fecha de inicio y fin**, checkbox "Reiniciar el plan al finalizar", y cantidad de datos de ruta tras la optimización (ej: 3 Meses).
- **Optimización (batches):** "Programar lotes de optimización" — frecuencia (cada N semanas), hora, y **días de la semana** (checkboxes Dom–Sáb) para incorporar nuevos clientes al plan.

### Kanban + Forecast [sólo si hay Oportunidades con forecast]
Kanban por etapa con drag&drop, probabilidad por columna, Collaborative Forecast, dashboard de pipeline con filtros.

### Wizard multi-paso (LWC) [sólo si alguna HU describe un LWC de varios pasos]
Progress indicator Lightning, navegación Atrás/Siguiente, estado conservado entre pasos, búsqueda con autocomplete donde aplique, validaciones por paso, resumen y confirmación final con bloqueo anti-duplicado.

### Approvals [SÓLO si el backlog tiene HUs de un proceso de aprobación]
Genera esto únicamente cuando alguna HU implique enviar a aprobación / aprobar / rechazar / registro bloqueado. Si no hay HUs de aprobación, NO inventes nada de aprobación en la Record Page. Cuando aplica:
- **Estado en el registro:** badge **"Pendiente de aprobación"** al lado del nombre y/o un campo de estado de aprobación. NO una leyenda amarilla arbitraria de "fue enviado".
- **Banner de solo-lectura (sólo cuando el registro queda bloqueado):** franja amarilla arriba "Pendiente de aprobación de [proceso] · Enviado a [persona] el [fecha] · Este registro es de solo lectura", botón "Ver historial de aprobación", **acciones principales deshabilitadas** (Editar/Convertir en gris) y badge **"Solo lectura"** con candado.
- **Pantalla de Solicitud de Aprobación** (a la que llega el aprobador): **header con compact layout** — ícono + "Solicitud de Aprobación" + nombre del registro + badge PENDIENTE, y los datos de la solicitud como compact layout (Solicitante · Fecha de solicitud · Aprobador actual · Asignado a · Estado · Proceso). Botones **Aprobar** (azul `#0176d3`) y **Rechazar** (rojo `#ea001e`) **solo en el header, arriba a la derecha** (no repetidos en el cuerpo). **Columna izquierda (principal):** el resumen/detalle del registro (Approval Details, los campos del registro). **Columna derecha:** Comentarios ("Agregar comentario…") + Historial de aprobación. Los botones Aprobar/Rechazar NO van dentro del bloque de Comentarios.
- **Notificación al aprobador:** entrada en la campana/notificaciones "El usuario [X] ha solicitado la aprobación del siguiente registro: [nombre]" que linkea a la pantalla de Solicitud de Aprobación.

### Notification Center [sólo si hay notificaciones/aprobaciones/alertas]
Panel Lightning desde la campana: aprobaciones, recordatorios, alertas, menciones. Incluye al menos un toast Lightning de ejemplo.

### Delete Confirmation
Modal estándar: "¿Está seguro que desea eliminar este registro?" con [Cancelar] [Eliminar].

### Dashboards / Reports [sólo si las HUs los piden]
Dashboards con gráficos + KPIs y filtros (territorio/canal/período/RT). Reports tabulares con columnas, filtros y botón Exportar.

### Documentos imprimibles (PDF) [sólo si las HUs generan PDFs: cotización, recibo, comprobante]
Plantilla PDF branded con datos del registro, desglose y firmas/condiciones según el caso.

## Experiencia Mobile (Salesforce Mobile App) — SECCIÓN SEPARADA
Genera los wireframes mobile en una **sección/lienzo PROPIO, claramente separado del Desktop. NO intercales pantallas mobile entre las desktop.** Cada wireframe principal lleva su versión móvil con el MISMO contenido (no una experiencia distinta). Sigue los patrones de la Salesforce Mobile App:
- **Header mobile BLANCO** (`#ffffff`, NUNCA navy/azul oscuro), con "‹ [Objeto]" o "‹ Atrás" + título a la izquierda y los íconos compartir / favorito (estrella) / buscar / notificaciones a la derecha, todos en azul. No dibujes una status-bar falsa estilizada (hora/wifi/batería): déjala neutra o nativa.
- **Bottom tab bar fija** (5 ítems, ej: Prospectos · Cuentas · Contactos · Eventos · Menú), con la activa en azul.
- **Mobile Record:** tarjeta con ícono+tipo de objeto y nombre, campos clave clave-valor, **acciones rápidas como botones circulares arriba** (ej: Crear Muestra, Agendar en Maps), secciones **colapsables "Relacionado" / "Detalles" con chevron ›**, **Path compacto horizontal** (scroll) + "Estado: X" + botón "Marcar Estado como completado(a)", botón "Seguir" y "Actividad reciente".
- **Mobile List View:** buscador arriba, grupos "Listas" / recientes, selector de vista con caret, **Filtrar y Ordenar como dos botones circulares** arriba, registros como **tarjetas apiladas clave-valor**.
- **Mobile Home / Eventos:** Home con las mismas tarjetas que desktop adaptadas a una columna; calendario mensual con el día actual resaltado cuando haya Eventos.
- **EXCEPCIÓN:** **Salesforce Maps y el Planificador avanzado de visitas NO tienen versión mobile** — genéralos solo en Desktop, no hagas su variante móvil.

## Reglas de fidelidad (qué evitar)
- **Idioma:** todos los labels, botones, mensajes y textos de la UI van en el **idioma del proyecto/HUs (acá español)**. Nunca dejes textos en inglés ("Save", "We hit a snag", "Add Filter"): tradúcelos ("Guardar", "Encontramos un problema", "Agregar filtro").
- **Header global blanco** (`#ffffff`), NUNCA una franja azul oscura/navy — ni en Desktop ni en Mobile. Logo = nube de Salesforce por default.
- Fondo de página gris claro SLDS `#f3f2f2`; header, cards y secciones en blanco `#ffffff`; bordes `#dddbda` (1px).
- NO headers azules estilo Classic; NO tarjetas modernas en Related Lists; NO emojis como íconos de objeto (usa los íconos Lightning del design system con su color).
- Campos side-by-side, no stacked. Path con chevrons reales (actual `#0176d3`, completadas `#2e844a`) y botón de etapa en línea con los chevrons. Tabs con subrayado azul `#1b96ff`. Selector de vistas como dropdown (no tabs). Toasts y modales SLDS; toast de guardado en success `#2e844a`. Links en `#0b5cab`.
- **Mobile siempre en sección separada del Desktop**, nunca intercalado.
- Datos de muestra realistas y coherentes entre pantallas (mismo registro a lo largo del flujo) para que el set sea navegable.

## Formato de salida
Wireframes navegables Desktop (1280px) + Mobile, coherentes entre sí, en el orden del inventario. El resultado debe parecer una implementación real de Salesforce Lightning Experience estándar; evita wireframes simplificados o conceptuales.
````

---

## Adaptaciones del template

- **CRM comercial:** incluye Home Lightning, List Views de estándar, Path, Lead Convert, Kanban + Forecast, Approvals según las HUs.
- **App operativa / integración:** quita Home de vendedor, Leads, Oportunidades, Cotizaciones y Forecast salvo pedido explícito; centrá en la(s) Record Page(s) del objeto eje y los LWCs.
- **Anexo de HU / demo cliente:** aclara que los datos son de muestra y el foco es validar campos y agrupamiento.
- **Pitch comercial / AppExchange:** datos ficticios pero realistas, estética polished.

## Notas para el fallback HTML (Paso 5)
- Define los tokens de `references/slds-design-tokens.md` como CSS custom properties (`:root { --slds-... }`) y referencialos en cada componente. No hardcodees hex sueltos.
- Un archivo por wireframe (o uno con navegación interna), CSS y JS inline, sin dependencias externas salvo las del design system.
- Links reales entre pantallas siguiendo el patrón de navegación (Home -> List View -> Record -> Edit -> proceso).
- Fondo de página `#f3f2f2`; header/cards/secciones en blanco `#ffffff`; bordes `#dddbda`. Campos side-by-side (label ~38%, `0.75rem`, color `#706e6b`; valor `0.875rem`). Record header blanco con ícono de objeto en su color. Tab bar con subrayado azul `#1b96ff` en la activa. Edición inline con toast verde `#2e844a` al guardar. Border-radius `0.25rem`; sombra de menú `0 2px 3px 0 rgba(0,0,0,0.16)`.
