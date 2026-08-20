---
name: pc-meta-artifact-publisher
metadata:
  version: 1.0.0
  last_modified: 2026-08-09
  owner: ariel.tarsitano@procontacto.com.mx
  connectors: [artifacts-procontacto, salesforce, jira]
description: >
  Publica en el gestor de artefactos de ProContacto (artifacts.procontacto.com.mx)
  un entregable HTML que se armó en la conversación sin pasar por un skill
  productor: lo envuelve como documento completo, aplica el anti-duplicado de dos
  pasos (listar_artefactos por título canónico → publicar_version si ya existía,
  publicar_artefacto si no), muestra el link y ofrece vincularlo al deal o al
  proyecto. Activar con "publica esto", "súbelo al gestor", "dame el link del
  entregable", "publica una versión nueva", "esto quedó como artefacto de la
  conversación", "publish this artifact". NO actives si el entregable lo produce
  un skill del catálogo (propuesta, SOW, wireframes, diagrama, deck, historias):
  esos ya traen la política adentro y publican solos. NO actives para los paneles
  y widgets que un skill declare explícitamente por mcp__visualize__show_widget:
  son pantallas de trabajo, no entregables, y no se publican en ningún lado. ES/EN.
---

# pc-meta-artifact-publisher — El caso ad-hoc también llega al gestor

## Changelog

- **1.0.0** (2026-08-09): versión inicial. Cierra el hueco que dejaban los 8 skills
  productores: un HTML armado en una conversación que no invocó a ninguno de ellos no tenía
  quién le aplicara la política de publicación. Aplica el módulo canónico
  `_shared/artifact-publish/`, envuelve el fragmento con `assets/documento-completo.html`,
  estampa el `gestor-id` en el trace y cierra con el gate de vinculación.

## Para qué existe

La política de publicación de ProContacto vive en `_shared/artifact-publish/artifact-publish.md`
y viaja **dentro** de los 8 skills que producen entregables. Eso funciona mientras el trabajo
entre por uno de ellos.

El hueco es el resto: alguien pide un informe, una tabla comparativa o un resumen, se arma el
HTML en la conversación, y ahí no hay ningún skill que lea la política. El entregable termina
como artefacto de la conversación — sin versionado, sin trazabilidad y sin forma de que otra
conversación lo encuentre dentro de un mes.

Un skill no puede activarse por **ausencia** de disparadores, así que este skill no se detecta
solo: lo nombra el hook de `SessionStart` del grupo `router`
(`_hooks/router/session-start.sh`), que es lo único que corre en todas las sesiones. El hook
avisa; este skill ejecuta.

## Qué hace y qué no

| Sí | No |
|---|---|
| Toma un HTML **ya armado** (de la conversación, de un archivo, o pegado) y lo publica | **No redacta ni diseña el entregable.** Si todavía no existe, el skill que lo produce es otro |
| Lo envuelve como documento completo, listo para el gestor | No reemplaza a los shells de `_shared/deck-engine`, `doc-engine` ni `wireframe-engine` |
| Corre el anti-duplicado de dos pasos y versiona sobre la misma URL | No borra ni da de baja artefactos (eso es manual, en el gestor) |
| Ofrece el gate de vinculación (`Project_Asset__c` / issue `Artifact`) | No crea la Opportunity ni el proyecto Jira si no existen: deja el registro pendiente |

**Si el entregable lo produce un skill del catálogo, no pases por acá.** `pc-sales-presentation-builder`,
`pc-delivery-presentation-builder`, `pc-crm-salesforce-wireframe-builder`,
`pc-crm-salesforce-data-dictionary-generator`, `pc-crm-userstory-generator`,
`pc-cg-cloud-userstory-generator`, `pc-delivery-salesforce-sow-generator` y
`pc-meta-conversation-to-slidedeck` ya publican solos, con el mismo procedimiento. Llamarlos y
además llamar a este skill duplica el entregable, que es justo lo que la política evita.

## Cómo funciona

**Lo que necesitas tener a mano**: el HTML del entregable (armado en la conversación, en un archivo o pegado), el **cliente o proyecto** al que pertenece, y —si vas a vincularlo— la Opportunity de Salesforce o el proyecto Jira.

**Conectores**: el **gestor de artefactos** de ProContacto (obligatorio), más **Salesforce** o **Jira** sólo para el gate de vinculación del cierre (opcional: sin ellos el registro queda pendiente y el skill termina igual).

**El recorrido, en corto**:

