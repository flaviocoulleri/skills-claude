  
**Statement of Work Refinado**

Guillermo Morales · Implementación Salesforce

Salesforce Sales Cloud  ·  Agentforce  ·  Marketing Cloud on Core

| Nombre del sistema | Tipo de documento | Versión | Fecha |
| :---- | :---- | :---- | :---- |
| Salesforce | Statement of Work Refinado | 1.0 | Junio 2026 |

**Preparado por: ProContacto  ·  Versión 1.0  ·  Junio 2026**

# **Control de versiones**

| Versión \# | Fecha de entrega | Creado por | Resumen de cambios |
| :---- | :---- | :---- | :---- |
| 1.0 | Junio 2026 | Lucas SeguraAccount Executive – ProContacto | Primera versión |

# **Índice**

1\. Introducción

2\. Glosario de términos

3\. Sales Cloud – Alcance de Implementación

    3.1 Modelo de Roles, Perfiles y Visibilidad

    3.2 Gestión de Leads

    3.3 Gestión de Cuentas Estándar

    3.4 Gestión de Contactos Estándar

    3.5 Gestión de Vehículos de Interés (Custom)

    3.6 Gestión de Oportunidades Estándar

    3.7 Gestión de Cotizaciones Estándar

    3.8 Gestión de Productos y Listas de Precios

    3.9 Gestión de Actividades

    3.10 Encuestas de Satisfacción (NPS)

    3.11 Reportería y Dashboards

4\. Marketing Cloud on Core – Alcance de Implementación

5\. Integraciones con Sistemas Externos

6\. Service Cloud / Omni-Channel

7\. Agentforce (Agentes de IA)

8\. Entregables – Etapas posteriores

9\. Cronología

10\. Controles de Cambio

11\. Fuera de Alcance – Release 1.0

12\. Aprobaciones

# **1\. Introducción**

El presente documento está orientado a brindar una descripción sobre el entendimiento de los requerimientos proporcionados para el desarrollo de la plataforma Salesforce en Guillermo Morales, concesionario multimarca con operaciones en Chile. Se pautarán qué consideraciones se tomarán en cuenta para dicho desarrollo, así como un entendimiento del proceso de trabajo, restricciones de negocio, automatizaciones, integraciones con sistemas externos, entre otros.

Se establecerá una delimitación clara del alcance del proyecto. El desarrollo de cualquier requerimiento o consideración no incluida en este documento — ya sea funcionalidad, automatización, validación, flujo o integración con otros sistemas — implica un esfuerzo adicional. Por lo tanto, los elementos no mencionados en este documento estarán fuera del alcance del proyecto.

Este SOW cubre la Fase 1 del proyecto, enfocada exclusivamente en la línea de negocio de venta de autos nuevos. Las líneas de autos usados y servicio postventa quedan como hito de fases posteriores.

Es importante tener en cuenta que este documento servirá como referencia para el desarrollo, configuración y personalización del entorno de Salesforce. Se espera que el equipo de implementación de ProContacto trabaje en estrecha colaboración con Guillermo Morales para asegurar una comprensión y alineación claras de los objetivos, requisitos y restricciones del proyecto.

# **2\. Glosario de términos**

| Concepto | Definición |
| :---- | :---- |
| Nube | Instancia de la plataforma Salesforce que ofrece servicios específicos para un área de negocio (ventas, marketing, servicio al cliente). |
| Integración | Conexión y sincronización de Salesforce con otros sistemas o herramientas utilizados por la empresa. |
| Alcance | Todas las características, entregables, objetivos y requisitos que se deben cumplir para considerar el proyecto completado con éxito. |
| Desvío | Requerimiento adicional no incluido en el alcance inicial, detectado durante el relevamiento. |
| Control de cambio | Proceso para gestionar y controlar los cambios en el sistema, minimizando riesgos. |
| Sprint | Período de tiempo fijo (2 semanas) en el cual se realiza trabajo concentrado y se entregan incrementos de funcionalidad. |
| Sprint 0 | Período previo a la implementación para relevamiento, entendimiento del negocio y corroboración del alcance. |
| UAT | User Acceptance Testing – Pruebas realizadas por los usuarios finales para validar el funcionamiento del sistema. |
| DDD | Diccionario de Datos de Diseño – Documento que especifica los campos, objetos y relaciones del modelo de datos. |
| SLA | Service Level Agreement – Tiempo máximo acordado para realizar una acción en cada etapa del embudo comercial. |
| Lead | Prospecto o cliente potencial que ingresa al sistema y aún no ha sido convertido en una oportunidad formal. |
| Oportunidad | Registro en Salesforce que representa un proceso de venta activo con alta probabilidad de concreción. |
| Cotización | Documento formal que refleja precio, bonos y condiciones de financiamiento ofrecidos al cliente. |
| Score IA | Clasificación automática del lead por Agentforce como frío, tibio o caliente, basada en datos de la conversación y formulario. |
| SIGA | ERP corporativo de Guillermo Morales que gestiona inventario, cotizaciones oficiales, notas de venta y facturación. |
| Frogmi | Plataforma de checklist de entrega de vehículos utilizada por el grupo Astara en Chile. |
| Omega CTI | Sistema de contact center telefónico integrado con Salesforce para gestión de llamadas. |
| Autorred | Plataforma externa de tasación de vehículos usados. |
| Agentforce | Motor de Inteligencia Artificial de Salesforce para automatización de atención y calificación de leads 24/7. |
| UTM | Parámetros de rastreo de campañas digitales (fuente, medio, campaña, contenido, término). |
| Journey | Secuencia automatizada de mensajes en diferentes canales con lógica basada en el comportamiento del receptor. |
| NPS | Net Promoter Score – Métrica de satisfacción del cliente medida mediante encuestas post test-drive y post entrega. |

# **3\. Sales Cloud – Alcance de Implementación**

Se detallan a continuación los requerimientos detectados y evaluados a un alto nivel de detalle, teniendo en cuenta la definición total del requerimiento en etapas posteriores de refinamiento, los permisos sobre la plataforma, el alcance del requerimiento y las integraciones involucradas.

## **3.1 Modelo de Roles, Perfiles y Visibilidad**

Como parte de la implementación de Salesforce Sales Cloud y Marketing Cloud on Core para Guillermo Morales, es necesario definir y configurar un modelo de roles, perfiles y visibilidad que asegure:

* Correcta segregación de datos por marca, sucursal y rol.

* Control del proceso comercial de autos nuevos.

* Protección de la información sensible entre marcas y sucursales.

* Escalabilidad del modelo para fases posteriores (usados, servicio).

Esta épica contempla la definición funcional y técnica del modelo de seguridad base, alineado a las buenas prácticas de Salesforce y a la operación actual de Guillermo Morales.

### **3.1.1 Definir roles funcionales del sistema**

**3.1.1.1 Narrativa:**

*Como equipo de proyecto,*

*quiero definir los roles funcionales que utilizarán Sales Cloud,*

*para asegurar una correcta asignación de permisos, visibilidad y responsabilidades en el proceso comercial.*

**3.1.1.2 Criterios de Aceptación:**

* Roles definidos y validados por Guillermo Morales:

  * Gerente Regional / Gerente General

  * Gerente de Sucursal

  * Ejecutivo de Ventas

  * Ejecutivo Digital (contact center / canal digital)

  * Jefe de Crédito

  * Gerente de Marketing

  * Administrador Salesforce (Guillermo Morales)

* La cantidad exacta de roles y perfiles, junto con sus permisos detallados, será definida en el Sprint 0\.

### **3.1.2 Definir permisos sobre Leads**

**3.1.2.1 Narrativa:**

*Como Administrador Salesforce,*

*quiero definir permisos por rol sobre el objeto Lead,*

*para controlar creación, edición, asignación, avance de etapa y cierre.*

**3.1.2.2 Criterios de Aceptación:**

* Ejecutivo Digital: crea y edita leads de su bandeja; puede reasignar; no puede eliminar.

* Ejecutivo de Ventas: edita únicamente los leads asignados a sí mismo; no puede eliminar.

* Gerente de Sucursal: ve y edita leads de su sucursal; puede reasignar dentro de la sucursal.

* Gerente Regional / General: acceso de lectura total; puede reasignar entre sucursales.

* Administrador: acceso completo.

### **3.1.3 Definir permisos sobre Cuentas, Contactos y Oportunidades**

**3.1.3.1 Narrativa:**

*Como Administrador Salesforce,*

*quiero definir permisos por rol sobre Cuentas, Contactos y Oportunidades,*

*para asegurar trazabilidad y calidad del dato una vez avanzado el proceso de venta.*

**3.1.3.2 Criterios de Aceptación:**

* Ejecutivo de Ventas: lectura y edición de registros propios de su sucursal y marca.

* Gerente de Sucursal: lectura y edición de todos los registros de su sucursal.

* Gerente Regional: lectura y edición de todas las sucursales bajo su jurisdicción.

* Administrador: acceso completo.

### **3.1.4 Definir modelo de visibilidad por marca y sucursal**

**3.1.4.1 Narrativa:**

*Como Gerente de Sucursal,*

*quiero que los usuarios visualicen solo información de su marca o sucursal,*

*para mantener foco comercial, evitar contaminación de datos entre marcas y asegurar el orden operativo.*

**3.1.4.2 Criterios de Aceptación:**

* Modelo de visibilidad documentado y validado por Guillermo Morales.

* Los ejecutivos solo ven registros de la marca y sucursal a la que están asignados.

* Los gerentes de sucursal ven información agregada de su sucursal.

* Los gerentes regionales ven información de todas las sucursales bajo su responsabilidad.

* No existe visibilidad cruzada no autorizada entre marcas distintas en la misma sucursal.

**3.1.4.3 Consideraciones:**

* La definición de la cantidad de perfiles y sus permisos específicos será responsabilidad del equipo de Guillermo Morales durante el Sprint 0\.

### **3.1.5 Configurar jerarquía de roles comerciales**

**3.1.5.1 Narrativa:**

*Como Administrador Salesforce,*

*quiero configurar la jerarquía de roles en Salesforce,*

*para permitir visibilidad escalonada hacia arriba, reportería correcta y acceso apropiado por nivel.*

**3.1.5.2 Criterios de Aceptación:**

* Jerarquía definida y configurada según el organigrama validado en Sprint 0\.

* Los gerentes de sucursal ven la información de sus equipos.

* No hay visibilidad cruzada no autorizada entre sucursales.

* La jerarquía soporta el crecimiento de la organización sin reestructuración mayor.

## **3.2 Gestión de Leads**

Guillermo Morales recibe entre 3.000 y 5.000 leads mensuales provenientes de múltiples fuentes: formularios web propios, campañas de Google Ads y Meta, leads de marcas Astara enviados desde Salesforce Astara, y llamadas entrantes gestionadas por el contact center a través de Omega CTI. Salesforce actuará como único repositorio central de todos los leads.

### **3.2.1 Almacenar información de Leads**

**3.2.1.1 Narrativa:**

