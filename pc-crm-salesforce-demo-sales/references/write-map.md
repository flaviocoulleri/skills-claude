# Mapa de escritura (contrato Q07)

Este documento declara, objeto por objeto, qué campos toca el skill y su obligatoriedad. Es la fuente de verdad para el **gate pre-write** (Fase 4 del SKILL.md) y la **verificación post-write** (Fase 6).

Convenciones:

- **Rol**: `simple` (texto/número/fecha), `picklist`, `lookup`.
- **Obligatorio**: `T` = técnico (el schema lo exige: `createable=true`, `nillable=false`, sin `defaultValue`), `N` = de negocio (lo exige este skill aunque el schema lo marque opcional), `—` = opcional real.
- **Valor**: siempre orientativo, **nunca contractual**. Los API names de campos custom y los valores de picklist mandan del schema real (`sf sobject describe`), resuelto en la Fase 2 y cacheado en `orgMeta` para toda la corrida.
- Todo campo marcado `⚠ resolver en runtime` es incierto porque depende de la configuración del org (custom field, rollup vs. campo directo) — no asumir, describe primero.

## Regla transversal: "todos los campos completos"

Para Lead, Account y la Opportunity elegida, el pedido original dice explícitamente "todos los campos completos" / "completa todos los campos posibles". Tratar como obligatorio de negocio (`N`) **todo campo `createable=true` del objeto** que no sea de sistema (Id, CreatedDate, OwnerId gestionado aparte, etc.), aunque el schema lo marque opcional. Completar con datos plausibles y coherentes con la temática elegida en la Fase 1 — nunca con placeholders tipo "N/A" o "test".

---

## Account (el "cliente potencial" de la demo)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| Name | simple | T | Nombre de una empresa ficticia de la industria elegida |
| Industry | picklist | N | Debe alinear con la temática de la demo |
| Phone | simple | N | |
| NumberOfEmployees | simple | N | |
| Type | picklist | N | p. ej. "Prospect" — valor real del schema |
| Description | simple | N | 2-4 líneas sobre el negocio ficticio, coherente con la temática |
| BillingStreet/City/State/PostalCode/Country | simple | N | Dirección de facturación completa |
| ShippingStreet/City/State/PostalCode/Country | simple | N | Dirección de envío completa (puede repetir la de facturación) |
| AccountNumber | simple | N | Número de cuenta ficticio |
| "Frecuencia de compra" (custom) | picklist o simple ⚠ resolver en runtime | N | Buscar por **Label** en `describe`, no asumir API name |
| "Campañas respondidas" (custom) | simple ⚠ resolver en runtime | N | Idem — buscar por Label |
| "Cantidad total de compras" (custom) | simple ⚠ resolver en runtime | N | Idem — buscar por Label |

Registros relacionados a crear sobre esta Account (ver secciones propias más abajo): 6 actividades, 3 Opportunities, 7 Orders (6 genéricas + 1 ligada a la Opportunity elegida), 3 Cases, 3 Visit (2 completas + 1 planeada), 2 archivos adjuntos.

---

## Lead ("Persona X")

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| LastName | simple | T | |
| Company | simple | T | Empresa ficticia — puede ser la misma industria que la Account o una relacionada |
| FirstName | simple | N | |
| Salutation | picklist | N | |
| Title | simple | N | |
| Email | simple | N | Formato válido |
| Phone / MobilePhone | simple | N | |
| Street/City/State/PostalCode/Country | simple | N | |
| Industry | picklist | N | Alineado a la temática |
| LeadSource | picklist | N | |
| Rating | picklist | N | |
| NumberOfEmployees | simple | N | |
| AnnualRevenue | simple | N | |
| Description | simple | N | |
| Website | simple | N | |
| **Status** | picklist | N (explícito del pedido) | Debe quedar en el valor equivalente a **"New"** — confirmar el valor exacto del picklist en el schema |

Relacionados: mínimo 6 actividades de distintos tipos (ver "Actividades" más abajo), `WhoId` = el Lead.

---

## Contact (3 en total)

Los 3 se relacionan a la Account creada (`AccountId`).

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| LastName | simple | T | |
| AccountId | lookup | N | La Account creada |
| FirstName | simple | N | |
| Email | simple | N | |
| Phone | simple | N | |
| Title | simple | N | |

**Contact #1 (homónimo del Lead)**: mismo `FirstName`/`LastName` que el Lead, pero con `Phone` y `Email` ajustados a propósito para esquivar las reglas de duplicados del org — ver `duplicate-workaround.md`. Es intencional, no un error.

**Contact #2 y #3**: personas nuevas, coherentes con la temática (p. ej. otros roles en la misma empresa ficticia).

---

