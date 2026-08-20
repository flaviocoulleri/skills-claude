# 04 · Flujo diario de trabajo

> Fuente canónica: Confluence PROCMOD — "Proceso de trabajo" (`2082144267`). Flujo programático y declarativo, del ticket Jira al PR y la promoción a ambientes superiores.

## Pre-requisito

Tener las tareas **definidas y asignadas en Jira**, con detalle suficiente para identificar qué cambios hacer. Esas tareas son la base para trackear y versionar los cambios.

## Rol Administrador (cambios declarativos)

1. Seleccionar una tarea asignada en el sprint.
2. Hacer las configuraciones declarativas necesarias en la **org de desarrollo**.
3. Al terminar, **coordinar con el desarrollador** de despliegue para identificar la metadata a versionar y correr las validaciones. (El admin no versiona solo — ver "cambios no programáticos".)

## Rol Desarrollador — cambios programáticos (Apex/LWC)

```bash
# 1. Actualizar develop local
git checkout develop
git pull origin develop

# 2. Crear rama desde la task de Jira
git checkout -b feature/COLOM-303        # COLOM-303 = task key de Jira

# 3. Commits pequeños y frecuentes (Conventional Commits — ver módulo 03)
git add .
git commit -m "feat(...): descripción acorde a los cambios"

# 4. Subir la rama (si no existe remota aún)
git push -u origin feature/COLOM-303
```

5. **Crear un Pull Request contra `develop`.** Lo revisa el administrador del repo; corren validaciones automáticas (ej. Salesforce Code Analyzer). Si no pasa el Code Review, ajustar hasta aprobación.
6. Al aprobarse → **merge a `develop`**.
7. Actualizar la rama local para continuar: `git checkout develop && git pull origin develop`.

## Rol Desarrollador — cambios NO programáticos (metadata declarativa)

```bash
git checkout develop && git pull origin develop
git checkout -b feature/COLOM-766

# Previsualizar metadata modificada en dev (read-only)
sf project retrieve preview --target-org $DEV_SFDX_USERNAME

# Recuperar los cambios de metadata (write local)
sf project retrieve start --target-org $DEV_SFDX_USERNAME --metadata CustomObject:MiObjeto__c
```

> **💡 Alternativa visual (VSCode Org Browser):** ícono de la Nube en la barra lateral → navegar la metadata (ej. Custom Objects), buscar el componente y clic en descargar (*Retrieve Source from Org*). Útil para juniors que prefieren no usar la consola.

- **Limpiar** cualquier XML bajado por accidente o config en progreso que **no** pertenezca al ticket actual.
- **Validar contra Testing:** `sf project deploy validate --target-org $TEST_SFDX_USERNAME --source-dir force-app` — corregir incompatibilidades antes de seguir.
- Commit + push de la metadata validada, y **PR contra `develop`**. Acá el code review es **automático** (no hay código, solo metadata).
- Actualizar `develop` local.

## Deploy a ambientes superiores (promoción)

- Para promover, se crea un **PR desde la rama de origen hacia la rama del ambiente superior**.
- Al aprobarse el PR, el **pipeline de Bitbucket** valida y despliega automáticamente en el destino.
- **Validaciones post-deploy por ambiente:**
  - `test` → QA interno (funcional + automatizado).
  - `qa` → validación con el cliente.
  - `uat` → pruebas de carga y aceptación final.
  - `productivo` → smoke tests y validación final.

> Toda promoción es **vía PR** — nunca push directo a `develop`/`test`/`qa`/`uat`/`main`.