*Como ejecutivo digital,*

*quiero almacenar la información relevante de cada lead ingresado al sistema,*

*para gestionar su calificación y seguimiento de forma centralizada.*

**3.2.1.2 Criterios de Aceptación:**

* Se deberá poder almacenar la información definida en el DDD asociada a un Lead.

* Se deberá asignar el vehículo de interés (marca, modelo, variante) al lead.

* Se deberán registrar los parámetros de origen: fuente, sub-fuente y canal de ingreso.

* Se implementará la herramienta de Chatter en la ficha del Lead.

* Campos obligatorios según DDD: nombre, apellido, teléfono (con código de país), correo electrónico, RUT, origen, marca de interés.

* El sistema validará que los campos obligatorios estén completos antes de guardar.

### **3.2.2 Buscar y visualizar Leads existentes**

**3.2.2.1 Narrativa:**

*Como ejecutivo digital,*

*quiero buscar y visualizar los Leads existentes por distintos campos,*

*para gestionar mis prospectos de manera efectiva sin necesidad de sistemas adicionales.*

**3.2.2.2 Criterios de Aceptación:**

* La ficha del Lead debe mostrar: datos personales, vehículo de interés, origen y UTM, score IA, historial de interacciones, actividades programadas y documentos adjuntos.

* Por defecto se visualizan los leads de la marca y sucursal asignada al ejecutivo.

* El ejecutivo digital puede ver todos los leads de su cola sin importar la marca.

* Los perfiles administrativos y gerenciales tienen acceso ampliado según su rol.

### **3.2.3 Crear Leads manualmente en Salesforce**

**3.2.3.1 Narrativa:**

*Como ejecutivo digital o ejecutivo de ventas,*

*quiero registrar prospectos que llegan directamente al concesionario o por medios no automatizados,*

*para asegurar que ningún prospecto quede fuera del sistema.*

**3.2.3.2 Criterios de Aceptación:**

* La creación del Lead será de forma manual desde la interfaz de Salesforce.

* El formulario respetará los campos definidos en el DDD para la marca seleccionada.

* Los campos obligatorios deberán estar completos para poder crear el registro.

* El Lead se asociará automáticamente al ejecutivo logueado o a la cola correspondiente.

* Se deberá registrar la fuente de ingreso (visita presencial, llamada entrante, referido, etc.).

### **3.2.4 Actualizar información de Leads**

**3.2.4.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero completar y actualizar datos adicionales del Lead a medida que interactúo con el prospecto,*

*para enriquecer su perfil y mejorar la calidad de la calificación.*

**3.2.4.2 Criterios de Aceptación:**

* El usuario podrá modificar los campos opcionales del lead.

* Los campos obligatorios no podrán quedar vacíos tras una actualización.

* Se debe registrar el historial de cambios por usuario y fecha.

* El sistema mostrará un mensaje de error si se intenta guardar sin completar los campos obligatorios.

### **3.2.5 Asignación automática de Leads**

**3.2.5.1 Narrativa:**

*Como administrador de ventas,*

*quiero que los Leads se asignen automáticamente al vendedor más idóneo,*

*para optimizar la velocidad de contacto y las probabilidades de conversión.*

**3.2.5.2 Criterios de Aceptación:**

* El sistema ejecutará reglas de asignación al momento de crear un lead, considerando: marca de interés, sucursal más cercana al cliente y carga de trabajo actual del vendedor.

* Si ninguna regla coincide, el lead se asignará a un usuario de respaldo predefinido (a definir en Sprint 0).

* Los leads no asignados deben quedar con estado 'No Asignado' y ser visibles en una lista compartida para ser tomados manualmente.

* Se debe registrar la fecha y hora de asignación y de toma del lead por el ejecutivo.

### **3.2.6 Establecer proceso de trabajo del Lead (Funnel Comercial)**

**3.2.6.1 Narrativa:**

*Como usuario,*

*quiero gestionar el lead a través de un proceso de trabajo definido por etapas,*

*para tener trazabilidad del avance de cada prospecto en el embudo y facilitar la gestión comercial.*

**3.2.6.2 Criterios de Aceptación:**

* Se establecerá el siguiente proceso de trabajo para los Leads:

  * No Asignado: el prospecto ingresa al sistema y queda en cola pendiente de asignación.

  * Calificación: Agentforce analiza el lead y asigna score. El ejecutivo digital verifica la calidad del dato.

  * Contacto Comercial: el vendedor realiza el primer contacto, entrega promoción y busca agendar visita.

  * Experiencia: el cliente visita la sucursal, realiza el test drive y se genera la cotización formal.

  * Negociación: el vendedor negocia precio, bonos y forma de pago con el cliente.

  * Pago: se acuerda la modalidad de pago y SIGA registra la nota de venta.

  * Entrega: Frogmi ejecuta el checklist de entrega; Salesforce cierra la oportunidad 24h después.

  * Cerrado Ganado / Cerrado Perdido: estados finales del proceso.

* La transición entre etapas será manual por parte del vendedor, salvo las transiciones automáticas disparadas por integraciones (SIGA, Frogmi).

* El sistema brindará ayuda textual al usuario en cada etapa (máximo 2.000 caracteres por etapa).

* Se podrán configurar hasta 5 campos clave visibles por etapa para facilitar el acceso a información crítica.

* Las restricciones de transición entre estados se definirán en el Sprint 0\.

### **3.2.7 Detectar Leads duplicados**

**3.2.7.1 Narrativa:**

*Como ejecutivo digital,*

*quiero que el sistema detecte automáticamente leads potencialmente duplicados,*

*para evitar la creación de registros redundantes y el doble trabajo.*

**3.2.7.2 Criterios de Aceptación:**

* El sistema identificará duplicados en base a: RUT, teléfono y correo electrónico (aplicables individualmente).

* Al detectar un duplicado durante la creación, el sistema mostrará un mensaje de advertencia con el registro existente.

* En la ficha del Lead ya existente, se mostrará un banner indicando la posible duplicación.

* Solo perfiles administrativos podrán ver duplicados entre distintas sucursales o marcas.

### **3.2.8 Enviar notificación cuando se genera o reasigna el Lead**

**3.2.8.1 Narrativa:**

*Como usuario,*

*quiero recibir una notificación cuando se crea un nuevo lead o se le asigna uno,*

*para reaccionar de inmediato y no perder tiempo de contacto.*

**3.2.8.2 Criterios de Aceptación:**

* Al crearse un nuevo Lead en estado 'No Asignado' o asignarse a un ejecutivo, se generará una notificación interna en Salesforce.

* El destinatario de la alerta será el ejecutivo asignado y/o el gerente de sucursal.

* La notificación redirigirá al registro del Lead al hacer clic sobre ella.

* El texto de la alerta seguirá el formato: 'Nuevo lead asignado: \[Nombre del lead\] – \[Marca de interés\]'.

### **3.2.9 Seguimiento y agendamiento de actividades con Leads**

**3.2.9.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero registrar llamadas, tareas y citas asociadas a un lead,*

*para dar seguimiento eficiente hasta la conversión sin salir de Salesforce.*

**3.2.9.2 Criterios de Aceptación:**

* Las actividades se registrarán como Tasks o Events asociadas al Lead.

* Salesforce mostrará en el panel de actividades: llamadas realizadas, próximas tareas y reuniones pendientes.

* Se permitirá reprogramar, marcar como completada o delegar una tarea.

* Las llamadas registradas desde Omega CTI se vincularán automáticamente al Lead como actividades.

**3.2.9.3 Consideraciones:**

* Todas las funcionalidades de integración con Omega CTI descritas en esta historia están supeditadas al conector que Omega disponibilice para Salesforce Lightning. Este conector es un supuesto del proyecto; las capacidades disponibles se confirmarán durante el Sprint 0\.

### **3.2.10 Captura y registro de parámetros UTM**

**3.2.10.1 Narrativa:**

*Como equipo de marketing,*

*quiero registrar automáticamente los parámetros UTM de cada lead digital,*

*para medir el costo por adquisición y la tasa de conversión por canal y campaña sin generar planillas manuales.*

**3.2.10.2 Criterios de Aceptación:**

* Todo lead generado desde formulario web o integración digital deberá capturar: utm\_source, utm\_medium, utm\_campaign, utm\_content y utm\_term.

* Los parámetros UTM serán campos visibles en la ficha del Lead y de la Oportunidad derivada.

* Los UTM serán incluidos como dimensiones en los dashboards de reportería.

* La configuración de los tags UTM en los formularios es responsabilidad del equipo de marketing de Guillermo Morales.

### **3.2.11 SLA y escalamiento automático por etapa**

**3.2.11.1 Narrativa:**

*Como gerente de sucursal,*

*quiero que el CRM gestione automáticamente los SLA por etapa y escale cuando no se cumplan,*

*para asegurar que ningún lead quede sin atención y maximizar la velocidad de respuesta.*

**3.2.11.2 Criterios de Aceptación:**

* El sistema controlará el cumplimiento de SLA en cada etapa del funnel (tiempos a definir en Sprint 0).

* Si el vendedor no realiza el primer contacto en el tiempo definido: el sistema envía una alerta al vendedor y copia al gerente de sucursal.

* Si el lead supera 12 horas sin gestión activa: se reasigna automáticamente dentro de la sucursal.

* Si el lead supera 24 horas sin avance: vuelve al ejecutivo digital con un journey de nutrición activado.

* Los SLA se configurarán por etapa del funnel y podrán ajustarse por marca o sucursal.

* El sistema generará alertas internas y notificaciones vía Salesforce para los responsables.

### **3.2.12 Registro de motivo de caída**

**3.2.12.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero registrar el motivo por el cual un lead no avanzó en el embudo al marcarlo como perdido,*

*para identificar patrones de caída, activar journeys de recuperación y mejorar la conversión futura.*

**3.2.12.2 Criterios de Aceptación:**

* Al marcar un lead como 'Cerrado Perdido', el sistema requerirá seleccionar un motivo de caída.

* Los motivos de caída estarán predefinidos en una lista de selección (picklist) a definir en Sprint 0\. Ejemplos: crédito rechazado, precio de competidor, no responde, cambió de modelo, compró en otro dealer.

* El motivo de caída será visible en la ficha del lead y en los dashboards de reportería.

* Según el motivo seleccionado, el sistema activará automáticamente el journey de nutrición correspondiente.

## **3.3 Gestión de Cuentas Estándar**

Una vez convertido el lead en oportunidad, el sistema crea automáticamente la Cuenta del cliente en Salesforce, consolidando toda la información del prospecto en un registro único.

### **3.3.1 Almacenar información de Cuentas**

**3.3.1.1 Narrativa:**

*Como usuario,*

*quiero almacenar la información relacionada a mis cuentas (clientes),*

*para realizar gestiones posteriores con ellos de forma centralizada.*

**3.3.1.2 Criterios de Aceptación:**

* Se podrá almacenar la información definida en el DDD asociada a una Cuenta.

* Se implementará Chatter en la ficha de la Cuenta.