1. Decide si es un **entregable** o una pantalla de trabajo. Si es pantalla, el skill no aplica y te lo dice.
2. Arma el **título canónico** `{Cliente} · {Entregable} · {Tipo}` y te lo muestra.
3. **Busca** el entregable en el gestor (`listar_artefactos`) antes de publicar nada.
4. Envuelve el HTML como **documento completo** con el template de `assets/`.
5. **Publica**: versión nueva sobre la misma URL si ya existía, artefacto nuevo si no.
6. Te da el **link en el chat** y ofrece cómo compartirlo.
7. Ofrece **vincularlo** al deal o al proyecto, siempre con tu OK.

**Lo que te devuelve**: el link del gestor (la URL del entregable, que ya no cambia), el `gestor-id` para el trace del HTML, y el registro en Salesforce o Jira si aceptaste el gate.

---

## Paso 0 — ⛔ Gate: ¿es un entregable o una pantalla de trabajo?

**Se corre siempre, antes de tocar nada.** Publicar lo que no había que publicar ensucia el
listado del que depende el anti-duplicado del Paso 3, y deja versionado algo que no significa
nada.

**No es un entregable — no se publica** en ninguno de estos dos casos:

1. **Widgets de interacción** del propio flujo: elegir una carpeta, confirmar una escritura,
   ofrecer exportar, ajustar algo. Son interfaz.
2. **Paneles y tableros que un skill declara explícitamente que van por
   `mcp__visualize__show_widget`.** Varios skills operativos lo dicen en su `description` o en
   sus reglas duras — por ejemplo `pc-sales-sf-contract-signature-orchestrator`: *"Panel via
   `mcp__visualize__show_widget` (nunca `create_artifact`)"*. También
   `pc-sales-sf-forecast-reviewer`, `pc-sales-sf-commit-pipeline` y
   `pc-legal-sf-contract-validator`.

   > **Esa instrucción del skill manda sobre este skill.** Si estás corriendo uno de ellos y
   > el panel salió por `show_widget`, terminó bien: no lo publiques, no lo ofrezcas, y si
   > alguien lo sugiere a mitad de la corrida, sigue con el widget. Este skill se saltea
   > entero.

**Sí es un entregable** cuando alguien lo va a volver a abrir, compartir o corregir más
adelante: propuesta, SOW, documento, informe, wireframes, diagrama, deck, matriz de alcance.

**La pregunta que los separa, cuando el skill no lo dice**: ¿cuánto vive? Una vista del estado
de HOY, para que alguien decida algo ahora (pipeline, hallazgos, checklist de revisión), se
muere con la conversación y versionarla no significa nada → pantalla de trabajo. Algo que
sobrevive a la conversación → entregable.

Ante una duda **real**, pregúntale al usuario en una línea. Nunca publiques "por las dudas".

---

## Paso 1 — Conseguir el HTML y el contexto

1. **El HTML.** Puede venir de tres lados: armado en esta misma conversación, en un archivo
   del working dir, o pegado por el usuario. Si lo armaste tú recién, ya lo tienes.
2. **De quién es.** Necesitas el **cliente o proyecto** al que pertenece — es la primera parte
   del título canónico y lo que después permite vincularlo. Si no surge del contexto,
   pregúntalo: es una sola pregunta y sin eso el título no matchea nunca.
3. **Qué es.** Tipo de entregable en una o dos palabras (Informe, Matriz de alcance,
   Comparativa, Minuta…).

> Si el HTML todavía no existe y lo que el usuario quiere es que lo armes, ese es otro trabajo:
> hazlo primero (o deriva al skill productor que corresponda) y vuelve acá con el HTML listo.
> **No se publican borradores** — cada versión del gestor queda en el historial para siempre.

---

## Paso 2 — Armar el título canónico

```
{Cliente} · {Entregable} · {Tipo}
```

Por ejemplo: `Tiendas del Sol · Informe de relevamiento · Documento`.

**Sin versión y sin fecha.** Un título como `… · Informe · v2` rompe dos cosas a la vez: la
búsqueda del Paso 3 no matchea en la vuelta siguiente, y contradice el modelo — la versión vive
**adentro** del artefacto, con su historial. Si en el Paso 3 aparece un artefacto viejo con
`v1` en el título, corrígelo al publicar la versión nueva.

Mostrale el título al usuario en una línea antes de seguir. Es barato y evita que el
anti-duplicado falle por una diferencia de nombre.

---

## Paso 3 — ⛔ Buscar antes de publicar (anti-duplicado)

**Éste es el paso que no se saltea nunca**, aunque estés seguro de que el entregable es nuevo.

1. Corre `listar_artefactos`.
2. Busca por el título canónico del Paso 2. Comparación **tolerante**: ignora mayúsculas,
   acentos y el separador (`·`, `-`, `|`), y considera candidato cualquiera que comparta
   cliente + entregable, aunque el tipo esté escrito distinto o arrastre un `v1`.
3. Si hay un candidato dudoso, **muéstraselo al usuario** con su URL y pregunta si es el mismo
   entregable. Es preferible una pregunta a un duplicado.

