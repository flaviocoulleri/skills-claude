# Audit Checklist — Qué revisa el audit

Este archivo lista **todas las reglas** que `scripts/audit_catalog.py` aplica sobre el catálogo. Cada regla tiene:

- **ID**: identificador estable (útil para Jira labels)
- **Tipo**: `naming`, `duplicate`, `description`, `metadata`, `taxonomy`, `design`
- **Severidad**: `blocking`, `high`, `medium`, `low`
- **Qué revisa**
- **Cómo arreglarlo**

El humano que reciba el reporte de audit puede decidir no arreglar algunos hallazgos (ej: un rename de un skill legacy en producción). El audit propone; no impone.

---

## NAMING — Reglas de nombres

### N00 · Bloqueante en creación · El nombre valida estrictamente

**Severidad**: blocking (más fuerte que `high` — no hay forma de mergear sin pasarla)

**Cuándo aplica**: al crear un skill nuevo. No al auditar ex-post.

**Regla**: el nombre propuesto debe pasar `scripts/validate_name.py` con exit code 0. Esto exige simultáneamente:

- Parseo correcto bajo `pc-[área]-[sistema?]-[objeto]-[acción]`.
- Cada slot contra sus valores permitidos (`VALID_AREAS`, `VALID_SYSTEMS`, `VALID_ACTIONS`).
- Respeto de `AREAS_OMIT_SYSTEM` (no incluir sistema cuando el área lo prohíbe).
- Ningún token del blocklist (`tool`, `helper`, `utility`, `pro`, `v2`, etc.).
- No colisión con un skill existente.

**Por qué bloqueante**: renombrar post-creación rompe triggers cacheados, docs, y memoria de Claude. El costo de prevenir es una validación de 50ms; el costo de corregir puede ser semanas de coordinación.

**Fix**: corregir el nombre al formato válido antes de crear cualquier archivo del skill.

**Diferencia con N01-N05**: las reglas N01-N05 son del audit ex-post sobre skills ya existentes — ahí toleramos deuda legacy con severidad high/medium. N00 es sólo para creación; ahí no se tolera nada.

---

### N01 · El `name` en frontmatter coincide con el directorio

**Severidad**: high

**Regla**: el campo `name` del YAML frontmatter debe ser exactamente igual al nombre del directorio.

**Por qué**: si divergen, se rompen los paths al cargar references/scripts.

**Ejemplo de violación**: directorio `sf-field-creator-pro/` con `name: SF Field Creator Pro` en frontmatter.

**Fix**: alinear ambos a kebab-case.

---

### N02 · El nombre sigue la fórmula `pc-[área]-[sistema?]-[objeto]-[acción]`

**Severidad**: high (para falta de `pc-` o de área/acción); medium (para violaciones de slot)

**Regla**: el nombre debe:

1. Empezar con `pc-` (prefijo obligatorio para skills propios de ProContacto).
2. Continuar con una **área** válida (ver `naming-convention.md`, tabla de áreas).
3. Opcionalmente incluir un **sistema** (de la lista `VALID_SYSTEMS`). Se OMITE cuando el área está en `AREAS_OMIT_SYSTEM` (cg-cloud, data-cloud, marketing-cloud, admin-interno, meta).
4. Incluir un **objeto** (la entidad sobre la que opera).
5. Terminar con una **acción** única, de `VALID_ACTIONS`.

**Por qué**: consistencia → descubribilidad. La fórmula unifica todos los skills ProContacto y permite filtrar por área/sistema/acción desde el nombre.

**Ejemplos de violación**:
- `procontacto-brand` → falta prefijo `pc-` y acción (debería ser `pc-admin-interno-brand-applier`).
- `adr-generator` → falta prefijo y área (debería ser `pc-admin-interno-adr-generator`).
- `sf-field-creator-pro` → prefijo viejo (`sf-` en lugar de `pc-crm-salesforce-`), y contiene `pro` (blocklist).
- `pc-cg-cloud-salesforce-account-creator` → `cg-cloud` está en `AREAS_OMIT_SYSTEM`, no lleva sistema (correcto: `pc-cg-cloud-account-creator`).

**Fix**: renombrar según la tabla de propuestas en `naming-convention.md`. Ojo: renombrar tiene costo — si el skill es `stable` y muy usado, coordinar con el owner y avisar a los usuarios cuya memoria caché de triggers dependa del nombre viejo.

---

### N03 · Slots consistentes con el área

**Severidad**: medium

**Regla**:
- Si el área está en `AREAS_OMIT_SYSTEM`, el slot de sistema debe estar ausente.
- Si el área NO está en `AREAS_OMIT_SYSTEM`, el sistema es obligatorio salvo que el skill no tenga sistema externo (raro en áreas de producto).
- El slot de objeto no puede estar vacío.

