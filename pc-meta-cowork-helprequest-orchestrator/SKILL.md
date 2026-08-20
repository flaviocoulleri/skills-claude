---
name: pc-meta-cowork-helprequest-orchestrator
metadata:
  version: 2.1.0
  last_modified: 2026-05-07
description: >
  Cuando un colaborador de ProContacto queda trabado por algo de
  Cowork/Claude (connector, skill, plugin, entorno, permisos), este skill
  arma un mensaje con el contexto del problema y lo envía en paralelo al
  canal `#05-ayuda` y por DM a Ariel Tarsitano — siempre con aprobación
  explícita antes de mandar. Activar cuando: una tool call MCP tira error
  (401/403, timeout, "not connected", "tool not found"); un connector
  aparece como "connecting" o no autenticado; un skill ProContacto falla,
  devuelve vacío, o no triggerea cuando claramente debería; un plugin no
  carga o falta; el folder de Cowork no está mounted; el usuario dice "no
  me funciona X", "está roto", "no puedo acceder", "estoy trabado", "esto
  no funciona", "Claude no me entiende"; un sistema externo niega acceso
  (Salesforce, Drive, Slack, Bitbucket); o hubo 2+ reintentos fallidos
  sobre el mismo componente. NO esperar que el usuario pida ayuda —
  ofrecérsela. ES/EN. Requiere Slack conectado.
---

# pc-meta-cowork-helprequest-orchestrator

## Para qué sirve

Cuando un colaborador de ProContacto queda trabado usando Cowork/Claude,
rara vez tiene la información necesaria para reportarlo bien (mensaje de
error exacto, qué componente falló, qué estaba haciendo, qué skill estaba
corriendo). El resultado típico es que se queda trabado en silencio,
abandona la tarea, o manda un mensaje vago tipo "no me anda esto".

Este skill cierra ese gap: detecta la falla, **clasifica el componente
afectado**, **arma tú el contexto** sin hacerle preguntas innecesarias al
usuario, **ofrece** mandarle el aviso al canal `#05-ayuda` y a Ariel por
DM, y sólo si el usuario aprueba expresamente, **envía** el mensaje.

Reemplaza al `pc-meta-connector-helprequest-orchestrator` (v1.x), que
cubría sólo errores de connector. Esta v2.0.0 amplía el alcance al stack
entero de Cowork.

## ⛔ Regla bloqueante: aprobación expresa antes de enviar

**Nunca enviar el mensaje (ni al canal `#05-ayuda` ni el DM a Ariel) sin
un "sí" explícito del usuario en la conversación actual.**

Esto no es negociable y aplica aun cuando:

- El usuario haya aprobado un envío en una conversación anterior.
- El usuario diga "mándalo siempre que pase" o algo similar — pídele
  aprobación igual cada vez.
- El error sea idéntico a uno ya escalado.

El workflow obligatorio es: detectar → clasificar componente → armar
mensaje → **mostrar preview exacta + indicar destinos** → esperar OK →
enviar. Una sola aprobación cubre los dos envíos (canal + DM) porque el
contenido es idéntico, pero el preview debe mencionar **explícitamente
ambos destinos**. Una autorización no es transitiva: si hay que actualizar
el mensaje, requiere otra aprobación.

**Por qué bloqueante**: el canal `#05-ayuda` es público al equipo y los
DMs los trata Ariel como señales de soporte real. Spam, duplicados o
envíos sin contexto degradan la señal y rompen el contrato implícito con
el equipo.

## Triggers — cuándo activarse

Activar el flow ante cualquiera de estas condiciones, agrupadas por
componente:

### A) Connectors (MCP)

1. Tool call MCP devuelve error visible: `401 Unauthorized`, `403
   Forbidden`, `timeout`, `Tool not found`, `MCP server not connected`,
   `Authentication required`, `not authenticated`, `connection refused`.
2. Connector aparece como "Connecting…" sostenido o no autenticado y
   bloquea la tarea actual.

### B) Skills / plugins ProContacto

3. Un skill ProContacto falla en su lógica interna (tira excepción, error
   en script bundleado, archivo de reference roto).
4. Un skill devuelve resultado vacío o claramente inconsistente (ej:
   `pc-sales-sf-account-builder` no encuentra una cuenta que el usuario
   sabe que existe).
