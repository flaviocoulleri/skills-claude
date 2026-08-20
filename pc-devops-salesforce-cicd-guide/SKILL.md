---
name: pc-devops-salesforce-cicd-guide
metadata:
  version: 1.2.0
  last_modified: 2026-07-02
  source: https://procontacto.atlassian.net/wiki/spaces/PROCMOD/pages/2073329674
  host: claude-code-only
  escalation_channel: C0B3UQ86VRT
  escalation_user: U03MYU8SHD3
description: >
  Guía paso a paso para Salesforce Devs, Admins y Tech Leads de ProContacto
  que trabajan repos Bitbucket con CI/CD Salesforce (Confluence 2073329674).
  SOLO Claude Code — declina si detecta Cowork. Ejecuta read-only (git
  status/diff, sf retrieve preview, validate, code-analyzer) y pide ✅ antes
  de write (commit, push, deploy, destructive, back-merge). Si el usuario
  queda trabado, escala automáticamente a Ezequiel Veliz por Slack. Cubre
  onboarding, ambientes dev/test/qa/uat/main, Conventional Commits, flujo
  diario, JWT + External Client App, Permission Sets exclusivos, Quality Gates
  (≥95%), sfdx-git-delta, destructiveChanges, conflictos, hotfix + back-merge,
  rollback y metadata SF. Activar con "cómo arranco con el repo", "crear rama",
  "armar el PR", "tengo un hotfix en prod", "back-merge", "rollback", "eliminar
  campo", "tengo conflictos", "falla el quality gate", "qué es SGD", "JWT no
  anda", "pásame con Eze", "estoy trabado". Funciona en español e inglés.
---

# pc-devops-salesforce-cicd-guide — Guía interactiva de CI/CD Salesforce + Bitbucket

Esta skill es el manual operativo de ProContacto para trabajar contra los repos de Bitbucket que orquestan los proyectos Salesforce. Replica fielmente la documentación oficial publicada en Confluence (página `2073329674` — "Índice de Documentación CI/CD") y la sirve de forma guiada, adaptada al seniority del usuario y con ejecución híbrida (read-only se corre, write se confirma).

## 🚨 Restricción de host — SOLO Claude Code

Este skill **no funciona en Cowork**. Antes de cualquier otra acción, hacer el check de host:

**Señales de Cowork (si está cualquiera, declinar):**

- Presencia de tools `mcp__cowork__*` (`create_artifact`, `request_cowork_directory`, `present_files`, `allow_cowork_file_delete`, `list_artifacts`, `read_widget_context`).
- Presencia de `mcp__workspace__bash` (el bash sandbox de Cowork).
- Presencia de `mcp__visualize__show_widget`.
- Presencia de `mcp__cowork-onboarding__*`.
- Working directory bajo `/Users/.../Library/Application Support/Claude/local-agent-mode-sessions/...`.

**Señales de Claude Code (todas o casi todas presentes — proceder):**

- `Bash` (no `mcp__workspace__bash`).
- `BashOutput`, `KillShell`.
- Working directory es un repo Git local del dev (ej: `~/dev/<repo>`).
- No están los `mcp__cowork__*`.

**Si se detecta Cowork → responder textualmente:**

```
Este skill (pc-devops-salesforce-cicd-guide) está pensado para ejecutarse
desde Claude Code, no desde Cowork. El flujo asume acceso directo al repo
Git local, sf CLI, y hooks de Husky — herramientas que viven en el shell
del dev.

Para usarlo:
1. Abre Claude Code en tu terminal, dentro del repo del proyecto.
2. Invoca el mismo skill ahí.

Si necesitas ayuda con CI/CD desde Cowork (sin tocar el repo directamente),
abre un mensaje en #05-ayuda o usa pc-meta-cowork-helprequest-orchestrator
para escalar a un dev.
```

No realizar ninguna otra acción. No proponer comandos. Salir limpio.

## 🆘 Escalación automática a Ezequiel Veliz

