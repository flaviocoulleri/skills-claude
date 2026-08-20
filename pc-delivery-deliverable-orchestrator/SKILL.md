---
name: pc-delivery-deliverable-orchestrator
metadata:
  version: 1.2.0
  last_modified: 2026-08-06
description: >
  Organiza el espacio de trabajo de un proyecto de delivery: crea las subcarpetas en la carpeta Drive
  del proyecto (por fases del proceso), traza los artefactos visuales (AS-IS, TO-BE, Wireframes v2, ERD,
  arquitectura de integraciones) que se materializan como artefactos de Cowork, y crea un issue
  `Artifact` (workflow Deliverable) por entregable en el proyecto Jira del cliente, todo trazado y
  vinculado. Parte de un `Project__c` de Salesforce y reutiliza la carpeta raíz de
  pc-delivery-sf-project-builder (no la re-crea). Activar con: "organiza las carpetas del proyecto",
  "arma la estructura de Drive", "crea los artefactos en Jira", "scaffolding del proyecto", "deja lista
  la estructura de entregables", "organize the project folders/artifacts". NO crea la raíz ni el tooling
  (eso es project-builder); NO redacta el contenido de los entregables. Confirma antes de cada escritura.
  Solo PMs/Delivery Managers. Requiere Cowork (Salesforce + Drive + Atlassian). ES/EN.
---

# pc-delivery-deliverable-orchestrator — Estructura de Drive + Artefactos + Artifacts en Jira

Este skill deja **lista la estructura de trabajo** de un proyecto de implementación de ProContacto:

1. **Drive** — crea el árbol de subcarpetas por fase del proceso dentro de la carpeta raíz del proyecto.
2. **Artefactos visuales** — los identifica del catálogo; su contenido se materializa como **artefacto de
   Cowork** (lo produce el skill de cada artefacto, no este skill), y acá se traza su link.
3. **Jira** — crea un issue `Artifact` (workflow "Deliverable") por cada entregable, con su link.

No genera el **contenido** de los entregables (para eso están los skills de cada documento —
ver `references/artifact-catalog.md`); deja el **contenedor** y la **trazabilidad**.

Fuente del proceso: `pc-delivery-blueprint-guide` (5 fases / 4 gates / 10 entregables del Sprint 0).

---

## CRITICAL RULES (leer antes de hacer nada)

1. **UNA pregunta a la vez.** Nunca batchear preguntas. Pregunta → espera respuesta → sigue.
2. **CONFIRMAR antes de crear cualquier recurso.** Formato:
   > "Voy a crear: **{tipo}** con nombre **{nombre exacto}**. ¿Confirmo?"
   No proceder sin un "sí" explícito del usuario.
3. **BUSCAR antes de crear (idempotencia).** Antes de crear una carpeta, un proyecto de Design o un
   issue `Artifact`, buscar si ya existe (por nombre / link). Si existe, **reusar y avisar**, no duplicar.
4. **Registrar/linkear después de cada escritura.** Tras crear cada recurso, mostrar el link clickeable.
5. **NUNCA renombrar ni borrar** carpetas, proyectos, issues o registros sin autorización explícita del usuario.
6. **NUNCA inventar el link de un artefacto.** Este skill NO produce el contenido de los artefactos
   visuales — los materializa el skill de cada artefacto como artefacto de Cowork (wireframes →
   `pc-crm-salesforce-wireframe-builder`; diagramas AS-IS/TO-BE/ERD/integraciones → su skill/Cowork).
   Si el artefacto todavía no fue producido, **degradar** al modo semi-automático: crear el `Artifact`
   en Jira como placeholder ("pendiente de link") y decir con qué skill se genera. Inventar o suponer
   una URL = violación crítica.
7. **NUNCA escribir campos calculados de `Project_Asset__c`.** `Link__c` es fórmula y `Name` es
   auto-number → nunca setearlos. Solo `Type__c` (picklist restringido) + `Value__c` (ID en crudo).
   Registrar como `Project_Asset__c` **solo** si existe un valor de picklist válido para ese tipo
   (verificar con `getObjectSchema`); si no existe, la trazabilidad va únicamente por el `Artifact` de Jira.
8. **El work type real de Jira es `Artifact`, NO `Artefacto`.** Verificar el `id`/`name` real del
   issuetype con el metadata de la org (no hardcodear el string en español). `Artifact` id conocido: 10209.
9. **No re-crear lo de project-builder.** La carpeta raíz de Drive y el Claude *Project* (chat) los crea
   `pc-delivery-sf-project-builder`. Este skill trabaja **adentro** de la raíz existente. Si la raíz no
   existe → derivar a project-builder, no crearla acá.

---

## Context

- **Salesforce:** org alias `procontacto`, instancia `grupoprocontacto.lightning.force.com`.
  Queries con las MCP tools de Salesforce (`soqlQuery`, `getObjectSchema`, `createSobjectRecord`).
