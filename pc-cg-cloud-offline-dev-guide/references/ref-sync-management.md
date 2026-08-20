# Referencia de Sync Management

Referencia de Sync Management

Si el Modeler (y su CLI) es el lado de desarrollo, Sync Management es el lado de administración y operación en la nube. Es la app de Salesforce donde configuras qué datos bajan, publicas tus customizaciones, ajustas el comportamiento del sync y —sobre todo— monitoreas y diagnosticas la flota de dispositivos. Este documento es el mapa completo de esa app: todas sus páginas, capacidades y configuraciones, con el foco puesto en las herramientas de debugging, monitoring y troubleshooting.

Cómo se relaciona con el resto del curso: el `02-modelo-datos.md` explica los Tracked Objects, Named Queries y NFTs; el `07-sincronizacion.md` el motor de sync; y el `08-troubleshooting-sync.md` el troubleshooting paso a paso. Acá tienes la consola entera de un vistazo, como hoja de consulta. Es el par administrativo de la Referencia de la CLI del Modeler.

## Resumen operativo

- Mapa de la consola Sync Management en tres familias: Configuracion (Sync Configuration: Assignments, Tracked Objects, NFT, Named Queries, Mobile Settings, Sync Settings; mas Sync Messages), Distribucion (Deployment Packages, Deploy Package Assignment, Mobile App Themes) y Monitoreo/Diagnostico.
- Diagnostico (detalle abajo): Device Health/Status, Device KPI Tracing, Sync History & KPIs, Device Events Log, Named Query Analyzer, Remote Requests. El `Sync ID` es el hilo conductor.
- Es la contraparte administrativa de la CLI del Modeler (`ref-cli-modeler.md`).

## 1. El mapa de la app

Las páginas de Sync Management caen en tres familias: las que configuran qué y cómo se sincroniza, las que distribuyen tu app a los dispositivos, y las que te dejan observar y diagnosticar qué está pasando. Ten presente este mapa: casi cualquier tarea cae en una de las tres.

> Diagrama (descrito, no embebido): Las tres familias de páginas de Sync Management: Configuración, Distribución y Monitoreo/Diagnóstico.

## 2. Configuración del sync

La pestaña Sync Configuration concentra qué datos viajan y cómo. Sus sub-pestañas:

| Sub-pestaña | Qué configura |
| --- | --- |
| Assignments | Asigna una Sync Configuration a usuarios, roles o profiles (el mapeo directo a un usuario tiene prioridad sobre role/profile). Maneja una jerarquía padre/hijo de hasta tres niveles; las configuraciones hijo heredan los Tracked Objects de su padre. |
| Tracked Objects | Las entidades que se vuelven tablas en la base del dispositivo (una por objeto de Salesforce). La cláusula SOQL Where acota el scope de registros a descargar. (`02-modelo-datos.md`) |
| Named Fetch Trees | La relación jerárquica root → nodos hijos resuelta en un único request disparado por la business logic; reduce drásticamente las llamadas a la API. (`02-modelo-datos.md`) |
| Named Queries | Sentencias SOQL que devuelven una lista de IDs para restringir el volumen; se invocan en el Where de un Tracked Object y son anidables para sortear límites de subconsultas. (`02-modelo-datos.md`) |
| Mobile Settings | Seguridad del dispositivo y conectividad de red (sección 3). |
| Sync Settings | Los parámetros globales del motor de sync (sección 4). |

## 3. Mobile Settings

Directivas de seguridad y almacenamiento que se aplican a todos los clientes móviles:

| Parámetro | Qué hace |
| --- | --- |
| PIN Protection | Obliga a definir un PIN tras inicializar el dispositivo. Configuras el tiempo de inactividad (5 a 60 min) que bloquea la app, la longitud del PIN (4 a 8 dígitos) y el tipo de autenticación. |
| Download Limits / Max File Size | Un slider con el tamaño binario máximo descargable al caché. El error 9806 (archivo supera el MaxBinaryFileSize) se resuelve subiéndolo. Ojo: un límite de archivo en el Where de un NFT sobreescribe este valor genérico. |
| Offline timeout | Un slider con el período máximo sin red; si el rep lo supera, la app lo desloguea automáticamente. |
| Validation | Un switch (Enabled) que evalúa las validaciones de esquema sobre lo que el usuario ingresa antes de volcarlo. |
| Connected App QR Code | Agrupa el Consumer Key, el Custom Domain y la Callback URL del aprovisionamiento, y permite generar un QR (Generate QR Code) para inicializar el dispositivo rápido. El origen del Consumer Key se cubre en el documento de la External Client App. |