**Ejemplos de violación**:
- `pc-meta-jira-skill-manager` → el área `meta` está en `AREAS_OMIT_SYSTEM`, sobra el `jira-`.
- `pc-crm-user-creator` → el área `crm` NO implica Salesforce (podría ser otro CRM), falta sistema explícito.

**Fix**: quitar el slot de sistema si es redundante; agregarlo si es obligatorio.

---

### N04 · Sin palabras de la blocklist

**Severidad**: medium

**Regla**: el nombre no debe contener `tool`, `helper`, `utility`, `assistant`, `smart`, `ai`, `pro`, `v2`, `new`, `my`, `custom`.

**Por qué**: son genéricas, no aportan información taxonómica.

---

### N05 · Una sola acción al final

**Severidad**: medium

**Regla**: el último token debe ser un único verbo de `VALID_ACTIONS`. No concatenar dos verbos (`creator-updater`, `builder-applier`).

**Fix**: si el skill hace múltiples operaciones sobre el mismo objeto, reemplazar por una acción paraguas: `manager`, `workflow`, u `orchestrator`.

---

## DESCRIPTION — Reglas de description

### D01 · Description ≥ 300 caracteres

**Severidad**: high

**Regla**: la description debe tener al menos 300 caracteres.

**Por qué**: descriptions cortas no triggerean. Claude necesita señal suficiente para decidir si el skill aplica.

**Fix**: expandir con frases disparadoras y contexto de uso.

---

### D02 · Incluye ≥ 5 frases disparadoras entre comillas

**Severidad**: medium

**Regla**: contar ocurrencias de texto entre comillas dobles o simples en la description. Deben ser ≥ 5.

**Por qué**: las frases disparadoras son lo que mejor matchea intenciones reales de usuario.

**Fix**: agregar al menos 5 frases literales que un usuario diría.

---

### D03 · Empieza con verbo activo

**Severidad**: low

**Regla**: la primera palabra (ignorando artículos) debe ser un verbo en presente: `Crea`, `Genera`, `Audita`, `Aplica`, `Permite`, `Guía`, etc.

**Por qué**: facilita el escaneo humano y la comprensión del modelo.

---

### D04 · Declara idioma si es bilingüe o EN

**Severidad**: low

**Regla**: si el skill funciona en ambos idiomas, debe terminar con "Funciona en español e inglés" (o equivalente).

---

## DUPLICATE — Solapamientos

### DUP01 · Solapamiento de triggers

**Severidad**: medium

**Regla**: si dos skills comparten ≥ 3 frases disparadoras literales, o sus descriptions tienen ≥ 70% de similaridad, marcar como posible duplicado.

**Fix**: el humano decide. Opciones: (a) merge, (b) afinar una description para diferenciar, (c) dejar como está y aceptar el solapamiento.

**Caso real conocido**: `sf-record-viewer` y `sf-prototype-builder` tienen descriptions casi idénticas — revisar.

---

### DUP02 · Mismo objeto + mismo sistema + mismo tipo

**Severidad**: low

**Regla**: si dos skills tienen la misma tripleta `(objeto, sistema[0], tipo)`, flaggear como solapamiento potencial.

**Fix**: validar que realmente son distintos. Si sí, asegurar que las descriptions los diferencien claramente.

---

## METADATA — Metadata del frontmatter

### M01 · Frontmatter YAML válido

**Severidad**: high

**Regla**: el SKILL.md debe empezar con `---` + YAML válido + `---`.

**Por qué**: sin frontmatter el skill no se registra.

---

### M02 · Campos obligatorios presentes

**Severidad**: high

**Regla**: `name` y `description` son obligatorios.

---

### M03 · No hay campos desconocidos

**Severidad**: low

**Regla**: el frontmatter sólo debería tener `name`, `description`, y opcionalmente `compatibility`. Otros campos confunden.

---

## VERSIONING — Versión y fecha de modificación

> **Nota sobre ubicación**: `version` y `last_modified` van dentro del bloque `metadata:` del frontmatter, no como keys de primer nivel. El validador del `skill-creator` rechaza keys custom fuera de `metadata`.
>
> ```yaml
> metadata:
>   version: 1.2.3
>   last_modified: 2026-04-23
> ```

### V01 · Campo `metadata.version` presente y válido

**Severidad**: medium

**Regla**: el frontmatter debe incluir `metadata.version` en formato SemVer `MAJOR.MINOR.PATCH` (ej: `1.2.3`, `0.1.0`).

