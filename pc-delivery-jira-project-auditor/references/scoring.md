# Scoring de salud del proyecto — detalle

Spec completa de cómo el skill calcula el score de salud. Este archivo se carga **sólo** cuando el modelo necesita el detalle exacto de pesos y dimensiones — el SKILL.md tiene un overview corto que basta para casos típicos.

## Detección de fase

Antes del scoring, decidir en qué fase está el proyecto:

- **Sprint 0 / relevamiento**: no hay sprints cerrados (o sólo hay un sprint llamado `Sprint 0` / `Discovery` / `Relevamiento`), no hay `fixVersions` released, los issues son mayoritariamente Tasks de descubrimiento. Cruzar con Salesforce: `Project__c.Stage__c IN ('Discovery')` confirma la fase.
- **Ejecución**: hay sprints cerrados anteriores **o** al menos una `fixVersion` con `releaseDate` pasada **o** `Project__c.Stage__c IN ('Build', 'UAT', 'Hypercare')`.
- **Indeterminado**: heurística no concluyente. El skill avisa y degrada a dimensiones genéricas.

## Dimensiones — fase Sprint 0 / relevamiento

Cada dimensión devuelve `0-100`. El score general es promedio ponderado.

| Dimensión | Peso | Cómo se mide |
|---|---|---|
| Plan de reuniones | 30 | Eventos en Google Calendar próximos 21 días con palabras clave (`kickoff`, `relevamiento`, `discovery`, `refinement`, `descubrimiento`) y al menos un asistente del dominio del cliente. Score = min(100, eventos × 25). |
| Nivel de interacción | 20 | Detectar interacción real con cliente y equipo en los últimos 14 días, sumando señales de los conectores disponibles: emails (Gmail con dominio cliente), threads de Slack en canal externo del cliente, comentarios en Confluence del space del proyecto. Si todos los conectores están ausentes, esta dimensión se omite y se reparte su peso entre las demás. Score = min(100, señales × 5). |
| Documentación inicial | 20 | Existe al menos 1 página en Confluence creada o editada en el space del proyecto en los últimos 30 días. 0 páginas = 0, 1 = 60, 3+ = 100. |
| Roles definidos | 15 | `Project__c` en Salesforce tiene Owner (PM), Tech_Lead__c y Account asignados. Cada rol presente vale 33. |
| Fecha objetivo de cierre Sprint 0 | 15 | Existe una `fixVersion` o sprint planeado con `releaseDate` o `endDate` definida para cerrar la fase. Sí = 100, no = 0. |

## Dimensiones — fase Ejecución

**Regla común a todas las dimensiones de Ejecución (desde v1.13.2)**: se calculan **siempre sobre el sprint activo**, nunca sobre todo el backlog ni sobre sprints futuros. PC trabaja sprint a sprint — los issues de sprints futuros típicamente no tienen los campos completos y eso es esperable, no un problema. La excepción es "Plan de sprints" que mira el plan macro a través de varios sprints.

| Dimensión | Peso | Cómo se mide |
|---|---|---|
| Historias cargadas | 20 | % de capacidad del **sprint activo** cubierta por Stories vs vacío. Capacidad = sum(estimación). Si no hay estimaciones, count > 5 issues = 100, sino prorrateado. |
| Asignaciones | 20 | % de issues **del sprint activo** con `assignee != null`. |
| Estimaciones | 15 | % de issues **del sprint activo** con `customfield_storyPoints` o `timeoriginalestimate` definidos. |
| Fechas | 10 | % de issues **del sprint activo** con `duedate` dentro del rango del sprint (`startDate` ≤ duedate ≤ `endDate`). |
| Dependencias explícitas | 15 | % de issues **del sprint activo** que tienen al menos un `issuelink` (excluyendo `clones`). Issues que claramente no necesitan dependencia cuentan como OK. La sub-detección B1 de Slack puede bajar este score si detecta gaps (ver `slack-integration.md`). |
| Epics / agrupación | 10 | % de issues **del sprint activo** con `Epic Link` (customfield_10014) definido. |
| Distribución de carga | 10 | Coeficiente de variación (CV) de issues por assignee, **calculado sobre el sprint activo**. CV ≤ 0.3 = 100, 0.3-0.6 = 70, > 0.6 = 30 (penaliza concentración fuerte). |
| Plan de sprints | 15 | **Excepción a la regla** — esta dimensión sí mira más allá del sprint activo: hay sprint activo (40%), hay siguiente sprint planeado con startDate (30%), cadencia consistente — duración entre sprints anteriores con CV < 0.2 (30%). 0% si el proyecto no tiene ningún sprint creado. Detalle en `sprint-planning.md`. |

