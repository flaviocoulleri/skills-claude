# Preview artifact del documento completo (antes de escribir cualquier archivo)

Mostrar el logo y los hex sueltos con `Read` (como pide `brand-scraping.md`) confirma que los
*assets* están bien, pero no muestra cómo queda el documento compuesto — layout, jerarquía,
si el logo blanco se pierde contra el hero, si la foto de producto pesa mal, etc. Para eso,
antes de pedir confirmación al usuario, armá un preview HTML del `QuotePdfTemplate.page.tmpl`
ya resuelto y publicalo como Artifact. Validado con el cliente Telectrónica: el usuario pidió
explícitamente poder ver "el HTML final de la quote" en el chat antes de aprobar.

## Por qué un Artifact y no el widget de `visualize`

El preview tiene que verse **igual al PDF real** (misma tipografía Arial, mismos colores de
marca, mismo layout de tablas) — no una reinterpretación con el design system de Claude. El
tool `visualize` fuerza esa capa de diseño (CDS, Tabler icons, paleta propia); el Artifact no,
así que es el que corresponde acá. Cargá el skill `artifact-design` igual (es obligatorio
antes de todo Artifact), pero tratá este caso como "utilitario / fiel a lo real": el único
"design system" que aplica es el del propio template — no inventes paleta ni tipografía nueva
para el documento en sí.

## Receta

1. **Resolvé el template exactamente como en el paso 5** (mismo `QuotePdfTemplate.page.tmpl`,
   mismos placeholders), pero traducido a HTML de navegador en vez de Visualforce:
   - Sacá la regla `@page` (no aplica en browser).
   - Reemplazá `apex:image value="{!$Resource[...]}"` por `<img src="data:image/png;base64,...">`
     con las imágenes ya descargadas del paso de brand-scraping.
   - Reemplazá `apex:repeat`/`apex:outputField` por filas de tabla ya resueltas contra datos
     reales de la Quote de ejemplo (paso 1.5) — traé los line items reales por SOQL, no
     inventes montos.
2. **Envolvé la "hoja" en un canvas neutro**, no la pegues pelada en el artifact:
   - Un contenedor con fondo neutro (claro/oscuro según tema del viewer, con tokens CSS y
     soporte `data-theme`), ancho ~816px (proporción carta).
   - Una barra de estado chica arriba con el nombre del archivo que se va a generar
     (`QuotePdfTemplate{{SUFFIX}}.page`) y de qué Quote salen los datos.
   - Un callout corto que aclare qué datos son reales (logo, colores, contacto) y cuáles son
     de ejemplo (dirección, IBAN/cuenta/SWIFT si no hay datos públicos) — mismo criterio que
     el paso 5 de `SKILL.md` sobre no inventar datos de pago sin avisar.
   - La "hoja" en sí (fondo blanco, CSS del template) queda fija/clara siempre — un documento
     impreso no es theme-aware, así que no le apliques dark mode al contenido del PDF, sólo al
     canvas que lo rodea.
3. **Base64 de las imágenes**: no pegues el base64 a mano en la respuesta — escribí un HTML
   con placeholders (`{{LOGO_B64}}`, `{{PHOTO_B64}}`) y un script Python chico que los
   reemplace leyendo los archivos ya descargados, para no gastar contexto pegando strings
   larguísimos.
4. **Publicá con `Artifact`**: `file_path` al HTML final, `title` (dejalo también como
   `<title>` del HTML — el tag le gana al parámetro), `favicon` fijo para este tipo de preview
   (ej. 📄), `description` corta.
5. **En tu respuesta de texto**, siempre devolvé el link como markdown clickeable con esta
   forma exacta — es la que el usuario confirmó que le sirve para ver el preview clickeando
   desde el chat:

   ```
   Acá está la vista previa: [{{TITLE}}]({{ARTIFACT_URL}})
   ```

   No lo reemplaces por una descripción en prosa del artifact ni asumas que el link ya quedó
   visible por otro lado — siempre repetí el link en texto plano de la respuesta.

## Cuándo saltear este paso

Si el paso 2 de brand-scraping no encontró nada usable (sin logo, sin colores confiables) no
tiene sentido armar un preview compuesto — en ese caso escalá directamente al usuario como ya
indica `brand-scraping.md`, sin generar un Artifact vacío o con placeholders genéricos.
