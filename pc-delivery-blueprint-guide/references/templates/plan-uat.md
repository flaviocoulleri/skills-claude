# Template — Plan de UAT

> Ventana, casos derivados de criterios, defecto vs cambio. Firma: **PO cliente**. Sprint 0. Es el instrumento de la limitante 10 (UAT acotado).

## Estructura mínima

1. **Ventana fija** — 5–10 días hábiles, fechas concretas acordadas en Sprint 0. El cliente reserva a sus usuarios; **reagendar tiene costo de desplazamiento**.
2. **Casos de prueba** — derivados 1:1 de los criterios Gherkin del Anexo B. **No se aceptan casos nuevos durante el UAT**: lo no descrito es un cambio.
3. **Definición de defecto** — *defecto = criterio firmado incumplido*; se corrige **sin costo** dentro de la ventana. Todo lo demás es mejora → control de cambios o fase 2. La clasificación se hace en el momento.
4. **Mecánica** — **1 ronda + 1 regresión**. Roles: quién ejecuta (usuarios del cliente), quién clasifica hallazgos (PO + líder del nodo), quién corrige (nodo).
5. **Criterio de salida** — cumplidos los criterios, el cliente firma el acta de aceptación. **La negativa a firmar activa la aceptación tácita** (5 días hábiles, limitante 04).
6. **Ambiente** — dónde se prueba y con qué datos.
