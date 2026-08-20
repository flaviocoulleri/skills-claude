# Generación de Weekly Status — template ProContacto

Acción global del PASO 2 que arma un documento Google Docs con el reporte semanal del proyecto, siguiendo el template formal usado por PC. Se guarda en la carpeta Drive del proyecto.

## Estructura del documento

El doc replica el formato de los weekly status que circulan en PC (referencia: weekly de Marketing Cloud / Solo Deportes 23/12). Tiene 7 secciones obligatorias en este orden:

1. **Título** — `Weekly Status <Sistema/Producto>: <Cliente> <DD/MM>`
2. **Tabla de detalle de avance** — Fecha, Sprint, Estado, Fechas de finalización con badges
3. **Detalle de avance del proyecto** — Semana anterior + Semana actual con issues
4. **Capacitaciones** — links a videos + sesiones agendadas
5. **Roadmap** — Gantt-style chart con sprints en columnas y entregables en filas
6. **Acciones pendientes** — Tabla Ítem / Responsable / Fecha / Status
7. **Footer** — Saludo + logo ProContacto

## Branding ProContacto

Aplica el manual de marca v2026 (capa visual). Detalle exacto en `pc-admin-interno-brand-applier`. Resumen para este doc:

- **Headings**: color `#0062FF` (azul ProContacto) en cursiva para los headers de sección.
- **Tipografía**: Open Sans (Google Docs default si está disponible, fallback Arial).
- **Badges de estado**:
  - `ON-TRACK` — fondo verde claro `#E5F5EE`, texto `#005F3E`
  - `AT-RISK` — fondo amarillo `#FFF1E5`, texto `#D14600`
  - `DEMORADO` — fondo rojo claro `#FCE8EC`, texto `#B6002D`
  - `FINALIZADO` — fondo verde claro `#E5F5EE`, texto `#005F3E`
  - `EN CURSO` / `TAREA EN CURSO` — fondo azul claro `#E5EFFF`, texto `#005FCB`
  - `DEPRECADO` — fondo gris claro, texto gris oscuro
  - `PENDIENTE` — fondo rojo claro, texto rojo
- **Footer**: logo ProContacto (asset desde el manual de marca) + texto "ProContacto · Soluciones tecnológicas integrales".
- **Tablas**: header row con fondo azul claro `#E5EFFF`, texto `#0B0C0E` bold. Bordes finos `#E2E8F0`.
- **Capa verbal**: usar el ANCLAJE en el footer ("Soluciones tecnológicas integrales"). NO usar el slogan institucional ("Aliados en tu transformación") — un weekly status es operativo, no de cierre.

## Mapeo scoring → estado del proyecto

El badge de "Estado del proyecto" se deriva del scoring del audit:

| Score | Letra | Estado |
|---|---|---|
| 75-100 | A, B | ON-TRACK |
| 60-74 | C | AT-RISK |
| 0-59 | D, F | DEMORADO |

Si el caller corrió el weekly **inmediatamente después** del PASO 2, reutilizar el score ya calculado. Si pasaron >5 minutos (cache invalidado), recalcular antes de armar el doc.

## Queries por sección

### Sección 2 — Tabla de detalle de avance

| Campo | Fuente | Cómo se extrae |
|---|---|---|
| Fecha | hoy | `today()` en `America/Argentina/Buenos_Aires` |
| Sprint actual | Jira | sprint activo del board del proyecto |
| Estado del proyecto | Scoring | mapeo letra → ON-TRACK / AT-RISK / DEMORADO |
| Fecha de finalización del proyecto inicial | Salesforce | `Project__c.Initial_End_Date__c` |
| Sub-status de finalización | Comparar con hoy | si `endDate < hoy` y status no es Done → DEMORADO; si `endDate < hoy + 7d` y aún hay >30% open → AT-RISK; sino ON-TRACK |
| Fecha de finalización personalization (u otro entregable) | Salesforce | `Project__c.Customizations_End_Date__c` o equivalente |

