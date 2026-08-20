# API de bl.js (runtime de business logic)

Esta es la referencia AUTORITATIVA de la API disponible dentro de los archivos `bl.js`.
Cuando escribas lógica de negocio, toma los nombres de acá; no reconstruyas firmas de
memoria. La lógica corre en el hilo **Engine**.

## Resumen operativo

- Persistencia: el action `SAVE` del proceso (y el framework) persiste el objeto del proceso; `beforeSaveAsync`/`afterSaveAsync` son HOOKS de lógica pre/post-guardado, no el guardado en sí. Para persistir objetos o registros relacionados de forma imperativa desde bl.js: `Facade.saveObjectAsync(obj)` (llena el buffer SQL) + `Facade.commitTransaction()` (ejecuta atómico).
- Cargar/crear objetos desde lógica: usa `BoFactory` (`loadObjectByParamsAsync`, `createListAsync`, `createAsync`); `Facade` queda para guardar/commit, archivos y dispositivo. Todo es async y devuelve promesa. Nunca SOQL directo desde bl.js.
- ApexDoc: marca `@module CUSTOM` en tu lógica (código de cliente/partner) para que el upgrade de release sea limpio (`CORE` es del producto). Un método bl.js = un archivo, nombrado `<Objeto>.<Metodo>.bl.js`.
- Propiedades del Business Object: getters/setters generados por campo (`getName()`, `setName(v)`), o `updateProperties({...})` para varias a la vez.
- Fechas: usa siempre los helpers ANSI de `Utils` (no `Date` crudo).
- Mensajes: `MessageBox.displayMessage(...)` para diálogos; `messageCollector.add({...})` para errores de validación.

## Acceso a propiedades del Business Object

Getters/setters se generan por nombre de propiedad (primera letra en mayúscula):

```
var me = this;
var pk   = me.getPKey();               // getter
me.setOrderMetaPKey(value);            // setter
me.updateProperties({                   // varias a la vez, sin cambiar el status del objeto
    "quantity": 12,
    "reason": "Sin stock"
});
```

Aplica a Simple Properties, Nested Objects y List Objects.

## Facade — datos, dispositivo e integraciones

Es la capa entre la lógica y los servicios (base local, cámara, GPS, terceros).

Acceso a datos (async, devuelven promesa):

| Método | Qué hace |
| --- | --- |
| `BoFactory.loadObjectByParamsAsync(TYPE, {params:[{field, value, operator}]})` | Carga un objeto por criterios (operator = `"EQ"`, etc.). La forma idiomática de traer un objeto desde lógica. |
| `BoFactory.createListAsync(LO_TYPE, {})` | Instancia un List Object nuevo. |
| `BoFactory.createAsync(TYPE, {...})` | Instancia un Business Object nuevo. |
| `Facade.getObjectAsync(objectClass, jsonQuery)` | Trae una instancia única (por PKey o criterio). |
| `Facade.getListAsync(objectClass, jsonQuery)` | Trae una lista según el `jsonQuery`. |
| `Facade.loadLookupsAsync(jsonParams)` | Carga objetos Lookup (read-only, info limitada). |
| `Facade.saveObjectAsync(object)` | Llena el buffer de SQL (INSERT/UPDATE/DELETE). NO guarda solo. |
| `Facade.saveListAsync(listObject)` | Igual, para todos los ítems de un List Object. |
| `Facade.commitTransaction()` | Ejecuta el buffer de SQL acumulado en una transacción atómica. |
| `Facade.loadFileAsync(path)` | Carga un archivo (base para trabajar con JSON). |

`TYPE` / `LO_TYPE` son constantes generadas en mayúsculas (`LO_ORDERITEMS`, `LO_SDOCONDITIONS`…). PKeys nuevos: `PKey.next()`. Estado de un registro/ítem: `.setObjectStatus(me.self.STATE_NEW_DIRTY)` (constantes tipo `STATE_NEW_DIRTY`).

Dispositivo e integraciones:

