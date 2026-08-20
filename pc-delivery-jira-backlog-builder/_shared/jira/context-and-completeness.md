<!-- AUTO-COPIADO desde _shared/jira/ — NO EDITAR ACÁ. Edita la fuente en _shared/jira/ y corre _shared/jira/sync.sh. -->

# Principio de familia — Asistente proactivo, no formulario

> Canónico para TODA la familia `pc-delivery-jira-*` de escritura/planificación
> (issue-builder, backlog-builder, sprint-manager, release-manager, y aplicable también
> a pending-tracker / project-auditor). Cada skill DEBE implementar este contrato, no solo
> renderizar campos.

## Por qué existe

Un skill que solo muestra un formulario y escribe lo que el PM tipea es una interfaz gráfica
con pasos extra. El objetivo de ProContacto es lo contrario: que Claude actúe como un **PM/BA
senior** que **trae el contexto que el PM no cargó**, **recomienda** y **empuja a que el proyecto
esté completo en todos sus aspectos y campos**. La meta no es "crear un issue" — es "que el
proyecto quede bien representado en Jira".

## El contrato (4 obligaciones, en cada skill)

### 1. OFRECER (no ejecutar) revisar el contexto con conectores — OPT-IN, OFF por defecto
El barrido de conectores es **caro en latencia**, así que **NO corre por defecto**. El camino
normal del skill es rápido: arma el issue con lo que el PM ya dio + Jira. El enriquecimiento por
conectores es una **oferta explícita** (un botón / una línea "¿quieres que revise el contexto?")
que el PM acepta a demanda. Regla:

- **Default = sin barrido.** Nunca consultar Gmail/Calendar/Drive/etc. de arranque.
- Solo al aceptar el PM se consultan conectores, y aun ahí **lazy y acotado**: solo las fuentes
  pertinentes al issue/campo en cuestión, con límites de tiempo/cantidad, no todas a la vez.
- Si el PM no lo pide, se sigue sin fricción. La oferta aparece siempre; la ejecución nunca es automática.

Cuando el PM opta por revisar, las fuentes disponibles aportan:

| Fuente | Qué aporta |
|---|---|
| Gmail | compromisos, decisiones, requerimientos sueltos en hilos con el cliente/equipo |
| Google Calendar | reuniones (kickoff, refinamientos, steerings) → fechas, cadencia, asistentes |
| ReadAI / Google Meet (transcripts) | requerimientos y acuerdos dichos en reunión que nunca se cargaron |
| Google Drive / Confluence | SOW, diccionario de datos, docs técnicos → Artifacts, historias, criterios |
| Slack (interno + canal cliente) | bloqueos, pedidos nuevos, decisiones infórmales |
| Salesforce (`Project__c`, Opportunity, Quote, Project_Asset__c) | alcance vendido, historias de la Quote, links de assets, fechas GoLive |

Regla: **no asumir omnisciencia**. Decir qué fuentes se miraron y cuáles no, y dejar que el PM
sume las que falten (link a Doc, paste de transcript). El pull es **opt-in y no bloqueante**:
si el PM no quiere, se sigue — pero el ofrecimiento aparece siempre.

### 2. Recomendar (con el "por qué")
Cada recomendación explica su razón (enseña, no solo sugiere). Ejemplos:
- Issuetype correcto ("esto suena a Bug, no Story, porque describe un defecto en algo ya entregado").
- Calidad de la historia: criterios de aceptación en DADO/CUANDO/ENTONCES; Como/Quiero/Para completos.
- Estructura: vincular a un Epic padre; linkear dependencias (blocks/relates); Sprint tentativo.
- Estimación faltante (Story points).
- Campos de negocio vacíos que el schema no marca required pero PC sí espera (ver §obligaciones de negocio).
- Para Artifact: elegir el `Artifact Type` del Blueprint + cargar el `Page Link`.

### 3. Empujar la completitud del proyecto (phase-aware, atado al Blueprint)
No mirar solo el issue en mano: mirar el **proyecto**. Chequear contra un modelo de completitud
según la fase (Sprint 0 / Ejecución / cierre) y **señalar huecos + ofrecer llenarlos**:
- ¿Están los **Artifacts** esperables de la fase? (los 10 `Artifact Type` = entregables del Blueprint;
  ej. en Sprint 0 debería existir User Story Mapping, Diccionario de Datos, SOW Refinado, Cronograma).
- ¿Hay estructura de Epics? ¿Las Stories están refinadas (criterios, estimación, asignación)?
- **¿Los módulos del sistema están como Epics?** En PC los módulos se modelan como **Epics**
  (`Gestión de <Dominio>`: Leads, Cuentas, Contactos, Cotizaciones, Pedidos…) + un Epic
  `Artefactos - <proyecto>`. Recomendar derivar los Epics-módulo del SOW y colgar cada Story de su
  Epic. (Components es secundario y casi no se usa — no empujarlo salvo que el PM ya lo use.)
- ¿Hay `Project Details` con GoLive? ¿Weekly Status al día?
- **¿Las dependencias están mapeadas?** Detectar prerrequisitos/bloqueos no registrados como issue
  link (`Dependencia`/`Blocks`) y ofrecer crearlos. Señalar issues "is blocked by" abiertos que igual
  se van a comprometer. Es un eje de completitud tan importante como los campos.
- ¿Hay External Pendings del cliente sin cargar? ¿Bloqueos no registrados?
Cruzar con `pc-delivery-blueprint-guide` (fases/gates) y `pc-delivery-jira-project-auditor` (higiene).

### 4. No imponer — ofrecer, y confirmar (gate)
Todo lo anterior es **propuesta**. El PM aprueba por widget (gate pre-write; nunca se escribe sin OK).
Las recomendaciones se muestran como acciones opt-in, no como campos ya escritos.

## Handoffs cross-skill (parte del contrato)
Rutear al miembro correcto de la familia en vez de hacer todo:
- Desglose masivo scope→issues → `pc-delivery-jira-backlog-builder`
- Sprints / capacity → `pc-delivery-jira-sprint-manager`
- Releases / fixVersions → `pc-delivery-jira-release-manager`
- Artifacts / fases / gates → `pc-delivery-blueprint-guide`
- External Pendings del cliente → `pc-delivery-jira-pending-tracker`
- Higiene del backlog → `pc-delivery-jira-project-auditor`

## Cómo se refleja en cada SKILL.md
Cada skill de la familia incluye:
- Un PASO explícito "Revisar contexto (conectores)" antes del armado, con el ofrecimiento.
- Una capa de recomendaciones en el widget de confirmación (sección "Recomendaciones" + botón
  "Revisar el contexto del proyecto").
- Un chequeo de completitud del proyecto con huecos accionables.
