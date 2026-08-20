# Estructura oficial del SOW Refinado (Template V2 — ProContacto)

Este archivo reproduce la estructura sección por sección del template oficial, con los textos fijos que se reutilizan tal cual (adaptando solo el nombre del cliente) y las reglas de redacción de cada parte. El documento generado debe ser reconocible como un SOW de ProContacto.

## Convenciones globales

- Idioma: español neutro-latinoamericano, formal, impersonal ("Se realizará la configuración de..."), voz pasiva refleja predominante.
- Numeración jerárquica multinivel en TODO el cuerpo: `3.`, `3.1.`, `3.1.1.`, `3.1.1.2.1.` Las historias y consideraciones se redactan como ítems numerados, no como prosa corrida.
- Placeholder del cliente: donde el template dice "Nombre del cliente" o deja espacio, usar el nombre real del cliente del proyecto.
- Pie de página: "Statement of Work Comercial (SOW) — [Cliente]" + número de página.
- Título de portada: "Statement of Work Comercial" + "Implementación Salesforce" + nombre del cliente. El título visible del documento es SIEMPRE "Statement of Work Comercial" (también en la ficha, campo Tipo de documento).
- Nombre del archivo: **"SOW Comercial - [Nombre del cliente].docx"** — siempre, sin variantes.
- El **índice** y el **glosario de términos** son secciones obligatorias en todos los SOW, sin excepción.

## Orden de secciones

1. Portada
2. Ficha del documento
3. Control de versiones
4. Índice
5. 1. Introducción
6. 2. Glosario de términos
7. 3..N. [NUBE] - Alcance de Implementación (una sección por nube)
8. Entregables - Etapas posteriores
9. Cronología
10. Controles de Cambio
11. Fuera de Alcance - Release 1.0
12. Aprobaciones

## Ficha del documento (página 2)

Tabla de tres filas:

| Nombre del sistema | Salesforce |
| Tipo de documento | Statement of Work Comercial |
| Versión de documento | 1.0 |

## Control de versiones

Tabla: Versión # / Fecha de entrega / Creado por (Nombre y Rol) / Resumen de cambios. Primera fila: versión 1.0, fecha actual, autor = el usuario (preguntar nombre y rol si no se conocen; no inventar), "Primera versión".

## 1. Introducción — TEXTO FIJO

Usar este texto tal cual, reemplazando [CLIENTE]:

> El presente documento está orientado a brindar una descripción sobre el entendimiento de los requerimientos proporcionados para el desarrollo de la plataforma de Salesforce. Se pautarán qué consideraciones se tomarán en cuenta para dicho desarrollo, así como un entendimiento del proceso de trabajo, restricciones de negocio, automatizaciones, entre otros. Además, se establecerá una delimitación clara del alcance del proyecto.
>
> El desarrollo de cualquier requerimiento o consideración no incluida en este documento ya sea funcionalidad, automatización, validación, flujo o integración implica un esfuerzo adicional. Por lo tanto, los elementos no mencionados en este documento estarán fuera del alcance del proyecto.
>
> Es importante tener en cuenta que este documento servirá como referencia para el desarrollo, configuración y personalización del entorno de Salesforce. Se espera que el equipo de implementación de ProContacto trabaje en estrecha colaboración con [CLIENTE] para asegurar una comprensión y alineación claras de los objetivos, requisitos y restricciones del proyecto.
>
> Asimismo, se establecerá un marco de trabajo para la gestión del proyecto, definiendo las responsabilidades y la comunicación entre todas las partes involucradas. Se acordarán plazos y entregables específicos, así como mecanismos de seguimiento y control para garantizar el cumplimiento de los objetivos del proyecto.
>
> Se espera que este proyecto sea una colaboración exitosa y productiva entre [CLIENTE] y ProContacto. Con un enfoque claro en los objetivos, una comunicación abierta y un seguimiento constante, lograremos entregar un software de alta calidad que cumpla con sus expectativas y contribuya al éxito de su organización.

## 2. Glosario de términos

Tabla de dos columnas (Concepto / Definición). Incluir SIEMPRE el glosario base: Nube, Integración, Alcance, Desvío, Control de cambio, Importación, Sprint, Sprint 0, UAT, Scrum, Relevamiento, Endpoint, Middleware, API, Backend, Frontend, Base de datos, Módulo, Responsividad, QA, Apex, Objeto, Registro, Trigger, Workflow Rule, Regla de validación, Tipo de registro. (Web to Lead y otros términos específicos solo si aplican al proyecto.) Las definiciones del template original están en estilo didáctico de 2-4 oraciones contextualizadas a Salesforce — mantener ese estilo. Agregar los términos propios del proyecto: nubes usadas (p.ej. "Field Service"), herramientas (Salesforce Maps, CRM Analytics, OmniStudio, Data Cloud), conceptos de negocio del cliente y sistemas externos integrados.

## 3..N. [NUBE] - Alcance de Implementación

