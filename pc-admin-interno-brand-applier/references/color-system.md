# ProContacto Color System — Referencia Técnica Completa

Fuente canónica: `colors_and_type.css` del ProContacto Design System (ProContactoDesignSystem_019dd0).

---

## Colores de marca

| Rol | Token | Hex |
|-----|-------|-----|
| **Azul primario** | `--pc-blue-500` | `#0062FF` |
| **Violeta secundario** | `--pc-violet-500` | `#8F7AFF` |
| **Canvas de fondo** | `--pc-bg-canvas` | `#0B0C0E` |

---

## Escala del Azul (Blue)

| Shade | Token | Hex |
|-------|-------|-----|
| 100 | `--pc-blue-100` | `#CCE7FF` |
| 200 | `--pc-blue-200` | `#99CCFF` |
| 300 | `--pc-blue-300` | `#66ACFF` |
| 400 | `--pc-blue-400` | `#3F90FF` |
| **500** (base) | `--pc-blue-500` | `#0062FF` |
| 600 | `--pc-blue-600` / `--pc-blue-deep` | `#004BDB` |
| 700 | `--pc-blue-700` | `#0032A3` |
| 800 | `--pc-blue-800` | `#001B66` |
| 900 | `--pc-blue-900` | `#000B33` |

## Escala del Violeta (Violet)

| Shade | Token | Hex |
|-------|-------|-----|
| 100 | `--pc-violet-100` | `#EAE4FF` |
| 200 | `--pc-violet-200` | `#D4C9FF` |
| 300 | `--pc-violet-300` | `#BEAFFF` |
| 400 | `--pc-violet-400` | `#AC9BFF` |
| **500** (base) | `--pc-violet-500` | `#8F7AFF` |
| 600 | `--pc-violet-600` | `#6B59DB` |
| 700 | `--pc-violet-700` | `#4C3DB7` |
| 800 | `--pc-violet-800` | `#322693` |
| 900 | `--pc-violet-900` | `#20177A` |

---

## Gradientes

| Token | Valor | Uso |
|-------|-------|-----|
| `--pc-gradient` | `linear-gradient(180deg, #0062FF 0%, #8F7AFF 100%)` | Fondos full-bleed, CTA bands, portadas en modo gradiente |
| `--pc-gradient-radial` | `radial-gradient(ellipse at 50% 100%, #0062FF 0%, #1a1280 35%, #0B0C0E 70%, #000000 100%)` | Fondo alternativo con transición desde azul al canvas |
| `--pc-gradient-glow` | `radial-gradient(ellipse 80% 50% at 50% 100%, rgba(0,98,255,0.55) 0%, rgba(143,122,255,0.25) 35%, rgba(11,12,14,0) 70%)` | Aurora azul→violeta superpuesta en portadas oscuras |

**Regla**: el gradiente va **solo en fondos**. Nunca en el logo, nunca en texto.

---

## Colores de estado (Status)

| Estado | Token base | Hex base | Token light | Hex light |
|--------|------------|----------|-------------|-----------|
| Success | `--pc-success-500` | `#009060` | `--pc-success-100` | `#C1E7D5` |
| Information | `--pc-info-500` | `#0070DD` | `--pc-info-100` | `#99CCFF` |
| Error | `--pc-error-500` | `#D21E41` | `--pc-error-100` | `#FBCCD7` |
| Warning | `--pc-warning-500` | `#DF4D03` | `--pc-warning-100` | `#FDCCB9` |

Cuando uses colores de status como fondo de badge: usa la variante light de fondo + la base como texto.

---

## Jerarquía de fondos (Backgrounds / Elevation)

| Token | Hex | Uso |
|-------|-----|-----|
| `--pc-bg-deepest` | `#000000` | Negro puro (sombras duras, overlays) |
| `--pc-bg-canvas` | `#0B0C0E` | Canvas principal — fondo de toda composición |
| `--pc-bg-elev-1` | `#1A1B1E` | Primera elevación |
| `--pc-bg-elev-2` | `#1F1F1F` | Cards, paneles |
| `--pc-bg-elev-3` | `#1F1F1F` | Cards anidadas |
| `--pc-bg-elev-4` | `#333333` | — |

---

## Escala de Neutrales (Gray)

| Token | Hex | Uso |
|-------|-----|-----|
| `--pc-neutral-0` | `#FFFFFF` | Blanco puro |
| `--pc-neutral-100` | `#F2F2F2` | Gray1 — fondos claros alternativos |
| `--pc-neutral-200` | `#D9D9D9` | Gray2 |
| `--pc-neutral-300` | `#BFBFBF` | Gray3 |
| `--pc-neutral-400` | `#A6A6A6` | Gray4 |
| `--pc-neutral-500` | `#8C8C8C` | Gray5 |
| `--pc-neutral-600` | `#737373` | Gray6 |
| `--pc-neutral-700` | `#4D4D4D` | Gray7 |
| `--pc-neutral-800` | `#333333` | Gray8 |
| `--pc-neutral-850` | `#1F1F1F` | Gray9 |
| `--pc-neutral-900` | `#0D0D0D` | Gray10 |
| `--pc-neutral-1000` | `#000000` | Negro |

