# UI y el patrón Master-Detail

En el `04-contracts-action-types.md` viste que la UI se describe en UserInterface Contracts y que un Process Contract la invoca con acciones VIEW. Ahora abrimos esos contratos de interfaz: cómo se estructuran en capas, qué controles tienes, cómo se cockpitean las pantallas de inicio, y —el plato fuerte— cómo se arma el patrón Master-Detail, que es el que vas a usar una y otra vez (una lista a la izquierda, el detalle del ítem seleccionado a la derecha).

## Resumen operativo

- La UI se anida: UIDescription -> Page -> Section -> Area -> Controls.
- Layout POR PATRONES (no libre): `<Page pagePattern="SingleSectionPage">`, `<Section sectionPattern="FilteredViewAreaSection">`, `<Area areaPattern="SingleElementArea|FilterElementArea">`. Los controles listan datos con `dataSource="ProcessContext::obj.loX.items[]"` y los ítems soportan layout responsive (`<Tablet>`/`<Phone>` con Col/Row). Archivo `<Nombre>UI.userinterface.xml`.
- Bindings conectan la vista al modelo: `TWO_WAY` para editables, lectura (`ONE_WAY`) para display. La editabilidad/visibilidad se puede reflejar declarativamente con bindings `type="Editable"` / `type="Visible"` ligados a campos que la lógica setea. No codees obligatoriedad/editabilidad con lógica de UI.
- Master-Detail: la seleccion dispara `ItemSelectedEvent(pKey)` y el `MASTER_DETAIL_HANDLER` coordina el detalle. Otros eventos: `ContextOpeningEvent`/`ContextSelectedEvent` (menús contextuales).
- Regla: si un campo debe volverse read-only por regla de negocio, hazlo por ACL (ver `06-logica-validaciones-acl.md`) o por binding Editable, no con lógica de UI.

## 1. La UI en capas

Un UserInterface Contract tiene una raíz <UIDescription> y se organiza en capas anidadas. De afuera hacia adentro: la Page define el layout general (con un pagePattern), se divide en Sections (con un sectionPattern), cada Section contiene Areas (con un areaPattern), y dentro de las Areas viven los Controls, que son los componentes atómicos.

> Diagrama (descrito, no embebido): La UI se anida en capas: UIDescription → Page → Section → Area → Controls.

Una regla a tener presente: una Section nunca debe partirse entre varias pantallas en tiempo de ejecución. Es la unidad lógica que el framework mantiene entera.

## 2. Page patterns

El pagePattern del nodo Page define cómo se disponen las secciones. Estos son los del set:

| pagePattern | Cuándo usarlo |
| --- | --- |
| SingleSectionPage | Una única sección que ocupa toda la pantalla. Ideal para dashboards y cockpits. |
| SingleSectionDialogPage | Igual que el anterior, pero renderizado como pop-up dialog. |
| MasterDetailSectionPage | Cuando la selección en una sección (masterSection) determina qué se renderiza en la otra (detailSection). Es el patrón maestro-detalle. |
| MultiSectionPage | Dos secciones (masterSection + planningSection / multiSection) sin dependencia entre sí; permite ocultar dinámicamente un multi-area. |
| SplitScreenPage | Optimizado para teléfonos: divide en leftSection y rightSection independientes, con un switch (SplitScreenButtons) que gestiona el framework. |

## 3. Sections, areas y controles

Dentro de la Page, cada Section usa un sectionPattern (por ejemplo SingleAreaSection o DashboardSection), y cada Area usa un areaPattern (SingleElementArea, GroupedElementsArea, TabElementArea o MultiArea). Las areas contienen los controles.

El catálogo de controles cubre desde una etiqueta hasta listas complejas. Los que más vas a usar:

| Categoría | Controles |
| --- | --- |
| Listas y tablas | GroupedList (agrupable y ordenable), EmbeddedList, CockpitList. |
| Inputs | InputArea (una línea), InputAreaMultiLine, SelectionBox, Dropdown, Checkbox, Stepper. |
| Fecha y hora | DatePicker, TimePicker, CalendarControl. |
| Acciones e info | ImageButton, MenuItem, Welcome. |

## 4. Bindings en la UI

Los controles se conectan a los datos con el nodo <Bindings>, que tiene dos tipos de elementos:

- Resource: para recursos estáticos o localizados (imágenes, labels), con valores por defecto (defaultLabel, defaultImage).