Una sección numerada por cada nube de la solución (p.ej. "3. Sales Cloud - Alcance de Implementación", "4. Service Cloud - Alcance de Implementación"). Abrir cada una con el texto fijo:

> Se detallan a continuación los requerimientos detectados y evaluados en un alto nivel de detalle, teniendo en cuenta ciertas consideraciones como la definición total del requerimiento en etapas posteriores de refinamiento, permisos sobre la plataforma, alcance del requerimiento, entre otros.

### Épicas e historias

Dentro de cada nube, subsecciones por **épica** (3.1, 3.2…). Bajo cada épica, las historias de usuario numeradas (3.1.1, 3.1.2…). Si el proyecto tiene User Story Map, dejar la nota "Insertar imagen de la épica en el USM" como marcador; si no, omitirla.

**Formato exacto de cada historia:**

```
3.1.1. [Nombre de la historia — corto, orientado a capacidad, p.ej. "Registro y conversión de candidatos"]
  3.1.1.1. Tipo de Funcionalidad: [Estándar | Personalizada | Híbrida]
  3.1.1.2. Narrativa:
    3.1.1.2.1. Como [ACTOR], quiero [ACCIÓN], para [BENEFICIO].
  3.1.1.3. Criterios de Aceptación:
    3.1.1.3.1. [criterio verificable]
    3.1.1.3.2. [criterio verificable]
    3.1.1.3.3. [criterio verificable]
    3.1.1.3.4. [criterio verificable]
```

Reglas de redacción de historias:
- ACTOR = rol real del cliente (Ejecutivo comercial, Supervisor de ruta, Agente de servicio, Administrador del sistema), nunca "usuario" a secas.
- ACCIÓN = capacidad concreta sobre la plataforma; BENEFICIO = valor de negocio, no una repetición de la acción.
- Tipo de Funcionalidad: "Estándar" si se resuelve con configuración out-of-the-box; "Personalizada" si requiere código o componentes custom; "Híbrida" si combina ambos.
- Criterios de Aceptación: 3 a 6, cada uno verificable en una demo (condición observable, no intención). Incluir criterios negativos/de borde cuando el proceso lo amerite ("Si el candidato no posee correo electrónico, el sistema impedirá la conversión mostrando un mensaje de error").
- Una historia = una capacidad. Si la narrativa necesita dos "quiero", son dos historias.

### Consideraciones Generales

Después de las historias de cada épica (o al final de la sección de la nube si aplican a toda la nube), agregar la subsección "Consideraciones Generales" organizada por dominios en mayúsculas: `ROLES Y PERFILES`, `IMPORTACIÓN DE DATOS`, `GESTIÓN DE [DOMINIO]` (LEADS, OPORTUNIDADES, COTIZACIONES, PEDIDOS, PRECIOS/MONEDAS, STOCK/INVENTARIO, RUTAS, VISITAS, CASOS, TAREAS, NOTIFICACIONES, REPORTES, DOCUMENTACIÓN, PAGOS…), más los que el proyecto requiera.

Contenido típico de cada dominio (ítems numerados):
- **Supuestos de diseño**: "Se hará uso del objeto estándar de X…", "Se realizará la configuración de N tipos de registro sobre el objeto X…".
- **Limitaciones del estándar explicadas**: "Por funcionalidad estándar de la plataforma de Salesforce, no se incluye…", con la explicación didáctica de por qué (el template siempre educa al cliente sobre la plataforma).
- **Delimitaciones negativas de alcance** (protección contractual): "No se consideran integraciones con…", "No se tendrá en cuenta la validación de…", "Sólo se podrá visualizar…".
- **Definiciones diferidas**: "…quedará pendiente de definición final. Se requerirá una planificación detallada en colaboración con los equipos de TI…", "La definición de campos se realizará en la etapa de refinamiento, dentro del documento 'Diccionario de Datos'".
- **Responsabilidades del cliente**: "La calidad de la información será responsabilidad del equipo de [CLIENTE]".

Para ROLES Y PERFILES e IMPORTACIÓN DE DATOS existe boilerplate casi fijo en el template — reutilizarlo adaptando objetos y sistemas:
- ROLES Y PERFILES: uso de configuración estándar (Perfiles = permisos CRUD; Roles = jerarquía; Conjuntos de Permisos = permisos temporales; Reglas de Colaboración = acceso por criterios), configuración detallada pendiente de definición final, entrega de la "Matriz de roles y perfiles", detalle fino por perfil se define en el sprint de configuración.
- IMPORTACIÓN DE DATOS: plantilla de carga masiva .CSV definida por ProContacto, datos desde una sola tabla, sin transformaciones (calidad = responsabilidad del cliente), datos finales con estructura requerida, importación posterior a configuración y validación del objeto, sin archivos adjuntos (PDF, videos, imágenes).

## Integraciones con Sistemas Externos (cuando el proyecto tiene integraciones)

Capítulo propio, después de las secciones de alcance por nube. Seguir el patrón del ejemplo real `knowledge-base/ejemplo-sow-guillermo-morales-crm.md` (sección 5):

