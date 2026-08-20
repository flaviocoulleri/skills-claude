# Snippets — patrones canónicos copy-paste

Patrones validados, listos para adaptar. Todos siguen las convenciones de CG Cloud
Offline. Al construir, toma el patrón de acá y ajusta nombres; para la API de runtime de
bl.js mira `bl-js-api.md`, para el detalle conceptual mira la referencia temática que se
cita en cada bloque.

## 1. Datos que bajan al dispositivo

Tracked Object (config en Sync Management; ver `02-modelo-datos.md`):

```
Object:             Display__c
Where:              Sales_Org__c = $User.cgcloud__Sales_Org__c
                    AND Id IN ::RelevantDisplays::
Field Sets:         MobilityRelevant
First Sync of Day:  ✓
```

Named Queries en cascada (cada una devuelve IDs que alimentan a la siguiente):

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
```

Traer un árbol on-demand con un Named Fetch Tree (desde bl.js):

```
BoSfReplicationCallback.requestOnDemandDataAsync(...)
//   internamente: Facade.requestSfDataOnDemandAsync(<nombre del NFT>, <array de ids>)
```

Gotcha: para que un campo viaje tiene que estar en el field set `MobilityRelevant` y en
el Tracked Object; para que vuelva al servidor, márcalo UploadRelevant. En Named Queries,
no te olvides del `__c` en los custom.

## 2. Process Contract (ver `04-contracts-action-types.md`)

Esqueleto (archivo `<Nombre>Process.processflow.xml`) con EntryActions (preload), Body y ExitHandlers:

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

Invocar lógica (action LOGIC → llama un método bl.js con parámetros y retorno):

```
<Action actionType="LOGIC" name="LoadNotStartedTasks"
        call="ProcessContext::VisitBo.loadTasksBasedOnStatus">
  <Parameters>
    <Input name="Status" type="Literal" value="NotStarted" />
  </Parameters>
  <Return name="ProcessContext::NotStartedTasks" />
</Action>
```

Ramificar con `DECISION` (evalúa una variable del ProcessContext) y cerrar con `END`:

```
<Action name="Validate_Decision" actionType="DECISION" parameter="ProcessContext::picsExceeded">
  <Case value="false" action="GetCameraSettings" />
  <Case value="true"  action="Cancel" />
  <CaseElse action="Cancel" />
  <CaseEmpty action="Cancel" />
</Action>
<Action name="Finish" actionType="END">
  <ReturnValues>
    <Return name="success"  value="1" type="Literal" />
    <Return name="parentId" value="ProcessContext::parentId" />
  </ReturnValues>
</Action>
```

Los 14 `actionType`: LOAD, SAVE, CREATE, VIEW, LOGIC, PROCESS, DECISION, NAVIGATION,
CONFIRM, VALIDATION, MASTER_DETAIL_HANDLER, END, SCAN, PRINTV2 (tabla completa en
`04-contracts-action-types.md`).

## 3. UI y Master-Detail (ver `05-ui-master-detail.md`)

Binding editable (los `bindingMode` válidos son ONE_TIME, ONE_WAY, TWO_WAY):

```
<InputArea name="Name">
  <Bindings>
    <Resource target="Label" type="Label" id="DisplayName" defaultLabel="Name" />
    <Binding target="Value"
             binding="ProcessContext::CurrentDisplay.name"
             bindingMode="TWO_WAY" />
  </Bindings>
</InputArea>
```

Handler Master-Detail en el proceso:

```
<Action actionType="MASTER_DETAIL_HANDLER" name="handleDisplayMD">
  <MasterList name="ProcessContext::DisplayList">
    <ItemUnselected type="RELOAD" />
  </MasterList>
  <DetailObject name="ProcessContext::CurrentDisplay">
    <Save type="DIRTY" confirmation="TRUE" validate="TRUE" />
  </DetailObject>
</Action>
```

La lista master emite la selección (que el handler usa para cargar el detalle):

```
<Events>
  <ItemSelectedEvent event="itemSelected">
    <Params><Param name="pKey" value=".pKey" /></Params>
  </ItemSelectedEvent>
