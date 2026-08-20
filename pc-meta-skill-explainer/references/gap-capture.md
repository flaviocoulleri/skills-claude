# Captura del skill faltante — mapeo de campos

Cómo registrar un **gap real** (la persona necesitaba algo y no hay skill que lo
haga, ni en su contexto ni en el registry) para que Ariel lo pueda crear.

Es la **única escritura** de `pc-meta-skill-explainer`. Siempre con OK explícito del
usuario, y siempre después de descartar las otras dos salidas del Paso R4:

1. El skill existe y lo tiene → handoff, no hay gap.
2. El skill existe pero no está en su contexto → **problema de distribución**, no un
   skill faltante. Se avisa distinto (ver el final de este archivo).
3. No existe → esto.

## Antes de escribir: buscar duplicados

Los gaps se repiten (varias personas chocan con lo mismo). Antes de crear:

```
JQL: project = PROCSKILLS AND labels = "skill-gap" AND statusCategory != Done
```

Si hay una issue abierta cuyo pedido es el mismo, **comentá ahí** (sumá el rol de
quien pidió y el caso concreto) y decile al usuario que el pedido ya estaba y que
sumaste su caso — eso es señal de demanda, vale más que una issue nueva.

## Issue en PROCSKILLS

**Tablero**: https://procontacto.atlassian.net/jira/software/c/projects/PROCSKILLS/boards/2952
**Project Key**: `PROCSKILLS`

| Campo Jira | Cómo completarlo |
|---|---|
| `project` | `PROCSKILLS` |
| `issuetype` | `Task` |
| `summary` | `[skill-gap] <área>: <qué necesitaba, ≤70 chars>` |
| `description` | Plantilla de abajo |
| `priority` | `High` si el pedido es recurrente y bloquea trabajo facturable · `Medium` si es recurrente · `Low` si fue un caso puntual |
| `labels` | `["skill-gap", "area:<área>", "source:router", "auto-generated"]` |
| `assignee` | Ariel Tarsitano (dueño del catálogo) |
| `reporter` | El usuario actual |

No inventes un nombre de skill en el `summary`. La convención
`pc-[área]-[sistema]-[objeto]-[acción]` la resuelve `pc-meta-skill-manager` cuando el
pedido se toma; un nombre inventado acá se pega y después nadie lo corrige.

### Plantilla de description

```
## Qué necesitaba hacer

{en las palabras del usuario, una o dos frases}

## Quién lo pidió

- **Persona**: {nombre}
- **Rol / área**: {rol} / {área}
- **Skills que tenía disponibles**: {N} ({áreas presentes en su contexto})

## Sistemas involucrados

{Salesforce / Jira / Drive / Odoo / Slack / … o "ninguno"}

## Qué terminó haciendo

{lo hizo a mano / lo dejó / lo resolvió parcial con el skill X}

## Frecuencia

{recurrente — {cada cuánto} | puntual | no lo sabe}

## Por qué no lo cubre nada existente

{qué skills se evaluaron y por qué no aplican — sé concreto, esto es lo que evita
que se cree un duplicado}

## Próximo paso

Definir nombre y alcance con `pc-meta-skill-manager` (convención
`pc-[área]-[sistema]-[objeto]-[acción]`) antes de construir.

---

*Registrada automáticamente por pc-meta-skill-explainer (modo enrutador) al no
encontrar ningún skill que cubriera el pedido.*
```

## DM a Ariel en Slack

Resolvé el usuario por email (`ariel.tarsitano@procontacto.com.mx`) con
`slack_search_users`; no hardcodees el ID. Un DM por issue creada — si comentaste en
una issue existente, mandá el DM solo si el label de prioridad sube.

```
:jigsaw: *Skill faltante* — {área}

{Persona} ({rol}) necesitaba: {qué quería lograr}
Sistemas: {sistemas} · Frecuencia: {frecuencia}
Terminó: {qué hizo a mano}

Evaluados y descartados: {skills}

Issue: {link a PROCSKILLS}
```

## Caso distinto: existe pero no lo tiene (distribución)

No es un gap: no crees issue de `skill-gap`. Avisale a Ariel por DM con el arreglo
concreto, que es de configuración y no de construcción:

```
:electric_plug: *Skill existente sin distribuir*

{Persona} ({rol}, área {área}) necesitaba `{skill}` y no lo tiene en su contexto.
Revisar: grupo en `config.json` / mapeo en `_areas.json` / bundle `.skill` subido.
```

Y a la persona decile la verdad completa: el skill existe, para qué sirve, y que
pediste que le habiliten el acceso — así no arranca a hacerlo a mano creyendo que no
hay nada.
