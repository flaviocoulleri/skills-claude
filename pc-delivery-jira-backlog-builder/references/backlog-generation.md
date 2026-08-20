# Generación del backlog — parser, estimación y dedup

> Lo lee el skill en el PASO 3. El write de cada nodo lo hace el núcleo
> `pc-delivery-jira-issue-builder` (mapeo de fields + ADF). Acá va solo la lógica de armado.

## Diferenciación vs el create nativo
El backlog del board ya ofrece "generate work items from Confluence, Loom, or an image" (AI nativo,
un item plano por vez). El valor de este skill: parte de **SOW/Quote de Salesforce**, arma un **árbol
estructurado** Epic→Story→Sub-task con los campos de PC (Como/Quiero/Para/criterios/estimación),
**deduplica**, propone **dependencias** y empuja **completitud** (Components/módulos). No compite con
el create suelto; lo complementa a nivel proyecto.

## Parser por tipo de fuente

### SOW / Doc de Drive
- Estructura típica: secciones = candidatas a **Epic**; ítems/requerimientos = **Story**;
  pasos técnicos = **Sub-task**.
- Extraer por Story: objetivo (→ Quiero), rol/usuario (→ Como), beneficio (→ Para), y condiciones
  de aceptación (→ Criterios DADO/CUANDO/ENTONCES). Si el SOW no las trae explícitas, redactarlas y
  marcarlas como "propuestas, revisar".

### Quote / Opportunity de Salesforce
- Las historias vendidas viven como Quote Line Items (puente con `pc-sales-sf-quote-builder`).
- Cada QLI de tipo historia → una Story. Agrupar por módulo/tema → Epics.
- Traer el nombre/desc& del producto (Product2) como base de la Story.

### Transcript / brief
- Extraer requerimientos concretos (no ruido). Confianza baja → no crear, listar como "a confirmar".

### Epic existente a desglosar
- Leer el Epic + su description → proponer las Stories/Sub-tasks que lo componen.

## Estimación (story points, `customfield_10016`)
- Heurística por tamaño relativo: XS=1, S=2, M=3, L=5, XL=8, XXL=13 (Fibonacci).
- Base para calibrar: si el proyecto ya tiene Stories estimadas, usar su distribución como ancla.
- **Sin base confiable → NO inventar**: dejar sin estimar y recomendar estimarlo en refinamiento.

## Sprint tentativo (`customfield_10020`)
- Sugerir agrupación por Epic/dependencias; es propuesta, no compromiso. La planificación fina
  es de `pc-delivery-jira-sprint-manager`.

## Dedup (obligatorio, PASO 4)
- `searchJiraIssuesUsingJql`: `project = "<KEY>" AND issuetype in (Story, Sub-task, Epic)`.
- Fuzzy match por summary (token-sort ratio ≥ 80) contra los nodos propuestos.
- Veredicto por nodo: `new` (crear) | `exists` (marcar, no duplicar). Ante duda → `exists`.

## Módulos = Epics (mecanismo real de PC)
- Las secciones/módulos del SOW mapean a **Epics** con naming `Gestión de <Dominio>` (ej. reales:
  Gestión de Leads, Cuentas (B2B), Contactos, Oportunidades, Cotizaciones, Pedidos, Listas de Precios,
  Visualización de Productos, Reportes y Dashboards, Cartera y Productividad del Ejecutivo).
- Crear también el Epic **`Artefactos - <proyecto>`** y colgar de ahí los Artifacts del Blueprint.
- Cada Story cuelga (parent) de su Epic-módulo. NO usar Components para modularizar (secundario en PC).
- El nivel Epic del árbol = los módulos; es lo primero a proponer desde la estructura del SOW.
- **Naming de Story por sub-alcance**: cuando un módulo se desglosa por perfil/proceso, usar
  `<Módulo> | <Variante>` (patrón real: "Gestión de Visitas | Gerentes Comerciales", "| SAC", "| Mediciones").
- Releases se usan como **MVPs** (`MVP N`): al proponer el árbol, se puede sugerir a qué MVP apunta cada módulo.

## Dependencias entre issues
- Detectar del alcance frases de orden/prerrequisito ("primero X, después Y", "requiere", "depende de",
  "una vez que…") → proponer links **`Dependencia`** (canónico PC: Y inward "Se requiere primero" X) o
  **`Blocks`** para bloqueos. Tipos en `_shared/jira/fields-by-issuetype.md`.
- Crear los links DESPUÉS de crear los issues (necesita las keys), vía `POST /rest/api/3/issueLink`.
- Mostrar las dependencias propuestas en el widget de revisión (edges) para que el PM las confirme/edite.
- No inventar dependencias sin señal en el alcance; ante duda, proponer como "posible" y que el PM decida.

## Orden de creación
Epic → Story (con parent = Epic) → Sub-task (con parent = Story). Necesario para linkear el `parent`.
Recordar: subtasks en PC = Sub-task (10003), Story Bug (10506), Opportunity for improvement (10539).