**Por qué**: sin versión, no hay forma de saber si un skill fue actualizado desde la última vez que se consumió. Los consumidores de skills (humanos y pipelines) dependen de esto para decidir cuándo re-leer.

**Fix**: agregar `metadata.version: 1.0.0` si el skill ya está publicado; `0.1.0` si está en desarrollo local.

---

### V02 · Campo `metadata.last_modified` presente y válido

**Severidad**: medium

**Regla**: el frontmatter debe incluir `metadata.last_modified` en formato ISO 8601 `YYYY-MM-DD` (ej: `2026-04-23`). La fecha no puede ser futura y no puede ser anterior a `2025-01-01` (sanity check).

**Por qué**: permite ordenar el catálogo por reciente, detectar skills estancados, y correlacionar cambios con incidentes.

**Fix**: agregar `metadata.last_modified: <YYYY-MM-DD>` con la fecha del último cambio publicado.

---

### V03 · Coherencia entre `version` bump y `last_modified`

**Severidad**: low

**Regla**: si un skill subió su `version` (tiene histórico de commits con bumps), el `last_modified` debe coincidir con la fecha del bump más reciente.

**Por qué**: detecta casos donde el owner actualizó la version sin actualizar la fecha (o viceversa).

**Fix**: alinear ambos campos. Regla: un cambio sin bump no existe; un bump sin actualizar fecha es un bug.

---

## TAXONOMY — Dimensiones de clasificación

### T01 · Todas las dimensiones asignables

**Severidad**: low

**Regla**: el skill debe poder mapearse inequívocamente a las 10 dimensiones de `taxonomy.md`. Si el audit no puede determinar `area`, `type` u `object` a partir del contenido, flaggear.

**Fix**: clarificar el propósito del skill en la description, o agregar una sección explícita.

---

### T02 · Owner declarado

**Severidad**: medium

**Regla**: cada skill debe tener un owner. Convención: un archivo `OWNER.md` o una línea `<!-- owner: handle -->` al final del SKILL.md.

**Por qué**: sin owner, nadie mantiene el skill cuando un consultor rota.

**Fix**: asignar owner.

---

### T03 · Skills `deprecated` tienen fecha de sunset

**Severidad**: medium

**Regla**: si el estado es `deprecated`, debe haber una nota indicando la fecha planeada de eliminación y el skill reemplazo.

---

## DESIGN — Reglas de diseño / calidad de skills (Q01–Q11)

Reglas de **cómo está diseñado el skill para operar** (UX, output, inputs, referencias, escritura de registros, interactividad), complementarias a las de nombre/metadata de arriba. Spec completa, con "por qué" y "cómo cumplir", en `references/skill-design-rules.md`. Acá la versión-checklist.

Gates ProContacto: **Q02, Q06, Q07, Q08 y Q11 son `blocking`** en creación/mejora. Q01 y Q05 son `high`. Q03, Q04 y Q09 son `medium`. El script `audit_catalog.py` chequea **Q01**, **Q06**, **Q07**, **Q08**, **Q09** y **Q11** (heurísticas); las demás las evalúa Claude leyendo el skill.

### Q01 · Template de output embebido

**Severidad**: high · **Tipo**: design · **Auditable**: sí

**Regla**: si el skill genera HTML/artifact/widget/dashboard como output, el template debe vivir en `assets/` (con placeholders), no idearse en cada ejecución.

**Señal de violación (script)**: el SKILL.md indica que produce HTML (`create_artifact`, `show_widget`, `mcp__visualize`, `.html`, "dashboard", "reporte HTML") pero `assets/` no tiene ningún archivo de template. Heurística — el humano confirma.

**Fix**: crear `assets/<output>-template.html` con placeholders y hacer que el paso de generación lo rellene en vez de improvisar markup.

---

### Q02 · Repaso pantalla-por-pantalla con aprobación del gestor

**Severidad**: blocking · **Tipo**: design · **Auditable**: no (proceso)

**Regla**: al crear/mejorar un skill con pantallas/HTML, recorrer **cada** pantalla (por más chica que sea, incluidos estados de error/vacío/confirmación) una por una y obtener **aprobación explícita del gestor** por cada una. Una pantalla = una aprobación; no es transitiva.

**Fix**: enumerar las pantallas, identificar al owner (ver T02), presentarlas de a una y registrar el OK. No publicar sin todas aprobadas.

---

### Q03 · Pasos cortos y guiados

**Severidad**: medium · **Tipo**: design · **Auditable**: no

**Regla**: el workflow avanza en pasos cortos y atómicos, guiando al usuario; un objetivo por paso, confirmando antes de avanzar. No vuelca todo de golpe ni pide muchos datos juntos.

