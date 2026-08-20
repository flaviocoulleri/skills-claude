---
name: pc-delivery-jira-pending-tracker
version: 1.0.0
description: >
  Extrae pendientes del cliente desde emails, transcripts (Google Meet, Read.ai),
  Google Docs y Confluence, y los crea/actualiza como issues tipo "External pending"
  en el proyecto Jira que elija el Project Manager. Activar cuando el usuario diga
  "cargar pendientes del cliente", "extraer compromisos", "armar los externals",
  "pasar pendientes a Jira", "sincronizar pendientes", "actualizar external pendings",
  "crear external pending", "trackear compromisos", "revisar pendientes vencidos".
  También activar proactivamente cuando el PM comparte un transcript o email con
  compromisos del cliente sin asignar. Pregunta período y proyecto Jira antes de
  crear, detecta postergaciones para actualizar duedate en vez de duplicar, y para
  pendings vencidos ofrece redactar un draft de email al cliente pidiendo nuevas
  fechas. Orientado a Project Managers. Funciona en español e inglés.
---

<!-- Changelog
1.0.0 (2026-04-25): Primera versión formal bajo la convención pc-[área]-[sistema]-[objeto]-[acción]. Renombrado desde `jira-pending-tracker` → `pc-delivery-jira-pending-tracker`. Sin cambios funcionales.
-->

# Skill: Trackeo de External Pendings en Jira

## Descripción

Automatiza el trabajo que hoy hace manualmente un Project Manager de ProContacto cuando después de cada reunión/mail con un cliente tiene que:

1. Identificar qué compromisos quedaron del lado del **cliente** (no los nuestros).
2. Cargarlos como issues tipo `External pending` en el proyecto Jira correspondiente.
3. Mantenerlos al día: si el cliente postergó una fecha, actualizarla; si pasaron la fecha y no se entregó, hacer follow-up.

El skill recolecta fuentes (Gmail, Confluence, y opcionalmente Google Docs / Google Meet / Read.ai con ayuda del PM), extrae solo los compromisos **externos** con un prompt estricto, detecta duplicados/postergaciones contra lo que ya existe en Jira, y entrega un artifact editable para que el PM confirme antes de escribir nada.

---

## Herramientas requeridas

- **Atlassian MCP** (`mcp__plugin_data_atlassian__*`): `getAccessibleAtlassianResources`, `atlassianUserInfo`, `createJiraIssue`, `editJiraIssue`, `searchJiraIssuesUsingJql`, `getJiraIssueTypeMetaWithFields`, `getConfluencePage`, `searchConfluenceUsingCql`, `addCommentToJiraIssue`.
- **Gmail MCP**: `search_threads`, `get_thread`, `create_draft` (para follow-ups).
- **Cowork artifacts**: `mcp__cowork__create_artifact` (UI de revisión).
- **Opcionales según fuente**: Google Docs vía link (pedir al PM), Google Meet y Read.ai via paste manual.

## Restricciones

- **NUNCA** crear un issue `External pending` sin confirmación explícita del PM. Estos issues pueden volverse visibles al cliente (vía portal, reportes de status, o conversación) — un falso positivo es costoso.
- **NO** crear como `External pending` un compromiso que sea de ProContacto. Si detectas uno interno, menciónalo al PM y sugerí crearlo como Task normal — pero eso queda fuera del alcance de este skill.
- **NO** tocar issues en estado `Done` / `Cerrado` / `Cancelado` al hacer update, salvo que el PM lo pida explícitamente.
- **NO** inferir el proyecto Jira de forma automática. El PM lo indica siempre — la consecuencia de crear en el proyecto equivocado es cara (borrar issues, contaminación de reportes).

---

## Flujo completo paso a paso

### PASO 0 — Validar conectores y usuario

Antes de cualquier otra acción:

1. `getAccessibleAtlassianResources` → si falla, decirle al PM:
   > "Necesitas el conector de Atlassian activo. Actívalo en Configuración → Conectores."
   → **Fin del flujo.**
