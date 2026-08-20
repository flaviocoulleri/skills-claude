# 12 · Rollback + post-deploy

> Fuente canónica: Confluence PROCMOD — "Tareas Post-Despliegue y Rollback" (`2082013248`).

## 1. Tareas post-despliegue

Salesforce muchas veces requiere configuración **manual** post-deploy que el Metadata API y el pipeline no gestionan:

- Asignación de Permisos o Grupos.
- Inserción/actualización de registros (**Data Seeding**).
- Pasos manuales requeridos por Managed Packages.

**Qué hacer:** toda Tarea Post-Despliegue debe estar **documentada en el ticket de Jira** del dev **antes** de crear el PR. Cuando el pipeline termina el deploy exitosamente, una persona designada (Tech Lead/Dev) abre el despliegue, verifica la org destino y **ejecuta manualmente** las tareas de configuración/Data Seeding acordadas en el ticket.

## 2. Estrategia de rollback

**No existe un botón "Undo" nativo** en el pipeline. Si se desplegó algo destructivo o equivocado, la metadata ya fue reescrita en la org. Para revertir:

1. **Revertir en Git:** en Bitbucket, buscar el Commit o PR a deshacer y hacer un **Revert** → crea un nuevo commit estructuralmente inverso al anterior.
2. **Volver a purgar (destructive automático):** si habías agregado archivos, el Revert los borra localmente y el pipeline usa **sfdx-git-delta** para generar un `destructiveChanges.xml` y eliminarlos de la plataforma (ver módulo 09).
3. **Si es Data/Registros:** NO se soluciona revirtiendo metadata. Hay que ejecutar consultas manuales para corregir los datos, o restaurar con un **Salesforce Data Backup** si hubo corrupción severa.

> `git revert` y el deploy resultante son **write** → pedir ✅. El rollback de metadata sigue el mismo camino de PR + pipeline que cualquier cambio.
