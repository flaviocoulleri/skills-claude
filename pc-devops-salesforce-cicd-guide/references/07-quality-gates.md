# 07 · Quality Gates

> Fuente canónica: Confluence PROCMOD — "Quality Gates: Reglas Automatizadas y Estrategias de Evaluación" (`2082045969`).

## 1. ¿Qué son?

Reglas automatizadas que el pipeline (Bitbucket Pipelines) y los entornos locales (Git pre-commit / Husky) evalúan **antes** de permitir que el código avance al siguiente ambiente.

## 2. Reglas estrictas (BLOQUEANTES)

Si alguna se rompe, el PR o el pipeline **falla automáticamente**:

- **Cobertura de Apex (Code Coverage):** mínimo **95%** a nivel de Org. El pipeline corre `RunLocalTests` en los deploys de `test`/`main` para garantizarlo.
- **Análisis estático (Code Analyzer):** ningún código nuevo puede contener vulnerabilidades de **Severidad 1 (Crítica)** ni **Severidad 2 (Alta)** identificadas por Salesforce Code Analyzer (PMD/ESLint).

> 🔴 El mínimo es **95%**, no 90. Si el usuario menciona 90, corregir y citar esta página (`2082045969`).

## 3. Reglas de advertencia (NO bloqueantes)

Si Code Analyzer encuentra problemas de **Severidad 3 o superior (Warnings/Low)**, el pipeline los reporta como **comentario en la línea afectada** dentro del PR de Bitbucket para revisión, pero **el pipeline sigue siendo exitoso** y permite el merge.

## Cómo correrlo localmente (read-only)

```bash
sf code-analyzer run --rule-selector Recommended
sf apex run test --synchronous --code-coverage --result-format human --target-org <alias>
```

Estos son read-only (modo report) → se pueden correr sin pedir ✅. El reporte de quality gates que genera el skill se arma con la salida de coverage + Code Analyzer.
