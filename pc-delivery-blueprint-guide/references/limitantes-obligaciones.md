# Las 12 limitantes al cliente y las obligaciones con consecuencia

Fuente: deck "ProContacto Blueprint v2", slides 15–16. El corazón comercial-contractual del modelo. Cada limitante tiene su **instrumento** (dónde vive contractualmente) y **cláusula tipo redactada — a validar con el asesor legal antes de usarse en contratos reales**.

## Las 12 limitantes

| # | Instrumento | Limitante | Detalle |
|---|---|---|---|
| 01 | SOW | **Alcance cerrado por referencia** | Solo existe lo descrito en SOW + Anexos B y C |
| 02 | Acta | **Congelamiento de alcance** | Al cierre del Sprint 0, con firma del sponsor |
| 03 | MSA | **Control de cambios** | Nada se construye sin orden de cambio firmada |
| 04 | MSA | **Aprobación tácita** | Silencio de 5 días hábiles = entregable aceptado |
| 05 | SOW | **Máx. 2 rondas de observaciones** | Consolidadas por el PO; la ronda 3 es un cambio |
| 06 | Contrato | **Product Owner único** | Sus decisiones en minuta son vinculantes (48 h de objeción) |
| 07 | SOW | **Disponibilidad mínima** | PO y expertos en Sprint 0, con calendario firmado en kickoff |
| 08 | MSA | **Retraso desplaza 1:1** | Cada día de retraso del cliente corre las fechas, automático |
| 09 | MSA | **Suspensión + remobilización** | Al superar 10 días hábiles acumulados de retraso |
| 10 | Plan de UAT | **UAT acotado** | Casos = criterios firmados; defecto ≠ mejora; 1 ronda + regresión |
| 11 | SOW | **Datos en plantillas** | Con calidad mínima y fecha; la limpieza se cotiza aparte |
| 12 | MSA | **Continuidad de decisiones** | Cambios de personal del cliente no reabren lo decidido |

## Obligaciones del cliente → consecuencia automática

Cada incumplimiento tiene una consecuencia automática. Presentarlas en el kickoff como **reglas del modelo, no como castigos** — y aplicarlas **siempre, desde la primera vez**. La consistencia evita negociar caso a caso.

| Obligación del cliente | → Consecuencia |
|---|---|
| Designar un Product Owner con autoridad | No inicia el Sprint 0 |
| PO y expertos disponibles en los talleres | El tema sin definir se excluye o pasa a fase 2 |
| Accesos, ambientes y datos en fecha | El cronograma se desplaza 1:1 |
| Aprobar u observar entregables en 5 días hábiles | Aprobación tácita |
| Feedback de demos consolidado en 48 h | El incremento queda aceptado |
| Ejecutar el UAT en la ventana acordada | Reagendar tiene cargo de desplazamiento |
| Retrasos acumulados sobre el umbral de 10 días hábiles | Suspensión + cargo de remobilización |

## Cómo usar esto como PM

- Al armar kickoff: presentar la tabla de obligaciones→consecuencias completa, desde el día 1.
- Ante un pedido fuera de alcance: apuntar a la limitante que aplica (01, 02, 03 o 05) y clasificar como CR o fase 2 — nunca "lo metemos".
- Ante un retraso del cliente: aplicar 08 (desplazamiento 1:1) desde la primera vez; si acumula >10 días hábiles, escala a 09 (suspensión + remobilización).
- Ante silencio del cliente sobre un entregable: recordar el SLA de 5 días y, cumplido, documentar la aprobación tácita (04).
- Las cláusulas tipo son material legal: **no** improvisar redacción contractual; derivar al asesor legal.

> Propuesta pendiente de validación: una 13ª limitante de "interlocución única por frente" para proyectos con varios voceros de negocio del cliente — ver `propuestas-metodologicas.md` P3. Complemento práctico ante rotación de personal del cliente: matriz de responsables por rol (`templates/matriz-responsables-rol.md`).
