# Catálogo canónico de artefactos — mapeo determinista

Regla de mapeo: **documento → carpeta Drive**; **deck / presentación → prompt para Claude Design**;
**wireframe / diagrama (AS-IS, TO-BE, ERD, arquitectura de integraciones) → artefacto en Cowork**.
No idear el mapeo en runtime — usar esta tabla. Fuente del proceso: `pc-delivery-blueprint-guide`.

Por cada entregable **aplicable** se crea un issue `Artifact` en Jira (uno por entregable), con su link.
La columna "Skill que lo produce" es para referenciar en la descripción del `Artifact` — este skill NO
redacta el contenido.

> **Cambio de criterio (jul-2026):** wireframes (v1 y v2) y los diagramas de diseño (AS-IS, TO-BE,
> ERD, integraciones) pasan de Claude Design a **artefacto en Cowork**. Claude Design queda reservado
> para **decks / presentaciones** (propuesta comercial, decks de delivery, caso de éxito). Los
> **documentos** siguen en Drive.

## Fase 1 — Venta (referencias; viven en la carpeta comercial del deal, se linkean, no se crean acá)

| Artefacto | Tipo | Herramienta | Carpeta Drive | Skill que lo produce |
|---|---|---|---|---|
| SOW comercial | doc | Drive (ref) | 00 · Comercial | pc-sales-sf-sow-builder |
| Propuesta / deck comercial | deck | Claude Design (ref) | 00 · Comercial | pc-sales-presentation-builder |
| Wireframes v1 | visual | **Cowork** (ref) | 00 · Comercial | pc-crm-salesforce-wireframe-builder |

## Fase 2 — Sprint 0 (los 10 entregables obligatorios)

| # | Entregable | Tipo | Herramienta | Carpeta Drive | Skill que lo produce |
|---|---|---|---|---|---|
| 1 | SOW refinado (vF) | doc | **Drive** | 01 · Sprint 0 › Scope Freeze | pc-delivery-salesforce-sow-generator |
| 2 | Backlog de HUs · Anexo B | doc | **Drive** | 01 · Sprint 0 › Historias de Usuario | pc-crm-userstory-generator (CG: pc-cg-cloud-userstory-generator) |
| 3 | Wireframes v2 · Anexo C | visual | **Cowork** ⭐ | 01 · Sprint 0 › Wireframes | pc-crm-salesforce-wireframe-builder |
| 4 | Diccionario de datos | doc/Sheet | **Drive** | 01 · Sprint 0 › Diccionario de datos | pc-crm-salesforce-data-dictionary-generator |
| 5 | Matriz de integraciones | doc/Sheet | **Drive** | 01 · Sprint 0 › Integraciones | (template blueprint-guide) |
| 6 | Plan de datos | doc | **Drive** | 01 · Sprint 0 › Plan de datos | (template blueprint-guide) |
| 7 | Plan de UAT | doc | **Drive** | 04 · UAT › Plan de UAT | (template blueprint-guide) |
| 8 | RACI + ceremonias | doc | **Drive** | 02 · Gobierno › RACI y ceremonias | (template blueprint-guide) |
| 9 | RAID log | Sheet | **Drive** | 02 · Gobierno › RAID log | (template blueprint-guide) |
| 10 | Acta de Scope Freeze | doc | **Drive** | 01 · Sprint 0 › Scope Freeze | (template blueprint-guide) |

## Diagramas de diseño del Sprint 0 (Cowork)

| Artefacto | Tipo | Herramienta | Carpeta Drive (soporte) | Aplica cuando |
|---|---|---|---|---|
| AS-IS (proceso actual) | diagrama | **Cowork** ⭐ | 01 · Sprint 0 › AS-IS · TO-BE | siempre |
| TO-BE (proceso futuro) | diagrama | **Cowork** ⭐ | 01 · Sprint 0 › AS-IS · TO-BE | siempre |
| Modelo de datos / ERD | diagrama | **Cowork** (opc.) | 01 · Sprint 0 › Diccionario de datos | si hay modelo de datos custom |
| Arquitectura de integraciones | diagrama | **Cowork** (opc.) | 01 · Sprint 0 › Integraciones | si hay integraciones |

