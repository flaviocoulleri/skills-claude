# Troubleshooting de sincronización

El `07-sincronizacion.md` te mostró cómo funciona el sync cuando todo va bien. Acá te preparas para cuando no: un rep que no ve datos que sí existen, un registro capturado en la calle que no sube, un sync que se cuelga en "Downloading data". El troubleshooting de sync es, sobre todo, saber dónde mirar y en qué orden, para no perder horas adivinando.

## Resumen operativo

- Triage por origen: CLIENT -> dispositivo/datos/red; SERVER -> configuracion (Named Query, Tracked Object, limites).
- Flujo: identificar -> Sync History (anota el Sync ID) -> Device Events Log + KPIs -> (si hace falta) Trace Mode + Request Logs -> corregir -> reset y re-sync.
- Lo que NO baja: suele ser Named Query mal armada (el `__c`) o governor limits (fallback a SF REST). Lo que NO sube: FLS/Sharing -> Clear Upload Failures.
- Herramientas (detalle en `ref-sync-management.md`): Device Status Overview, Sync History KPIs, Device Events Log, Named Query Analyzer, Remote Requests (Trace Mode, Clear Upload Failures, Resupply).

## 1. Cómo se ven los errores

Los mensajes de error se clasifican en tres categorías, y saber a cuál pertenece un error ya te dice dónde buscarlo:

- Sync Log Messages: errores de descarga, carga o fallos generales de sync. Se identifican por el namespace CGCloud en la página Device Events Log.

- Framework Log Messages: mensajes del propio dispositivo móvil. Usan el prefijo FW en el Event Code y el namespace CAS.

- Mobile Log Messages: errores intrínsecos del dispositivo; para analizarlos hay que activar el Trace Mode y descargar la información.

En la pantalla, el rep ve el estado en la Sync Card: un mensaje rojo al terminar indica errores; un signo de exclamación rojo señala fallo de carga o descarga de datos (aislado, es fallo de datos o datos + red); un ícono de cadena rota indica que la transferencia se cortó por la red.

El primer triage útil es el campo Error Originates From, que el Device Events Log informa como CLIENT o SERVER. Te orienta de entrada hacia dónde está el problema:

> Diagrama (descrito, no embebido): Triage por origen del error: CLIENT apunta al dispositivo/datos/red; SERVER, a la configuración (Named Query, Tracked Object, límites).

## 2. Los logs de sync

Cuando el ícono no alcanza, vas a los logs. Hay que entender tres cosas: los niveles, los archivos, y cómo accederlos.

### 2.1 Niveles y archivos

El log level define la severidad de lo que el dispositivo manda al backend: Security, Error, Warn, Info y Debug (más un nivel genérico "Log"). En los Log Settings del dispositivo puedes fijar topes de cantidad de eventos por período.

Los logs se guardan en el dispositivo como rolling logs (archivos rotativos): por defecto Log files count = 3 y Log files size = 1 MB (10 MB si el Trace Mode está activo). El almacenamiento interno es la SQLite cifrada casmobile.db.

### 2.2 Cómo acceder y correlacionar

- Device Events Log: objeto y vista dentro de Sync Management con los logs del cliente. Filtras por Event Code, Sync Version, Log Level o Namespace.

- Remote Requests → Request Logs: le ordenas al móvil que mande sus archivos de app y framework; después, desde Request History, usás Download Log para bajar el ZIP completo.

- Sync ID: cada sync genera un Sync ID único en la org. Es tu hilo conductor: cruzas el Sync History (en Salesforce) con los logs del dispositivo usando ese ID para aislar la transacción exacta y no perder tiempo.

## 3. Errores comunes

### 3.1 Registros que no bajan

Casi siempre es la evaluación de un NFT o un Tracked Object que falla porque la Named Query referencia objetos o columnas inválidos — el sospechoso clásico es un campo custom al que le falta el sufijo __c. También falla si se superan los governor limits de Salesforce (heap size, Apex CPU time) o los límites concurrentes.

- Si el error dice "Error Originates From: SERVER": corregí la Named Query (sintaxis, __c, objetos/columnas válidos).

