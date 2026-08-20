---
name: pc-delivery-jira-backlog-builder
metadata:
  version: 0.2.0
  last_modified: 2026-08-06
  status: beta
description: >
  Construye el backlog de un proyecto en Jira ProContacto a partir del alcance: desde un SOW/Doc
  de Drive, una Quote/Opportunity de Salesforce, un transcript o un Epic a desglosar → propone una
  estructura Epics → Stories → Sub-tasks con Como/Quiero/Para, criterios de aceptación DADO/CUANDO/
  ENTONCES, estimación y sprint tentativo, y la crea en Jira reusando el núcleo
  pc-delivery-jira-issue-builder. NO es un formulario: recomienda con el porqué y OFRECE (opt-in,
  sin barrer por defecto) revisar el contexto con conectores para detectar huecos y duplicados.
  Deduplica contra lo existente y confirma por widget antes de escribir (gate pre/post-write,
  nunca sin OK). Activar con "arma el backlog", "pasa el SOW a Jira", "desglosa este Epic en
  historias", "crea las historias del proyecto", "carga el backlog desde la Quote", "build the
  backlog". Orientado a PMs/BAs/Scrum Masters. Funciona en español e inglés.
---

<!-- Changelog
0.1.0 (2026-07-13): ESQUELETO / DRAFT. Flujo scope→backlog→Jira sobre el esquema real de
_shared/jira/ y delegando la escritura al núcleo pc-delivery-jira-issue-builder. Embebe el
principio de familia (context-and-completeness.md) con contexto OPT-IN/off por defecto.
Widget de revisión del árbol construido. Falta: parser de fuentes afinado, dedup en runtime,
smoke test end-to-end, ratificación meta + .skill.
-->

# Skill: Construcción del backlog en Jira (scope → Epics/Stories/Sub-tasks)

## Descripción

Toma el **alcance** de un proyecto y lo materializa como backlog en Jira: propone la estructura
`Epic → Story → Sub-task` con los campos reales de PC (Como/Quiero/Para, criterios, estimación,
sprint tentativo) y la crea. Es la contraparte **masiva** del `issue-builder`: por cada nodo del
árbol delega la escritura en el núcleo `pc-delivery-jira-issue-builder` (mismo mapeo de fields,
mismo ADF, mismo gate).

> 🧪 **BETA — en pruebas con el equipo delivery.** Esquema real cableado y validado end-to-end; se está afinando el runtime. Reporta lo que encuentres. Ver TODO al final.

## Principio rector (NO es un formulario)

Implementa el contrato `_shared/jira/context-and-completeness.md`: recomienda con el porqué y
**ofrece** (no ejecuta) enriquecer con conectores. El **input principal** (SOW/Quote/transcript)
lo da el PM explícitamente — eso no es un barrido. El **barrido amplio** de conectores
(Gmail/Slack/Calendar para cruzar y detectar huecos) es **OPT-IN y OFF por defecto** (encarece la
latencia); solo corre si el PM lo pide, y ahí lazy y acotado.

## Fuente de verdad del esquema
- `_shared/jira/fields-by-issuetype.md` (fields/picklists/statuses; **ADF** en textareas).
- `_shared/jira/issuetypes-and-workflows.md` (IDs) y `screen-schemes.md`.
- `_shared/jira/context-and-completeness.md` (principio de familia).
- Reusa `pc-delivery-jira-issue-builder` para el write de cada issue.

## Alcance y límites
- **SÍ**: parsear alcance → árbol Epic/Story/Sub-task, estimar, sugerir sprint, crear en batch (con OK).
- **NO**: borrar; transiciones masivas; crear External Pending (→ pending-tracker), Weekly Status (→ auditor).
- **NO**: inventar historias sin fuente — todo nodo se ancla a una parte del alcance provisto.
- **NO** duplica lo que ya existe en el proyecto (dedup obligatorio).

## Herramientas requeridas
- **Atlassian MCP**: igual que issue-builder (`createJiraIssue`, `getJiraIssueTypeMetaWithFields`,
  `searchJiraIssuesUsingJql`, parent linking, etc.).
- **Widgets**: `mcp__visualize__show_widget`.
- **Fuente del alcance (según elija el PM)**: Google Drive (SOW/Doc), Salesforce (Quote/Opportunity/
  QLI), Confluence, o paste de transcript. **Conectores de cruce** (Gmail/Slack/Calendar/ReadAI):
  opcionales y opt-in.

