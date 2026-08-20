---
name: pc-delivery-slack-channel-auditor
metadata:
  version: 2.16.0
  last_modified: 2026-07-11
description: >-
  Empuja al PM a postear status en el canal Slack externo del proyecto
  para mantener informado al comercial de Salesforce (partner seller).
  Recorre Project__c vigentes del PM y busca Project_Asset__c
  'SlackExternalProjectChannelId'; si falta, busca canales existentes y
  propone linkear o crea uno privado con PM+manager+comercial SF. Audita
  membresía y flagea +7d sin status. Ordena por Priority__c (más chico =
  más push) y agrupa por cuenta si hay multi-proyecto. En modo manager
  arma un DM conversacional al PM (no automático) y opcionalmente lee
  el DM 1:1 caller↔PM para enriquecer la auditoría con contexto privado.
  Tabla con multi-select + kebab: acciones globales e individuales para
  Completed/Ongoing/Stopped y Jira cross-check on demand. Toda decisión
  va por mcp__visualize__show_widget. Jira SOLO se consulta cuando el
  caller dispara la acción kebab. NUNCA crea, invita, postea, manda DM
  ni updatea SF sin aprobación expresa por widget. Solo PMs y managers
  de ProContacto. ES/EN.
---

<!-- Historial de versiones en CHANGELOG.md (no se carga en runtime). Versión actual: 2.16.0 -->

# pc-delivery-slack-channel-auditor

Empuja al PM a mantener al comercial de Salesforce informado del estado de
cada proyecto vigente. Recorre Salesforce, valida que cada proyecto tenga
canal externo armado (y lo crea si falta), y detecta cuándo el PM lleva
más de 7 días sin postear status. Cuando un manager audita a un PM de su
equipo, además puede armar un DM Slack conversacional de seguimiento.

---

## 🚨 REGLA DE SEGURIDAD CRÍTICA — lee esta sección primero

Los canales externos contienen conversaciones con el comercial de Salesforce
(partner seller). Aunque el cliente final no esté en el canal, el comercial
SF **es nuestro generador de oportunidades** — un mensaje enviado por error
compromete la relación y es imposible de "deshacer". Por eso este skill
opera bajo una regla inflexible:

> **NUNCA invites usuarios, crees canales, persistas registros en Salesforce,
> postees mensajes a Slack ni mandes DMs sin aprobación expresa del caller,
> acción por acción, en el turno actual, vía widget.**

### Qué significa en la práctica

- **Prohibido** llamar `slack_send_message`, `slack_schedule_message`,
  `slack_create_canvas`, o cualquier tool de write en Slack/SF, a menos que
  el caller haya confirmado en un widget de aprobación de la acción específica.
- **Prohibido** batch-aprobar. Si el caller dice "hazlo en todos", vuelve a
  pedir aprobación uno por uno con widget. La fricción es deliberada.
- **Prohibido** interpretar silencio, "sigue", "dale", "OK" genérico, o un
  pulgar arriba como aprobación. Solo vale el botón explícito del widget
  para esa acción específica.
- **Prohibido** "ayudar" modificando un draft y posteándolo en el mismo
  turno. Si corriges el texto, vuelve a render el widget de aprobación.
- **Default = no escribir.** Ante cualquier ambigüedad, render widget y
  espera.

### Cómo entregar drafts sin postear

Por defecto, los drafts se muestran **como texto en chat** (bloque de
código) o dentro de un widget con botón [Copiar]. El caller los copia y
pega a mano en Slack. Esta es la vía más segura y siempre disponible.

Si `slack_send_message_draft` está disponible y verificas en el turno
actual que **crea un draft persistido en Slack sin postearlo al canal**,
puedes ofrecerlo como alternativa vía widget. Si tienes cualquier duda de
que postea solo, **no lo uses**.

Para Fase 7 (DM follow-up) la única vía de envío es `slack_send_message`
tras un click explícito en [Aprobar y enviar DM] del widget de aprobación.

Más detalle, ejemplos y casos límite en `references/safety-rules.md`.

---

## 🎛 REGLA DE UX — widget-first, siempre

Esta regla complementa la regla de seguridad y aplica a TODO el flujo del
skill, no solo a las acciones de write.

> **TODA opción, CTA, pregunta o "próximo paso" que el skill le ofrezca al
> caller debe renderizarse vía `mcp__visualize__show_widget`. Prohibido
> enumerar opciones como bullets de texto en chat.**

### Qué significa en la práctica

- **Prohibido** terminar un mensaje con "¿Quieres A, B o C?" en bullets de
  texto. Render widget con un botón por opción que dispare `sendPrompt(...)`.
- **Prohibido** mostrar "Próximos pasos:" como lista markdown. Render widget
  con un botón por próximo paso.
- **Prohibido** pedir "tipea el ID del proyecto" en chat. Render widget con
  input o selector.
- **Prohibido** ofrecer "¿Sigo?" como sí/no en chat. Render widget con
  botones explícitos [Continuar] [Cancelar].
- **Permitido** texto descriptivo en chat (resumen narrativo, contexto,
  errores). Lo que va a widget son las **decisiones** que el caller tiene
  que tomar.

### Por qué

El skill es el "front-end" de un workflow de alto riesgo. Mezclar opciones
en texto plano:
1. rompe la consistencia visual (algunos pasos por widget, otros por chat),
2. invita al caller a responder con texto libre ambiguo en vez de un click
   explícito (= viola el espíritu de la regla de seguridad),
3. degrada la UX cuando el skill se ejecuta desde scheduled tasks o desde
   otros canales que renderizan widgets mejor que markdown.

### Cómo se ve en código

Para cada CTA: un botón en el widget con `onclick="sendPrompt('<intent>')"`.
El `<intent>` es el prompt en lenguaje natural que el caller "dispararía" si
escribiera a mano (ej. `"Onboardea los 4 canales faltantes"`).

---

## ☑ REGLA DE UX — checklist para mensajes propuestos (v2.6+)

Este patrón aplica a cualquier flow donde el skill propone **uno o más
ítems para incluir en un mensaje o serie de mensajes a enviar**: canales
sin update, status incompletos, bloqueos del cliente, proyectos finalizados,
drafts de status individuales, etc.

> **Cada ítem propuesto se muestra como un checkbox tildado por default.
> El caller puede deseleccionar los que no quiere incluir. El draft final
> se rearma en vivo según los checkboxes y el botón de envío refleja
> cuántos ítems quedan.**

### Por qué este patrón es seguro

El patrón checklist parece "batch aprobación" pero NO lo es. Cada checkbox
es una **micro-aprobación explícita del ítem** que el caller revisa
visualmente antes de enviar. La diferencia con la regla original "una
aprobación por mensaje":

| Original | Con checklist |
|---|---|
| 1 mensaje = 1 click de aprobación | 1 mensaje compuesto = 1 click por ítem (deselección o no) + 1 click final de envío |
| Fricción grande si hay 10 ítems | Fricción granular pero proporcional |
| Caller no puede dropear ítems individuales sin editar texto | Caller dropa ítems con 1 click |

El botón final **sigue siendo necesario** y el envío sigue requiriendo el
click explícito. La trazabilidad mejora porque el log puede registrar
qué ítems quedaron tildados y cuáles no.

### Reglas inviolables

1. **Default = todos tildados.** El caller deselecciona; no tilda desde cero.
   Si un ítem tiene riesgo especial (proyecto finalizado, bloqueo escalado),
   marcarlo visualmente con `⚠️` pero igual viene tildado.
2. **Preview live.** El widget muestra el texto resultante del DM (o
   contenido equivalente) en un panel que se rearma cada vez que cambia un
   checkbox. Sin este preview el patrón no aplica — el caller necesita ver
   qué va a salir.
3. **Counter en el botón.** El botón de envío dice "Aprobar y enviar DM
   con **N items**" — N se actualiza en vivo. Si N=0 el botón queda
   deshabilitado con tooltip "No hay items seleccionados".
4. **Editar individual posible.** Para cada ítem, un icono `✎` abre un
   mini-input para tweakear la línea sin tener que editar el draft entero.
   Cambios se reflejan en el preview live.
5. **Cancelar todo siempre disponible.** Botón [Cancelar] que cierra el
   widget sin enviar nada. Equivalente a "destildar todo + cerrar".
6. **No autocompletar.** Si el caller destilda TODOS los ítems, el botón
   se deshabilita — no se interpreta como "envía un DM vacío" ni como
   "cancelado, manda igual con default". El caller tiene que click
   explícito en cancelar o re-tildar.

### Cuándo NO aplica el patrón

- **Confirmaciones binarias** (crear canal sí/no, invitar usuario sí/no):
  no es una lista de ítems, es una decisión única. Mantener los botones
  [Confirmar] / [Cancelar] del patrón widget-first original.
- **Drafts standalone que se postean en canal externo** (Fase 6 con
  destino al canal del comercial SF): cada draft sigue su widget propio
  con [Copiar] / [Editar] / [Cerrar] porque postear ahí es un evento de
  alto riesgo independiente. El checklist aplica solo a la **lista** de
  drafts proyectos, no al contenido de cada draft.

### Aplicaciones actuales

| Fase | Qué se muestra como checklist |
|---|---|
| 6 | Lista de proyectos R0 con un draft de status cada uno. Destildar = no mostrar ese draft. |
| 7 | Cada ítem dentro del DM al PM: status incompletos, canales sin update, líneas de bloqueo de cliente, proyectos finalizados. Destildar = no incluir esa línea en el DM final. |

---

## Roles: PM, manager (caller), comercial SF

A partir de v2.5.0 el skill distingue dos modos de uso según quién es el
caller frente al `Owner` del proyecto auditado:

| Modo | `caller_email` vs `pm_email` (Owner) | Flujo |
|---|---|---|
| **Self-audit** | `caller == pm` | Fases 0–6. La Fase 7 (DM follow-up) **no aplica** — no tiene sentido auto-DM-arse. |
| **Manager-audit** | `caller != pm` | Fases 0–6 + Fase 7 disponible. El caller (típicamente un manager o líder de área) puede generar un DM Slack conversacional al PM auditado con la lista de canales sin update. |

`caller_email` se obtiene de `getUserInfo` de Salesforce al inicio.
`pm_email` se obtiene del widget de Fase 0 (default = caller).

---

## 🔒 REGLA DE PRIVACIDAD — contenido del DM 1:1 (v2.13+)

Los PMs frecuentemente le escriben al caller (manager) por DM 1:1 cosas
que NO pueden decir en el canal externo del proyecto: problemas con el
cliente, frustración con el comercial SF, decisiones sensibles, contexto
que solo se comparte verticalmente. Cuando la Fase 2.5 lee ese DM, el
contenido se vuelve material delicado.

> **El contenido textual del DM 1:1 entre caller y PM JAMÁS sale al canal
> externo, ni a un artefacto público, ni a un campo SF que terceros
> puedan leer. Solo puede aparecer en (a) el widget de auditoría que ve
> el caller, y (b) el DM de respuesta de Fase 7, porque el PM y el
> caller son ambos partes de esa conversación.**

### Qué significa en la práctica

| Destino | DM content puede aparecer | Por qué |
|---|---|---|
| Widget de Fase 5.2 (visible al caller) | ✅ Sí — extractos cortos, citas con `💬 DM` | El caller lee sus propios DMs, no hay leak |
| DM de respuesta de Fase 7 al PM | ✅ Sí — como acknowledgement ("Como me comentaste por DM, ...") | Misma conversación, mismos interlocutores |
| Draft de Fase 6 para postear al canal externo | ❌ Nunca | El comercial SF no debe ver lo que el PM dijo en privado |
| Campos SF visibles (Notes__c, Description__c) | ❌ Nunca como texto literal | Otros users de SF los pueden leer |
| Campos SF de valor (Estimated_Go_Live__c, Status__c) | ✅ Solo el valor, no el extracto | El SF guarda la fecha, no la cita textual del DM |
| Reportes / dashboards / Slack canvas | ❌ Nunca | Audiencia pública |

### Implementación obligatoria

- El extractor askClaude de Fase 2.5 devuelve `source_excerpt` que SOLO
  se usa en el widget del caller. Para Fase 7 se transforma a paráfrasis
  amable ("me comentaste que..."). Nunca se cita literal al canal externo.
- En Fase 9, si la fuente del valor propuesto es DM (`source = 'dm'`), el
  widget lo muestra al caller pero el `updateSobjectRecord` solo manda
  el valor, no el extracto. Si el campo SF a popular es Notes__c o
  Description__c, ahí sí evitar el extracto literal — usar paráfrasis
  generada por Haiku que sintetice sin citar.
- En cualquier flow nuevo que sume el skill, antes de incluir DM content
  en un output, validar contra esta tabla. Si no entra en la columna
  "Sí", el DM content no va.

### Test mental

> **Si el PM viera el output completo del flow, ¿se ofendería al notar
> que cosas que me dijo en privado terminaron en un canal donde está el
> comercial SF o un cliente?**

Si la respuesta es sí, el flow está violando la regla.

---

## 🎨 REGLA DE WIDGETS — shell canónico

Todo HTML que el skill renderice vía `mcp__visualize__show_widget` se arma
**componiendo los bloques del shell canónico** definido en
`references/widget-shell.md`. Esa es la única fuente de verdad para el markup
de los 8 widgets (Fases 0, 3A, 5.2, 6, 7, 8, 9, 10).

