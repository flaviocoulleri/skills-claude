<!-- ⚠️ AUTO-COPIADO desde _shared/drive-upload/ por sync.sh — NO EDITAR ACÁ. Editá el canónico y volvé a correr sync.sh. -->

# Gate de subida a Drive (canónico)

Fuente única de verdad. Edita acá y corre `_shared/drive-upload/sync.sh`.

Todo skill que **produce un entregable** (presentación, documento, informe) lo deja subido a la
carpeta de Drive que le corresponde. **El entregable que sólo vive en el chat se pierde**: no lo
encuentra el resto del equipo, no queda en el expediente del deal ni del proyecto, y en la próxima
versión nadie sabe cuál era la buena.

## La regla

**El gate no se saltea en silencio.** No se pregunta "¿querés subirlo a Drive?" —eso invita al "no,
después"—. Se muestra **la carpeta destino ya resuelta** y se pide **confirmarla o cambiarla**. No
subir es una tercera opción explícita, con su consecuencia dicha en una línea.

> Esto es persuasión, no bloqueo: si el usuario elige no subir, se respeta y se sigue. Lo que no se
> permite es que la subida se pierda por omisión.

## La secuencia canónica

Todo entregable sigue estos cuatro pasos, en este orden:

```
1. Se confirma o cambia la carpeta → widget: subir a Drive               (subir-a-drive.html)
   → una sola vez, antes de construir nada
2. Se crea el artefacto            → publicado, y el HTML sube a Drive
   → el entregable se presenta junto con su link de Drive
3. Se ofrece corregir o descargar  → widget: ajustar / formatos          (exportar-deck.html)
4. Se elige el formato             → PDF · PPTX · imágenes
   → se entrega en el chat; a Drive ya subió el original en el paso 2
5. Se engancha al registro         → gate de vinculación                 (artifact-linkage.md)
   → Comercial: se busca o se crea la Opportunity y el link de Drive queda
     como Project_Asset__c
   → Delivery: se busca el proyecto Jira y el link de Drive queda como
     issue Artifact del tipo que corresponda

En cada edición se vuelve al paso 2: se actualiza el artefacto, sube la versión
nueva a Drive y se avisa — sin volver a preguntar la carpeta.
```

**La carpeta se pregunta primero, una sola vez.** Como a Drive va siempre el mismo archivo —el HTML
original— tenerla resuelta desde el arranque hace que cada iteración se guarde sola. Preguntarla al
final obligaría a interrumpir en cada corrección, que es justo cuando el usuario está concentrado en
el contenido.

**Descargar implica subir el original.** No hay un camino que entregue un archivo sin que el
entregable quede en Drive. El motivo es de trazabilidad, no de burocracia: un entregable que existe
sólo en la computadora de una persona no se sabe en qué versión circula, el resto del equipo no lo
encuentra, y cuando ese deal o proyecto cambia de manos, se perdió.

**Siempre se dice que se subió y adónde.** La subida es parte del paso, no un movimiento silencioso:
el usuario tiene que ver el link en el mismo mensaje que recibe el archivo. Un paso que ocurre sin
que se note deja de ser trazabilidad y pasa a ser una sorpresa desagradable el día que aparezca un
archivo donde no se esperaba.

**Se pregunta una sola vez por conversación.** Confirmada la carpeta, todas las versiones siguientes
van ahí sin volver a preguntar, salvo que el usuario quiera cambiar el destino.

**La única salida es explícita.** Si el usuario dice que no lo suba —o si no hay acceso a la
carpeta—, se entrega el archivo igual y se avisa en una línea que quedó sin respaldo ni
trazabilidad. Nunca se bloquea la entrega por esto, y nunca se insiste dos veces en la misma vuelta.

## Versiones

Si el entregable se modifica —aunque sea un ajuste chico— se sube la versión nueva **en el mismo
momento en que se actualiza el artefacto**, sin preguntar de nuevo y avisando en una línea con el
link. No alcanza con haberlo subido una vez: lo que circula por Drive tiene que ser lo último. La
versión sube en cada iteración (`ProContacto - {cliente} - {descripción} - v{n}.html`).

Es la razón principal para confirmar la carpeta al principio: sin eso, cada corrección exigiría
volver a preguntar dónde va, y en la práctica el equipo terminaría con la v1 en Drive y la v4 sólo
en la conversación.

## La carpeta según el área

Las rutas viven en el `references/drive-structure.md` de cada skill. Resumen:

| Área | Ruta destino |
|---|---|
| **Comercial** | `A - Comercial / A - Oportunidades / {País} / {Cliente} / {Oportunidad}` |
| **Delivery** | `J - Delivery / B - Proyectos / {Cliente} / {Proyecto}` |

