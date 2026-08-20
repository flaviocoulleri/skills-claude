---
name: pc-crm-salesforce-demos-field-service
metadata:
  version: 1.0.0
  last_modified: 2026-07-29
description: >
  Crea un escenario de demo de Salesforce Field Service (FSL) — Account con
  Asset, Case, Work Order con line items, Service Appointments con técnico
  asignado y evidencia de servicio — para una reunión comercial o POC de
  Field Service. Activar con "arma una demo de Field Service", "escenario de
  FSL para la reunión con...", "crea un Work Order de ejemplo", "pobláme el
  org con data de Field Service", "mostrar Service Appointments con técnico
  asignado", o pedidos de Case/Work Order/Service Appointments realistas para
  un cliente. Pide para quién es la demo, notas del analista y el link de la
  cuenta del cliente para inferir la temática; si no alcanza, pregunta
  directo. Resuelve objetos y campos contra el schema real, nunca los
  inventa — reutiliza Service Territory, Service Resource y Work Type
  existentes, sin crearlos. Si Field Service no está habilitado, avisa antes
  de escribir. Entrega links de Account, Case, Work Order y Service
  Appointment. Español e inglés.
---

<!-- Changelog
1.0.0 (2026-07-29): Primera versión, bajo la convención pc-[área]-[sistema]-[objeto]-[acción] con excepción de nomenclatura autorizada explícitamente por el usuario (ver nota abajo).
-->

<!--
Nota de gobernanza de nombre: el nombre `pc-crm-salesforce-demos-field-service` no
pasa `validate_name.py` (el token final "service" no es una acción de la tabla:
creator/builder/generator/...). Es deuda de nomenclatura aceptada a propósito, para
alinear con la familia `pc-crm-salesforce-demo-sales` / `demos-marketing` /
`demos-segmentos` (todas legacy, tampoco pasarían la validación estricta hoy). El
usuario confirmó explícitamente mantener este nombre pese a una alternativa
compliant propuesta (mismo objeto/acción, orden de tokens distinto). Si el
catálogo migra alguna vez toda la familia `demo(s)-*` a un patrón compliant, este
skill debería migrar junto con sus hermanos, no por separado.
-->

# SF Demos Field Service

Arma un escenario de demo completo e interrelacionado de **Salesforce Field Service** — Account con Asset instalado, Contacto de sitio, Case, Work Order con Work Order Line Items, Service Appointments con técnico asignado, actividades y evidencia de servicio adjunta — con datos realistas sobre una temática elegida, para que preventa/ventas lo use frente a un cliente en una demo o POC de FSL.

Este skill **escribe registros en Salesforce**. Sigue el contrato de escritura (Fase 3, gate pre-write, y Fase 6, verificación post-write) sin excepciones — ver `references/write-map.md`. Nunca hardcodea API names de campos custom ni valores de picklist: todo se resuelve contra el schema real del org (`references/sf-cli-patterns.md`).

**Regla de encapsulamiento**: este skill sólo crea *datos* (Account, Contact, Asset, Case, Work Order y sus relacionados). **Nunca crea Service Territory, Service Resource ni Work Type** — son configuración compartida de Field Service (afecta despacho, licencias y calendarios de todo el org, no sólo la demo). Siempre busca y reutiliza los que ya existen; si no hay ninguno disponible, avisa y pregunta cómo seguir en vez de crearlos.

---

## Fase 1 — Contexto y temática

Pide, en un solo mensaje agrupado:

1. **¿Para quién es la demo?** — nombre del cliente/cuenta que va a ver la demo.
2. **Notas del analista** — cualquier texto pegado o adjunto sobre lo que dijo el cliente/analista respecto a la reunión (qué tipo de equipos/activos maneja, si ya usa Field Service, qué quiere ver).
3. **Link de la cuenta del cliente en Salesforce** — la cuenta a la que se le va a mostrar la demo (no la que se va a crear).

Con el link, extrae el Id y consulta la Account real (`references/sf-cli-patterns.md`, sección 2) para leer su industria, descripción y tamaño. Cruza eso con las notas del analista para inferir la temática del escenario: **el dataset de demo debe representar una empresa que instala/opera equipos que requieren mantenimiento o reparación en campo**, coherente con el negocio de esa cuenta (si la cuenta vende software de gestión para clínicas, el escenario de demo puede ser una clínica con equipamiento médico bajo contrato de mantenimiento; si vende para manufactura, una planta con maquinaria industrial).

Si la Account no trae suficiente información (Industry vacío, Description genérico) y las notas tampoco alcanzan, **pregunta directo**: "¿Sobre qué temática/industria y qué tipo de equipo armo el escenario?" — no inventes una temática sin base.

