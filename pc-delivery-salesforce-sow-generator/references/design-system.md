# Design System ProContacto aplicado al SOW (.docx)

Fuente: ProContacto Design System (Manual de Marca 2026). Esta referencia adapta los tokens de marca al medio Word. Regla general acordada: **portada de marca oscura + interior sobrio e imprimible**. Aplícala SIEMPRE al generar el documento en Fase 4.

## Paleta (valores hex para Word)

| Token | Hex | Uso en el SOW |
|---|---|---|
| Azul primario | `#0062FF` | Títulos H1, encabezados de tabla, acentos, links |
| Azul profundo | `#004BDB` | Títulos H2 |
| Azul oscuro | `#0032A3` | Títulos H3 / H4 |
| Violeta secundario | `#8F7AFF` | Solo como acento del gradiente en portada; nunca solo, nunca en texto |
| Canvas oscuro | `#0B0C0E` | Fondo de portada únicamente |
| Texto cuerpo | `#1F1F1F` | Texto normal sobre blanco |
| Gris tabla | `#F2F2F2` | Filas alternadas de tablas |
| Gris borde | `#D9D9D9` | Bordes de tabla |
| Éxito | `#009060` | Estado "Aprobado" en tablas de control |
| Advertencia | `#DF4D03` | Estado "En revisión" (Fuera de Alcance) |
| Error | `#D21E41` | Estado "Rechazado / No incluido" |

Proporción de color del manual: el azul es protagonista, el violeta es acento (~5%). En el interior del documento el color aparece solo en títulos, tablas y estados — el cuerpo es blanco y negro.

## Tipografía

Única familia: **Open Sans** (no sustituir por Calibri, Arial, Inter ni Roboto). Si Open Sans ExtraBold está disponible como familia separada ("Open Sans ExtraBold"), usarla para títulos; si no, Open Sans en bold.

| Elemento Word | Fuente | Tamaño | Color |
|---|---|---|---|
| Título portada | Open Sans ExtraBold | 32–40 pt | Blanco |
| Subtítulo portada | Open Sans Light | 16–18 pt | Blanco 72% (`#B8B9BC`) |
| Heading 1 | Open Sans ExtraBold/Bold | 18 pt | `#0062FF` |
| Heading 2 | Open Sans Bold | 14 pt | `#004BDB` |
| Heading 3 / 4 | Open Sans Bold | 12 / 11 pt | `#0032A3` |
| Cuerpo | Open Sans Regular | 10.5–11 pt | `#1F1F1F` |
| Destacado | Open Sans Bold | igual al cuerpo | `#1F1F1F` |
| Pie de página | Open Sans Regular | 9 pt | `#737373` |

El contraste Light/ExtraBold es la firma visual de la marca: úsalo en la portada (título ExtraBold + subtítulo Light grande).

## Portada (única página oscura)

1. Fondo de página completa `#0B0C0E`. Método preferido: generar la portada como imagen PNG a página completa (con PIL o similar): canvas `#0B0C0E` + glow radial azul→violeta suave desde el borde inferior (azul `#0062FF` ~55% opacidad → violeta `#8F7AFF` ~25% → transparente) e insertarla a sangre completa. Fallback: tabla de una celda a página completa con sombreado `#0B0C0E` (sin glow).
2. Logo: `assets/logo/logo_anclaje_white.png` (logo blanco con el anclaje "Soluciones tecnológicas integrales" debajo — NO separar ni recomponer el lockup), centrado o alineado a la izquierda en el tercio superior, ancho ≈ 45–55% de la página.
3. Título: "Statement of Work Comercial" (ExtraBold, blanco) + nombre del cliente (Light, grande). 
4. Cierre inferior de la portada: slogan **"Aliados en tu transformación."** en Open Sans Light, blanco 72%. El slogan SIEMPRE cierra, nunca abre — solo en la portada (abajo) o contraportada, nunca como encabezado de sección.
5. Prohibido en portada: co-branding Salesforce (reservado a materiales conjuntos con Salesforce; no aplica al SOW por decisión de marca), gradiente sobre el logo o el texto, sombras en texto, emoji.

