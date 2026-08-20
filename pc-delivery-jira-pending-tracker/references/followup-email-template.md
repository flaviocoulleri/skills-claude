# Follow-up Email Template — Pendings vencidos

Template para el draft de email que se crea en PASO 6 cuando hay `External pending` con
`duedate < hoy` y status abierto. El objetivo es pedirle al cliente una actualización de
fechas de compromiso, de forma profesional y no acusatoria.

---

## Principios

- **Tono**: cordial, colaborativo. No escribir como "reclamo" — el cliente puede tener mil
  razones por las que se atrasó, la mayoría legítimas.
- **Claridad**: listar los pendings de forma concreta con fechas comprometidas originales.
  No mezclar con otros temas.
- **Llamado a acción**: pedir nuevas fechas estimadas, no solo "updates". Sin fecha, el
  pending sigue sin cerrarse.
- **Firma**: la del PM que corre el skill — no una firma genérica de ProContacto.
- **Idioma**: español por defecto. Si el cliente históricamente se comunica en inglés (detectable
  por el thread de Gmail más reciente), cambiar a la versión en inglés de abajo.

---

## Template — Español (default)

**Asunto**:
```
Seguimiento de pendientes - {Nombre del cliente}
```

**Cuerpo**:
```
Hola {nombre_contacto_principal},

Espero que estés bien. Te escribo para hacer un seguimiento sobre algunos pendientes
que quedaron de tu lado y cuyas fechas comprometidas ya pasaron. Sabemos que a veces
surgen prioridades, así que simplemente queremos acomodar las nuevas fechas para
mantener el proyecto sincronizado.

Los pendientes son los siguientes:

{lista_pendings}

¿Podrías confirmarnos una fecha estimada actualizada para cada uno? Con eso
actualizamos el tracking de nuestro lado y alineamos cualquier dependencia que haya
en el roadmap.

Cualquier duda, quedo atento.

Saludos,
{nombre_pm}
{rol_pm} | ProContacto
```

**Formato de `{lista_pendings}`**:

```
- {titulo} — fecha original: {duedate_original} (atraso: {dias} días)
  Contexto: {descripcion_corta}
- {titulo} — ...
```

Ejemplo renderizado:

```
- Enviar credenciales de acceso SAP — fecha original: 2026-04-10 (atraso: 10 días)
  Contexto: Acceso al ambiente de QA para arrancar la integración.
- Confirmar disponibilidad del equipo de arquitectura — fecha original: 2026-04-05 (atraso: 15 días)
  Contexto: Para agendar el assessment de Fase 2.
```

---

## Template — Inglés

**Subject**:
```
Follow-up on pending items - {Client name}
```

**Body**:
```
Hi {contact_name},

I hope you are doing well. I am following up on a few pending items on your side whose
committed dates have passed. We understand priorities shift, so we just want to align
on the new timelines to keep the project in sync.

The items are:

{pending_list}

Could you confirm an updated target date for each one? Once we have that, we will
refresh our tracking on this side and align any downstream dependencies.

Happy to jump on a quick call if easier.

Best,
{pm_name}
{pm_role} | ProContacto
```

---

## Campos a completar por el skill

| Placeholder | De dónde sale |
|---|---|
| `{Nombre del cliente}` | De PASO 1 (si el PM lo especificó) o del proyecto Jira |
| `{nombre_contacto_principal}` | Preguntar al PM — el skill no debería asumirlo |
| `{lista_pendings}` | Los issues vencidos seleccionados en el artifact |
| `{titulo}`, `{duedate_original}`, `{dias}`, `{descripcion_corta}` | Del issue Jira |
| `{nombre_pm}`, `{rol_pm}` | De `atlassianUserInfo` (PASO 0) |

---

## Qué NO hacer

- No enviar el email automáticamente. Siempre crear un **draft** en Gmail con
  `create_draft`, y avisar al PM: "Revisa el draft y edita antes de enviar".
- No incluir más de 5-6 pendings en un solo email. Si hay más, el email se vuelve abrumador
  — mejor sugerir al PM agruparlos por dueño del cliente y mandar emails separados.
- No mencionar "está atrasado" / "no cumpliste" / "nos dijiste que…". Usar "fecha
  comprometida ya pasó" / "nos alineamos con nuevas fechas".
- No copiar stakeholders internos sin permiso explícito del PM. Default: solo el contacto
  principal del cliente.