5. Un skill **no triggerea** cuando claramente debería (el usuario
   describe en lenguaje natural una tarea que encaja con la `description`
   de un skill instalado y Claude no lo activa).
6. Un plugin instalado no carga o un skill que el equipo usa "no aparece".

### C) Cowork / entorno

7. Folder seleccionado no está mounted, scheduled task no corre, artifact
   no renderiza, Cowork pierde la sesión.
8. Cualquier comportamiento de Cowork mismo que rompe el flow del usuario
   (no de un sistema externo).

### D) Permisos descubiertos vía Cowork

9. Un sistema externo niega acceso al usuario en una operación que un
   skill ProContacto está ejecutando: `INSUFFICIENT_ACCESS` en Salesforce,
   "you are not in this channel" en Slack, 403 en Bitbucket/Drive/Jira,
   licencia faltante. (Acá el responsable directo puede ser
   `pc-admin-interno-user-orchestrator`, pero como Ariel es el escalamiento
   humano de ese skill también, redirigir a `#05-ayuda` con contexto es
   lo correcto.)

### E) Frustración explícita del usuario

10. El usuario verbaliza frustración con la herramienta: "esto no
    funciona", "no sé cómo seguir", "Claude no me entiende", "estoy
    trabado", "me rendí", "help" sin contexto previo, "no me anda nada".
11. 2+ reintentos fallidos sobre el mismo componente en la misma
    conversación, aun si cada error individual parecía transitorio.

Si dudas entre activar o no, **activa**. El skill pide aprobación antes
de hacer nada visible, así que un falso positivo es barato (el usuario
dice "no"); un falso negativo deja al colaborador sin soporte.

## Cuándo NO activar

Estos casos no son help requests para Ariel — tienen otro dueño o son
parte legítima del trabajo del usuario:

- **"No sé qué skill usar"** sin error previo. Eso es discovery —
  redirigir a `pc-sales-sf-general` (AE), `pc-training-onboarding-guide`
  (gente nueva), o el listado natural de skills. Si el usuario insiste
  después de eso, sí escalar.