Por qué importa tanto: una conversación nueva no sabe que el entregable ya existe. Lo publica
de cero, y el link que la otra persona ya tiene en el mail queda congelado en la v1 **sin que
nadie se entere**. No falla ruidosamente: falla en silencio. El costo de buscar de más es una
llamada; el de publicar duplicado es un cliente mirando una versión vieja.

Detalle completo del procedimiento en `_shared/artifact-publish/artifact-publish.md` §3.

---

## Paso 4 — Envolver como documento completo

El gestor sirve el HTML tal cual: **tiene que ser un documento completo** (`<!DOCTYPE html>`,
`<html>`, `<head>`, `<body>`). Los fragmentos pensados para el chat no lo son.

Usa el envoltorio **`assets/documento-completo.html`** — no improvises el `<head>` en cada
corrida. Reemplaza sus tres tokens:

| Token | Con qué |
|---|---|
| `__TITULO__` | El título canónico del Paso 2 |
| `__TRACE__` | El comentario de trazabilidad (Paso 6) |
| `__CUERPO__` | El fragmento tal cual vino, con su `<style>` si lo trae |

Tres cosas que el envoltorio resuelve y conviene no deshacer:

- **La fuente va por `<link>` a Google Fonts, no embebida.** El gestor **no tiene CSP**
  (verificado 4-ago-2026), así que carga sin problema y el entregable pesa **~110 KB menos**.
  La versión con la fuente embebida se reserva para la copia offline de Drive.
- **Define los tokens del host de Cowork** (`--color-text-primary`, `--s-3`, `--border`…). Un
  fragmento armado para el chat suele estilarse con esas variables, que fuera de Cowork no
  existen: publicado en crudo sale sin colores, sin bordes y sin espaciado, y el defecto
  aparece recién cuando alguien abre el link. Si al verificar ves algo sin estilo, el token que
  falta se agrega **al envoltorio**, no se parchea el fragmento.
- **Nada que dependa del host.** Los diagramas de mermaid **no funcionan acá**: Cowork le
  inyecta el motor, el gestor no. Si el fragmento trae un bloque mermaid, hay que renderizarlo
  a SVG antes de publicar (o publicarlo desde `pc-meta-mermaid-diagram-builder`, que ya entrega
  el SVG). Igual con cualquier script que espere una API del chat: `sendPrompt` no existe en el
  gestor, así que un botón cableado a eso es un botón muerto.

**Verifica antes de publicar, no después**: abre el documento envuelto y revisa que no haya
texto sin estilo, desbordes ni errores de consola. Publicar es caro (el HTML viaja en línea) y
cada versión queda en el historial.

---

## Paso 5 — Publicar

Con el resultado del Paso 3:

- **Apareció** → `publicar_version` con el `id` y un `message` que diga **qué cambió**
  ("se corrigió el total del sprint 2", no "actualización"). La URL no cambia.
- **No apareció** → `publicar_artefacto` con `title` (el canónico) y `html` (el documento
  completo). **Anota el `id` que devuelve.**

Sobre `password`: el parámetro se acepta y el artefacto queda privado, pero **hoy no habilita
el acceso externo** — ver los límites verificados más abajo. No lo uses creyendo que le abre el
link al cliente.

---

## Paso 6 — Que el `id` sobreviva a la conversación

El `id` se pierde al cerrar el chat, y la conversación que retome el entregable dentro de un
mes lo necesita para publicar una versión en vez de duplicar. Va en dos lugares:

1. **En el HTML**, dentro del comentario de trazabilidad (token `__TRACE__` del envoltorio):

   ```
   ProContacto · {Cliente} · {Entregable} · {Tipo}
   origen: conversación ad-hoc (pc-meta-artifact-publisher v1.0.0)
   fecha: {AAAA-MM-DD}
   gestor-id: {id}
   ```

2. **En el registro**, por el gate de vinculación del Paso 8.

> **El huevo y la gallina, resuelto sin ensuciar el historial.** En la primera publicación el
> `id` recién existe *después* de publicar, así que el HTML publicado queda sin el `gestor-id`.
> **No publiques una v2 sólo para estamparlo**: sería una versión que no significa ningún
> cambio real, y el módulo compartido lo prohíbe. Estámpalo en la copia local (la que va a
> Drive y la que retienes en la conversación) y deja que entre al gestor **con la próxima
> corrección real**. En una `publicar_version` no hay problema: el `id` ya lo tienes desde el
> Paso 3.

---

## Paso 7 — Mostrar el link y ofrecer cómo compartirlo

**Escribe el link del gestor en el chat, en el mismo mensaje.** Publicar sin mostrar el link es
no publicar.

