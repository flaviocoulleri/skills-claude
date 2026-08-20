# Crear el issue `Artifact` en Jira (uno por entregable)

El work type real es **`Artifact`** (workflow "0 - Implementation Workflow Deliverable v1"),
categoría Blueprint / entregables. **NO** es `Artefacto` (bug de JQL en español documentado).
Issuetype id conocido: **10209** — igual, **verificar en runtime** con el metadata de la org.

## Precondición

- MCP Atlassian disponible. Tools: `getVisibleJiraProjects` / `getJiraProjectIssueTypesMetadata`,
  `getJiraIssueTypeMetaWithFields`, `createJiraIssue`, `getJiraIssue`.
- Detectar `cloudId` en runtime (no hardcodear). Site: `procontacto.atlassian.net`.
- Proyecto Jira del cliente: del `Project_Asset__c` (`JiraProjectKey` / `JiraProjectId`) resuelto en el PASO 1.

## Receta (por cada entregable aplicable del catálogo)

1. **Metadata:** `getJiraIssueTypeMetaWithFields` para el proyecto → confirmar el `id`/`name` real de
   `Artifact` y los **campos requeridos** de la screen (pueden variar por proyecto; no asumir).
2. **Buscar duplicado:** JQL `project = <KEY> AND issuetype = "Artifact" AND summary ~ "<entregable>"`.
   Si ya existe → **reusar** (no crear otro). Si el link cambió, ofrecer editarlo, no duplicar.
3. **Crear:** `createJiraIssue` con:
   - `project` = key del proyecto Jira del cliente.
   - `issuetype` = `Artifact` (id verificado).
   - `summary` = nombre del entregable (del catálogo, ej. "Wireframes v2 · Anexo C").
   - `description` (ADF/markdown según la tool):
     - Propósito breve del entregable.
     - **Link**: la URL del gestor de ProContacto (`artifacts.procontacto.com.mx/a/<uuid>`),
       con la carpeta de Drive como respaldo si además se subió. Los
       `claude.ai/code/artifact/<uuid>` que aparezcan son de artefactos viejos: sirven para
       encontrar el entregable, no como link a compartir. Si el link quedó pendiente → texto explícito:
       *"Pendiente: generar el artefacto con {skill} y pegar el link"*.
     - Skill que lo produce (del catálogo) — para que el equipo sepa con qué generarlo.
     - Fase / gate al que pertenece.
   - `reporter` = usuario actual (el que corre el skill), si la tool lo permite.
   - Completar cualquier campo **requerido** que devuelva el metadata del paso 1.
4. **Verificación post-write:** `getJiraIssue` del issue creado → confirmar summary/issuetype/link antes
   de reportar éxito. Mostrar el link clickeable:
   `https://procontacto.atlassian.net/browse/<ISSUE-KEY>`.

## Notas

- **Granularidad:** un `Artifact` por entregable (decisión de diseño). No agrupar por carpeta.
- Para lógica compleja de campos, relaciones o alta masiva, delegar a `pc-delivery-jira-issue-builder`
  (dueño canónico del CRUD). Para el alta simple de `Artifact`, este skill la hace directo.
- Si el proyecto Jira usa componentes/labels por fase, aprovecharlos para etiquetar el `Artifact`
  (leerlos del metadata; no inventarlos).
