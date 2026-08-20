# Template — RAID log

> Riesgos, supuestos, issues y dependencias **con dueño y fecha**. Responsable: **líder del nodo**. Se inicia en Sprint 0 y vive durante todo el proyecto.

## Estructura mínima (una fila por ítem)

| Columna | Contenido |
|---|---|
| ID | R-01, A-01, I-01, D-01… |
| Tipo | **R**iesgo / **A**ssumption (supuesto) / **I**ssue / **D**ependencia |
| Descripción | Qué es, en una línea concreta |
| Impacto | Qué pasa si se materializa (alcance/fecha/costo) |
| Probabilidad | Alta/Media/Baja (solo riesgos) |
| Dueño | **Obligatorio** — persona con nombre, del cliente o del nodo |
| Fecha límite / revisión | **Obligatoria** |
| Mitigación / plan | Qué se hace al respecto |
| Estado | Abierto / mitigado / materializado / cerrado |

## Reglas

- Ningún ítem sin dueño y fecha.
- Las dependencias del cliente (accesos, ambientes, datos, disponibilidad) se cruzan con el checklist de insumos de la semana 1 — su retraso activa el desplazamiento 1:1 (limitante 08) y, acumulado >10 días hábiles, suspensión + remobilización (limitante 09).
- Revisar el log en cada demo semanal; los supuestos que se invalidan se convierten en riesgo o cambio.
