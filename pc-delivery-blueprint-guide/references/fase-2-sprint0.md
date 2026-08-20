# Fase 2 — Sprint 0: cuatro semanas para congelar el alcance

Fuente: deck "ProContacto Blueprint v2", slides 11–12. La mayor inversión humana del modelo. Gate de salida: **G2 · Scope Freeze**.

**Formato:** nodo de 3 personas, dedicación completa, 4 semanas. **Quickstarts: versión de 2 semanas.** El Sprint 0 **no se extiende por indecisión del cliente**.

## Semana a semana

### Semana 1 — Discovery dirigido
- Kickoff: reglas del juego, SLAs y proceso de scope freeze **desde el día 1** (las consecuencias se presentan como reglas del modelo, no como castigos).
- Talleres por dominio con decisiones en minuta — nada de «lo vemos después».
- Inventario técnico + checklist de insumos del cliente **con fecha límite**.

### Semana 2 — Refinamiento funcional
- Backlog completo de HUs con criterios **Gherkin verificables** (pasa / no pasa).
- **Diccionario de datos**: el insumo directo del agente de IA.
- Wireframes v2 como artefacto de Cowork + matriz de integraciones.

### Semana 3 — Validación con el cliente
- **Walkthrough navegable**: el cliente «usa» el sistema antes de que exista.
- Revisión HU por HU con el PO — **máximo 2 rondas consolidadas**.
- Re-estimación y clasificación: alcance comprometido vs backlog fase 2.

### Semana 4 — Cierre y congelamiento
- SOW refinado final con plan de sprints, UAT y RACI.
- **Piloto AI-ready**: el agente construye 2–3 historias reales en sandbox.
- Sesión de Scope Freeze: exclusiones **leídas en voz alta** y firma del sponsor.

## Los 10 entregables obligatorios

Uno congela todo (el Acta de Scope Freeze). Templates en `templates/_registry.md`.

| # | Entregable | Qué es | Firma / valida |
|---|---|---|---|
| 1 | **SOW refinado (vF)** | El alcance contractual final; reemplaza al SOW comercial | Firma: sponsor |
| 2 | **Backlog de HUs · Anexo B** | Criterios Gherkin: base del agente y de las pruebas de UAT | Firma: PO cliente |
| 3 | **Wireframes v2 · Anexo C** | El contrato visual: lo entregado se valida contra estas pantallas | Firma: PO cliente |
| 4 | **Diccionario de datos** | La especificación técnica que consume el agente de IA | Valida: arquitecto |
| 5 | **Matriz de integraciones** | Alcance y responsables de cada extremo, incluidos los del cliente | PO + arquitecto |
| 6 | **Plan de datos** | Plantillas, calidad mínima, fechas — responsable: el cliente | Firma: PO cliente |
| 7 | **Plan de UAT** | Ventana, casos derivados de criterios, defecto vs cambio | Firma: PO cliente |
| 8 | **RACI + ceremonias** | Quién decide qué; calendario de demos y SLAs | Ambas partes |
| 9 | **RAID log** | Riesgos, supuestos, issues y dependencias con dueño y fecha | Líder del nodo |
| 10 | **Acta de Scope Freeze** | Congela el alcance y activa el control de cambios | Firma: sponsor |

## Regla de oro

> **Lo que llega sin definir a la semana 4, se excluye o se difiere a fase 2. Nunca entra ambiguo a ejecución.**

## Gate 2 · Scope Freeze

El gate se cierra con el Acta de Scope Freeze firmada por el sponsor, que activa el control de cambios. Checklist verificable en `gates-checklists.md`.

## Práctica recomendada: chequeo de densidad al armar la parrilla

Antes de agendar los talleres de la semana 1, correr la calculadora de densidad de `practica-real-dm.md` §6: si la parrilla da **más de ~10 sesiones/semana sostenidas**, la respuesta correcta es **recortar alcance** (diferir dominios a fase 2), no comprimir el calendario ni extender el Sprint 0. También completar la **matriz de responsables por rol** (`templates/matriz-responsables-rol.md`) junto con el RACI si el cliente tiene rotación de personal. *(Práctica recomendada de campo, no canon del deck.)*

> Hay una propuesta metodológica pendiente de validación sobre exigir analista funcional asignado como condición de arranque — ver `propuestas-metodologicas.md` P1.
