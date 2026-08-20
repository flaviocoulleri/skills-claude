---
name: pc-meta-briefing-generator
version: 1.1.0
description: Genera el briefing diario del usuario como un Claude artifact (React/JSX). Recopila datos de Google Calendar (obligatorio), Gmail, Slack, Jira y ReadAI (opcionales), construye el objeto BRIEFING_DATA, y presenta el artefacto con el layout ProContacto.
---

<!-- Changelog
1.0.0 (2026-04-25): Primera versión formal bajo la convención pc-[área]-[sistema]-[objeto]-[acción]. Renombrado desde `morning-briefing` → `pc-meta-briefing-generator`. Sin cambios funcionales.
-->

# Morning Briefing

Generas el briefing del día como un Claude artifact visual con datos reales del usuario.

Sigue exactamente estos pasos en orden.

---

## PASO 0 — Validar conectores (obligatorio, solo validación — sin recopilar datos todavía)

Este paso verifica qué conectores están activos. **No recopiles datos aún.** Solo confirma disponibilidad con llamadas mínimas.

Ejecuta todas las validaciones **en paralelo**:

### 1. Atlassian (opcional)
Llama a `getAccessibleAtlassianResources`.
- Si falla o no está configurado: Jira queda deshabilitado. Marca `jira: false`. Continúa sin esa sección.
- Si responde: Jira habilitado. Usa el `cloudId` hardcodeado de ProContacto: `d041f87a-4f5e-40d1-b719-578536318f6a`.

### 2. Atlassian User Info
Llama a `atlassianUserInfo`.
- Si responde: captura el campo `email`. Usarlo como `calendarId` en las llamadas a Google Calendar.
- Si falla: usar `calendarId: "primary"` como fallback.

### 3. Google Calendar (obligatorio)
Llama a `gcal_list_events` con `calendarId` del paso anterior, rango mínimo (hoy 00:00–01:00 local) solo para verificar disponibilidad.
- Si falla o no está configurado:
  > "Para el morning briefing necesitas el conector de Google Calendar activo. Actívalo en Configuración → Conectores."
  → **Fin del flujo.** No continuar sin Calendar.
- Si responde: Calendar habilitado. Marca `calendar: true`.

### 4. Gmail (opcional)
Llama a `search_threads` con query `newer_than:1h` como verificación mínima.
- Si falla: marca `gmail: false`. Omitir sección emails silenciosamente.
- Si responde: marca `gmail: true`.

### 5. Slack (opcional)
Llama a `slack_search_public_and_private` con query `from:me after:yesterday` como verificación mínima.
- Si falla: marca `slack: false`. Omitir sección Slack silenciosamente.
- Si responde: marca `slack: true`.

### 6. ReadAI (opcional)
Llama a `list_meetings` sin parámetros (o con limit=1) como verificación mínima.
- Si falla: marca `readai: false`. Omitir silenciosamente.
- Si responde: marca `readai: true`. Usarlo en PASO 1 para enriquecer los briefs de reuniones del día anterior.

### Resultado esperado del PASO 0
Un mapa de conectores activos, por ejemplo:
```
calendar: true | atlassian: true | gmail: true | slack: true | readai: false
cloudId: "d041f87a-4f5e-40d1-b719-578536318f6a"
calendarId: "jonathan.leiva@procontacto.com.mx"
```

---

## PASO 1 — Recopilar datos (en paralelo, usando solo los conectores activos)

### Google Calendar (obligatorio)
- `gcal_list_events` con:
  - `calendarId`: email del usuario (de PASO 0)
  - `timeMin` = hoy 00:00 local, `timeMax` = hoy 23:59 local
  - `condenseEventDetails: false` — necesitas attendees y description completos
