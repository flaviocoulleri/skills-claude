# Mapa de skills del catálogo por fase y entregable

Mapeo determinista: cuando la respuesta implique producir un entregable o ejecutar un paso, recomendar el skill de esta tabla — no idear el mapeo en runtime.

**Nota de disponibilidad:** no todos los skills están publicados en todos los plugins (algunos son de área comercial, otros están excluidos del deploy a la org). Antes de recomendar, si el skill no aparece disponible para el usuario, decirlo y ofrecer el template manual como alternativa.

## Fase 1 — Venta comercial

| Paso / entregable | Skill | Cuándo invocarlo |
|---|---|---|
| Análisis del deal / HUs preliminares / sizing | `sf-deal-analyzer` | Con transcript de reunión o entrevista guiada al vendedor, para requerimientos y orden de magnitud |
| SOW comercial | `pc-sales-sf-sow-builder` | Para generar el SOW por unidades con export branded |
| Propuesta / deck comercial | `pc-sales-presentation-builder` | Para la presentación de la propuesta con el design system |
| Oportunidad en SF | `pc-sales-sf-opportunity-builder` | Alta/actualización de la Opportunity |
| Quote | `pc-sales-sf-quote-builder` | Cotización sobre la oportunidad |
| Contrato | `pc-sales-sf-contract-builder` | Contrato al cierre |
| Demo para la venta | `pc-sales-sf-demo-builder` | Cuando el deal necesita demo |

## Fase 2 — Sprint 0

| Entregable | Skill | Cuándo invocarlo |
|---|---|---|
| Alta de assets del proyecto (Jira, Slack, Drive, Confluence…) | `pc-delivery-sf-project-builder` | Al inicio del Sprint 0, para provisionar el tooling del proyecto |
| Backlog de HUs con criterios Gherkin (Anexo B) | `pc-crm-userstory-generator` — CG Cloud: `pc-cg-cloud-userstory-generator` | Semana 2, refinamiento funcional |
| Diccionario de datos | `pc-crm-salesforce-data-dictionary-generator` | Semana 2 — es el insumo directo del agente de IA |
| Wireframes v2 (Anexo C) | `pc-crm-salesforce-wireframe-builder` | Semana 2, como artefacto de Cowork |
| Decisiones de arquitectura | `pc-admin-interno-adr-generator` | Cuando en los talleres se toma una decisión técnica significativa |
| Arquitectura de permisos | `pc-crm-salesforce-perm-architect` | Si el diseño incluye modelo de permisos/visibilidad complejo |
| SOW refinado (vF) | `pc-sales-sf-sow-builder` | Semana 4, cierre |

## Fase 3 — Ejecución con IA

| Paso | Skill | Cuándo invocarlo |
|---|---|---|
| Configuración declarativa (campos, flows) | `pc-crm-salesforce-field-creator`, `pc-crm-salesforce-flow-builder` | HUs de configuración |
| Desarrollo (LWC, Apex) | `pc-crm-salesforce-lwc-builder`, `pc-crm-salesforce-dev-guide` | HUs de desarrollo |
| CI/CD, branches, deploys | `pc-devops-salesforce-cicd-guide` | Setup del pipeline y dudas del flujo diario |
| Seguimiento del sprint / pendientes | `pc-delivery-jira-pending-tracker` | Issues estancadas, sin fecha, sin estimación |
| Worklogs del equipo | `pc-delivery-jira-worklog-tracker` | Control de imputación de horas |
| Pulso de todos los proyectos | `pc-delivery-project-pulse` | Vista semáforo diaria para el nodo/DM |
| Status al cliente por Slack | `pc-delivery-slack-channel-auditor` | Mantener informado al canal externo del proyecto |
| Salud general del board | `pc-delivery-jira-project-auditor` | Auditoría de conformidad del proyecto Jira |

## Fases 4 y 5 — UAT y Go-live

| Paso | Skill | Cuándo invocarlo |
|---|---|---|
| Aviso de go-live | `pc-delivery-sf-project-golive-notifier` | Al salir a producción |
| Caso de éxito | `pc-crm-salesforce-success-case-generator` | Post go-live, para marketing/AppExchange |

## Transversales

| Necesidad | Skill | Cuándo invocarlo |
|---|---|---|
| Cualquier entregable visible (docs, decks, dashboards) | `pc-admin-interno-brand-applier` | Siempre que se genere material visible — aplica el design system |
| Registro de documentos del deal como assets | Modo D de este skill | Cuando hay docs en Drive / links Claude Design sin registrar como Artefacto en Jira |