| Método | Qué hace |
| --- | --- |
| `Facade.startThirdPartyAsync(url, jsonParams)` | Abre apps de terceros vía deep link (ej. Google Maps). El allowlist de iOS/Android importa. |
| `Facade.getPictureAsync(cameraSettings, source)` | Invoca cámara o galería (Cordova). `cameraSettings` = `{ quality: 0-100, encodingType: 'jpeg'|'png' }`; `source` = `"CAMERA"` \| `"IMAGE_LIBRARY"` \| `null`. Devuelve una promesa que resuelve con la URI/path de la imagen. Ver el patrón de guardado en `snippets.md` §12. |
| `Facade.getBarCodeScannerDataAsync()` | Activa el escáner de códigos de barras. |
| `Facade.sendEmailAsync(emailObject)` | Abre el cliente de correo con destinatarios/asunto/cuerpo. |
| `Facade.startPhoneCall(dial)` | Inicia una llamada con el marcador nativo. |
| `Facade.getNetworkConnectionStatus()` | Estado de red actual. |

## Utils — helpers

Validación y strings:

| Método | Qué hace |
| --- | --- |
| `Utils.isEmptyString(v)` | `true` si es vacío, null, undefined o solo espacios. |
| `Utils.isDefined(v)` | `true` si está inicializada (no null/undefined). |
| `Utils.isBlankString(t)` | `true` si es solo espacios y CRLF. |
| `Utils.identity(value)` | Devuelve el valor tal cual; se usa en acciones `LOGIC` para escribir en variables del ProcessContext sin JS extra. |

Fechas (ANSI = `YYYY-MM-DD`):

| Método | Qué hace |
| --- | --- |
| `Utils.createAnsiDateToday()` | Fecha de hoy en ANSI. |
| `Utils.createAnsiDateTimeNow()` / `createAnsiDateNow()` | Timestamp actual en ANSI. |
| `Utils.convertDate2Ansi(date)` | `Date` de JS → string ANSI. |
| `Utils.convertAnsiDate2Date(ansi)` | String ANSI → `Date` de JS (para aritmética). |
| `Utils.addDays2AnsiDate(sDate, iDays)` | Suma/resta días a una fecha ANSI. |
| `Utils.addDays2AnsiFullDate(sDate, iDays)` | Igual, conservando la parte de hora. |
| `Utils.convertAnsiTime2Time(v)` / `convertAnsiDateTime2AnsiDate(s)` | Conversiones de tiempo/fecha ANSI. |

Matemática y colecciones:

| Método | Qué hace |
| --- | --- |
| `Utils.round(value, precision, mode)` | Redondea; `mode` = financiero, `UP` o `DOWN`. |
| `Utils.createDictionary()` | Diccionario clave-valor con `add`, `get`, `remove`, `containsKey`, `keys`. |
| `Utils.distanceBetween(lat1, lon1, lat2, lon2, unit)` | Distancia geográfica entre dos coordenadas. |

## Contextos

```
// Usuario actual (BoUser) y sus roles
var user = ApplicationContext.get("user");
var roles = user._roles;              // roles asignados
user.hasRole("VisitSupervisor");      // chequeo de rol

// Estado del proceso actual
Framework.getProcessContext().__spec.name;      // nombre del proceso
Framework.getProcessContext().__attachedUI;     // UI vinculada actual
```

`ApplicationContext` es el caché de la app en ejecución. `Framework.getProcessContext()`
devuelve el proceso en curso, la UI vinculada, los objetos instanciados y los datos
cargados con su estado.

## Mensajería

```
// diálogo informativo/alerta al usuario (reemplaza a Framework.displayMessage, obsoleto)
MessageBox.displayMessage({ ... });

// error de validación (dentro de un método invocado por un action VALIDATION)
messageCollector.add({
    "level": "error",
    "objectClass": "BoVisit",
    "messageID": "MotivoNoPedidoRequerido"   // id de un ValidationMessages contract
});
```

## Lifecycle hooks (stubs que el framework invoca)

El framework llama automáticamente estos ganchos en el Business Object. Son stubs:
reprogramalos según necesites. El orden sigue el ciclo crear/inicializar/cargar/validar/guardar.

