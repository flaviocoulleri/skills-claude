# 13 · Escalación automática a Ezequiel Veliz

> Este módulo **no** viene de Confluence — es la lógica de escalación propia del skill (agregada en v1.1.0). Referente CI/CD: **Ezequiel Veliz** (`U03MYU8SHD3`). Canal Slack del equipo: `C0B3UQ86VRT`.

## Excepción autorizada a la regla de confirmación

ProContacto exige ✅ antes de **cualquier** acción Slack. Este skill tiene una **excepción autorizada por Ariel** solo para los mensajes de escalación a Ezequiel: destinatario fijo, contenido factual, alta frecuencia → la fricción del ✅ derrota el propósito. **La excepción aplica exclusivamente a la escalación a Eze**; cualquier otra acción Slack sigue la regla normal (draft + ✅).

## Cuándo escalar (4 triggers)

1. **Mismo comando falla 2+ veces** sobre el mismo target.
2. **El usuario lo dice explícito:** "estoy trabado", "no me funciona", "no sé seguir", "I'm stuck".
3. **Errores específicos del pipeline / SF:** `INVALID_SESSION_ID`, `Malformed XML`, governor limits recurrentes, `OAUTH_APPROVAL_ERROR_GENERIC`, `Code coverage <95%` irresoluble, conflictos masivos en `package.xml`.
4. **Pedido directo:** "pásame con Eze", "avísale al referente CI/CD".

## Cómo escalar

Llamar a `mcp__85095b11-725f-49b4-bd0c-062c7d4bcfb9__slack_send_message` con:

- `channel`: `C0B3UQ86VRT`
- `text`: arrobar a `<@U03MYU8SHD3>` + la plantilla de abajo.

**⚠ Antes de armar el cuerpo, redactar secrets** (JWTs, consumer keys, session IDs `00D...`, tokens en URLs). Nunca pegar credenciales en el mensaje.

### Plantilla del mensaje

```
<@U03MYU8SHD3> 🆘 un dev quedó trabado en CI/CD.

• Rol / seniority: <Developer|Admin|Tech Lead> / <Junior|Mid|Senior>
• Repo: <nombre del repo>
• Rama: <rama actual>
• Qué intentaba: <objetivo en 1 línea>
• Qué falló: <error, con secrets redactados>
• Qué ya se intentó: <acciones previas>
• Trigger de escalación: <1|2|3|4>
```

## Después de enviar

Decirle al usuario que **ya avisó a Eze** y proponer un **Plan B** mientras espera (ej. seguir con read-only, dejar el cambio en la rama, documentar en el ticket Jira).
