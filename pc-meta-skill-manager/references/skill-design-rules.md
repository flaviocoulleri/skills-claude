# Reglas de diseño de un buen skill ProContacto (Q01–Q11)

Estas son las reglas de **calidad de diseño / UX** que un buen skill ProContacto debe cumplir. Se aplican en dos momentos:

- **Al crear** un skill nuevo (Capacidad 1 del `pc-meta-skill-manager`): se buscan activamente, como parte del diseño.
- **Al auditar o mejorar** un skill existente (Capacidad 4): se revisan y se recomiendan.

Complementan a las reglas de `audit-checklist.md` (que cubren nombre, description, metadata, versión, taxonomía). Aquellas miran **cómo se llama y se cataloga** el skill; éstas miran **cómo está diseñado para operar**.

Cada regla tiene: **ID**, **severidad**, **cuándo aplica**, **qué exige**, **por qué**, y **cómo cumplirla**.

## Severidades y gates

| Severidad | Significado |
|---|---|
| `blocking` | Frena la publicación. En creación/mejora no se da por bueno el skill hasta resolverla. |
| `high` | Recomendación fuerte. Se señala siempre; el gestor decide, pero el default es cumplirla. |
| `medium` | Recomendación. Se sugiere; queda a criterio del gestor según el caso. |

Gates vigentes (decisión ProContacto): **Q02, Q06, Q07, Q08 y Q11 son `blocking`**. Q01 y Q05 son `high`. Q03 y Q04 son `medium`. Como toda regla del catálogo: el skill **propone, no impone** — pero las `blocking` no se saltean sin una decisión explícita y registrada del gestor.

Gate de idioma: **Q09 es `medium`** — el default del catálogo es español neutro, pero se respeta el override explícito (ver Q09).

Cuáles puede chequear el script (`audit_catalog.py`) en un barrido del catálogo: **Q01**, **Q06**, **Q07**, **Q08**, **Q09** y **Q11** (heurísticas, best-effort). Q02, Q03, Q04 y Q05 son de proceso/juicio y las evalúa Claude leyendo el skill. **Q08 tiene además una capa de proceso** — la prueba de humo de interactividad en runtime — que el script no reemplaza (ver Q08).

---

## Q01 · Template de output embebido en el skill

**Severidad**: high · **Auditable**: sí (heurística)

**Cuándo aplica**: a todo skill que produzca un artefacto estructurado como output — HTML, dashboard, widget, artifact, slide deck, documento.

**Regla**: si el skill genera HTML (u otro artefacto con layout fijo) como output, el **template debe vivir dentro del skill** (en `assets/`, p. ej. `assets/<output>-template.html`) con placeholders que el workflow rellena. El skill **no debe idear el HTML desde cero en cada ejecución**.

**Por qué**:
- **Consistencia**: todas las ejecuciones producen el mismo layout; no hay drift visual entre corridas.
- **Costo y latencia**: rellenar un template es mucho más barato (tokens/tiempo) que regenerar markup.
- **Revisabilidad**: tener el template como archivo es lo que habilita el repaso pantalla-por-pantalla de Q02. No se puede aprobar lo que se improvisa.
- **Mantenibilidad**: un cambio de marca/estilo se hace en un archivo, no en el prompt.

**Cómo cumplirla**:
1. Identifica cada output con layout del skill.
2. Crea un archivo template en `assets/` (`.html`, `.html.j2`, o equivalente) con placeholders claros (`{{titulo}}`, `{{filas}}`, …).
3. En el SKILL.md, el paso que genera el output **lee el template y lo rellena** — referencialo por path explícito.
4. Si hay datos dinámicos (tablas, listas), define el placeholder y el shape del dato, no el markup ad-hoc.

**Señal de violación que detecta el audit**: el SKILL.md indica que genera HTML/artifact/widget (`create_artifact`, `show_widget`, `mcp__visualize`, `.html`, "dashboard", "reporte HTML") pero **no hay ningún archivo de template** en `assets/`. Es heurística: puede haber falsos positivos (el template vive en otro lado) o negativos (genera HTML sin mencionarlo). El humano confirma.