</Events>
```

Gotcha: no codifiques obligatoriedad ni read-only en la UI; eso lo gobiernan la validación
y el ACL, y la vista reacciona sola por el binding.

## 4. bl.js: hooks, persistencia y datos (ver `bl-js-api.md`)

Esqueleto de un lifecycle hook (devuelve SIEMPRE la promesa):

```
/**
 * @function afterCreateAsync
 * @this BoFastOrderValidation
 * @async @param {Object} result @param {Object} context @returns promise
 */
function afterCreateAsync(result, context) {
    var me = this;
    var promise = when.resolve(result);
    // ... tu lógica ...
    return promise;
}
```

Guardado del objeto del proceso: lo hace el action `SAVE` (el framework dispara los hooks
`beforeSaveAsync`/`afterSaveAsync`). En `beforeSaveAsync` va lógica PRE-guardado (estado,
audit), y devuelves la promesa; no llamas `saveObjectAsync(me)` para el objeto principal:

```
/** @function beforeSaveAsync @this BoOrder @module CUSTOM @async @param {Object} context @returns promise */
function beforeSaveAsync(context) {
    var me = this;
    me.setModifiedDate(Utils.createAnsiDateTimeNow());
    // ... transiciones de estado, audit trail, etc. ...
    return when.resolve();               // devuelve siempre la promesa
}
```

Persistencia IMPERATIVA de objetos/registros relacionados desde lógica (no el objeto del
proceso): llena el buffer y comiteá:

```
return Facade.saveObjectAsync(otroObjeto)     // o saveListAsync(lo)
    .then(function () { return Facade.commitTransaction(); });
```

Cargar datos (forma idiomática: BoFactory por criterios):

```
var promise = BoFactory.loadObjectByParamsAsync(BO_RETAILSTORE, {
    "params": [ { "field": "pKey", "value": me.getStoreId(), "operator": "EQ" } ]
});
// lista nueva: BoFactory.createListAsync(LO_ORDERITEMS, {});
```

## 5. Validación completa (4 piezas; ver `06-logica-validaciones-acl.md`)

```
<!-- 1) ValidationMessages (mensaje traducible) -->
<ValidationMessages name="BoVisitNoteMessages"
                    businessObject="BoVisitNote" schemaVersion="0.0.0.5">
  <ValidationMessage name="NoteTextEmpty"
                     defaultMessage="La nota no puede quedar vacía." />
</ValidationMessages>

<!-- 2) Bloque <Validations> en el Business Object -->
<Validations>
  <Validation name="validateNoteNotEmpty" />
</Validations>
```

```
// 3) Método en el bl.js del Business Object
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
<!-- 4) En el Body del proceso, ANTES del SAVE -->
<Action name="validateNote" actionType="VALIDATION">
  <Validations>
    <Validation name="ProcessContext::Note.validateNoteNotEmpty" />
  </Validations>
