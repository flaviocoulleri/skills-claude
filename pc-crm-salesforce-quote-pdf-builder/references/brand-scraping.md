# Sacar la identidad de marca real del sitio del cliente

Nunca inventes colores, ni uses un logo o foto de stock genérico. El cliente tiene un sitio
público — de ahí sale todo. Esta es la secuencia que funcionó de punta a punta (validada con
`berrios.cl`).

## 1. Descargar el home

```bash
curl -s -A "Mozilla/5.0" "https://<dominio-cliente>/" -o /tmp/brand-home.html --max-time 20
```

El User-Agent evita que algunos sitios (Jumpseller, Shopify, WooCommerce) devuelvan una
versión reducida a bots.

## 2. Color primario — tres fuentes, en este orden de confiabilidad

1. **`<link rel="mask-icon" ... color="#XXXXXX">`** (Safari pinned-tab): casi siempre es
   exactamente el color de marca que el sitio declaró a propósito. Es la señal más confiable.
   ```bash
   grep -oiE '<link[^>]*mask-icon[^>]*color="#[0-9a-fA-F]{3,6}"' /tmp/brand-home.html
   ```
2. **`<meta name="theme-color" content="#XXXXXX">`**: color de la barra del navegador en
   mobile. Buena señal secundaria.
3. **Fills del SVG del logo** (ver paso 3): si el logo es un SVG, sus atributos `fill="#..."`
   son literalmente los colores de marca usados en el arte final.

Si las tres fuentes coinciden (o son consistentes), tenés tu `primaryColor`. Si divergen,
priorizá el `mask-icon` y el fill del logo por sobre el `theme-color` (este último a veces es
solo blanco/negro genérico, no el color de marca real).

No uses `grep` genérico de hexadecimales sobre toda la página o el CSS del theme — la mayoría
son colores de estados/utilidades del framework (`#f2545b` de error, `#53af41` de success,
etc.), no la marca. Andá directo a las tres fuentes de arriba.

## 3. Logo — encontrar el archivo real, evitar SVG cuando se puede

```bash
grep -oiE '<img[^>]*logo[^>]*>' /tmp/brand-home.html
```

Preferencia de formato, en este orden:
1. **JPG/PNG** con fondo blanco o transparente — es lo que mejor renderiza Visualforce
   `renderAs="pdf"`. El motor de PDF de Salesforce (no es un navegador real) tiene soporte
   inconsistente para SVG dentro de `<apex:image>`.
2. Si sólo hay SVG, buscá una variante raster. Muchos sitios e-commerce (Jumpseller, Shopify)
   guardan una copia JPG/PNG del logo en otra ruta (`/store/logo/`, `/assets/logo.png`) aunque
   el header use el SVG. Grepeá variantes:
   ```bash
   grep -oiE 'https://[^"'"'"']*[Ll]ogo[^"'"'"']*\.(png|jpg|jpeg|webp)[^"'"'"']*' /tmp/brand-home.html
   ```
3. Si de verdad sólo existe SVG, usalo — pero avisá al usuario que puede no renderizar
   perfecto en el PDF y ofrecé revisar el resultado.

Descargá y **mirá el logo con la herramienta Read antes de usarlo** — confirmá que tiene
buena resolución y que el fondo no choca con el `.hero` (fondo `#f7f7f7` del template).

```bash
curl -sL -A "Mozilla/5.0" "<url-logo>" -o /tmp/brand-logo.<ext> --max-time 20
```

## 4. Foto de producto (opcional, sólo si aporta)

El hero con foto de producto es la parte que le da "más power" al PDF (pedido típico del
usuario), pero **sólo tiene sentido si hay una foto real y relevante** — nunca generes ni
uses un placeholder genérico.

Estrategia, en orden:

1. Si la Quote tiene línea de producto con nombre reconocible (ej. "Toyota Yaris"), buscá esa
   ficha específica en el sitio del cliente:
   ```bash
   curl -s -A "Mozilla/5.0" "https://<dominio>/sitemap.xml" --max-time 15 \
     | grep -io '<loc>[^<]*<slug-del-producto>[^<]*</loc>'
   ```
   Si el sitemap no tiene el slug exacto, probá el buscador del sitio (`/search?q=...`) o
   revisá las categorías del menú.
2. Si no hay match exacto, usá una foto de un producto de la misma familia/marca que sí
   exista en el sitio (ej. Quote dice "Toyota Yaris" pero sólo hay foto de un Toyota RAV4) —
   es mejor que nada, pero **avisá explícitamente al usuario que es un producto similar, no
   el exacto**, y ofrecé cambiarla apenas tengas la real (así surgió el ajuste real de esta
   skill: primero se usó un RAV4 de relleno, después el usuario pidió el Yaris puntual).
3. Si no hay ninguna foto de producto usable, **no inventes un hero** — dejá el bloque
   `HERO_BLOCK_START...HERO_BLOCK_END` del template afuera del archivo final. Un PDF sin hero
   es mejor que uno con una imagen que no corresponde.

Extraé la URL de la imagen igual que el logo (buscá `.jpg|.jpeg|.png|.webp` cerca del nombre
del producto en la página de ficha, no en el home).

## 5. Antes de escribir cualquier archivo: mostrale el hallazgo al usuario

Con logo + foto descargados, usá la herramienta `Read` para mostrárselos (son imágenes, se
ven inline) junto con los hex encontrados, y pedí confirmación antes de generar los static
resources y el código. Esto evita tener que rehacer un deploy completo si el usuario no está
de acuerdo con lo que se encontró (ej. "esa no es la ubicación real" o "usá este otro logo").
