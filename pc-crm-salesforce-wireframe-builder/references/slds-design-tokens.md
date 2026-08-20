# SLDS Design Tokens — fuente de fidelidad de color, tipografía y spacing

Tokens oficiales del **Salesforce Lightning Design System** (`github.com/salesforce-ux/design-system`). Son la fuente de verdad de los valores exactos que hacen que un wireframe se vea como Salesforce real y no como un CRM genérico.

> **Cómo se usan.**
> - **Output Claude Design (default):** el design system del proyecto manda. Estos tokens van *embebidos en el prompt* (sección "Design tokens SLDS" de `wireframe-prompt-template.md`) como refuerzo, para que no invente colores ni spacing.
> - **Fallback HTML (Paso 5):** define estos valores como CSS custom properties (`:root { --slds-... }`) y referencialos en cada componente. No hardcodees hex sueltos: usa las variables.

---

## Mapeo token → componente Lightning (lo importante para fidelidad)

| Elemento de la UI | Token / valor |
|---|---|
| **Fondo de página** (desktop) | warmGray-3 `#f3f2f2` |
| **Global header / barra superior** (desktop y mobile) | white `#FFFFFF` con borde inferior `#dddbda` — **nunca navy/azul oscuro**; logo = nube Salesforce cloudBlue `#00a1e0` |
| Fondo de cards / header / secciones | white `#FFFFFF` |
| Bordes de cards, tablas, inputs | warmGray-5 `#dddbda` (border thin `1px`) |
| **Azul de marca / acciones primarias** | brand primaryActive `#0176d3` (hover/active `#014486`) |
| Azul de acento (tab activa, focus) | brand primary `#1b96ff`; focus ring `0 0 2px #0176d3` |
| **Links** | textLink `#0b5cab` (active `#014486`) |
| Texto principal | warmGray-12 `#2B2826` / neutral-10 `#181818` |
| Texto secundario / labels | warmGray-9 `#706e6b` |
| Texto deshabilitado / placeholder | warmGray-7 `#b0adab` |
| **Estado success** (toast guardado, Path completado) | green-50 `#2e844a` (bg suave green-95 `#ebf7e6`) |
| **Estado warning** | orange-60 `#dd7a01` (bg orange-95 `#fff1ea`) |
| **Estado error / required asterisk / destructive** | red-50 `#ea001e` (bg red-95 `#fef1ee`) |
| **Estado info** | blue-50 `#0176d3` (bg blue-95 `#eef4ff`) |
| Path: etapa actual | brand primaryActive `#0176d3` (chevron relleno) |
| Path: etapas completadas | green-50 `#2e844a` |
| Path: etapas pendientes | warmGray-4 `#ecebea` (texto warmGray-9) |
| Badges / pills neutros | bg warmGray-3 `#f3f2f2`, texto warmGray-11 `#3e3e3c`, radio pill |
| Highlights panel / record header | fondo white, ícono de objeto con su color Lightning |
| Hover de fila en tablas / list views | warmGray-2 `#fafaf9` |

> **Íconos de objeto Lightning:** cada objeto estándar tiene su color de fondo de ícono (Account turquesa, Contact azul, Opportunity amarillo/dorado, Lead naranja, Case rojo-naranja, etc.). Usa el ícono y color del design system del proyecto; nunca emojis.

---

## Tipografía

- **Familia base y headings:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif` (Salesforce Sans / system stack). Monospace: `Consolas, Menlo, Monaco, Courier, monospace`.
- **Escala (rem):** 1=`0.625` · 2=`0.75` · 3=`0.8125` · 4=`0.875` · 5=`1` · 6=`1.125` · 7=`1.25` · 8=`1.5` · 9=`1.75` · 10=`2` · 11=`2.625`.
  - Label de campo / metadatos: 2–3 (`0.75`–`0.8125rem`). Body / valor de campo: 4 (`0.875rem`). Título de sección: 5–6. Nombre de registro en el header: 8–9 (`1.5`–`1.75rem`).
- **Pesos:** light `300` · regular `400` · bold `700`. Labels y nombre de registro en bold.
- **Line-height:** heading `1.25` · text `1.5` · reset `1`.

---

## Spacing (rem)

`none 0` · `xxxSmall 0.125` · `xxSmall 0.25` · `xSmall 0.5` · `small 0.75` · `medium 1` · `large 1.5` · `xLarge 2` · `xxLarge 3`.

Padding típico de card/sección: `medium` (1rem) a `large` (1.5rem). Gap entre campos: `small`. Padding de celda de tabla: `xSmall`–`small`.

---

## Border radius / width / shadow

- **Radius:** small `0.125rem` · medium `0.25rem` (cards, inputs, botones) · large `0.5rem` · circle `50%` (avatares) · pill `15rem` (badges/toggles).
- **Border width:** thin `1px` · thick `2px`.
- **Box shadow:** focus/active `0 0 2px #0176d3` · dropdown/menú `0 2px 3px 0 rgba(0,0,0,0.16)` · drag `0 2px 4px 0 rgba(0,0,0,0.4)`.

