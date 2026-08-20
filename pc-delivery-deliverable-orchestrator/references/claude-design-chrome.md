# Crear proyectos de Claude Design vía Claude-in-Chrome

> **DEPRECADO para este skill (v1.1.0).** Los artefactos visuales (wireframes, AS-IS, TO-BE, ERD,
> integraciones) ya **no** se crean como proyectos de Claude Design: se materializan como **artefactos
> de Cowork** (`claude.ai/code/artifact/<uuid>`), producidos por el skill de cada artefacto. Este
> archivo se conserva solo como referencia histórica de la mecánica Claude-in-Chrome.

Claude Design (`claude.ai/design`) **no tiene API ni MCP**. Se opera con **Claude-in-Chrome**
(`mcp__claude-in-chrome__*`) sobre la sesión ya logueada del usuario. Si no hay sesión / Chrome no está
disponible → **fallback semi-automático** (ver abajo). Nunca inventar ni suponer una URL de Design.

## Precondición

- Cargar las tools con ToolSearch:
  `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__find,mcp__claude-in-chrome__tabs_create_mcp`
- Verificar sesión: navegar a `claude.ai/design` y `read_page`. Si aparece login / no hay sesión →
  **no intentar loguear** (prohibido ingresar credenciales) → pasar al fallback.

## Receta (por cada artefacto visual confirmado)

1. `navigate` a `https://claude.ai/design`.
2. `read_page` / `find` el control de **nuevo proyecto** ("New project" / "Nuevo proyecto" / "+").
   No adivinar selectores: localizar por texto con `find` y usar el `ref`.
3. `computer` click en crear nuevo proyecto.
4. Nombrar el proyecto: `{Proyecto} · {Artefacto}` (ej. `Colombina · Wireframes v2`).
   Escribir el nombre en el campo correspondiente (`form_input` o `computer type`).
5. **Confirmar la creación** (respetar la regla 2 del SKILL: mostrar al usuario qué se va a crear antes,
   si el flujo lo permite; como mínimo confirmar el batch de proyectos Design antes de empezar el PASO 3).
6. **Capturar la URL real** del proyecto desde la barra de direcciones tras crearlo
   (`claude.ai/design/p/<uuid>`). Leerla del page/URL, NO construirla a mano.
7. Verificar que la URL responde (`read_page` del proyecto recién creado) antes de darla por buena.

## Fallback semi-automático (obligatorio si Chrome falla)

Si no se pudo crear el proyecto (sin sesión, Chrome no disponible, UI no navegable):

1. **No fallar en duro.** Crear igual el issue `Artifact` en Jira (PASO 4) con la descripción marcando
   *"Pendiente: crear el proyecto en `claude.ai/design`, nombre sugerido `{Proyecto} · {Artefacto}`, y
   pegar el link acá."*
2. En el resumen final (PASO 6), listar estos artefactos bajo **"Pendientes de acción del DM"** con el
   nombre sugerido, para que los cree a mano y luego use `pc-delivery-blueprint-guide` (Modo D) o edite
   el `Artifact` para pegar el link.

## Registro

- La URL de Claude Design se guarda en la **descripción del `Artifact` de Jira** (fuente de trazabilidad).
- **No** registrar como `Project_Asset__c` salvo que exista un valor de picklist válido en `Type__c`
  para Claude Design (verificar con `getObjectSchema`; hoy no existe — `ClaudeProjectId` es el Claude
  *Project* de chat, NO Claude Design). Ver regla 7 del SKILL.
