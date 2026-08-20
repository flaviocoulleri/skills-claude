# Changelog — pc-delivery-deliverable-orchestrator

## 1.1.0 — 2026-07-17
- Cambio de criterio de output (alineado con `references/artifact-catalog.md`): los artefactos visuales
  (AS-IS, TO-BE, Wireframes v2, ERD, integraciones) pasan de **proyectos de Claude Design** a
  **artefactos de Cowork** (`claude.ai/code/artifact/<uuid>`). Claude Design queda reservado para
  decks/presentaciones (fuera del alcance de este skill).
- PASO 3 reescrito: ya no crea proyectos de Design vía Claude-in-Chrome; identifica el visual del
  catálogo, captura su link de Cowork si ya existe, o lo deja *pendiente* apuntando al skill que lo
  produce (wireframes → `pc-crm-salesforce-wireframe-builder`). Se quita Claude-in-Chrome del pre-flight.
- PASO 5: los visuales de Cowork sí se registran como `Project_Asset__c` (`WireframeId`/`CoworkArtifactId`).
- `references/claude-design-chrome.md` marcado como deprecado (histórico).

## 1.0.0 — 2026-07-17
- Versión inicial. Organiza el espacio de trabajo de un proyecto de delivery:
  - **Drive:** crea el árbol de subcarpetas por fase del proceso dentro de la carpeta raíz del
    proyecto (idempotente; no re-crea la raíz de project-builder).
  - **Claude Design:** crea un proyecto de Design por artefacto visual (AS-IS, TO-BE, Wireframes v2,
    y opcionalmente ERD y arquitectura de integraciones) vía Claude-in-Chrome, con fallback
    semi-automático (placeholder + link manual) cuando no hay sesión/Chrome.
  - **Jira:** crea un issue `Artifact` (workflow Deliverable) por entregable, con su link (Drive o Design).
  - Punto de entrada: `Project__c` de Salesforce; reutiliza `Project_Asset__c.GoogleDriveFolderId`.
  - Registro `Project_Asset__c` limitado a tipos con valor de picklist válido (no inventa tipos).
- Distribución: plugin `procontacto-delivery` (grupo `delivery/*`, auto-install + VS Code). No excluido.
- Catálogo de artefactos derivado de `pc-delivery-blueprint-guide` (5 fases / 4 gates / 10 entregables).