Notas de implementación (validadas en prueba con docx-js):
- El fondo se inserta como `ImageRun` flotante con `behindDocument: true` anclado a la página (offset 0,0); el logo y los textos van como párrafos normales encima.
- El slogan NO puede ir en el footer de la sección de portada: la capa de header/footer se dibuja detrás del cuerpo y la imagen de fondo la tapa. Usar un párrafo con `frame: { type: 'absolute', anchor: página, y ≈ 14300 DXA }` para anclarlo al pie.
- El índice se genera con `TableOfContents` + `features: { updateFields: true }` para que Word lo complete al abrir el documento (en el visor previo puede verse vacío).
- "Open Sans Light" debe existir como familia estática en el sistema que renderiza; si solo hay fuente variable, instanciar el peso 300 con fonttools o el Light caerá en una serif de fallback.
- Tamaños validados: título portada 36 pt ExtraBold, subtítulo 18 pt Light, cliente 24 pt Light, slogan 13 pt Light `#B8B9BC`.

## Página 2 — Ficha del documento (oscura)

Segunda página oscura estilo modelo Claude Design (misma técnica de fondo que la portada, PNG `#0B0C0E` con marca de agua del isotipo al ~5% de opacidad, centrado, grande):

- Overline "INFORMACIÓN DEL DOCUMENTO" en azul `#3F90FF`, mayúsculas, 7.5 pt, letter-spacing amplio.
- Título "Statement of Work Comercial" blanco 24 pt.
- Tabla de definición (sin ficha aparte en el cuerpo): filas Nombre del sistema / Tipo de documento ("Statement of Work Comercial") / Versión / Cliente / Elaborado por. Etiqueta gris `#8C8C8C` 9 pt a la izquierda, valor blanco 11 pt alineado a la derecha, separadores horizontales `#33353A`, sin bordes verticales.
- Logo primario blanco pequeño (~180 px) abajo a la izquierda. NO usar el lockup de co-branding: el SVG disponible tiene el badge de Salesforce como placeholder vacío.

## Interior (blanco, estilo modelo Claude Design)

- **Títulos de sección numerados** (1 Introducción, 2 Glosario, 3 [Nube] — Alcance de Implementación, … 8 Aprobaciones): banda negra `#0B0C0E` de ancho completo (párrafo con sombreado + bordes del mismo color con `space` para simular padding), número en azul `#3F90FF` bold + título en blanco bold, 13 pt. Insertar un `Bookmark` en cada banda para el índice.
- **Títulos sin número** (Control de versiones, Índice): texto oscuro 15 pt con regla inferior negra gruesa (border bottom size 16).
- **Épicas (H2)**: "3.1. Gestión de X" en negro `#111111` bold 12 pt, sin color azul.
- **Dominios de consideraciones (H3)**: "3.3.1. ROLES Y PERFILES" en mayúsculas, 10 pt, texto oscuro; contenido en bullets `•` con sub-ítems a. b. c.
- **Índice**: lista manual (no campo TOC): número azul `#0062FF` + título + tab con leader de puntos + `SimpleField('PAGEREF <bookmark> \\h')`; con `features: { updateFields: true }` Word actualiza los números al abrir.
- **Historias de usuario**: cada una en una TARJETA — tabla de 1 celda, fondo `#FAFBFC`, borde 0.5 pt `#E4E6EB`, márgenes internos generosos, `cantSplit: true` en la fila para que nunca se parta entre páginas. Contenido:
  - Título "3.1.1. Nombre" oscuro 11 pt.
  - Overline "TIPO DE FUNCIONALIDAD" (7.5 pt, gris `#8C8C8C`, mayúsculas, letter-spacing) + chip: run con sombreado `#DBEAFE` y texto azul `#004BDB` 8 pt (p.ej. "Estándar", "Personalizada (Flow)").
  - Overline "NARRATIVA" + narrativa con las palabras Como / quiero / para en azul `#0062FF`.
  - Overline "CRITERIOS DE ACEPTACIÓN" + lista a. b. c. (numbering LOWER_LETTER con `instance` único por tarjeta para reiniciar la letra).
  - En Fuera de Alcance la tarjeta agrega: overline "OBSERVACIONES" + texto, y overline "ESTADO FINAL" + chip "En revisión".
