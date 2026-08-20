# Source Handlers — Cómo invocar cada fuente

Detalle operativo del PASO 2. Una sección por fuente. Leer solo la(s) relevante(s) según lo
que haya disponible en la sesión del PM.

---

## 1. Gmail

**MCP**: `mcp__d9b6b35b-...__search_threads` + `get_thread`.

**Query típico** (cubre el caso "qué hablamos con este cliente en las últimas 2 semanas"):

```
from:{dominio_cliente} OR to:{dominio_cliente} after:{fechaDesde} before:{fechaHasta}
```

Donde `{dominio_cliente}` es el dominio obtenido en PASO 1 (ej: `@sura.com`). Si el PM no
dio el cliente, ampliar con label/filters que indique el PM, o skipear Gmail.

### Qué extraer por thread

Traer el cuerpo de cada mensaje del thread — no solo el último. Los pendings suelen aparecer
en mails intermedios que ya están "contestados" pero siguen abiertos operativamente.

Por cada thread, concatenar los mensajes en orden cronológico con separadores:

```
--- FUENTE: email | {threadUrl} | {fechaUltimoMensaje} ---

[De: <remitente> | Fecha: <ts>]
<cuerpo del mensaje 1>

[De: <remitente> | Fecha: <ts>]
<cuerpo del mensaje 2>
...
```

### Filtrar ruido

Ignorar (o al menos no prioritizar) threads que:

- Son solo confirmaciones ("recibido", "ok", "gracias") sin contenido nuevo.
- Son notificaciones automáticas (Jira, Confluence, GitHub, calendar invites).
- Tienen solo dominios internos (todo `@procontacto.com.mx`).

Regla práctica: si el thread tiene < 50 palabras totales, probablemente no hay pending
extraíble.

---

## 2. Confluence

**MCP**: `mcp__plugin_data_atlassian__searchConfluenceUsingCql` + `getConfluencePage`.

**CQL típico** para notas de reunión con un cliente en una ventana de tiempo:

```
space = "SURA" AND type = "page" AND lastmodified >= "2026-04-05" AND lastmodified <= "2026-04-20"
```

Si no conoces el space del cliente, listar spaces con `getConfluenceSpaces` y preguntar al PM.

### Filtro adicional por título

Las notas de reunión suelen tener títulos con patrones predecibles. Priorizar páginas con:

- "Notas de reunión" / "Meeting notes" en el título
- "Minuta" / "MoM" / "Weekly" / "Sync"
- Fechas en el título (ej: "2026-04-15 - Sura Weekly")

Si hay muchas páginas (> 20), priorizar las que matchean estos patrones primero.

### Extraer contenido

`getConfluencePage` devuelve el body en ADF o storage format. Convertir a texto plano
(stripear tags, preservar listas) antes de pasarle al extraction prompt.

Formato del bloque para el prompt:

```
--- FUENTE: confluence | {pageUrl} | {lastmodified} ---

{contenido en texto plano}
```

---

## 3. Google Docs

**MCP**: no hay un MCP nativo de Google Docs en la org (verificar en runtime con
`mcp__mcp-registry__search_mcp_registry` si hace falta).

**Fallback**: pedir al PM que pegue el link del Doc. Si el link es público (anyone with link),
se puede usar `mcp__workspace__web_fetch` para traer el contenido.

Si el Doc es privado y el PM no lo puede hacer público temporalmente, pedirle que copie el
contenido relevante y lo pegue en el chat.

**Importante**: no intentar extraer Docs privados con scraping o credenciales — respetar
los límites de acceso.

Formato del bloque:

```
--- FUENTE: google_doc | {docUrl o "manual:doc-<slug>"} | {fecha si se conoce} ---

{contenido pegado / fetched}
```

---

## 4. Google Meet

Los transcripts de Google Meet se guardan normalmente como Google Docs en Drive. Tratarlos
como Google Docs (sección 3).

Si el PM tiene el transcript en otra forma (texto pegado, archivo .txt, etc.), usar el
formato `--- FUENTE: transcript | ... ---`.

---

## 5. Read.ai

Sin MCP. Pedir al PM una de estas opciones:

- Link al resumen de Read.ai (si es compartido con la org, `web_fetch` puede traerlo).
- Paste del resumen o transcript completo.

Formato:

```
--- FUENTE: transcript | read.ai/meet/{id o slug} | {fecha} ---

{contenido}
```

---

## 6. Fuentes manuales (catch-all)

Para cualquier cosa que el PM pegue en el chat sin origen claro (ej: "pásame estos notes",
"armé esto yo aparte"), usar:

```
--- FUENTE: manual | manual:paste-{YYYY-MM-DD}-{HHMM} | {fecha que indique el PM} ---

{contenido pegado}
```

El identificador `manual:paste-...` sirve como trazabilidad aunque no sea un link.

---

## Orquestación: orden sugerido

1. Gmail primero — suele tener la mayor densidad de compromisos (el cliente escribe
   específicamente qué va a hacer y cuándo).
2. Confluence segundo — las notas de reunión suelen ser más "declarativas".
3. Transcripts al final — ruidosos, pero a veces tienen el contexto que falta en los dos
   anteriores.

Si el volumen total pasa ~15k tokens, **no consolidar** en una sola llamada al prompt:
correr una llamada por fuente y mergear los resultados al final. Es más caro, pero el modelo
pierde precisión con inputs muy grandes.
