# Arquitectura de la app offline y el Modeler

Antes de tocar una sola línea, necesitas un mapa mental de cómo está hecha la app. La Consumer Goods Cloud Offline App no se programa en código nativo: se configura con contratos XML y scripts de lógica que el Modeler compila. Entender qué capas existen, qué hace cada una, cómo el Modeler convierte tus contratos en una app que corre, y cómo viaja un dato desde un tap hasta la base local, es lo que te va a permitir ubicar cualquier cosa que veas en el resto del curso.

## Resumen operativo

- La app offline se estructura en cinco capas, cada una con su tipo de contract: Process (orquesta), UserInterface (vista), Business Object + bl.js (modelo/logica), Datasource (acceso a datos) y textos/locale.
- El dato fluye UI -> Process -> Business Logic -> Datasource -> SQLite, y la UI se refresca sola por bindings.
- Workspace: todo cuelga de `appl/` (app, build, config, data) + contractSnippets + src.
- Regla: pensa cualquier feature como una rebanada que atraviesa las cinco capas.

## 1. La app offline en una imagen

La arquitectura separa responsabilidades en cinco capas, cada una con su propio tipo de contract. De arriba hacia abajo: lo que el usuario ve (UI), el flujo que orquesta (Process), el modelo de datos y la lógica en memoria (Business Objects + Business Logic), el mapeo a la base local (Data Source), y la sincronización con Salesforce (Sync). Esta separación es la que hace mantenible una app que, por dentro, es bastante compleja.

> Diagrama (descrito, no embebido): Las cinco capas de la app offline, cada una con su tipo de contract y su responsabilidad.

## 2. Las cinco capas

- UI layer. Describe todo lo visual: cockpits, master-detail pages, pestañas, controles (botones, campos, listas), areas y sus bindings con los datos. Se define con UserInterface contracts (`05-ui-master-detail.md`).

- Process layer. Es el controlador. Define el flujo y la secuencia de acciones de un proceso de negocio (crear una orden, ejecutar una visita): instancia objetos, maneja las transiciones entre pantallas y procesa los eventos que dispara la UI. Se define con Process contracts (`04-contracts-action-types.md`).

- Business Objects + Business Logic. El modelo en memoria durante la ejecución. Incluye las entidades Business Object (BO), List Object y Lookup Object, y los Business Logic contracts: los métodos JavaScript (bl.js) que transforman datos, validan, manejan transacciones (crear/guardar) y aplican reglas de acceso (`06-logica-validaciones-acl.md`).

- Data Source layer. La capa de abstracción de datos: define cómo los atributos de un BO se mapean contra la estructura tabular física. Con los Datasource contracts, el framework construye dinámicamente el SQL para extraer, insertar, actualizar o eliminar datos de la SQLite local.

- Sync layer. El CG Cloud Synchronization Engine: maneja la transferencia asíncrona y basada en deltas entre la org de Salesforce y el cliente móvil, usando tracked objects y named fetch trees para reconciliar estructura, permisos y filas (`07-sincronizacion.md` y 8).

## 3. El VS Code Based Modeler

El Modeler es un entorno de desarrollo integrado en Visual Studio Code, que funciona como un plugin de la Salesforce CLI (@ind-rcg/modeler-sfdx-cli-plugin). En vez de editar código nativo, configuras Design Contracts en XML y scripts de lógica, neutrales frente a la tecnología final del dispositivo.

### 3.1 De contracts a Runtime Artifacts (RTAs)

Cuando corres sf modeler workspace build (o package), el Modeler toma los Design Contracts y los compila en Runtime Artifacts (RTAs): transforma los flujos y metadatos en un archivo consolidado (un fwrtas.json dentro del deployment package) y las operaciones XML de lógica en archivos JavaScript ejecutables (bl.js). Dos componentes hacen ese trabajo:

- Validator: verifica la correctitud semántica de los contracts contra los esquemas XML (las validaciones XSD que viste en el `04-contracts-action-types.md`).

- Generator: si el contract es válido, aplica las transformaciones y produce los artefactos ejecutables (el app definition) optimizados para el framework móvil.

### 3.2 El simulador

El simulador (Simulator UI application) corre localmente en http://localhost:3000 y levanta una réplica web en Chrome (preferentemente incógnito), emulando iOS o Android (teléfono y tablet). Te deja testear los RTAs construidos al instante, sin empaquetar ni desplegar a un dispositivo físico. Recuerda agregar localhost:3000 al CORS allowed list de la org (`03-setup-modeler-git.md`).

## 4. El contenedor vacío y el primer sync

La app corre en un contenedor nativo (Cordova) cuyo motor de persistencia es una base de datos SQLite cifrada (casmobile.db). Acá hay un concepto que confunde a muchos al principio: la app que se baja de la App Store o Google Play es un contenedor vacío. No trae configuración corporativa, ni layouts, ni datos: es un ejecutable cliente-independiente con la sola capacidad de conectarse a Salesforce.

Todo lo que hace que esa app sea "la app de tu cliente" llega en el primer sync (Initial Sync):

- Conecta con el backend y descarga el app definition vigente (el deployment package con los RTAs que construyó el Modeler) y el esquema de la base a partir de los metadatos de la Sync Configuration.

- Descarga las tablas, índices, valores de picklist y los tracked objects, y pobla el archivo SQLite para poder operar offline.

