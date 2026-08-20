# Estructura de carpetas de Drive — destino de presentaciones (delivery)

> **Qué es esto.** La ruta de Drive donde se archivan las presentaciones **de delivery**,
> usada por el **Paso 4.8** del SKILL.md (procedimiento común en `_shared/references/common-rules.md`).
> Los IDs raíz son fijos; los nombres llevan prefijo de orden (`J -`, `B -`) y se muestran **tal cual**
> en los widgets.

## Ruta destino

**Delivery** — `J - Delivery / B - Proyectos / {Cliente} / {Proyecto}`

| Nivel | Nombre real | ID | Cómo se resuelve |
|---|---|---|---|
| 1 | `J - Delivery` | `1R9MnqEWesNFN2iwTP7yG1xfNDRP1Ihxu` | fijo |
| 2 | `B - Proyectos` | `1TlZt2nV_kNcML1U_RBBYlaoITSUNRxUP` | fijo |
| 3 | `{Cliente}` | crear | Account del proyecto |
| 4 | `{Proyecto}` | crear | `Project__c.Name` |

> Delivery **no** tiene nivel de país: el cliente cuelga directo de `B - Proyectos`.

## Reglas

1. **Crear de arriba hacia abajo**: navega nivel por nivel; el primer nivel inexistente y los siguientes se crean con `create_file` (`mimeType: application/vnd.google-apps.folder`, `parentId` del padre), **siempre con confirmación del usuario** (widget `_shared/assets/drive-folder-path.html`, `{{AREA_LABEL}}` = "Delivery").
2. **Nunca** uses la carpeta de bases de delivery (`1Tdy-IVpVhDmMECODq_bhZBdIfS5wqu_F`, plantillas) como destino de entregables.
3. **Drive es la fuente de verdad**: si un ID cacheado ya no resuelve, reconcilia por nombre y actualiza esta tabla.

## Permisos — solicitar a Ariel por Slack

Si el skill **no tiene acceso** a `B - Proyectos` (o a un subnivel necesario) — `get_file_metadata` falla o la carpeta no aparece — **no sigas a ciegas**:

1. Busca a **Ariel Tarsitano** en Slack: `slack_search_users` por `ariel.tarsitano@procontacto.com.mx`.
2. Mándale un DM (`slack_send_message`) pidiendo **acceso de editor** a la carpeta, con el link y el motivo. Ej: _"Hola Ariel, necesito acceso de editor a la carpeta `{nombre}` ({link}) para guardar la presentación del proyecto {proyecto}. ¿Me lo habilitas? Gracias."_
3. Avisa que el prompt se genera igual, pero **el destino de Drive queda pendiente** hasta que Ariel habilite el acceso (o el usuario elija "No subir a Drive"). Nunca dejes un placeholder de carpeta ni inventes el acceso.

Owner de las carpetas raíz: `ariel.tarsitano@procontacto.com.mx`.