**Fix**: reestructurar el SKILL.md en pasos numerados; cada paso con qué hace, qué pide/muestra, y criterio para avanzar.

---

### Q04 · Pregunta de desambiguación si se parece a otro skill

**Severidad**: medium (high si DUP01/DUP02 confirma solapamiento) · **Tipo**: design · **Auditable**: parcial

**Regla**: si el skill se solapa con otro (triggers/dominio), debe abrir con una pregunta que confirme con el usuario cuál de los dos quiere.

**Fix**: correr el audit de duplicados; si hay solapamiento real, agregar al inicio del workflow una pregunta que nombre ambos skills. Sin solapamiento, no agregar la pregunta.

---

### Q05 · Inputs claros y seleccionables (sobre todo de conectores)

**Severidad**: high · **Tipo**: design · **Auditable**: no

**Regla**: los inputs deben ser explícitos y seleccionables. Cuando vienen de un conector, traer las opciones reales (schema / query canónica) y ofrecerlas para elegir — nunca inventar ni hardcodear (valores de picklist siempre del schema real; queries deterministas a referencia parametrizada, no improvisadas en runtime).

**Fix**: para cada input de conector, traer opciones reales, presentarlas seleccionables y validar la selección contra ellas; guardar las queries como referencia del skill.

---

### Q06 · Referencias a otros skills validadas

**Severidad**: blocking (creación/mejora) · high (audit ex-post) · **Tipo**: design · **Auditable**: sí

**Regla**: toda referencia a otro skill (`pc-…`) en el SKILL.md debe existir realmente en el catálogo, con el nombre vigente. No se publica con referencias rotas.

**Señal de violación (script)**: nombres `pc-…` estructuralmente válidos referenciados en el SKILL.md (fuera de bloques de código) que no corresponden a ningún skill escaneado. Heurística — si el audit corre sobre un subset, el skill referenciado puede vivir en otro dir; por eso `high` en audit y `blocking` en creación.

**Fix**: corregir la referencia al nombre vigente (típico tras un rename N02) o quitarla.

---

### Q07 · Contrato de escritura para skills que crean/actualizan registros

**Severidad**: blocking (creación/mejora) · high (audit ex-post) · **Tipo**: design · **Auditable**: sí

**Regla**: todo skill que cree/actualice registros en sistemas externos (Salesforce, Odoo, Jira, etc.) debe declarar un **mapa de escritura** (objetos + campos, marcando obligatorios **técnicos** del schema **y** de negocio como `Amount`) y aplicar el **contrato de escritura**: valores de picklist y API names resueltos a runtime con `getObjectSchema` (no hardcodeados), **gate pre-write** que bloquea si falta un obligatorio o un numérico de negocio no es > 0, y **verificación post-write** (re-query confirma que persistió). Modelo: `pc-sales-sf-quote-builder` (Paso 16.5 + 17.5).

**Señal de violación (script)**: el SKILL.md usa `createSobjectRecord` / `updateSobjectRecord` (u otra escritura a sistema externo) pero no documenta mapa de escritura ni gate de obligatorios / verificación post-write, **o** hardcodea valores de picklist / API names en vez de resolverlos con `getObjectSchema`. Heurística — el humano confirma.

**Fix**: declarar el mapa de escritura por objeto (campos + rol + obligatoriedad técnica/negocio), resolver valores a runtime, y agregar como pasos explícitos el gate pre-write y la verificación post-write. Previene registros incompletos (ej. una Opp creada sin `Amount`).

---

### Q08 · Interactividad cableada y probada en runtime

**Severidad**: blocking · **Tipo**: design · **Auditable**: sí (heurística estática) + proceso (prueba de humo)

**Regla**: todo template HTML de `assets/` con controles interactivos (botones, links de acción, pills/tabs, checkboxes de acción masiva, menús kebab) debe tener **cada control cableado a una acción real dentro del archivo commiteado**: `window.sendPrompt("...")` con el prompt horneado, un `href` real, o un listener JS local (directo o por *event delegation*). El **comportamiento no va en placeholders** (los `{{…}}`/`__…__` inyectan sólo datos), no hay handlers huérfanos ni IDs colgados, y al crear/modificar el HTML se corre la **prueba de humo de interactividad**: renderizar, stubear `sendPrompt`, **clickear cada control** y confirmar que dispara un efecto observable (llamada a sendPrompt / cambio de DOM / navegación) sin errores de consola. Es la contraparte de comportamiento de Q01 (que sólo exige que el markup exista). Modelo: `pc-sales-sf-contract-activator`.