---

## CSS custom properties listas para el fallback HTML

```css
:root {
  /* Layout */
  --slds-bg-page: #f3f2f2;
  --slds-bg-card: #ffffff;
  --slds-bg-row-hover: #fafaf9;
  --slds-border: #dddbda;
  /* Brand / acciones */
  --slds-brand: #1b96ff;
  --slds-brand-active: #0176d3;
  --slds-brand-dark: #014486;
  --slds-link: #0b5cab;
  --slds-link-active: #014486;
  /* Texto */
  --slds-text: #2b2826;
  --slds-text-weak: #706e6b;
  --slds-text-disabled: #b0adab;
  /* Estados */
  --slds-success: #2e844a;  --slds-success-bg: #ebf7e6;
  --slds-warning: #dd7a01;  --slds-warning-bg: #fff1ea;
  --slds-error:   #ea001e;  --slds-error-bg:   #fef1ee;
  --slds-info:    #0176d3;  --slds-info-bg:    #eef4ff;
  /* Forma */
  --slds-radius: 0.25rem;
  --slds-radius-pill: 15rem;
  --slds-shadow-focus: 0 0 2px #0176d3;
  --slds-shadow-dropdown: 0 2px 3px 0 rgba(0,0,0,0.16);
  /* Tipografía */
  --slds-font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  --slds-fs-label: 0.75rem;
  --slds-fs-body: 0.875rem;
  --slds-fs-section: 1rem;
  --slds-fs-record-name: 1.5rem;
}
```

---

## Tokens completos (JSON, fuente de verdad)

