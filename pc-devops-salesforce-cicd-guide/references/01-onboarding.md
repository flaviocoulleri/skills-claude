# 01 · Onboarding local

> Fuente canónica: Confluence PROCMOD — "Guía de Onboarding" (`2081751044`). Setup de la máquina del dev para sumarse al flujo CI/CD.

Condensa el paso a paso exacto para configurar la máquina y sumarse al flujo de CI/CD del proyecto.

## 1. Requisitos del sistema

Antes de tocar código, instalar a nivel global en el OS:

- **Git** — control de versiones.
- **Node.js v20+ y npm** — requerido para las validaciones locales, el linter y **Husky**.
- **Salesforce CLI (`sf`)** — para interactuar con las orgs. Verificar con `sf --version`.
- **JRE/JDK 11+ (Java)** — requerido localmente porque **Salesforce Code Analyzer (PMD)** lo usa por detrás.
- **Visual Studio Code** — el IDE. Instalar el **Salesforce Extension Pack**.

## 2. Clonado y preparación

```bash
git clone https://TU_USER@bitbucket.org/procontacto/NOMBRE_DEL_REPO.git
cd NOMBRE_DEL_REPO
```

**Paso crítico — instalar dependencias:**

```bash
npm install
```

`npm install` es **obligatorio**: instala **Husky, ESLint y Prettier**. Si no se corre, los hooks de validación local no funcionan y los PRs fallan en la nube.

## 3. Autorización contra Salesforce

Autorizar dos entornos: el **Dev Hub** (para Scratch Orgs si aplican) y tu **Sandbox de desarrollo** individual o compartido.

```bash
# Autorizar Dev Hub (alias: Hub)
sf org login web -a Hub -d

# Autorizar tu Sandbox personal (alias: MiDev)
sf org login web -a MiDev -s -r https://test.salesforce.com
```

> `sf org login web` es un comando **write** (abre browser y escribe credenciales locales) → pedir ✅ antes de correrlo.

## 4. Probando la instalación

```bash
# El linter del proyecto:
npm run lint

# Que Husky intercepte los commits (commit vacío de prueba):
git commit -m "test: onboarding commit" --allow-empty
```

Si `lint-staged` comprueba los archivos, el entorno está listo para programar.

## Errores comunes

- **Saltear `npm install`** → los hooks de Husky no corren localmente y el PR falla en la nube. Siempre correrlo post-clone.
- **No tener Java** → Code Analyzer (PMD) falla silenciosamente en local.
- Confundir el `-r` del login: la instancia de sandbox es `https://test.salesforce.com`.