**Señal de violación (script)**: en un template de `assets/`, un elemento clickeable (`<button>`, `[data-act]`, `[role=button]`, `.pill`, `<a>` sin `href`) sin señal de cableado (ni `onclick`, ni listener que lo alcance por id/clase/data-attr/delegación, ni `sendPrompt`), **o** un `onclick`/handler con un placeholder `{{…}}`/`__…__` adentro (comportamiento diferido a runtime). Heurística — el humano confirma con la prueba de humo.

**Fix**: hornear el handler de cada control en el template (sendPrompt con prompt completo / href real / listener local, preferentemente por delegación para filas dinámicas); mover cualquier lógica de acción fuera de los placeholders; y correr la prueba de humo clickeando control por control. Previene botones muertos y comportamiento no determinista entre corridas.

### Q09 · Español neutro por defecto

**Severidad**: medium · **Tipo**: language · **Auditable**: sí (heurística `check_default_dialect`)

**Regla**: el registro por defecto de todo texto que produce un skill (description, prosa, mensajes al usuario, HTML, drafts) es **español neutro** (tuteo: `usa`, `tienes`, `tú`), sin voseo rioplatense (`usá`, `tenés`, `vos`) ni mexicanismos fuertes. **Override, parte de la regla**: si el usuario pide otro dialecto, o la salida es para un cliente de otro país, o el skill declara un registro propio a propósito, se respeta — basta documentarlo en una línea que mencione el dialecto. Spec en `skill-design-rules.md` Q09. Tooling: `scripts/neutralize_voseo.py` + mapa `scripts/voseo_map.py` (fuente única fixer↔detector).

**Señal de violación (script)**: formas de voseo del mapa curado en la description o la prosa del SKILL.md, fuera de líneas que hablen *de* dialecto o de plantillas de mensaje en 1ª persona (pretérito). Heurística best-effort; el humano confirma.

**Fix**: neutralizar con `neutralize_voseo.py --apply` (idempotente, cero falsos positivos) o a mano; documentar el override si el dialecto es intencional.

---

### Q11 · El entregable HTML va al gestor

**Severidad**: blocking · **Tipo**: design · **Auditable**: sí (heurística `check_artifact_publish`)

**Regla**: todo skill que produzca un **entregable** HTML (algo que alguien vuelve a abrir, comparte o corrige: propuesta, SOW, documento, informe, wireframes, diagrama, deck) tiene que cumplir las **dos mitades** de la política de publicación: **(1)** el SKILL.md **cita** `_shared/artifact-publish/artifact-publish.md` y aplica su procedimiento de dos pasos (`listar_artefactos` por título canónico → `publicar_version` si ya existía, `publicar_artefacto` si no) — la política se cita, **no se copia**; y **(2)** el skill figura en el `TARGETS` de `_shared/artifact-publish/sync.sh`, con el script ya corrido, que es lo que mete el módulo dentro del bundle `.skill`. **No aplica** a las pantallas de trabajo del chat (widgets de interacción, paneles operativos), pero eso se **declara** en el SKILL.md con la fórmula explícita (`… via mcp__visualize__show_widget`). Spec en `skill-design-rules.md` Q11. Modelo: `pc-crm-userstory-generator`; caso ad-hoc: `pc-meta-artifact-publisher`.

**Señal de violación (script)**: señales de entregable HTML (salida HTML + vocabulario de entregable), sin declaración de `mcp__visualize__show_widget`, y falta alguna de las dos mitades — no menciona `_shared/artifact-publish` en la prosa, o lo menciona pero la carpeta no está dentro del skill. Heurística: un visor interno puede aparecer como candidato; el humano confirma con la prueba de "¿cuánto vive el output?".

**Fix**: agregar la sección de publicación citando el módulo, sumar `"<área>/<skill>"` al `TARGETS` de `_shared/artifact-publish/sync.sh` y correrlo (regenera el `.skill`). Si el output es una pantalla de trabajo, declararlo en el SKILL.md.

---

## Output del audit

Cada hallazgo tiene este shape:

```json
{
  "rule_id": "N02",
  "type": "naming",
  "severity": "high",
  "skill": "adr-generator",
  "description": "El nombre 'adr-generator' no empieza con el prefijo obligatorio 'pc-'.",
  "suggested_fix": "Renombrar directorio y actualizar `name` en frontmatter a `pc-admin-interno-adr-generator`. Coordinar rename con usuarios que tengan memoria cacheada del nombre viejo.",
  "proposed_new_value": "pc-admin-interno-adr-generator"
}
```

El JSON completo del audit es un array de estos hallazgos, más un bloque de resumen por severidad.