## Opportunity (3 relacionadas a la Account; 1 se profundiza)

Las 3 iniciales, con campos mínimos:

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| Name | simple | T | |
| AccountId | lookup | T | La Account creada |
| StageName | picklist | T | Valor real del schema |
| CloseDate | simple | T | |
| Amount | simple | N (explícito del pedido) | En **dólares** |

**La Opportunity elegida** (una de las 3, a definir en la Fase 4) suma, además de lo anterior, la regla transversal de "todos los campos completos": todo campo `createable` del objeto se completa con datos coherentes. Tres de esos campos son pedido explícito del usuario, no solo la regla transversal:

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| Description ("Descripción") | simple | N (explícito del pedido) | 2-4 líneas coherentes con la temática y la etapa (`StageName`) |
| NextStep ("Siguiente paso") | simple | N (explícito del pedido) | Texto breve y accionable, coherente con la etapa elegida |
| CampaignId ("Origen de la campaña principal") | lookup | N (explícito del pedido) | Debe apuntar a la Campaign **existente** llamada exactamente "All Email Marketing" — resolver su Id por SOQL en la Fase 2 (`sf-cli-patterns.md` sección 3c), nunca crearla ni inventar el Id. Si no existe en el org, avisar antes de escribir |
| Pricebook2Id | lookup | T ⚠ resolver en runtime | Solo obligatorio en orgs con "Enable custom pricebooks"/multi-pricebook, pero setearlo siempre en la Opportunity elegida (mismo Pricebook usado en sus `OpportunityLineItem`) **antes** de insertar los line items — si no, el insert puede fallar pidiendo elegir price book primero (confirmado en corrida real, 2026-08-19) |

Suma también:

- Mínimo 6 actividades, 1 de cada tipo si el schema lo permite (ver "Actividades").
- Mínimo 3 `OpportunityLineItem` (productos) que tengan sentido para la temática — ver más abajo.
- Una `Quote` asociada (ver "Quote"), con `QuoteLineItem` que espejan estos mismos productos.
- La 7ma `Order` ligada a esta Opportunity (ver sección "Order", subsección "Order ligada a la Opportunity elegida") usa los mismos productos elegidos acá.

### OpportunityLineItem (≥3, sobre la Opportunity elegida)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| OpportunityId | lookup | T | |
| Product2Id / PricebookEntryId | lookup | T | Elegir del Pricebook estándar del org — nunca inventar Ids de producto |
| Quantity | simple | T | |
| UnitPrice | simple | T | Coherente con `Amount` de la Opportunity, en USD |

⚠ Si el org no tiene productos en el Pricebook estándar que encajen con la temática, avisar al usuario antes de forzar productos genéricos — no inventar `Product2` nuevos sin confirmación (eso sería crear otro objeto fuera de alcance).

---

## Order (7 en total, relacionadas a la Account)

Las 6 primeras son genéricas; la 7ma está ligada a la Opportunity elegida. Comparten todos los campos base:

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| AccountId | lookup | T | |
| EffectiveDate | simple | T | |
| Status | picklist | T | Valor real del schema (frecuentemente arranca en "Draft") |
| Pricebook2Id | lookup | T ⚠ resolver en runtime | Solo si el org tiene Order Products habilitado |
| "Asunto" (campo pedido) | simple ⚠ resolver en runtime | N (explícito del pedido) | Casi seguro **custom** — Order estándar no trae "Subject". Buscar por Label en `describe`. Ahí va el **nombre de la orden**. |
| Amount / TotalAmount | simple ⚠ resolver en runtime | N (explícito del pedido) | Verificar si es un campo directo editable o un rollup de `OrderItem`. Si es rollup, cargar `OrderItem` cuya suma dé el monto en **USD**; si es editable directo, setearlo directo. |

### Order ligada a la Opportunity elegida (la 7ma, pedido explícito)

Mismos campos base de arriba, más:

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| "Asunto" / Description | simple | N (explícito del pedido) | Debe referenciar el **nombre de la Opportunity elegida**, para que la relación sea explícita para quien mira el registro |
| OrderItem | — | N (explícito del pedido) | Los **mismos productos** (`Product2Id`/`PricebookEntryId`) elegidos para la `OpportunityLineItem` de la Opportunity elegida — no elegir productos distintos |

⚠ El objeto `Order` estándar **no siempre** trae un lookup directo a `Opportunity` — depende del org. **No asumir que no existe**: confirmar en el describe de la Fase 2 buscando campos cuyo `referenceTo` incluya `Opportunity` (puede ser el propio `OpportunityId` estándar, habilitado en algunos orgs — confirmado en corrida real, 2026-08-19, org `demos2026`). Si existe, usarlo directo además de la referencia textual. Si no existe, la relación queda dada solo por el contenido (misma Account, mismos productos y referencia textual al nombre de la Opportunity) — aclararlo en el reporte final si aplica.