* Los campos obligatorios para la gestión de una cuenta se definirán en el DDD del Sprint 0\.

* La ficha de la Cuenta mostrará secciones relacionadas: Contactos, Oportunidades, Vehículos adquiridos, Cotizaciones, Actividades, Campañas de marketing recibidas.

### **3.3.2 Crear y actualizar Cuentas en Salesforce**

**3.3.2.1 Narrativa:**

*Como usuario,*

*quiero crear y actualizar cuentas manualmente cuando sea necesario,*

*para mantener el dato del cliente actualizado y centralizado en Salesforce.*

**3.3.2.2 Criterios de Aceptación:**

* Las cuentas podrán crearse de forma manual o por conversión automática desde un Lead.

* Los campos obligatorios definidos en el DDD deberán completarse para poder crear o guardar la cuenta.

* El usuario podrá completar o modificar los campos opcionales.

* Si un campo obligatorio queda vacío, el sistema mostrará un error y no guardará el registro.

### **3.3.3 Detectar Cuentas duplicadas**

**3.3.3.1 Narrativa:**

*Como usuario,*

*quiero que el sistema detecte automáticamente cuentas potencialmente duplicadas,*

*para evitar la creación de registros redundantes que afecten la calidad del dato.*

**3.3.3.2 Criterios de Aceptación:**

* El sistema identificará duplicados en base a: RUT, teléfono y correo electrónico (aplicables individualmente).

* Al intentar crear una cuenta duplicada, el sistema mostrará un mensaje de error con el registro existente.

* Los duplicados entre sucursales serán visibles solo para perfiles con permisos avanzados.

### **3.3.4 Visualizar Ficha 360 del cliente**

**3.3.4.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero acceder a una vista unificada del cliente que integre toda su información relevante,*

*para iniciar la conversación comercial con contexto completo sin cambiar de sistema.*

**3.3.4.2 Criterios de Aceptación:**

* La ficha 360 mostrará: datos personales y de contacto, historial de oportunidades (ganadas y perdidas), vehículos adquiridos, cotizaciones enviadas, actividades registradas (llamadas, tareas, emails), campañas de marketing recibidas y resultado NPS.

* La información estará organizada por tipo y orden cronológico.

* Se mostrará el score de calificación asignado por Agentforce si el cliente ingresó como lead digital.

* La ficha mostrará la pre-aprobación crediticia de Santander Consumer si fue consultada.

### **3.3.5 Visualizar vehículos adquiridos por el cliente**

**3.3.5.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero visualizar cuántos y cuáles vehículos ha comprado el cliente en Guillermo Morales,*

*para medir su nivel de fidelidad y diseñar ofertas de retención personalizadas en fases futuras.*

**3.3.5.2 Criterios de Aceptación:**

* En la ficha del cliente debe mostrarse una lista relacionada de Vehículos Adquiridos con: marca, modelo, año, fecha de compra y sucursal.

* Si el cliente no ha adquirido ningún vehículo, la lista se mostrará vacía.

## **3.4 Gestión de Contactos Estándar**

### **3.4.1 Almacenar información de Contactos**

**3.4.1.1 Narrativa:**

*Como usuario,*

*quiero almacenar la información de los contactos del cliente,*

*para gestionar la comunicación con múltiples personas de una misma cuenta.*

**3.4.1.2 Criterios de Aceptación:**

* Se podrá almacenar la información definida en el DDD asociada a un Contacto.

* Se implementará Chatter en la ficha del Contacto.

* Los campos obligatorios se definirán en el DDD del Sprint 0\.

### **3.4.2 Crear y actualizar Contactos manualmente**

**3.4.2.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero crear un nuevo contacto o actualizar uno existente con información relevante,*

*para mantener la base de datos de contactos actualizada.*

**3.4.2.2 Criterios de Aceptación:**

* La creación de contactos podrá ser manual o por conversión de lead.

* Los campos obligatorios deberán completarse para crear o actualizar el registro.

* Se podrá asociar un contacto a una o más cuentas.

### **3.4.3 Detectar Contactos duplicados**

**3.4.3.1 Narrativa:**

*Como usuario,*

*quiero que el sistema detecte automáticamente contactos potencialmente duplicados,*

*para evitar la creación de registros redundantes.*

**3.4.3.2 Criterios de Aceptación:**

* El sistema identificará duplicados en base a: RUT, teléfono y correo electrónico.

* Al detectar un duplicado en la creación, el sistema mostrará un error adjuntando el registro existente.

## **3.5 Gestión de Modelo de Vehículo de Interés (Objeto Custom)**

Se creará un objeto custom 'Modelo de Vehículo de Interés' para registrar el modelo deseado por el prospecto, incluyendo preferencias de variante, color y forma de pago. Este objeto se relacionará con el Lead y la Oportunidad.

### **3.5.1 Almacenar información del Vehículo de Interés**

**3.5.1.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero registrar el modelo de vehículo de interés del prospecto con sus características preferidas,*

*para tener disponible la información del modelo del vehículo deseado en toda la ficha del cliente sin reingreso manual.*

**3.5.1.2 Criterios de Aceptación:**

* El objeto Vehículo de Interés almacenará: marca, modelo, variante, color preferido, año, tipo de transmisión, forma de pago preferida (contado, financiamiento, parte de pago).

* Se implementará Chatter en la ficha del objeto.

* Los campos obligatorios se definirán en el DDD del Sprint 0\.

### **3.5.2 Asociar Vehículo de Interés a Lead u Oportunidad**

**3.5.2.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero asociar uno o más vehículos de interés a un lead o a una oportunidad,*

*para tener trazabilidad de todas las preferencias del cliente a lo largo del proceso de venta.*

**3.5.2.2 Criterios de Aceptación:**

* Se podrán asociar uno o más Vehículos de Interés a un Lead o Oportunidad.

* Al convertir el Lead, el Vehículo de Interés se trasladará automáticamente a la Oportunidad.

### **3.5.3 Registrar vehículo en parte de pago (usado)**

**3.5.3.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero registrar el vehículo que el cliente entrega en parte de pago, incluyendo datos básicos para la tasación,*

*para tener en Salesforce el contexto del usado y acceder a Autorred desde la oportunidad.*

**3.5.3.2 Criterios de Aceptación:**

* Se podrá registrar en la Oportunidad el vehículo en parte de pago con: marca, modelo, año, kilometraje y patente.

* La ficha incluirá un link de redirección a la plataforma Autorred para iniciar la tasación.

* La tasación formal del usado es realizada en Autorred y es responsabilidad del equipo de Guillermo Morales.

**3.5.3.3 Consideraciones:**

* La integración completa con Autorred vía API queda fuera del alcance de esta fase. El alcance se limita al link de redirección.

## **3.6 Gestión de Oportunidades Estándar**

La Oportunidad en Salesforce representa el proceso de venta activo de un vehículo nuevo. Sigue el pipeline de 6 etapas definido para Guillermo Morales y se convierte desde un Lead calificado.

### **3.6.1 Almacenar información de Oportunidades**

**3.6.1.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero almacenar la información relevante de la oportunidad de venta,*

*para gestionar el proceso de venta con toda la información centralizada en Salesforce.*

**3.6.1.2 Criterios de Aceptación:**

* Se podrá almacenar la información definida en el DDD asociada a una Oportunidad.

* La ficha deberá incluir: Cuenta del cliente, Contacto principal, Vehículo de Interés, Score IA, Forma de Pago, Pre-aprobación Santander, Motivo de Caída (si aplica), Número de Cotización SIGA, Fecha de Cierre.

* Se implementará Chatter en la ficha de la Oportunidad.

### **3.6.2 Crear Oportunidades desde conversión de Lead**

**3.6.2.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero convertir un Lead calificado en una Oportunidad con sus datos migrados automáticamente,*

*para evitar la doble carga de datos y mantener la trazabilidad del prospecto.*

**3.6.2.2 Criterios de Aceptación:**

* Al convertir un Lead, el sistema creará automáticamente: Cuenta, Contacto y Oportunidad con los datos del Lead mapeados según el DDD.

* El Vehículo de Interés asociado al Lead se trasladará a la Oportunidad.

* La Oportunidad se creará en etapa 'Contacto Comercial'.

* Los campos obligatorios de la Oportunidad deberán estar completos antes de la conversión.

### **3.6.3 Establecer proceso de trabajo de la Oportunidad (Pipeline)**

**3.6.3.1 Narrativa:**

*Como usuario,*

*quiero gestionar la Oportunidad a través de las etapas del pipeline comercial de Guillermo Morales,*

*para tener visibilidad del avance de cada proceso de venta y cumplir con los SLA establecidos.*

**3.6.3.2 Criterios de Aceptación:**

* El pipeline de la Oportunidad seguirá las siguientes etapas: Contacto Comercial → Experiencia → Negociación → Pago → Entrega → Cerrada Ganada / Cerrada Perdida.

* La transición de Experiencia → Negociación se disparará automáticamente cuando SIGA confirme la cotización oficial.

* La transición de Pago → Entrega se disparará automáticamente cuando SIGA confirme la nota de venta.

* La transición de Entrega → Cerrada Ganada se disparará automáticamente 24 horas después de la confirmación del cliente post-Frogmi.

* Las transiciones manuales requerirán confirmación del vendedor con los campos clave completados.

* Se podrán configurar hasta 5 campos clave por etapa.

### **3.6.4 Agregar y actualizar productos a la Oportunidad**

**3.6.4.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero asociar el vehículo cotizado como producto de la Oportunidad con su precio y descuentos,*

*para mantener el valor correcto de la operación y sincronizarlo con la cotización.*

**3.6.4.2 Criterios de Aceptación:**

* Se podrá asociar uno o más productos (vehículos) a la Oportunidad desde el Pricebook correspondiente.

* Se podrán aplicar descuentos a nivel de producto dentro de los márgenes configurados.

* El monto total de la Oportunidad se calculará automáticamente a partir de los productos asociados.

* Solo usuarios autorizados podrán aplicar descuentos superiores al umbral definido (flujo de aprobación a definir en Sprint 0).

### **3.6.5 Agendar visita y test drive desde la Oportunidad**

**3.6.5.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero coordinar y registrar la visita del prospecto como un evento en el calendario de Salesforce,*

*para tener visibilidad de los test drives agendados y disparar recordatorios automáticos al cliente.*

**3.6.5.2 Criterios de Aceptación:**

* Se podrá crear un Evento (Activity) de tipo 'Visita / Test Drive' directamente desde la ficha de la Oportunidad.

* El evento debe incluir: fecha, hora, sucursal, vendedor asignado y vehículo de prueba.

* El sistema enviará automáticamente un recordatorio al cliente vía WhatsApp o email 24 horas antes de la visita.

* Al registrarse la cotización oficial en SIGA, la visita quedará automáticamente marcada como completada.

### **3.6.6 Registrar cierre post-entrega (trigger Frogmi \+ confirmación cliente)**

**3.6.6.1 Narrativa:**

*Como ejecutivo digital,*

