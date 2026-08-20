# Debugging y testing en desarrollo

Debugging y testing en desarrollo

Hay dos mundos de diagnóstico y conviene no confundirlos. El troubleshooting de producción —dispositivos reales, logs en Sync Management— lo cubren el `08-troubleshooting-sync.md` y la Referencia de Sync Management. Este módulo es el otro: el inner loop de desarrollo, donde depuras tu propio código en el simulador, en tu máquina, antes de empaquetar. Saber hacer esto bien es lo que te vuelve autónomo: no dependes de subir a un dispositivo para entender por qué tu bl.js no hace lo que esperas.

## Resumen operativo

- Inner loop de desarrollo (distinto del troubleshooting de produccion de `08-troubleshooting-sync.md`/`ref-sync-management.md`). Tres superficies: Chrome DevTools (tu codigo), el Debug Window (logs y SQL del framework, triple toque) y la extension SQLite en VS Code (la base local).
- Simulador: `?desktop` (online) o `&forceOffline` (usa cache, mas rapido). Ábrelo en incognito; la logica corre en el hilo `Engine` (selecciónalo en Console y Sources).
- Breakpoints: bl.js en `<Objeto>.<metodo>.js` (hilo Engine); UIPluginV2 en `about:srcdoc/.../UIPluginV2_<Nombre>.js` (frame de consola en `about:srcdoc`).
- Antes de empaquetar: build limpio -> simular -> breakpoints -> consola del Engine sin errores -> package.

## 1. El inner loop

El ciclo de desarrollo es editar → build → simular → depurar → corregir, repetido hasta que el flujo anda. El simulador (localhost:3000) no es solo para mirar la UI: es tu entorno de depuración completo, porque corre el mismo framework que el dispositivo. Tienes tres superficies de depuración, cada una para un tipo de pregunta distinto:

> Diagrama (descrito, no embebido): Las tres superficies: Chrome DevTools (tu código), el Debug Window (logs y SQL del framework) y la extensión SQLite en VS Code (la base local).

## 2. Levantar el simulador para depurar

Con el servidor corriendo (sf mdl simulate), abres el simulador en Chrome, preferentemente en incógnito —para aislar la sesión y evitar authentication mismatches por credenciales cacheadas de otra org. Las URLs exactas:

```
# Online: autentica y sincroniza con Salesforce
http://localhost:3000/framework/index.html?desktop
 
# Offline: omite el sync y usa los datos ya cacheados (más rápido
#          para iterar UI, PrintLayout, lógica que no necesita datos nuevos)
http://localhost:3000/framework/index.html?desktop&forceOffline
```

Recuerda tener http://localhost:3000 en la CORS allowed list de la org (Setup → CORS), o el simulador levanta pero no autentica.

### 2.1 Emular iOS / Android, teléfono / tablet

Para probar el comportamiento responsive por plataforma:

- Abre Chrome DevTools (F12 o clic derecho → Inspect).

- Activa el Toggle device toolbar (en Mac, ⌘ + ⇧ + M).

- En el menú Dimensions elige el hardware a simular (iPhone 12, iPad Air, modelos Pixel/Galaxy, etc.).

- Refresca la pestaña para que el framework asimile el redimensionamiento e inicialice en portrait o landscape.

## 3. La consola y el hilo Engine

La lógica de negocio no corre en el hilo principal del navegador, sino en un hilo aparte llamado Engine. Por eso, en la pestaña Console de DevTools, lo primero es seleccionar el contexto de ejecución Engine en el menú desplegable; si no, tus comandos no ven el estado del framework.

Desde ese contexto puedes interrogar el framework en vivo:

```
// ¿en qué process contract estoy parado?
Framework.getProcessContext().__spec.name
 
// el Business Object del usuario actual y sus propiedades
ApplicationContext.get("user")
```

## 4. Breakpoints en bl.js

Para detener la ejecución dentro de un método de business logic e inspeccionar el estado:

- En DevTools, ve a la pestaña Sources y, en el selector de thread, elige Engine.

- Abre el archivo con Command+P (macOS) o Control+P (Windows) y escribe el nombre del objeto seguido del método, por ejemplo LoCustomerPOSCard.getCustomerPOSForCard.js.

- Pon el breakpoint en la línea sospechosa y disparas el evento desde la UI del simulador.

- La ejecución se suspende: inspeccionas variables en el panel Scope, recorres la pila en Call Stack, y usás step over / step in. Puedes evaluar expresiones en la consola contra el contexto pausado.

## 5. Breakpoints en un UIPluginV2

El código de un UIPluginV2 corre en un iframe y se inyecta con el patrón de nombre UIPluginV2_<NombreDelPlugin>. Para depurarlo:

- En Sources, navega a la ruta virtual about:srcdoc/localhost:3000/framework/UIPluginV2_<Nombre>.js.

