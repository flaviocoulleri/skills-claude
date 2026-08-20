---
name: pc-crm-salesforce-perm-architect
version: 1.1.0
description: >
  Diseña arquitecturas integrales de permisos Salesforce desde el modelo de negocio.
  Usa esta skill cuando el usuario pase un modelo de negocio, estructura org,
  flujos de datos, roles y responsabilidades de clientes/proyectos, y necesite recomendaciones
  sobre cómo gestionar permisos mediante Permission Sets, Permission Set Groups, Sharing Rules,
  Apex Sharing, OWD, y Roles sin abusar de custom permissions. Genera análisis estratégico,
  diagrama de acceso, artefactos implementables y considera buenas prácticas de Salesforce.
---

<!-- Changelog
1.0.0 (2026-04-25): Primera versión formal bajo la convención pc-[área]-[sistema]-[objeto]-[acción]. Renombrado desde `sf-perms-architect` → `pc-crm-salesforce-perm-architect`. Sin cambios funcionales.
-->

# Salesforce Permissions Architect

Transforma un modelo de negocio en una **arquitectura de permisos escalable, mantenible y segura**.
Analiza roles, flujos, sensibilidad de datos y recomienda la mejor combinación de herramientas
de control de acceso en Salesforce.

---

## Flujo principal

Sigue siempre este orden. Haz **una pregunta a la vez**. No adelantes preguntas.

---

### Paso 1 — Captura del contexto

**Pregunta (en 1-2 preguntas cortas):**

> "¿Me pasas el modelo de negocio del cliente? Puede ser texto libre, un documento,
> una imagen de un diagrama, o incluso un resumen en viñetas. Necesito entender:
> - Estructura de la organización (equipos, roles, jerarquía)
> - Principales flujos de datos (quién crea qué, quién accede a qué)
> - Industria/contexto del negocio"

**Si el usuario sube un archivo (.txt, .md, .pdf, .jpg, .xlsx):**
- Procesarlo automáticamente
- Leer con las skills apropiadas (`file-reading`, `pdf-reading`, etc.)
- Resumir lo entendido y preguntar si completó bien

**Si es un resumen en texto:**
- Pide que profundice en 1-2 aspectos que veas vagos

---

### Paso 2 — Análisis de roles y responsabilidades

**Pregunta (una por vez):**

1. "¿Cuáles son los **roles principales** en la organización y sus responsabilidades?"
   - Ejemplo: "Sales Manager, Sales Rep, Account Executive, Operations, Finance"
   - Incluye jerarquía si la hay (quién reporta a quién)

2. "¿Hay **roles especializados** o compartimientos (ej: Legal, Compliance, Auditoría)?"
   - Si sí: describe sus responsabilidades y si manejan datos sensibles

3. "¿Hay **usuarios que atraviesan múltiples roles** (ej: sales managers que también operan)?"
   - Esto es clave para Permission Set Groups

---

### Paso 3 — Sensibilidad y compartimentalización de datos

**Pregunta (una por vez):**

1. "¿Hay datos **altamente sensibles** que deban estar compartimentalizados?"
   - Ejemplos: contracts, pricing, employee data, financial records
   - Por cada conjunto sensible: ¿quiénes deben acceder?

2. "¿Hay **restricciones normativas o legales**?" (GDPR, SOX, compliance local)
   - ¿Aplica auditoría de acceso?

3. "¿La visibilidad es **jerárquica** (managers ven todo su equipo) o **por owner** (solo tus registros)?"

---

### Paso 4 — Flujos de datos y ciclos de vida

**Pregunta (una por vez):**

1. "Describe un **flujo crítico** (ej: 'Prospect → Opportunity → Contract → Invoice')"
   - ¿Quiénes participan en cada etapa?
   - ¿Quién tiene permisos de lectura/escritura?
   - ¿Hay validaciones o bloqueos por rol?

2. "¿Hay **procesos automatizados** (flujos, procesos, triggers) que afecten acceso?"
   - Ejemplo: "El sistema auto-asigna opportunities basado en territory"

3. "¿Necesitas **aprobaciones cruzadas** o escaladas?" (si sí → Approval Process, implica sharing)

---

### Paso 5 — Topología Salesforce actual (si aplica)

**Pregunta:**

