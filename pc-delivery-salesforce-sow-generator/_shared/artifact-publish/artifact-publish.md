<!-- ⚠️ AUTO-COPIADO desde _shared/artifact-publish/ por sync.sh — NO EDITAR ACÁ. Editá el canónico y volvé a correr sync.sh. -->

# Publicar y compartir entregables — el link es el entregable

> **Qué es esto.** La política de ProContacto para compartir entregables: **por link de artefacto,
> no por archivo**. Canónico en `_shared/artifact-publish/`; propagado por `sync.sh`.

## El principio

**Se comparte un link, no un archivo.** Un PDF que sale por mail se congela en el momento en que se
mandó: no se sabe quién lo tiene, en qué versión, ni cómo avisarle que cambió. Un link muestra
siempre lo último, deja rastro de quién lo abrió y se corrige sin volver a mandar nada.

Por eso el **archivo es la excepción que hay que justificar**, no el default. Cuando alguien pide
"mandámelo en PDF", casi siempre lo que quiere es *que la otra persona lo pueda ver* — y eso el link
lo resuelve mejor.

### Cómo se conversa (no es un no, es un mejor)

Nunca niegues el archivo. Ofrecé el link primero, con el motivo en una línea, y si igual lo quieren,
dáselo:

> *"Te paso el link: muestra siempre la última versión, así que si corregimos algo no hay que
> reenviar nada. Si igual necesitás el PDF para adjuntar, decime y te lo genero."*

Motivos que sí mueven la aguja, en el lenguaje del que escucha:

- **No se desactualiza.** Lo que el cliente abre hoy y lo que abre en dos semanas es lo vigente.
- **Se corrige sin reenviar.** Un número mal en un PDF ya mandado no tiene arreglo; en el link, sí.
- **Deja rastro.** Se sabe que se compartió y qué versión se estaba viendo.
- **No pesa.** No hay adjuntos de 20 MB rebotando en la casilla del cliente.

## Gate del conector (bloqueante, y va primero)

**Antes de construir nada, comprobá que el conector del gestor responde.** Una llamada a
`listar_artefactos` alcanza: es de sólo lectura, no escribe nada y es la misma que después necesita
el anti-duplicado.

**Si el conector no está disponible, el skill se detiene ahí.** No construye el entregable "por las
dudas", no lo deja como artefacto de la conversación, no ofrece mandar el archivo en su lugar y no
promete publicarlo después. Le pide a la persona que active el conector y espera.

> *"Necesito el conector del gestor de artefactos de ProContacto para poder entregarte esto, y ahora
> mismo no está disponible. Activalo en los conectores de tu sesión y seguimos — sin él puedo armarlo
> pero no puedo entregártelo de forma que quede versionado y compartible, y prefiero no dejarte un
> archivo suelto que mañana esté viejo."*

**Por qué el gate va antes de construir y no antes de publicar.** Si el chequeo queda para el final,
el trabajo ya está hecho y aparece la tentación de salvarlo por izquierda: *"te lo dejo acá en la
conversación y después lo subimos"*. Ese "después" no existe — la conversación siguiente arranca sin
memoria y el entregable ya se perdió. Frenar antes de gastar el trabajo es lo que hace que la regla
se cumpla sola.

La única salida sin conector es **no producir el entregable**. Si la persona insiste, se le explica
qué pierde (versionado, link estable, trazabilidad, que el equipo encuentre el original) y la decisión
queda registrada en el chat, pero el skill no publica en ningún otro lado.

## El original es HTML, siempre — aunque el entregable final sea otro formato

**Todo entregable se construye como HTML y se publica en el gestor. El `.docx`, el `.xlsx`, el
`.pdf`, el `.pptx` o el texto plano se exportan *después*, desde el chat, a pedido.** No hay
entregables que "nacen" en otro formato.

Esto vale también para las piezas que históricamente salían directo en su formato final — el SOW,
el ADR, el caso de éxito, el diccionario de datos, el Atlas renderizado. El razonamiento es el mismo
que sostiene al motor de decks: **un solo original del que salen todos los formatos**.

