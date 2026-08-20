# Motor de deck HTML — cómo se materializa una presentación de ProContacto

> **Qué es esto.** El procedimiento canónico para **construir el deck acá mismo** y publicarlo en el
> gestor de artefactos de ProContacto. Es la ruta por defecto de toda la familia
> `presentation-builder`: el skill ya no termina en un prompt para otra herramienta, termina en
> **la presentación publicada, con su link**.
>
> Vive una sola vez en `_shared/presentation-builder/deck-engine/` y `sync.sh` lo copia dentro de
> cada skill como `_shared/deck-engine/`. **No lo edites en la copia de un skill.**

## Por qué el HTML es el original y no un formato más

El deck HTML no es "una opción de salida": es **la fuente de verdad de la que salen todas las
demás**. El PDF, los PNG/JPG y el PPTX se generan capturando los mismos slides ya renderizados,
así que ninguno puede "verse distinto" del deck — son el deck.

Eso da tres cosas que ningún flujo de "armá el .pptx" consigue:

1. **Un solo original.** Se corrige una vez, se re-exporta todo. No hay versiones que divergen.
2. **Fidelidad garantizada.** Nada se re-maqueta al exportar: lo que se ve es lo que sale.
3. **Cero instalaciones.** Un archivo autocontenido que abre en cualquier navegador, sin plugins,
   sin fuentes que falten, sin "se me corrió el cuadro de texto".

Por eso, cuando alguien pide "un PowerPoint", la respuesta correcta **no** es negarse ni saltar a
otra herramienta: es **hacer el deck acá y entregarle el .pptx exportado**. Recibe exactamente lo
que pidió, y además queda el original vivo para la próxima versión. Cómo se conversa esto está en
`../references/common-rules.md` → "Salida del skill".

---

## 1. Invariantes del motor (no negociables)

| # | Invariante | Por qué |
|---|---|---|
| 1 | **Escenario fijo 1920×1080.** Todos los slides se diagraman a esa medida y el escenario completo se escala con un único `transform`. | Es lo que hace que el deck se vea igual en cualquier pantalla **y** que el export sea fiel: cada slide es un cuadro fijo. |
| 2 | **Nunca re-maquetar por tamaño de pantalla.** Nada de unidades de viewport (`vw`/`vh`) ni breakpoints que reordenen el contenido del slide. | Un slide que se reacomoda en el celular ya no es el slide que se exporta. **Las unidades de contenedor (`cqw`) del kit sí valen**: el contenedor es el slide, fijo en 1920px, así que `1cqw = 19.2px` siempre. |
| 3 | **Un solo archivo autocontenido.** CSS, JS e imágenes embebidas (SVG inline o data URI). La **tipografía** es la excepción: va por `<link>` a Google Fonts, porque el gestor no tiene CSP. | Un entregable que depende de archivos sueltos se rompe al moverlo. La fuente por red se permite sólo porque el gestor la deja pasar y ahorra 110 KB; para la copia offline de Drive existe `assets/brand-font.css` con la fuente embebida. |
| 4 | **Cada slide es `<section class="slide">`.** | El shell, el índice y los tres exportadores encuentran los slides por esa clase. |
| 5 | **El contenido entra en el slide o se parte en dos.** Sin scroll, sin desbordes, sin paneles superpuestos. | En un escenario fijo no hay "más abajo": lo que no entra, se pierde. |
| 6 | **Marca ProContacto, siempre.** Tokens, tipografía y logos del Design System (`../assets/slides/_kit.css` y `logos/`). | No hay "elegí un estilo": el estilo es la marca. Ver §3. |

## 2. Anatomía del artefacto

Se arma con `assets/deck-shell-template.html`, que ya trae el escenario, la navegación, el índice y
las notas del orador. Nunca improvises el HTML del visor: tomá el shell y reemplazá sus cuatro
tokens.

| Token | Qué va |
|---|---|
| `__DECK_TITLE__` | Título del deck con la nomenclatura obligatoria: `ProContacto - {cliente} - {descripción} - {versión}`. Es también el nombre base de los archivos exportados. |
| `__DECK_TRACE__` | Comentario oculto de trazabilidad: cliente/proyecto, tipo de deck, versión, fecha, el id del registro de origen (Opportunity, Contract o `Project__c`) y **`gestor-id: {id}`** una vez publicado. Ese id es lo que permite que otra conversación publique una versión nueva en vez de duplicar el entregable — ver `_shared/artifact-publish/artifact-publish.md`. No se muestra nunca. |
| `__DECK_CSS__` | El CSS propio del deck: `../assets/slides/_kit.css` íntegro **una sola vez**, más las clases propias de los slides. El kit ya trae su `@import` de Open Sans, que en el gestor **sí carga** — dejalo. Sólo para la copia offline de Drive se reemplaza por `assets/brand-font.css` (fuente embebida) quitando el `@import` con `@import\s+url\([^)]*\)[^;]*;`. |
| `__SLIDES__` | La secuencia de `<section class="slide">…</section>`, en orden. |

> Cada token aparece **una sola vez** en el shell. Si automatizás el reemplazo, cuidado con
> reemplazar la primera coincidencia: por eso el comentario de cabecera del shell nombra los tokens
> sin guiones bajos.