- Filtrar eventos sin valor: `workingLocation`, `outOfOffice`, `focusTime`, título genérico "Daily"
- Para cada evento relevante, intentar enriquecer el `brief` con las siguientes fuentes (en orden de prioridad):

  **a) ReadAI** (si `readai: true`): Llama a `list_meetings` y busca una reunión que coincida con el título del evento del día anterior o de hoy. Si encuentras match, llama a `get_meeting_by_id` para obtener el resumen. Usa ese texto como base del `brief`.

  **b) Notas de Gemini (Google Drive)**: Si el evento tiene `attachments` con `mimeType: "application/vnd.google-apps.document"` y título que contiene "Notas", llama a `google_drive_fetch` con el `fileId`. Si el doc tiene contenido útil (secciones "Resumen", "Próximos pasos", "Action items"), úsalo como `brief`. Si falla o está vacío → continuar sin interrumpir el flujo.

  **c) Descripción del evento**: Si el evento tiene `description` con contenido útil (agenda, puntos a tratar, links de contexto), resumirla en 1-2 líneas para el `brief`.

  **d) Email relacionado**: Si el título del evento menciona un cliente y Gmail está activo, busca threads recientes (`search_threads` con el nombre del cliente) y extrae contexto relevante.

### Gmail (si `gmail: true`)
- `search_threads` con query `newer_than:1d is:unread OR newer_than:1d is:important`
- Identificar: action items, preguntas dirigidas al usuario, deadlines mencionados
- Ignorar: newsletters, notificaciones automáticas (noreply@, no-reply@), correos de sistema, Jira notifications que no son asignaciones directas

### Slack (si `slack: true`)
- `slack_search_public_and_private` con query `to:<@USERID> after:yesterday` para menciones directas
- Identificar: DMs no leídos, threads que esperan respuesta del usuario
- NO incluir mensajes enviados por el usuario mismo

### Jira (si `atlassian: true`)
- `searchJiraIssuesUsingJql` con:
  - `cloudId`: `d041f87a-4f5e-40d1-b719-578536318f6a`
  - JQL principal: `assignee = currentUser() AND statusCategory != Done ORDER BY priority DESC`
  - Fields: `summary`, `status`, `priority`, `project`, `updated`, `timespent`
  - `maxResults`: 50
- JQL adicional por reunión con cliente (si hay reuniones hoy con externos): `assignee = currentUser() AND project = "<proyecto inferido>" AND statusCategory != Done`

---

## PASO 2 — Construir el objeto BRIEFING_DATA

Con todos los datos recopilados, construye el siguiente objeto JavaScript. **Escribe en español.**

```js
const BRIEFING_DATA = {
  date: "<día de la semana>, <dd> de <mes> de <año>",   // ej: "Lunes, 14 de abril de 2026"
  focus: "<foco del día — inferido por ti basado en los datos>",

  summary: [
    // 2-4 bullets ejecutivos. Lo más importante del día, ordenados por urgencia.
    // Incluir: reuniones críticas, issues bloqueados, emails con deadline hoy.
  ],

  tasks: [
    {
      id: "t1",                    // string único, usar "t1", "t2", etc.
      text: "<texto de la tarea>", // conciso, accionable
      urgent: true,                // true si: deadline hoy, bloqueado, reunión en <2h sin prep
      done: false,                 // siempre false al generar
      origin: "email",             // "email" | "calendar" | "slack" | "jira" | "manual"
      why: "<1-2 oraciones: por qué importa y qué hay que hacer exactamente>",
    },
    // Ordenar: urgentes primero, luego por impacto
    // NO incluir tareas delegadas al equipo
    // NO duplicar tareas ya existentes si el usuario las mencionó
  ],

  calendar: [
    {
      time: "09:00",              // hora local HH:MM
      title: "<título del evento>",
      brief: "<resumen de 1-3 líneas: contexto de la reunión, issues Jira relacionados, puntos pendientes>",
                                  // Fuente: ReadAI > Gemini Notes > descripción evento > email relacionado > null
      link: "<URL de meet/zoom o null>",
    },
    // Filtrar: workingLocation, outOfOffice, focusTime, "Daily" genérico
  ],

  emails: [
    {
      from: "<remitente>",
      subject: "<asunto del email>",
      actionItem: "<qué hay que hacer — 1 línea>",
      urgency: "high",            // "high" si tiene deadline hoy o es crítico | "normal"
    },
    // Incluir solo emails que requieren acción. Ignorar FYIs, newsletters, notificaciones.
  ],

  slack: [
    {
      type: "mention",            // "mention" | "dm" | "thread"
      from: "@username",
      channel: "#canal",          // null si es DM
      summary: "<de qué trata en 1 línea>",
      needsReply: true,           // true si requiere respuesta del usuario
    },
  ],

  jira: {
    totalActive: 0,               // total de issues asignados y no cerrados
    highPriority: 0,              // issues con prioridad High o Highest
    updatedYesterday: [
      {
        key: "PRJ-123",
        summary: "<resumen del issue>",
        status: "<status en Jira>",
        statusType: "progress",   // "progress" | "done" | "waiting" | "default"
      },
    ],
    byMeeting: {
      "<Nombre reunión HH:MM>": [
        { key: "PRJ-123", summary: "<resumen>", status: "<status>", statusType: "progress" },
      ],
    },
  },
};
```

