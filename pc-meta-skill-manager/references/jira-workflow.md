# Jira Workflow — Crear tareas en PROCSKILLS

Este archivo describe cómo crear issues en el tablero PROCSKILLS a partir de los hallazgos de una auditoría.

**Tablero**: https://procontacto.atlassian.net/jira/software/c/projects/PROCSKILLS/boards/2952
**Project Key**: `PROCSKILLS`

## Pre-flight

Antes de crear issues:

1. **Confirma con el usuario** explícitamente que quiere crear las tareas. Un audit puede arrojar 20+ hallazgos — crearlos sin confirmación es ruidoso.
2. **Verifica** que el conector Atlassian esté autenticado: llama a `mcp__plugin_data_atlassian__*` (alguna tool de listado). Si no lo está, avisa y párate — no inicies el flujo de auth a menos que el usuario te lo pida.
3. **Muéstrale al usuario** la preview: cuántas issues vas a crear, de qué severidad, agrupadas por responsable asignado.

## Mapping hallazgo → issue

| Campo Jira | Cómo completarlo |
|---|---|
| `project` | `PROCSKILLS` |
| `issuetype` | `Task` (default) — usar `Bug` solo si el hallazgo es `high` tipo `metadata` (frontmatter roto, skill no carga) |
| `summary` | `[{rule_id}] {skill_name}: {descripción corta ≤ 80 chars}` |
| `description` | Ver plantilla abajo |
| `priority` | Mapeo desde severidad: `high` → Highest, `medium` → Medium, `low` → Low |
| `labels` | `["skills-governance", "rule:{rule_id}", "type:{type}", "auto-generated"]` |
| `assignee` | Ver routing abajo |
| `reporter` | El usuario actual (Ariel por default) |

### Plantilla de description

```
## Problema detectado

{description del hallazgo}

## Skill afectado

- **Nombre actual**: {skill_name}
- **Path**: {relative_path}
- **Estado**: {status desde taxonomía}
- **Owner**: {owner o "unowned"}

## Fix sugerido

{suggested_fix}

## Contexto

- **Regla**: {rule_id} ({type}/{severity})
- **Generado por**: pc-skill-catalog-manager audit
- **Fecha**: {ISO date}

---

*Esta issue fue creada automáticamente por una auditoría del catálogo de skills.
Si consideras que el hallazgo no aplica, cierra la issue con status "Won't Do" y
un comentario explicando el motivo — eso nos ayuda a afinar las reglas de audit.*
```

## Routing / asignación

La asignación por defecto sigue esta lógica, en orden de preferencia:

1. **Si el skill tiene `owner` declarado en su metadata**: asignar al owner.
2. **Si no hay owner pero el skill tiene `area` clara**: asignar al lead de esa práctica (tabla abajo).
3. **Si no se puede determinar**: asignar al usuario que corrió el audit, con label adicional `needs-triage`.

### Leads por área (placeholder — confirmar con Ariel antes del primer run real)

| Área | Lead default |
|---|---|
| `crm`, `cg-cloud` | (admin-sf lead) |
| `data`, `data-cloud` | (data lead) |
| `devops`, `integrations` | (architect lead) |
| `admin-interno`, `meta` | ariel.tarsitano |

> **Importante**: en el primer run, **no** asignar automáticamente a ningún lead hasta que Ariel valide los handles reales. Crear issues sin assignee y con label `needs-triage` es el fallback seguro.

## Creación batch

Los MCP tools de Atlassian suelen exponer algo como `createJiraIssue` — **usa una llamada por issue**, no intentes batch APIs que probablemente el MCP no tenga.

Secuencia recomendada:

1. Genera la lista de issues a crear (dict con los campos).
2. Muéstrale al usuario la preview: primera issue completa + resumen de las demás ("... y 14 más").
3. Espera confirmación (`AskUserQuestion`: "¿Creo las 15 tareas?").
4. Iterá creando una a una. Si una falla, captura el error y sigue con las demás — al final muestra resumen de creadas vs fallidas.
5. Entrega al usuario la lista de links Jira creados, agrupados por assignee.

## Idempotencia

Si el audit se corre de nuevo la semana que viene y los mismos problemas siguen sin resolverse, **no** crear issues duplicadas. Antes de crear una issue:

1. Busca en PROCSKILLS issues abiertas con label `rule:{rule_id}` cuyo summary contenga `{skill_name}`.
2. Si existe una, no crees una nueva. Opcionalmente agrega un comentario "Sigue pendiente al {fecha}".

## Caso: conector no autenticado

Si al intentar listar issues Jira recibes error de auth:

1. No inicies el flow de OAuth automáticamente. Dile al usuario algo como:
   > "El conector de Atlassian no está autenticado. Necesito que lo actives en Configuración → Conectores, y después vuelve y retomamos. Alternativamente puedo generarte el reporte de auditoría en markdown sin crear issues, y las creas tú después."
2. Ofrece el fallback: reporte MD completo en el workspace.