---

## Q02 · Repaso pantalla-por-pantalla con aprobación del gestor

**Severidad**: blocking · **Auditable**: no (regla de proceso)

**Cuándo aplica**: al **crear o mejorar** un skill que tenga HTML / pantallas / templates visuales. Aplica a **cada** pantalla, por más chica que sea.

**Regla**: antes de dar por bueno el skill, hay que **recorrer una por una** todas las pantallas/templates que el skill produce o muestra a lo largo de sus pasos, presentárselas al **gestor (owner) del skill**, y obtener su **aprobación explícita por cada una**. Una pantalla = una aprobación. No se avanza con una pantalla sin OK.

**Por qué**: el output visual es la cara del skill ante el usuario final. Un cambio silencioso en una pantalla — un color, un campo que falta, un texto — rompe expectativas y pasa desapercibido en un diff. El repaso explícito es el control de calidad. Encaja con la filosofía bloqueante del `pc-meta-skill-manager`: nada se da por aprobado sin un "sí" puntual (ver la regla bloqueante del SKILL.md).

**Cómo cumplirla**:
1. **Enumerá** todas las pantallas/templates del skill (incluye estados: vacío, error, loading, confirmación — no sólo el "happy path").
2. **Identifica al gestor** del skill (regla T02 del audit: todo skill tiene owner declarado). Si no hay gestor declarado, primero hay que declararlo.
3. **Presenta cada pantalla** una a una — preview renderizado, screenshot, o el markup descrito — y pide OK puntual.
4. **Registra** las aprobaciones. Una autorización no es transitiva: aprobar la pantalla A no aprueba la B.
5. **No publiques** hasta tener todas las pantallas aprobadas.

**Nota**: esta regla es la contraparte de proceso de Q01. Q01 exige que el template **exista** como archivo; Q02 exige que ese template (y toda pantalla) sea **revisado y aprobado** por el gestor.

---

## Q03 · Pasos cortos y guiados

**Severidad**: medium · **Auditable**: no

**Cuándo aplica**: a todo skill conversacional/operativo (no a los `guide` de pura referencia).

**Regla**: el workflow del skill debe avanzar en **pasos cortos**, **guiando al usuario en todo momento**. Un objetivo por paso, confirmación antes de avanzar, sin volcar todo de golpe.

**Por qué**: los workflows con pasos largos o monolíticos pierden al usuario, acumulan errores y son difíciles de corregir a mitad de camino. Pasos cortos = el usuario mantiene el control y los errores se detectan temprano.

**Cómo cumplirla**:
- Estructurá el SKILL.md en **pasos numerados atómicos**.
- Cada paso dice: (a) qué se hace, (b) qué se le pide o muestra al usuario, (c) cuál es el criterio para avanzar al siguiente.
- Preferí preguntar y confirmar antes de ejecutar acciones con efecto (escrituras, envíos).
- Evita pedir 8 datos juntos: pide lo mínimo de cada paso.

---

## Q04 · Pregunta de desambiguación inicial cuando hay solapamiento

**Severidad**: medium (high si el solapamiento está confirmado por DUP01/DUP02) · **Auditable**: parcial

**Cuándo aplica**: a skills cuyos triggers o dominio se **parecen a los de otro skill** del catálogo.

**Regla**: si el skill se solapa con otro(s), debe **abrir con una pregunta de desambiguación** que confirme con el usuario que es el skill correcto y no otro. Ej.: *"¿Quieres X (esto) o Y (el otro skill)?"*

**Por qué**: cuando dos skills comparten frases disparadoras, el riesgo es que se active el equivocado y el usuario no se dé cuenta hasta el final. Una pregunta de una línea al inicio elimina ese riesgo. Se relaciona directamente con DUP01/DUP02 del `audit-checklist.md` (solapamiento de triggers).

