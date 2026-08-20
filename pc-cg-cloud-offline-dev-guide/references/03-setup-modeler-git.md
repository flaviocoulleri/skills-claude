# Setup del Modeler y workflow Git

Hasta acá entendiste qué es la app offline (`01-arquitectura.md`) y cómo se decide qué datos viven en el dispositivo (`02-modelo-datos.md`). En este módulo armas tu entorno de trabajo de punta a punta: instalas el VS Code-based Modeler, aprendes los comandos de la CLI, importas los contracts, corres el simulador, empaquetas y despliegas, y montas el workflow de Git que te va a permitir convivir con las releases de Salesforce sin romper tus customizaciones.

## Resumen operativo

- Ciclo: import de contracts -> iteracion local (customizar -> `sf mdl build` -> `sf mdl simulate`) -> `sf mdl package` -> publicar en Sync Management (Deployment Packages).
- Conexion al org: `sfConsumerKey` en `appl/config/config.json` (el Consumer Key sale de la External Client App, ver `external-client-app.md`); agrega `http://localhost:3000` al CORS allowed list o el simulador no autentica.
- Git: rama `core` protegida, `cust` como base del proyecto, feature branches por trabajo.
- Comandos: ver `ref-cli-modeler.md`.

## 1. Qué vas a montar

El desarrollo en el Modeler es un ciclo local con un cierre en la nube. Importas los contracts a tu workspace, los customizas, haces build de los runtime artifacts (RTAs), los pruebas en el simulador, y cuando están listos los empaquetas en un deployment.zip que subes a Sync Management para publicarlos. La parte iterativa (customizar → build → simular) la repites todas las veces que haga falta antes de empaquetar.

> Diagrama (descrito, no embebido): El ciclo de desarrollo: import, iteración local (customizar/build/simular), package y deploy.

## 2. Prerrequisitos

Antes de instalar nada del Modeler, tu máquina necesita esta base. En Windows hay algunos pasos extra que, si los salteas, te van a hacer fallar la instalación del plugin más adelante.

| Herramienta | Versión / detalle |
| --- | --- |
| Sistema operativo | Windows 10 o superior, Windows Server 2019, o Mac (Intel o M1). |
| Editor | Visual Studio Code. |
| Control de versiones | Un cliente Git instalado. |
| Node.js | Node.js 20. En Windows, no marques la opción de instalar las herramientas adicionales automáticas. |
| Python | Python 3.12, y luego pip install setuptools (o pip3 install setuptools). |
| Build Tools (solo Windows) | Microsoft Visual Studio Build Tools (Community) con el workload "Desktop development with C++" y el último Windows 10 SDK. |
| Navegador | Google Chrome, preferentemente usado en modo incógnito para evitar choques de sesión con la org. |

## 3. Instalación de la CLI y el plugin

Con los prerrequisitos listos, instalas la Salesforce CLI y, sobre ella, el plugin del Modeler:

```
# 1. Salesforce CLI (global, vía npm)
npm install @salesforce/cli --global
 
# 2. Plugin del Modeler
sf plugins install @ind-rcg/modeler-sfdx-cli-plugin
 
# Para actualizar el plugin más adelante:
sf plugins install @ind-rcg/modeler-sfdx-cli-plugin@latest
sf plugins update                  # actualiza todos los plugins
```

Para verificar la instalación y administrar el plugin:

```
sf plugins                                              # lista los plugins y sus versiones
sf plugins inspect @ind-rcg/modeler-sfdx-cli-plugin     # versión y detalle del plugin
sf plugins uninstall @ind-rcg/modeler-sfdx-cli-plugin   # desinstalar
```

Si la instalación del plugin falla en Windows, mira la sección 9: casi siempre es el SDK, la variable VCTargetsPath o el modo de PowerShell. Y si en algún momento necesitas el detalle completo de un comando, tienes la Referencia de la CLI del Modeler como hoja de consulta.

## 4. El workspace

El workspace es el directorio de trabajo del Modeler. Lo inicializas con sf modeler workspace create, y genera esta estructura:

| Carpeta / archivo | Qué contiene |
| --- | --- |
| src/ | Los contracts: el core extraído del DesignContracts.zip más tus customizaciones. Es donde editas. |
| appl/ | La carpeta de la aplicación. Adentro: app, build (los runtime artifacts del generador/validador y el deployment.zip final), config (el config.json con el sfConsumerKey) y data (información de runtime y el branch.config.json). |
| contractSnippets/ | Las plantillas por defecto que usa el wizard sf mdl add para crear recursos nuevos. |

