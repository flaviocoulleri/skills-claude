---
name: pc-meta-presentation-builder
metadata:
  version: 1.1.0
  last_modified: 2026-08-03
description: >
  Punto de entrada ÚNICO y OBLIGATORIO para armar CUALQUIER presentación, deck, propuesta, slides,
  PPT o pitch de ProContacto — úsalo aunque el usuario diga "PowerPoint", ".pptx" o "en PPT": el
  deck se construye acá como artefacto HTML y el .pptx sale exportado de él (no invoques la skill
  pptx/docx). Pregunta primero para qué área es (Comercial / Delivery / …) vía widget y deriva
  —transición invisible— al skill especializado; el router no arma nada, sólo rutea. ACTIVAR con
  "quiero crear/armar una propuesta o presentación", "propuesta/presentación para la empresa X",
  "ármame una presentación/deck/slides/PPT/PowerPoint", "necesito un deck", "haz un pitch",
  "presentarle algo al sponsor/comité"; EN: "make/build a deck/presentation/slides/pptx", "create a
  proposal". Proactivo con transcript/RFP/brief. Si el pedido ya nombra el tipo (propuesta,
  cotización, POC, first call → Comercial; kickoff, steering, status, cierre → Delivery), confirma
  el área y deriva. ES/EN.
---

# pc-meta-presentation-builder

## Para qué existe este skill

ProContacto arma presentaciones de dos naturalezas muy distintas: **comerciales** (propuestas a clientes, por Record Type de Opportunity, con pricing de Salesforce) y de **delivery** (kickoff, steering, status, cierre de proyectos activos). Cada una tiene su propio skill especializado, que vive en el plugin de su área (`procontacto-comercial`, `procontacto-delivery`).

Este skill es el **front-door transversal**: cuando el pedido del usuario es genérico ("ármame una presentación") o no deja claro el área, este router pregunta para qué área es y **deriva al skill correcto** con una transición invisible. No captura contexto de cliente, no barre conectores, no ensambla prompts — todo eso lo hace el skill especializado. Su única responsabilidad es rutear bien y rápido.

> **Por qué existe como skill aparte.** Los skills especializados se disparan solos cuando el pedido ya nombra el tipo (una "propuesta" activa el comercial; un "kickoff" activa el de delivery). Pero un pedido genérico o ambiguo necesita un lugar que desambigüe sin adivinar. Ese es este router.

## El registry de áreas

El router conoce las áreas desde esta tabla. **Para sumar un área nueva**: agrega una fila acá y una card al widget `assets/widgets/paso0-area.html` — nada más.

| Área | Skill destino | Qué presentaciones cubre | Ejemplos de pedido |
|---|---|---|---|
| **Comercial** | `pc-sales-presentation-builder` | Propuestas a clientes por Record Type (Project, Quickstart, POC, Support, Change Control, Marketing, Training, Outsourcing, Assessment), pitches, first-call decks; con pricing de Salesforce o base de Drive. | "propuesta", "cotización", "orden de magnitud", "first call deck", "pitch para el cliente", "POC", "soporte", "outsourcing" |
| **Delivery** | `pc-delivery-presentation-builder` | Presentaciones de proyectos activos: kickoff, sprint review, steering, status/weekly, mid-project, cierre/aceptación, retro. | "kickoff", "steering", "weekly status", "presentación de status", "carta de aceptación", "cierre de proyecto", "retro" |

## Flujo de trabajo

### Paso 1 — Preguntar el área (o confirmar la inferida)

**Llama a `mcp__visualize__read_me` antes del primer widget** (preparación silenciosa, no la narres). Después muestra el widget `assets/widgets/paso0-area.html` con `mcp__visualize__show_widget` — una card por área del registry (Patrón A: icono + título + descripción + "ideal para…").

- **Si el pedido ya sugiere un área** (nombró "propuesta", "kickoff", etc.), muestra igual el widget pero con la opción inferida como recomendada, para que el usuario confirme o corrija antes de derivar. No derives a ciegas.
- **Nunca** listes las áreas como bullets en el chat ni uses `AskUserQuestion` — siempre el widget.
- Idioma del widget = idioma de la conversación.

### Paso 2 — Derivar al skill especializado (transición invisible)

Con el área elegida, **invoca el skill destino del registry** y deja que ese skill maneje todo el resto del flujo (captura, conectores, ensamble, entrega del prompt).

- La transición es **invisible**: no le menciones al usuario el nombre técnico del skill. Háblale en lenguaje natural — "Perfecto, vamos con la presentación comercial" / "Dale, armamos la del proyecto" — y sigue.
- Pásale al skill destino todo el contexto que el usuario ya haya dado (cliente/proyecto, tipo de deck, transcript/brief adjunto) para que no lo vuelva a pedir.
- A partir de la derivación, el router no vuelve a intervenir: el skill especializado es el dueño del flujo.

## Reglas inviolables

- **El router NO construye la presentación.** Su salida es la derivación al skill de área. Si te encuentras capturando datos de cliente, barriendo conectores o ensamblando un prompt, algo salió mal: eso es trabajo del skill especializado.
- **Siempre confirma el área con el widget** antes de derivar, aun cuando el pedido parezca obvio. La confirmación cuesta un click y evita armar el deck equivocado.
- **Transición invisible**: nunca nombres los skills técnicos al usuario.
- **No dupliques definiciones.** Las reglas de negocio del deck (calidad, anti-placeholder, motor del artefacto, Drive, vinculación, nomenclatura) viven en `_shared/presentation-builder/` y las aplican los skills especializados. El router no las repite.
- **El deck se construye en Cowork, no en Claude Design.** Si el usuario menciona Claude Design, no discutas acá: derivá igual, que el skill de área ya lo ofrece como última opción marcada "En retiro".
- **Escalabilidad**: agregar un área = una fila en el registry + una card en el widget + el skill especializado correspondiente (en su plugin de área, con su `_shared/` sincronizado).

## Cómo se relaciona con el resto de la familia

```
pc-meta-presentation-builder   ← este router (meta, transversal)
        │  pregunta área y deriva
        ├──► pc-sales-presentation-builder      (comercial)
        └──► pc-delivery-presentation-builder   (delivery)

_shared/presentation-builder/  ← núcleo común canónico (deck-engine, ui-patterns, deck-craft,
                                  connector-sweep, common-rules, slides, widgets)
                                  se copia dentro de cada skill especializado vía sync.sh
_shared/drive-upload/          ← gate de subida a Drive (carpeta primero, versión en cada edición)
_shared/artifact-linkage/      ← gate de vinculación (Project_Asset__c / issue Artifact)
```

Los skills especializados también tienen, cada uno, una **red de seguridad**: si el usuario los invoca directo desde el área equivocada, arrancan preguntando el área y derivan igual. Así el ruteo funciona con o sin pasar por este router.

## Changelog

- **1.1.0 (2026-08-03)** — Alineado al giro de la familia: el deck **se construye en Cowork como artefacto HTML**, no en Claude Design, que queda en retiro. Cambia la `description` (dejaba de ser cierto que "el deck SIEMPRE se hace en Claude Design") y se agrega la regla de no discutir Claude Design en el router: se deriva igual y el skill de área lo ofrece como última opción. El ruteo en sí no cambia.
- **1.0.0 (2026-07-06)** — Nace del split de `pc-sales-presentation-builder`.

<!-- owner: ariel.tarsitano -->