</Action>
```

El `Save` del detalle lleva `validate="TRUE"`. El framework muestra el popup solo.

## 6. ACL por rol/estado (ver `06-logica-validaciones-acl.md`)

Se evalúa al cargar (típicamente en `afterLoadAsync`) y la UI reacciona sola:

```
function afterLoadAsync(result, context) {
    var me = this;
    if (user.hasRole("Supervisor") === false) {
        me.getACL().removeRight(AclObjectType.PROPERTY,
                                "isFlagged", AclPermission.EDIT);
    }
    return when.resolve(result);
}
```

`AclObjectType.PROPERTY`; `AclPermission.EDIT` / `AclPermission.VISIBLE`. Usa
`removeRight`/`addRight`, NUNCA `setAce` (obsoleto, pisa todo el objeto de permisos).

## 7. UIPluginV2 (ver `09-uipluginv2-mobile-links.md`)

El plugin ES el contract `.uipluginv2.xml`: HTML, CSS y JS van inline en bloques CDATA.
Las props declaradas en `<Interface>` se leen desde el JS como `PluginManager.<id>`:

```
<UIPluginV2 name="CardSurveyExceptionsUiPluginV2">
  <Interface>
    <Property id="surveys" />
    <Property id="maximizedMode" />
  </Interface>
  <Labels><Label id="Card_NoExceptions" /></Labels>
  <Libraries><Library name="C3JS" /><Library name="D3JS" /></Libraries>
  <UIComponentHTML name="UIComponentHTML"><![CDATA[
    <div id="chart_CallSummary"></div>
  ]]></UIComponentHTML>
  <UIComponentCSS name="UIComponentCSS"><![CDATA[ /* estilos */ ]]></UIComponentCSS>
  <UIComponentJS name="UIComponentJS"><![CDATA[
    function connectCallback()    { renderChart(); }
    function renderCallback()     { inputChanged(); }        // se re-invoca al cambiar un input
    function disconnectCallback() {                          // limpieza de recursos
      if (PluginManager.helpers.isDefined(chartReference)) { chartReference.destroy(); }
    }
    function renderChart() {
      var data   = PluginManager.surveys;                    // prop del <Interface>
      var color  = PluginManager.pluginConfiguration.Color8; // tema/config
      var label  = PluginManager.locale.labels.Card_NoExceptions;
      // ... c3/d3 disponibles por <Libraries> ...
    }
  ]]></UIComponentJS>
</UIPluginV2>
```

Superficie de `PluginManager` (real): `PluginManager.<propDelInterface>` (datos de entrada),
`PluginManager.helpers.isDefined(x)`, `PluginManager.pluginConfiguration.<ColorN|isPortrait>`
(tema y layout), `PluginManager.locale.labels.<id>` (textos), y `PluginManager.throwEvent(nombre, payload)`
para emitir un evento al proceso (mapeado con `<CustomPluginEvent name="..." event="handler" />`
en el control que hospeda el plugin). El plugin corre aislado: nada de tocar el framework por fuera de `PluginManager`.

## 8. Mobile Links (ver `09-uipluginv2-mobile-links.md`)

Inbound (otra app abre la nuestra) — declaras el ExternalEvent que dispara una acción:

```
cgcloud://share?payload=<encodedPayload>   // btoa(JSON.stringify(payload))

<ExternalEvent name="linkLaunchEvent" action="ReceiveKpis" />
```

Outbound (abrir un tercero, ej. navegación) desde bl.js:

```
var lat = me.getStore().getLatitude();
var lng = me.getStore().getLongitude();
Facade.startThirdPartyAsync(
    "http://maps.google.com/maps?mode=d&daddr=" + lat + "," + lng, {});
```

## 9. PDF con PrintLayoutV2 (ver `10-theming-pdf-localization.md`)

Disparar la generación (action PRINTV2):

```
<Action name="PrintPDF" actionType="PRINTV2" printId="MyDisplayPDF"
        locale="ApplicationContext::user.languageSpoken" showShareButton="true">
  <Parameters>
    <Input name="currentDisplay" value="ProcessContext::CurrentDisplay" />
  </Parameters>
</Action>
```

El layout (Declarations = datos, ReportLayout = XHTML; textos con `{{Labels::Id; defaultLabel=...}}`):

```
<PrintLayout name="MyDisplayPDF" xmlns="https://www.salesforce.com/cgcloud/xsds">
  <Declarations>
    <DataDeclaration name="currentDisplay" type="BoMyDisplay" />
  </Declarations>
  <ReportLayout pageMargins="[30]" pageSize="[216, auto]">
    <h2 alignment="center">{{Labels::CurrentDisplayId; defaultLabel=Current Display}}</h2>
    <table tableLayout="noBorders">
      <tbody>
        <tr>
          <td>{{Labels::NameId; defaultLabel=Name:}}</td>
          <td>{{Declarations::currentDisplay.name}}</td>
        </tr>
      </tbody>
    </table>
  </ReportLayout>
</PrintLayout>
```

Imágenes al PDF: convertí con la CLI `sf mdl utils base64encode`. Texto traducible via
Label + Locale Contract (nunca hardcode).

## 10. Autenticación del simulador (ver `external-client-app.md`)

```
// $workspace/appl/config/config.json
{ "sfConsumerKey": "<tu Consumer Key>", ... }
// Callback del simulador: http://localhost:3000/fake/services/oauth/success
```

El Consumer Key sale de la External Client App. Agrega `http://localhost:3000` al CORS
allowed list de la org o el simulador no autentica.