*quiero que el sistema gestione automáticamente el cierre de la Oportunidad tras la confirmación de entrega,*

*para evitar cierres manuales tardíos y asegurar que el dato de 'ganado' sea confiable y trazable.*

**3.6.6.2 Criterios de Aceptación:**

* Al recibir el evento de checklist completado desde Frogmi, Salesforce marcará la Oportunidad como 'Lista para Cierre'.

* Dentro de las 24 horas siguientes, el sistema enviará automáticamente un mensaje de WhatsApp al cliente consultando si recibió su vehículo correctamente.

* La respuesta afirmativa del cliente (vía Agentforce) disparará el cierre definitivo de la Oportunidad como 'Cerrada Ganada'.

* Si no hay respuesta en 24 horas, el sistema notificará al vendedor para gestionar el cierre manualmente.

### **3.6.7 Seleccionar Forma de Pago en la Oportunidad**

**3.6.7.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero registrar la modalidad de pago acordada con el cliente dentro de la Oportunidad,*

*para reflejar correctamente cómo el cliente abonará la operación y sincronizarlo con SIGA.*

**3.6.7.2 Criterios de Aceptación:**

* La Oportunidad incluirá un campo picklist 'Forma de Pago' con valores: Contado, Financiamiento Santander, Parte de Pago con Usado, Combinación.

* Al seleccionar 'Financiamiento Santander', el sistema mostrará el resultado de la pre-aprobación crediticia (si fue consultada).

* La forma de pago será un dato requerido para avanzar a la etapa de Pago.

## **3.7 Gestión de Cotizaciones Estándar**

La cotización en Salesforce representa la propuesta comercial formal emitida al cliente, incluyendo precio de lista, bonos vigentes del mes y condiciones de financiamiento. La cotización está sincronizada bidireccionalmente con SIGA ERP.

### **3.7.1 Almacenar información de Cotizaciones**

**3.7.1.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero almacenar la información de la cotización generada para el cliente,*

*para tener disponible la propuesta comercial en la ficha de la Oportunidad.*

**3.7.1.2 Criterios de Aceptación:**

* Se podrá almacenar la información definida en el DDD asociada a una Cotización.

* Se implementará Chatter en la ficha de la Cotización.

* Campos mínimos: vehículo cotizado, precio de lista, bonos aplicados, descuento concesionaria, precio final, forma de pago, plan de financiamiento (si aplica), fecha de vencimiento.

### **3.7.2 Crear cotización desde Salesforce**

**3.7.2.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero generar una cotización formal directamente desde la Oportunidad en Salesforce,*

*para evitar la doble carga de datos en SIGA y centralizar el proceso en el CRM.*

**3.7.2.2 Criterios de Aceptación:**

* La cotización se creará desde la ficha de la Oportunidad.

* Los campos obligatorios definidos en el DDD deberán completarse para crear la cotización.

* El precio de lista se tomará del Pricebook correspondiente (actualizado según SIGA para marcas Stellantis o desde Salesforce Astara para marcas Astara).

### **3.7.3 Generar documento PDF de cotización y compartir como link**

**3.7.3.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero generar un PDF de la cotización con el branding de Guillermo Morales y enviarlo al cliente como link de acceso,*

*para ofrecer al cliente una propuesta formal y profesional sin necesidad de imprimir documentos físicos.*

**3.7.3.2 Criterios de Aceptación:**

* El sistema generará automáticamente un PDF de la cotización con el layout y branding definidos por Guillermo Morales.

* El PDF incluirá: datos del cliente, vehículo cotizado, precio, bonos, forma de pago y vigencia.

* El documento se compartirá con el cliente como un link de acceso vía WhatsApp o email.

### **3.7.4 Enviar cotización para aprobación**

**3.7.4.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero enviar la cotización a un flujo de aprobación cuando los descuentos excedan los umbrales definidos,*

*para controlar los márgenes de descuento y garantizar la rentabilidad de la operación.*

**3.7.4.2 Criterios de Aceptación:**

* Las condiciones de activación del flujo de aprobación se definirán en el Sprint 0\.

* El usuario dispondrá de un botón para enviar la solicitud de aprobación.

* El aprobador recibirá una notificación para revisar y aceptar o rechazar la cotización.

* El historial de la cotización registrará el estado de la solicitud.

* Mientras la solicitud esté pendiente, el registro quedará bloqueado para edición.

### **3.7.5 Seleccionar Forma de Pago en la Cotización**

**3.7.5.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero seleccionar la forma de pago dentro de la cotización,*

*para reflejar correctamente cómo el cliente desea abonar la operación.*

**3.7.5.2 Criterios de Aceptación:**

* La cotización incluirá un campo picklist 'Forma de Pago': Contado, Financiamiento Santander, Parte de Pago, Combinación.

* Solo deben mostrarse formas de pago activas y vigentes.

### **3.7.6 Asociar Plan de Financiamiento (Santander Consumer)**

**3.7.6.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero asociar el plan de financiamiento de Santander Consumer a la cotización,*

*para mostrar al cliente el detalle de cuotas, tasa y condiciones del crédito ofrecido.*

**3.7.6.2 Criterios de Aceptación:**

* La cotización incluirá un campo de plan de financiamiento con la respuesta de pre-aprobación de Santander Consumer.

* El plan mostrará: monto aprobado, tasa, número de cuotas, valor cuota mensual.

* Este campo se completará con los datos obtenidos de la integración con Santander Consumer.

### **3.7.7 Sincronizar cotización con SIGA ERP**

**3.7.7.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero que la cotización generada en Salesforce se sincronice automáticamente con SIGA ERP,*

*para evitar la doble carga de datos y que SIGA sea el registro oficial de precios y stock.*

**3.7.7.2 Criterios de Aceptación:**

* Al crear o actualizar una cotización en Salesforce, el sistema enviará automáticamente los datos al ERP SIGA.

* Cuando SIGA confirme la cotización oficial, Salesforce actualizará el estado y marcará la visita como completada.

* Los campos a sincronizar se definirán en el DDD y en la documentación técnica de la integración con SIGA.

* Se registrarán logs de éxito o error por cada sincronización para auditoría.

### **3.7.8 Sincronizar cotización con Oportunidad**

**3.7.8.1 Narrativa:**

*Como usuario,*

*quiero sincronizar una cotización activa con su Oportunidad asociada,*

*para mantener consistencia entre los productos y precios negociados en ambos registros.*

**3.7.8.2 Criterios de Aceptación:**

* Solo una cotización podrá estar sincronizada con la Oportunidad al mismo tiempo.

* Al sincronizar una nueva cotización, se retirará la sincronización de la anterior conservando su historial.

* Los cambios en los productos o precios de la cotización sincronizada se reflejarán en la Oportunidad.

## **3.8 Gestión de Productos y Listas de Precios**

El catálogo de productos de Salesforce incluye los modelos y variantes de vehículos nuevos de cada marca comercializada por Guillermo Morales. Los precios se recibirán desde SIGA (marcas Stellantis) o desde Salesforce Astara (marcas Astara).

### **3.8.1 Almacenar y gestionar información de Productos (vehículos)**

**3.8.1.1 Narrativa:**

*Como administrador de Salesforce,*

*quiero registrar y mantener actualizado el catálogo de vehículos nuevos como productos en Salesforce,*

*para que estén disponibles para su uso en Oportunidades y Cotizaciones.*

**3.8.1.2 Criterios de Aceptación:**

* Se podrá almacenar: marca, modelo, variante, año, motor, color, estado (activo/inactivo).

* Los productos inactivos no podrán agregarse a nuevas Oportunidades o Cotizaciones.

* Solo usuarios autorizados podrán crear, modificar o desactivar productos.

### **3.8.2 Gestionar marcas comerciales (Business Brand)**

**3.8.2.1 Narrativa:**

*Como administrador de Salesforce,*

*quiero crear y organizar las marcas comerciales de Guillermo Morales dentro de Salesforce,*

*para agrupar los vehículos bajo la identidad de marca correcta y facilitar la asignación de vendedores.*

**3.8.2.2 Criterios de Aceptación:**

* Se deberán registrar las marcas: Peugeot, Citroën, DS (grupo Astara) y los modelos Stellantis correspondientes.

* Cada producto debe asociarse a una marca específica.

* La visibilidad de los productos por marca se controlará mediante permisos de perfil.

### **3.8.3 Asociar productos a Pricebooks y actualizar precios**

**3.8.3.1 Narrativa:**

*Como administrador de Salesforce,*

*quiero asociar cada vehículo a su Pricebook correspondiente con el precio de lista vigente,*

*para que los precios mostrados en las Cotizaciones sean siempre los oficiales del mes.*

**3.8.3.2 Criterios de Aceptación:**

* Se creará al menos un Pricebook por grupo de marcas (Astara / Stellantis).

* Los precios de lista recibirán actualizaciones desde SIGA (Stellantis) o Salesforce Astara (Astara) según la integración.

* Solo usuarios autorizados podrán modificar precios en los Pricebooks.

## **3.9 Gestión de Actividades**

### **3.9.1 Gestionar Tareas**

**3.9.1.1 Narrativa:**

*Como usuario,*

*quiero crear y gestionar tareas relacionadas a Leads, Cuentas, Contactos y Oportunidades,*

*para dar seguimiento ordenado a mis pendientes y no perder compromisos con los clientes.*

**3.9.1.2 Criterios de Aceptación:**

* Se pueden crear tareas con: Asunto, Comentarios, Prioridad, Estado, Fecha de vencimiento, Propietario, Tipo, Relacionado a.

* La tarea queda visible en el Activity Timeline del registro relacionado.

* Se puede marcar como Completada, reasignar y adjuntar archivos.

* Las tareas vencidas, de hoy y próximas son visibles desde la vista de lista de Tareas.

### **3.9.2 Enviar y registrar correo desde Salesforce**

**3.9.2.1 Narrativa:**

*Como usuario,*

*quiero enviar y registrar correos electrónicos directamente desde el Activity Timeline,*

*para mantener el historial de comunicación centralizado en Salesforce.*

**3.9.2.2 Criterios de Aceptación:**

* Se puede enviar correo desde el botón Email del Timeline usando: Para, CC, BCC, Asunto, Cuerpo, Plantillas y adjuntos.

* El correo enviado se registra como EmailMessage relacionado al registro y visible en el timeline.

* Las respuestas del cliente pueden registrarse automáticamente si está habilitado Enhanced Email.

### **3.9.3 Crear y gestionar Notas en registros**

**3.9.3.1 Narrativa:**

*Como usuario,*

*quiero crear notas vinculadas a registros de Salesforce,*

*para documentar información relevante que complemente los datos estructurados del registro.*

**3.9.3.2 Criterios de Aceptación:**

* La nota permite: Título, Cuerpo con texto enriquecido y adjuntar archivos.

* La nota queda asociada al registro principal y puede vincularse a múltiples registros.

* Solo el propietario o usuarios con permisos de modificar todos los datos pueden editar o eliminar la nota.

