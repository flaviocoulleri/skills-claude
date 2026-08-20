<!-- ⚠️ AUTO-COPIADO desde _shared/presentation-builder/ por sync.sh — NO EDITAR ACÁ. Editá el canónico y volvé a correr sync.sh. -->

# Esqueleto canónico del prompt final

> **Fuente única de verdad del formato del prompt que genera este skill** (Paso 5 del SKILL.md).
> Cubre los tres sub-flujos: **Comercial a-medida**, **Comercial base-Drive** y **Delivery base-Drive**.
>
> **Reglas de oro al instanciarlo:**
> 1. Las `{{...}}` se reemplazan con datos reales capturados/barridos. **Nunca quedan en el output.**
> 2. **Si una sección no tiene datos reales, se OMITE entera — jamás se deja un placeholder.**
>    Las marcas `‹incluye sólo si …›` indican secciones condicionales: si la condición no se cumple, borra la sección completa.
>    Esto operacionaliza la regla anti-placeholder (Paso 4.7 + reglas inviolables del SKILL.md).
> 3. El bloque "Principios de diseño del deck" se pega **textual** desde `_shared/references/deck-craft.md` (sección "Bloque para el prompt").
> 4. La estructura de slides viene del template (`references/templates/<recordtype>.md`) en a-medida, o de la base de Drive elegida en base-Drive/delivery.

---

# Generar presentación para {{CLIENTE_O_PROYECTO}}

## ⚠️ Antes de generar — verificaciones obligatorias (de a una)

Antes de crear nada tienes **dos** verificaciones obligatorias con el usuario. **Pídelas una por una, en mensajes separados: haz UNA sola pregunta, espera la respuesta del usuario, y recién entonces pasa a la siguiente.** Nunca las juntes en un mismo mensaje. **No generes la presentación hasta tener las dos resueltas.**

- **Primero** pregunta y **espera la respuesta**: ¿"ProContacto Design System" es el **único** Design System seleccionado? Claude permite tener más de uno activo a la vez — no debe haber ningún otro. Si hay otros, pídele que deje sólo ese.
- **Recién cuando confirme**, pídele y **espera**: que copie la **URL del navegador** y te la pegue (no puedes leer tu propia URL). Formato obligatorio `https://claude.ai/design/p/{id}` (ej: `https://claude.ai/design/p/e2f17c2f-73ca-4915-9ddf-2446a1561715`); si falta o el formato no coincide, vuelve a pedírsela. Esa URL se incrusta como dato invisible en el HTML (ver Output esperado).

**Sugerencia (no bloquea):** para mejor resultado, recomiéndale usar el **modelo Sonnet**; si prefiere otro modelo, sigue igual.

Recién con las dos verificaciones obligatorias resueltas, genera la presentación.

## Contexto

- **Área**: {{Comercial | Delivery}}
- **Cliente**: {{CLIENTE}}
- **Industria**: {{INDUSTRIA}}  ‹incluye sólo si es comercial›
- **País**: {{PAIS}}  ‹incluye sólo si es comercial›
- **Proyecto**: {{PROYECTO}}  ‹incluye sólo si es delivery›
- **Stakeholder / Audiencia**: {{QUIÉN LO RECIBE}} ({{ROL}})
- **Brief / Hito**: {{BRIEF DEL CLIENTE — si comercial | HITO DEL PROYECTO — si delivery}}
- **Período cubierto**: {{PERÍODO}}  ‹incluye sólo si es delivery y el hito lo requiere (status/steering)›
- **Idioma del deck**: {{ES | EN}}

## Señales del sitio del cliente

‹incluye esta sección sólo si se proporcionó la web del cliente y el fetch del Paso 2.5 devolvió señales que el AE aprobó›

- {{SEÑAL}} — cómo se describe, a quién le vende, qué vende, casos que menciona, tono de marca.

## Señales relevantes (barrido de conectores)

‹incluye esta sección sólo si el barrido del Paso 3 devolvió señales que el usuario aprobó›

- {{SEÑAL}} ({{FUENTE — ej: transcript ReadAI 2026-05-03}})

## Personalización por industria — {{INDUSTRIA}}

‹incluye esta sección sólo si es comercial›

- **Vocabulario a usar**: {{VOCABULARIO}}
- **Vocabulario a evitar**: {{VOCABULARIO_EVITAR}}
- **Dolores típicos del sector que aplican acá**: {{DOLORES}}
- **KPIs que mira el stakeholder**: {{KPIS}}
- **Framing recomendado**: {{FRAMING}}

