# UIPluginV2 y Mobile Links

Los controles nativos cubren la enorme mayoría de los casos, pero a veces necesitas algo que el framework no trae: un gráfico complejo, una visualización a medida, o conectar la app con un sistema externo. Para eso hay dos mecanismos de extensión. El UIPluginV2 te deja embeber tu propio HTML/CSS/JS dentro de una pantalla, y los Mobile Links (deeplinks) permiten que la app y aplicaciones de terceros se comuniquen entre sí.

## Resumen operativo

- UIPluginV2 corre aislado en un iFrame y habla con el framework SOLO via `PluginManager`. Callbacks: `connectCallback`, `renderCallback` (se re-invoca al cambiar un input), `disconnectCallback` (limpieza).
- El plugin ES el contract `.uipluginv2.xml`: HTML/CSS/JS van inline en bloques CDATA (`<UIComponentHTML/CSS/JS>`), las props de entrada se declaran en `<Interface><Property id=/>` y se leen como `PluginManager.<id>`, textos en `<Labels>` (`PluginManager.locale.labels.<id>`), y librerías JS en `<Libraries>` (C3JS, D3JS disponibles). Snippet en `snippets.md` §7.
- Superficie de `PluginManager`: `PluginManager.<propInterface>` (datos), `PluginManager.helpers.isDefined(x)`, `PluginManager.pluginConfiguration.<ColorN|isPortrait>` (tema/layout), `PluginManager.locale.labels.<id>` (textos), `PluginManager.throwEvent(nombre, payload)` (emitir evento al proceso, mapeado con `<CustomPluginEvent>`).
- Depuracion: en Sources, ruta `about:srcdoc/localhost:3000/framework/UIPluginV2_<Nombre>.js`; cambia el frame de la consola a `about:srcdoc` para evaluar `PluginManager` (ver `debugging-desarrollo.md`).
- Mobile Links: inbound entra por `cgcloud://share` y dispara `linkLaunchEvent`; outbound sale con `Facade.startThirdPartyAsync`.
- Regla: usa UIPluginV2 solo cuando la UI declarativa no alcanza, y respeta el aislamiento (nada de tocar el framework por fuera del PluginManager).

## 1. Cuándo personalizar más allá de lo nativo

Antes de escribir un plugin, pregúntate si un control nativo no resuelve lo mismo: los nativos rinden mejor, se integran sin fricción y no suman riesgo. El UIPluginV2 es la herramienta cuando necesitas una visualización que los controles no ofrecen (un gauge, un gráfico C3JS/D3JS, una UI muy específica). Los Mobile Links, en cambio, no son sobre la UI: son sobre comunicar la app con otra aplicación, en ambos sentidos.

## 2. UIPluginV2: qué es y dónde va

Un UIPluginV2 es un archivo XML con configuraciones de HTML, CSS y JavaScript que se ejecuta dentro de un iFrame embebido en la pantalla. Ese aislamiento es importante: explica tanto su flexibilidad como sus límites.

El control solo se puede colocar en tres contenedores de un UIDescription: GroupedElementsArea, SingleElementArea y CardContainer. Ponerlo en cualquier otro lado falla. El flag IsReadyToLoad (típicamente a nivel del CardContainer) indica que ya están todos los datos en memoria y el plugin puede renderizar.

> Diagrama (descrito, no embebido): Arquitectura del UIPluginV2: corre aislado en un iFrame y se comunica con el framework solo a través del PluginManager.

## 3. La comunicación: PluginManager

Como el plugin vive en un iFrame, no puede llamar directamente al framework (no tienes FWThrowEvent ni acceso directo al ProcessContext). El sistema inyecta un objeto JavaScript oculto, PluginManager, que es el único puente. La comunicación es estrictamente vía Bindings y Events, declarados en el contrato del plugin:

```
<UIPluginV2 name="MyNewV2Plugin" uiPlugin="TestUiPluginV2">
  <Bindings>
    <Binding target="id" binding="ProcessContext::MyBo.id"
             type="Text" bindingMode="TWO_WAY" />
  </Bindings>
  <Events>
    <CustomPluginEvent name="onTextChange" event="onTextChangeHandler" />
  </Events>
</UIPluginV2>
```

- Bindings: accedes o actualizas un valor con PluginManager.[PropertyId]. Si el binding es TWO_WAY, hacer PluginManager.Title = "Nuevo" actualiza el ProcessContext del proceso.

- Events: para disparar un evento hacia el framework usás PluginManager.throwEvent(name, params), donde name coincide con el string del contrato y params es un objeto JSON.