**Cómo cumplirla**:
1. Corre el audit de duplicados (DUP01/DUP02) para detectar con qué skills se solapa.
2. Si hay solapamiento real, agrega al **inicio del workflow** una pregunta que distinga este skill del otro, nombrando ambos.
3. Si NO hay solapamiento, no hace falta la pregunta — no agregues fricción innecesaria.

---

## Q05 · Inputs claros y seleccionables (sobre todo desde conectores)

**Severidad**: high · **Auditable**: no

**Cuándo aplica**: a todo skill que reciba inputs del usuario — crítico cuando los datos vienen de **conectores** (Salesforce, Jira, Slack, Google, etc.).

**Regla**: los inputs deben ser **explícitos y seleccionables** por el usuario. Cuando la info viene de un conector, el skill debe **traer las opciones reales del conector y ofrecerlas para que el usuario elija** — nunca inventar, adivinar ni hardcodear valores.

**Por qué**: inputs ambiguos o inventados producen resultados incorrectos con apariencia de correctos. Esta regla codifica dos convenciones de ProContacto:
- **Valores reales del schema, no inventados**: p. ej. los valores de un picklist de Salesforce siempre se traen del schema real (`getObjectSchema`), nunca se inventan.
- **Queries canónicas, no improvisadas**: las consultas a conectores deben ser deterministas (a un archivo de referencia parametrizado del skill), no ideadas en runtime cada vez.

**Cómo cumplirla**:
1. Para cada input que venga de un conector: trae las opciones reales (schema / query canónica) y **preséntalas seleccionables** (lista, picker, opciones numeradas).
2. No hardcodees valores de picklists, IDs, nombres de campos: léelos del sistema.
3. Guarda las queries canónicas como referencia parametrizada del skill; no las redactes ad-hoc en cada corrida.
4. Valida la selección del usuario contra las opciones reales antes de usarla.

---

## Q06 · Referencias a otros skills validadas

**Severidad**: blocking (en creación/mejora) · high (en audit ex-post) · **Auditable**: sí (heurística)

**Cuándo aplica**: a todo skill cuyo SKILL.md mencione, derive a, o dependa de **otros skills** (p. ej. "usa `pc-crm-salesforce-field-creator`", "el output de `pc-cg-cloud-userstory-generator`").

**Regla**: toda referencia a otro skill debe **validarse contra el catálogo**: el skill referenciado tiene que **existir realmente** y con el nombre exacto vigente. No se publica un skill con referencias rotas.

**Por qué**: una referencia a un skill inexistente (o a un nombre viejo que ya fue renombrado) manda al usuario a la nada. Es especialmente frágil después de un rename (regla N02): el skill cambia de nombre y las referencias en otros skills quedan colgadas.

**Cómo cumplirla**:
1. Extrae todos los nombres `pc-…` que el SKILL.md referencia como skills.
2. Verifica que cada uno **exista** en el catálogo (directorio presente / entrada en `catalog.json`).
3. Para los que no existan: ¿es un typo? ¿un nombre viejo post-rename? ¿un skill que aún no se creó? Corregí la referencia al nombre vigente, o quita la referencia.

**Señal de violación que detecta el audit**: nombres `pc-…` estructuralmente válidos referenciados en el SKILL.md (fuera de bloques de código de ejemplo) que **no** corresponden a ningún skill escaneado. Es heurística: si el audit corre sobre un subconjunto del catálogo, un skill referenciado podría vivir en otro directorio — por eso en el audit ex-post es `high` y se verifica a mano, mientras que en creación/mejora es `blocking`.

---

## Q07 · Contrato de escritura para skills que crean/actualizan registros

**Severidad**: blocking (en creación/mejora) · high (en audit ex-post) · **Auditable**: sí (heurística)

**Cuándo aplica**: a todo skill que **cree o actualice registros en sistemas externos** (Salesforce, Odoo, Jira, etc.) — cualquier skill con `createSobjectRecord` / `updateSobjectRecord` / equivalente.

