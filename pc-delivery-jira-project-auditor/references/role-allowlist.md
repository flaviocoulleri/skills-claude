# Allowlist de PMs y Scrum Masters autorizados

Este archivo lista los emails de Atlassian autorizados a aprobar cambios en el flujo de `pc-delivery-jira-project-auditor`. Lo lee el skill en PASO 0 para validar el rol del usuario que invoca.

## Cómo se usa

El skill llama a `atlassianUserInfo` y captura el `email`. Si ese email aparece en la sección **Activos** de abajo, el flujo continúa normal. Si no aparece, el flujo continúa igual pero el comentario de auditoría que se deja en cada issue actualizado lleva la marca **`rol no verificado`**.

No se bloquea el flujo cuando un email no está en la lista. La razón: una allowlist desactualizada genera más fricción que valor. La trazabilidad queda en el comentario de Jira y eso es suficiente para auditoría posterior.

## Cómo se mantiene

- Se actualiza manualmente. No hay sync automático con Salesforce ni con Google Workspace.
- Cada entrada lleva nombre + email + rol + fecha de alta + (opcional) fecha de baja.
- Cuando alguien deja de ser PM/SM, se mueve a **Inactivos** con la fecha. No se borra — la trazabilidad histórica importa para entender comments viejos.
- Owner de este archivo: Ariel Tarsitano (ariel.tarsitano@procontacto.com.mx).

## Activos

| Nombre | Email | Rol | Alta |
|---|---|---|---|
| _(pendiente — completar antes del primer run productivo)_ | | | |

## Inactivos

| Nombre | Email | Rol | Alta | Baja |
|---|---|---|---|---|
| _(vacío)_ | | | | |

---

## Nota sobre el primer run

Hasta que esta tabla esté poblada, **todos los runs van a quedar marcados como `rol no verificado`** en los comentarios. Eso está bien — el skill funciona igual, sólo que el log queda incompleto. Es preferible eso a bloquear y forzar mantenimiento de una lista que todavía nadie validó.

Cuando Ariel valide la lista inicial de PMs/SMs activos en ProContacto, este archivo se actualiza con el set definitivo y los runs siguientes ya quedan con trazabilidad completa.
