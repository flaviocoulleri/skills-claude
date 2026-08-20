# Convención de Nomenclatura — Skills ProContacto

## La fórmula

```
pc-[área]-[sistema]-[objeto]-[acción]
```

- **`pc-`** → obligatorio siempre. Prefijo de ProContacto.
- **`[área]`** → obligatorio. Práctica organizacional (crm, cg-cloud, data, delivery, admin-interno, meta, etc.).
- **`[sistema]`** → opcional. Herramienta externa (salesforce, jira, gmail…). Se **omite** cuando el área lo implica o cuando no hay sistema externo.
- **`[objeto]`** → obligatorio. Entidad sobre la que opera el skill (user, field, opportunity…).
- **`[acción]`** → obligatorio. Verbo único (creator, builder, generator, viewer, guide, manager…).

Todo en **kebab-case**, sin mayúsculas, sin espacios, sin `_`. Rango típico: 4-5 tokens (6 es aceptable si el objeto es multi-palabra).

## Tabla de áreas

| Área | Descripción | Sistema implícito |
|---|---|---|
| `crm` | CRM Core (Sales Cloud, Service Cloud) | ninguno (incluir `salesforce`) |
| `cg-cloud` | Consumer Goods Cloud | `salesforce` (omitir) |
| `data-cloud` | Salesforce Data Cloud / CDP | `salesforce` (omitir) |
| `marketing-cloud` | Marketing Cloud / Account Engagement (**producto** Salesforce) | `salesforce` (omitir) |
| `marketing` | Marketing / comunicación de ProContacto: casos de éxito, contenido, difusión (**equipo/práctica**, NO el producto SF) | ninguno (incluir sistema si aplica) |
| `integrations` | MuleSoft, APIs, middleware | ninguno (siempre incluir sistema) |
| `devops` | Release management, CI/CD, SF DX | ninguno (siempre incluir sistema) |
| `data` | Data warehouse, analytics, BI | ninguno (siempre incluir sistema) |
| `delivery` | Gestión de proyectos, PMO, metodología | varía (siempre incluir sistema si aplica) |
| `admin-interno` | Gobernanza, branding, procesos de ProContacto | sin sistema externo (omitir) |
| `meta` | Skills que gestionan el entorno Claude | sin sistema externo (omitir) |
| `legal` | Legales de ProContacto: revisión de contratos, cumplimiento, firmas (**equipo/práctica**) | ninguno (incluir sistema si aplica) |

**Regla**: cuando la columna "Sistema implícito" dice "omitir", no se pone el sistema en el nombre. En los otros casos es obligatorio.

**`marketing` vs `marketing-cloud`**: son áreas distintas y no intercambiables. `marketing-cloud` es el **producto** Salesforce (Marketing Cloud / Account Engagement) que ProContacto implementa para clientes → omite sistema. `marketing` es la **práctica interna** de ProContacto (casos de éxito, contenido, difusión) → lleva sistema explícito (ej. `pc-marketing-salesforce-success-case-generator` persiste en SF).

## Tabla de sistemas (cuando aplica)

| Sistema | Uso |
|---|---|
| `salesforce` | Salesforce Core u otras nubes SF (explicitar cuando el área no lo implica) |
| `jira` | Jira / Atlassian |
| `gcal` | Google Calendar |
| `gmail` | Gmail |
| `slack` | Slack |
| `snowflake` / `bigquery` / `databricks` / `postgres` | Warehouses específicos |
| `mulesoft` | MuleSoft |
| `github` | GitHub / Git |
| `sf-cli` | Salesforce CLI / DX |

**No usar** sistemas genéricos como `api`, `web`, `db`. Siempre el nombre específico.

## Tabla de acciones (verbo único)

| Acción | Significado | Ejemplo |
|---|---|---|
| `creator` | Crea registros/objetos en un sistema | `pc-crm-salesforce-user-creator` |
| `builder` | Construye artefactos configurables (no crea datos, arma piezas) | `pc-crm-salesforce-flow-builder` |
| `generator` | Produce artefactos nuevos a partir de input libre | `pc-admin-interno-adr-generator` |
| `viewer` | Muestra/visualiza datos existentes | `pc-crm-salesforce-record-viewer` |
| `guide` | Skill de referencia (documenta, no ejecuta) | `pc-cg-cloud-guide` |
| `tracker` | Registra actividad a lo largo del tiempo | `pc-delivery-jira-worklog-tracker` |
| `auditor` | Revisa conformidad contra un estándar | `pc-meta-skill-auditor` |
| `architect` | Diseña arquitecturas complejas | `pc-crm-salesforce-perm-architect` |
| `applier` | Aplica un template/estándar a inputs existentes | `pc-admin-interno-brand-applier` |
| `manager` | Orquesta múltiples acciones sobre un mismo dominio | `pc-meta-skill-manager` |
| `workflow` | Orquesta múltiples pasos secuenciales | `pc-crm-salesforce-onboarding-workflow` |
| `orchestrator` | Coordina múltiples objetos y sistemas | `pc-delivery-multi-tool-orchestrator` |
| `validator` | Valida datos/configuración contra reglas | `pc-crm-salesforce-metadata-validator` |
| `publisher` | Publica en un destino versionado un artefacto **que ya existe** (no lo produce) | `pc-meta-artifact-publisher` |