## Tipo de presentación

- **Comercial a-medida**: `{{RECORD_TYPE}}` — {{DESCRIPCIÓN}}
- **Comercial / Delivery base-Drive**: `Base de partida: {{NOMBRE_ARCHIVO_DRIVE}}`
- **Delivery**: `Hito del proyecto: {{HITO}}`

(Usa la línea que corresponda al sub-flujo; borra las otras dos.)

## Estructura obligatoria del deck

{{ESTRUCTURA_SLIDES}}

> **Divisores de sección (obligatorio).** Agrupa los slides en bloques del arco (contexto, problema, solución,
> inversión, cierre…) y **antes de cada bloque inserta un slide divisor de sección** (fondo azul full-bleed de la
> marca, número correlativo 01/02/03…, etiqueta + título de sección). No los omitas: le dan capítulos y ritmo al deck.
>
> - **A-medida**: lista exacta de slides del template `references/templates/{{RECORD_TYPE_SLUG}}.md`, con la
>   intención de cada slide (qué debe lograr, no sólo su título).
> - **Base-Drive**: estructura textual extraída del archivo de Drive elegido (títulos, secciones, mensajes),
>   **personalizada** a este cliente/proyecto — Claude Design reconstruye la capa visual desde cero según el manual de marca.
>   Mantén todas las secciones de la base salvo las claramente irrelevantes para este caso.

## Principios de diseño del deck (obligatorios)

{{BLOQUE_DECK_CRAFT}}

> Pega acá, textual, el "Bloque para el prompt" de `_shared/references/deck-craft.md`. Ajusta "cliente"/"proyecto" según el área.

## Reglas de marca

Aplica el manual de marca de ProContacto (colores institucionales, tipografía Open Sans, slogan y arquitectura
verbal). Si vas a materializar slides, usa la skill `pc-admin-interno-brand-applier` como referencia obligatoria.
Si es co-branding con Salesforce, aplica las reglas de co-branding.

## Idioma y dialecto

Escribe todo el deck en {{IDIOMA}}, **adaptado al dialecto del país del cliente ({{PAIS}})** — formas de tratamiento, vocabulario y expresiones locales, no un español neutro genérico. Guía:

- **Argentina / Uruguay / Paraguay** → voseo ("vos", "tenés", "podés").
- **México / Colombia / Perú / Chile / Centroamérica** → tuteo ("tú", "tienes") o "usted" según la formalidad del stakeholder; evitá el voseo.
- **España** → "tú"/"vosotros" y vocabulario ibérico (ej. "ordenador", no "computadora").

Ajusta los términos locales al país (celular/móvil, compañía/empresa, etc.). Si el deck es en inglés, usa inglés neutro de negocios.

## Inversión

‹incluye esta sección sólo si es comercial Y hay un número real de Salesforce. Si es delivery, o si el AE decidió
no incluir slide de inversión, BORRA esta sección entera — nunca dejes un placeholder›

- **Si hay Quote sincronizada**: inversión total **{{QUOTE_TOTAL}}** + breakdown por familia
  ({{FAMILIA}}: {{MONTO}}). Pie: "Cotización detallada — Quote {{QUOTE_NUMBER}}".
- **Si hay Orden de Magnitud en la Opp**: inversión estimada **{{OPP_AMOUNT}}** + breakdown por bloque
  ({{BLOQUE}}: {{MONTO}}). Leyenda obligatoria: "Orden de magnitud — sujeta a propuesta detallada".

Enmarca el número contra el costo de no actuar planteado antes en el deck — la inversión se lee mejor como retorno que como gasto.

### Ancla de precio y descuento por alcance total

‹incluye este sub-bloque sólo si es comercial Y el AE activó el ancla de descuento (Paso 4.6). Si no, BORRA este sub-bloque›

- Muestra el **precio de lista** {{PRECIO_LISTA}} y, debajo, el **precio con descuento** {{PRECIO_DESCUENTO}} destacado
  (el precio de lista tachado o atenuado; el precio final resaltado como el valor a pagar).
- **Condición del descuento (badge/pie visible):** "{{CONDICION_DESCUENTO}}" — por defecto:
  *"Precio promocional válido únicamente contratando la totalidad del alcance propuesto. La contratación parcial se cotiza al precio de lista."*
- El descuento es **{{MONTO_O_PORCENTAJE_DESCUENTO}}**. No lo presentes como regalo: es el incentivo por comprometerse con el alcance completo.