```json
{
  "name": "Salesforce Lightning Design System Tokens",
  "source": "github.com/salesforce-ux/design-system",
  "typography": {
    "fontFamily": {
      "base": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'",
      "heading": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'",
      "monospace": "Consolas, Menlo, Monaco, Courier, monospace"
    },
    "fontSize": {
      "1": "0.625rem", "2": "0.75rem", "3": "0.8125rem", "4": "0.875rem",
      "5": "1rem", "6": "1.125rem", "7": "1.25rem", "8": "1.5rem",
      "9": "1.75rem", "10": "2rem", "11": "2.625rem"
    },
    "fontWeight": { "light": "300", "regular": "400", "bold": "700" },
    "lineHeight": { "heading": "1.25", "text": "1.5", "reset": "1" }
  },
  "color": {
    "brand": {
      "primary": "#1b96ff", "primaryActive": "#0176d3", "light": "#f4f6fe",
      "lightActive": "#e3e5ed", "dark": "#0176d3", "darkActive": "#253045",
      "accessible": "#0176d3", "accessibleActive": "#014486", "disabled": "#c9c7c5",
      "contrast": "#1a1b1e", "contrastActive": "#0d0e12", "backgroundPrimary": "#eef4ff",
      "backgroundDark": "#014486", "textLink": "#0b5cab", "textLinkActive": "#014486"
    },
    "palette": {
      "blue": { "10": "#001639", "15": "#03234d", "20": "#032d60", "30": "#014486", "40": "#0b5cab", "50": "#0176d3", "60": "#1b96ff", "65": "#57a3fd", "70": "#78b0fd", "80": "#aacbff", "90": "#d8e6fe", "95": "#eef4ff" },
      "cloudBlue": { "10": "#001a28", "15": "#0a2636", "20": "#023248", "30": "#084968", "40": "#05628a", "50": "#107cad", "60": "#0d9dda", "65": "#08abed", "70": "#1ab9ff", "80": "#90d0fe", "90": "#cfe9fe", "95": "#eaf5fe" },
      "green": { "10": "#071b12", "15": "#0c2912", "20": "#1c3326", "30": "#194e31", "40": "#396547", "50": "#2e844a", "60": "#3ba755", "65": "#41b658", "70": "#45c65a", "80": "#91db8b", "90": "#cdefc4", "95": "#ebf7e6" },
      "red": { "10": "#300c01", "15": "#4a0c04", "20": "#640103", "30": "#8e030f", "40": "#ba0517", "50": "#ea001e", "60": "#fe5c4c", "65": "#fe7765", "70": "#fe8f7d", "80": "#feb8ab", "90": "#feded8", "95": "#fef1ee" },
      "orange": { "10": "#201600", "15": "#371e03", "20": "#3e2b02", "30": "#5f3e02", "40": "#825101", "50": "#a96404", "60": "#dd7a01", "65": "#f38303", "70": "#fe9339", "80": "#ffba90", "90": "#fedfd0", "95": "#fff1ea" },
      "hotOrange": { "10": "#281202", "15": "#421604", "20": "#4a2413", "30": "#7e2600", "40": "#aa3001", "50": "#d83a00", "60": "#ff5d2d", "65": "#ff784f", "70": "#ff906e", "80": "#feb9a5", "90": "#ffded5", "95": "#fef1ed" },
      "yellow": { "10": "#281202", "15": "#2e2204", "20": "#4f2100", "30": "#6f3400", "40": "#8c4b02", "50": "#a86403", "60": "#ca8501", "65": "#d79304", "70": "#e4a201", "80": "#fcc003", "90": "#f9e3b6", "95": "#fbf3e0" },
      "teal": { "10": "#071b12", "15": "#072825", "20": "#023434", "30": "#024d4c", "40": "#056764", "50": "#0b827c", "60": "#06a59a", "65": "#03b4a7", "70": "#01c3b3", "80": "#04e1cb", "90": "#acf3e4", "95": "#def9f3" },
      "purple": { "10": "#240643", "15": "#300b60", "20": "#401075", "30": "#5a1ba9", "40": "#7526e3", "50": "#9050e9", "60": "#ad7bee", "65": "#b78def", "70": "#c29ef1", "80": "#d7bff2", "90": "#ece1f9", "95": "#f6f2fb" },
      "indigo": { "10": "#200647", "15": "#1f0974", "20": "#321d71", "30": "#2f2cb7", "40": "#3a49da", "50": "#5867e8", "60": "#7f8ced", "65": "#8e9bef", "70": "#9ea9f1", "80": "#bec7f6", "90": "#e0e5f8", "95": "#f1f3fb" },
      "violet": { "10": "#2e0039", "15": "#3d0157", "20": "#481a54", "30": "#730394", "40": "#9602c7", "50": "#ba01ff", "60": "#cb65ff", "65": "#d17dfe", "70": "#d892fe", "80": "#e5b9fe", "90": "#f2defe", "95": "#f9f0ff" },
      "pink": { "10": "#370114", "15": "#4b0620", "20": "#61022a", "30": "#8a033e", "40": "#b60554", "50": "#e3066a", "60": "#ff538a", "65": "#fe7298", "70": "#fe8aa7", "80": "#fdb6c5", "90": "#fddde3", "95": "#fef0f3" },
      "warmGray": { "1": "#FFFFFF", "2": "#fafaf9", "3": "#f3f2f2", "4": "#ecebea", "5": "#dddbda", "6": "#c9c7c5", "7": "#b0adab", "8": "#969492", "9": "#706e6b", "10": "#514f4d", "11": "#3e3e3c", "12": "#2B2826", "13": "#080707" },
      "coolGray": { "1": "#FFFFFF", "2": "#F9F9FA", "3": "#F2F2F3", "4": "#E9EAEC", "5": "#D9DBDD", "6": "#C4C6CA", "7": "#ABADB0", "8": "#919297", "9": "#6B6D70", "10": "#4E5356", "11": "#3E4041", "12": "#292C2E", "13": "#070808" },
      "neutral": { "00": "#000000", "10": "#181818", "15": "#242424", "20": "#2e2e2e", "30": "#444444", "40": "#5c5c5c", "50": "#747474", "60": "#939393", "65": "#a0a0a0", "70": "#aeaeae", "80": "#c9c9c9", "90": "#e5e5e5", "95": "#f3f3f3", "100": "#ffffff" }
    },
    "semantic": { "success": "#2e844a", "warning": "#dd7a01", "error": "#ea001e", "info": "#0176d3" },
    "base": { "white": "#FFFFFF", "black": "#000000" }
  },
  "spacing": { "none": "0", "xxxSmall": "0.125rem", "xxSmall": "0.25rem", "xSmall": "0.5rem", "small": "0.75rem", "medium": "1rem", "large": "1.5rem", "xLarge": "2rem", "xxLarge": "3rem" },
  "borderRadius": { "small": "0.125rem", "medium": "0.25rem", "large": "0.5rem", "circle": "50%", "pill": "15rem" },
  "borderWidth": { "thin": "1px", "thick": "2px" },
  "boxShadow": { "active": "0 0 2px #0176d3", "dropDown": "0 2px 3px 0 rgba(0,0,0,0.16)", "drag": "0 2px 4px 0 rgba(0,0,0,0.4)" }
}
```