- Apertura del capítulo: "Se detallan a continuación las integraciones entre Salesforce y los sistemas externos de [CLIENTE]. Los protocolos de autenticación, frecuencia de sincronización, URLs de endpoint y esquemas de datos se definirán en detalle durante el Sprint 0 con los equipos técnicos de cada sistema."
- Por cada sistema, un alcance taxativo por entidad y dirección: "El alcance de la integración con [SISTEMA] se limita exclusivamente a las siguientes entidades: [Entidad (dirección/modalidad)], … Cualquier otra entidad, funcionalidad o endpoint que no esté listado aquí queda fuera del alcance de esta fase del proyecto."
- Una historia por interfaz, con título que indica dirección: "Integración Saliente/Entrante/Bidireccional – [SISTEMA] ([Entidad])", y estructura Narrativa / Criterios de Aceptación / Consideraciones.
- En Consideraciones de cada interfaz: dependencias del cliente explícitas (disponibilidad del equipo técnico del sistema externo, documentación de API, autenticación), remisión de campos al DDD, manejo de errores/logs, y la repetición del alcance taxativo ("Sin excepciones en esta fase").

## Entregables - Etapas posteriores — TEXTO FIJO

Cuatro subsecciones con listas de viñetas. Reutilizar tal cual del template (adaptando [CLIENTE]):

**Entregables y Compromisos del Cliente - Etapa de Sprint 0**: Participación Activa; Retroalimentación Continua; Definición de Roles y Responsabilidades; Requerimientos iniciales; Documentación Complementaria; Documentación Técnica Complementaria para Integraciones (documentación técnica de su API, forma de autenticación); Lectura del Documento SOW; Aclaración de Dudas del SOW; Brindar Veredicto de los Controles de Cambio (tomar en release actual vía gestión comercial / no tomar / tomar en release posterior); Aprobación del Documento SOW.

**Entregables y Compromisos del Equipo de ProContacto - Etapa de Sprint 0**: Statement of Work (SOW) Refinado; Grabación de Sesiones de Relevamiento; Plan de Trabajo del Proyecto (cronograma detallado post-firma).

**Entregables y Compromisos del Cliente - Etapa de Ejecución**: Detalles de Requerimientos; Aprobación de Historias de Usuario; Comentarios sobre la demostración realizada (Feedback Tracker); Aprobación de Funcionalidad (Demostración); Datos de Prueba; Usuarios de Prueba; Aprobación Final; Capacitación de Usuarios Finales.

**Entregables del Equipo de ProContacto - Etapa de Ejecución**: User Stories (US); Configuración de Objetos; Código Personalizado; Entregables de Interfaces/Integraciones; Documentación de Entrega de Aplicativo; Planes de Testing; Planes y Materiales de Capacitación; Documentación de Capacitación; Grabación de Capacitación.

Cada viñeta lleva el título en negrita seguido de dos puntos y la descripción de una o dos oraciones (tomar las descripciones del template original).

## Cronología — TEXTO FIJO

Párrafos fijos del template: la priorización de historias es responsabilidad del cliente según sus prioridades internas; ProContacto prioriza según dependencias técnicas de la plataforma; se propone un roadmap conjunto; el roadmap definitivo con fechas de compromiso se elabora una vez leído, refinado, firmado y aceptado el SOW; en cada sprint se refinan los requerimientos de este documento.

## Controles de Cambio — TEXTO FIJO

> Los ítems no contemplados en el alcance inicial del proyecto o cambios adicionales que surjan en el desarrollo de la implementación y que afecten alguna configuración, flujo establecido o integración con otros sistemas de información, se tendrán que estimar en cómo impactan a los tiempos de implementación con su estimación de horas de configuración correspondiente. Esta información se escalará al área comercial para que se coticen los cambios adicionales sobre la plataforma y sean enviados a [CLIENTE].

## Fuera de Alcance - Release 1.0

Abrir con el texto fijo del template (requerimientos detectados en Sprint 0 que exceden el alcance del acuerdo comercial; el cliente debe emitir veredicto: incorporar a fase actual / posponer / descartar; incorporar impacta tiempos y costos).

Luego, misma estructura de épica → historia que el alcance, pero cada historia lleva solo: Tipo de Funcionalidad, Narrativa, y dos subsecciones adicionales:
- **Observaciones**: incluir siempre la nota fija "En caso de que el equipo de [CLIENTE] decida incluir alguna de estas funcionalidades dentro del alcance, el equipo de ProContacto incurrirá en esfuerzo de estimación, factibilidad y detalle de las mismas, con el fin de escalar al área comercial su tratamiento." + observaciones propias del requerimiento.
- **Estado final**: "En revisión" por defecto.

## Aprobaciones

Sección final: "Individuos que necesitan aprobar el SOW antes de que pueda implementarse". Tabla de tres columnas (Nombre / Rol / Aprobación) con 4-5 filas vacías o con los nombres si se conocen.