- **Google Drive:** carpeta padre "B - Proyectos" = `1TlZt2nV_kNcML1U_RBBYlaoITSUNRxUP`.
  Crear carpetas con la MCP de Drive `create_file` (`mimeType: application/vnd.google-apps.folder`,
  `parentId`). Estructura: `B - Proyectos > {Cuenta} > {Proyecto (raíz)} > subcarpetas de este skill`.
- **Jira:** site `procontacto.atlassian.net`. MCP Atlassian (`getJiraIssueTypeMetaWithFields`,
  `createJiraIssue`, `getJiraIssue`). Detectar `cloudId` en runtime (no hardcodear). Issuetype `Artifact`.
- **Artefactos visuales:** wireframes y diagramas (AS-IS, TO-BE, ERD, integraciones) se publican en el
  **gestor de ProContacto** (`artifacts.procontacto.com.mx/a/<uuid>`), producidos por el skill
  de cada artefacto — no por este skill. Acá solo se traza su link y se registra el `Artifact`/asset.
  Claude Design queda para decks/presentaciones (fuera del alcance de este skill).
- **Directorio / tokens:** `/Users/ariel089/Workspaces/procontacto-delivery` (`.env` con los tokens).
- **Usuarios:** PMs / Delivery Managers.

---

## Gate de continuidad — ¿este proyecto ya venía trabajándose en otra conversación? (ADVISORY)

> Runbook completo en `_shared/session-continuity/gate.md`. Corre **una sola vez**, en cuanto sabés de qué proyecto se trata y **antes de crear nada**. **Nunca bloquea.**

Cada conversación de Cowork arranca sin memoria de las anteriores. Si el usuario ya venía trabajando esto en otra, acá se re-pregunta todo y —peor— se puede terminar duplicar el trabajo y **partir el backlog en dos tandas** para el mismo alcance. Cowork **no expone** las conversaciones del usuario, así que no intentes detectarlas ni linkearlas: lo que sí podés es leer la **huella del trabajo previo** y recomendarle volver.

1. Buscá actividad reciente del proyecto (`Project__c` y sus `Project_Asset__c` activos), con `LastModifiedDate` y `LastModifiedBy`. Sumá la huella de **Jira** (issues creados/modificados en las últimas 72 h, sprint activo) y de la carpeta de **Drive** del proyecto — pero sólo con los conectores que el skill ya iba a usar igual.
2. **Dos señales fuertes** (modificado en las últimas 72 h · por el mismo usuario · backlog o assets tocados hoy · onboarding a medias) → mostrá el aviso. Actividad de más de 30 días no cuenta.
3. Mostrá **la evidencia concreta** (qué, cuándo, quién) y después la recomendación, siempre condicional: *"si venías trabajando este proyecto en otra conversación, seguí ahí — vas a tener el contexto; acá arranco sin esa memoria"*. **Nunca inventes un link a la conversación.**
4. Ofrecé: **(a)** continuar acá levantando el contexto *(default)* · **(b)** frenar para ir a buscar la otra conversación — no escribas nada · **(c)** es otro alcance, crear igual.

**Salteá este paso** si el skill fue invocado encadenado desde otro skill en la misma conversación.

---

## Flujo

### PASO 0 — Pre-flight de conectores
Verificar que estén disponibles: **Salesforce**, **Google Drive** y **Atlassian (Jira)**. Si falta
alguno → detener y avisar cuál falta (sin empezar). Este skill no crea contenido visual, así que no
requiere Claude-in-Chrome.

### PASO 1 — Resolver el proyecto (desde `Project__c`)
1. Pedir la **cuenta o proyecto** (una pregunta). Resolver el `Project__c` en SF:
   ```soql
   SELECT Id, Name, Account__r.Name, RecordType.DeveloperName
   FROM Project__c
   WHERE Account__r.Name LIKE '%<texto>%'
   ORDER BY CreatedDate DESC
   ```
   Si hay varios, mostrar la lista y que el usuario elija. Si no hay ninguno → derivar a
   `pc-delivery-sf-project-builder` (este skill no crea el `Project__c`).
2. Leer los assets del proyecto (raíz Drive + proyecto Jira):
   ```soql
   SELECT Type__c, Value__c FROM Project_Asset__c
   WHERE Project__c = '<projectId>' AND Type__c IN ('GoogleDriveFolderId','JiraProjectKey','JiraProjectId','ClaudeProjectId')
   ```
   - **Sin `GoogleDriveFolderId`** → derivar a project-builder (no hay raíz para organizar).
   - **Sin proyecto Jira** → preguntar el key del proyecto Jira del cliente (o derivar a project-builder).
3. Determinar el **slug de cuenta** (para nombres) y el idioma del cliente si aplica.

### PASO 2 — Estructura de Drive
Crear el árbol de subcarpetas de `references/drive-tree.md` **dentro** de la carpeta raíz
(`GoogleDriveFolderId`). Reglas: **buscar antes de crear** (por `name` + `parentId`), no duplicar,
crear de arriba hacia abajo (nivel 1 → nivel 2). Mostrar el árbol resultante con links al final.

