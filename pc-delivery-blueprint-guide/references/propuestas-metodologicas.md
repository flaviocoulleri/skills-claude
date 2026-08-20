# Propuestas de cambio a la metodología — PENDIENTES DE VALIDACIÓN

> **Estatus: NO son metodología vigente.** Son propuestas derivadas de la evidencia de campo (análisis de reuniones reales, ene–jul 2026), pendientes de validación por los Delivery Managers y el autor de la metodología. **El skill NUNCA las presenta como regla**: si son relevantes a una consulta, mencionarlas como "hay una propuesta pendiente de validación sobre esto" y sugerir escalarla. Cuando alguna se apruebe, se mueve al reference canónico correspondiente y se elimina de acá.

## P1 — Gate duro de "analista funcional asignado" (afecta G1/G2)

**Evidencia:** la ausencia de analista funcional dedicado causó retrabajo documentado (Radio Victoria) y es preocupación recurrente al planificar nuevos Sprint 0 (GeoVictoria). El equipo técnico sin analista tiene sesgo hacia "lo técnicamente posible" en vez de la solución de negocio.

**Propuesta:** agregar al checklist del G1 (o al arranque del Sprint 0) un ítem bloqueante: *"Analista funcional asignado con dedicación definida"*. Sin analista, el Sprint 0 no arranca — mismo tratamiento que la falta de PO del cliente.

## P2 — Variante multi-país / multi-salida (afecta SOW, plan de sprints, hypercare)

**Evidencia:** proyecto real con 9 salidas a producción (2 MVPs + 7 países) sobre un contrato que asumía una salida única; el hypercare, el costeo y el plan se reinterpretaron ad-hoc.

**Propuesta:** cuando el proyecto tiene más de una salida a producción, el SOW refinado debe incluir: plan de cutover por salida, hypercare definido **por salida** (duración y alcance), costeo del esfuerzo de cada salida adicional, y criterio de qué versión del alcance congelado aplica a cada país/oleada.

## P3 — Limitante 13: interlocución de negocio con jerarquía única (afecta MSA/contrato)

**Evidencia:** múltiples voceros del cliente con roles de decisión superpuestos generan fricción recurrente (reforzar clasificación de tickets una y otra vez, decisiones revisitadas).

**Propuesta:** sumar a las 12 limitantes una 13ª: *"Interlocución única por frente: el cliente designa un único aprobador de alcance por frente funcional; los demás participantes opinan pero no aprueban"*. Complementa la limitante 06 (PO único) extendiéndola a proyectos grandes con varios frentes.

## P4 — Reconciliar "máx. 2 rondas de observaciones" con el ciclo real de feedback en ejecución (afecta limitante 05 / F3)

**Evidencia:** en ejecución real se opera con un ciclo continuo de feedback (ej. 5 días hábiles para cargar tickets + 5 días para ajustar + validación), con backlogs de 100+ tickets — y no está definido cómo eso mapea a la regla "máx. 2 rondas consolidadas; la ronda 3 es un cambio".

**Propuesta:** definir explícitamente la equivalencia: ¿cada ciclo de carga+ajuste cuenta como una ronda? ¿la regla de 2 rondas aplica por entregable (Sprint 0) y el ciclo de tickets aplica solo a F3/UAT? Documentar la regla resultante en `fase-3-ejecucion.md` y en el Plan de UAT.

---

**Cómo escalar estas propuestas:** llevar este archivo (o el informe completo del análisis de campo) a la mesa de Delivery Managers; las que se aprueben pasan al canon en la siguiente versión del skill.
