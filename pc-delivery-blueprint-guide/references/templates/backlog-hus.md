# Template — Backlog de HUs · Anexo B

> Criterios Gherkin: base del agente de IA y de las pruebas de UAT. Firma: **PO cliente**. Semana 2 del Sprint 0. Skill: `pc-crm-userstory-generator` (CG Cloud: `pc-cg-cloud-userstory-generator`).

## Estructura mínima por HU

- **ID** — clave Jira.
- **Título** — "Como <rol> quiero <acción> para <beneficio>".
- **Descripción funcional** — contexto y regla de negocio.
- **Criterios de aceptación Gherkin** — verificables pasa/no-pasa:
  ```gherkin
  DADO <precondición>
  CUANDO <acción>
  ENTONCES <resultado observable>
  ```
- **Pantalla asociada** — referencia al wireframe del Anexo C (obligatoria: sin pantalla, la HU no es AI-ready).
- **Referencia al diccionario de datos** — objetos/campos involucrados.
- **Clasificación** — alcance comprometido | backlog fase 2.

## Reglas del anexo

- Sin criterios verificables y pantalla asociada, una historia **no entra a ejecución** (principio 2).
- Máximo 2 rondas de observaciones consolidadas por el PO; la ronda 3 es un cambio (limitante 05).
- Los casos de UAT derivan 1:1 de estos criterios — lo no descrito acá es un cambio.
- El backlog vive en Jira; el anexo firmado es el snapshot al Scope Freeze.