**Regla**: el skill debe declarar un **mapa de escritura** por objeto y aplicar el **contrato de escritura** (gate pre-write + verificación post-write). En concreto:

1. **Mapa de escritura declarado.** Para cada objeto que el skill escribe, documentar (en el SKILL.md o un reference): los **campos** que toca, marcando por cada uno su **rol** (dato simple / picklist / lookup), y si es **obligatorio**. Los obligatorios son la unión de:
   - **técnicos** — del schema (`getObjectSchema`: `createable=true`, `nillable=false`, sin `defaultValue`), y
   - **de negocio** — los que el skill exige aunque el schema los marque opcionales (ej. `Opportunity.Amount`). Este es el caso que se escapa y crea registros inútiles.
2. **Valores y API names SIEMPRE a runtime, nunca hardcodeados.** Los valores de picklist y los API names reales se resuelven en ejecución con `getObjectSchema` y se cachean en `orgMeta`. El mapa puede listar valores **orientativos** por campo, pero **marcados como no contractuales** ("mandan los del schema") — nunca como fuente de verdad. (Esto es la cara "de escritura" de Q05.)
3. **Gate pre-write (bloqueante).** Antes de cada create/update: validar el payload campo por campo — todo obligatorio presente y no vacío (`null`/`''`/lista vacía = inválido), numéricos de negocio `> 0` (salvo cero aprobado), lookups a Ids existentes, picklists con valores reales. Si algo falta → **no escribir**; pedir el dato faltante. Prohibido crear registros parciales.
4. **Verificación post-write (bloqueante).** Tras el create, re-query del registro para confirmar que los obligatorios persistieron (una validation rule o FLS puede dropear un campo en silencio). Si no persistió → no dar por exitoso; corregir o escalar.

**Por qué**: un skill que escribe sin este contrato crea **registros incompletos con apariencia de correctos** — el caso real que lo motivó: una Opportunity Partner Fee creada sin `Amount`. Declarar el mapa obliga al autor a pensar los obligatorios (técnicos + de negocio) de entrada; el gate los hace cumplir; la verificación caza los drops silenciosos. Mantener los valores a runtime evita el drift que rompe los picklists (otro bug real: `Asset_Type__c` y tipos de fee inexistentes). La eficiencia real la da cachear el schema en `orgMeta` una vez por sesión; el mapa suma **consistencia y auditabilidad**.

**Cómo cumplirla**:
1. Lista los objetos que el skill escribe y, por cada uno, su mapa de campos (rol + obligatoriedad técnica/negocio).
2. Asegurate de que API names y valores de picklist se resuelvan con `getObjectSchema` (cacheado en `orgMeta`), no hardcodeados.
3. Implementa el gate pre-write y la verificación post-write como pasos explícitos del workflow.
4. Modelo de referencia: `pc-sales-sf-quote-builder` (Paso 16.5 pre-write + Paso 17.5 re-query/integridad) y la regla "Contrato de escritura" de `common-rules.md` (§ 4-bis) de los skills comerciales.

**Señal de violación que detecta el audit**: el SKILL.md usa `createSobjectRecord` / `updateSobjectRecord` (u otra escritura a sistema externo) pero **no documenta un mapa de escritura** ni menciona gate de obligatorios / verificación post-write, **o** hardcodea valores de picklist / API names en vez de resolverlos con `getObjectSchema`. Heurística: el humano confirma.

---

## Q08 · Interactividad cableada y probada en runtime

**Severidad**: blocking · **Auditable**: sí (heurística estática) + proceso (prueba de humo en runtime)

**Cuándo aplica**: a todo skill cuyo output HTML (template de `assets/` para `show_widget`, artefacto, dashboard) tenga **controles interactivos** — botones, links de acción, pills/tabs, checkboxes que disparan acciones masivas, ítems de menú kebab, cualquier elemento clickeable. Es la contraparte de comportamiento de Q01: Q01 exige que el **markup** viva en el template; Q08 exige que el **cableado de cada acción** también viva ahí, resuelto y probado — no improvisado en runtime.