### Lo que el shell ya resuelve (no lo reimplementes)

- Escalado del escenario, letterbox y `resize`.
- Navegación: flechas, Espacio, Re/Av Pág, Inicio/Fin, rueda, deslizar, clic a los costados.
- Contador, barra de progreso, pantalla completa.
- Índice con miniaturas en vivo (tecla `O`) y notas del orador (tecla `N`).
- Ayuda con los atajos (`?`).
- `window.PCDeck` — API para recorrer el deck por código; la usa el exportador headless.

> **El deck no exporta ni descarga nada.** Es un visor puro: navegación, índice y notas. La
> exportación se pide **en el chat**, con un widget, y pasa por el agente a propósito — así queda
> registrado qué archivo se generó y de qué versión salió. Ver `export-formats.md` y
> `../artifact-publish/artifact-publish.md`.

### Anatomía de un slide

```html
<section class="slide" data-notes="Lo que dice quien presenta. No se ve en el slide ni en los exports.">
  <div style="position:absolute;inset:0;background:var(--pc-gradient-radial)"></div>
  <div style="position:relative;padding:120px 140px;height:100%;
              display:flex;flex-direction:column;justify-content:center">
    <p  class="reveal" >…kicker…</p>
    <h1 class="reveal" >…headline que afirma…</h1>
    <ul class="reveal" >…</ul>
  </div>
</section>
```

- **`data-notes`** — notas del orador. Opcional, muy recomendado: es donde va el detalle que
  *no* debe estar en el slide (ver `../references/deck-craft.md` → "sin muros de texto").
- **`.reveal`** — entrada escalonada al activarse el slide. El exportador la congela antes de capturar.
- **Medidas fijas en px**, pensadas sobre 1920×1080, o `cqw` del kit. Nada de `vw`/`vh` dentro del slide.

## 3. La capa visual: el Design System, no un catálogo de estilos

Acá **no se elige estilo ni se ofrecen previews de aspecto**. Un deck de ProContacto se ve como
ProContacto: canvas oscuro `#0B0C0E`, azul `#0062FF`, violeta `#8F7AFF`, Open Sans con el contraste
ExtraBold(800)/Light(300). Lo que sí se decide es la **densidad** (§4) y, sobre todo, el
**contenido y el arco narrativo**, que es donde se gana o se pierde el deck.

- **Componentes estandarizados primero.** Antes de componer un slide a mano, mirá
  `../assets/slides/INVENTORY.md`: si el slide ya está estandarizado (portada, divisor de sección,
  cierre), **cloná el markup del kit y rellená los slots** — no cambies layout, colores, tipografía
  ni logos. Si no está, componelo con las clases y tokens de `_kit.css`.
- **Logos siempre inline** desde `../assets/slides/logos/`. Nunca `<img src>` a un archivo suelto
  ni recreados con texto o CSS.
- **La tipografía va por red en el gestor y embebida sólo offline.** El gestor **no tiene CSP**, así
  que el `@import` de Open Sans del kit carga sin problema y el entregable pesa 110 KB menos. Para la
  copia de Drive —que puede abrirse sin internet— existe `assets/brand-font.css` con Open Sans en
  cuatro instancias estáticas (300/400/700/800, subconjunto latino) como data URI; se regenera con
  `scripts/build-brand-font.sh` si cambia la fuente del DS.
  > Se probó con la variable (un archivo, más chico) y **no sirve**: el eje `wght` sobrevive al
  > subset pero el navegador no lo aplica, y se pierde el contraste ExtraBold/Light que es la firma
  > de la marca. Cuatro estáticas pesan menos y no dependen de que el eje funcione.
- **El kit adentro del escenario fijo.** Cada `<section class="slide">` envuelve un `.pc-slide`; hay
  que neutralizarle el chrome de tarjeta, que existe para el modo galería:
  `.slide > .pc-slide{width:1920px;height:1080px;border-radius:0;box-shadow:none}`.
- **Ilustraciones materializadas, nunca placeholders.** Portada, divisores, el slide de la visión y
  el cierre llevan una composición gráfica real (SVG de marca inline, patrón, imagen embebida como
  data URI). La prohibición de cajas grises y `[ilustración]` está en `../references/deck-craft.md`
  y aplica igual acá.
- **Fuente por red = no carga.** El `@import` de Open Sans queda en el CSS por si el `.html` se abre
  fuera de Cowork, pero dentro del artefacto la CSP lo bloquea y cae al Open Sans del sistema. Es
  esperado. No intentes esquivarlo con otro CDN: no hay CDN que funcione.

## 4. Densidad: deck para hablar vs deck para leer

Preguntalo una vez y diseñá todo el deck en consecuencia. Es la única decisión de forma que cambia
de verdad el resultado.

| Modo | Cuándo | Cómo se diseña |
|---|---|---|
| **Para hablar** (baja densidad) | Se presenta en vivo: pitch, kickoff, steering, comité. | Una idea por slide, tipografía grande, mucho aire, 1-3 bullets. Más slides si hace falta. |
| **Para leer** (alta densidad) | Circula sin nadie que lo explique: propuesta que se reenvía, informe, leave-behind. | Slides autocontenidos, tablas y grillas comparativas, 4-6 bullets o tarjetas, texto explicativo breve pero suficiente. |