**Si no hay active sprint** (proyecto en Sprint 0, entre sprints, o board kanban sin sprints): las dimensiones que dependen del sprint activo se omiten y se reparte su peso entre las que sí pueden calcularse. Si todas dependen del sprint, la fase se reclasifica como "Indeterminada" y se aplica el set genérico de fallback.

## Dimensiones — fase Indeterminada (fallback genérico)

Si la heurística no decide, sólo aplican estas tres y se calcula el score sobre ellas:

| Dimensión | Peso |
|---|---|
| Asignaciones | 40 |
| Fechas | 30 |
| Releases | 30 |

## Escala letra → número

| Letra | Rango | Color del badge |
|---|---|---|
| A | 90-100 | `--color-text-success` |
| B | 75-89 | `--color-text-success` |
| C | 60-74 | `--color-text-warning` |
| D | 40-59 | `--color-text-danger` |
| F | 0-39 | `--color-text-danger` |

## Score por sprint (histórico, on-demand)

El **score general** se calcula sobre el sprint activo (o todo el proyecto si está en Sprint 0). El **histórico por sprint** no se carga por defecto — multiplica el costo de queries. Aparece como botón **"Ver histórico ↗"** en el widget del PASO 2: cuando el PM lo dispara, el skill trae los últimos 5 sprints cerrados, calcula el score de cada uno con las dimensiones de fase Ejecución, y renderiza un widget secundario con una mini tabla y una sparkline de tendencia.

## Accionables derivados del scoring

Cuando una dimensión saca score < 60, se agrega un botón global correspondiente al widget del PASO 2 (suma a los 4 botones priorizados por categoría de hallazgo):

| Dimensión floja | Botón accionable nuevo | Prompt que dispara |
|---|---|---|
| Plan de reuniones (Sprint 0) | "Arma la agenda de relevamiento ↗" | `Para el proyecto <KEY> en Sprint 0, propón una agenda de reuniones de relevamiento de las próximas 3 semanas (kickoff, discovery con cliente, refinement interno, sync con stakeholders). Tirame los drafts de eventos para que los cree en Calendar — sin crear nada hasta mi OK.` |
| Nivel de interacción (Sprint 0) | "Sugerime cómo abrir interacción con el cliente ↗" | `Para el proyecto <KEY>, no detecté interacción reciente con el cliente. Propón un plan de outreach: email de status, mensaje en canal Slack externo, próxima reunión a coordinar. Sin enviar nada hasta mi OK.` |
| Documentación inicial (Sprint 0) | "Crear página de relevamiento en Confluence ↗" | `Crea un draft de página de relevamiento en el space Confluence del proyecto <KEY>: secciones objetivos, stakeholders, scope inicial, riesgos identificados. Sin publicar hasta mi OK.` |
| Asignaciones < 80% (Ejecución) | (ya existe) "Asignar por histórico" | — |
| Estimaciones < 80% | "Pedir estimaciones al equipo ↗" | (ver `slack-integration.md`, categoría Seguimiento al equipo) |
| Distribución de carga (CV > 0.6) | "Rebalancear el sprint ↗" | `Muestra el histograma de carga del sprint activo de <KEY> (issues por assignee) y propón redistribuciones concretas para nivelar. Sin reasignar nada hasta mi OK.` |
| Dependencias explícitas < 50% | "Detectar dependencias implícitas ↗" | `Analiza los issues del sprint activo de <KEY> y propón qué dependencias deberían existir (basado en summaries y descripciones que se referencien entre sí). Sin agregar issuelinks hasta mi OK.` |
| Plan de sprints (Ejecución) < 60 | "Crear plan de sprints ↗" | `El proyecto <KEY> no tiene un plan de sprints saludable. Detéctame el estado actual (sprints existentes, cadencia histórica) y ármame un widget de PASO 3 para crear los próximos N sprints. Sin crear nada hasta mi OK.` |
| Plan de sprints (Sprint 0) sin cierre planeado | "Planificar cierre de Sprint 0 ↗" | `El proyecto <KEY> está en Sprint 0 sin fecha de cierre planeada. Ármame un widget para crear UN sprint de cierre con fecha objetivo. Sin crear nada hasta mi OK.` |