## Práctica recomendada (no canon del deck)

| Artefacto | Tipo | Herramienta | Carpeta Drive |
|---|---|---|---|
| Status semanal / comité | doc | Drive | 02 · Gobierno › Status semanales |
| Garantía vs. control de cambios | doc | Drive | 02 · Gobierno › Control de cambios |
| Matriz de responsables por rol | doc | Drive | 02 · Gobierno › RACI y ceremonias |

## Fase 3 — Ejecución

| Artefacto | Tipo | Herramienta | Carpeta Drive | Skill |
|---|---|---|---|---|
| ADRs (decisiones de arquitectura) | doc | Drive | 03 · Ejecución › Documentación técnica | pc-admin-interno-adr-generator |
| Órdenes de cambio (CRs) | doc | Drive | 02 · Gobierno › Control de cambios | — |
| Demos (links/grabaciones) | ref | Drive | 03 · Ejecución › Demos | — |

## Fases 4–5 — UAT y Go-live

| Artefacto | Tipo | Herramienta | Carpeta Drive | Skill |
|---|---|---|---|---|
| Casos de UAT + evidencia | doc/Sheet | Drive | 04 · UAT › Casos y evidencia | — |
| Acta de aceptación | doc | Drive | 04 · UAT › Acta de aceptación | — |
| Runbook de go-live | doc | Drive | 05 · Go-live y cierre › Runbook | — |
| Acta de cierre | doc | Drive | 05 · Go-live y cierre › Acta de cierre | — |
| Caso de éxito | deck | Claude Design | 05 · Go-live y cierre | pc-marketing-salesforce-success-case-generator |

## Artefactos visuales a generar en Cowork (uno por artefacto)

1. **AS-IS** — proceso actual del cliente (siempre)
2. **TO-BE** — proceso futuro en Salesforce (siempre)
3. **Wireframes v2 (Anexo C)** — el contrato visual (siempre) ⭐
4. **Modelo de datos / ERD** (opcional — si hay modelo custom)
5. **Arquitectura de integraciones** (opcional — si hay integraciones)

Cada artefacto se publica en el **gestor de ProContacto** y se registra como `Project_Asset__c`
(`Type__c='ProContactoArtifactId'`, `Value__c` = **el uuid en crudo** de
`https://artifacts.procontacto.com.mx/a/<uuid>`, `Description__c` = qué documento es) y como issue
`Artifact` en Jira con su link.

> **La `Description__c` es la que hace legible el inventario.** Los cinco artefactos de arriba caen
> todos bajo el mismo `Type__c`: sin descripción, el `Project__c` termina con cinco assets idénticos
> salvo por el uuid. Usá el nombre del artefacto y qué contiene — `AS-IS — proceso actual de
> pedidos y cobranza`, `ERD del modelo custom (Pedido, Visita, Liquidación)`.
>
> `CoworkArtifactId` es el tipo **legado** de cuando el entregable vivía en un artefacto de
> conversación: se lee para encontrar registros viejos, no se crean nuevos.

## Artefactos que van a Claude Design (prompt)

- Propuesta / deck comercial (fase venta) — `pc-sales-presentation-builder`
- Decks de delivery: kickoff, steering, status, cierre — `pc-delivery-presentation-builder`
- Deck desde una conversación — `pc-meta-conversation-to-slidedeck`
- Caso de éxito — `pc-marketing-salesforce-success-case-generator`

Cada deck de Claude Design se registra como `Project_Asset__c` (`Type__c='ClaudeDesignProjectId'` o el
rol semántico correspondiente, `Value__c` = uuid del proyecto CD) y como issue `Artifact` en Jira.
