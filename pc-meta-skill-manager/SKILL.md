---
name: pc-meta-skill-manager
metadata:
  version: 1.8.0
  last_modified: 2026-08-09
description: >
  Gobierna el catálogo de skills de ProContacto bajo la convención
  `pc-[área]-[sistema]-[objeto]-[acción]`. Activar cuando el usuario pida crear un
  skill nuevo ("qué nombre le pongo a...", "estoy armando un skill para..."),
  auditar skills existentes ("revisa el catálogo", "qué skills tenemos duplicados",
  "el nombre de X está mal"), catalogar/mapear por dimensiones ("qué skills hay para
  admins SF", "muéstrame el inventario"), o validar metadata antes de publicar un skill
  ("revisa el frontmatter", "mi description está bien?"). También activar proactivamente
  cuando el usuario esté creando un skill y NO haya mencionado nombre ni taxonomía —
  es obligatorio pasar por acá para mantener consistencia. Produce un inventario
  estructurado, propone renombres, y crea tareas en el tablero Jira PROCSKILLS
  (board 2952) asignadas a los responsables de cada skill. Funciona en español e inglés.
---

# pc-meta-skill-manager — Gobierno del catálogo de skills ProContacto

## ⛔ Regla bloqueante: NO modificar skills existentes sin autorización explícita

**Este skill NUNCA modifica archivos de otros skills sin autorización previa, explícita y puntual del usuario.**

Esto aplica — sin excepción — a:

- Renombrar directorios de skills existentes.
- Editar SKILL.md, references/, scripts/ o cualquier archivo dentro de un skill.
- Reescribir frontmatter (`name`, `description`, etc.).
- Borrar o mover archivos.
- Aplicar fixes sugeridos por el audit.

El workflow permitido es:

1. **Proponer** el cambio por escrito, citando el archivo exacto y el diff conceptual.
2. **Esperar** un "sí" explícito del usuario para ese cambio puntual.
3. **Aplicar** sólo después de la autorización — y sólo el cambio autorizado.

Una autorización no es transitiva: aprobar un rename no autoriza a editar la description. Cada cambio requiere su propio "sí". Si hay varios hallazgos, se autorizan uno por uno o se enumera el set completo explícitamente.

**Por qué esta regla es bloqueante**: este skill es un gobernador de catálogo, no un editor masivo. Cambios automáticos sobre skills de otros owners rompen memoria cacheada de triggers, invalidan docs compartidas, y generan conflictos invisibles para los usuarios que dependen de esos skills.

Las únicas acciones que este skill sí puede hacer sin autorización previa son: **leer** cualquier skill, **generar reportes/JSON** en su propio workspace, **crear tareas Jira** (con confirmación previa en la conversación como siempre), y **escribir archivos nuevos en su propio directorio** (`pc-meta-skill-manager/`).

## Objetivo

Mantener el catálogo de skills de ProContacto **consistente**, **descubrible** y **escalable**. Todos los skills propios de ProContacto deben seguir una única fórmula:

```
pc-[área]-[sistema]-[objeto]-[acción]
```

- `pc-` — prefijo fijo que identifica propiedad de ProContacto (siempre va).
- `[área]` — práctica a la que pertenece (crm, cg-cloud, data, delivery, admin-interno, meta, etc.).
- `[sistema]` — herramienta externa principal (salesforce, jira, gmail, etc.). **Opcional**: se omite cuando el área lo implica (ej: `cg-cloud` ya implica Salesforce) o cuando no hay sistema externo (skills internos).
- `[objeto]` — entidad sobre la que actúa (user, field, opportunity, worklog, brand).
- `[acción]` — un único verbo (creator, builder, generator, viewer, guide, manager…). Si el skill hace múltiples operaciones sobre el mismo objeto, usar acción paraguas (`manager`, `workflow`, `orchestrator`) en vez de concatenar verbos.

Detalle completo, tabla de prefijos, mapa área→sistema implícito, y ejemplos sobre el catálogo real en `references/naming-convention.md`.

### Por qué esta fórmula

- `pc-` al frente identifica toda la producción interna de un vistazo — diferenciable de skills de Anthropic y plugins externos.
- **Área antes de sistema**: "¿qué hay para CRM?" es más frecuente que "¿qué hay para Jira?". Orden alfabético agrupa naturalmente por práctica.
- Sistema opcional evita nombres redundantes (`pc-cg-cloud-salesforce-...` sería rellenado con info que el área ya tiene).
- Una acción por skill mantiene la granularidad: un skill = una cosa. Si hace muchas, `manager` lo captura.

## Las 4 capacidades

| Capacidad | Cuándo usar | Output |
|---|---|---|
| **Nombrar** | El usuario está creando un skill nuevo y necesita un nombre | Nombre kebab-case validado + justificación |
| **Auditar** | El usuario pide revisar el catálogo entero o un subset | Reporte MD con hallazgos + tareas Jira creadas y asignadas |
| **Catalogar** | El usuario quiere ver qué skills hay, por dimensión | JSON/artifact con el inventario completo |
| **Validar** | El usuario está por publicar un skill y quiere un check final | Lista de issues a corregir antes de mergear |

Las cuatro capacidades miran **cómo se llama y se cataloga** un skill. Transversal a todas está la pregunta de **cómo está diseñado para operar** — las reglas de diseño de abajo.

---

## Reglas de diseño de un buen skill ProContacto (Q01–Q11)

Más allá del nombre y la metadata, un buen skill ProContacto cumple diez reglas de diseño (Q01–Q09 y Q11; el Q10 está reservado y sin spec, ver la tabla). **Recomiéndalas y busca que se apliquen en dos momentos**: al **crear** un skill (Capacidad 1) y al **validar o mejorar** uno existente (Capacidad 4). La spec completa — con "por qué" y "cómo cumplir" cada una — está en `references/skill-design-rules.md`.

| ID | Regla | Severidad | Auditable por script |
|---|---|---|---|
| **Q01** | Si genera HTML/artefacto como output, el **template vive en `assets/`** (no se improvisa en cada corrida) | high | sí (heurística) |
| **Q02** | Repaso **pantalla-por-pantalla** de cada HTML, con **aprobación explícita del gestor** del skill | ⛔ blocking | no (proceso) |
| **Q03** | Workflow en **pasos cortos**, guiando al usuario en todo momento | medium | no |
| **Q04** | Si se **parece a otro skill**, pregunta de **desambiguación al inicio** | medium / high | parcial |
| **Q05** | Inputs **claros y seleccionables**; si vienen de un conector, traer las **opciones reales** (schema / query canónica), nunca inventar | high | no |
| **Q06** | Las **referencias a otros skills** (`pc-…`) deben **existir** en el catálogo | ⛔ blocking | sí (heurística) |
| **Q07** | Si **crea/actualiza registros** en sistemas externos: **mapa de escritura** declarado (obligatorios técnicos + de negocio) + valores a runtime (no hardcode) + gate pre-write + verificación post-write | ⛔ blocking | sí (heurística) |
| **Q08** | Si el HTML tiene **botones/controles**: cada uno **cableado a una acción real en el template** (sendPrompt/href/listener), comportamiento **no** en placeholders, y **probado clickeándolo renderizado** (prueba de humo de interactividad) | ⛔ blocking | sí (heurística estática) + proceso |
| **Q09** | **Español neutro por defecto**: la `description`, la **prosa/instrucciones** y sobre todo la **salida al usuario** (mensajes, HTML, plantillas, drafts) se escriben en tuteo neutro, sin voseo ni mexicanismos. Override: dialecto del cliente por país o registro propio declarado | medium | sí (heurística `check_default_dialect`) |
| **Q10** | ⏸ **RESERVADO, sin spec escrita.** El registry y el explainer ya citan un Q10 (declarar `metadata.connectors` + sección `## Cómo funciona`) que nunca se escribió. No reusar el número — ver `references/skill-design-rules.md` | — | no |
| **Q11** | Si produce un **entregable HTML**: el SKILL.md **cita** `_shared/artifact-publish/` (no copia la política) **y** el skill está en el `TARGETS` de su `sync.sh`, con el módulo ya dentro de su carpeta. Si el output es una **pantalla de trabajo**, queda **declarado** que va por `mcp__visualize__show_widget` y la regla no aplica | ⛔ blocking | sí (heurística) |

### ⛔ Gates bloqueantes de diseño: Q02, Q06, Q07, Q08 y Q11

Al crear o mejorar un skill, **Q02, Q06, Q07, Q08 y Q11 frenan la publicación** (igual que la validación de nombre de la Capacidad 1):

- **Q02** — ningún skill con pantallas/HTML se da por bueno hasta haber recorrido **cada pantalla** (incluidos estados de error/vacío/confirmación, por más chicos que sean) con el **gestor del skill** y tener su OK puntual por cada una. Una aprobación no es transitiva. Si el skill no tiene gestor declarado (regla T02), primero hay que declararlo. Q02 aprueba **cómo se ve**; Q08 aprueba **que responde**.
- **Q06** — ningún skill se publica con referencias a otros skills que no existan. Toda referencia `pc-…` se valida contra el catálogo antes de mergear.
- **Q07** — ningún skill que escriba registros se publica sin declarar su **mapa de escritura** (qué objetos/campos, cuáles obligatorios técnicos + de negocio) y aplicar el **contrato de escritura**: valores/API names resueltos a runtime (no hardcodeados), gate pre-write que bloquea si falta un obligatorio, y verificación post-write. Previene registros incompletos (ej. una Opp creada sin `Amount`). Modelo: `pc-sales-sf-quote-builder` (Paso 16.5 + 17.5).
- **Q11** — ningún skill que produzca un **entregable HTML** se publica sin la política de publicación **citada y propagada**. Las dos mitades: el SKILL.md tiene una sección que remite a `_shared/artifact-publish/artifact-publish.md` y aplica su procedimiento de dos pasos (`listar_artefactos` por título canónico → `publicar_version` si ya existía, `publicar_artefacto` si no), **y** el skill figura en el `TARGETS` de `_shared/artifact-publish/sync.sh` con el script ya corrido. Las dos fallan en silencio y de forma distinta: sin la cita el módulo viaja en el bundle y nadie lo lee; sin el `TARGETS` la cita apunta a un archivo que en la máquina del usuario no existe. La política **no se copia** en el skill: se cita. Si el output es una **pantalla de trabajo** (widget de interacción, panel operativo), la regla no aplica — pero eso se **declara** en el SKILL.md con la fórmula explícita (`… via mcp__visualize__show_widget`), porque un skill que no dice a dónde va su output deja la decisión librada a cada corrida. El caso ad-hoc (un HTML armado sin skill productor) ya tiene dueño: `pc-meta-artifact-publisher` + el hook de `SessionStart` del grupo `router`. Modelo: `pc-crm-userstory-generator`.
- **Q08** — ningún template HTML con controles interactivos se da por bueno con **botones muertos**. Cada botón/link/pill/menú resuelve a una acción real **horneada en el archivo commiteado** (`sendPrompt` con el prompt completo, un `href` real, o un listener JS local — preferentemente por *event delegation* para filas dinámicas); el **comportamiento no vive en placeholders** (los `{{…}}`/`__…__` inyectan sólo datos); y antes de publicar se corre la **prueba de humo de interactividad**: renderizar el HTML, stubear `sendPrompt`, **clickear cada control** y confirmar que dispara un efecto observable (llamada a `sendPrompt` / cambio de DOM / navegación) sin errores de consola. Es la contraparte de comportamiento de Q01 y ataca el bug recurrente de "botones que no hacen nada o se comportan distinto en cada corrida". Modelo: `pc-sales-sf-contract-activator`.

Q01 y Q05 son recomendaciones fuertes (se señalan siempre, el default es cumplirlas); Q03 y Q04 son recomendaciones según el caso. Como toda regla del catálogo: el skill **propone, no impone** — pero las bloqueantes no se saltean sin una decisión explícita y registrada del gestor.

El script `audit_catalog.py` chequea **Q01**, **Q06**, **Q07**, **Q08**, **Q09** y **Q11** automáticamente en los barridos del catálogo (heurísticas best-effort, ver `references/skill-design-rules.md`); Q02/Q03/Q04/Q05 las evalúa Claude leyendo el skill. Para Q08, el script caza candidatos a botón muerto por estática, pero **no reemplaza la prueba de humo en runtime** — esa la hace Claude renderizando y clickeando.

---

## Capacidad 1 — Nombrar un skill nuevo

Cuando el usuario diga "estoy armando un skill para X" o "qué nombre le pongo":

1. **Extrae** del pedido: área (práctica), sistema (si aplica), objeto/entidad, y acción (qué hace).
2. **Aplica** la fórmula `pc-[área]-[sistema]-[objeto]-[acción]`. Si el área implica el sistema o no hay sistema externo, omitilo. Consulta la tabla en `references/naming-convention.md`.
3. **Chequea colisiones** contra el catálogo actual (lee los directorios bajo `.claude/skills/` o el workspace de skills).
4. **Propón** 1 nombre primario + 1-2 alternativas con justificación corta. El usuario elige.
5. **Valida** el nombre elegido con `scripts/validate_name.py` (ver sub-sección bloqueante abajo).
6. **Genera también** un frontmatter inicial (`name`, `description`, `version`, `last_modified`) siguiendo la plantilla.
7. **Aplica las reglas de diseño (Q01–Q11)** al diseñar el skill — ver la sección "Reglas de diseño de un buen skill" arriba y `references/skill-design-rules.md`. Recuerda los gates: si va a tener HTML, el template arranca en `assets/` (Q01) y se repasa pantalla-por-pantalla con el gestor (Q02 ⛔); si toma datos de conectores, los inputs son seleccionables con valores reales (Q05); toda referencia a otro skill se valida contra el catálogo (Q06 ⛔); si crea/actualiza registros, declara su mapa de escritura con gate pre-write + verificación post-write (Q07 ⛔); y si el HTML tiene botones/controles, cada uno queda cableado a una acción real en el template y se prueba clickeándolo renderizado (Q08 ⛔); si produce un entregable HTML, cita `_shared/artifact-publish/` y se suma al `TARGETS` de su `sync.sh` — y si en cambio su output es una pantalla de trabajo, lo declara por `mcp__visualize__show_widget` (Q11 ⛔); y toda la prosa y la **salida al usuario** se escriben en español neutro (tuteo), salvo override de dialecto (Q09).
8. **Pregunta la configuración de distribución**: antes de cerrar, pregúntale a Ariel qué config de `config.json` quieres (¿se distribuye o va a `excluir`?, ¿en qué grupo/carpeta?, ¿`auto` u on-demand para su área?), propón el diff y aplícalo con su OK. Ver "🚚 Configuración de distribución en `config.json`" más abajo.
9. **Cierra con el handoff del bundle**: genera el `.skill` y compárteselo a Ariel por Slack DM para que lo suba al repo — la creación no termina hasta ese paso. Ver "📎 Handoff del bundle `.skill`" más abajo.

### ⛔ Validación bloqueante del nombre y la description en creación

**Antes de crear cualquier directorio, archivo, o empaquetar un skill, el nombre elegido DEBE pasar la validación estricta.**

La validación exige cinco invariantes simultáneas:

1. **Estructura**: el nombre debe parsear correctamente bajo la fórmula `pc-[área]-[sistema?]-[objeto]-[acción]` — cada slot contra su lista de valores permitidos (`VALID_AREAS`, `VALID_SYSTEMS`, `VALID_ACTIONS`, reglas de `AREAS_OMIT_SYSTEM`).
2. **Coincidencia directorio = frontmatter**: el nombre del directorio del skill debe coincidir **carácter por carácter** con el campo `name` del YAML frontmatter (regla N01 elevada a bloqueante en creación).
3. **No colisión**: el nombre no debe duplicar un skill existente en el catálogo. Si hay colisión, es error incluso si el parseo es OK.
4. **Exit code 0 de `validate_name.py`**: la validación automática del nombre debe pasar.
5. **Description ≤ 1024 caracteres**: el campo `description` del frontmatter NO puede superar los 1024 caracteres — es el límite duro del validador de Anthropic (skill-creator). Arriba de eso el skill no se puede crear, empaquetar ni modificar. Piso recomendado ProContacto: ≥300 caracteres para que triggerea bien.

Comando de validación obligatorio:

```bash
python3 pc-meta-skill-manager/scripts/validate_name.py <nombre-propuesto>
# exit 0 → seguir; exit 1 → detener todo el flow

# Y validar la longitud de la description contra el límite de 1024:
python3 pc-meta-skill-manager/scripts/validate_description.py --skill-md <ruta-al-SKILL.md>
# (o --file desc.txt, o pasando la description inline)
# exit 0 → OK; exit 1 → description > 1024, detener y acortar
```

Si cualquiera de las 5 invariantes falla:

- **NO** se propone el frontmatter.
- **NO** se crea el directorio del skill.
- **NO** se invoca `package_skill.py`.
- **NO** se escribe ningún archivo del skill nuevo.

Se explica al usuario qué slot falla, se propone la corrección concreta, y se reinicia la validación con el nombre corregido. Esta regla es más estricta que las reglas N02-N05 del audit ex-post: aquellas toleran deuda legacy, ésta no tolera nada en creación.

**Por qué bloqueante**: renombrar un skill después de creado es costoso (rompe triggers cacheados, referencias en docs, memoria de Claude en sesiones vivas). Prevenir es mucho más barato que corregir.

### Ejemplo

Usuario: "estoy haciendo un skill para crear oportunidades de Salesforce a partir de emails de Gmail"

Respuesta esperada:
```
Propongo: pc-crm-salesforce-opportunity-creator (primario)

Razonamiento:
- área: crm (el skill entrega valor en Sales Cloud)
- sistema: salesforce (destino de la acción; no se omite porque CRM puede tener
  múltiples sistemas)
- objeto: opportunity
- acción: creator

Nota: Gmail es fuente de datos pero no parte de la identidad del skill. La dependencia
de Gmail va documentada en el frontmatter/taxonomía (`dependencies: [gmail]`), no en
el nombre.

Alternativa si el skill también actualiza/elimina oportunidades:
  pc-crm-salesforce-opportunity-manager

Frontmatter sugerido:
---
name: pc-crm-salesforce-opportunity-creator
metadata:
  version: 1.0.0
  last_modified: 2026-04-23
description: >
  Crea Opportunities en Salesforce a partir de emails de Gmail. Activar cuando el
  usuario diga "crear oportunidad desde email", "convertir email en opportunity",
  "sacar oportunidad de este correo", o reenvíe un email preguntando si debería
  volverse oportunidad. Parsea el email, matchea Account y Contact existentes,
  sugiere Stage y Amount basándose en señales del email, y pide confirmación
  antes de crear el registro en SF. Funciona en español e inglés.
---
```

### Política de versionado y fecha de modificación

Todos los skills ProContacto deben llevar versión y fecha de modificación dentro del bloque `metadata:` del frontmatter (el validador del `skill-creator` de Anthropic no acepta keys custom de primer nivel; `metadata` es el slot oficial para extensiones):

```yaml
metadata:
  version: 1.2.3
  last_modified: 2026-04-23
```

| Campo | Formato | Qué rastrea |
|---|---|---|
| `metadata.version` | SemVer `MAJOR.MINOR.PATCH` (ej: `1.2.3`) | Estado público del skill |
| `metadata.last_modified` | ISO 8601 `YYYY-MM-DD` (ej: `2026-04-23`) | Fecha del último cambio publicado |

Reglas de versionado (SemVer aplicado a skills):

- **MAJOR** (+1.0.0): cambia el nombre del skill, se quitan capacidades, o se reescribe la convención de triggers de forma incompatible con memoria cacheada.
- **MINOR** (+0.1.0): se agrega una capacidad, se amplía la `description` con nuevos triggers, se suman referencias/scripts.
- **PATCH** (+0.0.1): fix de redacción, typos, ajustes menores al workflow que no cambian qué hace el skill.

Reglas sobre `last_modified`:

- Se actualiza **junto con cada bump de versión**. Un cambio sin bump de versión no existe para el catálogo.
- Formato ISO 8601 estricto, zona UTC implícita, sin hora (día completo).
- Nunca retroceder. Si se corrige un archivo antiguo, la fecha es la del día de la corrección, no la de creación.

Versión inicial de un skill nuevo: **`1.0.0`** cuando se publica. Durante desarrollo local pre-publicación, usar `0.x.y` (ej: `0.1.0`) y escalar a `1.0.0` al mergear.

### 📎 Handoff del bundle `.skill` a Ariel por Slack DM (cierre obligatorio de la creación)

**Quien crea un skill casi nunca tiene permisos para subirlo al repo.** El repositorio de skills lo administra **Ariel Tarsitano** (`ariel.tarsitano@procontacto.com.mx`). Por eso, la creación de un skill **no se da por terminada** hasta que el bundle `.skill` esté en manos de Ariel para que él lo suba al repo.

**Regla**: al finalizar la creación (o una modificación que deba publicarse) de un skill, este skill (`pc-meta-skill-manager`) debe:

1. **Generar el bundle `.skill`** del skill nuevo/modificado (empaquetar la carpeta con su `SKILL.md` + `references/` + `scripts/` + `assets/`). El `.skill` es el artefacto deployable — sin él, Ariel no puede publicarlo. (Ligado a la regla "generar el `.skill` antes de deployar".)
2. **Mandárselo a Ariel por Slack DM** — mensaje directo, no a un canal. Ubica a Ariel con `slack_search_users` por su email `ariel.tarsitano@procontacto.com.mx` (nunca adivines el user id). El DM debe incluir:
   - nombre del skill + versión (`metadata.version`),
   - qué hace en una línea,
   - el **archivo `.skill` adjunto** (si el conector no permite subir archivo, dejar el path del bundle en el repo/working tree y avisar que queda para que Ariel lo suba),
   - una nota de qué falta para publicar (p. ej. "pendiente: subir a `<área>/` + push a main").
3. **Confirmar antes de enviar**: como toda acción con efecto externo, el DM se muestra/confirma en la conversación y se manda sólo con el OK. Nunca DM automático sin aprobación.

**Por qué**: cierra el hueco entre "creé un skill" y "el skill está en el repo/flota". Sin este handoff, los skills quedan en la máquina de quien los creó y nunca llegan al catálogo. Centralizar la subida en Ariel mantiene el repo como fuente única de verdad y evita bundles sueltos sin revisar.

> Excepción: si **Ariel mismo** está creando el skill (tiene acceso al repo), no hace falta el DM — puede commitear/pushear directo. El handoff aplica cuando lo crea otra persona.

### 🚚 Configuración de distribución en `config.json` (PREGUNTAR SIEMPRE al crear o modificar)

**Siempre que se crea o se modifica un skill, hay que preguntarle a Ariel qué configuración de distribución quiere en `config.json`** — antes de dar por cerrado el trabajo. `config.json` es la fuente de verdad de cómo el skill llega (o no) a la flota; nunca se asume por default.

Las preguntas a hacer (una por una, con las opciones reales):

1. **¿Se distribuye o queda interno?** Si es interno/operativo, va a la lista **`excluir`** (`"<carpeta>/<skill>"`) y no se publica a nadie. Si se distribuye, no va en `excluir`.
2. **¿En qué carpeta/grupo vive?** La carpeta del repo = el grupo = el plugin `procontacto-<carpeta>` (comercial, delivery, meta, devops, legales, marketing, administracion, rrhh). Normalmente la del área del skill; confirmarlo.
3. **¿Modo de instalación para su área?** En la sección `areas`:
   - **`auto`** — el plugin de esa carpeta se **auto-instala** a los usuarios de su área (y queda on-demand para el resto vía `general`).
   - **`disponible`** (default) — aparece en el **Directorio de Cowork** y se instala on-demand; nadie lo tiene solo.
4. **¿Alguna excepción puntual?** (`omitir` en una asignación de área, o `vscode: true` para copiarlo también a `~/.claude/skills`).

Con las respuestas, **proponer el diff de `config.json` y aplicarlo sólo con el OK** (igual que cualquier cambio con efecto: `config.json` gobierna a toda la flota, así que nunca se edita sin confirmación puntual). Recuerda las consecuencias al presentar el diff (p. ej. "esto deja el plugin `procontacto-X` sin skills", o "esto lo auto-instala a toda el área Y").

**Por qué preguntar siempre**: el default silencioso (heredar la config de la carpeta) manda skills operativos/internos a manos de toda un área, o deja sin distribuir uno que sí debía llegar. Preguntar de entrada evita ambos errores y mantiene `config.json` como decisión explícita, no accidental.

---

## Capacidad 2 — Auditar el catálogo

Cuando el usuario pida auditar (total o parcial), ejecuta `scripts/audit_catalog.py`:

```bash
python3 scripts/audit_catalog.py --skills-dir <ruta-al-directorio-de-skills> --output audit.json
```

El script produce un JSON con un array de hallazgos. Cada hallazgo tiene tipo (`naming`, `duplicate`, `description`, `metadata`), severidad (`low`, `medium`, `high`), skill afectado, descripción del problema, y una sugerencia de fix.

### Flujo después del audit

1. **Resume** los hallazgos agrupados por tipo y severidad. No arrojes el JSON crudo al usuario.
2. **Muestra el top 5-10** de hallazgos más importantes en el chat, con ejemplos concretos.
3. **Pregunta** al usuario: "¿Quieres que cree tareas Jira en PROCSKILLS para cada hallazgo?" — espera confirmación.
4. **Si sí**, sigue `references/jira-workflow.md` para crear las issues, una por hallazgo, asignadas según las reglas de routing.
5. **Entrega** al final un reporte MD en el workspace con todo el detalle, más los links a las issues creadas.

> **Importante**: no crees issues Jira sin confirmación explícita. Son artefactos visibles al equipo y un audit puede generar decenas de ellas.

> **Bloqueante**: NUNCA apliques los `suggested_fix` directamente sobre los skills auditados. El audit describe el problema y propone el fix, pero la ejecución pasa por el owner del skill vía una issue Jira, no por edición automática. Ver la regla bloqueante al inicio del SKILL.md.

Ver `references/audit-checklist.md` para la lista completa de qué revisa el audit.

---

## Capacidad 3 — Catalogar por dimensiones

Cuando el usuario pida ver el inventario ("qué skills tenemos para admins SF", "cuáles usan Jira", "muéstrame el catálogo"):

1. **Corre** `scripts/audit_catalog.py --mode catalog --output catalog.json`. Este modo extrae las dimensiones de cada skill (rol, área, objeto, sistema, tipo, estado, idioma, owner, dependencias) sin evaluar hallazgos.
2. **Si el usuario pidió un subset** (por rol, por sistema, etc.), filtra el JSON y muestra una tabla en chat.
3. **Si pidió el catálogo completo**, genera un **artifact interactivo** (HTML filtrable) **a partir del template embebido** `assets/catalog-viewer-template.html` — no improvises el markup (esto es Q01 aplicado a este propio skill). Reemplaza el token `__CATALOG_JSON__` por el array de skills del `catalog.json` y entrega el HTML resultante. El template ya trae la tabla + filtros por dimensión (área, sistema, acción, idioma, origen) y búsqueda. Es la forma natural de consumir esto — el usuario va a querer volver a abrirlo.

Ver `references/taxonomy.md` para las dimensiones y sus valores permitidos.

---

## Capacidad 4 — Validar o mejorar un skill

Cuando el usuario diga "revisa este skill antes de mergear", "mejorá este skill", "valida el diseño de X" o pase el path a un SKILL.md:

1. **Lee** el SKILL.md y su directorio (incluye `references/`, `scripts/` y `assets/`).
2. **Corre** dos checklists contra ese skill: el de `references/audit-checklist.md` (nombre, description, metadata, versión, taxonomía) **y** el de `references/skill-design-rules.md` (reglas de diseño Q01–Q11). Para Q01, Q06, Q07, Q08, Q09 y Q11 puedes apoyarte en `audit_catalog.py`.
3. **Lista** los issues encontrados con severidad. Si no hay ninguno, dilo explícitamente ("OK para mergear").
4. **Trata como bloqueantes** los issues `blocking`/high: las reglas de nombre/description high-severity, y los gates de diseño **Q02** (repaso pantalla-por-pantalla aprobado por el gestor), **Q06** (referencias a skills que existan), **Q07** (contrato de escritura en skills que crean/actualizan registros), **Q08** (controles del HTML cableados y probados en runtime) y **Q11** (política de publicación citada y propagada en los skills que producen un entregable HTML). No los menciones como "sugerencias" — propón el fix concreto.
5. **Si el skill tiene HTML y lo estás mejorando**, ejecuta el repaso de Q02 **y** la prueba de humo de Q08: recorre cada pantalla/template una por una con el gestor del skill y pide aprobación visual por cada una (Q02); y renderiza el HTML, stubea `sendPrompt` y **clickea cada control** confirmando que dispara un efecto observable sin errores de consola (Q08), antes de dar por buena la mejora. Q02 = cómo se ve; Q08 = que responde.
6. **Nunca escribas el fix directamente** en el SKILL.md del skill revisado. Proponlo en chat y espera autorización explícita antes de aplicarlo — aun cuando el usuario sea el owner del skill. Ver la regla bloqueante al inicio del SKILL.md.
7. **Al modificar un skill, cierra con distribución + bundle**: pregunta si cambia la config de distribución en `config.json` (ver "🚚 Configuración de distribución"), y regenerá el `.skill` para que el bundle no quede viejo (ver "📎 Handoff del bundle `.skill`").

---

## Integración con Jira PROCSKILLS

El tablero https://procontacto.atlassian.net/jira/software/c/projects/PROCSKILLS/boards/2952 es donde se trackea el trabajo de governance del catálogo. Cada hallazgo significativo de una auditoría se vuelve una tarea Jira asignada a un responsable.

El workflow detallado (tipo de issue, campos, labels, reglas de routing/asignación) está en `references/jira-workflow.md`. Léelo antes de crear issues — no improvises los campos, porque el tablero tiene filtros configurados.

Dependencia: el conector Atlassian debe estar autenticado. Si no lo está, avisa al usuario y no intentes crear las tareas.

---

## Estructura del skill

```
pc-meta-skill-manager/
├── SKILL.md                         ← este archivo (workflow maestro)
├── references/
│   ├── naming-convention.md         ← fórmula pc-[área]-[sistema]-[objeto]-[acción] + ejemplos reales
│   ├── taxonomy.md                  ← las 10 dimensiones y sus valores permitidos
│   ├── audit-checklist.md           ← qué revisa el audit (reglas N/D/DUP/M/V/T + diseño Q01–Q11)
│   ├── skill-design-rules.md        ← reglas de diseño de un buen skill (Q01–Q11, spec completa)
│   └── jira-workflow.md             ← cómo crear issues en PROCSKILLS
├── scripts/
│   ├── audit_catalog.py             ← escanea skills y genera audit/catalog JSON (incl. Q01/Q06/Q07/Q08)
│   ├── normalize_name.py            ← propone nombre normalizado desde input libre
│   ├── validate_name.py             ← validación bloqueante (exit 0/1) del nombre, para creación
│   └── validate_description.py      ← valida que la description no supere el techo de 1024
└── assets/
    ├── catalog-schema.json          ← schema del inventario (referencia)
    └── catalog-viewer-template.html ← template del artifact de catálogo (Q01: HTML embebido)
```

## Principios de diseño

- **Pragmatismo sobre pureza**: si un skill ya está en producción con un nombre viejo, renombrarlo es caro (rompe triggers cacheados, docs, memoria de Claude en sesiones vivas). Audita y sugerí, pero no forces.
- **Convención aplica a skills ProContacto, no a los de terceros**: `docx`, `pptx`, `pdf`, `xlsx`, `skill-creator`, `consolidate-memory` etc. vienen de Anthropic o de plugins externos. No los renombres. Márcalos como `origin: external` en el catálogo.
- **El catálogo es vivo**: el audit y el inventario se van a correr varias veces por mes. Optimiza los scripts para ser idempotentes y rápidos.
- **Feedback antes que autoridad**: este skill propone, el humano decide. Ver la regla bloqueante al inicio del SKILL.md — nunca editar skills ajenos (ni el propio en un flow automático) sin autorización explícita y puntual. Una autorización no es transitiva.
- **Diseño, no sólo nombre**: un nombre perfecto no salva a un skill con UX pobre. Las reglas Q01–Q11 (`references/skill-design-rules.md`) son tan parte de "un buen skill" como la convención de nombres — recomiéndalas siempre al crear o mejorar.
- **Autoaplicación**: este mismo skill sigue la convención (`pc-meta-skill-manager`) y sus propias reglas de diseño — p. ej. Q01: su artifact de catálogo sale del template `assets/catalog-viewer-template.html`, no se improvisa. Si encuentras alguna inconsistencia en él, es un bug; repórtala.