## 4. Sync Settings

Los parámetros que modulan el comportamiento global del motor de sync en runtime:

| Parámetro | Qué controla |
| --- | --- |
| Background Sync | La sincronización automática en segundo plano: un Intervalo (10 a 9999 min) y un modo — Complete Sync (baja y sube todo), Upload Only (solo sube, ahorra red) o Deactivated (sin disparo automático; el usuario sincroniza a mano). |
| App Startup Sync | El sync al abrir la app: Always, Time threshold o No sync, con un App Startup Sync Time Threshold de 10 a 1440 min (default 30). |
| Gestión de eventos / logs | Topes volumétricos de eventos que un dispositivo puede mandar por período (en horas), con un máximo para Log Level = Error y otro para el resto (Debug, Info, Log). |
| Queue sync users at maximum limit | La concurrencia de syncs simultáneos: de 2 a 600 usuarios (se recomienda 200), solo a nivel de configuración top-level. Si se activa el check y se excede, encola y avisa la posición (aplica a FSOD e Initial Sync). |
| CPU Calculation Threshold | Calculate sync time with CPU time: resta un buffer del límite del gobernador (default 6500 ms) para evitar Apex CPU limit exceptions. |

## 5. Distribución de la app

Cómo llega tu trabajo del Modeler a los dispositivos, y cómo se ve y comunica la app:

| Página | Qué hace |
| --- | --- |
| Deployment Packages | Administra los .zip con las customizaciones del Modeler: acá subes el deployment.zip que generó sf mdl package. (`03-setup-modeler-git.md`) |
| Deploy Package Assignment | Publica y asigna el package a nivel All o User; el dispositivo lo detecta e instala en el siguiente sync. (`03-setup-modeler-git.md` y 7) |
| Mobile App Themes | Colores, íconos y componentes de UI mediante macros RGBA; los temas base no se editan, se clonan en Custom Themes. (`10-theming-pdf-localization.md`) |
| Sync Messages | Los mensajes de espera durante FSOD, Initial Sync y App Start. Estáticos (máx 20) o dinámicos (usan el macro #recordCount# para insertar la cantidad de registros). Se traducen en Sync Message Translations, y lo definido acá sobreescribe el core y el Modeler. |

## 6. Monitoreo y diagnóstico

Acá está el corazón operativo. El hilo conductor de casi todo es el Sync ID: único en la org, te permite cruzar un evento del Sync History con sus logs en el Device Events Log. Las herramientas, de la visión general al detalle fino:

| Herramienta | Qué muestra y cuándo la usás |
| --- | --- |
| Device Health Summary / Details | Dashboards de salud de la flota: FSOD Average Duration, API Calls per Day, Deployment Package Installation/Utilization, Free Disk Space. Para auditar a gran escala y detectar anomalías (picos de API, FSOD lento, disco lleno, versiones de package inconsistentes). |
| Device Status Overview | Lista de dispositivos con semáforo de FW Status y Sync Status; desde acá haces Reset Status y entras a Device KPI Tracing y a Device Details Edit (API Calls Up/Down/NFT, Resets, Trace Mode, Last Connection). |
| Device KPI Tracing | Solo con Trace Mode activo. Desglosa los endpoints APEX de un sync: Endpoint, Category (clase APEX), Sub Category (SELECT/INSERT/UPDATE/COUNT), Input Data Volume, Records Affected, Time Taken (ms) y el SOQL Statement. Para perfilar queries lentas. |
| Sync History & KPIs | Cada ciclo de sync con su estado, tipo, volumen y duración (filtrable por user, Installation ID, Sync Type, Sync ID, etc.). La pestaña KPIs lo abre por Tracked Object, NFT y Named Query para ver qué artefacto mete el cuello de botella. |
| Device Events Log | Los logs del cliente y del servidor. Filtros por Event Code, Min Log Level, Namespace, Installation ID, Sync Version. Namespaces: SYNC (motor, prefijo CGCloud) y FW (framework, prefijo CAS). Indica el origen (Error Originates From CLIENT/SERVER) y la etapa (Stage). |
| Named Query Analyzer | Simula la ejecución de Named Queries sin dispositivo, a partir de un User y Client App ID. Dibuja el Call Tree de dependencias y reporta el recuento total de SOQL y la frecuencia de uso. Para prevenir Apex CPU y límites SOQL antes de que exploten. |

## 7. Remote Requests

Comandos asíncronos que le mandas a un dispositivo para diagnosticarlo o recuperarlo. Se crean desde la sección Remote Request o desde Device Details Edit:

| Acción | Qué hace y parámetros |
| --- | --- |
| Activate Trace Mode | Pone al dispositivo en logging debug absoluto. Trace Mode Duration (OFF, 1, 2, 4, 8, 16, 24 o 48 h) y Log Area (All, Synchronization o Application). Habilita el Device KPI Tracing. |
| Activate Debug Window | ON/OFF. Habilita un panel técnico en el dispositivo (triple toque sobre la interfaz) para ver configuraciones y eventos. |
| Clear Upload Failures | Limpia la cola de subidas fallidas del dispositivo. Parámetro Clear Records Till (timestamp). Genera un log descargable de los registros limpiados (JSON). Para destrabar la cola bloqueada por un registro corrupto. |
| Resupply | Fuerza al dispositivo a re-descargar todos los registros de los Tracked Objects que selecciones. Para cuando faltan datos tras corregir una config. |
| Request Logs | Trae al servidor los logs operativos del framework y la app desde el dispositivo (descargas el ZIP). |
| Request Statistics | Recopila las estadísticas de la base local CasMobile.db del dispositivo. |
| Reset API Stats | Resetea los contadores de llamadas a la API en el dispositivo. |
| Request Data | Trae registros tabulares exactos: Tracked Object, Fields, Record IDs y Sort Order (asc/desc). Hasta 30 MB descomprimidos, en JSON, para validar el dato crudo del dispositivo. |

## 8. Qué herramienta para qué síntoma

La tabla de decisión rápida cuando algo falla (el flujo completo paso a paso está en el `08-troubleshooting-sync.md`):

| Síntoma | Dónde mirar |
| --- | --- |
| Un sync falló o reportó un código | Sync History (anota el Sync ID) → Device Events Log filtrado por ese Sync ID |
| El sync es lento o baja demasiado | Sync History KPIs (por TO/NFT/NQ) + Device KPI Tracing (con Trace Mode) |
| Sospechas de una Named Query | Named Query Analyzer (Call Tree y recuento de SOQL) |
| Un registro no sube | Device Events Log (suele ser FLS/Sharing) → Remote Request Clear Upload Failures |
| Faltan datos en el dispositivo | Remote Request Resupply de los Tracked Objects; Request Data para ver el dato crudo |
| Salud general de la flota | Device Status Overview y Device Health Details |
| Necesito el máximo detalle | Activate Trace Mode → reproducir → Request Logs |

## 9. Cheat-sheet

Dónde está cada cosa, de un vistazo:

| Quiero… | Voy a… |
| --- | --- |
| acotar qué datos bajan | Sync Configuration → Tracked Objects / Named Queries / NFT |
| asignar la config a usuarios | Sync Configuration → Assignments |
| ajustar PIN, timeout, Max File Size | Sync Configuration → Mobile Settings |
| tocar background sync o concurrencia | Sync Configuration → Sync Settings |
| publicar mi deployment.zip | Deployment Packages → subir → Deploy Package Assignment |
| personalizar colores/íconos | Mobile App Themes |
| ver por qué falló un sync | Sync History (Sync ID) → Device Events Log |
| analizar una Named Query | Named Query Analyzer |
| recuperar un dispositivo trabado | Remote Request (Clear Upload Failures / Resupply / Trace Mode) |

Nota: este documento es la referencia transversal de la consola. Los mecanismos detrás de cada cosa están en los módulos: el modelo de datos del sync en el `02-modelo-datos.md`, el motor y los tipos de sync en el 7, y el flujo de troubleshooting de punta a punta en el 8.