- **Bugs de datos del cliente** (ej: "el contacto está mal cargado en
  SF", "el proyecto no aparece"). El connector funciona; el problema es
  un dato del CRM con sus propios responsables (Admin SF, PM del
  proyecto).
- **Decisiones de producto, scope, presupuesto, aprobación comercial**.
  Escapan al rol de Ariel como admin de Cowork.
- **Errores de juicio de Claude** (alucinación, info incorrecta, decisión
  discutible que no involucra una herramienta rota). Eso es feedback a
  Anthropic vía thumbs-down, no soporte interno.
- **"Cómo se usa X"** cuando X funciona bien. Es training/docs, no
  soporte.
- **Errores claramente del lado del usuario** (SOQL malformado, archivo
  no existe en el path que escribió, fecha inválida) que no involucran
  un componente de Cowork roto.

## Pipeline

### 1. Detectar y diagnosticar

Cuando se cumple un trigger, antes de armar nada:

- Identifica el **componente afectado** y clasifícalo en una de estas
  6 categorías: `Connector | Skill | Plugin | Cowork | Permisos | Otro`.
  Si dudas entre dos, elige la más específica.
- Captura el **detalle del componente** por nombre legible (no IDs MCP):
  - Connector: "Slack", "Jira", "Salesforce", "Google Calendar", "Gmail",
    "Drive", "Confluence", "ReadAI".
  - Skill: nombre del skill ProContacto (`pc-...`).
  - Plugin: nombre del plugin / marketplace.
  - Cowork: "folder mount", "scheduled task", "session", "artifact", etc.
  - Permisos: el sistema externo ("Salesforce", "Slack channel
    #X-cliente", "Bitbucket repo Y").
  - Otro: descripción corta del componente cuando no encaja arriba.
- Captura el **mensaje de error textual** tal cual lo devolvió el sistema.
  Si el trigger es frustración explícita sin error técnico, deja
  `(sin error técnico, frustración del usuario)`.
- Reconstruí en una línea **qué intentaba hacer el usuario** en lenguaje
  natural, basándote en su pedido original o el último mensaje. No le
  preguntes al usuario — inferilo del contexto. Si no puedes inferirlo,
  una línea genérica es suficiente.
- Si el problema ocurrió dentro de un **skill específico**, inclúyelo
  como `Skill / comando`. Si fue tool call directa fuera de un skill,
  déjalo en blanco.

### 2. Armar el mensaje con la plantilla canónica

El **mismo mensaje** se envía al canal y al DM (sin variantes). Plantilla
obligatoria — copiar tal cual, reemplazar los `{placeholders}`:

```
Un componente de Cowork me dejó trabado y necesito ayuda.

• Componente afectado: {Connector|Skill|Plugin|Cowork|Permisos|Otro}
• Detalle: {nombre legible del componente}
• Skill / comando: {skill_o_comando_o_"—"}
• Qué estaba haciendo: {intent_en_una_linea}
• Error textual: {error_message}
• Reportado por: {user_email} a las {timestamp_iso}

Avísame cómo seguir, gracias 🙏
```

Reglas de armado:

- `{timestamp_iso}` en formato `YYYY-MM-DD HH:MM` zona local del usuario.
  Si no puedes determinarla, usa UTC y deja `Z` al final.
- `{user_email}` se toma del contexto de la sesión (campo userEmail del
  system prompt). Si no está disponible, deja `(email no detectado)`.
- `{error_message}` se incluye **textual**, sin parafrasear. Si supera
  500 caracteres, truncalo con `… [truncado]` y mantén las primeras 500.
  Si el trigger fue frustración sin error técnico, deja la frase del
  usuario entre comillas (sanitizada).
- `{intent_en_una_linea}` máx ~150 caracteres, sin info sensible (no
  incluyas contenido de mensajes privados, datos de clientes,
  credenciales).
- Si el campo "Skill / comando" no aplica, deja `—` (guion m). No lo
  elimines: Ariel filtra por estos campos.

### 3. Mostrar preview y pedir aprobación (con botones)

Antes de mandar nada, renderiza un widget interactivo vía
`mcp__visualize__show_widget` que muestre el preview y exponga botones
clickeables para resolver la decisión. Esto reduce la fricción para el
usuario (un click vs. tipear) y mantiene el historial del chat limpio.

**Setup**: la primera vez en la sesión, llama silenciosamente a
`mcp__visualize__read_me` con `modules: ["interactive"]` antes del primer
`show_widget`. No narres esa llamada al usuario.

**Estructura del widget**:

- Una línea de contexto ("Detecté un problema con `{componente}: {detalle}`. Te muestro el mensaje que mandaría y eliges.")
- Un bloque `<pre>` con la **plantilla rellena tal cual va a salir** —
  idéntica al texto que recibirían `#05-ayuda` y Ariel.
- Una línea aclarando los dos destinos: "Va al canal `#05-ayuda` y por
  DM a Ariel Tarsitano."
- Una grilla de 4 botones, en este orden y con estos `sendPrompt(...)`
  exactos:

  | Botón | `sendPrompt` que dispara |
  |---|---|
  | Mandar a ambos (Recommended) | `Sí, mándalo a #05-ayuda y a Ariel por DM` |
  | Solo al canal `#05-ayuda` | `Mándalo solo al canal #05-ayuda` |
  | Solo DM a Ariel | `Mándalo solo por DM a Ariel` |
  | Editar mensaje primero | `Necesito editar el mensaje antes de mandarlo` |

- Importante: NO incluyas un botón "Cancelar". El usuario puede tipear
  "no" o simplemente ignorar el widget — silencio significa no enviar.
  Un botón explícito de cancelar agrega ruido sin valor.

**Esqueleto del widget** (adapta los `{placeholders}`):

```html
<h2 class="sr-only">Preview del help request a #05-ayuda y Ariel</h2>
<div style="padding: 1rem 0;">
  <p style="font-size: 14px; color: var(--color-text-secondary); margin: 0 0 12px;">
    Detecté un problema con <code>{componente}: {detalle}</code>. Te muestro el mensaje que mandaría y eliges.
  </p>
  <pre style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 12px; font-family: var(--font-mono); font-size: 13px; white-space: pre-wrap; margin: 0 0 12px;">{plantilla rellena}</pre>
  <p style="font-size: 13px; color: var(--color-text-tertiary); margin: 0 0 12px;">
    Destinos: canal <code>#05-ayuda</code> y DM a Ariel Tarsitano.
  </p>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 8px;">
    <button onclick="sendPrompt('Sí, mándalo a #05-ayuda y a Ariel por DM')">Mandar a ambos ↗</button>
    <button onclick="sendPrompt('Mándalo solo al canal #05-ayuda')">Solo al canal ↗</button>
    <button onclick="sendPrompt('Mándalo solo por DM a Ariel')">Solo DM a Ariel ↗</button>
    <button onclick="sendPrompt('Necesito editar el mensaje antes de mandarlo')">Editar primero ↗</button>
  </div>
</div>
```

**Cómo cuenta la aprobación**:

- Cuando el usuario clickea un botón, `sendPrompt` postea el texto literal
  al chat. Eso cuenta como confirmación explícita en la conversación —
  no rompe la regla bloqueante de approval, porque el texto queda en el
  transcript exactamente igual a si el usuario lo hubiera tipeado.
- Si el usuario tipea su respuesta libre en vez de clickear, manéjala
  igual: aceptación explícita ("sí", "dale", "ok", "send it") procede;
  cualquier otra cosa o silencio significa no enviar.
- Si elige "Editar primero", pregúntale qué quiere cambiar, ajusta la
  plantilla y vuelve a renderizar el widget. La aprobación se reinicia
  con cada cambio.
- Si elige uno de los destinos individuales, ajusta el step 4 (envío)
  para mandar sólo a ese destino y no al otro.

### 4. Resolver destinatarios y enviar

Solo después del OK explícito. Detalles completos del lookup en
`references/targets.md`. Resumen:

1. **Resolver ambos targets antes de enviar nada**:
   - `slack_search_users(query="ariel.tarsitano@procontacto.com.mx")` →
     tomar el match cuyo `profile.email` coincida exactamente.
   - `slack_search_channels(query="05-ayuda")` → tomar el match cuyo
     `name` sea exactamente `05-ayuda`. Si hay ambigüedad, pedirle al
     usuario que confirme.
2. **Enviar primero al canal `#05-ayuda`**, después el DM a Ariel:
   - Canal: `slack_send_message` contra el `channel_id` resuelto.
   - DM: `slack_send_message` contra el `user_id` resuelto.
3. Si el envío al canal falla, abortar el DM y reportar el error —
   preferimos no escalar a medias.
4. Si la búsqueda de usuario o canal falla, avisar al usuario qué destino
   no se resolvió y dejarle decidir si manda al que sí resolvió o cancela
   todo. No inventar destinatarios.

### 5. Confirmar al usuario (con botones de próximo paso)

Una vez enviado, muéstrale al usuario un nuevo widget vía
`mcp__visualize__show_widget` con la confirmación de envío + botones
para elegir cómo seguir mientras espera respuesta de Ariel/equipo.

**Estructura del widget de confirmación**:

- Una línea de confirmación: "Listo, mandé el aviso a `{destinos efectivos}`."
- 2-3 botones según el componente afectado, mapeando a workarounds
  concretos:

  | Componente | Botón | `sendPrompt` |
  |---|---|---|
  | Connector | Probar otro connector | `Sugerime un workaround usando otro connector mientras tanto` |
  | Skill | Hacerlo sin el skill | `Hagamos la tarea a mano sin usar el skill` |
  | Plugin | Cómo instalo el plugin | `Pásame las instrucciones para instalar el plugin que falta` |
  | Cowork | Reiniciar sesión | `Cómo reinicio la sesión de Cowork sin perder el contexto` |
  | Permisos | A quién le pido acceso | `Dime a quién le pido el acceso que falta` |
  | Otro/genérico | Sugerime un workaround | `Sugerime un workaround para seguir mientras espero respuesta` |

- Y un botón siempre presente:

  | Botón | `sendPrompt` |
  |---|---|
  | Esperar respuesta | `Espero respuesta, no necesito workaround ahora` |

**Esqueleto** (ejemplo para un connector caído, ambos destinos):

```html
<h2 class="sr-only">Help request enviado, próximos pasos</h2>
<div style="padding: 1rem 0;">
  <p style="font-size: 14px; margin: 0 0 12px;">
    Listo, mandé el aviso al canal <code>#05-ayuda</code> y un DM directo a Ariel.
  </p>
  <p style="font-size: 13px; color: var(--color-text-secondary); margin: 0 0 12px;">
    ¿Cómo seguimos mientras esperas respuesta?
  </p>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 8px;">
    <button onclick="sendPrompt('Sugerime un workaround usando otro connector mientras tanto')">Probar otro connector ↗</button>
    <button onclick="sendPrompt('Espero respuesta, no necesito workaround ahora')">Esperar respuesta ↗</button>
  </div>
</div>
```

Adapta los botones según el componente clasificado en el step 1. No
metas más de 3 botones — si hay muchos workarounds posibles, deja el
botón genérico "Sugerime un workaround" y desplegalo en chat después
del click.

## Información que NO debe ir en el mensaje

El canal `#05-ayuda` es visible al equipo entero, así que la regla de
sanitización es **estricta**. Nunca incluyas:

- Credenciales, tokens, API keys, passwords (aunque hayan aparecido en
  el error textual — sanitiza antes de pegar).
- Contenido literal de mensajes privados de Slack, threads internos,
  emails, o documentos de clientes.
- PII de terceros más allá de lo estrictamente necesario para
  diagnosticar el componente. Nombres genéricos de cuentas/proyectos
  están OK; números de tarjeta, DNI, dirección personal, no.

Si el `error_message` original contiene algo de lo anterior, reemplázalo
por `[redactado: contenía credenciales]` o similar antes de armar el
mensaje.

## Dependencias

- **Connector de Slack autenticado**: requerido para poder enviar a
  ambos destinos. Si el componente roto **es Slack mismo**, no puedes
  escalar por Slack — en ese caso dile al usuario:
  > "El connector de Slack está caído, así que no puedo escribir yo
  > mismo. Pega este mensaje en el canal `#05-ayuda` y mándale el mismo
  > texto por DM a @ariel.tarsitano:" + plantilla rellena lista para
  > copiar.
- **Tool `mcp__visualize__show_widget`**: requerido para renderizar el
  widget de preview/aprobación (step 3) y el de confirmación (step 5).
  Si la tool no está disponible en el entorno (ej: Claude.ai sin
  visualize), degrada el flow al formato texto del v2.0.0 — preview
  como blockquote y aprobación esperando "sí" tipeado. No abortar el
  skill por falta de visualize; el patrón de botones es UX, no
  funcional.

## Convenciones de marca

El mensaje va de un colaborador de ProContacto a otro — tono interno,
directo, sin formalismo corporativo. Sin emojis salvo el 🙏 final de la
plantilla. No incluir slogan institucional ni firma de marca; es un
mensaje operativo, no comunicacional externo.

## Migración desde v1.x (`pc-meta-connector-helprequest-orchestrator`)

Este skill **reemplaza** al `pc-meta-connector-helprequest-orchestrator`
(v1.0.0 / v1.1.0). Los triggers de connectors (categoría A) se mantienen
1:1; lo nuevo son las categorías B–E. Cuando se instale v2.x,
desinstalar la v1.x para evitar doble triggering.

Cambios MAJOR vs v1.1.0 (v2.0.0):

- Nombre del skill cambió (de `connector` a `cowork` como objeto).
- Plantilla del mensaje gana dos campos: `Componente afectado` (con las
  6 categorías) y `Detalle`. El campo `Connector afectado` de v1 se
  retira — ahora va en `Detalle` cuando el componente es `Connector`.
- Triggers ampliados de 4 (categoría A) a 11 (categorías A-E).
- Sección "Cuándo NO activar" explícita para evitar saturar `#05-ayuda`.

Cambios MINOR v2.0.0 → v2.1.0:

- Step 3 (preview/aprobación) y step 5 (confirmación) ahora rendean
  widgets interactivos vía `mcp__visualize__show_widget` con botones
  que invocan `sendPrompt(...)`. La aprobación por click cuenta igual
  que tipeada (el texto queda en transcript).
- Si el entorno no tiene `mcp__visualize__show_widget`, el skill cae
  automáticamente al flow texto del v2.0.0 — no es bloqueante.
