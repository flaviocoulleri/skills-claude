# Lógica de negocio, validaciones y ACL

En el `05-ui-master-detail.md` armaste pantallas. Pero una pantalla sin lógica solo muestra datos: para que la app calcule, decida, valide y controle quién ve o edita qué, necesitas tres piezas que viven en la capa de modelo. La lógica de negocio (archivos bl.js, JavaScript), las validaciones (que frenan los datos inconsistentes antes de guardarlos) y el ACL (el control de acceso a nivel de propiedad, que muestra u oculta y habilita o bloquea campos según el rol).

## Resumen operativo

- bl.js = JavaScript en el hilo `Engine`. Documenta con ApexDoc (`/** @function ... @this ... @param ... */`).
- Validacion, tres piezas: mensaje en un contract `ValidationMessages` (traducible) + `<Validation>` en el BO + metodo bl.js que arma `{level, objectClass, messageID}` y hace `messageCollector.add(...)`. Se dispara con action type `VALIDATION`; el `Save` lleva `validate="TRUE"`. El framework muestra el popup solo.
- ACL: `getACL()` + `addRight`/`removeRight(AclObjectType.PROPERTY, "prop", AclPermission.EDIT|VISIBLE)` segun `user.hasRole(...)` y estado. NUNCA `setAce` (obsoleto, sobreescribe todo). La UI reacciona sola al ACL.
- Patron MVC ampliado: el proceso orquesta, bl.js calcula/valida/ajusta ACL, la UI reacciona por bindings.
- API de runtime (Facade, Utils, contextos, lifecycle hooks, persistencia): `bl-js-api.md`. Patrones copy-paste (validacion, ACL, hooks): `snippets.md`. Recorda: la persistencia va en `beforeSaveAsync` con `Facade.saveObjectAsync(me)` (SaveAsync no se autogenera).
- Change events (lógica reactiva ante cambio de VALOR de una propiedad/ítem, distinto de los eventos de UI): property `onChanged` declarativo o `addItemChangedEventListener` programático → recalcular dependientes. Detalle en `bl-js-api.md`; snippet en `snippets.md` §11.

## 1. La capa de lógica y reglas

La app sigue un patrón MVC ampliado. El Process Contract es el controlador: orquesta el flujo. El Business Object junto con su bl.js es el modelo: calcula, valida y ajusta los permisos. El UserInterface Contract es la vista: reacciona al modelo mediante bindings. Las tres piezas de este módulo —lógica, validación y ACL— viven en el modelo, y el proceso es quien las dispara.

> Diagrama (descrito, no embebido): MVC ampliado: el proceso orquesta, el modelo (bl.js) calcula/valida/ajusta ACL, y la UI reacciona.

## 2. bl.js: estructura y convenciones

La lógica de negocio se escribe exclusivamente como JavaScript, en archivos bl.js. A diferencia del resto, no es XML. Pero para integrarse con el framework, cada función depende de etiquetas JSDoc: @function, @this, @kind, @async, @namespace, @param y @returns.

### 2.1 La convención Async (obligatoria)

Toda función asíncrona lleva el sufijo Async (loadAsync, saveAsync, createAsync, afterCreateAsync). No es estético: le indica a cualquiera que lee el código que ese método devuelve una promise. Saltearse esta convención es una de las causas más comunes de bugs de retorno (lo vemos en la sección 7).

Un método típico, con su bloque JSDoc:

```
/**
 * @function afterCreateAsync
 * @this BoFastOrderValidation
 * @kind businessobject
 * @async
 * @namespace CUSTOM
 * @param {Object} result
 * @param {Object} context
 * @returns promise
 */
function afterCreateAsync(result, context) {
    var me = this;
    var promise = when.resolve(result);
    // ... tu lógica ...
    return promise;
}
```

## 3. Invocar lógica desde el proceso

El Process Contract llama a una función de bl.js con un action type LOGIC. El atributo call apunta al método sobre la instancia del objeto en el contexto, pasas argumentos con <Parameters> y recibes el resultado con <Return>:

```
<Action actionType="LOGIC" name="LoadNotStartedTasks"
        call="ProcessContext::VisitBo.loadTasksBasedOnStatus">
  <Parameters>
    <Input name="Status" type="Literal" value="NotStarted" />
  </Parameters>
  <Return name="ProcessContext::NotStartedTasks" />
</Action>
```

### 3.1 BusinessObjectHelper (BoHelper)

Cuando tienes funciones de utilidad que no están atadas a un registro de base de datos y no necesitan un data source, usás el contract BusinessObjectHelper (BoHelper). Se declara como una variable del ProcessContext y el framework lo instancia automáticamente. Soporta métodos asíncronos arbitrarios y un único método estándar createAsync, pero no admite SAVE, LOAD ni VALIDATE, porque no tiene contraparte en la base.

## 4. Validaciones

Una validación completa son cuatro piezas que se enganchan: el mensaje, la declaración de la regla, el método que la evalúa, y la acción que la dispara. El framework valida el Business Object modificado antes de guardarlo.

