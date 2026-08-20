# Template — RACI + ceremonias

> Quién decide qué; calendario de demos y SLAs. Acuerdan: **ambas partes**. Sprint 0.

## RACI mínimo

Matriz por actividad clave (R=Responsable, A=Aprobador, C=Consultado, I=Informado):

| Actividad | Sponsor | PO cliente | Expertos cliente | Líder del nodo | Revisor técnico | Operador del agente |
|---|---|---|---|---|---|---|
| Aprobación de SOW refinado | A | C | — | R | — | — |
| Aprobación de HUs y wireframes | — | A | C | R | — | — |
| Decisiones funcionales en talleres | — | A | C | R | — | — |
| Clasificación defecto vs cambio | — | A | — | R | C | — |
| Órdenes de cambio | A | C | — | R | — | — |
| Aceptación de UAT | A | R | C | I | — | — |

Reglas asociadas: **PO único** con decisiones en minuta vinculantes, 48 h de objeción (limitante 06). Cambios de personal del cliente **no reabren lo decidido** (limitante 12).

## Ceremonias

| Ceremonia | Frecuencia | Participantes | SLA asociado |
|---|---|---|---|
| Kickoff | Única (día 1 Sprint 0) | Todos + sponsor | Reglas del juego y consecuencias presentadas |
| Talleres por dominio | Semana 1 Sprint 0 | PO + expertos + nodo | Disponibilidad firmada en kickoff (limitante 07); tema sin definir → excluido o fase 2 |
| Revisión de entregables | Por entregable | PO | Aprobar u observar en 5 días hábiles → aprobación tácita (limitante 04) |
| Demo semanal | Semanal (F3) | PO + nodo | Feedback consolidado en 48 h hábiles → incremento aceptado |
| Sesión de Scope Freeze | Única (semana 4) | Sponsor + PO + nodo | Exclusiones leídas en voz alta + firma |

Calendario concreto (fechas y horarios) se firma en el kickoff.
