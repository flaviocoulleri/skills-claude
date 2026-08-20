<!-- ⚠️ AUTO-COPIADO desde _shared/presentation-builder/ por sync.sh — NO EDITAR ACÁ. Editá el canónico y volvé a correr sync.sh. -->

# Reglas comunes de la familia presentation-builder

> **Qué es esto.** El contrato compartido por TODOS los skills de la familia
> `presentation-builder` (comercial, delivery y los que se sumen). Vive una sola vez en
> `_shared/presentation-builder/` (fuente única de verdad) y `sync.sh` lo copia dentro de cada
> skill como `_shared/references/common-rules.md`. **No lo edites en la copia de un skill** —
> edita el canónico y vuelve a correr el sync.
>
> Cada `SKILL.md` de la familia declara: *"Las reglas de `_shared/references/common-rules.md`
> aplican íntegras."* Lo que sigue es ese cuerpo común; el `SKILL.md` sólo agrega lo específico
> de su área.

## Salida del skill (qué produce y qué NO)

**La salida es la presentación terminada y publicada en el gestor de artefactos de ProContacto,
con su link.** El skill ya no entrega un encargo para otra herramienta ni un archivo adjunto:
entrega **un link que muestra siempre la última versión**. Cómo se construye está en
`_shared/deck-engine/deck-engine.md`; cómo se publica y comparte, en
`_shared/artifact-publish/artifact-publish.md`; los formatos, en
`_shared/deck-engine/export-formats.md`.

### Camino por defecto (recomendado, y hay que defenderlo)

0. Se resuelve el contenido (estructura, arco narrativo, gate anti-placeholder).
1. **Se construye el deck** siguiendo el motor y **se verifica localmente** — sin publicar nada.
2. **Se publica en el gestor de ProContacto** (`publicar_artefacto`) y **se muestra el link en el
   chat** — ver `_shared/artifact-publish/artifact-publish.md`. Es el único destino: no hay artefacto
   de la conversación para entregables.
3. **Se ofrece compartir o ajustar** con `_shared/artifact-publish/assets/compartir-entregable.html`.
   El primer botón es **compartir el link** — el link es el entregable; el archivo es la excepción.
4. **Sólo si insisten con el archivo**, se genera el formato con
   `_shared/deck-engine/scripts/export-deck.mjs` y se entrega en el chat.
5. **Se sube el HTML a Drive** como respaldo interno y **se engancha al registro**: la **URL del
   artefacto** queda como `Project_Asset__c` de la Opportunity (comercial) o como issue `Artifact`
   del proyecto Jira (delivery).

**Cada modificación es una versión nueva en el gestor** (`publicar_version`), sobre la misma URL. No
se publican borradores: cada versión tiene que significar un cambio real.

> **Exportar exige haber publicado.** El botón de PDF u otro formato **no se ofrece** hasta que el
> entregable esté en el gestor. Un archivo generado desde algo no registrado es un entregable
> huérfano: no se sabe de qué versión salió.

> **La exportación se pide en el chat, no dentro del deck.** El deck es un visor: navegación, índice
> y notas del orador, nada más. El export pasa por el agente a propósito — así queda registrado qué
> se generó y de qué versión salió, que es toda la razón de la regla anterior.

Por qué este camino y no otro, en el lenguaje que hay que usar con el usuario:

- **El link no se desactualiza.** Lo que abren hoy y lo que abren en dos semanas es lo vigente. Un
  PDF mandado por mail se congela en el momento en que salió.
- **Se lleva todos los formatos igual.** Si de verdad hace falta el archivo, PDF, imágenes y PPTX
  salen del mismo original. No es "en vez de PowerPoint": es PowerPoint **y** el link.
- **Una sola fuente de verdad, versionada.** Se corrige una vez sobre la misma URL. No hay tres
  versiones circulando ni nadie preguntando cuál es la buena.
- **Los ajustes se piden en la misma conversación**, con todo el contexto del cliente ya cargado.

### Si el usuario pide un `.pptx`, `.docx` o "hacelo en PowerPoint"

**No te niegues y no lo derives**: es exactamente lo que este camino resuelve. Armá el deck y
entregale el `.pptx` exportado. Una línea alcanza:

> *"Te lo armo acá y te lo exporto a PowerPoint: sale del mismo deck, así que se ve igual, y si hay
> que cambiar algo lo corregimos acá y te lo vuelvo a exportar."*

Aclará una sola vez que en el `.pptx` cada diapositiva es la imagen del slide (el texto no queda
editable en PowerPoint) y que **el lugar para editar es el deck**. No invoques las skills `pptx` /
`docx` para esto: producen otro archivo, desconectado del original.

### Claude Design — en retiro

ProContacto **está discontinuando el uso de Claude Design** para presentaciones. Sigue disponible
como camino secundario, pero:

- **No hay elección previa.** El deck se construye acá y punto: preguntar "¿cómo te lo entrego?"
  antes de que exista el entregable pone una bifurcación donde todavía no hay valor que comparar.
- **Claude Design vive como la ÚLTIMA opción** del widget post-entrega
  (`_shared/artifact-publish/assets/compartir-entregable.html`), después de compartir y de los
  formatos, con borde punteado y la etiqueta "En retiro". Disponible, no recomendado, y se ve que no
  es el camino.
- Si el usuario lo pide, **decí una vez por qué conviene el otro camino** (los cuatro motivos de
  arriba, en dos oraciones — no un sermón) y ofrecé armarlo acá.
- **Si insiste, hacelo sin fricción**: generás el prompt como antes (ver "Camino heredado" más
  abajo) y seguís. La decisión es del usuario; se le informa, no se le bloquea.
- No lo describas como roto ni prometas una fecha de baja que no tenés.

### Camino heredado — prompt para Claude Design

Sólo cuando el usuario lo elige expresamente tras la recomendación. Se ensambla el prompt siguiendo
`_shared/assets/prompt-skeleton.md` y se entrega en bloque de código (Patrón E). Rigen las mismas
reglas de contenido (deck-craft, anti-placeholder, nomenclatura, trazabilidad) y las dos
verificaciones de apertura del prompt, pedidas **de a una**: (1) que "ProContacto Design System" sea
el único Design System seleccionado; (2) que el usuario pegue la URL del proyecto
(`https://claude.ai/design/p/{id}`), que se incrusta invisible en el HTML. El modelo Sonnet se
sugiere, no bloquea.

## Consistencia visual obligatoria (Patrones A–E)

- Toda interacción que requiera elección o input se renderiza vía `mcp__visualize__show_widget` siguiendo los patrones de `_shared/references/ui-patterns.md`. **Lee ese archivo antes del primer widget.**
- No se permite listar opciones como bullets en el chat ni usar `AskUserQuestion` para elecciones cubiertas por los patrones A–D.
- Única excepción: la entrega del prompt final (Patrón E — bloque de código copiable en chat).
- Idioma del widget = idioma de la conversación (default español). Tono cercano, no corporativo.

## Enriquecimiento por conectores

- **Nunca preguntes al usuario qué conectores barrer.** Usa todos los disponibles (regla de memoria: barrido multi-fuente sin picker). Ver `_shared/references/connector-sweep.md`.
- El fetch del sitio del cliente (web-first) es independiente del barrido de conectores.
- Resume lo encontrado en un widget con checkboxes y deja que el usuario marque qué sumar al prompt. No es todo-o-nada. Cita la fuente de cada señal.
- No inventes señales: sólo lo que está textualmente en la fuente.

## Chequeo de completitud (gate anti-placeholder, bloqueante)

Antes de ensamblar el prompt, corre SIEMPRE este gate:

1. Arma mentalmente el prompt y detecta qué campos quedarían sin valor real.
2. Clasifica cada faltante:
   - **Requerido** (sin esto el deck no tiene sentido) → **pregúntalo**. No se avanza sin resolverlo.
   - **Opcional** (puede no ir en el deck) → **pregunta primero si quieres incluirlo**; si el usuario dice que no, **se omite la sección entera** — nunca se deja un marcador.
3. Presenta los faltantes en UN solo widget cuando se pueda (Patrón B; opcionales con toggle "incluir / omitir"). Binarios → Patrón A.
4. **Pasada final de texto sobre el prompt ensamblado**: si contiene cualquier `[...]` de relleno (`[A completar]`, `[nombre]`, `[email]`, `[TBD]`, `[TODO]`, corchetes sin resolver), **no lo entregues** — vuelve a preguntar el dato. Los únicos corchetes admisibles son instrucciones internas dirigidas a Claude Design (ej. `[CLIENTE]` dentro de una instrucción explícita), nunca valores que el usuario debía completar.

> **Principio rector:** el usuario recibe un prompt que puede pegar y mandar tal cual. Si algo falta, se resuelve *acá*, preguntando — jamás se delega "complétalo a mano" al output.

## Ensamble del prompt (Paso 5, común)