2. `atlassianUserInfo` → capturar email + accountId del PM (se usa para asignar owner y armar el `reporter` del issue).
3. Probar Gmail con un `search_threads` trivial → si falla, avisar al PM que sin Gmail el skill solo puede trabajar con fuentes pegadas a mano (Confluence, transcripts).

Si todo OK → PASO 1.

---

### PASO 1 — Recolectar contexto del PM (obligatorio)

Usar `AskUserQuestion` para pedir tres cosas en una sola pantalla:

1. **Período a analizar**: "Última semana" / "Últimos 15 días" / "Último mes" / "Elegir fechas".
   → Calcular `fechaDesde` / `fechaHasta` en `America/Argentina/Buenos_Aires`.
2. **Proyecto Jira destino**: mostrar al PM la lista de proyectos visibles (vía `getVisibleJiraProjects`) y que elija uno. Si tiene muchos, permitir typeahead.
3. **Cliente/cuenta** (opcional): nombre o dominio de email del cliente — sirve para filtrar Gmail y priorizar fuentes. Si no lo dan, se busca más amplio.

**No avanzar** sin las dos primeras respuestas. Son la base del resto del flujo y la consecuencia de equivocarse es cara.

---

### PASO 2 — Recolectar fuentes

Por cada fuente disponible, recolectar contenido del período y cliente indicados. Detalle operativo (queries, CQL, filtros) en `references/source-handlers.md`.

Resumen de cobertura:

| Fuente | Cómo se accede | Si no hay MCP |
|---|---|---|
| Gmail | `search_threads` con filtros `from:` / `to:` / `after:` / `before:` | — |
| Confluence | `searchConfluenceUsingCql` por space + lastmodified en rango | — |
| Google Docs | Se accede si el PM pega el link (no hay MCP nativo hoy) | Pedir links |
| Google Meet | Transcripts en Docs si el meet los generó | Pedir link o paste |
| Read.ai | Sin MCP hoy | Pedir al PM que pegue el resumen o el link público |

**Siempre preguntar al PM al final de esta fase**: "¿Hay alguna fuente adicional que quieras sumar (link a un Doc, paste de un transcript, etc.)?". Un skill que parece "omnisciente" genera falsa confianza — mejor explicitar qué miró y qué no.

**Guardar**, para cada extracto de texto recolectado, su origen (URL o identificador) — se usa en el PASO 4 para anclar cada pending a una fuente verificable.

---

### PASO 3 — Extraer pendings (externos) del texto recolectado

Leer `references/extraction-prompt.md` — contiene el prompt exacto a usar. Los puntos clave:

- Distinguir **externo** (cliente debe hacer X) de **interno** (nosotros debemos hacer Y). Solo los externos avanzan.
- Capturar por pending: `titulo` (imperativo corto, <80 chars), `descripcion` (contexto), `dueno_cliente` (nombre/rol si aparece), `fecha_compromiso` (ISO si existe, null si no), `fuente_url`, `confianza` (`alta` / `media` / `baja`).
- **Detectar señales de postergación**: frases como "lo movemos al…", "lo reprogramamos para…", "en lugar del X va el Y", "se corre a…". Marcarlo como `tipo_cambio: "reschedule"` con la fecha nueva. Esto habilita el update de `duedate` en PASO 5.
- Si la confianza es baja (ej: un "lo vamos a revisar" sin compromiso concreto), **no** lo incluyas — es ruido. Mejor perder cobertura que generar falsos positivos.

El output esperado es un array JSON. Formato exacto en `references/extraction-prompt.md`.

---

### PASO 4 — Buscar issues existentes + deduplicar

Llamar `searchJiraIssuesUsingJql` con:

```
project = "<PROJ>" AND issuetype = "External pending" AND statusCategory != Done
ORDER BY duedate ASC
```

Campos a traer: `summary`, `description`, `duedate`, `status`, `customfield_*` si el proyecto usa custom fields para dueño cliente.

Para cada pending extraído en PASO 3, correr `scripts/dedupe.py` contra los issues existentes. El script hace fuzzy matching por título (token-sort ratio ≥ 80) y devuelve uno de tres veredictos:

