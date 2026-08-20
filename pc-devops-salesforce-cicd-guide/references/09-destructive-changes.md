# 09 · destructiveChanges (eliminar metadata)

> Fuente canónica: Confluence PROCMOD — "Eliminación de Componentes (destructiveChanges)" (`2082308133`).

Eliminar metadata en Salesforce requiere decirle explícitamente qué borrar vía un archivo `destructiveChanges.xml`. Con **sfdx-git-delta** el proceso es natural dentro del flujo de Git:

## Flujo (el dev NO arma el XML a mano)

1. **Elimina el archivo localmente** — con el IDE o la terminal, borra el archivo que ya no necesitas dentro de `force-app` (un campo custom, una clase, etc.).
2. **Commit de la eliminación** — haz Stage de la eliminación y un commit regular (Conventional Commits).
3. **Push** a Bitbucket.
4. **SGD hace la magia** — durante el pipeline, SGD detecta que el archivo estaba en la rama principal y ya no está en tu rama, **genera automáticamente el `destructiveChanges.xml` en caliente** y ejecuta la eliminación contra Salesforce.

## Regla

**No hace falta crear el `destructiveChanges.xml` a mano nunca más**, siempre y cuando:
- el archivo **existía previamente** en Bitbucket y Salesforce, y
- tú simplemente lo eliminas del árbol de Git y pusheas.

> El deploy destructivo se aplica en la promoción vía PR como cualquier otro cambio — es un **write** contra la org, así que la confirmación ✅ y las validaciones normales aplican.