### Calendario de pagos

‹incluye este slide (JUSTO DESPUÉS del slide de inversión/precio final) sólo si es comercial Y el AE lo pidió (Paso 4.6). Si no, BORRA este bloque›

Agrega un slide de **calendario de pagos** posterior al precio final, con una tabla de hitos de pago **atados a la
finalización de sprints/entregables**. Cada fila: hito (ej: "Firma", "Fin Sprint 2", "Fin Sprint 4", "Go-live") ·
monto o % · fecha estimada. La suma de los pagos = el precio final (con descuento si aplica). Hitos capturados:

{{CALENDARIO_PAGOS}}

## Reglas inviolables (para ti, Claude Design)

- **Los números de inversión vienen de Salesforce.** No los inventes ni los cambies.
- **[Comercial] Sin spoilers de precio.** No adelantes cifras de inversión, precios, montos, rangos ni porcentajes de
  descuento en NINGÚN slide anterior al slide de inversión/precio final. El número aparece por primera vez recién ahí (y en
  su calendario de pagos, si lo hay). Antes de ese slide, habla de valor y de resultado, nunca de plata. **Única excepción:
  que el AE lo haya pedido expresamente** (ver el prompt: si no dice lo contrario, no hay spoilers).
- **No inventes casos de éxito ni referencias a clientes reales** — sólo los que figuran en "Señales relevantes".
- **Cero placeholders en el deck final** — ni de texto ni de imagen. Si un dato no está, la sección no existe (ya se
  resolvió antes de este prompt). Ninguna caja gris, "imagen aquí", `[ilustración]` ni marco vacío: las ilustraciones de
  los slides clave (portada, divisores de sección, visión, cierre) van **materializadas** (SVG/patrón de marca inline o
  imagen generada embebida como data URI).
- **Divisores de sección entre bloques.** Cada capítulo del deck abre con su slide divisor (azul full-bleed, numerado).
- **El cliente debe sentir que el deck fue hecho para él/ella**, no extraído de una plantilla. Su nombre va en los slides clave.
- **Tono profesional pero cercano** — ni corporate plano ni exceso de jerga.

## Output esperado

Genera el deck completo como artifact:

- Si se va a presentar en pantalla e iterar visualmente → **HTML interactivo** (deck navegable).
- Si se va a entregar como archivo al cliente → **PPTX**.
- Si dudas → genera HTML y ofrece pasarlo a PPTX al final.

El HTML debe ser **standalone**: un único archivo autocontenido con todo el CSS, el JS y las imágenes embebidos inline (data URIs), **sin dependencias externas ni archivos sueltos** — así se abre en cualquier navegador y se sube a Drive sin romperse.

**Título y nombre de archivo (nomenclatura obligatoria).** El título del deck (slide de portada) y el nombre del archivo deben seguir EXACTAMENTE: `ProContacto - {{CLIENTE}} - {{DESCRIPCION_PROPUESTA}} - {{VERSION}}` (ej: `ProContacto - BBVA México - Propuesta AgentForce - v1`). `{{VERSION}}` es la versión de la propuesta (v1, v2…); súbela en cada nueva iteración.

**Trazabilidad (dato invisible).** Incrusta en el HTML, como comentario al inicio (`<!-- ... -->`) o `<meta>` oculto, **la URL del proyecto de Claude Design que te pasó el usuario** en la verificación inicial. No debe verse al renderizar — sirve para volver a la fuente y seguir iterando.

Una sección/slide por cada ítem de "Estructura obligatoria", respetando el arco narrativo y los principios de diseño de arriba.

## Destino en Drive

‹incluye esta sección sólo si el AE confirmó una carpeta de Drive destino (Paso 4.8). Si eligió no subir a Drive, BORRA esta sección entera›

Cuando termines la presentación, **sube el HTML del deck a esta carpeta de Drive** usando tu conector de Google Drive:

- **Carpeta destino**: {{URL_CARPETA_DRIVE}}
- **Nombre del archivo**: `ProContacto - {{CLIENTE}} - {{DESCRIPCION_PROPUESTA}} - {{VERSION}}.html` (misma nomenclatura que el título del deck)

Confirma el link del archivo subido al terminar. **Y cada vez que el usuario te pida un cambio sobre el deck, vuelve a subir el HTML actualizado a esa misma carpeta** (mismo nombre, sobrescribiendo) y confirma el link — la carpeta siempre debe tener la última versión.
