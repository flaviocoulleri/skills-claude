---
name: pc-delivery-jira-sprint-manager
metadata:
  version: 0.2.0
  last_modified: 2026-08-06
  status: beta
description: >
  Gestiona los sprints de un proyecto en Jira ProContacto vía la Agile API: crea sprints,
  los inicia y cierra, mueve issues dentro/fuera del sprint y ayuda a planificar la capacity.
  NO es un formulario: recomienda con el porqué (historias sin estimar antes de comprometer,
  carry-over del sprint anterior, sobre/sub-carga vs capacidad) y OFRECE (opt-in, sin barrer por
  defecto) revisar el contexto con conectores (Calendar para disponibilidad/feriados, Slack para
  bloqueos). Confirma por widget antes de escribir (gate pre/post-write, nunca sin OK). Delega la
  creación/edición de issues sueltos al núcleo pc-delivery-jira-issue-builder. Activar con
  "arma el sprint", "planifica el próximo sprint", "inicia/cierra el sprint", "meté estas historias
  al sprint", "cuánto entra en el sprint", "capacity del equipo", "plan sprints", "start/close
  sprint". Orientado a PMs/Scrum Masters. Funciona en español e inglés.
---

<!-- Changelog
0.1.0 (2026-07-13): ESQUELETO / DRAFT. Flujo de gestión de sprints sobre la Agile API
(/rest/agile/1.0/) validada en vivo (AA200 → board 482 scrum). Embebe el principio de familia
(context-and-completeness.md, contexto OPT-IN). Widget de planificación con capacity. Falta:
smoke test end-to-end, ratificación meta + .skill. Extrae/amplía lo que hacía a medias el auditor.
-->

# Skill: Gestión de sprints en Jira (crear / iniciar / cerrar / planificar)

## Descripción
Maneja el ciclo de sprints de un proyecto: crear, iniciar, cerrar, mover issues y planificar la
capacity. Extrae y amplía lo que hoy hace parcialmente `pc-delivery-jira-project-auditor` (que
queda en higiene/diagnóstico). Para crear/editar issues sueltos delega en el núcleo
`pc-delivery-jira-issue-builder`.

> 🧪 **BETA — en pruebas con el equipo delivery.** Esquema real cableado y validado end-to-end; se está afinando el runtime. Reporta lo que encuentres. Ver TODO al final.

## Principio rector (NO es un formulario)
Implementa `_shared/jira/context-and-completeness.md`: recomienda con el porqué usando lo que ya
hay (Jira), y **ofrece** (no ejecuta) enriquecer con conectores. El barrido de conectores es
**OPT-IN y OFF por defecto** (latencia); solo corre si el PM lo pide, lazy y acotado.

## Fuente de verdad
- `_shared/jira/fields-by-issuetype.md` (Sprint = `customfield_10020`, story points = `customfield_10016`; statuses).
- `_shared/jira/context-and-completeness.md` (principio).
- Agile API: `/rest/agile/1.0/board?projectKeyOrId=<KEY>`, `/board/{id}/sprint`,
  `POST /sprint`, `POST /sprint/{id}` (state=active/closed), `POST /sprint/{id}/issue` (mover issues).
- Campos del sprint (validado en pantalla Edit sprint IMPNTR): **name*** (req), **duration**
  (1/2/3/4 weeks o custom → autocalcula end), **start date** (con hora), **end date** (con hora), **sprint goal**.

## Alcance y límites
- **SÍ**: crear sprint, iniciar/cerrar, mover issues, sugerir plan de capacity.
- **NO**: borrar sprints con issues sin reubicar (avisar y reubicar primero); transiciones de estado de issues en masa (eso es del auditor, fila por fila).
- **NO**: crear issues nuevos — delega al `issue-builder`.
- Cerrar un sprint mueve los issues no terminados: preguntar destino (backlog o siguiente sprint), nunca decidir solo.

## Herramientas requeridas
- **Atlassian MCP** + Agile API (vía `fetch` a `/rest/agile/1.0/` — la Agile API no está en createmeta).
- **Widgets**: `mcp__visualize__show_widget`.
- **Conectores de contexto (opt-in)**: Google Calendar (disponibilidad/feriados → capacity real), Slack (bloqueos).