Ante la duda: si lo va a presentar una persona, **para hablar**; si se manda por mail, **para leer**.
Ningún modo habilita amontonar: si un slide denso desborda, se parte en dos.

## 5. Procedimiento

0-bis. **Confirmá la carpeta de Drive antes de construir** (`subir-a-drive.html`) — ver
   `../drive-upload/drive-upload.md`. Se pregunta una sola vez; después cada versión sube sola.
1. **Resolvé el contenido.** Estructura del deck (template de Record Type o base de Drive),
   arco narrativo e intención por slide, según `../references/deck-craft.md`. El gate
   anti-placeholder de `../references/common-rules.md` ya corrió: no debería faltar ningún dato.
2. **Elegí densidad** (§4) y contá los slides.
3. **Componé los slides**: kit estandarizado donde exista, tokens del DS donde no.
4. **Ensamblá el artefacto**: shell + los cuatro tokens.
5. **Verificá antes de publicar** (§6).
6. **Publicá en el gestor** (`publicar_artefacto`) envolviendo el shell en un documento completo, y
   **mostrá el link en el chat** — ver `../artifact-publish/artifact-publish.md`. No se publica como
   artefacto de la conversación: el gestor es el único destino del entregable.
7. **Ofrecé corregir o descargar** con `../assets/exportar-deck.html` (`show_widget`).
8. **Con el formato elegido**, generá el archivo con `scripts/export-deck.mjs` — ver
   `export-formats.md` — y entregalo en el chat. A Drive no sube: el original ya está.
9. **Corré el gate de vinculación** (`../artifact-linkage/artifact-linkage.md`): el **link de Drive**
   queda enganchado como `Project_Asset__c` de la Opportunity (comercial) o como issue `Artifact`
   del proyecto Jira (delivery). El gate busca el padre y, en comercial, ofrece crearlo.

**Cada edición repite el 6**: nueva versión del artefacto, nueva versión a Drive, aviso con el link.
Sin volver a preguntar la carpeta.

## 6. Verificación antes de publicar (bloqueante)

El escenario fijo perdona poco: un slide que desborda no se ve "apretado", se ve **cortado**. Antes
de dar el deck por bueno, verificá **en el render**, no leyendo el código:

- [ ] **Los tokens del Design System resuelven.** No alcanza con que "se vea un deck": comprobá en el
      render que `--w-extrabold` vale `800`, que el kicker sale azul (`#66ACFF`) y que el título pesa
      800 contra un subtítulo de 300. Si un token cae, el deck sigue renderizando pero **pierde la
      marca** — y eso se nota tarde. (Ver la trampa del `@import` más abajo.)
- [ ] Cada slide entra completo en 1920×1080: **ningún** desborde, scroll ni panel superpuesto.
- [ ] La navegación recorre todos los slides y el contador cierra en el total correcto.
- [ ] El índice (`O`) muestra una miniatura por slide y todas se ven bien.
- [ ] Cero errores en consola.
- [ ] Cero placeholders de texto **y de imagen** (`[A completar]`, cajas grises, marcos vacíos).
- [ ] Ningún recurso por red: sin `<img src="http…">`, sin `<script src>`, sin hojas externas.
- [ ] El título sigue la nomenclatura `ProContacto - {cliente} - {descripción} - {versión}`.
- [ ] La navegación, el índice y las notas responden (probalos, no los des por buenos).

Si algo falla, **arreglalo y volvé a verificar** — no lo publiques avisando que "puede tener un
detalle".

### La trampa del `@import` (pasó de verdad)

El `@import` del kit apunta a Google Fonts y **contiene punto y coma adentro del `url()`**:

```
@import url('…family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap');
```

Al sacarlo con un `@import[^;]+;` el corte cae en ese punto y coma interno y queda un resto de
línea suelto (`1,300..800&display=swap');`) que invalida la regla siguiente: **se pierde el bloque
`:root` entero y con él todos los tokens de marca**. El deck sigue viéndose "bien" a primera vista,
pero sin ExtraBold, sin azul de marca y con todo en 400.

Usá siempre un patrón que respete los paréntesis:

```
css.replace(/@import\s+url\([^)]*\)[^;]*;/g, '')
```

## 7. Modificar un deck existente

Cuando el pedido es cambiar un deck ya hecho, el riesgo número uno es romper el encaje:

1. **Antes de agregar**, contá lo que ya hay en ese slide contra los límites de densidad (§4).
2. **Si no entra, partí el slide en dos.** Proactivamente, sin esperar que te lo pidan — y decilo.
3. **Después de cada cambio, volvé a correr la verificación de §6** sobre los slides tocados.
4. **Subí la versión** en el título y en la trazabilidad. La versión sube en cada iteración.
5. **Volvé a correr el gate de Drive.** Una versión nueva que no se sube deja circulando la vieja:
   es el modo más común de que el equipo trabaje sobre el archivo equivocado.
