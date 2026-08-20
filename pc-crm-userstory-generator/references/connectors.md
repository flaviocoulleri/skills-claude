# Connector Integration — Plumbing concreto

Este doc complementa la sección `## Connector Integration` del SKILL.md. Acá viven los detalles de qué tool MCP usar para cada operación, qué parámetros pasar, qué devuelve, y los gotchas que se ven recién al tirar la primera llamada.

**Regla general antes de usar cualquier conector**: si el conector no está autenticado, **no lo uses** — caé al modo offline y avisa al usuario. No improvisar fallbacks que escriban en sistemas equivocados.

---

## 1. Lectura de épica desde Jira

Caso típico: el usuario dice "haz las HUs de la épica PROJ-123" o pega la URL `https://procontacto.atlassian.net/browse/PROJ-123`.

**Tool**: `getJiraIssue`

**Parámetros clave**:
- `issueIdOrKey`: la key (ej. `PROJ-123`). Si te pasaron URL, parsea la key después de `/browse/`.
- `cloudId`: lo obtienes una sola vez con `getAccessibleAtlassianResources` y lo cacheas durante la sesión.

**Qué extraer del response**:
- `fields.summary` → contexto del título de la épica.
- `fields.description` (ADF) → cuerpo de la épica, parsealo a markdown plano antes de razonar sobre él.
- `fields.issuetype.name` → confirmar que es `Epic`. Si no lo es, avisa al usuario antes de seguir.
- `fields.status.name` → si está en `Done` o `Cancelled`, preguntar si igual se quieren generar las HUs.
- `fields.labels` → señales de módulo/área.

**Gotchas**:
- La descripción Jira viene en formato ADF (Atlassian Document Format), no en markdown plano. Hay que recorrer el árbol `content[].content[].text` para extraer texto. No pegues el JSON crudo en la HU.
- Si la épica tiene HUs hijas existentes (`getJiraIssue` no las trae), corre `searchJiraIssuesUsingJql` con `jql='"Epic Link" = PROJ-123'` para detectar dups antes de crear nuevas.

---

## 2. Lectura de page de Confluence

Caso típico: "el contexto está en https://procontacto.atlassian.net/wiki/.../12345" o "busca la page que se llama 'Épica Onboarding Cliente X'".

**Tools**:
1. `searchConfluenceUsingCql` con `cql='title = "Épica Onboarding Cliente X" AND space = "PROJ"'` para encontrar el `pageId`.
2. `getConfluencePage` con `pageId` para traer el contenido.

**Qué extraer**:
- `body.storage.value` → HTML de la page. Convertilo a markdown limpio antes de usarlo.
- Tablas embebidas → si hay tablas con campos/AC, parsea la tabla con cuidado (no asumas estructura — confirmar con el usuario).
- Links a otras pages → si la page referencia un DDD o un Figma, suma esos a la cola de lectura.

**Gotchas**:
- Confluence pages traen `<ac:link>` y `<ac:inline-comment-marker>` que ensucian el texto. Fíltralos.
- Si la page tiene >50KB de HTML, léela y resúmela en lugar de pegarla entera al razonamiento.

---

## 3. Lectura de archivos Drive (DDD, PPT, transcripts Read.ai)

Caso típico: "el DDD está en Drive bajo el cliente X" o "levanta el transcript del meeting de ayer con el cliente".

