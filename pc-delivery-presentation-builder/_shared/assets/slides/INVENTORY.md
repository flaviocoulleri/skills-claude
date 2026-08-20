# Inventario de slides estandarizados

> **Qué es esto.** El registro de qué slides ya tienen un **template HTML estandarizado** (anclado al Design System oficial de ProContacto) y cuáles todavía no. Es la fuente de verdad de la coexistencia: el skill consulta este inventario en el Paso 5 para decidir, slide por slide, si embebe el template del kit o cae al modo actual.

## Cómo lo usa el skill (coexistencia)

Por cada slide de la estructura del deck (definida por el template del Record Type o la base de Drive):

1. **¿Está estandarizado acá (estado ✅)?** → el skill embebe en el prompt el `_kit.css` (una sola vez) + el markup del slide (región `EMBED`) con la instrucción: *"clona este componente y rellena los slots con el contenido de abajo; NO cambies layout, colores, tipografía ni logos."*
2. **¿No está (estado ⬜)?** → **fallback**: el skill describe el slide como hasta ahora (intención del template + principios de `deck-craft.md`) y Claude Design lo compone.

Así la homogeneidad crece a medida que estandarizamos, y el skill **siempre funciona** — nunca se bloquea por un slide no estandarizado. Se puede **deployar en cualquier momento** con lo que haya en ✅.

## Estado

| # | Slide | Archivo | Estado | Aplica a | Slots |
|---|---|---|---|---|---|
| ① | Portada | `cover.html` | ✅ Estandarizado | Todas | KICKER, TITULO, CLIENTE, SUBTITULO, FECHA, CONFIDENCIAL |
| ② | Divisor de sección | `section-divider.html` | ✅ Estandarizado | Todas | NN, ETIQUETA, TITULO_SECCION |
| ③ | Cierre / Próximos pasos | `closing.html` | ✅ Estandarizado | Todas | PASO_1..3, CONTACTO |
| ④ | Quiénes somos / Pilares | `about-pillars.html` | ⬜ Pendiente | Comercial (casi todas) | — |
| ⑤ | Agenda | `agenda.html` | ⬜ Pendiente | Todas | — |
| ⑥ | Qué problemas vemos (dolor→KPI) | `problem.html` | ⬜ Pendiente | Comercial | — |
| ⑦ | Alcance / módulos | `scope.html` | ⬜ Pendiente | Project, Quickstart, Integration | — |
| ⑧ | Inversión (tabla) | `pricing.html` | ⬜ Pendiente | Comercial | — |
| ⑨ | Entregables | `deliverables.html` | ⬜ Pendiente | Casi todas | — |
| ⑩ | Equipo / roles | `team.html` | ⬜ Pendiente | Support, Outsourcing, Assessment | — |
| ⑪ | Cronograma / Timeline | `timeline.html` | ⬜ Pendiente | Project, POC, Integration | — |
| ⑫ | Fuera de alcance | `out-of-scope.html` | ⬜ Pendiente | Casi todas | — |

**Progreso: 3 / 12 estandarizados.**

> Slides muy específicos por tipo (SLAs de Support, customer journey de Marketing, arquitectura de Integration, hipótesis de POC) quedan en fallback hasta una etapa posterior — son menos repetidos entre decks.

## Reglas del kit

- **Anclado al DS oficial.** Tokens y clases salen de `_kit.css` (sincronizado de `colors_and_type.css` del Manual de Marca 2026, export 2026-06-15). No inventar colores, tipografía ni espaciados fuera de los tokens.
- **Logos siempre inline desde `logos/`** (copiados del DS). Nunca recrearlos con texto/CSS ni `<img src>`.
- **Una idea por slide**, headline que afirma, contraste ExtraBold/Light. (Ver `../../references/deck-craft.md`.)
- **El contenido de ejemplo** en cada archivo (cliente ficticio "Tiendas del Sol") es sólo para previsualizar; los slots se rellenan con datos reales del cliente/proyecto.
- **Slogan "Aliados en tu transformación"** sólo como remate (cierre), nunca de apertura.

## Cómo agregar un slide al kit (checklist)

1. Crear `assets/slides/<slide>.html` con la región `<!-- EMBED:START -->…<!-- EMBED:END -->`, usando clases de `_kit.css` y logos inline de `logos/`.
2. Marcar los slots con comentarios `<!--{{SLOT}}-->` + contenido de ejemplo realista.
3. Verificar que renderiza solo (abrir en el preview).
4. Actualizar la fila correspondiente en la tabla de arriba a ✅ y completar Slots.
5. Mapear el slide en `../references/slide-kit.md` (qué template/Record Type lo usa).
6. Commit + deploy.

## Versión del Design System

- Fuente: `ProContacto Design System` export **2026-06-15** (canvas `#0B0C0E`, azul `#0062FF`, violeta `#8F7AFF`, Open Sans 300/800).
- Si el DS se actualiza, re-sincronizar el bloque `:root` + clases base de `_kit.css` y revisar los slides.