⚠ **Patrón seguro de Status**: insertar las 7 Orders siempre en `Status='Draft'`, cargar sus `OrderItem`, y recién después hacer un `update` a los `Status` finales objetivo. Ver `sf-cli-patterns.md` sección 5.

Lleva además su propio archivo adjunto — ver "Archivos adjuntos" más abajo.

---

## Case (3, relacionados a la Account)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| AccountId | lookup | T | |
| Status | picklist | T | Valor real del schema |
| Origin | picklist | N | |
| Subject | simple | N | Coherente con la temática |
| Description | simple | N | |
| Priority | picklist | N | |
| BusinessHoursId | lookup ⚠ resolver en runtime | T en orgs con Entitlement/Business Hours habilitado | No asumir que es opcional — el describe puede marcarlo `nillable=false`. Si lo es, resolver `SELECT Id, Name, IsDefault FROM BusinessHours WHERE IsActive=true` y usar el `IsDefault=true` (confirmado en corrida real, 2026-08-19) |

---

## Visit (3, relacionadas a la Account — objeto estándar)

`Visit` es un objeto **estándar** de Salesforce (API name `Visit`, sin `__c`), disponible cuando el org tiene habilitado Field Service / Consumer Goods Cloud — no es un custom object a buscar por Label. Aun así, **confirmar en la Fase 2 que el describe de `Visit` responde** (si el org no tiene esa nube/feature habilitada, el describe falla con `INVALID_TYPE` — en ese caso avisar al usuario antes de escribir nada, no inventar un objeto alternativo).

⚠ **Confirmado en corrida real (2026-07-29, org `sdo-sales`)**: `Visit` **no** tiene campos `Subject` ni `Description` — el compilador de Apex tira `Field does not exist`. Tampoco se relaciona a la Account por un lookup técnicamente obligatorio: el campo requerido es `PlaceId`, que **no acepta un Account directo** (`referenceTo`: `Address`, `ContactPointAddress`, `Location`, `RetailStore`).

### Prerrequisito: RetailStore (1, reusado por las 3 Visit)

Como esta Account no va a tener necesariamente un `RetailStore` previo, crear **uno solo** y reusar su Id como `PlaceId` en las 3 Visit (patrón confirmado con el usuario — no crear un RetailStore por Visit):

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| Name | simple | T | p. ej. "\<Nombre de la Account\> - Sede \<ciudad\>" |
| AccountId | lookup | T | La Account creada |

### Visit

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| PlaceId | lookup | T | El `Id` del `RetailStore` creado arriba (no un Account ni un Contact) |
| PlannedVisitStartTime | simple | T | Fecha/hora planeada — único campo de fecha técnicamente obligatorio |
| AccountId | lookup | N | Opcional pero recomendado — igual conviene setearlo con la Account, para que la Visit aparezca relacionada directo en su related list |
| Status | picklist ⚠ resolver en runtime | N (explícito del pedido) | Confirmado en la corrida real: valores activos son **`Planned`, `InProgress`, `Completed`, `Abandoned`, `Unscheduled`, `None`, `Error`** (en inglés) — no asumir que existen "Completada"/"Planificada" literales, usar `Completed`/`Planned` salvo que el describe de otro org confirme otros valores |
| PlannedVisitEndTime | simple | N | |
| ActualVisitStartTime / ActualVisitEndTime | simple | N | Solo se completan en las 2 Visit con `Status = Completed`; se dejan vacíos en la planeada |
| InstructionDescription ("Special Instruction") | simple | N | Reemplaza a "Subject" — usar para el propósito/tema de la visita, coherente con la temática elegida |
| StatusRemarks ("Status Remark") | simple | N | Reemplaza a "Description" — notas/resultado de la visita (en las completas) |
| VisitPriority | picklist | N (explícito del pedido) | Completar siempre — valores reales confirmados: `High`/`Medium`/`Low`. Elegir el que tenga más sentido para cada visita (p. ej. mayor prioridad para la que cierra la propuesta) |
| VisitorId ("Visitor") | lookup a User | N (explícito del pedido) | **Siempre el usuario Flavio Coulleri** — resolver su Id por `SELECT Id FROM User WHERE Name='Flavio Coulleri'` (en el org de referencia es `005aj00000Y8vOvAAJ`, pero no hardcodear ese Id entre orgs: volver a resolverlo). Si no existe ningún User con ese nombre en el org, avisar al usuario antes de dejarlo vacío |

