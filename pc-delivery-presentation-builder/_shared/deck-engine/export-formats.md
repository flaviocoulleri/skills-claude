# Exportar el deck — formatos, dónde se piden y qué prometer

> **Qué es esto.** Qué formatos entrega el motor, cómo se ofrecen y qué decirle al usuario sobre
> cada uno. Canónico en `_shared/presentation-builder/deck-engine/`; propagado por `sync.sh`.

## El principio

**El deck HTML es el original; todo lo demás se exporta de él.** Ningún formato se maqueta aparte,
así que ninguno puede quedar desalineado con el deck. Cuando el usuario quiere un cambio, se corrige
el deck y se vuelve a exportar — nunca se edita el PDF o el PPTX por separado.

## Dónde viven las opciones de exportación: en el chat, no en el deck

Las opciones se ofrecen **en el chat**, con `_shared/assets/exportar-deck.html` vía
`mcp__visualize__show_widget`, apenas queda publicado el artefacto. **No van adentro del deck.**

Esto no es una preferencia estética, es una restricción real del contenedor:

- El visor embebe el artefacto en un iframe con
  `sandbox="allow-scripts allow-same-origin allow-forms"`. Sin `allow-downloads`, `allow-popups` ni
  `allow-modals`, **la descarga falla en silencio** (no lanza excepción), `window.open` devuelve
  `null` y `window.print()` no hace nada. Un botón "Descargar PDF" adentro del deck no avisa que
  falló: parece que funcionó y no pasó nada.
- **`sendPrompt` no existe dentro de un artefacto** — sólo en los widgets de `show_widget`. Un botón
  del deck no puede pedirle nada al agente.
- En un widget, en cambio, `sendPrompt` está garantizado: el click llega al chat, el agente genera
  el archivo con `scripts/export-deck.mjs` y lo entrega como archivo de verdad.

Por eso el artefacto es **un visor puro** (navegación, índice, notas del orador, pantalla completa,
ayuda) y la exportación es un paso del flujo, no un botón del deck.

## Los formatos

| Formato | Qué es | Para qué sirve | Texto editable |
|---|---|---|---|
| **HTML** (el original) | Un archivo autocontenido, animado, navegable | Presentar en vivo, compartir el artefacto, subirlo a Drive, seguir iterando | Sí, es la fuente |
| **PDF** | Una página por slide, 16:9, con texto seleccionable | Mail, impresión, adjuntar, leave-behind | No |
| **PNG** | Una imagen por slide, 1920×1080 | Pegar un slide en un doc, un mensaje o una propuesta | No |
| **JPG** | Igual que PNG, más liviano | Decks largos, adjuntos con límite de tamaño | No |
| **PPTX** | PowerPoint, un slide por diapositiva a página completa | Entregarlo a quien trabaja en PowerPoint o Keynote | **No** — cada diapositiva es la imagen del slide |

**Las animaciones no viajan en ningún archivo.** Cada slide se captura en su estado final. Decilo
siempre: es lo primero que alguien nota y no es un error.

## Cómo se genera

Con `scripts/export-deck.mjs`, que abre el deck en un navegador headless y captura cada slide a
1920×1080:

```bash
node scripts/export-deck.mjs <deck.html> --formato=pdf,png,pptx --salida=./export
```

| Opción | Qué hace |
|---|---|
| `--formato=LISTA` | Coma separada: `pdf,png,jpg,pptx` o `todos`. Por defecto `pdf`. |
| `--salida=DIR` | Carpeta destino. Por defecto, al lado del deck. |
| `--compacto` | Renderiza a 1280×720 en vez de 1920×1080: 50-70% menos de peso, casi sin diferencia visible. |
| `--calidad-jpg=N` | Calidad JPEG 1–100 (por defecto 92). |

El PDF sale de la impresión del navegador headless, así que **conserva el texto seleccionable**. El
`.pptx` lo arma `scripts/pptx.mjs`, un empaquetador OOXML propio sin dependencias (validado: 16:9
exacto, una imagen full-bleed por diapositiva). Playwright se instala solo la primera vez en la
caché del usuario; si no hay red o falla, el script lo dice y termina — no rompe nada más.

## Cómo ofrecerlo (guion)

Al entregar el deck, en una línea, y después el widget:

> *"Ya está la presentación: recorrela con las flechas, tenés el índice y las notas del orador en la
> barra de abajo. ¿En qué formato te la llevás?"*

Reglas:

- **No preguntes el formato antes de tener el deck.** Primero se construye, después se exporta. El
  formato no cambia cómo se diseña.
- **Primero el gate de Drive, después la exportación.** Ver `_shared/drive-upload/drive-upload.md`:
  el entregable se sube a la carpeta que corresponde antes de repartir formatos, y **en cada nueva
  versión** se vuelve a ofrecer la subida.
- **No prometas texto editable en PowerPoint.** Cada diapositiva es la imagen del slide. Si el
  usuario necesita editar el texto, lo correcto es **editar el deck** y re-exportar: ese es el
  circuito, y conviene decirlo antes de que descubra el .pptx no editable.
- **Verificá antes de cantar victoria.** Confirmá que los archivos existen y que la cantidad de
  páginas/imágenes coincide con la cantidad de slides. Si no coincide, arreglá y volvé a exportar —
  no reportes éxito. El script ya hace esta comprobación y termina con error si algo no cuadra.
