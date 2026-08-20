<!-- ⚠️ AUTO-COPIADO desde _shared/artifact-linkage/ por sync.sh — NO EDITAR ACÁ. Editá el canónico y volvé a correr sync.sh. -->

# Gate de vinculación de artefactos (canónico)

Fuente única de verdad. Edita acá y corre `_shared/artifact-linkage/sync.sh`.
Todo skill que **crea o modifica un entregable/artefacto** corre este gate **al cerrar**, para
dejarlo vinculado en el sistema de registro. **No bloqueante**: se ofrece y se crea **solo con OK**;
si falta el contexto de destino, se deja **pendiente** y se sigue.

## Destino según el área

| Área del skill | Registro | Objeto |
|---|---|---|
| **Comercial** (artefacto de un deal) | Salesforce | `Project_Asset__c` |
| **Delivery** (artefacto de un proyecto) | Jira | issue `Artifact` |
| **Meta / genérico** | según a qué pertenece el artefacto | asset si es de un deal, `Artifact` si es de un proyecto; si es interno y no pertenece a ninguno, el gate **no aplica** (dilo en una línea y cierra) |

Si el mismo artefacto vive en un deal **y** en un proyecto (p. ej. wireframes que pasan de venta a
Sprint 0), se registra en **ambos** lados.

## Cómo corre el gate (secuencia)

1. **Identifica el artefacto** que produjiste/modificaste: tipo (deck / wireframe / diagrama / doc /
   SOW / backlog…) + su **id o link**.

   > **Lo que se registra es el entregable publicado en el gestor de ProContacto**
   > (`https://artifacts.procontacto.com.mx/a/{uuid}`), **nunca el artefacto de la conversación**. El
   > gestor es la URL que versiona, que el cliente ya tiene y que sobrevive a la conversación; un
   > registro que apunta a un artefacto de Claude envía a quien lo abra dentro de seis meses a una
   > conversación ajena. Como el gate corre después de publicar (`_shared/artifact-publish/`), a esta
   > altura el `id` del gestor ya existe: usá ese.
   >
   > **Si además se subió a Drive**, el archivo de Drive va como **registro aparte** (respaldo del
   > original re-editable), nunca en lugar del registro del gestor. Y si el entregable **solo** vive
   > en Drive —un documento que no pasó por el gestor—, entonces sí el registro es el de Drive.
2. **Resuelve el destino** (registro SF o proyecto Jira) — ver §A / §B. **No alcanza con preguntar
   y rendirse**: buscá primero, ofrecé crear después, y recién si no hay forma dejá pendiente.
   El detalle de cómo buscar y crear está en §A (comercial) y §B (delivery).
3. **Chequea duplicado** antes de crear (por `Value__c` en SF / por summary+issuetype en Jira). Si ya
   existe, **reusa** (y ofrece actualizar el link si cambió) — nunca dupliques.
4. **Ofrece con OK.** Muestra qué vas a registrar y dónde —incluida la **descripción** que vas a
   dejar, que el usuario puede corregir ahí mismo— y espera confirmación explícita (widget de acción
   o pregunta directa). Nunca escribas sin OK.
5. **Crea y verifica** (post-write) — ver §A / §B. Reporta el link clickeable.
6. **Sin contexto → pendiente.** Si falta el registro SF o el proyecto Jira, no bloquees: informa
   "el artefacto quedó en {link}; cuando tengas {la Opp/Cuenta/Contrato | el proyecto Jira} corre de
   nuevo y lo engancho" y termina normal.

## §A · Comercial → `Project_Asset__c` (Salesforce)

Modelo de escritura (canónico del repo):

- **El rol vive en `Type__c`** (semántico): `ProContactoArtifactId`, `CommercialProposalId`,
  `UserStoriesSOWId`, `WireframeId`, `ClaudeDesignProjectId`, `DocuSignEnvelopeId`, etc. Verifica el
  picklist real con `getObjectSchema` — no inventes valores.