Después de actualizar el plugin (o de tocar configuraciones avanzadas como el branch.config.json, sección 9), corre sf modeler workspace upgrade para que el workspace adopte las capacidades de la nueva versión y revincule los XSD.

## 5. Importar contracts

Un workspace recién creado está vacío de contracts: hay que importarlos. El comando es importContracts, y según el zip de origen ocurren transformaciones automáticas distintas.

```
sf modeler workspace utils importContracts -i <zip> [-p <src>] [-c] [--json]
 
#  -i   el zip de contracts a importar (DesignContracts.zip o MCP.zip)
#  -p   (opcional) path al directorio src de destino
#  -c   importar core contracts
#  --json  salida en formato JSON
```

### 5.1 Las dos transformaciones

Lo importante es entender qué le pasa a los archivos al importarlos a src/:

- Desde el core (DesignContracts.zip): el sistema toma los archivos .core.xml y los convierte directamente a archivos .xml. Es el core que entrega Salesforce en cada release.

- Desde un paquete custom (MCP.zip): el sistema convierte automáticamente todos los archivos XML de business logic a archivos bl.js (JavaScript). Por eso, a partir de hoy, la lógica de negocio la vas a ver y editar como JavaScript, no como XML.

El DesignContracts.zip lo entrega Salesforce en cada release: es el paquete con todos los core contracts de esa versión, y es la base que heredas. El MCP.zip aparece cuando traes customizaciones generadas previamente.

Caso especial: si vienes de un workspace del viejo Modeler de Windows Server, el comando sf modeler workspace utils migrateContracts lo migra — pasa los XML de business logic a archivos bl.js, saca los namespaces obsoletos y valida atributos como pagePattern, bindingMode y actionType.

## 6. El ciclo de desarrollo local

Con los contracts importados, el bucle de trabajo son dos comandos. build genera y valida los runtime artifacts a partir de tus contracts; server start levanta el simulador para que pruebes la app sin un dispositivo físico.

```
sf modeler workspace validate       # alias: sf mdl validate
                                    # chequea esquema/coherencia SIN generar RTAs
 
sf modeler workspace build          # alias: sf mdl build
                                    # genera y valida los RTAs (en appl/build)
 
sf modeler workspace server start   # alias: sf mdl simulate
                                    # simulador en http://localhost:3000
 
sf modeler workspace cleanup        # alias: sf mdl clean
                                    # limpia cache y resetea la SQLite del simulador
```

Un paso fácil de olvidar: para que el simulador pueda hablar con tu org, tienes que agregar http://localhost:3000 a la CORS allowed list de la org (Setup → CORS). Sin eso, el simulador levanta pero no autentica.

El Consumer Key que va en el config.json sale de la External Client App de la org (el reemplazo de la Connected App); cómo crearla y de dónde sacar el Consumer Key, el Custom Domain y la Callback URL está en el documento External Client App.

Y una vez que el flujo corre en el simulador, ahí mismo lo depuras: breakpoints en tu bl.js, la consola del hilo Engine y el Debug Window. Todo eso está en el módulo Debugging y testing en desarrollo.

Dos comandos de apoyo: validate hace la verificación sintáctica sin compilar (ideal para un pipeline de CI/CD), y cleanup resetea el cache y la base local del simulador cuando se comporta raro.

## 7. Empaquetar y desplegar

Cuando el cambio quedó como quieres, lo llevas a la org en cuatro pasos:

- Build de artifacts. Ejecutas sf modeler workspace build para compilar los RTAs a partir de tus contracts customizados.

- Crear el deployment package. Ejecutas sf modeler workspace package (alias sf mdl package). Empaqueta los RTAs en un deployment.zip que queda en $workspace/appl/build.

- Registrar en Sync Management. En la org, entras a la app Sync Management, página Deployment Packages, y subes (upload) el deployment.zip. El mapa completo de esa app —todas sus páginas, configuraciones y herramientas de diagnóstico— está en la Referencia de Sync Management.

- Publicar los cambios. En esa misma sección, asignas y publicas el package a todos los usuarios o a grupos específicos. En el próximo sync, la app descarga y aplica los cambios.

## 8. Workflow Git

La razón de ser de la estrategia de branches es una sola: aislar el core que entrega Salesforce de tus customizaciones, para poder subir de release sin pisar tu trabajo. Se arma en tres niveles.

> Diagrama (descrito, no embebido): Modelo de branches: core protegida, cust como base del proyecto, y feature branches por trabajo.

- Rama core (p. ej. 246-core o SpringXX-core): aloja únicamente los core contracts del DesignContracts.zip de esa release. Se protege estrictamente y no se modifica jamás; solo sirve para importar actualizaciones y fixes de core.