---

## Tokens semánticos — para UI

| Token | Referencia | Uso |
|-------|-----------|-----|
| `--bg` | `#0B0C0E` | Fondo base |
| `--bg-elevated` | `#1F1F1F` | Elemento flotante sobre canvas |
| `--surface` | `#1F1F1F` | Cards, paneles |
| `--surface-2` | `#1F1F1F` | Cards anidadas |
| `--border` | `rgba(255,255,255,0.10)` | Bordes en superficies oscuras |
| `--border-strong` | `rgba(255,255,255,0.18)` | Bordes hover/focus |
| `--fg` | `#FFFFFF` | Texto principal |
| `--fg-1` | `rgba(255,255,255,0.96)` | Texto alto énfasis |
| `--fg-2` | `rgba(255,255,255,0.72)` | Texto cuerpo |
| `--fg-3` | `rgba(255,255,255,0.52)` | Labels, secundario |
| `--fg-4` | `rgba(255,255,255,0.34)` | Footers, terciario |
| `--fg-on-blue` | `#FFFFFF` | Texto sobre fondo azul |
| `--fg-on-light` | `#0A0A19` | Texto sobre fondo claro |
| `--accent` | `#0062FF` | Acento primario |
| `--accent-2` | `#8F7AFF` | Acento secundario |
| `--link` | `#66ACFF` | Links en superficie oscura |
| `--link-hover` | `#99CCFF` | Links hover |
| `--success` | `#009060` | Status: success |
| `--info` | `#0070DD` | Status: info |
| `--warning` | `#DF4D03` | Status: warning |
| `--danger` | `#D21E41` | Status: error |

---

## CSS completo para HTML/React artifacts