**Regla**: **cada control interactivo del template debe resolver a una acción real, determinista y auto-contenida en el archivo commiteado.** En concreto:

1. **Todo actionable tiene handler cableado en el template.** Cada botón/link/pill/menú resuelve a exactamente una de estas tres cosas, escrita en el propio HTML: (a) `window.sendPrompt("...")` con el **prompt completo horneado** (para widgets de `show_widget`), (b) un `href` real y no vacío (para navegación), o (c) un handler JS local definido en el mismo archivo (listener directo o por *event delegation* con `closest(selector)`). Ningún control puede quedar "pendiente de que Claude le agregue el onclick en runtime".
2. **El comportamiento NO va en placeholders.** Los `{{placeholders}}` / `__TOKENS__` sólo inyectan **datos** (textos, filas, contadores, IDs). La **lógica de la acción** (qué prompt se manda, qué DOM cambia, a dónde navega) está escrita fija en el template. Un `onclick="__ACTION__"` o un cuerpo de listener con un placeholder = violación: eso es justamente lo que se improvisa distinto en cada corrida.
3. **Sin handlers huérfanos ni IDs colgados.** Todo `getElementById('x')` / `querySelector('.y')` / `data-act="z"` referenciado por el JS tiene su elemento correspondiente en el markup, y viceversa: no hay botones sin listener ni listeners hacia elementos que no existen.
4. **Determinismo.** El mismo estado de datos produce el mismo set de controles y las mismas acciones en cada render. Nada de comportamiento que dependa del orden en que Claude "arme" cosas a runtime.
5. **`sendPrompt` usado con guarda.** Si el template llama `window.sendPrompt`, lo hace defensivamente (existe en el host de `show_widget`; para artefactos u otros hosts puede no existir). Un control cuya única acción es `sendPrompt` en un contexto donde no está disponible es un botón muerto.

**Prueba de humo de interactividad (gate de proceso, obligatorio al crear/modificar el HTML).** La parte estática de arriba se chequea barato con el script, pero **no** garantiza que el botón funcione al clickearlo — que es la falla real. Por eso, antes de dar por bueno un template con controles, hay que **ejercitarlo renderizado**:

1. Renderiza el HTML (dev server + preview tools, o el harness del host).
2. Stubea `window.sendPrompt` para capturar sus llamadas (`window.sendPrompt = (t)=>{ window.__calls.push(t); }`).
3. **Clickea cada control una por una** y confirma que produce un efecto observable: una llamada a `sendPrompt` con el prompt esperado, un cambio visible en el DOM, o una navegación. Revisa también la consola: cero errores de JS al cargar y al clickear.
4. Un control que al click no dispara nada, tira `ReferenceError`/`is not a function`, o se comporta distinto entre clicks → **no pasa**. Se corrige en el template y se re-prueba.

**Por qué**: es el bug recurrente que motivó la regla — botones que aparecen pero al clickearlos no hacen nada, o que "cada ejecución se comportan distinto". La causa raíz es dejar el cableado de la acción pendiente de crearse en runtime en vez de hornearlo en el template. Los datos cambian por corrida (por eso van en placeholders); **el comportamiento no debería cambiar nunca** (por eso va fijo y probado). Encaja con Q01 (consistencia/revisabilidad del output) y con la filosofía bloqueante del skill: nada se da por bueno sin verificación explícita.

**Cómo cumplirla**:
1. Por cada actionable del template, escribe su handler completo en el archivo (sendPrompt con prompt horneado / href real / listener local). Preferí *event delegation* para listas dinámicas (`document.addEventListener("click", e => { const b = e.target.closest("[data-act]"); ... })`), así los controles de filas renderadas a runtime ya nacen cableados.
2. Mantén los placeholders limitados a datos. Si necesitas variar el prompt por fila, constrúyelo en JS a partir de los datos inyectados — no metas el prompt en un placeholder de comportamiento.
3. Corre la prueba de humo de interactividad (arriba) y regístrala junto con el repaso pantalla-por-pantalla de Q02: Q02 aprueba **cómo se ve**, Q08 aprueba **que responde**.
4. Modelo de referencia: `pc-sales-sf-contract-activator` (`assets/contract-activator-panel.html`) — botones y menús kebab cableados por delegación con `sendPrompt` de prompt completo; y este mismo skill, `assets/catalog-viewer-template.html` (filtros/orden cableados por listener local).