- **`new`** → no matchea con ninguno → candidato a crear.
- **`update_date`** → matchea con existente **y** el pending tiene `tipo_cambio: "reschedule"` con fecha nueva → candidato a `editJiraIssue` actualizando solo `duedate` + comentario con la fuente.
- **`duplicate`** → matchea con existente y no hay cambios → ignorar (no hacer nada).

---

### PASO 5 — Revisar con el PM (artifact editable)

Leer `assets/review-artifact-template.html`. Reemplazar el placeholder `__PENDINGS_DATA__` con el JSON del resultado combinado (nuevos + updates de fecha + vencidos — ver PASO 6), y `__PROJECT_KEY__` con el proyecto elegido.

Generar el artifact con `mcp__cowork__create_artifact`. El PM ve una tabla con tres secciones:

1. **Nuevos** (`new`): cada fila editable. Toggle individual para descartar. Campos editables: título, descripción, duedate, dueño.
2. **Updates de fecha** (`update_date`): muestra fecha vieja → fecha nueva. Toggle para confirmar o rechazar.
3. **Vencidos** (detectados aparte, ver PASO 6): lista de issues `External pending` del proyecto con `duedate < hoy` y status abierto.

El PM confirma la selección → el artifact llama de vuelta al skill con el subset aprobado.

**Importante:** no crear/editar nada antes de la confirmación explícita. El artifact es el único mecanismo de aprobación.

---

### PASO 6 — Detectar pendings vencidos y ofrecer follow-up

Antes de renderizar el artifact, calcular los vencidos: en el resultado de PASO 4, filtrar los existentes que tienen `duedate < hoy` y status != Done.

En el artifact (sección "Vencidos") mostrar para cada uno: issue key, título, dueño cliente, fecha comprometida, días de atraso.

Al final, incluir un botón: **"Redactar email de follow-up al cliente"**. Si el PM lo aprieta:

1. Leer `references/followup-email-template.md` → template base.
2. Personalizar con los pendings vencidos seleccionados por el PM (puede tildar un subset).
3. Usar Gmail `create_draft` con el email del cliente como destinatario (el PM completa/ajusta el destinatario si hay más de uno).
4. Notificar al PM: "Draft creado en Gmail — revísalo antes de enviar."

**No enviar automáticamente.** Son comunicaciones al cliente, pasan siempre por el PM.

---

### PASO 7 — Ejecutar crear / update en Jira

Con el subset aprobado desde el artifact:

Para cada pending `new`:
- `createJiraIssue` con `issuetype = "External pending"`, `project = <PROJ>`. Mapeo completo de campos en `references/jira-fields-mapping.md`.
- Incluir en la `description` un link a la fuente (email/doc/confluence) para trazabilidad.
- Reporter = el PM (accountId de PASO 0).

Para cada pending `update_date`:
- `editJiraIssue` sobre el `issueKey` existente, actualizando solo `duedate`.
- `addCommentToJiraIssue` con: "Fecha actualizada desde [fuente] el YYYY-MM-DD. Valor anterior: [old_date]. Valor nuevo: [new_date]."

Hacer las llamadas **una por una** (no en paralelo) para que el PM pueda ver si alguna falla. Al terminar, resumir en chat:
- X pendings creados: lista con links a Jira.
- Y fechas actualizadas: lista con links.
- Z vencidos con draft de email generado (si aplica).

---

## Reglas de negocio / no obvias

