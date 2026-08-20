# Targets — destinatarios del help request

El skill envía **el mismo mensaje** a dos destinos en paralelo (no son
alternativas, son ambos):

1. **DM directo a Ariel Tarsitano** — atención personal y trazabilidad
   uno-a-uno.
2. **Canal `#05-ayuda`** — para que el resto del equipo vea el problema
   y pueda ayudar si Ariel está ocupado, y para construir un historial
   común de incidencias de Cowork.

Ambos envíos requieren el mismo OK explícito del usuario en el preview.
Una sola aprobación cubre los dos envíos (no se piden por separado),
pero la preview debe mencionar **explícitamente** que se mandará a
ambos lugares.

## 1) DM a Ariel Tarsitano

- **Nombre**: Ariel Tarsitano
- **Email corporativo**: `ariel.tarsitano@procontacto.com.mx`
- **Workspace de Slack**: ProContacto

Resolver el `user_id` por email — los handles cambian, los emails no:

```
slack_search_users(query="ariel.tarsitano@procontacto.com.mx")
```

Tomar el primer match cuyo `profile.email` coincida exactamente con el
email de arriba (case-insensitive).

## 2) Canal `#05-ayuda`

- **Nombre del canal**: `05-ayuda` (con `#` al referirlo en chat, sin
  `#` al usar la API)
- **Workspace de Slack**: ProContacto

Resolver el `channel_id` por nombre:

```
slack_search_channels(query="05-ayuda")
```

Tomar el match cuyo `name` sea exactamente `05-ayuda`. Si hay variantes
con nombre parecido (ej: `04-ayuda`, `05-ayuda-cowork`), no asumas —
pídele al usuario que confirme cuál usar.

## Orden y manejo de fallos

1. Resolver primero ambos targets (DM y canal) **antes** de enviar nada.
   Si alguno no se puede resolver, decirle al usuario qué falló y
   dejarlo decidir si igual quiere mandar al destino que sí se resolvió.
2. Enviar primero al canal `#05-ayuda` y después el DM a Ariel. Si el
   envío al canal falla, abortar el DM y reportar el error — preferimos
   no escalar a medias.
3. En el mensaje de confirmación al usuario, listar a dónde llegó el
   mensaje:
   > Listo, mandé el aviso al canal `#05-ayuda` y un DM directo a Ariel.

## Fallback — Slack mismo está caído

Si el componente roto **es Slack**, no se puede mandar a ningún destino.
En ese caso, darle al usuario el texto del mensaje listo para copiar y
dos instrucciones:

- "Pégalo en el canal `#05-ayuda` del workspace de Slack."
- "Y mándale un DM a @ariel.tarsitano con el mismo texto."

## Cambios al destinatario

Si en algún momento el destinatario tiene que cambiar (Ariel de
licencia, canal renombrado, nuevo canal de soporte, etc.), actualizar
este archivo y subir la versión `MINOR` del SKILL.md (`metadata.version`
y `metadata.last_modified` en frontmatter). No cambiar el nombre del
skill.