**Señal de violación que detecta el audit (estática)**: en un template de `assets/`, un elemento clickeable (`<button>`, `[data-act]`, `[role=button]`, `.pill`, `<a>` sin `href`) sin ninguna señal de cableado (ni `onclick`, ni un listener que lo alcance por id/clase/data-attr o por delegación, ni `sendPrompt`); **o** un `onclick`/cuerpo de handler que contiene un placeholder `{{…}}`/`__…__` (comportamiento diferido a runtime); **o** un `sendPrompt` usado sin que el archivo lo referencie de forma consistente. Es heurística — la delegación de eventos hace imposible el análisis exacto, así que el script reporta **candidatos a botón muerto** y el humano confirma corriendo la prueba de humo.

---

## Q09 · Español neutro por defecto

**Severidad**: `medium` · **Chequeable por script**: sí (heurística `check_default_dialect`).

**Cuándo aplica**: a todo texto que produce un skill — su `description`, la prosa de instrucciones, y sobre todo **lo que le habla al usuario** (mensajes, HTML de `show_widget`/artefactos, plantillas, drafts). No aplica a nombres de API, campos, código ni identificadores.

**Qué exige**: el registro por defecto del catálogo es **español neutro** — tuteo (`usa`, `arma`, `tienes`, `puedes`, `tú`), sin voseo rioplatense (`usá`, `armá`, `tenés`, `podés`, `vos`) ni mexicanismos fuertes. Neutro = entendible en cualquier país hispanohablante, sin marca regional.

**Override (parte de la regla, no excepción)**: si el usuario pide el resultado en otro dialecto, o el skill produce salida para un cliente cuyo país tiene otro registro, **se respeta ese dialecto**. Esto engancha con:
- La regla cliente-facing de presentaciones/`brand-applier`: adaptar idioma **y dialecto** al país del cliente (voseo/tuteo/usted), documentada en `_shared/presentation-builder/…` — esas líneas hablan *de* dialecto y el detector no las cuenta.
- Skills con registro propio declarado a propósito (interno, agentes que hablan el dialecto del interlocutor): basta que lo digan en una línea que mencione el dialecto.

**Por qué**: consistencia de voz del catálogo. La casa históricamente escribía en voseo; se estandariza a neutro para que ningún entregable quede marcado regionalmente salvo intención explícita. El default vive acá; el dialecto se elige, no se hereda del autor.

**Cómo cumplir**: escribir en tuteo neutro. Para neutralizar voseo existente hay tooling: `scripts/neutralize_voseo.py` (fixer) sobre el mapa curado `scripts/voseo_map.py` — **fuente única** que comparten fixer y detector. El mapa es explícito token→token (cero falsos positivos: no toca futuros del tuteo como `confirmarás`, ni pretéritos como `encontré`, ni topónimos como `Panamá`). Correr `--apply` es idempotente; el detector `check_default_dialect` marca lo que sobrevive para revisión.

**Señal de violación que detecta el audit (estática)**: formas de voseo del mapa curado en la `description` o la prosa del `SKILL.md`, fuera de líneas que hablen *de* dialecto (`voseo`/`rioplatense`/`tuteo`) o de plantillas de mensaje en 1ª persona (pretérito, no imperativo). Es heurística best-effort: reporta candidatos y el humano confirma.

---

## Q10 · ⏸ RESERVADO — ficha auto-explicable (`metadata.connectors` + `## Cómo funciona`)

**Estado**: número **tomado pero sin spec escrita**. No reusar.

