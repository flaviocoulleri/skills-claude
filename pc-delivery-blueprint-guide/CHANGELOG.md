# Changelog — pc-delivery-blueprint-guide

## 1.1.1 — 2026-07-13

- Fix del bug de issuetype: la carga de contexto filtraba `issuetype = "Artefacto"` (inexistente en la org) → la JQL fallaba y el skill nunca traía los Artifacts del proyecto, cayendo siempre al camino manual. Corregido al nombre real **`Artifact`** (id 10209) y nombrado el campo real del link **`customfield_10158` (Page Link, url)** + tipo **`customfield_10263` (Artifact Type)**, con fallback a discovery. Fuente: introspección REST (`_shared/jira/fields-by-issuetype.md`).

## 1.1.0 — 2026-07-04

Mejoras derivadas del análisis de campo (~92 reuniones reales de un DM, ene–jul 2026).

- Nuevo `references/practica-real-dm.md`: protocolo de escalamiento en capas, comité operativo semanal con métricas cuantitativas, venta de soporte post-hypercare como actividad del DM, acuerdo garantía-vs-cambios pre-go-live, matriz de responsables por rol, calculadora de densidad del Sprint 0. Todo marcado como práctica recomendada, separado del canon del deck.
- Nuevo `references/propuestas-metodologicas.md`: 4 propuestas de cambio a la metodología PENDIENTES de validación (gate de analista asignado, variante multi-país/multi-salida, limitante 13 de interlocución única, reconciliación de "máx 2 rondas" con el ciclo real de tickets). El skill nunca las presenta como regla vigente.
- 3 templates nuevos de práctica recomendada: `status-semanal.md`, `garantia-vs-cambios.md`, `matriz-responsables-rol.md` (registrados en `_registry.md` en sección aparte de los 10 canónicos).
- Referencias de fase (Sprint 0, ejecución, UAT/go-live) y limitantes con secciones de práctica recomendada y punteros a las propuestas.
- SKILL.md: regla de los 3 niveles de contenido (canon / práctica recomendada / propuesta pendiente) que el skill debe diferenciar siempre al responder.

## 1.0.0 — 2026-07-03

Versión inicial.

- Metodología ProContacto Blueprint v2 completa (deck de 23 slides, junio 2026): 3 etapas, 5 principios, 5 fases + 4 gates, Sprint 0 con 10 entregables, 12 limitantes, obligaciones→consecuencias, métricas y evolución de nodos.
- 4 modos: consulta metodológica (A), fase y próximos pasos (B), validación de gate con semáforo (C), vinculación de Artefactos en Jira (D — única escritura, con confirmación).
- Contexto de proyecto desde Jira (proyecto + issuetype "Artefacto"); validación lazy con Drive, Gmail, Calendar, ReadAI, Confluence y Salesforce como fuente secundaria.
- Mapa de skills del catálogo por fase/entregable (`skills-map.md`).
- Templates esqueleto de los 10 entregables del Sprint 0 + registro híbrido con `drive_url` completable.
- Pendiente para próximas versiones: variante Marketing y checklist oficial de 8 criterios del Gate 1 (requieren el doc fuente de la metodología).
