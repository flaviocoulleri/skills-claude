<!-- ⚠️ AUTO-COPIADO desde _shared/session-continuity/ por sync.sh — NO EDITAR ACÁ. Editá el canónico y volvé a correr sync.sh. -->

# Gate de continuidad — ¿esto ya venía trabajándose en otra conversación?

> Corre **antes de crear nada**, en cuanto sabés sobre qué cliente/deal (comercial) o proyecto (delivery) estás trabajando. **Nunca bloquea** — avisa y ofrece. Hablá en el idioma del área: ver la tabla de vocabulario más abajo.

## El problema que resuelve

Cada conversación de Cowork arranca sin memoria de las anteriores. Si el usuario ya venía trabajando esto en otra conversación —donde están el contexto del discovery, las decisiones de alcance, los montos o el plan acordados— y abre una nueva para "seguir", acá se arranca de cero: se vuelve a preguntar lo mismo, se re-deriva lo ya decidido, y en el peor caso **se crean registros duplicados** (una segunda Opp abierta del mismo cliente, una Quote paralela, un SOW que compite con el que ya existe).

El costo no es la molestia: es que después hay dos verdades en Salesforce y nadie sabe cuál vale.

## Lo que este gate NO puede hacer

**No se puede detectar ni linkear la conversación previa.** Cowork no expone un listado de conversaciones del usuario, ni el skill conoce la URL de la suya. No lo intentes ni inventes un link.

Lo que sí se puede es **detectar la huella del trabajo previo** (Salesforce, y en delivery también Jira y Drive) y, con eso, hacer una recomendación informada. La decisión de volver a la otra conversación es del usuario — vos solo se lo hacés visible en el momento en que sirve, que es **antes** de crear algo.

## Hablá en el idioma del área

La unidad de trabajo que el usuario reconoce **cambia según el área**. Usá la de tu área y ninguna otra — decirle "deal" a un PM o "proyecto" a un AE delata que el mensaje es genérico y le quita autoridad.

| Área | Unidad | Cómo lo decís | Dónde vive la huella |
| --- | --- | --- | --- |
| **comercial** | el **deal** | *"si venías trabajando **este deal** en otra conversación…"* | `Opportunity` abierta, sus `Quote`, `Contract` sin activar, `Project_Asset__c` de la Cuenta |
| **delivery** | el **proyecto** | *"si venías trabajando **este proyecto** en otra conversación…"* | `Project__c`, sus `Project_Asset__c`, issues y sprints del proyecto Jira, carpeta de Drive del proyecto |
| **marketing** | la **pieza** / el caso | *"si venías armando **esto** en otra conversación…"* | `Project_Asset__c` del caso, documentos en Drive |
| **meta** (diagramas, wireframes) | el **entregable** | *"si venías armando **este entregable** en otra conversación…"* | `Project_Asset__c` de tipo `ProContactoArtifactId` / `WireframeId` / `BlueprintId` (y `CoworkArtifactId` en registros viejos) del Account o Project |

En delivery el riesgo no es sólo duplicar registros: es **partir el backlog en dos** (dos tandas de issues para el mismo alcance) o generar un segundo entregable que compite con el que el cliente ya recibió.

## Cuándo corre

En cuanto tenés identificada la unidad del área (el **cliente/deal** en comercial, el **proyecto** en delivery), y **siempre antes de la primera escritura**. Si el skill entra encadenado desde otro skill en la misma conversación, **saltealo**: el contexto viene del skill anterior, no de otra conversación.

## Qué buscar

Una sola pasada, barata.

### En comercial — actividad reciente sobre el cliente

```soql
SELECT Id, Name, StageName, RecordType.DeveloperName, Amount, CloseDate,
       LastModifiedDate, LastModifiedBy.Name, IsClosed,
       (SELECT Id, QuoteNumber, Status, IsSyncing, TotalPrice, LastModifiedDate FROM Quotes)
FROM Opportunity
WHERE AccountId = '<accountId>' AND IsClosed = false
ORDER BY LastModifiedDate DESC LIMIT 10
```

```soql
SELECT Id, Type__c, Value__c, LastModifiedDate, LastModifiedBy.Name,
       Opportunity__c, Quote__c, Contract__c
FROM Project_Asset__c
WHERE Account__c = '<accountId>' AND Status__c = 'Active'
ORDER BY LastModifiedDate DESC LIMIT 15
```

Si el objeto del skill es un Contract, sumá `SELECT Id, ContractNumber, Status, StartDate, LastModifiedDate FROM Contract WHERE AccountId = '<accountId>' AND Status != 'Cancelled'`.

### En delivery — actividad reciente sobre el proyecto

```soql
SELECT Id, Name, LastModifiedDate, LastModifiedBy.Name, Completion_Summary__c,
       (SELECT Id, Type__c, Value__c, LastModifiedDate, LastModifiedBy.Name FROM Project_Assets__r WHERE Status__c = 'Active')
FROM Project__c
WHERE Id = '<projectId>'
```

Si el skill entra por cliente y no por proyecto, buscá los `Project__c` de esa Cuenta ordenados por `LastModifiedDate DESC`.

**Sumá la huella fuera de Salesforce cuando el skill ya tiene el conector:**

- **Jira** — issues creados o modificados en las últimas 72 h en el proyecto (`updated >= -3d ORDER BY updated DESC`), y si hay un sprint activo. Un backlog al que alguien le metió mano hoy es la señal más fuerte de que hay una conversación en curso.
- **Drive** — archivos tocados hoy en la carpeta del proyecto.