## **3.10 Encuestas de Satisfacción (NPS)**

Se configurarán dos encuestas de satisfacción: una post cotización formal (NPS de experiencia en sucursal) y una post entrega (NPS de entrega). Los resultados alimentarán el índice de calidad de vendedores y servirán como base para journeys de fidelización o recuperación de detractores.

### **3.10.1 Encuesta de satisfacción post cotización (NPS Test Drive)**

**3.10.1.1 Narrativa:**

*Como gerente de sucursal,*

*quiero enviar automáticamente una encuesta de satisfacción al cliente dentro de las 2 horas posteriores a la cotización formal,*

*para medir la experiencia en sucursal, la atención del vendedor y el NPS para alimentar el índice de calidad.*

**3.10.1.2 Criterios de Aceptación:**

* La encuesta se disparará automáticamente cuando SIGA confirme la cotización oficial (trigger de visita completada).

* Los canales de envío serán: WhatsApp (preferente) o email (secundario).

* La encuesta medirá: atención del vendedor, experiencia en sucursal, probabilidad de recomendación (NPS).

* Los resultados serán visibles en la ficha de la Oportunidad y en los dashboards de NPS.

* Si el NPS es bajo (detractor), se generará una alerta al gerente de sucursal.

### **3.10.2 Encuesta de experiencia post entrega (NPS Entrega)**

**3.10.2.1 Narrativa:**

*Como gerente de sucursal,*

*quiero enviar automáticamente una encuesta de experiencia global al cliente una vez confirmada la entrega del vehículo,*

*para medir el NPS post entrega e incorporar al cliente a un journey de fidelización o recuperación de detractores.*

**3.10.2.2 Criterios de Aceptación:**

* La encuesta se disparará automáticamente tras el cierre de la Oportunidad como 'Cerrada Ganada'.

* La encuesta medirá: experiencia de entrega, satisfacción con el vehículo, NPS global.

* Según el resultado, el sistema incorporará al cliente a un journey de fidelización (promotores) o recuperación (detractores).

* Los resultados serán visibles en la ficha de la Cuenta y en los dashboards de NPS.

## **3.11 Reportería y Dashboards**

Se configurará un set inicial de 10 dashboards operativos y de marketing que permitirán al equipo directivo y comercial de Guillermo Morales tomar decisiones en base a datos en tiempo real desde el día del go-live.

### **3.11.1 Dashboard comercial por etapa, marca y sucursal**

**3.11.1.1 Narrativa:**

*Como gerente de sucursal,*

*quiero disponer de un dashboard operativo que muestre el estado del embudo de ventas en tiempo real,*

*para identificar cuellos de botella, priorizar acciones y supervisar al equipo.*

**3.11.1.2 Criterios de Aceptación:**

* El dashboard incluirá: embudo de venta por etapa, leads por marca y sucursal, ratio de conversión por etapa, oportunidades abiertas por ejecutivo.

* Filtros por: período, marca, sucursal, ejecutivo.

### **3.11.2 Dashboard de SLA y cumplimiento por vendedor**

**3.11.2.1 Narrativa:**

*Como gerente de sucursal,*

*quiero visualizar el cumplimiento de SLA por vendedor y las alertas de reasignación activas,*

*para supervisar la velocidad de respuesta del equipo y tomar acciones correctivas.*

**3.11.2.2 Criterios de Aceptación:**

* El dashboard mostrará: tiempo promedio de primer contacto por vendedor, porcentaje de leads dentro del SLA, reasignaciones automáticas por período, leads en nutrición por motivo de caída.

### **3.11.3 Dashboard de conversión por origen de lead**

**3.11.3.1 Narrativa:**

*Como gerente de marketing,*

*quiero visualizar la tasa de conversión y el costo por adquisición por fuente y campaña,*

*para optimizar la inversión en medios y tomar decisiones de pauta basadas en datos.*

**3.11.3.2 Criterios de Aceptación:**

* El dashboard mostrará: leads por fuente (Web, Meta, Astara, CTI, etc.), tasa de conversión por fuente, CAC estimado por canal, performance por parámetros UTM.

### **3.11.4 Dashboard de NPS y satisfacción del cliente**

**3.11.4.1 Narrativa:**

*Como gerente de marketing,*

*quiero visualizar el NPS por vendedor, sucursal y etapa del proceso,*

*para identificar detractores, mejorar la experiencia del cliente y optimizar el sello Morales.*

**3.11.4.2 Criterios de Aceptación:**

* El dashboard mostrará: NPS promedio por vendedor, sucursal y período, distribución de promotores / pasivos / detractores, alertas de detractores activos.

# **4\. Marketing Cloud on Core – Alcance de Implementación**

Se detallan a continuación los requerimientos detectados para la implementación de Marketing Cloud on Core, orientada a los canales de comunicación digital y a la configuración de journeys de nutrición para prospectos de Guillermo Morales.

## **4.1 Configuración Inicial**

Se realizará la configuración base de la instancia de Marketing Cloud on Core para Guillermo Morales.

### **4.1.1 Delegación de subdominio**

Descripción: Se realizará la creación y delegación de DNS de un (1) subdominio para Marketing Cloud on Core.

**Consideraciones:**

* Es necesario que el subdominio sea creado y delegado por el equipo técnico de Guillermo Morales.

* Se dispone de un SAP form para un (1) subdominio.

### **4.1.2 Roles y usuarios**

Descripción: Se crearán los usuarios necesarios dentro de Marketing Cloud on Core con sus respectivos roles y permisos.

**Consideraciones:**

* Los roles personalizados con permisos especiales deberán ser definidos por el equipo de Guillermo Morales.

## **4.2 Configuración del canal de WhatsApp**

### **4.2.1 Conexión línea de WhatsApp Business**

Descripción: Se realizará la conexión de una (1) línea de WhatsApp Business para uso en campañas y journeys.

**Criterios de Aceptación:**

* Se conectará una (1) nueva línea de WhatsApp de tipo Business.

* Se apoyará en la verificación de la línea en Meta.

* Se capacitará al equipo en la creación de plantillas de WhatsApp desde Meta.

* Una vez creadas y aprobadas las plantillas en Meta, serán configuradas en los journeys de Marketing Cloud.

**Consideraciones:**

* Se requiere una línea nueva para la conexión; no puede usarse una línea ya vinculada a otra cuenta de WhatsApp.

* Se requiere acceso de administrador a Meta para realizar la autenticación.

* La configuración de líneas está limitada a una (1) línea por país según restricciones de Salesforce.

## **4.3 Confección de Registros (Data Streams)**

### **4.3.1 Importación de contactos y configuración de Data Stream**

Descripción: Se contempla la importación inicial de Contactos desde Salesforce Sales Cloud hacia Marketing Cloud on Core y la creación del Data Stream correspondiente.

**Criterios de Aceptación:**

* Se creará una Data Stream conectada al objeto Contacto (y Lead, según necesidad) de Sales Cloud.

* Esta conexión se utilizará como fuente de entrada para los journeys de nutrición.

* Los campos a sincronizar se definirán en el Sprint 0\.

**Consideraciones:**

* Guillermo Morales deberá proveer una base de datos de contactos históricos en formato CSV si se requiere una importación inicial masiva.

* La eliminación de la base de datos afectará directamente a los journeys activos.

## **4.4 Configuración de journeys**

### **4.4.1 Configuración de 1 campaña automatizada**

Descripción: Se configurará exactamente una (1) journey de marketing automatizada operativa al momento del go-live. El tipo de campaña será definido durante el proyecto junto al equipo de Guillermo Morales. Las opciones disponibles son:

* Opción A – Rescate por no gestión del asesor: se activa cuando un lead lleva más del SLA definido sin contacto del vendedor.

* Opción B – Rescate de oportunidad caliente con cotización sin cierre: se activa cuando una oportunidad en etapa Negociación supera el SLA sin avance.

* Opción C – Campaña de renovación: dirigida a clientes con vehículos de más de 3 años de antigüedad.

**Criterios de Aceptación:**

* Se configurará la fuente de entrada del journey basada en el objeto Lead o Contacto de Sales Cloud.

* Se definirán los criterios de entrada (estado del lead, tiempo sin gestión, etc.) en el Sprint 0\.

* Se configurará un template de email y/o WhatsApp según la campaña elegida.

* El journey incluirá hasta 12 nodos de lógica (acciones, esperas, bifurcaciones).

* El journey será activado cuando Sales Cloud esté en producción.

* Se realizarán pruebas con el equipo de Guillermo Morales antes del paso a productivo.

**Consideraciones:**

* El alcance de esta sección es exactamente 1 (una) campaña. Campañas adicionales quedan fuera del alcance de esta fase y deberán gestionarse como control de cambio.

* El contenido de los emails, landing pages y plantillas de WhatsApp será definido y aprobado por el equipo de marketing de Guillermo Morales.

# **5\. Integraciones con Sistemas Externos**

Se detallan a continuación las integraciones entre Salesforce y los sistemas externos de Guillermo Morales. Los protocolos de autenticación, frecuencia de sincronización, URLs de endpoint y esquemas de datos se definirán en detalle durante el Sprint 0 con los equipos técnicos de cada sistema.

## **Integraciones SIGA ERP**

El alcance de la integración con SIGA ERP se limita exclusivamente a las siguientes entidades: Stock (consulta en tiempo real), Lista de precios (entrante), Tipo de vehículo (entrante), Clientes (bidireccional), Cotización (saliente) y Facturación (saliente). Cualquier otra entidad, funcionalidad o endpoint de SIGA que no esté listado aquí queda fuera del alcance de esta fase del proyecto.

### **5.1 Integración Saliente – SIGA ERP (Envío de Cotización)**

**5.1.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero que la cotización generada en Salesforce se envíe automáticamente a SIGA para su registro como cotización oficial,*

*para eliminar la doble carga de datos entre el CRM y el ERP.*

**5.1.2 Criterios de Aceptación:**

* Al crear o actualizar una cotización en Salesforce, el sistema enviará los datos al ERP SIGA.

* Los campos a enviar se definirán en el DDD de la integración con SIGA.

* Se generará una confirmación de éxito o log de error por cada sincronización.

**5.1.3 Consideraciones:**

* El equipo técnico de SIGA debe estar disponible para la integración. Esta es una dependencia de Guillermo Morales.

* Alcance de integración SIGA: Stock (consulta), Lista de precios (entrante), Tipo de vehículo (entrante), Clientes (bidireccional), Cotización (saliente) y Facturación (saliente). Sin excepciones en esta fase.

### **5.2 Integración Entrante – SIGA ERP (Confirmación de Cotización y Nota de Venta)**

**5.2.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero que Salesforce reciba automáticamente la confirmación de cotización y nota de venta desde SIGA,*

*para que los eventos de SIGA disparen automáticamente los avances de etapa en Salesforce sin intervención manual.*

**5.2.2 Criterios de Aceptación:**

* Cuando SIGA confirme la cotización oficial, Salesforce avanzará la Oportunidad de 'Contacto Comercial' a 'Experiencia' y marcará la visita como completada.