```css
/* ProContacto Design System — copiar en todo artifact */
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wdth,wght@0,75..100,300..800;1,75..100,300..800&display=swap');

:root {
  /* ─── Brand ─── */
  --pc-blue-100: #CCE7FF;
  --pc-blue-200: #99CCFF;
  --pc-blue-300: #66ACFF;
  --pc-blue-400: #3F90FF;
  --pc-blue-500: #0062FF;
  --pc-blue-600: #004BDB;
  --pc-blue-700: #0032A3;
  --pc-blue-800: #001B66;
  --pc-blue-900: #000B33;

  --pc-violet-100: #EAE4FF;
  --pc-violet-200: #D4C9FF;
  --pc-violet-300: #BEAFFF;
  --pc-violet-400: #AC9BFF;
  --pc-violet-500: #8F7AFF;
  --pc-violet-600: #6B59DB;
  --pc-violet-700: #4C3DB7;
  --pc-violet-800: #322693;
  --pc-violet-900: #20177A;

  --pc-gradient: linear-gradient(180deg, #0062FF 0%, #8F7AFF 100%);
  --pc-gradient-radial: radial-gradient(ellipse at 50% 100%, #0062FF 0%, #1a1280 35%, #0B0C0E 70%, #000000 100%);
  --pc-gradient-glow: radial-gradient(ellipse 80% 50% at 50% 100%, rgba(0,98,255,0.55) 0%, rgba(143,122,255,0.25) 35%, rgba(11,12,14,0) 70%);

  /* ─── Status ─── */
  --pc-success-100: #C1E7D5;  --pc-success-500: #009060;
  --pc-info-100:    #99CCFF;  --pc-info-500:    #0070DD;
  --pc-error-100:   #FBCCD7;  --pc-error-500:   #D21E41;
  --pc-warning-100: #FDCCB9;  --pc-warning-500: #DF4D03;

  /* ─── Backgrounds ─── */
  --pc-bg-canvas:  #0B0C0E;
  --pc-bg-elev-1:  #1A1B1E;
  --pc-bg-elev-2:  #1F1F1F;
  --pc-bg-elev-4:  #333333;

  /* ─── Neutrals ─── */
  --pc-neutral-0:   #FFFFFF;
  --pc-neutral-100: #F2F2F2;
  --pc-neutral-200: #D9D9D9;
  --pc-neutral-500: #8C8C8C;
  --pc-neutral-800: #333333;

  /* ─── Semantic tokens (usar estos en UI) ─── */
  --bg:            #0B0C0E;
  --bg-elevated:   #1A1B1E;
  --surface:       #1F1F1F;
  --surface-2:     #1F1F1F;
  --border:        rgba(255,255,255,0.10);
  --border-strong: rgba(255,255,255,0.18);

  --fg:            #FFFFFF;
  --fg-1:          rgba(255,255,255,0.96);
  --fg-2:          rgba(255,255,255,0.72);
  --fg-3:          rgba(255,255,255,0.52);
  --fg-4:          rgba(255,255,255,0.34);
  --fg-on-blue:    #FFFFFF;
  --fg-on-light:   #0A0A19;

  --accent:        #0062FF;
  --accent-2:      #8F7AFF;
  --link:          #66ACFF;
  --link-hover:    #99CCFF;

  --success:       #009060;
  --info:          #0070DD;
  --warning:       #DF4D03;
  --danger:        #D21E41;

  /* ─── Typography ─── */
  --font-sans:     'Open Sans', system-ui, -apple-system, sans-serif;
  --w-light:       300;
  --w-regular:     400;
  --w-bold:        700;
  --w-extrabold:   800;

  --t-display-xl:  clamp(56px, 8vw, 120px);
  --t-display-lg:  clamp(44px, 6vw, 80px);
  --t-display-md:  clamp(36px, 4.5vw, 56px);
  --t-h1:          clamp(32px, 3.5vw, 48px);
  --t-h2:          clamp(26px, 2.6vw, 36px);
  --t-h3:          22px;
  --t-h4:          18px;
  --t-body-lg:     18px;
  --t-body:        16px;
  --t-body-sm:     14px;
  --t-caption:     12px;

  --lh-tight:   1.05;
  --lh-snug:    1.18;
  --lh-normal:  1.45;
  --lh-relaxed: 1.6;

  --ls-tight:   -0.02em;
  --ls-snug:    -0.01em;
  --ls-wide:    0.04em;
  --ls-overline:0.12em;

  /* ─── Spacing (8pt grid) ─── */
  --s-1:4px; --s-2:8px; --s-3:12px; --s-4:16px; --s-5:24px;
  --s-6:32px; --s-7:48px; --s-8:64px; --s-9:96px; --s-10:128px;

  /* ─── Radii ─── */
  --r-xs:4px; --r-sm:6px; --r-md:10px; --r-lg:16px; --r-xl:24px; --r-2xl:32px; --r-pill:9999px;

  /* ─── Shadows ─── */
  --shadow-sm:         0 1px 2px rgba(0,0,0,0.45);
  --shadow-md:         0 8px 24px rgba(0,0,0,0.45);
  --shadow-lg:         0 24px 64px rgba(0,0,0,0.55);
  --shadow-glow-blue:  0 0 0 1px rgba(0,98,255,0.4), 0 8px 32px rgba(0,98,255,0.35);
  --shadow-glow-violet:0 0 60px rgba(143,122,255,0.45);

  /* ─── Motion ─── */
  --ease-out:    cubic-bezier(.2,.8,.2,1);
  --ease-in-out: cubic-bezier(.65,.05,.36,1);
  --dur-quick:   140ms;
  --dur-base:    220ms;
  --dur-slow:    420ms;

  font-family: var(--font-sans);
  background: var(--bg);
  color: var(--fg-1);
  -webkit-font-smoothing: antialiased;
}

/* ─── Clases de tipografía ─── */
.pc-display-xl { font-size: var(--t-display-xl); font-weight: 800; line-height: 1.05; letter-spacing: -0.02em; }
.pc-display-lg { font-size: var(--t-display-lg); font-weight: 800; line-height: 1.05; letter-spacing: -0.02em; }
.pc-subtitle   { font-size: var(--t-display-md); font-weight: 300; line-height: 1.18; color: var(--fg-2); }
.pc-h1         { font-size: var(--t-h1);         font-weight: 800; line-height: 1.18; }
.pc-h2         { font-size: var(--t-h2);         font-weight: 800; line-height: 1.18; }
.pc-h3         { font-size: var(--t-h3);         font-weight: 700; }
.pc-body-lg    { font-size: var(--t-body-lg);    font-weight: 400; line-height: 1.6; }
.pc-body       { font-size: var(--t-body);       font-weight: 400; line-height: 1.6; }
.pc-body-sm    { font-size: var(--t-body-sm);    font-weight: 400; line-height: 1.45; }
.pc-caption    { font-size: var(--t-caption);    color: var(--fg-3); }
.pc-overline   { font-size: 11px; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 700; color: var(--fg-3); }
.pc-anclaje    { font-size: 14px; font-weight: 400; letter-spacing: -0.01em; color: var(--fg-2); }

/* ─── Cards ─── */
.pc-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: var(--s-5);
  box-shadow: var(--shadow-md);
}

/* ─── Fondos ─── */
.pc-bg-blue     { background: var(--pc-blue-500); color: #fff; }
.pc-bg-violet   { background: var(--pc-violet-500); color: #fff; }
.pc-bg-dark     { background: var(--pc-bg-canvas); color: var(--fg-1); }
.pc-bg-gradient { background: var(--pc-gradient); color: #fff; }

/* ─── Selección ─── */
::selection { background: var(--pc-blue-500); color: #fff; }
```

---

## Tailwind — equivalencias aproximadas

Para componentes Tailwind que necesiten colores de marca (no exactos — para exactitud usar inline styles con los tokens):

| Rol PC | Tailwind aproximado |
|--------|---------------------|
| `#0062FF` (blue-500) | `blue-600` |
| `#8F7AFF` (violet-500) | `violet-400` |
| `#0B0C0E` (canvas) | `gray-950` |
| `#1F1F1F` (surface) | `gray-900` |
| `#009060` (success) | `emerald-600` |
| `#D21E41` (error) | `rose-600` |

Para precisión de marca, usar siempre los hex canónicos del Design System via inline styles o variables CSS.
