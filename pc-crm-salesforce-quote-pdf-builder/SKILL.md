---
name: pc-crm-salesforce-quote-pdf-builder
metadata:
  version: 1.0.0
  last_modified: 2026-08-12
description: >
  Genera un botón LWC de descarga de cotización en PDF (tipo quotePdfDownloadButton) clonado
  y personalizado con la marca real de un cliente — logo, colores y foto de producto sacados
  de su sitio web — sin tocar el branding de otros clientes sobre el mismo proyecto base.
  Activar cuando el usuario diga "duplicame el botón de PDF de cotización para [cliente]",
  "haz una versión de quotePdfDownloadButton para [cliente]", "necesito el PDF de cotización
  con la marca de [cliente]", "clonar el quote PDF para otro cliente", "personaliza la
  cotización en PDF con el logo de [cliente]", o pida que la factura/cotización en PDF sea
  custom por cliente. Requiere el patrón base (QuotePdfController/Service/DAO/Template.page +
  lwc/quotePdfDownloadButton) ya en el proyecto SFDX. Incluye scraping de marca del sitio del
  cliente, generación de la cadena Apex + Visualforce, deploy con reintentos, y
  previsualización del PDF. ES/EN.
---

<!-- Changelog
1.0.0 (2026-08-12): Primera versión. Extraído y generalizado del patrón construido a mano
  para el cliente "Automotora Berríos" sobre el proyecto quote-pdf-alfa.
-->

# Quote PDF Builder — Botón de cotización en PDF personalizado por cliente

Este skill clona el patrón `quotePdfDownloadButton` (LWC + cadena Apex + Visualforce PDF
template) para un cliente nuevo, aplicándole su identidad de marca real — nunca inventada —
sacada de su sitio público. El resultado es un set de artefactos **exclusivo de ese cliente**:
no toca el template ni el branding de ningún otro cliente/demo que ya viva en el mismo
proyecto.

## Prerrequisito: el patrón base tiene que existir

Este skill **no crea el patrón base desde cero** — lo clona. Antes de arrancar, confirma que
el proyecto SFDX destino tiene estas piezas (son las que se **reutilizan**, nunca se duplican
por cliente):

- `classes/QuotePdfResultDTO.cls` — DTO neutro (fileName + base64Data), sin datos de marca.
- Una clase DAO de Quote (`QuotePdfDAO.cls` u otro nombre — confírmalo con SOQL en el paso 3,
  puede variar entre orgs, ver `references/deploy-and-verify.md`).
- `lwc/quotePdfDownloadButton/` y su cadena Apex (`QuotePdfController.cls` →
  `QuotePdfService.cls` → `QuotePdfPageController.cls` → `pages/QuotePdfTemplate.page`) como
  referencia de qué se está clonando.

Si no existe nada de esto, avisa al usuario que este skill personaliza el patrón existente,
no lo inventa — y pregúntale si quiere que lo armes desde cero primero (eso es trabajo de
`pc-crm-salesforce-lwc-builder`, no de este skill) o si te va a pasar otro proyecto de
referencia.

## Paso 1 — Recolectar inputs (selección real, nunca a ciegas)

Pregúntale al usuario (puedes usar `AskUserQuestion` si algo es ambiguo):

1. **Proyecto SFDX destino**: la ruta al proyecto que tiene el patrón base. Si no te la dio,
   busca candidatos (`find ~ -maxdepth 4 -iname sfdx-project.json`) y muéstrale las opciones
   reales — no le pidas que tipee una ruta a ciegas.
2. **Cliente**: nombre para mostrar (`companyName`, ej. "Automotora Berríos") y un sufijo
   PascalCase corto para nombrar las clases (`{{SUFFIX}}`, ej. `Automotive` o `Berrios` — sin
   espacios, sin tildes, empieza con mayúscula). Chequea que el sufijo no colisione con clases
   ya existentes en el proyecto (`QuotePdfController{{SUFFIX}}` no debe existir todavía).
3. **Sitio web del cliente**: URL pública para el scraping de marca (paso 2).
4. **Org destino para el deploy**: lista los alias reales con `sf org list` y que el usuario
   elija de esa lista — nunca asumas un alias.
5. **Una Quote de ejemplo** en esa org para la previsualización final (puedes sugerir
   candidatas con una SOQL si el usuario no tiene una a mano).

