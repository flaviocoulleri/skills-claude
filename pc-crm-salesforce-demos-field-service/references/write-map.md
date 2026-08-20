# Mapa de escritura (contrato Q07)

Este documento declara, objeto por objeto, qué campos toca el skill y su obligatoriedad. Es la fuente de verdad para el **gate pre-write** (Fase 3 del SKILL.md) y la **verificación post-write** (Fase 6).

Convenciones:

- **Rol**: `simple` (texto/número/fecha), `picklist`, `lookup`.
- **Obligatorio**: `T` = técnico (el schema lo exige: `createable=true`, `nillable=false`, sin `defaultValue`), `N` = de negocio (lo exige este skill aunque el schema lo marque opcional), `—` = opcional real.
- **Valor**: siempre orientativo, **nunca contractual**. Los API names de campos custom y los valores de picklist mandan del schema real (`sf sobject describe`), resuelto en la Fase 2 y cacheado en `orgMeta` para toda la corrida.
- Todo campo marcado `⚠ resolver en runtime` es incierto porque depende de la configuración del org (custom field, feature habilitada, nube activa) — no asumir, describe primero.

## Regla transversal: objetos de configuración de Field Service NUNCA se crean

`ServiceTerritory`, `ServiceResource`, `ServiceTerritoryMember` y `WorkType` **no aparecen** en este mapa de escritura como objetos a crear — este skill sólo los **lee y referencia por Id**. Son configuración compartida del org (despacho, licencias Field Service, calendarios), fuera del alcance de un dataset de demo. Ver la "Regla de encapsulamiento" en `SKILL.md`.

---

## Account (el "cliente potencial" de la demo)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| Name | simple | T | Nombre de una empresa ficticia de la industria elegida |
| Industry | picklist | N | Debe alinear con la temática de la demo |
| Phone | simple | N | |
| NumberOfEmployees | simple | N | |
| Type | picklist | N | p. ej. "Customer"/"Prospect" — valor real del schema |
| Description | simple | N | 2-4 líneas sobre el negocio ficticio y el tipo de equipamiento que opera, coherente con la temática |
| BillingStreet/City/State/PostalCode/Country | simple | N | Dirección de facturación completa |
| ShippingStreet/City/State/PostalCode/Country | simple | N | Dirección de envío/sitio (relevante para Field Service: es donde se hace el servicio) |

Registros relacionados a crear sobre esta Account: 2 Contacts, 2 Assets, 1 Case.

---

## Contact (2 en total, relacionados a la Account)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| LastName | simple | T | |
| AccountId | lookup | N | La Account creada |
| FirstName | simple | N | |
| Email | simple | N | |
| Phone | simple | N | |
| Title | simple | N | p. ej. "Jefe de Mantenimiento", "Encargado de Planta" |

**Contact #1**: quien reporta el problema (solicitante del Case). **Contact #2**: responsable de mantenimiento/facilities del lado del cliente, coherente con la temática.

---

## Asset (2, relacionados a la Account)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| Name | simple | T | Nombre/modelo del equipo, coherente con la temática |
| AccountId | lookup | N (explícito del pedido) | La Account creada |
| ContactId | lookup | N | El Contact responsable de mantenimiento, si el schema lo permite |
| SerialNumber | simple | N | Formato plausible |
| Status | picklist ⚠ resolver en runtime | N | Valor real equivalente a "instalado"/activo |
| InstallDate | simple | N | Fecha pasada plausible |
| Product2Id | lookup | — | Sólo si hay un `Product2` del Pricebook que represente bien el equipo; si no, omitir sin bloquear |
| Description | simple | N | Detalle del equipo y su función en el sitio del cliente |

Uno de los dos Asset es el que queda vinculado al Case/Work Order (el que falla); el otro sólo aporta contexto de "parque instalado" en la cuenta.

---

## Case (1, relacionado a la Account, Contact y Asset)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| AccountId | lookup | T | La Account creada |
| ContactId | lookup | N | El Contact solicitante |
| AssetId | lookup | N (explícito del pedido) | El Asset afectado, si el schema lo permite en Case |
| Status | picklist | T | Valor real del schema |
| Origin | picklist | N | p. ej. "Teléfono"/"Email" — valor real |
| Subject | simple | N | Descripción breve de la falla, coherente con la temática |
| Description | simple | N | Detalle de lo reportado |
| Priority | picklist | N | |

Este Case es el que origina el Work Order (Fase 5, paso 5) — la relación se establece por contenido (mismo Account/Asset) y, si el org tiene un lookup `CaseId` en `WorkOrder` (estándar en orgs con Field Service), por ese lookup directo.

---

## WorkOrder (1, originado desde el Case)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| AccountId | lookup | T | La Account creada |
| ContactId | lookup | N | El Contact solicitante |
| AssetId | lookup | N (explícito del pedido) | El Asset afectado |
| CaseId | lookup | N (explícito del pedido) | El Case creado — confirmar en el describe que `WorkOrder.CaseId` existe (estándar cuando Field Service está habilitado) |
| WorkTypeId | lookup | — | Sólo si la Fase 4 eligió un `WorkType` existente; si no hay ninguno en el org, se omite y se aclara en el reporte final — **nunca se crea uno** |
| ServiceTerritoryId | lookup ⚠ resolver en runtime | N (explícito del pedido) | El `ServiceTerritory` elegido en la Fase 4 — confirmar el nombre real del campo en el describe |
| Status | picklist | T | Valor real del schema |
| Priority | picklist | N | |
| Subject | simple | N | Coherente con el motivo del Case |
| Description | simple | N | |
| StartDate / EndDate | simple | N | Ventana plausible que contenga las fechas de las Service Appointments (Fase 5, paso 7) |