**Regla de una acción**: si el skill hace múltiples cosas sobre el mismo objeto, usar acción paraguas (`manager`, `workflow`, `orchestrator`) en lugar de concatenar verbos (`creator-updater-deleter` ← mal).

**`publisher` vs `generator` / `builder`**: el skill que **produce** el artefacto es `generator` o `builder`, y publicarlo es apenas su paso de cierre — no cambia su nombre. `publisher` se reserva para el skill cuyo trabajo **entero** es tomar algo ya hecho y dejarlo publicado y versionado en su destino. Si dudás, preguntate qué queda si le sacás la publicación: si queda un skill que igual sirve, no es un `publisher`.

**Blocklist**: `tool`, `helper`, `utility`, `assistant`, `smart`, `ai`, `pro`, `v2`, `new`, `my`, `custom`. Son genéricos o versionan — no aportan información taxonómica.

## Ejemplos aplicados al catálogo actual

Esta tabla muestra cómo quedan los skills actuales bajo la convención nueva. Skills `external` (Anthropic, plugins) **no se renombran**.

| Nombre actual | Propuesto | Razonamiento |
|---|---|---|
| `sf-field-creator-pro` | `pc-crm-salesforce-field-creator` | área crm, sistema explícito, sin modificador `-pro` |
| `sf-user-creator` | `pc-crm-salesforce-user-creator` | estándar |
| `sf-flow-builder` | `pc-crm-salesforce-flow-builder` | estándar |
| `sf-perms-architect` | `pc-crm-salesforce-perm-architect` | singular `perm` |
| `sf-record-viewer` | `pc-crm-salesforce-record-viewer` | estándar |
| `sf-prototype-builder` | `pc-crm-salesforce-record-prototyper` | `prototype` no es acción estándar; convertir a `prototyper` o redefinir como `builder` |
| `sf-opportunity-from-calendar` | `pc-crm-salesforce-opportunity-creator` | el origen (calendar) es dependencia, no identidad |
| `lwc-apex-builder` | `pc-crm-salesforce-lwc-builder` | LWC es objeto SF |
| `cg-cloud-guide` | `pc-cg-cloud-guide` | área implica sistema → omitir `salesforce` |
| `salesforce-developer` | `pc-crm-salesforce-dev-guide` | agregar acción (guía de dev), objeto `dev` |
| `jira-worklog` | `pc-delivery-jira-worklog-tracker` | área delivery (PMO usa worklogs), acción tracker |
| `adr-generator` | `pc-admin-interno-adr-generator` | área admin-interno → sin sistema |
| `procontacto-brand` | `pc-admin-interno-brand-applier` | área admin-interno → sin sistema; acción applier |
| `morning-briefing` | `pc-meta-briefing-generator` | área meta → sin sistema; objeto briefing |
| `pc-skill-catalog-manager` | `pc-meta-skill-manager` | (el propio skill — autoaplicación) |
| `docx`, `pptx`, `pdf`, `xlsx` | — | externos, NO renombrar |
| `skill-creator`, `consolidate-memory`, `schedule`, `setup-cowork` | — | externos, NO renombrar |

## Reglas sobre `name` en frontmatter

El campo `name` del frontmatter YAML debe **coincidir exactamente** con el nombre del directorio. Kebab-case, sin Title Case.

Mal:
```yaml
name: PC CRM Salesforce Field Creator
```

Bien:
```yaml
name: pc-crm-salesforce-field-creator
```

Razón: el nombre del directorio es lo que Claude ve al resolver paths. Si el `name` frontmatter diverge, se rompen referencias y pipelines de packaging.

## Reglas sobre `description` en frontmatter

La description es el **único mecanismo de triggering**. Si está mal escrita, el skill no se activa — es como si no existiera.

Plantilla recomendada (ES):

```
[Una oración: qué hace el skill, con verbo activo].
Activar cuando el usuario [lista de frases/contextos en primera persona del usuario,
5-10 ejemplos].
También activar si [contextos secundarios o proactivos].
[Detalle adicional sobre qué no hace, o qué requiere como input].
Funciona en español e inglés.
```

### Checklist de description

- [ ] ≥ 300 caracteres (las cortas no triggerean)
- [ ] Empieza con verbo activo (crea, genera, audita, aplica)
- [ ] Incluye ≥ 5 frases disparadoras literales del usuario entre comillas
- [ ] Menciona el sistema/objeto principal explícitamente
- [ ] Si es bilingüe, lo dice al final
- [ ] Si se activa proactivamente (sin pedido explícito), aclara en qué contexto

## Test de olfato rápido

Antes de aceptar un nombre, pregúntate:

1. **¿Empieza con `pc-`?** Si no, y es un skill ProContacto → rechazar.
2. **¿El área es una de la tabla?** Si no, agrégala al catálogo con discusión explícita — no improvises.
3. **¿El sistema es obligatorio según el mapa área→sistema?** Si el área lo requiere y falta, rechazar. Si el área lo implica y está duplicado, rechazar.
4. **¿Hay una sola acción al final?** Si hay dos verbos concatenados, reemplazar por acción paraguas.
5. **¿Usaste alguna palabra del blocklist?** → rechazar.
