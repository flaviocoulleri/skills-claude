# Estrategia de consultas — minimizar latencia

El skill consulta múltiples conectores. Sin estrategia, un audit puede arrastrar 15-20s. Esta spec documenta el sistema de 3 niveles, time bounds, fields mínimos y caching de sesión que mantienen el audit típico bajo 5s.

## Los 3 niveles

| Nivel | Cuándo se ejecuta | Qué consulta | Tiempo aprox |
|---|---|---|---|
| **1 — Core** | Siempre, automático en PASO 2 | Jira Q1-Q6 (paralelo, fields mínimos), Salesforce 1 query para fase, `getJiraProjectIssueTypesMetadata` para `recurringTypes` | 2-4s |
| **2 — Scoring contextual** | Default sólo si fase = Sprint 0. En Ejecución, on-demand vía botón "Calcular scoring completo ↗" en el widget | Calendar (eventos próximos 21d), Confluence (páginas últimos 30d), Slack (counts de mensajes 14d en canal interno) | +3-5s |
| **3 — Trabajo invisible (multi-fuente)** | **Siempre on-demand** vía botón "Buscar trabajo invisible ↗". Nunca por default | ReadAI, Meet transcripts, Gmail interno, Slack interno + externo (contenido completo), Calendar descriptions, Confluence "Action items" | +8-15s |

**Por qué Nivel 2 sí corre por default en Sprint 0**: en relevamiento, el scoring depende casi enteramente de señales externas a Jira (¿hay reuniones planeadas? ¿hay docs?). Sin Nivel 2, el scoring sería inservible. En Ejecución, el scoring central viene de Jira (asignaciones, fechas, releases) y Nivel 2 sólo refina — por eso queda on-demand.

## Reglas para minimizar consultas

### Fields mínimos por query Jira

Cada Q pide sólo lo que necesita su categoría. Tabla:

| Query | Fields necesarios |
|---|---|
| Q1 (sin asignar) | `summary`, `issuetype` |
| Q2 (vencidas) | `summary`, `issuetype`, `duedate`, `assignee` |
| Q3 (sin fecha) | `summary`, `issuetype`, `assignee` |
| Q4 (bloqueadas) | `summary`, `issuetype`, `status`, `issuelinks` (necesario para fallback Q4) |
| Q5 (sin release) | `summary`, `issuetype`, `assignee` |
| Q6 (artefactos) | `summary`, `customfield_<URL>` (después de descubrir el field) |

Nunca pedir `description` salvo que sea estrictamente necesario (es el campo más pesado). El payload por query baja 50-70% vs lo que el skill pedía hasta v1.7.x.

### Time bounds fijos por fuente

Cada fuente con un rango pre-definido — el modelo NO debe re-decidir el rango en cada audit:

| Fuente | Ventana | Justificación |
|---|---|---|
| Jira (queries del PASO 2) | sin filtro de tiempo (filtra por `statusCategory != Done`) | el scope ya viene del PM en PASO 1.3 |
| Sprint activo (PASO 2) | startDate → endDate del sprint | obvio |
| Histórico para asignación (PASO 3) | últimos 90 días resueltos | balance entre tener señal y no traer ruido |
| Calendar (Nivel 2 — Sprint 0) | próximos 21 días | el plan de relevamiento típico cubre 3 semanas |
| Calendar (Nivel 3 — multi-fuente) | últimos 21 días + próximos 21 días | capturar action items pasados y agendas futuras |
| Confluence (Nivel 2) | modificadas últimos 30 días | cubre creación + actualizaciones de relevamiento |
| Confluence (Nivel 3) | modificadas últimos 30 días | mismo |
| Slack canal interno (B1, bloqueos) | últimos 7 días | bloqueos que no son inmediatos pierden relevancia |
| Slack canal interno (B4, requerimientos) | últimos 14 días | dar tiempo a que se discuta |
| Slack canal externo cliente | últimos 14 días | mismo |
| Gmail interno (Nivel 3) | últimos 14 días | similar a Slack |
| ReadAI (Nivel 3) | últimos 30 días | reuniones de descubrimiento típicamente son cada 1-2 semanas |
| Meet transcripts (Nivel 3) | últimos 30 días | mismo |

### Cache durante la sesión

Si el PM corre el diagnóstico (PASO 2) y después dispara una acción (botón global de PASO 2 → PASO 3), reutilizar la data ya traída en lugar de re-querear:

- Lista de issues abiertos del proyecto: cache durante 5 minutos. Invalidado al cambiar proyecto o explícitamente con un "Refrescar diagnóstico ↗" si el modelo lo expone.
- `getJiraProjectIssueTypesMetadata`: cache durante toda la sesión (no cambia).
- Custom field de URL del Artefacto: cache durante toda la sesión.
- Releases abiertas: cache durante 5 minutos.
- Sprint activo: cache durante 5 minutos.
- Resultados de Nivel 2 (Calendar/Confluence/Slack counts): cache durante 5 minutos.
- Resultados de Nivel 3 (multi-fuente trabajo invisible): cache durante 10 minutos — son las más costosas, conviene reutilizar más.

El modelo lleva un dict `session_cache[<project_key>][<query_id>] = {data, timestamp}` y antes de re-querear chequea si el ttl está vigente.

### Conectores opcionales degradan silenciosamente

Si un conector no responde:

- Para Nivel 2: la dimensión que dependía de ese conector se omite y su peso se reparte entre las restantes (ya está en v1.5+).
- Para Nivel 3: la fuente se salta. El widget muestra "ReadAI no disponible — saltado" como nota chica al final, no como error bloqueante.

### Orden de ejecución dentro de un nivel

Dentro de cada nivel, las consultas se ejecutan en paralelo (Jira + Calendar + Confluence al mismo tiempo) salvo en el Nivel 3 que va **serial con orden de costo creciente** para que el usuario vea progreso:

1. ReadAI (rápido, devuelve action items estructurados)
2. Calendar (medio)
3. Confluence (medio)
4. Slack interno + externo (lento, requiere parsing)
5. Gmail (lento)

Si el usuario cancela mientras Nivel 3 corre, los resultados parciales se muestran igual con nota "búsqueda parcial — cancelada en `<paso>`".

### Counts antes que detalles

Para las queries Q1-Q6, primero traer `total` (un solo número) y sólo después de que el PM expanda una categoría, traer los issues completos. Esto va contra `searchJiraIssuesUsingJql` que devuelve `nodes` por default — workaround: `maxResults=1` en la primera tanda y `maxResults=N` cuando el PM expande.

Por simplicidad operativa, puede arrancarse con `maxResults=10` para todas las queries (suficiente para el resumen y la tabla detallada compacta) y subir a 50 sólo si el usuario expande explícitamente.