Cierra la fase confirmando en una línea: "Voy a armar el escenario de Field Service sobre [temática], con [tipo de equipo] como activo. ¿Confirmas?" — no avances a la Fase 2 sin ese OK.

---

## Fase 2 — Descubrimiento de schema (org real, nunca inventado)

Antes de proponer un solo valor, describe contra el org conectado (`references/sf-cli-patterns.md`, secciones 1 y 3):

1. Confirma en qué org conectada corre el escenario (`sf org list`).
2. **Confirma que Field Service está habilitado**: describe `WorkOrder`, `WorkOrderLineItem`, `ServiceAppointment`, `AssignedResource`, `ServiceResource`, `ServiceTerritory`. Si alguno falla (`INVALID_TYPE`), el org no tiene Field Service habilitado — avisa al usuario y **detente**, no sigas con un objeto custom inventado (`sf-cli-patterns.md` sección 3d).
3. Describe también Account, Contact, Case, Asset, Task, Event, ContentVersion — los objetos "de datos" que sí vas a crear.
4. Resuelve por **Label** cualquier campo custom que el usuario pida explícitamente (p. ej. un campo de "Contrato de mantenimiento" en Asset o Account). Si no existe con ese nombre exacto, avísalo y pide al usuario el nombre correcto en vez de adivinar.
5. Trae los valores reales de los picklists que vas a usar: `Case.Status`/`Origin`/`Priority`, `Asset.Status`, `WorkOrder.Status`/`Priority`, `WorkOrderLineItem.Status`, `ServiceAppointment.Status` (confirmar los valores equivalentes a "Completado"/"Programado"/"Despachado" — no asumir que vienen en español), `Task.Type`.
6. Trae del Pricebook estándar (`sf-cli-patterns.md` sección 4) los productos disponibles para elegir los que tengan sentido como repuestos/partes de la temática (Work Order Line Items).
7. **Busca configuración de Field Service existente — nunca la crees**:
   - `ServiceTerritory` activos (`IsActive=true`). Si hay más de uno, pregunta cuál usar o propone el más relevante a la temática/ubicación.
   - `ServiceResource` activos (`IsActive=true`, `ResourceType='T'`) que sean miembro (`ServiceTerritoryMember`) del territorio elegido. Este es el "técnico" que se va a asignar a las Service Appointments.
   - `WorkType` existentes (define duración estimada y, si aplica, skills requeridas). Si hay varios, elige el más coherente con la temática; si no hay ninguno, el Work Order se puede crear sin `WorkTypeId` — no lo bloquees por eso, pero avisa que el escenario queda sin ese dato.
   - Si **no hay ningún** `ServiceTerritory` activo o **ningún** `ServiceResource` disponible, **detente y avisa al usuario**: sin al menos un territorio y un recurso activos no se puede asignar ninguna Service Appointment de forma realista. Pregunta si prefiere que se los cree él mismo/el admin del org, o si sigue sin la asignación de técnico (Service Appointments sin `AssignedResource`, aclarado en el reporte final).

Cachea todo esto en memoria de la corrida — no vuelvas a describir el mismo objeto dos veces.

---

## Fase 3 — Plan de escritura (gate pre-write, bloqueante)

Antes de crear un solo registro, presenta un resumen de **todo** lo que se va a crear (y de la configuración existente que se va a reutilizar):

| Objeto | Cantidad | Detalle |
|---|---|---|
| Account | 1 | Nombre propuesto + industria |
| Contact | 2 | Contacto de sitio (solicitante) + responsable de mantenimiento |
| Asset | 2 | Equipos instalados en la Account, coherentes con la temática |
| Case | 1 | Service request que origina el Work Order |
| Work Order | 1 | Sobre la Account, Contact, Asset y Case; `WorkTypeId` si hay uno elegido |
| Work Order Line Item | ≥2 | Repuestos/partes del Pricebook, sobre el Work Order |
| Service Appointment | 3 | 2 completadas (diagnóstico + reparación) + 1 programada (seguimiento/mantenimiento preventivo) |
| Assigned Resource | hasta 3 | Une cada Service Appointment con el Service Resource elegido (Fase 2) — se omite si no hay recurso disponible |
| Actividades (Task/Event) | ≥12 | ≥4 en el Case, ≥4 en el Work Order, ≥4 en la Service Appointment completada de reparación |
| Archivos adjuntos | 2 | "Informe de servicio" sobre la Service Appointment de reparación, "Ficha técnica" sobre uno de los Asset |