Así se ve la implementación JavaScript del plugin, leyendo un binding al cargar y disparando un evento al cambiar un input:

```
function connectCallback() {
    document.getElementById("titleText").innerHTML = PluginManager.Title;
}
 
document.body.addEventListener("input", function (e) {
    if (e.target.id === "titleId") {
        PluginManager.throwEvent("updateReceiverTitle",
                                 { title: e.target.value });
    }
});
```

## 4. El ciclo de vida del plugin

El plugin expone tres callbacks que el framework invoca en momentos precisos. Implementarlos bien es la diferencia entre un plugin estable y uno que parpadea o pierde datos:

| Callback | Cuándo se invoca y para qué |
| --- | --- |
| connectCallback() | Cuando el plugin se carga y el PluginManager ya está disponible. Inicializas variables y dibujas la UI inicial. |
| renderCallback() | Cada vez que el componente padre se re-renderiza. Actúa como listener ante cambios en los bindings o de orientación; acá redibujas. |
| disconnectCallback() | Justo antes de desmontar el plugin (p. ej. al tocar Back). Haces limpieza (clearTimeout). Tiene un timeout estricto: cualquier throwEvent o actualización de binding en esta fase se ignora. |

## 5. Limitaciones de UIPluginV2

El aislamiento en iFrame tiene un precio. Estas restricciones condicionan cómo escribes el plugin:

- Sin anidamiento ni reuso: un UIPluginV2 no soporta plugins anidados, y no se puede reutilizar código entre plugins distintos.

- Memoria y performance: como corren en iFrames, impactan fuerte en la RAM y el rendimiento; minimizar las librerías externas es obligatorio.

- Estilos y fuentes: se aplica un CSS Reset dentro del plugin (los estilos por defecto de la app se reinician) y las fuentes de la plataforma (como Fira Sans) no están expuestas: tienes que definirlas explícitamente por CSS.

- Red restringida: cualquier llamada web desde el JS del plugin está limitada a los dominios listados en la allowlist de la app (Webscopes).

- Bindings de listas: los enlaces a colecciones (List target) son de solo lectura y se truncan en exactamente 105 elementos; el exceso genera un warning y expone listbindingName.meta.isTruncated.

## 6. Mobile Links: qué son y el formato

Los Mobile Links (deeplinks) permiten comunicación bidireccional en tiempo real entre la app offline y aplicaciones de terceros (externas o internas): integrar KPIs contextuales (no históricos), encuestas, o compartir datos JSON. La app usa un custom URL scheme con el payload obligatoriamente codificado en Base64:

```
cgcloud://share?payload=<encodedPayload>
 
// donde <encodedPayload> es Base64 de un JSON en string:
//   btoa(JSON.stringify(payload))
```

En la configuración de links salientes puedes usar macros dinámicos que el framework reemplaza en runtime: $ACCOUNTNUMBER$, $ACCOUNTID$, $EMPLOYEENUMBER$ o $SALESORG$.

## 7. Inbound y outbound

> Diagrama (descrito, no embebido): Mobile Links: inbound entra a la app por cgcloud://share y dispara linkLaunchEvent; outbound sale con Facade.startThirdPartyAsync.

### 7.1 Inbound (hacia la app)

Registras un <ExternalEvent> en el Process Contract actual. Cuando el usuario abre el enlace cgcloud://share..., la app invoca la acción mapeada, pasándole event.success y event.data (el JSON ya decodificado):

```
<ExternalEvent name="linkLaunchEvent" action="ReceiveKpis" />
```

### 7.2 Outbound (desde la app a terceros)

Usás el método asíncrono Facade.startThirdPartyAsync(url, jsonParams). Por ejemplo, abrir Google Maps y rutear a unas coordenadas:

```
Facade.startThirdPartyAsync(
    "http://maps.google.com/maps?mode=d&daddr=" + lat + "," + lng, {});
```

También se integra Agentforce con Facade.launchAgentForce(payload), usando el evento agentforceLaunchEvent.

## 8. Limitaciones y errores de Mobile Links