`_shared/skill-registry/` y `pc-meta-skill-explainer` ya citan un "Q10" que exige que el skill **declare `metadata.connectors`** en el frontmatter y traiga una sección **`## Cómo funciona`**: es lo que hace que `build_registry.py` marque la ficha como `help_quality: "rich"` en vez de armarla por inferencia. Las referencias están en `_shared/skill-registry/README.md`, `schema.json`, `build_registry.py` y `pc-meta-skill-explainer/references/data-sources.md` — pero la regla **nunca se escribió acá**, así que hoy el número está reclamado y vacío.

**Qué hacer con esto**: escribir la spec en este slot (severidad, señal de violación, fix) o, si se decide que no va a ser una regla, limpiar las cuatro referencias. Mientras siga así, **Q10 no se usa para otra regla** — reusarlo dejaría dos reglas distintas con el mismo ID en documentos que ya circulan.

---

## Q11 · El entregable HTML va al gestor (política de publicación citada + propagada)

**Severidad**: `blocking` · **Chequeable por script**: sí (heurística `check_artifact_publish`).

**Cuándo aplica**: a todo skill que produzca un **entregable** HTML — algo que otra persona va a volver a abrir, compartir o corregir más adelante: propuesta, SOW, documento, informe, wireframes, diagrama, deck, backlog, diccionario de datos.

**Cuándo NO aplica (parte de la regla, no excepción)**: a las **pantallas de trabajo del chat**, que van por `mcp__visualize__show_widget` y no se publican en ningún lado. Son dos casos:

1. **Widgets de interacción** del propio flujo — elegir carpeta, confirmar una escritura, ofrecer exportar.
2. **Paneles, tableros y visores que el skill declara explícitamente que van por `mcp__visualize__show_widget`.** Cuando un skill lo dice —por ejemplo `pc-sales-sf-contract-signature-orchestrator`: *"Panel via `mcp__visualize__show_widget` (nunca `create_artifact`)"*— **esa declaración manda** y Q11 no se le aplica. Modelos vigentes: `pc-sales-sf-forecast-reviewer`, `pc-sales-sf-commit-pipeline`, `pc-legal-sf-contract-validator`.

> **La prueba que los separa: ¿cuánto vive?** Una vista del estado de HOY, para que alguien decida algo ahora, se muere con la conversación y versionarla no significa nada → pantalla de trabajo. Algo que sobrevive a la conversación → entregable. Al crear el skill, esta decisión **se escribe** en el SKILL.md: un skill que no dice a dónde va su output deja la decisión librada a cada corrida, que es exactamente el bug.

**Qué exige** (las dos mitades, no una):

1. **Citar el módulo canónico.** El SKILL.md tiene una sección de publicación que remite a `_shared/artifact-publish/artifact-publish.md` y aplica su procedimiento de dos pasos (`listar_artefactos` por título canónico → `publicar_version` si ya existía, `publicar_artefacto` si no). **No se copia la política**: se cita. El texto vive en un solo lugar.
2. **Sumarse al `TARGETS` de su `sync.sh`.** Agregar la línea `"<área>/<skill>"` al array `TARGETS` de `_shared/artifact-publish/sync.sh` y correrlo. Sin esto el módulo **no viaja dentro del bundle `.skill`**, y como cada skill se deploya como zip aislado, el SKILL.md termina citando un archivo que en la máquina del usuario no existe.

**Por qué las dos**: son dos formas distintas de la misma falla silenciosa.

- Sin la cita, el módulo viaja pero **nadie lo lee** — que es justo lo que pasó entre que se escribió la política y el commit que la cableó: `_shared/artifact-publish/` estaba dentro de 8 bundles y ningún `SKILL.md` la invocaba. Una regla que no se lee no es una regla.
- Sin el `TARGETS`, la cita apunta al vacío. El repo se ve bien y el bundle deployado está incompleto; el desfase no falla ruidosamente, falla callado.

