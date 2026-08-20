---
name: pc-delivery-jira-worklog-tracker
version: 1.0.0
description: Permite cargar horas trabajadas en tickets de Jira directamente desde Claude. Activar cuando el usuario diga "quiero cargar horas", "cargar horas", "registrar horas", "loguear horas", "cargar tiempo", "registrar tiempo trabajado", "cargar worklog", "quiero registrar mis horas", "log hours", "log time", "log my hours in jira", "timesheet", "completar timesheet", "poner mis horas", "poner horas en jira". También activar si el usuario menciona un ticket de Jira junto con una cantidad de tiempo (ej: "cargué 2h en PROJ-123"). Consulta Google Calendar para inferir proyectos trabajados en el período elegido, busca tickets abiertos del usuario en esos proyectos, y renderiza un artefacto interactivo para registrar el tiempo por día.
---

<!-- Changelog
1.0.0 (2026-04-25): Primera versión formal bajo la convención pc-[área]-[sistema]-[objeto]-[acción]. Renombrado desde `jira-worklog` → `pc-delivery-jira-worklog-tracker`. Sin cambios funcionales.
-->

# Skill: Carga de horas en Jira

## Descripción
Permite a cualquier colaborador de ProContacto registrar horas trabajadas en sus tickets de Jira directamente desde Claude. El flujo usa Google Calendar como fuente de verdad para inferir en qué proyectos trabajó el usuario, y luego busca los tickets relevantes en Jira.

---

## Flujo completo paso a paso

### PASO 0 — Validar conectores y resolver identidad del usuario (obligatorio)

Antes de cualquier otra acción:

1. Llamar a `getAccessibleAtlassianResources` → si no devuelve resultados, decirle al usuario:
   > "Para cargar horas necesitas tener el conector de Atlassian activo. Actívalo en Configuración → Conectores."
   → **Fin del flujo.**

2. Llamar a `atlassianUserInfo` → capturar el **email del usuario autenticado** (campo `email`). Este email se usará como `calendarId` en todas las llamadas a Google Calendar. Si falla, usar `primary` como fallback.

3. Llamar a `gcal_list_events` con un rango mínimo (hoy) usando el email del usuario como `calendarId` → si falla, decirle:
   > "Para cargar horas necesitas tener el conector de Google Calendar activo. Actívalo en Configuración → Conectores."
   → **Fin del flujo.**

Si ambos conectores están disponibles → continuar al PASO 1.

---

### PASO 1 — Preguntar el período

Antes de hacer cualquier consulta a Jira o Calendar, preguntarle al usuario de qué período quiere cargar horas.

Usar `ask_user_input` con tipo `single_select` y las siguientes opciones:
- "Hoy"
- "Esta semana (lunes a hoy)"
- "Semana pasada"
- "Elegir fechas"

Si el usuario elige "Elegir fechas", pedirle que ingrese el rango en formato libre (ej: "del 7 al 11 de abril").

Con la respuesta, calcular `fechaDesde` y `fechaHasta` en formato `YYYY-MM-DDTHH:MM:SS` en zona horaria `America/Argentina/Buenos_Aires`.

---

### PASO 2 — Consultar Google Calendar (obligatorio)

Llamar a `gcal_list_events` con:
- `calendarId`: email del usuario obtenido en PASO 0 (o `primary` si no se obtuvo)
- `timeMin`: `fechaDesde`
- `timeMax`: `fechaHasta`
- `timeZone`: `America/Argentina/Buenos_Aires`
- `condenseEventDetails`: `false` (necesitamos ver los attendees para inferir el cliente)

#### Filtrar eventos relevantes

Ignorar automáticamente eventos de estos tipos o con estos patrones en el nombre:
- `eventType: "workingLocation"` → "Casa", "Oficina", etc.
- `eventType: "outOfOffice"` → "Fuera de la oficina"
- `eventType: "focusTime"` → "Armar resumen de tareas", etc.
- Nombres genéricos: "Daily", "Daily Equipo", "1:1", "Jonathan / X", "Organicemos", "Ordenamiento", "KT Agentforce" (o similares sin cliente explícito)

#### Inferir proyectos a partir de los eventos

Para cada evento relevante, inferir el proyecto de Jira usando dos señales combinadas:

**Señal 1 — Nombre del evento:**
Buscar palabras clave en el `summary` del evento que coincidan con nombres de proyecto conocidos. Ejemplos:
- "Tfs" / "Toyota" → `support-tfs` o `tfs-soporte-core`
- "Sura" → `support-sura-1`
- "GCDC" → `support-gcdc`
- "Colombina" → `soporte-calypsocolombia`
- "Andrómaco" / "Andromaco" → `support-andromaco-1`
- "Medical Hair" → buscar en Jira por nombre
- "Bioplastic" → `support-bioplastic`
- "Dipisa" → buscar en Jira por nombre
- "Yamaha" → `support-yamaha-5`
- "TyA" / "Tierra y Armonía" → buscar en Jira por nombre

**Señal 2 — Dominio de los participantes (`attendees`):**
Revisar los emails de los participantes del evento. El dominio del email del organizador o de participantes externos puede identificar al cliente:
- `@tfs.com.mx`, `@toyota*` → Toyota / TFS
- `@colombina.com*` → Colombina
- `@sura*` → Sura
- `@clinicalmarket.cl` → proyecto de integración Salesforce-SAP (buscar por nombre)
- Dominios `@procontacto.com.mx` solos → evento interno, no mapea a cliente externo

Si ambas señales coinciden → usar ese proyecto. Si solo una señal es clara → usarla. Si ninguna señal es clara → ignorar el evento.

**Importante:** Si un evento no matchea ninguna regla pero tiene participantes externos, incluirlo en el PASO 3 con el nombre del evento como etiqueta, para que el usuario decida manualmente.

#### Resultado esperado
Una lista de claves de proyecto Jira inferidas. Ejemplo: `["support-tfs", "tfs-soporte-core", "support-sura-1", "soporte-calypsocolombia"]`

**Si el calendario no tiene eventos en el período:** saltar al PASO 3 directamente, mostrando todos los proyectos del usuario sin preselección.

#### Enriquecer con contexto por reunión (hacer en paralelo con la inferencia de proyectos)

Para cada evento relevante, intentar extraer un `suggestedComment` que pre-llenará el campo comentario en el artefacto:

**a) Notas de Gemini:** Si el evento tiene `attachments` con `mimeType: "application/vnd.google-apps.document"` y título que contiene "Notas", llamar a `google_drive_fetch` con el `fileId`. Si el doc tiene contenido en las secciones "Resumen" o "Próximos pasos", usar ese texto como `suggestedComment` para los tickets del proyecto. Si falla, está vacío, o no tiene permisos → ignorar silenciosamente, sin interrumpir el flujo.

**b) Ticket en el título del evento:** Si el `summary` contiene patrones como `tk 123`, `tk-123`, `PROJ-123`, `#123`, capturar esa referencia. En PASO 5, ese ticket recibirá el título del evento como `suggestedComment` y será marcado visualmente como sugerido.

**c) Descripción del evento:** Si el evento tiene `description` con contenido útil (agenda, puntos tratados), resumirla en 1-2 líneas como `suggestedComment`.

---

### PASO 3 — Preguntar en qué proyectos cargar

Se pregunta en cuáles proyectos cargar para evitar mostrar decenas de tickets irrelevantes — el usuario puede tener tickets en muchos proyectos pero solo trabajó en algunos esta semana.

Mostrarle al usuario los proyectos inferidos del calendario y preguntar en cuáles quiere cargar horas.

Usar `ask_user_input` con tipo `multi_select`. Marcar con 📅 los proyectos que tienen eventos en el calendario del período seleccionado.

Si el usuario quiere cargar horas en un proyecto que no apareció en el calendario, puede seleccionar "Mostrar todos mis proyectos" (incluir esta opción al final de la lista).

---

### PASO 4 — Buscar tickets en Jira

Con los proyectos seleccionados, llamar a `searchJiraIssuesUsingJql` con:
- `cloudId`: `d041f87a-4f5e-40d1-b719-578536318f6a`
- JQL: `assignee = currentUser() AND project in (PROJ1, PROJ2, ...) AND updated >= "YYYY-MM-DD" AND statusCategory != Done ORDER BY updated DESC`
  - Usar las claves de proyecto seleccionadas
  - Usar `fechaDesde` como fecha de corte de `updated`
- `fields`: `["summary", "status", "project", "updated", "timespent", "aggregatetimespent"]`
- `maxResults`: 50

Si no hay tickets → decirle al usuario y ofrecer buscar sin filtro de fecha o con otro criterio.

