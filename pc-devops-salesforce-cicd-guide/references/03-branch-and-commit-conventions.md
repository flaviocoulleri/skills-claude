# 03 · Convenciones de ramas y commits

> Fuente canónica: Confluence PROCMOD — "Convenciones Estrictas de Ramas y Commits" (`2082078735`). Estándar **Conventional Commits** + naming de Git, para historial limpio y Release Notes automatizadas.

## 1. Nomenclatura de ramas

Toda rama lleva un **prefijo lógico** + un **ticket de Jira** representativo (enlaza el código con el tablero):

| Prefijo | Para qué |
|---|---|
| `feature/PROC-XYZ-descripcion` | Nuevas funcionalidades, LWC, objetos nuevos. |
| `bugfix/PROC-XYZ-descripcion` | Reparar errores identificados en QA o UAT. |
| `hotfix/PROC-XYZ-descripcion` | **Exclusivamente** errores críticos en Producción; nace directo de `main`. |
| `chore/PROC-XYZ-descripcion` | Mantenimiento (dependencias, scripts de pipeline) que no afecta Salesforce. |

**Ejemplo correcto:** `feature/PROC-102-alta-clientes`

> El skill puede proponer el nombre de rama desde un ticket Jira (ver `scripts/propose-branch-name.sh`).

## 2. Conventional Commits

`git commit -m` **no** admite texto libre ("Corregido el error", "WIP"). Estructura obligatoria:

```
<tipo>[scope opcional]: <descripción breve en infinitivo>
```

**Tipos permitidos:**

| Tipo | Uso |
|---|---|
| `feat` | Nueva funcionalidad (clase, LWC nuevo). |
| `fix` | Corrección de un defecto. |
| `docs` | Cambios solo en README / documentación. |
| `style` | Cambios que no afectan el significado del código (espacios, formateo). |
| `refactor` | Cambio que ni arregla bug ni añade feature (ej. renombrar variable). |
| `perf` | Mejora de rendimiento. |
| `test` | Agregar/corregir tests Apex/LWC. |
| `chore` | Build, `package.json`, herramientas auxiliares. |

**Ejemplos válidos:**

```
feat(lwc): crear componente de facturación interactiva
fix(apex): manejar el NullPointerException en el trigger de Contacto
docs(cicd): agregar mapa mental de branches en readme
test(apex): incrementar cobertura de AccountService al 98%
```

**Blocklist (regla del skill):** `fix`, `update`, `WIP`, `asdf`, textos libres sin prefijo. Si el mensaje propuesto no cumple, **regenerarlo** (ver `scripts/validate-commit-msg.sh`).

**Por qué importa:** seguir esta estructura habilita a futuro el plugin **`semantic-release`**, que lee los prefijos para compilar y publicar automáticamente las Release Notes (PDF) sin intervención humana.