* Cuando SIGA confirme la nota de venta, Salesforce avanzará la Oportunidad de 'Negociación' a 'Pago'.

* El número de cotización y el número de nota de venta de SIGA se almacenarán en campos de la Oportunidad.

* Se registrarán logs de éxito o error por cada sincronización.

**5.2.3 Consideraciones:**

* Alcance de integración SIGA: Stock (consulta), Lista de precios (entrante), Tipo de vehículo (entrante), Clientes (bidireccional), Cotización (saliente) y Facturación (saliente). Cualquier otra entidad de SIGA queda fuera del alcance de esta fase.

### **5.3 Integración en Tiempo Real – SIGA ERP (Consulta de Stock)**

**5.3.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero que Salesforce consulte en tiempo real la disponibilidad de stock en SIGA al momento de confirmar la nota de venta,*

*para validar que el vehículo seleccionado tiene existencia antes de avanzar la oportunidad a ganada, sin almacenar información de inventario en el CRM.*

**5.3.2 Criterios de Aceptación:**

* La consulta de stock se ejecuta automáticamente cuando la Oportunidad avanza al estado 'Pago' (nota de venta confirmada en SIGA).

* Salesforce envía a SIGA el código de modelo y color del vehículo de la Oportunidad y recibe una respuesta de disponibilidad en tiempo real.

* La respuesta de SIGA indica si hay existencia global del vehículo (disponible: sí/no). No se consulta ni almacena stock por almacén o sucursal.

* El resultado de la consulta se muestra al ejecutivo en la Oportunidad como un indicador de estado (Disponible / Sin stock).

* Si SIGA retorna sin stock, el sistema genera una alerta al ejecutivo y al supervisor para gestionar la situación antes de confirmar la venta.

* Salesforce no almacena ni persiste datos de stock. El resultado es una lectura puntual en tiempo real; SIGA es el sistema de inventario oficial.

* Se registra un log de cada consulta (timestamp, modelo consultado, resultado) para trazabilidad.

**5.3.3 Consideraciones:**

* Salesforce no es el sistema de gestión de inventario del proyecto. SIGA es el único registro oficial de stock.

* La lógica para determinar disponibilidad (vehículos reservados, en tránsito, etc.) es responsabilidad de SIGA.

* El endpoint de consulta de stock de SIGA se definirá durante el Sprint 0 junto con el equipo técnico de Guillermo Morales.

* Alcance de integración SIGA: Stock (consulta), Lista de precios (entrante), Tipo de vehículo (entrante), Clientes (bidireccional), Cotización (saliente) y Facturación (saliente). Sin excepciones en esta fase.

### **5.4 Integración Entrante – SIGA ERP (Lista de Precios)**

**5.4.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero que las listas de precios vigentes de cada modelo de vehículo se sincronicen periódicamente desde SIGA hacia Salesforce,*

*para que el ejecutivo pueda cotizar siempre con el precio oficial actualizado sin consultar manualmente el ERP.*

**5.4.2 Criterios de Aceptación:**

* SIGA enviará periódicamente (frecuencia a definir en Sprint 0\) la lista de precios por modelo y versión hacia Salesforce.

* La lista de precios se almacenará en el Pricebook de Salesforce, vinculada al catálogo de productos.

* Cada registro de precio incluirá: código de modelo, versión, precio de lista, moneda (CLP) y vigencia (fecha desde / hasta).

* Si un precio vence o es reemplazado, el registro anterior se desactivará automáticamente en Salesforce.

* Se registrarán logs de cada sincronización (éxito o error) para trazabilidad.

**5.4.3 Consideraciones:**

* Salesforce no es el sistema de origen de precios; SIGA es el registro oficial. Salesforce solo consume la información.

* Alcance de integración SIGA: Stock (consulta), Lista de precios (entrante), Tipo de vehículo (entrante), Clientes (bidireccional), Cotización (saliente) y Facturación (saliente). Sin excepciones en esta fase.

* El diseño del payload y la frecuencia de sincronización se definirán durante el Sprint 0 con el equipo técnico de SIGA.

### **5.5 Integración Entrante – SIGA ERP (Tipo de Vehículo / Catálogo)**

**5.5.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero que el catálogo de modelos de vehículos disponibles en SIGA esté sincronizado en Salesforce,*

*para poder seleccionar el vehículo correcto al crear una cotización u oportunidad sin depender de listas manuales.*

**5.5.2 Criterios de Aceptación:**

* SIGA enviará periódicamente el catálogo de modelos hacia Salesforce (marca, modelo, versión, año, categoría, estado activo/inactivo).

* Cada modelo se almacenará como un Producto (Product2) en Salesforce, vinculado al Pricebook.

* Los modelos desactivados en SIGA se marcarán como inactivos en Salesforce y dejarán de aparecer en las cotizaciones.

* Se registrarán logs de cada sincronización (éxito o error) para trazabilidad.

**5.5.3 Consideraciones:**

* El catálogo en Salesforce es de solo lectura; las altas y bajas de modelos se gestionan desde SIGA.

* Alcance de integración SIGA: Stock (consulta), Lista de precios (entrante), Tipo de vehículo (entrante), Clientes (bidireccional), Cotización (saliente) y Facturación (saliente). Sin excepciones en esta fase.

* El diseño del payload y la frecuencia de sincronización se definirán durante el Sprint 0 con el equipo técnico de SIGA.

### **5.6 Integración Bidireccional – SIGA ERP (Clientes)**

**5.6.1 Narrativa:**

*Como ejecutivo de ventas,*

*quiero que los datos de clientes estén sincronizados de forma bidireccional entre Salesforce y SIGA,*

*para evitar duplicaciones, garantizar que SIGA sea el sistema oficial de clientes y que Salesforce tenga el historial completo para la gestión comercial.*

**5.6.2 Criterios de Aceptación:**

* SIGA → Salesforce (entrante): sincronización periódica de la cartera de clientes existente desde SIGA hacia Salesforce (carga inicial \+ actualizaciones). El identificador único es el RUT del cliente.

* Salesforce → SIGA (saliente): al cerrarse una oportunidad como ganada, Salesforce envía los datos del cliente a SIGA para crearlo o actualizarlo como cliente oficial.

* La lógica de deduplicación se basa en el RUT; si el cliente ya existe en Salesforce, se actualizará el registro en lugar de crear uno nuevo.

* Los campos a sincronizar (nombre, RUT, email, teléfono, dirección) se definirán en el DDD de la integración.

* Se registrarán logs de cada sincronización (éxito o error) para trazabilidad.

**5.6.3 Consideraciones:**

* SIGA es el sistema de registro oficial de clientes. Salesforce actúa como sistema de gestión comercial; cualquier conflicto de datos se resuelve a favor de SIGA.

* Alcance de integración SIGA: Stock (consulta), Lista de precios (entrante), Tipo de vehículo (entrante), Clientes (bidireccional), Cotización (saliente) y Facturación (saliente). Sin excepciones en esta fase.

* El diseño del payload y la lógica de sincronización se definirán durante el Sprint 0 con el equipo técnico de SIGA.

### **5.7 Integración – Santander Consumer (Pre-aprobación Crediticia)**

**5.7.1 Narrativa:**

*Como ejecutivo digital,*

*quiero poder consultar desde la ficha del lead o la oportunidad la pre-aprobación crediticia de Santander Consumer,*

*para que el ejecutivo tenga la información de crédito disponible en el momento de la calificación sin salir de Salesforce.*

**5.7.2 Criterios de Aceptación:**

* Salesforce mostrará un botón o acción 'Consultar Pre-aprobación' en la ficha del Lead y de la Oportunidad.

* Al ejecutar la acción, Salesforce enviará los datos del cliente a la API de Santander Consumer y recibirá la respuesta.

* La respuesta (monto aprobado, tasa, cuota estimada) se almacenará en la ficha del registro.

* Si Santander rechaza el crédito, el sistema generará una alerta al ejecutivo digital para evaluar financieras alternativas.

**5.7.3 Consideraciones:**

* La API de Santander Consumer está en desarrollo. Su disponibilidad en los plazos del proyecto es una dependencia externa.

### **5.8 Integración Entrante – Frogmi (Checklist de Entrega)**

**5.8.1 Narrativa:**

*Como ejecutivo digital,*

*quiero que Salesforce reciba automáticamente el evento de checklist de entrega completado desde Frogmi,*

*para disparar el proceso de cierre de la Oportunidad sin depender de la acción manual del vendedor.*

**5.8.2 Criterios de Aceptación:**

* Al completarse el checklist de entrega en Frogmi, el sistema enviará el evento a Salesforce.

* Salesforce marcará la Oportunidad como 'Lista para Cierre' e iniciará el proceso de confirmación post-entrega.

* Se almacenará la fecha y hora del checklist de Frogmi en un campo de la Oportunidad.

* Se registrarán logs de éxito o error por cada evento recibido.

**5.8.3 Consideraciones:**

* Frogmi es facilitado por Astara Chile. La coordinación técnica es responsabilidad del equipo de Guillermo Morales.

### **5.9 Integración – Omega CTI (Llamadas Entrantes y Salientes)**

**5.9.1 Narrativa:**

*Como ejecutivo digital,*

*quiero gestionar llamadas entrantes y salientes desde la consola omnicanal de Salesforce integrada con Omega CTI,*

*para tener todas las interacciones telefónicas registradas automáticamente en el CRM sin cambio de sistema.*

**5.9.2 Criterios de Aceptación:**

* Se configurará la integración de Omega CTI con Salesforce mediante el conector CTI certificado provisto por Omega.

* Las llamadas entrantes se asociarán automáticamente al Lead o Contacto correspondiente por número de teléfono.

* Las llamadas se registrarán como actividades (Tasks) en el Activity Timeline del registro asociado.

* El ejecutivo podrá ver la ficha del Lead/Cliente en pantalla al recibir la llamada (screen pop).

**5.9.3 Consideraciones:**

* Todas las funcionalidades de integración con Omega CTI descritas en esta historia están supeditadas al conector que Omega disponibilice para Salesforce Lightning. Este conector es un supuesto del proyecto; las capacidades disponibles se confirmarán durante el Sprint 0\.

### **5.10 Integración Entrante – Web / Meta / Google Ads (Captura de Leads Digitales)**

**5.10.1 Narrativa:**

*Como equipo de marketing,*

*quiero que los leads generados por formularios web propios, Google Ads y campañas Meta ingresen automáticamente a Salesforce con sus parámetros UTM,*

*para asegurar velocidad de respuesta y trazabilidad de la inversión en medios.*

**5.10.2 Criterios de Aceptación:**

* Los formularios web de Guillermo Morales (desarrollados en su sitio) enviarán los datos al endpoint de Salesforce.

* Las campañas de Meta Ads usarán la integración nativa de Lead Ads de Salesforce.

* Todos los leads digitales ingresarán con: nombre, apellido, teléfono, email, marca de interés, y parámetros UTM.

