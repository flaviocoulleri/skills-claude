# Sincronización

La app es offline: el representante trabaja sin señal y la base de datos local es la fuente de verdad mientras está en la calle. La sincronización es el puente que mantiene esa base local alineada con Salesforce: sube lo que el rep capturó y baja lo que cambió en la org. Entender el sync es entender por qué un dato aparece (o no) en el dispositivo, y qué pasa cuando algo no se puede subir.

Este módulo cubre el motor de sync: los tres tipos de sincronización y su orden, qué controla lo que baja, cómo suben los cambios y cómo se resuelven los conflictos, la consola de administración, los límites, y un recorrido completo de un registro. El `08-troubleshooting-sync.md` se dedica a diagnosticar cuando el sync falla.

## Resumen operativo

- El sync alinea casmobile.db con el org: primero sube los cambios locales, despues baja los datos filtrados.
- Orden de un Regular Sync: Connecting -> Upload -> Download (Named Queries + Tracked Objects -> registros -> NFTs) -> Listo.
- Tipos: FSOD/Initial (primera carga completa), Regular (incremental) y background (Complete / Upload Only / Deactivated).
- Para que un cambio vuelva al servidor el campo debe ser UploadRelevant. Consola y verificacion: `ref-sync-management.md`; diagnostico: `08-troubleshooting-sync.md`.

## 1. Qué es sincronizar

El motor de sync transfiere datos entre Salesforce y la base de datos local del dispositivo, una SQLite llamada casmobile.db. Un ciclo de sync tiene dos mitades: el Upload (subir los cambios que el rep hizo offline) y el Download (bajar los registros nuevos o modificados que le corresponden). El orden importa: salvo en el primer sync, siempre se sube antes de bajar.

> Diagrama (descrito, no embebido): El sync mantiene casmobile.db alineada con la org: primero sube los cambios, después baja los datos filtrados.

## 2. Los tres tipos de sync

No todos los syncs son iguales. Hay tres, y se diferencian por cuánto mueven y en qué orden.

> Diagrama (descrito, no embebido): El orden de un Regular Sync: Connecting → Upload → Download (Named Queries + Tracked Objects → registros → NFTs) → Listo.

### 2.1 Initial Sync

Es el primer sync después de instalar la app. No hay Upload, porque el dispositivo es un contenedor vacío. El orden: Connecting (verificación y autenticación) → Downloading app content → carga de configuración y metadatos de los Tracked Objects → inicialización de la base → migración de scheduled jobs → Downloading data → evaluación de Named Queries y Tracked Objects → descarga de los registros → Configuring app → Downloading more data → descarga de los Named Fetch Trees.

### 2.2 First-Sync-of-Day (FSOD)

Se ejecuta al inicio de la jornada: hace una limpieza exhaustiva y mueve volúmenes grandes. El orden es estricto: Connecting → Uploading data (primero, para asegurar que cualquier cambio local llegue al servidor) → Downloading data → evaluación de Named Queries y Tracked Objects → descarga de registros → limpieza y descarga de IDs faltantes → descarga on-demand → descarga de NFTs → Purging (limpieza de datos obsoletos) y limpieza de logs de NFTs. El usuario queda bloqueado hasta que termina.

### 2.3 Regular Sync (incremental / delta)

Es el del día a día (y el On-Demand). Sube los datos modificados y baja solo lo estrictamente necesario y cambiado, para reducir llamadas API y ancho de banda. Como siempre, prioriza el Upload antes del Download.

## 3. Qué baja al dispositivo

Qué registros bajan a cada usuario lo decide un algoritmo de mapeo basado en Assignments (por usuario, perfil o rol). Las tres piezas que filtran son las que ya conoces del `02-modelo-datos.md`, ahora vistas desde el sync:

- Tracked Objects: objetos estándar o custom que se sincronizan como tabla local. Se guardan como custom settings y usan una cláusula Where de SOQL para decir qué registros bajar; un Where vacío baja todos.

- Named Queries: SOQL válido que devuelve solo una lista de IDs. Se usan dentro del Where de un Tracked Object para esquivar los límites de subconsultas anidadas de Salesforce, y se pueden anidar una dentro de otra.

- Named Fetch Trees (NFTs): describen relaciones jerárquicas (root object + nodos hijos unidos por Object Join y Parent Join) y traen varios objetos en una sola petición REST o APEX, reduciendo llamadas API.

El macro $user es clave para personalizar la descarga: en la consulta se reemplaza por el ID del usuario, pero la query corre en el contexto del usuario autenticado, así que respeta estrictamente el sharing, la field-level security y la object-level security. Un ejemplo de Where de un Tracked Object con macro y Named Query:

```
Sales_Org__c = $User.cgcloud__Mobility_Sales_Org__c
  AND Id IN ::RelevantDisplays::
```

## 4. Qué sube y manejo de conflictos

Cuando el rep crea, edita o borra algo offline, la operación se persiste de forma asíncrona con Facade.saveTrackedObject, que evalúa el parámetro changeType (N nuevo, U update, D delete) y encola el INSERT, UPDATE o DELETE en el buffer SQL local:

```
Facade.saveTrackedObject({ changeType: "N", /* ...campos... */ });
// el objeto queda marcado STATE.NEW | STATE.DIRTY en casmobile.db
```

En el paso de Uploading, el dispositivo sube esos registros marcados. Pero, ¿qué pasa si Salesforce rechaza la subida (una validación del servidor, un permiso)? Eso lo decide, por Tracked Object, la bandera Manage upload issues (Upload Issue Management):

- Activada: el registro que falla se saca de la cola de carga pero se marca _syncStatus = Not Syncable en casmobile.db. El rep lo puede corregir y reintentar el sync. No pierde el dato.

