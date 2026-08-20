# Widget shell canónico — pc-delivery-slack-channel-auditor

> **Esta es la ÚNICA fuente de verdad para el HTML de TODOS los widgets del
> skill.** Cada `mcp__visualize__show_widget` (Fases 0, 3A, 5.2, 6, 7, 8, 9,
> 10) se arma **componiendo los bloques de abajo**, no inventando markup nuevo.
> Si dos widgets muestran lo mismo (header, KPIs, tabla, checklist, botones),
> tienen que verse idénticos — para eso existe este archivo.

## Principios (alineados con la plataforma `visualize`)

1. **Tema auto-adaptable, NO forzado.** Usar los tokens nativos de la
   plataforma (`--surface-*`, `--text-*`, `--bg-*`, `--border*`), que siguen
   automáticamente claro/oscuro del host. **No** forzar dark ni overridear
   variables; **no** poner background en el contenedor exterior (el host lo
   provee — contenedor transparente).
2. **Cero colores hardcoded.** Nunca `#fff`, `#000`, `rgb(...)` ni nombres de
   color. Solo tokens. Un hex hardcodeado es invisible o ilegible en uno de los
   dos modos.
3. **Íconos Tabler, no emoji.** En el HTML de los widgets usar la webfont
   Tabler (`<i class="ti ti-NAME" aria-hidden="true"></i>`), no emoji. (Los
   emoji SÍ valen en el **texto de mensajes Slack** —drafts de Fase 6/7/10— que
   no es HTML; ahí Slack los renderiza nativo.)
4. **Sentence case**, pesos 400/500 únicamente, sin gradientes ni sombras
   decorativas. Números siempre redondeados.

## Cómo usar este shell

1. Compones los bloques que la fase necesite, **en este orden canónico**:
   `header-card` → (`kpi-grid` | `banner`) → cuerpo (`data-table` o
   `checklist-block` o `form`) → `button-row`.
2. No hace falta wrapper exterior: el contenido arranca directo y llena el
   widget (~680px de ancho).
3. Antes de pegar el HTML, corre el **test mental** del final.

---

## Tokens disponibles (referencia rápida)

| Rol | Tokens |
|---|---|
| Superficies | `--surface-2` (card), `--surface-1` (sutil), `--surface-0` (página) |
| Texto | `--text-primary`, `--text-secondary`, `--text-muted`; rol `--text-{accent,danger,success,warning}` |
| Fondos de rol | `--bg-{accent,danger,success,warning}`, `--bg-pro` (violeta) |
| Bordes | `--border` (hairline 0.5px), `--border-strong`; rol `--border-{accent,danger,success,warning}` |
| Layout | `--radius` (8px controles); `12px` para cards |

Inputs, selects, textarea, range y `<button>` ya vienen pre-estilados — úsalos
"pelados" y solo overridea el ancho si hace falta.

---

## Bloque `header-card` — encabezado estándar

Card de acento con título + filas key/value + slot de badges. Mismo estilo en
todas las fases; cada una pasa título y pares.

```html
<div style="background: var(--bg-accent); border-radius: 12px; padding: 10px 12px; margin-bottom: 10px;">
  <div style="font-weight: 500; color: var(--text-primary); font-size: 15px;">{TÍTULO}</div>
  <div style="font-size: 13px; color: var(--text-secondary);">{pares · separados · por · puntos}</div>
  <!-- slot de badges opcional (bloque `badges`) -->
</div>
```

**Qué pone cada fase en el header:**

| Fase | Título | Pares key/value | Badges |
|---|---|---|---|
| 5.2 | Auditoría de canales externos | PM auditado + email · Fecha · Thresholds (R0=7d) · Modo | `Modo manager — caller: <email>` si `is_manager_audit` |
| 7 | Draft de DM para `<PM_NAME>` | Caller · Hora estimada de envío · Contador "N de M items" | `is_first_dm_today` si aplica |
| 8 | Jira cross-check | Project + Account · Channel (link) · Jira board (URL) · Timestamp | — |
| 9 | Updates SF desde canales | PM auditado · Fecha · # proyectos en scope | — |
| 10 | Repo check | Project + Account · Repo (link) · Threshold (N días) | Estado global (ver `badges`) |

Fases 0, 3A, 6 usan un header simple (título + 1 línea de contexto).

---

## Bloque `kpi-grid` — grilla de KPI cards

Grilla de cards. Card estándar: label arriba (secundario), valor grande abajo
(primario), border-left de color de rol según umbral.

```html
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 8px; margin-bottom: 10px;">
  <!-- card neutra -->
  <div style="background: var(--surface-1); border-radius: var(--radius); padding: 8px 10px;">
    <div style="font-size: 12px; color: var(--text-secondary);">{label}</div>
    <div style="font-size: 22px; font-weight: 500; color: var(--text-primary);">{valor}</div>
  </div>
  <!-- card crítica: sumar border-left -->
  <div style="background: var(--surface-1); border-radius: var(--radius); padding: 8px 10px; border-left: 3px solid var(--border-danger); border-radius: 0 var(--radius) var(--radius) 0;">
    <div style="font-size: 12px; color: var(--text-secondary);">{label}</div>
    <div style="font-size: 22px; font-weight: 500; color: var(--text-primary);">{valor}</div>
  </div>
</div>
```

