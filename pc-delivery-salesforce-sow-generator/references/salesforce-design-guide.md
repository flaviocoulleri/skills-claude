# Guía de diseño de solución Salesforce (para el SOW)

Criterios para mapear procesos de negocio a la plataforma. El principio rector: **clicks before code** — agotar la configuración estándar antes de proponer desarrollo, porque el estándar es más barato de implementar, más barato de mantener, sobrevive a los releases de Salesforce y no consume presupuesto de testing propio.

## 1. Selección de nubes

| Señal en el proceso del cliente | Nube / producto |
|---|---|
| Prospección, pipeline, cotizaciones, cierre de ventas B2B/B2C | Sales Cloud |
| Atención al cliente, reclamos, mesa de ayuda, SLAs, canales de contacto | Service Cloud |
| Consumo masivo: rutas de venta, visitas a punto de venta, ejecución en tienda, promociones comerciales | Consumer Goods Cloud (+ CG Offline para campo) |
| Concesionarios, vehículos, garantías, ciclo de vida automotor | Automotive Cloud |
| Técnicos en campo, órdenes de trabajo, agendamiento, inventario de camión | Field Service |
| Portales para clientes/socios/distribuidores, autogestión | Experience Cloud |
| Campañas, journeys, email marketing, segmentación | Marketing Cloud |
| Catálogo de productos complejo, precios avanzados, facturación, suscripciones (CPQ) | Revenue Cloud |
| Unificación de datos de múltiples fuentes, perfiles unificados, segmentos | Data Cloud |
| Geolocalización, optimización de rutas, visualización en mapa | Salesforce Maps |
| Analítica avanzada, predicciones, dashboards sobre grandes volúmenes | CRM Analytics (licencia adicional — verificar disponibilidad) |
| Flujos guiados complejos, industria, transformación de datos declarativa | OmniStudio |

Una solución típica usa 1-2 nubes + transversales. No agregues nubes por completitud: cada nube es licenciamiento. Si el proceso lo sugiere pero el cliente no la tiene contratada, señálalo como riesgo/pregunta, no como alcance.

## 2. Mapeo a objetos estándar

Usar el objeto estándar siempre que la semántica coincida, aunque el cliente use otro nombre ("empresas" → Account, "solicitudes" → Case, "negocios" → Opportunity):

- **Lead**: prospectos sin calificar. Recordar la conversión Lead → Account + Contact + Opportunity y sus limitaciones (documentarla como consideración, el template lo hace).
- **Account / Contact**: empresas y personas. Person Accounts solo si el negocio es B2C puro (decisión irreversible — documentar como decisión de diseño).
- **Opportunity + OpportunityLineItem**: negocios en curso. Etapas = proceso de ventas del cliente.
- **Quote**: cotizaciones. Objeto separado de Opportunity por naturaleza de la plataforma (el template lo aclara al cliente). PDF de cotización estándar tiene limitaciones fuertes de formato — documentarlas siempre que haya generación de PDF.
- **Order**: pedidos. No hay traspaso automático Quote→Order estándar — si el cliente lo espera, es automatización (consideración típica del template).
- **Product2 + PriceBook**: catálogo y listas de precios; multi-divisa si hay varios territorios.
- **Case**: reclamos, solicitudes, tickets. Tipos de registro por proceso; homologar procesos similares en uno.
- **Campaign**: campañas y miembros.
- **Contract / Asset**: contratos y productos instalados/activos del cliente.
- **Task / Event**: actividades. Un solo responsable por tarea (limitación estándar documentable).
- **Territory Management, Forecast**: territorios y objetivos de venta. Forecast estándar solo suma Opportunities ganables, no divide objetivos por períodos — limitación clásica a documentar.

**Objeto custom** solo cuando: (a) la entidad de negocio no tiene equivalente estándar razonable (p.ej. "Póliza", "Expediente técnico"), o (b) forzar el estándar rompería su semántica y sus automatizaciones nativas. En el SOW, la historia que introduce un objeto custom lleva Tipo de Funcionalidad "Personalizada" y una consideración justificando por qué el estándar no aplica.