### PASO 3 — Artefactos visuales (Cowork)
Para cada artefacto **visual** del catálogo (`references/artifact-catalog.md`, columna Herramienta =
Cowork), preguntar si aplica al proyecto (los opcionales — ERD, arquitectura de integraciones — según
haya modelo de datos / integraciones). Este skill **no genera el contenido**: los visuales se
materializan como **artefactos de Cowork** con el skill de cada artefacto (wireframes →
`pc-crm-salesforce-wireframe-builder`; AS-IS/TO-BE/ERD/integraciones → su skill/Cowork). Para cada uno
confirmado:
- Si el artefacto **ya existe**, pedir/capturar su link del gestor (`artifacts.procontacto.com.mx/a/<uuid>`); si lo que aparece es un `claude.ai/code/artifact/<uuid>` viejo, tomalo como referencia y anotá que hay que republicarlo en el gestor.
- Si **no existe todavía**, marcarlo como *pendiente de link* para el PASO 4 y dejar anotado con qué
  skill se genera. No crear el contenido acá ni inventar el link (regla 6).

### PASO 4 — Issues `Artifact` en Jira (uno por entregable)
Por **cada entregable** del catálogo aplicable (documentos y artefactos visuales de Cowork):
1. Verificar el issuetype `Artifact` real con `getJiraIssueTypeMetaWithFields` (id/name, campos requeridos).
2. **Buscar** si ya existe un `Artifact` con ese summary en el proyecto → si existe, reusar (no duplicar).
3. Crear con `createJiraIssue`: `project` = proyecto Jira del cliente, `issuetype` = Artifact,
   `summary` = nombre del entregable, `description` = propósito + **link** (carpeta Drive para docs / URL
   de Cowork para visuales) + skill que lo produce (del catálogo). Si el link quedó pendiente → dejarlo
   explícito ("pendiente: generar el artefacto con {skill} y pegar el link").
4. **Verificación post-write:** releer con `getJiraIssue` y confirmar antes de reportar éxito.

### PASO 5 — Registro en Salesforce (limitado)
Registrar como `Project_Asset__c` **solo** los recursos con un valor de picklist válido en `Type__c`
(verificar con `getObjectSchema`). Los **artefactos visuales publicados en el gestor** sí tienen tipo
propio (`WireframeId` para wireframes, **`ProContactoArtifactId`** para el resto) → registrarlos con
`Value__c` = **el uuid en crudo** de `https://artifacts.procontacto.com.mx/a/<uuid>` y
**`Description__c`** con qué documento es (≤255: AS-IS, TO-BE, ERD, arquitectura…). Sin la
descripción, varios `ProContactoArtifactId` del mismo proyecto son indistinguibles entre sí.
`CoworkArtifactId` queda **sólo para leer registros viejos** — no se crean nuevos. Las subcarpetas de Drive normalmente **no** tienen un tipo propio → su
trazabilidad queda en el `Artifact` de Jira. No inventar tipos (regla 7). Mecánica canónica del gate
de vinculación: `_shared/artifact-linkage/artifact-linkage.md` (si está presente en el bundle).

### PASO 6 — Resumen final
Mostrar un panel/resumen con: árbol de Drive (con links), proyectos de Claude Design (con URL o
"pendiente"), issues `Artifact` creados (con link a Jira), y los pendientes de acción del DM.

---

## Frontera con otros skills

- **`pc-delivery-sf-project-builder`** — crea el `Project__c`, la carpeta **raíz** de Drive, el Claude
  *Project* (chat), Slack, Jira, etc. Este skill corre **después** y organiza el interior; project-builder
  ofrece el handoff a este skill al terminar (su PHASE 4). Cuando lo invoca project-builder, el `Project__c`
  ya está resuelto con su `GoogleDriveFolderId` y proyecto Jira → arrancar directo en el PASO 2. Si se corre
  suelto y falta la raíz Drive, derivar a project-builder.
- **`pc-delivery-blueprint-guide`** — dueño del **Modo D** (detectar docs/links sin registrar como
  `Artifact`). Este skill es la contraparte proactiva: deja los `Artifact` creados desde el arranque.
- **Skills que redactan cada entregable** (userstory-generator, data-dictionary-generator,
  wireframe-builder, sow-generator, etc.) — este skill **no** escribe su contenido; ver el catálogo.
- **`pc-delivery-jira-issue-builder`** — dueño canónico del CRUD de issues Jira. Si hace falta lógica
  compleja de campos/links, delegar; para el alta simple de `Artifact`, este skill la hace directo.

## Referencias
- `references/artifact-catalog.md` — catálogo canónico: artefacto → tipo → herramienta → skill que lo produce.
- `references/drive-tree.md` — árbol de subcarpetas por fase.
- `references/claude-design-chrome.md` — DEPRECADO para este skill (los visuales ya no se crean como
  proyectos de Claude Design; se materializan como artefactos de Cowork). Se conserva solo como
  referencia histórica de la mecánica Claude-in-Chrome.
- `references/jira-artifact.md` — mecánica de creación del issue `Artifact`.