- **`Value__c` = el id EN CRUDO**, nunca la URL completa (gestor → **uuid**; Drive → id del archivo;
  Claude Design → **uuid**, nunca un id de Drive).
- **`Link__c` es fórmula** (arma la URL) y **`Name` es auto-number** → **nunca los escribas**.
- **`Description__c` dice de qué documento se trata** (texto libre, **máx. 255**). Ver abajo: es
  **obligatorio de facto** en `ProContactoArtifactId` y `CoworkArtifactId`.
- Relación al padre por el lookup correspondiente: `Account__c` / `Opportunity__c` / `Quote__c` /
  `Contract__c` / `Project__c` (el que corresponda al artefacto).
- `Grouper__c` NO es para el rol (es para duplicados prod/sandbox, opcional).

#### Qué `Type__c` corresponde a cada cosa

| Dónde vive el entregable | `Type__c` | `Value__c` (en crudo) |
|---|---|---|
| **Gestor de ProContacto** (el default: todo entregable publicado) | **`ProContactoArtifactId`** | el **uuid** de `https://artifacts.procontacto.com.mx/a/{uuid}` |
| Copia / original re-editable en Drive | `GoogleDriveFileId` · `GoogleDocsId` · `GoogleSlidesId` · `GoogleSheetId` | id del archivo de Drive |
| Deck iterado en Claude Design | `ClaudeDesignProjectId` | uuid del proyecto de Claude Design |
| Artefacto de conversación de Claude | `CoworkArtifactId` | uuid — **legado: ya no se crean nuevos** |

**El tipo semántico y el `ProContactoArtifactId` no compiten: conviven.** `CommercialProposalId`,
`UserStoriesSOWId` y `WireframeId` dicen *qué es* el entregable y siguen siendo el registro principal
cuando aplican; `ProContactoArtifactId` dice *dónde está publicado*. Si la propuesta se publicó en el
gestor, van los dos assets (mismo padre, distinto `Type__c`) — el semántico con el id del documento y
el `ProContactoArtifactId` con el uuid del gestor.

> **No es redundancia: es que `Link__c` deriva la URL del `Type__c`.** Un uuid del gestor metido en un
> `CommercialProposalId` produce un link roto, porque la fórmula le va a anteponer el dominio de
> Drive. **Cada id va en el tipo que corresponde a su sistema.** Si sólo vas a registrar uno, que sea
> el del gestor: es el que el cliente tiene y el que versiona.

> **`CoworkArtifactId` está en retiro.** Existe por los registros viejos y para leerlos (búsquedas de
> continuidad, dedupe). Un entregable nuevo **nunca** se registra así: el artefacto de conversación
> dejó de alojar entregables (ver `_shared/artifact-publish/`). Si al buscar duplicados encontrás un
> `CoworkArtifactId` del mismo entregable, ofrecé **reemplazarlo** por el `ProContactoArtifactId` una
> vez que esté publicado en el gestor.

#### `Description__c` — sin esto, el registro no dice nada

`Type__c` alcanza cuando es específico (`CommercialProposalId` ya dice qué es). Pero
**`ProContactoArtifactId` y `CoworkArtifactId` son contenedores**: bajo el mismo tipo entra una
propuesta, un ERD, un informe o un tablero. Dos assets `ProContactoArtifactId` colgados de la misma
Opp son indistinguibles entre sí — y quien abra el inventario dentro de seis meses tiene que abrir
los dos links para saber cuál era cuál.

Por eso, en esos dos tipos **`Description__c` es obligatorio de facto**: si no sabés qué poner, no
tenés el contexto para registrar el asset.

- **Qué va:** *qué es el documento* y *a qué corresponde*, en una línea. Máx. **255 caracteres**
  (`textarea`; si te pasás, Salesforce corta o rechaza — recortá vos).
- **Qué NO va:** ni versión ni fecha (el gestor versiona, y el `LastModifiedDate` ya está), ni la URL
  (está en `Value__c`/`Link__c`), ni el nombre del skill.

