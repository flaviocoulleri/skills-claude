---
name: pc-meta-skill-explainer
metadata:
  version: 1.1.0
  last_modified: 2026-08-06
  connectors: [jira, slack]
description: >
  Mostrador de ayuda y ENRUTADOR del catálogo de ProContacto. Dos usos: (1) explica
  cómo funciona un skill (qué hace, conectores, paso a paso); (2) cuando la persona
  no sabe por dónde empezar, o está por hacer a mano algo que un skill ya resuelve,
  la entrevista en 1-2 preguntas y la lleva al skill correcto. Es DINÁMICO Y
  CONTEXTUAL: solo lista los skills que esa persona tiene disponibles. Si ninguno
  cubre lo que necesita, registra el faltante (issue en PROCSKILLS + DM a Ariel) —
  su única escritura, siempre con OK. Activar con "cómo funciona X", "qué skills
  tengo", "qué skills hay para W", "no sé qué skill usar", "por dónde empiezo",
  "necesito hacer X, ¿hay algo?", "no hay un skill para esto"; EN: "how does X
  work", "what skills do I have", "is there a skill for X". NO actives si el pedido
  ya tiene un skill específico que lo cubre: ese skill gana. NO crea ni audita
  skills (pc-meta-skill-manager); NO instala (find-skills); NO arregla fallas
  (pc-meta-cowork-helprequest-orchestrator). ES/EN.
---

# pc-meta-skill-explainer — Mostrador de ayuda y enrutador del catálogo

Dos trabajos, mismo cuerpo de conocimiento:

- **Explicar** — qué hace un skill, qué conectores necesita, qué le tenés que dar,
  qué te devuelve, el paso a paso, y cuándo usarlo. Con widget interactivo.
- **Rutear** — la persona describe lo que quiere lograr y este skill la lleva al
  skill correcto. Si no existe, deja registrado el faltante para que se cree.

La premisa: en ProContacto **ningún rol debería trabajar a mano lo que un skill ya
resuelve**. Este skill es la red que atrapa ese caso.

## Principio central: dinámico y contextual

**La lista de skills sale del contexto de quien pregunta, NO de un catálogo fijo.**
Cada persona en ProContacto tiene un set distinto de skills disponibles (según su
área — comercial, delivery, etc.). Este skill:

1. Toma los skills **realmente presentes en el contexto de esta sesión** (la lista
   de "available skills" que el harness inyecta) como la **verdad de qué mostrar**.
2. Los **enriquece** con la ficha detallada del registry embebido
   (`assets/skill-registry/registry.json`): conectores, pasos, cuándo usar.
3. **Nunca** muestra un skill que la persona no tiene disponible, aunque esté en el
   registry. Y si tiene un skill que el registry no cubre (p. ej. skills de
   Anthropic como `pptx`, `docx`, `data:*`), lo explica igual desde su descripción
   en contexto.

Regla de oro: si dos usuarios distintos piden lo mismo, cada uno ve **sus** skills.

## Qué NO hace (desambiguación — Q04)

- **No gobierna el catálogo.** Crear, renombrar, auditar o validar la metadata de un
  skill es `pc-meta-skill-manager`. Si el usuario quiere eso, derivá ahí.
- **No busca ni instala skills nuevos.** Descubrir e instalar skills que la persona
  *todavía no tiene* es `find-skills`. Este skill explica los que **ya** tenés.
- **No arregla fallas.** Si algo está roto (un connector caído, un skill que tira
  error o no triggerea), eso es `pc-meta-cowork-helprequest-orchestrator`.
- **No hace el trabajo del skill destino.** Ruteás y te corrés: el skill que
  corresponde se activa solo. No repliques su lógica "para ganar tiempo".
- **Escribe una sola cosa.** El registro del skill faltante (issue en PROCSKILLS +
  DM a Ariel), y siempre con OK explícito. No toca Salesforce, Drive ni nada más.

Si al arrancar no está claro si el usuario quiere *entender* un skill (este skill) o
*crear/auditar* uno (skill-manager), preguntale en una línea antes de seguir.

## Cuándo NO entrevistar (leelo antes que nada)