**border-left por semántica del KPI:** crítico >0 → `--border-danger`;
warning >0 → `--border-warning`; success → `--border-success`; neutro → sin
border-left. (Borde de un solo lado ⇒ sin radius en ese lado.)

**Qué métricas pone cada fase:**

| Fase | KPI cards |
|---|---|
| 5.2 | `scanned_projects` (neutro) · `r0_red` (danger) · `missing_asset` (warn) · `missing_comercial_sf` (warn) · `client_anomaly` (danger) · `inaccessible` (warn) · `ok` (success) · `finished_recently` (neutro) |
| 8 | N críticos (danger) · N faltantes (warn) · N informativos (neutro) |
| 10 | Commits en últimos N días · Autores únicos · Último commit (relativo) · Branch principal |

Fases 0, 3A, 6, 7, 9 no usan `kpi-grid`.

---

## Bloque `banner` — aviso prominente (estados especiales)

Banner full-width con tint de rol, para estados que merezcan destacarse (status
general de Fase 8, estado del repo en Fase 10).

```html
<div style="background: var(--bg-warning); color: var(--text-warning); border-left: 3px solid var(--border-warning); border-radius: 0 var(--radius) var(--radius) 0; padding: 8px 10px; margin-bottom: 10px; font-size: 13px;">
  <i class="ti ti-alert-triangle" aria-hidden="true"></i> {contenido}
</div>
```

Cambia el trío `--bg-* / --text-* / --border-*` a `danger`, `success` o
`accent` según la semántica.

---

## Bloque `data-table` — tabla base + add-ons

Tabla con header en `--surface-1` y filas con tint de rol. **Siempre dentro de
un wrapper con scroll horizontal** (`overflow-x: auto`) — la tabla de Fase 5.2
tiene 15 columnas y no entra en ~680px; el scroll es la solución estándar.

```html
<div style="overflow-x: auto;">
  <table style="width: 100%; border-collapse: collapse; font-size: 12.5px;">
    <thead>
      <tr style="background: var(--surface-1); color: var(--text-secondary); text-align: left;">
        <th style="padding: 6px 8px; font-weight: 500; white-space: nowrap;">{columna}</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 0.5px solid var(--border);">
        <td style="padding: 6px 8px; color: var(--text-primary);">{celda}</td>
      </tr>
    </tbody>
  </table>
</div>
```

**Tint de fila por semántica** (`<tr>`): default/OK → transparente; R0/crítica →
`--bg-danger`; warning (⚠ incompleto, sin canal) → `--bg-warning`; gris
(FINISHED, INACCESSIBLE) → `--surface-1`; hover → `--surface-1`.

**Add-ons (solo Fase 5.2):** columna `multi-select` (checkbox por fila + master
en el `<th>`), columna `kebab` (ícono `ti-dots-vertical` con dropdown; las
acciones de escritura disparan `sendPrompt`, nunca inline), y barra de
`filtros` arriba (input de búsqueda + selects, JS vanilla, sin librerías).

**Link a Slack en celda Canal:**
`<a href="slack://channel?id={channel_id}" style="color: var(--text-accent);">#nombre</a>`.
Sin `channel_id` (filas `MISSING_CHANNEL`) → "—".

---

## Bloque `checklist-block` — checklist de ítems propuestos (patrón v2.6)

Patrón único para todo flow que proponga ítems a incluir en un mensaje
(Fases 6, 7, 9).

**Reglas inviolables:**
1. **Default = todos tildados.** El caller destilda. Ítems de riesgo especial
   (finalizado, bloqueo escalado) se marcan con un ícono `ti-alert-triangle`
   pero vienen tildados. **Excepción (Fase 9):** campos `confidence='low'`
   vienen **destildados**.
2. **Preview live.** Panel que re-arma el texto cada vez que cambia un checkbox.
3. **Counter en el botón de envío.** "… con **N items**" — N en vivo; N=0 ⇒
   botón deshabilitado.
4. **Editar individual (`ti-pencil`).** Mini-input inline por ítem.
5. **Cancelar siempre disponible.**
6. **No autocompletar.** Destildar todo no equivale a "envía igual" ni a
   "cancelado" — el caller hace click explícito.