- Desactivada: el registro con error se elimina de la cola y de la base móvil. Si era nuevo, desaparece de casmobile.db. Si era uno existente que falló al actualizarse, el dispositivo sobrescribe su copia local bajando la versión más reciente desde Salesforce en el próximo sync.

La decisión es de diseño: activa Upload Issue Management cuando perder un dato capturado en la calle sea inaceptable; déjala desactivada cuando prefieres que la verdad del servidor gane siempre.

## 5. La consola Sync Management

Sync Management es la app donde el administrador gestiona los metadatos de sync y los artefactos móviles. Acá vemos las dos áreas que más te importan como desarrollador; el mapa completo de la app (todas sus páginas, configuraciones y herramientas de diagnóstico) está en la Referencia de Sync Management. Dos áreas:

- Deployment Packages: las customizaciones que armaste con el Modeler se empaquetan en un deployment.zip (`03-setup-modeler-git.md`). Acá se publican y se activan en Deploy Package Assignment, asignables a nivel All o User. La app detecta el paquete nuevo en el siguiente ciclo (paso Configuring app) y lo instala al reiniciar. Un deployment package se descarga en cada sync, incluido el background sync.

- Scheduling / Sync Settings: el Background Sync se automatiza con el parámetro intervalInSeconds (configurable entre 10 y 9999 minutos), y soporta los tipos Complete Sync, Upload Only o Deactivated. La concurrencia se controla con Queue sync users at maximum limit, que manda notificaciones push si se supera la capacidad.

## 6. Límites y parámetros

Estos límites condicionan cómo diseñas la distribución de datos. Conocerlos de memoria te evita rediseños tardíos:

| Área | Límites |
| --- | --- |
| Tracked Objects | Máx 1000 mapeos por custom setting. Máx 1020 objetos transaccionalmente dependientes insertables en una sola transacción de base de datos. |
| Named Queries | Máx 99 resueltas en el Where de un Tracked Object. Profundidad de anidación máx 7. SOQL ≤ 1020 caracteres. Result set ≤ 25000 IDs. Máx 1000 consultas por custom setting. |
| Named Fetch Trees | Máx 7 child NFTs por transacción APEX. Where ≤ 1020 caracteres. Máx 1000 NFTs por custom setting. |
| Usuarios concurrentes | Entre 2 y 600 usuarios sincronizando en simultáneo (valor recomendado: 200). |
| Logs | Buffer JS por defecto 10000 (mín 100, máx 70000). De 1 a 5 archivos de log rodantes, de 1 a 10 MB (con Trace Mode el default sube a 10 MB). |

## 7. Caso práctico de punta a punta

Sigamos un registro del objeto custom Display__c (inspección de exhibidores en tienda) por un ciclo completo, atando todo lo anterior.

- Backend: el admin expone el objeto agregando los campos críticos a un Field Set MobilityRelevant, y define una Named Query RelevantDisplays:

```
Select Id From Display__c WHERE Account__c IN ::RelevantAccountsForUser::
```

- Tracked Object: en el Sync Configurator asocia el Tracked Object a Display__c con el Where que combina el macro y la Named Query:

```
Sales_Org__c = $User.cgcloud__Mobility_Sales_Org__c
  AND Id IN ::RelevantDisplays::
```

- Captura local: el rep crea un Display__c offline. La lógica llama Facade.saveTrackedObject({ changeType: "N", ... }), el objeto queda STATE.NEW | STATE.DIRTY y se encola en casmobile.db.

- Ejecuta el sync: fuerza un Regular Sync; arranca la etapa Connecting.

- Uploading: el motor lee el estado DIRTY del Display__c y sube el JSON del registro nuevo; queda consolidado en la nube.

- Downloading: reevalúa la Named Query en el contexto del rep ($user mapeado a su usuario), obtiene ≤ 25000 IDs, aplica el filtro del Tracked Object para aislar los exhibidores de su Sales_Org__c, y baja los metadatos por APEX o REST.

- NFT y cierre: si hay un NFT anidado (p. ej. NFT_Display para traer el ContentDocumentLink de las fotos), corre en Downloading named fetch tree data; la UI renderiza el registro con sus fotos y el indicador de Sync Status pasa a verde.

## 8. Puntos clave

- El sync alinea la base local (casmobile.db) con Salesforce: Upload (cambios locales) + Download (lo nuevo/modificado). Salvo el Initial Sync, siempre sube antes de bajar.

- Tres tipos: Initial (sin upload, dispositivo vacío), First-Sync-of-Day (limpieza + volúmenes grandes, bloquea al usuario), y Regular/delta (el día a día, mínimo movimiento).

- Lo que baja se filtra con Tracked Objects (Where), Named Queries (listas de IDs) y NFTs (relaciones jerárquicas); el macro $user corre en el contexto del usuario y respeta sharing/FLS/OLS.

- Lo que sube se encola con Facade.saveTrackedObject (changeType N/U/D). Los conflictos los maneja Upload Issue Management: activado conserva el dato como Not Syncable; desactivado deja ganar al servidor.

- Sync Management administra los deployment packages (asignación All/User) y el background sync (intervalInSeconds, Complete/Upload Only/Deactivated).

- Memoriza los límites: 99 Named Queries por Where, anidación 7, 25000 IDs, 1020 chars, 1000 mapeos por custom setting, 7 child NFTs, 2–600 usuarios concurrentes.

## Checklist de verificacion

- El campo que debe volver esta marcado UploadRelevant.
- Elegiste el tipo de sync correcto (background Complete vs Upload Only) para el caso.
- Verificaste en Sync History (Sync ID) que baja y sube lo esperado.
- Contemplaste el manejo de conflictos.