| | El HTML publicado | El archivo exportado |
|---|---|---|
| Qué es | El entregable | Una copia, congelada en el momento en que se generó |
| Corregirlo | Nueva versión, misma URL, sin avisar a nadie | Hay que regenerarlo y reenviarlo |
| Quién lo encuentra | Cualquiera con el link, siempre lo último | Sólo quien lo tenga en su casilla |

**Cómo se ofrece el formato.** Una vez publicado, se muestra el link y se ofrece la exportación en el
chat, nunca dentro del artefacto (ver "Exportar exige haber publicado"). El pedido explícito de un
formato no reemplaza la publicación: se publica igual y después se exporta. Que alguien pida "pasámelo
en Word" es un pedido de *archivo*, no un permiso para saltear el original.

## Un solo destino: el gestor

**El entregable vive únicamente en el gestor de ProContacto.** No se publica como artefacto de la
conversación: no hay copia local, no hay dos versiones del mismo documento, no hay ambigüedad sobre
cuál es la real.

La secuencia es:

0. **Se comprueba el conector** (gate de arriba). Sin gestor no se arranca.
1. **Se construye y se verifica localmente** — sin publicar nada. La verificación del motor (tokens
   del DS, nada que desborde, cero errores de consola) corre acá.
2. **Recién cuando pasa la verificación, se publica** en el gestor — siempre precedido por la
   búsqueda anti-duplicado (`listar_artefactos` → `publicar_version` si ya existía, `publicar_artefacto`
   si no). Ese es el entregable.
3. **Se muestra el link en el chat**, en el mismo mensaje. Sin eso el paso 2 es invisible.
4. **Cada modificación es una versión nueva** sobre la misma URL (`publicar_version`, con un
   `message` que diga qué cambió). El link compartido nunca cambia.

**No se publican borradores.** Cada versión del gestor tiene que significar algo — un cambio real,
acordado — no un ajuste a mitad de camino. Si algo está por corregirse, corregilo antes: el gestor
versiona, y esa v1 con un defecto queda en el historial para siempre.

## Cómo se garantiza (una regla escrita no alcanza)

Todo lo de arriba es una intención. Una intención se saltea sin querer: alcanza con que el usuario
pida "mostrámelo" y el skill renderice el HTML donde le quede más a mano. Lo que hace que el
entregable **llegue siempre** al gestor no es recordarlo, son cuatro barreras que lo vuelven el
camino más corto.

### 1 · No existe otro camino para mostrarlo

**Un entregable no se renderiza nunca como artefacto de la conversación.** No es una preferencia: es
que `publicar_artefacto` es *el paso de mostrar*. Si no se publica, no hay nada que ver.

Esto convierte la regla en una imposibilidad práctica en vez de un recordatorio. Los skills no
ofrecen "¿lo querés acá o en el gestor?" — esa pregunta reabre la puerta que estamos cerrando.