## Restricciones (gate)
- **NUNCA** iniciar/cerrar/mover sin OK explícito vía widget.
- Solo opera si el caller tiene rol lead/admin del board.
- Escrituras una por una + verificación post-write.
- Cerrar sprint: confirmar explícitamente el destino de los issues no terminados.

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
### PASO 0 — Preflight + identidad (igual a issue-builder).
### PASO 1 — Proyecto + board
Elegir proyecto; descubrir board vía `/rest/agile/1.0/board?projectKeyOrId=<KEY>`. Si hay varios, preguntar.
### PASO 2 — Intención
Detectar: crear / iniciar / cerrar / mover issues / planificar. Traer sprints (`/board/{id}/sprint`): activo, futuros, cerrado reciente.
### PASO 3 — Armar la propuesta + recomendaciones (sin conectores)
Según intención: capacity sugerida (velocity histórica de sprints cerrados), candidatos del backlog
priorizados, carry-over del sprint activo. Recomendar con el porqué: "estas historias no tienen
estimación → estima antes de comprometer"; "vas 42 pts sobre una velocity de 30"; "3 historias del
sprint activo quedaron sin terminar → carry-over".
### PASO 3.5 — Oferta de contexto (OPT-IN)
Botón "Revisar el contexto": Calendar (feriados/PTO → capacity real), Slack (bloqueos que afectan el plan). Solo si el PM lo pide.
### PASO 4 — Revisión (widget, gate)
`assets/sprint-plan.html`: sprint objetivo (o crear nuevo con nombre/fechas/goal), lista de candidatos
con estimación y toggle incluir, medidor de capacity (Σ pts vs capacidad). El PM confirma. Nada se escribe antes del OK.
### PASO 5 — Ejecutar
Crear sprint (`POST /sprint`), mover issues (`POST /sprint/{id}/issue`), iniciar/cerrar (`POST /sprint/{id}` con state). Una por una.
### PASO 6 — Verificar + reportar (releer sprint + conteo de issues).
### PASO 7 — Handoff: refinar historias (`issue-builder`), higiene (`project-auditor`), weekly status (`auditor`).

## Reglas de negocio / no obvias
- **Sprint tentativo del backlog-builder ≠ compromiso**: acá se planifica en firme.
- **Capacity**: base = velocity de los últimos sprints cerrados; ajustar por disponibilidad solo si el PM trae el contexto de Calendar (opt-in).
- **Dependencias/bloqueos**: al elegir candidatos, avisar si un issue tiene un link `is blocked by` /
  `Se requiere primero` abierto — meter algo bloqueado al sprint es riesgo (recomendar, no impedir).
  Tipos de link en `_shared/jira/fields-by-issuetype.md`.
- **Naming de sprint**: el default real de Jira es `<Proyecto> Sprint N` (ej. "IMPNTR Sprint 1"),
  con fechas cargadas aparte (`Add dates`). Respetar ese patrón salvo que el board ya use otro;
  no imponer `Sprint N — DD/MM`.
- **Board pre-crea un sprint vacío** ("Sprint 1"): al planificar, reusar el sprint existente si está vacío en vez de crear otro.
- **Cerrar sprint**: los no terminados van a backlog o al siguiente, según elija el PM.

## Archivos referenciados
| Archivo | Cuándo | Estado |
|---|---|---|
| `_shared/jira/fields-by-issuetype.md` | PASO 3 — Sprint/story points/statuses | ✅ |
| `_shared/jira/context-and-completeness.md` | PASO 3.5 — principio | ✅ |
| `assets/sprint-plan.html` | PASO 4 — widget de planificación | ✅ (smoke test pendiente) |

## TODO antes de 1.0.0
1. Smoke test end-to-end (crear sprint + mover issues en `ZCLAUDE` — requiere board; asignar workflow scheme antes).
2. Ratificar nombre + distribución con `pc-meta-skill-manager` + tarea PROCSKILLS.
3. Coordinar el recorte del `project-auditor` (que deje de crear sprints).
4. Generar `.skill` + deploy Cowork.
