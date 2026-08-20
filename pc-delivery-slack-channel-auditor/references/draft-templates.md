# Draft templates

Templates de borradores para el flujo. **Ningún draft se postea sin
aprobación expresa por widget.** Default: el PM copia y pega.

## Convenciones

- Tono cercano pero profesional, en español.
- Sin emojis salvo en bienvenida.
- Mantener entre 60 y 200 palabras.
- Cerrar con apertura para feedback.

Placeholders:
- `<PROJECT>` — `Project__c.Name`.
- `<ACCOUNT>` — `Account__c.Name`.
- `<PM_FIRSTNAME>` — primer nombre del PM.
- `<COMERCIAL_SF_FIRSTNAME>` — primer nombre del comercial SF.
- `<DAYS_SILENT>` — días desde el último post del PM.
- `<NEXT_MILESTONE>` — próximo hito (si existe en SF).
- `<NEXT_DATE>` — fecha del próximo hito.

---

## Status para comercial SF (uso primario, R0)

### Variante A — Status semanal

```
Hola <COMERCIAL_SF_FIRSTNAME>, paso update de <PROJECT> con <ACCOUNT>:

Avance esta semana:
• [Hito o entregable principal]
• [Bloqueo resuelto / decisión cerrada]
• [Otro punto relevante]

Próximas fechas:
• <NEXT_MILESTONE> — <NEXT_DATE>

Si quieres sumar algo desde el lado comercial o necesitas material para
el cliente, avísame por acá.
```

### Variante B — Recuperar silencio largo (>14 días)

```
Hola <COMERCIAL_SF_FIRSTNAME>, retomo este canal con un update de
<PROJECT>. Estuve heads-down con [contexto] y se me pasó postear acá.

Estado actual:
• [resumen ejecutivo en 2-3 líneas]

Próximas fechas:
• <NEXT_MILESTONE> — <NEXT_DATE>

Te paso este update también porque sé que estás cerca del cliente y
quiero que tengas todo a mano si surge la conversación. Cualquier cosa,
seguimos por acá.
```

### Variante C — Hito alcanzado

```
Hola <COMERCIAL_SF_FIRSTNAME>, te aviso que cerramos <NEXT_MILESTONE>
en <PROJECT> con <ACCOUNT>.

Lo hicimos en [tiempo / scope]. El cliente reaccionó [feedback breve].

Próximo foco: [siguiente bloque de trabajo].

Si te sirve este input para alguna conversación con el cliente, dime
y te paso material.
```

---

## Bienvenida-comercial-sf

Para postear cuando se acaba de crear el canal (Fase 7 de onboarding).

```
Hola equipo 👋, abro este canal para mantenerte al tanto del proyecto
<PROJECT> con <ACCOUNT>.

Voy a postear status semanal acá: avance del sprint, hitos cumplidos
y próximas fechas. Si necesitas algo puntual, taggeame en este canal.

— <PM_FIRSTNAME>
```

---

## R1 — Reply a comercial SF que no recibió respuesta

Cuando el comercial SF posteó algo y nadie del equipo PC respondió hace
+48h.

```
Hola <COMERCIAL_SF_FIRSTNAME>, perdón la demora. Sobre lo que
mencionaste de [tema]:

[respuesta concreta / próximo paso / fecha]

Si necesitas algo más, dime.
```

---

## R2 — Reactivar canal sin actividad PC

Cuando ningún humano de PC posteó en la ventana, sin que haya un mensaje
puntual del comercial pendiente.

```
Hola <COMERCIAL_SF_FIRSTNAME>, retomo este canal con un check rápido
de <PROJECT>. Estamos [estado en una línea]. Si necesitas algo puntual
de mi lado, dime por acá.
```

---

## R3 — Reply en thread del comercial SF

Cuando hay un thread abierto cuyo último reply es del comercial.

```
Hola <COMERCIAL_SF_FIRSTNAME>, sobre lo que comentas en el thread:

[respuesta concreta]

Si quieres profundizamos en otro thread, o lo armamos en una call corta.
```

---

## R4 — Responder mención sin reply

Cuando alguien @taggeó a un user PC y no respondió hace +24h.

```
Hola <COMERCIAL_SF_FIRSTNAME>, vi tu mención. Sobre [tema]:

[respuesta concreta]

Si quieres más detalle, dime y armo un punteo aparte.
```

---

## Pedir mail comercial SF (mensaje DM al PM, NO al canal)

No es un mensaje al canal externo — es un draft para que el PM se
recuerde a sí mismo. Solo para casos donde el flujo se interrumpe y
hay que retomar mañana.

```
Recordatorio para ti: necesito el mail del comercial SF de
<PROJECT> (<ACCOUNT>) para crear el canal externo. Tipealo en el
widget cuando retomes.
```

---

## Anti-patrones de templates

- **Mismo draft idéntico en N canales** — si el PM tiene 5 proyectos
  con R0 RED, no generes 5 drafts idénticos. Ofrece un template único
  con variables y deja que el PM ajuste por proyecto.
- **Draft asumiendo que el comercial sabe del proyecto** — el comercial
  SF puede tener 50 cuentas en seguimiento. Siempre incluir
  `<PROJECT>` y `<ACCOUNT>` en la primera línea.
- **Draft con info que sale solo del lado del cliente** — el comercial
  SF no necesita detalle técnico fino, sino estado, hitos y fechas.
- **Postear sin que el PM haya leído el draft** — regla de seguridad
  inflexible. Ver `safety-rules.md`.
