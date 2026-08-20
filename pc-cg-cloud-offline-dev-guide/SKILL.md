---
name: pc-cg-cloud-offline-dev-guide
description: "Guía de desarrollo para Salesforce Consumer Goods Cloud Offline, la app móvil de retail execution que se construye con el Modeler basado en VS Code. Usa esta skill siempre que el usuario quiera construir, configurar, depurar o entender la app offline de CG Cloud: modelar qué datos bajan (Tracked Objects, Named Queries, Named Fetch Trees), contracts y action types, pantallas (UI, Master-Detail, bindings), lógica en bl.js, validaciones con messageCollector, control de acceso por registro (ACL), sincronización y su troubleshooting, UIPluginV2, Mobile Links, theming/PDF/localización, la CLI (sf mdl), la app Sync Management, el simulador, debugging con DevTools y build/package/deploy. Dispárala aunque no diga 'CG Cloud': menciones como Modeler, bl.js, Tracked Object, action type, Named Fetch Tree, sync offline, casmobile.db, UIPluginV2 o sfConsumerKey alcanzan. NO es para la configuración del modelo de datos CG Cloud (pc-cg-cloud-guide) ni para Apex/LWC general (pc-crm-salesforce-dev-guide). ES (neutro) e inglés."
---

# Desarrollo en Consumer Goods Cloud Offline

Manual operativo para asistir a desarrolladores que construyen sobre la app móvil offline
de Consumer Goods Cloud, configurada con el Modeler (VS Code Based). El detalle profundo
vive en `references/`, que se leen bajo demanda. Registro por defecto: español neutro
(tuteo), salvo que el usuario escriba en inglés.

## Principio de trabajo

Antes de afirmar una API, una firma o un nombre, toma el dato del material: no lo
reconstruyas de memoria. Para la API de runtime de bl.js, `references/bl-js-api.md` es
AUTORITATIVA. Para patrones de código listos, `references/snippets.md` es la librería
copy-paste. Si una tarea cruza capas, lee varias referencias.

## Modelo mental

Una feature nace como un campo en el org y desciende por toda la pila, sumando
responsabilidad en cada capa:

```
Org (campo + field set MobilityRelevant)                       prerrequisito de admin
  -> Tracked Object     ¿qué baja? Where / Named Query / NFT               (02)
  -> Datasource + Business Object   columna local + propiedad              (04, 06)
  -> UI                 pantallas y bindings (Master-Detail, TWO_WAY)      (05)
  -> bl.js              lógica en el hilo Engine                           (06, bl-js-api)
  -> Validación         messageCollector + action VALIDATION               (06)
  -> ACL                visibilidad/edición por registro y rol             (06)
  -> Sync               qué sube (UploadRelevant), tipos, conflictos       (07)
  -> Build/Deploy       build -> package -> Deployment Packages            (03, ref-cli, ref-sync-management)
```

Patrón MVC ampliado: el Process Contract orquesta (controlador), el Business Object +
bl.js calcula/valida/ajusta ACL (modelo), la UI reacciona por bindings (vista). Mucho
comportamiento de UI es automático: si el ACL revoca la edición de una propiedad, su campo
TWO_WAY se vuelve read-only solo; si una validación falla, el framework muestra el popup.

## Flujo de desarrollo (con comandos)

1. **Setup del entorno** — `sf mdl create`; carga `sfConsumerKey` en `appl/config/config.json` y `http://localhost:3000` al CORS de la org. (03, external-client-app)
2. **Traer contracts** — `sf mdl importContracts`. (03, 04)
3. **Modelar qué baja** — Tracked Objects / Named Queries / NFT en Sync Configuration. (02)
4. **Crear artefactos** — `sf mdl add` (module / businessobject / listobject / lookupobject / datasource / businesslogic / userinterface / process). (04)
5. **UI** — pantallas, bindings y Master-Detail. (05, snippets §3)
6. **Lógica, validación, ACL** — bl.js. (06, bl-js-api, snippets §4-6)
7. **Sync** — configurar y verificar en la consola. (07, ref-sync-management)
8. **Build / test / deploy** — `sf mdl build` -> simular (`sf mdl simulate`; `?desktop` o `&forceOffline`) -> `sf mdl package` -> subir a Deployment Packages y asignar. (03, ref-cli, debugging)
9. **Debug en desarrollo** — DevTools (hilo Engine), Debug Window, SQLite local. (debugging)

## Reglas de oro (no negociables)

