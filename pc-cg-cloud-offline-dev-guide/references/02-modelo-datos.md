# Modelo de datos offline

En el `01-arquitectura.md` vimos que la app se instala como un contenedor vacío y que su base de datos se materializa en el primer sync. Este módulo te enseña a decidir, con precisión, qué datos viven en el dispositivo y con qué forma. Es, posiblemente, la decisión de diseño más cara del desarrollo offline: si sincronizas de más, lentificas la sincronización, llenas el almacenamiento del dispositivo y disparas el consumo de API; si sincronizas de menos, al representante le falta información para trabajar en la góndola. Todo el módulo gira alrededor de ese equilibrio.

## Resumen operativo

- Tú decidis que baja al dispositivo, y el equilibrio es todo: de mas -> sync lento, storage lleno, API disparada; de menos -> al rep le falta info.
- Tracked Object = tabla local; la clausula `Where` acota filas; el Field Set acota columnas (sin field set baja todo).
- Named Queries devuelven IDs para restringir volumen (anidables en cascada); los Named Fetch Trees traen arboles relacionados en una sola request y bajan las llamadas a la API.
- Reglas de decision: filas -> Where/Named Query; columnas -> Field Set; jerarquia relacionada -> NFT (pre-sync lo que se necesita siempre; on-demand lo voluminoso o poco frecuente). Para que un campo viaje: field set MobilityRelevant + Tracked Object; para que vuelva: UploadRelevant.
- Fotos/binarios: se modelan con una `SimpleProperty type="DomBlob"` (`blobTable`/`blobPKeyField`); en la base local se guarda el path, no el binario. En el server van como `ContentVersion` vinculada por `ContentDocumentLink`, y se bajan con un NFT on-demand (`Registro -> ContentDocumentLink -> ContentDocument -> ContentVersion`). Patrón completo en `snippets.md` §12.

## 1. Tú modelas qué baja al dispositivo

Piensa el modelo de datos offline como cuatro decisiones sobre cada objeto que quieres tener disponible en el dispositivo: qué objeto sincronizar (Tracked Object), qué filas bajan (Sync Rules y Named Queries en el WHERE), qué columnas se exponen (Field Set), y cómo traer lo relacionado o lo puntual que no conviene pre-sincronizar (Named Fetch Trees). Estas cuatro decisiones, combinadas, determinan exactamente la base de datos local de cada representante.

> Diagrama (descrito, no embebido): La forma de la tabla local: la Sync Rule / Named Query acota las filas y el Field Set acota las columnas.

Mantén esta imagen presente durante todo el módulo: cada mecanismo que veamos cae en una de estas dos dimensiones (filas o columnas) o resuelve el problema de lo relacionado (los NFTs).

## 2. Tracked Objects

Un Tracked Object es un objeto estándar o custom de Salesforce que se sincroniza al dispositivo como una tabla de la base local (SQLite). Internamente se guardan como custom settings y definen qué registros recibe cada dispositivo.

### 2.1 Dónde se configura

Desde el App Launcher abres Sync Configuration (o la app Sync Management) → pestaña Tracked Objects → Add Tracked Object. El SELECT es implícito (lo dan el objeto y sus columnas); todo el control fino lo haces con los parámetros que siguen. El mapa completo de la app Sync Management y sus pestañas de configuración está en la Referencia de Sync Management.

### 2.2 Los parámetros de configuración

Estos son los parámetros que vas a tocar al definir un Tracked Object. No es necesario que uses todos, pero conviene conocerlos porque varios resuelven problemas concretos de performance y de integridad:

| Parámetro | Para qué sirve |
| --- | --- |
| Object | El API name del objeto de Salesforce a trackear (estándar o custom). |
| Replace $user Macro with | En diseño, un usuario para sustituir la macro $user y evaluar el resultado considerando su sharing y field-level security. |
| Where | Una SOQL válida (máx. 1020 caracteres) que se concatena a la consulta de sync y acota los registros. Vacío = se sincronizan TODOS los registros a TODOS los dispositivos. |
| First Sync of Day | Si está activo, en el ciclo First-Sync-of-Day se refrescan exhaustivamente todos los registros del objeto: limpia inválidos e inyecta los faltantes. |
| Use Salesforce REST API… | Fuerza el uso de la REST API estándar en vez de los endpoints Apex. Los Apex están optimizados para volumen, pero ante governor limits restrictivos, REST evita fallos transaccionales. |
| Allow Null Values | Permite ingresar valores nulos para los KPIs. |
| Show Pending Upload + Condition | Hace que el objeto participe en la vista Pending Upload del Sync Cockpit, según una condición (columna, operador, valor). |
| Manage upload issues | Define qué hace la cola de carga ante un fallo: retener y marcar "Not Syncable", o limpiar de la base local y forzar el redescenso en el próximo sync. |
| Field Sets | Acota la sincronización a los campos del field set (p. ej. MobilityRelevant). Sin field set, se sincronizan todos los campos. |
| Index List | Genera índices (simples o compuestos) sobre la tabla local, para acelerar las consultas en el dispositivo. |
| Transactionally Dependent Lookup | Liga transaccionalmente el registro padre con hasta 10 dependientes, para garantizar atomicidad en la base local. |

### 2.3 Una configuración real

Así se ve, en concreto, un Tracked Object para un objeto custom de exhibiciones (Display__c), acotado al sales org del usuario y a un conjunto de displays relevantes calculado por una named query:

```
Object:             Display__c
Where:              Sales_Org__c = $User.cgcloud__Sales_Org__c
                    AND Id IN ::RelevantDisplays::
Field Sets:         MobilityRelevant
First Sync of Day:  ✓
```

### 2.4 Jerarquía de configuraciones

Los tracked objects no viven sueltos: pertenecen a una configuración, y las configuraciones forman una jerarquía de hasta tres niveles. Una configuración hija hereda las propiedades del tracked object de su configuración padre inmediata. Esto te deja definir una base común (la configuración Standard) y especializarla por mercado o por perfil sin duplicar todo.

## 3. Sync Rules

Las Sync Rules controlan exactamente qué datos bajan, para que el representante reciba solo lo que su proceso necesita y para optimizar las llamadas a la API y el ancho de banda. Hay dos categorías, y la diferencia es dónde vive la lógica del filtro:

- Sync Rules for Tracked Objects: el filtro va directo en el WHERE del objeto, con variables o banderas pre-procesadas. Por ejemplo, Id IN ::RelevantVisitsforUserCockpit:: o una bandera booleana que un proceso dejó calculada.

- Sync Rules for Named Queries: el filtro se arma con named queries que devuelven IDs de forma jerárquica. Por ejemplo, StoresVisited identifica las tiendas que visitó el usuario en un rango de fechas, y AccountsVisited usa esos IDs para filtrar las cuentas.

En la práctica casi siempre terminas combinando las dos: named queries para resolver el alcance jerárquico, y filtros directos para condiciones simples sobre el propio objeto.

## 4. Named Queries

### 4.1 Qué son y qué devuelven

Una Named Query es una SOQL válida que, por defecto, devuelve exclusivamente una lista de IDs, pensada para restringir el volumen de datos que se distribuye. Para escenarios especiales (por ejemplo, esquemas complejos de cálculo de precios) se pueden seleccionar varias columnas separadas por comas, y la query devuelve los valores fusionados en un único result set; pero el caso normal es "SELECT Id".

### 4.2 Anidamiento: la cadena de filtrado

El poder de las named queries está en el anidamiento: una query referencia a otra con la sintaxis ::Nombre::, y así armas una cadena donde cada paso acota el siguiente. Este es un encadenamiento realista para llevarle al dispositivo las visitas del usuario y, a partir de ellas, sus tiendas, cuentas y contactos:

```
StoresVisited:
  SELECT RetailStoreId FROM Visit
  WHERE VisitorId = $User.Id
    AND (PlannedVisitStartTime = LAST_N_DAYS:7
         OR PlannedVisitStartTime = NEXT_N_DAYS:14)
    AND RetailStoreId != null
 
AccountsVisited:
  SELECT AccountId FROM RetailStore
  WHERE Id IN ::StoresVisited:: AND AccountId != null
 
AccountContactsVisited:
  SELECT Id FROM Contact WHERE AccountId IN ::AccountsVisited::
 
ContactsVisited:
  SELECT PrimaryContactId FROM RetailStore WHERE Id IN ::StoresVisited::
 
AllContactsVisited:
  SELECT Id FROM Contact
  WHERE Id IN ::AccountContactsVisited:: OR Id IN ::ContactsVisited::
```

> Diagrama (descrito, no embebido): Cascada de Named Queries: cada una devuelve IDs que alimentan a la siguiente.

Hay un beneficio técnico clave además de la reutilización: usar una named query en el WHERE de un Tracked Object te permite saltar el límite estándar de SOQL sobre subqueries anidadas. Por eso es la forma de expresar filtrados jerárquicos que, escritos como una sola SOQL, no serían válidos.

### 4.3 Qué combinaciones se permiten en el WHERE

No todo vale en el WHERE de un Tracked Object cuando intervienen named queries. Estas son las combinaciones soportadas y las que no:

| Combinación en el WHERE | ¿Soportada? |
| --- | --- |
| Una named query + filtros: Id IN ::NQ1:: AND Name = 'X' | Sí |
| Varias named queries con OR: Id IN ::NQ1:: OR Id IN ::NQ2:: | Sí |
| Varias named queries con AND: Id IN ::NQ1:: AND Id IN ::NQ2:: | Sí |
| Varias named queries + filtros: ::NQ1:: OR ::NQ2:: AND Name = 'X' | No |
| Mezcla cruzada de OR y AND para el motor de named queries | No |

### 4.4 Límites que tienes que conocer

| Límite | Valor |
| --- | --- |
| Anidamiento de named queries dentro de otra | 7 como máximo |
| Resoluciones totales de named queries al evaluar un Tracked Object | 99 como máximo |
| Tamaño del result set | 25.000 IDs |
| Longitud de la cláusula WHERE | 1.020 caracteres |
| Governor limits del endpoint Apex | CPU, heap, ConcurrentPerOrgApex y filas; si se exceden, falla en silencio y cae a REST API |

Ese último punto importa: cuando el endpoint Apex se pasa de un governor limit, la descarga no se cae con un error visible — hace fallback a la REST API estándar, que tiene límites más laxos pero pierde la eficiencia de batching y dispara muchas más llamadas a la API. Un modelo que "funciona pero sincroniza lento y gasta API" suele ser esto.

### 4.5 Batch vs. directo

Para objetos pesados (como Orders y Visits), evaluar named queries complejas en cada sync es caro. La alternativa es el enfoque batch: un proceso por lotes evalúa periódicamente los registros, escribe una bandera de distribución (distribution-relevant flag) en la base, y el Tracked Object simplemente consulta esa bandera en su WHERE. El sync queda liviano, a cambio de depender de que el batch haya corrido y de cierta latencia entre el cambio y su disponibilidad en el dispositivo. Regla práctica: filtrado directo para objetos chicos y condiciones simples; batch cuando el cálculo del alcance es pesado o se comparte entre muchos dispositivos.

## 5. Field Sets e índices

Mientras las sync rules y las named queries deciden las filas, los Field Sets deciden las columnas. Un field set lista los campos relevantes para la app móvil; por convención sueles tener uno del estilo MobilityRelevant por objeto.

Al seleccionar el field set en la configuración del Tracked Object, la tabla generada en el dispositivo importa y muestra solo esos campos. Si no seleccionas field set, se sincronizan todos los campos del objeto: más almacenamiento, sync más lento y mayor riesgo de tocar governor limits. En objetos con muchos campos, definir el field set es prácticamente obligatorio.

