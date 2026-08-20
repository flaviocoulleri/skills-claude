# Fuentes de datos y reconciliación contexto ↔ registry

Este skill combina dos fuentes. Entender el rol de cada una es lo que lo hace
**dinámico y contextual** (muestra los skills de *quien* pregunta) sin perder
profundidad.

## 1. Lista viva del contexto (qué mostrar)

El harness inyecta en la sesión una lista de "available skills" (nombre +
description) — son exactamente los que **esta persona** tiene habilitados según su
área. Esa lista es la **verdad de qué skills existen para este usuario**.

- Puede incluir skills de ProContacto (`pc-...`) y de Anthropic (`pptx`, `docx`,
  `data:*`, `find-skills`, etc.).
- Cambia de persona a persona. Nunca asumas un catálogo fijo.

## 2. Registry embebido (con qué profundidad explicarlos)

`assets/skill-registry/registry.json` — copia embebida generada por
`_shared/skill-registry/build_registry.py`. Trae por skill: `one_liner`,
`connectors` (+ `connectors_source`), `steps`, `when_to_use`, `writes`, `type`,
`area`, `help_quality`.

## Algoritmo de reconciliación

```
disponibles = skills del contexto (available skills)
registry    = leer assets/skill-registry/registry.json → mapa por name

para cada s en disponibles:
    ficha = registry[s.name]  si existe
            si no: ficha mínima desde la description en contexto
                   (one_liner = 1ª frase; connectors_source = "none";
                    steps = []; marcar como "aprox.")
    incluir ficha

# Nunca incluir un skill del registry que NO esté en `disponibles`.
```

### Casos borde

- **Skill en contexto pero no en registry** (p. ej. `pptx`): explicá desde su
  description. Decí que el paso a paso detallado no está en el registry.
- **Skill en registry pero no en contexto**: NO lo listes. Si el usuario lo nombró
  explícitamente, avisá que no lo tiene disponible y ofrecé `find-skills`.
- **Registry ausente/vacío**: trabajá solo con el contexto; avisá que la
  explicación es de alto nivel.

## Honestidad sobre conectores (`connectors_source`)

| source | Cómo presentarlo |
|---|---|
| `declared` | "Usa: …" — confiable (el skill lo declara en su frontmatter). |
| `requiere-line` | "Requiere: …" — lo dice su description. |
| `inferred` | "Probablemente usa: …" + "(inferido; puede no ser exacto)". |
| `none` (declarado vacío) | "No usa conectores externos." |
| `none` (inferencia vacía) | "No detecté conectores." |

Nunca presentes un conector `inferred` como requisito duro: un skill que *menciona*
Salesforce en un ejemplo no necesariamente lo *usa*. Esta ambigüedad desaparece a
medida que los skills adoptan **Q10** (declarar `metadata.connectors`).