| Hook | Cuándo se dispara |
| --- | --- |
| `beforeCreateAsync` / `afterCreateAsync` | Antes/después de instanciar el objeto (`CreateAsync`). |
| `beforeInitialize` / `afterInitialize` | Antes/después de inicializar los atributos. |
| `beforeLoadAsync` / `afterLoadAsync` | Antes de cargar Simple Properties / después de cargar el objeto y sus anidados (recursivo). |
| `beforeDoValidateAsync` / `afterDoValidateAsync` | Antes/después de la validación de consistencia (`ValidateAsync`). |
| `beforeSaveAsync` / `afterSaveAsync` | Antes/después de persistir en SQLite. Son HOOKS de lógica (transiciones de estado, audit trail, mensajes post-guardado), no el guardado en sí. |

Notas clave:

- `LoadAsync` y `CreateAsync` se autogeneran si `generateLoadMethod` / `generateCreateMethod` están en `true` en el contrato del Business Object.
- El objeto del proceso se persiste con el action `SAVE` (el framework dispara `beforeSaveAsync` → guarda → `afterSaveAsync`); en proyectos reales no hay un `SaveAsync.bl.js`. Usa `Facade.saveObjectAsync(obj)` + `commitTransaction()` solo para persistir objetos o registros relacionados de forma imperativa desde tu lógica.
- Firma de los hooks: recibes `context` (y en algunos, `result`); el objeto en sí es `this` (`var me = this;`). Ej.: `function beforeSaveAsync(context) { var me = this; ... }`.

## Change events (reacción a cambios de datos)

Distinto de los eventos de UI: esto se dispara cuando cambia el VALOR de una propiedad o de
un ítem de lista, y sirve para lógica reactiva (recalcular dependientes, re-evaluar
derechos). Dos mecanismos:

- **Property change (Business Object o List Item)** — declarativo, en el `.businessobject.xml` / `.listitem.xml`, dentro de la `<SimpleProperty>`:

  ```
  <SimpleProperty name="Quantity" ...>
    <Events>
      <Event name="onChanged" eventHandler="onQuantityChanged" />
    </Events>
  </SimpleProperty>
  ```

  El `eventHandler` es un método bl.js sin parámetros obligatorios; `this` es la instancia
  que cambió. Lee con el getter, calcula, escribe el dependiente con el setter, y la UI se
  actualiza sola por los bindings.

- **Item change (List Object)** — programático, se registra en `Initialize` / `afterLoadAsync`:

  ```
  ListModel.addItemChangedEventListener(listObjectName, itemChangeEventName, host);
  ```

  El handler recibe un objeto con `oldValue` y `newValue` del ítem.

APIs de List Model para casos de lista:

| Método | Qué hace |
| --- | --- |
| `addItemChangedEventListener(hostReference, eventName)` | Dispara el handler cada vez que cambia un ítem de la lista. |
| `addItemChangedBatchEventListener(hostReference, eventName)` | Handler para cambios en lote (útil al reanudar tras suspender el refresh). |
| `suspendListRefresh()` | Detiene los eventos de cambio durante updates masivos (performance). |
| `resumeListRefresh(discardQueuedEvents, returnEventsAsBatch)` | Reanuda; con `returnEventsAsBatch=true` entrega los cambios acumulados como array. |
| `BindingUtils.refreshEARights()` | Re-evalúa derechos de edición/visibilidad (EA rights) en la UI tras un cambio de valor. |

Tras recalcular, persistí con `Facade.saveObjectAsync(object)`. Snippet completo en
`snippets.md` §11.

## Patrón async (promesas)

Los métodos `*Async` devuelven una promesa; encadenalas y devuelve la promesa final para
que el motor espere. Al resolverse, el motor consulta el `TransitionTo` de la acción en
el Process Contract para decidir el siguiente paso.

```
function beforeSaveAsync(result, context) {
    var me = this;
    me.setModifiedDate(Utils.createAnsiDateTimeNow());
    var promise = Facade.saveObjectAsync(me);   // llena el buffer
    return promise;                              // devolver la promesa SIEMPRE
}
```

Nunca dejes cadenas de promesas rotas (una promesa sin `return`/encadenar): `sf mdl build`
las detecta y la lógica queda a medio ejecutar en runtime.