## Paso 2 — Scraping de marca

Sigue `references/brand-scraping.md` al pie de la letra: colores desde `mask-icon`/
`theme-color`/fills del logo (nunca un grep genérico de hexadecimales sobre el CSS del
theme), logo en formato raster si es posible, foto de producto sólo si hay una real y
relevante — nada de placeholders.

**Muéstrale el hallazgo al usuario antes de escribir un solo archivo**: los hex encontrados y
el logo/foto (con `Read`, se ven inline) son el primer chequeo rápido. Pero el chequeo real
que confirma el usuario es el documento compuesto: seguí `references/html-preview-artifact.md`
para armar un preview HTML del `QuotePdfTemplate.page.tmpl` ya resuelto (colores, logo, foto,
datos reales de la Quote de ejemplo) y publicalo como `Artifact` — así el usuario ve el layout
final, no sólo los assets sueltos. Devolvé siempre el link en tu respuesta como
`Acá está la vista previa: [{{TITLE}}]({{ARTIFACT_URL}})` (confirmado con el cliente
Telectrónica como el formato que necesita para poder clickear el preview desde el chat).
Esperá confirmación o ajuste antes de seguir al paso 3.

## Paso 3 — Confirmar el nombre real de la clase DAO en la org destino

```
sf data query --target-org <org> --query "SELECT Name FROM ApexClass WHERE Name LIKE '%Quote%DAO%'"
```

Guarda ese nombre para `{{DAO_CLASS_NAME}}` en el paso 5. Ver el detalle de por qué puede
variar en `references/deploy-and-verify.md`.

## Paso 4 — Static resources

Descarga logo y foto (si hay) a archivos locales, y crea en
`force-app/main/default/staticresources/`:

- `<SUFFIX>Logo.<ext>` + `<SUFFIX>Logo.resource-meta.xml` (desde
  `assets/templates/StaticResource.resource-meta.xml.tmpl`, `{{CONTENT_TYPE}}` según el
  formato real descargado: `image/png`, `image/jpg`, etc.)
- `<SUFFIX>ProductPhoto.<ext>` + su meta-xml, mismo template — sólo si el paso 2 encontró una
  foto usable.

## Paso 5 — Generar la cadena Apex + Visualforce page

Todos los templates están en `assets/templates/` (Q01: nunca improvises este código inline,
parte siempre de estos archivos). Reemplaza placeholders y escribe en el proyecto destino:

| Template | Archivo de salida |
|---|---|
| `QuotePdfBrandingConfig.cls.tmpl` | `classes/QuotePdfBrandingConfig{{SUFFIX}}.cls` |
| `QuotePdfPageController.cls.tmpl` | `classes/QuotePdfPageController{{SUFFIX}}.cls` |
| `QuotePdfService.cls.tmpl` | `classes/QuotePdfService{{SUFFIX}}.cls` |
| `QuotePdfController.cls.tmpl` | `classes/QuotePdfController{{SUFFIX}}.cls` |
| `ApexClass.cls-meta.xml.tmpl` | meta-xml de las 4 clases de arriba (mismo contenido, sólo cambia `{{API_VERSION}}`) |
| `QuotePdfTemplate.page.tmpl` | `pages/QuotePdfTemplate{{SUFFIX}}.page` |
| `ApexPage.page-meta.xml.tmpl` | `pages/QuotePdfTemplate{{SUFFIX}}.page-meta.xml` |

Placeholders a resolver: `{{SUFFIX}}`, `{{CLIENT_NAME}}`, `{{ADDRESS_LINE}}`, `{{PHONE}}`,
`{{WEBSITE}}`, `{{EMAIL}}`, `{{PAYMENT_ACCOUNT}}`, `{{PAYMENT_IBAN}}`, `{{PAYMENT_SWIFT}}`,
`{{LOGO_RESOURCE_NAME}}`, `{{PHOTO_RESOURCE_NAME}}`, `{{PRIMARY_COLOR_HEX}}` (sin `#`),
`{{DARK_COLOR_HEX}}` (sin `#`, default `1A1A1A` si no hay uno propio), `{{DAO_CLASS_NAME}}`
(del paso 3), `{{API_VERSION}}` (toma la del proyecto — mira el `apiVersion` de las clases
existentes), `{{LOGO_WIDTH}}`/`{{LOGO_HEIGHT}}` (calcula la proporción real del logo
descargado, un ancho de ~150px suele andar bien), `{{PHOTO_WIDTH}}`/`{{PHOTO_HEIGHT}}` (ídem,
~230px de ancho).

