# Metodología ProContacto Blueprint — Framework core

Fuente: deck "ProContacto Blueprint v2" (junio 2026), slides 02–09. Una sola metodología, siempre.

## El cambio de paradigma (por qué existe esta metodología)

La IA no es una herramienta más: **es un cambio en quién ejecuta el proceso**.

- **Antes:** el humano ejecuta, la herramienta asiste.
- **Ahora:** la IA ejecuta, el humano dirige y valida.
- **Resultado:** un nodo de 8 personas puede operar como 2 nodos de 2.

## Las 3 etapas del framework

| # | Etapa | Qué pasa | Rol humano |
|---|---|---|---|
| 01 | **Diseñar** | Sprint 0 — AS-IS, TO-BE, Historias de Usuario, Wireframes, Blueprint Document | **El humano lidera** (la IA asiste) |
| 02 | **Construir** | Agentes autónomos ejecutan el backlog. Sin aprobaciones intermedias | **La IA ejecuta** |
| 03 | **Operar** | Post Go Live — nodo reducido supervisa, sostiene y genera upsells | **El nodo supervisa** |

Detalle de cada etapa:

- **Diseñar (Sprint 0):** (1) el AE releva la operatoria del cliente durante la etapa comercial; (2) AS-IS · TO-BE: cómo opera hoy el cliente → cómo operará en Salesforce; (3) Historias de Usuario, Wireframes y Blueprint Document: backlog validado y documentación completa antes de construir. **Gate: nada pasa a Construir sin aprobación del cliente.** Pendiente definir: cómo acompañamos a los equipos a convertirse en analistas (ref. modelo Geovictoria).
- **Construir:** los agentes construyen 100% autónomo, sin aprobaciones intermedias; el humano ve los resultados en la demo final. Cuatro roles de agente: **Analista** (interpreta HUs y define criterios de aceptación), **Configurador** (ejecuta configuración Salesforce sobre el org), **Dev** (desarrolla LWC, Apex y código personalizado), **QA** (valida criterios de aceptación y cierra tickets). Flujo: Jira → agente selecciona skill → ejecuta → cierra ticket.
- **Operar:** el nodo reducido supervisa la base instalada — resuelve **incidentes** (resolución rápida con soporte de agentes), gestiona **mejoras** (iteraciones continuas sobre la solución implementada) y origina **upsells** (origen natural del crecimiento de cuenta). Operar es el piso de revenue de ProContacto y el origen de los upsells.

## Modelo AI-Delivery (cómo se lleva a la práctica)

Venta con prototipos, Sprint 0 de consolidación de alcance y ejecución asistida por agentes de IA. Los números del modelo:

- **5 fases**
- **4 gates de control**
- **12 limitantes al cliente**
- **1 alcance congelado**

## Los 5 principios (las reglas del juego)

Cualquier decisión operativa o contractual debe poder justificarse contra ellos. Citarlos textual:

1. **El alcance es lo firmado, no lo conversado.** SOW refinado + backlog + wireframes firmados son la única fuente de verdad. Lo que no está ahí, no existe.
2. **La ambigüedad se resuelve antes de construir, nunca durante.** Sin criterios de aceptación verificables y pantalla asociada, una historia no entra a ejecución.
3. **El prototipo es el contrato visual.** Los wireframes dejan de ser material de venta: se vuelven anexo contractual. Lo entregado se valida contra esas pantallas.
4. **La velocidad de la IA exige velocidad del cliente.** Un proyecto que se construye en semanas no tolera aprobaciones de 15 días. SLAs con consecuencias automáticas.
5. **Todo cambio tiene precio y fecha.** No hay cambios «pequeños» gratis: control de cambios con impacto documentado, o fase 2.

## El flujo end-to-end: 5 fases, 4 gates

Sin checklist, no se avanza. Un gate es un checklist verificable: protege a delivery de los proyectos mal vendidos y a ejecución de los alcances ambiguos.

| Fase | Nombre | Salida | Duración | Gate de salida |
|---|---|---|---|---|
| F1 | Venta comercial | SOW por unidades + wireframes v1 + exclusiones explícitas | Según ciclo de venta | **G1 · Ready for Delivery** |
| F2 | Sprint 0 | SOW refinado + backlog HU + wireframes v2 firmados | 4 semanas (2 en quickstarts) | **G2 · Scope Freeze** |
| F3 | Ejecución con IA | El agente construye; el nodo revisa y demuestra al cliente | Sprints de 1 semana | **G3 · Criterios cubiertos** |
| F4 | UAT | El cliente prueba contra los criterios firmados; el nodo corrige | Ventana fija de 5–10 días | **G4 · Aceptación firmada** |
| F5 | Go-live | Sistema en producción + acta de cierre del proyecto | 1–2 semanas de hypercare | — (cierre del proyecto) |

Detalle de cada fase en su reference: `fase-1-venta.md`, `fase-2-sprint0.md`, `fase-3-ejecucion.md`, `fase-4-5-uat-golive.md`. Checklists de gate en `gates-checklists.md`.

## Preguntas abiertas (la metodología aún NO las define)

Si el PM pregunta por alguno de estos temas, responder que está pendiente de definición y sugerir escalarlo a Delivery Managers — no inventar:

1. ¿Cuánto del relevamiento hace el AE vs el Nodo en Sprint 0?
2. ¿Cuánto dura el Sprint 0 según tamaño del proyecto?
3. ¿Cada cuánto se hace demo al cliente durante el Construir?
4. ¿Cuántos agentes trabajan en paralelo y qué skills ejecuta cada uno?
5. ¿Sprints o continuous delivery — qué metodología rige el Construir?
6. ¿Cómo maneja el agente un cambio de scope durante la construcción?
7. ¿Qué skills debe dominar cada perfil antes de pasar a Fase 2?
8. ¿Cuánto tiempo estimamos en Fase 1 (Vibe Coding) antes de mover un nodo a Fase 2 (Agentes)?
9. ¿Qué pasa con los perfiles que los agentes reemplazan?
10. ¿Cómo acompañamos a los equipos a convertirse en analistas? (ref. modelo Geovictoria)