Después muestra el widget de compartir —
`_shared/artifact-publish/assets/compartir-entregable.html`, con los slots `{{URL_ARTEFACTO}}` y
`{{TIPO}}`— por `mcp__visualize__show_widget`. Ojo con la asimetría, que es a propósito: **el
entregable va al gestor, el widget va al chat.** El widget es interfaz (Paso 0, caso 1).

Si el usuario pide un PDF u otro formato: se genera **después** de publicar, nunca antes. Un
archivo que sale de algo que nunca se registró no tiene original identificable detrás.

---

## Paso 8 — Gate de vinculación (cierre, no bloqueante)

Corre el gate de `_shared/artifact-linkage/artifact-linkage.md`. **Lo que se registra es la URL
del gestor** — es la que sobrevive y versiona. En Salesforce eso es
`Project_Asset__c(Type__c='ProContactoArtifactId', Value__c=<uuid>, Description__c=<qué documento es>)`:
el **uuid solo**, la última parte de `https://artifacts.procontacto.com.mx/a/{uuid}`, nunca la URL
entera. La `Description__c` no es opcional acá: bajo este tipo entra cualquier entregable, así que sin
ella el asset no distingue una propuesta de un ERD. Reusá el título canónico del Paso 3 y mostrala en
el OK para que el usuario la corrija si hace falta.

Como skill de área **meta**, el destino depende de a qué pertenece el entregable, no del área
del skill:

- **Es de un deal** → `Project_Asset__c` en Salesforce, colgado de la Opportunity / Account /
  Contract que corresponda.
- **Es de un proyecto** → issue `Artifact` en Jira (workflow "Deliverable" — **no**
  `Artefacto`).
- **Es interno y no pertenece a ninguno de los dos** → el gate **no aplica**: dilo en una
  línea y cierra.

Busca duplicado antes de crear, ofrece y crea **sólo con OK**, y si falta el contexto de
destino deja el registro pendiente sin bloquear:

> *"El entregable quedó en {link}. Cuando tengas la Opp / el proyecto Jira, corre de nuevo y lo
> engancho."*

---

## Mapa de escritura (Q07)

| Sistema | Qué escribe | Obligatorios | Gate |
|---|---|---|---|
| Gestor de artefactos | `publicar_artefacto` | `title` (canónico), `html` (documento completo) | Paso 3 corrido; Paso 0 pasado |
| Gestor de artefactos | `publicar_version` | `id`, `html`, `message` con el cambio real | El `id` sale del Paso 3, nunca de memoria |
| Salesforce | `Project_Asset__c` | `Type__c='ProContactoArtifactId'` (el tipo del gestor; verificá el picklist con `getObjectSchema`), `Value__c` = **el uuid en crudo** (no la URL), `Description__c` = qué documento es (≤255), lookup al padre | OK explícito; `Name` y `Link__c` **nunca** se escriben (auto-number y fórmula) |
| Jira | issue `Artifact` | proyecto, summary, link | OK explícito; issuetype verificado con el metadata |

Verificación post-write: en el gestor, que la URL devuelta abra; en SF/Jira, releer el registro
creado y devolver el link clickeable.

---

## Límites verificados (no los re-descubras)

- **El acceso del cliente externo todavía no funciona.** La pantalla de login ofrece **sólo
  Google restringido a `@procontacto.com.mx`** y **no tiene ningún campo para la palabra
  clave** — verificado publicando un artefacto con `password` y revisando el HTML servido: no
  hay un solo `<input>`. **Con un cliente externo, no prometas que el link le va a abrir.**
  Hacia adentro de ProContacto se comparte sin problema; para afuera, genera el archivo hasta
  que el ingreso por palabra clave esté disponible.
- **El `slug` lindo redirige al UUID**, así que el link que termina viendo la otra persona
  muestra el uuid. No lo vendas como "link corto y legible".
- **El gestor no tiene CSP** (verificado 4-ago-2026): por eso la fuente va por `<link>` y no
  embebida.
- **Publicar cuesta tokens**: el HTML viaja en línea (un deck son ~13k). Es la razón real por
  la que no se publican borradores.

---

## Estructura del skill

```
pc-meta-artifact-publisher/
├── SKILL.md
├── assets/
│   └── documento-completo.html      ← envoltorio del fragmento (Q01)
└── _shared/                          ← AUTO-COPIADO, no editar acá
    ├── artifact-publish/             ← la política canónica (sync.sh)
    └── artifact-linkage/             ← el gate de vinculación (sync.sh)
```

La política **no se duplica** en este archivo: el canónico es
`_shared/artifact-publish/artifact-publish.md` y se edita ahí, propagándose con su `sync.sh`.
Lo que agrega este skill es el **camino de entrada** para el caso ad-hoc y el envoltorio.