| Ejemplo bueno | Por qué |
|---|---|
| `Propuesta comercial CRM — alcance, inversión y plan de trabajo` | dice qué es y qué contiene |
| `ERD del modelo de datos custom (Pedido, Visita, Liquidación)` | un lector sabe si le sirve sin abrirlo |
| `Wireframes v2 del Anexo C — 14 pantallas de la consola de ventas` | distingue de los v1 |
| `Informe de reconciliación Odoo↔SF↔Jira al cierre del sprint 4` | ubica el documento en el proceso |

| Ejemplo malo | Por qué |
|---|---|
| `Artefacto` / `Documento` / `HTML` | no distingue nada: es lo mismo que dejarlo vacío |
| `Propuesta v3 — 11/08/2026` | versión y fecha: las dos cosas que el sistema ya sabe |
| `https://artifacts.procontacto.com.mx/a/bcbf…` | la URL ya está en `Value__c` |

En el resto de los tipos `Description__c` es **opcional pero recomendado** cuando hay más de un asset
del mismo tipo en el mismo padre (p. ej. varios `GoogleDocsId` en una Opp): ahí cumple la misma
función de desambiguar. En los tipos de credencial/config (`sf_client_secret`, `MID`, claves) **no
pongas nada**: no describas un secreto.

> ⚠️ **`Link__c` para el tipo nuevo.** `Link__c` es fórmula y arma la URL a partir de `Type__c` +
> `Value__c`. Si al verificar el post-write el `Link__c` del `ProContactoArtifactId` viene vacío o mal
> armado, **no lo escribas** (es read-only): el `Value__c` con el uuid ya es el registro válido —
> reportá el link a mano (`https://artifacts.procontacto.com.mx/a/{Value__c}`) y avisá que a la
> fórmula le falta la rama del tipo nuevo.

### Primero: la Oportunidad tiene que existir

El `Project_Asset__c` cuelga de un padre. En comercial ese padre casi siempre es la **Opportunity**,
así que resolverla es parte del gate, no un prerrequisito ajeno:

1. **Buscá** la Opp por nombre de cliente y descripción del deal
   (`soqlQuery` sobre `Opportunity` filtrando por `Account.Name` y estados abiertos). Mostrá lo que
   encontraste y pedí que confirmen cuál es — no elijas por tu cuenta si hay más de una.
2. **Si no existe, ofrecé crearla.** No la crees de una: mostrá qué se va a crear y esperá el OK. Con
   el OK, **auto-invocá `pc-sales-sf-opportunity-builder`** (transición invisible) en vez de crear la
   Opp a mano — ese skill sabe el Record Type, la Business Unit, el template y los obligatorios.
3. **Si el usuario no quiere crearla todavía**, dejá el registro pendiente (paso 6) y decilo en una
   línea. El entregable ya está en Drive: lo que falta es el enganche, y se puede hacer después.

### Después: el asset

`getObjectSchema('Project_Asset__c')` → buscá si ya existe uno con ese `Value__c` en el padre → si no,
`createSobjectRecord` con `Type__c` + `Value__c` (**el id en crudo**: el uuid del gestor, o el id del
archivo de Drive según la tabla de arriba) + **`Description__c`** + lookup del padre → `soqlQuery` de
verificación → mostrá el `Link__c`.

```
createSobjectRecord('Project_Asset__c', {
  Opportunity__c: oppId,                       // o Account__c / Quote__c / Contract__c / Project__c
  Type__c: 'ProContactoArtifactId',
  Value__c: '<uuid>',                          // la última parte de artifacts.procontacto.com.mx/a/<uuid>
  Description__c: 'Propuesta comercial CRM — alcance, inversión y plan de trabajo',  // ≤255
  Status__c: 'Active'
  // NO Name (auto-number) ni Link__c (fórmula)
})
```

Si el asset ya existía **sin** `Description__c` (registros anteriores al campo), aprovechá el paso y
ofrecé completarlo con el mismo OK — es una línea y evita que el inventario siga siendo ilegible.