- **Persistencia**: el objeto del proceso lo persiste el action `SAVE` (el framework dispara `beforeSaveAsync`/`afterSaveAsync` como HOOKS de lógica, no como el guardado en sí; en proyectos reales no hay `SaveAsync.bl.js`). Para persistir objetos/registros relacionados de forma imperativa: `Facade.saveObjectAsync(obj)` + `commitTransaction()`. Devuelve siempre la promesa.
- **Datos**: desde bl.js, carga con `BoFactory` (`loadObjectByParamsAsync`, `createListAsync`); `Facade` para guardar/commit/dispositivo. Todo async, nunca SOQL directo. No dejes cadenas de promesas rotas (`sf mdl build` las detecta).
- **Release-safe**: en tu lógica bl.js marca el ApexDoc con `@module CUSTOM` (no `CORE`) para que el upgrade de release del producto no pise tu código.
- **Fechas**: siempre ANSI con helpers de `Utils` (`createAnsiDateToday`, `convertDate2Ansi`, `addDays2AnsiDate`), no `Date` crudo.
- **Validación**: 4 piezas — `ValidationMessages` + `<Validation>` en el BO + método bl.js con `messageCollector.add({level,objectClass,messageID})` + action `VALIDATION` antes del Save; y `Save ... validate="TRUE"`. El framework muestra el popup solo.
- **ACL**: `getACL()` + `removeRight`/`addRight` (`AclObjectType.PROPERTY`, `AclPermission.EDIT|VISIBLE`) por rol/estado, típicamente en `afterLoadAsync`. NUNCA `setAce` (obsoleto).
- **Change events**: para recalcular al cambiar un valor, property `onChanged` (`<Events>` en la `SimpleProperty`) o `addItemChangedEventListener` para List Objects; el handler recalcula y la UI reacciona por bindings. Es reacción al cambio de DATO, distinta de los eventos de UI.
- **UI**: bindings `TWO_WAY` para editables; el modelo (validación + ACL) gobierna obligatoriedad y editabilidad, no la interfaz.
- **Qué baja**: acota con `Where` / Named Query / NFT. Para que un campo viaje: field set `MobilityRelevant` + Tracked Object; para que vuelva: `UploadRelevant`.
- **Textos** visibles: del Locale Contract, nunca hardcode.
- **Antes de `sf mdl package`**: build sin errores + probar el flujo en el simulador + consola del hilo Engine sin errores.

## Gotchas frecuentes

- Olvidar el field set `MobilityRelevant` o el CORS de `localhost:3000`: la feature "no aparece" o el simulador "no autentica".
- Faltó el `__c` en una Named Query de objeto custom.
- Lo que NO baja: Named Query mal armada o governor limits (fallback a SF REST). Lo que NO sube: FLS/Sharing -> Clear Upload Failures.
- Usar `setAce` (obsoleto) en vez de `removeRight`/`addRight`.
- Confundir el debugging de desarrollo (simulador, DevTools) con el troubleshooting de producción (Sync Management, dispositivos reales).
- Citar una "Figura N": los diagramas están descritos, no embebidos. Si un visual ayuda, regeneralo con el visualizador.

## Mapa de tareas -> receta

| Si el usuario quiere… | Lee | Snippet |
| --- | --- | --- |
| Entender arquitectura o estructura del workspace | `01-arquitectura.md` | — |
| Modelar qué baja (Tracked Objects, Named Queries, NFT, scope) | `02-modelo-datos.md` | §1 |
| Montar entorno, conectar org, Git, ciclo diario | `03-setup-modeler-git.md` + `external-client-app.md` | §10 |
| Definir contracts / action types (los 14) / `sf mdl add` | `04-contracts-action-types.md` | §2 |
| Mapear un objeto al backend (Datasource: joins, condiciones, atributos) | `04-contracts-action-types.md` | §13 |
| Armar pantallas, bindings, Master-Detail | `05-ui-master-detail.md` | §3 |
| Escribir bl.js, validaciones, ACL | `06-logica-validaciones-acl.md` + `bl-js-api.md` | §4, §5, §6 |
| Recalcular al cambiar un campo/ítem (change events) | `bl-js-api.md` + `06-logica-validaciones-acl.md` | §11 |
| Capturar/guardar/sincronizar fotos | `02-modelo-datos.md` + `bl-js-api.md` | §12 |
| Saber qué método de Facade/Utils/contexto usar, o un lifecycle hook | `bl-js-api.md` | §4 |
| Entender/configurar sincronización | `07-sincronizacion.md` | §1 |
| Diagnosticar un error de sync | `08-troubleshooting-sync.md` + `ref-sync-management.md` | — |
| UIPluginV2 o Mobile Links | `09-uipluginv2-mobile-links.md` | §7, §8 |
| Theming, PDF (PrintLayoutV2), localización | `10-theming-pdf-localization.md` | §9 |
| Un comando o flag `sf mdl` | `ref-cli-modeler.md` | — |
| Cualquier página/herramienta de la consola Sync Management | `ref-sync-management.md` | — |
| Depurar en desarrollo (simulador, breakpoints, SQLite) | `debugging-desarrollo.md` | — |