**Configuración existente reutilizada** (no se crea, sólo se referencia): Service Territory `<nombre real>`, Service Resource `<nombre real>`, Work Type `<nombre real o "ninguno">`.

Valida campo por campo contra `references/write-map.md`: todo obligatorio (técnico + de negocio) tiene un valor propuesto no vacío. Si falta algo, **no escribas nada** — pide el dato faltante o decide un valor razonable y muéstralo en el resumen para confirmación.

**Espera la confirmación explícita del usuario antes de ejecutar cualquier DML.** Este es un volumen grande de escritura (~25+ registros) — no se ejecuta sin un "sí" puntual.

---

## Fase 4 — Confirmar territorio, recurso y tipo de trabajo

De lo relevado en la Fase 2, confirma con el usuario (o propone y pide OK) cuál `ServiceTerritory`, `ServiceResource` y `WorkType` (si hay) se usan para todo el escenario. Esta elección no se crea — sólo se referencia por Id en el Work Order y las Service Appointments.

---

## Fase 5 — Creación (orden de dependencias)

Ejecuta en lotes, en este orden (`references/sf-cli-patterns.md` sección 5), usando `Database.insert(records, false)` para permitir éxito parcial y reportar cualquier error registro por registro:

1. **Account** — campos de `write-map.md`.
2. **Contacts** (2) relacionados a la Account.
3. **Assets** (2) relacionados a la Account (y a Contact si el objeto lo permite), coherentes con la temática, `Status` = valor real equivalente a "instalado"/activo.
4. **Case** relacionado a la Account, Contact y (si el schema lo permite) al Asset afectado.
5. **Work Order** — a partir del Case: `AccountId`, `ContactId`, `AssetId`, `CaseId`, `WorkTypeId` (si hay uno elegido), `ServiceTerritoryId` (el elegido en la Fase 4), `Status`, `Priority`.
6. **Work Order Line Items** (≥2) sobre el Work Order, con productos reales del Pricebook.
7. **Service Appointments** (3), `ParentRecordId` = el Work Order: 2 con `Status` equivalente a "Completada" (`SchedStartTime`/`ActualStartTime`/`ActualEndTime` en el pasado, una etiquetada como diagnóstico y otra como reparación) y 1 con `Status` equivalente a "Programada" (`SchedStartTime`/`SchedEndTime` en el futuro, sin campos `Actual*`).
8. **Assigned Resource** (hasta 3, una por Service Appointment) uniendo cada Service Appointment con el `ServiceResource` elegido en la Fase 4 — omitir este paso si la Fase 2 confirmó que no hay recurso disponible.
9. **Actividades** sobre el Case (≥4), el Work Order (≥4) y la Service Appointment de reparación (≥4).
10. **2 archivos adjuntos** vía `ContentVersion` + `ContentDocumentLink`: "Informe de servicio" sobre la Service Appointment de reparación, "Ficha técnica" sobre uno de los Asset.

---

## Fase 6 — Verificación post-write (bloqueante)

Para cada registro creado, re-consulta y confirma que los campos obligatorios de `write-map.md` (técnicos + de negocio) persistieron (`references/sf-cli-patterns.md` sección 6). Presta particular atención a los `AssignedResource` (si el `ServiceResource` no era miembro del `ServiceTerritory` elegido, la asignación puede fallar silenciosamente o quedar sin disponibilidad — no des el registro por exitoso sin confirmarlo) y al `WorkOrder.ServiceTerritoryId`. Si algo quedó vacío por una validation rule o FLS que lo dropeó en silencio, **no des el registro por exitoso** — corrígelo o avisa al usuario exactamente qué campo no pudo guardarse y por qué.

---

## Fase 7 — Reporte final

Responde exactamente con este formato (sin texto adicional antes o después salvo que haya errores para reportar):

```
Cuenta: <link>
Case: <link>
Work Order: <link>
Service Appointment (programada): <link>
```

Usa el formato de link real del org: `https://<mydomain>.lightning.force.com/lightning/r/<Object>/<Id>/view`.

Si algún registro falló o quedó incompleto tras la Fase 6, repórtalo antes del bloque de links, sin ocultar el problema. Si no había Service Territory o Service Resource disponibles y el escenario quedó sin técnico asignado, acláralo también acá.

---

## Referencias

- `references/write-map.md` — mapa de escritura completo por objeto (contrato Q07: campos, obligatoriedad técnica/negocio, notas de runtime).
- `references/sf-cli-patterns.md` — patrones de SF CLI en Windows (patrón `.bat`/PowerShell), consultas de schema, Pricebook, búsqueda de configuración FSL existente, inserción por lotes y verificación post-write.
