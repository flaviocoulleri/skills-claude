# Template — Acuerdo de garantía vs. control de cambios (práctica recomendada)

> **No es uno de los 10 entregables canónicos** — es un anexo recomendado que se firma ANTES del go-live para que la frontera garantía / hypercare / control de cambios no se negocie ad-hoc después. Evidencia de campo: sin este acuerdo, la discusión termina ocurriendo en llamadas improvisadas releyendo el contrato.

## Estructura

1. **Definiciones operativas** (referenciando el canon):
   - *Defecto en garantía*: incumplimiento de un criterio firmado del Anexo B — se corrige **sin costo** durante el hypercare.
   - *Cambio*: todo lo demás (mejoras, casos no descritos, nuevos pedidos) — control de cambios cobrado o fase 2.
   - *Limitación de plataforma*: comportamiento de Salesforce no modificable — se documenta, no es defecto ni cambio.
2. **Ventana de hypercare**: fechas concretas de inicio y fin, alcance (solo defectos), canal de reporte y SLA de respuesta.
3. **Multi-salida (si aplica)**: hypercare definido **por salida** (país/oleada) — duración, alcance y equipo asignado de cada una. Nunca "1 mes" genérico para N salidas.
4. **Qué pasa al terminar el hypercare**: el proyecto cierra; todo pedido posterior va al contrato de soporte (aparte). Datos de contacto del esquema de soporte si ya existe, o compromiso de propuesta comercial antes del fin del hypercare.
5. **Firmas**: sponsor + responsable ProContacto, antes del go-live.

## Regla de uso

Se prepara en F4 (durante el UAT) y se firma como condición del go-live — es la extensión natural del Plan de UAT (que ya define defecto vs cambio para la ventana de pruebas) hacia el período post-productivo.