Cuando el usuario queda trabado, este skill **envía un DM automático** (sin pedir ✅) al canal Slack del equipo arrobando a Eze. Detalle completo en `references/13-escalation-to-eze.md`.

### Excepción a la regla global de confirmación previa

ProContacto exige ✅ antes de cualquier acción Slack. **Este skill tiene una excepción autorizada por Ariel** para los mensajes de escalación, porque:
- Destinatario fijo, contenido factual, alta frecuencia → la fricción del ✅ derrota el propósito.
- La excepción aplica **solamente** a la escalación a Ezequiel — cualquier otra acción Slack del skill sigue la regla normal.

### Cuándo escalar (4 triggers)

1. **Mismo comando falla 2+ veces** sobre el mismo target.
2. **Usuario lo dice explícito**: "estoy trabado", "no me funciona", "no sé seguir", "I'm stuck".
3. **Errores específicos del pipeline / SF**: `INVALID_SESSION_ID`, `Malformed XML`, governor limits recurrentes, `OAUTH_APPROVAL_ERROR_GENERIC`, `Code coverage <95%` irresoluble, conflictos masivos en `package.xml`.
4. **Pedido directo**: "pásame con Eze", "avísale al referente CI/CD".

### Cómo escalar

Llamar a `mcp__85095b11-725f-49b4-bd0c-062c7d4bcfb9__slack_send_message` con:

- `channel`: `C0B3UQ86VRT`
- `text`: arrobar a `<@U03MYU8SHD3>` + plantilla de `references/13-escalation-to-eze.md` (rol, repo, rama, qué intentaba, qué falló, qué se intentó, trigger).

Antes de armar el cuerpo, **redactar secrets** (JWTs, consumer keys, session IDs `00D...`, tokens en URLs).

Después de enviar, decirle al usuario que avisó a Eze y proponer un Plan B mientras espera.

## Audiencia

Tres roles, todos cubiertos:

- **Salesforce Developers** — quienes tocan Apex/LWC/Flows y trabajan ramas `feature/PROC-XYZ`.
- **Salesforce Admins** — quienes hacen cambios declarativos y deben coordinar con un dev para versionarlos.
- **Tech Leads / Release Managers** — quienes manejan merges a `main`, releases, hotfixes y rollbacks.

## Política de ejecución

**Híbrida por tipo de comando**. Se aplica sin excepción:

- **Read-only se ejecuta sin pedir permiso**: `git status`, `git fetch`, `git log`, `git diff`, `git branch`, `sf org list`, `sf project retrieve preview`, `sf project deploy validate --dry-run`, `sf code-analyzer run`, `sf apex run test` (cuando es modo report).
- **Write requiere ✅ explícito antes de cada ejecución**: `git commit`, `git push`, `git checkout -b` (crea rama nueva), `git merge`, `git rebase`, `git revert`, `sf project retrieve start`, `sf project deploy start`, `sf project deploy validate` (en orgs superiores), `sf org login`, cualquier comando que escriba en una org.

Esta regla es bloqueante (regla de memoria de Ariel — confirmación previa obligatoria).

## Pre-flight obligatorio

Antes de cualquier acción guiada, recolectar y guardar en contexto:

1. **Rol del usuario**: Developer / Admin / Tech Lead. Si no está claro, preguntar con `AskUserQuestion`.
2. **Seniority**: Junior (≤1 año en SF DX/CI-CD) / Mid (1-3 años) / Senior (3+). Junior recibe explicaciones extra; Senior recibe sólo comandos.
3. **Proyecto / repo**: ruta absoluta al working copy local. Sin esto no se puede ejecutar nada local.
4. **Org alias activos**: correr `sf org list` (read-only, ejecutar sin permiso) y confirmar qué orgs están autenticadas.
5. **Rama actual y estado**: `git -C <repo> status` (read-only).

Persistir esta info para no preguntar dos veces dentro de la misma sesión.

## Las 12 capacidades (módulos)

Cada módulo tiene su propio archivo en `references/`. Cargarlo sólo cuando el usuario entre en ese flujo — no leerlos todos por adelantado.

