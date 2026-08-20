# Referencia de la CLI del Modeler

Referencia de la CLI del Modeler

El Modeler no es una aplicación con botones: es un plugin de la Salesforce CLI, y prácticamente todo el trabajo de construir, validar, simular y empaquetar la app pasa por la terminal. Este documento es la referencia completa de esa CLI: todos los comandos, sus alias, sus flags y el orden en que se usan. Es el papel que vas a tener al lado del teclado.

Cómo se relaciona con el resto del curso: el `03-setup-modeler-git.md` explica el setup inicial y el flujo de trabajo con Git de punta a punta; este documento se concentra en la CLI en sí, como referencia de consulta rápida. Algunos comandos aparecen también en otros módulos (refreshLocale en el 10, build y simulate en el 1 y el 3); acá están todos juntos y en detalle.

## Resumen operativo

- Hoja de referencia de todos los comandos `sf mdl`. El ciclo: instalar -> `create` -> `importContracts` -> (`add`/editar -> `build` -> `simulate`, iterando) -> `package` -> publicar en Sync Management.
- Busca el comando/flag exacto en las tablas de abajo antes de escribirlo; no reconstruyas flags de memoria.

## 1. Instalación y verificación

La CLI del Modeler corre sobre la Salesforce CLI estándar, así que primero instalas esa y después el plugin @ind-rcg/modeler-sfdx-cli-plugin. Requiere Node.js 20; en Windows, además, las Microsoft Build Tools bien configuradas (variable VCTargetsPath).

```
# 1) la Salesforce CLI
npm install @salesforce/cli --global
 
# 2) el plugin del Modeler (--verbose si quieres ver el detalle)
sf plugins install @ind-rcg/modeler-sfdx-cli-plugin
 
# instalar/actualizar a la última versión
sf plugins install @ind-rcg/modeler-sfdx-cli-plugin@latest
sf plugins update            # actualiza todos los plugins
```

| Comando | Qué hace |
| --- | --- |
| sf plugins | Lista los plugins instalados y sus versiones. |
| sf plugins inspect @ind-rcg/modeler-sfdx-cli-plugin | Muestra la versión y el detalle del plugin del Modeler. |
| sf plugins uninstall @ind-rcg/modeler-sfdx-cli-plugin | Desinstala el plugin del Modeler. |

## 2. El workspace que crea la CLI

Al correr sf modeler workspace create, la CLI genera el andamiaje de carpetas. Conviene tenerlo claro porque casi todos los comandos leen o escriben en alguna de estas:

| Carpeta | Qué contiene |
| --- | --- |
| src | Los design contracts: el core importado más tus contracts customizados. |
| appl | La carpeta de la aplicación. Adentro: app, build (la salida del generador/validador y el deployment.zip final), config (el config.json con el sfConsumerKey) y data (información de runtime y el branch.config.json). |
| contractSnippets | Las plantillas por defecto que usa el wizard sf mdl add para crear recursos nuevos. |

Nota de corrección: en el `01-arquitectura.md` mostré build y config como carpetas de primer nivel del workspace; en rigor cuelgan de appl (appl/build, appl/config). Esta es la estructura exacta — ver la sección de cierre del documento.

## 3. Comandos: inicialización y configuración

| Comando | Qué hace |
| --- | --- |
| sf modeler workspace create; | Crea e inicializa el workspace en el directorio actual (genera src, appl y contractSnippets). Es el primer comando de todo proyecto. |
| sf modeler workspace upgrade; (sf mdl ws upgrade) | Actualiza la configuración local del workspace para aprovechar las capacidades de la versión instalada del plugin. Hay que correrlo tras actualizar el plugin o tras tocar el branch.config.json (vincula los XSD más recientes a .vscode/settings.json). |

## 4. Comandos: contratos y recursos

### 4.1 importContracts

Importa y transforma los design contracts desde un paquete (un DesignContracts.zip del core, o un MCP custom) hacia src. Es como traes el core de Salesforce al workspace.

```
sf modeler workspace utils importContracts -i DesignContracts.zip
```

| Flag | Significado |
| --- | --- |
| -i <zip> | Requerido. Ruta al archivo .zip a importar. |
| -p <path> | Opcional. Ruta de destino al directorio src (por defecto, el workspace actual). |
| -c | Opcional. Al importar un MCP custom, extrae solo los core contracts (.core.xml) y omite los custom. Si se omite el flag, importa solo los custom (.xml). |
| --json | Opcional. Devuelve la salida en formato JSON. |

Transformaciones: al importar un MCP clásico, convierte los XML de business logic a archivos bl.js; al importar el DesignContracts.zip, renombra los .core.xml a .xml.

### 4.2 Otros comandos de recursos

| Comando | Qué hace |
| --- | --- |
| sf modeler workspace add; (sf mdl add) | Wizard interactivo que crea recursos nuevos a partir de los contractSnippets: module, businessobject, listobject, lookupobject, datasource, businesslogic, userinterface y process. Genera los XML y .bl.js en src/<Module> (BO/, DS/, PR/…). Al crear un listobject, genera también su listitem y los métodos base. |
| sf modeler workspace utils base64encode; --input <archivo> | Convierte un binario (imagen, fuente) a una cadena Base64 para incrustarla en el CDATA de un Image Contract o External Files contract. Ej.: --input ./Barcode.svg |
| sf modeler workspace utils migrateContracts; | Migra un workspace del viejo Modeler de Windows Server: pasa los XML de business logic a .bl.js, saca los namespaces obsoletos y valida atributos (pagePattern, bindingMode, actionType). |
| sf modeler workspace refreshLocale; | Sincroniza los Locale contracts (src/Locale) agregando labels e imágenes nuevas o modificadas desde el framework/global labels. Nunca borra. Flag -c <idioma.locale.xml> para actualizar un solo idioma (ej. -c de.locale.xml). |

