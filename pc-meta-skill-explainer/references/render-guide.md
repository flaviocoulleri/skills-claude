# Guía de render de los widgets

Dos templates en `assets/`. Vos solo inyectás **datos** en los placeholders; la
lógica (búsqueda, clicks) ya está horneada (Q08). Antes del primer `show_widget`
de la sesión, llamá silenciosamente a `mcp__visualize__read_me` con
`modules: ["interactive"]`.

## `skill-picker-panel.html` — Modo Elegir / Filtrar

Placeholder único **`__SKILLS_JSON__`**: array de fichas breves de los skills
**disponibles para esta persona** (ya reconciliados; ver `data-sources.md`).

```json
[
  {"name":"pc-sales-sf-quote-builder","area":"comercial","type":"builder",
   "one_liner":"Construye Quotes en Salesforce…","connectors":["salesforce","google-drive"]},
  {"name":"pc-meta-skill-explainer","area":"meta","type":"utility",
   "one_liner":"Explica cómo funciona un skill…","connectors":[]}
]
```

- En **Modo Filtrar** pasás ya filtrada la lista (p. ej. solo los que tienen
  `salesforce` en `connectors`) y agregás una línea de contexto en tu mensaje.
- El widget agrupa por `area`, trae buscador local y al tocar una tarjeta dispara
  `Explícame cómo funciona <name>`.

## `skill-explanation-panel.html` — Modo Explicar

Placeholder único **`__SKILL_JSON__`**: la ficha completa de UN skill.

```json
{
  "name":"pc-sales-sf-quote-builder","area":"comercial","type":"builder",
  "one_liner":"Construye Quotes en Salesforce con líneas planas…",
  "connectors":["salesforce","google-drive","slack"],
  "connectors_source":"requiere-line",
  "when_to_use":["ármame la quote","build the quote","importa las historias del doc"],
  "writes":true,
  "steps":["Paso 1 — Asegurar Opp existente","Paso 2 — Detectar Quote previa","…"],
  "help_quality":"basic"
}
```

- Copiá los campos tal cual del registry (o de la ficha mínima). No inventes pasos:
  si `steps` viene vacío, el widget ya muestra el mensaje correcto.
- `connectors_source` **debe** ir: el widget elige el verbo y la advertencia según
  su valor (ver tabla en `data-sources.md`).
- Botones de pie ya cableados: "Ver otro skill" → `Explícame mis skills`; "Usar
  este skill ahora" → arma el prompt desde `when_to_use[0]` (o un fallback con el
  `name`).

## Sustitución de placeholders

Reemplazá el token por el JSON **crudo** (sin comillas alrededor):

- ✅ `var SKILLS = [ {...}, {...} ];`
- ❌ `var SKILLS = "[{...}]";`

## Fallback sin widgets

Si `mcp__visualize__show_widget` no está disponible, listá los skills en markdown
(agrupados por área) y explicá el elegido en prosa con las mismas secciones: Qué
hace · Conectores (con la advertencia si son inferidos) · Paso a paso · Cuándo
usarlo · ¿Escribe datos?.