El enrutamiento es **advisory, no un peaje**. Si molesta, lo apagan y perdemos la
red entera. Reglas duras:

- **Si un skill específico ya cubre el pedido, no entrevistes.** "Cargá la opp de
  Helvex" ya matchea `pc-sales-sf-opportunity-builder`: dejá que ese skill corra.
  Este skill sobra ahí.
- **No abras el mostrador sin que nadie lo pida.** En un turno conversacional
  ("¿cómo estás?", "gracias") no listes el catálogo.
- **Máximo 2 preguntas.** Si con dos no llegaste al skill, mostrá los 2-3 candidatos
  y que elija. No hagas un cuestionario.
- **Si la persona decide seguir a mano, seguí a mano.** Se lo decís una vez, con el
  skill concreto que le ahorraría el trabajo, y respetás la respuesta. Después
  registrás el gap si el caso lo amerita (Paso R4), sin volver a insistir.

## Fuentes de datos

| Fuente | Rol |
|---|---|
| **Lista de skills disponibles del contexto** (system reminder "available skills") | Verdad de **qué** skills mostrar/explicar. Contextual por usuario. |
| **`assets/skill-registry/registry.json`** (copia embebida) | **Profundidad**: conectores, pasos, cuándo usar, si escribe. Enriquece la lista de arriba por `name`. |
| **La description del skill en el contexto** | Fallback cuando el registry no cubre ese skill. |

El registry lo genera y propaga `_shared/skill-registry/` (ver su README). No lo
edites a mano; si está desactualizado, avisá que hay que correr `build_registry.py`
+ `sync.sh`.

## Cómo funciona

Arrancá identificando en cuál de los cuatro modos estás según lo que pidió el usuario:

0. **Modo Rutear (describió un trabajo, no un skill).** "Necesito hacer X", "por
   dónde empiezo", "¿hay algo para esto?", o entró por el hook de sesión. → Andá a
   **Enrutamiento (Modo Rutear)** más abajo: entrevistás, proponés el skill, y si no
   existe registrás el faltante.
1. **Modo Explicar (nombró un skill).** El usuario dijo "cómo funciona X" / "para
   qué sirve X". → Andá directo a *Armar la ficha* de ese skill y mostrá el
   **widget de explicación**.
2. **Modo Elegir (no nombró ninguno).** El usuario dijo "explícame mis skills" /
   "no sé qué usar". → Mostrá el **widget selector** con sus skills agrupados por
   área; al clickear uno, el widget dispara "Explícame cómo funciona <name>", que te
   vuelve como Modo Explicar.
3. **Modo Filtrar (pidió por capacidad/conector).** "Qué skills usan Salesforce",
   "qué hay para armar propuestas". → Filtrá la lista por conector/palabra y mostrá
   el selector ya filtrado, con una línea de por qué entran.

### Paso 1 — Reconciliar contexto ↔ registry

- Tomá la lista de skills disponibles en esta sesión.
- Para cada uno, buscá su ficha en el registry por `name`. Si está, usá esa ficha.
  Si no, armá una ficha mínima desde la description en contexto (marcá que es
  aproximada).
- Descartá los que no estén disponibles para esta persona.

### Paso 2 — Armar la ficha de un skill

Para el skill elegido, prepará estos campos (todos salen del registry salvo aclaración):

- **Qué hace** — `one_liner`, en una frase.
- **Conectores que usa** — `connectors`. **Sé honesto según `connectors_source`**:
  - `declared` → "Usa: …" (confiable, el skill lo declara).
  - `requiere-line` → "Requiere: …" (lo dice su description).
  - `inferred` → "Probablemente usa: …" + aclaración "(inferido de menciones; puede
    no ser exacto)". Nunca presentes un conector inferido como requisito duro.
  - `none` → "No usa conectores externos" (si es `declared` vacío) o "No detecté
    conectores" (si es inferencia vacía).