## 5. Comandos: validación, compilación y limpieza

| Comando | Qué hace |
| --- | --- |
| sf modeler workspace validate; (sf mdl validate) | Verifica el esquema y la coherencia de los contracts sin generar los runtime artifacts. Ideal para un pipeline de CI/CD. |
| sf modeler workspace build; (sf mdl build) | Valida y compila los contracts generando los Runtime Artifacts (RTAs). Escribe el resultado en appl/build. Si hay errores, falla y los lista en consola. Es el comando que más vas a correr. |
| sf modeler workspace cleanup; (sf mdl clean) | Limpia el workspace: borra artefactos cacheados corruptos y resetea el estado de la base local (SQLite) del entorno de simulación. Útil cuando el simulador se comporta raro. |

## 6. Comandos: simulación y empaquetado

| Comando | Qué hace |
| --- | --- |
| sf modeler workspace server start; (sf mdl simulate) | Levanta el servidor Node.js local que aloja la simulación, en el puerto 3000. Requiere el sfConsumerKey seteado en appl/config/config.json. |
| sf modeler workspace package; (sf mdl package) | Empaqueta los RTAs válidos en el deployment.zip dentro de appl/build. Requiere que el último build haya sido exitoso. Ese zip es lo que se sube a Sync Management. |

El simulador se abre en Chrome (preferentemente incógnito) en estas URLs; agrega &forceOffline para forzar el modo sin red:

```
http://localhost:3000/framework/index.html?desktop
http://localhost:3000/framework/index.html?desktop&forceOffline
```

Sobre "deploy": no existe un comando sf mdl deploy. La distribución es manual: se toma appl/build/deployment.zip y se registra en la app Sync Management de Salesforce, donde se publica el cambio.

## 7. Configuraciones críticas

### 7.1 Validación estricta de XML (USE_LATEST_XSD_VALIDATIONS)

Para que el editor te sugiera valores válidos (de actionType, pagePattern, bindingMode) junto con una extensión como XML Language Support de Red Hat, activas el flag en branch.config.json (carpeta data del workspace; por defecto está en false) y después corres upgrade:

```
// branch.config.json
{ "USE_LATEST_XSD_VALIDATIONS": true }
 
# aplicar el cambio (vincula los XSD a .vscode/settings.json)
sf modeler workspace upgrade
```

### 7.2 Consumer Key para la simulación

Antes del primer server start, inserta tu Consumer Key de la org en appl/config/config.json. Sin esto, el simulador no levanta:

```
// appl/config/config.json
{ "sfConsumerKey": "<tu Consumer Key>", ... }
```

## 8. El ciclo de desarrollo de punta a punta

Así se encadenan los comandos en el día a día. Los pasos amarillos son el lazo iterativo donde vas a pasar la mayor parte del tiempo:

> Diagrama (descrito, no embebido): El ciclo de la CLI: instalar → create → importContracts → (add/editar → build → simulate, iterando) → package → publicar en Sync Management.

- Instalar la Salesforce CLI y el plugin del Modeler.

- Preparar Git con las ramas core (p. ej. 246-core) y customizer (246-cust), como detalla el `03-setup-modeler-git.md`.

- create el workspace en la rama de feature.

- importContracts para traer el core (DesignContracts.zip bajado del App Builder).

- Modelar (iterativo): sf mdl add para crear recursos, editar XML/JS, sf mdl build para compilar, sf mdl simulate para probar en localhost:3000 y revisar logs.

- Sincronizar metadata: refreshLocale para los labels, y cleanup si el cache local se ensució.

- package para generar el deployment.zip.

- Publicar: registrar el deployment.zip en Sync Management y publicar.

## 9. Errores frecuentes con la CLI

| Síntoma | Causa y solución |
| --- | --- |
| EADDRINUSE en el puerto 3000 | Ya hay un proceso usando el 3000 (un simulador anterior). Ciérralo y vuelve a correr server start. |
| El simulador abre en blanco / error de CORS | Usa Chrome en incógnito y asegurate de que localhost:3000 esté en el CORS allowed list de la org. |
| "Unable to update lock" al instalar el plugin | Reintenta la instalación agregando --verbose para ver el detalle. |
| Falla node-gyp / Build Tools (Windows) | Configurá las Microsoft Build Tools (C++ y el SDK) y verifica que VCTargetsPath termine en backslash. |
| El build falla por validación XSD | El log de consola indica el contract mal formado y el atributo; ábrelo y corregí el valor inválido. |

## 10. Cheat-sheet

Los comandos que vas a usar el 90% del tiempo, en orden de uso:

| Comando | Para |
| --- | --- |
| sf modeler workspace create | crear el workspace |
| sf mdl ws utils importContracts -i <zip> | traer el core |
| sf mdl add | crear un recurso (BO, DS, proceso, UI…) |
| sf mdl build | compilar a RTAs |
| sf mdl simulate | probar en localhost:3000 |
| sf modeler workspace refreshLocale | propagar labels |
| sf mdl clean | resetear el cache local |
| sf mdl package | generar el deployment.zip |

Pendiente para revisión: este documento corrige la estructura del workspace respecto del `01-arquitectura.md` (build y config cuelgan de appl, no son de primer nivel). Si te parece, ajusto esa tabla del `01-arquitectura.md` y, de paso, reviso que el `03-setup-modeler-git.md` use exactamente esta misma nomenclatura, así queda todo consistente.
