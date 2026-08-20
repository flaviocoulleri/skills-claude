# Fases 4 y 5 — UAT acotado y Go-live con hypercare

Fuente: deck "ProContacto Blueprint v2", slide 14. Gate de salida de F4: **G4 · Aceptación firmada**.

## Fase 4 — UAT

**Duración: ventana fija de 5–10 días hábiles**, acordada en Sprint 0 (Plan de UAT, entregable 7). Reglas:

1. **Ventana fija.** El cliente reserva a sus usuarios; **reagendar tiene costo de desplazamiento**.
2. **Los casos ya están escritos.** Se prueba contra los criterios del Anexo B (backlog de HUs firmado). **No se aceptan casos nuevos**: lo no descrito es un cambio.
3. **Defecto ≠ mejora.** Defecto (incumple criterio firmado) se corrige **sin costo** dentro de la ventana. Todo lo demás: control de cambios o fase 2.
4. **1 ronda + 1 regresión.** Cumplidos los criterios, el cliente firma el acta. **La negativa a firmar activa la aceptación tácita** (silencio de 5 días hábiles = entregable aceptado — limitante 04).

## Gate 4 · Aceptación firmada

Acta de aceptación de UAT firmada (o aceptación tácita activada y documentada). Checklist en `gates-checklists.md`.

## Fase 5 — Go-live

- Sistema en producción + **acta de cierre del proyecto**.
- **Hypercare: 1–2 semanas post go-live, limitado a defectos.**
- Después del hypercare **el proyecto cierra** y todo pasa al esquema de soporte — **contrato aparte** (etapa Operar; esta metodología deja de aplicar).

## Qué revisar como PM en estas fases

- F4: la ventana está agendada con usuarios reservados; los casos de UAT derivan 1:1 de los criterios del Anexo B; cada hallazgo clasificado como defecto o cambio en el momento.
- F5: acta de cierre firmada, alcance del hypercare comunicado (solo defectos), handoff a soporte con contrato aparte antes de apagar el proyecto.

## Práctica recomendada (no canon del deck)

- **Firmar el acuerdo de garantía vs. control de cambios antes del go-live** (`templates/garantia-vs-cambios.md`), preparado durante el UAT. En proyectos multi-salida, hypercare definido por salida — nunca "1 mes" genérico. *(Hay además una propuesta metodológica pendiente sobre proyectos multi-país — ver `propuestas-metodologicas.md` P2.)*
- **El go-live no es el final:** en paralelo al cierre, el DM abre la conversación comercial de soporte (conectar con el AE antes de que termine el hypercare, cuantificando el volumen de tickets que seguirá llegando). Detalle en `practica-real-dm.md` §3 — Operar es el piso de revenue de ProContacto.
