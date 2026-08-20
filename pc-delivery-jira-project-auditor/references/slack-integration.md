# Integración con Slack — detalle

Slack entra al skill como **destino** (drafts de DM al equipo) y como **fuente** (análisis de canales para descubrir gaps con Jira). Las integraciones son aditivas — si Slack MCP no está conectado, todas las features de esta sección se omiten silenciosamente del widget de PASO 2 y el resto del skill sigue funcionando.

## Detección del canal interno del proyecto

Antes de cualquier feature de Slack, el skill necesita conocer el canal interno del proyecto:

1. Buscar en `Project_Asset__c` (Salesforce) el asset tipo `Slack channel internal` con `Value__c` = canal id o nombre.
2. Si no existe, hacer `slack_search_channels` con el `Project__c.Name` + variantes (`#proyecto-<name>`, `#<account>-<name>`, etc.) y proponer el match al PM como widget. El PM confirma o descarta.
3. Si tampoco hay match razonable, omitir las features de Slack para este audit y dejar nota en el widget: "Sin canal interno detectado — suma uno como Project_Asset para activar las features de Slack."

## Categoría: "Seguimiento al equipo" (A1+A2+worklog unificadas)

**Cuándo aparece**: cuando hay issues del sprint activo en alguna de estas 3 situaciones:

1. Sin `storyPoints` / `originalEstimate` (motivo: estimación faltante)
2. Con `duedate < hoy` (motivo: vencido)
3. **En "In Progress" >3 días sin worklog** (motivo: sin tiempo cargado — agregado en v1.9.0, ver `jql-queries.md` Q7)

**Cómo se renderiza**: el botón global "Mandar follow-up al equipo por Slack ↗" aparece en la sección de Acciones globales del PASO 2. Al click, dispara `sendPrompt` al modelo que arranca PASO 3 (preview de drafts).

**Widget de PASO 3 para esta categoría** (variante del template general): en lugar de una tabla de cambios a Jira, muestra una tabla de **drafts de DM agrupados por assignee**. Una fila por assignee, con:

- Avatar circular + nombre del assignee.
- Lista de issues que le tocan (links a Jira) con etiqueta "sin estimar" / "vencido" / ambos.
- Textarea editable con el draft del mensaje. Plantilla por default (cada motivo agrega su línea):

  > Hola `<nombre>`, paso a pedirte un follow-up rápido sobre los siguientes issues del sprint activo de `<PROJECT_NAME>`:
  >
  > • `<KEY>` — `<summary>` (sin estimar) → ¿puedes cargar la estimación cuando puedas?
  > • `<KEY>` — `<summary>` (vencido el `<date>`) → ¿necesitas mover la fecha o el ticket está más cerca de cerrar?
  > • `<KEY>` — `<summary>` (en progreso desde `<date>` sin tiempo cargado) → ¿puedes cargar las horas trabajadas hasta ahora? Sirve para que el reporte de avance sea fiel.
  >
  > Gracias!

- Botón ✕ "Descartar" por fila para sacar a un assignee del batch.
- Footer: botón "Enviar (N drafts) ↗" que dispara `sendPrompt` con los drafts aprobados → PASO 4 envía vía `slack_send_message_draft`.

**Restricciones**: nunca envía sin OK explícito. Los mensajes los firma el PM (`as_user: true` no aplica acá — los mensajes salen desde la cuenta del PM con preview previo).

## Sub-detección B1: bloqueos no registrados en Jira

**Qué hace**: lee mensajes del canal interno del proyecto últimos 7 días buscando keywords (`bloqueado`, `blocker`, `bloqueado por`, `esperando a`, `no puedo avanzar`, `falta info de`, `dependo de`). Para cada match, intenta correlacionar:

- ¿Hay un issue Jira mencionado explícitamente en el mensaje (regex `<KEY>-\d+`)?
- ¿Hay un issue Jira mencionado en mensajes cercanos del mismo thread (±5 mensajes)?
- ¿El autor del mensaje es assignee de algún issue del sprint activo?

Si hay correlación con confianza alta o media, el skill flagea el issue como "potencialmente bloqueado" y lo cruza con sus `issuelinks` actuales:

- Si el issue YA tiene un `is blocked by` o `depends on` activo → no se hace nada (ya está reflejado).
- Si el issue NO tiene issuelink → se reporta como gap. Suma al contador de la dimensión "Dependencias explícitas" del scoring (baja el score si el ratio de gaps es alto).

Suma el botón global "Crear issuelinks sugeridos desde Slack ↗" cuando hay al menos 1 gap detectado. El PASO 3 muestra una tabla con 4 columnas: issue / extracto del mensaje Slack (con timestamp) / link sugerido (`is blocked by` / `relates to` / `depends on` — el modelo decide según contexto) / botón ✕.

## Sub-detección B4: requerimientos sin cargar

**Qué hace**: lee mensajes del canal interno últimos 14 días filtrando por autores con rol PO/cliente (heurística: dominio de email del workspace + autor mencionado en `Project__c.Account__r`). Busca keywords (`agregar`, `nuevo feature`, `también necesitamos`, `falta también`, `cambio en`, `nueva funcionalidad`).

Para cada match, hace búsqueda fuzzy contra issues abiertos en Jira (summary similarity > 70%). Si NO hay match, se reporta como "Posible requerimiento sin cargar" — sub-categoría informativa al lado de "Posible mistype". No se ejecuta fix automático: el cambio correcto es discutirlo en refinement y crear el issue manualmente. Sólo se reporta para que el PM lo lea.