- Eventualmente dispara un First-Sync-of-Day que purga registros obsoletos del SQLite para estabilizar el tamaño y la consistencia (`07-sincronizacion.md`).

## 5. El Design Contract Package y el workspace

Salesforce publica en cada release (mayor o parche) un Design Contract Package (ModelerDesignContracts.zip) con los contracts core estándar del sistema. Ese paquete es la base que heredas y nunca modificas directamente: es el punto de partida de tu customización.

El workspace es el andamiaje local de directorios que creas con sf modeler workspace create:

| Carpeta / archivo | Qué contiene |
| --- | --- |
| src | Los contracts fuente en crudo: acá se descomprime el core del ModelerDesignContracts.zip (la rama de origen) y se agregan tus contracts customizados. |
| appl | La carpeta de la aplicación. Adentro: app, build (la salida del Generator: validación, compilación y el deployment.zip final), config (el config.json con sfConsumerKey, applicationId y puerto, que vincula el workspace con tu org de test) y data (información de runtime y el branch.config.json). |
| contractSnippets | Las plantillas por defecto que usa el wizard sf mdl add para crear recursos nuevos. |

La relación es directa: el core entra a src, lo customizas, el build lo compila a RTAs en appl/build, y el config.json (en appl/config) es lo que ata todo a tu org. El `03-setup-modeler-git.md` cubre el ciclo completo y la estrategia de branches Git para convivir con las releases.

## 6. Cómo fluye una interacción de extremo a extremo

Para fijar las capas, sigamos un solo tap a través de toda la arquitectura. Es el recorrido que, con variantes, hace cualquier acción de la app:

> Diagrama (descrito, no embebido): De un tap al dato y de vuelta: UI → Process → Business Logic → Datasource → SQLite, y el refresco por bindings.

- Tap en la UI. El usuario toca un control (p. ej. un ImageButton). Se levanta un evento de UI, como un ButtonPressedEvent con una etiqueta (event="NavigateTo").

- Transición en el Process. El Process (controlador) captura ese evento en su bloque <Events> y lo mapea a una <Action>, que ejecuta una TransitionTo hacia otro estado o corre lógica.

- Invocación de Business Logic. Si hace falta lógica, la acción llama a un método del BO vía su call (p. ej. ProcessContext::CurrentDisplay.miMetodo), que opera sobre el estado del objeto en memoria.

- Acceso a datos. Para leer o persistir, se despacha la instrucción al Datasource contract del objeto (p. ej. DsBoMyDisplay).

- Ejecución en SQLite. El Datasource resuelve una query SQL paramétrica e interactúa con la base local.

- Refresco de la UI. Al cambiar el estado de los objetos, el framework usa los bindings (ONE_WAY / TWO_WAY) para propagar de vuelta a la UI, y la pantalla se regenera. El círculo se cierra.

## 7. Errores conceptuales comunes

Estos son los malentendidos típicos de quien recién entiende la arquitectura. Tenerlos presentes te ahorra horas:

| Malentendido | La realidad |
| --- | --- |
| "Modifico el contract core y listo" | Nunca se tocan los contracts core directamente. Se usan ramas Git paralelas (core vs cust) y Pull Requests para integrar las releases sin colisiones (`03-setup-modeler-git.md`). |
| "Uso un UIPluginV2 para maquetar la pantalla" | El UIPluginV2 es un iFrame con HTML/JS y librerías externas: pesa en memoria y performance. Solo para lo que los controles nativos no cubren, como charts complejos (`09-uipluginv2-mobile-links.md`). |
| "Creo el campo y aparece en SQLite" | El esquema de SQLite lo impulsa el servidor vía Sync Configuration. Un campo custom no aparece localmente si antes no está en el Field Set y se distribuye con el sync (`07-sincronizacion.md`). |
| "Pruebo los deep links en el simulador" | Facade.startThirdPartyAsync y los deep links no corren en el simulador; hay que validarlos en un dispositivo físico (`09-uipluginv2-mobile-links.md`). |
| "Guardo el cambio y el simulador lo refleja" | Guardar el XML no actualiza localhost:3000. Hay que correr el build (Validator + Generator) para que el simulador consuma los RTAs recompilados. |

## 8. Puntos clave

- La app se configura con Design Contracts (XML) + lógica (bl.js), no con código nativo; el Modeler los compila.

- Cinco capas: UI (UserInterface), Process (controlador), Business Objects + Business Logic (modelo), Data Source (mapeo a SQL) y Sync (engine con Salesforce).

- El Modeler es un plugin de la Salesforce CLI: el Validator chequea los XSD y el Generator produce los RTAs; el simulador (localhost:3000) los prueba sin dispositivo.

- La app instalada es un contenedor vacío (SQLite cifrada casmobile.db); el primer sync baja el app definition, el esquema y los datos.

- Salesforce entrega el ModelerDesignContracts.zip (core) cada release; entra a src, se customiza, el build lo compila a appl/build, y el config.json (en appl/config) ata todo a tu org.

- Un tap viaja UI → Process → Business Logic → Datasource → SQLite, y vuelve a la UI por bindings.

## Checklist de verificacion

- Identificaste que capa(s) toca el cambio antes de escribir nada.
- Respetaste la responsabilidad de cada contract (no metiste logica en la vista ni datos en el proceso).
- La estructura del workspace es la esperada (todo bajo `appl/`).