| # | Módulo | Archivo | Cuándo invocarlo |
|---|---|---|---|
| 1 | Onboarding local | `references/01-onboarding.md` | "cómo arranco", "configurar mi máquina", primer día en el proyecto |
| 2 | Ambientes y mapping orgs↔ramas | `references/02-environments-and-branches.md` | "qué ambientes hay", "qué rama corresponde a qa", duda sobre dev/test/qa/uat/main |
| 3 | Convenciones de ramas y commits | `references/03-branch-and-commit-conventions.md` | "cómo nombro la rama", "el commit me da error", PR rechazado por hook |
| 4 | Flujo diario de dev | `references/04-daily-workflow.md` | "voy a empezar una tarea", "cómo subo este cambio", "armar el PR" |
| 5 | Preparación de ambientes + JWT | `references/05-environments-setup.md` | "configurar External Client App", "JWT no anda", proyecto nuevo, sandbox refrescado |
| 6 | Permission Sets exclusivos | `references/06-permission-sets.md` | "qué pasa con los Profiles", "cómo doy FLS", "permission set vs profile" |
| 7 | Quality Gates | `references/07-quality-gates.md` | "falla el pipeline", "cobertura baja", "Code Analyzer me marca un issue" |
| 8 | sfdx-git-delta (SGD) | `references/08-sfdx-git-delta.md` | "qué es SGD", "por qué el deploy tarda tanto", "el pipeline sólo despliega lo cambiado" |
| 9 | destructiveChanges | `references/09-destructive-changes.md` | "cómo borro un campo del repo", "destructiveChanges.xml", "eliminar metadata" |
| 10 | Conflictos de merge | `references/10-conflicts.md` | "tengo conflictos", "VSCode me muestra <<<<<<<", "PR no mergea" |
| 11 | Hotfix + back-merge | `references/11-hotfix-and-backmerge.md` | "bug crítico en prod", "necesito un hotfix", "back-merge" |
| 12 | Rollback + post-deploy | `references/12-rollback-and-postdeploy.md` | "rollback", "deshacer el deploy", "tareas manuales después del deploy" |
| 13 | Escalación a Ezequiel Veliz | `references/13-escalation-to-eze.md` | usuario trabado, error recurrente, "pásame con Eze", "ping al referente" |

Adicional — referencia de metadata de Salesforce (qué archivo se genera al hacer cada acción en SF):

| Anexo | Archivo | Cuándo invocarlo |
|---|---|---|
| A | Referencia de metadata SF (16 secciones) | `references/A-metadata-reference.md` | "qué metadata tira un Flow", "cómo extraigo un Permission Set", "ruta SFDX de un Record Type" |

## Workflow maestro

Cuando se activa el skill, seguir este árbol de decisión:

```
0. Pre-flight de host (¿estoy en Claude Code? — ver sección "Restricción de host")
   ├── Cowork detectado → DECLINAR con mensaje fijo, salir
   └── Claude Code → continuar
                ↓
1. Pre-flight (rol + seniority + repo + orgs + rama) — usar AskUserQuestion sólo
   para lo que falte
                ↓
2. ¿Qué quiere hacer el usuario?
   ├── "Es mi primer día" / "configurar máquina"
   │     → Módulo 1 (onboarding) → opcionalmente Módulo 2 (orientación)
   │
   ├── "Voy a empezar una tarea" (feature/bugfix/chore)
   │     → Módulo 3 (convenciones) → Módulo 4 (flujo diario)
   │     → Si toca metadata declarativa: subsección "cambios no programáticos"
   │     → Si elimina algo: Módulo 9
   │     → Si toca permisos: Módulo 6
   │
   ├── "El PR falla / quality gate / pipeline rojo"
   │     → Módulo 7 (quality gates)
   │     → Si es timing del deploy: Módulo 8 (SGD)
   │     → Si es conflicto: Módulo 10
   │
   ├── "Bug crítico en prod"
   │     → Módulo 11 (hotfix + back-merge)
   │
   ├── "Necesito deshacer un deploy"
   │     → Módulo 12 (rollback)
   │
   ├── "Configurar / refrescar un ambiente"
   │     → Módulo 5 (JWT + External Client App + variables)
   │
   └── "Qué metadata tira tal acción de SF" / "cómo extraigo X"
         → Anexo A (referencia metadata)
                ↓
3. Para CADA comando a ejecutar:
   - read-only → ejecutar directo
   - write → mostrar comando + propósito + pedir ✅ explícito → ejecutar
   - Si falla 2 veces seguidas o el usuario dice "estoy trabado" → Módulo 13
                ↓
4. Monitor permanente: cualquier trigger del Módulo 13 dispara escalación
   automática a Ezequiel Veliz sin pedir ✅ (excepción autorizada).
                ↓
5. Al cerrar el módulo, recordar al usuario qué viene después (ej: después de
   crear la rama, recordar conventional commits; después de pushear, recordar
   abrir PR contra develop).
```