- Binding: para datos dinámicos. El atributo binding apunta a la ruta del dato (p. ej. ProcessContext::BoName.PropertyName) y el atributo target define qué propiedad del control se afecta: Value, Visible, Editable, etc.

El bindingMode controla la dirección de actualización (lo vimos en el `04-contracts-action-types.md`): ONE_WAY (del modelo a la UI), TWO_WAY (bidireccional, para inputs editables) y ONE_TIME (se inyecta una sola vez en la carga). En una lista, los bindings de cada ítem suelen ser ONE_WAY; en un formulario de detalle editable, TWO_WAY.

## 5. Cockpits

Un cockpit es la pantalla que agrupa información en tarjetas (cards) en un formato condensado. Hay cockpits de usuario (el "Your Day") y cockpits de tienda (el "Store Cockpit"). Es lo primero que ve el representante.

Se arma con un SingleSectionPage que contiene componentes CardContainer, uno por tarjeta. Cada CardContainer puede incluir una ActionBar, una LinkBar y un UIPlugIn, y tiene dos mecanismos importantes:

- IsReadyToLoad: un flag dinámico que le avisa al framework que ya están cargados todos los datos necesarios para renderizar la tarjeta.

- VisibilityRoles: el nodo <VisibilityRoles> permite mostrar u ocultar la tarjeta según el rol del usuario (un Merchandiser y un Supervisor pueden ver cockpits distintos).

## 6. El patrón Master-Detail

El MasterDetailSectionPage renderiza una lista maestra y el detalle del ítem seleccionado, correlacionados. La página declara dos secciones con nombres reservados: masterSection (la lista) y detailSection (el detalle). Cuando el usuario toca un ítem de la lista, se dispara un evento que le avisa a la sección de detalle que cargue los datos de ese registro.

> Diagrama (descrito, no embebido): Flujo Master-Detail: la selección dispara ItemSelectedEvent(pKey) y el MASTER_DETAIL_HANDLER coordina el detalle.

Dos cosas hacen que esto funcione: en el control de la lista maestra (por ejemplo un GroupedList) tienes que poner master="true", y registrar un ItemSelectedEvent que pase el pKey del ítem seleccionado como parámetro a la acción del handler en el Process Contract.

## 7. El MASTER_DETAIL_HANDLER

La orquestación vive en el Process Contract, en una acción de tipo MASTER_DETAIL_HANDLER. Esa acción define el comportamiento del maestro y del detalle:

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

- <MasterList>: apunta al List Object de la lista. Su <ItemUnselected type="..."> define qué pasa al deseleccionar un ítem: RELOAD (recargar), UPDATE (actualizar) o NONE (nada).

- <DetailObject>: apunta al Business Object del registro. Su <Save> configura cuándo persistir: type DIRTY (guarda solo si el objeto cambió), ALWAYS o NEVER; confirmation="TRUE" muestra un popup al cambiar de fila o cerrar; validate="TRUE" dispara la validación asíncrona del BO (doValidateAsync).

## 8. La UI Master-Detail, comentada

Este es un UI Contract real (condensado) de una pantalla maestro-detalle: a la izquierda una lista de displays, a la derecha el formulario del display seleccionado. Nota el master="true" en la lista, el ItemSelectedEvent que pasa el pKey, y el binding TWO_WAY del campo editable del detalle.

```
<UIDescription name="MyDisplay::DisplayDetailsUI" schemaVersion="0.0.0.5">
  <Page pagePattern="MasterDetailSectionPage"
        masterSectionFlex="40" detailSectionFlex="60">
 
    <!-- ===== Master: la lista ===== -->
    <Section sectionName="masterSection" sectionPattern="SingleAreaSection">
      <Area areaName="mainArea" areaPattern="SingleElementArea">
        <GroupedList name="displayList" master="true"
                     dataSource="ProcessContext::DisplayList.items []"
                     searchable="true">
          <Items name="Items" itemPattern="displayListItems">
            <Bindings>
              <Binding target="Row_Name" type="Text"
                       binding=".name" bindingMode="ONE_WAY" />
            </Bindings>
          </Items>
          <Events>
            <ItemSelectedEvent event="itemSelected">
              <Params><Param name="pKey" value=".pKey" /></Params>
            </ItemSelectedEvent>
          </Events>
        </GroupedList>
      </Area>
    </Section>
 
    <!-- ===== Detail: el formulario ===== -->
    <Section sectionName="detailSection" sectionPattern="SingleAreaSection">
      <Area areaName="detailArea" areaPattern="GroupedElementsArea">
        <GroupElement name="Info">
          <InputArea name="Name">
            <Bindings>
              <Resource target="Label" type="Label" id="DisplayName"
                        defaultLabel="Name" />
              <Binding target="Value"
                       binding="ProcessContext::CurrentDisplay.name"
                       bindingMode="TWO_WAY" />
            </Bindings>
          </InputArea>
        </GroupElement>
      </Area>
    </Section>
  </Page>
</UIDescription>
```

