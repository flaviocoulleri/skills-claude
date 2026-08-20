---
name: pc-delivery-jira-release-manager
metadata:
  version: 0.2.0
  last_modified: 2026-08-06
  status: beta
description: >
  Gestiona las releases (fixVersions) de un proyecto en Jira ProContacto: crea versiones, les
  asigna issues, arma release notes/changelog y las marca como released. NO es un formulario:
  recomienda con el porqué (issues Done sin versión asignada, alcance de la versión incompleto,
  fecha de release vs GoLive del Project Details) y OFRECE (opt-in, sin barrer por defecto) revisar
  el contexto con conectores. Confirma por widget antes de escribir (gate pre/post-write, nunca sin
  OK). Activar con "crea la release", "arma la versión", "asigna estos issues a la versión",
  "marca la release como liberada", "genera las release notes", "qué entra en la próxima release",
  "create/release version". Orientado a PMs/Scrum Masters/Release Managers. Funciona en español e inglés.
---

<!-- Changelog
0.1.0 (2026-07-13): ESQUELETO / DRAFT. Flujo de releases sobre la API de versions
(/rest/api/3/project/{key}/versions, /version) validada en vivo. Embebe el principio de familia
(context-and-completeness.md, contexto OPT-IN). Widget de armado de versión + release notes. Nota:
varios proyectos PC no usan versions (AA200 tenía 0) → el skill puede arrancar el uso desde cero.
Falta: smoke test, ratificación meta + .skill.
-->

# Skill: Gestión de releases (fixVersions) en Jira

## Descripción
Maneja el ciclo de versiones/releases de un proyecto: crear una versión, asignarle issues, armar las
release notes y marcarla como released. Muchos proyectos de PC todavía no usan fixVersions (AA200
tenía 0) — el skill puede **arrancar la práctica desde cero** y recomendar qué versionar.

> 🧪 **BETA — en pruebas con el equipo delivery.** Esquema real cableado y validado end-to-end; se está afinando el runtime. Reporta lo que encuentres. Ver TODO al final.

## Principio rector (NO es un formulario)
Implementa `_shared/jira/context-and-completeness.md`: recomienda con el porqué usando lo que ya hay
(Jira), y **ofrece** (no ejecuta) enriquecer con conectores. Barrido **OPT-IN y OFF por defecto**.

## Fuente de verdad
- `_shared/jira/fields-by-issuetype.md` (fixVersion; `Project Details` tiene GoLive `customfield_10161`).
- `_shared/jira/context-and-completeness.md` (principio).
- API: `GET/POST /rest/api/3/project/{key}/versions`, `POST/PUT /rest/api/3/version/{id}` (crear/editar/marcar released),
  asignar issues vía el campo `fixVersions` en `editJiraIssue`.
- Campos de la versión (validado en pantalla Create release IMPNTR): **name*** (req), **startDate**,
  **releaseDate**, **driver** (usuario responsable, default = usuario actual), **description**.

## Alcance y límites
- **SÍ**: crear versión, editar (fechas/descripción), asignar issues, marcar released/archived, armar release notes.
- **NO**: borrar una versión con issues asignados sin reasignar (avisar primero).
- **NO**: crear issues — delega al `issue-builder`.
- Marcar released es un hito visible: solo con OK explícito.

## Herramientas requeridas
- **Atlassian MCP** (versions + `editJiraIssue` + `searchJiraIssuesUsingJql`).
- **Widgets**: `mcp__visualize__show_widget`.
- **Conectores de contexto (opt-in)**: Salesforce (`Project__c` GoLive, `Project Details` en Jira), Drive/Confluence (notas de versión previas).

## Restricciones (gate)
- **NUNCA** crear/asignar/marcar released sin OK explícito vía widget.
- Escrituras una por una + verificación post-write.
- Al marcar released, chequear que no queden issues abiertos en la versión y avisar si los hay.

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
### PASO 0 — Preflight + identidad.
### PASO 1 — Proyecto + intención
Elegir proyecto; traer versiones (`/project/{key}/versions`). Detectar: crear / asignar issues / release notes / marcar released.
### PASO 2 — Armar propuesta + recomendaciones (sin conectores)
- Issues **Done sin fixVersion** → candidatos a la versión (recomendar con el porqué).
- Consistencia de fechas: `releaseDate` vs GoLive del `Project Details`.
- Alcance: agrupar por Epic; señalar issues abiertos que no deberían entrar.
### PASO 3 — Oferta de contexto (OPT-IN)
Botón "Revisar el contexto": SF `Project__c` (GoLive comprometido), docs de versión previas. Solo si el PM lo pide.
### PASO 4 — Revisión (widget, gate)
`assets/release-plan.html`: nombre/fechas/descripción de la versión, lista de issues candidatos con
toggle incluir, y preview de **release notes** (agrupadas por tipo/Epic). El PM confirma. Nada antes del OK.
### PASO 5 — Ejecutar
Crear versión (`POST /version`), asignar `fixVersions` a los issues (`editJiraIssue`, una por una),
opcionalmente marcar released (`PUT /version/{id}` con `released:true`).
### PASO 6 — Verificar + reportar (releer versión + issues asignados + link).
### PASO 7 — Handoff: Acceptance Certificate / Checklist Pasaje a Producción (`issue-builder`/`blueprint-guide`), weekly status (`auditor`).

## Reglas de negocio / no obvias
- **Releases = MVPs**: en PC las versiones se usan como hitos **MVP** (naming `MVP N`; ej. proyecto real
  CMIB4B con "MVP 3" en la fila Releases de la Timeline). Proponer ese naming salvo que el proyecto use otro.
- **Release notes** = derivadas de los issues de la versión (summary + tipo), agrupadas por Epic; editable antes de publicar.
- **No versionar issues abiertos** salvo que el PM lo pida (una release debería contener trabajo terminado).
- **GoLive**: si la fecha de la versión contradice el GoLive del `Project Details`, avisar (aviso blando, no bloquea).

## Archivos referenciados
| Archivo | Cuándo | Estado |
|---|---|---|
| `_shared/jira/fields-by-issuetype.md` | PASO 2 — fixVersion / GoLive | ✅ |
| `_shared/jira/context-and-completeness.md` | PASO 3 — principio | ✅ |
| `assets/release-plan.html` | PASO 4 — widget de versión + notes | ✅ (smoke test pendiente) |

## TODO antes de 1.0.0
1. Smoke test end-to-end (crear versión + asignar issues en `ZCLAUDE`).
2. Ratificar nombre + distribución con `pc-meta-skill-manager` + tarea PROCSKILLS.
3. Generar `.skill` + deploy Cowork.