```html
<div style="display: flex; gap: 12px; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 240px;">
    <label style="display: block; font-weight: 500; color: var(--text-primary); margin: 8px 0 2px;">
      <input type="checkbox" checked> {Sección N · título}
    </label>
    <label style="display: flex; align-items: center; gap: 8px; padding: 3px 0 3px 20px; color: var(--text-primary); font-size: 13px;">
      <input type="checkbox" checked> {línea del ítem}
      <i class="ti ti-pencil" aria-hidden="true" style="cursor: pointer;"></i>
    </label>
  </div>
  <div style="flex: 1; min-width: 240px; background: var(--surface-1); border-radius: var(--radius); padding: 10px;">
    <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 4px;">Preview live</div>
    <pre style="white-space: pre-wrap; color: var(--text-primary); font-family: inherit; font-size: 12.5px; margin: 0; line-height: 1.5;">{preview}</pre>
  </div>
</div>
```

**Cuándo NO aplica:** confirmaciones binarias (crear canal sí/no) → `button-row`
con [Confirmar]/[Cancelar]. Drafts standalone a canal externo (Fase 6.2) →
widget propio con [Copiar]/[Editar]/[Cerrar]. El checklist aplica solo a la
**lista** de drafts (Fase 6.1), no al contenido de cada draft.

---

## Bloque `button-row` / `cta` — botones y convención sendPrompt

Fila de botones al pie. **Toda opción/CTA/próximo paso va como botón acá, nunca
como bullets de texto en chat.** Los `<button>` ya vienen pre-estilados; úsalos
pelados con un ícono Tabler opcional al inicio.

```html
<div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;">
  <button onclick="sendPrompt('{intent en lenguaje natural}')">
    <i class="ti ti-link" aria-hidden="true"></i> {label} ↗
  </button>
</div>
```

**Reglas:**
- Cada botón que dispara una acción de Claude usa `sendPrompt('<intent>')` y
  lleva una flecha `↗` al final del label. Acciones puramente locales (copiar
  con `navigator.clipboard.writeText`, toggles, edición inline) no usan
  `sendPrompt` ni flecha.
- **NUNCA** ejecutar una escritura (Slack/SF) inline desde el botón: las
  escrituras pasan SIEMPRE por un widget de confirmación (ver `safety-rules.md`).
- Evitar botones deshabilitados salvo el de envío con N=0 (con tooltip).

---

## Bloque `badges` — pills semánticas con ícono Tabler

Pill reutilizable: fondo de rol + texto de rol + ícono Tabler. Mismo estilo en
todas las fases. **Sin emoji.**

```html
<span style="display: inline-flex; align-items: center; gap: 3px; padding: 1px 7px; border-radius: var(--radius); font-size: 11.5px; font-weight: 500; background: var(--bg-danger); color: var(--text-danger);">
  <i class="ti ti-flame" aria-hidden="true"></i> P1
</span>
```

| Badge | Fondo / texto | Ícono Tabler |
|---|---|---|
| Prioridad alta P1/P2 | `--bg-danger` / `--text-danger` | `ti-flame` |
| Prioridad P3-P5 | `--bg-warning` / `--text-warning` | (sin ícono, "P{n}") |
| Tipo Delivery | `--bg-accent` / `--text-accent` | `ti-rocket` |
| Tipo Support | `--bg-pro` / `--text-pro` | `ti-lifebuoy` |
| Confidence high (Fase 9) | `--bg-success` / `--text-success` | `ti-circle-check` |
| Confidence medium | `--bg-warning` / `--text-warning` | — |
| Confidence low | `--bg-danger` / `--text-danger` | `ti-alert-circle` |
| Severidad Crítico (Fase 8) | `--bg-danger` / `--text-danger` | `ti-alert-triangle` |
| Severidad Faltante | `--bg-warning` / `--text-warning` | `ti-help-circle` |
| Severidad Informativo | `--surface-1` / `--text-secondary` | `ti-info-circle` |
| Estado repo Activo (Fase 10) | `--bg-success` / `--text-success` | `ti-circle-check` |
| Estado repo Poco activo | `--bg-warning` / `--text-warning` | `ti-alert-triangle` |
| Estado repo Inactivo | `--bg-danger` / `--text-danger` | `ti-circle-x` |
| Status DM Completo / Incompleto / Falta | success / warning / danger | `ti-check` / `ti-alert-triangle` / `ti-x` |
| Menciones en DM 1:1 | (texto + ícono) | `ti-message` |
| Sensibilidad alta del DM | (ícono al lado) | `ti-lock` |
| Modo manager | `--bg-accent` / `--text-accent` | `ti-users` |

**Bloqueo del cliente (columna de la tabla):** ícono + texto corto —
`ti-calendar-off` No vino a meet / `ti-volume-off` No responde /
`ti-edit-off` No define temas / `ti-package` No entrega pendings / "—" (none).

---

## Test mental obligatorio antes de pegar el HTML

> **"¿Cada texto y borde se lee bien tanto en claro como en oscuro?"** Si usaste
> solo tokens (`--surface-*`, `--text-*`, `--bg-*`, `--border*`) y ningún hex
> hardcodeado, la respuesta es sí automáticamente. Si hardcodeaste un color,
> reemplázalo por el token de rol más cercano antes de pegar.

Y: ningún emoji en el HTML del widget (sí en texto de mensajes Slack).
