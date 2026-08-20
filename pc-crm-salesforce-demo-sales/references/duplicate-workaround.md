# Workaround de reglas de duplicados — Contact homónimo del Lead

## Contexto

El escenario de demo pide un `Contact` con el **mismo nombre y apellido** que el `Lead` creado, relacionado a la `Account` de la demo. En la mayoría de los orgs de Salesforce, las **Duplicate Rules** estándar (Lead/Contact) matchean por combinación de Nombre + Email o Nombre + Teléfono, y van a bloquear o alertar la creación de un Contact que sea un calco exacto del Lead.

Esto es un pedido **explícito** del usuario para fines de demo (mostrar el mismo prospecto en dos roles del proceso comercial) — no es una forma de evadir controles de calidad de datos en un dataset real.

## Regla exacta

Al crear el Contact #1 (el homónimo):

1. **Nombre y Apellido**: idénticos al Lead. Esto es intencional — no variar.
2. **Teléfono**: tomar el `Phone` del Lead y **quitar el último dígito**.
   - Ej.: Lead `Phone = "+54 11 4555 1234"` → Contact `Phone = "+54 11 4555 123"`.
3. **Email**: tomar el `Email` del Lead y **quitar la última letra de la parte local** (la porción antes del `@`), dejando el dominio intacto.
   - Ej.: Lead `Email = "juan.perez@acme.com"` → Contact `Email = "juan.pere@acme.com"`.
   - No truncar el dominio ni dejar un email inválido (sin `@` o sin parte local).

## Por qué este approach y no otro

- Cambiar nombre/apellido rompería el propósito del escenario (se pide que sea la "misma persona").
- Recortar un dígito del teléfono y una letra del email es suficiente para que la mayoría de las duplicate rules estándar (que matchean por igualdad exacta o fuzzy match configurado) no bloqueen la inserción, sin dejar el dato irreconocible.
- Si el org tiene duplicate rules más estrictas (fuzzy match por nombre solo) y el Contact sigue bloqueado pese al ajuste, **no forzar el insert con `DuplicateRuleHeader.allowSave=true` sin avisar** — reportar el bloqueo al usuario y preguntar si se aprueba forzar el guardado o si prefiere ajustar el dato de otra forma.

## Fallback probado — el ajuste solo no siempre alcanza

**Corrida real (2026-07-29, org `sdo_comercial`)**: el ajuste de teléfono/email de arriba **no fue suficiente** — la duplicate rule de ese org matcheaba por otro criterio (aparentemente Nombre, sin considerar teléfono/email) y bloqueó el insert igual (`DUPLICATES_DETECTED`). Esto confirma que el ajuste es un primer intento razonable, pero **no una garantía** — depende de cómo esté configurada la duplicate rule de cada org, y eso no se puede saber sin intentarlo.

Cuando el Contact sigue bloqueado pese al ajuste:

1. **No reintentar variando más el dato** por default (cambiar nombre/apellido rompe el propósito del escenario). Reportar el bloqueo al usuario tal como dice la regla de arriba, con el mensaje de error real de la duplicate rule.
2. **Preguntar explícitamente** cómo seguir — no asumir. Opciones típicas a ofrecer: (a) forzar el guardado saltando la regla puntualmente en este registro, (b) ajustar también el nombre para evitar el match, (c) omitir este Contact.
3. **Si el usuario aprueba forzar**, usar `Database.DMLOptions` con `DuplicateRuleHeader.allowSave = true` en un insert separado (no en el batch original, para no arriesgar el resto del lote):

```apex
Database.DMLOptions dml = new Database.DMLOptions();
dml.DuplicateRuleHeader.allowSave = true;
dml.DuplicateRuleHeader.runAsCurrentUser = true;
Database.SaveResult sr = Database.insert(contactRecord, dml);
```

4. **Reconectar lo que haya quedado huérfano.** Si otros registros ya se crearon apuntando a este Contact (p. ej. `Quote.ContactId`) y se insertaron con el lookup en blanco porque el Contact todavía no existía, hacer un `update` puntual de esos registros una vez que el Contact fuerza-insertado tiene Id. No dar la corrida por terminada con lookups colgados.

## Alcance de esta excepción

Este workaround aplica **únicamente** dentro de este skill, para el propósito específico de generar un dataset de demo. No es un patrón a reutilizar en flujos de creación de datos reales/producción sin una instrucción equivalente explícita del usuario en ese contexto.