De la mano del field set va el Index List: una vez que la tabla local existe, puedes declarar índices (simples o compuestos) sobre las columnas por las que vas a filtrar o joinear en el dispositivo. No cambia qué datos bajan, pero cambia mucho la performance de las consultas locales (las que arma la Data Source layer del `01-arquitectura.md`).

## 6. Named Fetch Trees

### 6.1 Qué son y su estructura

Los Named Fetch Trees (NFTs) describen una relación jerárquica entre varios objetos para traer datos relacionados en una sola request, reduciendo las llamadas a la API. Tienen un objeto raíz (root) y uno o más nodos hijos y nietos (child y subchild), donde cada nodo se vincula al padre por un par de campos.

> Diagrama (descrito, no embebido): Un Named Fetch Tree del modelo Contract: el contrato raíz con sus productos y tácticas como nodos hijos.

### 6.2 Cómo se define

Se crean en Sync Configuration → Named Fetched Trees → New. Los pasos:

- Ingresa un nombre para el NFT (el nombre se define en el nodo padre; los hijos heredan el de la raíz).

- Selecciona el Object API name del que se recupera la data.

- Elige el Join Field: la columna de anclaje local para cruzar el nodo.

- Opcionalmente, elige el Parent Join Field: el campo del padre que se compara con el del hijo.

- Define la cláusula Where para filtrar los registros del nodo.

- Marca SF Rest Enabled si necesitas forzar la REST API para ese nodo.

Llevado al ejemplo del diagrama (un contrato comercial con sus productos y tácticas), la definición de nodos queda así:

| Nodo | Object | Join Field | Parent Join Field |
| --- | --- | --- | --- |
| Raíz | Contract__c | Account__c | (ninguno) |
| Hijo | Contract_Product__c | Contract__c | Id |
| Hijo | Contract_Tactic__c | Contract__c | Id |

El nodo raíz recibe las cuentas como parámetros externos (los root IDs) y actúa como lookup; cada hijo cuelga del Id del padre vía su Join Field.

### 6.3 Pre-sync vs. on-demand

La gran decisión con un NFT es cuándo cargarlo:

- Pre-sync: por defecto, los NFTs no se cargan en cada sync estándar de la app. No inflan la base de todos los dispositivos.

- On-demand: la lógica de negocio los pide cuando hacen falta. Cuando se necesitan datos que no están en el dispositivo (por ejemplo, descargar adjuntos obligatorios o el contrato de una tienda al abrirla), se invoca el callback de replicación, que obtiene los IDs y fuerza el fetch inmediato a la base local:

```
// La lógica de negocio detecta que faltan datos y los pide:
BoSfReplicationCallback.requestOnDemandDataAsync(...)
 
//   internamente ejecuta el fetch del árbol contra el servidor:
Facade.requestSfDataOnDemandAsync(<nombre del NFT>, <array de ids>)
```

Criterio práctico: pre-sincroniza lo que el representante necesita siempre y para todas sus tiendas; deja on-demand lo voluminoso o poco frecuente (contratos, adjuntos, históricos), para no pagar su costo en cada dispositivo y en cada sync.

## 7. Performance, límites y errores comunes

Un modelo de datos mal armado no "anda un poco más lento": colapsa la capa de sincronización. Estos son los problemas más frecuentes, su causa y cómo se manifiestan.

| Síntoma / código | Causa típica | Qué revisar |
| --- | --- | --- |
| La tabla entera de la org baja a todos los dispositivos | WHERE vacío en el Tracked Object | Agregar un WHERE o una named query que acote los registros |
| Sync lento y explosión de llamadas a la API | Demasiadas columnas/registros: el endpoint Apex excede CPU/heap y cae a REST API | Definir field set, acotar registros, agregar índices, considerar batch |
| U2001 (Sync download failed) / U2005 (Named query execution failed) bloquean la app | Named query mal armada u objeto/columna inexistente | Nombres de objeto, sufijo __c y columnas en el Sync Configurator |
| TQException 9806 (File download skipped, size > MaxBinaryFileSize) | Blobs/imágenes grandes sin filtrar en un NFT | Filtrar o limitar los binarios que trae el árbol |
| Comportamiento inestable / WHERE roto | Superar 7 anidamientos o 99 resoluciones de named queries | Reducir la profundidad y la cantidad de named queries |