> **Tres reglas inflexibles (detalle completo en `references/widget-shell.md`):**
> 1. **Tema auto-adaptable**, NO forzado: solo tokens nativos de la plataforma
>    (`--surface-*`, `--text-*`, `--bg-*`, `--border*`), que siguen claro/oscuro
>    del host. Sin background en el contenedor exterior (transparente).
> 2. **Cero colores hardcoded** — un hex queda ilegible en uno de los dos modos.
> 3. **Íconos Tabler, no emoji** en el HTML (`<i class="ti ti-NAME">`). Los emoji
>    SÍ valen en el texto de mensajes Slack —drafts de Fase 6/7/10—, que no es
>    HTML del widget.

**Antes de armar cualquier widget, carga `references/widget-shell.md`** y
compón con sus bloques (`header-card`, `kpi-grid`, `banner`, `data-table`,
`checklist-block`, `button-row`, `badges`). Si dos widgets muestran lo mismo,
tienen que verse idénticos. Test mental antes de pegar el HTML: "¿cada texto y
borde se lee bien en claro y en oscuro?".

---

## 👥 REGLA — canales compartidos por varios PMs (v2.7.1+)

Un mismo canal Slack externo puede estar registrado como
`Project_Asset__c` de varios `Project__c` distintos, cada uno con su
propio `OwnerId`. Esto pasa típicamente cuando varios PMs trabajan
proyectos en paralelo para la misma cuenta y comparten un único canal
con el comercial SF.

> **Cuando audites a un PM, solo cuentan los mensajes de ESE PM como
> "status posteado". Los mensajes de otros PMs en el mismo canal NO
> destildan el R0 del PM auditado.**

### Qué significa en la práctica

- `last_pm_post_days` se calcula buscando el último mensaje top-level
  cuyo `author == Owner.Email` del proyecto auditado en esta ejecución,
  NO el último mensaje top-level del canal (eso es `days_inactive`).
- R0 dispara para PM A aunque PM B haya posteado hoy — son responsables
  de status separados.
- En el DM follow-up, si PM B también es responsable de algún proyecto
  en ese canal, eso queda **fuera** del DM a PM A. PM B se audita en
  su propia ejecución (típicamente su propia scheduled task).
- Esto vale incluso si el canal tiene un solo `Project_Asset__c` y los
  otros PMs solo están "de paso". El filtro es por author, no por
  membresía.

### Edge case — canal multi-PM detectado

Cuando audites un canal y encuentres mensajes top-level de **otros PMs**
de ProContacto (otros emails @procontacto en la ventana de 10 msgs), el
skill puede agregar una nota informativa (no R0 amarillo, no anomalía)
en el `preview` de la fila: "Canal compartido — también postean: <PM B>,
<PM C>". Esto ayuda al caller a entender por qué `days_inactive` es bajo
pero `last_pm_post_days` es alto.

### Identificación de "otro PM de ProContacto"

Un mensaje cuenta como "de otro PM" cuando el author:
- Tiene un email del dominio de ProContacto (ver `references/team-identification.md`).
- NO es el `Owner.Email` del proyecto auditado.
- NO es un bot (ver mismo reference).

Bots, comercial SF y eventualmente el cliente final caen en otras
categorías y no se rotulan como "PM compartiendo el canal".

---

## Qué cambió respecto de v1

| Aspecto | v1 (auditoría de pending del cliente) | v2 (impulso de status al comercial SF) |
|---|---|---|
| Audiencia del canal | Cliente + equipo PC | **Comercial SF + equipo PC** (cliente NO está) |
| Regla primaria | R1: cliente preguntó y PC no respondió | **R0: PM no postea status hace +7d** |
| Si no hay canal | Sugiere registrar el asset | **Crea canal privado + invita Owner + Manager + comercial SF + persiste asset** |
| UX inputs | `AskUserQuestion` | **`mcp__visualize__show_widget` siempre** |
| UX opciones / CTAs | Bullets de texto en chat | **`mcp__visualize__show_widget` siempre (v2.1+)** |
| Output principal | Artifact HTML (deprecado en v2.2.0) | **Widget único (`mcp__visualize__show_widget`) con KPIs + tabla + CTAs (v2.2+)** |
| Threshold default | R1=48h, R2=7d, R3/R4=24h | **7 días unificado para R0**; R1-R4 quedan secundarias |
| Follow-up al PM | (no existía) | **Fase 7 (v2.5+) — DM conversacional al PM auditado en modo manager** |

---

## Qué detecta el skill

### Regla primaria — R0: silencio del PM frente al comercial SF

| # | Tipo | Default threshold |
|---|---|---|
| **R0** | El PM (Owner del Project__c) no postea ningún mensaje top-level en el canal externo | **> 7 días** |

R0 dispara incluso si el comercial SF está activo. La idea es: **el comercial
no debería tener que pedir update — el PM debería estar empujándolo
proactivamente**.

### Reglas secundarias (vista adicional, no primaria)

| # | Tipo | Default threshold |
|---|---|---|
| R1 | El más reciente de los últimos 10 msgs es del comercial SF y nadie de PC respondió | > 48 h |
| R2 | Ninguno de los últimos 10 msgs top-level es de PC (humano) | > 7 d |
| R3 | Thread (cuyo root está en los últimos 10) abierto y último reply es del comercial SF | > 24 h |
| R4 | `@mención` a usuario PC en la ventana, sin reply del mencionado | > 24 h |

**Ventana fija = últimos 10 mensajes top-level del canal + sus threads.**

Algoritmo exacto y edge cases en `references/detection-rules.md`.

### Señales nuevas para Fase 7 (manager-audit DM)

A partir de v2.5.0, además de R0/R1-R4, el skill calcula por canal:

| Señal | Cómo se detecta |
|---|---|
| `status_completeness` | Si el último post del PM en el canal incluye **fecha de golive** + **próximos pasos** explícitos. Si falta alguno de los dos = "status incompleto". |
| `client_blocker` | El PM mencionó en la ventana de 10 msgs alguno de los patrones: cliente no vino a meet, cliente no responde, cliente no termina de definir temas, cliente no entrega pendientes. Inferencia con `askClaude` (Haiku) sobre el contenido del canal. |
| `hypothetical_golive_week` | Si hay pendientes del cliente y se puede inferir desde Project__c (Estimated_Go_Live__c, backlog Jira), la semana en que caería el golive si el cliente entregara HOY. |

---

## Gate: proyecto vigente + PM seleccionado

**Solo audita proyectos que pasen las DOS condiciones:**

1. `Project__c.Completion_Summary__c = null` — el proyecto no está cerrado.
   No uses `Status__c` — `Completion_Summary__c` es la única fuente de
   verdad para "proyecto vigente".
2. `Project__c.OwnerId = <PM seleccionado en Fase 0>`. Default: el usuario
   que invoca el skill (tú). El caller puede tipear otro user para auditar
   proyectos de un colega.

Para cada proyecto que pasa el gate:

- **Tiene `Project_Asset__c` con `Type__c = 'SlackExternalProjectChannelId'`** →
  Fase 3B (auditar actividad).
- **No lo tiene** → Fase 3A (onboarding del canal).

### Proyectos finalizados recientemente (para Fase 7)

Fase 7 además consulta una query auxiliar:

```sql
SELECT Id, Name, Account__r.Name, Completion_Summary__c,
       LastModifiedDate
FROM Project__c
WHERE Completion_Summary__c != null
  AND OwnerId = '<PM_USER_ID>'
  AND LastModifiedDate = LAST_N_DAYS:30
```

Los proyectos finalizados en los últimos 30 días se mencionan **aparte** en
el DM follow-up con su fecha de cierre, para que el PM los baje del
seguimiento si todavía aparecen "activos" en su dashboard mental.

---

## Workflow (10 fases)

### Fase 0 — Inputs vía widget

Render `mcp__visualize__show_widget` con los bloques del shell (ver
`references/widget-shell.md`): un `header-card` corto + un formulario que
pregunta:

1. **PM a auditar** — input text con default = email del caller actual
   (`getUserInfo` de Salesforce).
2. **Threshold de silencio R0** — slider con default 7 días.
3. **Modo** — radio buttons:
   - "solo diagnóstico"
   - "diagnóstico + onboarding de canales faltantes"
   - "diagnóstico + drafts de status (para postear en el canal)"
   - **"diagnóstico + DM follow-up al PM" (v2.5+, solo visible si caller != PM)**
4. **Incluir DM 1:1 con el PM** (v2.13+, toggle, default ON cuando
   `is_manager_audit = true`, oculto cuando `caller = PM`) — si está
   tildado, el skill lee el DM 1:1 entre caller y PM en los últimos 30
   días para enriquecer la auditoría con menciones privadas. Ver
   "🔒 REGLA DE PRIVACIDAD".

El widget cierra con un `button-row`: botón "Ejecutar auditoría" que dispara
`sendPrompt(...)` con los valores elegidos. NO arranques el flujo hasta tener
esos inputs.

Si el caller ya dio los datos en el pedido inicial, render igual el widget
pre-llenado para que confirme — un click sigue siendo más rápido que tipear,
y queda registro visual de los parámetros.

### Fase 1 — Query a Salesforce

```sql
SELECT Id, Name, Account__c, Account__r.Name,
       OwnerId, Owner.Name, Owner.Email, Owner.ManagerId,
       Owner.Manager.Name, Owner.Manager.Email,
       Estimated_Go_Live__c, Completion_Summary__c,
       Status__c, Priority__c,
       RecordTypeId, RecordType.DeveloperName
FROM Project__c
WHERE Completion_Summary__c = null
  AND OwnerId = '<PM_USER_ID>'
ORDER BY Priority__c ASC NULLS LAST, Name
```

**Priority__c** (v2.7+): número entero, **más chico = más prioritario**.
Default si es `null` = 99 (no priorizar lo no-priorizado).

**RecordType.DeveloperName** (v2.8+): clasifica el proyecto como Delivery
o Support. Mapeo:
- `Support` → `project_type = 'Support'`
- cualquier otro valor (típicamente `Project`, `Quickstart`, `POC`,
  `Integration`, `Change_Control`, `Outsourcing`, `TaaS`, etc.) →
  `project_type = 'Delivery'`
- Si el RecordType no se puede leer o es `null`, fallback a `Delivery`
  (conservador — el cierre con golive+sprint es el más común) y agregar
  una nota informativa en el output: "N proyectos sin RecordType — los
  traté como Delivery".

Esto determina el sub-bloque del DM (Delivery / Support) en Fase 7 y el
cierre que se aplica a ese proyecto.

**Status__c**: picklist con los valores que la org tenga definidos
(típicamente `Ongoing`, `Stopped`, `On Hold`, `Completed`). Las acciones
de la tabla en Fase 5.2 escriben en este campo (`Ongoing` / `Stopped`) y
la acción "Marcar como Completed" escribe en `Completion_Summary__c`. Si
los valores del picklist difieren, hay que mapearlos vía `getObjectSchema`
antes de habilitar la acción.

Detalle completo + query de `Project_Asset__c` en
`references/salesforce-schema.md`.

Si los nombres de campo difieren del esperado, llama `getObjectSchema` de
`Project__c` y `Project_Asset__c` antes de la primera query y documenta el
mapeo detectado en el output. Si `Priority__c` no existe en la org, omitilo
del query y trata todos los proyectos como priority=99 (sin priorización).

### Fase 2 — Para cada proyecto, buscar canal externo

```sql
SELECT Id, Project__c, Type__c, Value__c, Grouper__c
FROM Project_Asset__c
WHERE Project__c IN (<lista>)
  AND Type__c = 'SlackExternalProjectChannelId'
```

`Value__c` guarda el channel ID Slack (formato `C01234567`).

Bifurcación por proyecto:

- Hay asset → **Fase 3B** (auditar).
- No hay asset → **Fase 3A** (onboarding).

### Fase 2.5 — Leer DM 1:1 caller↔PM (v2.13+, opcional)

Solo se ejecuta si `is_manager_audit = true` Y el toggle "Incluir DM 1:1
con el PM" de Fase 0 quedó tildado (default ON).

**Paso 2.5.1 — Resolver el canal DM**

- `slack_search_users` por `pm_email` → `pm_slack_user_id`.
- Resolver el canal DM 1:1 entre `caller_slack_user_id` y `pm_slack_user_id`.
  En la API REST de Slack, esto sería `conversations.open` con `users=` la
  pareja, devolviendo `im_channel_id`. En el conector Cowork, equivale a
  buscar un canal de tipo `im` con esos dos miembros.
- Si no existe el DM 1:1 (nunca se hablaron) → marcar `dm_available = false`
  y saltar Pasos 2.5.2-2.5.3. Mostrar nota en el output: "No hay DM 1:1
  con <PM> — el caller y el PM nunca se hablaron por DM".

**Paso 2.5.2 — Leer mensajes del DM en los últimos 30 días**

- `slack_read_channel` sobre `im_channel_id` con paginación suficiente
  para cubrir 30 días calendario (estimar 30-100 msgs según frecuencia).
- Conservar tanto msgs del caller como del PM — el contexto es bidireccional.
  Para extracción nos interesan mensajes del PM principalmente, pero el
  thread completo da contexto a Haiku.
- Si en 30 días no hay nada del PM (solo del caller) → marcar
  `dm_pm_silent_in_window = true` y seguir con extracción vacía. Esto es
  informativo — el PM no respondió DMs del caller en un mes, lo cual es
  una señal de coordinación pero no se usa para R0.

**Paso 2.5.3 — Extracción por proyecto vía askClaude**

Una sola llamada a `askClaude` con el contenido del DM y la lista de
proyectos auditados. Prompt:

```
Texto: <últimos 30 días del DM 1:1 entre <caller_name> y <pm_name>,
ordenado cronológicamente, con autor y timestamp por mensaje>.

Lista de proyectos auditados (con id, nombre y account):
<lista de project_id + project_name + account_name>.

Para cada proyecto de la lista, identifica si el PM lo mencionó en este
DM. Para cada mención devuélveme un objeto con:
- project_id: el id del proyecto mencionado.
- ts: timestamp de la mención.
- summary: 1-2 oraciones resumiendo qué dijo el PM (paráfrasis amable,
  no copia textual cuando hay info sensible).
- source_excerpt: cita textual corta (≤120 chars). Solo se usa en el
  widget del caller — NO en outputs públicos.
- classification: uno de "status_update" | "blocker_client" |
  "blocker_internal" | "golive_change" | "scope_change" | "decision" |
  "vent" | "other".
- sensitivity: "low" | "medium" | "high". Marca "high" cuando el PM
  desahoga frustraciones, critica a comercial SF o cliente, o comparte
  info que no debería salir del 1:1.

Devuélveme JSON: { "mentions": [...] }.

Reglas estrictas:
- Solo incluir menciones que claramente refieren a un proyecto de la lista.
- Si el PM habla de "el cliente" sin nombrar proyecto, intentar deducir
  por contexto. Si no es claro, no atribuir.
- NO inferir más allá de lo que el PM dijo.
- Si todo el DM es small talk sin nada de proyectos, devolver mentions: [].
```

Resultado: array `dm_mentions` global, que después se agrupa por
`project_id` y se enchufa en cada fila correspondiente.

**Paso 2.5.4 — Enriquecer rows**

Para cada fila de `audit.rows`, agregar:

- `dm_mentions_in_window`: array de menciones para ese project_id.
- `latest_dm_mention_ts`: timestamp más reciente del array (o `null`).
- `has_dm_context`: `true` si el array tiene ≥1 entry.
- `dm_highest_sensitivity`: `low` / `medium` / `high` (max del array, o
  `null`).

Si una fila tiene `dm_highest_sensitivity = 'high'`, el widget agrega
un ícono `ti-lock` al lado del `ti-message` para alertar al caller que ese
contexto es sensible.

**Paso 2.5.5 — Casos especiales**

- **DM mencionó un proyecto NO auditado**: el PM puede haber hablado de
  un proyecto que no entró en `audit.rows` (porque está completado, o
  porque está en otro Owner). Esos mentions van a un bucket aparte
  `dm_extra_mentions` y se muestran en la Sección B (KPI cards) como
  "N menciones de otros proyectos en DM" — informativo, sin acción.
- **DM con conversación larga sin proyectos**: si Haiku devuelve
  mentions=[], skip silencioso. El KPI card "DM mentions" muestra 0.

### Fase 3A — Onboarding del canal (proyecto sin asset)

Para cada proyecto sin canal externo, render widget secuencial con OK por
acción. **Cada paso requiere botón explícito** — no se encadena solo. Cada
widget de este wizard se arma con los bloques del shell (`header-card` corto +
checklist/inputs + `button-row`); los bloques de código de abajo son mockups
conceptuales del contenido, no del HTML. Ver `references/widget-shell.md`.

**⚠ Regla anti-duplicado (v2.3+):** "sin Project_Asset__c" NO implica
"sin canal Slack". Muchos PMs crean el canal y se olvidan de registrar el
asset. ANTES de proponer crear canal, hay que buscar en Slack si ya existe
uno que matchee el proyecto.

**Paso 3A.0 — Buscar canales Slack candidatos (siempre primero)**

Para el proyecto en curso, genera un set de keywords a partir de:
- `Account.Name` slugificado (lowercase, sin espacios, sin acentos)
- `Project.Name` slugificado
- Tokens individuales del account name (ej. "Repuestos Boston" → ["repuestos", "boston"])
- Aliases comunes detectados en el catálogo PC: prefijos `cc-`, `proy-`,
  `ext-`, `pc-`, sin prefijo

Llama `slack_search_channels` con cada keyword (limit 20 por llamada,
incluye privados de los que el PM es miembro). Unifica los resultados,
dedupliçá por `channel_id`, y filtra:
- Excluye canales archivados.
- Excluye canales DM y group DM.
- Prioriza los que tienen al PM como miembro.
- Prioriza los que el nombre contiene el slug del account.

Render widget con el resultado:

```
Proyecto: <Project.Name> · Account: <Account.Name>

Encontré N canal(es) en Slack que podrían ser este proyecto:

[ ] #cc-repuestosboston   · 12 miembros · creado 2025-08-14 · PM es miembro ✓
[ ] #proy-repuestos       · 5 miembros  · creado 2024-11-02
[ ] #ext-boston-rollout   · 8 miembros  · creado 2025-02-10 · PM es miembro ✓

Opciones:
[Linkear el seleccionado]  [Ninguno aplica — crear nuevo]  [Cancelar este proyecto]
```

Comportamiento según elección:

- **Linkear el seleccionado** → salta los Pasos 3A.1-3A.3 y ve directo a
  Paso 3A.4 modificado: persistir `Project_Asset__c` con
  `Value__c = <channel_id_seleccionado>`. **NO** crees canal, **NO**
  invites usuarios (asumí que la membresía ya está armada — quedará para
  Fase 3B detectar issues de membresía en la próxima auditoría).
- **Ninguno aplica — crear nuevo** → sigue con Paso 3A.1.
- **Cancelar** → salta este proyecto, pasa al siguiente.

Si Slack devuelve 0 candidatos, muestra igual el widget con el mensaje "No
encontré canales que matcheen" y las opciones [Crear nuevo] [Cancelar].

**Paso 3A.1 — Pedir mail del comercial SF**
Widget con un input text: "Mail del comercial de Salesforce que originó
la oportunidad de **<Project.Name>** (Account: **<Account.Name>**)".

**Paso 3A.2 — Validar mail en Slack**
`slack_search_users` con el mail. Si no aparece, render widget de
re-tipeo con el error. No avanzar sin un user Slack válido.

**Paso 3A.3 — Confirmar plan de onboarding**
Widget con resumen visual:

```
Proyecto: <Project.Name>
Account: <Account.Name>

Voy a:
1. Crear canal Slack PRIVADO con nombre "ext-<account-slug>-<project-slug>"
2. Invitar a:
   • <Owner.Name> (PM, <Owner.Email>)
   • <Owner.Manager.Name> (Manager del PM, <Owner.Manager.Email>)
   • <Comercial SF Name> (<comercial_sf_email>)
3. Persistir Project_Asset__c (Type__c='SlackExternalProjectChannelId',
   Value__c=<channel_id>) en el Project__c

¿Confirmas?  [Sí, ejecutar]  [Cancelar]
```

**Paso 3A.4 — Ejecución (solo después de confirmar)**

**Pre-check anti-duplicado (v2.3+):** antes de invocar la API de creación,
llama `slack_search_channels` una última vez con el nombre exacto propuesto
(`ext-<account-slug>-<project-slug>`). Si aparece un match exacto:

- Frena la ejecución (no crees nada).
- Render widget mostrando "Detecté que `<channel_name>` ya existe en Slack —
  ¿linkeas el existente o ajustas el nombre?".
- Opciones: [Linkear el existente] [Renombrar y reintentar] [Cancelar].
- Si "Linkear", salta al paso 3 con `Value__c` del canal hallado.

Si el pre-check pasa, continuar:

1. Crear canal privado.
2. Invitar a los 3 usuarios.
3. Persistir el `Project_Asset__c` con `createSobjectRecord`.
4. (Opcional, por widget aparte) Postear un mensaje de bienvenida — solo
   si el PM aprueba el texto exacto.

Detalle paso a paso, fallbacks, naming convention y troubleshooting en
`references/channel-onboarding.md`.

### Fase 3B — Auditar canal existente

Para cada canal:

1. **Membresía** — leer miembros del canal.
   - Verificar que `Owner.Email` (PM) está → si no, flag amarillo.
   - Pedir al caller (vía widget) el mail del comercial SF si no se conoce →
     verificar que está → si no, flag amarillo + CTA "invitar".
   - Verificar que **no hay un user con dominio del cliente final**. Si
     aparece, flag anomalía (cliente no debería estar en este canal).

2. **Lectura de actividad**:
   - `slack_read_channel` límite fijo = 10 mensajes top-level recientes.
   - Para cada uno que sea root de thread, `slack_read_thread`.
   - **Nunca** leas más de esa ventana.

3. **Cálculo de R0** (regla v2.7.1 — multi-PM en canal compartido):
   - Buscar el último mensaje top-level cuyo author == `Owner.Email`
     del **proyecto auditado en esta ejecución**. Otros emails (incluso
     otros PMs de ProContacto que posteen en el mismo canal por proyectos
     paralelos) NO cuentan.
   - `last_pm_top_level_ts` = ts de ese mensaje (o `null` si no hay
     ninguno del owner en la ventana — aunque haya otros mensajes de
     otros PMs).
   - Si `last_pm_top_level_ts == null` o `now - last_pm_top_level_ts >
     7 días` → **R0 ROJA** para ese proyecto.
   - Si la ventana contiene mensajes top-level de otros emails
     `@procontacto.com.mx` distintos del owner, agregar al `preview`
     de la fila una nota: "Canal compartido — también postean: <Otro PM A>,
     <Otro PM B>". Sin penalizar — es informativo.

4. **Cálculo de R1-R4 (vista secundaria)** — ver
   `references/detection-rules.md`.

5. **Cálculo de señales para Fase 7 (v2.5+, v2.9 extendido):**

   Se consolidan en **una sola llamada a `askClaude` por canal** que
   devuelve un JSON con todas las señales. El prompt al extractor:

   ```
   Texto: <últimos 10 msgs top-level del canal + threads, filtrando a
   mensajes de cualquier autor humano de ProContacto>.

   Devuélveme JSON con estas claves:
   - status_completeness: "complete" | "incomplete" | "missing" según si
     el último post del PM (Owner.Email = <email>) tiene fecha de golive
     y lista de próximos pasos.
   - client_blocker: uno de "no_meet_attendance" | "no_response" |
     "no_scope_definition" | "no_pendings_delivery" | "none".
   - mentioned_golive_date: la fecha de go-live más reciente que el PM
     declaró en sus posts (formato YYYY-MM-DD). null si no la mencionó.
   - mentioned_module: el módulo o producto Salesforce que el PM mencionó
     que se entrega o se entregó. Valores aceptados: "Sales Cloud",
     "Service Cloud", "Marketing Cloud", "Account Engagement", "Consumer
     Goods Cloud", "Field Service", "Experience Cloud", "Financial
     Services Cloud", "Health Cloud", "Industries", "CRM Custom",
     "Integration", "Data Cloud", "Agentforce", "Other (texto libre)".
     Si menciona varios, devolver el principal. null si no lo dijo.

   IMPORTANTE: no inferir cosas que el PM no dijo. Si tienes dudas, devolver
   null en ese campo.
   ```

   Derivados a partir del JSON:

   - `recent_golive` (v2.9+): bool. True si `mentioned_golive_date` no es
     null Y `(today - mentioned_golive_date)` está entre **-7 y 30 días**
     (incluye ventana de gracia de una semana pre-golive por si dieron
     una fecha futura cercana, y 30 días post-golive como pediste).
   - `hypothetical_golive_week` (v2.5+): si `client_blocker != none` y
     `Project__c.Estimated_Go_Live__c` existe, devolver la semana ISO de
     `Estimated_Go_Live__c`. Si no, `null`. NO consultar Jira (regla v2.7).

6. Casos especiales:
   - Canal con 0 mensajes → R0 roja con detalle "canal vacío".
   - Canal inaccesible (PM no es miembro, ID obsoleto) → bucket aparte.

### Fase 4 — Calcular `days_inactive` y armar filas

```
last_activity_ts = max(ts de los últimos 10 msgs top-level + replies de sus threads)
days_inactive    = floor((now - last_activity_ts) / 86400)
```

`days_inactive` es la sort key principal de la tabla.

> **Distinción importante:** `days_inactive` mide cuándo fue el último
> mensaje del canal (cualquier miembro). `last_pm_post_days` mide cuándo
> fue el último post del **owner del proyecto** específicamente.
> R0, el resumen de chat y la Fase 7 usan **`last_pm_post_days`**, no `days_inactive`.

**Nunca** usar `LastModifiedDate` ni `CreatedDate` de Salesforce — el
indicador real vive en Slack.

Cada fila incluye además:
- `last_pm_post_days` — días desde el último post del PM (clave de R0).
- `comercial_sf_in_channel` — bool.
- `cliente_final_anomaly` — bool (true si detectamos un user con dominio cliente).
- `status_completeness` — `complete` / `incomplete` / `missing` (v2.5+).
- `client_blocker` — uno de los enums de señal (v2.5+).
- `hypothetical_golive_week` — semana ISO o `null` (v2.5+).
- `priority` — entero, default 99 si no hay priority en SF (v2.7+).
- `current_status` — valor crudo de `Project__c.Status__c` (v2.7+).
- `account_id`, `account_name` — para agrupar por cuenta en Fase 7 (v2.7+).
- `project_type` — `Delivery` o `Support`, según RecordType.DeveloperName
  (v2.8+).
- `mentioned_golive_date` — fecha de golive extraída del canal (v2.9+),
  ISO `YYYY-MM-DD` o `null`.
- `mentioned_module` — módulo/producto extraído del canal (v2.9+),
  string del catálogo o `null`.