- **Tablas de datos** (glosario, control de versiones, sprints, aprobaciones): fila de encabezado NEGRA (`#000000`) con texto blanco 8.5 pt; filas alternadas blanco / `#F5F6F8`; solo separadores horizontales finos `#E8E8EC`, SIN bordes verticales ni laterales.
- **Callouts** (notas de alcance, dependencias críticas): tabla de 1 celda con fondo `#EAF2FF`, borde `#C7DBFF`, texto azul `#004BDB` con destacados en bold. Usar al cierre de la introducción (alcance de la fase) y en cronología (dependencias).
- **Estados**: como chips (En revisión con fondo `#DBEAFE`), no como texto de color suelto.
- Pie de página en todas las páginas interiores: `Statement of Work Comercial (SOW) — [Cliente]` a la izquierda y número de página a la derecha, 8 pt gris `#9CA0A6`.
- Numeración de secciones: TODAS las secciones principales van numeradas (1..N) incluyendo Entregables, Cronología, Controles de Cambio, Fuera de Alcance y Aprobaciones; épicas 3.1, historias 3.1.1; los sub-ítems de historia ya no llevan numeración 3.1.1.2.1 — la estructura interna de la tarjeta la reemplaza.

## Capa verbal (obligatoria)

- La marca se escribe **ProContacto** — una palabra, dos mayúsculas. Nunca "Pro Contacto" ni "PROCONTACTO".
- Anclaje: "Soluciones tecnológicas integrales" — solo bajo el logo. No mezclarlo con el slogan.
- Slogan: "Aliados en tu transformación." — solo como remate (portada abajo / contraportada).
- Registro: español LATAM profesional B2B, directo, verbos en primera persona plural ("Diseñamos…", "Implementaremos…"). Sin emoji, sin signos de exclamación.
- Ortografía española impecable: tildes, ñ, signos de apertura ¿¡ — UTF-8 innegociable.

## Activos incluidos en la skill

| Archivo | Uso |
|---|---|
| `assets/logo/logo_anclaje_white.png` | Portada oscura (preferido) |
| `assets/logo/logo_anclaje.svg` | Fuente vectorial del anterior |
| `assets/logo/logo_primario_white.png` / `.svg` | Alternativa sin anclaje sobre fondo oscuro |
| `assets/logo/logo_primario_black.svg` | Variante para fondos claros si se pide interior con logo |
| `assets/logo/isotipo_blue.svg` | Encabezado interior / detalles |
| `assets/logo/isotipo_white.png` | Detalles sobre portada oscura |

Prohibiciones sobre el logo: no estirar, no recolorear, no rotar, no agregar sombras o contornos, no recortar, no escalar partes por separado.

## Checklist de verificación de marca (sumar a Fase 5)

- Portada: fondo `#0B0C0E`, logo blanco con anclaje, título ExtraBold, slogan al pie.
- Página 2: ficha oscura con marca de agua del isotipo, tabla de definición y logo blanco.
- Secciones numeradas con banda negra (número azul + título blanco) y bookmark para el índice.
- Cada historia en su tarjeta con chips, overlines y Como/quiero/para en azul; tarjetas que no se parten entre páginas.
- Tablas de datos con encabezado negro y zebra `#F5F6F8`, sin bordes verticales.
- Interior 100% Open Sans; cuerpo `#1F1F1F` sobre blanco.
- Pie de página `Statement of Work Comercial (SOW) — [Cliente]` + número de página.
- "ProContacto" bien escrito en todo el documento; slogan solo como cierre; sin co-branding Salesforce; sin emoji.