Si el entregable ya estaba registrado y lo que cambió es la versión, **actualizá el `Value__c` del
asset existente** en vez de crear uno nuevo: dos assets del mismo entregable es exactamente la
ambigüedad que el registro venía a evitar.

> Con el gestor en juego esto pasa **menos**: una versión nueva es `publicar_version` sobre la misma
> URL, así que el uuid **no cambia** y el asset ya registrado sigue siendo válido sin tocar nada. Lo
> que sí hay que actualizar es un asset que apunte a un artefacto de Cowork o a una copia de Drive
> que quedó vieja.

## §B · Delivery → issue `Artifact` (Jira)

El work type real es **`Artifact`** (workflow "Deliverable"), **no** `Artefacto`. Issuetype id conocido
**10209** — igual **verifica en runtime** con el metadata de la org (`getJiraIssueTypeMetaWithFields`).

Receta:

1. **Metadata** del proyecto → confirma `id`/`name` real de `Artifact` y campos requeridos (varían por
   proyecto; no asumas). `cloudId` en runtime; site `procontacto.atlassian.net`.
2. **Busca duplicado:** `project = <KEY> AND issuetype = "Artifact" AND summary ~ "<entregable>"`. Si
   existe, reusa (ofrece actualizar el link).
3. **Crea** (`createJiraIssue`): `summary` = nombre del entregable; `description` con propósito breve +
   **link del gestor** (`https://artifacts.procontacto.com.mx/a/{uuid}`), con el de Drive como
   respaldo si además se subió; si el link quedó pendiente, dilo explícito) + skill que lo produce +
   fase/gate. Completa los campos requeridos del metadata.
4. **Verifica** (`getJiraIssue`) y muestra `https://procontacto.atlassian.net/browse/<ISSUE-KEY>`.

### Primero: encontrar el proyecto Jira

1. **Buscalo en Salesforce**: el `Project_Asset__c` del `Project__c` guarda `JiraProjectKey` /
   `JiraProjectId`. Es la vía preferida porque es la que ya usa el resto de la cadena.
2. **Si no está ahí, buscalo en Jira** por nombre de cliente o proyecto
   (`jira_get_all_projects` / `getVisibleJiraProjects`) y mostrá los candidatos para que confirmen.
3. **Si aparece pero no estaba registrado en Salesforce**, ofrecé dejar el `JiraProjectKey` como
   `Project_Asset__c` del proyecto: es la causa de que la próxima vez haya que volver a buscarlo.
4. **Si el proyecto no existe**, no lo crees: dar de alta un proyecto Jira es una decisión de PMO,
   no un efecto colateral de guardar un entregable. Dejá el registro pendiente y avisá.

### Después: el issue

Del tipo que corresponda al entregable — el work type real es **`Artifact`** (workflow "Deliverable"),
y dentro de él el campo que clasifica (AS-IS, TO-BE, Wireframes, ERD, SOW, acta…) sale del metadata
del proyecto, que **varía por proyecto**: leelo, no lo asumas.

En la `description` va **el link del gestor** del entregable, más el propósito breve, el skill que lo
produjo y la fase o gate. El link de Drive va como referencia secundaria cuando además se subió.

Si el proyecto también tiene `Project__c` en Salesforce, dejá **además** el
`Project_Asset__c(Type__c='ProContactoArtifactId', Value__c=<uuid>, Project__c=<projectId>)`: el issue
de Jira es la trazabilidad del entregable en el proyecto, el asset es el índice consultable desde
Salesforce, y el resto de la cadena lee de ahí.

Para alta compleja de campos/relaciones, delegá a `pc-delivery-jira-issue-builder`; para el alta
simple del `Artifact`, hacela directo.

## Delegación

Si el skill corre **dentro de un flujo de delivery** orquestado por `pc-delivery-deliverable-orchestrator`,
puedes **devolver el control** al orchestrator para el registro en lugar de duplicarlo — pero solo si el
orchestrator está en el mismo flujo. Fuera de ese flujo, el gate lo corre el propio skill.