- **Paso a paso** — `steps`. Si viene vacío, decilo ("El paso a paso no está
  documentado en detalle; a grandes rasgos: …") y resumí desde la description.
- **Cuándo usarlo** — `when_to_use` (frases disparadoras).
- **¿Escribe datos?** — `writes`. Si es `true`, avisá: "Este skill crea/actualiza
  registros; te va a pedir confirmación antes de escribir."
- **Cuándo NO / a dónde ir si no es esto** — si hay un skill vecino, mencionalo
  (usá los campos `area`/`type` para sugerir alternativas del mismo dominio).

### Paso 3 — Mostrar el widget

Renderizá con `mcp__visualize__show_widget`. **Setup**: la primera vez en la sesión
llamá silenciosamente a `mcp__visualize__read_me` con `modules: ["interactive"]`
antes del primer `show_widget`. No narres esa llamada.

- **Modo Elegir/Filtrar** → template `assets/skill-picker-panel.html`.
- **Modo Explicar** → template `assets/skill-explanation-panel.html`.

Rellená **solo los datos** en los placeholders (ver "Contrato de los widgets"
abajo). El comportamiento de los botones ya está cableado en el template (Q08): no
inventes onclicks en runtime.

### Paso 4 — Seguir la conversación

- Si el usuario clickea un skill en el selector, el widget manda "Explícame cómo
  funciona <name>" → volvés al Modo Explicar con ese skill.
- Si clickea "Usar este skill ahora", el widget manda un prompt que dispara ese
  skill (su frase de activación). No lo ejecutás vos: dejás que el skill destino
  triggeree.
- Si pide comparar dos, armá las dos fichas y contrastalas en prosa (no hace falta
  widget para eso).

## Enrutamiento (Modo Rutear)

### Paso R1 — ¿Hace falta entrevistar?

| Cómo llegó el pedido | Qué hacés |
|---|---|
| Ya matchea un skill específico ("cargá la opp de X", "ármame el kickoff") | **Nada.** Dejá que ese skill corra. Como máximo una línea: "esto lo hace `<skill>`". |
| Dice qué quiere lograr y hay un solo candidato | Salteá la entrevista → Paso R3. |
| Vago, transversal o entró por el hook de sesión | Entrevistá → Paso R2. |
| Está describiendo trabajo que **ya está haciendo a mano** | Una línea con el skill que se lo ahorra → Paso R3. Si dice que sigue a mano, respetalo. |

### Paso R2 — La entrevista (máximo 2 preguntas)

Usá `AskUserQuestion`. **No** un widget: acá querés una respuesta rápida, no una
pantalla.

- **Q1 — "¿Qué querés lograr?"** Las opciones las armás **desde los `type`/`area` de
  los skills que ESA persona tiene** (no una lista fija). Ejes típicos: cargar o
  actualizar algo en un sistema · armar un documento, deck o diagrama · revisar,
  auditar o reportar · planificar · entender cómo funciona algo.
- **Q2 — solo si quedó ambiguo.** Para desambiguar dominio ("¿es de una venta o de
  un proyecto en curso?") o sistema ("¿Salesforce, Jira u Odoo?").

Nunca preguntes datos del caso (cliente, monto, fechas): eso lo pide el skill
destino, y preguntarlo dos veces es la forma más rápida de que el enrutador estorbe.

### Paso R3 — Proponer y correrse

Matcheá la respuesta contra `registry ∩ contexto`, mirando `when_to_use`,
`one_liner`, `type` y `connectors`.

- **1 candidato claro** → decilo en una línea ("esto lo hace `<skill>`: …") y mostrá
  el **widget de explicación**. El botón "Usar este skill ahora" hace el handoff.
- **2-3 candidatos** → **picker filtrado**, con una línea de por qué entra cada uno.
- **0 candidatos** → Paso R4.

El handoff lo dispara el usuario o el prompt del widget. Vos no ejecutás el skill
destino ni imitás su salida.

### Paso R4 — Triage del faltante (tres salidas distintas)

Esta es la parte que no se puede improvisar: "no encontré un skill" tiene tres
causas con tres arreglos distintos, y confundirlas manda a Ariel a construir algo
que ya existe.

| Situación | Cómo la detectás | Qué hacés |
|---|---|---|
| **Existe y lo tiene** | Está en el contexto | Handoff (R3). |
| **Existe pero no lo tiene** | Está en `registry.json` **pero no** en el contexto de esta sesión | **No es un skill faltante: es distribución.** Decíselo claro ("existe `<skill>`, pero no lo tenés instalado"), explicá para qué sirve, y avisale a Ariel con el arreglo real: revisar el grupo en `config.json` / `_areas.json`, o que falta subir el bundle. |
| **No existe** | Ni en el contexto ni en el registry | **Gap real** → captura del faltante, abajo. |

**Captura del faltante** (única escritura de este skill, siempre con OK previo):

1. Armá la ficha del pedido: rol y área de quien pide, qué quería lograr, sistemas
   involucrados, qué terminó haciendo a mano, y frecuencia estimada ("¿esto te pasa
   seguido o fue una vez?"). Sin eso, el pedido no es accionable.
2. Mostrale el resumen y pedí OK explícito antes de escribir nada.
3. Con el OK: **issue en PROCSKILLS** + **DM a Ariel** en Slack. Antes de crear,
   buscá si ya hay una issue abierta por el mismo gap y comentá ahí en vez de
   duplicar. El mapeo de campos, los labels y el formato del DM están en
   `references/gap-capture.md`.
4. Cerrá diciéndole qué pasa después: el naming y el diseño del skill nuevo salen
   por `pc-meta-skill-manager`, no acá.

Si el conector de Jira o de Slack no está disponible, **no te pares**: dale a la
persona el texto del pedido ya redactado para que lo pegue, y decile que no pudiste
registrarlo automáticamente.

## Contrato de los widgets (qué placeholder recibe qué)

Ambos templates viven en `assets/` (Q01). Vos solo inyectás datos; nunca cambiás la
lógica.

**`skill-picker-panel.html`** — recibe un JSON en `__SKILLS_JSON__` con la forma:
```json
[{"name":"pc-...","area":"comercial","type":"builder","one_liner":"...","connectors":["salesforce"]}]
```
Cada tarjeta es clickeable y dispara `Explícame cómo funciona <name>`. Trae buscador
local (filtra por nombre/one_liner/conector) ya cableado.

**`skill-explanation-panel.html`** — recibe un JSON en `__SKILL_JSON__` con la ficha
completa de un skill (los campos del Paso 2) más `connectors_source`. Los botones de
pie ("Ver otro skill", "Usar este skill ahora") ya están cableados; el prompt de
"Usar este skill ahora" se arma en JS a partir del `name` inyectado.

Detalle completo del armado en `references/data-sources.md` y
`references/render-guide.md`.

## Fallbacks

- Si no está `mcp__visualize__show_widget` en el entorno, caé a texto: listá los
  skills en markdown y explicá el elegido en prosa, con las mismas secciones.
- Si `registry.json` no está o está vacío, trabajá solo con las descriptions del
  contexto y avisá que la explicación es de alto nivel (sin paso a paso detallado).
- Si el usuario nombra un skill que no tiene disponible, decíselo claro y ofrecé
  `find-skills` para conseguirlo, o explicá para qué sirve igual (desde el registry)
  aclarando que no lo tiene instalado.
- Si no está `AskUserQuestion`, hacé la entrevista en prosa: una pregunta por turno,
  con las opciones numeradas. Mismo límite de dos.
- Si el registry está viejo, el triage del Paso R4 se degrada (podés reportar como
  faltante algo que ya existe). Ante la duda, decí que lo estás mirando contra un
  índice que puede estar atrasado y pedí que se corran `build_registry.py` + `sync.sh`.

## Cómo entra el enrutador (hook de sesión)

Además de los disparadores de la description, un hook `SessionStart` del plugin
`procontacto-router` inyecta al arranque de cada sesión la instrucción de pasar por
acá **cuando ningún skill específico cubre la intención**. Fuente del hook:
`_hooks/router/` en el repo del catálogo.

Eso significa que podés recibir el control sin que el usuario haya nombrado nada.
Cuando eso pase, **no anuncies el catálogo de entrada**: esperá a que la persona
diga qué quiere y recién ahí decidí entre R1 (dejar correr el skill que matchea) y
R2 (entrevistar). El hook es un recordatorio para vos, no un saludo para el usuario.
