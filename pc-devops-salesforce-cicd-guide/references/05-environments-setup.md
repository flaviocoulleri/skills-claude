# 05 · Preparación de ambientes + JWT

> Fuente canónica: Confluence PROCMOD — "Preparación de ambientes y repositorio" (`2082078742`). Habilitar CI/CD en las orgs: certificado, External Client App, usuario técnico, variables Bitbucket y pipeline. Autenticación máquina-a-máquina vía **OAuth 2.0 JWT Bearer**.

Para que un servidor remoto (Bitbucket) pueda leer/escribir componentes en una org, hay que preparar la infraestructura de autenticación.

## 0. Seguridad y comunicación Salesforce ↔ repositorio

- **Proyecto existente** (sandboxes ya creados): crear el Self-Signed Certificate + External Client App **en cada org**.
- **Proyecto nuevo:** crear solo en **Producción** y luego generar los sandboxes (heredan la config).

### Self-Signed Certificate

Local con OpenSSL (clave privada + cert autofirmado, válido 10 años):

```bash
openssl req -x509 -sha256 -nodes -days 3650 -newkey rsa:2048 -keyout server.key -out server.crt
```

Alternativa desde Salesforce: **Setup > Certificate and Key Management > Create Self-Signed Certificate**. Nombre `Bitbucket Integration`, Key Size **4096**. Descargar el `.crt` y generar su versión **base64** para usarla como variable de entorno.

### External Client App (Connected App moderna)

**Setup > App Manager > New External Client App:**

1. Nombre `DevOps`, email de contacto del proyecto y descripción corta.
2. Habilitar configuraciones a nivel de **API**. Callback URL: `http://localhost:8081/callback`.
3. OAuth Scopes: **Full access (`full`)** y **Perform requests at any time (`refresh_token`, `offline_access`)**.
4. En Flow Enablement, activar: **Enable Client Credentials Flow** y **Enable JWT Bearer Flow** (esta última es la que permite cargar el certificado `.crt` del paso anterior).
5. **Create**.
6. Tras crearla: pestaña **Settings > OAuth Settings > Consumer Key And Secret** → obtener el **Consumer Key** (alimenta la variable `SFDX_CONSUMER_KEY`).

### Usuario técnico (service user) para CI/CD

- Crear/asignar un usuario técnico que usarán los pipelines.
- Permisos necesarios (ej. **Modify Metadata**, **API Enabled**; System Administrator o equivalente para deploy de metadata).
- Asociar su perfil/permission set a la External Client App.

## 1. Ambiente productivo (org principal / Dev Hub)

- **Setup > Dev Hub** → activar. Permite administrar Scratch Orgs y source tracking en sandboxes compatibles.

## 2. Sandboxes (dev, test, qa, uat)

Cada sandbox debe poder recibir despliegues automáticos:

- **Usuario técnico:** clonar el perfil/permission set de Productivo y asignarlo al mismo usuario técnico en cada sandbox (permisos de admin para deploy de metadata).
- **External Client App + certificado:** confirmar que están presentes en cada sandbox.

## Variables de entorno en Bitbucket (por org)

Reemplazar `{{ORG_NAME}}` por el prefijo del ambiente (`DEV`, `TEST`, `QA`, `UAT`, `PROD`):

- `{{ORG_NAME}}_SFDX_CLIENT_CERT` — el certificado en **base64**:
  - Linux: `base64 "Bitbucket_Integration(dev).crt" > dev.txt`
  - Windows (PowerShell): `[System.Convert]::ToBase64String([System.IO.File]::ReadAllBytes("Bitbucket_Integration(dev).crt")) | Set-Content "dev.txt"`
- `{{ORG_NAME}}_SFDX_CONSUMER_KEY` — Consumer Key de la External Client App.
- `{{ORG_NAME}}_SFDX_USERNAME` — username del usuario integrador técnico del ambiente.

## 3. Bitbucket (pipeline)

El pipeline lee las credenciales inyectadas, se autentica con **`sf org login jwt`** sin intervención manual, y corre CI/CD (tests + PMD). `bitbucket-pipelines.yml` (extracto real):

```yaml
image: salesforce/cli:2.110.13-full
definitions:
  caches:
    sfdx-share: ~/.local/share/sf
    sfdx-cache: ~/.cache/sf
  steps:
    - step: &run-code-analysis
        name: Run Static Code Analysis
        caches: [sfdx-share, sfdx-cache]
        script:
          - source ./scripts/run-analysis.sh
        artifacts: [analysis-results.sarif]
    - step: &run-apex-tests
        name: Run Apex Tests and Check Coverage
        script:
          - source ./scripts/auth.sh DEV
          - sf apex run test --synchronous --target-org $DEV_SFDX_USERNAME --code-coverage --result-format junit --output-dir test-results
          # chequeo de cobertura vía jq sobre orgWideCoverage
    - step: &validate-dev
        name: Validate against DEV
        script: [source ./scripts/auth.sh DEV, source ./scripts/validate.sh DEV]
    - step: &deploy-to-dev
        name: Deploy to DEV
        trigger: manual
        script: [source ./scripts/auth.sh DEV, source ./scripts/quick-deploy.sh DEV]
    # ... continúa para TEST, QA, UAT, PROD
pipelines:
  pull-requests:
    develop:
      - parallel: [step: *run-code-analysis, step: *run-apex-tests]
    test:
      - step: *validate-test
    # ... configuración modular
```

> ⚠ El snippet del pipeline chequea cobertura `< 90`, pero el **gate oficial es 95%** (ver módulo 07 / página `2082045969`). Ante duda, corregir a 95%.

## Recordatorio post-refresh

Un refresh de sandbox **borra** External Client App, usuario técnico y permission sets de integración → hay que **re-inyectarlos/reactivarlos** (ver módulo 02, Política de refresco). Avisar siempre.
