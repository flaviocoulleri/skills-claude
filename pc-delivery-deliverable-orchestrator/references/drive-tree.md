# Árbol de subcarpetas Drive (por fase del proceso)

Se crean **dentro** de la carpeta raíz del proyecto (`Project_Asset__c.GoogleDriveFolderId`).
El skill NO crea la raíz (la crea `pc-delivery-sf-project-builder`).

## Estructura

```
{Proyecto} (raíz — ya existe)
├── 00 · Comercial                        (links a SOW comercial, propuesta, contrato firmado)
├── 01 · Sprint 0 – Diseño
│   ├── AS-IS · TO-BE
│   ├── Historias de Usuario (Anexo B)
│   ├── Wireframes (Anexo C)              ← soporte; el diseño vive en un artefacto de Cowork
│   ├── Diccionario de datos
│   ├── Integraciones
│   ├── Plan de datos
│   └── Scope Freeze (SOW vF · Acta · exclusiones)
├── 02 · Gobierno
│   ├── RACI y ceremonias
│   ├── RAID log
│   ├── Status semanales
│   └── Control de cambios (CRs)
├── 03 · Ejecución
│   ├── Demos
│   └── Documentación técnica (ADRs)
├── 04 · UAT
│   ├── Plan de UAT
│   ├── Casos y evidencia
│   └── Acta de aceptación
├── 05 · Go-live y cierre
│   ├── Runbook / go-live
│   ├── Acta de cierre
│   └── Hypercare
└── 99 · Insumos del cliente             (plantillas de datos, credenciales doc, etc.)
```

## Mecánica de creación (idempotente)

Preferir la MCP de Google Drive. Por cada carpeta:

1. **Buscar** dentro del padre antes de crear:
   - MCP: `search_files` con `q` = `'<parentId>' in parents and name = '<Nombre>' and mimeType = 'application/vnd.google-apps.folder' and trashed = false`.
   - Si existe → reusar su `id` como `parentId` de sus hijas. No duplicar.
2. **Crear** si no existe:
   - MCP `create_file`: `title` = `<Nombre>`, `contentMimeType`/`mimeType` = `application/vnd.google-apps.folder`, `parentId` = `<padre>`.
3. Crear **nivel por nivel** (primero las 8 de nivel 1, luego las hijas de cada una).
4. Guardar el mapa `{ruta → folderId}` para poner los links en los issues `Artifact` y en el resumen.

## Notas

- Los nombres llevan el separador ` · ` (punto medio) y el número de fase con cero a la izquierda para
  que ordenen alfabéticamente en Drive.
- No borrar ni renombrar carpetas existentes que no encajen en el árbol; reportarlas en el resumen para
  que el DM decida (regla 5 del SKILL).
- Los archivos de contenido NO se crean acá (los generan los skills de cada entregable). Este skill
  solo deja las carpetas.