No dispares conectores extra sólo para este gate: usá los que el skill ya iba a usar igual. Si Jira no está conectado, resolvé con lo de Salesforce y listo.

## Cómo decidir si hay "conversación previa probable"

No alcanza con que existan registros — casi todo cliente tiene historia. Lo que indica **una conversación en curso** es actividad **fresca**:

| Señal | Peso |
| --- | --- |
| Algo modificado en las **últimas 72 h** | fuerte |
| Modificado por **el mismo usuario** que está corriendo el skill | fuerte |
| Opp abierta con **overlap de familias** con lo que se está por crear | fuerte |
| Quote en `Draft` sin sincronizar | fuerte (quedó a mitad de camino) |
| Contract en `Draft` sin activar | fuerte |
| `Project_Asset__c` de tipo `ProContactoArtifactId` para este cliente/Opp | fuerte — **ese entregable publicado es el output de la conversación anterior**; retomalo con `publicar_version` sobre el mismo uuid, no publiques uno nuevo |
| `Project_Asset__c` de tipo `CoworkArtifactId` para este cliente/Opp | fuerte, pero **es un registro legado** — el entregable vivía en un artefacto de conversación; al retomarlo publicalo en el gestor y reemplazá el asset por `ProContactoArtifactId` |
| **[delivery]** issues de Jira creados/modificados en las últimas 72 h, o sprint activo con movimiento | fuerte |
| **[delivery]** `Project__c` con `Completion_Summary__c` vacío y assets recién tocados | fuerte — el onboarding quedó a medias |
| Actividad de hace más de 30 días | débil — es historia, no una conversación en curso |

**Dos señales fuertes → mostrá el gate.** Una sola y débil → seguí sin molestar. Ante la duda, mostralo: el costo de mostrarlo es un click; el de no mostrarlo es un registro duplicado.

## Qué mostrar

Un solo bloque, con lo concreto adelante y la recomendación al final. Nada de nombres técnicos de objetos (regla de lenguaje de `common-rules.md`).

```
⚠️ Este cliente ya tiene trabajo en curso

  · Oportunidad "Wexler SAS | Support | Soporte Sales Cloud"
    modificada hace 2 h por vos · USD 2.000 · etapa Negociación
  · Cotización 00006773 — en borrador, sin sincronizar
  · Resumen del deal: <link al artefacto>

Si venías trabajando este deal en otra conversación, seguí ahí:
vas a tener el contexto de lo ya hablado. Acá arranco sin esa memoria,
y si creamos algo nuevo podemos terminar con registros duplicados.

¿Cómo seguimos?
  a) Continúo acá sobre lo que ya existe (levanto el contexto desde Salesforce).
  b) Voy a buscar la otra conversación — frená acá.
  c) Es un deal distinto: creá algo nuevo igual.
```

En **delivery** el mismo bloque, con la unidad del área:

```
⚠️ Este proyecto ya tiene trabajo en curso

  · Proyecto "BBVA — Implementación Service Cloud"
    carpeta y canal creados hace 3 h por vos
  · 14 issues creados hoy en el backlog de BBVA-102
  · Sprint 1 activo

Si venías trabajando este proyecto en otra conversación, seguí ahí:
vas a tener el contexto de lo ya decidido. Acá arranco sin esa memoria,
y podemos terminar con el backlog partido en dos tandas.

¿Cómo seguimos?
  a) Continúo acá sobre lo que ya existe.
  b) Voy a buscar la otra conversación — frená acá.
  c) Es otro alcance: creá algo nuevo igual.
```

Reglas del mensaje:

- **Mostrá evidencia, no una sospecha.** "Modificada hace 2 h por vos" es lo que hace que el AE se acuerde de la otra conversación. "Puede que tengas otra conversación" solo, es ruido.
- **Nunca afirmes que existe una conversación previa** — no lo podés saber. La formulación es condicional: *"si venías trabajando este deal en otra conversación…"*.
- **No prometas un link a la conversación.** Sí linkeá el artefacto Cowork si existe: es lo más cercano al contexto anterior que podés ofrecer.
- **El default es (a).** Si el AE no responde o dice "dale", continuás acá levantando el contexto — no frenes el trabajo.

## Qué hacer con cada respuesta

- **(a) Continuar acá** — cargá el contexto desde los registros encontrados (Opp, Quote, montos, familias, assets) y **seguí sobre ellos en modo update**, no crees paralelos. Es el camino que el resto del skill ya sabe recorrer.
- **(b) Frenar** — cerrá con una línea corta: *"Listo, lo dejo acá. Todo lo que hay quedó sin tocar."* **No escribas nada.** No insistas.
- **(c) Es otro deal** — seguí con el flujo normal de creación. Registrá en la `Description` del registro nuevo una línea del tipo `Deal separado del existente <Name> (<Id>) — confirmado por el AE` para que la convivencia quede explicada.

## Anti-patrones

- **Bloquear.** Este gate no bloquea nunca. El AE puede tener una razón perfectamente válida (dos frentes distintos del mismo cliente, un CR, una re-cotización).
- **Mostrarlo dos veces en la misma conversación.** Corre una sola vez, en el primer skill que toque el deal. Si otro skill se invoca encadenado, ya viene resuelto.
- **Mostrarlo con actividad vieja.** Un cliente con una Opp cerrada hace ocho meses no justifica el gate; solo genera ruido y entrena al AE a ignorarlo.
- **Inventar un link a la conversación previa.** No existe. Ofrecé el artefacto o nada.