> Diagrama (descrito, no embebido): Flujo de validación: la acción dispara el método bl.js, que carga el messageCollector, y el framework muestra el popup.

### 4.1 El contract ValidationMessages

Define los mensajes de error que ve el usuario, traducibles y referenciables globalmente. Cada mensaje genera un messageID:

```
<ValidationMessages name="MyBoMyDisplayMessages"
                    businessObject="BoMyDisplay" schemaVersion="0.0.0.5">
  <ValidationMessage name="DisplayNameEmpty"
                     defaultMessage="Please enter a name." />
</ValidationMessages>
```

### 4.2 El bloque <Validations> en el Business Object

El contract del Business Object declara qué funciones de bl.js son reglas de validación:

```
<Validations>
  <Validation name="myValidateNameEmpty" />
</Validations>
```

### 4.3 El método en bl.js (messageCollector)

El framework le inyecta a la función un parámetro messageCollector. Si la regla falla, armas un objeto de error con level, objectClass y el messageID, y lo agregas al collector:

```
/**
 * @function myValidateNameEmpty
 * @this BoMyDisplay
 * @param {messageCollector} messageCollector
 */
function myValidateNameEmpty(messageCollector) {
    var me = this;
    if (Utils.isEmptyString(me.getName())) {
        var newError = {
            "level": "error",
            "objectClass": "BoMyDisplay",
            "messageID": "DisplayNameEmpty"
        };
        messageCollector.add(newError);
    }
}
```

El método estándar de validación de un objeto es doValidateAsync; también puedes definir validaciones a medida como la de arriba.

### 4.4 El action type VALIDATION

En el proceso, disparas la validación explícitamente. El framework intercepta el messageCollector y, si hay errores, muestra el popup en la UI:

```
<Action name="ValidateName" actionType="VALIDATION">
  <Validations>
    <Validation name="ProcessContext::CustomerDetail.myValidateNameEmpty" />
  </Validations>
</Action>
```

## 5. ACL: control de acceso por registro

El ACL (Access Control List) configura de forma dinámica la visibilidad y la editabilidad de las propiedades de un registro. Obtienes el objeto de permisos con getACL() y lo manipulas con addRight y removeRight, usando las constantes AclObjectType.PROPERTY y AclPermission.VISIBLE / AclPermission.EDIT.

Importante: setAce quedó obsoleto. addRight y removeRight se agregaron después justamente para evitar colisiones y la sobreescritura total del objeto de permisos; son la práctica recomendada porque dan control granular.

Un caso real: ocultar propiedades a quien no tenga cierto rol. Se evalúa el rol con user.hasRole(...) y se quitan permisos puntuales:

```
var bHasRole = user.hasRole("MobileDSDDriver");
if (bHasRole === false) {
    var aclBoOrderRole = me.getBoOrderRole().getACL();
    aclBoOrderRole.removeRight(AclObjectType.PROPERTY,
                               "ordererType", AclPermission.VISIBLE);
    aclBoOrderRole.removeRight(AclObjectType.PROPERTY,
                               "sdoMetaBlocked", AclPermission.VISIBLE);
}
```

## 6. Cómo encaja todo

Las tres piezas se coordinan dentro del patrón MVC ampliado, y el premio es que mucha de la reacción de la UI es automática:

- Controller (proceso): carga el contexto con EntryActions/LOAD, llama a la lógica con LOGIC, y antes de un SAVE o una transición clave dispara VALIDATION (o valida en los ExitHandlers).

- Model (BO + bl.js): calcula, valida (genera el messageCollector) y ajusta el ACL con getACL().removeRight(...) según el rol o el estado del registro.

- View (UI): reacciona vía bindings. Si el ACL revoca AclPermission.EDIT sobre una propiedad, el campo TWO_WAY asociado se renderiza read-only automáticamente, sin lógica extra de interfaz. Y si una validación falla, el popup lo genera el framework a partir del messageCollector.

Ese automatismo es la clave: no escribes código de UI para deshabilitar un campo ni para mostrar un cartel de error; ajustas el modelo (ACL, validación) y la vista responde sola.

Cuando tu bl.js no hace lo que esperas, lo depuras en el simulador con breakpoints en el hilo Engine y mirando el SQL en vivo del Debug Window — el cómo está en el módulo Debugging y testing en desarrollo.

## 7. Errores comunes

| Error | Causa y cómo evitarlo |
| --- | --- |
| Cadenas de promesas rotas (deadlock de la UI) | Crear un when.defer() nuevo dentro de una función async y no manejar el reject. Todas las excepciones deben propagarse; si no, el framework no se entera y la UI queda esperando para siempre. Cubre todos los caminos de la promise. |
| Llamada async en un método síncrono | Dispara un error de validación en compilación. Las llamadas asíncronas deben estar bien encapsuladas o no estar; respeta el sufijo Async y el @async. |
| Typo en variables de objeto | Usa las constantes del framework BO_<nombre> (p. ej. BO_CUSTOMER), no strings sueltos. Un string mal escrito no rompe la compilación: falla recién en runtime en el dispositivo. |
| La validación de Input automática no funciona | El Domain de la propiedad no tiene tipo ni longitud definidos. Sin eso se anula la Input Validation estándar de los controles. Declará tipo y longitud en el dominio. |

