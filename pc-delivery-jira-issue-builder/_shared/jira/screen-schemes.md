<!-- AUTO-COPIADO desde _shared/jira/ — NO EDITAR ACÁ. Edita la fuente en _shared/jira/ y corre _shared/jira/sync.sh. -->

# Jira ProContacto — Screen Schemes por issuetype

> Complemento de `issuetypes-and-workflows.md`. Mapea cada issuetype a su **screen
> scheme** (qué pantalla, y por lo tanto qué set de campos, usa). Confirma que cada
> issuetype tiene su propio set de campos → ningún skill debe asumir un set fijo.
> Fuente: config de Jira (screen schemes), provista por Ariel 2026-07-13.
>
> ⚠️ Esto da el **screen scheme por issuetype**, NO la lista de campos dentro de cada
> screen. Para los campos concretos: expandir cada screen en la config, o introspectar
> con `getJiraIssueTypeMetaWithFields`. Volcar a `issuetype-field-mapping.md`.

| Issuetype | Screen Scheme | Shared by |
|---|---|---|
| Incidente Seguridad Informatica, Internal Pending | `Default Screen Scheme` (DEFAULT) | 117 |
| Story | `0 - Screen Scheme Story` | 121 |
| Epic | `1 - Screen Scheme Epic` | 121 |
| Task (DEFAULT), Sub-task | `3 - Screen Scheme Task` | 121 |
| QAlity Test | `3 - Screen Scheme QAlity Test` | 116 |
| Weekly Status | `4 - Screen Scheme Weekly Status` | 117 |
| External Pending | `5 - Screen Scheme External Work` | 116 |
| Bug | `6 - Screen Scheme Bug` | 120 |
| Artifact | `7 - Screen Scheme Artifact` | 116 |
| Acceptance Certificate | `9 - Screen Scheme Acceptance Certificate` | 116 |
| Feedback Tracker | `10 - Screen Scheme Feedback Tracker` | 116 |
| Project Details | `12 - Screen Scheme Project Detail` | 116 |
| Exploratory Testing | `13 - Screen Scheme Exploratory Testing` | 116 |
| Story Bug | `14 - Screen Scheme Story Bug` | 116 |
| Opportunity for improvement | `15 - Screen Scheme Opportunity for improvement` | 116 |
| Change Control | `16 - Screen Scheme Change Control` | 116 |

Total: 16 screen configurations, casi todas compartidas org-wide (~116-121 proyectos).

## ✅ Confirmaciones clave
- El work type real es **`Artifact`** (no `Artefacto`). El screen scheme es "Artifact".
  → **Bug confirmado** en `pc-delivery-blueprint-guide` y `pc-delivery-jira-project-auditor`,
  que hardcodean JQL `issuetype = "Artefacto"` (valor inexistente → error de validación de
  JQL → caen al camino manual y nunca encuentran los artefactos). Ver también
  `pc-delivery-sf-project-builder`. Fix: usar `Artifact` (o resolver el name/id real vía
  `getJiraProjectIssueTypesMetadata` antes de armar la JQL).
- `External Pending` → screen scheme "External Work" (nombre del screen ≠ nombre del issuetype).
- `Task` y `Sub-task` comparten screen scheme y workflow (Task v4).
