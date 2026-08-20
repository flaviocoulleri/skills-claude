# Recetas de validación por conector (lazy)

Queries canónicas para los modos B, C y D. Regla general: **Jira primero, después llamadas dirigidas**. Total típico de un modo C: 5–8 llamadas. Si un conector no está disponible, degradar el ítem a "⬜ verificar manualmente" y seguir.

## §1 — Resolver el proyecto (modo B, siempre primero)

1. Identificar el proyecto Jira por el nombre que da el PM (si maneja varios y es ambiguo, preguntar — no listar todos los proyectos del sitio).
2. Traer los **Artefactos** del proyecto:

```jql
project = "<KEY>" AND issuetype = "Artifact"
```

- Si el issuetype "Artifact" no existe en el proyecto (verificar con `getJiraProjectIssueTypesMetadata` si la JQL falla), avisar: *"El proyecto no tiene issue type 'Artifact'"* — y pedir los links al PM.
- El link de cada Artifact vive en **`customfield_10158` (Page Link, tipo url)** y su tipo en **`customfield_10263` (Artifact Type, select)** — valores = los entregables del Blueprint (SOW Comercial, User Story Mapping, Diccionario de Datos, etc.). Confirmado por introspección; ver `_shared/jira/fields-by-issuetype.md`. Fallback: si el id difiere en el sitio, descubrirlo con `getJiraIssueTypeMetaWithFields` para "Artifact" (field tipo `url`). Cachear para la sesión.
3. De los Artefactos salen: carpeta Drive del proyecto, links de Claude Design, espacio Confluence, canal Slack, etc.

## §2 — Inferir fase (modo B)

Con 1–2 llamadas más, no exhaustivo:
- Épicas/sprints del board: ¿hay sprint activo? ¿HUs con criterios cargados? → indica F2 tardía o F3.
- Artefactos presentes: solo SOW comercial → F1/F2 temprana; Acta de Scope Freeze → F3+; Plan de UAT en ejecución → F4.
- Lo que cuente el PM pesa más que la inferencia: confirmar con él antes de asumir.

## §3 — Verificaciones por ítem de checklist (modo C)

Buscar **solo** los ítems del gate consultado. Recetas por tipo de evidencia:

| Evidencia | Conector | Receta |
|---|---|---|
| Documento entregable (SOW, actas, planes, diccionario, matriz) | Drive | `search_files` con `parentId = '<carpeta del proyecto>'` (de §1) y `title contains '<término>'`. Términos: "SOW", "Acta", "Scope Freeze", "UAT", "RACI", "RAID", "Diccionario", "Matriz". Sin carpeta conocida: `fullText contains '<cliente>' and title contains '<término>'` |
| Wireframes / prototipo | Drive + Artefactos | Link del artefacto de Cowork (`claude.ai/code/artifact/<uuid>`) registrado como Artefacto, o export en la carpeta Drive |
| Backlog de HUs con criterios | Jira | `project = "<KEY>" AND issuetype in (Story, "Historia")` — muestrear 5–10 y revisar que description tenga criterios Gherkin (DADO/CUANDO/ENTONCES). No traer todas las HUs completas |
| Piloto AI-ready (2–3 HUs en sandbox) | Jira | HUs con label/comentario de piloto en estado Done — si no hay convención visible, preguntar al PM |
| Sesiones/talleres/kickoff/demos | Calendar | `list_events` acotado al rango de fechas de la fase, filtrando por nombre del cliente/proyecto |
| Minutas de sesiones | ReadAI | `list_meetings` en el rango; verificar existencia y fecha — no citar contenido textual |
| Aprobaciones / feedback del cliente | Gmail | `search_threads` con nombre del cliente + término del entregable, rango de fechas acotado |
| Firmas de documentos | Drive | Versión firmada en la carpeta (título con "firmado"/"signed") — si no, ⬜ manual |
| CRs post-freeze | Jira + Drive | Issues tipo cambio/CR en el board + órdenes de cambio en la carpeta |
| Contexto comercial (SOW monto, AE, etapa) | Salesforce | `soqlQuery` sobre Opportunity/`Project__c` — solo si la consulta lo requiere |

**Anti-patrones:** no hacer full-text search global de Drive sin acotar carpeta o cliente; no traer más de ~20 resultados por llamada; no consultar un conector para un ítem que el checklist marca "Manual".

## §4 — Detección y vinculación de Artefactos (modo D)

1. Listar la carpeta Drive del proyecto (`search_files` con `parentId`) — 1 llamada, paginar solo si hace falta.
2. Clasificar los documentos relevantes por título: SOW, propuesta, actas, planes, diccionario, matriz, backlog. Ignorar archivos de trabajo (borradores, copias, temporales).
3. Detectar links de Claude Design mencionados por el PM o registrados en docs/Artefactos (`claude.ai/design/p/<uuid>`).
4. Diff contra los Artefactos de §1 (comparar por URL normalizada; si el Artefacto apunta al mismo fileId de Drive, es el mismo documento).
5. Draft por faltante: `summary` = "<Tipo de documento> — <nombre>", issuetype "Artifact", URL en el custom field descubierto en §1.
6. **Crear solo tras confirmación explícita del PM** sobre la lista de drafts. Reportar creados con link al issue.