Si hay más de 30 tickets → preguntar al usuario el orden de prioridad y tomar los primeros 30.

---

### PASO 5 — Renderizar el artefacto

Leer el archivo completo `assets/worklog-artifact.jsx`.

En el JSX descargado, reemplazar los valores de estas dos constantes al inicio del archivo:
- `const CURRENT_USER_EMAIL = "usuario@procontacto.com.mx"` → poner el email real del usuario (obtenido en PASO 0)
- `const INITIAL_TICKETS = []` → poner el array de tickets reales en el formato especificado abajo

Formato de cada ticket en `INITIAL_TICKETS`:
```js
{
  key: "PROJ-123",         // clave del ticket
  id: "10000",             // id numérico
  project: "nombre-proyecto",
  title: "Resumen del ticket",
  status: "Nombre del estado",
  statusType: "done" | "progress" | "waiting" | "default",
  updated: "7 abr 2026",   // fecha legible
  timespent: 7200,         // segundos totales ya cargados (null → 0)
  suggestedComment: "..."  // opcional — pre-llena el campo comentario (de Notas Gemini, descripción del evento, o título)
}
```

**Mapeo de statusType:**
- `done` → status contiene: "resuelto", "done", "closed", "listo"
- `progress` → status contiene: "curso", "progress", "doing", "working"
- `waiting` → status contiene: "espera", "waiting", "hold", "blocked", "pendiente"
- `default` → cualquier otro

Luego:
1. Guardar el resultado en `/mnt/user-data/outputs/jira_worklog.jsx` con `create_file`
2. Presentar con `present_files`

**NO usar `show_widget` para este artefacto. NO reescribir el JSX desde cero.**

---

### PASO 6 — El artefacto opera de forma autónoma

El artefacto llama directamente a la API de Anthropic con el MCP de Atlassian — no necesita enviar mensajes de vuelta a Claude para registrar horas. El flujo es completamente interno al artefacto:

1. Usuario completa horas + comentario → confirma en el modal
2. El artefacto llama `logWorkToJira()` → POST a `api.anthropic.com/v1/messages` con `mcp_servers: atlassian`
3. El spinner y los toasts dan feedback visual sin interrumpir el chat

Claude solo interviene si el usuario escribe en el chat durante esta etapa (ej: "agrega el ticket SP-900"). En ese caso, re-ejecutar el JQL del PASO 4 y actualizar `INITIAL_TICKETS` en un nuevo artefacto.

---

## Notas de implementación

- **cloudId Atlassian**: `d041f87a-4f5e-40d1-b719-578536318f6a` (constante de la org ProContacto)
- **Calendario / usuario**: Detectado dinámicamente via `atlassianUserInfo` en PASO 0
- **Zona horaria worklogs**: Registrar siempre en UTC. Convertir fechas locales antes del API call.
- **Formato de tiempo**: Aceptar `2h`, `1h 30m`, `90m`, `1.5` (decimales = horas). Convertir a `Xh Ym`.
- **Permisos**: Solo tickets de `currentUser()`. Claude nunca accede a tickets de otros usuarios.

---

## Ejemplo de conversación esperada

```
Usuario: quiero cargar horas

Claude: [valida conectores OK]
        [obtiene email via atlassianUserInfo]
        ¿De qué período quieres cargar horas?
        [opciones: Hoy / Esta semana / Semana pasada / Elegir fechas]

Usuario: Esta semana

Claude: [consulta Google Calendar lunes-hoy con el email del usuario]
        [infiere proyectos: TFS, Colombina, Sura, Medical Hair]
        Encontré reuniones de estos proyectos esta semana.
        ¿En cuáles quieres cargar horas?
        [opciones: 📅 support-tfs / 📅 tfs-soporte-core / 📅 soporte-calypsocolombia / 📅 support-sura-1 / Mostrar todos mis proyectos]

Usuario: [selecciona support-tfs y soporte-calypsocolombia]

Claude: [busca tickets con JQL filtrado por proyecto y updated >= lunes]
        [lee assets/worklog-artifact.jsx, inyecta tickets y email, genera el archivo]
        [presenta con present_files]

Usuario: [en el artefacto carga 2h el martes en TFS-456]
         → sendPrompt: "Cargar 2h en TFS-456 el 2026-04-08 con comentario: 'Revisión de integración'"

Claude: [llama a addWorklogToJiraIssue silenciosamente]
```