**Flow**:
1. `search_files` con query tipo `name contains 'DDD' and '<folderId-cliente>' in parents` o por mimeType (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` para xlsx).
2. `get_file_metadata` para confirmar fileId, lastModifiedTime, owner.
3. `read_file_content` (texto plano) o `download_file_content` (binario, ej. xlsx → procesarlo en bash con la skill `xlsx`).

**Tipos de archivo y qué hacer con cada uno**:
- **xlsx (DDD)**: descargar y abrir con la skill `xlsx`. No intentes parsearlo como texto plano.
- **pptx (reglas de negocio)**: descargar y usar la skill `pptx` para extraer texto de cada slide.
- **txt / Google Doc (transcript Read.ai)**: `read_file_content` directo; los transcripts traen timestamps `[00:12:34]` que conviene preservar para citar al cliente.
- **pdf (SOW)**: descargar y usar la skill `pdf` para extraer texto.

**Gotchas**:
- Read.ai genera dos formatos: el "summary" (corto, útil para contexto) y el "transcript" (largo, útil para citar literal). Si ambos existen, lee summary primero y solo pasa al transcript si necesitas precisión literal.
- El owner de un archivo no siempre es ProContacto; si el archivo es del cliente, no escribas sobre él.

---

## 4. Calendar y Gmail (minutas + threads)

Caso típico: "el contexto está en la reunión que tuvimos ayer" o "la épica salió del thread con `cliente@ejemplo.com`".

**Calendar**:
- `list_events` con rango de fecha + filtro por `q='<nombre del cliente>'`.
- `get_event` con el `eventId` para traer descripción, attendees, attachments y conferenceData (link Meet).

**Gmail**:
- `search_threads` con query `from:cliente@ejemplo.com subject:"épica"` o `after:2026-04-01 from:cliente.com`.
- `get_thread` con el `threadId`.

**Qué extraer**:
- Calendar: si el evento tiene `attachments[].fileUrl` apuntando a Drive, súmalo a los inputs Drive.
- Gmail: cuerpo del último mensaje + cuerpo del primero. El medio suele ser ruido.

**Gotchas**:
- Calendar `list_events` tira sólo eventos del calendario primario por default. Si el meeting está en un calendario compartido del proyecto, lístalo explícito.
- Gmail no devuelve adjuntos en `get_thread` por default — sólo metadata. Para descargar adjunto hace falta otra call (no implementada en este skill; pide al usuario que lo suba si es crítico).

---

## 5. Persistencia en Drive (carpeta del proyecto)

El output de las HUs no se persiste en Jira — se escribe como **Google Doc** dentro de la carpeta Drive del proyecto. La razón: las HUs salen de este skill en estado **draft de analista funcional** y el ciclo siguiente (review con dev/admin SF, validación con cliente, eventual carga a Jira) lo decide el PM. Persistir directo a Jira atajaría ese review y crearía issues prematuros.

### 5.1 Localizar la carpeta del proyecto

Dos vías, en orden de preferencia:

1. **Vía Salesforce `Project_Asset__c`** (cuando el usuario te da el `Project__c` o el código del proyecto). El proyecto tiene un asset tipo `Drive Folder` con la URL de la carpeta. Pídele al usuario el código del proyecto y resuelve la carpeta desde ahí. Ver memoria `project_asset_schema.md` para el schema del asset.
2. **Vía búsqueda directa en Drive**: `search_files` con query tipo `mimeType = 'application/vnd.google-apps.folder' and name contains '<cliente>' and trashed = false`. Si hay más de un match, muestra los candidatos al usuario y que elija.

Si no encuentras carpeta, **detén el flow** y pídele al usuario que cree el `Project_Asset__c` o que te pase el folderId de Drive a mano. No improvises creando carpetas nuevas — ese es scope de `pc-sales-sf-account-builder` u otro skill de delivery, no de éste.

### 5.2 Estructura del Doc

Un único Google Doc por sesión (o por épica), con esta estructura:

```
Título: HUs — [Épica / Requerimiento] — [YYYY-MM-DD]

Sección por HU, en orden:
  H1: [Módulo] | [Nombre HU]
  Descripción (Como/Quiero/Para)
  Criterios de Aceptación
  Escenarios (Gherkin)
  Evaluación Funcional y Técnica
  Tareas Sugeridas
  Anexo (si aplica)
  ───────────────────────────  (separador entre HUs)

Pie del doc:
  - Fecha de generación
  - Inputs usados (links a Jira épica, Confluence pages, transcripts Drive, etc.)
  - Versión del skill (pc-crm-userstory-generator vX.Y.Z)
```

### 5.3 Tool y flow

**Tool primario**: `create_file` (del conector Drive) con:
- `name`: `HUs - <Épica> - <YYYY-MM-DD>.gdoc` (o `.md` si el usuario prefiere markdown — pregunta una vez al inicio).
- `parents`: `[<folderId del proyecto>]`.
- `mimeType`: `application/vnd.google-apps.document` para Doc nativo, o `text/markdown` para .md.
- `content`: el cuerpo armado según 5.2.

**Antes del create**: preview en chat del título del doc, la carpeta destino (con nombre + URL), y un índice de las HUs que va a contener. Espera "sí" literal.

**Después del create**:
- Guarda el `fileId` y `webViewLink` que devuelve.
- Muestra al usuario el link `https://docs.google.com/document/d/<fileId>` para abrirlo de una.
- Si el usuario quiere, opcionalmente registra el doc como `Project_Asset__c` tipo `User Stories Draft` en Salesforce (no es default — pregunta).

### 5.4 Re-runs y versionado

Si el usuario corre el skill por segunda vez sobre la misma épica, **no sobreescribir** el doc anterior. Crear uno nuevo con sufijo de versión (`HUs - <Épica> - 2026-05-07 - v2.gdoc`) y mencionar al usuario que el anterior queda archivado por si quieres diff manual. Sobreescribir doc de cliente sin doble confirmación rompe trazabilidad — esa regla es estricta.

### 5.5 Gotchas

- `create_file` con `mimeType: application/vnd.google-apps.document` ignora el contenido binario y espera texto plano. Para formato más rico (tablas, headings) hay que crear el doc primero y después editar con la API de Docs (no expuesta directo en el MCP actual; si necesitas formato fuerte, usa .md).
- El `parents` array es **literal** — pasa el folderId, no el nombre. Si te confundes y pasas el nombre, el doc se crea en "My Drive" y nadie lo encuentra.
- Si la carpeta del proyecto tiene permisos restringidos (sólo el cliente), el doc nuevo hereda esos permisos. Confirmar con el PM que el destinatario correcto es la carpeta interna de PC, no la compartida con el cliente — no quieres que un draft de analista termine visible al cliente sin review.
- No creas el doc con tu owner — el doc queda owneado por la cuenta de quien autenticó el conector (el usuario). Eso está bien; no intentes cambiar ownership.

---

## 6. Notificación Slack al equipo (opcional)

Caso típico: "avísale al PM que ya están las HUs" o "mándale un DM al admin SF con el link del doc".

**Tool**: `slack_send_message_draft` (siempre draft, nunca `slack_send_message` directo).

**Flow**:
1. `slack_search_users` con el nombre o email del destinatario para resolver el `userId`.
2. `slack_send_message_draft` con el `userId` y un mensaje tipo:

   > Listas las HUs de la épica *Onboarding Cliente X* (3 HUs en draft). Quedaron en Drive: <link al doc>. Cualquier ajuste me avisas.

3. Mostrar el draft en chat al usuario y esperar "sí, mándalo" antes de enviar el draft real.

**Gotchas**:
- `slack_send_message_draft` arma un draft pero no manda — tiene que aprobarlo el usuario en la UI de Slack o que tú llames a `slack_send_message` después de la confirmación. Documenta esto al usuario para que sepa dónde mirar.
- Si el destinatario es un canal externo del cliente (`Slack Channel External` en `Project_Asset__c`), regla extra: nunca enviar sin doble confirmación. Mejor pedirle al PM que copie el mensaje a mano.

---

## 7. Handoff a skills hermanos

Si el usuario aceptó persistir las HUs y el anexo DDD trae fields nuevos, haz un handoff a `pc-crm-salesforce-data-dictionary-generator` para que el DDD del proyecto quede sincronizado:

> "Las HUs introducen 4 fields nuevos sobre Case y 1 sobre Contact. ¿Quieres que pase el control a `pc-crm-salesforce-data-dictionary-generator` para actualizar el DDD?"

Si dice sí, abandona el contexto del story-writing y déjale el control al otro skill — no intentes hacer la actualización tú mismo, porque ese skill conoce reglas (naming SF, picklist values, FLS) que tú no.

Mismo patrón para `pc-crm-salesforce-flow-builder` si las HUs implican Flows nuevos: pásale el control para que arme nombres bajo la convención.

---

## Tabla rápida — qué tool para qué

| Operación | Tool | Origen/Destino |
|---|---|---|
| Leer épica | `getJiraIssue` | Jira |
| Buscar HUs hijas existentes | `searchJiraIssuesUsingJql` | Jira |
| Leer page de épica | `searchConfluenceUsingCql` + `getConfluencePage` | Confluence |
| Buscar archivo | `search_files` | Drive |
| Leer contenido txt/doc | `read_file_content` | Drive |
| Descargar binario (xlsx/pptx/pdf) | `download_file_content` | Drive |
| Leer evento | `get_event` | Calendar |
| Buscar thread | `search_threads` + `get_thread` | Gmail |
| **Persistir HUs como Doc** | `create_file` (Drive) | Drive (carpeta del proyecto) |
| Resolver Slack user | `slack_search_users` | Slack |
| Mandar DM (draft) | `slack_send_message_draft` | Slack |

---

## Modo dry-run

Para todas las operaciones de **escritura** (`create_file` en Drive, `slack_send_message_draft`, `createConfluencePage`), el default es **dry-run**:

1. Mostrar al usuario en chat exactamente qué se va a crear/modificar (preview).
2. Esperar confirmación literal.
3. Recién después, ejecutar.

Esto es coherente con la regla bloqueante del SKILL.md: el skill nunca persiste sin confirmación explícita. Una autorización ("sí, crea todas") sólo aplica al batch que se acaba de previsualizar; un nuevo batch requiere nueva confirmación.