- **`_shared/assets/prompt-skeleton.md` es la fuente única del formato del prompt.** Léelo y síguelo al instanciar (cubre los sub-flujos, no lleva placeholders, marca qué secciones son condicionales). Si editas el formato, edita el skeleton.
- **Antes de ensamblar, lee `_shared/references/deck-craft.md`** y pega su "Bloque para el prompt" textual en la sección "Principios de diseño del deck". Sin esa capa, Claude Design produce slides sueltas en vez de un deck que cuenta una historia.
- La estructura del deck **nunca** se entrega como lista pelada de títulos: cada slide va con su intención (qué debe lograr).
- El prompt abre con **dos verificaciones obligatorias, pedidas DE A UNA** (mensajes separados, esperando respuesta entre cada una): (1) "ProContacto Design System" es el **único** Design System seleccionado; (2) el usuario pega la URL del proyecto (`https://claude.ai/design/p/{id}`), que se incrusta invisible en el HTML. El **modelo Sonnet** se **sugiere** (no bloquea).
- **Nomenclatura obligatoria** del título del deck y del archivo: `ProContacto - {cliente} - {descripción} - {versión}`. La versión sube en cada iteración.
- **Trazabilidad invisible**: el HTML incrusta como comentario/`<meta>` oculto la URL del proyecto de Claude Design.
- **HTML standalone**: un único archivo autocontenido (CSS/JS/imágenes inline), sin dependencias externas, para abrirlo y subirlo a Drive sin romperse.
- Aplicá el manual de marca vía `pc-admin-interno-brand-applier` (referenciado en el prompt). Adaptá idioma **y dialecto** al país del cliente (voseo/tuteo/usted), nunca español neutro genérico.

## Carpeta de Drive destino (Paso 4.8, procedimiento común)

El prompt lleva la URL de la carpeta de Drive donde Claude Design subirá el HTML. **Las rutas y los IDs raíz son específicos de cada área** — están en el `drive-structure.md` del skill. El procedimiento es común:

1. Verifica acceso a la raíz con `get_file_metadata`. Si no tienes acceso, **pide permisos a Ariel Tarsitano por Slack** (`slack_search_users` por `ariel.tarsitano@procontacto.com.mx`, luego DM pidiendo acceso de editor con link + motivo). Avisa que el destino queda pendiente. Nunca inventes el acceso ni dejes placeholder de carpeta.
2. Navega la ruta nivel por nivel con `search_files`. Anota qué existe y qué falta.
3. Confirma con el usuario vía `_shared/assets/drive-folder-path.html` (rellena los slots). Opciones: **Crear y usar / Cambiar ubicación / No subir a Drive**.
4. Crea los niveles faltantes **sólo tras el OK**, de arriba hacia abajo (`create_file`, `mimeType: application/vnd.google-apps.folder`). Nunca crees sin confirmación.
5. Guarda el `webViewLink` final = `{{URL_CARPETA_DRIVE}}` para el prompt. Reutiliza esa carpeta al ofrecer guardar el `.md`.
6. Si el usuario elige "No subir a Drive", omití la sección "Destino en Drive" del prompt.
7. **Nunca** uses una carpeta de bases/plantillas como destino de entregables.

## Entrega del prompt (Paso 6, común)

- Muestra el prompt completo en chat dentro de un bloque de código (Patrón E) — **ese es siempre el canal principal de copy/paste y nunca se reemplaza por un archivo**.
- Acompañalo con una línea: *"Listo. Copia este prompt y pégalo en Claude Design — te va a generar el deck completo, personalizado. Si quieres ajustes finos sobre slides puntuales, volvemos acá."*
- **Paso 6.5 (opcional, sólo a pedido)**: ofrece guardar el prompt como `.md` en la carpeta de Drive ya resuelta (Patrón A). Nombre: `[YYYY-MM-DD]_prompt-deck_[CLIENTE_O_PROYECTO]_[TIPO].md`. Guarda vía `create_file` y confirma el `webViewLink`. Nunca lo guardes sin OK.

## Reglas inviolables (comunes a toda la familia)

- **Nunca dejes etiquetas "a completar" ni inventes datos** del cliente/proyecto/contacto (nombre, cargo, email, teléfono, industria, stakeholder, fechas, montos). Si falta un dato, páralo y valídalo vía widget. Si existe en una fuente (SF, web, conectores), tráelo y confírmalo; si no existe, pídeselo; nunca lo rellenes tú.
- **De una base de Drive, extrae sólo el contenido** (estructura narrativa, secciones, mensajes, bullets). Ignorá colores, tipografía, layouts e imágenes embebidas — la capa visual la reconstruye Claude Design según el manual de marca.
- **Drive es la fuente de verdad; el índice es sólo caché.** Reconcilia en runtime; si divergen, gana Drive y reescribes el índice. Nunca presentes una base que ya no está en Drive.
- **Nunca inventes casos de éxito o referencias.** Sólo los que el usuario pase o que vengan de `pc-crm-salesforce-success-case-generator`.
- **Transiciones a otros skills son invisibles.** Háblale al usuario en lenguaje de flujo ("armemos la oportunidad", "elijamos una base"), nunca de nombres técnicos de skills.
- **Todo prompt lleva la capa deck-craft y sigue el skeleton canónico.** Son fuentes únicas; no las dupliques ni dejes que diverjan.