- Si es por governor limits: la plataforma intenta un fallback automático a la Salesforce Standard REST API; si persiste, el admin habilita el flag SF Rest Enabled ("Use Salesforce Rest API to download tracked object") en el Tracked Object o NFT para procesar con más llamadas API y relajar los límites.

### 3.2 Registros que no suben

Un mensaje como "Failed to upload 1 record(s)" suele ser un problema de validación del servidor o de permisos: el usuario de ventas no tiene el acceso (FLS/Sharing) adecuado al Tracked Object.

- Qué le pasa al dato: con Upload Issue Management activado, el registro se saca de la cola y queda marcado _syncStatus = Not Syncable en casmobile.db (recuperable); desactivado, se borra de la base local (los nuevos desaparecen; los existentes se sobrescriben con la versión del servidor).

- Solución: revisa los Permission Sets del usuario, y usa el Remote Request Clear Upload Failures para vaciar la cola atascada.

### 3.3 Problemas de performance

Cuando el sync es lento o se cuelga, suele ser volumen de datos excesivo, sentencias ineficientes, o superar los límites (por ejemplo más de 200 usuarios concurrentes, que encola a los demás si Queue sync users at maximum limit está activo). Las dos herramientas: el Named Query Analyzer para reducir el recuento de SOQL, y convertir los NFTs a SF REST Enabled ("Sync using enhanced NFT over REST") para descargas incrementales.

## 4. Códigos de error

Los códigos que vas a ver con más frecuencia y qué hacer con cada uno:

| Código | Significado | Solución |
| --- | --- | --- |
| U2001 | Sync download failed | Revisar el descriptor de descarga: Named Queries y Tracked Objects involucrados |
| U2005 | Named query execution failed | Corregir la Named Query (sintaxis, sufijo __c, objetos/columnas válidos) |
| U0000 | Error de inicialización | Revisar el deployment package y reiniciar la app |
| U1000 | Fallo de autenticación del usuario | Revisar credenciales y permisos del usuario |
| U9000 | Conectividad de red limitada o nula | Recuperar señal y reintentar el sync |
| TQException 9806 | File download skipped: el archivo supera MaxBinaryFileSize | Aumentar el Max File Size (Download Limits) en Mobile Settings |
| TQException 9452 | ArgumentError: theFetchTreeName has to be a non-blank String | Revisar el nombre del NFT: no puede quedar vacío |

## 5. Las herramientas de Sync Management

Sync Management trae un set de herramientas de diagnóstico. Conocerlas es la diferencia entre resolver en minutos o en horas (el detalle de cada página de la app, con sus campos y parámetros, está en la Referencia de Sync Management):

| Herramienta | Para qué sirve |
| --- | --- |
| Device Status Overview | Salud integral (semáforo verde/amarillo/rojo) del Framework y del Sync. Permite Reset Status y ver métricas de API y KPI tracing. |
| Device KPI Tracing | Desglose cronológico de los endpoints APEX consumidos en Trace Mode: Time Taken (ms) y el SOQL Statement ejecutado. |
| Sync History & KPIs | Duración, llamadas API, volumen de subida/descarga, red y tipo de sync de cada evento; la pestaña KPIs lo abre por Tracked Object, NFT o Named Query. |
| Device Events Log | El log crudo, filtrable por Event Code o dispositivo: muestra el origen (CLIENT/SERVER) y los registros afectados. |
| Named Query Analyzer | Diagnostica y simula la ejecución de Named Queries sin un dispositivo físico; reporta el Call Tree de dependencias y el recuento de SOQL. |
| Remote Requests | Órdenes asíncronas al móvil: Activate Trace Mode, Clear Upload Failures, Resupply (reenviar datos de un Tracked Object), Request Logs/Data. |

## 6. Flujo sistemático de diagnóstico

Ante cualquier problema de sync, sigue siempre el mismo orden. Te evita saltar a conclusiones y te asegura cerrar el círculo:

> Diagrama (descrito, no embebido): El flujo de diagnóstico: identificar → Sync History (Sync ID) → Events Log + KPIs → (si hace falta) Trace Mode + logs → corregir → reset y re-sync.

- Identificar la anomalía. Verifica el código reportado en la app (p. ej. U2005) o el ícono de la Sync Card (exclamación roja = error de datos).

