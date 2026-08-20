# Team identification

Cómo clasificar usuarios Slack en las 4 categorías que el skill maneja:

1. **PM** — el Owner del Project__c. Usuario único por proyecto.
2. **Equipo PC (extendido)** — cualquier user con dominio
   `procontacto.com.mx` (incluye al PM).
3. **Comercial SF** — partner seller con mail tipeado por el PM en el
   widget. NO está en SF.
4. **Cliente final** — anomalía. No debería aparecer en este canal.

## Identificación por dominio de email

Fuente: `slack_read_user_profile(user_id).profile.email`.

```pseudo
def domain(user):
    email = user.profile.email
    return email.split("@")[1].lower() if email else None

def is_pc_team(user):
    return domain(user) == "procontacto.com.mx"

def is_pm(user, project):
    return user.profile.email == project.Owner.Email

def is_comercial_sf(user, comercial_sf_email):
    return user.profile.email == comercial_sf_email

def is_client_anomaly(user, account):
    client_domains = derive_client_domains(account)
    return domain(user) in client_domains
```

## Derivar dominios del cliente

`derive_client_domains(account)` busca:

1. `Account.Website` → extraer dominio. Ej: `https://www.acme.com` → `acme.com`.
2. Emails de `Account.Contacts[].Email` → extraer dominios distintos de
   `procontacto.com.mx` y `gmail.com` / dominios públicos.
3. Si Account tiene varios dominios, tratarlos todos como cliente.

Si no se puede derivar (Account sin Website ni Contacts), saltear el
check de anomalía para ese proyecto y dejar nota en el output ("no se
pudo verificar dominios cliente").

## Bots y webhooks

```pseudo
def is_bot(user):
    return user.is_bot or user.profile.api_app_id is not None
```

Bots **no cuentan** como "el PM posteó" ni como "PC respondió" en
ninguna regla. Si el único mensaje de PC en el canal es del bot Jira,
R0 sigue corriendo.

Excepción: si el canal entero es solo de bots (sin humanos en N días),
flagearlo aparte como "canal solo bots" — es señal de que el PM y el
comercial SF nunca interactuaron.

## Cache

Para no llamar `slack_read_user_profile` por cada mensaje, cachear por
`user_id` durante la auditoría. Una sola llamada por user único en
toda la corrida.

## Edge cases

### User sin email en el profile

Algunos guests / users limitados no exponen email. Marcar como
"unknown" y excluir de PC team / cliente. Si el user en cuestión es el
último que posteó, aparece en el output como "(usuario sin email visible)".

### Email con dominio desconocido

Ni `procontacto.com.mx`, ni el dominio cliente, ni el comercial SF →
puede ser un partner adicional, un freelance o un user con dominio
custom. Tratarlo como "externo no clasificado" y mostrarlo en el
detalle del proyecto sin disparar reglas.

### Cliente final con dominio compartido

Si `Account.Website` es `gmail.com` u otro dominio público (raro pero
ocurre con cuentas pequeñas), no usar dominio para detectar anomalía
— en su lugar, comparar contra `Account.Contacts[].Email` exacto.

### El comercial SF tiene dominio Salesforce

Lo más común: `@salesforce.com`. Eso ayuda a validar visualmente, pero
**no lo uses como heurística** — el PM puede tipear un mail con dominio
distinto (consultora externa, partner con email propio, etc.). La
fuente de verdad es el mail tipeado por el PM.