| Restricción / error | Detalle |
| --- | --- |
| Tamaño del payload | Máximo 400 KB en Base64. Excederlo arroja INVALID_PAYLOAD_SIZE. |
| Contexto de UI | Los eventos inbound fallan si la app está cerrada o killeada en background, o si el usuario está en una página distinta a la que define el linkLaunchEvent. |
| Uno por flujo | Solo se permite un único linkLaunchEvent por cada Process Flow. |
| Sin eval() | El motor rechaza compilar contracts que contengan funciones eval(). |
| Sin deeplinking direccional | No se puede forzar la apertura en una pantalla específica (p. ej. abrir el Store Cockpit desde cero) ni manejar autenticación externa. |
| Códigos nativos | MISSING_PAYLOAD_PARAM, INVALID_PAYLOAD_ENCODING (falla el parseo Base64), INVALID_HOSTNAME (falta el host 'share' en cgcloud://share). |
| iOS y jsonParams | En iOS se ignoran los jsonParams de startThirdPartyAsync: hay que agregarlos manualmente a la URL. |

## 9. Caso práctico de punta a punta

Combinemos ambos mecanismos en un escenario real: una tarjeta de Share-of-Shelf que muestra un gauge a medida (UIPluginV2) y un botón que rutea hasta la tienda con Google Maps (Mobile Link saliente).

### 9.1 El gauge como UIPluginV2

Declaras el plugin dentro de un CardContainer, con el valor enlazado TWO_WAY y un evento para cuando el rep ajusta el objetivo:

```
<CardContainer name="ShareOfShelfCard">
  <UIPluginV2 name="SosGauge" uiPlugin="ShareOfShelfGauge">
    <Bindings>
      <Binding target="value" binding="ProcessContext::Audit.sosPercent"
               type="Text" bindingMode="TWO_WAY" />
    </Bindings>
    <Events>
      <CustomPluginEvent name="onTargetChange" event="recalcTargetHandler" />
    </Events>
  </UIPluginV2>
</CardContainer>
```

```
// JS del plugin: dibuja el gauge y avisa cuando cambia el objetivo
function connectCallback() { drawGauge(PluginManager.value); }
function renderCallback()  { drawGauge(PluginManager.value); }
document.body.addEventListener("change", function (e) {
    if (e.target.id === "targetInput") {
        PluginManager.throwEvent("onTargetChange",
                                 { target: e.target.value });
    }
});
function disconnectCallback() { /* limpieza si hiciera falta */ }
```

### 9.2 El botón "Cómo llegar" como Mobile Link

Una acción LOGIC del proceso llama a la business logic que abre Maps ruteando a las coordenadas de la tienda (resueltas desde el registro):

```
// en el bl.js, al tocar "Cómo llegar"
var lat = me.getStore().getLatitude();
var lng = me.getStore().getLongitude();
Facade.startThirdPartyAsync(
    "http://maps.google.com/maps?mode=d&daddr=" + lat + "," + lng, {});
```

Leído de corrido: la tarjeta carga (IsReadyToLoad) → connectCallback dibuja el gauge con el sosPercent del audit → el rep ajusta el objetivo y el plugin dispara onTargetChange, que el proceso atiende para recalcular → al tocar "Cómo llegar", el outbound link abre Maps con la ruta. Y si más tarde un sistema externo necesita empujar KPIs a esta pantalla, registras un linkLaunchEvent inbound que reciba el JSON en event.data. Con esto cubres los dos modos de extensión sin salirte de sus límites.

## 10. Puntos clave

- Primero evalúa un control nativo; usa UIPluginV2 solo para lo que los nativos no pueden (gráficos, UIs a medida).

- El UIPluginV2 es HTML/CSS/JS en un iFrame; solo va en GroupedElementsArea, SingleElementArea o CardContainer, y IsReadyToLoad habilita su render.

- La única vía de comunicación es el PluginManager: bindings con PluginManager.[PropertyId] (TWO_WAY actualiza el ProcessContext) y eventos con PluginManager.throwEvent(name, params).

- Ciclo de vida: connectCallback (init), renderCallback (re-render/bindings), disconnectCallback (cleanup, con timeout estricto).

- Límites del plugin: sin anidar ni reusar, alto costo de RAM, CSS reset y fuentes no expuestas, red restringida a la allowlist, y List bindings de solo lectura truncados en 105.

- Mobile Links: cgcloud://share?payload=Base64. Inbound con <ExternalEvent linkLaunchEvent> (event.data); outbound con Facade.startThirdPartyAsync / launchAgentForce.

- Límites de los links: payload ≤ 400 KB, un linkLaunchEvent por flujo, sin eval(), sin deeplinking direccional a pantallas; en iOS los jsonParams van en la URL.

## Checklist de verificacion

- El plugin se comunica solo por `PluginManager` (sin acceder al framework por fuera).
- Implementaste `connect/render/disconnectCallback` y liberas recursos en disconnect.
- Mobile Links: inbound (`cgcloud://share` -> `linkLaunchEvent`) y outbound (`Facade.startThirdPartyAsync`) bien cableados.
- Lo probaste apuntando la consola al frame `about:srcdoc`.