## 3. Árbol de decisión de automatizaciones

En orden de preferencia:

1. **Configuración declarativa pura** (campos de fórmula, valores predeterminados, reglas de validación, tipos de registro, páginas Lightning dinámicas) — para lógica de presentación y validación simple.
2. **Flow** (Record-Triggered para reacciones a datos; Screen Flow para procesos guiados; Schedule-Triggered para procesos batch/programados declarativos) — el default para toda automatización. Workflow Rules y Process Builder están deprecados: no proponerlos en SOWs nuevos (el glosario del template puede definirlos, pero el diseño usa Flow).
3. **Approval Process** — para aprobaciones con matriz de aprobadores, resubmisión y bloqueo de registro.
4. **OmniStudio** — flujos guiados complejos multi-paso con transformación de datos, si el cliente tiene licencia.
5. **Apex** (triggers, Batch, Queueable, servicios) — cuando Flow no alcanza: lógica compleja sobre volúmenes altos, callouts complejos, transaccionalidad fina. Historia "Personalizada" + justificación.
6. **Platform Events / Change Data Capture** — arquitectura orientada a eventos, desacople con sistemas externos.
7. **LWC** — solo cuando la UI estándar no puede resolver la experiencia requerida.

Regla para el SOW: cada automatización es una historia (o parte de los criterios de una historia funcional) y sus supuestos van a Consideraciones (qué la dispara, qué NO hace, notificaciones en texto plano, etc.).

## 4. Integraciones

Detectar integración cuando el proceso menciona: otro sistema como fuente/destino de datos (ERP, facturación, e-commerce, WhatsApp, pasarelas de pago, BI), sincronización, "que se cargue automático desde", "que se envíe a".

Por cada integración, definir en el SOW:
- Dirección (entrante / saliente / bidireccional), objetos y datos involucrados, disparador (tiempo real vía API/Platform Events vs. batch programado), y responsable del desarrollo de la contraparte.
- Historia(s) de tipo "Personalizada" + consideraciones: dependencia de documentación técnica de la API del sistema externo y forma de autenticación (compromiso del cliente en Sprint 0 — el template lo lista), delimitación de qué NO se sincroniza, responsabilidad sobre integridad de datos cuando no hay integración saliente (patrón del template: si no hay sync de vuelta, se restringen permisos de edición y si el cliente los quiere, la integridad es su responsabilidad).
- Si no hay integración con un sistema mencionado, delimitarlo explícitamente: "No se consideran integraciones con [sistema] para [propósito]".

## 5. Estándar vs. Custom — cómo justificar

Cuando propongas custom, la justificación en el documento sigue el patrón del template: nombrar la limitación estándar concreta + la consecuencia + la solución. Ejemplo: "Por funcionalidad estándar de la plataforma de Salesforce, no se incluye la generación del registro y el traspaso automático de información desde el objeto cotización hacia el objeto pedidos. Se realizará una automatización mediante Flow que…".

Cuando el cliente pida algo innecesariamente complejo, el patrón es: documentar la alternativa estándar adoptada + delimitar lo no incluido + (si el cliente insiste) mover la versión compleja a Fuera de Alcance. Las objeciones de diseño se discuten con el usuario en el checkpoint (Fase 3), no se imponen silenciosamente en el documento.

## 6. Riesgos típicos a señalar

- Volumen de datos (límites de storage, performance de reportes >4 objetos relacionados — límite real documentado en el template).
- Calidad de datos del cliente para la migración (el template descarga la responsabilidad en el cliente — mantenerlo).
- Dependencia de terceros (APIs sin documentación, middleware inexistente).
- Licencias no confirmadas (CRM Analytics, Maps, OmniStudio, Data Cloud).
- Decisiones irreversibles (Person Accounts, arquitectura de territorios).
- Uso offline / conectividad en campo (validaciones de georreferencia informativas vs. restrictivas según conectividad — patrón CG del template).
- Gobernanza: definir matriz de roles y perfiles temprano (el template entrega el artefacto "Matriz de roles y perfiles").