- **Un pending externo solo captura lo que el CLIENTE se comprometió**. Si la reunión dice "el cliente nos va a enviar las credenciales" → sí, externo. Si dice "les vamos a mandar la propuesta el viernes" → no, es interno.
- **Tolerancia a ambigüedad**: si no está claro quién se comprometió (ej: "vamos a armar el pipeline"), NO crear el pending. Mejor reportarlo al PM como "pending ambiguo" y que él decida.
- **Postergaciones solo modifican `duedate`**. No cambiar título/descripción a partir de un reschedule — el cliente puede postergar sin cambiar el qué, y reescribir el título pierde la historia.
- **Deduplicación agresiva**: ante duda, marcar como duplicado. Prefiero omitir un pending real que ensuciar el proyecto con copias.
- **Idempotencia**: el skill se puede correr varias veces sobre la misma ventana sin ensuciar Jira — los mismos inputs producen los mismos veredictos (`new` / `update_date` / `duplicate`). Esto implica que el fuzzy matching del dedupe debe ser estable; ver `scripts/dedupe.py`.
- **Multi-cliente en el mismo proyecto**: si el proyecto Jira trackea a varios clientes, no mezclar pendings del cliente A con el proyecto del cliente B. El PM debe correr el skill una vez por cliente (o filtrar en PASO 1 por cuenta).

---

## Ejemplo de conversación esperada

```
PM: quiero armar los externals del cliente Sura de las últimas dos semanas, y pasarlos al proyecto SURA-EXT

Claude: [valida conectores → OK]
        [muestra AskUserQuestion con período + proyecto + cliente]

PM: Últimos 15 días / SURA-EXT / Sura

Claude: [busca en Gmail: threads de la última quincena con *@sura.*]
        [busca en Confluence: páginas del space "Sura" modificadas en rango]
        Encontré 4 threads de Gmail y 2 páginas en Confluence.
        ¿Quieres sumar alguna fuente más? (link a transcript de Meet, resumen de Read.ai, etc.)

PM: Sí, pega este transcript: [pega contenido de una reu de Read.ai]

Claude: [corre extraction-prompt sobre las 3 fuentes]
        Identifiqué 5 pendings externos candidatos + detecté que 1 issue existente
        (SURA-EXT-23) tiene fecha postergada del 15/04 al 29/04.
        Además encontré 2 External pendings vencidos en el proyecto.
        Abro el artifact para que revises.

        [genera artifact con 3 secciones: nuevos / updates / vencidos]

PM: [confirma 4 nuevos + rechaza 1 + aprueba el update de fecha + tilda los 2 vencidos para follow-up]

Claude: [createJiraIssue x4, editJiraIssue x1 + comment, Gmail create_draft con template]
        Listo:
        - Creados: SURA-EXT-47, -48, -49, -50
        - Fecha actualizada: SURA-EXT-23 (15/04 → 29/04)
        - Draft de follow-up generado en Gmail → revísalo antes de enviar.
```

---

## Notas de implementación

- **cloudId Atlassian**: detectar dinámicamente en PASO 0 vía `getAccessibleAtlassianResources`. No hardcodear.
- **Issue type "External pending"**: validar que existe en el proyecto con `getJiraIssueTypeMetaWithFields` antes de crear. Si no existe, detener el flujo y avisar: "El issue type 'External pending' no está disponible en el proyecto [X]. Pídele al admin de Jira que lo habilite."
- **Zona horaria**: trabajar en `America/Argentina/Buenos_Aires` para el input del PM; convertir a UTC al hablar con Atlassian.
- **Fuzzy matching**: `scripts/dedupe.py` usa `rapidfuzz` (fallback a stdlib `difflib` si no está instalado). Umbral por defecto: 80.
- **Idempotencia del dedupe**: mismo input → mismo veredicto. Esto requiere que el orden del JQL sea estable (`ORDER BY created ASC`).

---

## Archivos referenciados

| Archivo | Cuándo leerlo |
|---|---|
| `references/extraction-prompt.md` | Antes del PASO 3 — define el prompt de extracción y el formato de salida. |
| `references/jira-fields-mapping.md` | Antes del PASO 7 — cómo mapear cada campo extraído a campos Jira. |
| `references/source-handlers.md` | En PASO 2 — detalle operativo de cada fuente (queries Gmail, CQL Confluence, etc.). |
| `references/followup-email-template.md` | En PASO 6 — template del email de follow-up. |
| `scripts/dedupe.py` | En PASO 4 — función de fuzzy matching. |
| `assets/review-artifact-template.html` | En PASO 5 — UI de revisión/edición. |