> "¿Ya tienen Salesforce implementado o es greenfield?"
>
> - **Si greenfield**: salta al Paso 6
> - **Si ya existe**: ¿Puedes describir o mostrar la estructura actual?
>   - Objetos principales (Accounts, Opportunities, Contracts, etc.)
>   - Perfiles activos vs. desactivos
>   - Si hay Permission Sets o Sharing Rules ya en uso

---

### Paso 6 — Análisis & Recomendaciones (GENERADOR)

**Aquí es donde la skill agrega valor consultivo.** Genera un análisis estructurado:

#### 6a — Matriz de acceso propuesta

Crea una tabla que mapee:
- **Rol / Usuario** → **Objeto** → **Permisos (CRUD)** → **Visibilidad (OWD / Sharing)** → **Herramienta recomendada (PSet, PSG, SharingRule, Apex)**

Ejemplo:
```
Rol: Sales Manager
├─ Account
│  ├─ CRUD: Read (all), Edit (team owned), Create
│  ├─ OWD: Private
│  ├─ Sharing: Manager sees team's via Sharing Rule
│  └─ Herramienta: Permission Set "Account_Manager_Visibility" + Sharing Rule "Account_Share_By_Manager"
├─ Opportunity
│  ├─ CRUD: Read (all), Edit (owned/team), Create
│  ├─ Sharing: Role hierarchy (Manager > Reps)
│  └─ Herramienta: Rol + OWD "Public Read/Write" + Sharing Rule
└─ Contract
   ├─ CRUD: Read only (all signed), Edit (draft owned)
   ├─ Sharing: Private, solo admin + Contract Owner
   └─ Herramienta: Permission Set "Contract_Reviewer" + manual sharing
```

#### 6b — Recomendaciones por herramienta

**Permission Sets** (cuándo usarlos):
- Dar permisos a un grupo de usuarios sin asignar perfil
- Acceso a features específicas (API, Deploy metadata, Create reports)
- Acceso temporal o por proyecto

**Permission Set Groups** (cuándo usarlos):
- Usuarios multi-rol (ej: Sales Rep que también hace Onboarding)
- Composición modular: Admin = Core + Security + Reporting
- Facilita auditoría: ver exactamente qué PSets tiene cada PSG

**Sharing Rules** (cuándo usarlos):
- Visibilidad jerárquica (managers ven subordinados)
- Compartir por criterios (BillingCity = "NYC" → NYC Sales Team)
- OWD Private, sharing automático por regla

**Apex Sharing** (cuándo usarlos):
- Lógica de sharing muy compleja (múltiples criterios, cálculos)
- Sharing dinámico basado en lookups o fórmulas
- Auditoría de sharing programático

**Roles & Role Hierarchy** (cuándo usarlos):
- Estructura jerárquica clara
- Data visibility inheritance (manager ve subordinados por defecto)
- Combinado con OWD "Public Read/Write"

**OWD** (decisión estratégica):
- Private: máxima seguridad, requiere sharing explícito
- Public Read Only: default visibility, edit solo owner/manager
- Public Read/Write: máxima colaboración, cuidado con datos sensibles

#### 6c — Patrones recomendados para casos comunes

Muestra qué patrón aplica mejor al contexto:

- **"Jerárquico + colaborativo"** (típico en Sales):
  - OWD: Public Read/Write
  - Role Hierarchy: habilitado
  - Sharing Rules: para excepciones

- **"Compartimentalizado + seguro"** (típico en Finance/Legal):
  - OWD: Private
  - PSGs: composición granular
  - Sharing Rules: por departamento/región
  - Auditoría: built-in via sharing records

- **"Datos públicos + permisos granulares"** (típico en Customer Community):
  - OWD: Public Read Only
  - PSets: funcionalidad específica (edit solo si PSG = "Editor")
  - Apex Sharing: para edge cases

#### 6d — Cambios propuestos vs. anti-patterns

Lista qué **evitar**:

- ❌ Perfiles con FLS granulares cuando PSets son cleaner
- ❌ Custom Permissions para lógica que puede ser PSGs
- ❌ OWD Public Read/Write para datos sensibles
- ❌ Sharing Rules anidadas complejas (mejor: Apex)
- ❌ Roles desusados que siguen en la jerarquía

---

### Paso 7 — Validación y refinamiento

**Pregunta:**

