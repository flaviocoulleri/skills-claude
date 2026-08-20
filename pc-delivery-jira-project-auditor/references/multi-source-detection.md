# Detección multi-fuente de "Trabajo invisible"

Categoría on-demand del PASO 2 que detecta tareas, compromisos y requerimientos que viven en otras fuentes (Slack, ReadAI, Meet, Calendar, Gmail, Confluence) pero no están cargados como issues en Jira. El usuario la dispara con el botón "Buscar trabajo invisible ↗" — nunca por default por costo de queries (ver `query-strategy.md` Nivel 3).

## Boundary con `pc-delivery-jira-pending-tracker`

Los dos skills barren fuentes externas. La diferencia:

| Skill | Qué carga | Tipo de issue |
|---|---|---|
| `pc-delivery-jira-pending-tracker` | Compromisos **del cliente** (External pendings) | `External pending` |
| `pc-delivery-jira-project-auditor` (categoría Trabajo invisible) | Trabajo **del equipo** no cargado + requerimientos del cliente sin convertir a Story | `Task` / `Story` |

Si los dos detectan el mismo extracto, gana el más específico:

- Si autor del mensaje es del dominio del cliente Y el verbo está en futuro/imperativo (`vamos a mandar`, `voy a enviar`) → External pending (pending-tracker).
- Si autor es del equipo PC Y el verbo es de compromiso (`yo me ocupo`, `lo hago`) → Task (este skill).
- Si es del cliente Y describe un requerimiento (`agregar`, `nuevo feature`) → Story (este skill).

## Fuentes y reglas

### ReadAI

**Cuándo se usa**: si el conector ReadAI MCP existe en la sesión, primero se intenta. Si no, se prompt-eaba al PM que pegue link de la reunión — pero esto degrada UX. En v1.8.0 se asume MCP presente; si no está, ReadAI se salta.

**Query**: action items extraídos por ReadAI en reuniones taggeadas con el proyecto, últimos 30 días.

**Filtro**: `meeting.project_tag == <PROJECT_NAME>` o asistentes incluyen email del PM/equipo del proyecto.

**Output**: action items con `text`, `assignee` (si ReadAI lo extrajo), `meeting_url`, `timestamp`, `confidence: high` (ReadAI ya hizo el trabajo de NLP).

**Cruce con Jira**: por cada action item, fuzzy match contra summary de issues abiertos del proyecto (>70% similitud). Si NO matchea, candidato a "Trabajo invisible".

### Google Calendar

**Query**: `list_events` últimos 21 días + próximos 21 días, filtrando por título o invitados que contengan referencias al proyecto.

**Filtro de extracción**: del campo `event.description`, extraer bullets/checkboxes:

```
• Action: enviar mockup a cliente — Andrea
- [ ] Revisar storypoints del epic — equipo
* TODO: agregar test de integración
```

Regex: líneas que arranquen con `[•\-\*]` o `\[\s\]` o keywords (`Action:`, `TODO:`, `Pendiente:`).

**Cruce con Jira**: cada bullet, fuzzy match contra summary. Si NO hay match, candidato.

**Confianza**: `media` por default (las descripciones de eventos son ruidosas), `alta` si el bullet tiene assignee explícito.

### Confluence

**Query**: `searchConfluenceUsingCql` en el space del proyecto, páginas modificadas últimos 30 días.

**Filtro de extracción**: parsear el contenido buscando secciones con headings que matcheen `(?i)action items|próximos pasos|decisiones|pendientes|next steps`. Extraer items de la lista que sigue al heading.

**Cruce con Jira**: cada item, fuzzy match contra summary + buscar issue key citado en el item (regex `<KEY>-\d+`). Si no hay key citada y no hay match → candidato.

**Confianza**: `alta` (Confluence está bien estructurado, los headings son señal fuerte).

### Slack — canal interno

**Query**: `slack_read_channel` del canal interno (ya detectado en `slack-integration.md`), últimos 14 días.

**Filtros de keywords** para compromisos del equipo:

```
yo me ocupo, lo hago yo, queda en mi backlog, lo agarro yo,
me lo llevo, lo arranco yo, voy a meter, voy a hacer
```

Sólo mensajes de autores del equipo PC (filtro por dominio email del workspace).

**Cruce con Jira**: regex de issue key cercano (±5 mensajes en el thread). Si no hay key cercano + el mensaje no tiene un issue Jira citado → candidato.

**Confianza**: `media` (Slack es ruidoso, los compromisos a veces son retórica). Sube a `alta` si el mensaje tiene `:white_check_mark:` o `:point_up:` (señales de "esto es serio").

### Slack — canal externo (cliente)

**Query**: `slack_read_channel` del canal externo del cliente (registrado como `Project_Asset__c` tipo `Slack channel external`), últimos 14 días.

**Filtros de keywords** para requerimientos del cliente:

```
agregar, nuevo feature, también necesitamos, falta también,
cambio en, nueva funcionalidad, sería bueno que, podríamos
sumar, queremos que
```

Sólo mensajes de autores del lado cliente (filtro por dominio).

**Cruce con Jira**: fuzzy match contra summary de issues abiertos. Si no hay match → candidato como Story.

**Confianza**: `media`.

### Gmail (interno)

**Query**: `search_threads` con filtro de threads donde TODOS los participantes son del dominio PC (workspace propio), últimos 14 días, asunto o body contiene referencias al proyecto.

**Filtros de keywords**: similar a Slack interno (`yo me ocupo`, etc.).

**Cruce con Jira**: regex de issue key + fuzzy match contra summary.

**Confianza**: `media`. Sube a `alta` si el thread tiene asunto tipo `[ACTION]` o `[Pendiente]` explícito.

## Deduplicación cross-fuente

Después de juntar candidatos de las 6 fuentes, deduplicar por similitud de texto:

1. Para cada par de candidatos, calcular similarity (Levenshtein normalizado o token-set ratio sobre el `extract`).
2. Si similarity > 80%, consolidar en una sola fila.
3. La fila consolidada lleva las dos fuentes como badges (`Slack + Calendar`) y el extracto del que tenga `confidence: high` (o el más reciente si empatan).

Esto evita que el mismo compromiso aparezca 3 veces si se mencionó en una reunión, después en Slack y después en un email.

## Schema del candidato

Cada candidato tiene este shape:

```json
{
  "extract": "Enviar mockup de pantalla principal a Andrea antes del jueves",
  "source": "readai",
  "source_url": "https://read.ai/meeting/abc123",
  "timestamp": "2026-04-28T14:30:00Z",
  "author": "Mariana Sosa",
  "author_side": "team" | "client",
  "confidence": "high" | "media" | "baja",
  "suggested_issue_type": "Task" | "Story",
  "suggested_assignee": "Mariana Sosa" | null,
  "suggested_summary": "Enviar mockup pantalla principal — fase 1"
}
```

`suggested_summary` es una versión normalizada del extract (verbo + objeto + contexto, max 80 chars) para que sea usable directamente en `createJiraIssue`. El usuario puede editarlo en el widget de PASO 3.

## Restricción importante

La categoría "Trabajo invisible" es la **única** donde el skill ejecuta `createJiraIssue`. Las otras categorías sólo modifican issues existentes (`editJiraIssue`). Esta excepción está documentada en las restricciones del SKILL.md y limita máximo 10 issues nuevos por batch, todos en estado `To Do`, con description que incluye link a la fuente para trazabilidad.