- Pon breakpoints dentro de connectCallback(), renderCallback() o disconnectCallback().

- Al recargar la pantalla o disparar un cambio en los bindings (que provoca un re-render), la ejecución se pausa.

- Para inspeccionar el estado del plugin, cambia el frame de ejecución de la consola a about:srcdoc; ahí puedes evaluar el objeto PluginManager (el puente del plugin con el framework, ver `09-uipluginv2-mobile-links.md`).

## 6. El Debug Window

El framework trae su propia ventana de depuración. Se abre con un triple toque (triple clic) sobre el área del encabezado de la UI o sobre la pantalla de sync. Sus pestañas:

| Pestaña | Qué te da |
| --- | --- |
| Log Settings | Los controles del logging: el toggle Logs to console (manda los logs a la consola JS), Enable Logs / AppLogs, Log business logic performance (dirige métricas a AppLogs) y Truncate log messages (recorta a 1024 caracteres). El Log level fija la granularidad: Info, Debug, Trace, Status, Warning, Performance. |
| Logs | Las sentencias SQL que el framework construye a partir de tus Datasource contracts, en vivo. Es donde aislas una query fallida o que vuelve vacía. |
| AppLogs | Las métricas de performance de la business logic, cuando activas Log business logic performance. |

Entre la consola del Engine (tu JavaScript) y la pestaña Logs (el SQL generado), tienes visibilidad de las dos mitades de cualquier operación de datos.

## 7. Inspeccionar la base local

Cuando la duda es "¿el dato llegó / se guardó realmente?", miras la base local, por dos vías:

- Application tab de DevTools: en Local Storage gestionas y limpias el estado de la sesión, configuración y metadata cacheada — útil para forzar un arranque limpio.

- Extensión SQLite en VS Code: la base del simulador es un SQLite (casmobile.db) cifrado y manejado por el framework. Con una extensión de SQLite en VS Code puedes ver el schema y correr SQL para verificar, por ejemplo, que la columna de un campo nuevo se creó o que los registros esperados están ahí. Es la forma directa de confirmar el efecto de tu Datasource y de la Sync Configuration.

## 8. Rutina de testing antes de empaquetar

Antes de generar el deployment.zip, sigue siempre esta rutina. Te evita empaquetar algo roto:

- Verifica el build. Corre sf mdl build: aplica las validaciones XSD y detecta atributos inválidos, promesas rotas (broken promise chains, ver `06-logica-validaciones-acl.md`) e inconsistencias. Si dice Build failed, corregí antes de seguir.

- Levanta el simulador. sf mdl simulate; usa &forceOffline si no necesitas probar el sync, para iterar más rápido sobre los datos cacheados.

- Reproducí el flujo con breakpoints. Navega al módulo que tocaste y pon breakpoints en el bl.js (Sources → Engine) para confirmar que la lógica hace lo esperado, mirando Scope y Call Stack.

- Revisa la consola del Engine. Que no aparezcan errores asíncronos: eventos LongPress sin definir, macros XML no procesables, o violaciones a la API pública de Facade o Utils.

- Limpieza previa (opcional). sf mdl cleanup para remover configuraciones temporales de compilación y resetear la base local.

- Empaqueta. Solo cuando el build no arroja errores y el simulador confirma que el flujo anda, generas el deployment.zip con sf mdl package.

## 9. Puntos clave

- Esto es el inner loop de desarrollo (depurar tu código en el simulador), distinto del troubleshooting de producción (`08-troubleshooting-sync.md` / Sync Management).

- Abre el simulador en Chrome incógnito; ?desktop para online, &forceOffline para iterar sobre datos cacheados; emula dispositivos con el device toolbar de DevTools.

- La lógica corre en el hilo Engine: selecciónalo en Console y Sources, o no vas a ver el estado del framework.

- Breakpoints en bl.js: Sources → Engine → Cmd/Ctrl+P → <Objeto>.<método>.js. En un UIPluginV2: about:srcdoc/.../UIPluginV2_<Nombre>.js, y cambia el frame de consola a about:srcdoc para ver PluginManager.

- El Debug Window (triple toque): Log Settings (Logs to console, niveles), Logs (el SQL en vivo de los Datasource) y AppLogs (performance).

- Para confirmar datos: Application → Local Storage, y una extensión SQLite en VS Code para ver el schema y los registros de casmobile.db.

- Rutina antes de empaquetar: build limpio → simular → breakpoints → consola del Engine sin errores → (cleanup) → package.

## Checklist de verificacion

- Seleccionaste el hilo `Engine` en Console y Sources.
- Reprodujiste el flujo con breakpoints y revisaste Scope/Call Stack.
- La consola del Engine quedo sin errores asincronos (LongPress, macros XML, API Facade/Utils).
- Confirmaste el dato en la base local (Application -> Local Storage / extension SQLite).