- Buscar la transacción en Sync History. En Sync Management → Sync History, filtra por Installation ID o usuario, ubica el evento fallido y anota el Sync ID.

- Inspeccionar KPIs y Device Events Log. Con View KPIs miras si un Tracked Object o NFT tardó demasiado o falló (columna Records with Error); en paralelo, filtras el Device Events Log por el Sync ID para ver el Event Code y si el origen es CLIENT o SERVER.

- Si no es evidente, activar Trace Mode. En Device Status Overview → Device Details Edit → Remote Requests, fija un Trace Mode Duration con Log Area = All o Synchronization; en el próximo intento del rep se recolecta el detalle.

- Descargar los logs. Ejecuta un Request Logs (o Request Statistics) y baja el ZIP desde Request History → Download Log.

- Acción correctiva. Si es configuración (Named Query / Tracked Object), valida con el Named Query Analyzer; si es cola de subida atascada, Clear Upload Failures; si falta data, Resupply apuntando a los Tracked Objects.

- Reset y verificación. Haz Reset Status para limpiar el semáforo y pídele al rep que ejecute un First-Sync-of-Day.

## 7. Caso práctico de punta a punta

Un representante reporta que su sync no pasa de "Downloading data" y termina con un error rojo y el código U2005. Lo resolvemos con el flujo de la sección 6.

- Sync History. Filtras por el usuario del rep y el Sync State fallido; anotas el Sync ID.

- Device Events Log. Con el Sync ID encuentras una entrada CGCloud: "Named query execution failed, Stage: Download descriptor, Error Originates From: SERVER". El origen SERVER te confirma que es configuración.

- Named Query Analyzer. Ingresas el Client App ID y el usuario; al evaluar las queries dependientes, la herramienta marca un fallo en la Named Query de Promotions. Detectas el error: el SOQL selecciona Promotion_Category en vez de Promotion_Category__c (faltaba el sufijo __c).

- Corregir. En la pestaña Named Queries de la configuración, ubicas el registro y corriges Promotion_Category a Promotion_Category__c; guardas y haces Execute en el configurador para verificar que ahora resuelve bien.

- Restaurar y confirmar. Para asegurar consistencia, en Device Details Edit creas un Remote Request Resupply para los Tracked Objects de Promociones; haces Reset Status del dispositivo y le pides al rep que sincronice. Esta vez termina bien y el dispositivo pasa a verde.

La moraleja se repite en la mayoría de los casos: el Sync ID te lleva al log, el log te dice el origen (CLIENT o SERVER), y el origen te lleva a la herramienta correcta. El resto es disciplina.

## 8. Puntos clave

- Tres categorías de error: Sync Log (namespace CGCloud), Framework (prefijo FW, namespace CAS) y Mobile (requiere Trace Mode). En la Sync Card: rojo = errores, exclamación = datos, cadena rota = red.

- El campo Error Originates From (CLIENT/SERVER) es el primer triage: CLIENT apunta al dispositivo/datos/permisos; SERVER, a la configuración (Named Query, Tracked Object, límites).

- El Sync ID es el hilo conductor: cruza el Sync History con el Device Events Log para aislar la transacción.

- Lo que no baja suele ser una Named Query mal armada (¡el __c!) o governor limits (fallback a SF REST / flag SF Rest Enabled). Lo que no sube suele ser FLS/Sharing (Clear Upload Failures).

- Las herramientas clave: Device Status Overview, Sync History KPIs, Device Events Log, Named Query Analyzer y Remote Requests (Trace Mode, Clear Upload Failures, Resupply).

- Códigos a memorizar: U2001 (download), U2005 (named query), U1000 (auth), U9000 (red), TQException 9806 (archivo > Max File Size).

- El flujo siempre cierra igual: corregir → Reset Status → pedir un First-Sync-of-Day.

## Checklist de verificacion

- Identificaste el origen (CLIENT vs SERVER) antes de tocar nada.
- Usaste el Sync ID como hilo entre Sync History y Device Events Log.
- Registro que no sube: revisaste FLS/Sharing y usaste Clear Upload Failures.
- Datos que faltan: validaste la Named Query (Analyzer) y probaste Resupply.
- Si hace falta detalle fino: Trace Mode + Request Logs.