* Los leads recibirán asignación automática según las reglas definidas en el módulo 3.2.

**5.10.3 Consideraciones:**

* La configuración de formularios en el sitio web y la inserción de parámetros UTM es responsabilidad del equipo de marketing de Guillermo Morales.

### **5.11 Autorred – Link de Redirección para Tasación de Usado**

Descripción: Se implementará un link de redirección dentro de la Oportunidad de Salesforce que dirija al ejecutivo a la plataforma Autorred para gestionar la tasación del vehículo en parte de pago.

**Criterios de Aceptación:**

* La Oportunidad incluirá un botón o link visible en la sección del vehículo en parte de pago.

* Al hacer clic, el sistema abrirá Autorred en el navegador del ejecutivo.

**Consideraciones:**

* El alcance de esta integración es únicamente el link de redirección. La integración vía API de Autorred queda fuera del alcance de esta fase.

### **5.12 Recepción de Leads desde Mercado Libre y AutoChile (Autos Usados)**

**5.12.1 Narrativa:**

*Como ejecutivo comercial de autos usados,*

*quiero que los leads generados en los portales Mercado Libre y AutoChile sean recibidos automáticamente en Salesforce a través de una API expuesta por ProContacto,*

*para gestionar el seguimiento de prospectos interesados en vehículos usados desde una única plataforma, sin necesidad de ingresar datos manualmente.*

**5.12.2 Criterios de Aceptación:**

* ProContacto expone un endpoint REST en Salesforce que Mercado Libre y AutoChile pueden invocar para enviar datos de leads (nombre, RUT, teléfono, email, vehículo de interés).

* Al recibir la solicitud, se crea un Lead en Salesforce con el campo Origen (LeadSource) poblado según el portal: \\"Mercado Libre\\" o \\"AutoChile\\".

* El sistema aplica reglas de deduplicación: si ya existe un registro con el mismo RUT, teléfono o email, el lead entrante se asocia al registro existente en lugar de crear un duplicado.

* Las reglas de asignación automática de Salesforce se ejecutan sobre cada lead recibido, distribuyéndolo al ejecutivo correspondiente según las reglas configuradas.

* El endpoint retorna una respuesta HTTP 200 con un identificador de Lead al portal origen en caso de éxito, o un código de error estándar (4xx/5xx) en caso de falla.

* Se registra en el campo Descripción del Lead la información del vehículo de interés enviada por el portal (marca, modelo, año, precio publicado), en la medida en que el portal la provea.

**5.12.3 Consideraciones:**

* Esta integración corresponde a la línea de autos usados, que está fuera del alcance del pipeline de ventas de Fase 1\. Sin embargo, la recepción y registro del lead en Salesforce sí está contemplada en esta fase.

* La configuración del endpoint en los portales Mercado Libre y AutoChile (credenciales, URL de destino, formato de payload) es responsabilidad del cliente junto con los equipos técnicos de cada portal.

* El mapeo exacto de campos dependerá del payload que cada portal sea capaz de enviar; esto se definirá durante la fase de análisis técnico.

# **6\. Omnicanalidad**

Se detalla la implementación de la consola omnicanal para que el ejecutivo digital gestione todas las interacciones con prospectos (WhatsApp, llamadas CTI) desde una única interfaz en Salesforce.

### **6.1 Configuración de Omni-Channel**

**6.1.1 Narrativa:**

*Como supervisor de ejecutivos digitales,*

*quiero que el sistema asigne automáticamente los chats transferidos por Agentforce y las llamadas de Omega CTI a los ejecutivos disponibles,*

*para evitar que los prospectos esperen o que se acumule carga en un solo ejecutivo.*

**6.1.2 Criterios de Aceptación:**

* Se habilitará el widget de Omni-Channel en la Consola de Servicio.

* Se configurarán estados de presencia: Disponible, Ocupado, Almuerzo, Offline.

* Se configurarán Routing Configurations para priorizar canales según criterio de negocio (a definir en Sprint 0).

* Se crearán las colas habilitadas para enrutamiento automático.

**6.1.3 Consideraciones:**

* La integración de llamadas de Omega CTI en la consola de Omni-Channel está supeditada al conector que Omega disponibilice para Salesforce Lightning. Este conector es un supuesto del proyecto y se validará durante el Sprint 0\.

### **6.2 Consola de Servicio (Interfaz del Ejecutivo Digital)**

**6.2.1 Narrativa:**

*Como ejecutivo digital,*

*quiero trabajar en una interfaz optimizada (Consola) que me muestre la información del lead y la conversación activa en una misma pantalla,*

*para gestionar prospectos con mayor velocidad y sin pérdida de contexto.*

**6.2.2 Criterios de Aceptación:**

* Se habilitará la Lightning Service Console.

* Se configurará la navegación basada en Pestañas y Sub-pestañas.

* Se configurará el Panel de Resaltado (Highlights Panel) con datos clave del lead: nombre, teléfono, email, score IA, etapa del funnel.

* El ejecutivo podrá ver la transcripción previa de la conversación con Agentforce al recibir un chat transferido.

### **6.3 Reportes y Tableros de Atención Digital**

**6.3.1 Narrativa:**

*Como gerente de operaciones,*

*quiero visualizar un tablero con las métricas del canal digital,*

*para monitorear el volumen de interacciones y los tiempos de respuesta del equipo.*

**6.3.2 Criterios de Aceptación:**

* Se configurará un tablero de atención digital que incluya: conversaciones activas por canal, tiempo promedio de primera respuesta, leads transferidos por Agentforce, leads convertidos desde canal digital.

# **7\. Agentforce (Agentes de IA)**

Esta sección detalla la implementación de un Agente Autónomo basado en Inteligencia Artificial (Salesforce Agentforce) diseñado para gestionar la primera línea de contacto digital en los canales de Guillermo Morales (WhatsApp Business API y Chat Web), disponible 24 horas al día, 7 días a la semana.

### **7.1 Agente de Primera Respuesta 24/7**

**7.1.1 Narrativa:**

*Como gerente de Guillermo Morales,*

*quiero implementar un Agente de IA en los canales digitales (WhatsApp Business API y Chat Web) que actúe como recepcionista virtual 24/7,*

*para identificar automáticamente la intención del cliente, responder consultas frecuentes y reducir la carga operativa del equipo humano.*

**7.1.2 Criterios de Aceptación:**

* Se configurará un (1) Agente de IA utilizando Agentforce.

* Se conectará el Agente a los canales de mensajería: WhatsApp Business API y Chat Web (Embedded Service).

* Se definirán y entrenarán los Tópicos de Conversación (Intenciones) principales:

  * Interés en compra de vehículo nuevo (por marca y modelo)

  * Consulta sobre precios, disponibilidad y financiamiento

  * Consulta sobre sucursales, horarios y ubicación

* Se configurarán Instrucciones de Seguridad (Guardrails) para evitar que el agente responda sobre política de precios no oficial o competidores.

### **7.2 Calificación y Scoring de Leads con IA**

**7.2.1 Narrativa:**

*Como supervisor de ventas,*

*quiero que el Agente analice cada conversación entrante y asigne automáticamente un score de intención (frío, tibio, caliente) al lead,*

*para que los leads calientes sean derivados inmediatamente al vendedor sin revisión manual y los tibios o fríos entren a journeys de nutrición.*

**7.2.2 Criterios de Aceptación:**

* Agentforce analizará el texto de la conversación, los datos del formulario y señales transaccionales para asignar el score.

* El score se almacenará en la ficha del Lead en Salesforce y será visible para el ejecutivo digital y el vendedor.

* Los leads calientes serán asignados automáticamente según las reglas del módulo 3.2.

* Los leads tibios o fríos serán incorporados automáticamente al journey de nutrición correspondiente de Marketing Cloud.

### **7.3 Cotización Inicial Automática**

**7.3.1 Narrativa:**

*Como ejecutivo digital,*

*quiero que el Agente envíe automáticamente una cotización inicial con precio de lista al prospecto calificado como link de acceso al documento,*

*para reducir el tiempo de respuesta y ofrecer al prospecto información concreta en su primer contacto.*

**7.3.2 Criterios de Aceptación:**

* Una vez calificado el lead, Agentforce generará y enviará automáticamente una cotización inicial con precio de lista y branding de Guillermo Morales.

* La cotización se compartirá como link de acceso al documento (PDF) vía WhatsApp o el canal de origen.

* La cotización inicial no requiere intervención humana.

* El envío quedará registrado como actividad en la ficha del Lead.

### **7.4 Transferencia Inteligente a Vendedor Humano**

**7.4.1 Narrativa:**

*Como ejecutivo digital,*

*quiero que cuando el Agente detecte alta intención de compra o el cliente solicite atención humana, la conversación se transfiera a la cola correcta con el historial completo,*

*para que el ejecutivo no repita preguntas al cliente y pueda continuar la conversación desde donde la dejó el agente de IA.*

**7.4.2 Criterios de Aceptación:**

* Agentforce transferirá la sesión a la cola de Ventas cuando detecte intención de compra alta o cuando el cliente lo solicite explícitamente.

* Al recibir el chat, el ejecutivo visualizará la transcripción completa de la conversación con el agente de IA.

* El Lead generado por el agente ya estará disponible en Salesforce con sus datos capturados.

* Si el agente no logra capturar los datos mínimos tras dos intentos, derivará automáticamente a un humano.

# **8\. Entregables – Etapas Posteriores**

## **8.1 Entregables y Compromisos del Cliente – Etapa de Sprint 0**

* Participación Activa: compromiso de participación en sesiones de relevamiento, revisión, pruebas y capacitación.

* Retroalimentación Continua: aprobación oportuna de los criterios de aceptación a lo largo del proyecto.

* Definición de Roles y Responsabilidades: especificación del equipo clave (Product Owner, Key Users por área).

* Requerimientos iniciales: descripción clara de los objetivos comerciales, funcionalidades deseadas y restricciones.

* Documentación Complementaria: formularios actuales, protocolos comerciales, documentación técnica de sistemas.

* Documentación Técnica de Integraciones: credenciales, documentación de API, forma de autenticación de: SIGA, Santander Consumer, Omega CTI, Frogmi.

* Habilitación Astara: gestión de la habilitación de acceso API (o bot RPA) con Astara España.

* Lectura y Aprobación del SOW: revisión y firma del presente documento.

* Veredicto sobre Controles de Cambio: decisión sobre los ítems fuera de alcance detectados.

## **8.2 Entregables y Compromisos del Equipo de ProContacto – Etapa de Sprint 0**

* Statement of Work Refinado (SOW): el presente documento.

* Grabación de Sesiones de Relevamiento: disponibles para consulta futura.

* Plan de Trabajo del Proyecto: una vez firmado el SOW, se entregará el roadmap definitivo con fechas y objetivos por release.

## **8.3 Compromisos del Cliente – Etapa de Ejecución**

* Detalles de Requerimientos: definiciones claras en las reuniones de refinamiento de historias de usuario.

* Aprobación de Historias de Usuario: validación funcional de cada HU antes de su desarrollo.