Para tareas que cruzan capas (lo habitual), sigue el orden del modelo mental (la rebanada vertical): primero qué dato necesitas, después contract/lógica, UI, sync y entrega, componiendo desde `snippets.md` y las referencias temáticas.

## Estructura de un proyecto real

Cómo se organiza un workspace del Modeler (visto en repos reales), útil para ubicarte y
generar artefactos con la convención correcta:

- `src/<Módulo>/` por dominio (Order, Visit, Product, Promotion, Call, Tour, Attachment, Sync, Locale, UI Plugins, BusinessObjectHelpers…), y adentro subcarpetas por tipo: **`BO`** (business/list/lookup objects), **`DS`** (datasource), **`PR`** (process), **`PL`** (UI/plugin), **`TB`** (text bundle).
- Prefijos de nombre: **`Bo`** business object, **`Lo`** list object, **`Li`** list item, **`Lu`** lookup object, **`Ds`** datasource. Extensiones: `.businessobject.xml`, `.listobject.xml`, `.listitem.xml`, `.processflow.xml` (procesos), `.userinterface.xml` (UI), `.datasource.xml`, `.uipluginv2.xml` (plugins; V1 `.uiplugin.xml`), `.validationmessages.xml` (mensajes de validación).
- La UI se arma **por patrones**: `Page[pagePattern] -> Section[sectionPattern] -> Area[areaPattern] -> controles`. La editabilidad/visibilidad se refleja con bindings `type="Editable"`/`type="Visible"` o por ACL.
- La lógica se parte en **un archivo por método**, nombrado `<Objeto>.<Metodo>.bl.js`, bajo una carpeta de versión de modelo (`Mv1`, `Mv2`). El nombre del archivo lo determinan los tags `@this` y `@function` del ApexDoc.
- Los `bl.js` son **parcialmente autogenerados**: personalizas dentro de los rangos de inserción marcados, o con funciones PRE/POST/REPLACE. Marca tu lógica como `@module CUSTOM`.
- Convenciones de código observadas: `"use strict";` arriba, `var me = this;`, promesas con la librería `when` (`when.resolve`, `when.all`) devolviendo siempre la promesa, getters/setters encadenados (`me.getBoOrderMeta().getX()`), constantes de tipo en mayúscula (`LO_ORDERITEMS`), `PKey.next()` para nuevos PKeys, `.setObjectStatus(me.self.STATE_NEW_DIRTY)`.

## Cómo usar las referencias

- Cada archivo abre con un **"Resumen operativo"**: léelo primero (fast-path accionable + reglas de decisión); baja al detalle solo si hace falta.
- Los módulos temáticos cierran con un **"Checklist de verificación"**: úsalo para validar el trabajo del dev antes de darlo por terminado.
- `bl-js-api.md` (API de runtime) y `snippets.md` (patrones copy-paste) son tus dos herramientas de construcción: reachá por ellas al escribir código.
- Los diagramas no están embebidos; aparecen como "Diagrama (descrito, no embebido): …". No cites una "Figura N" al usuario; si un visual ayuda, regeneralo con el visualizador.
- Las referencias cruzadas apuntan al archivo (`06-logica-validaciones-acl.md`), no a "módulos".

## Límites de esta skill

- Configuración/administración del modelo de datos de CG Cloud del lado plataforma (objetos `cgcloud__`, retail execution config, promociones) -> `pc-cg-cloud-guide`.
- Desarrollo Apex/LWC general fuera de la app offline -> `pc-crm-salesforce-dev-guide`.
- El setup del org (licencias, perfiles, Permission Sets, instalar Sync Management) es prerrequisito de admin; esta skill solo cubre el punto de contacto config<->app (la External Client App).