En comercial, el cliente y la oportunidad son **dos niveles distintos**: un cliente recurrente
acumula sus oportunidades adentro de su carpeta, en vez de repetir el nombre del cliente en el
mismo nivel. Las carpetas históricas nombradas sólo con el cliente (`GNP`, `Gepp`, `Clip`) **ya son**
el nivel de cliente: se reutilizan tal cual y la oportunidad se crea adentro.

**Nunca** uses una carpeta de bases o plantillas como destino de un entregable.

## Procedimiento

1. **Resolvé la carpeta antes de preguntar.** Verificá el acceso a la raíz (`get_file_metadata`) y
   navegá la ruta nivel por nivel (`search_files`). Anotá qué existe y qué falta. Llegá al widget con
   una respuesta concreta, no con una pregunta abierta.
2. **Mostrá el gate** con `assets/subir-a-drive.html` (Patrón A), con la ruta completa a la vista y
   marcando qué niveles habría que crear.
3. **Con el OK, creá los niveles faltantes** de arriba hacia abajo (`create_file`,
   `mimeType: application/vnd.google-apps.folder`) y subí el archivo. Nunca crees carpetas sin
   confirmación.
4. **Verificá y reportá el `webViewLink`** clickeable. Si la subida falla, decilo — no des por hecho
   que quedó.
5. **Si el usuario elige otra carpeta**, pedile el link o el nombre y resolvé contra Drive antes de
   subir. Si elige no subir, registralo en una línea y seguí sin insistir de nuevo en esa vuelta.
6. **Sin acceso a la raíz**: pedí permisos a Ariel Tarsitano por Slack (`slack_search_users` por
   `ariel.tarsitano@procontacto.com.mx`, luego DM con link y motivo), avisá que el destino queda
   pendiente y seguí. Nunca inventes el acceso ni dejes un placeholder de carpeta.

## Qué se sube: sólo el HTML liviano

**A Drive va un único archivo: el HTML liviano del entregable** — el original, sin la tipografía
embebida. Siempre el mismo, se haya pedido un formato o no.

Los formatos exportados (PDF, PPTX, imágenes) **se entregan al usuario en el chat pero no se
suben**. Si hace falta cualquiera de ellos otra vez, se regenera del HTML en segundos.

Por qué así, y no subiendo también el exportado:

- **El HTML es el original.** Es lo único desde lo que se puede volver a generar todo lo demás. Un
  PDF en Drive sin su fuente al lado es un callejón sin salida: para cambiar una cifra hay que
  rehacerlo entero.
- **Es lo único que se puede subir hoy.** El conector de Drive **no acepta rutas de archivo, sólo
  contenido en línea**, así que el agente tiene que emitir el archivo entero. Medido sobre un deck
  de 9 slides: HTML liviano ~6k tokens, PDF ~34k, PNG ~29k por imagen, **PPTX ~247k — inviable**.
  Subir binarios no es caro, es imposible.
- **Sin la fuente embebida pesa una fracción.** Los ~110 KB de Open Sans viven en el artefacto, que
  es donde se presenta; el PDF ya sale con la tipografía correcta porque lo genera el exportador
  headless con su propio navegador.

> **Pendiente de infra.** La restricción es de herramienta, no de diseño. Con una service account de
> Google y `curl` contra la API de Drive se podría subir cualquier archivo de cualquier tamaño sin
> costo de tokens, y ahí conviene revisar esta regla. Sirve para todos los skills que escriben en
> Drive, no sólo para los entregables.

**Nombre**: la nomenclatura del entregable, `ProContacto - {cliente} - {descripción} - v{n}.html`.

## Relación con el gate de vinculación (paso 5)

Los dos gates son distintos y van **en este orden**: primero el archivo queda guardado donde el
equipo lo encuentra (Drive), después queda **enganchado** al registro que corresponde. Guardar sin
enganchar deja un archivo que existe pero que nadie va a encontrar desde el deal o el proyecto;
enganchar sin guardar deja un registro que apunta a una conversación.

**Lo que se registra es el id del archivo de Drive** que acaba de subirse — por eso este gate corre
después y no antes. El detalle de cómo se busca o se crea el padre está en
`_shared/artifact-linkage/artifact-linkage.md`:

- **Comercial** → `Project_Asset__c` colgando de la Opportunity. Si la Opp no existe, se **ofrece
  crearla** delegando en `pc-sales-sf-opportunity-builder`; nunca se crea sin OK.
- **Delivery** → issue `Artifact` en el proyecto Jira del cliente, del tipo que corresponda al
  entregable. El proyecto se busca en el `Project_Asset__c` y, si no está, en Jira. **Un proyecto
  Jira no se crea** para guardar un entregable: eso es decisión de PMO.

Si el padre no aparece, el registro queda pendiente y se dice en una línea. Nunca se bloquea la
entrega del archivo por esto.
