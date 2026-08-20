<!-- ⚠️ AUTO-COPIADO desde _shared/presentation-builder/ por sync.sh — NO EDITAR ACÁ. Editá el canónico y volvé a correr sync.sh. -->

# Patrón visual estándar del skill

Este skill conversa con el usuario en muchos pasos y necesita verse **consistente** del primer paso al último. Toda interacción que requiera elección o input usa `mcp__visualize__show_widget`, nunca bullets en chat ni `AskUserQuestion`. Las screenshots que validó Ariel el 2026-05-26 son la referencia: lo que está bien renderizado ahí, así debe renderizarse en todos los pasos.

## Reglas globales

1. **Siempre `mcp__visualize__show_widget`** para todo lo que requiera click del usuario, salvo cuando el usuario está dictando texto libre extenso (en ese caso, dentro del widget va un `<textarea>`).
2. **Llama a `mcp__visualize__read_me` antes del primer widget** de la conversación. No lo narres al usuario — es preparación silenciosa.
3. **Idioma del widget = idioma de la conversación** (default español).
4. **Tono cercano, no corporativo.** "¿Para qué área es la presentación?" — no "Por favor, indique el área…".
5. **Una pregunta por widget.** Si necesitas 5 cosas, haz un form con 5 campos en un solo widget — no 5 widgets seguidos.
6. **Muestra el progreso** cuando el flujo tiene varios pasos. Header del widget: "Paso 2 de 5 — Datos del cliente" o un breadcrumb minimalista.

## Patrón A — Pregunta de opciones discretas (cards)

Úsalo para: pregunta de área (Comercial/Delivery), sub-flujo comercial (A medida / Base de Drive), Record Type, hito de proyecto, "¿cómo quieres resolver el pricing?", "¿qué hacemos ahora?".

**Layout:**
- Grilla `repeat(auto-fit, minmax(260px, 1fr))` con `gap: 16px`. En desktop típicamente 2 columnas; mobile colapsa a 1.
- Cada opción es una **card clicable** con padding generoso (20-24px), border-radius 8-12px, borde sutil, hover state.
- Pregunta arriba o abajo de la grilla, en tono natural, terminando en signo de pregunta.

**Estructura de cada card:**
1. **Icono** (Lucide o emoji). Tamaño 24-28px. Color tenue.
2. **Badge "Recomendado"** arriba a la izquierda (pill azul) — sólo en la opción recomendada cuando aplique.
3. **Título** bold, 16-18px.
4. **Descripción** en 2-3 líneas, gris medio. Qué hace esta opción y cómo se diferencia de las otras.
5. **Línea ejemplo / "Ideal para…"** en gris más claro, 1 línea, tono "cuándo elegir esta".

**Ejemplo de markup conceptual** (no usar literal — usar el design system de Cowork):

```
[ICON]                              [Recomendado]
A medida
Capturo Record Type, cliente, industria y contexto.
Enriquezco con conectores y resuelvo pricing desde Salesforce.
Propuesta 100% personalizada.

Ideal cuando hay un deal real con Opp en SF.
```

## Patrón B — Form de captura de datos del cliente / proyecto

Úsalo para: Paso 2 (datos del cliente comercial), Paso 1B.3 (datos del proyecto delivery), captura de pricing manual si el AE quiere dictar números.

**Layout:**
- Una sola card-form con header explicativo y campos adentro.
- Header: bold, 1 frase ("Ahora necesito el contexto del cliente para personalizar el prompt. ¿Me pasas estos datos?").
- Campos cortos (Cliente, País, URL) en grilla de 2 columnas; campos largos (Brief, modelos operativos) full-width.
- Botón "Continuar" abajo a la derecha. Botón "Cancelar" o "Atrás" a la izquierda si es navegable.

**Estructura de cada campo:**
1. **Label** en bold arriba, 14-15px. Si es requerido, asterisco rojo (`*`) inmediatamente después del label.
2. **Input** con placeholder de ejemplo concreto (no genérico). Ejemplos:
   - Cliente: `Nombre comercial del cliente` (no "Cliente").
   - País: `Ej: México, Colombia, Argentina`.
   - Industria: `Ej: Alimentos y bebidas, Cuidado personal, Distribuidora, etc.`
   - Stakeholder: `Ej: Director Comercial, CIO, VP de Operaciones`.
   - Brief: `¿Qué quiere el cliente? ¿Qué dolor lo trajo? ¿Por qué nos contactó?` (placeholder en textarea).
   - Web del cliente: `https://www.ejemplo.com`.