## Restricciones (gate de escritura — contrato de la casa)
- **NUNCA** crear en batch sin OK explícito del PM vía el widget de revisión del árbol.
- Gate pre-write: cada Story respeta las obligaciones de negocio (Como/Quiero/Para, criterios) del
  `issue-builder`; los required de sistema se validan contra la org.
- Escritura **una por una**, con verificación post-write; reportar fallas individuales.
- Dedup contra issues existentes antes de proponer.

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

## Flujo paso a paso

### PASO 0 — Preflight + identidad
`getAccessibleAtlassianResources` + `atlassianUserInfo` (idéntico a issue-builder). Sin Atlassian, fin.

### PASO 1 — Fuente del alcance (la da el PM)
Preguntar de dónde sale el backlog:
- **SOW / Doc de Drive** (link) — el PM lo pega.
- **Quote / Opportunity de Salesforce** — las historias vendidas (QLI) del deal (puente con `pc-sales-sf-quote-builder`).
- **Transcript / brief** (paste).
- **Epic existente a desglosar** (issue key).
No barrer nada todavía — solo se lee la fuente que el PM indica.

### PASO 2 — Proyecto destino + anclaje
Elegir proyecto Jira (`getVisibleJiraProjects`). Definir si los Epics son nuevos o se cuelga de uno existente.

### PASO 3 — Generar el árbol propuesto
Leer `references/backlog-generation.md`. Parsear la fuente → `Epic → Story → Sub-task` con, por Story:
summary imperativo, Como/Quiero/Para, criterios DADO/CUANDO/ENTONCES, estimación (story points) y
sprint tentativo. Cada nodo **anclado** a la parte del alcance de la que sale (trazabilidad).

### PASO 3.5 — Recomendaciones + oferta de contexto (OPT-IN)
Como en el issue-builder: recomendar con lo que ya se tiene (huecos de estructura, historias sin
criterios, estimaciones faltantes) SIN conectores. **Ofrecer** (botón) cruzar con conectores para
detectar alcance no cubierto o duplicados — solo si el PM lo pide.

### PASO 4 — Dedup + revisión del árbol (widget, gate)
`searchJiraIssuesUsingJql` sobre el proyecto → marcar nodos que ya existen (fuzzy por summary).
Cargar `assets/backlog-review.html`: árbol editable con toggles incluir/excluir por nodo, edición
inline de summary/estimación/sprint, y badges de "ya existe". El PM confirma el subset. **Nada se
escribe antes del OK.**

### PASO 5 — Crear en batch (delegando al núcleo)
Por cada nodo aprobado, en orden Epic → Story → Sub-task (para poder linkear el parent):
`createJiraIssue` con el mapeo del `issue-builder` (**ADF** en textareas). Una por una.

### PASO 6 — Verificar + reportar
Releer (`getJiraIssue`) una muestra; reportar en chat el árbol creado con links y el conteo
(creados / omitidos por duplicado / fallidos).

### PASO 7 — Handoff
Ofrecer próximos pasos: planificar sprints (`pc-delivery-jira-sprint-manager`), registrar Artifacts
del Blueprint (`pc-delivery-blueprint-guide`), o cargar External Pendings (`pending-tracker`).

---

## Reglas de negocio / no obvias
- **Trazabilidad**: cada Story cita la sección del SOW/QLI de la que sale (en description o comentario).
- **Estimación**: heurística en `references/backlog-generation.md`; si no hay base, marcar "sin estimar" y recomendarlo, no inventar.
- **Dedup agresivo**: ante duda, marcar como existente y no duplicar.
- **Sprint tentativo ≠ compromiso**: se sugiere, el PM decide; la planificación fina es del sprint-manager.
- **Delegación real**: el write vive en el issue-builder — no reimplementar el mapeo de fields acá.

---

## Archivos referenciados
| Archivo | Cuándo | Estado |
|---|---|---|
| `_shared/jira/fields-by-issuetype.md` | PASO 3/5 — fields + ADF | ✅ |
| `_shared/jira/context-and-completeness.md` | PASO 3.5 — principio | ✅ |
| `references/backlog-generation.md` | PASO 3 — parser + estimación + dedup | ⏳ TODO |
| `assets/backlog-review.html` | PASO 4 — widget del árbol | ✅ (smoke test pendiente) |

## TODO antes de 1.0.0
1. Afinar `references/backlog-generation.md` (parser por tipo de fuente, heurística de estimación, dedup).
2. Smoke test end-to-end en `ZCLAUDE` (SOW de prueba → árbol → creación con parents).
3. Ratificar nombre + distribución con `pc-meta-skill-manager` + tarea PROCSKILLS.
4. Generar `.skill` + deploy Cowork.
