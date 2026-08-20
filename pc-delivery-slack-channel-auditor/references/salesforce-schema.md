# Salesforce schema y queries

## Objetos involucrados

- `Project__c` — proyecto activo.
  - `Completion_Summary__c` — gate de vigencia. `null` = vigente.
  - `OwnerId` — PM (= comercial nuestro). User standard.
  - `Account__c` — cuenta cliente.
- `Project_Asset__c` — registro de assets (canales Slack, drives, creds,
  etc.) de un proyecto. Schema completo en la memoria
  `project_asset_schema.md`. Para este skill:
  - `Type__c = 'SlackExternalProjectChannelId'` → canal externo.
  - `Value__c` → channel ID Slack (formato `C01234567`).
  - `Project__c` → lookup al `Project__c`.
- `User` — usuarios SF.
  - `ManagerId` — manager del user (standard).

## Query 1: proyectos vigentes del PM seleccionado

```sql
SELECT Id, Name,
       Account__c, Account__r.Name, Account__r.Website,
       OwnerId, Owner.Name, Owner.Email,
       Owner.ManagerId, Owner.Manager.Name, Owner.Manager.Email
FROM Project__c
WHERE Completion_Summary__c = null
  AND OwnerId = :PM_USER_ID
ORDER BY Name
```

Si el PM tipea un email en el widget en vez de un Id, primero resolverlo:

```sql
SELECT Id, Name, Email FROM User WHERE Email = :PM_EMAIL AND IsActive = true LIMIT 1
```

## Query 2: assets de canal externo por lote de proyectos

```sql
SELECT Id, Project__c, Type__c, Value__c, Grouper__c
FROM Project_Asset__c
WHERE Project__c IN :PROJECT_IDS
  AND Type__c = 'SlackExternalProjectChannelId'
```

## Insert: persistir canal externo recién creado

```javascript
createSobjectRecord("Project_Asset__c", {
  Project__c: <project_id>,
  Type__c: "SlackExternalProjectChannelId",
  Value__c: <slack_channel_id>,
  // Grouper__c queda null — solo aplica a credenciales SF multi-ambiente
});
```

## Validación con `getObjectSchema`

Antes de la primera query, llama:

```javascript
getObjectSchema("Project__c");
getObjectSchema("Project_Asset__c");
```

y verifica:

- `Project__c.Completion_Summary__c` existe y es del tipo esperado
  (long text / textarea, según implementación).
- `Project_Asset__c.Type__c` es picklist y contiene
  `SlackExternalProjectChannelId` entre los values activos.

Si un campo difiere del esperado (ej: `Type__c` se llama distinto, o el
picklist value cambió), documéntalo en chat al PM y ajusta las queries
sin frenar el flujo.

## Account.Website para detectar cliente final

`Account__r.Website` puede usarse para inferir el dominio del cliente y
detectar anomalías (cliente en el canal). Si está vacío, también revisar
emails de `Account__r.Contacts` (otra query si hace falta — ver
`team-identification.md`).

## Notas

- **Nunca** uses `Status__c` como filtro de vigencia. La fuente de
  verdad es `Completion_Summary__c = null`.
- **Nunca** uses `LastModifiedDate` para inferir actividad — la
  actividad real vive en Slack.
- `Owner.Manager.Email` puede ser null si el user no tiene manager
  configurado en SF. En ese caso, durante el onboarding informa al PM
  ("tu manager no está configurado en SF, no lo voy a invitar — quieres
  invitarlo manual?") y seguir.
