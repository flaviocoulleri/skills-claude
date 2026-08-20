---
name: pc-meta-conversation-to-slidedeck
metadata:
  version: 1.1.0
  last_modified: 2026-08-07
description: >
  Convierte la conversación actual en un prompt estructurado listo para pegar
  en Claude Design y generar una presentación en modalidad slide deck. Activar
  SIEMPRE que el usuario diga "ármame una presentación de esto", "convertí esta
  conversación en slides", "genera un prompt para Claude Design", "quiero un deck
  de esta conversación", "haz una presentación con lo que hablamos", "pasa esto
  a slides", "haz un deck", "quiero presentar esto", "ármame el deck", "genera
  el prompt para el deck", "quiero mostrar esto en slides", "hazme un powerpoint
  de esto". También activar proactivamente cuando la conversación contiene
  decisiones importantes, análisis, planes, resultados o cualquier contenido que
  tenga valor ser presentado visualmente, incluso si el usuario no lo menciona
  explícitamente. ES/EN.
---

# pc-meta-conversation-to-slidedeck

## Para qué existe este skill

Muchas conversaciones con Claude terminan con insights valiosos, decisiones documentadas, análisis completos o planes de acción — y esa información queda enterrada en el chat. Este skill toma ese contenido y genera un **prompt optimizado** para que el usuario lo lleve a Claude Design y obtenga una presentación profesional en minutos.

El skill no genera el PPTX directamente. Genera el **prompt** que el usuario lleva a Claude Design. Esa separación es intencional: Claude Design tiene el design system de ProContacto incorporado y es el mejor lugar para iterar el visual slide por slide.

## Flujo de trabajo

### Paso 1 — Leer la conversación

Intenta obtener el transcript completo de la sesión actual usando las tools de `session_info` (primero `list_sessions` para el ID, luego `read_transcript`).

Si esas tools no están disponibles o fallan, continúa igual — tienes acceso al contexto de la conversación directamente. Trabaja desde los mensajes visibles en el contexto.

### Paso 2 — Analizar y extraer el contenido

Procesa el transcript/contexto y extrae estos elementos:

- **Tema principal**: una oración que capture de qué trata la conversación.
- **Puntos clave**: los 3-7 bloques de contenido más importantes — decisiones, hallazgos, planes, datos, conclusiones.
- **Tipo de contenido**: ¿análisis? ¿propuesta? ¿plan de trabajo? ¿resultados? ¿decisión técnica? ¿investigación? Elige el que mejor describe el núcleo.
- **Audiencia inferida**: ¿a quién parece estar dirigido el contenido? (ejecutivos, equipo técnico, cliente, equipo interno)
- **Idioma dominante**: español o inglés.
- **Título sugerido**: un título claro y específico para la presentación, derivado del contenido.
- **Estructura propuesta**: lista tentativa de 6-10 slides basada en la narrativa natural del contenido.

La calidad de este análisis determina la calidad del prompt final. Tómate el tiempo para hacerlo bien.

### Paso 3 — Mostrar widget con opciones

Muestra un widget interactivo usando `mcp__visualize__show_widget`. El widget cumple dos funciones: confirmar que tu análisis fue correcto, y darle al usuario control sobre la presentación antes de que generes el prompt.

El widget debe incluir:

- **Tema detectado**: mostrado como título informativo (no editable), para que el usuario confirme que entendiste bien la conversación.
- **Opciones ajustables** con tus inferencias pre-seleccionadas como valores por defecto:
  - Audiencia: Ejecutivos / Equipo técnico / Cliente externo / Equipo interno
  - Tono: Formal / Profesional cercano / Didáctico
  - Cantidad de slides: 5-8 / 10-15 / 20+
  - Idioma: Español / Inglés
  - Propósito: Informar / Proponer o vender / Reportar avance / Capacitar
- **Estructura propuesta**: la lista de slides sugeridos, para que el usuario vea la narrativa antes de confirmar.
- **Botón "Generar prompt"** que llame a `sendPrompt()` con las opciones seleccionadas en un formato parseable:

```
Generar prompt con: audiencia=[AUDIENCIA], tono=[TONO], slides=[CANTIDAD], idioma=[IDIOMA], propósito=[PROPÓSITO]
```

Pre-llenas todas las opciones con tus inferencias del Paso 2. El objetivo es que el usuario haga clic en "Generar" sin necesidad de cambiar nada — si tus inferencias son buenas, el default debería estar bien.

**Diseño del widget**: usa botones de selección visual (tipo pill/chip), no dropdowns. La estructura propuesta puede ir en una lista compacta debajo de las opciones. El widget debe verse limpio y poder usarse con 1-2 clicks.

### Paso 4 — Generar el prompt para Claude Design

Cuando el usuario confirme las opciones (via el widget o directamente en chat), construye el prompt con esta estructura exacta:

