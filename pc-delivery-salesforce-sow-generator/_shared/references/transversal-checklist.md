<!-- ⚠️ AUTO-COPIADO desde _shared/sow/ por sync.sh — NO EDITAR ACÁ. Edita el canónico y vuelve a correr sync.sh. -->

# Checklist de procesos transversales

Recorrer esta lista completa en la Fase 2 para CADA proyecto. Los clientes casi nunca piden estos procesos explícitamente, pero sin ellos la solución no es operable — y si no están escritos en el SOW, quedan fuera de alcance y aparecen como conflicto en la ejecución. Por cada ítem, decidir una de tres salidas:

- **Aplica** → generar historia(s) + consideraciones.
- **Aplica pero diferido** → consideración "quedará pendiente de definición en etapas posteriores de refinamiento".
- **No aplica** → delimitación negativa explícita en Consideraciones ("No se considera...") cuando el cliente podría razonablemente esperarlo.

Los actores típicos de las historias transversales son "Administrador del sistema", "Supervisor / Gerente" (reportes y aprobaciones) y el rol operativo correspondiente.

## 1. Configuración inicial y administración
Estructura organizativa (roles, jerarquía), apps Lightning, page layouts por tipo de registro, usuarios y licencias, divisas y territorios, horarios de negocio. Historia tipo: "Como Administrador del sistema, quiero contar con la aplicación Lightning configurada con los objetos y vistas del proceso comercial, para que los usuarios operen desde un único espacio de trabajo."

## 2. Seguridad, perfiles y visibilidad
Perfiles/Permission Sets (CRUD y FLS), jerarquía de roles, OWD y reglas de colaboración, restricciones de edición sobre objetos sincronizados desde sistemas externos. Siempre incluir el boilerplate de ROLES Y PERFILES del template (ver template-structure.md) y la entrega de la "Matriz de roles y perfiles". Si hay datos sensibles (PII, precios, comisiones): consideración de visibilidad específica.

## 3. Migración / importación de datos
Carga inicial de cada objeto con datos preexistentes (cuentas, contactos, productos, casos históricos…). Usar el boilerplate de IMPORTACIÓN DE DATOS del template: plantilla .CSV de ProContacto, una tabla por carga, sin transformaciones, calidad = responsabilidad del cliente, sin adjuntos. Historia por objeto o grupo de objetos a migrar. Delimitar explícitamente qué histórico NO se migra.

## 4. Automatizaciones
Toda regla de negocio del proceso: asignaciones automáticas, actualizaciones de estado, creación de registros derivados, cálculos. Ver árbol de decisión en salesforce-design-guide.md. Delimitar qué NO hace cada automatización.

## 5. Validaciones
Reglas de integridad sobre datos de entrada (campos obligatorios por etapa, formatos, coherencia entre campos). Consideración estándar: las validaciones aplican en la plataforma, no sobre contenido de archivos adjuntos.

## 6. Procesos de aprobación
Descuentos, excepciones de precio, créditos, cambios de etapa sensibles. Historia con matriz de aprobadores (o diferir la matriz a refinamiento).

## 7. Notificaciones y alertas
Emails, notificaciones in-app/push. Boilerplate del template: cuerpo de correo en texto plano, sin imágenes ni firmas; el disparo no modifica información; condiciones del disparador a definir. Delimitar canales NO incluidos (SMS, WhatsApp) si no hay integración.

## 8. Gestión documental
Adjuntos en registros (carga manual — patrón del template), plantillas de documentos, generación de PDFs (documentar limitaciones de plantilla PDF estándar: datos solo de objetos relacionados, restricciones de formato/tipografía, logo en posición fija, sin tablas salvo detalle de líneas).

## 9. Auditoría y trazabilidad
Historial de campos (límite de campos rastreados por objeto), historial de etapas, Setup Audit Trail, requisitos regulatorios del cliente. Si el negocio exige trazabilidad fuerte (quién aprobó qué y cuándo), historia explícita.

## 10. Reportería, dashboards y KPIs
Por cada rol gerencial mencionado, al menos una historia de reportes/dashboard con los KPIs del negocio detectados. Boilerplate del template: informes cruzan hasta 4 objetos relacionados; solo datos dentro de la plataforma; permisos por carpetas pendientes de definición; gestión desde la app online. Forecast: solo sobre Opportunities, sin división de objetivos por período, actualización manual de cumplimientos. CRM Analytics requiere licencia adicional.

## 11. Integraciones
Ver sección 4 de salesforce-design-guide.md. Incluir también la delimitación de las NO-integraciones esperables (pasarelas de pago, stock, BI directo).

## 12. Procesos batch / programados
Cargas o cálculos periódicos, vencimientos, recordatorios programados, sincronizaciones nocturnas. Schedule-Triggered Flow o Batch Apex según volumen/complejidad.

## 13. Monitoreo y operación
Manejo de errores de automatizaciones e integraciones (quién se entera y cómo), logs, reintentos. Para integraciones críticas: historia de monitoreo o consideración explícita de que el monitoreo es responsabilidad del cliente/middleware.

## 14. Capacitación y adopción
No genera historias de alcance (está cubierta por los Entregables fijos del template), pero si el cliente pidió algo específico (manuales por rol, train-the-trainer), documentarlo en Entregables o como consideración.
