# 11 · Hotfix + back-merge

> Fuente canónica: Confluence PROCMOD — "Estrategia de Hotfixes y Back-Merging" (`2082144289`).

## 1. El escenario de hotfix

Un **hotfix** ocurre cuando hay un bug crítico en Producción que **no puede esperar** al ciclo de release regular. Se parchea inmediatamente.

## 2. Flujo de trabajo

1. **Crear rama:** en Bitbucket, rama nacida **directamente desde `main`** (NO desde `develop` ni `test`). Nombre: `hotfix/nombre-del-bug` (o `hotfix/PROC-XYZ-...`).
2. **Corrección:** descargar la rama a local, conectarse al Sandbox de desarrollo o a un Sandbox dedicado de hotfix y hacer la corrección.
3. **Validación:** commit normal (Conventional Commits) + **PR contra `main`**. Bitbucket valida estáticamente y prueba el despliegue como siempre.
4. **Despliegue a Producción:** aprobar y mergear el PR → el pipeline despliega el hotfix en Producción.

## 3. 🔴 Back-merge (¡OBLIGATORIO!)

Una vez que `main` tiene el parche, **el resto de los ambientes quedaron desactualizados** (les falta la corrección). Si no se arregla, en el siguiente pase a producción **se re-introduce el bug** y se rompe la automatización.

**Inmediatamente después del hotfix en Producción**, crear **Pull Requests desde `main` hacia todas las demás ramas de ambientes estables** (`develop`, `test`, `qa`, `uat`) — un **back-merge**. Esto alinea a todos los devs con el parche que subió a Producción.

**No es opcional.** Si el usuario dice "ya está, hicimos el hotfix", recordarle el back-merge a `develop`, `test`, `qa`, `uat`.

> Todos los `git merge` y el deploy son **write** → pedir ✅. La rama de hotfix sale de `main`, nunca de `develop`.