```
# Generar presentación: [TÍTULO]

## Configuración de la presentación
- Audiencia: [AUDIENCIA]
- Tono: [TONO]
- Cantidad de slides: [CANTIDAD]
- Idioma: [IDIOMA]
- Propósito: [PROPÓSITO]

## Contenido fuente

[RESUMEN ESTRUCTURADO — ver reglas abajo]

## Estructura de slides propuesta

1. [Nombre slide] — [mensaje principal de este slide, 1 línea]
2. [Nombre slide] — [mensaje principal de este slide, 1 línea]
...

## Sobre el diseño visual
NO apliques reglas de diseño desde este prompt. NO definas colores, tipografía,
slogans institucionales, layouts ni co-branding. Claude Design tiene el design
system de ProContacto cargado por configuración y lo aplica solo. Limita el
contenido a qué dice cada slide y cuál es el mensaje clave de cada uno.

## Output esperado
Genera la presentación completa en modalidad slide deck. Una sección por cada
slide de la estructura propuesta. Incluye un slide de portada al inicio y un
slide de cierre o próximos pasos al final si aplica al propósito.

## Principios de diseño de contenido
- Cada slide tiene un solo mensaje principal.
- Prioriza listas cortas, datos y visualizaciones sobre párrafos de texto.
- Mantén coherencia narrativa: cada slide lleva al siguiente.
- No repitas información cubierta en slides anteriores.
- Mantén el tono consistente con la audiencia indicada.
```

### Paso 5 — Entregar el prompt

Muestra el prompt completo en chat dentro de un bloque de código (para copiar con un click) y dile al usuario:

> Listo. Copia este prompt y pégalo en Claude Design (o en una nueva sesión de Claude). Va a generar la presentación con la estructura propuesta y el tono que elegiste. Si quieres ajustar algún slide puntual, puedes hacerlo directamente en Claude Design.

No envíes el prompt como archivo. El usuario lo copia del bloque de código — ese flow es el más rápido.

---

## Reglas para el resumen de contenido

El campo "Contenido fuente" del prompt es la pieza más importante. No es una transcripción — es una destilación que permite que Claude Design genere la presentación sin acceso a la conversación original. Sigue estas reglas:

**Incluir:**
- El contexto de fondo necesario para entender el tema (1-3 oraciones).
- Los puntos clave, numerados o en bullets claros.
- Las decisiones tomadas, explicitadas como tales ("Se decidió X porque Y").
- Los datos, números, fechas, nombres propios — sin generalizar.
- Los action items o próximos pasos si los hay.
- El vocabulario del dominio (si la conversación habla de Salesforce, preserva esos términos; si habla de finanzas, usa el lenguaje financiero).

**Excluir:**
- La mecánica de la conversación ("el usuario preguntó", "Claude respondió").
- Contenido repetido o reformulado varias veces en la conversación — quedarte con la versión más clara.
- Tangentes o hilos que no aportan al tema central.

**Longitud:** tan largo como necesario para que la presentación sea autosuficiente, pero sin padding. Típicamente 150-400 palabras.

---

## Casos especiales

**Conversación muy corta (menos de 5 mensajes sustantivos):** El contenido puede no ser suficiente para una presentación completa. Dile honestamente al usuario y pregúntale si quiere agregar contexto antes de generar el prompt.

**Múltiples temas en la misma conversación:** Identifica el hilo principal y construye la presentación alrededor de ese. Si hay subtemas relevantes, consideralos como slides separados dentro de la estructura.

**Conversación técnica con código o configs:** El resumen debe capturar el *qué* y el *por qué* de las decisiones técnicas, no el código en sí. El código puede ir como referencia en el último slide si aporta valor a la audiencia.

**Conversación ya estructurada (un plan, un análisis, un reporte):** La estructura propuesta puede seguir de cerca la estructura original. No es necesario reinventarla si ya está bien organizada.

---

## Reglas inviolables

- Nunca inventes contenido que no esté en la conversación.
- Nunca inyectes reglas de diseño visual en el prompt. Claude Design maneja eso.
- El prompt siempre va en un bloque de código en el chat, nunca como archivo descargable.
- Las opciones del widget se pre-llenan con inferencias razonables — si son buenas, el usuario no necesita cambiar nada.
- Si la conversación no tiene suficiente contenido, díselo antes de generar un prompt vacío.
---

## Publicación en el gestor (antes de vincular)

**El entregable se publica en el gestor de artefactos de ProContacto — nunca como artefacto de la
conversación.** Lee `_shared/artifact-publish/artifact-publish.md` y aplica su procedimiento, que es
de dos pasos y no de uno:

1. `listar_artefactos` y busca por título canónico `{Cliente} · {Entregable} · {Tipo}` (sin versión
   ni fecha en el título — la versión vive adentro del artefacto).
2. Si ya existía → `publicar_version` sobre la misma URL, con un `message` que diga qué cambió.
   Si no → `publicar_artefacto`, y anota el `id`.

Nunca publiques sin haber buscado primero, aunque estés seguro de que es nuevo: una segunda
publicación del mismo entregable deja al cliente con un link que quedó viejo sin que nadie se entere.
Escribe el link del gestor en el chat — publicar sin mostrar el link es no publicar — y deja el `id`
en el comentario de trazabilidad del HTML.

Exportar a PDF u otro formato **exige que el artefacto ya esté publicado**: sin eso, el archivo que
circula no tiene original identificable detrás.

**Recién después** corre el gate de vinculación: lo que se registra es la URL del gestor.

## Gate de vinculación del deck (cierre)

Si el deck pertenece a un deal o a un proyecto, corre el **gate de vinculación** (no bloqueante) — ver `_shared/artifact-linkage/artifact-linkage.md`: regístralo como `Project_Asset__c` en Salesforce si es de un deal, o como issue `Artifact` en Jira si es de un proyecto, **solo con OK**. Si el deck es interno y no pertenece a ninguno, el gate no aplica (dilo en una línea y cierra).