### Sección 3 — Semana anterior

```jql
project = "<KEY>"
  AND sprint = "<previous_sprint_id>"
  AND statusCategory = Done
ORDER BY rank ASC
```

Render: lista jerárquica con issues padre y sub-tareas indentadas. Cada issue: link `<KEY>: <summary>` + badge de status.

Si el sprint anterior tiene >25 issues completados, mostrar sólo los Story/Bug top-level y agrupar las subtasks bajo su padre. No listar todos los Sub-task individualmente — agrega ruido al weekly.

### Sección 3 — Semana actual

```jql
project = "<KEY>"
  AND sprint = "<current_sprint_id>"
ORDER BY rank ASC
```

Para cada issue, agregar contexto si está en `customfield_<NotaWeekly>` o description tipo "Salida a producción: <fecha>". Si no hay contexto, omitir el sub-bullet.

### Sección 4 — Capacitaciones

Source 1: Calendar — eventos próximos 14 días con keywords (`capacitación`, `training`, `sesión`, `walkthrough`) e invitados del cliente.

Source 2: Confluence — páginas del space con etiqueta `training` o título matcheando `(?i)capacitación|video tutorial|onboarding`.

Source 3: Project_Asset__c con `Type__c = 'Training video'` o `'Training session'` — links a Drive/Loom con videos grabados.

Estructura del bullet:
- Si es video grabado: `<título>: <link>`
- Si es sesión a coordinar (sin fecha): `<tema>: coordinar sesión`
- Si es sesión agendada: `<tema>: <fecha> <hora>`

### Sección 5 — Roadmap

Ideal: imagen del Gantt de Jira (la "Roadmap view" de Jira Software). Si el MCP de Atlassian no expone export de roadmap, hay 3 fallbacks en orden:

1. **Tabla simple** — generar con `searchJiraIssuesUsingJql` por Epic, mostrar columnas con sprints (1, 2, 3, ..., Hypercare) y celdas marcadas según en qué sprint cae cada Epic.
2. **Mermaid Gantt** — generar el código mermaid en el doc. Google Docs no renderiza mermaid nativamente, así que esta opción sólo aplica si el doc se exporta a HTML/PDF.
3. **Link a Jira roadmap** — `https://procontacto.atlassian.net/jira/software/projects/<KEY>/boards/<BOARD_ID>/roadmap` y un disclaimer "Roadmap interactivo en Jira ↗".

Por default arrancar con el Fallback 3 (link). Si el PM en el preview pide "ármame la tabla", regenerar con Fallback 1.

### Sección 6 — Acciones pendientes

Source: cross-skill con `pc-delivery-jira-pending-tracker`. Si el caller ya corrió ese skill en la sesión, reutilizar la lista de External pendings. Si no, hacer una query rápida a Jira:

```jql
project = "<KEY>"
  AND issuetype = "External pending"
  AND statusCategory != Done
ORDER BY duedate ASC
```

Render como tabla con columnas: Ítem (summary truncado a 80 chars) / Responsable (assignee o "Cliente" si está en custom field) / Fecha (duedate o vacío) / Status (badge).

### Sección 7 — Footer

Texto fijo:

```
Equipo, recuerden que estamos atentos a cualquier novedad, duda o inquietud
en pro de mantener los tiempos esperados del proyecto.

¡Muchas gracias y les deseamos excelente fin de semana!

[Logo ProContacto]
ProContacto · Soluciones tecnológicas integrales
```

## Preview chat-inline antes de generar

El widget de PASO 3 para esta acción muestra una tabla con las 7 secciones, cada una expandible y con toggle "incluir/no incluir":

