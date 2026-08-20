# Checklists de gate (G1–G4)

Un gate es un **checklist verificable**: sin checklist, no se avanza. Protege a delivery de los proyectos mal vendidos y a ejecución de los alcances ambiguos.

Los ítems derivan del deck "ProContacto Blueprint v2". Cada ítem indica si es **verificable por conector** (columna "Verificación" — receta en `validacion-conectores.md`) o manual. Los ítems marcados `TBD` requieren el doc fuente de la metodología para el detalle fino.

## G1 · Ready for Delivery (cierra F1, habilita Sprint 0)

El deck define un checklist de **8 criterios** cuyo listado exacto está en el doc fuente <!-- TBD: doc fuente — reemplazar estos ítems derivados por los 8 criterios oficiales -->. Ítems derivados del deck mientras tanto:

| # | Ítem | Verificación |
|---|---|---|
| 1 | SOW comercial armado por unidades del catálogo (no descripciones libres) | Drive (doc SOW en carpeta del deal) |
| 2 | Exclusiones explícitas listadas en la propuesta (mínimo: migración/limpieza de datos, integraciones y reportes no listados, capacitación extra, soporte post go-live) | Drive (sección exclusiones en SOW) |
| 3 | Wireframes v1 anexados a la propuesta con leyenda estándar | Drive / link Cowork |
| 4 | Pre-validación técnica de delivery hecha (obligatoria si hay integraciones, multinube o migración) | Calendar/ReadAI (sesión 30–60 min) |
| 5 | Buffer de estimación conforme al tipo de proyecto (no rebajado sin aprobación CTO) | Manual |
| 6 | Product Owner del cliente designado con autoridad (sin PO no inicia el Sprint 0) | Manual / Gmail |
| 7 | Contrato/orden de compra en estado que habilita arrancar | SF (Opportunity/Contract) |
| 8 | Handoff comercial → delivery realizado y aceptado por el nodo (el nodo puede rechazar con observaciones) | Manual |

## G2 · Scope Freeze (cierra Sprint 0, habilita ejecución)

| # | Ítem | Verificación |
|---|---|---|
| 1 | SOW refinado (vF) firmado por sponsor | Drive |
| 2 | Backlog de HUs (Anexo B) completo, con criterios Gherkin pasa/no-pasa, firmado por PO | Jira (HUs con criterios) + Drive |
| 3 | Wireframes v2 (Anexo C) firmados por PO | Drive / link Cowork |
| 4 | Diccionario de datos validado por arquitecto | Drive |
| 5 | Matriz de integraciones cerrada (PO + arquitecto), con responsables de cada extremo | Drive |
| 6 | Plan de datos firmado por PO (plantillas, calidad mínima, fechas, responsable cliente) | Drive |
| 7 | Plan de UAT firmado por PO (ventana fija, casos derivados de criterios, defecto vs cambio) | Drive |
| 8 | RACI + calendario de ceremonias acordado por ambas partes | Drive / Calendar |
| 9 | RAID log iniciado con dueño y fecha por ítem (líder del nodo) | Drive / Confluence |
| 10 | Piloto AI-ready ejecutado: el agente construyó 2–3 historias reales en sandbox | Jira (HUs piloto cerradas) |
| 11 | Sesión de Scope Freeze realizada: exclusiones leídas en voz alta | Calendar/ReadAI (minuta) |
| 12 | **Acta de Scope Freeze firmada por sponsor** (congela el alcance y activa el control de cambios) | Drive |
| 13 | Alcance clasificado: comprometido vs backlog fase 2; lo sin definir a semana 4 excluido o diferido | Jira (labels/épicas) |

## G3 · Criterios cubiertos (cierra ejecución, habilita UAT)

| # | Ítem | Verificación |
|---|---|---|
| 1 | Todas las HUs del alcance comprometido pasaron la revisión humana binaria (criterios + wireframe) | Jira (HUs done) |
| 2 | Sin HUs del alcance comprometido pendientes o ambiguas (nada entró sin estar AI-ready) | Jira |
| 3 | Demos semanales realizadas y feedback del PO consolidado (48 h) o incrementos aceptados por regla | Calendar/ReadAI + Gmail |
| 4 | Cambios post-freeze capturados como CR cobrado o fase 2 (100%) | Jira / Drive (órdenes de cambio) |
| 5 | Despliegue continuo al ambiente de validación al día (el cliente puede tocar lo demostrado) | Manual |

## G4 · Aceptación firmada (cierra UAT, habilita go-live)

| # | Ítem | Verificación |
|---|---|---|
| 1 | UAT ejecutado dentro de la ventana fija (5–10 días hábiles) | Calendar |
| 2 | Casos probados = criterios del Anexo B (sin casos nuevos; lo no descrito se clasificó como cambio) | Manual / Jira |
| 3 | Defectos (criterio firmado incumplido) corregidos sin costo dentro de la ventana | Jira (bugs cerrados) |
| 4 | 1 ronda + 1 regresión completadas | Manual |
| 5 | **Acta de aceptación firmada** — o aceptación tácita activada (silencio 5 días hábiles) y documentada | Drive / Gmail |

## Cierre de F5 (no es gate, es cierre de proyecto)

| # | Ítem | Verificación |
|---|---|---|
| 1 | Sistema en producción | Manual |
| 2 | Acta de cierre del proyecto firmada | Drive |
| 3 | Hypercare acotado a defectos, 1–2 semanas, comunicado al cliente | Gmail |
| 4 | Handoff a soporte con contrato aparte (etapa Operar) | SF/Odoo — manual |