- `recent_golive` — bool, true si `mentioned_golive_date` cae entre -7 y
  +30 días respecto de hoy (v2.9+).

### Fase 5 — Output: widget único `mcp__visualize__show_widget`

**v2.2.0:** la salida ya NO es un artifact HTML. Es **un solo widget** que
contiene KPIs + tabla completa + CTAs accionables. Esto garantiza que toda
ejecución (interactiva o headless / scheduled task) entrega siempre una
superficie viva — nunca bullets inertes.

#### Paso 5.1 — Construir el objeto `audit`

```json
{
  "generated_at": "2026-05-12T10:30:00Z",
  "caller_email": "ariel.tarsitano@procontacto.com.mx",
  "pm_name": "Ariel T.",
  "pm_email": "ariel.tarsitano@procontacto.com.mx",
  "is_manager_audit": false,
  "thresholds": { "r0_days": 7, "r1_hours": 48, "r2_days": 7, "r3_hours": 24, "r4_hours": 24 },
  "summary": {
    "scanned_projects": N,
    "audited_channels": M,
    "r0_red": X,
    "r0_filtered_for_dm": Xf,
    "missing_asset": W,
    "missing_comercial_sf": K,
    "client_anomaly": A,
    "inaccessible": I,
    "ok": Z,
    "finished_recently": F
  },
  "rows": [
    {
      "priority": "red" | "yellow" | "white",
      "project": "BetaCorp",
      "project_id": "a0X...",
      "account": "BetaCorp SA",
      "channel": "#ext-betacorp-rollout",
      "channel_id": "C01...",
      "rule": "R0",
      "last_pm_post_days": 12,
      "days_inactive": 8,
      "comercial_sf_in_channel": true,
      "cliente_final_anomaly": false,
      "status_completeness": "incomplete",
      "client_blocker": "no_response",
      "hypothetical_golive_week": "2026-W26",
      "preview": "Último msg del canal: ..."
    }
  ],
  "finished_recently_rows": [
    {
      "project": "Omega Migration",
      "project_id": "a0Z...",
      "account": "Omega SA",
      "channel_id": "C0A...",
      "completion_date": "2026-05-12",
      "completion_summary": "Completed"
    }
  ],
  "missing_asset_projects": [
    { "project": "Epsilon HR", "project_id": "a0Y...", "account": "Epsilon SA" }
  ],
  "membership_issues": [
    { "project": "Iota Corp", "channel_id": "C02...", "issue": "comercial SF no está en el canal" },
    { "project": "Kappa Co", "channel_id": "C03...", "issue": "user con dominio cliente detectado" }
  ],
  "inaccessible_channels": [
    { "project": "Lambda Co", "channel_id": "C04...", "reason": "PM no es miembro" }
  ],
  "cta_buttons": [
    {
      "id": "link_existing",
      "visible_if": "missing_asset > 0",
      "label": "Buscar y linkear canales Slack existentes para los {missing_asset} sin asset",
      "icon": "🔗",
      "intent": "Para cada uno de los proyectos sin Project_Asset__c, corre Paso 3A.0 del skill pc-delivery-slack-channel-auditor: busca en Slack candidatos por account+project slug+alias, muéstrame por widget los matches con opción de linkear el existente o crear nuevo, uno proyecto por vez."
    },
    {
      "id": "onboard_missing",
      "visible_if": "missing_asset > 0",
      "label": "Onboardear (crear) los {missing_asset} canales faltantes",
      "icon": "🔧",
      "intent": "Arranca el onboarding de los canales faltantes uno por uno con widget de aprobación. Empieza siempre con Paso 3A.0 (buscar existente) antes de Paso 3A.1."
    },
    {
      "id": "drafts_r0",
      "visible_if": "r0_red > 0",
      "label": "Generar drafts de status para los {r0_red} en R0",
      "icon": "✍",
      "intent": "Genera los drafts de status R0 con un widget por draft (no postees nada)."
    },
    {
      "id": "dm_follow_up",
      "visible_if": "is_manager_audit && r0_filtered_for_dm > 0",
      "label": "Armar DM de seguimiento al PM ({r0_filtered_for_dm} canales sin update)",
      "icon": "💬",
      "intent": "Corre Fase 7 del skill pc-delivery-slack-channel-auditor: arma el draft del DM conversacional al PM auditado con todos los canales >=7d sin status, bloqueos del cliente y fechas hipotéticas de golive. Muéstralo en widget de aprobación. NO mandes nada hasta que apruebe explícitamente."
    },
    {
      "id": "update_sf_from_channels",
      "visible_if": "audited_channels > 0",
      "label": "Actualizar SF desde los canales ({audited_channels} proyectos, últimos 14 días)",
      "icon": "🔄",
      "intent": "Corre Fase 9 del skill pc-delivery-slack-channel-auditor: para los {audited_channels} proyectos auditados, lee los posts del PM auditado en cada canal externo de los últimos 14 días, extrae con askClaude los valores mapeables a campos de Salesforce (Estimated_Go_Live__c, Status__c, Completion_Summary__c, Priority__c, etc.), compara con los valores actuales y muéstrame un widget checklist con todos los diffs propuestos para que apruebe lo que quiera aplicar. NO ejecutes updateSobjectRecord hasta que apruebe via [Aplicar N updates]."
    },
    {
      "id": "invite_comercial",
      "visible_if": "missing_comercial_sf > 0",
      "label": "Invitar al comercial SF en los {missing_comercial_sf} pendientes",
      "icon": "📨",
      "intent": "Invita al comercial SF en los canales que lo tengan faltante, uno por uno con aprobación."
    },
    {
      "id": "client_anomaly",
      "visible_if": "client_anomaly > 0",
      "label": "Revisar las {client_anomaly} anomalías de cliente",
      "icon": "⚠️",
      "intent": "Muéstrame el detalle de las anomalías de cliente detectadas para que decida acción."
    },
    {
      "id": "diag_inaccessible",
      "visible_if": "inaccessible > 0",
      "label": "Diagnosticar los {inaccessible} canales inaccesibles",
      "icon": "🔍",
      "intent": "Diagnostica los canales inaccesibles y propón fix por proyecto."
    },
    {
      "id": "rerun",
      "visible_if": "always",
      "label": "Re-correr la auditoría con otros parámetros",
      "icon": "🔄",
      "intent": "Reabrí el widget de Fase 0 para que ajuste PM, threshold o modo."
    }
  ]
}
```

**Cálculo de `r0_filtered_for_dm`** (v2.5+): la cantidad de filas que cumplen
`rule == "R0"` Y `last_pm_post_days >= 7`. La condición `>=7` es redundante
con R0 actualmente pero queda explícita para que el filtro de Fase 7 sea
trazable (si en el futuro R0 cambia a >5d, este filtro se mantiene en 7d
como pide el spec del DM).

**`is_manager_audit`** = `caller_email != pm_email` — controla la
visibilidad del CTA `dm_follow_up`.

**Orden de `rows`**: descendente por `last_pm_post_days`. Desempate:
prioridad (🔴>🟡>⚪) → alfabético por project.

**`cta_buttons`** se genera en este paso (no en el render). Cada botón tiene
`visible_if` evaluable contra `summary` + flags (`is_manager_audit`), `label`
con placeholders `{key}` que se reemplazan al render, e `intent` que es el
prompt que dispara `sendPrompt`.

#### Paso 5.2 — Render del widget único

> **Arma este widget componiendo los bloques de `references/widget-shell.md`
> (cárgalo primero). Cero HTML inventado, cero colores hardcoded, cero emoji.**

Llama `mcp__visualize__show_widget` una sola vez, con `title` =
`audit-canales-externos-<pm-slug>-<YYYY-MM-DD>`. Compón **estas cuatro
secciones en orden**:

**Sección A · `header-card`** — título "Auditoría de canales externos" + pares:
PM auditado + email · Fecha · Thresholds (R0=7d default) · Modo (diagnóstico /
+onboarding / +drafts / +dm follow-up). Badge `👥 Modo manager — caller:
<caller_email>` si `is_manager_audit == true`.

**Sección B · `kpi-grid`** — cards: `scanned_projects` (neutro) · `r0_red`
(danger) · `missing_asset` (warn) · `missing_comercial_sf` (warn) ·
`client_anomaly` (danger) · `inaccessible` (warn) · `ok` (success) ·
`finished_recently` (neutro). El color del border-left lo define el bloque
`kpi-grid` según la semántica.

**Sección C · `data-table` con add-ons multi-select + kebab + filtros (v2.7+)**

TODAS las filas de `rows` + las filas sintéticas de `missing_asset_projects`,
`membership_issues`, `inaccessible_channels` y `finished_recently_rows`
(estas últimas con `rule` = `MISSING_CHANNEL` / `MEMBER_ISSUE` / `INACCESSIBLE` /
`FINISHED` y `priority` = `yellow`, `red` o `gray` según corresponda).
Columnas:

| ☐ | Prio | Tipo | Project | Account | Canal | DM | Regla | last_pm_post_days | days_inactive | comercial SF | Anomalía cliente | Status | Bloqueo cliente | ⋮ |

Todos los badges salen del bloque `badges` del shell (íconos Tabler, sin
emoji).

- **☐** (primera columna): checkbox por fila para multi-select. Header
  de la columna es un master checkbox que tilda/destilda todas las filas
  visibles (respetando filtros activos).
- **Prio** (segunda columna): número entero (`audit.rows[i].priority`).
  `priority <= 2` → badge "Prioridad alta" (`ti-flame`, rol danger);
  `priority <= 5` → badge naranja "P{n}" (rol warning); el resto texto plano.
- **Tipo** (tercera columna, v2.8+): badge según `project_type` — Delivery
  (`ti-rocket`) o Support (`ti-lifebuoy`).
- **DM** (v2.13+): cantidad de menciones del proyecto en el DM 1:1 caller↔PM
  de los últimos 30 días, con ícono `ti-message`. Si > 0, link clickeable que
  abre un popover/modal con los extractos. Si `dm_highest_sensitivity = 'high'`,
  suma ícono `ti-lock` al lado. Si la Fase 2.5 no corrió (toggle apagado o
  self-audit) → mostrar "—".
- **Canal** debe renderizarse como un enlace clickeable usando el patrón
  `<a href="slack://channel?id={channel_id}">#nombre</a>`. Para filas de
  tipo `MISSING_CHANNEL` donde no hay `channel_id`, mostrar "—".
- **⋮** (última columna): icono kebab (`ti-dots-vertical`) por fila que abre un
  dropdown con acciones individuales (ver "Kebab por fila" abajo).

Las columnas **Status** y **Bloqueo cliente** (v2.5+) usan ícono Tabler + texto
(ver bloque `badges`):
- Status: Completo (`ti-check`) / Incompleto (`ti-alert-triangle`) / Falta (`ti-x`)
- Bloqueo cliente: No vino a meet (`ti-calendar-off`) / No responde
  (`ti-volume-off`) / No define temas (`ti-edit-off`) / No entrega pendings
  (`ti-package`) / "—" (none)

**Orden default de la tabla**: ASC por `priority`, luego DESC por
`last_pm_post_days`, luego alfabético por project. Click en header de
columna permite reordenar.

**Filtros inline**: input de búsqueda libre + select de prioridad + select de
"bloqueo de cliente" + select de "Status SF" (Ongoing/Stopped/On Hold/...) +
select de "Tipo" (Todos / Delivery / Support, v2.8+). JS vanilla. **No**
dependas de Grid.js ni librerías externas — keep it self-contained.

**Action bar al pie de la tabla (v2.7+)**

Debajo de la tabla, una barra de acciones globales que opera sobre las
filas tildadas en la columna ☐:

```
☐ N filas seleccionadas
[ Marcar como Completed ]  [ Cambiar Status a Ongoing ]  [ Cambiar Status a Stopped ]  [ Limpiar selección ]
```

Comportamiento:
- Si N=0, todos los botones de acción están deshabilitados con tooltip
  "Tilda al menos una fila".
- Click en cualquier acción NO ejecuta inmediatamente — dispara
  `sendPrompt(...)` con un intent que arranca el flujo de confirmación
  vía widget (sigue REGLA DE SEGURIDAD: nada se escribe en SF sin
  aprobación expresa por widget de confirmación). Intent de ejemplo:

  ```
  "Confirma los siguientes proyectos antes de cambiarlos a Status='Stopped':
  Project A (a0X...), Project B (a0Y...), Project C (a0Z...). Muéstrame
  un widget de aprobación uno por uno, y si confirmo todos, ejecuta el
  update via updateSobjectRecord."
  ```

- **Marcar como Completed** → llama a `updateSobjectRecord` por cada
  Project__c con `Completion_Summary__c = 'Completed'`. Excluye filas
  sintéticas (MISSING_CHANNEL / MEMBER_ISSUE / INACCESSIBLE / FINISHED).
- **Cambiar Status a Ongoing** → `Status__c = 'Ongoing'` (verificar el
  valor exacto del picklist en la org vía `getObjectSchema` antes de
  habilitar la acción la primera vez).
- **Cambiar Status a Stopped** → `Status__c = 'Stopped'` ídem.
- **Limpiar selección** → destilda todas las filas.

**Cada acción de escritura sigue la regla checklist (v2.6)** — el flujo
disparado por el `sendPrompt` muestra un widget con la lista de proyectos
afectados como checkboxes (todos tildados por default), permitiendo
destildar antes de confirmar el batch.

**Kebab por fila (v2.7+)**

Click en `⋮` abre un dropdown con:

| Acción | Comportamiento |
|---|---|
| Marcar como Completed | Igual que la acción global pero para esa sola fila. Dispara widget de confirmación de 1 ítem. |
| Cambiar Status a Ongoing | Idem, individual. |
| Cambiar Status a Stopped | Idem, individual. |
| Cross-check Jira | Dispara **Fase 8** (ver sección dedicada). Solo se habilita si la fila tiene `Project_Asset__c` de tipo `JiraBoardId` o `JiraProjectKey`. |
| Actualizar SF desde el canal (v2.11+) | Dispara **Fase 9** pero acotada a este proyecto. Lee los posts del PM en este canal de los últimos 14 días, extrae los campos mapeables y muestra el widget de diff solo para esta fila. |
| Verificar repo de código (v2.12+) | Dispara **Fase 10**. Lee `Project_Asset__c` con tipos de repo (`BitbucketRepoSlug`, etc) y consulta commits recientes en Bitbucket. Si no hay asset o no hay actividad, ofrece armar un DM al PM. Siempre disponible — si no hay asset, el widget igual permite accionar. |
| Abrir Project en SF | Abre `https://<sf-instance>/lightning/r/Project__c/<project_id>/view` en una nueva tab. |
| Abrir canal en Slack | `slack://channel?id={channel_id}` en nueva tab. |

Las acciones de escritura del kebab también disparan `sendPrompt(...)` —
nunca ejecutan inline. La regla de seguridad obliga a que TODA escritura
pase por un widget de confirmación, incluso para 1 fila.

**Sección D · `button-row` con los CTAs**
Itera `audit.cta_buttons`; para cada uno cuya condición `visible_if` evalúe
true contra `summary` + flags top-level, render un botón del bloque
`button-row` con `onclick="sendPrompt('<intent>')"`. Reemplaza los
placeholders `{key}` del label antes de pintarlo. Si **ningún** CTA es visible
(todo en verde, edge case raro), muestra "Todo OK, no hay acción pendiente".

**Prohibido**: renderizar `<ol>`/`<ul>` de "próximos pasos" (solo botones con
`sendPrompt`); llamar `mcp__cowork__create_artifact` además del widget (es UNO
u otro, v2.2.0 elige widget).

#### Paso 5.3 — Mensaje en chat

Después de renderizar el widget, **una sola línea** de texto en chat:

```
Auditoría lista — {r0_red} R0 roja, {missing_asset} sin canal, {ok} OK.
```

Si `r0_red > 0`, agrega a continuación los canales afectados **uno por línea**,
con formato `<#CHANNEL_ID>` seguido de cuántos días hace que el **owner del
proyecto** (= `Project__c.OwnerId`) no postea un mensaje top-level en el canal.

**Campo a usar: `last_pm_post_days`** — días desde el último post top-level
cuyo autor es el Owner. Es el mismo campo que dispara R0. **No usar
`days_inactive`** (ese mide actividad general del canal, de cualquier miembro).

```
R0 roja en:
<#C01234567> — owner sin posts hace 31 días
<#C07891011> — owner sin posts hace 12 días
<#C01121314> — owner nunca posteó en este canal
```

Si `last_pm_post_days` es `null` (owner nunca posteó en la ventana visible),
muestra "owner nunca posteó en este canal" y pon ese canal al tope de la lista.
Ordena descendente por `last_pm_post_days` (más inactivo primero).

Sin bullets, sin "Próximos pasos:", sin "¿Quieres...?". Todo eso vive
dentro del widget que ya se rindió arriba.

### Fase 6 — Drafts de status (checklist + widget por draft seleccionado, v2.6+)

Solo si el caller lo pidió en Fase 0 modo "diagnóstico + drafts de status",
o lo pide después de ver el widget de output (clickeando el CTA
`drafts_r0` de Fase 5.2).

**Paso 6.1 — Checklist de proyectos con draft propuesto**

Antes de mostrar drafts individuales, render UN widget de selección con el
bloque `checklist-block` del shell (ver `references/widget-shell.md`):

```
Tengo drafts de status para estos proyectos en R0 — destilda los que no
quieras armar:

☑ <Project A> · <#CHANNEL_A> — owner sin posts hace 45 días
☑ <Project B> · <#CHANNEL_B> — owner sin posts hace 18 días
☑ <Project C> · <#CHANNEL_C> — owner sin posts hace 9 días
☑ <Project D> · <#CHANNEL_D> — owner nunca posteó       ⚠️

[Generar N drafts seleccionados]   [Cancelar]
```

Default: todos tildados (incluido los que tienen `last_pm_post_days = null`,
marcados con ⚠️ pero no destildados automáticamente). El contador del
botón se actualiza en vivo. Si N=0, el botón queda deshabilitado.

**Paso 6.2 — Widget individual por draft seleccionado**

Para cada proyecto que quedó tildado en Paso 6.1, render **un widget
separado** (`header-card` + draft + `button-row`) con:
- Project + `last_pm_post_days` (días sin posts del owner)
- Draft pre-llenado usando `references/draft-templates.md` (template
  "status para comercial SF": avance del sprint, hitos, próximas fechas)
- El draft referencia el canal propio con `<#CHANNEL_ID>`
- Botones: [Copiar al portapapeles] [Editar] [Cerrar]

Cada draft individual no es un checklist (es un mensaje único destinado
a postear en el canal externo, lo cual es alto riesgo) — por eso se
mantiene el flujo widget-por-draft del v2.0.

**Reglas de formato estrictas para los drafts:**

1. **Un proyecto por línea, siempre.** Nunca agrupes dos proyectos en la
   misma línea aunque tengan algo en común (ej: "brm y clínica urbana" está
   mal — son dos líneas separadas).

2. **Cada canal va con sus días de inactividad del owner.** El formato es:
   ```
   <#CHANNEL_ID> — owner sin posts hace N días
   ```
   Nunca listar un canal sin su contador. Si `last_pm_post_days` es null,
   usar "owner nunca posteó".

3. **Orden descendente por `last_pm_post_days`** — el más inactivo primero.

Ejemplo correcto de lista en un draft o resumen:
```
<#C01234567> — owner sin posts hace 45 días
<#C07891011> — owner sin posts hace 12 días
<#C01121314> — owner sin posts hace 8 días
<#C01415161> — owner nunca posteó
```

Ejemplo incorrecto (nunca hacer esto):
```
<#C01234567> y <#C07891011> — sin actividad reciente
brm y clínica urbana — proyectos nuevos
```

**El widget NO postea nada**. El draft se muestra para copiar.
El PM pega el texto en Slack y los `<#...>` se resuelven automáticamente
como links clickeables.
Repite la regla de seguridad si el caller pide postear directamente.

### Fase 7 — DM follow-up al PM auditado (v2.5+, solo modo manager)

**Audiencia:** el PM auditado (Owner del Project__c), no el comercial SF.
**Sender:** el caller (manager). El DM se envía desde la cuenta Slack del
caller (Ariel típicamente) al canal DM 1:1 con el PM.

**Trigger:** click en el CTA `dm_follow_up` del widget de Fase 5.2, o el
caller eligió "diagnóstico + DM follow-up al PM" en Fase 0.

**Precondiciones:**
- `is_manager_audit == true` (caller ≠ Owner). Si no se cumple, este flow
  no se ofrece. Si el caller intenta forzar, responder en chat: "No tiene
  sentido auto-DM-arse. Si quieres una nota interna con la misma info, te
  la armo como texto sin enviar nada".
- `r0_filtered_for_dm > 0`. Si no hay nada que pedir, no armar DM (el PM
  está al día).

**Paso 7.1 — Detectar si es el primer DM del día**

- Buscar el canal DM 1:1 entre `caller_email` y `pm_email` (vía
  `slack_search_users` → `id`, luego `im.list` o equivalente).
- Leer los últimos N msgs (limit 5) de ese DM.
- `is_first_dm_today` = `true` si:
  - El último msg del caller en ese DM es de un día calendario anterior
    (zona horaria del caller, default America/Argentina/Buenos_Aires).
  - O nunca hubo DM previo.
- `is_first_dm_today` = `false` si:
  - Hay al menos un msg del caller hoy.

Esto define si el draft abre con "¿Cómo estás, <PM>?" o va directo al pedido.

**Paso 7.2 — Filtrar, agrupar y ordenar canales a incluir**

Si el set filtrado de abajo queda vacío → no se arma ningún DM (el PM está al
día). Caller ve "El PM está al día, no hay que mandar nada".

De `audit.rows`, tomar solo:
- `rule == "R0"` Y `last_pm_post_days >= 7` — **excluir** los que tienen
  status posteado hace <7 días.
- Más los que tengan `status_completeness == "incomplete"` aunque tengan
  posts recientes (status compartido pero sin golive o sin próximos pasos).

**Agrupación por cuenta (v2.7+):**

Antes de ordenar, agrupar los ítems filtrados por `account_id`. Si una
cuenta tiene **>=2 proyectos** en la lista filtrada, esos canales se
empaquetan en un "Account Group" y se renderizan en el DM bajo un header
de cuenta:

```
Para <Account.Name> tienes N proyectos activos sin update completo,
pásame el status de los N:
<#CHANNEL_A> — hace 31 días sin status (P1)
<#CHANNEL_B> — hace 18 días sin status (P3)
<#CHANNEL_C> — status del 25/05 sin golive (P5)
```

Si una cuenta tiene 1 solo proyecto en la lista, se renderiza standalone
(sin header de cuenta).

**Orden (v2.7+):**

Aplicar al set agrupado:
1. Primero **Account Groups con priority mínima del grupo <=2** (alta
   prioridad en algún proyecto de la cuenta).
2. Después ítems standalone con `priority <=2`.
3. Después `status_completeness == "incomplete"` independientemente de
   priority (el PM hizo el esfuerzo de postear, vale empujarlo a cerrar).
4. Después por `priority ASC`, luego `last_pm_post_days DESC`.
5. Ítems con `priority >=10` van al fondo, antes de finalizados.
6. Desempate alfabético por project name.

**Paso 7.3 — Compilar bloqueos del cliente por canal**

**Identificación del responsable externo (v2.15+):**

Para cada canal con `client_blocker != none`, antes de armar la frase del
bloqueo el skill identifica al **responsable externo a empujar**. Fuentes
de búsqueda:

- Últimos 10 msgs del canal externo: nombres propios mencionados por el
  PM ("Juan Pérez no nos respondió", "esperando a María del equipo de
  IT", etc.).
- Menciones del DM 1:1 (Fase 2.5) si están disponibles.
- Si no hay nombre explícito, identificar el ROL ("el referente del
  cliente", "el sponsor", "el área de marketing del cliente", "el
  consultor externo").

Persistir en `row.client_blocker_responsible` (string, default
"el referente del cliente").

**Frase del bloqueo (actualizada v2.15):**

Para cada canal de la lista filtrada con `client_blocker != none`, generar
una línea de bloqueo:

| Enum | Frase a usar |
|---|---|
| `no_meet_attendance` | "el cliente no se subió al último meet" |
| `no_response` | "el cliente todavía no nos contestó" |
| `no_scope_definition` | "el cliente no termina de definir los temas" |
| `no_pendings_delivery` | "el cliente tiene pendientes sin entregar" |

Si hay `hypothetical_golive_week`, agregarla: "si lo destrabamos esta
semana, la fecha tentativa de golive sería semana del **<lunes de esa
semana>**".

**Paso 7.4 — Detectar proyectos finalizados recientemente**

De la query auxiliar (Fase 1 — proyectos con `Completion_Summary != null`
en últimos 30 días del PM), incluir cada uno como línea aparte en el draft
con su `completion_date`.

**Paso 7.4.c — Generar sugerencia por proyecto (v2.15+)**

Para cada item incluido en el DM, generar una **sugerencia concreta de
acción** que va debajo del bullet del proyecto en el formato:

```
<#CHANNEL_ID> — Pn · <contexto>
  → Sugerencia: <acción puntual>
```

La sugerencia se compone con una mini-llamada a Haiku que recibe el
contexto del proyecto (last_pm_post_days, client_blocker,
status_completeness, recent_golive, mentioned_module, project_type,
client_blocker_responsible) y devuelve una oración de 1 línea (≤140
chars) accionable.

La **tabla de reglas por situación**, el **tono** (hereda las reglas
inviolables de Fase 7) y los **casos especiales** (bloqueo interno a PC,
múltiples blockers, fallback si Haiku falla) viven en
`references/dm-follow-up-template.md` (sección "Sugerencia por proyecto").
No inventar nombres de responsables externos: usar el rol genérico si no hay
nombre claro.

**Persistencia:**

Cada row gana `row.dm_suggestion` (string) en Fase 4. Esto se enchufa
directo en el template bajo cada línea de proyecto.

**Paso 7.4.b — Integrar contexto del DM 1:1 (v2.13+)**

Antes de armar el draft, para cada ítem incluido en el DM follow-up,
chequear `row.dm_mentions_in_window`:

- Si el PM ya dijo en DM cosas relevantes sobre ese proyecto en los
  últimos 30 días → **NO repreguntar** lo mismo. En lugar de pedir
  "pásame el status de X", el draft debe acknowledgear ("Como me
  comentaste el otro día sobre X, dale tranquilo — me avisas cuando
  cierres el sprint").
- Para cada mención, la frase de acknowledgement se genera con
  paráfrasis amable, NO cita textual. La cita textual queda en el
  widget de auditoría (que solo ve el caller) — el DM de respuesta usa
  paráfrasis para evitar volcar exactamente lo que el PM escribió en
  privado (regla de privacidad).
- Si un proyecto tiene `dm_highest_sensitivity = 'high'`, el skill
  agrega una nota interna en el widget de aprobación del DM (Paso 7.6)
  recordándole al caller que ese tema es sensible y conviene revisar
  la paráfrasis con cuidado antes de enviar.

**Paso 7.5 — Armar el draft**

El template del DM vive en **`references/dm-follow-up-template.md`** (cárgalo
para armar el draft): bloques Delivery / Support / Bloqueos del cliente /
Finalizados + cierres por tipo + sub-bloque "recién en producción" + catálogo
de métricas por módulo.

El mismo reference tiene las **banned phrases con justificación** (valida el
draft contra ellas antes de mostrarlo: una banned phrase bloquea el render) y
las reglas de tono de la sección de alta prioridad. El cierre del DM **NO**
consulta Jira automáticamente (pedido genérico Sprint 0 / sprint actual); el
cross-check contra Jira se hace después vía la acción kebab de Fase 8.

**Paso 7.6 — Widget de aprobación con checklist (v2.6+)**

Se arma con el bloque `checklist-block` del shell (`references/widget-shell.md`):
dos paneles lado a lado (o stack vertical en mobile), `header-card` arriba y
`button-row` al pie.

**Panel izquierdo · Checklist de ítems propuestos**

Cuatro secciones, cada una con su lista de checkboxes (todos tildados por
default):

```
☑ Sección 1 · Status incompletos
  ☑ <#CHANNEL_X> — status del 22/05 sin golive          ✎
  ☑ <#CHANNEL_Y> — status del 20/05 sin próximos pasos  ✎

☑ Sección 2 · Sin status (>=7 días)
  ☑ <#CHANNEL_A> — hace 31 días sin status              ✎
  ☑ <#CHANNEL_B> — hace 18 días sin status              ✎
  ☑ <#CHANNEL_C> — hace 9 días sin status               ✎

☑ Sección 3 · Bloqueos del cliente
  ☑ <#CHANNEL_A> — el cliente todavía no nos contestó.
    Si destrabamos esta semana, golive tentativo: 22/06  ✎
  ☑ <#CHANNEL_B> — el cliente no termina de definir
    los temas. ¿Te ayudo a empujar?                     ✎

☑ Sección 4 · Proyectos finalizados a dar de baja        ⚠️
  ☑ <#CHANNEL_FIN_1> — finalizó el 12/05                ✎
  ☑ <#CHANNEL_FIN_2> — finalizó el 03/05                ✎
```

Cada checkbox individual + el checkbox de sección (que actúa como
master/tilda-todo-o-destilda-todo de su sección). El icono `✎` al lado de
cada línea abre un mini-input inline para tweakear la línea sin tocar el
draft entero.

**Panel derecho · Preview live del DM**

Renderiza el texto final del DM tal cual va a salir a Slack, regenerado
desde cero cada vez que cambia un checkbox o se edita una línea. Incluye:
- Apertura (¿cómo estás? si aplica)
- Las secciones cuyos ítems quedaron tildados
- Cierre con golive + próximos pasos + sprint
- Despedida

Si una sección entera quedó destildada, se omite del DM (no se renderiza
el header de la sección sin items).

**Header (`header-card`)**
- Título "Draft de DM para `<PM_NAME>`"
- Pares: caller · hora estimada de envío · badge `is_first_dm_today` si aplica
- Contador: "**N items seleccionados** de M propuestos"

**Botonera**

| Botón | Comportamiento | Habilitado si |
|---|---|---|
| Aprobar y enviar DM con **N items** | `slack_send_message` al DM 1:1 con el texto del preview | N ≥ 1 |
| Solo copiar al portapapeles | Muestra el texto del preview en `<pre>` + `navigator.clipboard.writeText`. No envía. | N ≥ 1 |
| Cancelar | Cierra el widget sin enviar | siempre |

**El send se hace UNA sola vez tras click explícito sobre el botón habilitado.
Nunca antes. Si N = 0 el botón está deshabilitado con tooltip "No hay items
seleccionados — destildaste todo, ¿quieres cancelar?".**

**Edición inline (icono ✎)**

Al click en el `✎` de un ítem, ese ítem entra en modo edición: la línea
se reemplaza por un `<input type="text">` con el texto actual, más botones
[Guardar] y [Cancelar edit]. Al guardar, el texto se actualiza en el panel
izquierdo Y se rerenderiza el preview live. Edición no afecta el checkbox
(queda tildado).

**Edición del cierre y la apertura**

El cierre (golive + sprint + próximos pasos) y la apertura (¿cómo estás?)
no son checklist — son partes fijas del DM. Pero hay un botón "Editar
apertura" / "Editar cierre" debajo del preview que abre un textarea
modal para tweakearlos. Default = el texto generado en Paso 7.5.

**Paso 7.7 — Confirmación post-envío**

Después de enviar, render un mini-widget con:
- `ti-circle-check` "Enviado a <PM_NAME> a las <HH:mm>"
- Botón [Marcar en Salesforce] → opcional: crear un Task en el PM en SF
  con subject "Manager follow-up sent" para auditoría
- Botón [Cerrar]

NO posteas en chat el contenido del DM enviado (queda en el widget). Solo
una línea de confirmación: "DM enviado a <PM_NAME>".

**Paso 7.8 — Si el caller decide no enviar**

Si elige [Solo copiar al portapapeles], renderiza el draft en `<pre>` con
un botón "Copiar texto" usando `navigator.clipboard.writeText(...)`. No
llames a `slack_send_message`. Confirmación: "Listo, el draft quedó arriba
para que lo copies."

### Fase 8 — Jira cross-check on demand (v2.7+)

**Trigger único:** click en la acción "Cross-check Jira" del kebab `⋮` de
una fila puntual en la tabla de Fase 5.2. **NO** se dispara automáticamente
desde Fase 3B, Fase 5, Fase 6 ni Fase 7. La regla es: Jira solo se
consulta cuando el caller lo pide expresamente, fila por fila.

**Precondición bloqueante:**
- La fila debe tener `Project_Asset__c` de tipo `JiraBoardId` o
  `JiraProjectKey` registrado en el proyecto. Si no lo tiene, el kebab
  muestra la acción deshabilitada con tooltip "Falta Project_Asset__c
  JiraBoardId — no puedo cross-checkear contra Jira".

**Paso 8.1 — Resolver el proyecto Jira**

Leer el `Project_Asset__c.Value__c` correspondiente:
- Si `Type__c = JiraBoardId` → board ID directo.
- Si `Type__c = JiraProjectKey` → buscar el board(s) asociado al project
  key vía `/rest/agile/1.0/board?projectKeyOrId=<key>`.

Si hay múltiples boards para el mismo project key, renderizar un widget
de selección para que el caller elija cuál usar (caso scrum + kanban
paralelos, por ejemplo).

**Paso 8.2 — Recolectar el estado en Jira**

Para el board elegido, traer:

| Dato | Endpoint | Comentario |
|---|---|---|
| Sprint(s) activo(s) | `/rest/agile/1.0/board/{boardId}/sprint?state=active` | Soporta múltiples sprints simultáneos. |
| Sprint próximo (future) | `/rest/agile/1.0/board/{boardId}/sprint?state=future` | Solo el más cercano por start date. |
| Issues del sprint activo | `/rest/agile/1.0/sprint/{sprintId}/issue` | Filtrar a Status not in (Done, Closed). |
| Releases (versions) del proyecto | `/rest/api/3/project/{projectKey}/versions` | Filtrar a released=false. |
| Issues pendientes "externos" | JQL `project = <key> AND issuetype = "External pending" AND status != Done` | Para cruzar con los bloqueos del cliente que el PM mencionó en el canal. |

Limitar cada llamada por paginación razonable (50 items max). Si alguno
falla por permisos del conector, capturar el error y reportar en el
widget de output ("No accedí a releases del proyecto X — chequea el
permiso en el conector Atlassian") sin abortar el resto.

**Paso 8.3 — Recolectar lo que el PM dijo en el canal**

Leer los últimos 10 mensajes top-level del canal externo + sus threads,
filtrando a los autorizados por `Owner.Email`. Pasarlos a
`window.cowork.askClaude` con un prompt extractor:

```
Extrae del siguiente texto de Slack las afirmaciones del PM sobre:
- Sprint actual (nombre, número, fecha de fin estimada).
- Sprint próximo (si lo mencionó).
- Releases/lanzamientos planeados (nombre, fecha).
- Pendientes del cliente (descripción, status).
- Próximas tareas / hitos.
- Fecha estimada de golive.

Devuélveme JSON con las claves: current_sprint, next_sprint, releases[],
client_pendings[], next_tasks[], golive_date. Si algo no se menciona,
devuelve null. NO inferir cosas que el PM no dijo explícitamente.
```

**Paso 8.4 — Comparar y armar discrepancias**

Por cada eje, comparar lo que dijo el PM vs lo que está en Jira:

| Eje | Match esperado | Discrepancia → |
|---|---|---|
| Sprint actual | Nombre + fecha de fin | "PM dijo Sprint X termina YY; Jira dice termina ZZ" |
| Sprint próximo | Si mencionó algo, debe estar en Jira como future | "PM mencionó Sprint Y pero no figura como future en Jira" |
| Releases | Cada release del PM debe existir en Jira | "PM mencionó release 1.2 pero no está en Jira; o existe pero released=true" |
| Pendientes del cliente | Cada pendiente del PM debe matchear un issue "External pending" abierto | "Hay N pendientes del cliente en Jira que el PM no mencionó; o M pendientes que mencionó pero no existen en Jira" |
| Próximas tareas | Top issues del sprint activo no-Done | "PM mencionó tarea A pero no está en Jira; o tarea B está top del sprint pero el PM no la mencionó" |
| Fecha de golive | Si la mencionó, comparar con `Project__c.Estimated_Go_Live__c` | "PM dijo golive YY, SF dice ZZ" (esto cruza con SF, no Jira, pero queda en el mismo reporte) |

Cada discrepancia se clasifica (badge del bloque `badges`):
- **Crítico** (`ti-alert-triangle`, danger) — datos contradictorios (PM dijo X, sistema dice Y).
- **Faltante** (`ti-help-circle`, warning) — el PM no mencionó algo que está en Jira (o viceversa).
- **Informativo** (`ti-info-circle`, neutro) — match ok pero vale notar.

**Paso 8.5 — Render del widget de cross-check**

Render `mcp__visualize__show_widget` con `title =
jira-cross-check-<project-slug>-<YYYY-MM-DD>`, componiendo con los bloques del
shell (`references/widget-shell.md`):

**Sección A · `header-card`** — título "Jira cross-check" + pares: Project +
Account · Channel (link) · Jira board (name + URL) · Timestamp.

**Sección B · `kpi-grid` + `banner`** — cards: N críticos (danger) · N
faltantes (warn) · N informativos (neutro). Banner con el status general:
"Tienes cosas para reconciliar" (danger) / "Faltan menciones" (warning) /
"Todo cuadra" (success).

**Sección C · `data-table`** (base, sin add-ons) con columnas:

| Severidad | Eje | Lo que dijo el PM | Lo que dice Jira/SF | Sugerencia |
|---|---|---|---|---|

La severidad usa el bloque `badges` (Crítico / Faltante / Informativo). La columna "Sugerencia" propone
una micro-acción accionable, por ejemplo:
- "Pídele al PM que confirme la fecha de fin de sprint en el próximo update."
- "Marca el External Pending JIRA-123 como resuelto si ya entregó."
- "Actualiza `Estimated_Go_Live__c` en SF al 22/06 si la fecha del PM es la buena."

**Sección D · `button-row`**

- [Volver a la auditoría general] — vuelve al widget de Fase 5.2.
- [Armar DM al PM con estas discrepancias] — dispara una mini-fase
  derivada de Fase 7 que solo arma un DM puntual sobre este proyecto
  mencionando las discrepancias en tono de pedido ("para alinear lo que
  pasaste con lo que veo en Jira, ¿puedes confirmar X?"). Sigue todas las
  reglas de tono y aprobación de Fase 7.
- [Cerrar] — cierra el widget.

**Importante**: Fase 8 es READ-ONLY contra Jira. No crea, transiciona ni
modifica issues. Si una sugerencia involucra escribir en Jira (cerrar un
external pending, mover un sprint), tiene que dispararse por separado
mediante otro skill o flow — Fase 8 solo reporta.

### Fase 9 — Actualizar SF desde los canales (últimos 14 días, v2.11+)

**Trigger:** click en el CTA global `update_sf_from_channels` (Fase 5.2 
Sección D) → procesa **todos** los canales auditados. O click en la acción
kebab "Actualizar SF desde el canal" de una fila puntual → procesa **solo
ese** proyecto.

**Audiencia:** caller (cualquier rol). El skill propone — el caller aprueba
qué updates correr.

**Paso 9.1 — Detectar campos disponibles en Project__c**

Una sola vez por sesión, llama `getObjectSchema('Project__c')` y arma un
catálogo de **campos updatables** que el skill sabe popular desde texto:

| Campo SF (si existe) | Origen del valor |
|---|---|
| `Estimated_Go_Live__c` | fecha de golive más reciente mencionada por el PM |
| `Status__c` | si el PM mencionó pausa, retomada, on hold, etc. — mapear al picklist real de la org |
| `Completion_Summary__c` | si el PM mencionó cierre del proyecto |
| `Priority__c` | si el PM mencionó cambio de prioridad |
| `Last_Status_Posted_Date__c` | timestamp del último post top-level del owner (si el campo existe) |
| `Notes__c` / `Description__c` | resumen ejecutivo del estado actual (1-2 oraciones generadas por Haiku) |

Campos que NO existen en la org → omitirlos del catálogo y no proponer
updates para ellos. Cualquier campo extra que la org haya agregado y
matche un patrón conocido (`*_Go_Live__c`, `*_Status__c`, etc.) puede
sumarse al catálogo con confirmación previa del caller la primera vez.

**Paso 9.2 — Leer posts de los últimos 14 días + DM (v2.13+)**

Para cada canal en scope, llama `slack_read_channel` con suficiente paginación
para cubrir 14 días calendario (estimar ~20-50 msgs según frecuencia del canal,
ajustar dinámicamente). Filtrar a mensajes top-level cuyo autor coincida con
`Owner.Email` del proyecto auditado (regla v2.7.1 — solo posts del PM auditado).

**v2.13+** — además del canal, sumar las menciones del proyecto en el DM 1:1
caller↔PM (ya extraídas en Fase 2.5, disponibles en `row.dm_mentions_in_window`).
Cada mención del DM se trata como una "fuente extra" del proyecto al evaluar
diff vs SF, con `source = 'dm'` en el JSON del extractor (vs `source = 'channel'`).

Si en 14 días NO hay ningún post del PM en el canal NI menciones en DM →
no se proponen updates para ese proyecto y se agrega al reporte como "sin
posts ni menciones en 14d, sin updates a aplicar".

**Paso 9.3 — Extraer valores con askClaude**

Por canal, una sola llamada a `askClaude` con el contenido de los posts
del PM en los últimos 14 días + el catálogo de campos disponibles:

```
Texto: <posts del PM, ordenados cronológicamente, ts + contenido>.

Catálogo de campos SF disponibles para este proyecto:
- Estimated_Go_Live__c (Date)
- Status__c (Picklist: Ongoing | Stopped | On Hold | Completed)
- Completion_Summary__c (Text)
- Priority__c (Number)
- Last_Status_Posted_Date__c (DateTime)
- Notes__c (Long Text)

Para cada campo, devuélveme JSON con:
- value: el valor extraído del texto (formato apropiado al tipo), o null si
  el PM no lo mencionó claramente.
- source_excerpt: la cita textual del post donde aparece (máximo 120 chars).
- confidence: "high" | "medium" | "low" según qué tan explícito fue el PM.
- mentioned_at: ts del post donde lo dijo.

Reglas estrictas:
- NO inferir. Si el PM no lo dijo, devolver value: null.
- Si dijo cosas contradictorias en posts distintos, usar el más reciente y
  mencionar la contradicción en source_excerpt.
- Para Status__c, normalizar al picklist exacto (case-sensitive del valor SF).
- Para Notes__c, generar 1-2 oraciones resumiendo el último estado posteado.
- Para fechas, devolver formato YYYY-MM-DD.
```

**Paso 9.4 — Computar diff vs valores actuales de SF**

Para cada (proyecto, campo) extraído con `value != null`, comparar con
el valor actual del campo en `Project__c`. Posibles estados:

| Estado | Cuándo | Tratamiento |
|---|---|---|
| `match` | extraído == SF actual | Skip (no proponer update — ya está al día). |
| `update` | extraído != SF actual, SF tiene valor | Proponer update con diff (valor actual → valor nuevo). |
| `fill` | extraído != null, SF está vacío | Proponer fill (vacío → valor nuevo). |
| `conflict` | extraído != null, SF tiene valor distinto Y confidence='low' | Proponer pero marcado como "revisar — confidence low". |

Resultado: array de proposed_updates con shape:

```json
{
  "project_id": "a0X...",
  "project_name": "BetaCorp Sales Cloud",
  "field_api": "Estimated_Go_Live__c",
  "field_label": "Estimated Go-Live",
  "current_value": "2026-07-15",
  "proposed_value": "2026-08-01",
  "source_excerpt": "movimos el golive a la primera semana de agosto",
  "confidence": "high",
  "mentioned_at": "2026-05-30T14:22:00Z",
  "state": "update"
}
```

**Paso 9.5 — Render del widget checklist con diff**

Render `mcp__visualize__show_widget` con `title =
sf-updates-from-channels-<pm-slug>-<YYYY-MM-DD>`, usando el bloque
`checklist-block` del shell (`references/widget-shell.md`) con `header-card` +
`button-row`:

**Layout: grupo por proyecto, dentro de cada grupo un row por campo**

```
☑ Proyecto: BetaCorp Sales Cloud · #ext-betacorp-salesforce
  ☑ Estimated_Go_Live__c       2026-07-15 → 2026-08-01   high  ✎
    💬 "movimos el golive a la primera semana de agosto"
  ☑ Status__c                  Ongoing → On Hold          high  ✎
    💬 "el cliente nos pidió pausarlo hasta julio"
  ☐ Priority__c                3 → 2                      low   ✎
    💬 "le subimos un poquito la prioridad" (confidence low — chequear)

☑ Proyecto: GammaCorp Migration · #ext-gammacorp-salesforce
  ☑ Last_Status_Posted_Date__c (vacío) → 2026-06-03T10:15  high
  ☑ Notes__c                   (vacío) → "Sprint 4 en curso, golive
                                          tentativo 22/06 si destrabamos
                                          definiciones del cliente."  medium
```

Reglas del widget:
- Todos los proyectos vienen **tildados** por default. El caller destilda
  los que quiere skipear.
- Cada campo dentro de un proyecto tiene su propio checkbox. Default
  tildado, **excepto** los con `confidence='low'` que vienen
  **destildados** (la fricción default es no aplicar low-confidence).
- Master checkbox del proyecto tilda/destilda todos sus campos.
- `✎` por campo abre un mini-editor para corregir el valor propuesto
  antes de aplicarlo (útil cuando el extractor casi acierta pero falta
  un detalle).
- Diff: valor actual en `--text-secondary`, flecha `→`, valor nuevo en
  `--text-primary` (más prominente). `source_excerpt` debajo en `--text-muted`
  con ícono `ti-message`. `confidence` como `badge` del shell
  (high→`c-teal`, medium→`c-amber`, low→`c-red`).

**Botonera al pie del widget:**

| Botón | Comportamiento | Habilitado si |
|---|---|---|
| Aplicar **N updates** | Itera los seleccionados y llama `updateSobjectRecord` por proyecto agrupando los campos en un solo PATCH | N ≥ 1 |
| Aplicar solo high confidence | Atajo — destilda automáticamente medium+low, deja solo high tildado | siempre |
| Exportar JSON sin aplicar | Descarga el array `proposed_updates` como JSON para revisión offline | siempre |
| Cancelar | Cierra el widget sin aplicar nada | siempre |

**Paso 9.6 — Aplicación**

Solo si el caller clickeó "Aplicar N updates":
- Agrupar los campos seleccionados por `project_id`.
- Por cada proyecto, una sola llamada `updateSobjectRecord` con todos los
  campos de ese proyecto en el mismo payload (más eficiente que un PATCH
  por campo).
- Si falla un update específico, capturar el error y mostrarlo en el
  reporte post-aplicación sin abortar los otros.
- Reporte final: widget compacto con "N proyectos actualizados, X
  campos aplicados, Y errores" (ícono `ti-circle-check`). Si hay errores, lista con
  project_name + field + error_message.

**Paso 9.7 — Edge cases**

- **PM no posteó nada en 14d para un proyecto**: skip silencioso, mencionar
  en el resumen post-Fase 9.
- **Conflict de timestamps**: si el PM dijo "el golive es el 15/07" el día
  10 y "movimos al 22/07" el día 25, usar el más reciente (25).
- **Picklist value inválido**: si el extractor devuelve un Status__c que
  no existe en la org (ej. "Activo" pero la org tiene "Ongoing"), marcar
  como `confidence='low'` y proponer el más cercano del picklist real.
- **Conflict con write reciente en SF**: si `Project__c.LastModifiedDate`
  es más reciente que el último post del PM en el canal, agregar warning
  "alguien actualizó SF después del último post del PM — revisa si el
  update propuesto sigue válido".

**Fase 9 es WRITE en Salesforce.** Como toda escritura en SF, requiere
aprobación explícita por widget. Nunca ejecutar `updateSobjectRecord`
sin click confirmado del caller.

### Fase 10 — Verificar repo de código + commits recientes (v2.12+)

**Trigger único:** click en la acción kebab "Verificar repo de código" de
una fila puntual en la tabla de Fase 5.2. **NO** se dispara automáticamente
desde otras fases — sigue la regla v2.7 de "consultas a sistemas externos
solo on demand".

**Paso 10.1 — Buscar Project_Asset__c de tipo repo**

Para el proyecto seleccionado, query SOQL acotada:

```sql
SELECT Id, Type__c, Value__c, Grouper__c
FROM Project_Asset__c
WHERE Project__c = '<project_id>'
  AND Type__c IN ('BitbucketRepoSlug', 'BitbucketWorkspaceRepoSlug',
                  'GitRepoUrl', 'CodeRepo')
```

El tipo recomendado para nuevas registraciones es `BitbucketRepoSlug` con
`Value__c` en formato `<workspace>/<repo-slug>` (ej.
`procontacto/repuestosboston-sf`). Los otros tipos se mantienen por
compatibilidad con assets viejos.

Tres caminos según el resultado:

**Camino A · Sin asset registrado (0 resultados)** → Paso 10.2.
**Camino B · Asset registrado** → Paso 10.3 (consulta Bitbucket).
**Camino C · Múltiples assets** → Widget de selección "Encontré N repos
registrados — ¿cuál quieres verificar?" con un botón por repo. El caller
elige y se procesa como Camino B.

**Paso 10.2 — Camino A: sin asset registrado**

Render widget rojo con:

```
🚫 No hay repo de código registrado en este proyecto
Project: <Name> · Account: <Account.Name>

El asset Project_Asset__c.Type__c con un repo (BitbucketRepoSlug,
GitRepoUrl, etc.) no existe para este proyecto. Esto puede significar:
  • El team todavía no armó el repo.
  • El repo existe pero nadie lo registró como asset en SF.
  • El proyecto no tiene componente de código (puro config, sin custom dev).

Opciones:
[ Armar DM al PM pidiendo creación del repo + commit inicial ]
[ Registrar un repo existente como Project_Asset__c (manual) ]
[ Marcar como "no aplica" — proyecto sin código ]
[ Cancelar ]
```

Si el caller elige "Armar DM al PM..." → salta a **Paso 10.6** con
template B (sin repo).

Si elige "Registrar repo existente" → widget con input "Workspace/repo
slug" + un Paso 10.2.b que persiste el `Project_Asset__c` con
`createSobjectRecord` luego de confirmación. Esto es WRITE en SF, requiere
aprobación explícita por widget.

Si elige "Marcar como no aplica" → opcionalmente persistir un asset
`Type__c = 'NoCodeRepo'` con `Value__c = 'true'` (también WRITE — requiere
aprobación) para que la próxima auditoría no vuelva a preguntar.

**Paso 10.3 — Camino B: consultar Bitbucket**

Con el `Value__c = '<workspace>/<repo-slug>'`, llamar al conector Bitbucket
(`bb_get`):

```
GET /repositories/{workspace}/{repo-slug}/commits
?include=master,main,develop&pagelen=50
```

Filtrar a commits con `date >= now - <commit_recent_days>` (default 7 días,
configurable por input en el widget). Capturar para cada commit:
- `hash` (short, 8 chars)
- `date` (ISO)
- `message` (primera línea)
- `author.user.display_name` (o `author.raw` si no hay user resolved)

Si Bitbucket devuelve 404 → el slug está mal o el repo no existe.
Mostrar widget de error con opción "Corregir el slug" (que actualiza
`Project_Asset__c.Value__c`) o "Marcar repo como inaccesible".

Si Bitbucket devuelve 403 → el conector no tiene permisos sobre ese
workspace/repo. Mostrar widget "Sin permisos para acceder al repo —
chequear que el conector Atlassian/Bitbucket tenga acceso al workspace
<workspace>".

**Paso 10.4 — Clasificar el resultado**

| Estado | Condición | Badge (bloque `badges`) |
|---|---|---|
| Activo | `commits_recientes.length >= 1` | success (`ti-circle-check`) |
| Poco activo | `commits_recientes.length == 0` pero `last_commit_overall` existe y es de menos de 30 días | warning (`ti-alert-triangle`) |
| Inactivo | `commits_recientes.length == 0` y `last_commit_overall` es de >30 días, o el repo nunca tuvo commits | danger (`ti-circle-x`) |

**Paso 10.5 — Render del widget de resultado (Camino B)**

Render `mcp__visualize__show_widget` con título
`repo-check-<project-slug>-<YYYY-MM-DD>`, componiendo con los bloques del shell
(`references/widget-shell.md`):

**Sección A · `header-card`** — título "Repo check" + pares: Project + Account ·
Repo (link a `https://bitbucket.org/<workspace>/<repo-slug>`) · Threshold
("últimos N días" + input para reajustar y re-correr). Badge de estado global
(Activo / Poco activo / Inactivo) del paso 10.4.

**Sección B · `kpi-grid`** — cards: "Commits en últimos N días" · "Autores
únicos" · "Último commit" (timestamp relativo) · "Branch principal" (master/main).

**Sección C · `data-table`** (base, sin add-ons), solo si hay commits:

| Hash | Fecha | Autor | Mensaje |

Cada hash linkea a `https://bitbucket.org/<workspace>/<repo-slug>/commits/<hash>`.

**Sección D · `button-row`**

Si estado = Activo:
- [ Cerrar ] — el repo está sano, no hay acción pendiente.

Si estado = Poco activo o Inactivo:
- [ Armar DM al PM pidiendo push de metadata + código ] → Paso 10.6.
- [ Ver historial completo en Bitbucket ] → abre link.
- [ Cerrar sin acción ].

**Paso 10.6 — Draft del DM al PM (template B o C)**

Sigue las reglas de tono y aprobación de Fase 7. Dos templates según el
escenario:

**Template B — sin repo registrado:**

```
[Si is_first_dm_today]
¡Hola <PM_FIRST_NAME>! ¿Cómo estás?

Quería pedirte una mano con un tema del proyecto <#CHANNEL_ID>.

Veo que todavía no tenemos registrado un repo de código en Salesforce
para este proyecto. ¿Puedes coordinar con el dev team para:

• Crear el repo en Bitbucket (workspace procontacto) siguiendo la
  convención de nombre.
• Hacer el commit inicial con la metadata y el código que se haya
  desarrollado hasta ahora.
• Una vez creado, pasarme el slug para registrarlo como
  Project_Asset__c en SF y mantenerlo trackeado.

Si ya está el repo armado y solo faltó registrarlo, dime el slug y
te lo cargo.

¡Gracias!
```

**Template C — repo sin actividad reciente:**

```
[Si is_first_dm_today]
¡Hola <PM_FIRST_NAME>! ¿Cómo estás?

Quería revisar contigo un punto del repo de <#CHANNEL_ID>:

Vi que <https://bitbucket.org/<workspace>/<repo-slug>|el repo> no tiene
commits hace <N días> (último commit <fecha> por <autor>).

¿Puedes coordinar con el dev team para hacer push de la metadata y el
código que tengan en sus orgs/locales? Es importante para mantener el
versionado al día y que el resto del team pueda colaborar.

Si hay algo que está trabando los commits (config del CI/CD, permisos
en el repo, branch protection) dime y vemos cómo destrabarlo.

¡Gracias!
```

**Reglas de tono inviolables** (aplica las mismas de Fase 7):

| ❌ NO usar | ✅ Sí usar |
|---|---|
| "tienen que commitear ya" | "¿puedes coordinar con el dev team para..." |
| "el team está fallando en commitear" | "el repo no tiene actividad reciente" |
| "es urgente que pusheen" | "es importante para mantener el versionado al día" |

**Paso 10.7 — Widget de aprobación del DM**

Igual que Paso 7.6 pero con el draft de Paso 10.6 ya armado en el
`<textarea>` editable. Botones:
- [ Aprobar y enviar DM ]
- [ Solo copiar al portapapeles ]
- [ Cancelar ]

Nunca enviar sin click explícito. Aplica todas las reglas de seguridad.

**Fase 10 es READ-ONLY contra Bitbucket.** No crea repos, no commitea, no
modifica nada. Solo lee commits, reporta el estado, y eventualmente arma
un draft Slack que el caller decide enviar o no.

---

## 📌 REGLA DE FORMATO — referencias a canales Slack

Esta regla aplica a **todo output del skill** que muestre o mencione canales
Slack: widgets, drafts de mensajes, resúmenes en chat, confirmaciones de
onboarding y el DM follow-up de Fase 7.

### Formato de referencia en mensajes Slack

Siempre que tengas el `channel_id` (formato `C01234567`), usa la notación
nativa de Slack en cualquier texto que sea copiado/enviado a Slack:

```
<#CHANNEL_ID>          → Slack lo renderiza como #nombre-del-canal clickeable
<#CHANNEL_ID|alias>    → si quieres forzar un alias legible
```

Ejemplos:
- ✅ `<#C01234567>` — se muestra como `#ext-betacorp-rollout` al pegar en Slack
- ✅ `<#C01234567|ext-betacorp-rollout>` — alias explícito
- ❌ `#ext-betacorp-rollout` — texto plano, no es clickeable en Slack

### Listado de múltiples canales — uno por línea

Cuando el output incluye más de un canal (draft, widget de confirmación,
resumen post-auditoría, DM follow-up), lista cada canal en su propia línea.
Nunca en línea separados por comas ni dentro de una misma oración.

```
✅ Correcto (un canal por línea):
Los canales con R0 roja son:
<#C01234567> — hace 31 días sin status
<#C07891011> — hace 18 días sin status
<#C01121314> — hace 9 días sin status

❌ Incorrecto (inline):
Los canales con R0 roja son: #ext-betacorp, #cc-gammacorp, #proy-delta
```

### En widgets HTML

Los widgets no procesan la sintaxis `<#CHANNEL_ID>` de Slack. En su lugar,
usa un enlace que abra el canal directamente en la app de Slack:

```html
<a href="slack://channel?id=C01234567" target="_blank">#nombre-del-canal</a>
```

Esto funciona en macOS y Windows con Slack instalado. Si no tienes el
`channel_id` (proyectos `MISSING_CHANNEL`), muestra el nombre en texto plano.

---

## Dependencias (MCPs requeridos)

- **Slack**: `slack_read_channel`, `slack_read_thread`,
  `slack_read_user_profile`, `slack_search_users`, `slack_search_channels`,
  `slack_send_message` (solo Fase 7, con aprobación obligatoria).
  Para onboarding además: tool de creación de canal e invitación de
  miembros (verificar disponibilidad en el turno — fallback en
  `references/channel-onboarding.md`).
- **Salesforce**: `soqlQuery`, `getObjectSchema`, `createSobjectRecord`,
  `updateSobjectRecord` (v2.7+ para las acciones de tabla — Completed /
  Ongoing / Stopped), `getUserInfo`.
- **Cowork**: `mcp__visualize__show_widget` para TODOS los inputs,
  aprobaciones, opciones, próximos pasos **y el output principal** (v2.2.0+).
  Ya no se usa `mcp__cowork__create_artifact` — el output entero (KPIs +
  tabla + CTAs) vive en un único widget. Fase 7 usa
  `window.cowork.askClaude` para detectar bloqueos del cliente con Haiku.
- **Atlassian (v2.7+, solo Fase 8 — Jira cross-check on demand)**: lectura
  read-only de board / sprints / issues / releases del proyecto Jira.
  Se invoca EXCLUSIVAMENTE cuando el caller dispara la acción kebab
  "Cross-check Jira" sobre una fila puntual. Si el conector no está
  autenticado, la acción kebab se muestra deshabilitada con tooltip
  explicativo. **Ningún otro flow consulta Jira** — la regla v2.7+ es
  "Jira on demand only".
- **Bitbucket (v2.12+, solo Fase 10 — Verificar repo de código on demand)**:
  lectura read-only de commits via `bb_get` sobre
  `/repositories/{workspace}/{repo-slug}/commits`. Se invoca
  EXCLUSIVAMENTE cuando el caller dispara la acción kebab "Verificar
  repo de código" sobre una fila puntual. Si el conector no está
  autenticado, la acción kebab muestra widget de error con instrucciones.
  **Ningún otro flow consulta Bitbucket** — misma regla "on demand only"
  que para Jira.

Si alguno no está autenticado, avisa al caller y frena el workflow. No
intentes workarounds — el caller autenticó explícitamente lo que está
autenticado.

---

## Errores comunes y cómo evitarlos

**Identidad y gate**
- `Project__c.OwnerId` es el **PM** (comercial nuestro), NO el comercial SF
  (externo, identificado por mail tipeado por el caller).
- El cliente final NO debe estar en el canal externo. Si aparece → bucket
  `client_anomaly`.
- Gate de vigencia = `Completion_Summary__c = null`. Nunca usar `Status__c`.
- Auditar siempre filtrando por PM (sus proyectos, o los de su equipo si es
  manager). No barrer todo PC sin filtro.
- Posts de bots PC (CI/CD webhooks) NO cuentan como "PM posteó". Ver
  `references/team-identification.md`.
- En canal compartido por varios PMs, `last_pm_post_days`/R0 se calculan SOLO
  con posts cuyo autor == `Owner.Email` del proyecto auditado. Ver "REGLA —
  canales compartidos por varios PMs".
- Un PM que solo escribió por DM (no en el canal externo) sigue gatillando R0
  — el DM no reemplaza el canal del comercial SF.

**Seguridad / escritura (ver REGLA DE SEGURIDAD + `safety-rules.md`)**
- Nunca postear, mandar DM, crear canal/invitar, ni `createSobjectRecord` /
  `updateSobjectRecord` sin aprobación explícita por widget — incluido el DM
  de Fase 7/10 y las acciones de tabla/kebab de Fase 5.2 y los updates de
  Fase 9. Las acciones de tabla disparan `sendPrompt`, nunca escriben inline.
- Toda opción/CTA/próximo paso va por widget, no por bullets en chat
  (widget-first). El output principal es el widget, no `create_artifact`.
- Confundir "sin `Project_Asset__c`" con "sin canal Slack": el canal puede
  existir sin asset. Correr Paso 3A.0 + pre-check exacto antes de crear.

**On-demand only**
- Jira (Fase 8) y repo Bitbucket (Fase 10) se consultan SOLO al disparar la
  acción kebab. Nada de Jira/Bitbucket en corridas automáticas ni scheduled
  tasks. Para barrido masivo de repos, usar `pc-delivery-bb-commit-reporter`.

**Extractor — no inventar (devolver null ante duda)**
- `mentioned_golive_date` / `mentioned_module` solo si el PM lo dijo explícito.
  Nunca inferir desde nombre del proyecto, Industry o productos de la Opp.
- Valores de Fase 9: prompt estricto, `null` si el PM no lo dijo — una
  alucinación sale como bug a SF.
- Slug de repo: si no hay asset, no inferir desde el nombre — pedir al caller.
- `mentioned_module = null` con `recent_golive` → fila "Other" del catálogo,
  no elegir un módulo plausible.
- Nombres de responsables externos: rol genérico si no hay nombre claro,
  nunca inventar.

**Tono del DM (ver `dm-follow-up-template.md`)**
- Banned phrases bloquean el render — reescribir antes de mostrar. Aplica a
  Fase 7, Fase 10 y a la línea de sugerencia.
- La sugerencia por proyecto es obligatoria (fallback genérico si Haiku falla),
  y hereda el tono (nada de "urgente"/"exigile"/"presiónalo").
- Auto-DM-arse: si `caller == pm`, no ofrecer Fase 7.
- Incluir en el DM canales con status <7d: excluirlos (threshold estricto).

**Clasificación**
- RecordType → Support solo si `DeveloperName == 'Support'` exacto
  (case-sensitive). Cualquier otro valor o null → Delivery.
- No asumir el picklist de `Status__c`: mapear con `getObjectSchema` la 1ª vez.
- `Priority__c`: usar si existe; si no, todo priority=99 (no inventar).
- No pedir golive/sprint a Support ni métricas de adopción a Support — su
  cierre es horas/renovación/issues. Métricas por módulo solo en Delivery.
- Agrupar por cuenta cuando el PM tiene 2+ proyectos vigentes del mismo Account.

**Privacidad del DM 1:1 (ver REGLA DE PRIVACIDAD)**
- El contenido textual del DM 1:1 solo aparece en el widget de auditoría (lo ve
  el caller) y en el DM de respuesta de Fase 7 (parafraseado). Nunca en drafts
  de canal externo ni en campos SF visibles. En Fase 7 se acknowledgea con
  paráfrasis, no cita literal.

**Widget (ver REGLA DE WIDGETS + `widget-shell.md`)**
- Cero colores hardcoded y cero emoji en el HTML — solo tokens nativos
  (`--surface-*`, `--text-*`, `--bg-*`, `--border*`) e íconos Tabler. El tema
  es auto-adaptable (no forzar dark). Compón siempre con los bloques del shell;
  si un widget se ve roto en claro u oscuro, hay un hex hardcodeado.

---

## Archivos de referencia

Carga estos solo cuando el flujo lo requiera — no los cargues todos al
arranque.

- `references/widget-shell.md` — **Shell canónico de TODOS los widgets**:
  bloques HTML reutilizables (`header-card`, `kpi-grid`, `banner`,
  `data-table`, `checklist-block`, `button-row`, `badges`) + reglas de tema
  auto-adaptable e íconos Tabler. Cárgalo antes de armar cualquier widget.
- `references/safety-rules.md` — Regla de no-envío con casos límite.
  Reléela antes de cualquier interacción con tools de write.
- `references/detection-rules.md` — Algoritmo exacto de R0 y R1-R4,
  edge cases (bots, reacciones, threads huérfanos), y cálculo de
  `status_completeness` / `client_blocker` (v2.5+).
- `references/salesforce-schema.md` — Queries SOQL exactas, mapeo de
  campos, manejo del campo `Owner.ManagerId`, y query auxiliar de
  proyectos finalizados (v2.5+).
- `references/channel-onboarding.md` — Flujo paso a paso para crear
  canal privado, invitar usuarios y persistir el asset. Incluye naming
  convention y fallbacks si el conector no expone tool de creación.
- `references/team-identification.md` — Cómo distinguir PM, comercial
  SF, bots y cliente final por dominio de email del profile Slack.
- `references/draft-templates.md` — Templates de status orientados al
  comercial SF + templates secundarios para R1-R4. Para postear en el
  canal externo (Fase 6).
- `references/dm-follow-up-template.md` (v2.5+) — Template del DM de Fase 7,
  lista de banned phrases con justificación, reglas de tono, sugerencia por
  proyecto y catálogo de métricas por módulo.

Historial de versiones: `CHANGELOG.md` (no se carga en runtime).
