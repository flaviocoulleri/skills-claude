---
name: pc-meta-sow-builder
metadata:
  version: 1.0.0
  last_modified: 2026-07-13
  owner: ariel.tarsitano@procontacto.com.mx
description: >
  Punto de entrada ÚNICO para armar CUALQUIER SOW (Statement of Work / documento de alcance)
  de ProContacto cuando el pedido no deja claro el área. Pregunta primero para qué es
  (Comercial: alcance de un deal en venta, sobre una Quote de Salesforce / Delivery: SOW
  Refinado del Sprint 0 de un proyecto ya vendido) vía widget y deriva —transición invisible—
  al skill especializado; el router no arma nada, sólo rutea. ACTIVAR con "quiero armar un
  SOW", "ármame el SOW", "Statement of Work", "documento de alcance", "necesito el SOW del
  proyecto/cliente X", "hagamos el alcance"; EN: "build/create the SOW", "statement of work",
  "scope document". Si el pedido ya nombra señales de área (Quote/cotización/deal/propuesta →
  Comercial; Sprint 0/proyecto vendido/discovery/kickoff/transcripts de relevamiento →
  Delivery), confirma el área y deriva. ES/EN.
---

# pc-meta-sow-builder

## Para qué existe este skill

ProContacto produce SOWs de dos naturalezas muy distintas:

- **Comercial** — el alcance de un deal **en venta**: Historias de Usuario que viven como
  líneas de una Quote de Salesforce, con precio, exportadas como anexo del contrato (`.docx`)
  y/o planilla de revisión (`.xlsx`). Lo usa el AE/Pre-Sales antes de la firma.
- **Delivery** — el **SOW Refinado** que cierra el Sprint 0 de un proyecto **ya vendido**: un
  documento Word con el alcance funcional completo (nubes, épicas, historias, consideraciones,
  integraciones), producto del relevamiento de discovery. Lo usa el BA/PM/consultor.

Cada una tiene su skill especializado en el plugin de su área (`procontacto-comercial`,
`procontacto-delivery`). Este skill es el **front-door transversal**: cuando el pedido es
genérico ("ármame un SOW") o no deja claro el área, pregunta y **deriva al skill correcto** con
una transición invisible. No captura contexto, no lee transcripts, no toca Salesforce — su
única responsabilidad es rutear bien y rápido.

> **Por qué existe como skill aparte.** Los especializados se disparan solos cuando el pedido
> ya nombra el contexto (una "Quote" activa el comercial; un "Sprint 0" activa el de delivery).
> Pero un pedido genérico necesita un lugar que desambigüe sin adivinar. Ese es este router.

## El registry de áreas

| Área | Skill destino | Qué SOW cubre | Señales del pedido |
|---|---|---|---|
| **Comercial** | `pc-sales-sf-sow-builder` | Alcance de un deal en venta sobre una Quote de SF; historias cotizadas; anexo del contrato + planilla de revisión. Si la Quote no existe, ese skill delega el armado en `pc-sales-sf-quote-builder`. | "Quote", "cotización", "deal", "oportunidad", "propuesta", "anexo del contrato", "todavía no se firmó" |
| **Delivery** | `pc-delivery-salesforce-sow-generator` | SOW Refinado (Word) del Sprint 0 de un proyecto ya vendido, desde transcripts/diagramas/minutas de discovery; rol BA + Solution Architect. | "Sprint 0", "proyecto vendido/arrancado", "discovery", "workshops", "relevamiento", "SOW refinado/funcional" |

## Flujo de trabajo

### Paso 1 — Preguntar el área (o confirmar la inferida)

**Llama a `mcp__visualize__read_me` antes del primer widget** (preparación silenciosa, no la
narres). Después muestra el widget `assets/widgets/paso0-area.html` con
`mcp__visualize__show_widget` — una card por área del registry.

- **Si el pedido ya sugiere un área** (nombró "Quote", "Sprint 0", etc.), muestra igual el
  widget con la opción inferida como recomendada, para que el usuario confirme o corrija antes
  de derivar. No derives a ciegas.
- **Nunca** listes las áreas como bullets en el chat ni uses `AskUserQuestion` — siempre el widget.
- Idioma del widget = idioma de la conversación.

### Paso 2 — Derivar al skill especializado (transición invisible)

Con el área elegida, **invoca el skill destino del registry** y deja que ese skill maneje todo
el resto del flujo.

- La transición es **invisible**: no le menciones al usuario el nombre técnico del skill.
  Háblale en lenguaje natural — "Perfecto, vamos con el alcance del deal" / "Dale, armamos el
  SOW del proyecto" — y sigue.
- Pásale al skill destino todo el contexto que el usuario ya haya dado (cliente/Opp/proyecto,
  transcripts, links de Drive) para que no lo vuelva a pedir.
- A partir de la derivación, el router no vuelve a intervenir.

## Reglas inviolables

- **El router NO construye el SOW.** Su salida es la derivación. Si te encuentras leyendo
  transcripts, consultando Salesforce o redactando historias, algo salió mal.
- **Siempre confirma el área con el widget** antes de derivar, aun cuando parezca obvio.
- **Transición invisible**: nunca nombres los skills técnicos al usuario.
- **No dupliques definiciones.** Los estándares de historia y el checklist de transversales
  viven en `_shared/sow/` y los aplican los especializados. El router no los repite.
- **Escalabilidad**: agregar un área = una fila en el registry + una card en el widget + el
  skill especializado (con su `_shared/` sincronizado).

## Cómo se relaciona con el resto de la familia

```
pc-meta-sow-builder            ← este router (meta, transversal)
        │  pregunta área y deriva
        ├──► pc-sales-sf-sow-builder                (comercial; delega el armado de
        │        │                                    historias en pc-sales-sf-quote-builder)
        │        └── exporta anexo/planilla y hace handoff a ↓ cuando el deal se vende
        └──► pc-delivery-salesforce-sow-generator   (delivery; SOW Refinado Sprint 0)

_shared/sow/  ← núcleo común canónico (story-standards, transversal-checklist)
                se copia dentro de cada skill especializado vía sync.sh
```

Los especializados también tienen **red de seguridad**: si el usuario los invoca directo desde
el área equivocada, derivan igual. Así el ruteo funciona con o sin pasar por este router.
