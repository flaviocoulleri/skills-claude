# Jira Fields Mapping — External Pending

Cómo mapear los campos extraídos (PASO 3) a campos del issue Jira al crear/actualizar.

---

## Create (pending `new`)

| Campo extraído | Campo Jira | Notas |
|---|---|---|
| `titulo` | `summary` | Directo. Truncar a 255 chars si superara (no debería, el prompt limita a 80). |
| `descripcion` | `description` | Ver formato abajo. |
| `dueno_cliente` | `description` (prefijo) | No usar `assignee` — los assignees en Jira son users internos, no contactos del cliente. Dejar el dueño en el texto. |
| `fecha_compromiso` | `duedate` | Formato `YYYY-MM-DD`. Si `null`, no pasar el campo. |
| `fuente_url` | `description` (footer) | Link al final del cuerpo. |
| — | `issuetype` | Siempre `"External pending"` (fijo). |
| — | `project` | El proyecto elegido por el PM en PASO 1. |
| — | `reporter` | `accountId` del PM (obtenido en PASO 0). |
| — | `labels` | `["external-pending", "auto-extracted"]` — útil para filtrar reportes. |
| — | `priority` | No setear por defecto. El PM puede ajustar después. |

### Formato de `description`

Usar Atlassian Document Format (ADF) si el MCP lo requiere, o plain text si acepta ambos.
Plantilla:

```
Dueño del cliente: {dueno_cliente}

{descripcion}

---
Extraído automáticamente desde {fuente_tipo} el {fecha_extraccion}.
Fuente: {fuente_url}
```

Ejemplo renderizado:

```
Dueño del cliente: Laura Gómez (Sura / Seguridad)

El equipo de seguridad de Sura se comprometió a confirmar el acceso al ambiente
de QA para arrancar la integración de SSO.

---
Extraído automáticamente desde transcript el 2026-04-20.
Fuente: https://read.ai/meet/abc123
```

---

## Update (pending `update_date`)

**Solo actualizar `duedate`**. No tocar `summary`, `description`, ni ningún otro campo.

Además, agregar un **comment** en el issue con `addCommentToJiraIssue`:

```
Fecha actualizada automáticamente desde {fuente_tipo}.
  Anterior: {old_duedate}
  Nueva: {new_duedate}
Fuente: {fuente_url}
Extraído el {fecha_extraccion}.
```

### Por qué solo duedate

- Modificar `summary` / `description` al detectar un reschedule rompe la historia del issue
  (el PM pierde el contexto original).
- El cliente postergó una fecha, no cambió el alcance. Si cambió el alcance, eso es un
  pending nuevo (detectado por fuzzy matching como `new` en PASO 4).

---

## Custom fields

Si el proyecto Jira tiene custom fields para "Dueño cliente" o "Fuente", preferirlos al
texto en la description. Para detectarlos, llamar `getJiraIssueTypeMetaWithFields` al
inicio del flujo y cachear el mapping:

```python
# Pseudocódigo
fields = getJiraIssueTypeMetaWithFields(project, "External pending")
customFieldMap = {
  "Dueño Cliente": next((f.id for f in fields if f.name == "Dueño Cliente"), None),
  "Fuente URL":    next((f.id for f in fields if f.name == "Fuente URL"), None),
}
```

Si existen → usarlos en el create/update. Si no → fallback a la description.

---

## Errores comunes y cómo manejarlos

| Error | Causa probable | Acción |
|---|---|---|
| `400 — issuetype not found` | El proyecto no tiene el issue type "External pending" | Detener y pedir al admin de Jira que lo habilite. No elegir otro issue type. |
| `400 — required field missing` | El proyecto tiene un campo custom obligatorio no cubierto aquí | Listar el campo al PM y pedirle el valor antes de reintentar. |
| `403 — permission denied` | El PM no tiene permiso de crear en ese proyecto | Avisar al PM y sugerir que pida acceso o elija otro proyecto. |
| `duedate inválido` | El modelo de extracción devolvió una fecha malformada | Validar con regex `^\d{4}-\d{2}-\d{2}$` antes de enviar; si falla, crear el issue sin duedate y reportar al PM. |

---

## Idempotencia

Si el skill se corre dos veces con el mismo input, el segundo run debería:

- Para pendings que se crearon la primera vez → verlos como `duplicate` (porque ya existen en Jira) → no hacer nada.
- Para pendings con `update_date` → si la fecha ya fue actualizada, ver duedate nuevo = extraído → no hacer nada.

Esto solo se cumple si el fuzzy matching es estable (ver `scripts/dedupe.py`) y el orden
del JQL en PASO 4 es determinístico (`ORDER BY created ASC`).