## 11. Change events: recalcular al cambiar un valor (ver `bl-js-api.md`)

Property change de un Business Object / List Item — declarativo en el `.businessobject.xml`
/ `.listitem.xml`, y el handler en bl.js:

```
<!-- en la SimpleProperty que se observa -->
<SimpleProperty name="Quantity" type="DomInteger">
  <Events>
    <Event name="onChanged" eventHandler="onQuantityChanged" />
  </Events>
</SimpleProperty>
```

```
// bl.js del objeto: recalcular al cambiar la cantidad
/** @function onQuantityChanged @this BoOrderItem @module CUSTOM @async @returns promise */
function onQuantityChanged() {
    var me = this;
    var prices = me.getPricingCalculator().calculateItemValue(me, me.getBoOrderMeta());
    // reset del array de atributos modificados: evita que el evento se dispare 2 veces
    // para qty y deje valores erróneos (el list refresh no alcanza a limpiarlo solo)
    me.modified = [];
    var deferreds = [                       // los setters pueden ser async → junten y esperen
        me.setPrice(prices.price),
        me.setGrossValue(prices.grossValue),
        me.setValue(prices.value)           // el binding TWO_WAY refresca la UI solo
    ];
    return when.all(deferreds);
}
```

Item change de un List Object — programático, regístralo en `Initialize`/`afterLoadAsync`
del padre:

```
function afterLoadAsync(result, context) {
    var me = this;
    ListModel.addItemChangedEventListener("OrderItems", "orderItemChanged", me);
    return when.resolve(result);
}
// handler: recibe { oldValue, newValue }; recalcula el encabezado y guarda.
```

Perf en updates masivos: `ListModel.suspendListRefresh()` antes, y
`resumeListRefresh(false, true)` después para procesar los cambios como lote (con
`addItemChangedBatchEventListener`). Si el cambio afecta editabilidad/visibilidad, llama
`BindingUtils.refreshEARights()`.

Gotcha: no confundir con eventos de UI (`ItemSelectedEvent`, `CustomPluginEvent`); estos se
disparan por el cambio de DATO, no por la interacción con un control.

## 12. Captura de fotos punta a punta (ver `02-modelo-datos.md` y `bl-js-api.md`)

1) Modela la propiedad binaria como `DomBlob` (no se guarda el binario en la tabla: se
guarda el path, y el archivo va al file system del dispositivo):

```
<SimpleProperty name="photo" type="DomBlob"
                blobTable="ClbAttachmentBlob" blobPKeyField="attachmentBlobPKey" />
```

2) Captura. En proyectos reales la captura se orquesta desde un proceso (`.processflow.xml`)
con acciones `LOGIC` sobre un helper de imagen y una lista de adjuntos, no con
`getPictureAsync` suelto:

```
<!-- en el Body del proceso: obtener settings -> capturar -> validar URI -> crear adjunto -->
<Action name="GetCameraSettings" actionType="LOGIC" call="ProcessContext::imageHelper.getCameraSettings">
  <Return name="ProcessContext::CameraSettings" />
  <Parameters><Input name="settingsType" value="picture" type="Literal" /></Parameters>
  <TransitionTo action="CapturePicture" />
</Action>
<Action name="CapturePicture" actionType="LOGIC" call="ProcessContext::imageHelper.capturePicture">
  <Return name="ProcessContext::imageURI" />
  <Parameters><Input name="cameraSettings" value="ProcessContext::CameraSettings" /></Parameters>
  <TransitionTo action="CapturePicture_Decision" />
</Action>
<Action name="CapturePicture_Decision" actionType="DECISION" parameter="ProcessContext::imageURI">
  <CaseElse action="CreateAttachment" />
  <CaseEmpty action="Cancel" />
</Action>
<Action name="CreateAttachment" actionType="LOGIC" call="ProcessContext::attachmentList.addPicture">
  <Parameters>
    <Input name="mediaPath" value="ProcessContext::imageURI" />
    <Input name="parentId"  value="ProcessContext::parentId" />
  </Parameters>
</Action>
```

