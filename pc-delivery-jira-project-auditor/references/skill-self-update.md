# Verificación de actualizaciones del skill

Acción meta del PASO 2 que permite al PM saber si está corriendo una versión vieja del skill. **No** es auto-update real — el skill cargado en la sesión es inmutable hasta que el PM reinstale manualmente desde Configuración → Skills. Esta acción detecta el diff y guía la reinstalación.

## Limitación inherente: el skill no puede recargarse a sí mismo

Cuando Cowork instala un .skill, el contenido del SKILL.md y los `references/` se cargan al runtime de la sesión. El modelo opera contra esa snapshot. Recargar requiere:

1. Desinstalar la versión actual (Configuración → Skills → ⋮ → Desinstalar).
2. Instalar el .skill nuevo (Configuración → Skills → "Install skill").
3. Volver al chat — la próxima invocación del skill usa la versión nueva.

El paso 1-2 lo hace el PM manualmente. El skill puede **detectar** que hay versión nueva y **guiar** la reinstalación, pero no ejecutarla.

## Detección de la versión instalada

Trivial: el modelo lee la frontmatter del SKILL.md que tiene cargado en la sesión.

```yaml
metadata:
  version: 1.13.0
  last_modified: 2026-05-04
```

## Detección de la latest publicada

Tres fuentes en orden de preferencia:

### Fuente A (preferida) — Drive folder de releases

PC mantiene una carpeta de releases en Drive con la última versión de cada skill:

```
procontacto-claude/
└── skills-releases/
    ├── pc-delivery-jira-project-auditor/
    │   ├── pc-delivery-jira-project-auditor.skill        ← latest
    │   ├── CHANGELOG.md                                   ← histórico de versiones
    │   └── archived/
    │       ├── pc-delivery-jira-project-auditor-v1.0.0.skill
    │       └── pc-delivery-jira-project-auditor-v1.5.0.skill
    └── ...
```

El skill busca el `.skill` en `procontacto-claude/skills-releases/pc-delivery-jira-project-auditor/` con el nombre exacto del skill (sin sufijo de versión). El `.skill` es un zip — para leer el `metadata.version` del frontmatter sin descargar todo, conviene leer `CHANGELOG.md` que mantiene el equipo de governance con la última versión al inicio.

Procedimiento:

1. `mcp__ebf93048-...__search_files` con `name contains 'pc-delivery-jira-project-auditor.skill'` filtrado al folder de releases.
2. Si no encuentra, fallback a Fuente B.
3. Si encuentra, leer `CHANGELOG.md` del mismo folder (file en Drive, formato markdown) — primera línea de versión es la latest.
4. Comparar la latest con la instalada (semver: si latest > instalada → hay actualización).

### Fuente B (fallback) — Cross-skill con `pc-meta-skill-manager`

Si la carpeta de releases no existe o no es accesible, invocar `pc-meta-skill-manager` que mantiene el catálogo de skills:

```
sendPrompt: "Activa pc-meta-skill-manager y devuélveme la latest version
publicada del skill pc-delivery-jira-project-auditor según tu catálogo.
Sólo informativo — no modificar nada."
```

`pc-meta-skill-manager` corre su `audit_catalog.py` y devuelve metadata. Si el skill aparece, ahí está la latest. Si no aparece (skill aún no catalogado), Fuente C.

### Fuente C (último recurso) — Aviso al PM

Si las dos fuentes anteriores fallan, mostrar widget al PM con:

```
No pude detectar la versión latest publicada — ni la carpeta de releases en
Drive ni el catálogo de pc-meta-skill-manager respondieron.

Tu versión instalada: 1.13.0
Última que conozco: 1.13.0 (la que estoy ejecutando ahora)

Si sospechas que hay versión nueva, pídeselo a Ariel directamente o revisa
el ticket PROCSKILLS-10 en Jira.
```

## Comparación semver

Comparar `instalada` vs `latest`:

- Si `latest == instalada` → "Estás en la última versión".
- Si `latest > instalada` → hay actualización disponible, mostrar diff.
- Si `latest < instalada` → "Estás en una versión más reciente que la publicada (probablemente local-dev). No hace falta actualizar."

Comparación correcta de semver: parsear `MAJOR.MINOR.PATCH` y comparar numéricamente. NO comparar como strings (`"1.10.0" < "1.9.0"` lexicográficamente, lo cual es incorrecto).

## Widget chat-inline cuando hay actualización

Si `latest > instalada`, renderizar widget con:

**Header**:

```
🔔 Hay una versión nueva disponible
Instalada: 1.10.0  →  Latest: 1.13.0
3 versiones intermedias publicadas desde tu instalación.
```

**Changelog acumulado**:

Listar las entradas de changelog de cada versión intermedia (extraídas del CHANGELOG.md o del comment del frontmatter del .skill nuevo). Cada versión como una card colapsable:

```
[ ▼ ] v1.13.0 (2026-05-04) — Acción meta de auto-update
[ ▼ ] v1.12.0 (2026-04-30) — Creación de sprints
[ ▼ ] v1.11.0 (2026-04-30) — Generación de Weekly Status
```

Click en ▼ expande la entrada completa.

**Footer**:

```
[Descargar nueva versión ↗]   [Recordarme después]   [Cerrar]
```