## Notificaciones al canal interno del proyecto (v1.10.0+)

Botones opt-in que el PM dispara desde el widget para postear comunicación al canal del equipo. **Nunca envía sin OK explícito** — siempre preview editable.

### Post-diagnóstico (después de PASO 2)

Botón "Postear resumen del diagnóstico al canal interno ↗". Plantilla del mensaje:

```
🔍 Auditoría de proyecto — <PROJECT_NAME>
Score: <LETRA> / <NÚMERO> (fase <FASE>)

Hallazgos accionables:
• <N> issues sin asignar
• <N> vencidas
• <N> sin fecha
• <N> artefactos huérfanos
<otras categorías con N > 0>

<Si trabajo invisible se ejecutó:>
🔎 Trabajo invisible detectado: <N> candidatos en <X> fuentes (<lista de fuentes>)

Voy a empezar a accionar los más urgentes hoy.
Auditoría generada con `pc-delivery-jira-project-auditor` v<VERSION>.
```

Render: el PM ve esta plantilla en un widget de PASO 3 (variante "post-mensaje") con textarea editable. Puede ajustar el texto. Footer: "Postear al canal ↗" / "Cancelar ↗". Al confirmar, dispara `slack_send_message` al canal interno (id detectado en `Project_Asset__c` tipo "Slack channel internal").

### Post-batch aplicado (después de PASO 4)

Botón "Postear resumen del batch aplicado al canal interno ↗" en el reporte de PASO 4. Plantilla:

```
✅ Auditoría aplicada — <PROJECT_NAME>

Cambios ejecutados (<N>/<N>):
• <N> issues asignados (<lista de assignees nuevos>)
• <N> fechas actualizadas (<rango de fechas>)
• <N> artefactos vinculados a Drive/Figma
• <N> issues transicionados a <status>
<otros tipos de cambios aplicados>

<Si quedan más batches:>
Quedan <N> hallazgos pendientes — voy a procesar el próximo batch en breve.

<Si fue el último batch:>
Auditoría cerrada. Score actualizado: <LETRA NUEVA> / <NÚMERO NUEVO>.
```

Mismo flujo: preview editable + OK explícito + envío vía `slack_send_message`.

### Cuándo NO postear automáticamente

- **Nunca** sin OK explícito por mensaje, aunque el PM haya aprobado posteos en una sesión anterior.
- **Nunca** si el canal interno no fue confirmado en el PASO 0 (puede no existir o estar mal vinculado).
- **Nunca** si el batch tuvo fallas — en ese caso reportar primero el detalle de la falla en chat y dejar al PM decidir si igual quiere postear con la transparencia de "5 ok, 2 fallaron".

## Acción "Falta alcance del proyecto" — DM al caller

Detección: el skill chequea 3 fuentes en orden, y si **ninguna** tiene el documento de alcance:

1. Salesforce: `Project__c.Scope_Document_URL__c` (o `Scope__c`, según schema del cliente).
2. Salesforce: `Project_Asset__c` tipo `Scope document`, `SOW`, `Statement of Work` apuntando a Drive/Confluence.
3. Confluence: `searchConfluenceUsingCql` en el space del proyecto, página con título matcheando `(?i)scope|alcance|sow|statement of work`.

Si ninguna existe, el flag `missing_scope = true` y el botón "Pedirme cargar el alcance ↗" aparece en las acciones globales del widget de PASO 2.

**Por qué DM al caller (no al PM)**: cuando un Manager está auditando proyectos del equipo, el alcance suele faltar porque el PM no lo cargó. Mandar DM directo al PM puede ser percibido como reproche. Mejor: el caller (Manager) recibe el DM como recordatorio y decide cómo y cuándo pedirselo al PM. Si el caller ES el PM (modo self-audit), el DM funciona como self-reminder.

Lookup del Slack user: `slack_search_users` con el `email` del `atlassianUserInfo.email`.

Plantilla del DM:

```
🚨 Recordatorio del audit de hoy — proyecto <PROJECT_NAME>

No detecté un documento de alcance cargado para este proyecto:
• Salesforce Project__c.Scope_Document_URL__c: vacío
• Project_Asset__c tipo SOW: no existe
• Confluence space del proyecto: ninguna página de alcance encontrada

Acción sugerida:
1. Subir el SOW / scope document a Drive (carpeta del cliente).
2. Crear `Project_Asset__c` con Type__c = "Scope document" y Value__c = <URL>.
3. (Opcional) Replicar en Confluence como página viva.

Sin alcance cargado el scoring de relevamiento no puede subir de C, y el equipo trabaja con menos contexto.
```

Render: preview editable + botón "Mandarme el DM ↗" / "Cancelar ↗".

## Resumen de cómo afecta al widget de PASO 2

| Feature | Dónde aparece | Cuándo se omite |
|---|---|---|
| A1+A2 (Seguimiento al equipo) | Botón global en Acciones | Slack desconectado, o sin issues sin estimar/vencidos |
| B1 (Bloqueos no registrados) | Sub-score de Dependencias + botón global | Slack desconectado, o sin canal interno detectado |
| B4 (Requerimientos sin cargar) | Sub-categoría informativa en tabla resumen | Slack desconectado, o sin Account asociada para detectar autores cliente |

Las 3 features son aditivas — el skill funciona igual con o sin Slack, sólo que con Slack se detectan más cosas.