```
[ ▼ ] [✓] Título                        Weekly Status MC: Solo Deportes 23/12
[ ▼ ] [✓] Tabla de avance               (4 filas con Fecha/Sprint/Estado/Fechas fin)
[ ▼ ] [✓] Semana anterior — Sprint 5    12 issues finalizados
[ ▼ ] [✓] Semana actual — Sprint 6      8 issues planificados
[ ▼ ] [✓] Capacitaciones                3 ítems (1 video + 2 sesiones)
[ ▼ ] [✓] Roadmap                       Link a Jira roadmap
[ ▼ ] [✓] Acciones pendientes           5 items (2 cliente + 3 PC)
[ ▼ ] [✓] Footer                        Saludo + logo
```

Cada sección expandible muestra el contenido editable en textarea/tabla. El PM puede:
- Desmarcar una sección para omitirla del doc final.
- Editar texto de cada sección.
- Agregar manualmente bullets que el skill no detectó.

Footer del widget: botón "Generar doc en Drive ↗" + "Cancelar ↗".

## Generación del doc en Drive

### Detección de la carpeta destino

1. Buscar `Project_Asset__c` con `Type__c = 'Drive folder'` y `Value__c` apuntando al folder ID.
2. Si no existe, buscar en Drive por nombre `<Account.Name> / <Project.Name>` o `<Project.Name>` en la carpeta raíz del cliente.
3. Si tampoco se encuentra, **avisar al PM** en el preview con un banner warning y opción "Crear carpeta nueva en Drive ↗" — pero esa creación va aparte, no se hace silenciosamente.

### Generación

Dos approaches según tools disponibles:

**Approach A (preferido)** — Google Doc nativo via Drive API:

```
mcp__ebf93048-...__create_file con:
  parent_folder_id: <folder_id>
  name: "Weekly Status <Producto>: <Cliente> <DD-MM-YYYY>"
  mime_type: "application/vnd.google-apps.document"
  content: <markdown o HTML del doc>
```

El MCP convierte el markdown/HTML a Google Doc nativo. Conserva tablas, listas y links. No siempre conserva colores exactos del branding — para colores se necesita la API de Google Docs específica que el MCP probablemente no expone directamente.

**Approach B (fallback)** — `.docx` generado localmente + upload:

1. Usar la skill `docx` para generar un `.docx` con todo el branding (colores exactos, logo embebido, badges).
2. `create_file` en Drive con mime_type del .docx (`application/vnd.openxmlformats-officedocument.wordprocessingml.document`).
3. El doc queda en Drive como archivo Office (no Google Doc nativo). Se puede abrir en Google Docs igualmente.

Por default arrancar con Approach A (más simple, doc editable directamente en Drive sin convertir). Si el branding de los badges es crítico para el cliente, usar Approach B.

### Naming del archivo

```
Weekly Status <Producto>: <Cliente> <DD-MM-YYYY>
```

Ejemplo: `Weekly Status MC: Solo Deportes 30-04-2026`. El "Producto" se extrae de `Project__c.Product_Line__c` o se infiere del Account/Project.

### Confirmación final

Después de generar exitosamente, el skill responde en chat con:

```
✅ Weekly status generado.
   Doc: <link al Google Doc>
   Carpeta: <link a la Drive folder>

Sugerencia: ¿Quieres postearlo al canal interno del proyecto?
[Postear link al canal ↗] [Cerrar ↗]
```

El botón "Postear link al canal" reusa el flow de notificaciones al canal interno (ver `slack-integration.md`).

## Restricciones

- **Nunca** sobreescribir un doc existente — si ya hay un weekly de la misma fecha en la carpeta, agregar sufijo `-v2`, `-v3`, etc.
- **Nunca** generar el doc sin OK explícito en el preview. El preview es la única vía de aprobación.
- **No incluir** en el doc data sensible (credenciales, tokens, datos personales fuera del nombre del assignee). Si el skill detecta keywords (`password`, `token`, `api_key`) en algún issue summary o description, **flagear y pedir al PM que confirme** antes de incluir.
- **Branding obligatorio** — invocar `pc-admin-interno-brand-applier` si está disponible para asegurar que colores y tipografía respetan el manual.