Y el costo de que falle es el que la política entera intenta evitar: el entregable sale como artefacto de la conversación, sin versionado ni trazabilidad, o se republica de cero y el link que el cliente ya tiene queda viejo sin que nadie se entere.

**Cómo cumplirla**:

1. Decide y **escribe** si el output es entregable o pantalla de trabajo. Si es pantalla, decláralo con la fórmula explícita (`… via mcp__visualize__show_widget`) y terminaste: Q11 no aplica.
2. Si es entregable, agrega al SKILL.md la sección de publicación **antes** del gate de vinculación, citando el módulo. Modelo: `pc-crm-userstory-generator` (sección "Publicación en el gestor (antes de vincular)").
3. Agrega `"<área>/<skill>"` al `TARGETS` de `_shared/artifact-publish/sync.sh` y **corre el script**. Verifica que quedó `<área>/<skill>/_shared/artifact-publish/artifact-publish.md` y que el `.skill` se regeneró.
4. Si el skill además deja el entregable vinculado (lo habitual), haz lo mismo con `_shared/artifact-linkage/sync.sh`.
5. **El caso ad-hoc ya tiene dueño**: si lo que vas a escribir es "y si el HTML lo armó una conversación cualquiera", eso es `pc-meta-artifact-publisher` + el hook de `SessionStart` del grupo `router`. No lo re-implementes.

**Señal de violación que detecta el audit (estática)**: el SKILL.md muestra señales de producir un entregable HTML (salida HTML + vocabulario de entregable), **no** declara que su output va por `mcp__visualize__show_widget`, y le falta alguna de las dos mitades — no menciona `_shared/artifact-publish` en su prosa, o lo menciona pero la carpeta `_shared/artifact-publish/` no está físicamente dentro del skill (no está en `TARGETS`, o el `sync.sh` no se corrió). Es heurística: un visor interno cuyo output nadie comparte puede aparecer como candidato. El humano confirma con la prueba de arriba (¿cuánto vive?) y, si es pantalla de trabajo, lo resuelve **declarándolo en el SKILL.md** — que es la corrección correcta, no una excepción al chequeo.

---

## Resumen para el flujo de creación / mejora

Al crear o mejorar un skill, recorre esta lista:

- [ ] **Q01** — ¿Genera HTML/artefacto? → el template está en `assets/`, no se improvisa. *(high)*
- [ ] **Q02** — ¿Tiene pantallas? → repasadas una por una y **aprobadas por el gestor**. *(blocking)*
- [ ] **Q03** — ¿El workflow avanza en pasos cortos y guiados? *(medium)*
- [ ] **Q04** — ¿Se parece a otro skill? → pregunta de desambiguación al inicio. *(medium / high)*
- [ ] **Q05** — ¿Los inputs son claros y seleccionables, con valores reales del conector? *(high)*
- [ ] **Q06** — ¿Las referencias a otros skills existen y están bien nombradas? *(blocking)*
- [ ] **Q07** — ¿Crea/actualiza registros? → mapa de escritura declarado (obligatorios técnicos + de negocio), valores a runtime (no hardcode), gate pre-write + verificación post-write. *(blocking)*
- [ ] **Q08** — ¿El HTML tiene botones/controles? → cada uno cableado a una acción real en el template (sendPrompt/href/listener), comportamiento no en placeholders, y **probado clickeándolo renderizado** (prueba de humo de interactividad). *(blocking)*
- [ ] **Q09** — ¿El texto/salida está en español neutro (tuteo)? → sin voseo rioplatense, salvo override explícito por dialecto del cliente o registro propio declarado. *(medium)*
- [ ] **Q11** — ¿Produce un entregable HTML? → el SKILL.md **cita** `_shared/artifact-publish/` (no copia la política) y el skill está en el `TARGETS` de su `sync.sh`, con el módulo ya dentro de su carpeta. Si el output es una pantalla de trabajo, **queda declarado** que va por `mcp__visualize__show_widget` y Q11 no aplica. *(blocking)*
