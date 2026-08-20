# Contracts y action types

Ya tienes el entorno montado (`03-setup-modeler-git.md`). Ahora entramos al material con el que vas a construir de verdad: los contracts. En el Modeler, casi todo lo que hace la app —cómo se ve, qué datos toca, qué pasos sigue un proceso de negocio— está descrito en archivos XML llamados Design Contracts. Y el contract que orquesta el comportamiento, el Process Contract, ejecuta su lógica a través de acciones tipadas: los action types. Entender estas dos cosas es entender el 80% del trabajo de customización.

## Resumen operativo

- Familia de contracts: Process (orquesta), UserInterface (pantallas), Datasource (datos), List y textos. El Process es el controlador.
- Flujo de un Process: Entry -> defaultAction -> Body -> ExitHandlers -> return.
- Action types clave: LOAD (traer datos), LOGIC (ejecutar bl.js), VALIDATION (validar antes de guardar), mas navegacion/UI. EntryActions y ExitHandlers enmarcan el proceso.
- Scaffolding: `sf mdl add` abre el wizard (module/businessobject/listobject/lookupobject/datasource/businesslogic/userinterface/process).

## 1. El sistema de contracts

Un Design Contract es, en concreto, un archivo XML independiente del dispositivo que describe una parte de la app: una pantalla, un proceso, el acceso a una tabla, una lista, los textos traducidos. "Design Contract" es el término paraguas; en la práctica trabajas con una familia de contracts especializados, y el que los coordina es el Process Contract.

> Diagrama (descrito, no embebido): La familia de contracts: el Process Contract orquesta, y los demás describen UI, datos, listas y textos.

## 2. Los tipos de contracts

| Contract | Para qué sirve |
| --- | --- |
| Process Contract | Define la secuencia de acciones y el flujo de ejecución de un proceso de negocio (gestión de órdenes, promociones, visitas). Instancia objetos, procesa eventos, controla la UI y puede llamar subprocesos. |
| UserInterface Contract | Describe la interfaz: las capas de diseño según un UI pattern (áreas, secciones), los controles (calendarios, tablas, botones), los menús y los bindings con los Business Objects. |
| Datasource Contract | Es la capa de abstracción entre la base SQLite local y los Business Objects: mapea las simple properties a columnas (vía el atributo `dataSourceProperty` de cada `SimpleProperty`) y construye el SQL (SELECT, INSERT, UPDATE, DELETE). Los campos binarios se mapean con `type="DomBlob"` + `blobTable`/`blobPKeyField`. Archivo `Ds<Objeto>_sf.datasource.xml`: `<Attributes>` (table+column, `DateTimeAttribute`, `DerivedAttribute`), `<Entities>`+`<Join>`, `<QueryCondition>` con `#param#`, `<OrderCriteria>`, `<Parameters>`. Normalmente lo genera `sf mdl add datasource`; estructura completa en `snippets.md` §13. |
| List Object / List Item | Modela relaciones 1..n desde un Business Object. El List Object es el contenedor lógico de la lista; el List Item describe la estructura de cada elemento visible. |
| Locale Contract | Gestiona la localización: mapea IDs a labels traducidos y referencias a imágenes localizadas, según el idioma del usuario y la sales org. |
| Design Contract | Término general para el conjunto de estos archivos XML que definen la arquitectura de la app offline. |

### 2.1 Crear contracts con el wizard sf mdl add

No hace falta escribir cada contract desde cero. El comando sf modeler workspace add (alias sf mdl add) abre un wizard interactivo que scaffoldea el recurso a partir de las plantillas del workspace (contractSnippets), generando los XML y bl.js en la carpeta correcta de src/<Module> (BO/, DS/, PR/, etc.). Los recursos que puede crear:

```
sf mdl add
 
#  module          un módulo nuevo (la carpeta contenedora)
#  businessobject  un Business Object
#  listobject      un List Object (genera también su listitem y métodos base)
#  lookupobject    un Lookup Object
#  datasource      un Datasource Contract
#  businesslogic   un archivo de business logic (bl.js)
#  userinterface   un UserInterface Contract
#  process         un Process Contract
```