1. "¿Ves algo **incompleto o fuera de lugar** en las recomendaciones?"
2. "¿Hay **restricciones adicionales** que no mencionaste?" (ej: "Sales team nunca ve Finance data")
3. "¿Necesitas que profundice en **alguna herramienta específica**?"

---

### Paso 8 — Generación de artefactos

Pregunta qué necesita:

> "¿Qué quieres que genere?"
>
> - **Diagrama de acceso** (visual: Mermaid o descripción clara)
> - **YAML config** (estructura para el deployment)
> - **Documentación de diseño** (cómo está pensado y por qué)
> - **Manifests & metadata XML** (Permission Sets, Sharing Rules)
> - **Apex Sharing Scripts** (si aplica)
> - **Test cases** (validar acceso post-deploy)
> - Todo lo anterior

Si elige "todo", genera en este orden:

#### 8a — Diagrama conceptual (Mermaid)

Muestra visualmente:
- Roles → Permission Sets/Groups (flechas)
- Objetos → OWD & Sharing Rules (nodes coloreados por sensibilidad)
- Flujos críticos (A accede a B bajo condición C)

#### 8b — Documento de diseño (markdown)

Estructura:
```
# Permissions Architecture Design — [Client Name]

## Executive Summary
[1 párrafo: qué se está habilitando, nivel de seguridad, complejidad]

## Current State vs. Proposed
[Tabla comparativa]

## Role Hierarchy & Permission Structure
[Diagrama en texto: Role → PSG → PSets → Permisos]

## Object-Level Security (OWD & Sharing Rules)
[Por cada objeto sensible: OWD + reglas aplicadas]

## Apex Sharing (si aplica)
[Qué se comparte programáticamente y por qué]

## Custom Permissions
[Solo si hay; justificar cada una]

## Audit Trail & Compliance
[Cómo se audita, qué registra Salesforce]

## Migration Plan
[Orden de deploy, rollback strategy]

## Maintenance & Growth
[Cómo escala esto, qué monitorear]
```

#### 8c — YAML Config (si quiere deployment)

```yaml
metadata_version: "1.0"
org: "client_name"
date: "2026-04-XX"
designed_by: "Mili + Claude"

# Roles (si necesita cambios en jerarquía)
roles:
  - id: "sales_manager"
    name: "Sales Manager"
    parent: "vpSales"
  - id: "sales_rep"
    name: "Sales Representative"
    parent: "sales_manager"

# Permission Sets (módulos reutilizables)
permission_sets:
  - id: "core_user"
    label: "Core User Permissions"
    permissions:
      system: ["ApiEnabled"]
      objects:
        Account: [read, create, edit]

  - id: "account_visibility"
    label: "Account Full Visibility"
    permissions:
      objects:
        Account: [read_all, edit_all]

# Permission Set Groups (composición)
permission_set_groups:
  - id: "sales_rep"
    label: "Sales Representative"
    description: "Sales rep with account & opportunity management"
    permission_sets:
      - "core_user"
      - "account_visibility"
      - "opportunity_management"

  - id: "sales_manager"
    label: "Sales Manager"
    permission_sets:
      - "core_user"
      - "account_visibility"
      - "opportunity_management"
      - "team_reporting"
      - "forecast_access"

# OWD (Object-level baseline)
owds:
  - object: "Account"
    default_access: "private"
    default_internal_access: "private"
    justification: "Sensitive client data; visibility via sharing rules"

  - object: "Opportunity"
    default_access: "public_read_write"
    justification: "Sales collaboration model"

# Sharing Rules
sharing_rules:
  - object: "Account"
    name: "Account_Manager_Hierarchy"
    type: "ownership_based"
    access_level: "read"
    description: "Managers see team's accounts via role hierarchy"

  - object: "Account"
    name: "Account_Share_By_Region"
    type: "criteria_based"
    criteria:
      field: "BillingState"
      operator: "equals"
      value: "CA"
    access_level: "edit"
    share_with: "public_group"
    share_with_name: "West_Coast_Sales"

# Apex Sharing (si lógica es compleja)
apex_sharing: []

# Custom Permissions (solo si realmente necesario)
custom_permissions: []

# Assignments (quién obtiene qué)
assignments: []
```

#### 8d — Metadata XML files

Genera los archivos XML listos para SFDX deploy:
- `permissionsets/*.permissionset-meta.xml`
- `permissionsetgroups/*.permissionsetgroup-meta.xml`
- `sharingRules/*.sharingRules-meta.xml`
- `roles/*.role-meta.xml` (si aplica cambios)

