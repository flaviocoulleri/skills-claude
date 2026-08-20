# 08 · sfdx-git-delta (SGD)

> Fuente canónica: Confluence PROCMOD — "Sfdx-Git-Delta (SGD) y Optimización de Tiempos de Deploy" (`2082242583`).

## 1. El problema: deploy de org completa

Por defecto, al crear un PR las herramientas toman **toda** la carpeta `force-app` y validan miles de componentes contra la org destino → validaciones de **20 a 45 minutos** por commit, ralentizando el ciclo.

## 2. La solución: SGD

**sfdx-git-delta** es un plugin oficial de la comunidad que compara la rama del PR (ej. `feature/XYZ`) contra la rama destino (`develop` o `main`) e identifica **exactamente qué archivos** se modificaron, añadieron o eliminaron.

En vez de desplegar toda la carpeta, SGD empaqueta **solo los componentes modificados** en una carpeta `delta`, y el pipeline valida exclusivamente sobre ella.

**Resultado:** tiempos de validación reducidos a **1–2 minutos**.

## 3. Casos de uso del día a día

- **Trabajo normal de un dev:** no hay que hacer nada especial. Commit + push; el pipeline de Bitbucket aísla la diferencia automáticamente.
- **Componentes anidados (bundles):** SGD es inteligente. Si modificas solo el JS de un LWC, empaqueta **todo el bundle** (`html`, `js`, `meta.xml`) porque Salesforce requiere el bundle completo para desplegar.

> Cuando el usuario pregunte "por qué el deploy tarda tanto" o "por qué solo se despliega lo cambiado", es esto: SGD calcula el delta y despliega únicamente lo modificado.
