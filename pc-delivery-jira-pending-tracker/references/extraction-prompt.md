# Extraction Prompt — Pendings externos del cliente

Este archivo contiene el prompt que Claude debe correr internamente para extraer pendings
desde un blob de texto (email, transcript, página de Confluence, etc.). El prompt es estricto
a propósito: preferimos cobertura baja con precisión alta, sobre lo opuesto. Un falso positivo
en un `External pending` que termina visible al cliente es costoso; una omisión se recupera
corriendo el skill de nuevo con más contexto.

---

## Cuándo usar este prompt

En PASO 3 del flujo (ver `SKILL.md`). Una vez por cada fuente recolectada, o consolidando
todas las fuentes en una sola llamada si el volumen lo permite (< ~15k tokens de input).

Si se consolida, incluir al inicio de cada bloque la línea:

```
--- FUENTE: <tipo> | <url o identificador> | <fecha> ---
```

para que la extracción pueda anclar cada pending a su fuente.

---

## El prompt

> Tu tarea es identificar **compromisos externos** mencionados en el texto que sigue.
>
> Un **compromiso externo** es una acción futura a la que el **CLIENTE** (no ProContacto,
> no nosotros) se comprometió. Ejemplos:
>
> - "Nos van a enviar las credenciales de SAP el viernes."
> - "El equipo de Finanzas va a confirmar el budget antes del 30/4."
> - "Juan nos pasa el contacto del área de seguridad esta semana."
>
> Un compromiso **interno** (lo que nosotros debemos hacer) NO es un external pending.
> Ejemplos de lo que NO debes extraer:
>
> - "Les vamos a mandar la propuesta el viernes."
> - "Armamos el roadmap y lo pasamos antes del lunes."
> - "Claude va a generar el ADR."
>
> Si el compromiso es ambiguo (no queda claro quién se comprometió), NO lo incluyas.
> Mejor omitir que suponer.
>
> ### Detección de postergación
>
> Si el texto menciona un cambio de fecha para un compromiso que probablemente ya exista
> (ej: "la fecha del assessment que era el 15 se corre al 29", "movemos la entrega del
> catálogo al viernes"), marca ese pending con `tipo_cambio: "reschedule"` y pon la fecha
> nueva en `fecha_compromiso`. No inventes el título del pending viejo — usa el título que
> surge del texto actual; la deduplicación se encargará de matchearlo con lo que ya existe.
>
> Si es un compromiso **nuevo** (no postergación), usa `tipo_cambio: "new"`.
>
> ### Formato de salida
>
> Devuelve **solo** un JSON array, sin texto adicional ni markdown. Cada elemento con estos campos:
>
> ```json
> {
>   "titulo": "Enviar credenciales de acceso SAP",
>   "descripcion": "El equipo de SAP del cliente se comprometió a enviar las credenciales de acceso al ambiente de QA para que arranque la integración.",
>   "dueno_cliente": "Juan Pérez (SAP Lead)",
>   "fecha_compromiso": "2026-04-29",
>   "fuente_url": "https://mail.google.com/...",
>   "fuente_tipo": "email",
>   "tipo_cambio": "new",
>   "confianza": "alta"
> }
> ```
>
> Reglas de cada campo:
>
> - `titulo`: verbo en infinitivo (enviar, confirmar, validar, firmar…) + objeto. Máximo 80 caracteres.
>   NO incluyas "el cliente va a" — ya sabemos que es el cliente.
> - `descripcion`: 1-3 oraciones con el contexto mínimo para que alguien que no estuvo en la
>   reunión entienda de qué se trata. Si no hay contexto suficiente, déjala en `null`.
> - `dueno_cliente`: nombre + rol si están ambos. Si solo hay rol ("el equipo de Finanzas"),
>   pon el rol. Si no hay información, `null`.
> - `fecha_compromiso`: formato `YYYY-MM-DD`. Si la fecha es relativa ("la semana que viene",
>   "antes del viernes"), resuelve contra la fecha de la fuente (que viene en el encabezado
>   `--- FUENTE: … | fecha ---`). Si no hay ninguna fecha mencionable, `null`.
> - `fuente_url`: URL específica del email/doc/página — no la URL raíz del sistema.
> - `fuente_tipo`: uno de `email`, `confluence`, `google_doc`, `transcript`, `manual`.
> - `tipo_cambio`: `new` (compromiso nuevo) o `reschedule` (postergación de fecha).
> - `confianza`:
>   - `alta`: el texto usa verbos claros de compromiso ("se compromete a", "va a enviar",
>     "confirma que envía") + hay un dueño identificado.
>   - `media`: hay compromiso claro pero falta dueño o fecha.
>   - `baja`: es una intención sin compromiso firme ("ideal sería", "podrían ver si…", "queda
>     por confirmar"). **No incluir los de confianza baja** en el output.
>
> ### Texto a analizar
>
> ```
> {{TEXTO_FUENTE}}
> ```

---

## Post-procesamiento del output

Después de que el LLM devuelva el JSON:

1. **Parsear**. Si no es JSON válido, reintentar una vez con una nota: "El output anterior no
   fue JSON válido. Devuelve solo el array JSON, sin markdown ni texto extra."
2. **Filtrar `confianza: "baja"`** si el modelo las incluyó igual (paranoia — el prompt ya
   las excluye pero vale la cintura).
3. **Normalizar fechas** a `YYYY-MM-DD`. Si viene un timestamp, truncar la hora.
4. **Validar `fuente_url`**: si está vacía o no es una URL, reemplazar por el identificador de
   la fuente (ej: `manual:paste-2026-04-20-0934` si fue un paste del PM).

---

## Ejemplos de entrada → salida

### Ejemplo 1 — Transcript con mix interno/externo

**Input:**
```
--- FUENTE: transcript | read.ai/meet/abc123 | 2026-04-18 ---

Ariel: Entonces quedamos que el martes les mandamos la propuesta revisada.
Laura (Sura): Perfecto. De nuestro lado, el equipo de seguridad va a confirmar el acceso
al ambiente de QA antes del jueves 24. Yo te lo chequeo.
Ariel: Listo. Y el tema del SSO, ¿lo vemos en la próxima?
Laura: Sí, pero necesito que nos pasen el documento técnico antes. Ahí lo revisamos.
Ariel: Te lo mando el miércoles.
```

**Output esperado:**
```json
[
  {
    "titulo": "Confirmar acceso al ambiente de QA",
    "descripcion": "El equipo de seguridad de Sura se comprometió a confirmar el acceso al ambiente de QA. Laura (Sura) hace el seguimiento interno.",
    "dueno_cliente": "Laura (Sura) / Equipo de Seguridad",
    "fecha_compromiso": "2026-04-24",
    "fuente_url": "read.ai/meet/abc123",
    "fuente_tipo": "transcript",
    "tipo_cambio": "new",
    "confianza": "alta"
  }
]
```

Notas: "mandamos la propuesta", "te lo mando el miércoles" son internos (ProContacto).
El SSO no tiene compromiso firme del cliente — es una intención a futuro condicional.

---

### Ejemplo 2 — Email con postergación

**Input:**
```
--- FUENTE: email | https://mail.google.com/mail/u/0/#inbox/xyz | 2026-04-19 ---

Asunto: Re: Assessment Fase 2 - Fechas
De: Carlos Méndez <carlos.mendez@sura.com>

Ariel,

Te cuento que la fecha del assessment que habíamos quedado para el 22/4 la tenemos que
mover. El equipo de arquitectura de nuestro lado tiene un cierre de otro proyecto esa
semana. ¿Podemos correrlo al 6 de mayo?

Saludos,
Carlos
```

**Output esperado:**
```json
[
  {
    "titulo": "Assessment Fase 2",
    "descripcion": "Carlos (Sura) pide correr la fecha del assessment del 22/4 al 6/5 por cierre de otro proyecto en arquitectura.",
    "dueno_cliente": "Carlos Méndez (Sura)",
    "fecha_compromiso": "2026-05-06",
    "fuente_url": "https://mail.google.com/mail/u/0/#inbox/xyz",
    "fuente_tipo": "email",
    "tipo_cambio": "reschedule",
    "confianza": "alta"
  }
]
```

Notas: el título `"Assessment Fase 2"` es genérico a propósito — la deduplicación contra
Jira va a matchearlo con el issue existente por fuzzy matching. Si el modelo lo devolviera
con un título muy específico tipo "Correr la fecha del assessment del 22 al 6", perderíamos
el match y crearíamos un duplicado.

---

### Ejemplo 3 — Texto sin compromisos extraíbles

**Input:**
```
--- FUENTE: confluence | ... | 2026-04-17 ---

Notas de reunión semanal:
- Revisamos el pipeline del Q2.
- El cliente comentó que están pensando en sumar el módulo de reportes pero todavía no está definido.
- Próxima reunión en dos semanas.
```

**Output esperado:**
```json
[]
```

Notas: "están pensando" = intención, no compromiso. Confianza baja → filtrada.
