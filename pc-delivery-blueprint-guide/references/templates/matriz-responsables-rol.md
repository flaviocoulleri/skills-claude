# Template — Matriz de responsables por rol (práctica recomendada)

> **No es uno de los 10 entregables canónicos** — complementa al RACI cuando el cliente tiene rotación de personal. Evidencia de campo: fijar responsables por nombre deja tickets sin dueño y decisiones huérfanas cuando la persona rota; definir por **rol** mantiene la continuidad.

## Estructura

| Rol (del cliente) | Responsabilidad | Persona actual | Backup | Última revisión |
|---|---|---|---|---|
| Product Owner | Decisiones de alcance vinculantes (48 h de objeción) | | | |
| Referente de dominio <X> | Validar HUs y UAT de su dominio | | | |
| Referente técnico / IT | Accesos, ambientes, integraciones (extremo cliente) | | | |
| Responsable de datos | Plantillas de carga en fecha y calidad | | | |
| Sponsor | Firma SOW, Acta de Scope Freeze, aceptación final | | | |

## Reglas de uso

- La asignación es **al rol**: si la persona cambia, el rol hereda todas las decisiones tomadas (refuerza la limitante 12 — cambios de personal del cliente no reabren lo decidido).
- La columna "persona actual" se revisa en cada comité operativo; un rol sin persona asignada es un bloqueante que se reporta con fecha (dependencia del cliente → desplazamiento 1:1 si frena trabajo).
- Los tickets/issues se asignan por rol (usuario genérico por rol si el sistema lo permite), no por persona.
- Se completa en Sprint 0 junto con el RACI y se registra como Artefacto en Jira.