## 9. Errores comunes

| Error | Causa y solución |
| --- | --- |
| Falla de validación en el build por la lista | Declaraste a la vez agrupamiento/orden estático (groupBy, sortBy) y dinámico (DynamicallyGroupBy, DynamicallySortBy) en el mismo GroupedList. Usa uno solo. |
| Aparece una imagen de reemplazo en lugar de la tuya | Extensión no soportada: solo JPG y PNG. Si el binding apunta a un tipo ausente o no soportado, el framework inyecta una imagen por defecto. |
| El detalle no reacciona al seleccionar | Olvidaste master="true" en el control de la lista maestra; sin eso el framework no notifica al handler del detalle. |
| Render roto / sección partida | Una Section nunca debe partirse entre pantallas; revisa el patrón. Y un UIPluginV2 solo es válido dentro de GroupedElementsArea, SingleElementArea o CardContainer. |

## 10. Caso práctico de punta a punta

Vamos a armar la pantalla maestro-detalle de displays completa, uniendo la UI (sección 8), el handler (sección 7) y lo que sabes de procesos (`04-contracts-action-types.md`). Son tres piezas que encajan:

- El UI Contract (MyDisplay::DisplayDetailsUI): un MasterDetailSectionPage con la lista en masterSection (GroupedList master="true" + ItemSelectedEvent que pasa el pKey) y el formulario en detailSection (InputArea con binding TWO_WAY a CurrentDisplay.name).

- El Process Contract: en las EntryActions haces un LOAD de la lista de displays a ProcessContext::DisplayList; en el Body, una acción VIEW que muestra la UI y la acción MASTER_DETAIL_HANDLER que coordina DisplayList con CurrentDisplay.

- El cableado del evento: el ItemSelectedEvent de la lista entrega el pKey a la acción del handler; el handler hace el LOAD del display seleccionado en CurrentDisplay y, gracias a Save type="DIRTY", guarda automáticamente si el usuario editó el nombre antes de cambiar de fila.

Leído de corrido: la pantalla abre con la lista cargada → el rep toca un display → ItemSelectedEvent pasa su pKey → el MASTER_DETAIL_HANDLER carga ese display en el detalle → el rep edita el nombre (binding TWO_WAY) → al cambiar de fila, como el objeto quedó dirty y validate="TRUE", se valida y se guarda solo. Con este esqueleto cubres la enorme mayoría de las pantallas de la app.

## 11. Puntos clave

- La UI se anida: UIDescription → Page (pagePattern) → Section (sectionPattern) → Area (areaPattern) → Controls. Una Section nunca se parte entre pantallas.

- Elige el page pattern según el caso: SingleSectionPage para cockpits, MasterDetailSectionPage para lista+detalle, SplitScreenPage para teléfonos.

- Los controles se enlazan con Bindings: Resource (estático/localizado) y Binding (dinámico, con target = Value/Visible/Editable y bindingMode).

- Los cockpits se arman con CardContainers dentro de un SingleSectionPage; IsReadyToLoad controla el render y VisibilityRoles la visibilidad por rol.

- Master-Detail: master="true" en la lista + ItemSelectedEvent(pKey) + acción MASTER_DETAIL_HANDLER en el proceso.

- El handler define MasterList (ItemUnselected: RELOAD/UPDATE/NONE) y DetailObject (Save type DIRTY/ALWAYS/NEVER, confirmation, validate).

## Checklist de verificacion

- Los campos editables usan binding `TWO_WAY`.
- Dejaste que el ACL/validacion manejen editabilidad y obligatoriedad, sin logica de UI para eso.
- El Master-Detail coordina bien (ItemSelectedEvent -> handler -> detalle).
- El `Save` del detalle lleva `validate="TRUE"` si hay validaciones.