* Feedback Tracker: comentarios sobre las demostraciones en cada sprint (correcciones menores, dudas, aclaraciones).

* Datos de Prueba: suministrar datos realistas para pruebas y validaciones UAT.

* Usuarios de Prueba: designar Key Users por área para participar en las pruebas.

* Aprobación Final: validación formal antes del paso a producción de cada release.

* Capacitación de Usuarios Finales: Guillermo Morales es responsable de la capacitación masiva bajo el modelo de Formador de Formadores.

## **8.4 Entregables del Equipo de ProContacto – Etapa de Ejecución**

* User Stories (HUs) refinadas por sprint.

* Configuración de objetos, campos y automatizaciones en Salesforce.

* Código personalizado (Apex, Flows, LWC) cuando sea necesario.

* Documentación de integraciones con sistemas externos.

* Documentación técnica de entrega del aplicativo.

* Planes y materiales de capacitación (sesión de Formador de Formadores).

* Grabación de sesiones de capacitación.

# **9\. Cronología**

Una vez leído, refinado, firmado y aceptado el presente Statement of Work, se procederá a la elaboración del roadmap definitivo del proyecto incluyendo fechas de compromiso y los objetivos a cumplir en cada release.

El proyecto se ejecuta bajo framework Scrum con sprints de 2 semanas. Se contemplan 3 releases productivos en 22 semanas:

| Release | Semana | Contenido principal |
| :---- | :---- | :---- |
| Release 1 | Semana 10 | Agentforce (primera respuesta \+ scoring \+ cotización inicial). Captura de leads digitales (Web, Meta). Funnel básico en Sales Cloud (Calificación → Contacto Comercial). Omni-Channel básico (WhatsApp \+ consola). |
| Release 2 | Semana 16 | Embudo comercial completo (6 etapas). Integración SIGA (cotización \+ nota de venta). Integración Santander Consumer. Cotizaciones en Salesforce. SLAs y escalamiento automático. Marketing Cloud: 1 campaña configurada. Dashboards comerciales. |
| Release 3 | Semana 22 | Integración completa Salesforce Astara (API o RPA). Integración Frogmi (cierre automático). Integración Omega CTI. Encuestas NPS (post cotización y post entrega). Dashboards de NPS y canal. Capacitación Formador de Formadores. |

Cada release contará con un período de Hypercare de 14 días con soporte 5/8 del equipo de implementación de ProContacto.

La priorización de funcionalidades dentro de cada sprint será acordada entre el equipo de Guillermo Morales y ProContacto, respetando las dependencias técnicas de la plataforma.

# **10\. Controles de Cambio**

Los ítems no contemplados en el alcance inicial del proyecto o cambios adicionales que surjan durante la implementación y que afecten alguna configuración, flujo establecido o integración con otros sistemas se tendrán que estimar en cómo impactan los tiempos de implementación y su estimación de horas de configuración correspondiente.

Esta información se escalará al área comercial de ProContacto para que se coticen los cambios adicionales y sean enviados a Guillermo Morales para su aprobación antes de ser incluidos en el alcance activo del proyecto.

# **11\. Fuera de Alcance – Release 1.0**

En esta sección se detallan los requerimientos y necesidades identificadas que, por su naturaleza, exceden el alcance establecido en el acuerdo comercial inicial. Estos elementos requieren ajustes en plazos, costos o recursos asignados en caso de incluirlos al alcance del proyecto.

El equipo de Guillermo Morales deberá emitir un veredicto sobre los elementos fuera de alcance detectados, decidiendo si se incorporarán a la fase actual (como control de cambio), se pospondrán para una fase posterior o no serán considerados.

**Principio rector:** Todo lo que no esté explícitamente documentado en las historias de usuario de este SOW se considera fuera del alcance y requerirá una nueva evaluación y acuerdo por parte de ProContacto.

## **11.1 Líneas de Negocio Excluidas (Fase 1\)**

### **11.1.2 Servicio postventa (taller y mantención)**

**11.1.2.1 Narrativa:**

*Como futuras fases,*

*quiero gestionar el agendamiento de mantenciones, órdenes de trabajo y seguimiento de reparaciones en Salesforce,*

*para centralizar también la operación del taller.*

**11.1.2.2 Criterios de Aceptación:**

**11.1.2.3 Consideraciones:**

* El agendamiento de mantenciones, órdenes de trabajo, stock de repuestos y seguimiento de reparaciones quedan fuera del alcance de esta fase.

* Estado: En revisión para Fase 2\.

### **11.1.3 Venta de repuestos y accesorios**

**11.1.3.1 Narrativa:**

*Como futuras fases,*

*quiero gestionar cotización, stock y despacho de repuestos y accesorios en Salesforce,*

*para centralizar también la línea de repuestos.*

**11.1.3.2 Criterios de Aceptación:**

**11.1.3.3 Consideraciones:**

* Queda fuera del alcance de esta fase. Estado: No contemplado.

## **11.2 Integraciones Excluidas o Condicionales**

### **11.2.1 Integración API profunda con Autorred**

**11.2.1.1 Narrativa:**

*Como futuras fases,*

*quiero que la tasación del vehículo en parte de pago fluya automáticamente desde Autorred hacia Salesforce,*

*para eliminar el cambio de sistema para el proceso de peritaje.*

**11.2.1.2 Criterios de Aceptación:**

**11.2.1.3 Consideraciones:**

* Esta integración queda sujeta a disponibilidad de API pública de Autorred. Fase 1 incluye únicamente link de redirección. Estado: En revisión.

### **11.2.2 Integración en tiempo real con financieras distintas a Santander Consumer**

**11.2.2.1 Narrativa:**

*Como futuras fases,*

*quiero consultar automáticamente la pre-aprobación en Forum y otras financieras desde Salesforce,*

*para ofrecer al cliente múltiples opciones de financiamiento en tiempo real.*

**11.2.2.2 Criterios de Aceptación:**

**11.2.2.3 Consideraciones:**

* Forum y otras financieras no están incluidas en la integración de esta fase. La evaluación alternativa es realizada manualmente por el jefe de crédito. Estado: No contemplado para Fase 1\.

### **11.1.1 Venta y gestión de vehículos usados**

**11.1.1.1 Narrativa:**

*Como futuras fases,*

*quiero gestionar el pipeline de compra, preparación, fotografía y venta de vehículos usados en Salesforce,*

*para centralizar también la línea de usados en el CRM.*

**11.1.1.2 Criterios de Aceptación:**

**11.1.1.3 Consideraciones:**

* Si bien el proyecto contempla la recepción de leads de autos usados provenientes de los portales Mercado Libre y AutoChile (vía API entrante), el alcance se limita exclusivamente a: (1) recibir el lead, (2) crearlo en Salesforce con su origen etiquetado y (3) asignarlo automáticamente a un ejecutivo para su seguimiento.

* Queda explícitamente fuera del alcance de esta fase cualquier funcionalidad adicional relacionada con autos usados, incluyendo: proceso o pipeline de venta de usados, integración con stock de usados en SIGA u otro sistema, envío a facturar, peritaje formal, preparación, publicación en portales, o cualquier otro flujo operativo asociado a la línea de usados.

* El pipeline de venta de usados (recepción, peritaje formal, preparación, publicación en portales) queda fuera del alcance de esta fase.

* La tasación referencial de usados via Autorred está contemplada únicamente como link de redirección dentro de la Oportunidad de autos nuevos.

* Estado: En revisión para Fase 2\.

### **11.2.3 Integración con plataformas de seguros**

**11.2.3.1 Narrativa:**

*Como futuras fases,*

*quiero gestionar el proceso de póliza y comisiones de seguro dentro de Salesforce,*

*para centralizar la venta de seguros junto al proceso de venta del vehículo.*

**11.2.3.2 Criterios de Aceptación:**

**11.2.3.3 Consideraciones:**

* Queda fuera del alcance de esta fase. Estado: No contemplado.

## **11.3 Funcionalidades de Salesforce Excluidas**

* Configuración de Experience Cloud (portal de clientes o concesionarios).

* Gestión de contratos o documentación legal de venta dentro de Salesforce (DocuSign u otro).

* Módulo de gestión de inventario propio dentro de Salesforce: el inventario vive en SIGA; Salesforce solo consulta disponibilidad.

* Gestión de facturación o contabilidad: la facturación se realiza exclusivamente en SIGA.

* Configuración de Salesforce Field Service para técnicos de taller.

* Dashboards o reportes adicionales a los 10 acordados en el set inicial; reportes extra son bajo demanda.

* Más de una campaña de marketing automatizada en esta fase (el alcance es exactamente 1 campaña).

* Data Cloud o CRM Analytics para modelos predictivos avanzados.

## **11.4 Procesos de Negocio Excluidos**

* Proceso de patentamiento e inscripción del vehículo: responsabilidad del área administrativa de Guillermo Morales.

* Gestión de garantías de fábrica o garantías extendidas.

* Gestión de incentivos, comisiones o liquidación de sueldos de vendedores.

* Gestión de proveedores o compras de inventario de vehículos.

* Proceso de inspección física del vehículo en parte de pago: la tasación presencial es un proceso operativo de Guillermo Morales.

## **11.5 Canales y Plataformas Excluidas**

* Gestión de la pauta publicitaria en Meta Ads, Google Ads u otros medios: el proyecto configura la recepción de leads pero no incluye la administración de campañas pagas.

* Rediseño o desarrollo de la página web de Guillermo Morales.

* Gestión de redes sociales o contenido orgánico.

* Integración con TikTok Ads u otras plataformas de pauta no mencionadas.

* Sincronización de mensajes de WhatsApp personales de los vendedores con Salesforce: la plataforma se integra exclusivamente con WhatsApp Business API. Las conversaciones iniciadas o gestionadas desde cuentas personales de WhatsApp de los vendedores no serán capturadas ni registradas en el CRM.

## **11.6 Actividades de Gestión del Cambio**

* Diseño o ejecución del plan de gestión del cambio cultural (comunicación interna, esquemas de incentivos, contratos laborales): responsabilidad de Guillermo Morales.

* Revisión o rediseño de protocolos comerciales presenciales del 'Sello Morales' más allá de los checklists configurables en Salesforce.

* Capacitación masiva a los \~150 usuarios finales: responsabilidad del equipo de Guillermo Morales bajo el modelo de Formador de Formadores. ProContacto capacita únicamente a los Key Users designados.

# **12\. Aprobaciones**

Los siguientes individuos deberán revisar y aprobar el presente Statement of Work antes de que el proyecto pueda iniciar su etapa de ejecución. Al firmar, confirman haber leído y aceptado el alcance, las condiciones y los compromisos descritos en este documento.

| Por ProContacto Firma: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Nombre: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Cargo: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Fecha: \_\_\_/\_\_\_/\_\_\_\_\_\_ | Por Guillermo Morales Firma: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Nombre: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Cargo: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Fecha: \_\_\_/\_\_\_/\_\_\_\_\_\_ |
| :---- | :---- |

