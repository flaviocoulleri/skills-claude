# Taxonomía — Dimensiones del Catálogo de Skills

Cada skill del catálogo se clasifica según estas dimensiones. Los valores fuera de las listas permitidas se rechazan en la validación — si un skill no encaja, agregamos la dimensión al catálogo con discusión previa (no inventar valores nuevos al vuelo).

## Dimensión 1 — Rol de usuario

Quién usa el skill. Un skill puede tener **múltiples roles** (array).

| Valor | Perfil |
|---|---|
| `admin-sf` | Salesforce Admin — configura orgs, objetos, permisos, flows |
| `developer-sf` | Salesforce Developer — Apex, LWC, integraciones |
| `developer` | Developer general (no SF) — integraciones, scripts, backends |
| `pm` | Project Manager — tracking, reporting, reuniones |
| `delivery` | Delivery / Functional Consultant — requerimientos, configuración, UAT |
| `analyst-data` | Data Analyst — SQL, dashboards, reportes |
| `architect` | Arquitecto — diseño de soluciones, ADRs |
| `consultant` | Consultor senior — cliente-facing, mixto |
| `end-user` | Usuario final no-técnico (ventas, marketing) |
| `any` | Aplica a cualquier rol (skills utilitarios como `pc-brand-applier`) |

## Dimensión 2 — Área / Práctica

A qué práctica de ProContacto pertenece el skill. **Una sola** área (el área dominante si hay ambigüedad).

| Valor | Descripción |
|---|---|
| `crm` | CRM Core (Sales Cloud, Service Cloud) |
| `cg-cloud` | Consumer Goods Cloud |
| `data-cloud` | Salesforce Data Cloud / CDP |
| `marketing-cloud` | Marketing Cloud / Account Engagement |
| `integrations` | MuleSoft, APIs, middleware |
| `devops` | Release management, CI/CD, SF DX |
| `data` | Data warehouse, analytics, BI |
| `delivery` | Gestión de proyectos, metodología, entregables |
| `admin-interno` | Gobernanza, branding, procesos de ProContacto |
| `meta` | Skills que gestionan el entorno Claude / workflow del consultor |

## Dimensión 3 — Objeto de dato / entidad

Entidad principal sobre la que opera el skill. Texto libre pero **singular** y **en la forma del sistema** donde vive.

Ejemplos:
- `Account` (SF)
- `Opportunity` (SF)
- `User` (SF)
- `FieldDefinition` (SF metadata)
- `PermissionSet` (SF)
- `Flow` (SF)
- `Visit_Job__c` (CG Cloud)
- `Tactic__c` (CG Cloud)
- `Issue` (Jira)
- `Worklog` (Jira)
- `Event` (Google Calendar)
- `Message` (Slack/Gmail)
- `Document` (doc genérico)
- `ADR` (artefacto interno)
- `Skill` (meta)
- `n/a` (skills que no tocan un objeto específico, ej: guías)

## Dimensión 4 — Sistema / herramienta

Qué herramientas externas usa. **Array** — un skill puede tocar varios sistemas.

| Valor | Herramienta |
|---|---|
| `salesforce` | Salesforce (cualquier cloud) |
| `jira` | Jira / Atlassian |
| `google-calendar` | Google Calendar |
| `gmail` | Gmail |
| `slack` | Slack |
| `ms-office` | Word / Excel / PowerPoint / PDF |
| `data-warehouse` | Snowflake, BigQuery, Databricks, Postgres |
| `github` | GitHub / Git |
| `sf-cli` | Salesforce CLI / DX |
| `internal` | Solo conocimiento interno, sin herramienta externa |

## Dimensión 5 — Tipo de skill

Qué forma tiene el skill. **Un solo** valor.

| Valor | Significado |
|---|---|
| `generator` | Produce artefactos nuevos (ADR, briefing, código) |
| `creator` | Crea registros en sistemas externos |
| `builder` | Construye piezas configurables paso a paso |
| `viewer` | Visualiza datos existentes |
| `validator` | Audita conformidad contra estándares |
| `guide` | Documentación / referencia (no ejecuta) |
| `workflow` | Orquesta múltiples pasos/sistemas |
| `utility` | Aplica una transformación puntual |

## Dimensión 6 — Estado de madurez

En qué etapa del ciclo de vida está. **Un solo** valor.

| Valor | Significado |
|---|---|
| `draft` | En desarrollo activo, no publicado oficialmente |
| `beta` | Publicado pero bajo observación, sujeto a cambios |
| `stable` | Producción, API estable |
| `deprecated` | Se planea discontinuar, evitar usar |

## Dimensión 7 — Idioma

Idioma principal del skill (description + body). **Un solo** valor.

| Valor | Idioma |
|---|---|
| `es` | Solo español |
| `en` | Solo inglés |
| `bi` | Bilingüe explícito (description y triggers en ambos idiomas) |

**Nota**: para ProContacto la recomendación es `bi` para skills orientados a clientes/partners internacionales, y `es` para skills internos. Evitar `en` puro salvo skills externos.

## Dimensión 8 — Owner / Mantenedor

Handle de GitHub o email del responsable técnico del skill. Si nadie se hace cargo formalmente, poner `unowned` (y eso es un hallazgo del audit — ningún skill debería quedar `unowned` > 30 días).

## Dimensión 9 — Dependencias (connectors / MCPs)

Array de MCPs / connectors externos que el skill necesita para funcionar. Ejemplos:

- `mcp__plugin_data_atlassian__*` (Jira)
- `mcp__e6a74789-...__*` (Salesforce MCP de la org)
- `mcp__cowork__create_artifact` (para skills que generan artifacts)
- `google-calendar` (a través del conector)
- `gmail`
- `slack`

Si el skill no tiene dependencias externas (solo lee/escribe archivos), poner `[]`.

## Dimensión 10 — Origen

De dónde viene el skill. **Un solo** valor.

| Valor | Significado |
|---|---|
| `procontacto` | Skill desarrollado por ProContacto |
| `external` | De Anthropic, plugins de terceros, etc. — **no auditar** con reglas PC |

---

## Ejemplo de entrada de catálogo (JSON)

```json
{
  "name": "sf-opportunity-creator",
  "directory_name": "sf-opportunity-from-calendar",
  "roles": ["delivery", "consultant"],
  "area": "crm",
  "object": "Opportunity",
  "systems": ["salesforce", "google-calendar"],
  "type": "creator",
  "status": "stable",
  "language": "es",
  "owner": "ariel.tarsitano",
  "dependencies": ["mcp__e6a74789-...__createSobjectRecord", "google-calendar"],
  "origin": "procontacto",
  "name_conformance": false,
  "name_issue": "El nombre incluye '-from-calendar' que es origen, no acción. Propuesto: sf-opportunity-creator"
}
```

Los campos `name_conformance` y `name_issue` sólo aparecen cuando el audit detecta un problema. Un skill en buen estado los omite.