## Adaptación por seniority

| Seniority | Estilo de respuesta |
|---|---|
| **Junior** | Explicar el "por qué" antes del comando. Ofrecer alternativas visuales (Org Browser, Source Control de VSCode). Mencionar errores comunes. Pedir confirmación incluso en read-only la primera vez de cada tipo. |
| **Mid** | Comando + 1-2 líneas de contexto. Mostrar el resultado esperado. Saltear basics. |
| **Senior** | Sólo comando. Asumir conocimiento. Si el usuario pide explicación, expandir. |

Si el rol del usuario no está claro al inicio, asumir **Mid** y ajustar según señales.

## Reglas inflexibles

1. **Nunca commit/push/deploy sin ✅ explícito**. La memoria global de Ariel lo exige; este skill lo aplica también para el resto del equipo.
2. **Nunca proponer flujos contra `master`/`main` directos**. Toda promoción es vía PR.
3. **Nunca tocar Profiles para FLS de features nuevos**. La política es Permission Sets exclusivos (ver Módulo 6). Si el usuario insiste, advertir y citar la página `2082209816`.
4. **Conventional Commits es obligatorio**. Si el mensaje propuesto no cumple, regenerarlo. El blocklist es: "fix", "update", "WIP", "asdf", textos libres sin prefijo.
5. **Cobertura mínima 95%** (no 90 — la doc oficial dice 95%). Si el usuario menciona 90, corregir y citar la página `2082045969`.
6. **Refrescar Sandbox = re-inyectar config CI/CD**. Después de un refresh, el sandbox pierde External Client App, usuario técnico, permission sets. Avisar siempre.
7. **Back-merge después de hotfix es obligatorio**. No es opcional. Si el usuario dice "ya está, hicimos el hotfix", recordar back-merge a `develop`, `test`, `qa`, `uat`.

## Comandos read-only que siempre se pueden correr

Lista exhaustiva para no andar dudando:

```
git status
git branch -a
git log --oneline -20
git diff
git fetch origin
git remote -v
sf --version
sf org list
sf org display --target-org <alias>
sf project retrieve preview --target-org <alias>
sf project deploy validate --target-org <alias> --source-dir <dir> --dry-run
sf code-analyzer run --rule-selector Recommended
sf org list metadata-types --target-org <alias>
sf org list metadata --metadata-type <Type> --target-org <alias>
npm run lint  (cuando ya esté instalado)
```

## Comandos write que SIEMPRE requieren ✅

```
git commit
git push
git checkout -b <branch>
git merge
git rebase
git revert
git reset
git cherry-pick
sf org login <flujo>
sf project retrieve start
sf project deploy start
sf project deploy validate (contra orgs superiores — no dry-run)
sf apex run test (cuando escribe en org compartido)
```

## Salidas que el skill puede generar

- **Plan textual de pasos** (siempre).
- **Mensaje de commit Conventional Commits** propuesto a partir del diff.
- **Nombre de rama** propuesto a partir de un ticket Jira.
- **Diff resumen** (al usar `git diff`).
- **Lista de archivos de metadata afectados** (al usar SGD localmente).
- **Reporte de quality gates** (al correr coverage + Code Analyzer).
- **Borrador de descripción de PR** estructurado (qué cambia, por qué, cómo testear, ticket Jira).