3. **Helper text** debajo cuando aporte ("Si no sabes todavía, déjalo vacío"; "Si la pasas, leo la home y un par de páginas clave").
4. **Select** para campos cerrados (Idioma del deck con default "Español"; Record Type cuando va dentro del form).

**Campos típicos del Paso 2 (comercial a-medida):**

| Campo | Tipo | Requerido | Placeholder |
|---|---|---|---|
| Cliente | text | sí | Nombre comercial del cliente |
| País | text | sí | Ej: México, Colombia, Argentina |
| Industria / subsector | text | no | Ej: Alimentos y bebidas, Cuidado personal, Distribuidora, etc. |
| Stakeholder principal | text | no | Ej: Director Comercial, CIO, VP de Operaciones |
| Brief del cliente (2-3 oraciones) | textarea | no | ¿Qué quiere el cliente? ¿Qué dolor lo trajo? |
| **Web del cliente** | url | **no** (recomendado) | https://www.ejemplo.com |
| Modelos operativos que le interesan | text | no | Si no sabes todavía, déjalo vacío |
| Idioma del deck | select | sí (default ES) | Español / Inglés |

## Patrón C — Selector de archivo de Drive

Úsalo para: elegir base comercial (Paso 1A.b) y elegir base delivery (Paso 1B.2).

**Layout:**
- Header con tipo de presentación, contador ("Encontré 7 presentaciones base en la carpeta comercial").
- Buscador full-width arriba si hay más de 12 ítems.
- Grilla `repeat(auto-fit, minmax(280px, 1fr))` con `gap: 16px`.

**Estructura de cada card de archivo:**
1. **Icono** según tipo (Slides / Doc / PDF).
2. **Nombre del archivo** bold, 15-16px, truncado a 2 líneas.
3. **Meta** en una línea gris: tipo · última modificación.
4. **Acciones:**
   - Botón secundario "Ver en Drive" → abre `webViewLink` en nueva pestaña.
   - Botón primario "Usar como base" → dispara la selección.

## Patrón D — Confirmación / resumen antes de ensamblar

Úsalo antes del Paso 5 (ensamblar prompt). Muestra al AE qué entrada va a tener el prompt para que pueda corregir antes de generarlo.

**Layout:**
- Card con secciones plegables (accordions): "Contexto del cliente", "Señales de conectores", "Señales de la web del cliente", "Pricing", "Base de partida".
- En cada sección, los datos en formato key-value, editables inline.
- Botón "Generar prompt" abajo a la derecha. Botón "Editar paso X" arriba de cada sección.

## Patrón E — Bloque de prompt final

El Paso 6 (entregar el prompt) **no es un widget** — es un bloque de código en el chat para que el AE haga copy/paste. Eso es deliberado: el flow de copy/paste con un click en el botón de copiar del bloque es más rápido que cualquier widget.

Acompañalo con una sola línea en chat: "Listo. Copia este prompt y pégalo en Claude Design — te va a generar el deck con la estructura completa, personalizado al cliente."

## Anti-patrones (no hacer)

- ❌ Listar opciones como bullets en el chat.
- ❌ Usar `AskUserQuestion` para opciones que ya están cubiertas por los patrones A-D.
- ❌ Hacer una pregunta por widget cuando son varios campos relacionados — un solo form por contexto.
- ❌ Mezclar patrones en un mismo widget (cards + form en el mismo render).
- ❌ Placeholders genéricos ("Ingrese el cliente") en vez de ejemplos concretos.
- ❌ Olvidar el helper text en campos opcionales — el AE no sabe si tiene que llenarlo.
- ❌ Cambiar el idioma del widget vs el de la conversación.
- ❌ Hacer el form muy largo (>8 campos) — partir en dos pasos si hace falta.

## Consistencia con el resto del catálogo ProContacto

Otros skills del catálogo (pc-delivery-project-pulse, pc-delivery-jira-project-auditor, pc-admin-interno-team-dailycheckin) usan `mcp__visualize__show_widget` con criterios parecidos. Si en algún momento ProContacto unifique los patrones en una librería compartida, este archivo se reemplazará por un link a ella.