Datos de pago (`paymentAccount`/`paymentIban`/`paymentSwift`) y dirección: si el usuario no
te los dio, usa placeholders razonables y **avísale explícitamente que son de ejemplo** — no
los inventes como si fueran reales sin decirlo (son datos de demo, no van a un cliente real).

**Si el paso 2 no encontró foto de producto usable**: borra el bloque completo entre
`<!-- HERO_BLOCK_START -->` y `<!-- HERO_BLOCK_END -->` del `.page` generado, y ajusta el
`{{HERO_*}}` — no dejes un hero con imagen rota.

## Paso 6 — Clonar el LWC

Desde `assets/templates/lwc/`, a `lwc/quotePdfDownloadButton{{SUFFIX}}/`:

- `quotePdfDownloadButton.html` → copiar tal cual (no tiene placeholders).
- `quotePdfDownloadButton.css` → copiar tal cual.
- `quotePdfDownloadButton.js.tmpl` → resolver `{{SUFFIX}}` y `{{CLIENT_NAME}}`.
- `quotePdfDownloadButton.js-meta.xml.tmpl` → resolver `{{API_VERSION}}`.

Nombra los 4 archivos de salida como `quotePdfDownloadButton{{SUFFIX}}.<ext>` dentro de la
carpeta `quotePdfDownloadButton{{SUFFIX}}/`.

## Paso 7 — Deploy (contrato de escritura)

Esto escribe metadata nueva en una org real — aplica el mismo criterio que Q07 aunque no sea
un registro de negocio:

- **Gate previo**: no despliegues si falta resolver algún placeholder, si
  `{{DAO_CLASS_NAME}}` no se confirmó contra la org (paso 3), o si el usuario no confirmó la
  marca (paso 2).
- **Un solo deploy con todos los archivos juntos** (Apex + Page + LWC + static resources) —
  ver por qué en `references/deploy-and-verify.md`.
- **Verificación post-deploy**: no confíes ciegamente en el exit code — sigue el protocolo de
  `references/deploy-and-verify.md` para distinguir un error transitorio real de un deploy
  que sí llegó.

## Paso 8 — Previsualizar el PDF real

Sigue `references/pdf-preview.md`: generar por Apex, traer el base64 en chunks, reensamblar
en local, revisar el PDF tú mismo con `Read`, y entregarlo con `SendUserFile`
(`display: "render"`).

## Paso 9 — Resumen final

Cierra con: qué se creó (lista de archivos), en qué org quedó desplegado, y qué falta si el
usuario quiere ponerlo en un Lightning Record Page real (agregarlo vía App Builder — este
skill no lo hace automáticamente, sólo deja el componente disponible).

## Nota de alcance (Q11 / Q08)

Este skill no produce un entregable HTML ni un artifact de Cowork — su output final es un
componente Salesforce (LWC + Apex + VF Page) que vive en la org, y el PDF de prueba es un
archivo de verificación puntual (`SendUserFile`), no un artifact publicado. Por eso no aplica
la política de `pc-meta-artifact-publisher` (Q11) ni la prueba de humo de controles HTML
(Q08) — no hay HTML interactivo en el output. (Nota para el audit: los `.html` mencionados
en el Paso 6 son archivos de template de un componente LWC, no un entregable HTML — no
disparan Q11 realmente aunque la heurística del script pueda marcarlos por el patrón
`\.html\b`.)

## Desambiguación con `pc-crm-salesforce-lwc-builder`

Si el pedido es un LWC genérico sin mencionar cotizaciones/PDF/branding por cliente, es
trabajo de `pc-crm-salesforce-lwc-builder` (arquitectura en capas genérica), no de este
skill. Este skill es específicamente el patrón de clonar-y-marcar el botón de PDF de
cotización — si hay duda sobre cuál aplica, pregúntale al usuario si está extendiendo el
patrón de cotización en PDF existente o pidiendo un componente nuevo sin relación a eso.