El helper envuelve la API nativa: `capturePicture` internamente hace
`Facade.getPictureAsync({ quality: 40, encodingType: "jpeg" }, "CAMERA")` (devuelve la URI/path).
`addPicture(mediaPath, parentId)` crea el ítem de adjunto en la lista (queda DIRTY para el sync).

3) Upload: el Sync Engine detecta el campo `DomBlob` del Tracked Object marcado DIRTY y
sube el archivo; en el server queda como `ContentVersion` vinculada al registro por
`ContentDocumentLink`. En el Datasource (ver §13), el blob mapea a `SF_File.VersionData` y el
vínculo a `SF_FileLink` (ContentDocumentLink).

4) Download (traer fotos existentes) con un Named Fetch Tree on-demand que navegue
`Registro -> ContentDocumentLink -> ContentDocument -> ContentVersion`:

```
// bl.js BoSfReplicationCallbacks.RequestOnDemandDataAsync
request.addRequest("NFT_DisplayPhotos", idsArray);
```

Límites: la galería (`IMAGE_LIBRARY`) rechaza imágenes > 10 MB. Del lado de la descarga, el
tope es el Max File Size / Download Limits de Mobile Settings (si se excede aparece el
error de binario 9806; ver `08-troubleshooting-sync.md`). Un límite en el `Where` de un NFT
sobreescribe ese valor genérico.

## 13. Datasource Contract (ver `04-contracts-action-types.md`)

Mapea un BO/LO a entidades del backend (SF). Archivo `Ds<Objeto>_sf.datasource.xml`.
Normalmente lo genera `sf mdl add datasource`; se edita para joins, condiciones o atributos derivados.

```
<DataSource name="DsLoRetailVisitKPIAttachment" backendSystem="sf"
            editableEntity="SF_File" businessObjectClass="LoRetailVisitKPIAttachment"
            readOnly="false" schemaVersion="2.0" linkedEntityAttributeName="parentId">
  <Attributes>
    <Attribute name="pKey" table="SF_FileLink" column="Id" />
    <Attribute name="parentId" table="SF_FileLink" column="ParentId" />
    <DateTimeAttribute dateName="creationDate" timeName="creationTime"
                       table="SF_File" column="CreatedDate" />
    <Attribute name="fileName" table="SF_File" column="PathOnClient" />
    <DerivedAttribute name="fileType" value="/* expresión SQL */" />
    <Attribute name="attachmentBlob" table="SF_File" column="VersionData" />
  </Attributes>
  <Entities>
    <Entity name="SF_File" idAttribute="Id" />
    <Entity name="SF_FileLink">
      <Join Type="inner">
        <SimpleJoin>
          <Condition leftSideValue="SF_File.Id" comparator="eq"
                     rightSideType="Attribute" rightSideValue="SF_FileLink.FileId" />
        </SimpleJoin>
      </Join>
    </Entity>
  </Entities>
  <QueryCondition><![CDATA[ SF_FileLink.ParentId = #parentId# AND SF_FileLink.IsDeleted = '0' ]]></QueryCondition>
  <OrderCriteria>
    <OrderCriterion entity="SF_File" attribute="CreatedDate" direction="DESC" />
  </OrderCriteria>
  <Parameters><Parameter name="parentId" type="TEXT" /></Parameters>
</DataSource>
```

Claves: cada `<Attribute name=` (propiedad del BO) apunta a `table`+`column` del backend;
`<DateTimeAttribute>` parte fecha/hora; `<DerivedAttribute>` es una expresión SQL; los `<Join>`
relacionan entidades; `<QueryCondition>` usa placeholders `#param#` (declarados en `<Parameters>`).
Para archivos/fotos: `SF_File` = ContentVersion (`VersionData` = binario, `PathOnClient` = nombre),
`SF_FileLink` = ContentDocumentLink (`ParentId`, `FileId`).
