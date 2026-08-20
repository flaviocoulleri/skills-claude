# Channel onboarding

Flujo paso a paso para crear el canal Slack externo de un proyecto que
no lo tiene, invitar a los stakeholders y persistir el `Project_Asset__c`.

**Cada paso requiere aprobación expresa vía
`mcp__visualize__show_widget`. La regla de seguridad de
`safety-rules.md` aplica entera.**

## Precondición

El proyecto pasa el gate:
- `Project__c.Completion_Summary__c = null`.
- `Project__c.OwnerId = <PM seleccionado>`.
- No tiene `Project_Asset__c` con `Type__c =
  'SlackExternalProjectChannelId'`.

## Paso 1 — Pedir mail del comercial SF

Render widget con un input text:

```
Proyecto: <Project.Name>
Account: <Account.Name>
Owner (PM): <Owner.Name>

Mail del comercial de Salesforce que originó esta oportunidad:
[                                          ]

[Continuar]   [Saltar este proyecto]
```

Si el PM saltea, marca el proyecto en el output como "onboarding postpuesto"
y sigue con el próximo.

## Paso 2 — Validar el mail en Slack

```javascript
slack_search_users({ query: comercial_sf_email })
```

Si el resultado está vacío:

Render widget de error:

```
No encontré el mail "<email>" en el workspace Slack.
Revisa el dato y vuelve a tipear, o saltea este proyecto.

[Reintentar mail]   [Saltar proyecto]
```

Si aparece, captura el `user.id` de Slack para invitarlo después.

## Paso 3 — Validar Owner y Manager en Slack

```javascript
slack_search_users({ query: Owner.Email })
slack_search_users({ query: Owner.Manager.Email })  // si existe
```

Si el Owner (PM) no aparece en Slack, abortar — el PM debe estar en
Slack para que el skill tenga sentido.

Si el manager no aparece o `Owner.ManagerId` es null, mostrar al PM en
el widget de confirmación: "Tu manager no figura en Slack / no está en
SF. Voy a invitar solo al PM y al comercial SF. ¿OK?"

## Paso 4 — Naming convention del canal

Formato sugerido:

```
ext-<account-slug>-<project-slug>
```

Donde:
- `<account-slug>` — `Account.Name` lowercase, sin espacios, sin
  acentos, sin caracteres especiales (mantener solo `[a-z0-9-]`),
  truncado a 15 chars.
- `<project-slug>` — idem con `Project.Name`, truncado a 15 chars.

Total ≤ 80 caracteres (límite Slack).

Ejemplos:
- `ext-betacorp-rollout-fase2`
- `ext-coca-loyalty-cgc`

Si el nombre ya existe en el workspace, sufijar con `-2`, `-3`, etc.

## Paso 5 — Widget de confirmación

```
Proyecto: <Project.Name>
Account: <Account.Name>

Voy a:
1. Crear canal Slack PRIVADO llamado #<channel-name>
2. Invitar a:
   • <Owner.Name> (PM, <Owner.Email>)
   • <Manager.Name> (Manager, <Manager.Email>)   ← si existe
   • <Comercial SF Name> (<comercial_sf_email>)
3. Persistir Project_Asset__c en SF:
   - Project__c = <Project.Id>
   - Type__c = 'SlackExternalProjectChannelId'
   - Value__c = <channel_id>

⚠ El cliente final NO se invita a este canal.

[Sí, ejecutar]   [Cancelar]   [Editar nombre del canal]
```

## Paso 6 — Ejecutar (solo después de [Sí, ejecutar])

### 6.1 Crear canal

Verificar que el conector Slack expone un tool de creación de canal en
el turno actual. Tools posibles:

- `slack_create_channel` (no estándar — verificar)
- `slack_conversations_create` (a través de `slack_send_message_draft`
  o similar — verificar)

Si **ningún tool de creación** está disponible, render widget:

```
El conector Slack autenticado no expone un tool para crear canales.
Tienes dos opciones:

1. Crea el canal manualmente en Slack y pégame el channel ID:
   [                    ]

2. Salta este proyecto y avanza con el siguiente.

[Channel ID listo]   [Saltar]
```

Si pegan un channel ID válido (`C0...`), sigue con 6.2.

### 6.2 Invitar usuarios

Por cada user (PM, Manager, comercial SF), invitar al canal con el
tool del conector. Si alguna invitación falla, capturarlo y reportar
al final — no abortar el proceso.

### 6.3 Persistir asset

```javascript
createSobjectRecord("Project_Asset__c", {
  Project__c: project_id,
  Type__c: "SlackExternalProjectChannelId",
  Value__c: channel_id,
});
```

### 6.4 Reporte al PM

```
✅ Canal #<channel-name> creado
✅ Invitados: PM, Manager, comercial SF
✅ Project_Asset__c persistido (Id: <new_asset_id>)

Próximo paso opcional: postear un mensaje de bienvenida al canal.
¿Quieres que prepare un draft?  [Sí, draft de bienvenida]   [No]
```

## Paso 7 (opcional) — Mensaje de bienvenida

Si el PM elige draft de bienvenida:

Template (de `draft-templates.md`, sección "bienvenida-comercial-sf"):

```
Hola equipo, abro este canal para mantenerte al tanto del proyecto
<Project.Name> con <Account.Name>.

Voy a postear status semanal acá: avance del sprint, hitos cumplidos
y próximas fechas. Si necesitas algo puntual, taggeame en este canal.

— <PM.Name>
```

Render widget con el draft + botones [Copiar] [Editar] [Postear].

**[Postear]** dispara una segunda confirmación (releer texto exacto +
"¿Confirmas envío?") antes de llamar al tool de envío. Default seguro:
copiar y postear manualmente.

## Fallbacks generales

Si en cualquier paso un tool falla:

- **Slack rate limit** → esperar y reintentar una vez. Si sigue
  fallando, reportar al PM.
- **SF DML error** → mostrar el error textual al PM, ofrecer reintentar
  o saltear.
- **Tool de invitación faltante** → render widget pidiendo que el PM
  invite manualmente y después confirme; persistir el asset igual
  porque el canal existe.

## Naming/Slack edge cases

- Slack canal names solo permiten `[a-z0-9-_]`. Si el slug genera otros
  chars, los sustituyes por `-` y colapsas repetidos.
- Canales privados aparecen con `🔒` en Slack pero el ID sigue siendo
  `C...`.
- Si el conector es de bot, el bot debe estar en el canal para invitar
  a otros — verificar este paso si la invitación falla con permission
  error.
