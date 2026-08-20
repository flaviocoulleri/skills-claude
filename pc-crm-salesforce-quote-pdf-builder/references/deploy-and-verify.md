# Deployar y verificar contra la org (con reintentos)

## Shell: usar PowerShell para `sf`, no Bash

En Windows, el `sf` CLI resuelto vía Git Bash a veces falla con
`"C:\Program" no se reconoce como un comando interno o externo` — es un problema de
resolución de PATH del propio Bash tool, intermitente, **no** un problema de la org. Si ves
ese error exacto, no lo diagnostiques como falla de org: repetí el mismo comando con la
herramienta PowerShell en vez de Bash.

## Error transitorio conocido: `UNKNOWN_EXCEPTION: java.lang.reflect.InvocationTargetException`

Algunas orgs (observado en orgs demo/DevHub compartidas) devuelven este error de forma
intermitente en llamadas a Metadata API y Tooling API — deploys, `org list limits`,
`apex run`, incluso a veces SOQL vía REST. **No es necesariamente que el deploy haya
fallado**: en la mayoría de los casos el deploy/execute sí se aplicó del lado del servidor,
y sólo el polling/response del CLI se cayó.

Protocolo cuando aparece:

1. **No asumas que falló.** El JSON de error trae `"data": {"id": "0Af..."}` (deploy) — ese
   es el Job Id real.
2. Reintentá `sf project deploy report --target-org <org> --job-id <id>` — si también falla
   con el mismo error, no sirve como fuente de verdad todavía.
3. **Verificá con una query SOQL simple y sin relación al deploy** primero, para separar
   "la org está caída de verdad" de "esta llamada puntual falló":
   ```
   sf data query --target-org <org> --query "SELECT Id FROM Organization LIMIT 1"
   ```
   Si esto también falla, esperá ~15-20s y reintentá — es un bache real de la org, no hace
   falta reintentar el deploy todavía.
4. Si la query de sanity check funciona, **verificá el artefacto puntual por
   `LastModifiedDate`** en vez de confiar en el reporte del deploy:
   ```
   sf data query --target-org <org> --query "SELECT Name, LastModifiedDate FROM ApexClass WHERE Name = '<Clase>'"
   sf data query --target-org <org> --query "SELECT Name, LastModifiedDate FROM ApexPage WHERE Name = '<Page>'"
   sf data query --target-org <org> --query "SELECT Name, LastModifiedDate FROM StaticResource WHERE Name = '<Resource>'"
   sf data query --target-org <org> --use-tooling-api --query "SELECT DeveloperName FROM LightningComponentBundle WHERE DeveloperName = '<lwc>'"
   ```
   Si el `LastModifiedDate` es de hace unos segundos/minutos (coincide con el intento de
   deploy), **el deploy sí llegó** — seguí adelante, no reintentes el deploy completo.
5. Sólo si el `LastModifiedDate` es viejo (o el componente no existe), reintentá el deploy.

## No uses loops de `sleep` para esperar — usá Monitor o reintento manual espaciado

Evitá encadenar `sleep` en un loop de Bash como mecanismo de espera (el propio harness lo
bloquea). Si necesitás esperar a que la org se recupere:

- Para una sola espera puntual: reintentá el comando directamente después de unos segundos,
  sin loop.
- Para monitoreo real en background mientras seguís haciendo otra cosa: usá la herramienta
  `Monitor` con un `until` en bash — pero **si el propio `sf` dentro del loop de Bash sufre
  el bug de PATH ("C:\Program") en vez del error real de la org, vas a ver reintentos
  infinitos sin sentido.** En ese caso, cortá el monitor (`TaskStop`) y verificá manual con
  PowerShell — es lo que resolvió el falso bloqueo en la sesión donde se construyó esta skill.

## Dependencia cruzada: el nombre de la clase DAO puede variar entre orgs

Distintas orgs demo pueden tener versiones distintas de la app base — una puede tener
`QuotePdfDAO` y otra sólo una `QuoteDAO` más vieja (sin el prefijo `Pdf`). **Antes de
deployar los archivos generados**, confirmá el nombre real de la clase DAO en la org
destino:

```
sf data query --target-org <org> --query "SELECT Name FROM ApexClass WHERE Name LIKE '%Quote%DAO%'"
```

Usá ese nombre exacto en el placeholder `{{DAO_CLASS_NAME}}` de los templates. Si la org no
tiene ninguna DAO de Quote, hay que deployar primero la `QuotePdfDAO.cls` base (viene del
proyecto de referencia) antes de los archivos nuevos — si no, el deploy falla con
`Variable does not exist: <Clase>DAO` y además falla en cascada la Service, el
PageController y la ApexPage que dependen de ella.

## Orden de deploy recomendado (un solo comando, todos los archivos juntos)

Deployar todo en una sola invocación de `sf project deploy start --source-dir <archivo1> <archivo2> ...`
en vez de una por archivo — la Metadata API resuelve las dependencias cruzadas
(Apex → Apex, Page → Apex, LWC → Apex) en un solo paquete. Deployar de a uno multiplica la
chance de pisar el error transitorio de arriba y complica la verificación.