---

## WorkOrderLineItem (≥2, sobre el Work Order)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| WorkOrderId | lookup | T | |
| Product2Id / PricebookEntryId | lookup | T | Elegir del Pricebook estándar del org, repuestos/partes coherentes con el equipo del Asset — nunca inventar Ids de producto |
| Quantity | simple | T | |
| UnitPrice | simple | T | Coherente con precios reales del Pricebook |
| Status | picklist | N | Valor real del schema |

⚠ Si el org no tiene productos en el Pricebook estándar que encajen como repuestos, avisar al usuario antes de forzar productos genéricos — no inventar `Product2` nuevos sin confirmación.

---

## ServiceAppointment (3, `ParentRecordId` = el Work Order)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| ParentRecordId | lookup | T | El Work Order creado |
| ServiceTerritoryId | lookup | N | El mismo territorio elegido en la Fase 4, si el objeto lo requiere para el despacho |
| Status | picklist ⚠ resolver en runtime | N (explícito del pedido) | Confirmar en el describe los valores reales equivalentes a **"Completada"** y **"Programada"**/"Despachada" (suele venir en inglés: "Completed"/"Scheduled"/"Dispatched" — no asumir sin confirmar) |
| SchedStartTime / SchedEndTime | simple | N | Ventana programada |
| ActualStartTime / ActualEndTime | simple | N | Sólo se completan en las 2 Service Appointment con estado "Completada"; vacíos en la programada |
| Subject | simple | N | Una "Diagnóstico", la otra "Reparación", la tercera "Mantenimiento preventivo"/seguimiento |
| Street/City/State/PostalCode/Country | simple | — | Si el objeto no hereda la dirección del Work Order automáticamente, completar con la dirección de la Account |
| Description | simple | N | Notas/resultado de la visita (en las completas) |

Repartir: **2 con el estado equivalente a "Completada"** (`SchedStartTime`/`ActualStartTime`/`ActualEndTime` en el pasado) y **1 con el estado equivalente a "Programada"** (`SchedStartTime`/`SchedEndTime` en el futuro, sin campos `Actual*`).

---

## AssignedResource (hasta 3, une cada Service Appointment con el Service Resource elegido)

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| ServiceAppointmentId | lookup | T | |
| ServiceResourceId | lookup | T | El `ServiceResource` **existente** elegido en la Fase 4 — nunca crear uno nuevo |

⚠ Si el `ServiceResource` elegido no es miembro (`ServiceTerritoryMember`) del `ServiceTerritory` usado en el Work Order/Service Appointment, la asignación puede fallar o quedar sin disponibilidad calculada. Confirmar la membresía en la Fase 2; si no existe, avisar antes de escribir en vez de forzarlo.

Si la Fase 2 confirmó que no hay ningún `ServiceResource` disponible en el org, **omitir este objeto completo** y aclararlo en el reporte final (Fase 7) — las Service Appointment quedan creadas pero sin técnico asignado.

---

## Archivos adjuntos (2 en total, sobre 2 destinos distintos)

Vía `ContentVersion` + `ContentDocumentLink` (patrón estándar moderno; no usar `Attachment` legado salvo que el org no tenga Files habilitado).

| Destino | Cantidad | Título |
|---|---|---|
| Service Appointment de reparación (la 2da "Completada") | 1 | "Informe de servicio …" |
| Asset (el afectado por el Case) | 1 | "Ficha técnica …" |

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| ContentVersion.Title | simple | N (explícito del pedido) | Según destino (ver tabla arriba) |
| ContentVersion.PathOnClient | simple | T | `.txt` para ambos, salvo que el usuario pida otro formato |
| ContentVersion.VersionData | simple | T | Contenido de texto plano base64, coherente con el título (detalle del servicio realizado o ficha técnica del equipo, ficticios pero acordes a la temática) |
| ContentDocumentLink.LinkedEntityId | lookup | T | La Service Appointment o el Asset, según destino |
| ContentDocumentLink.ShareType | picklist | N | `V` (Viewer) por defecto |

---

## Actividades (Task / Event) — aplica a Case, Work Order y la Service Appointment de reparación

Cada uno de estos 3 registros necesita **mínimo 4 actividades**, con la mayor variedad de tipo posible (llamada, reunión, email). Total mínimo: 12 actividades.

| Campo | Rol | Obligatorio | Nota |
|---|---|---|---|
| Subject | simple | T | Coherente con la temática y la etapa del proceso de servicio |
| WhoId | lookup | N | Para actividades del Case: el Contact solicitante. Para las del Work Order/Service Appointment sin contacto puntual, puede omitirse y usar sólo `WhatId` |
| WhatId | lookup | T | El registro relacionado (Case / Work Order / Service Appointment) |
| ActivityDate (Task) / StartDateTime+EndDateTime (Event) | simple | T | Fechas plausibles, escalonadas en el tiempo (no todas el mismo día) |
| Type | picklist | N | Usar los valores reales del schema para variar entre "Llamada"/"Reunión"/"Email" o equivalentes — **no asumir que existen esos 3 valores exactos**, confirmarlo en el describe |
| Status (Task) | picklist | T | |
| Description | simple | N | |

⚠ Si el schema del org no tiene 3 valores de `Type` distintos disponibles, avisar al usuario y usar la mayor variedad posible entre `Task` y `Event` en vez de forzar un tercer tipo inexistente.