Dónde mirar: en el dispositivo, el indicador de sync muestra un ícono de exclamación rojo con el código (U2001, U2005, etc.). En el backend, el Device Events Log trae el Event Code y un mensaje como "Named query execution failed, Stage: Download descriptor, Error Originates From: SERVER", que te orienta a validar nombres de objetos, sufijos y columnas en la configuración.

## 8. Caso práctico de punta a punta

Cerramos con un escenario completo, que es como vas a pensar el modelo en un proyecto real. Objetivo: que el representante tenga en el dispositivo sus visitas de las próximas dos semanas (y las recientes), las tiendas de esas visitas, sus cuentas y contactos, y que el contrato promocional de una tienda se traiga solo cuando la abre.

Paso 1 — Tracked Objects. Trackeas Visit, RetailStore, Account, Contact (y Order / Order Item si hay toma de pedidos). A cada uno le asignas un field set MobilityRelevant para no arrastrar columnas de más, e índices sobre las columnas de join (por ejemplo RetailStore.AccountId).

Paso 2 — Cadena de named queries. Reutilizas la cadena de la sección 4.2: StoresVisited → AccountsVisited → AccountContactsVisited / ContactsVisited → AllContactsVisited.

Paso 3 — Conectas cada WHERE a su filtro:

```
Visit:        VisitorId = $User.Id AND (rango de fechas)   // filtro directo
RetailStore:  Id IN ::StoresVisited::
Account:      Id IN ::AccountsVisited::
Contact:      Id IN ::AllContactsVisited::
```

Paso 4 — Lo voluminoso, on-demand. El contrato promocional (Contract__c con sus productos y tácticas) NO se pre-sincroniza: defines el NFT de la sección 6 y lo disparas con Facade.requestSfDataOnDemandAsync cuando el representante abre la tienda. Así cada dispositivo trae su set de trabajo justo, y los datos pesados llegan solo cuando hacen falta.

El resultado es un modelo que respeta el equilibrio del principio: cada representante recibe exactamente lo suyo, con columnas acotadas, sin reventar la API ni el almacenamiento, y con los datos caros bajo demanda.

## 9. Puntos clave

- El modelo offline son cuatro decisiones: qué objeto (Tracked Object), qué filas (Sync Rules / Named Queries), qué columnas (Field Set) y cómo traer lo relacionado/on-demand (NFT).

- El Tracked Object tiene muchos parámetros más allá del WHERE: First Sync of Day, REST API, Index List, Transactionally Dependent Lookup, Manage upload issues. Conocerlos es resolver problemas de performance e integridad.

- Las named queries devuelven IDs, se anidan con ::Nombre:: (hasta 7 niveles, 99 resoluciones, 25.000 IDs, 1020 chars) y, en el WHERE, solo admiten ciertas combinaciones de AND/OR.

- Si el endpoint Apex se pasa de un governor limit, cae a REST API en silencio: sync lento y derroche de API son la pista.

- El Field Set acota columnas y los índices aceleran las consultas locales; sin field set baja todo y se degrada el rendimiento.

- Los NFTs traen árboles relacionados en una request; pre-sincroniza lo que se necesita siempre y deja on-demand lo voluminoso o poco frecuente.

## Checklist de verificacion

- El scope de filas esta acotado con `Where`/Named Query y no baja de mas.
- El Field Set limita las columnas a lo necesario.
- Combinaciones SOQL validas: no mezclaste `OR` de subconsultas con `AND` de campos de forma invalida (usa NQ anidadas).
- El campo esta en el field set MobilityRelevant y en el Tracked Object para viajar, y marcado UploadRelevant si debe volver.
- Jerarquias: pre-sync para lo siempre-necesario, NFT on-demand para lo voluminoso.