Repartir: **2 con `Status = Completed`** (`PlannedVisitStartTime`/`ActualVisitStartTime`/`ActualVisitEndTime` en el pasado, con `StatusRemarks` con el resultado) y **1 con `Status = Planned`** (`PlannedVisitStartTime`/`PlannedVisitEndTime` en el futuro, sin campos `Actual*`). Las 3 con `VisitorId` = Flavio Coulleri y `VisitPriority` completo.

---

## Archivos adjuntos (4 en total, sobre 3 destinos distintos)

Vía `ContentVersion` + `ContentDocumentLink` (patrón estándar moderno; no usar `Attachment` legado salvo que el org no tenga Files habilitado).

| Destino | Cantidad | Título |
|---|---|---|
| Account | 2 | "Facturación …" |
| Order ligada a la Opportunity elegida | 1 | "Facturación …" |
| Quote | 1 | "Cotización …" (pedido explícito, `.txt`) |

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| ContentVersion.Title | simple | N (explícito del pedido) | "Facturación …" o "Cotización …" según el destino (ver tabla arriba) |
| ContentVersion.PathOnClient | simple | T | `.txt` para los 4 (el pedido explícito de la Cotización es `.txt`; usar el mismo tipo para consistencia, salvo que el usuario pida `.pdf` para alguno) |
| ContentVersion.VersionData | simple | T | Contenido de texto plano base64, coherente con el título (p. ej. un detalle de facturación o de cotización ficticio acorde a la temática) |
| ContentDocumentLink.LinkedEntityId | lookup | T | El registro correspondiente según la tabla de destinos (Account, la Order ligada a la Opportunity, o la Quote) |
| ContentDocumentLink.ShareType | picklist | N | `V` (Viewer) por defecto |

---

## Quote (1, sobre la Opportunity elegida)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| Name | simple | T | |
| OpportunityId | lookup | T | La Opportunity elegida |
| Pricebook2Id | lookup | T ⚠ resolver en runtime | Debe coincidir con el Pricebook usado en los `OpportunityLineItem` |
| Status | picklist | N | Valor real del schema |
| ExpirationDate | simple | N | |
| ...resto de campos `createable` | — | N (regla transversal) | "Completa todos los campos posibles" — llenar con datos coherentes |

### QuoteLineItem (≥3, sobre la Quote — espejo de la OpportunityLineItem, pedido explícito)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| QuoteId | lookup | T | |
| Product2Id / PricebookEntryId | lookup | T | **Los mismos productos** (mismo `PricebookEntryId`) que los `OpportunityLineItem` de la Opportunity elegida — no elegir productos distintos ni agregar otros de más. ⚠ A diferencia de `OrderItem`/`OpportunityLineItem`, en `QuoteLineItem` el describe suele marcar **ambos** campos (`Product2Id` y `PricebookEntryId`) como obligatorios — resolver `Product2Id` con `SELECT Id, Product2Id FROM PricebookEntry WHERE Id IN (...)` antes de armar los registros, no asumir que se autocompleta (confirmado en corrida real, 2026-08-19) |
| Quantity | simple | T | Igual a la cantidad del `OpportunityLineItem` correspondiente |
| UnitPrice | simple | T | Igual al `UnitPrice` del `OpportunityLineItem` correspondiente |

Relacionados: mínimo 6 actividades, 1 de cada tipo si el schema lo permite (`WhatId` = la Quote); 1 archivo adjunto ("Cotización …" — ver "Archivos adjuntos").

---

## Actividades (Task / Event) — aplica a Lead, Account, Opportunity elegida y Quote

Cada uno de estos 4 registros necesita **mínimo 6 actividades**, con la mayor variedad de tipo posible (llamada, reunión, email). Total mínimo: 24 actividades.

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| Subject | simple | T | Coherente con la temática y la etapa del proceso comercial |
| WhoId | lookup | N | Para actividades del Lead: el propio Lead. Para las de Account/Opportunity/Quote sin contacto puntual, puede omitirse y usar solo `WhatId` |
| WhatId | lookup | T | El registro relacionado (Account / Opportunity / Quote) — para el Lead usar `WhoId`, no `WhatId` |
| ActivityDate (Task) / StartDateTime+EndDateTime (Event) | simple | T | Fechas plausibles, escalonadas en el tiempo (no todas el mismo día) |
| Type | picklist | N | Usar los valores reales del schema para variar entre "Llamada"/"Reunión"/"Email" o equivalentes — **no asumir que existen esos 3 valores exactos**, confirmarlo en el describe |
| Status (Task) | picklist | T | |
| Description | simple | N | |

⚠ Si el schema del org no tiene 3 valores de `Type` distintos disponibles, avisar al usuario y usar la mayor variedad posible entre `Task` y `Event` en vez de forzar un tercer tipo inexistente.