- **"Descargar nueva versión"** → link directo al `.skill` en Drive (Fuente A) con texto guía: "Bájalo, ve a Configuración → Skills, desinstala la versión vieja, instala esta nueva, y vuelve al chat. Cuando estés listo, tipeame `regenerá` y vuelvo a correr el audit con la versión nueva."
- **"Recordarme después"** → cierra el widget sin acción. Si el PM corre otro audit en la misma sesión, NO se vuelve a chequear (cache de 30 min para no spamear).
- **"Cerrar"** → mismo que "Recordarme" pero sin cache (el siguiente audit vuelve a chequear).

## Flow después de la reinstalación

El PM tipea `regenerá` (o algo equivalente: `ok ya reinstalé`, `listo, vuelve a auditar`) en chat:

1. El skill (ahora corriendo la versión nueva) detecta el contexto previo de la sesión: ¿qué proyecto estaba auditando? ¿qué scope?
2. Si la sesión tiene contexto suficiente, dispara el PASO 2 directamente con esos parámetros.
3. Si no, vuelve a PASO 1.1 (selección de PM/proyecto) — el PM elige de nuevo.

**Importante**: el contexto de "qué proyecto estábamos auditando" sobrevive a la reinstalación porque vive en el transcript del chat, no en el código del skill. La nueva versión leyendo el transcript reconstruye el estado.

## Cache de la verificación

Para no consultar Drive cada vez que el PM corre un audit:

- Si la verificación dio "estás en la última" → cachear 24h.
- Si dio "hay actualización pero PM eligió Recordarme después" → cachear 30 min.
- Si dio error en la detección (Fuente C) → cachear 10 min.

El cache vive en la sesión actual del modelo (no persiste entre sesiones del PM).

## Cuándo NO mostrar el botón

- Si Drive MCP no está conectado y `pc-meta-skill-manager` tampoco está instalado → no aparece (sin las dos fuentes, el botón no puede hacer nada útil).
- Si el PM tipea explícitamente "no me ofrezcas updates en esta sesión" → cachear ese opt-out durante la sesión y omitir el botón.

## Bootstrap del registry — primera publicación

El feature de verificación de actualizaciones depende de que exista la carpeta de releases en Drive. La primera vez que se usa el skill en una org, esa carpeta puede no existir todavía. Acción "Publicar esta versión en Drive para activar las actualizaciones ↗" resuelve eso de un saque.

**Cuándo aparece el botón**: sólo si la carpeta `procontacto-claude/skills-releases/pc-delivery-jira-project-auditor/` no existe en Drive cuando el skill arranca. Si ya existe, el botón se omite (no hace falta bootstrap dos veces).

**Qué hace al click** (con OK explícito previo):

1. **Crear la carpeta** `procontacto-claude/skills-releases/` si no existe.
2. **Crear sub-carpeta** `pc-delivery-jira-project-auditor/` adentro.
3. **Subir el `.skill` actualmente instalado** ahí. El skill puede leer el `.skill` desde la ubicación donde fue instalado (Configuración → Skills mantiene el archivo localmente, accesible vía path predecible). Si el path no es accesible, fallback: pedir al PM que arrastre el `.skill` que tiene en su Downloads.
4. **Generar `CHANGELOG.md`** con el contenido del comment `<!-- Changelog ... -->` del frontmatter del SKILL.md, formateado como markdown legible.

**Preview antes de escribir** (regla del skill — nada se escribe sin OK):

Widget chat-inline mostrando:

```
Voy a hacer 3 cosas en Drive:

1. Crear carpeta:    procontacto-claude/skills-releases/pc-delivery-jira-project-auditor/
2. Subir archivo:    pc-delivery-jira-project-auditor.skill (versión 1.13.1, 58 KB)
3. Generar archivo:  CHANGELOG.md (con las 14 entradas del changelog actual)

Después de esto, el botón "Verificar actualizaciones del skill" va a poder
comparar versiones contra esta carpeta de Drive.

[Confirmar y publicar ↗]   [Cancelar ↗]
```

**Después del bootstrap**, mostrar en chat:

```
✅ Sistema de actualizaciones activado.

Carpeta creada: <link a Drive>
Archivo .skill subido (v1.13.1)
CHANGELOG.md generado con histórico de versiones

A partir de ahora, cada versión nueva se publica acá. El botón
"Verificar actualizaciones del skill" del PASO 2 ya puede chequear si hay
versiones más nuevas comparando contra esta carpeta.
```

**Si la carpeta ya existía** (el PM tocó el botón sin necesidad), el skill detecta y dice:

```
⚠ La carpeta de releases ya existía con este contenido:

  • pc-delivery-jira-project-auditor.skill (v1.12.0, subida 2026-04-30)
  • CHANGELOG.md

Tu versión actual es la 1.13.1 (más nueva que la publicada).
¿Quieres agregar la 1.13.1 al registry?

[Sí, agregar 1.13.1 ↗]   [No, dejar como está ↗]
```

Si elige "agregar", sube el `.skill` actual con sufijo de versión (`pc-delivery-jira-project-auditor-v1.13.1.skill`) y mueve el viejo a `archived/`. Actualiza el CHANGELOG con la nueva entrada.

## Restricciones

- **Nunca** intentar reinstalarse automáticamente — incluso si el MCP de Cowork expusiera tools para instalar/desinstalar skills (que hoy no expone), la reinstalación cambia el código del skill cargado en la sesión, lo que puede dejar el modelo en estado inconsistente.
- **Nunca** sugerir versiones beta o pre-release — sólo versiones formalmente publicadas en la carpeta de releases.
- **Nunca** descargar el `.skill` automáticamente al disco del PM — sólo proveer link para que el PM decida cuándo descargar.
- **Nunca** sobrescribir un `.skill` existente en el registry — siempre archivar el viejo en `archived/` antes de subir el nuevo.