## 8. Caso práctico de punta a punta

Retomamos el proceso Visit::AddNoteProcess del `04-contracts-action-types.md` (crear una nota en una visita) y le sumamos las dos reglas que faltaban: que el texto no pueda quedar vacío (validación) y que un campo sensible solo lo edite un supervisor (ACL). Son las cuatro piezas de validación más un ajuste de ACL en el bl.js de la nota.

### 8.1 La validación de texto no vacío

Primero el mensaje (ValidationMessages), luego la declaración en el BO, el método en bl.js, y el disparo en el proceso:

```
<!-- 1) ValidationMessages -->
<ValidationMessages name="BoVisitNoteMessages"
                    businessObject="BoVisitNote" schemaVersion="0.0.0.5">
  <ValidationMessage name="NoteTextEmpty"
                     defaultMessage="La nota no puede quedar vacía." />
</ValidationMessages>
 
<!-- 2) Bloque <Validations> en BoVisitNote -->
<Validations>
  <Validation name="validateNoteNotEmpty" />
</Validations>
```

```
// 3) Método en el bl.js de BoVisitNote
/**
 * @function validateNoteNotEmpty
 * @this BoVisitNote
 * @param {messageCollector} messageCollector
 */
function validateNoteNotEmpty(messageCollector) {
    var me = this;
    if (Utils.isEmptyString(me.getText())) {
        messageCollector.add({
            "level": "error",
            "objectClass": "BoVisitNote",
            "messageID": "NoteTextEmpty"
        });
    }
}
```

```
<!-- 4) En el Body del proceso, antes del SAVE -->
<Action name="validateNote" actionType="VALIDATION">
  <Validations>
    <Validation name="ProcessContext::Note.validateNoteNotEmpty" />
  </Validations>
</Action>
```

### 8.2 El campo editable solo para supervisores

En el bl.js de la nota, al cargarla, ajustamos el ACL según el rol. Si el usuario no es supervisor, le quitamos el permiso de edición sobre el campo sensible; el binding TWO_WAY de ese campo se volverá read-only solo:

```
/**
 * @function afterLoadAsync
 * @this BoVisitNote
 * @async
 * @param {Object} result @param {Object} context
 * @returns promise
 */
function afterLoadAsync(result, context) {
    var me = this;
    if (user.hasRole("Supervisor") === false) {
        me.getACL().removeRight(AclObjectType.PROPERTY,
                                "isFlagged", AclPermission.EDIT);
    }
    return when.resolve(result);
}
```

Leído de corrido: el rep abre la nota → afterLoadAsync evalúa el rol y, si no es supervisor, revoca EDIT sobre isFlagged → en la UI ese campo aparece deshabilitado automáticamente → el rep escribe el texto → al guardar, la acción VALIDATION corre validateNoteNotEmpty; si el texto está vacío, el framework muestra el popup "La nota no puede quedar vacía." y no guarda. Con esto cierras el circuito completo: lógica, validación y permisos, todo enganchado al proceso y a la UI que ya sabías construir.

## 9. Puntos clave

- La business logic se escribe en bl.js (JavaScript) y depende de etiquetas JSDoc; toda función async lleva el sufijo Async porque devuelve una promise.

- El proceso invoca la lógica con un action LOGIC (call + Parameters + Return). Para utilidades sin DB se usa el BoHelper (no soporta SAVE/LOAD/VALIDATE).

- Una validación son cuatro piezas: el contract ValidationMessages (el texto), el bloque <Validations> del BO (la regla), el método bl.js con messageCollector, y el action VALIDATION (el disparo).

- El ACL se maneja con getACL() y addRight/removeRight (setAce quedó obsoleto), usando AclObjectType.PROPERTY y AclPermission.VISIBLE/EDIT.

- Mucho es automático: revocar EDIT vía ACL deja un campo TWO_WAY read-only sin código de UI, y un messageCollector con errores dispara el popup solo.

- Cuidado con las promesas rotas (deadlock), las llamadas async en métodos síncronos, los strings en vez de constantes BO_<nombre>, y los dominios sin tipo/longitud.

## Checklist de verificacion

- La validacion tiene sus tres piezas alineadas (mensaje + `<Validation>` en el BO + metodo bl.js con `messageCollector.add`).
- Se dispara con un action `VALIDATION` antes del Save, y el Save tiene `validate="TRUE"`.
- El ACL usa `removeRight`/`addRight` (nunca `setAce`) y evalua rol + estado.
- No metiste en la UI logica que corresponde al modelo (validacion/ACL).
- Los metodos bl.js tienen ApexDoc y no rompen la cadena de promesas.
