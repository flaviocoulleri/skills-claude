# Detection rules

Algoritmo exacto para R0 (primaria) y R1-R4 (secundarias).

## Ventana de análisis

Para todas las reglas: **últimos 10 mensajes top-level del canal + replies
de los threads cuyo root cae en esos 10**. No se lee más historia.

## Notación

- `MSG_TOP[]` — los 10 mensajes top-level más recientes (orden descendente
  por ts).
- `THREADS[mt]` — replies del thread cuyo root es `mt` (si tiene replies).
- `now` — timestamp actual.
- `is_pm(u)` — `u.profile.email == Project__c.Owner.Email`.
- `is_pc_team(u)` — dominio del email del user en `procontacto.com.mx`
  (ver `team-identification.md`).
- `is_comercial_sf(u)` — `u.profile.email == comercial_sf_email` tipeado
  por el PM.
- `is_bot(u)` — `u.is_bot == true` o user es app/integration.

---

## R0 — PM en silencio frente al comercial SF (PRIMARIA)

**Threshold default: 7 días.**

```pseudo
last_pm_top_level = max(m.ts for m in MSG_TOP if is_pm(m.user) and not is_bot(m.user))

if last_pm_top_level is null:
    R0 = RED
    detail = "PM nunca posteó en la ventana"
elif (now - last_pm_top_level) > 7d:
    R0 = RED
    detail = f"PM no postea hace {(now - last_pm_top_level) / 86400} días"
else:
    R0 = OK
```

R0 considera **solo mensajes top-level** del PM. Replies en threads no
cuentan como "status" — un status real es un mensaje propio del PM al
canal.

R0 dispara incluso si el comercial SF está activo. La idea es que el PM
debe ser proactivo, no reactivo.

### Edge case: canal vacío

Si `MSG_TOP == []` → R0 = RED con detail = "canal vacío, sin actividad".

### Edge case: canal recién creado

Si el canal tiene menos de 7 días de antigüedad (creation date), marcar
R0 como YELLOW (no RED) con detail = "canal nuevo, dar tiempo".

---

## R1 — Comercial SF preguntó y nadie de PC respondió (SECUNDARIA)

**Threshold default: 48 horas.**

```pseudo
latest = MSG_TOP[0]  # más reciente
if is_comercial_sf(latest.user) and (now - latest.ts) > 48h:
    # Verificar que ningún PC humano respondió en thread
    replies = THREADS[latest] or []
    pc_replies = [r for r in replies if is_pc_team(r.user) and not is_bot(r.user)]
    if pc_replies == []:
        R1 = RED
```

---

## R2 — Sin actividad de PC humano en la ventana (SECUNDARIA)

**Threshold default: 7 días.**

```pseudo
pc_human_msgs = [m for m in MSG_TOP if is_pc_team(m.user) and not is_bot(m.user)]
if pc_human_msgs == []:
    last_any = max(m.ts for m in MSG_TOP) if MSG_TOP else None
    if last_any and (now - last_any) > 7d:
        R2 = YELLOW
```

R2 se solapa con R0 cuando el PM = único PC humano. Si R0 ya está RED,
no hace falta sumar R2.

---

## R3 — Thread del comercial SF sin reply de PC (SECUNDARIA)

**Threshold default: 24 horas.**

```pseudo
for mt in MSG_TOP:
    replies = THREADS[mt] or []
    if not replies: continue
    last_reply = replies[-1]
    if is_comercial_sf(last_reply.user) and (now - last_reply.ts) > 24h:
        R3 = YELLOW for this thread
```

Solo threads cuyo **root está en los 10 top-level**. No leas threads
fuera de la ventana.

---

## R4 — @mención a PC sin reply (SECUNDARIA)

**Threshold default: 24 horas.**

```pseudo
for m in MSG_TOP + flatten(THREADS):
    for mention in m.mentions:
        if is_pc_team(mention) and not is_bot(mention):
            # ¿el mencionado respondió después?
            replied = exists(later_msg
                             where later_msg.user == mention
                             and later_msg.ts > m.ts)
            if not replied and (now - m.ts) > 24h:
                R4 = YELLOW
                who_should_respond = mention
```

---

## Edge cases generales

### Bots y webhooks

- Si el único mensaje "del PM" es un webhook que postea en su nombre →
  no cuenta. R0 sigue corriendo.
- Mensajes de Jira/CI/notificadores nunca cuentan como status.
- `is_bot(u) == true` → ignorar para todas las reglas excepto para
  detectar canales con solo bots (caso aparte).

### Reacciones como respuesta

Una reacción 👍 al mensaje del comercial SF **no cuenta** como respuesta
en R1/R3. Solo replies escritos.

### Threads huérfanos

Si un thread tiene replies pero el root fue borrado / quedó fuera de la
ventana de 10 → no procesar.

### Usuarios desactivados

Si el último mensaje viene de un user `deleted: true`, calcular el ts
igual pero marcar el user en el output como "(desactivado)".

### Fines de semana / feriados

No ajustar thresholds por fin de semana — 7 días son 7 días corridos.
Si el PM quiere otro threshold, lo configura en el widget de Fase 0.

### Anomalía: cliente final en el canal

Si detectas un user con dominio del cliente (i.e., dominio del
`Account.Website` o emails del Account.Contacts), no es un caso de
regla — va al bucket `client_anomaly` directamente.

---

## Cómo combinar R0 con R1-R4 en el output

- Cada fila de la tabla principal del artefacto tiene un campo `rule` con
  la regla que disparó. R0 tiene precedencia.
- Si un canal tiene R0 RED + R1 RED, la fila se rotula `R0` (R1 va en
  un campo `secondary_rules` para que el detalle del row la muestre).
- `priority` se calcula así:
  - `red` si R0 = RED.
  - `yellow` si cualquier R1-R4 = RED/YELLOW pero R0 = OK.
  - `white` si todo OK.
