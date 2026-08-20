# Template — Status semanal / comité operativo (práctica recomendada)

> **No es uno de los 10 entregables canónicos del Sprint 0** — es la plantilla de reporting semanal en fase de ejecución (F3) y post-go-live, derivada del patrón real más consistente observado en campo. Presenta métricas cuantitativas, no relato.

## Estructura

### 1. Backlog cuantificado (números, siempre los mismos 4 estados)

| Estado | Cantidad | Δ vs semana anterior |
|---|---|---|
| Abiertos | | |
| En progreso | | |
| Listos para validar (esperando al cliente) | | |
| Cerrados | | |

### 2. Clasificación del backlog abierto

| Tipo | Cantidad | Tratamiento |
|---|---|---|
| Error (defecto = criterio firmado incumplido) | | Se corrige sin costo |
| Modificación simple (cambio) | | Control de cambios / fase 2 |
| Limitación de plataforma | | Se documenta, no se "arregla" |
| Permisos / accesos | | Acción del cliente con fecha |

### 3. Avance contra plan

- **% avance real vs. % plan** (ej.: 61% real / 62% plan) + explicación de la brecha en una línea.
- Criterio de secuenciación de la semana entrante, explícito (ej.: "primero los N errores críticos salvo bloqueantes").

### 4. Bloqueantes y dependencias del cliente

Por ítem: qué, quién (rol del cliente), desde cuándo, impacto en fechas. Recordatorio de la regla: retraso del cliente desplaza el cronograma 1:1.

### 5. Ítems esperando validación del cliente

Lista con fecha de entrega — recordando el SLA de 5 días hábiles y la aprobación tácita (limitante 04).

## Reglas de uso

- Mismos 4 estados y misma clasificación todas las semanas — la comparabilidad es el valor.
- La clasificación error/cambio se hace en el comité, delante del cliente: es donde se sostiene defecto≠mejora en la práctica.
- El status se postea también en el canal Slack externo del proyecto (skill `pc-delivery-slack-channel-auditor`).