Arrancar un contract con el wizard te asegura la estructura base correcta (nombres, carpetas, namespaces) y te evita errores de tipeo en el andamiaje. El detalle de cada comando y sus flags está en la Referencia de la CLI del Modeler.

## 3. Anatomía de un Process Contract

Un Process Contract (archivo `<Nombre>Process.processflow.xml`) arranca con un elemento raíz <Process name="Namespace::NombreProceso" defaultAction="..." schemaVersion="0.0.0.5">. Dentro hay tres bloques: <Entry>, <Body> y <ExitHandlers>.

### 3.1 Entry

- ProcessContext: declaras las variables del proceso (<Declarations>) y los parámetros de entrada (<Parameters>) que recibe.

- EntryActions: acciones que corren automáticamente en la inicialización para precargar datos (típicamente LOAD de los objetos que el proceso va a necesitar).

### 3.2 Body y ExitHandlers

- Body: el flujo real, dentro de <Actions>. Acá viven los renderizados de UI, la lógica y las validaciones.

- ExitHandlers: validaciones o funciones que corren antes de devolver el control de un subproceso al proceso padre; si fallan, OnValidationError redirige el flujo.

### 3.3 El flujo de ejecución

Juntando las piezas: el proceso recibe las variables del ProcessContext, ejecuta en secuencia las EntryActions para precargar datos, y luego el framework corre la acción indicada en defaultAction, que transfiere el control al Body. Al salir de una vista o terminar, se evalúan los ExitHandlers; si una validación falla, OnValidationError te manda de vuelta a una acción del Body.

> Diagrama (descrito, no embebido): Flujo de un Process Contract: Entry → defaultAction → Body → ExitHandlers → return.

## 4. Los action types

Cada nodo <Action> del Body tiene un atributo actionType que define su comportamiento. Hay catorce, y conviene pensarlos en cinco familias: datos (LOAD, SAVE, CREATE), flujo (PROCESS, DECISION, NAVIGATION, END), interfaz (VIEW, CONFIRM, MASTER_DETAIL_HANDLER), lógica (LOGIC, VALIDATION) y dispositivo (SCAN, PRINTV2).

| Action type | Qué hace |
| --- | --- |
| LOAD | Carga datos desde la base local hacia una instancia de un Business Object o List Object. |
| SAVE | Guarda en la base una instancia o lista de objetos ya declarada en el proceso. |
| CREATE | Crea e inicializa una instancia de un Business Object y devuelve su referencia al contexto del proceso. |
| VIEW | Renderiza una UI; declara el manejo de eventos disparados desde la interfaz y gestiona las validaciones de los ExitHandlers asociados. |
| LOGIC | Invoca funciones de business logic en JavaScript (del framework/API o métodos del objeto). |
| PROCESS | Inicia un subproceso desde el actual; puede pasar parámetros y devolver valores al proceso invocador. |
| DECISION | Funciona como un switch/case: `parameter="ProcessContext::x"` y ramas `<Case value="..." action="..." />`, `<CaseElse action="..." />`, `<CaseEmpty action="..." />`. Desvía la transición según el valor. |
| NAVIGATION | Hace transiciones de alto nivel, típicamente cambiar el flujo hacia otras áreas o subprocesos vía menú contextual. |
| CONFIRM | Interrumpe el flujo con un diálogo para que el usuario decida (p. ej. Sí/No) si mantener o descartar cambios pendientes. |
| VALIDATION | Llama a métodos de business logic dedicados a validar la integridad de un Business Object; interrumpe el flujo si hay errores. |
| MASTER_DETAIL_HANDLER | Coordina la lista maestra (MasterList) y el detalle (DetailObject): recarga, guardado y borrado coordinados. |
| END | Termina incondicionalmente el proceso en ejecución y devuelve el control al llamador. |
| SCAN | Abre el escáner de códigos de barras (UPC/EAN) y devuelve el string escaneado a una variable del contexto. |
| PRINTV2 | Ejecuta el motor de impresión para generar o previsualizar PDFs, a partir del contract PrintLayoutV2 y variables de datos. |

## 5. Referencias y binding

