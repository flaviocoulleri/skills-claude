# External Client App: punto de contacto con la org

External Client App: el punto de contacto con la org

Disclaimer de alcance. Poner el org de Salesforce a punto para Consumer Goods Cloud Offline (licencias, perfiles y Permission Sets, instalar y habilitar la app Sync Management, asignar la configuración) es trabajo de administración y queda fuera de este curso de desarrollo: trátalo como un prerrequisito. Este documento cubre solo el único punto donde esa configuración toca tu trabajo de dev: la app de autenticación que produce el Consumer Key que tu simulador y los dispositivos necesitan para conectarse a la org.

Desde Spring ’26, Salesforce restringió la creación de Connected Apps nuevas; el reemplazo es la External Client App (las Connected Apps existentes siguen funcionando). El rol es el mismo: habilitar OAuth y entregar el Consumer Key. Eso es lo que vas a ver acá.

## Resumen operativo

- Punto de contacto config<->app: la External Client App (reemplazo de la Connected App desde Spring '26) provee el Consumer Key. El resto del setup del org es prerrequisito de admin, fuera de alcance.
- Crearla: Setup -> External Client Apps -> Enable OAuth Settings; scopes id/api/refresh_token; deselecciona los flags de secret/PKCE/JWT para evitar popups repetidos.
- Tres datos: Consumer Key (Manage Consumer Details), Custom Domain (Domains; `.sandbox` si aplica) y Callback URL. Simulador: `sfConsumerKey` en config.json + callback `localhost:3000/fake/services/oauth/success`. Dispositivos: Connected App QR Code (Mobile Settings) -> Generate QR Code.

## 1. Crear la External Client App

En Setup, busca External Client Apps y entrá a External Client App Settings para crear la app (este es el reemplazo de la Connected App). Después:

- Habilita Enable OAuth Settings.

- Asigna estos Selected OAuth Scopes: "Access the identity URL service (id, profile, email, address, phone)", "Manage user data via APIs (api)" y "Perform requests at any time (refresh_token, offline_access)".

- Deselecciona estos flags para evitar ventanas de autenticación repetidas al abrir la app: "Require Secret for Web Server Flow", "Require Proof Key for Code Exchange (PKCE) Extension for Supported Authorization Flows", "Require Secret for Refresh Token Flow" e "Issue JSON Web Token (JWT)-based access tokens for named users".

## 2. Los tres datos que la app necesita

| Dato | De dónde sale |
| --- | --- |
| Consumer Key | En Setup → Manage Connected Apps, seleccionas la app y entras a Manage Consumer Details (sección API / Enable OAuth Settings). Tras pasar la verificación con el código, copias el Consumer Key. |
| Custom Domain | En Setup → Domains, copias el dominio administrado. Es el endpoint base de los flujos de login. Si la org es sandbox, agrega el sufijo .sandbox al dominio. |
| Callback URL | La ruta de redirección tras autenticar. Para el simulador: http://localhost:3000/fake/services/oauth/success. Para dispositivos, va en el QR (sección 4). |

Reglas de resolución del callback (útil saberlas): si das el Custom Domain pero omites la Callback URL, la app le concatena /services/oauth2/success al dominio. Si omites ambos, cae por defecto a login.salesforce.com/services/oauth2/success.

## 3. Conectar el simulador

Para que el simulador del Modeler autentique, inyectas el Consumer Key en la propiedad sfConsumerKey del config.json del workspace, y usás la Callback URL del simulador:

```
// $workspace/appl/config/config.json
{ "sfConsumerKey": "<tu Consumer Key>", ... }
 
// Callback URL configurada para el simulador:
//   http://localhost:3000/fake/services/oauth/success
```

Y acuérdate del paso que ya viste en el `03-setup-modeler-git.md`: agregar http://localhost:3000 a la CORS allowed list de la org, o el simulador levanta pero no autentica.

## 4. Aprovisionar dispositivos (QR)

Para los dispositivos físicos, los tres datos (Consumer Key, Custom Domain y Callback URL) convergen en la funcionalidad Connected App QR Code, en la página Mobile Settings de Sync Management. Al ejecutar Generate QR Code, se renderiza un QR que el field rep escanea: la app parsea la URI, inyecta el Consumer Key y el Custom Domain, y queda autenticada sin que el usuario tipee credenciales de red.

## 5. Puntos clave

- El setup completo del org es prerrequisito de admin (fuera de alcance). Lo único que toca al dev es la app de autenticación que da el Consumer Key.

- Desde Spring ’26 se usa la External Client App (reemplaza la Connected App): Setup → External Client Apps → Enable OAuth Settings, con los scopes indicados y los cuatro flags deseleccionados.

- Tres datos: Consumer Key (Manage Consumer Details), Custom Domain (Domains; .sandbox si es sandbox) y Callback URL.

- Simulador: sfConsumerKey en appl/config/config.json, Callback http://localhost:3000/fake/services/oauth/success, y localhost:3000 en el CORS allowed list.

- Dispositivos: Connected App QR Code en Mobile Settings → Generate QR Code; el rep escanea y queda autenticado.