## Integración con otros skills de ProContacto

- **pc-crm-salesforce-dev-guide** — para preguntas sobre cómo escribir el código Apex/LWC en sí (no cómo subirlo). Si el usuario pregunta "cómo manejo governor limits", invocar ese skill, no este.
- **pc-crm-salesforce-lwc-builder** — para scaffold de LWC nuevos. Después, este skill toma la posta para commit/push/PR.
- **pc-delivery-bb-commit-reporter** — si el usuario quiere VER quién commitió qué (read-only retrospectivo), delegar a ese skill.
- **pc-meta-cowork-helprequest-orchestrator** — si un comando falla por permisos/conectores y el usuario queda trabado, ofrecer escalación via ese skill.

## Estructura del skill

```
pc-devops-salesforce-cicd-guide/
├── SKILL.md                                  ← este archivo
├── references/
│   ├── 01-onboarding.md                      ← setup local (git, node, sf, java, vscode)
│   ├── 02-environments-and-branches.md       ← dev/test/qa/uat/main + política de refresh
│   ├── 03-branch-and-commit-conventions.md   ← Conventional Commits + naming
│   ├── 04-daily-workflow.md                  ← flujo programático + declarativo
│   ├── 05-environments-setup.md              ← JWT, External Client App, variables Bitbucket
│   ├── 06-permission-sets.md                 ← Permission Sets exclusivos, .forceignore
│   ├── 07-quality-gates.md                   ← cobertura 95%, Code Analyzer, severidades
│   ├── 08-sfdx-git-delta.md                  ← SGD: deltas, LWC bundles
│   ├── 09-destructive-changes.md             ← eliminación automática vía SGD
│   ├── 10-conflicts.md                       ← XMLs, layouts, package.xml, VSCode merge editor
│   ├── 11-hotfix-and-backmerge.md            ← hotfix desde main + back-merge obligatorio
│   ├── 12-rollback-and-postdeploy.md         ← revert, destructiveChanges, post-deploy en Jira
│   ├── 13-escalation-to-eze.md               ← escalación auto a Ezequiel Veliz (canal C0B3UQ86VRT)
│   └── A-metadata-reference.md               ← referencia completa de metadata SF (16 secciones)
└── scripts/
    ├── check-env.sh                          ← valida prerequisitos locales
    ├── propose-branch-name.sh                ← genera nombre de rama desde ticket Jira
    └── validate-commit-msg.sh                ← chequea Conventional Commits

```

## Versión y fuente

- **Versión**: 1.1.0
- **Última modificación**: 2026-05-14
- **Fuente canónica**: Confluence space PROCMOD, página raíz `2073329674` ("Índice de Documentación CI/CD")
- **Owner**: Ariel Tarsitano
- **Referente CI/CD**: Ezequiel Veliz (`U03MYU8SHD3`) — destinatario de escalación
- **Host permitido**: Claude Code solamente

### Changelog

- **1.2.0** (2026-07-02) — Creados los 14 archivos de `references/` (01–13 + A) y los 3 `scripts/` (check-env, propose-branch-name, validate-commit-msg) que el SKILL.md referenciaba pero no existían. Contenido transcrito fielmente desde las 15 páginas hijas de Confluence `2073329674`, incluida la **referencia de metadata completa (Anexo A, 16 secciones)** de la página `2084012041`.
- **1.1.0** (2026-05-14) — Agregado: pre-flight de host (Claude Code only, declina en Cowork), escalación automática a Ezequiel Veliz vía Slack canal `C0B3UQ86VRT` con excepción autorizada a la regla de confirmación previa.
- **1.0.0** (2026-05-14) — Versión inicial. 12 módulos + anexo de referencia metadata SF basados en Confluence space PROCMOD.

Si la página de Confluence cambia, este skill puede quedar desincronizado. Cualquier reviewer debe re-leer las 15 páginas hijas y bumpear versión.