Los contracts se referencian entre sí con la sintaxis de doble dos puntos (::). Por ejemplo, una acción VIEW llama a su UI con <UIDescription>Namespace::NombreUI</UIDescription>, y una llamada a lógica o a una variable de contexto se escribe como ProcessContext::MainBO.getButtonVisibility.

La UI se enlaza a los Business Objects con el nodo <Bindings>, usando los atributos target, binding y, sobre todo, bindingMode, que controla el ciclo de actualización entre el control y el objeto:

| bindingMode | Comportamiento |
| --- | --- |
| ONE_WAY | Actualiza el control de la UI solo cuando cambia el valor del Business Object (lectura del objeto hacia la UI). |
| TWO_WAY | Sincronización bidireccional: si el usuario edita la UI, se actualiza el objeto, y si cambia el objeto, se actualiza la UI. |
| ONE_TIME | Escribe el valor del objeto en la UI una sola vez, en la carga inicial; después no actualiza nada. |

Regla práctica: TWO_WAY para campos editables (inputs), ONE_WAY para campos de solo lectura que pueden cambiar, ONE_TIME para valores fijos que se muestran una vez.

## 6. Un Process Contract real, comentado

Este es un Process Contract real (condensado) que muestra el detalle de una visita: recibe la visita como parámetro, precarga la tienda y la cuenta en las EntryActions, y en el Body muestra dos vistas. El ExitHandler valida la visita antes de salir.

```
<Process name="Visit::DetailsProcess" defaultAction="showVisitDetails"
         schemaVersion="0.0.0.5">
  <Entry>
    <ProcessContext>
      <Declarations>
        <Declaration name="RetailStoreDetail" type="BoRetailStore" />
        <Declaration name="Account" type="BoAccount" />
      </Declarations>
      <Parameters>
        <Input name="BoVisit" type="BoVisit" />
      </Parameters>
    </ProcessContext>
    <EntryActions>
      <Action actionType="LOAD" name="LoadRetailStore" type="BoRetailStore">
        <Parameters>
          <Input name="pKey" value="ProcessContext::BoVisit.StoreId" />
        </Parameters>
        <Return name="ProcessContext::RetailStoreDetail" />
      </Action>
      <Action actionType="LOAD" name="LoadAccount" type="BoAccount">
        <Parameters>
          <Input name="pKey" value="ProcessContext::BoVisit.AccountId" />
        </Parameters>
        <Return name="ProcessContext::Account" />
      </Action>
    </EntryActions>
  </Entry>
  <Body>
    <Actions>
      <Action actionType="View" name="showVisitDetails">
        <UIDescription>Visit::DetailsUI</UIDescription>
      </Action>
      <Action actionType="View" name="showRetailOverview">
        <UIDescription>Visit::RetailStoreCockpitUI</UIDescription>
      </Action>
    </Actions>
  </Body>
  <ExitHandlers>
    <ExitHandler handlerName="beforeExit1" type="Validate"
                 name="ProcessContext::BoVisit">
      <OnValidationError transitionTo="showVisitDetails" />
    </ExitHandler>
  </ExitHandlers>
</Process>
```

## 7. Errores comunes

El build (sf modeler workspace build) valida los contracts contra esquemas XSD. La validación más estricta se activa con USE_LATEST_XSD_VALIDATIONS: true en branch.config.json. Estos son los tropiezos habituales:

| Error | Causa | Cómo resolverlo |
| --- | --- | --- |
| Enumeración XSD inválida | Pusiste un valor no soportado en actionType, pagePattern o bindingMode | Usar un valor del set permitido (ver el mensaje del error, que lista las opciones válidas) |
| Nombres duplicados | Dos Action o dos Case con el mismo name en la misma lista | Cada name debe ser único dentro de Body.Actions y dentro de Action.Cases |
| Problemas de promesas / retorno | Definir una función async de BL sin el sufijo Async | Respetar la convención: las funciones asíncronas terminan en Async |
| Alerta de integridad relacional | El UIDescription referencia una UI que no existe en el módulo | Verificar que el identificador Namespace::NombreUI exista |

El mensaje típico de una enumeración inválida es explícito y te lista las opciones válidas, por ejemplo:

```
Element 'Binding', attribute 'bindingMode': [facet 'enumeration']
  The value 'Invalid_BindingMode' is not an element of the set
  ('ONE_TIME', 'ONE_WAY', 'TWO_WAY').
```

## 8. Caso práctico de punta a punta

Vamos a diseñar un proceso simple desde cero: registrar una nota rápida durante una visita. El proceso recibe la visita, crea una nota ligada a ella, muestra un formulario, valida y guarda. Es el patrón CREATE → VIEW → VALIDATION → SAVE → END, el esqueleto de la mayoría de los procesos de captura.

```
<Process name="Visit::AddNoteProcess" defaultAction="showNoteForm"
         schemaVersion="0.0.0.5">
  <Entry>
    <ProcessContext>
      <Declarations>
        <Declaration name="Note" type="BoVisitNote" />
      </Declarations>
      <Parameters>
        <Input name="BoVisit" type="BoVisit" />
      </Parameters>
    </ProcessContext>
    <EntryActions>
      <Action actionType="CREATE" name="createNote" type="BoVisitNote">
        <Parameters>
          <Input name="VisitId" value="ProcessContext::BoVisit.Id" />
        </Parameters>
        <Return name="ProcessContext::Note" />
      </Action>
    </EntryActions>
  </Entry>
  <Body>
    <Actions>
      <Action actionType="View" name="showNoteForm">
        <UIDescription>Visit::AddNoteUI</UIDescription>
      </Action>
      <Action actionType="Validation" name="validateNote"
              type="ProcessContext::Note" />
      <Action actionType="Save" name="saveNote" type="ProcessContext::Note" />
      <Action actionType="End" name="finish" />
    </Actions>
  </Body>
  <ExitHandlers>
    <ExitHandler handlerName="beforeExit" type="Validate"
                 name="ProcessContext::Note">
      <OnValidationError transitionTo="showNoteForm" />
    </ExitHandler>
  </ExitHandlers>
</Process>
```

El formulario (la UI Visit::AddNoteUI) enlaza el campo de texto a la property de la nota en modo TWO_WAY, para que lo que escribe el usuario quede en el objeto:

```
<Bindings>
  <Binding target="noteTextField"
           binding="ProcessContext::Note.Text"
           bindingMode="TWO_WAY" />
</Bindings>
```

Leído de corrido: entra la visita → se crea la nota ligada a su Id (CREATE) → se muestra el formulario con el binding TWO_WAY (VIEW) → se valida la nota (VALIDATION) → se guarda (SAVE) → termina (END). Si al intentar salir la validación del ExitHandler falla, OnValidationError devuelve al usuario al formulario. Con este esqueleto y la tabla de action types, ya puedes construir procesos de captura completos.

## 9. Puntos clave

- Todo en la app son Design Contracts (XML): Process, UserInterface, Datasource, List Object/Item y Locale. El Process Contract es el que orquesta.

- Un Process Contract tiene Entry (ProcessContext + EntryActions), Body (Actions) y ExitHandlers; el flujo entra por defaultAction al Body y valida al salir.

- Hay 14 action types en cinco familias: datos (LOAD/SAVE/CREATE), flujo (PROCESS/DECISION/NAVIGATION/END), UI (VIEW/CONFIRM/MASTER_DETAIL_HANDLER), lógica (LOGIC/VALIDATION) y dispositivo (SCAN/PRINTV2).

- Los contracts se referencian con :: y la UI se enlaza a los objetos con bindings: TWO_WAY (editable), ONE_WAY (lectura que cambia), ONE_TIME (una sola vez).

- El patrón CREATE → VIEW → VALIDATION → SAVE → END es el esqueleto de los procesos de captura.

- Los errores de build suelen ser enumeraciones XSD inválidas, nombres duplicados, falta del sufijo Async o un UIDescription inexistente.

## Checklist de verificacion

- El Process tiene Entry, defaultAction y ExitHandlers coherentes.
- Cada action type es el correcto para su intencion (LOGIC vs VALIDATION vs LOAD).
- La validacion se dispara con un action VALIDATION antes del Save (`validate="TRUE"`).
- Usaste `sf mdl add` para generar el andamiaje en vez de escribirlo a mano.