#### 8e — Apex Sharing Scripts (si aplica)

Genera Batch/Scheduled jobs para programmatic sharing:
```apex
// Ejemplo: Compartir Custom Objects con usuarios por criterio
```

#### 8f — Test Cases / Validation Queries

Genera SOQL queries y Apex tests para validar:
```soql
-- Verificar que usuario X tiene acceso a Objeto Y
SELECT Id FROM Account WHERE CreatedById = :userId LIMIT 1

-- Verificar composición de PSG
SELECT PermissionSetId FROM PermissionSetGroupMember
WHERE PermissionSetGroupId = [...]

-- Auditar sharing
SELECT Id, UserOrGroupId, PermissionLevel FROM AccountShare
```

---

### Paso 9 — Resumen final y siguiente paso

Mostrar un checklist de lo generado:

```
✅ Diagrama conceptual
✅ Documento de diseño (PDF o Markdown)
✅ YAML config
✅ Permission Sets (XML)
✅ Permission Set Groups (XML)
✅ Sharing Rules (XML)
✅ Apex Scripts (si aplica)
✅ Test cases
```

**Preguntar:**

> "¿Quieres que te ayude con:"
> - Deployment a un org específico (via `sf` CLI)
> - Refinamientos sobre algún aspecto
> - Integración con un Change Set Management
> - Documentación adicional (runbooks, FAQ)

---

## Buenas prácticas incorporadas en el análisis

✅ **Modularidad**: PSets reutilizables, PSGs como composición
✅ **Seguridad**: OWD Private por default, compartir explícitamente
✅ **Escalabilidad**: Evita perfiles con FLS granular, usa PSets
✅ **Auditoría**: Sharing records registran quién accede a qué
✅ **Mantenibilidad**: Documentación clara, no custom permissions innecesarias
✅ **Compliance**: Respeta normas (GDPR, SOX, etc.)
✅ **Performance**: Role Hierarchy > Manual Sharing para escala

---

## Validaciones

- Si hay Custom Permissions propuestas, **justifica por qué**
- Si la complejidad requiere Apex Sharing, **explica por qué no bastan Sharing Rules**
- Si hay objetos sin OWD definido, **recomienda un valor por defecto seguro**
- Si la jerarquía de roles es circular o inconsistente, **señálalo**

---

## Referencias & Extensiones

- `references/psg-patterns.md` — Patrones comunes de Permission Set Groups
- `references/sharing-logic.md` — Decisiones OWD vs. Sharing Rules vs. Apex
- `references/security-checklist.md` — Audit & compliance checklist
- `references/deployment.md` — Cómo deployar sin downtime
- `references/troubleshooting.md` — Casos problemáticos comunes

## Publicación en el gestor (regla dura)

**Todo entregable de este skill se publica en el gestor de artefactos de ProContacto — nunca como
artefacto de la conversación, y nunca solamente como archivo.** Lee
`_shared/artifact-publish/artifact-publish.md` y aplicá su procedimiento completo. Tres partes que no
son opcionales:

1. **Gate del conector, antes de construir.** Una llamada a `listar_artefactos` comprueba que el
   gestor responde. Si no está disponible, **el skill se detiene y le pide a la persona que lo
   active**: no construye "por las dudas", no deja el entregable en la conversación y no ofrece
   mandar el archivo en su lugar.
2. **Anti-duplicado de dos pasos.** `listar_artefactos` por título canónico
   `{Cliente} · {Entregable} · {Tipo}` (sin versión ni fecha) → `publicar_version` sobre la misma URL
   si ya existía, `publicar_artefacto` si no. Anotá el `id` y dejalo en el trace del HTML.
3. **El link va escrito en el chat.** Publicar sin mostrar el link es no publicar.

La arquitectura de permisos se entrega como **HTML** publicado — el diagrama de acceso y la matriz por rol adentro del mismo documento. El `.xlsx` y el `.pdf` pasan a ser **exportaciones a pedido**, después de publicar.

**Exportar exige haber publicado.** Cualquier formato (`.docx`, `.xlsx`, `.pdf`, `.pptx`, texto) se
ofrece en el chat **después** de que el artefacto existe, y sale del mismo original. Que la persona
pida un formato no es permiso para saltear la publicación.
