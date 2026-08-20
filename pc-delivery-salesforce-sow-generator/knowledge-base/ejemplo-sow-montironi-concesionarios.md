<!--
Ejemplo real de SOW aprobado: Montironi (grupo de concesionarios automotrices, Argentina).
Usar como referencia de estilo y criterio para proyectos de CONCESIONARIOS / AUTOMOTRIZ:
modelo de roles y visibilidad por marca/concesionario, gestión de Leads multicanal,
objeto custom Vehículo, Boletos, Pruebas de Manejo, integración con DMS,
Service Cloud (Omni-Channel) y Agentforce. Las imágenes del original fueron omitidas.
-->

 Statement of Work Refinado  
Montironi  
Implementación Salesforce

| Nombre del sistema  Salesforce |
| :---- |
| Tipo de documento  Statement of Work Refinado |
| Versión de documento  1.0 |

## **Control de versiones** {#control-de-versiones}

| Versión \# | Fecha de entrega | Creado por  | Resumen de cambios |
| :---: | :---: | :---: | :---: |
| 1.0 | 26 may 2026 | **Julian Reggio Matina** Analista Funcional **Micaela Dato Firpo** Project Manager | Primera versión |

## 

# **Índice** {#índice}

[Control de versiones	3](#control-de-versiones)

[Índice	4](#índice)

[1\. Introducción	5](#1.-introducción)

[2\. Glosario de términos	6](#2.-glosario-de-términos)

[3\. Sales Cloud \- Alcance de Implementación	9](#3.-sales-cloud---alcance-de-implementación)

[3.1 Modelo de Roles, Perfiles y Visibilidad	9](#3.1-modelo-de-roles,-perfiles-y-visibilidad)

[3.1.1 Definir roles funcionales del sistema	10](#3.1.1-definir-roles-funcionales-del-sistema)

[3.1.2 Definir permisos sobre Leads	10](#3.1.2-definir-permisos-sobre-leads)

[3.1.3 Definir permisos sobre Cuentas y Contactos	11](#3.1.3-definir-permisos-sobre-cuentas-y-contactos)

[3.1.4 Definir permisos sobre Oportunidades	11](#3.1.4-definir-permisos-sobre-oportunidades)

[3.1.5 Definir modelo de visibilidad por marca / concesionario	12](#3.1.5-definir-modelo-de-visibilidad-por-marca-/-concesionario)

[3.1.6 Configurar jerarquía de roles comerciales	12](#3.1.6-configurar-jerarquía-de-roles-comerciales)

[3.2 Gestión de Leads Estándar	13](#3.2-gestión-de-leads-estándar)

[3.2.1 Almacenar información de Leads	13](#3.2.1-almacenar-información-de-leads)

[3.2.2 Buscar y visualizar Leads existentes	14](#3.2.2-buscar-y-visualizar-leads-existentes)

[3.2.3 Crear Leads manualmente en Salesforce	14](#3.2.3-crear-leads-manualmente-en-salesforce)

[3.2.4 Actualizar información de Leads	15](#3.2.4-actualizar-información-de-leads)

[3.2.5 Asignación automática de Leads	16](#3.2.5-asignación-automática-de-leads)

[3.2.6 Establecer proceso de trabajo de un Leads	16](#3.2.6-establecer-proceso-de-trabajo-de-un-lead)

[3.2.7 Enviar para aprobación un Lead \[Presente Sow Original\]	18](#3.2.7-enviar-para-aprobación-un-lead-[presente-sow-original])

[3.2.8 Aprobar Leads \[Presente Sow Original\]	19](#3.2.8-aprobar-leads-[presente-sow-original])

[3.2.9 Rechazar Leads \[Presente Sow Original\]	19](#3.2.9-rechazar-leads-[presente-sow-original])

[3.2.10 Migración de campos del objeto Lead a Cuenta, Contacto y Oportunidad	20](#3.2.10-migración-de-campos-del-objeto-lead-a-cuenta,-contacto-y-oportunidad)

[3.2.11 Detectar Leads duplicados	21](#3.2.11-detectar-leads-duplicados)

[3.2.12 Enviar notificación vía Salesforce cuando se genera el Lead	22](#3.2.12-enviar-notificación-vía-salesforce-cuando-se-genera-el-lead)

[3.2.13 Seguimiento y agendamiento de actividades con Leads	23](#3.2.13-seguimiento-y-agendamiento-de-actividades-con-leads)

[3.2.14 Generar formulario Web To Lead Estándar	23](#3.2.14-generar-formulario-web-to-lead-estándar)

[3.3 Gestión de Cuenta Estándar	25](#3.3-gestión-de-cuenta-estándar)

[3.3.1 Almacenar información de Cuentas	26](#3.3.1-almacenar-información-de-cuentas)

[3.3.2 Crear cuentas manualmente en Salesforce	27](#3.3.2-crear-cuentas-manualmente-en-salesforce)

[3.3.3 Buscar y visualizar Cuentas existentes	28](#3.3.3-buscar-y-visualizar-cuentas-existentes)

[3.3.4 Actualizar información de Cuentas	28](#3.3.4-actualizar-información-de-cuentas)

[3.3.5 Enviar para aprobación una Cuenta \[Presente Sow Original\]	29](#3.3.5-enviar-para-aprobación-una-cuenta-[presente-sow-original])

[3.3.6 Aprobar Cuenta \[Presente Sow Original\]	30](#3.3.6-aprobar-cuenta-[presente-sow-original])

[3.3.7 Rechazar Cuenta \[Presente Sow Original\]	31](#3.3.7-rechazar-cuenta-[presente-sow-original])

[3.3.8 Detectar Cuentas duplicadas	31](#3.3.8-detectar-cuentas-duplicadas)

[3.3.9 Configurar y visualizar jerarquías de cuentas	32](#3.3.9-configurar-y-visualizar-jerarquías-de-cuentas-[presente-sow-original])

[3.3.10 Visualizar cantidad de vehículos adquiridos	33](#3.3.10-visualizar-cantidad-de-vehículos-adquiridos)

[3.3.11 Visualizar campañas de marketing que alcanzó el cliente	33](#3.3.11-visualizar-campañas-de-marketing-que-alcanzó-el-cliente)

[3.3.12 Visualizar oportunidades vigentes	34](#3.3.12-visualizar-oportunidades-vigentes)

[3.4 Gestión de Contactos Estándar	36](#3.4-gestión-de-contactos-estándar)

[3.4.1 Almacenar información de Contactos	36](#3.4.1-almacenar-información-de-contactos)

[3.4.2 Crear contactos manualmente en Salesforce	37](#3.4.2-crear-contactos-manualmente-en-salesforce)

[3.4.3 Actualizar información de Contactos	38](#3.4.3-actualizar-información-de-contactos)

[3.4.4 Buscar y visualizar Contactos existentes	38](#3.4.4-buscar-y-visualizar-contactos-existentes)

[3.4.5 Detectar Contactos duplicados	39](#3.4.5-detectar-contactos-duplicados)

[3.4.6 Enviar un correo electrónico al contacto \[Presente SOW Original\]	40](#3.4.6-enviar-un-correo-electrónico-al-contacto-[presente-sow-original])

[3.4.7 Almacenar y relacionar contactos con sus cuentas	41](#3.4.7-almacenar-y-relacionar-contactos-con-sus-cuentas)

[3.5 Gestión de Vehículos Custom	43](#3.5-gestión-de-vehículos-custom)

[3.5.1 Almacenar información de Vehículos	43](#3.5.1-almacenar-información-de-vehículos)

[3.5.2 Asociar garantías al vehículo	44](#3.5.2-asociar-garantías-al-vehículo)

[3.5.3 Ver y registrar actividades relacionadas al vehículo	45](#3.5.3-ver-y-registrar-actividades-relacionadas-al-vehículo)

[3.5.4 Registrar y relacionar la definición técnica de un modelo con vehículos específicos	46](#3.5.4-registrar-y-relacionar-la-definición-técnica-de-un-modelo-con-vehículos-específicos)

[3.5.5 Registrar y visualizar activos de cualquier tipo	46](#3.5.5-registrar-y-visualizar-activos-de-cualquier-tipo)

[3.6 Gestión de Oportunidades Estándar	48](#3.6-gestión-de-oportunidades-estándar)

[3.6.1 Almacenar información de Oportunidades	48](#3.6.1-almacenar-información-de-oportunidades)

[3.6.2 Crear oportunidades manualmente en Salesforce	49](#3.6.2-crear-oportunidades-manualmente-en-salesforce)

[3.6.3 Actualizar información de oportunidad	50](#3.6.3-actualizar-información-de-oportunidad)

[3.6.4 Asociar Pricebook a la oportunidad	50](#3.6.4-asociar-pricebook-a-la-oportunidad)

[3.6.5 Agregar productos a la oportunidad	51](#3.6.5-agregar-productos-a-la-oportunidad)

[3.6.6 Actualizar productos en la oportunidad	52](#3.6.6-actualizar-productos-en-la-oportunidad)

[3.6.7 Enviar para aprobación una Oportunidad \[Presente Sow Original\]	52](#3.6.7-enviar-para-aprobación-una-oportunidad-[presente-sow-original])

[3.6.8 Aprobar oportunidad \[Presente Sow Original\]	53](#3.6.8-aprobar-oportunidad-[presente-sow-original])

[3.6.9 Rechazar oportunidad \[Presente Sow Original\]	54](#3.6.9-rechazar-oportunidad-[presente-sow-original])

[3.6.10 Establecer proceso de trabajo de una oportunidad	55](#3.6.10-establecer-proceso-de-trabajo-de-una-oportunidad)

[3.6.11 Visualizador interactivo de vehículos, formas de pago y financiamiento	56](#3.6.11-visualizador-de-vehículos,-formas-de-pago-y-financiamiento)

[3.6.12 Registro de Vehículo Usado en Venta directa	57](#3.6.12-registro-de-vehículo-usado-en-venta-directa)

[3.6.13 Carga de Evidencia Visual de Usado	57](#3.6.13-carga-de-evidencia-visual-de-usado)

[3.6.14 Aprobación y Fijación de Precio de Usado	58](#3.6.14-aprobación-y-fijación-de-precio-de-usado)

[3.6.15 Impacto en la Oportunidad (Económico)	58](#3.6.15-impacto-en-la-oportunidad-\(económico\))

[3.6.16 Agendar pruebas de manejo de la Oportunidad	59](#3.6.16-agendar-pruebas-de-manejo-de-la-oportunidad)

[3.7 Gestión de Cotizaciones Estándar	60](#3.7-gestión-de-cotizaciones-estándar)

[3.7.1 Almacenar información de Cotizaciones	60](#3.7.1-almacenar-información-de-cotizaciones)

[3.7.2 Crear cotizaciones manualmente en Salesforce	62](#3.7.2-crear-cotizaciones-manualmente-en-salesforce)

[3.7.3 Actualizar información de cotización	62](#3.7.3-actualizar-información-de-cotización)

[3.7.4 Establecer proceso de trabajo de una cotización	63](#3.7.4-establecer-proceso-de-trabajo-de-una-cotización)

[3.7.5 Asociar productos a la cotización	64](#3.7.5-asociar-productos-a-la-cotización)

[3.7.6 Actualizar productos en la cotización	65](#3.7.6-actualizar-productos-en-la-cotización)

[3.7.7 Generar documentos PDF de cotización	65](#3.7.7-generar-documentos-pdf-de-cotización)

[3.7.8 Enviar para aprobación una cotización	66](#3.7.8-enviar-para-aprobación-una-cotización)

[3.7.9 Aprobar cotización	67](#3.7.9-aprobar-cotización)

[3.7.10 Rechazar cotización	68](#3.7.10-rechazar-cotización)

[3.7.11 Sincronizar cotización con oportunidad	68](#3.7.11-sincronizar-cotización-con-oportunidad)

[3.7.12 Seleccionar Forma de Pago en la Cotización	69](#3.7.12-seleccionar-forma-de-pago-en-la-cotización)

[3.7.13 Asociar Plan de Financiamiento a la Cotización	69](#3.7.13-asociar-plan-de-financiamiento-a-la-cotización)

[3.8 Gestión de Productos Estándar	71](#3.8-gestión-de-productos-estándar)

[3.8.1 Almacenar información de Productos	71](#3.8.1-almacenar-información-de-productos)

[3.8.2 Crear productos manualmente	72](#heading=h.v5rtw6vgs8uo)

[3.8.3 Actualizar información de productos	73](#heading=h.i9ks4b9cv3b9)

[3.8.4 Crear marcas comerciales (Business Brand) dentro de la organización	73](#3.8.2-crear-marcas-comerciales-\(business-brand\)-dentro-de-la-organización)

[3.8.5 Asociar productos a Pricebooks	74](#3.8.3-asociar-productos-a-pricebooks)

[3.8.6 Gestionar estado de productos (activo o inactivo)	75](#heading=h.54t0d38q1qft)

[3.8.7 Detectar SKUs de productos duplicados \[Presente SOW Original\]	75](#3.8.4-detectar-skus-de-productos-duplicados-[presente-sow-original])

[3.9 Gestión de Listas de Precios Estándar	77](#3.9-gestión-de-listas-de-precios-estándar)

[3.9.1 Almacenar información de lista de precios	77](#3.9.1-almacenar-información-de-lista-de-precios)

[3.9.2 Crear lista de precios manualmente en Salesforce	78](#heading=h.b17wxx4miz8s)

[3.9.3 Actualizar información de lista de precios	79](#heading=h.yjs5hybg55qy)

[3.9.4 Asociar productos a Pricebooks	80](#heading=h.7nbymvers2r4)

[3.10 Gestión de Actividades	81](#3.10-gestión-de-actividades)

[3.10.1 Gestionar Tareas	81](#3.10.1-gestionar-tareas)

[3.10.2 Enviar y Registrar Correo desde Salesforce	82](#3.10.2-enviar-y-registrar-correo-desde-salesforce)

[3.10.3 Crear y Gestionar Notas en Registros	83](#3.10.3-crear-y-gestionar-notas-en-registros)

[4\. Marketing Cloud on Core \- Alcance de Implementación	83](#heading=h.jc95wj4qcrvh)

[4.1 Configuración inicial	84](#heading=h.tc2xhxkexye1)

[4.1.1 Delegación de subdominio	84](#heading=h.wx82akol9n8f)

[4.1.2 Roles y usuarios	84](#heading=h.px1ezjm94why)

[4.2 Configuración del canal de WhatsApp	85](#heading=h.uidvqse3rze5)

[4.2.1 Conexión linea de Whatsapp	86](#heading=h.4uhxjj4j7200)

[4.3 Confección de Registros (Data Streams)	87](#heading=h.d73whlrgntm)

[4.3.1 Importación de contactos	87](#heading=h.ym7wrvd8sddi)

[4.4 Configuración de journeys	88](#heading=h.roj7allmub34)

[4.4.1 Configuración de 2 campañas	89](#heading=h.2ty4vm86vtkv)

[5\. Integraciones con DMS	91](#5.-integraciones-con-dms)

[5.1 Integración saliente de Cuentas	91](#5.1-integración-saliente-de-cuentas)

[5.2 Integración entrante de Cuentas	92](#5.2-integración-entrante-de-cuentas)

[5.3 Integración entrante de Productos	92](#5.3-integración-entrante-de-productos)

[5.4 Integración Entrante de Stock de Vehículos (DMS)	93](#5.4-integración-entrante-de-stock-de-vehículos-\(dms\))

[5.5 Integración Saliente de Operación/Boleto (Outbound)	94](#5.5-integración-saliente-de-operación/boleto-\(outbound\))

[5.6 Integración Entrante de Leads de Fábrica (Inbound)	94](#5.6-integración-entrante-de-leads-de-fábrica-\(inbound\))

[5.7 Integración Saliente de Estado de Leads	95](#5.7-integración-saliente-de-estado-de-leads)

[6\. Service Cloud	96](#6.-service-cloud)

[6.1 Configuración de Omni-Channel	96](#6.1-configuración-de-omni-channel)

[6.2 Configuración de Casos	97](#6.2-configuración-de-casos)

[6.3 Canal de Email-to-Case	97](#6.3-canal-de-email-to-case)

[6.4 Consola de Servicio (Interfaz de Agente)	98](#6.4-consola-de-servicio-\(interfaz-de-agente\))

[6.5 Reportes y Tableros de Servicio	99](#6.5-reportes-y-tableros-de-servicio)

[7\. Agentforce (Agentes de IA)	99](#7.-agentforce-\(agentes-de-ia\))

[7.1 Agente de Primera Respuesta	100](#7.1-agente-de-primera-respuesta)

[7.2 Calificación y Generación de Leads	101](#7.2-calificación-y-generación-de-leads)

[7.3 Transferencia Inteligente	101](#7.3-transferencia-inteligente)

[8\. Entregables \- Etapas posteriores	102](#8.-entregables---etapas-posteriores)

[8.1 Entregables y Compromisos del Cliente \- Etapa de Sprint 0	102](#8.1-entregables-y-compromisos-del-cliente---etapa-de-sprint-0)

[8.2 Entregables  y Compromisos del Equipo de ProContacto \- Etapa de Sprint 0	103](#8.2-entregables-y-compromisos-del-equipo-de-procontacto---etapa-de-sprint-0)

[8.3 Entregables  y Compromisos del Cliente \- Etapa de Ejecución	104](#8.3-entregables-y-compromisos-del-cliente---etapa-de-ejecución)

[8.4 Entregables del Equipo de ProContacto \- Etapa de Ejecución	104](#8.4-entregables-del-equipo-de-procontacto---etapa-de-ejecución)

[9\. Cronología	106](#9.-cronología)

[10\. Controles de Cambio	107](#10.-controles-de-cambio)

[11\. Fuera de Alcance \- Release 1.0	108](#11.-fuera-de-alcance---release-1.0)

[11.1 Automatización Predictiva de Marketing (Marketing Cloud)	108](#11.1-automatización-predictiva-de-marketing-\(marketing-cloud\))

[11.1.1 Predictive Journey – Flujo de Administración de Planes	108](#11.1.1-predictive-journey-–-flujo-de-administración-de-planes)

[11.1.2 Predictive Journey – Flujo de Reactivación de Compras	109](#11.1.2-predictive-journey-–-flujo-de-reactivación-de-compras)

[11.1.3 Segmentación Inteligente – Prospección de Posventa	109](#11.1.3-segmentación-inteligente-–-prospección-de-posventa)

[11.1.4 Segmentación Inteligente – Reactivación de Presupuestos No Autorizados	110](#11.1.4-segmentación-inteligente-–-reactivación-de-presupuestos-no-autorizados)

[11.1.5 Observaciones	111](#11.1.5-observaciones)

[11.1.6 Estado final	111](#11.1.6-estado-final)

[11.2 Inteligencia de Datos y Modelos (Data Cloud & Analytics)	111](#11.2-inteligencia-de-datos-y-modelos-\(data-cloud-&-analytics\))

[11.2.1 Modelado de Prospección Algorítmica – Fase 1	111](#11.2.1-modelado-de-prospección-algorítmica-–-fase-1)

[11.2.2 Análisis de Cartera con IA – Dashboards Predictivos CRM Analytics	112](#11.2.2-análisis-de-cartera-con-ia-–-dashboards-predictivos-crm-analytics)

[11.2.3 Unificación de Datos para IA – Configuración de Data Cloud	113](#11.2.3-unificación-de-datos-para-ia-–-configuración-de-data-cloud)

[11.2.4 Observaciones	113](#11.2.4-observaciones)

[11.2.5 Estado final	113](#11.2.5-estado-final)

[11.3 Flujos de Trabajo Inteligentes (Flow Builder)	114](#11.3-flujos-de-trabajo-inteligentes-\(flow-builder\))

[11.3.1 Automatización de Calidad – Planes de Acción tras Detractores NPS	114](#11.3.1-automatización-de-calidad-–-planes-de-acción-tras-detractores-nps)

[11.3.2 Optimización Logística – Seguimiento Automatizado de Traslados	114](#11.3.2-optimización-logística-–-seguimiento-automatizado-de-traslados)

[11.3.3 Observaciones	115](#11.3.3-observaciones)

[11.3.4 Estado final	115](#11.3.4-estado-final)

[11.4 Objeto "Plan de Ahorro"	115](#11.4-objeto-"plan-de-ahorro")

[11.4.1 Creación del Objeto Plan de Ahorro	115](#11.4.1-creación-del-objeto-plan-de-ahorro)

[11.4.2 Automatización de Baja de Plan de Ahorro por Cuotas Impagas	116](#11.4.2-automatización-de-baja-de-plan-de-ahorro-por-cuotas-impagas)

[11.4.3 Reactivación de Plan de Ahorro Dado de Baja	117](#11.4.3-reactivación-de-plan-de-ahorro-dado-de-baja)

[11.4.4 Observaciones	117](#11.4.4-observaciones)

[11.4.5 Estado final	118](#11.4.5-estado-final)

[11.5 Objeto "Cuota"	118](#11.5-objeto-"cuota")

[11.5.1 Creación del Objeto Cuota	118](#11.5.1-creación-del-objeto-cuota)

[11.5.2 Observaciones	119](#11.5.2-observaciones)

[11.5.3 Estado final	119](#11.5.3-estado-final)

[11.6 Objeto "Licitación"	119](#11.6-objeto-"licitación")

[11.6.1 Creación del Objeto Licitación	119](#11.6.1-creación-del-objeto-licitación)

[11.6.2 Integración con Fábrica al Crear Licitación	120](#11.6.2-integración-con-fábrica-al-crear-licitación)

[11.6.3 Flujo de Aprobación de Tasación de Vehículo Usado en Licitación	120](#11.6.3-flujo-de-aprobación-de-tasación-de-vehículo-usado-en-licitación)

[11.6.4 Observaciones	121](#11.6.4-observaciones)

[11.6.5 Estado final	121](#11.6.5-estado-final)

[12\. Aprobaciones	122](#12.-aprobaciones)

[12.1 Individuos que necesitan aprobar el SOW antes de que pueda implementarse	122](#12.1-individuos-que-necesitan-aprobar-el-sow-antes-de-que-pueda-implementarse)

# **1\. Introducción** {#1.-introducción}

El presente documento está orientado a brindar una descripción sobre el entendimiento de los requerimientos proporcionados para el desarrollo de la plataforma de Salesforce. Se pautarán qué consideraciones se tomarán en cuenta para dicho desarrollo, así como un entendimiento del proceso de trabajo, restricciones de negocio, automatizaciones, entre otros.

Además, se establecerá una delimitación clara del alcance del proyecto. El desarrollo de cualquier requerimiento o consideración no incluida en este documento ya sea funcionalidad, automatización, validación, flujo o integración implica un esfuerzo adicional. Por lo tanto, los elementos no mencionados en este documento estarán fuera del alcance del proyecto.

Es importante tener en cuenta que este documento servirá como referencia para el desarrollo, configuración y personalización del entorno de Salesforce. Se espera que el equipo de implementación de ProContacto trabaje en estrecha colaboración con MONTIRONI para asegurar una comprensión y alineación claras de los objetivos, requisitos y restricciones del proyecto.

Asimismo, se establecerá un marco de trabajo para la gestión del proyecto, definiendo las responsabilidades y la comunicación entre todas las partes involucradas. Se acordarán plazos y entregables específicos, así como mecanismos de seguimiento y control para garantizar el cumplimiento de los objetivos del proyecto.

Se espera que este proyecto sea una colaboración exitosa y productiva entre MONTIRONI y ProContacto. Con un enfoque claro en los objetivos, una comunicación abierta y un seguimiento constante, lograremos entregar un software de alta calidad que cumpla con sus expectativas y contribuya al éxito de su organización.

# **2\. Glosario de términos** {#2.-glosario-de-términos}

| Concepto | Definición |
| ----- | ----- |
| Nube | En el contexto de Salesforce, una nube se refiere a una instancia de la plataforma que ofrece servicios específicos para un área de negocio, como ventas, marketing o servicio al cliente. Cada nube de Salesforce tiene sus propias características y funcionalidades adaptadas a las necesidades de esa área en particular. |
| Integración | La integración implica combinar diferentes sistemas, aplicaciones o plataformas para que funcionen de manera conjunta y compartan información de manera eficiente. En el contexto de Salesforce, la integración se refiere a la conexión y sincronización de la plataforma con otros sistemas o herramientas utilizados por la empresa. |
| Alcance | Se define como todas las características, entregables, objetivos y requisitos que se deben cumplir para considerar que el proyecto ha sido completado con éxito. |
| Desvío | El desvío se refiere a la identificación de un requerimiento adicional que no estaba inicialmente incluido en el alcance del proyecto. Durante el relevamiento de requerimientos, se descubre un nuevo requisito que no fue contemplado en el alcance original. |
| Control de cambio | El control de cambio es un proceso que se utiliza para gestionar y controlar los cambios en un sistema o aplicación, como Salesforce. Implica la planificación, evaluación, implementación y seguimiento de los cambios realizados para minimizar riesgos y garantizar una transición suave. |
| Importación | La importación se refiere al proceso de transferir datos o información desde una fuente externa a una plataforma o sistema, como Salesforce. Permite cargar datos desde archivos o bases de datos externas para su uso en la plataforma. |
| Sprint | El sprint es un marco de trabajo utilizado en metodologías ágiles, como Scrum. Representa un período de tiempo fijo y corto (generalmente de 1 a 4 semanas) en el cual se realiza un trabajo concentrado y se entregan incrementos de funcionalidad en un proyecto. |
| Sprint 0 | Período de tiempo previo a la implementación de la plataforma, en el cual se relevan los requerimientos, se detectan puntos de mejora, se lleva a cabo un entendimiento del negocio, se corrobora el alcance inicial e identifica desvíos en caso de aplicar. |
| UAT | UAT (User Acceptance Testing), conocido también como prueba de aceptación del usuario, se refiere a un proceso en el cual los usuarios finales prueban el software o sistema implementado para validar su funcionamiento y verificar que cumple con los requisitos y expectativas. |
| Scrum | Scrum es una metodología ágil utilizada para la gestión de proyectos. Se basa en el desarrollo iterativo e incremental, donde el trabajo se divide en sprints y se enfoca en la colaboración, la adaptabilidad y la entrega de valor de manera rápida y constante. |
| Relevamiento | El relevamiento, también conocido como análisis de requerimientos, es un proceso en el cual se recopila y analiza información sobre las necesidades y objetivos del cliente o usuario final. En el contexto de la implementación de Salesforce, implica comprender los requisitos empresariales y determinar cómo se pueden abordar utilizando la plataforma. |
| Endpoint | Un endpoint se refiere a un punto final de comunicación en un sistema o servicio, generalmente a través de una API (Application Programming Interface).  Los endpoints se utilizan para establecer conexiones y permitir la interacción con otros sistemas o servicios externos. |
| Middleware | El middleware es un software que actúa como intermediario entre diferentes aplicaciones, sistemas o componentes. El middleware puede utilizarse para facilitar la integración y la comunicación entre la plataforma y otros sistemas empresariales. |
| API | La API (Application Programming Interface) es un conjunto de reglas y protocolos que permiten que diferentes sistemas o aplicaciones se comuniquen e intercambien información entre sí. En Salesforce, las API se utilizan para acceder y manipular los datos y funcionalidades de la plataforma desde aplicaciones externas o sistemas personalizados. |
| Backend | El backend se refiere a la parte de un sistema o aplicación que se encarga del procesamiento de datos, la lógica de negocio y la gestión de la base de datos. En Salesforce, el backend se refiere a los componentes y procesos internos que permiten el funcionamiento de la plataforma y el manejo de los datos de los usuarios. |
| Frontend | El frontend se refiere a la parte de un sistema o aplicación que los usuarios finales interactúan directamente. En Salesforce, el frontend se compone de la interfaz de usuario y las funcionalidades que los usuarios utilizan para acceder y trabajar con la plataforma. |
| Base de datos | Una base de datos es un conjunto estructurado de datos organizados y almacenados de manera que se puedan acceder y manipular de forma eficiente. En Salesforce, la base de datos almacena los datos de los clientes, contactos, oportunidades y otros objetos relacionados con la gestión de la relación con el cliente (CRM). |
| Módulo | Un módulo se refiere a una parte o componente funcional específico de un sistema o aplicación. En Salesforce, los módulos representan las diferentes áreas o funcionalidades de la plataforma, como ventas, marketing, servicio al cliente, entre otros. |
| Responsividad | La responsividad se refiere a la capacidad de una plataforma o aplicación para adaptarse y ofrecer una experiencia de usuario óptima en diferentes dispositivos y tamaños de pantalla, como computadoras de escritorio, tabletas o teléfonos móviles. En Salesforce, la responsividad asegura que la plataforma se pueda utilizar de manera eficiente en diversos dispositivos. |
| QA | QA (Quality Assurance) se refiere a un conjunto de actividades y procesos que tienen como objetivo garantizar la calidad de un producto o servicio. En el contexto de una empresa implementadora de Salesforce, el QA implica la planificación y ejecución de pruebas para asegurar que la plataforma funcione correctamente y cumpla con los requisitos establecidos. |
| Apex | Apex es un lenguaje de programación orientado a objetos utilizado en la plataforma Salesforce. Permite personalizar y extender la funcionalidad de Salesforce mediante el desarrollo de código. Apex se utiliza principalmente para escribir lógica empresarial, crear controladores de flujo de trabajo y desarrollar aplicaciones personalizadas en la plataforma. |
| Objeto | En Salesforce, un objeto es una representación de una entidad o tabla en una base de datos relacional. Los objetos almacenan y organizan los datos relacionados con una determinada entidad de negocio, como cuentas, contactos, oportunidades, entre otros. |
| Registro | Un registro se refiere a una instancia o entrada específica de un objeto en Salesforce. Representa una entidad de datos única con atributos y valores específicos. Por ejemplo, un registro de contacto representa a una persona específica con su información personal. |
| Trigger | En Salesforce, un trigger es un fragmento de código Apex que se ejecuta automáticamente antes o después de un evento específico en la plataforma. Los triggers actúan como disparadores para iniciar acciones, como actualizaciones de datos, cuando se produce el evento asociado. Los triggers son utilizados para personalizar y automatizar la lógica empresarial en Salesforce. |
| Web to Lead | En Salesforce, web to lead es una funcionalidad que permite capturar y recopilar información de prospectos o clientes potenciales directamente desde un formulario web y crear automáticamente registros de leads en Salesforce. Al configurar Web-to-Lead, se genera un código HTML que se puede incrustar en una página web o formulario en línea. |
| Workflow Rule | Las Workflow Rules son automatizaciones que ejecutan una serie de acciones predefinidas cuando se cumplen ciertas condiciones. Esto ahorra tiempo al realizar acciones como enviar correos electrónicos o actualizar información, sin tener que hacerlo manualmente. |
|  Regla de validación | Una Regla de Validación es un mecanismo que verifica y asegura la exactitud y coherencia de los datos introducidos. Si los datos no cumplen con ciertos criterios predefinidos, la regla emite un mensaje de error, garantizando así la integridad de la información almacenada y preservando la calidad de los datos en el sistema. |
| Tipo de registro | Refiere a una clasificación predefinida que determina la estructura y las características de los datos que se pueden almacenar en una base de datos o sistema de información. Estas categorías actúan como plantillas estandarizadas que especifican los campos de información requeridos y las reglas para su ingreso. Si un objeto posee varios tipos de registro, cada uno de ellos podrá tener un conjunto de campos independiente del resto. |

# **3\. Sales Cloud \- Alcance de Implementación** {#3.-sales-cloud---alcance-de-implementación}

Se detallan a continuación los requerimientos detectados y evaluados en un alto nivel de detalle, teniendo en cuenta ciertas consideraciones como la definición total del requerimiento en etapas posteriores de refinamiento, permisos sobre la plataforma, alcance del requerimiento, entre otros.

## **3.1 Modelo de Roles, Perfiles y Visibilidad** {#3.1-modelo-de-roles,-perfiles-y-visibilidad}

(imagen omitida)

Como parte de la implementación de Salesforce Sales Cloud y Marketing Cloud para Montironi, es necesario definir y configurar un modelo de roles, perfiles y visibilidad de la información que asegure:

* Correcta segregación de datos por marca, concesionario y rol.  
* Control del accionar comercial.  
* Protección de la información sensible.  
* Escalabilidad del modelo para futuras fases.

Esta épica contempla la definición funcional y técnica del modelo de seguridad base, alineado a las buenas prácticas de Salesforce y a la operación actual de Montironi.

### 3.1.1 Definir roles funcionales del sistema {#3.1.1-definir-roles-funcionales-del-sistema}

3.1.1.1 Narrativa:

**Como** equipo de proyecto,  
**Quiero** definir los roles funcionales que utilizarán Sales Cloud,  
**Para** asegurar una correcta asignación de permisos y visibilidad.

3.1.1.2 Criterios de aceptación:

* Roles definidos y validados por Montironi.

* La jerarquía de roles es la siguiente:

  * Director General — lectura de toda la operación, todas las marcas y todas las sucursales.

    * Gerente de Canal de Venta (Venta Tradicional / Venta Plan de Ahorro) — visibilidad de todas las marcas y sucursales dentro de su canal.

      * Gerente de Marca (por tipo de venta) — visibilidad de todas las sucursales de su marca.

        * Supervisor de Ventas — visibilidad de su marca y su(s) sucursal(es) asignada(s).

          * Vendedor — visibilidad restringida a su marca y sucursal asignada únicamente.

* Marketing — acceso transversal de lectura para campañas y reportes, sin acceso a detalles de cartera de vendedores.

* Administrador Salesforce — acceso total al sistema.

* Administrador de Leads (Contact Center) — visibilidad transversal de leads de todas las marcas y sucursales, sin acceso a la cartera de oportunidades de los vendedores.

* La visibilidad por **marca y sucursal** se implementa mediante la combinación de jerarquía de roles \+ **Grupos públicos** (uno por combinación marca/sucursal) \+ **Reglas de Colaboración** para excepciones, evitando la proliferación de roles específicos por cada combinación posible.

* Un vendedor estándar accede únicamente a los registros (leads, cuentas, contactos, oportunidades) correspondientes a su marca y sucursal asignada. Las mismas restricciones de visibilidad que aplican a leads aplican de forma consistente a cuentas y contactos.

* Para vendedores **híbridos o multimarca/multisucursal** (ej.: vendedor que opera en dos sucursales o cubre dos marcas), el acceso ampliado se gestiona exclusivamente mediante **Reglas de Colaboración**, sin crear roles adicionales. Esto debe ser la excepción, no la regla.

* Cada usuario tiene **un único rol** en la jerarquía. La granularidad operativa (marca \+ sucursal) se resuelve a nivel de grupos y reglas de colaboración, no a nivel de rol.

* Las restricciones de visibilidad se aplican de forma transversal a todos los objetos del sistema: Leads, Cuentas, Contactos y Oportunidades.

* Los perfiles (qué puede hacer el usuario) se definen de forma independiente a los roles (qué puede ver el usuario), siguiendo el esquema acordado durante la implementación.

  ### 3.1.2 Definir permisos sobre Leads {#3.1.2-definir-permisos-sobre-leads}

  3.1.2.1 Narrativa:

  **Como** Administrador Salesforce,  
  **Quiero** definir permisos por rol sobre el objeto Lead,  
  **Para** controlar creación, edición, asignación y conversión.

  3.1.2.2 Criterios de aceptación:

* Permisos:  
  * Ejecutivo Comerciales:  
    Crea y edita solo sus leads  
    No puede eliminar  
  * Supervisor:  
    Ve y edita leads de su equipo pero no puede eliminar  
  * Administrador/Directivos:

  * Dirección general solo de lectura. 

  * Gerencias para abajo edición, porque participan de procesos de aprobación y/o cierran ventas. Con acceso limitado, se deberá definir posteriormente el acceso específico por objeto y campo.

  * Administrador de leads transversal para todas las marcas (coordinación del Contact Center), con acceso limitado a realizar cambios como vendedor asignado, grupo, entre otros.

    ### 3.1.3 Definir permisos sobre Cuentas y Contactos {#3.1.3-definir-permisos-sobre-cuentas-y-contactos}

    3.1.3.1 Narrativa:

    **Como** Administrador Salesforce  
    **Quiero** definir permisos por rol sobre Cuentas y Contactos  
    **Para** asegurar trazabilidad y calidad del dato una vez convertido el lead.

    3.1.3.2 Criterios de aceptación:

* Permisos:

  * Ejecutivo Comerciales:  
    Lectura y edición limitada en base al origen del lead. No tiene permisos de borrado de leads

  * Supervisor:  
    Edición y control. Aplican las mismas restricciones que el vendedor.

  * Administrador/Directivos:  
    Acceso total. Aplican las mismas restricciones que al resto. 

  * Administrador de leads transversal para todas las marcas (coordinación del Contact Center), con acceso limitado a realizar cambios como vendedor asignado, grupo, etc 

    ### 3.1.4 Definir permisos sobre Oportunidades {#3.1.4-definir-permisos-sobre-oportunidades}

    3.1.4.1 Narrativa:

    **Como** Administrador Salesforce  
    **Quiero** definir permisos por rol sobre Oportunidades  
    **Para** controlar el ciclo de venta y el forecast.

    3.1.4.2 Criterios de aceptación:

* Permisos:  
  * Ejecutivo Comerciales:  
    Crea y edita oportunidades propias. No borra  
  * Supervisor:  
    Ve oportunidades del equipo  
  * Administrador/Directivos:  
    Acceso total de sólo lectura.

    ### 3.1.5 Definir modelo de visibilidad por marca / concesionario {#3.1.5-definir-modelo-de-visibilidad-por-marca-/-concesionario}

    3.1.5.1 Narrativa:

    **Como** Gerente Comercial  
    **Quiero** que los usuarios visualicen sólo información de su marca o concesionario  
    **Para** mantener el foco comercial y el orden operativo.

    3.1.5.2 Criterios de aceptación:

* Permisos:  
  * Modelo de visibilidad documentado y validado por Montironi antes de la configuración.

  * Los ejecutivos solo ven registros de su ámbito (sucursal \+ marca asignada).

  * Supervisores ven información agregada de su marca, respetando la jerarquía de roles definida en este documento.

  * La segmentación se aplica de forma transversal sobre Leads, Cuentas, Contactos y Oportunidades.

  * Para casos excepcionales donde un vendedor opera en más de una marca o sucursal, se utilizarán **Reglas de Colaboración (Sharing Rules)** en Salesforce para ampliar el acceso puntualmente, sin modificar la jerarquía de roles ni crear combinaciones adicionales.

  * El uso de Sharing Rules para excepciones debe ser solicitado al Administrador de Salesforce y queda registrado como configuración auditada.

    ### 3.1.6 Configurar jerarquía de roles comerciales {#3.1.6-configurar-jerarquía-de-roles-comerciales}

    3.1.6.1 Narrativa:

    **Como** Administrador Salesforce  
    **Quiero** configurar la jerarquía de roles  
    **Para** permitir visibilidad escalonada y reportería correcta.

    3.1.6.2 Criterios de aceptación:

* Permisos:

  * Jerarquía definida y configurada según el esquema validado por Montironi.

  * Supervisores ven información de sus equipos por herencia de jerarquía.

  * Cada usuario tiene un único rol en la jerarquía. El rol determina la visibilidad vertical (qué registros de jerarquía inferior puede ver).

  * La segmentación por canal, marca y sucursal se implementa mediante **grupos de Salesforce**, no mediante la multiplicación de roles. Esto evita una lista inmanejable de combinaciones marca/sucursal/tipo de venta.

  * La visibilidad cruzada autorizada (ej. un supervisor que necesita ver datos de otra marca) se gestiona mediante **Reglas de Colaboración**, no mediante cambios de rol.

    ### 3.1.7 Consideraciones

    3.1.7.1 La definición específica de cantidad de roles y perfiles junto a sus permisos será definido en fases posteriores por el equipo de Montironi.

  ## **3.2 Gestión de Leads Estándar** {#3.2-gestión-de-leads-estándar}

(imagen omitida)

### 3.2.1 Almacenar información de Leads {#3.2.1-almacenar-información-de-leads}

3.2.1.1 Narrativa:

Como ejecutivo de ventas,  
quiero almacenar la información relacionada a mis Leads,  
para posteriormente, realizar gestiones con ellos.

3.2.1.2 Criterios de Aceptación:

* Se deberá poder almacenar la información definida dentro del DDD asociada a un Lead.  
* Se deberá implementar la herramienta de Chatter a la hora de encontrarse dentro de la ficha de un Lead.  
* Se deberá asignar el o los vehículos de interés.  
* Se deberán incluir las siguientes validaciones con respecto a la información a almacenar:  
  * Se deberán establecer obligatorios los campos definidos en el DDD para la gestión de un Lead.  
  * Se establecerá qué información será obligatoria, dependiendo del estado del lead según la información en el DDD.

    ### 3.2.2 Buscar y visualizar Leads existentes {#3.2.2-buscar-y-visualizar-leads-existentes}

    3.2.2.1 Narrativa:

    **Como** ejecutivo de ventas,  
    **Quiero** buscar y visualizar los Leads existentes por distintos campos   
    **para** posteriormente, gestionar mis prospectos de manera efectiva.

    3.2.2.2 Criterios de Aceptación:

    * La ficha del Lead debe mostrar todos los campos que se especificaron en el relevamiento. 

      * Por defecto se podrá ver la información de Leads del concesionario al que el ejecutivo está asignado, salvo perfiles administrativos.

        * Los duplicados entre dealers deben ser visibles solo para perfiles con permisos avanzados y el sistema debe alertar en el caso de duplicaciones aun si el duplicado está en otra marca y el usuario no tiene permiso para visualizarlo. 

    ### 3.2.3 Crear Leads manualmente en Salesforce {#3.2.3-crear-leads-manualmente-en-salesforce}

    3.2.3.1 Narrativa:

    **Como** ejecutivo de ventas,  
          **quiero** registrar prospectos que llegan directamente al concesionario,  
          **para** realizar un seguimiento adecuado.

    3.2.3.2 Criterios de Aceptación:

* La creación de los Lead será de forma manual, en forma individual, es decir que cada vendedor podrá dar de alta leads de a uno, en su usuario y solo para su gestión individual.  
* El formulario de creación del lead debe respetar los campos correspondientes a cada una de las marcas de Montironi (Ford, Fiat, Jeep / RAM, Peugeot, Hyundai, GAC), sucursal y tipo de venta.   
* Es importante que el campo Origen no sea editable ni tengan la posibilidad de crear infinitos orígenes. Tiene que ser un desplegable con opciones, que solo puedan cambiar los administradores.  
* En el caso que un supervisor o gerente quiera dar de alta una lista de leads para gestionar, debe solicitarlo a través de un proceso de solicitud al área de Contact Center, ya sea para que gestione su equipo o el mismo contact center. La vía de ingreso de los leads a gestionar debe ser a través de una campaña, para que mantengan o conserven su origen inicial.   
* Los campos obligatorios establecidos en la historia de usuario Almacenar información de Leads deberán ser completados para la creación.  
* El usuario podrá completar los campos opcionales.  
* Se debe asociar el Lead al ejecutivo logueado.  
* Los usuarios deberán completar la información obligatoria.  
* En el caso que exista al menos un campo obligatorio sin completar, no se podrá crear el registro.

* En el caso de que algún dato del lead permita verificar que es una cuenta ya existente en la base de datos consolidada (no por marca), durante la conversión, el usuario podrá seleccionar la cuenta existente como destino, evitando la creación de un duplicado. Las oportunidades previas de esa cuenta no se verán afectadas y convivirán con la nueva oportunidad generada por la conversión.

  ### 3.2.4 Actualizar información de Leads {#3.2.4-actualizar-información-de-leads}

  3.2.4.1 Narrativa:

  **Como**  ejecutivo de ventas,  
  **quiero** completar datos adicionales del Lead a medida que interactúo,  
  **para** enriquecer su perfil y calificar mejor su intención de compra.

  3.2.4.2 Criterios de Aceptación:

* Los campos obligatorios establecidos en la historia de usuario [Almacenar información de Leads](https://procontacto.atlassian.net/wiki/spaces/PROCMOD/pages/edit-v2/1111326738?draftShareId=a385bc25-3529-4c6c-b597-4b34d0a381fd#Almacenar-informaci%C3%B3n-de-%5Bobjeto%5D) deberán permanecer completados ante la modificación. Caso contrario, el sistema mostrará un mensaje de error.  
* El usuario podrá modificar el contenido de los campos opcionales.  
* Los usuarios deberán completar o mantener completada la información obligatoria.  
* El origen del lead no puede modificarse, sin excepción.   
* En el caso que exista al menos un campo obligatorio sin completar, no se podrá actualizar el registro.

  ### 3.2.5 Asignación automática de Leads {#3.2.5-asignación-automática-de-leads}

  3.2.5.1 Narrativa:

  **Como** administrador de ventas,  
  **quiero** que los Leads se asignen automáticamente  
  **para**  que puedan ser tomados por ejecutivos disponibles según reglas predefinidas.

  3.2.5.2 Criterios de Aceptación:

* El sistema debe ejecutar reglas de asignación cuando ingresa un lead, distribuyendo entre los usuarios de un grupo dependiendo del tipo de venta y luego la marca, cuando corresponda. 

* El bot de Agentforce gestiona **exclusivamente** leads que ingresan por canal **WhatsApp**. Si un lead llega por cualquier otro canal (email, formulario web, integración de fábrica, etc.) o sin un número de teléfono asociado, el bot no tiene capacidad de gestionarlo. En esos casos, el lead se asigna directamente a la cola de Coordinación de Venta Digital del Contact Center con estado "Unassigned" para atención manual. 

* Cuando el lead ingresa por WhatsApp, el bot de AgentForce atiende la conversación, determina el motivo de consulta (Venta Tradicional, Venta de Planes, Posventa, Usados, Repuestos, Administración u Otros) y crea el lead con ese campo completado. 

*  Al ingresar un lead, el sistema debe verificar el motivo de consulta mediante un campo picklist obligatorio con los siguientes valores: Venta Tradicional, Venta de Planes, Posventa, Usados, Repuestos, Administración y Otros.

* Este campo será completado automáticamente por Agentforce cuando el lead ingrese por canal digital (WhatsApp/Web). En caso de no poder tipificarse, el sistema asignará el lead a la cola de Coordinación de Venta Digital del Contact Center con estado "Unassigned" para asignación manual. 

* Los leads tipificados como Venta Tradicional o Venta de Planes se asignan automáticamente al equipo de Asesores Digitales del Contact Center, sin discriminar marca en esta primera instancia. 

* La asignación se realizará en modalidad **round-robin secuencial 1 a 1**: cada nuevo lead se asigna al asesor que recibió su última asignación hace más tiempo dentro del equipo activo.

  * Antes de ejecutar el round-robin, el sistema debe verificar si el cliente (identificado por DNI, email o teléfono) ya cuenta con una **Oportunidad abierta** para la misma marca de interés del lead. Si existe, el nuevo lead se asigna automáticamente al mismo vendedor que gestiona esa oportunidad, sin pasar por el round-robin. 

  * Si la oportunidad existente es de una **marca diferente**, se aplica el round-robin normal al equipo de esa otra marca. 

* Se configurarán dos equipos diferenciados por horario: uno activo de lunes a viernes y otro para días sábado. La regla de asignación evaluará el día y hora de ingreso del lead para determinar a qué equipo corresponde.

* Una vez asignado, el asesor debe completar los siguientes campos requeridos sobre el registro del Lead antes de poder convertirlo:

  * Tipo de venta confirmado (Venta Tradicional / Venta de Planes / Otro).

  * Sucursal de preferencia del cliente.

  * Marca de interés.

  * Vehículo de interés.

* Si el asesor determina que el tipo de venta debe cambiar respecto al ingresado originalmente, debe actualizar el campo correspondiente en el Lead. El valor original debe quedar registrado en el historial del campo para trazabilidad.

* Si el lead no califica, el asesor cambia el estado a "Descartado" y debe completar obligatoriamente el campo "Motivo de descarte" para poder guardar el registro.

* Una vez validados el tipo de venta, sucursal, marca y vehículo de interés, el asesor convierte el lead generando una oportunidad. En ese momento aplica la lógica de asignación de oportunidades definida en HU 3.6.17.

* La conversión debe respetar la lógica de detección de cuentas existentes definida en HU 3.2.11 y 3.2.3.

* Si ninguna regla de asignación coincide, el lead se asigna automáticamente a la cola de Coordinación de Venta Digital del Contact Center (usuario/grupo de respaldo predefinido).

* Los leads no asignados deben quedar con estado "Unassigned" y ser visibles en una lista compartida desde la cual los asesores habilitados pueden tomarlo voluntariamente.

* Al momento en que un ejecutivo toma un lead, el sistema debe registrar automáticamente la fecha y hora de esa acción en un campo de auditoría del registro.

* Las reglas de asignación automática aplican únicamente a leads ingresados por canales digitales y/o creados por el Contact Center.

* Los leads creados manualmente por un vendedor desde su propio usuario quedan asignados a ese vendedor y no pasan por las reglas de asignación automática.

(imagen omitida)

### 3.2.6 Establecer proceso de trabajo de un Lead {#3.2.6-establecer-proceso-de-trabajo-de-un-lead}

3.2.6.1 Narrativa:

**Como** usuario,  
**quiero** poder establecer un proceso de trabajo de mis Lead,  
**para** realizar su tratamiento correspondiente.

3.2.6.2 Criterios de Aceptación:

* Se deberá establecer el siguiente proceso de trabajo para los Leads \[Propuesta Procontacto\]:

  * Unassigned/Nuevo: El prospecto entra al sistema y queda pendiente de asignación al usuario responsable o se asigna directamente al usuario que cumple las reglas de asignación.

  * Contactado: El prospecto tuvo un primer contacto con el agente designado, ya sea por teléfono, mail, whatsapp u otro medio de comunicación. Durante esta etapa se completa el resto de la información necesaria para el cliente en el caso de que muestre interés.

  * Convertido/Descartado: El lead se convierte en oportunidad (si está listo para cotizar) o se descarta como no calificado.

* La transición entre etapas deberá ser automática cuando cumpla determinadas condiciones estipuladas en el proceso detallado arriba.

* Las restricciones entre las transiciones serán las representadas en el diagrama de estados.

(imagen omitida)

* Se deberá brindar una ayuda textual al usuario en cada etapa del proceso.

  * El texto de ayuda no deberá sobrepasar los 2000 caracteres.

  * El texto de ayuda no deberá variar entre tipos de registro.

* Se podrá adicionar acceso directo de cierta información en cada una de las etapas (campos clave). Esto con el fin de brindar mayor accesibilidad al usuario.

  * Se podrá agregar hasta cinco (5) campos clave.

* Se podrá establecer restricciones de transiciones entre estados. Dichas restricciones deberán realizarse según información (campos) almacenados dentro del registro. Pueden existir hasta cinco (5) campos como condicionante por estado.

  ### 3.2.7 Enviar para aprobación un Lead \[Presente Sow Original\] {#3.2.7-enviar-para-aprobación-un-lead-[presente-sow-original]}

  3.2.7.1 Narrativa:

  **Como** usuario,  
  **quiero** enviar una solicitud de aprobación de los Lead,  
  **para** validar la acción previo a continuar con el proceso de trabajo.

  3.2.7.2 Criterios de Aceptación:

* La solicitud de aprobación debe enviarse manualmente cuando el Lead cumpla ciertas condiciones:

  * Las condiciones para el envío de solicitud de aprobación de un Lead dependerá de la información completada. Dichas condiciones serán definidas en etapas posteriores.

  * El usuario dispondrá de un botón para realizar el envío de la solicitud.

* Se deberá poder redactar un comentario con respecto a la solicitud de aprobación, previo a su envío.

* Los aprobadores deben recibir una notificación para revisar y aceptar o rechazar la transformación.

* El estado de la solicitud debe ser registrado en el historial del Lead, con los detalles de la aprobación o rechazo.

* No se contempla modificar la lógica del flujo de aprobación ni los usuarios involucrados según los campos editados o la información específica que se desee aprobar.

* La solicitud de aprobación no debe dividirse ni redirigirse según la información editada del lead.

* No se deben contemplar envíos diferenciados de aprobación por campo individual ni combinaciones de campos.

* El sistema debe permitir el bloqueo del registro completo del lead al momento de enviar la solicitud de aprobación o al aprobarlo.

* No se debe contemplar el bloqueo parcial de campos o secciones individuales del registro.

* Mientras el registro esté bloqueado, no se debe permitir la edición de ningún campo del mismo.

  3.2.7.3 Consideraciones:

* Forma parte del alcance inicial, pero no se vio necesario en el relevamiento de Sprint 0\. 

  ### 3.2.8 Aprobar Leads \[Presente Sow Original\] {#3.2.8-aprobar-leads-[presente-sow-original]}

  3.2.8.1 Narrativa:

  **Como** usuario,  
  **quiero** poder aprobar un Lead,  
  **para** permitir su avance en el proceso de trabajo.

  3.2.8.2 Criterios de Aceptación:

* El sistema debe permitir a el o los usuarios involucrados con permisos adecuados, aprobar un Lead.

* El aprobador debe poder acceder a la ficha del registro en la solicitud de aprobación.

* Se deberá poder asociar opcionalmente un comentario con respecto a la aprobación, para informar al usuario solicitante sobre la decisión.

* Los usuarios quienes envían la solicitud de aprobación deben recibir una notificación si el Lead es aprobado.

* Se podrá considerar automatizaciones relacionadas a la actualización de campos dentro del lead aprobado.

* Se deberá dejar registro de la aprobación del lead a través de un historial.

  3.2.8.3 Consideraciones:

* Forma parte del alcance inicial, pero no se vio necesario en el relevamiento de Sprint 0\. 

  ### 3.2.9 Rechazar Leads \[Presente Sow Original\] {#3.2.9-rechazar-leads-[presente-sow-original]}

  3.2.9.1 Narrativa:

  **Como** usuario,  
  **quiero** poder rechazar un Lead,  
  **para** filtrar aquellos que no cumplen con los criterios.

  3.2.9.2 Criterios de Aceptación:

* El sistema debe permitir a los usuarios con permisos adecuados rechazar el lead. 

* El usuario que brinda el veredicto debe poder acceder a la ficha del registro en la solicitud de aprobación.

* Se deberá poder asociar opcionalmente un comentario con respecto al rechazo, para informar al usuario solicitante sobre la decisión.

* Los usuarios quienes envían la solicitud de aprobación deben recibir una notificación si el Lead es rechazado.

* El usuario tendrá la disponibilidad de volver a enviar la solicitud de aprobación.

* Se podrá considerar automatizaciones relacionadas a la actualización de campos dentro del lead rechazado.

* Se deberá dejar registro del rechazo del lead a través de un historial.

  3.2.9.3 Consideraciones:

* Forma parte del alcance inicial, pero no se vio necesario en el relevamiento de Sprint 0\. 

  ### 3.2.10 Migración de campos del objeto Lead a Cuenta, Contacto y Oportunidad {#3.2.10-migración-de-campos-del-objeto-lead-a-cuenta,-contacto-y-oportunidad}

  3.2.10.1 Narrativa:

  **Como** usuario,  
  **quiero** migrar los campos del objeto Lead a Cuenta, Contacto y Oportunidad durante la conversión,  
  **para** conservar la información completa del prospecto en los objetos correspondientes.

  3.2.10.2 Criterios de Aceptación:

* El sistema debe mapear cada campo del Lead a su campo destino en Cuenta, Contacto u Oportunidad, según su información definida.

* La migración debe ejecutarse automáticamente al presionar Convertir y transferir valores sin pérdida ni truncado de información.

* Si algún campo obligatorio en el objeto destino carece de valor, el sistema debe impedir la conversión y mostrar los campos faltantes al usuario.

* Los registros creados (Cuenta, Contacto y Oportunidad) deben vincularse entre sí.

* Al convertir el lead, el sistema crea automáticamente **una Oportunidad de tipo Vehículo por cada vehículo de interés** registrado en el lead. Todas quedan vinculadas a la misma cuenta y contacto generados en la conversión. 

* Una vez convertido, el registro de Lead debe quedar archivado y no visible dentro de la plataforma de Salesforce.

  ### 3.2.11 Detectar Leads duplicados {#3.2.11-detectar-leads-duplicados}

  3.2.11.1 Narrativa:

  **Como** ejecutivo de ventas,  
  **quiero** que el sistema detecte automáticamente leads potencialmente duplicados,  
  **para** evitar la creación de registros redundantes.

  3.2.11.2 Criterios de Aceptación:

* El sistema debe identificar leads potencialmente duplicados en función de la información clave del mismo (Teléfono, Email, DNI).

* Dichos criterios podrán ser tomados individualmente.

* La detección de los duplicados se realizará únicamente a través de campos almacenados en el lead de tipo “Texto” o “Número”.

* Al detectar un duplicado a la hora de realizar la creación de un Lead, el sistema restringirá al usuario de realizar dicha acción, mostrando un mensaje de error y adjuntando el Lead con el cuál existen incongruencias.  

* En caso de detectar un duplicado por fuera de la creación de un prospecto o candidato, se deberá visualizar un mensaje en la ficha del cliente sobre si el mismo es potencialmente duplicado o no.

* La detección de un duplicado únicamente aplicará cuando el lead esté siendo convertido a una cuenta, se esté creando un lead ya generado previamente, o se esté creando un lead ya almacenado como cliente. 

  ### 3.2.12 Enviar notificación vía Salesforce cuando se genera el Lead {#3.2.12-enviar-notificación-vía-salesforce-cuando-se-genera-el-lead}

  3.2.12.1 Narrativa:

  **Como** usuario,  
  **quiero** recibir una notificación ante un evento definido,  
  **para** estar informado y tomar acciones según corresponda.

  3.2.12.2 Criterios de Aceptación:

* A la hora de cumplirse una condición definida, se deberá generar automáticamente una alerta interna.

  * Cuando se crea un nuevo Lead en estado Unassigned o Nuevo se debe disparar la notificación o cuando hay un cambio de dueño del registro.

* Los destinatarios de la alerta serán las personas encargadas de controlar ese registro.

* La alerta deberá mostrarse a través de la funcionalidad de “Notificaciones” de Salesforce.

* El texto de la alerta debe seguir el siguiente formato:

  * “\[Nombre del propietario\] \[acción\]”

  * El \[Nombre del propietario\] debe ser dinámico y reflejar el nombre del usuario destinatario.

  * La \[acción\] será un texto sobre la descripción de dicha alerta. \[Propuesta de ProContacto\]:  
    “Un nuevo lead necesita tu atención \<Nombre del lead con url al mismo\>”

* A la hora de accionar sobre la notificación, la misma deberá redirigir al registro el cuál la generó.

* El usuario debe poseer acceso a la plataforma de Salesforce para visualizar la notificación.

  ### 3.2.13 Seguimiento y agendamiento de actividades con Leads {#3.2.13-seguimiento-y-agendamiento-de-actividades-con-leads}

  3.2.13.1 Narrativa:

  **Como** ejecutivo de ventas,  
  **quiero** registrar llamadas, tareas y citas con un lead  
  **para** poder dar seguimiento eficiente hasta la conversión.

  3.2.13.2 Criterios de Aceptación:

* Las actividades deben registrarse como Tasks o Events asociadas al Lead

* Salesforce debe mostrar en el panel de actividades: llamadas realizadas, próximas tareas, reuniones pendientes.

* Se debe permitir reprogramar, marcar como completada o delegar una tarea.

  ### 3.2.14 Generar formulario Web To Lead Estándar {#3.2.14-generar-formulario-web-to-lead-estándar}

  3.2.14.1 Narrativa:

  **Como** usuario del equipo de marketing,  
  **quiero** registrar automáticamente un Lead desde formularios web,  
  **para** gestionar prospectos generados por campañas digitales.

  3.2.14.2 Criterios de Aceptación:

* Se deberá establecer un formulario HTML para que un prospecto pueda completarlo. La información requerida en dicho formulario será:

  * Marca

  * Nombre y Apellido

  * Teléfono

  * Correo electrónico

  * Sucursal de preferencia

  * Vehículo de interés

  * Venta TRadicional o Venta por Plan de Ahorro

* Los campos del Web to Lead deberán coincidir con los campos obligatorios del candidato.

* Se debe establecer automáticamente los siguientes campos, según la información proporcionada de donde se encuentre el formulario:

  * Fuente

  * Campaña

  * Unidad de negocio

  * Solo se creará el fragmento de código, es responsabilidad del administrador del sitio introducir el código HTML al mismo.

  * El completado de la información relacionada a los campos UTM’s del formulario deberán ser asignados manualmente por el administrador del sitio web, a la hora de insertar el código HTML.

* El prospecto debe completar todos los campos obligatorios para poder enviar el formulario. Una vez enviado, la información deberá recepcionarse en salesforce a través de un nuevo prospecto.

* Se utiliza nomenclatura interna para identificar el origen de la campaña.

* A la hora de crearse dentro de la plataforma de Salesforce, la asignación se deberá realizar de manera automática.

**Límite de configuraciones**

| Elemento | Cantidad | Descripción |
| :---: | :---: | ----- |
| Compact Layout | 2 | Se configurará esa cantidad de Compact Layouts que son un resumen con los 5 campos más importantes de una entidad de información, utilizado habitualmente para visualizar rápidamente la información básica para operar. |
| Informe | 2 | Se configurará esa cantidad de Informes, los cuales son una representación tabular o gráfica de datos con filtros y cruces de datos, basada en requerimientos de áreas de la organización. |
| Pack de 5 Validation Rules | 2 | Se configurará esa cantidad de paquetes de reglas de validación, que es una regla con lógica de negocio que permite identificar inconsistencia en la forma de ingresar datos de una determinada entidad de información. Cada unidad es un paquete de 5 reglas de validación. |
| Pack de 20 Custom Fields | 2 | Se configurará esa cantidad de paquetes de custom fields, que son todos aquellos campos añadidos a objetos para adaptar el modelo de datos a las necesidades de la organización. |
| Pack de 1 Nodo de Flow | 2 | Se configurará esa cantidad de series acciones automatizadas que permite hacer más eficiente la ejecución de tareas. |
| Page Layout | 2 | Se configurará esa cantidad de layouts, que es un esquema de visualización de los datos y acciones de una entidad de información. |
| Record Type | 2 | Se configurará esa cantidad de Record Types, los cuales permiten determinar si para un determinado objeto puede haber variaciones en sus campos, procesos o formas de visualizarlo. |

## **3.3 Gestión de Cuenta Estándar** {#3.3-gestión-de-cuenta-estándar}

(imagen omitida)

### 3.3.1 Almacenar información de Cuentas {#3.3.1-almacenar-información-de-cuentas}

3.3.1.1 Narrativa:

**Como** usuario,  
**quiero** almacenar la información relacionada a mis cuentas,  
**para** posteriormente, realizar gestiones posteriores con ellas.

3.3.1.2 Criterios de Aceptación:

* Se deberá poder almacenar la información definida en el DDD asociada a una cuenta.

* Vehiculo de Interes

* Se deberá implementar la herramienta de Chatter a la hora de encontrarse dentro de la ficha de una cuenta.

* Se deberán incluir las siguientes validaciones con respecto a la información a almacenar:

  * Se deberán establecer los campos obligatorios para la gestión de una cuenta según el DDD.

  * Se establecerá qué información es obligatoria, dependiendo del estado en el cuál se encuentre la cuenta en base al DDD.

    ### 3.3.2 Crear cuentas manualmente en Salesforce {#3.3.2-crear-cuentas-manualmente-en-salesforce}

    3.3.2.1 Narrativa:

    **Como** usuario,  
    **quiero** crear una nueva cuenta ingresando información relevante de la misma,  
    **para** realizar un seguimiento adecuado y facilitar la gestión comercial.

    3.3.2.2 Criterios de Aceptación:

* La creación de las cuentas será de forma automática a través de la conversión de un Lead.

* Los campos obligatorios establecidos en la historia de usuario "Almacenar información de Cuentas" deberán ser completados para la creación.

* El usuario podrá completar los campos opcionales.

* Los usuarios deberán completar la información obligatoria.

* En el caso que exista al menos un campo obligatorio sin completar, no se podrá crear el registro.

* Se podrán generar N oportunidades asociadas a la misma cuenta, con la posibilidad de asignar un vendedor diferente en oportunidad, dependiendo del producto y la marca. 

  ### 3.3.3 Buscar y visualizar Cuentas existentes {#3.3.3-buscar-y-visualizar-cuentas-existentes}

  3.3.3.1 Narrativa:

  **Como** ejecutivo de ventas,  
  **quiero** buscar y visualizar los clientes existentes por distintos campos  
  **para** posteriormente, gestionarlos de manera efectiva.

  3.3.3.2 Criterios de Aceptación:

* La ficha del Cliente debe mostrar: contacto, origen, vehículo de interés, historial de comunicaciones, citas y documentos adjuntos.

  * Servicios realizados.

  * Vehículos comprados.

  * Oportunidades ganadas o perdidas.

  * Emails y citas asociadas.

  * Impacto de campañas de marketing.

  * Documentos Adjuntos.

* La información debe estar organizada por tipo y orden cronológico.

* Solo se podrá ver la información del Cliente del concesionario al que el ejecutivo está asignado, salvo perfiles administrativos.

* Los duplicados entre dealers deben ser visibles solo para perfiles con permisos avanzados.

* El ejecutivo podrá acceder a esta cuenta solo si tiene permisos sobre ese dealer.

  ### 3.3.4 Actualizar información de Cuentas {#3.3.4-actualizar-información-de-cuentas}

  3.3.4.1 Narrativa:

  **Como** usuario,  
  **quiero** modificar mis cuentas,  
  **para** mantener la información actualizada.

  3.3.4.2 Criterios de Aceptación:

* Los campos obligatorios establecidos en la historia de usuario "Almacenar información de Cuentas" deberán permanecer completados ante la modificación. Caso contrario, el sistema mostrará un mensaje de error.

* El usuario podrá modificar el contenido de los campos opcionales.

* Los usuarios deberán completar o mantener completada la información obligatoria.

* En el caso que exista al menos un campo obligatorio sin completar, no se podrá actualizar el registro.

* El campo Teléfono principal (en particular el número de WhatsApp validado) es de solo lectura para todos los perfiles de ejecutivos y supervisores. No puede ser modificado ni eliminado por el vendedor bajo ninguna circunstancia. Solo el Administrador de Salesforce puede modificarlo, con registro obligatorio de la razón.

* El campo Email principal puede ser modificado por usuarios con permisos, pero no puede ser eliminado (vaciado). Si se requiere actualizar el email, se sobrescribe el valor existente y el sistema registra el cambio en el historial de campo.

* Se habilitan campos secundarios "Teléfono alternativo" y "Email alternativo" para que el vendedor pueda registrar datos de contacto adicionales o actualizados, sin afectar los datos validados originales.

* Todo cambio realizado sobre los campos Teléfono principal, Email principal, DNI y Email alternativo debe quedar registrado en el historial de campo con: usuario que realizó el cambio, fecha y hora, valor anterior y valor nuevo.

* Cuando un usuario con permisos modifica un campo sensible (teléfono, email, DNI), el sistema debe solicitar de forma obligatoria el ingreso de una nota de justificación antes de guardar el cambio. Esta nota queda visible en el registro.

  ### 3.3.5 Enviar para aprobación una Cuenta \[Presente Sow Original\] {#3.3.5-enviar-para-aprobación-una-cuenta-[presente-sow-original]}

  3.3.5.1 Narrativa:

  **Como** usuario,  
  **quiero** enviar una solicitud de aprobación de las cuentas,  
  **para** validar la acción previo a continuar con el proceso de trabajo.

  3.3.5.2 Criterios de Aceptación:

* La solicitud de aprobación debe enviarse manualmente cuando la cuenta cumpla ciertas condiciones:

* Las condiciones para el envío de solicitud de aprobación de un Lead dependerá de la información completada. Dichas condiciones serán definidas en etapas posteriores.

* El usuario dispondrá de un botón para realizar el envío de la solicitud.

* Se deberá poder redactar un comentario con respecto a la solicitud de aprobación, previo a su envío.

* Los aprobadores deben recibir una notificación para revisar y aceptar o rechazar la transformación. 

* El estado de la solicitud debe ser registrado en el historial de la cuenta, con los detalles de la aprobación o rechazo.

* No se contempla modificar la lógica del flujo de aprobación ni los usuarios involucrados según los campos editados o la información específica que se desee aprobar.

* La solicitud de aprobación no debe dividirse ni redirigirse según la información editada de la cuenta.

* No se deben contemplar envíos diferenciados de aprobación por campo individual ni combinaciones de campos.

* El sistema debe permitir el bloqueo del registro completo del lead al momento de enviar la solicitud de aprobación o al aprobarlos.

* No se debe contemplar el bloqueo parcial de campos o secciones individuales del registro.

* Mientras el registro esté bloqueado, no se debe permitir la edición de ningún campo del mismo.

  3.3.5.3 Consideraciones:

* Forma parte del alcance inicial, pero no se vio necesario en el relevamiento de Sprint 0\. 

  ### 3.3.6 Aprobar Cuenta \[Presente Sow Original\] {#3.3.6-aprobar-cuenta-[presente-sow-original]}

  3.3.6.1 Narrativa:

  **Como** usuario,  
  **quiero** poder aprobar una cuenta,  
  **para** permitir su avance en el proceso de trabajo.

  3.3.6.2 Criterios de Aceptación:

* El sistema debe permitir a el o los usuarios involucrados con permisos adecuados, aprobar una cuenta.

* El aprobador debe poder acceder a la ficha del registro en la solicitud de aprobación.

* Se deberá poder asociar opcionalmente un comentario con respecto a la aprobación, para informar al usuario solicitante sobre la decisión.

* Los usuarios que envían la solicitud de aprobación deben recibir una notificación si la cuenta es aprobada.

* Se podrá considerar automatizaciones relacionadas a la actualización de campos dentro de la cuenta aprobada.

* Se deberá dejar registro de la aprobación de la cuenta a través de un historial.

  3.3.6.3 Consideraciones:

* Forma parte del alcance inicial, pero no se vio necesario en el relevamiento de Sprint 0\. 

  ### 3.3.7 Rechazar Cuenta \[Presente Sow Original\] {#3.3.7-rechazar-cuenta-[presente-sow-original]}

  3.3.7.1 Narrativa:

  **Como** usuario,  
  **quiero** poder rechazar una cuenta,  
  **para** filtrar aquellas que no cumplen con los criterios.

  3.3.7.2 Criterios de Aceptación:

* El sistema debe permitir a los usuarios con permisos adecuados rechazar la cuenta.

* El usuario que brinda el veredicto debe poder acceder a la ficha del registro en la solicitud de aprobación.

* Se deberá poder asociar opcionalmente un comentario con respecto al rechazo, para informar al usuario solicitante sobre la decisión.

* Los usuarios que envían la solicitud de aprobación deben recibir una notificación si la cuenta es rechazada.

* El usuario tendrá la disponibilidad de volver a enviar la solicitud de aprobación.

* Se podrá considerar automatizaciones relacionadas a la actualización de campos dentro de la cuenta rechazada.

* Se deberá dejar registro del rechazo de la cuenta a través de un historial.

  3.3.7.3 Consideraciones:

* Forma parte del alcance inicial, pero no se vio necesario en el relevamiento de Sprint 0\. 

  ### 3.3.8 Detectar Cuentas duplicadas {#3.3.8-detectar-cuentas-duplicadas}

  3.3.8.1 Narrativa:

  **Como** usuario,  
  **quiero** que el sistema detecte automáticamente cuentas potencialmente duplicadas,  
  **para** evitar la creación de registros redundantes.

  3.3.8.2 Criterios de Aceptación:

* El sistema debe identificar cuentas potencialmente duplicadas en función de la información clave de la misma:

* DNI, Email, Teléfono

* Dichos criterios podrán ser tomados individualmente.

* La detección de los duplicados se realizará únicamente a través de campos almacenados en el lead de tipo “Texto” o “Número”.

* Al detectar un duplicado a la hora de realizar la creación de una cuenta, el sistema restringirá al usuario de realizar dicha acción, mostrando un mensaje de error y adjuntando la cuenta con la cuál existen incongruencias.

* En caso de detectar un duplicado por fuera de la creación, se deberá visualizar un mensaje en la ficha de la cuenta sobre si la misma es potencialmente duplicada o no.

* La detección de un duplicado únicamente aplicará cuando la cuenta esté siendo creada.

  ### 3.3.9 Configurar y visualizar jerarquías de cuentas \[Presente Sow Original\] {#3.3.9-configurar-y-visualizar-jerarquías-de-cuentas-[presente-sow-original]}

  3.3.9.1 Narrativa:

  **Como** usuario,  
  **quiero** almacenar la relación jerárquica entre cuentas principales y secundarias,  
   **para** entender mejor la estructura organizacional de nuestros clientes y consolidar información a nivel grupo.

  3.3.9.2 Criterios de Aceptación:

* Se habilitará el campo estándar Parent Account (Cuenta principal) para establecer relaciones jerárquicas.

* Cada cuenta podrá tener asignada una cuenta principal (padre) y, opcionalmente, varias cuentas hijas.

* El sistema mostrará una vista jerárquica navegable que incluya nombres de cuentas, tipos, industrias y otros campos clave definidos.

* Se podrá acceder fácilmente desde la ficha de cualquier cuenta a la jerarquía completa de su grupo económico.

* No se permitirá que una cuenta se asocie como hija de sí misma ni que se generen bucles jerárquicos (una cuenta no puede ser su propio ancestro).

* Sólo usuarios con permisos adecuados podrán modificar la relación jerárquica.

  3.3.9.3 Consideraciones:

* Forma parte del alcance inicial, pero no se vio necesario en el relevamiento de Sprint 0\. 

  ### 3.3.10 Visualizar cantidad de vehículos adquiridos {#3.3.10-visualizar-cantidad-de-vehículos-adquiridos}

  3.3.10.1 Narrativa:

  **Como** ejecutivo de ventas,  
  **quiero** visualizar cuántos vehículos ha comprado el cliente,  
  **para** medir su nivel de fidelidad y diseñar ofertas de retención o upsell.

  3.3.10.2 Criterios de Aceptación:

* En la ficha del cliente debe mostrarse una lista relacionada del objeto Vehículo con la etiqueta “Vehículos Adquiridos”, donde se lista cada uno de ellos.

* Se puede generar un reporte en el que se debe incluir el modelo y año en un subpanel o gráfico de torta, el cual quedará vinculado a la cuenta por una lista relacionada.

* Si el cliente no ha adquirido ningún vehículo, la lista se mostrará vacía.

* El ejecutivo podrá seleccionar un vehículo en específico y visualizar su detalle correspondiente.

  ### 3.3.11 Visualizar campañas de marketing que alcanzó el cliente {#3.3.11-visualizar-campañas-de-marketing-que-alcanzó-el-cliente}

  3.3.11.1 Narrativa:

  **Como** ejecutivo de ventas, **quiero** visualizar las campañas de marketing a las que se ha expuesto o respondido el cliente, **para** personalizar mis comunicaciones con base en su participación.

  3.3.11.2 Criterios de Aceptación:

* En la ficha del cliente debe aparecer una lista relacionada del objeto Campañas con etiqueta “Campañas” con todas las campañas de Marketing Cloud on Core o Pardot en las que figura (mailable, responded, clics).

* Cada registro debe mostrar: Nombre de campaña, Fecha de envío, Estado de la respuesta (Abierto, Clic, No interactuó).

* Ofrecer filtros por periodo y por nivel de interacción.

* Al hacer clic en una campaña, el usuario debe ver un panel con métricas de esa campaña y la actividad concreta del cliente.

* Sólo ejecutivos de ventas y marketing podrán ver el detalle de interacción; otros perfiles solo verán la lista básica de campañas.

  ### 3.3.12 Visualizar oportunidades vigentes {#3.3.12-visualizar-oportunidades-vigentes}

  3.3.12.1 Narrativa:

  **Como** ejecutivo de ventas,

  **quiero** visualizar mis oportunidades abiertas con el cliente y recibir una alerta si ese cliente tiene gestiones activas en otras marcas,

  **para** priorizar seguimientos, evitar conflictos internos y coordinar con el equipo sin infringir permisos de privacidad. 

  3.3.12.2 Criterios de Aceptación:

* La ficha del cliente debe incluir una lista relacionada del objeto Oportunidades con la etiqueta “Oportunidades”, listando todas las oportunidades que el ejecutivo puede ver según sus permisos relacionadas al cliente.

* Cada oportunidad debe mostrar: Nombre, Monto, Etapa actual y Fecha de cierre estimada.

* Debe poderse ordenar por fecha de cierre y filtrar por etapa.

* Al hacer clic en una oportunidad, debe dirigirse a la vista detallada de la misma.

* En la ficha de la cuenta debe mostrarse un indicador visible que informe al ejecutivo si el cliente tiene oportunidades abiertas gestionadas por otras marcas dentro del grupo Montironi.

* El indicador muestra únicamente: cantidad de oportunidades abiertas en otras marcas y los nombres de esas marcas (ej. "2 oportunidades abiertas: Jeep, Peugeot"). No expone el nombre del vendedor, monto, detalles de negociación ni ningún dato adicional.

* Este indicador es de solo lectura y no permite navegar al detalle de esas oportunidades.

**Límite de configuraciones**

| Elemento | Cantidad | Descripción |
| :---: | :---: | ----- |
| Compact Layout | 2 | Se configurará esa cantidad de Compact Layouts que son un resumen con los 5 campos más importantes de una entidad de información, utilizado habitualmente para visualizar rápidamente la información básica para operar. |
| Informe | 2 | Se configurará esa cantidad de Informes, los cuales son una representación tabular o gráfica de datos con filtros y cruces de datos, basada en requerimientos de áreas de la organización. |
| Pack de 5 Validation Rules | 2 | Se configurará esa cantidad de paquetes de reglas de validación, que es una regla con lógica de negocio que permite identificar inconsistencia en la forma de ingresar datos de una determinada entidad de información. Cada unidad es un paquete de 5 reglas de validación. |
| Pack de 20 Custom Fields | 2 | Se configurará esa cantidad de paquetes de custom fields, que son todos aquellos campos añadidos a objetos para adaptar el modelo de datos a las necesidades de la organización. |
| Pack de 1 Nodo de Flow | 2 | Se configurará esa cantidad de series acciones automatizadas que permite hacer más eficiente la ejecución de tareas. |
| Page Layout | 2 | Se configurará esa cantidad de layouts, que es un esquema de visualización de los datos y acciones de una entidad de información. |
| Record Type | 2 | Se configurará esa cantidad de Record Types, los cuales permiten determinar si para un determinado objeto puede haber variaciones en sus campos, procesos o formas de visualizarlo. |

## **3.4 Gestión de Contactos Estándar** {#3.4-gestión-de-contactos-estándar}

(imagen omitida)

### 3.4.1 Almacenar información de Contactos {#3.4.1-almacenar-información-de-contactos}

3.4.1.1 Narrativa:

**Como** usuario,   
**quiero** almacenar la información relacionada a mis contactos,   
**para** posteriormente, realizar gestiones posteriores con ellos.

3.4.1.2 Criterios de Aceptación:

* Se deberá poder almacenar la siguiente información asociada a un contacto:

* En la ficha de un contacto en específico, se deberá visualizar los campos definidos en el DDD.

* Se deberá implementar la herramienta de Chatter a la hora de encontrarse dentro de la ficha de un contacto.

* Se deberán incluir las siguientes validaciones con respecto a la información a almacenar:

  * Se establecerá qué campos serán obligatorios para la gestión de un contacto en base al DDD.

  * Se establecerá qué información será obligatoria, dependiendo del estado en el cuál se encuentre el contacto en base al DDD.

    ### 3.4.2 Crear contactos manualmente en Salesforce {#3.4.2-crear-contactos-manualmente-en-salesforce}

    3.4.2.1 Narrativa:

    **Como**  ejecutivo de ventas,   
    **quiero** crear un nuevo contacto ingresando información relevante del mismo  
    **para** realizar un seguimiento adecuado y facilitar la gestión comercial.

    3.4.2.2 Criterios de Aceptación:

* La creación de los contactos será de forma manual.

* Los campos obligatorios establecidos en la historia de usuario "Almacenar información de Contactos" deberán ser completados para la creación.

* El usuario podrá completar los campos opcionales.

* Los usuarios deberán completar la información obligatoria.

* En el caso que exista al menos un campo obligatorio sin completar, no se podrá crear el registro.

  ### 3.4.3 Actualizar información de Contactos {#3.4.3-actualizar-información-de-contactos}

  3.4.3.1 Narrativa:

  **Como** usuario  
  **quiero** modificar mis contactos  
  **para** mantener la información actualizada.

  3.4.3.2 Criterios de Aceptación:

* Los campos obligatorios establecidos en la historia de usuario "Almacenar información de Contactos" deberán permanecer completados ante la modificación. Caso contrario, el sistema mostrará un mensaje de error.

* El usuario podrá modificar o borrar el contenido de los campos opcionales.

* Los usuarios deberán completar o mantener completada la información obligatoria.

* En el caso que exista al menos un campo obligatorio sin completar, no se podrá actualizar el registro.

* El campo Teléfono principal (número de WhatsApp validado) es de solo lectura para todos los perfiles de ejecutivos y supervisores. No puede ser modificado ni eliminado. Solo el Administrador de Salesforce puede intervenir, con justificación obligatoria.

* El campo Email principal puede ser modificado pero no eliminado. Si se actualiza, el sistema registra el cambio automáticamente en el historial de campo.

* Se habilitan campos secundarios "Teléfono alternativo" y "Email alternativo" para registrar datos adicionales sin pisar los validados.

* Todo cambio en Teléfono principal, Email principal, DNI y Email alternativo queda en historial de campo con: usuario, fecha/hora, valor anterior, valor nuevo.

* Cuando un usuario con permisos modifica un campo sensible, el sistema solicita de forma obligatoria una nota de justificación antes de guardar. La nota queda visible en el registro.

  ### 3.4.4 Buscar y visualizar Contactos existentes {#3.4.4-buscar-y-visualizar-contactos-existentes}

  3.4.4.1 Narrativa:

  **Como** ejecutivo de ventas,  
  **quiero** buscar y visualizar los contactos existentes por distintos campos  
  **para** posteriormente, gestionarlos de manera efectiva.

  3.4.4.2 Criterios de Aceptación:

* La ficha del Contacto debe mostrar: contacto, origen, vehículo de interés, historial de comunicaciones, citas y documentos adjuntos.

  * Servicios realizados.

  * Vehículos asociados.

  * Oportunidades ganadas o perdidas.

  * Emails y citas asociadas.

  * Impacto de campañas de marketing.

  * Documentos Adjuntos

* La información debe estar organizada por tipo y orden cronológico.

* Solo se podrá ver la información del Contacto del concesionario al que el ejecutivo está asignado, salvo perfiles administrativos.

* Los duplicados entre dealers deben ser visibles solo para perfiles con permisos avanzados.

* El ejecutivo podrá acceder a este contacto solo si tiene permisos sobre ese dealer.

  ### 3.4.5 Detectar Contactos duplicados {#3.4.5-detectar-contactos-duplicados}

  3.4.5.1 Narrativa:

  **Como** usuario,   
  **quiero** que el sistema detecte automáticamente contactos potencialmente duplicados,   
  **para** evitar la creación de registros redundantes.

  3.4.5.2 Criterios de Aceptación:

* El sistema debe identificar contactos potencialmente duplicados en función de la información clave del mismo:

  * DNI, Telefono o Email

* Dichos criterios podrán ser tomados individualmente.

* La detección de los duplicados se realizará únicamente a través de campos almacenados en el lead de tipo “Texto” o “Número”.

* Al detectar un duplicado a la hora de realizar la creación de un contacto, el sistema restringirá al usuario de realizar dicha acción, mostrando un mensaje de error y adjuntando el contacto con el cuál existen incongruencias.

* En caso de detectar un duplicado por fuera de la creación, se deberá visualizar un mensaje en la ficha del contacto sobre si el mismo es potencialmente duplicado o no.

  ### 3.4.6 Enviar un correo electrónico al contacto \[Presente SOW Original\] {#3.4.6-enviar-un-correo-electrónico-al-contacto-[presente-sow-original]}

  3.4.6.1 Narrativa:

  **Como** ejecutivo de ventas,  
  **quiero** poder enviar un email desde la ficha del contacto  
  **para** mantener una conversación con trazabilidad sin salir del CRM.

  3.4.6.2 Criterios de Aceptación:

* A la hora de cumplirse una condición definida, se deberá generar automáticamente una alerta mediante correo electrónico.

* La condición se encuentra pendiente de definición.

* La condición que dispare la notificación podrá estar relacionada con el completado o la modificación de un campo específico dentro del registro.

* La condición también podrá estar relacionada con la creación o actualización general del registro.

* Los destinatarios de la alerta deberán estar definidos según los criterios del proceso.

* Las respuestas del cliente deben almacenarse en el historial de la ficha

* El texto contenido dentro del correo electrónico deberá ser definido en etapas posteriores.

* Se contempla que dentro del cuerpo de dicho correo electrónico será de texto plano. No se incluirán imágenes, fuentes de letra alternativas, o firmas adjuntas. Se podrá realizar el adjunto de datos almacenados en la plataforma de Salesforce, tales como el número del caso, información de contacto, entre otros.

* El usuario remitente será el dueño del registro de SF.

* El disparo de estas notificaciones no realizará ningún tipo de modificación sobre alguna información contenida dentro del sistema de Salesforce.

  ### 3.4.7 Almacenar y relacionar contactos con sus cuentas {#3.4.7-almacenar-y-relacionar-contactos-con-sus-cuentas}

  3.4.7.1 Narrativa:

  **Como** asesor comercial,  
  **quiero** asociar cada contacto a la cuenta que corresponda dentro de la jerarquía  
  **para** identificar las personas clave de cada cliente, su rol en la relación comercial

  3.4.7.2 Criterios de Aceptación:

* Cada contacto deberá asociarse a una cuenta mediante el campo estándar Cuenta.

* Desde la vista de una cuenta, el usuario deberá poder acceder al listado de contactos relacionados, mostrando nombre, teléfono, correo y rol.

* Se deberá permitir asignar un rol del contacto (por ejemplo: decisor, comprador, conductor, garante) mediante un campo tipo picklist o usando Contact Roles en oportunidades.

* No se deberán crear relaciones personalizadas: se utilizarán las funcionalidades estándar de Contact–Account y Contact Roles.

**Límite de configuraciones**

| Elemento | Cantidad | Descripción |
| :---: | :---: | ----- |
| Compact Layout | 2 | Se configurará esa cantidad de Compact Layouts que son un resumen con los 5 campos más importantes de una entidad de información, utilizado habitualmente para visualizar rápidamente la información básica para operar. |
| Informe | 2 | Se configurará esa cantidad de Informes, los cuales son una representación tabular o gráfica de datos con filtros y cruces de datos, basada en requerimientos de áreas de la organización. |
| Pack de 5 Validation Rules | 2 | Se configurará esa cantidad de paquetes de reglas de validación, que es una regla con lógica de negocio que permite identificar inconsistencia en la forma de ingresar datos de una determinada entidad de información. Cada unidad es un paquete de 5 reglas de validación. |
| Pack de 20 Custom Fields | 2 | Se configurará esa cantidad de paquetes de custom fields, que son todos aquellos campos añadidos a objetos para adaptar el modelo de datos a las necesidades de la organización. |
| Pack de 1 Nodo de Flow | 2 | Se configurará esa cantidad de series acciones automatizadas que permite hacer más eficiente la ejecución de tareas. |
| Page Layout | 2 | Se configurará esa cantidad de layouts, que es un esquema de visualización de los datos y acciones de una entidad de información. |
| Record Type | 2 | Se configurará esa cantidad de Record Types, los cuales permiten determinar si para un determinado objeto puede haber variaciones en sus campos, procesos o formas de visualizarlo. |

## **3.5 Gestión de Vehículos Custom** {#3.5-gestión-de-vehículos-custom}

(imagen omitida)

### 3.5.1 Almacenar información de Vehículos {#3.5.1-almacenar-información-de-vehículos}

3.5.1.1 Narrativa:

**Como** asesor comercial de la concesionaria,  
**quiero**  registrar y consultar los vehículos asociados a cada cliente,  
**para** gestionar su historial, estado, propiedad y las operaciones relacionadas.

3.5.1.2 Criterios de Aceptación:

* Se deberá poder crear un registro de vehículo asociado a una cuenta o contacto mediante los campos estándar de Salesforce.

* Cada vehículo deberá incluir la información clave definida dentro de DDD.

* El usuario deberá poder visualizar los vehículos asociados desde la ficha del cliente (Cuenta o Contacto).

* El sistema deberá permitir registrar casos, órdenes de trabajo u oportunidades vinculadas al vehículo para mantener su trazabilidad.

* Se podrá registrar un historial de cambios de propietario o uso mediante campos de auditoría o registros relacionados.

* No se crearán objetos personalizados: se utilizará el objeto estándar Asset de Salesforce y sus relaciones nativas con Cuenta, Contacto, Caso y Oportunidad.

  ### 3.5.2 Asociar garantías al vehículo {#3.5.2-asociar-garantías-al-vehículo}

  3.5.2.1 Narrativa:

  Como agente de postventa,  
  quiero registrar las garantías activas del vehículo,  
  para saber si tiene cobertura vigente ante un reclamo o servicio.

  3.5.2.2 Criterios de Aceptación:

* Cada vehículo debe permitir asociar una o más garantías, con los siguientes campos:

  * Tipo de garantía (fábrica, extendida, motor, etc.)

  * Fecha de inicio y vencimiento

  * Coberturas incluida

  * Estado (vigente / expirada / cancelada)

* Debe validarse automáticamente si el vehículo tiene garantías activas al momento de registrar un servicio.

* La garantía debe estar relacionada con el dealer o entidad que la emitió.

  ### 3.5.3 Ver y registrar actividades relacionadas al vehículo {#3.5.3-ver-y-registrar-actividades-relacionadas-al-vehículo}

  3.5.3.1 Narrativa:

  Como ejecutivo de servicio o ventas,  
  quiero ver y registrar tareas, llamadas o citas relacionadas a un vehículo,  
  para coordinar mantenimientos, seguimientos o inspecciones.

  3.5.3.2 Criterios de Aceptación:

* Desde la ficha del vehículo se debe poder acceder al:

  * Ver el historial de actividades.

  * Registrar una nueva tarea o evento (ej. llamada al cliente, inspección técnica).

* Las actividades deben incluir:

  * Fecha y hora

  * Tipo de actividad

  * Responsable

  * Resultado 

  * Eventos de milestone

  * Cambios de propiedad

  * Servicios realizados

  * Oportunidades asociadas (si aplica)

    ### 3.5.4 Registrar y relacionar la definición técnica de un modelo con vehículos específicos {#3.5.4-registrar-y-relacionar-la-definición-técnica-de-un-modelo-con-vehículos-específicos}

    3.5.4.1 Narrativa:

    Como responsable de gestión de productos,

    **quiero** poder registrar la definición técnica de cada modelo de vehículo y relacionarla con las unidades físicas que llegan a nuestros concesionarios,

    **para** asegurar consistencia en la información técnica y operativa en todos los canales de venta y postventa.

    3.5.4.2 Criterios de Aceptación:

* Se podrá crear una ficha de modelo que contenga las especificaciones técnicas del vehículo definidas en el DDD.

* Cada vehículo físico (unidad real con VIN) podrá vincularse a una de estas definiciones, heredando automáticamente todos los datos técnicos del modelo.

* Esto permitirá que las unidades que compartan el mismo modelo están correctamente clasificadas, sin necesidad de repetir la información técnica en cada caso.

* Las unidades físicas podrán tener además información individual como número de serie, color, ubicación, kilometraje y estado (en stock, vendido, entregado, etc.).

* Se debe poder navegar desde el vehículo a la ficha de la cuenta, contacto o Household relacionado para ampliar la información.

  ### 3.5.5 Registrar y visualizar activos de cualquier tipo {#3.5.5-registrar-y-visualizar-activos-de-cualquier-tipo}

  3.5.5.1 Narrativa:

  Como usuario del sistema,

  **quiero** registrar información clave sobre activos como vehículos, piezas o accesorios,

  **para** poder identificar, rastrear y consultar cada unidad instalada, vendida o mantenida

  3.5.5.2 Criterios de Aceptación:

* Se podrán registrar activos con datos como nombre, número de serie, cantidad, precio unitario, fecha de compra o instalación.

* Cada activo estará relacionado con un cliente y un contacto asociado.

* Se podrán incluir jerarquías entre activos para representar piezas asociadas a un vehículo.

* El sistema mostrará una cronología de eventos relevantes como mantenimientos, garantías, órdenes de trabajo, reclamos, etc.

  ### 3.5.6 Creación automática de Opps al registrar un Vehículo

  3.5.6.1 Narrativa:

    
  Como usuario del sistema,

  **quiero** que al registrarse un nuevo Vehículo en el sistema, se creen automáticamente una Oportunidad de tipo Accesorio y una Oportunidad de tipo Seguro asociadas a la misma cuenta,

  **para** garantizar que ninguna oportunidad comercial derivada de la compra de un vehículo quede sin gestionar, sin depender de la carga manual del vendedor.

  3.5.6.2 Criterios de Aceptación:

* Cuando se crea un registro de tipo Vehículo en Salesforce (por integración desde DMS), el sistema debe generar automáticamente dos oportunidades asociadas a la misma cuenta:

  * Opp tipo Accesorio: puede contener uno o más accesorios. El vendedor no la crea manualmente.

  * Opp tipo Seguro: El vendedor no la crea manualmente.

* Esta lógica se implementa mediante un Flow disparado por la creación del objeto Vehículo.

* El sistema notifica internamente al vendedor asignado cuando las oportunidades son creadas.

* Si las oportunidades ya existen, el sistema no debe duplicarlas. Debe verificar si ya existen oportunidades abiertas del mismo tipo vinculadas a la misma cuenta y vehículo antes de crear nuevas.

  ### 3.5.7 Gestionar flujo de estados de entrega de vehículo 

  3.5.7.1 Narrativa:

    
  **Como** administrativo de ventas,  
  **quiero** gestionar los estados previos a la entrega del vehículo directamente en Salesforce (preparación, alistamiento, lavado),  
  **para** tener visibilidad en tiempo real del estado de cada unidad antes de la entrega al cliente, sin depender de planillas externas. 

  3.5.7.2 Criterios de Aceptación:

* Desde la ficha del objeto Vehículo (Asset) relacionado debe existir un camino de estados con los siguientes valores:

  * Preparación

  * Alistamiento / Equipamiento de Accesorios

  * Lavado y Presentación

  * Entregado

* Cada estado tiene asociado un indicador visual de color (semáforo):

  * Preparación → 🔴 Rojo

  * Alistamiento → 🟡 Amarillo

  * Lavado y Presentación → 🟢 Verde

  * Entregado → ✅ Completado (sin color de alerta)

* El usuario encargado avanza los estados manualmente dentro de Salesforce. No existe avance automático entre estos estados.

* Solo usuarios con el perfil autorizado (Administrativo de Ventas, Logística o Administrador) pueden cambiar el Estado de Entrega.

* Cada cambio de estado queda registrado en el historial con: usuario, fecha y hora del cambio.

* El estado de entrega es visible desde la ficha de la oportunidad para el vendedor y el supervisor, en modo solo lectura.

* El estado "Entregado" activa la automatización de tareas post-entrega definida en la HU 3.5.8.

  ### 3.5.8 Automatización post-entrega de vehículo 

  3.5.8.1 Narrativa:

    
  **Como** supervisor comercial,  
  **quiero** que al registrarse la entrega de un vehículo en el sistema, se dispare automáticamente un email de bienvenida al cliente y una tarea de llamada para el Contact Center,  
  **para** asegurar que el 100% de las entregas tenga seguimiento postventa sin depender de la memoria o iniciativa del vendedor.

  3.5.8.2 Criterios de Aceptación:

* Cuando el estado del Vehículo pasa a "Entregado", el sistema dispara automáticamente las siguientes acciones:

  * Email de bienvenida al cliente:

    * El sistema envía un email automático al email registrado en la cuenta/contacto vinculado a la oportunidad.

    * El contenido del email se basa en una plantilla predefinida (template a diseñar en fases posteriores con el equipo de Montironi).

    * Si el cliente no tiene email registrado, el sistema crea una tarea interna para el vendedor informando que el email de bienvenida no pudo enviarse.

    * El envío del email queda registrado en el timeline de actividades de la oportunidad.

  * Tarea de llamada de bienvenida para el Contact Center:

    * El sistema crea automáticamente una tarea de tipo "Llamada de Bienvenida" asignada al agente responsable.

    * La tarea incluye: nombre del cliente, datos de contacto, vehículo entregado.

    * La tarea tiene una fecha de vencimiento de 5 días corridos a partir de la fecha de entrega (configurable por el administrador de Salesforce).

* El vendedor y el supervisor reciben una notificación interna de Salesforce confirmando que ambas acciones (email y tarea) fueron disparadas correctamente.

**Límite de configuraciones**

| Elemento | Cantidad | Descripción |
| :---: | :---: | ----- |
| Compact Layout | 2.00 | Se configurará esa cantidad de Compact Layouts que son un resumen con los 5 campos más importantes de una entidad de información, utilizado habitualmente para visualizar rápidamente la información básica para operar. |
| Informe | 2.00 | Se configurará esa cantidad de Informes, los cuales son una representación tabular o gráfica de datos con filtros y cruces de datos, basada en requerimientos de áreas de la organización. |
| Pack de 5 Validation Rules | 2.00 | Se configurará esa cantidad de paquetes de reglas de validación, que es una regla con lógica de negocio que permite identificar inconsistencia en la forma de ingresar datos de una determinada entidad de información. Cada unidad es un paquete de 5 reglas de validación. |
| Pack de 20 Custom Fields | 2.00 | Se configurará esa cantidad de paquetes de custom fields, que son todos aquellos campos añadidos a objetos para adaptar el modelo de datos a las necesidades de la organización. |
| Pack de 1 Nodo de Flow | 2.00 | Se configurará esa cantidad de series acciones automatizadas que permite hacer más eficiente la ejecución de tareas. |
| Page Layout | 2.00 | Se configurará esa cantidad de layouts, que es un esquema de visualización de los datos y acciones de una entidad de información. |
| Record Type | 2.00 | Se configurará esa cantidad de Record Types, los cuales permiten determinar si para un determinado objeto puede haber variaciones en sus campos, procesos o formas de visualizarlo. |

## **3.6 Gestión de Oportunidades Estándar** {#3.6-gestión-de-oportunidades-estándar}

(imagen omitida)

### 3.6.1 Almacenar información de Oportunidades {#3.6.1-almacenar-información-de-oportunidades}

3.6.1.1 Narrativa:

**Como** usuario,  
**quiero** registrar información relevante en la oportunidad,  
**para** que el proceso comercial sea estructurado y trazable.

3.6.1.2 Criterios de Aceptación:

* Se deberá poder almacenar la información definida en el DDD asociada a una oportunidad.

* La información básica y obligatoria deberá ser completada para la creación.

* El usuario podrá completar campos opcionales según corresponda.

* Se deberá implementar la herramienta de Chatter a la hora de encontrarse dentro de la ficha de una oportunidad.

* Se deberán incluir las siguientes validaciones con respecto a la información a almacenar:

  * Se establecerá qué campos serán obligatorios para la gestión de una oportunidad según el DDD.

  * Se establecerá qué información será obligatoria, dependiendo del estado en el cuál se encuentre la oportunidad según el DDD.

* El campo que vincula el **vehículo de interés** a la oportunidad es de **solo lectura** una vez que la oportunidad es guardada por primera vez. El vendedor no puede modificarlo posteriormente.

* Si el cliente cambia de interés de vehículo, se debe crear una nueva oportunidad. El sistema puede ofrecer un botón de "Clonar oportunidad con nuevo vehículo" para facilitar este flujo

* Al crear una oportunidad, el sistema verifica si ya existe una oportunidad **abierta** (no cerrada) para el mismo cliente y el mismo vehículo de interés.

* Si existe, el sistema muestra una **advertencia** informando al usuario que ya hay una gestión activa para esa combinación. El sistema no bloquea la creación, sólo alerta.

* Si la oportunidad previa está cerrada (ganada o perdida), no se muestra la advertencia.

  ### 3.6.2 Crear oportunidades manualmente en Salesforce {#3.6.2-crear-oportunidades-manualmente-en-salesforce}

  3.6.2.1 Narrativa:

  **Como** ejecutivo de ventas,  
   **quiero** crear una nueva oportunidad ingresando información relevante,  
   **para** comenzar el proceso de venta formal del vehículo seleccionado

  3.6.2.2 Criterios de Aceptación:

* La creación de oportunidades será de forma manual.

* Los campos obligatorios definidos en la historia "Almacenar información de Oportunidades" deberán ser completados para la creación.

* El usuario podrá completar campos opcionales.

* Los usuarios deberán completar la información obligatoria.

* En el caso que exista al menos un campo obligatorio sin completar, no se podrá crear el registro.

* Se podrán generar N oportunidades asociadas a la misma cuenta, con la posibilidad de asignar un vendedor diferente en oportunidad, dependiendo del producto y la marca. 

* El campo de vehículo de interés puede completarse durante la creación. Una vez guardada la oportunidad, ese campo queda bloqueado para edición. 

* Antes de guardar, si el sistema detecta una oportunidad abierta para el mismo cliente y el mismo vehículo, muestra una advertencia en pantalla. El vendedor puede continuar igualmente si lo considera necesario (doble intención de compra) pero queda registrado el aviso. 

  ### 3.6.3 Actualizar información de oportunidad {#3.6.3-actualizar-información-de-oportunidad}

  3.6.3.1 Narrativa:

  **Como** usuario,  
  **quiero** modificar mis oportunidades,  
  **para** mantener la información actualizada.

  3.6.3.2 Criterios de Aceptación:

* Los campos obligatorios establecidos en la historia de usuario “Almacenar información de oportunidad” deberán permanecer completados ante la modificación. Caso contrario, el sistema mostrará un mensaje de error.

* El usuario podrá modificar o borrar el contenido de los campos opcionales.

* Los usuarios deberán completar o mantener completada la información obligatoria.

* En el caso que exista al menos un campo obligatorio sin completar, no se podrá actualizar el registro.

  ### 3.6.4 Asociar Pricebook a la oportunidad {#3.6.4-asociar-pricebook-a-la-oportunidad}

  3.6.4.1 Narrativa:

  **Como** usuario,  
  **quiero** asociar un Pricebook específico a la oportunidad,  
  **para** asegurar que los productos y precios sean adecuados para la venta.

  3.6.4.2 Criterios de Aceptación:

* Se debe habilitar la selección de un Pricebook al momento de crear o editar una oportunidad.

* Solo se podrán agregar productos a una oportunidad si previamente se ha seleccionado un Pricebook.

* El Pricebook seleccionado determinará los productos disponibles para agregar a la oportunidad.

* Una vez agregado un producto a la oportunidad, el Pricebook asociado ya no podrá modificarse, salvo que se eliminen todos los productos previamente agregados.

* El Pricebook a seleccionar deberá estar activo y visible para el perfil del usuario correspondiente.

* Si la organización maneja múltiples listas de precios (por región, canal u otro criterio), solo se deben mostrar los Pricebooks habilitados según la lógica de negocio establecida.

  ### 3.6.5 Agregar productos a la oportunidad {#3.6.5-agregar-productos-a-la-oportunidad}

  3.6.5.1 Narrativa:

  **Como** usuario,  
  **quiero** agregar productos desde el Pricebook asociado a la oportunidad,  
  **para** registrar los ítems que el cliente desea comprar con cantidades y precios correctos.

  3.6.5.2 Criterios de Aceptación:

* Solo se podrán agregar productos que pertenezcan al Pricebook asociado.

* El usuario podrá ingresar la cantidad de cada producto.

* El precio se obtendrá automáticamente del Pricebook y podrá modificarse su precio de venta.

* El sistema calculará el total automáticamente.

  ### 3.6.6 Actualizar productos en la oportunidad {#3.6.6-actualizar-productos-en-la-oportunidad}

  3.6.6.1 Narrativa:

  **Como** usuario,  
  **quiero** modificar cantidades o precios de productos en la oportunidad,  
  **para** mantener la información actualizada según negociaciones.

  3.6.6.2 Criterios de Aceptación:

* Se debe permitir modificar la cantidad, precio y descuento de los productos previamente agregados a la oportunidad, siempre que la oportunidad no esté en estado cerrado.

* Se debe poder agregar nuevos productos a la oportunidad, siempre que esta tenga un Pricebook previamente asociado.

* Se debe poder eliminar productos existentes de la oportunidad.

* El sistema recalculará totales después de cada cambio.

  ### 3.6.7 Enviar para aprobación una Oportunidad \[Presente Sow Original\] {#3.6.7-enviar-para-aprobación-una-oportunidad-[presente-sow-original]}

  3.6.7.1 Narrativa:

  **Como** usuario,  
   **quiero** enviar una solicitud de aprobación de las oportunidades,  
   **para** validar la acción previo a continuar con el proceso de trabajo.

  3.6.7.2 Criterios de Aceptación:

* La solicitud de aprobación debe enviarse manualmente cuando la oportunidad cumpla ciertas condiciones:

* Las condiciones para el envío de solicitud de aprobación de una oportunidad dependerá de la información completada. Dichas condiciones serán definidas en etapas posteriores.

* El usuario dispondrá de un botón para realizar el envío de la solicitud.

* Se deberá poder redactar un comentario con respecto a la solicitud de aprobación, previo a su envío.

* Los aprobadores deben recibir una notificación para revisar y aceptar o rechazar la transformación.

* El estado de la solicitud debe ser registrado en el historial de la oportunidad, con los detalles de la aprobación o rechazo.

* No se contempla modificar la lógica del flujo de aprobación ni los usuarios involucrados según los campos editados o la información específica que se desee aprobar.

* La solicitud de aprobación no debe dividirse ni redirigirse según la información editada de la oportunidad.

* No se deben contemplar envíos diferenciados de aprobación por campo individual ni combinaciones de campos.

* El sistema debe permitir el bloqueo del registro completo de la oportunidad al momento de enviar la solicitud de aprobación o al aprobarlo.

* No se debe contemplar el bloqueo parcial de campos o secciones individuales del registro.

* Mientras el registro está bloqueado, no se debe permitir la edición de ningún campo del mismo.

  ### 3.6.8 Aprobar oportunidad \[Presente Sow Original\] {#3.6.8-aprobar-oportunidad-[presente-sow-original]}

  3.6.8.1 Narrativa:

  **Como** usuario,  
  **quiero** poder aprobar una oportunidad,  
  **para** permitir su avance en el proceso de trabajo.

  3.6.8.2 Criterios de Aceptación:

* El sistema debe permitir a los usuarios con permisos adecuados aprobar una oportunidad.

* El aprobador debe poder acceder a la ficha de la oportunidad en la solicitud de aprobación.

* Se deberá poder asociar opcionalmente un comentario con respecto a la aprobación, para informar al usuario solicitante sobre la decisión.

* Los usuarios que envían la solicitud de aprobación deben recibir una notificación si la oportunidad es aprobada.

* Se podrá considerar automatizaciones relacionadas a la actualización de campos dentro de la oportunidad aprobada.

* Se deberá dejar registro de la aprobación de la oportunidad a través de un historial.

  ### 3.6.9 Rechazar oportunidad \[Presente Sow Original\] {#3.6.9-rechazar-oportunidad-[presente-sow-original]}

  3.6.9.1 Narrativa:

  **Como** usuario,  
  **quiero** poder rechazar una oportunidad,  
  **para** filtrar aquellas que no cumplen con los criterios.

  3.6.9.2 Criterios de Aceptación:

* El sistema debe permitir a los usuarios con permisos adecuados rechazar una oportunidad.

* El usuario que brinda el veredicto debe poder acceder a la ficha del registro en la solicitud de aprobación.

* Se deberá poder asociar opcionalmente un comentario con respecto al rechazo, para informar al usuario solicitante sobre la decisión.

* Los usuarios que envían la solicitud de aprobación deben recibir una notificación si la oportunidad es rechazada.

* El usuario tendrá la disponibilidad de volver a enviar la solicitud de aprobación.

* Se podrá considerar automatizaciones relacionadas a la actualización de campos dentro de la oportunidad rechazada.

* Se deberá dejar registro del rechazo a través de un historial.

  ### 3.6.10 Establecer proceso de trabajo de una oportunidad {#3.6.10-establecer-proceso-de-trabajo-de-una-oportunidad}

  3.6.10.1 Narrativa:

  **Como** ejecutivo de ventas,  
  **quiero** poder establecer un proceso de trabajo de mis oportunidades,  
  **para** reflejar correctamente el estado de la venta y facilitar la gestión.

  3.6.10.2 Criterios de Aceptación:

* Se deberá establecer el siguiente proceso de trabajo para las oportunidades \[Propuesta de Procontacto\]:

  * Nueva: Cuando se crea una nueva oportunidad

  * Definición: Cuando se encuentra completando los datos de la misma como tipo de oportunidad (Venta tradicional o plan de ahorro), Tipo de plan, toma de usados, etc.

  * Negociación: Cuando se encuentra la oportunidad con cotizaciones asociadas pero sin ser ninguna aprobada.

  * Cotizada: Cuando se encuentra la oportunidad con una cotización asociada.

  * Cerrada Ganada/Cerrada perdida: Cuando la oportunidad ya queda definida y se debe crear el objeto asociado o cuando la oportunidad no se sigue avanzando, debiendo dejar un comentario de porque se perdió.

* La transición entre etapas deberá ser manual.

* Las restricciones entre las transiciones serán las representadas en el diagrama de estados.

(imagen omitida)

* Se deberá brindar una ayuda textual al usuario en cada etapa del proceso.

* Se podrá adicionar acceso directo de cierta información en cada una de las etapas (campos clave). Esto con el fin de brindar mayor accesibilidad al usuario.

* Se podrá agregar hasta cinco (5) campos clave.

* Se podrá establecer restricciones de transiciones entre estados. Dichas restricciones deberán realizarse según información (campos) almacenados dentro del registro. Pueden existir hasta cinco (5) campos como condicionante por estado.

* El sistema debe registrar la fecha de cambio de etapa y el usuario que realizó la acción.

  ### 3.6.11 Visualizador de vehículos, formas de pago y financiamiento {#3.6.11-visualizador-de-vehículos,-formas-de-pago-y-financiamiento}

  3.6.11.1 Narrativa:

  **Como** ejecutivo de ventas**, quiero** registrar en la oportunidad la forma de pago y el plan de financiamiento seleccionado por el cliente**, para** documentar las condiciones comerciales acordadas y dejar trazabilidad de la operación. 

  3.6.11.2 Criterios de Aceptación:

* La oportunidad debe incluir un campo lookup al Modelo para vincular la unidad de interés del cliente.

* La oportunidad debe incluir un campo picklist **"Forma de Pago"** con las opciones vigentes según el tipo de venta (Tradicional / Plan de Ahorro).

* La oportunidad debe incluir un campo lookup o objeto relacionado **"Plan de Financiamiento"** que permita seleccionar un plan activo y vigente. El plan seleccionado debe mostrar los siguientes atributos asociados como campos de solo lectura: cuotas, plazo, tasa estimada, bonificaciones, pago inicial y costo total.

* Solo se deben mostrar planes de financiamiento activos, filtrados por marca, modelo y vigencia.

* Los campos son completados manualmente por el vendedor durante el proceso comercial.

  ### 3.6.12 Registro de Vehículo Usado en Venta directa {#3.6.12-registro-de-vehículo-usado-en-venta-directa}

  3.6.12.1 Narrativa:

  **Como** Vendedor,   
  **quiero** registrar los datos técnicos del vehículo usado que el cliente ofrece en parte de pago dentro de la misma Oportunidad de venta,   
  **para** iniciar el proceso de tasación sin tener que enviar mensajes infórmales al perito.

  3.6.12.2 Criterios de Aceptación:

* Creación del objeto personalizado "Tasación" (o Vehículo de Retoma) con relación principal a la Oportunidad.

* Configuración de los campos necesarios para la cotización:

  * Marca, Modelo, Versión.

  * Año de fabricación.

  * Kilometraje.

  * Color y Patente (Dominio).

  * Estado General (Bueno/Regular/Malo).

    ### 3.6.13 Carga de Evidencia Visual de Usado {#3.6.13-carga-de-evidencia-visual-de-usado}

    3.6.13.1 Narrativa:

    **Como** Vendedor,   
    **quiero** poder adjuntar fotografías del vehículo usado directamente desde mi celular o computadora al registro de la tasación,   
    **para** que el Gerente de Usados tenga evidencia visual del estado de la unidad antes de poner un precio.

    3.6.13.2 Criterios de Aceptación:

* Habilitación del componente estándar "Archivos" (Files) en el objeto de Tasación.

* Capacidad de subir múltiples archivos de imagen (Formatos: JPG, PNG).

* Instrucción de uso (Capacitación): Se definirá un estándar de 4 fotos mínimas (Frente, Trasera, Interior, Motor).

  ### 3.6.14 Aprobación y Fijación de Precio de Usado {#3.6.14-aprobación-y-fijación-de-precio-de-usado}

  3.6.14.1 Narrativa:

  **Como** Gerente de Usados,   
  **quiero** recibir una notificación cuando hay un vehículo para tasar, revisar las fotos y datos, y establecer el "Precio de Toma Aprobado" en el sistema,   
  **para** formalizar la oferta al cliente.

  3.6.14.2 Criterios de Aceptación:

* Configuración de un Proceso de Aprobación simple o Flujo de Notificación:

  * Al crear la Tasación, se notifica al Gerente de Usados.

  * Permisos de Campo: El campo "Precio de Toma Aprobado" debe ser editable únicamente por el perfil de Gerente de Usados (Read-only para vendedores).

  * Estados de la Tasación: "Borrador", "En Revisión", "Tasado/Aprobado", "Rechazado".

    ### 3.6.15 Impacto en la Oportunidad (Económico) {#3.6.15-impacto-en-la-oportunidad-(económico)}

    3.6.15.1 Narrativa:

    **Como** Vendedor,   
    **quiero** que una vez aprobado el precio del usado, este monto se sume automáticamente a los fondos de la Oportunidad,   
    **para** calcular el saldo restante que debe pagar el cliente.

    3.6.15.2 Criterios de Aceptación:

* Automatización (Flow): 

  * Cuando la Tasación pasa a estado "Aprobado", el valor del campo "Precio de Toma Aprobado" se copia automáticamente al campo "Monto Usado" en la Oportunidad padre.

* Recálculo: El sistema actualiza el campo de fórmula "Saldo a Pagar" (Precio Venta \- Seña \- Monto Usado).

  ### 3.6.16 Agendar pruebas de manejo de la Oportunidad {#3.6.16-agendar-pruebas-de-manejo-de-la-oportunidad}

  3.6.16.1 Narrativa:

  **Como** ejecutivo de ventas,  
  **quiero** agendar pruebas de manejo para una Oportunidad,  
  **para** brindarle una experiencia directa con el vehículo y aumentar la probabilidad de cierre.

  3.6.16.2 Criterios de Aceptación:

* Desde la ficha de la Oportunidad deben existir el objeto relacionado “Prueba de Manejo”

* El sistema debe validar que la franja horaria y el vehículo estén disponibles consultando el calendario de flota de pruebas.

  ### 3.6.17 Asignación automática de Oportunidades

  3.6.17.1 Narrativa:

  **Como** administrador de ventas**, quiero** que el sistema asigne automáticamente al vendedor correcto según el tipo de venta, sucursal de preferencia y marca**, para** asegurar que cada oportunidad llegue al asesor con el perfil adecuado sin intervención manual.

  3.6.17.2 Criterios de Aceptación:

* El sistema debe evaluar los siguientes campos de la oportunidad para determinar el equipo destino:

  * Tipo de venta (Venta Tradicional / Venta de Planes).

  * Sucursal de preferencia.

  * Marca.

* En base a esa combinación, el sistema identifica la cola de vendedores que corresponde y asigna la oportunidad al vendedor disponible según modalidad round-robin secuencial 1 a 1 dentro de ese equipo.

* Si la combinación de tipo de venta, sucursal y marca no coincide con ningún equipo configurado, la oportunidad debe quedar asignada a una cola de respaldo predefinida con estado visible para el supervisor, quien la reasignará manualmente.

* El sistema debe generar una alerta interna al supervisor cuando una oportunidad queda sin asignación por falta de coincidencia de regla.

* El sistema debe registrar en el historial de la oportunidad: el equipo al que fue derivada, el vendedor asignado, y la fecha y hora de la asignación automática. 

* Si el tipo de venta fue modificado por el asesor durante la calificación del lead (respecto al valor original de ingreso), ese cambio debe ser trazable en el historial del lead relacionado para análisis de conversión por canal. 

* Si la oportunidad no avanza, el vendedor debe cambiar el estado a "Cerrada Perdida" y completar obligatoriamente el campo "Motivo de pérdida" para poder guardar el cambio de estado. 

**Límite de configuraciones**

| Elemento | Cantidad | Descripción |
| :---: | :---: | ----- |
| Compact Layout | 2.00 | Se configurará esa cantidad de Compact Layouts que son un resumen con los 5 campos más importantes de una entidad de información, utilizado habitualmente para visualizar rápidamente la información básica para operar. |
| Informe | 2.00 | Se configurará esa cantidad de Informes, los cuales son una representación tabular o gráfica de datos con filtros y cruces de datos, basada en requerimientos de áreas de la organización. |
| Pack de 5 Validation Rules | 2.00 | Se configurará esa cantidad de paquetes de reglas de validación, que es una regla con lógica de negocio que permite identificar inconsistencia en la forma de ingresar datos de una determinada entidad de información. Cada unidad es un paquete de 5 reglas de validación. |
| Pack de 20 Custom Fields | 2.00 | Se configurará esa cantidad de paquetes de custom fields, que son todos aquellos campos añadidos a objetos para adaptar el modelo de datos a las necesidades de la organización. |
| Pack de 1 Nodo de Flow | 2.00 | Se configurará esa cantidad de series acciones automatizadas que permite hacer más eficiente la ejecución de tareas. |
| Page Layout | 2.00 | Se configurará esa cantidad de layouts, que es un esquema de visualización de los datos y acciones de una entidad de información. |
| Record Type | 2.00 | Se configurará esa cantidad de Record Types, los cuales permiten determinar si para un determinado objeto puede haber variaciones en sus campos, procesos o formas de visualizarlo. |

## **3.7 Gestión de Cotizaciones Estándar** {#3.7-gestión-de-cotizaciones-estándar}

(imagen omitida)

### 3.7.1 Almacenar información de Cotizaciones {#3.7.1-almacenar-información-de-cotizaciones}

3.7.1.1 Narrativa:

**Como** usuario,  
**quiero** registrar la información relevante en una cotización para las ventas,  
**para** que el proceso comercial sea estructurado y trazable.

3.7.1.2 Criterios de Aceptación:

* Se deberá poder almacenar la información definida en el DDD asociada a una cotización.

* La información básica y obligatoria deberá ser completada para la creación.

* El usuario podrá completar campos opcionales según corresponda.

* Se deberá implementar la herramienta de Chatter a la hora de encontrarse dentro de la ficha de una cotización.

* Se deberán incluir las siguientes validaciones con respecto a la información a almacenar:

  * Se establecerán qué campos serán obligatorios para la gestión de una cotización según el DDD.

  * Se establecerá qué información será obligatoria, dependiendo del estado en el cuál se encuentre la cotización según el DDD.

    ### 3.7.2 Crear cotizaciones manualmente en Salesforce {#3.7.2-crear-cotizaciones-manualmente-en-salesforce}

    3.7.2.1 Narrativa:

    **Como** ejecutivo de ventas,  
    **quiero** poder generar una cotización  desde una oportunidad existente,  
    **para** formalizar propuestas comerciales con clientes.

    3.7.2.2 Criterios de Aceptación:

* La creación de cotizaciones será manual desde la ficha de la oportunidad. 

* La generación de una cotización se realizará una vez el cliente muestre interés en base a una unidad específica.

* La cotización debe incluir marca, modelo, versión, precio sugerido.

* Se debe seleccionar el producto asociado a la cotización.

* Los campos obligatorios definidos en la historia "Almacenar información de Cotizaciones" deberán ser completados para la creación.

* Se debe usar una única lista de precios para todos los dealers según marca, modelo y año.

* El usuario podrá completar campos opcionales.

* Los usuarios deberán completar la información obligatoria. En el caso que exista al menos un campo obligatorio sin completar, no se podrá crear el registro.

* La cotización debe estar asociada al ejecutivo responsable y permitir añadir colaboradores.

  ### 3.7.3 Actualizar información de cotización {#3.7.3-actualizar-información-de-cotización}

  3.7.3.1 Narrativa:

  **Como** usuario,  
  **quiero** modificar mis cotizaciones ,  
  **para** mantener la información actualizada.

  3.7.3.2 Criterios de Aceptación:

* Los campos obligatorios establecidos en la historia de usuario “Almacenar información de Cotizaciones ” deberán permanecer completados ante la modificación. Caso contrario, el sistema mostrará un mensaje de error.

* El usuario podrá modificar o borrar el contenido de los campos opcionales.

* Los usuarios deberán completar o mantener completada la información obligatoria.

* En el caso que exista al menos un campo obligatorio sin completar, no se podrá actualizar el registro.

* Cuando el vendedor cambia el estado de una cotización a **"Aprobada"**, el sistema debe actualizar automáticamente el campo **"Tipo de Plan"** en la oportunidad padre con el valor correspondiente registrado en esa cotización. 

  ### 3.7.4 Establecer proceso de trabajo de una cotización {#3.7.4-establecer-proceso-de-trabajo-de-una-cotización}

  3.7.4.1 Narrativa:

  **Como** usuario,  
  **quiero** poder establecer un proceso de trabajo de mis cotizaciones ,  
  **para** realizar su tratamiento correspondiente.

  3.7.4.2 Criterios de Aceptación:

* Se deberá establecer el siguiente proceso de trabajo para las cotizaciones \[Propuesta de ProContacto\]:

* Propuesta de Cotización: Se prepara la cotización inicial con precios, promociones y posibles valores de retoma.  

* Cotización enviada: Se comparte la cotización con el cliente para su revisión.  

* Negociación: Se ajustan plazos, montos, retoma y otros detalles según el feedback del cliente. 

* Pendiente aprobación: Este estado solo se debe pasar en situaciones que dentro de la cotización se esté tomando a un usado como parte de pago, el mismo debe ser aprobado por juan antes de dejarle avanzar a cerrar la cotización. 

* Vendida (Closed Won): La operación se cierra exitosamente y queda marcada como “Sold”.  

* Perdida (Closed Lost): La venta no se concreta y se registra una razón de pérdida para análisis (Se puede llegar a este camino si no se aprueba la cotización por parte de Juan).  

* La transición entre etapas deberá ser automática.

* Las restricciones entre las transiciones serán las representadas en el diagrama de estados.

(imagen omitida)

* Se deberá brindar una ayuda textual al usuario en cada etapa del proceso.

* Se podrá adicionar acceso directo de cierta información en cada una de las etapas (campos clave). Esto con el fin de brindar mayor accesibilidad al usuario.

* Se podrá agregar hasta cinco (5) campos clave.

* Se podrá establecer restricciones de transiciones entre estados. Dichas restricciones deberán realizarse según información (campos) almacenados dentro del registro. Pueden existir hasta cinco (5) campos como condicionante por estado.

* Al cambiar el estado de la cotización a "Perdida (Closed Lost)", el sistema requiere que el vendedor complete obligatoriamente el campo "Motivo de pérdida" mediante una picklist predefinida. No se puede guardar el cambio de estado sin ese campo completado.

* Los valores de la picklist se definen en el DDD. Como propuesta inicial: Precio fuera de mercado, El cliente eligió otra marca, El cliente eligió otro vehículo, Sin respuesta del cliente, Financiamiento no aprobado, Otros.

* Este campo alimenta el reporte automático de motivos de cierre de cotizaciones para análisis de ventas.

  ### 3.7.5 Asociar productos a la cotización {#3.7.5-asociar-productos-a-la-cotización}

  3.7.5.1 Narrativa:

  **Como** usuario,  
   **quiero** agregar productos desde el Pricebook asociado a la cotización,  
   **para** reflejar con detalle la propuesta comercial al cliente.

  3.7.5.2 Criterios de Aceptación:

* Solo se podrán agregar productos que pertenezcan al Pricebook asociado a la oportunidad relacionada.

* El usuario podrá ingresar la cantidad de cada producto.

* El precio se obtendrá automáticamente del Pricebook y podrá modificarse su precio de venta.

* El sistema calculará el total automáticamente.

  ### 3.7.6 Actualizar productos en la cotización {#3.7.6-actualizar-productos-en-la-cotización}

  3.7.6.1 Narrativa:

  **Como** usuario,  
   **quiero** modificar cantidades o precios de productos en la cotización,  
   **para** mantener la información actualizada según negociaciones.

  3.7.6.2 Criterios de Aceptación:

* Se debe permitir modificar la cantidad, precio y descuento de los productos previamente agregados a la cotización, siempre que la misma no esté en estado cerrado.

* Se debe poder agregar nuevos productos a la cotización, siempre que esta tenga un Pricebook previamente asociado.

* Se debe poder eliminar productos existentes de la cotización.

* El sistema recalculará totales después de cada cambio.

  ### 3.7.7 Generar documentos PDF de cotización {#3.7.7-generar-documentos-pdf-de-cotización}

  3.7.7.1 Narrativa:

  **Como** usuario,  
   **quiero** generar un documento PDF con la cotización,  
   **para** enviarlo formalmente al cliente con detalles de productos, precios y condiciones.

  3.7.7.2 Criterios de Aceptación:

* El sistema permitirá generar un PDF con el formato corporativo definido.

* Se utilizará la plantilla estándar de Salesforce, con la inclusión del logo corporativo de Montironi.

* El documento incluirá información del cliente, del vendedor, de vehículos junto a cantidades, precios, descuentos y totales.

* Se podrá guardar y descargar el PDF para envío por correo o impresión.

* Solo usuarios autorizados podrán generar documentos PDF.

  ### 3.7.8 Enviar para aprobación una cotización {#3.7.8-enviar-para-aprobación-una-cotización}

  3.7.8.1 Narrativa:

  **Como** usuario,  
   **quiero** enviar una solicitud de aprobación de las cotizaciones,  
   **para** validar la acción previo a continuar con el proceso de trabajo.

  3.7.8.2 Criterios de Aceptación:

* La solicitud de aprobación debe enviarse manualmente cuando la cotización cumpla ciertas condiciones:

* Cuando la cotización tenga una taza de un vehículo usado como método de pago.

* El usuario dispondrá de un botón para realizar el envío de la solicitud.

* Se deberá poder redactar un comentario con respecto a la solicitud de aprobación, previo a su envío.

* Los aprobadores deben recibir una notificación para revisar y aceptar o rechazar la transformación.

* El estado de la solicitud debe ser registrado en el historial de la cotización, con los detalles de la aprobación o rechazo.

* No se contempla modificar la lógica del flujo de aprobación ni los usuarios involucrados según los campos editados o la información específica que se desee aprobar.

* La solicitud de aprobación no debe dividirse ni redirigirse según la información editada de la cotización.

* No se deben contemplar envíos diferenciados de aprobación por campo individual ni combinaciones de campos.

* El sistema debe permitir el bloqueo del registro completo del la cotización al momento de enviar la solicitud de aprobación o al aprobarla.

* No se debe contemplar el bloqueo parcial de campos o secciones individuales del registro.

* Mientras el registro esté bloqueado, no se debe permitir la edición de ningún campo del mismo.

  ### 3.7.9 Aprobar cotización {#3.7.9-aprobar-cotización}

  3.7.9.1 Narrativa:

  Como usuario,  
   quiero poder aprobar una cotización,  
   para permitir su avance en el proceso de trabajo.

  3.7.9.2 Criterios de Aceptación:

  * El sistema debe permitir a los usuarios con permisos adecuados aprobar la cotización.

    * El usuario que brinda el veredicto debe poder acceder a la ficha de la cotización en la solicitud de aprobación.

      * Se deberá poder asociar opcionalmente un comentario con respecto a la aprobación, para informar al usuario solicitante sobre la decisión.

        * Los usuarios quienes envían la solicitud de aprobación deben recibir una notificación si la cotización es aprobada.

        * Se podrá considerar automatizaciones relacionadas a la actualización de campos dentro de la cotización aprobada.

        * Se deberá dejar registro de la aprobación de la cotización a través de un historial.

    ### 3.7.10 Rechazar cotización {#3.7.10-rechazar-cotización}

    3.7.10.1 Narrativa:

      **Como** usuario,  
           **quiero** poder rechazar una cotización,  
           **para** filtrar aquellas que no cumplen con los criterios.

    3.7.10.2 Criterios de Aceptación:

* El sistema debe permitir a los usuarios con permisos adecuados rechazar la cotización.

* El usuario que brinda el veredicto debe poder acceder a la ficha del registro en la solicitud de aprobación.

* Se deberá poder asociar opcionalmente un comentario con respecto al rechazo, para informar al usuario solicitante sobre la decisión.

* Los usuarios que envían la solicitud de aprobación deben recibir una notificación si la cotización es rechazada.

* El usuario tendrá la disponibilidad de volver a enviar la solicitud de aprobación.

* Se podrá considerar automatizaciones relacionadas a la actualización de campos dentro de la cotización rechazada.

* Se deberá dejar registro del rechazo de la cotización a través de un historial.

  ### 3.7.11 Sincronizar cotización con oportunidad {#3.7.11-sincronizar-cotización-con-oportunidad}

  3.7.11.1 Narrativa:

  **Como** usuario,  
   **quiero** poder sincronizar una cotización con su oportunidad asociada,  
   **para** mantener consistencia entre los productos y precios negociados.

  3.7.11.2 Criterios de Aceptación:

* El sistema deberá permitir seleccionar una cotización activa para sincronizar con su oportunidad relacionada.

* Una vez sincronizada, cualquier cambio en los productos, cantidades o descuentos de la cotización deberá reflejarse automáticamente en los productos de la oportunidad.

* Solo una cotización podrá estar sincronizada con la oportunidad al mismo tiempo.

* Al sincronizar una nueva cotización, se deberá quitar la sincronización de la anterior, conservando su historial.

  ### 3.7.12 Seleccionar Forma de Pago en la Cotización {#3.7.12-seleccionar-forma-de-pago-en-la-cotización}

  3.7.12.1 Narrativa:  
  Como ejecutivo de ventas,  
  quiero seleccionar una forma de pago dentro de la cotización,  
  para reflejar correctamente cómo el cliente desea abonar la operación.

  3.7.12.2 Criterios de Aceptación:

* La cotización debe incluir un campo de lista de selección (picklist) “Forma de Pago”.

* Al seleccionar la forma de pago, solo deben mostrarse formas de pago activas y vigentes.

* La forma de pago depende del tipo de venta “plan de ahorro” o “convencional”.

  ### 3.7.13 Asociar Plan de Financiamiento a la Cotización {#3.7.13-asociar-plan-de-financiamiento-a-la-cotización}

  3.7.13.1 Narrativa:

  **Como** ejecutivo de ventas,  
  **quiero** asociar un plan de financiamiento específico a la cotización,  
  **para** poder mostrar al cliente el detalle de cuotas, tasa y condiciones del crédito ofrecido.

  3.7.13.2 Criterios de Aceptación:

* La cotización debe incluir un campo de lista de selección (picklist) “Plan de Financiamiento”.

* El listado de planes disponibles varían por:

* Marca y modelo del vehículo cotizado.  
* Vigencia del plan (fecha desde / hasta).  
* Estado del plan (vigente / no vigente).

**Límite de configuraciones**

| Elemento | Cantidad | Descripción |
| :---: | :---: | ----- |
| Compact Layout | 2.00 | Se configurará esa cantidad de Compact Layouts que son un resumen con los 5 campos más importantes de una entidad de información, utilizado habitualmente para visualizar rápidamente la información básica para operar. |
| Informe | 2.00 | Se configurará esa cantidad de Informes, los cuales son una representación tabular o gráfica de datos con filtros y cruces de datos, basada en requerimientos de áreas de la organización. |
| Pack de 5 Validation Rules | 2.00 | Se configurará esa cantidad de paquetes de reglas de validación, que es una regla con lógica de negocio que permite identificar inconsistencia en la forma de ingresar datos de una determinada entidad de información. Cada unidad es un paquete de 5 reglas de validación. |
| Pack de 20 Custom Fields | 2.00 | Se configurará esa cantidad de paquetes de custom fields, que son todos aquellos campos añadidos a objetos para adaptar el modelo de datos a las necesidades de la organización. |
| Pack de 1 Nodo de Flow | 2.00 | Se configurará esa cantidad de series acciones automatizadas que permite hacer más eficiente la ejecución de tareas. |
| Page Layout | 2.00 | Se configurará esa cantidad de layouts, que es un esquema de visualización de los datos y acciones de una entidad de información. |
| Record Type | 2.00 | Se configurará esa cantidad de Record Types, los cuales permiten determinar si para un determinado objeto puede haber variaciones en sus campos, procesos o formas de visualizarlo. |

## 

## **3.8 Gestión de Productos Estándar** {#3.8-gestión-de-productos-estándar}

(imagen omitida)

### 3.8.1 Almacenar información de Productos {#3.8.1-almacenar-información-de-productos}

3.8.1.1 Narrativa:

**Como** usuario,  
**quiero** registrar la información relevante de un producto,  
**para** que esté disponible para su uso en oportunidades, cotizaciones y pedidos.

3.8.1.2 Criterios de Aceptación:

* Se deberá poder almacenar la información definida en el DDD asociada a un producto:

  * Se deberá implementar la herramienta de Chatter a la hora de encontrarse dentro de la ficha de un producto.

    * Se deberán incluir las siguientes validaciones con respecto a la información a almacenar:

      * Se establecerá qué campos serán obligatorios para la gestión de un producto según el DDD.

    ### 3.8.2 Crear marcas comerciales (Business Brand) dentro de la organización {#3.8.2-crear-marcas-comerciales-(business-brand)-dentro-de-la-organización}

    3.8.2.1 Narrativa:

        Como fabricante automotriz,

    **quiero** poder registrar y organizar las distintas marcas comerciales que maneja mi empresa,

    **para** agrupar productos como vehículos, accesorios y repuestos bajo la identidad de marca correcta y facilitar su gestión y visibilidad ante clientes y distribuidores.

    3.8.2.2 Criterios de Aceptación:

        * Se debe poder registrar una nueva marca comercial indicando su nombre y un identificador interno.

        * Se podrá definir una marca principal (madre) y relacionar otras marcas como parte de ella.

        * Se debe poder crear múltiples marcas dentro del mismo entorno para representar diferentes líneas de productos (ej: lujo, utilitarios, deportivos).

        * Al registrar nuevos productos, se podrá asociar cada uno a una marca específica.

        * Debe existir la posibilidad de compartir productos asociados a una marca solo con ciertos grupos, como concesionarios o clientes, en función de permisos configurados por el administrador.

    ### 3.8.3 Asociar productos a Pricebooks {#3.8.3-asociar-productos-a-pricebooks}

    3.8.3.1 Narrativa:

        **Como** usuario,

        **quiero** asociar productos a Pricebooks específicos,

         **para** definir catálogos con precios para diferentes clientes o condiciones.

    3.8.3.2 Criterios de Aceptación:

        * Se podrá asociar un producto a uno o más Pricebooks con precio específico para cada uno.

        * Sólo usuarios autorizados podrán realizar esta asociación.

        * Los productos y precios asociados estarán disponibles para oportunidades y cotizaciones.

    ### 3.8.4 Detectar SKUs de productos duplicados \[Presente SOW Original\] {#3.8.4-detectar-skus-de-productos-duplicados-[presente-sow-original]}

    3.8.4.1 Narrativa:

        **Como** usuario,

         **quiero** que el sistema detecte automáticamente productos potencialmente duplicados,

         **para** evitar la creación de registros redundantes.

    3.8.4.2 Criterios de Aceptación:

* El sistema debe identificar productos potencialmente duplicados en función de la información clave del mismo.

  * El SKU del producto.

* Dichos criterios podrán ser tomados individualmente o por combinación de ellos (O lógico; Y lógico).

* La detección de los duplicados se realizará únicamente a través de campos almacenados en el lead de tipo “Texto” o “Número”.

* Al detectar un duplicado a la hora de realizar la creación de un producto, el sistema restringirá al usuario de realizar dicha acción, mostrando un mensaje de error y adjuntando el producto con el cuál existen incongruencias.

* La detección de un duplicado únicamente aplicará cuando el producto esté siendo generado.

**Límite de configuraciones**

| Elemento | Cantidad | Descripción |
| :---: | :---: | ----- |
| Compact Layout | 2.00 | Se configurará esa cantidad de Compact Layouts que son un resumen con los 5 campos más importantes de una entidad de información, utilizado habitualmente para visualizar rápidamente la información básica para operar. |
| Informe | 2.00 | Se configurará esa cantidad de Informes, los cuales son una representación tabular o gráfica de datos con filtros y cruces de datos, basada en requerimientos de áreas de la organización. |
| Pack de 5 Validation Rules | 2.00 | Se configurará esa cantidad de paquetes de reglas de validación, que es una regla con lógica de negocio que permite identificar inconsistencia en la forma de ingresar datos de una determinada entidad de información. Cada unidad es un paquete de 5 reglas de validación. |
| Pack de 20 Custom Fields | 2.00 | Se configurará esa cantidad de paquetes de custom fields, que son todos aquellos campos añadidos a objetos para adaptar el modelo de datos a las necesidades de la organización. |
| Pack de 1 Nodo de Flow | 2.00 | Se configurará esa cantidad de series acciones automatizadas que permite hacer más eficiente la ejecución de tareas. |
| Page Layout | 2.00 | Se configurará esa cantidad de layouts, que es un esquema de visualización de los datos y acciones de una entidad de información. |
| Record Type | 2.00 | Se configurará esa cantidad de Record Types, los cuales permiten determinar si para un determinado objeto puede haber variaciones en sus campos, procesos o formas de visualizarlo. |

## **3.9 Gestión de Listas de Precios Estándar** {#3.9-gestión-de-listas-de-precios-estándar}

(imagen omitida)

### 3.9.1 Almacenar información de lista de precios {#3.9.1-almacenar-información-de-lista-de-precios}

3.9.1.1 Narrativa:

**Como** usuario,  
 **quiero** almacenar la información relacionada a mis listas de precios,  
 **para** posteriormente, realizar gestiones posteriores con ellos.

3.9.1.2 Criterios de Aceptación:

* Se deberá poder almacenar la información definida en el DDD asociada a una lista de precios:

* En la ficha de una lista de precios en específico, se deberá visualizar los productos asociados a ella en conjunto con su precio establecido.

* Se deberá implementar la herramienta de Chatter a la hora de encontrarse dentro de la ficha de una lista de precios.

* Se incluirán las validaciones con respecto a la información a almacenar definidas dentro del DDD.

* Se deberán establecer qué campos serán obligatorios para la gestión de una lista de precios.

  ## **3.10 Gestión de Actividades** {#3.10-gestión-de-actividades}

(imagen omitida)

### 3.10.1 Gestionar Tareas {#3.10.1-gestionar-tareas}

3.10.1.1 Narrativa:

Como usuario,  
**quiero** crear y gestionar tareas relacionadas a cuentas, contactos, oportunidades y casos,  
**para** dar seguimiento ordenado a mis pendientes y no perder compromisos.

3.10.1.2 Criterios de Aceptación:

* Se pueden crear tareas con: Asunto, Comentarios, Prioridad, Estado, Fecha de vencimiento, Propietario, Tipo, Relacionado a.

  * La tarea queda visible en el Activity Timeline del registro relacionado.

    * Puedo marcar la tarea como Completada y queda registrada con fecha/hora y usuario que la completó.

      * Puedo reasignar el Propietario y queda trazabilidad del cambio.

        * Puedo adjuntar archivos a la tarea y verlos desde el timeline.

        * Puedo filtrar y ver mis tareas vencidas, de hoy y próximas desde la vista de lista de Tareas.

    ### 3.10.2 Enviar y Registrar Correo desde Salesforce {#3.10.2-enviar-y-registrar-correo-desde-salesforce}

    3.10.2.1 Narrativa:

          Como usuario,

    **quiero** enviar y registrar correos electrónicos directamente desde el Activity Timeline,

    **para** mantener el historial de comunicación centralizado en Salesforce.

    3.10.2.2 Criterios de Aceptación:

      * Puedo enviar correo desde el botón Email del timeline usando: Para, CC, BCC, Asunto, Cuerpo, Plantillas (Lightning/Classic según habilitación) y adjuntos.

      * El correo enviado se registra como EmailMessage relacionado al registro (Cuenta/Contacto/Oportunidad/Caso) y visible en el timeline.

      * Soporta direcciones desde el Contacto/Lead y correos manuales válidos.

      * Puedo usar la firma del usuario y plantillas con variables del registro relacionado.

      * Las respuestas del cliente pueden registrarse automáticamente si está habilitado Enhanced Email y/o Einstein Activity Capture / Inbox (según licencias y política), manteniendo el hilo.

      * El envío respeta límites y permisos de email de la organización (dominios permitidos, tamaño de adjuntos, límites diarios).

    ### 3.10.3 Crear y Gestionar Notas en Registros {#3.10.3-crear-y-gestionar-notas-en-registros}

    2. Narrativa:

       **Como** usuario,  
       **quiero** crear notas vinculadas a registros de Salesforce,  
       **para** documentar información relevante que complemente los datos estructurados del registro.

    3. Criterios de Aceptación:

* La nota permite: Título, Cuerpo (texto enriquecido con formato básico), y adjuntar archivos.

* La nota queda asociada al registro principal y puede vincularse a múltiples registros (multi-relacionada) si está habilitada la opción.

* Solo usuarios con permisos de lectura sobre el registro y sobre la nota pueden visualizarla.

* La edición/eliminación solo está disponible para el propietario o usuarios con permisos de modificar todos los datos.

* Se puede buscar y filtrar notas por título, contenido o registro relacionado desde la pestaña global de Notas.

* Se pueden marcar notas como privadas o públicas según política de la organización.

  ## **3.11 Gestión de Boletos**

(imagen omitida)

### 3.11.1 Almacenar información Boletos

3.11.1.1 Narrativa:

**Como** usuario,  
**quiero** registrar la información relevante de un boleto,  
**para** que esté disponible para su uso en oportunidades.

3.11.1.2 Criterios de Aceptación:

* Se deberá poder almacenar la información definida en el DDD asociada a un boleto.

  * Se deberá implementar la herramienta de Chatter a la hora de encontrarse dentro de la ficha de un boleto.

    * Se deberán incluir las siguientes validaciones con respecto a la información a almacenar:

      * Se establecerá qué campos serán obligatorios para la gestión de un boleto según el DDD.

    ### 3.11.2 Asociar boletos a Oportunidades

    3.11.2.1 Narrativa:

        Como usuario,

    **quiero** asociar automáticamente boletos a Oportunidades específicas,

    **para** mantener un registro de trazabilidad de la operación.

    3.11.2.2 Criterios de Aceptación:

      * Se podrá asociar un boleto a una oportunidad.

      * Sólo usuarios autorizados podrán realizar esta asociación.

    ### 3.11.3 Actualizar información de Boleto

    3.11.3.1 Narrativa:

        Como administrador,

    **quiero** editar los campos de un boleto existente,

    **para** mantener la información de la operación actualizada ante cambios en el proceso de venta.

    3.11.3.2 Criterios de Aceptación:

      * Los campos del boleto que no estén bloqueados por permisos o lógica de negocio son editables desde la ficha.  
      * Solo usuarios con permisos de edición sobre el objeto Boleto pueden modificar sus datos.  
      * Al guardar cambios, el sistema registra fecha, hora y usuario que realizó la modificación en el historial del campo.  
      * Si un campo obligatorio se deja vacío durante la edición, el sistema muestra un mensaje de error y no guarda hasta que se complete.  
      * Los cambios quedan reflejados de forma inmediata en la vista del registro y en la sección relacionada de la Oportunidad.

  ## **3.12 Gestión de Pruebas de Manejo**

(imagen omitida)

### 3.11.1 Almacenar información de Pruebas de Manejo

3.11.1.1 Narrativa:

**Como** usuario,  
**quiero** registrar la información relevante de una Prueba de manejo,  
**para** que esté disponible para su registro a la oportunidad asociada.

3.11.1.2 Criterios de Aceptación:

* Se deberá poder almacenar la información definida en el DDD asociada a una prueba de manejo.

  * Se deberá implementar la herramienta de Chatter a la hora de encontrarse dentro de la ficha de una prueba de manejo.

    * Se deberán incluir las siguientes validaciones con respecto a la información a almacenar:

      * Se establecerá qué campos serán obligatorios para la gestión de una prueba de manejo según el DDD.

    ### 3.11.2 Asociar pruebas de manejo a Oportunidades

    3.11.2.1 Narrativa:

        Como usuario,

    **quiero** asociar pruebas de manejo a Oportunidades específicas,

    **para** mantener un registro de trazabilidad de la operación.

    3.11.2.2 Criterios de Aceptación:

      * Se podrá asociar una o unas Pruebas de manejo a una oportunidad.

      * Sólo usuarios autorizados podrán realizar esta asociación.

    ### 3.11.3 Actualizar información de Prueba de manejo

    3.11.3.1 Narrativa:

        Como usuario,

    **quiero** editar los campos de una prueba de manejo existente,

    **para** mantener la información de la operación actualizada ante cambios en el proceso de venta.

    3.11.3.2 Criterios de Aceptación:

      * Los campos de la prueba de manejo que no estén bloqueados por permisos o lógica de negocio son editables desde la ficha.  
      * Solo usuarios con permisos de edición sobre el objeto Prueba de manejo pueden modificar sus datos.  
      * Al guardar cambios, el sistema registra fecha, hora y usuario que realizó la modificación en el historial del campo.  
      * Si un campo obligatorio se deja vacío durante la edición, el sistema muestra un mensaje de error y no guarda hasta que se complete.  
      * Los cambios quedan reflejados de forma inmediata en la vista del registro y en la sección relacionada de la Oportunidad.

# **5\. Integraciones con DMS** {#5.-integraciones-con-dms}

Se detallan a continuación las integraciones con el DMS de Montironi. El mismo será desplegado por Montironi. 

(imagen omitida)

## **5.1 Integración saliente de Cuentas** {#5.1-integración-saliente-de-cuentas}

1. **Narrativa:**

   **Como** vendedor,   
   **quiero** que la información de las cuentas se integre automáticamente hacia otros sistemas,   
   **para** garantizar que los datos del cliente estén sincronizados y disponibles en plataformas externas como DMS.

   2. **Criterios de aceptación:**

* El sistema debe enviar automáticamente los datos de la cuenta al Middleware quien se encargará de ingresar en el DMS correspondiente una vez cumplidos los criterios de sincronización.  
* Los campos a integrar son aquellos definidos dentro del DDD.  
* La integración debe generar un identificador o confirmación de éxito al completarse.

  ## **5.2 Integración entrante de Cuentas** {#5.2-integración-entrante-de-cuentas}

**5.2.1. Narrativa:**

**Como** vendedor,   
**quiero** que los datos de clientes creados o modificados en otros sistemas se integren automáticamente en Salesforce,   
**para** contar con información actualizada y evitar registros duplicados o desfasados.

**5.2.2. Criterios de aceptación:**

* El sistema debe recibir datos de cuentas desde el Middleware de forma automática.  
* La cuenta debe crearse o actualizarse en Salesforce respetando los criterios de integración definidos.  
* Se debe validar si la cuenta ya existe para evitar duplicados, utilizando reglas de coincidencia establecidas.  
* Los datos integrados deben conservar formato, relaciones y estado de sincronización.  
* Los cambios realizados por integración deben quedar registrados con su origen y fecha de actualización.

  ## **5.3 Integración entrante de Productos** {#5.3-integración-entrante-de-productos}

**5.3.1. Narrativa:**

**Como** vendedor,   
**quiero** que los datos de los productos de DMS se integren automáticamente en Salesforce,   
**para** contar con información actualizada de ellos.

**5.3.2. Criterios de aceptación:**

* El sistema debe recibir datos de los productos desde el Middleware de forma automática.  
* Los productos deben crearse o actualizarse en Salesforce respetando los criterios de integración definidos.  
* Los datos integrados deben conservar formato, relaciones y estado de sincronización.

  ## **5.4 Integración Entrante de Stock de Vehículos (DMS)** {#5.4-integración-entrante-de-stock-de-vehículos-(dms)}

**5.4.1. Narrativa:**

**Como** Vendedor,   
**quiero** visualizar en Salesforce el inventario real de vehículos disponibles en el DMS, incluyendo su ubicación física, color y estado (Disponible/Reservado),   
**para** poder asignar unidades concretas a mis clientes y evitar errores de venta.

**5.4.2. Criterios de aceptación:**

* Desarrollo de proceso para recepción de novedades de stock desde el DMS (Batch o Real-time según disponibilidad técnica).  
* Actualización del objeto Vehículo (Asset/Product) en Salesforce utilizando el VIN (Chasis) como clave única.  
* Campos a sincronizar:  
* Modelo, Versión, Año.  
* Color, Motor, Chasis (VIN).  
* Ubicación Física (Sucursal).  
* Estado de Disponibilidad (Disponible, Reservado, Vendido, Facturado).  
* Lógica de Inactivación: Si un vehículo desaparece del stock del DMS, debe marcarse como "No Disponible" en Salesforce.

  ## **5.5 Integración Saliente de Operación/Boleto (Outbound)** {#5.5-integración-saliente-de-operación/boleto-(outbound)}

**5.5.1. Narrativa:**

**Como** Administrativo de Ventas,   
**quiero** que al marcar una Oportunidad como "Cerrada Ganada" se cree un Boleto, los datos completos de la operación viajen automáticamente al DMS   
**para** generar la Nota de Pedido, evitando la doble carga manual de datos y errores de facturación.

**5.5.2 Criterios de aceptación:**

* Validación previa: El sistema verificará que la Oportunidad tenga un Vehículo (VIN) asignado y los datos fiscales del cliente completos antes de enviar.  
* Envío de la estructura de datos al DMS:  
* Datos de la Cuenta (Cliente).  
* Datos del Vehículo (VIN).  
* Detalle Económico: Precio Venta, Monto Seña, Anticipo, Financiación declarada.  
* Confirmación de Éxito: Recepción del "Número de Operación/Boleto" generado por el DMS, el cual se guardará en un campo de la Oportunidad en Salesforce.

  ## **5.6 Integración Entrante de Leads de Fábrica (Inbound)** {#5.6-integración-entrante-de-leads-de-fábrica-(inbound)}

**5.6.1. Narrativa:**

 **Como** Gerente de Marketing,   
**quiero** que los prospectos generados en los portales de las terminales (FordHub, Grow, Extranet) ingresen automáticamente a Salesforce a través de la integración,   
**para** centralizar la gestión en una única bandeja de entrada y asegurar la inmediatez en el contacto.

**5.6.2. Criterios de aceptación:**

* Disponibilización de un Endpoint REST en Salesforce para recibir la información desde el Middleware.  
* Mapeo de campos estándar de la industria (AIV):  
* Datos del Cliente: Nombre, Apellido, Teléfono, Email, DNI/CUIT.  
* Datos del Vehículo: Modelo de Interés, Versión.  
* Origen del Dato: Identificador de la fuente (ej. "FordHub", "Grow", "Web").  
* Concesionario Asignado: Código de sucursal.  
* Lógica de Deduplicación: El servicio validará si el Lead ya existe por Email o Teléfono.  
* Si existe: Actualizará el registro y creará una Tarea de aviso al vendedor.  
* Si no existe: Creará un nuevo Lead.

  ## **5.7 Integración Saliente de Estado de Leads** {#5.7-integración-saliente-de-estado-de-leads}

**5.7.1. Narrativa:**

**Como** Responsable de Calidad,   
**quiero** que Salesforce reporte automáticamente al sistema externo cada vez que un Lead cambia de estado o se cierra una venta,   
**para** que esta información llegue a las terminales y cumpla con los requisitos de compliance y SLAs de la marca.

**5.7.2. Criterios de aceptación:**

* Desarrollo de un disparador automático (Flow/Trigger) que se ejecute al modificarse el campo "Estado" (Lead Status) o "Etapa" (Opportunity Stage).  
* Generación del mensaje de salida (JSON Payload) hacia el Middleware con los datos requeridos:  
* ID Externo del Lead.  
* Nuevo Estado Homologado (ej: "En Gestión", "Contactado", "Vendido", "Caído").  
* Motivo de Caída (si aplica).  
* Registro de Logs de Integración: Se guardará un registro de éxito o error de cada envío para auditoría.

  ## **5.8 Integración Entrante de Boleto (Inbound)**

**5.8.1. Narrativa:**

**Como** Administrativo de Ventas,   
**quiero** que al confirmarse el Boleto en el DMS, el Número de Operación/Boleto se registre automáticamente en la Oportunidad de Salesforce,   
**para** tener trazabilidad completa de la operación sin necesidad de carga manual y evitar errores de seguimiento.

**5.8.2 Criterios de aceptación:**

* Trigger de recepción: El sistema recibe la respuesta del DMS con el Número de Operación/Boleto una vez que el DMS confirma la creación del boleto.  
* Actualización automática: El Número de Operación/Boleto recibido se guarda en el campo correspondiente de la Oportunidad en Salesforce sin intervención manual.  
* Notificación al usuario: Una vez recibido y registrado el número, el sistema notifica al Administrativo de Ventas responsable de la Oportunidad mediante una notificación en Salesforce.

* Manejo de error: Si el DMS no responde o devuelve un error dentro del tiempo establecido, el sistema registra el fallo, notifica al usuario responsable y deja la Oportunidad en un estado que permita reintentar el envío.

* Confirmación de éxito: La Oportunidad muestra el Número de Operación/Boleto recibido y la fecha de confirmación del DMS en los campos correspondientes.

  ## **5.9 Integración entrante de Vehículos**

**5.9.1. Narrativa:**

**Como** Administrativo de Ventas,   
**quiero** quiero que cuando el DMS confirme la entrega de un vehículo a un cliente, los datos de ese vehículo se registren automáticamente en Salesforce asociados a la Oportunidad cerrada ganada correspondiente,   
**para** tener trazabilidad completa del vehículo entregado sin necesidad de carga manual.

**5.9.2 Criterios de aceptación:**

* El sistema solo debe recibir y procesar datos de vehículos desde el Middleware cuando el DMS notifique la entrega efectiva del vehículo al cliente.

* La recepción del vehículo debe vincularse a la Oportunidad en estado "Cerrada Ganada" correspondiente, utilizando el identificador de operación/boleto como clave de cruce.

* El registro del vehículo en Salesforce debe crearse o actualizarse respetando los criterios de integración definidos en el DDD.

* Los datos integrados deben conservar formato, relaciones y estado de sincronización.

* Si no existe una Oportunidad cerrada ganada asociada al identificador recibido, el sistema debe registrar el error para auditoría y notificar al responsable.

  ## **5.10 Integración saliente de Vehículos**

**5.10.1. Narrativa:**

**Como** Administrativo de Ventas,   
**quiero** que cuando se registre o modifique un vehículo en Salesforce, la información sea enviada automáticamente al DMS a través del Middleware,   
**para** garantizar que el catálogo de vehículos esté sincronizado entre ambas plataformas.

**5.10.2 Criterios de aceptación:**

* El sistema debe enviar automáticamente los datos del vehículo al Middleware quien se encargará de ingresarlos en el DMS correspondiente una vez cumplidos los criterios de sincronización.

* Los campos a integrar son aquellos definidos dentro del DDD.

* La integración debe generar un identificador o confirmación de éxito al completarse.

* En caso de error en el envío, el sistema debe registrar el fallo para auditoría y reintento.

  ## **5.11 Integración entrante de Lista de Precios**

**5.11.1. Narrativa:**

**Como** Administrativo de Ventas,   
**quiero** que las listas de precios del DMS se integren automáticamente en Salesforce (Pricebooks),   
**para** contar con precios actualizados al momento de crear cotizaciones y oportunidades sin necesidad de actualización manual.

**5.11.2 Criterios de aceptación:**

* El sistema debe recibir datos de listas de precios desde el Middleware de forma automática.

* Los Pricebooks y sus entradas (PricebookEntry) deben crearse o actualizarse en Salesforce respetando los criterios de integración definidos.

* Los precios deben asociarse correctamente a los productos/vehículos correspondientes utilizando el identificador único de cada producto.

* Los datos integrados deben conservar formato, relaciones y estado de sincronización.

* Los campos a sincronizar son aquellos definidos dentro del DDD.

# **6\. Service Cloud** {#6.-service-cloud}

Se detallan a continuación las historias de usuario para realizar un quickstart de Service Cloud, con la finalidad de que el contact center gestione consultas, quejas o reclamos.

(imagen omitida)

## **6.1 Configuración de Omni-Channel** {#6.1-configuración-de-omni-channel}

**6.1.1. Narrativa:**

**Como** Supervisor,   
**quiero** que el sistema asigne automáticamente los chats transferidos por el Agente de IA y los mensajes entrantes a la cola de Contact Center que estén "Disponibles" en ese momento, **para** evitar que los clientes esperen o que se acumulen tareas en una sola persona.

**6.1.2. Criterios de aceptación:**

* Habilitación del widget de Omni-Channel en la Consola de Servicio.  
* Configuración de Estados de Presencia: "Disponible", "Ocupado", "Almuerzo", "Offline".  
* Configuración de Configuraciones de Enrutamiento (Routing Configs) para priorizar Chats sobre Emails (ej: el chat entra primero).  
* Creación de las Colas (Queues) habilitadas para enrutamiento automático (Cola de Ventas, Cola de Atención).

  ## **6.2 Configuración de Casos** {#6.2-configuración-de-casos}

**6.2.1. Narrativa:**

**Como** Agente del Contact Center,   
**quiero** disponer de un sistema unificado para registrar y dar seguimiento a consultas administrativas, reclamos o pedidos de posventa, diferenciándolos de las oportunidades comerciales,   
**para** asegurar que cada solicitud de cliente tenga su resolución.

**6.2.2. Criterios de aceptación:**

* Habilitación del objeto estándar Caso (Case).  
  * Configuración de hasta tres (3) Tipos de Registro para segmentar la atención en base al DDD.  
    * Configuración de Estados del Caso (Path) en base a lo definido en el DDD.  
      * Configuración de una Cola de Atención General donde se asignarán los casos que no tengan un propietario definido.

  ## **6.3 Canal de Email-to-Case** {#6.3-canal-de-email-to-case}

**6.3.1. Narrativa:**

**Como** Supervisor de Atención,   
**quiero** que los correos electrónicos enviados a la casilla institucional de atención se conviertan automáticamente en Casos dentro de Salesforce,   
**para** evitar la pérdida de información en bandejas de entrada personales y medir tiempos de respuesta.

**6.3.2. Criterios de aceptación:**

* Configuración de **Email-to-Case** para una (1) dirección de correo electrónico provista por el cliente (ej: *atencion@montironi.com*).  
  * Configuración de una **Respuesta Automática (Auto-Response Rule)** estándar al cliente confirmando la recepción del caso y su número de ticket.  
    * Asignación automática de estos casos a la Cola de Atención General.  
      * Capacitación y habilitación para que el equipo de Desarrollo pueda realizar esta tarea con completa autonomía, porque tendremos más de una dirección de correo. 

  ## **6.4 Consola de Servicio (Interfaz de Agente)** {#6.4-consola-de-servicio-(interfaz-de-agente)}

**6.4.1. Narrativa:**

**Como** Agente,   
**quiero** trabajar en una interfaz optimizada (Consola) que me permita ver la información del cliente y del caso en una misma pantalla sin perder contexto al navegar,   
**para** gestionar los reclamos con mayor velocidad.

**6.4.2. Criterios de aceptación:**

* Habilitación de la Lightning Service Console.  
  * Configuración de la navegación basada en Pestañas y Sub-pestañas (Ej: Al abrir un Caso, se abre como sub-pestaña de la Cuenta del cliente).  
    * Configuración del Panel de Resaltado (Highlights Panel) para mostrar datos clave del cliente (Teléfono, Email, DNI) en el encabezado del caso.

  ## **6.5 Reportes y Tableros de Servicio** {#6.5-reportes-y-tableros-de-servicio}

**6.5.1. Narrativa:**

**Como** Gerente de Atención, **quiero** visualizar un tablero con las métricas clave de mi equipo, **para** entender el volumen de trabajo y los tiempos de resolución.

**6.5.2. Criterios de aceptación:**

* Creación de una (1) Carpeta de Reportes de Servicio y una (1) Carpeta de Tableros.  
  * Configuración de un Tablero de Servicio (Dashboard) que incluya:  
    * Casos abiertos por Estado.  
      * Casos abiertos por Agente.  
        * Casos creados hoy/esta semana por Origen (Email vs. Chat/IA).  
        * Tiempo promedio de resolución (si aplica).  
      * Capacitación y habilitación para el área de Desarrollo para que pueda crear los tableros que necesite la operación.

  ## **6.6 Configurar encuesta NPS con Salesforce Surveys** 

**6.6.1. Narrativa:**

**Como** administrador de Salesforce, **quiero** configurar una encuesta NPS estándar mediante Salesforce Surveys, **para** capturar el nivel de satisfacción del cliente y registrar automáticamente las respuestas en Salesforce como base para las automatizaciones de seguimiento.

**6.6.2. Criterios de aceptación:**

* Se configurará una encuesta con diferentes preguntas de satisfacción, de acuerdo a los tipos de respuestas aceptados de forma estándar en Salesforce Surveys.  
  * La encuesta se enviará desde Salesforce por correo electrónico al contacto asociado a la cuenta.  
    * Cada respuesta quedará registrada como un objeto Respuesta de Encuesta vinculado a la cuenta y contacto correspondiente.  
      * Solo usuarios autorizados podrán crear y modificar encuestas.

#  **7\. Agentforce (Agentes de IA)** {#7.-agentforce-(agentes-de-ia)}

Esta sección detalla la implementación de un Agente Autónomo basado en Inteligencia Artificial (Salesforce Agentforce) diseñado para gestionar la primera línea de contacto en los canales digitales de Montironi (WhatsApp y Web).

(imagen omitida)

## **7.1 Agente de Primera Respuesta** {#7.1-agente-de-primera-respuesta}

**7.1.1. Narrativa:**

**Como** Gerente de Montironi,   
**quiero** implementar un Agente de Inteligencia Artificial en los canales digitales (WhatsApp y Web) que actúe como "Recepcionista Virtual" 24/7,   
**para** identificar automáticamente la intención del cliente y responder consultas frecuentes, reduciendo la carga operativa del equipo humano.

**7.1.2. Criterios de aceptación:**

* Configuración de un (1) Agente de IA utilizando Agentforce.  
* Conexión del Agente a los canales de mensajería: WhatsApp Business API y Chat Web (Embedded Service).  
* Definición y entrenamiento de Tópicos de Conversación (Intenciones) principales:  
  * Interés en Compra 0km / Usado.  
  * Consulta sobre Plan de Ahorro o Venta tradicional.  
  * Posventa (Service), compra de repuestos, compra o consulta de accesorios y compra o consulta de seguros.  
  * Administración/Atención al Cliente.  
* Configuración de Instrucciones de Seguridad (Guardrails) para evitar que el agente responda sobre temas sensibles, política de precios no oficiales o competidores.

  ## **7.2 Calificación y Generación de Leads** {#7.2-calificación-y-generación-de-leads}

**7.2.1. Narrativa:**

**Como** Supervisor de Ventas,   
**quiero** que si el Agente detecta una intención de compra, solicite los datos clave al cliente y genere el Lead automáticamente en Salesforce,   
**para** asegurar que los vendedores reciban prospectos ya calificados y con datos de contacto validados.

**7.2.2. Criterios de aceptación:**

* Configuración de lógica de Slot Filling (Captura de Datos): El agente deberá solicitar obligatoriamente Nombre, Apellido, Modelo+Marca de Interés, sucursal más cercana (de las de Montironi),  correo electrónico y teléfono celular.  
* Configuración de Acciones del Agente (Agent Actions):  
  * Si la intención es Venta: Ejecutar un "Flow" que busque si el cliente existe; si no, crea un nuevo registro de Lead.  
  * Si la intención es Posventa/Admin: No crear Lead de venta. Identificar la cuenta cliente para registrar el contacto en la cuenta relacionada. Luego abrir un caso en Service Cloud y derivarlo a la bandeja de Atención al Cliente.  
  * Manejo de Errores: Si el agente no logra capturar los datos tras dos intentos, deberá derivar a un humano para no frustrar al usuario.

  ## **7.3 Transferencia Inteligente** {#7.3-transferencia-inteligente}

**7.3.1. Narrativa:**

**Como** Agente del Call Center,   
**quiero** que cuando el bot me transfiera una conversación, esta llegue a la cola correcta (Ventas o Servicio) y yo pueda ver el resumen de lo que el cliente habló con la IA,   
**para** no volver a preguntarle lo mismo.

**7.3.2. Criterios de aceptación:**

* Integración con Omni-Channel: El Agente debe transferir la sesión a la cola específica según la intención detectada (ej: Intención "Compra" \-\> Cola "Ventas"; Intención "Reclamo" \-\> Cola "Atención").  
* Visibilidad del Historial: Al recibir el chat, el agente humano debe poder visualizar la transcripción previa de la conversación entre el cliente y el Agente de IA, y que eso forme parte del historial de contactos del contacto. 

### **7.4 Crear Artículos**

**7.4.1. Narrativa:**

* **Como** administrador de Salesforce, **quiero** crear nuevos artículos de conocimiento, **para** tener los protocolos de servicio documentados y centralizados.

**7.4.2. Criterios de aceptación:**

* El Usuario Salesforce puede acceder al objeto Knowledge (Artículos). 

* El Usuario Salesforce puede completar un formulario con los datos de Knowledge (Artículos) para crear el registro (hasta 20 campos personalizados). 

* El Usuario Salesforce recibe una confirmación de que la información del registro ha sido almacenada con éxito. 

* La información registrada es visible y accesible en las secciones correspondientes del objeto contactos.

* El equipo implementador generará la creación de un máximo de 10 Knowledge (Artículos) para el equipo Montironi.

### **7.5 Editar Artículos**

**7.5.1. Narrativa:**

* **Como** agente de servicio, **quiero** editar la información de artículos de conocimiento existentes y/o generar nuevas versiones, **para** mantener sus datos de los artículos o bases de conocimiento actualizados.

  **7.5.2. Criterios de aceptación:**

* El Usuario Salesforce puede ingresar al objeto Knowledge (Artículos). 

* El Usuario Salesforce puede seleccionar el registro y dar clic en modificar/editar, para cambiar los campos correspondientes en el registro (nombre, descripción, lenguaje, estado).

* El Usuario Salesforce puede guardar las modificaciones realizadas en cada registro.

### **7.6 Eliminar Artículos**

**7.6.1. Narrativa:**

* **Como** administrador de Salesforce, **quiero** inactivar artículos de conocimiento, **para** depurar los artículos que no se utilicen y mantener una base de datos relevante.

  **7.6.2. Criterios de aceptación:**

* El Administrador de la plataforma puede ingresar al objeto Knowledge (Artículos).

* El Administrador de la plataforma al seleccionar un registro puede ver el botón 'inactivar'.

* El Administrador de la plataforma puede visualizar el botón 'inactivar'.

* El sistema debe informar que el registro se inactivó correctamente al seleccionar el botón inactivar.

### **7.7 Visualizar Artículos**

**7.7.1. Narrativa:**

* **Como** usuario de Salesforce, **quiero** visualizar los artículos de conocimiento creados, **para** poder ingresar a los datos completos de los artículos o bases de conocimiento que se requieran.

  **7.7.2. Criterios de aceptación:**

* El Usuario Salesforce puede ingresar al objeto Knowledge (Artículos).

* El Usuario Salesforce al seleccionar un registro puede ver la información correspondiente al registro.

### **7.8 Buscar Artículos**

**7.8.1. Narrativa:**

* **Como** usuario de Salesforce, **quiero** buscar artículos de conocimiento por nombre, **para** encontrar rápidamente la información de los artículos o bases de conocimiento necesarias.

  **7.8.2. Criterios de aceptación:**

* El Usuario Salesforce puede ingresar al objeto Knowledge (Artículos).

* El Usuario Salesforce puede visualizar la lista de registros de Knowledge (Artículos).

* El sistema debe permitir buscar los registros según criterios (nombre, código).

* El sistema debe permitir visualizar el buscador general de Salesforce, donde el Usuario Salesforce podrá buscar los registros correspondientes a Knowledge (Artículos) según los criterios (Nombre o código).

# **8\. Entregables \- Etapas posteriores** {#8.-entregables---etapas-posteriores}

## **8.1 Entregables y Compromisos del Cliente \- Etapa de Sprint 0** {#8.1-entregables-y-compromisos-del-cliente---etapa-de-sprint-0}

* **Participación Activa:** Compromiso en la participación activa en sesiones de revisión, pruebas y capacitación según lo requiera el proyecto.

* **Retroalimentación Continua:** Proporcionar retroalimentación y aprobación oportuna a lo largo del proyecto, especialmente en lo que respecta a los criterios de aceptación.

* **Definición de Roles y Responsabilidades:** Especificación de quién en el equipo del cliente desempeñará qué roles y cuáles serán sus responsabilidades.

* **Requerimientos iniciales:** Proporcionar una descripción clara y detallada de los requisitos iniciales del proyecto, incluyendo objetivos comerciales, funcionalidades deseadas y restricciones.

* **Documentación Complementaria:** Proporcionar documentación complementaria que ayude a la comprensión o definición de los requerimientos, tales como formularios, documentación que es utilizada actualmente, documentación técnica (en caso de aplicar), ejemplos, entre otros.

* **Documentación Técnica Complementaria para Integraciones:** Proporcionar documentación complementaria para poder realizar las integraciones con el o los sistemas externos contemplados dentro del alcance del proyecto, siendo principalmente:

  * Documentación técnica de su API.

  * Forma de autenticación.

* **Lectura del Documento Statement of Work (SOW):** Leer y revisar activamente la documentación que brinda cierre a la etapa de Sprint 0\.

* **Aclaración de Dudas del Documento Statement of Work (SOW):** En caso de que existan dudas, proporcionar la retroalimentación al equipo de ProContacto.

* **Brindar Veredicto de los Controles de Cambio:** En caso de existir algún control de cambios dentro de la etapa de Sprint 0, se deberá conocer el veredicto final sobre cada uno de ellos, siendo:

  * Llevar a cabo el requerimiento para el release actual, implicando su continuación por medio de una gestión comercial.

  * No tomar el requerimiento.

  * Tomar el requerimiento para un release posterior a la primera fase, dejando constancia de la detección de dicho requerimiento.

* **Aprobación del Documento Statement of Work (SOW):** Revisar y aprobar la documentación proporcionada por el equipo implementador, para poder continuar con el desarrollo e implementación del proyecto.

  ## **8.2 Entregables  y Compromisos del Equipo de ProContacto \- Etapa de Sprint 0** {#8.2-entregables-y-compromisos-del-equipo-de-procontacto---etapa-de-sprint-0}

* **Statement of Work (SOW) Refinado:** Documentación actual, en el cuál se detalla a un alto nivel los requerimientos principales incluídos del alcance inicial, así también como los controles de cambio detectados en esta etapa (en caso de aplicar), y las integraciones involucradas dentro del proyecto (en caso de aplicar).

* **Grabación de Sesiones de Relevamiento:** Grabación de sesiones de relevamiento para su disponibilidad futura realizadas en el sprint 0\.

* **Plan de Trabajo del Proyecto:** Una vez realizada la firma del presente documento, se realizará y entregará un cronograma detallado de las funcionalidades y objetos que se desarrollarán, en conjunto con los hitos clave de cada etapa del proyecto desde el inicio de la ejecución hasta la entrega final del aplicativo.

  ## **8.3 Entregables  y Compromisos del Cliente \- Etapa de Ejecución** {#8.3-entregables-y-compromisos-del-cliente---etapa-de-ejecución}

1. **Detalles de Requerimientos:** A la hora de abordar las reuniones de refinamiento de historias de usuario, proporcionar definiciones y descripciones claras y detalladas.

2. **Aprobación de Historias de Usuario:** Aprobar las historias de usuario que se llevarán a cabo, como validación a nivel funcionalidad de la implementación posterior.

3. **Comentarios sobre la demostración realizada (Feedback Tracker):** En caso de aplicar, se podrá realizar comentarios de la funcionalidad presentada en la ceremonia Demo del sprint correspondiente. Estos comentarios involucran correcciones menores, dudas, aclaraciones, entre otras devoluciones. Los comentarios serán gestionados a través de un documento compartido llamado “Feedback Tracker”.

4. **Aprobación de Funcionalidad (Demostración):** El equipo de ProContacto realizará una demostración sobre una funcionalidad llevada a cabo durante una iteración. El cliente deberá expresar la conformidad de la funcionalidad entregada.

5. **Datos de Prueba:** Suministrar datos de prueba realistas y representativos para las pruebas y validaciones.

6. **Usuarios de Prueba:** Designar a usuarios clave para participar en las pruebas y evaluación del sistema.

7. **Aprobación Final:** Aprobar formalmente la solución implementada antes de la puesta en producción.

8. **Capacitación de Usuarios Finales:** Facilitar la capacitación de usuarios finales, asegurando que estén preparados para utilizar la plataforma Salesforce de manera efectiva.

   ## **8.4 Entregables del Equipo de ProContacto \- Etapa de Ejecución** {#8.4-entregables-del-equipo-de-procontacto---etapa-de-ejecución}

* **User Stories (US):** Documentación de los requisitos del cliente en forma de historias de usuario.

* **Configuración de Objetos:** Configuración de objetos personalizados y campos en Salesforce según los requisitos del cliente.

* **Código Personalizado:** Desarrollo de código personalizado cuando sea necesario para cumplir con los requisitos del proyecto.

* **Entregables de Interfaces/Integraciones:** Desarrollo y documentación de las interfaces e integraciones con sistemas externos.

* **Documentación de Entrega de Aplicativo:** Documento técnico acerca de las configuraciones y desarrollos realizados sobre la plataforma de Salesforce.

* **Planes de Testing:** Planificación y documentación de las pruebas de calidad y rendimiento.

* **Planes y Materiales de Capacitación:** Creación de planes de capacitación y materiales para usuarios finales.

* **Documentación de Capacitación:** Documentos informativos sobre cómo utilizar el sistema para usuarios finales.

* **Grabación de Capacitación:** Grabación de sesiones de capacitación para su disponibilidad futura.

# **9\. Cronología** {#9.-cronología}

El completado de la priorización para cada una de las historias de usuario y tareas, contenidas dentro de cada módulo, objeto o funcionalidad será responsabilidad del equipo de Montironi, teniendo en cuenta las prioridades internas que puedan llegar a considerar.

Asimismo, el equipo de ProContacto realizará una priorización de las funcionalidades estipuladas dentro del alcance, así también como aquellas funcionalidades fuera de alcance detectadas durante la etapa de discovery que han pasado por el proceso de control de cambios y posterior agregado al alcance del proyecto. El criterio de la priorización de las funcionalidades mencionadas será según dependencias técnicas que puedan existir por naturaleza propia de toda la plataforma de Salesforce.

Por consiguiente, se realizará una propuesta de roadmap de implementación considerando la priorización brindada por parte del equipo de Montironi y el equipo de ProContacto. La priorización de funcionalidades a desarrollar por parte del equipo de Montironi puede no verse reflejada según su orden dentro del roadmap de implementación, debido a los criterios de priorización establecidos y realizados por parte del equipo de Pro Contacto.Una vez leído, refinado, firmado y aceptado el presente documento “Statement of Work Refinado”, se procederá a la elaboración del roadmap definitivo del proyecto incluyendo fechas de compromiso y los objetivos a cumplir en cada una de estas, teniendo en cuenta lo incluído en el alcance inicial del proyecto y aquellos controles de cambio aceptados por el equipo de Montironi. En cada uno de los sprints se realizará el refinamiento de los requerimientos nombrados en el presente archivo.

# **10\. Controles de Cambio** {#10.-controles-de-cambio}

Los ítems no contemplados en el alcance inicial del proyecto o cambios adicionales que surjan en el desarrollo de la implementación y que afecten alguna configuración, flujo establecido o integración con otros sistemas de información, se tendrán que estimar en cómo impactan a los tiempos de implementación con su estimación de horas de configuración correspondiente.Esta información se escalará al área comercial para que se coticen los cambios adicionales sobre la plataforma y sean enviados a Montironi.

# **11\. Fuera de Alcance \- Release 1.0** {#11.-fuera-de-alcance---release-1.0}

En esta sección se detallan los requerimientos y necesidades identificadas durante la fase de Sprint 0 que, por su naturaleza, exceden el alcance originalmente establecido en el acuerdo comercial inicial. Estos elementos requieren ajustes o desarrollos en los plazos, costos o recursos asignados, en caso de incluirlos al alcance del proyecto.

El equipo de Montironi deberá emitir un veredicto sobre los elementos fuera de alcance detectados, decidiendo si se incorporarán al alcance de la fase actual, se pospondrán para una fase posterior o no serán considerados en ninguna fase. Esta decisión permitirá ajustar la planificación y los recursos en función de las prioridades establecidas.

En caso de que el equipo de Montironi desee incorporar al alcance de la fase actual algún requerimiento o necesidad, se procederá con un tratamiento de los mismos con el área comercial. La adición de requerimientos o necesidades al alcance del proyecto que se adicionen en la fase actual impactará en los tiempos de desarrollo del proyecto.

## **11.1 Automatización Predictiva de Marketing (Marketing Cloud)** {#11.1-automatización-predictiva-de-marketing-(marketing-cloud)}

### **11.1.1 Predictive Journey – Flujo de Administración de Planes** {#11.1.1-predictive-journey-–-flujo-de-administración-de-planes}

**11.1.1.1 Tipo de Funcionalidad: Personalizada**

**11.1.1.2 Narrativa:**

**Como** usuario de Marketing Cloud,  
**quiero** implementar un flujo de Predictive Journey para la "Administración de Planes" que utilice IA para determinar el mejor momento y canal de envío,  
**para** incrementar la tasa de apertura y conversión de comunicaciones dirigidas a clientes con planes activos.

**11.1.1.3 Criterios de Aceptación:**

* El sistema evaluará, mediante un modelo de IA, el historial de interacción de cada cliente para determinar el canal óptimo (email, SMS, push notification) antes de cada envío.  
* Se configurará una cadencia de envío dinámica basada en el nivel de engagement del cliente en los últimos 30 días.  
* El Journey deberá contar con una rama de "Sin respuesta" que reencamine al cliente a un canal alternativo tras 48 horas sin interacción.  
* Se registrarán métricas de apertura, clic y conversión por canal para retroalimentar el modelo de IA.  
* El administrador podrá visualizar en un dashboard de Marketing Cloud el rendimiento predictivo del Journey.

  **11.1.1.4 Consideraciones:**

* Está sujeto a cambios a partir de decisiones internas del Grupo Montironi.

  ### **11.1.2 Predictive Journey – Flujo de Reactivación de Compras** {#11.1.2-predictive-journey-–-flujo-de-reactivación-de-compras}

  **11.1.2.1 Tipo de Funcionalidad: Personalizada**

  **11.1.2.2 Narrativa:**

  **Como** usuario de Marketing Cloud,

  **quiero** implementar un flujo de Predictive Journey para la "Reactivación de Compras" que utilice IA para identificar el momento y canal óptimo de contacto con clientes inactivos,

  **para** aumentar la tasa de reactivación y recuperar oportunidades de venta.

  **11.1.2.3 Criterios de Aceptación:**

* El sistema identificará automáticamente clientes con más de X días sin actividad de compra (umbral configurable) como candidatos para el Journey.  
* La IA determinará el canal de comunicación óptimo (email, SMS, WhatsApp) basándose en el historial de interacciones pasadas.  
* El Journey incluirá al menos 3 nodos de decisión basados en score predictivo: alto, medio y bajo.  
* Se configurarán mensajes personalizados por segmento de score, con contenido diferenciado para cada nivel.  
* Los clientes que no respondan luego de completar el Journey serán enviados automáticamente a una lista de seguimiento manual.

  **11.1.2.4 Consideraciones:**

* Está sujeto a cambios a partir de decisiones internas del Grupo Montironi.

  ### **11.1.3 Segmentación Inteligente – Prospección de Posventa** {#11.1.3-segmentación-inteligente-–-prospección-de-posventa}

  **11.1.3.1 Tipo de Funcionalidad: Personalizada**

  **11.1.3.2 Narrativa:**

  **Como** usuario de Marketing Cloud,

  **quiero** aplicar modelos de IA para segmentar clientes con potencial de compra de posventa,

  **para** realizar campañas de prospección dirigidas y mejorar la eficiencia del equipo comercial.

  **11.1.3.3 Criterios de Aceptación:**

* Se configurará un modelo de segmentación en Data Cloud que analice el historial de comportamiento del cliente (compras anteriores, visitas al taller, interacciones digitales).  
* Los segmentos generados serán exportados automáticamente a Marketing Cloud como audiencias activables.  
* La segmentación se actualizará de forma dinámica con una frecuencia mínima diaria.  
* Cada segmento contará con un score de propensión de compra de posventa visible en el perfil del cliente en Salesforce.  
* El administrador podrá definir y ajustar los criterios del modelo sin intervención técnica, desde la interfaz de Data Cloud.

  **11.1.3.4 Consideraciones:**

* Está sujeto a cambios a partir de decisiones internas del Grupo Montironi.

  ### **11.1.4 Segmentación Inteligente – Reactivación de Presupuestos No Autorizados** {#11.1.4-segmentación-inteligente-–-reactivación-de-presupuestos-no-autorizados}

  **11.1.4.1 Tipo de Funcionalidad: Personalizada**

  **11.1.4.2 Narrativa:**

  **Como** usuario de Marketing Cloud,

  **quiero** utilizar modelos de IA basados en patrones históricos de comportamiento para identificar presupuestos no autorizados con mayor probabilidad de conversión,

  **para** diseñar campañas de reactivación enfocadas y aumentar la tasa de cierre de oportunidades perdidas.

  **11.1.4.3 Criterios de Aceptación:**

* El modelo de IA analizará presupuestos con estado "No Autorizado" y les asignará un score de reactivación basado en variables históricas (tiempo transcurrido, valor del presupuesto, canal de origen, comportamiento digital posterior).  
* Los presupuestos con score superior al umbral configurable serán incluidos automáticamente en el segmento de reactivación.  
* El segmento se sincronizará con Marketing Cloud para su uso en Journeys de reactivación.  
* Se generará un reporte mensual con el rendimiento de la segmentación (presupuestos reactivados vs. totales segmentados).  
* Los presupuestos reactivados exitosamente deberán actualizar su estado en Salesforce CRM de forma automática.

  **11.1.4.4 Consideraciones:**

* Está sujeto a cambios a partir de decisiones internas del Grupo Montironi.

  ### **11.1.5 Observaciones** {#11.1.5-observaciones}

  11.1.5.1 En caso de que el equipo de Montironi decida incluir alguna de estas funcionalidades dentro del alcance, el equipo de ProContacto incurrirá en esfuerzo de estimación, factibilidad y detalle de las mismas, con el fin de escalar al área comercial su tratamiento.

  ### **11.1.6 Estado final** {#11.1.6-estado-final}

  **En revisión**

  ## **11.2 Inteligencia de Datos y Modelos (Data Cloud & Analytics)** {#11.2-inteligencia-de-datos-y-modelos-(data-cloud-&-analytics)}

  ### **11.2.1 Modelado de Prospección Algorítmica – Fase 1** {#11.2.1-modelado-de-prospección-algorítmica-–-fase-1}

  **11.2.1.1 Tipo de Funcionalidad: Personalizada**

  **11.2.1.2 Narrativa:**

  **Como** administrador de Salesforce,

  **quiero** implementar el algoritmo de prospección de posventa dentro del ecosistema Salesforce para la Fase 1,

  **para** identificar proactivamente clientes con mayor potencial de compra y optimizar los esfuerzos del equipo de posventa.

  **11.2.1.3 Criterios de Aceptación:**

* Se deben contar con las licencias necesarias de Analytics para usarlas. (Queda pendiente definir cuántas son necesarias)

* El algoritmo de prospección será configurado dentro de Salesforce utilizando Data Cloud como repositorio central de datos.

* El modelo procesará las variables definidas en el documento de diseño de Fase 1 (historial de compra, kilometraje estimado, antigüedad del vehículo, entre otros).

* Los resultados del algoritmo serán almacenados como un campo de "Score de Prospección" visible en el registro del cliente (Account/Contact) en Salesforce.

* El score se actualizará automáticamente según la frecuencia definida en el diseño (mínimo semanal).

* Se realizará una validación inicial del modelo contra datos históricos para verificar una tasa de acierto mínima acordada con el cliente.

  ### **11.2.2 Análisis de Cartera con IA – Dashboards Predictivos CRM Analytics** {#11.2.2-análisis-de-cartera-con-ia-–-dashboards-predictivos-crm-analytics}

  **11.2.2.1 Tipo de Funcionalidad: Personalizada**

  **11.2.2.2 Narrativa:**

  **Como** gerente comercial o de posventa,

  **quiero** contar con dashboards predictivos en CRM Analytics que muestren riesgo de fuga, análisis de detractores y proyecciones de fin de crédito,

  **para** tomar decisiones estratégicas informadas sobre la gestión de la cartera de clientes.

  **11.2.2.3 Criterios de Aceptación:**

* Se debe contar con las licencias de Analytics necesarias para los usuarios (Queda pendiente definir cuántas son necesarias)

* Se crearán al menos 3 dashboards en CRM Analytics: (1) Riesgo de Fuga, (2) Análisis de Detractores NPS, y (3) Proyecciones de Fin de Crédito.  
* Cada dashboard incluirá filtros interactivos por período, sucursal/concesionario y segmento de cliente.  
* El dashboard de Riesgo de Fuga mostrará un ranking de clientes por nivel de riesgo (alto, medio, bajo) con los principales indicadores que lo determinan.  
* El dashboard de Detractores mostrará la distribución geográfica y temporal de las respuestas negativas en encuestas NPS.  
* El dashboard de Fin de Crédito proyectará los vencimientos de crédito en los próximos 30, 60 y 90 días.  
* Los dashboards tendrán acceso segmentado por perfil de usuario (gerente regional, gerente de sucursal, ejecutivo de cuenta).

  ### **11.2.3 Unificación de Datos para IA – Configuración de Data Cloud** {#11.2.3-unificación-de-datos-para-ia-–-configuración-de-data-cloud}

  **11.2.3.1 Tipo de Funcionalidad: Personalizada**

  **11.2.3.2 Narrativa:**

  **Como** administrador de Salesforce,

  **quiero** configurar Data Cloud como repositorio central de datos limpios para alimentar los modelos de IA de posventa y ventas tradicionales,

  **para** garantizar que los algoritmos de IA operen con datos unificados, actualizados y de alta calidad.

  **11.2.3.3 Criterios de Aceptación:**

* Se configurarán los Data Streams necesarios para ingestar datos de posventa y ventas tradicionales desde las fuentes definidas en el diseño (CRM, ERP u otros sistemas).  
* Se definirá y configurará el modelo de datos unificado (Unified Individual / Unified Account) en Data Cloud para consolidar identidades de clientes duplicados o fragmentados.  
* Se implementarán reglas de transformación y limpieza de datos para garantizar consistencia en los campos críticos para los modelos de IA.  
* Se establecerá un proceso de monitoreo de calidad de datos con alertas configurables para campos con alto índice de nulidad o inconsistencia.  
* Los segmentos de Data Cloud estarán disponibles para activación en Marketing Cloud y CRM Analytics en tiempo real o near-real-time según lo acordado.

  ### **11.2.4 Observaciones** {#11.2.4-observaciones}

  11.2.4.1 En caso de que el equipo de Montironi decida incluir alguna de estas funcionalidades dentro del alcance, el equipo de ProContacto incurrirá en esfuerzo de estimación, factibilidad y detalle de las mismas, con el fin de escalar al área comercial su tratamiento.

  ### **11.2.5 Estado final** {#11.2.5-estado-final}

  **En revisión**

  ## **11.3 Flujos de Trabajo Inteligentes (Flow Builder)** {#11.3-flujos-de-trabajo-inteligentes-(flow-builder)}

  ### **11.3.1 Automatización de Calidad – Planes de Acción tras Detractores NPS** {#11.3.1-automatización-de-calidad-–-planes-de-acción-tras-detractores-nps}

  **11.3.1.1 Tipo de Funcionalidad: Personalizada**

  **11.3.1.2 Narrativa:**

  **Como** administrador de Salesforce,

  **quiero** implementar flujos automatizados (Flow Builder) con lógica de IA que detecten respuestas detractoras en encuestas NPS y generen planes de acción automáticos,

  **para** gestionar de forma proactiva la insatisfacción del cliente y reducir el riesgo de churn.

  **11.3.1.3 Criterios de Aceptación:**

* El Flow se disparará automáticamente cuando se registre una respuesta NPS con score menor o igual a 6 (detractor).  
* El sistema clasificará al detractor según el motivo de insatisfacción (análisis de texto libre o categorías predefinidas) y seleccionará la plantilla de plan de acción correspondiente.  
* Se creará automáticamente un registro de "Plan de Acción" en Salesforce con el responsable asignado, la fecha límite de gestión y las acciones recomendadas.  
* Se enviará una notificación automática al responsable de gestión del cliente y a su supervisor inmediato.  
* Si el plan de acción no es atendido dentro del SLA definido (configurable), el sistema escalará automáticamente al siguiente nivel jerárquico.  
* Se generará un reporte mensual de planes de acción por NPS, estado y tiempo de resolución.

  ### **11.3.2 Optimización Logística – Seguimiento Automatizado de Traslados** {#11.3.2-optimización-logística-–-seguimiento-automatizado-de-traslados}

  **11.3.2.1 Tipo de Funcionalidad: Personalizada**

  **11.3.2.2 Narrativa:**

  **Como** usuario de operaciones,

  **quiero** contar con flujos automatizados en Salesforce (Flow Builder) para el seguimiento de traslados de vehículos,

  **para** minimizar errores manuales en la carga de datos y tener visibilidad en tiempo real del estado de cada traslado.

  **11.3.2.3 Criterios de Aceptación:**

* El Flow gestionará el ciclo de vida del traslado de vehículos desde la solicitud hasta la confirmación de recepción.  
* Se validarán automáticamente los campos obligatorios antes de permitir la selección del campo registro de traslado sobre el objeto Vehículo, mostrando mensajes de error descriptivos ante datos faltantes o incorrectos.  
* El sistema actualizará automáticamente el estado del traslado (En Tránsito, Recibido, Demorado) según los eventos registrados.  
* Se enviarán notificaciones automáticas a los responsables logísticos ante cambios de estado críticos (demora, recepción confirmada).  
* Se generará un log de auditoría automático con cada cambio de estado del traslado, registrando usuario, fecha y datos modificados.  
* El Flow prevendrá la duplicación de registros de traslado para el mismo vehículo en el mismo período.

  ### **11.3.3 Observaciones** {#11.3.3-observaciones}

  11.3.3.1 En caso de que el equipo de Montironi decida incluir alguna de estas funcionalidades dentro del alcance, el equipo de ProContacto incurrirá en esfuerzo de estimación, factibilidad y detalle de las mismas, con el fin de escalar al área comercial su tratamiento.

  ### **11.3.4 Estado final** {#11.3.4-estado-final}

  **En revisión**

  ## **11.4 Objeto "Plan de Ahorro"** {#11.4-objeto-"plan-de-ahorro"}

  ### **11.4.1 Creación del Objeto Plan de Ahorro** {#11.4.1-creación-del-objeto-plan-de-ahorro}

  **11.4.1.1 Tipo de Funcionalidad: Personalizada**

  **11.4.1.2 Narrativa:**

  **Como** administrador de Salesforce,

  **quiero** crear el objeto custom "Plan de Ahorro" en Salesforce con sus campos y relación a Oportunidad,

  **para** llevar un control centralizado del pago de planes de ahorro dentro del CRM.

  **11.4.1.3 Criterios de Aceptación:**

* El objeto "Plan de Ahorro" deberá crearse como objeto custom en Salesforce con los campos: Cantidad Máxima de Clientes, Vehículo, Fecha de Inicio, Monto de Cuota, Número Total de Cuotas, Estado, y los campos adicionales definidos en el Diccionario de Datos.  
* El objeto tendrá una relación Lookup o Master-Detail con el objeto Oportunidad (configurable según la necesidad de eliminar en cascada).  
* El campo Estado deberá ser un picklist con los valores: "Activo", "En Espera de Pago", "Dado de Baja" y "Pagado".  
* Se configurarán las reglas de validación necesarias para garantizar que los campos obligatorios sean completados al crear un registro.  
* El perfil de usuario correspondiente tendrá acceso de lectura/escritura al objeto según el rol definido en el diseño de seguridad.  
* Se configurará el layout del registro de Plan de Ahorro para mostrar los campos principales y la lista relacionada de Cuotas.

  ### **11.4.2 Automatización de Baja de Plan de Ahorro por Cuotas Impagas** {#11.4.2-automatización-de-baja-de-plan-de-ahorro-por-cuotas-impagas}

  **11.4.2.1 Tipo de Funcionalidad: Personalizada**

  **11.4.2.2 Narrativa:**

  **Como** administrador de Salesforce,

  **quiero** implementar una automatización que detecte cuando las últimas 5 cuotas de un Plan de Ahorro no están pagas y cambie el estado del plan a "Dado de Baja" automáticamente,

  **para** mantener la cartera de planes actualizada sin intervención manual.

  **11.4.2.3 Criterios de Aceptación:**

* La automatización evaluará diariamente (o en tiempo real ante cada actualización de cuota) si las últimas 5 cuotas consecutivas del Plan de Ahorro tienen estado impago.  
* Si las 5 últimas cuotas consecutivas están impagas, el estado del Plan de Ahorro se actualizará automáticamente a "Dado de Baja".  
* Se registrará la fecha de baja automática en un campo "Fecha de Baja" del objeto Plan de Ahorro.  
* Se enviará una notificación al responsable del plan y al cliente informando la baja automática.  
* La automatización generará un registro de actividad en el Plan de Ahorro documentando el motivo de la baja (cuotas impagas).  
* No se podrá dar de baja manualmente un plan con cuotas al día; el sistema mostrará un mensaje de error si se intenta.

  ### **11.4.3 Reactivación de Plan de Ahorro Dado de Baja** {#11.4.3-reactivación-de-plan-de-ahorro-dado-de-baja}

  **11.4.3.1 Tipo de Funcionalidad: Personalizada**

  **11.4.3.2 Narrativa:**

  **Como** ejecutivo comercial,

  **quiero** poder reactivar un Plan de Ahorro que fue dado de baja, previa verificación del pago de las cuotas pendientes,

  **para** brindar al cliente la posibilidad de continuar su plan de ahorro sin perder su historial de pagos.

  **11.4.3.3 Criterios de Aceptación:**

* El sistema calculará automáticamente el monto de reactivación: cuotas impagas que originaron la baja más cuotas que debían pagarse durante el período en que el plan estuvo dado de baja.  
* Solo un usuario con el perfil/rol habilitado podrá iniciar el proceso de reactivación de un Plan de Ahorro con estado "Dado de Baja".  
* El cambio de estado a "Activo" solo será posible una vez que se registre el pago completo del monto de reactivación calculado.  
* El sistema registrará la fecha de reactivación y el monto total pagado en el objeto Plan de Ahorro.  
* Se generará automáticamente un registro de actividad documentando la reactivación, el período de baja y las cuotas pagadas para completar la reactivación.  
* El historial de cuotas del plan (pagas e impagas) se conservará íntegramente tras la reactivación.

  ### **11.4.4 Observaciones** {#11.4.4-observaciones}

  11.4.4.1 En caso de que el equipo de Montironi decida incluir alguna de estas funcionalidades dentro del alcance, el equipo  de ProContacto incurrirá en esfuerzo de estimación, factibilidad y detalle de las mismas, con el fin de escalar al área comercial su tratamiento.

  ### **11.4.5 Estado final** {#11.4.5-estado-final}

  **En revisión**

  ## **11.5 Objeto "Cuota"** {#11.5-objeto-"cuota"}

  ### **11.5.1 Creación del Objeto Cuota** {#11.5.1-creación-del-objeto-cuota}

  **11.5.1.1 Tipo de Funcionalidad: Personalizada**

  **11.5.1.2 Narrativa:**

  **Como** administrador de Salesforce,

  **quiero** crear el objeto custom "Cuota" relacionado al objeto "Plan de Ahorro",

  **para** registrar y controlar cada pago individual realizado en el marco de un plan de ahorro.

  **11.5.1.3 Criterios de Aceptación:**

* El objeto "Cuota" deberá crearse como objeto custom con los campos: Monto, Fecha de Pago, Fecha Límite, Estado (Pagada / Pendiente / Vencida), y un campo checkbox "Pagada Fuera de Tiempo".  
* El objeto Cuota tendrá una relación Master-Detail con el objeto "Plan de Ahorro", permitiendo múltiples registros de Cuota por Plan de Ahorro.  
* El campo "Pagada Fuera de Tiempo" se marcará automáticamente como verdadero cuando la Fecha de Pago sea posterior a la Fecha Límite de la cuota.  
* Se configurará una lista relacionada de Cuotas en el layout del objeto Plan de Ahorro mostrando al menos: número de cuota, monto, fecha límite, fecha de pago y estado.  
* Se configurarán reglas de validación para impedir que se registre una fecha de pago futura al crear una cuota como pagada.  
* El perfil de usuario correspondiente tendrá acceso de lectura/escritura al objeto según el rol definido.

  ### **11.5.2 Observaciones** {#11.5.2-observaciones}

  11.5.2.1 En caso de que el equipo de Montironi decida incluir alguna de estas funcionalidades dentro del alcance, el equipo  de ProContacto incurrirá en esfuerzo de estimación, factibilidad y detalle de las mismas, con el fin de escalar al área comercial su tratamiento.

  ### **11.5.3 Estado final** {#11.5.3-estado-final}

  **En revisión**

  ## **11.6 Objeto "Licitación"** {#11.6-objeto-"licitación"}

  ### **11.6.1 Creación del Objeto Licitación** {#11.6.1-creación-del-objeto-licitación}

  **11.6.1.1 Tipo de Funcionalidad: Personalizada**

  **11.6.1.2 Narrativa:**

  **Como** administrador de Salesforce,

  **quiero** crear el objeto custom "Licitación" relacionado al objeto "Plan de Ahorro",

  **para** registrar y gestionar las licitaciones asociadas a cada plan de ahorro dentro del CRM.

  **11.6.1.3 Criterios de Aceptación:**

* El objeto "Licitación" deberá crearse como objeto custom con los campos: Nombre, Fecha de Licitación, Estado (picklist: "Creada", "Rechazada", "Aprobada"), Plan de Ahorro (lookup/master-detail), Incluye Vehículo Usado (checkbox), y los campos adicionales definidos en el Diccionario de Datos.  
* Se podrán crear múltiples licitaciones para un mismo Plan de Ahorro, siempre que no exista una licitación con estado "Aprobada" para ese plan.  
* Una regla de validación o automatización impedirá la creación de una nueva Licitación para un Plan de Ahorro que ya tenga una Licitación aprobada, mostrando un mensaje de error descriptivo.  
* Se configurará el layout del registro de Licitación con los campos relevantes y se agregará la lista relacionada en el layout del Plan de Ahorro.  
* El campo Estado comenzará con valor "Creada" al crear un nuevo registro y solo podrá avanzar según el flujo de estados definido.

  ### **11.6.2 Integración con Fábrica al Crear Licitación** {#11.6.2-integración-con-fábrica-al-crear-licitación}

  **11.6.2.1 Tipo de Funcionalidad: Personalizada**

  **11.6.2.2 Narrativa:**

  **Como** administrador de Salesforce,

  **quiero** implementar una integración automática que envíe los datos de una nueva Licitación al sistema externo "Fábrica" al momento de su creación,

  **para** que los datos sean analizados en el sistema externo sin necesidad de intervención manual.

  **11.6.2.3 Criterios de Aceptación:**

* Al crearse un nuevo registro de Licitación (estado "Creada") que NO incluya vehículo usado, se disparará automáticamente el proceso de integración hacia el sistema externo "Fábrica".  
* La integración enviará los datos definidos en el contrato de interfaz acordado con el equipo de Fábrica (campos mínimos a definir en el diseño técnico).  
* En caso de error en el envío (timeout, error HTTP, etc.), el sistema reintentará según la política de reintentos definida (mínimo 3 intentos) y notificará al administrador si persiste el fallo.  
* Se registrará el resultado de la integración (éxito/fallo, timestamp, respuesta del sistema externo) en el registro de la Licitación en Salesforce.  
* Las licitaciones que incluyan vehículo usado NO se enviarán a Fábrica hasta que completen el flujo de aprobación de tasación (ver HU Flujo de Aprobación de Tasación).  
* El administrador podrá reintentar manualmente el envío desde el registro de la Licitación en caso de fallo.

  ### **11.6.3 Flujo de Aprobación de Tasación de Vehículo Usado en Licitación** {#11.6.3-flujo-de-aprobación-de-tasación-de-vehículo-usado-en-licitación}

  **11.6.3.1 Tipo de Funcionalidad: Personalizada**

  **11.6.3.2 Narrativa:**

  **Como** responsable del área de tasación,

  **quiero** contar con un flujo de aprobación en Salesforce para las licitaciones que incluyan un vehículo usado como parte de pago,

  **para** garantizar que la tasación del vehículo sea validada por el rol correspondiente antes de enviar la licitación al sistema externo Fábrica.

  **11.6.3.3 Criterios de Aceptación:**

* Cuando se cree o actualice una Licitación con el campo "Incluye Vehículo Usado" marcado como verdadero, el sistema no enviará los datos a Fábrica de forma automática.  
* Se iniciará un proceso de aprobación en Salesforce dirigido al rol de tasación definido en el diseño de seguridad.  
* El tasador podrá aprobar o rechazar la tasación directamente desde el registro de la Licitación en Salesforce o desde el email de notificación de aprobación.  
* Si la tasación es aprobada, el estado de la Licitación avanzará al estado correspondiente y se disparará automáticamente la integración con Fábrica.  
* Si la tasación es rechazada, el estado de la Licitación pasará a "Rechazada" y se notificará al creador con los comentarios del tasador.  
* Se registrará en el historial del registro de Licitación cada acción del proceso de aprobación (solicitado, aprobado, rechazado) con fecha, hora y usuario responsable.

  ### **11.6.4 Observaciones** {#11.6.4-observaciones}

  11.6.4.1 En caso de que el equipo de Montironi decida incluir alguna de estas funcionalidades dentro del alcance, el equipo  de ProContacto incurrirá en esfuerzo de estimación, factibilidad y detalle de las mismas, con el fin de escalar al área comercial su tratamiento.

  ### **11.6.5 Estado final** {#11.6.5-estado-final}

  **En revisión**

# **12\. Aprobaciones** {#12.-aprobaciones}

## **12.1 Individuos que necesitan aprobar el SOW antes de que pueda implementarse** {#12.1-individuos-que-necesitan-aprobar-el-sow-antes-de-que-pueda-implementarse}

| Nombre | Rol | Aprobación |
| :---: | :---: | :---: |
| Romina Pilar Borrani | COO | Aprobado |
| Andres Linares | Lider de Software | Aprobado  |