- Rama de customización (p. ej. 246-cust): se crea a partir de la rama core y es la base del proyecto, donde viven tus custom features.

- Feature branches: para cada trabajo de desarrollo te ramificas desde la rama cust, y reincorporas los cambios con un pull request, resolviendo los conflictos localmente.

### 8.1 Subir de release

Cuando Salesforce saca una release nueva, creas la rama core de la versión destino (por ejemplo 248-core) a partir de la core existente (246-core), importas el nuevo DesignContracts.zip, y luego haces el back-merge hacia tu rama cust, resolviendo los conflictos entre el core nuevo y tus customizaciones. Como el core y lo custom están separados por diseño, el merge es manejable.

Sobre el .gitignore: la documentación de arquitectura no fija una configuración estricta, así que usa las directivas estándar de proyectos Node y Salesforce CLI (excluye node_modules, variables de entorno y logs temporales).

## 9. Errores comunes de setup y deploy

| Error / síntoma | Causa | Solución |
| --- | --- | --- |
| EADDRINUSE al iniciar el simulador | El puerto 3000 ya está ocupado por otro proceso | Terminar el proceso que usa el puerto y reejecutar server start |
| El simulador levanta pero no autentica | Varias instancias del navegador abiertas o no usar incógnito | Usar Chrome en modo incógnito; agregar http://localhost:3000 al CORS allowed list de la org |
| "Unable to update lock within the stale threshold" (Windows, install plugin) | Bloqueo durante la instalación | Reintentar el comando con el modificador --verbose |
| Errores de node-gyp al instalar (Windows) | Falta un SDK de compilación | Instalar el Windows 8.1 SDK desde el Visual Studio Installer |
| Falla de compilación nativa (Windows) | La variable VCTargetsPath no apunta a Build Tools | Apuntar VCTargetsPath a la instalación de MS Build Tools, terminando en barra invertida (\) |
| La instalación falla en PowerShell | La sesión no está en modo FullLanguage | Abrir PowerShell en modo FullLanguage |
| build falla por validación XSD | Contracts mal formados | Revisar atributos como actionType o bindingMode en los XML contra las reglas del Modeler; el log lista los contracts con error |

## 10. Caso práctico de punta a punta

Esta es la secuencia completa, de máquina limpia a una customización publicada, atando todo lo anterior:

```
# (0) Prerrequisitos ya instalados: VS Code, Git, Node 20, Python 3.12, CLI + plugin
 
# (1) Rama core: workspace e importación del core de la release
git checkout 246-core
sf modeler workspace create
sf modeler workspace utils importContracts -i DesignContracts.zip -c
 
# (2) Rama de customización desde core, y feature branch para el trabajo
git checkout -b 246-cust
git checkout -b feature/cambio-cockpit
 
# (3) (opcional) importar customizaciones previas -> se transforman a bl.js
sf modeler workspace utils importContracts -i MCP.zip
 
# (4) Customizar en src/, luego iterar build + simulador
sf modeler workspace build
sf modeler workspace server start        # http://localhost:3000
 
# (5) Empaquetar cuando esté listo
sf modeler workspace package             # -> appl/build/deployment.zip
 
# (6) Merge por Pull Request a 246-cust, y deploy en la org:
#     Sync Management -> Deployment Packages -> subir deployment.zip -> publicar
```

A partir de acá, cada cambio nuevo es repetir los pasos 2 a 6 desde una feature branch.

## 11. Puntos clave

- El Modeler vive sobre la Salesforce CLI: instalas la CLI con npm y el plugin con sf plugins install @ind-rcg/modeler-sfdx-cli-plugin.

- En Windows, los Build Tools, el SDK, VCTargetsPath y el modo FullLanguage de PowerShell son la causa de casi todos los fallos de instalación.

- El workspace (sf modeler workspace create) tiene src/ (editas acá), appl/ (con build —los RTAs y el deployment.zip— y config —el config.json—) y contractSnippets/.

- importContracts transforma: el core .core.xml → .xml, y el custom MCP.zip → bl.js (la lógica de negocio se vuelve JavaScript).

- El ciclo local es build + server start (simulador en localhost:3000, que necesita CORS habilitado).

- Deploy = build → package (deployment.zip) → subir a Sync Management → publicar.

- Git: rama core protegida (solo DesignContracts.zip), rama cust como base, feature branches por trabajo; las releases se suben creando una core nueva y haciendo back-merge.

## Checklist de verificacion

- `sf mdl build` corre sin errores antes de simular/empaquetar.
- `sfConsumerKey` cargado y `localhost:3000` en el CORS allowed list.
- Estas en la feature branch correcta (no en `core`/`cust` directo).
- Probaste en el simulador antes de `sf mdl package`.