### Reglas de contenido
- Escribir todo en español (excepto keys técnicas como status de Jira)
- Las tareas urgentes (`urgent: true`) se detectan de: emails con deadline hoy, issues bloqueados, prep de reuniones en menos de 2h
- Si un conector no estaba disponible (según PASO 0): la sección correspondiente queda con array vacío `[]` o `null` para jira. Nunca inventar datos.
- El campo `calendar[].brief` es la pieza más valiosa del briefing. Prioriza enriquecerlo con datos reales (ReadAI → Gemini → descripción → email). Si no hay ninguna fuente disponible, usar `null` en lugar de inventar.
- No crear tareas de trabajo que ya fue delegado al equipo
- El campo `focus` debe ser una frase accionable, no genérica ("Día normal" no sirve)

---

## PASO 3 — Renderizar el artefacto

1. Lee el archivo `assets/morning-briefing-artifact.jsx` completo.

2. Localiza esta línea cerca del inicio del archivo:
   ```js
   const BRIEFING_DATA = {};
   ```
   (puede que tenga un comentario arriba: `// REEMPLAZAR con los datos del briefing generados por la skill`)

3. Reemplaza **solo esa constante** con el objeto construido en PASO 2. No toques ninguna otra parte del JSX.

4. Presenta el artefacto con `present_files`.

**IMPORTANTE:**
- NO reescribir el JSX desde cero
- NO usar `show_widget`
- NO modificar ningún componente React del archivo
- Solo reemplazar el valor de `BRIEFING_DATA`

## Publicación en el gestor (regla dura)

**Todo entregable de este skill se publica en el gestor de artefactos de ProContacto — nunca como
artefacto de la conversación, y nunca solamente como archivo.** Lee
`_shared/artifact-publish/artifact-publish.md` y aplicá su procedimiento completo. Tres partes que no
son opcionales:

1. **Gate del conector, antes de construir.** Una llamada a `listar_artefactos` comprueba que el
   gestor responde. Si no está disponible, **el skill se detiene y le pide a la persona que lo
   active**: no construye "por las dudas", no deja el entregable en la conversación y no ofrece
   mandar el archivo en su lugar.
2. **Anti-duplicado de dos pasos.** `listar_artefactos` por título canónico
   `{Cliente} · {Entregable} · {Tipo}` (sin versión ni fecha) → `publicar_version` sobre la misma URL
   si ya existía, `publicar_artefacto` si no. Anotá el `id` y dejalo en el trace del HTML.
3. **El link va escrito en el chat.** Publicar sin mostrar el link es no publicar.

El briefing se materializa como **HTML autocontenido** (no como componente React suelto) y se publica. Título canónico por persona, no por día: cada briefing es una **versión nueva sobre la misma URL**, para que el gestor no se llene de uno por jornada y la persona tenga siempre el mismo link.

**Exportar exige haber publicado.** Cualquier formato (`.docx`, `.xlsx`, `.pdf`, `.pptx`, texto) se
ofrece en el chat **después** de que el artefacto existe, y sale del mismo original. Que la persona
pida un formato no es permiso para saltear la publicación.