> **La excepción son las pantallas de trabajo del chat.** No son entregables: van por
> `mcp__visualize__show_widget` y no se publican en ningún lado. Entran acá dos casos:
>
> 1. **Los widgets de interacción** del propio flujo — elegir carpeta, confirmar una escritura,
>    exportar, ajustar.
> 2. **Los paneles y tableros que el skill declara explícitamente que van por
>    `mcp__visualize__show_widget`.** Varios skills operativos lo dicen en su `description` o en sus
>    reglas duras (por ejemplo `pc-sales-sf-contract-signature-orchestrator`: *"Panel via
>    `mcp__visualize__show_widget` (nunca `create_artifact`)"*). **Esa instrucción manda**: el panel
>    se muestra en el chat y no pasa por el gestor. Un skill así no tiene que invocar esta política
>    ni pasar por `pc-meta-artifact-publisher` — y si alguien se lo sugiere en medio de la corrida,
>    lo correcto es seguir con el widget.
>
> **Cómo distinguirlos cuando el skill no lo dice.** Preguntate para quién es y cuánto vive. Si es
> una vista del estado de HOY para que alguien decida algo ahora (pipeline, hallazgos, checklist de
> revisión), es pantalla de trabajo: se muere con la conversación y versionarla no significa nada.
> Si es algo que alguien va a volver a abrir, compartir o corregir más adelante (propuesta, SOW,
> wireframes, diagrama, documento, deck, informe), es entregable y va al gestor. Ante una duda real,
> preguntale al usuario en una línea — no publiques un panel "por las dudas": ensucia el listado que
> usa el anti-duplicado del paso 3.

### 2 · Lo que el usuario quiere pasa por acá

Exportar a PDF, subir a Drive y compartir el link **exigen que el artefacto ya exista en el gestor**.
No hay que convencer a nadie: quien quiere el PDF publica, porque es el paso previo. La regla se
sostiene sola porque está montada sobre lo que la persona ya venía a buscar.

### 3 · Antes de publicar, buscar siempre (anti-duplicado)

**Éste es el agujero por donde se escapan las actualizaciones.** Una conversación nueva no sabe que
el entregable ya existe, lo publica de cero, y el link que el cliente tiene en el mail queda
congelado para siempre en la v1 sin que nadie se entere. No falla ruidosamente: falla en silencio.

Por eso **publicar es siempre un dos pasos**, nunca uno:

1. `listar_artefactos` y buscar por **título canónico** (ver abajo).
2. **¿Apareció?** → `publicar_version` con `id` y un `message` que diga qué cambió.
   **¿No apareció?** → `publicar_artefacto`, y anotá el `id` que devuelve.

Nunca llames a `publicar_artefacto` sin haber corrido el paso 1, aunque estés seguro de que es nuevo.
El costo de buscar de más es una llamada; el de publicar duplicado es un cliente mirando una versión
vieja.

#### Título canónico (de esto depende que el paso 1 encuentre algo)

```
{Cliente} · {Entregable} · {Tipo}
```

Por ejemplo: `Tiendas del Sol · SOW CG Cloud · Documento`.

**Sin versión y sin fecha en el título.** Un título como `… - SOW CG Cloud - v1` rompe las dos cosas
a la vez: la búsqueda del paso 1 no matchea cuando toca la v2, y contradice el modelo —la versión
vive *adentro* del artefacto, con su historial, no en el nombre. Si ves un artefacto viejo con `v1`
en el título, corregilo al publicar la versión siguiente.

### 4 · El `id` tiene que sobrevivir a la conversación

El `id` se pierde al cerrar el chat, y la conversación que retome el entregable dentro de un mes
necesita encontrarlo. Va en dos lugares, siempre:

- **En el HTML**, dentro del comentario de trazabilidad (`__DECK_TRACE__` / `__DOC_TRACE__` /
  `__WF_TRACE__`): `gestor-id: {id}`. Viaja con el archivo y sobrevive a la copia de Drive.
- **En el registro** (`_shared/artifact-linkage/`): en Salesforce como
  `Project_Asset__c(Type__c='ProContactoArtifactId', Value__c=<el uuid en crudo>)` —el tipo existe
  justamente para esto—, o como issue `Artifact` en Jira. Es lo que hace que el entregable sea
  encontrable desde el deal o el proyecto, no sólo desde el chat donde nació.

  > `Value__c` va **sin** la URL: sólo el uuid de `https://artifacts.procontacto.com.mx/a/{uuid}`.
  > `Link__c` es fórmula y `Name` auto-number → nunca se escriben.
  >
  > Y **siempre con `Description__c`** (≤255): bajo `ProContactoArtifactId` entra cualquier
  > entregable —propuesta, ERD, informe, wireframes—, así que sin descripción dos assets de la misma
  > Opp son indistinguibles. Reusá el título canónico: `{Cliente} · {Entregable} · {Tipo}` ya dice de
  > qué documento se trata.

### 5 · El caso ad-hoc también tiene dueño

Las cuatro barreras de arriba viven **dentro de los skills productores**. Queda un hueco: un HTML
armado en una conversación que no invocó ninguno de ellos — un informe puntual, una tabla que
alguien pidió ver, un documento improvisado. Ahí no hay skill que lea esta política, y un skill no
puede activarse por *ausencia* de disparadores.

Ese hueco lo cierran dos piezas, en este orden:

- **El hook de `SessionStart` del grupo `router`** (`_hooks/router/session-start.sh`) inyecta la
  regla corta en cada sesión de la flota. Es lo único que corre siempre, sin que nadie lo invoque.
- **`pc-meta-artifact-publisher`** es el destino: recibe el HTML, lo envuelve como documento
  completo, corre el dos pasos, muestra el link y ofrece el gate de vinculación.

Si estás en un skill productor, no lo llames: ya tenés la política adentro.

### Checklist de cierre

Antes de dar el entregable por entregado:

- [ ] El conector del gestor se comprobó **antes de construir**, no al final.
- [ ] El original es **HTML**. Si el usuario pidió `.docx`/`.xlsx`/`.pdf`/texto, ese archivo se
      exportó **después** de publicar, y el HTML sigue siendo el entregable.
- [ ] Corrió `listar_artefactos` **antes** de publicar.
- [ ] Está en el gestor, y **no** hay una copia del mismo entregable como artefacto de conversación.
- [ ] El título es el canónico, sin `v1` ni fecha.
- [ ] El link del gestor está **escrito en el chat** (publicar sin mostrar el link es no publicar).
- [ ] El `id` quedó en el trace del HTML y en el registro (`Project_Asset__c` / issue `Artifact`).
- [ ] El asset de SF tiene `Type__c='ProContactoArtifactId'`, `Value__c` = uuid en crudo y
      `Description__c` con qué documento es.
- [ ] Si hubo correcciones después de publicar, cada una es una `publicar_version` con su `message`.

### Qué cambia respecto de publicar en Cowork

- **Un solo empaquetado.** El gestor **no tiene CSP** (verificado 4-ago-2026), así que la tipografía
  de marca va por `<link>` a Google Fonts en vez de embebida como data URI: **110 KB menos** por
  entregable. La versión con fuente embebida queda sólo para la copia offline de Drive.
- **Documento completo, siempre.** `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`. Los shells del
  motor son fragmentos pensados para el host de Cowork: hay que envolverlos.
- **Cuesta tokens.** El HTML viaja en línea, así que publicar un deck son unos 13k. Es la razón por
  la que no se publican borradores: no es sólo prolijidad, es costo real.

> **El artefacto de Cowork no desaparece del todo**: sigue siendo el canal de los **widgets** del
> chat y de vistas de trabajo efímeras. Lo que ya no hace es alojar entregables.

## Los dos destinos, y por qué no compiten

| | Gestor de ProContacto | Artefacto de Claude |
|---|---|---|
| URL | `https://artifacts.procontacto.com.mx/a/{id}` | `claude.ai/…/artifact/{uuid}` |
| Para qué | **Todos los entregables** | Sólo widgets del chat y vistas efímeras |
| Versionado | Sí — misma URL, historial, se puede volver atrás | No |
| Acceso | Google de ProContacto, o palabra clave para externos (ver abajo) | Privado del usuario |
| Trazabilidad | El `id` es el identificador del entregable | No sirve como registro |

**Regla:** **todo entregable va al gestor de ProContacto, y sólo ahí.**

## El modelo de acceso

Al abrir el link pueden pasar dos cosas, según quién sea:

- **Alguien de ProContacto** → entra con su cuenta de Google. Después el permiso puede ser de
  **lectura** o de **lectura y escritura**, o no tener permiso.
- **Alguien externo (el cliente)** → entra con la **palabra clave** que se le compartió aparte.

> ⚠️ **Estado real a 4-ago-2026: el camino del cliente todavía no funciona.** La pantalla de login
> ofrece **sólo Google, restringido a `@procontacto.com.mx`**, y **no tiene ningún campo para la
> palabra clave** — verificado publicando un artefacto con `password` y revisando el HTML servido: no
> hay un solo `<input>`. El parámetro se acepta y el artefacto queda privado, pero el externo no
> tiene cómo usarla.
>
> **Consecuencia para los skills:** con un cliente externo, **no prometas que el link le va a abrir**.
> Compartilo hacia adentro de ProContacto sin problema, y para afuera generá el archivo hasta que el
> ingreso por palabra clave esté disponible. Cuando lo esté, esta sección se actualiza y el archivo
> vuelve a ser la excepción también para clientes.

## Exportar exige haber publicado (regla dura)

**El botón de exportar a PDF o a cualquier otro formato sólo se ofrece una vez que el artefacto está
publicado en el gestor.** Sin excepción.

El motivo es de trazabilidad: un archivo generado desde algo que nunca se registró es un entregable
huérfano — no se sabe de qué versión salió ni con qué se corresponde. Publicar primero garantiza que
todo archivo que circula tiene un original identificable detrás.

En la práctica: si el usuario pide un formato antes de que exista el artefacto en el gestor,
publicalo primero (es un paso, no una pregunta) y después generá el archivo, mencionando el link.

## Herramientas

| Qué | Herramienta |
|---|---|
| **Buscar antes de publicar (siempre)** | `listar_artefactos` — devuelve título, URL, `id`, dueño y versión activa de cada uno. Matcheá por título canónico. |
| Publicar por primera vez | `publicar_artefacto` — `title`, `html` (documento completo), y opcionales `slug`, `password`, `expires_days`. Devuelve URL e `id`. **Anotá el `id`**. |
| Nueva versión, misma URL | `publicar_version` — `id`, `html`, `message` con el cambio |
| Historial | `listar_versiones` — `id` |
| Volver atrás | `volver_a_version` |
| Baja / alta / borrado | `dar_de_baja_artefacto`, `reactivar_artefacto`, `borrar_artefacto` |

Notas de uso verificadas:

- **El HTML tiene que ser documento completo** (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`). Los
  shells del motor son *fragmentos* pensados para el host de Cowork: hay que envolverlos.
- **Nada que dependa del host.** El diagrama de mermaid no sirve acá: Cowork le inyecta el motor de
  mermaid, este gestor no. Sólo HTML autocontenido.
- **Guardá el `id` apenas publicás.** Si se pierde, `listar_artefactos` lo recupera (devuelve título,
  URL, `id`, dueño y versión activa de cada artefacto) — verificado 7-ago-2026, después de haber
  fallado con error 500 el 4-ago. Aun así conviene anotarlo: el listado no dice de qué conversación
  salió cada uno.
- El `slug` lindo redirige al UUID, así que el link que ve el cliente termina mostrando el uuid.

## Versiones

Cada corrección del entregable es una **versión nueva sobre la misma URL** (`publicar_version`), con
un `message` que diga qué cambió. El link compartido nunca se rompe ni cambia.

Esto reemplaza la necesidad de re-subir archivos: quien tenga el link ve lo último sin que nadie le
avise. Es la razón principal por la que el link le gana al archivo.

## Relación con Drive y con el registro

- **Drive** (`_shared/drive-upload/`) sigue siendo el respaldo interno del original re-editable. El
  gestor es el canal para **compartir**; Drive es el archivo de la casa. No compiten.
- **El registro** (`_shared/artifact-linkage/`) engancha el entregable al deal o al proyecto. Con el
  gestor en juego, **lo que se registra es la URL del artefacto** —es la que sobrevive y versiona—,
  con el link de Drive como respaldo si además se subió. En Salesforce eso es un
  `Project_Asset__c` de `Type__c='ProContactoArtifactId'`, con el **uuid** en `Value__c`.
- **El uuid no cambia entre versiones.** `publicar_version` mantiene la misma URL, así que el asset
  registrado una vez sigue siendo válido para siempre: no hay que actualizarlo en cada corrección.
