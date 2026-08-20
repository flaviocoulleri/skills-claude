---
name: pc-crm-salesforce-demo-sales
metadata:
  version: 1.7.2
  last_modified: 2026-08-19
description: >
  Crea un dataset completo de demo en Salesforce (Lead, Account, Contactos,
  Opportunities, Órdenes, Casos y Quote) para preparar una reunión comercial.
  Activar cuando el usuario diga "arma una demo de Salesforce", "necesito data
  de demo para la reunión con...", "prepárame un lead y una cuenta para
  mostrarle a...", "crea el escenario de demo", "necesito una oportunidad con
  productos para la demo", "pobláme el org con data de ejemplo", o pida
  construir un Lead, Account, Contact, Opportunity y Quote realistas para
  presentar frente a un cliente. Pide para quién es la demo, notas del
  analista y el link de la cuenta del cliente para inferir la temática; si no
  alcanza, pregunta directamente sobre qué temática construir. Resuelve
  siempre campos custom y picklists contra el schema real del org, nunca los
  inventa. Al finalizar entrega un panel "Sales Cloud" (Home, Lead, Account,
  Opportunity y Quote de la corrida, Forecast y Dashboard) más una sección
  "Cowork" con prompts sugeridos para seguir la gestión. Funciona en español
  e inglés.
---

<!-- Changelog
1.7.2 (2026-08-19): Fase 1 — cuando el cliente da uno o más sitios web en vez del link de Account, ya no alcanza con leer la home: recorrer las pestañas/secciones principales del menú (Nosotros, Productos, Servicios, Industrias, Soluciones, Clientes) con WebFetch antes de inferir la temática, priorizando las secciones que explican el negocio y evitando páginas irrelevantes (blog, legal, careers).
1.7.1 (2026-08-19): Fase 7 suma un resumen narrativo corto (prosa, sin header) antes del panel "Sales Cloud" — cuenta la historia del escenario (quién es el Lead, por qué se interesó según su `LeadSource` real, cómo llegó a la Opportunity elegida, en qué estado quedó la Quote) con los datos reales de la corrida, nunca una plantilla genérica.
1.7.0 (2026-08-19): Rediseño del reporte final (Fase 7) a pedido explícito del usuario — de un bloque plano de 4 links pasa a un panel "Sales Cloud" (Home + Lead/Cuenta/Oportunidad/Quote de la corrida + Forecast + Dashboard, con `###` en vez de `##` para agrupar bajo el título de sección) más una sección "Cowork" con 4 prompts sugeridos para seguir la conversación. Home/Forecast/Dashboard son links **fijos** pedidos por el usuario (pinneados al org de referencia `demos2026`/`pr1782405263810` — avisar si se corre en otro org). Los 4 prompts de Cowork no son plantilla fija: se adaptan a los datos reales de la corrida (nombre de Account, `NextStep` de la Opportunity elegida, si hay o no una Visit planeada a futuro, rango real de `CloseDate`).
1.6.0 (2026-08-19): Corrida real (org `demos2026`, escenario Krontec & Davinco / Minera Los Cóndores). Fase 1: si el usuario no tiene o no quiere pasar el link de la Account cliente, acepta uno o más sitios web de la empresa como fuente alternativa para inferir la temática (WebFetch). Fase 2 punto 3: sumada guía para desambiguar labels custom casi-idénticos (mayúscula/singular-plural) y para no rendirse cuando el label pedido no existe exacto — presentar los candidatos semánticamente más cercanos y confirmar con el usuario en vez de asumir. Sumados a `write-map.md`/`sf-cli-patterns.md`: gotcha de encoding UTF-8 en PowerShell al buscar labels con tildes/ñ; `Order.OpportunityId` puede existir como lookup directo en el org (verificar primero, no asumir que no existe); `Case.BusinessHoursId` puede ser técnicamente obligatorio (resolver el BusinessHours default); `QuoteLineItem.Product2Id` es obligatorio a diferencia de `OrderItem`/`OpportunityLineItem` (resolverlo desde el `PricebookEntry`); `Opportunity.Pricebook2Id` debe setearse en la Opportunity elegida antes de insertar sus `OpportunityLineItem`; patrón seguro de Orders (insertar en `Draft`, cargar `OrderItem`, recién ahí actualizar `Status` final) para evitar bloqueos de edición en órdenes activadas.
1.5.1 (2026-08-12): Rehace el formato del reporte final (Fase 7) a pedido explícito del usuario —
antes era un bloque `Label: link` dentro de un triple backtick (se veía como texto plano en un
recuadro gris); ahora es `## Label` seguido del link en su propia línea, como markdown real
directo en la respuesta, sin fence. Fase 8 (contexto reutilizable) no cambió.
1.5.0 (2026-07-29): Nueva Fase 8 — después del reporte final de links, sumar siempre un bloque de "contexto reutilizable" (temática, Account/Lead/Opportunity/Quote/productos, datos fijos) pensado para que el usuario lo pase directo a otra skill (marketing, field service, etc.) sin repetir la conversación.
1.4.0 (2026-07-29): Las 3 Visit ahora completan siempre `VisitPriority` (High/Medium/Low según corresponda) y `VisitorId` fijo en el User "Flavio Coulleri" (resuelto por nombre en la Fase 2, nunca hardcodeado entre orgs — ver `sf-cli-patterns.md` sección 3e). Aplicado retroactivamente sobre las 3 Visit ya creadas en la corrida de `sdo-sales`.
1.3.2 (2026-07-29): Corrida real (org `sdo-sales`, retrofit sobre Opportunity/Order/Quote/Account existentes de Asocebú). Confirmado: `Visit` no tiene `Subject` ni `Description` (usar `InstructionDescription`/`StatusRemarks`); su lookup técnicamente obligatorio es `PlaceId` (no acepta Account directo — referencia Address/ContactPointAddress/Location/RetailStore), resuelto creando **un solo** `RetailStore` para la Account y reusándolo en las 3 Visit; valores reales de `Visit.Status` confirmados en inglés (`Planned`/`InProgress`/`Completed`/...). También confirmado que `Order.TotalAmount` es un rollup no editable de `OrderItem` (no hardcodear el monto). Ver `references/write-map.md`.
1.3.1 (2026-07-29): Corrección — `Visit` es un objeto **estándar** de Salesforce (Field Service/CG Cloud), no uno a identificar por Label. La Fase 2 ahora solo confirma que el describe de `Visit` responde (si el org no tiene esa nube habilitada, avisa en vez de inventar un custom object) y usa sus campos estándar reales (`AccountId`, `Status`, `PlannedVisitStartTime`/`PlannedVisitEndTime`, `ActualVisitStartTime`/`ActualVisitEndTime`, `Subject`, `Description`).
1.3.0 (2026-07-29): Sumadas 3 Visitas sobre la Account (2 completas + 1 planeada). "Visita" no es un objeto estándar universal, así que la Fase 2 ahora identifica su API name real por Label (Tooling API, ver `sf-cli-patterns.md` sección 3d) antes de describirlo — nunca se asume ni se inventa el objeto o sus campos.
1.2.0 (2026-07-29): Sumado a la Opportunity elegida: Descripción, Siguiente paso y Origen de la campaña principal (fijo en la Campaign existente "All Email Marketing"). Nueva 7ma Order ligada en contenido a la Opportunity elegida (mismos productos + referencia textual), con su propio archivo "Facturación …". La Quote ahora suma QuoteLineItem espejando los productos de la Opportunity y su propio archivo "Cotización …". Ver `references/write-map.md` y `references/sf-cli-patterns.md` sección 3c.
1.1.1 (2026-07-29): Renombrado de pc-crm-salesforce-demo-creator a pc-crm-salesforce-demo-sales. Sin cambios de comportamiento.
1.1.0 (2026-07-29): Corrida real de prueba (org sdo_comercial, escenario Asocebú). Sumado en references/sf-cli-patterns.md: invocación directa de `sf` por PowerShell (sin el workaround `.bat`/`cmd` que solo aplica al tool Bash), parsing robusto de JSON con `ConvertFrom-Json`, el gotcha de `static` en clases helper de Apex anónimo, y el patrón de un solo script encadenado con Ids grepeables por prefijo. Sumado en references/duplicate-workaround.md el fallback probado con `DuplicateRuleHeader.allowSave=true` cuando el ajuste de teléfono/email no alcanza, más la reconexión de lookups huérfanos. Sin cambios de comportamiento/interfaz del skill.
1.0.0 (2026-07-29): Primera versión bajo la convención pc-[área]-[sistema]-[objeto]-[acción].
-->

# SF Demo Creator

Arma un escenario de demo completo e interrelacionado en Salesforce — Lead, Account, Contactos, Opportunities, Órdenes, Casos y Quote — con datos realistas sobre una temática elegida, para que un vendedor o preventa lo use frente a un cliente.

Este skill **escribe registros en Salesforce**. Sigue el contrato de escritura (Fase 3, gate pre-write, y Fase 6, verificación post-write) sin excepciones — ver `references/write-map.md`. Nunca hardcodea API names de campos custom ni valores de picklist: todo se resuelve contra el schema real del org (`references/sf-cli-patterns.md`).

---

## Fase 1 — Contexto y temática

Pide, en un solo mensaje agrupado:

1. **¿Para quién es la demo?** — nombre del cliente/cuenta que va a ver la demo.
2. **Notas del analista** — cualquier texto pegado o adjunto sobre lo que dijo el cliente/analista respecto a la reunión.
3. **Link de la cuenta del cliente en Salesforce** — la cuenta a la que se le va a mostrar la demo (no la que se va a crear).

Con el link, extrae el Id y consulta la Account real (`references/sf-cli-patterns.md`, sección 2) para leer su industria, descripción y tamaño. Cruza eso con las notas del analista para inferir la temática del escenario: **el dataset de demo debe representar una empresa que podría ser cliente del negocio de esa cuenta** (si la cuenta vende software para retail, el escenario de demo es una empresa de retail).

**Si el usuario no tiene o no quiere pasar el link de Salesforce**, acepta como alternativa uno o más **sitios web de la empresa cliente** (p. ej. "no es necesario, mira son estos sitios: ..."). No te quedes solo con la home: **recorré las pestañas/secciones principales del menú de navegación** (típicamente "Nosotros"/"About", "Productos"/"Products", "Servicios"/"Services", "Industrias"/"Industries", "Soluciones", "Clientes"/"Casos de éxito") con WebFetch — primero la home para identificar qué secciones tiene el menú, después cada una de esas secciones relevantes — antes de inferir la temática. Una sola lectura de la home suele quedarse corta (portadas genéricas, poco texto); el detalle real de a qué se dedica la empresa, qué vende y a quién suele estar en esas subpáginas. No hace falta recorrer todo el sitio (footer legal, blog, careers) — priorizar las secciones que expliquen el negocio. Usa esa lectura completa, cruzada con las notas del analista, para inferir la misma relación de negocio del párrafo anterior — el dataset de demo representa un prospecto plausible del negocio real de esa empresa. Si el cliente son varias empresas relacionadas (un grupo, dos razones sociales que operan juntas), aplicá este mismo recorrido a cada una antes de definir la temática.

Si ninguna fuente disponible (Account de Salesforce, sitios web, notas) trae suficiente información, **pregunta directo**: "¿Sobre qué temática/industria armo el escenario?" — no inventes una temática sin base.

Cierra la fase confirmando en una línea: "Voy a armar el escenario sobre [temática]. ¿Confirmas?" — no avances a la Fase 2 sin ese OK.

---

## Fase 2 — Descubrimiento de schema (org real, nunca inventado)

Antes de proponer un solo valor, describe contra el org conectado (`references/sf-cli-patterns.md`, secciones 1 y 3):

1. Confirma en qué org conectada corre el escenario (`sf org list`).
2. Describe Account, Lead, Contact, Opportunity, OpportunityLineItem, Order, Case, Quote, Task, Event, ContentVersion, y el objeto estándar **`Visit`**. Este último requiere Field Service / Consumer Goods Cloud habilitado en el org: si el describe falla (`INVALID_TYPE`), avisa al usuario antes de seguir — no lo reemplaces por un custom object inventado (`sf-cli-patterns.md` sección 3d).
3. Resuelve por **Label** los campos custom pedidos explícitamente: Account → "Frecuencia de compra", "Campañas respondidas", "Cantidad total de compras"; Order → "Asunto"; Opportunity → "Siguiente paso" y "Origen de la campaña principal" (probablemente los estándar `NextStep` y `CampaignId`, pero confirmar el Label exacto en el describe). Si alguno no existe con ese nombre exacto, avísalo y pide al usuario el nombre correcto en vez de adivinar.
   - **Ambigüedad de labels casi-idénticos**: en orgs con muchos campos custom (frecuente en este tipo de org demo compartido) puede haber más de un campo cuyo Label difiere solo en mayúscula o singular/plural (p. ej. "Frecuencia de compra" vs "Frecuencia de Compra"). El match por Label debe ser **case-sensitive y exacto**; si aparece más de un candidato, no elijas por tu cuenta — mostrale ambos al usuario (Name, Label exacto, Type) y que confirme cuál usar (`sf-cli-patterns.md` sección 3a).
   - **Si el Label pedido no existe exacto**: antes de avisar "no existe" sin más, buscá campos (estándar o custom) cuyo Label sea semánticamente cercano (por texto parcial del label, p. ej. "campa"/"origen") y presentalos como candidatos con su Label real y tipo — dejá que el usuario confirme cuál es, en vez de asumir uno o rendirte (`sf-cli-patterns.md` sección 3a).
   - **Gotcha de encoding**: al buscar labels con tildes/ñ desde PowerShell, un mismatch de encoding entre el script y la salida de `sf` puede hacer que una comparación exacta falle en falso aunque el campo exista — ver el workaround en `sf-cli-patterns.md` sección 3a.
4. Trae los valores reales de los picklists que vas a usar: `Lead.Status` (para confirmar el equivalente a "New"), `Account.Industry`/`Type`, `Opportunity.StageName`, `Order.Status`, `Case.Status`/`Origin`/`Priority`, `Task.Type`, `Quote.Status`, y `Visit.Status` (confirmar los valores equivalentes a "Completada"/"Planificada" — no asumir que vienen en español).
5. Trae del Pricebook estándar (`sf-cli-patterns.md` sección 4) los productos disponibles para elegir los que tengan sentido con la temática.
6. Busca la Campaign existente llamada exactamente **"All Email Marketing"** (`sf-cli-patterns.md` sección 3c) para usar su Id en "Origen de la campaña principal" de la Opportunity elegida. Si no existe en el org, avisa al usuario antes de escribir — no crear una Campaign nueva fuera de alcance salvo que lo pida explícitamente.
7. Busca el User llamado exactamente **"Flavio Coulleri"** (`sf-cli-patterns.md` sección 3e) para usar su Id en `VisitorId` de las 3 `Visit` — es el visitante fijo pedido explícitamente, no el usuario que corre el script. Si no existe en el org, avisa antes de escribir.

Cachea todo esto en memoria de la corrida — no vuelvas a describir el mismo objeto dos veces.

---

## Fase 3 — Plan de escritura (gate pre-write, bloqueante)

Antes de crear un solo registro, presenta un resumen de **todo** lo que se va a crear:

| Objeto | Cantidad | Detalle |
|---|---|---|
| Account | 1 | Nombre propuesto + industria |
| Lead | 1 | Nombre de "Persona X" |
| Contact | 3 | Incluido el homónimo del Lead (ver `references/duplicate-workaround.md`) |
| Opportunity | 3 | Nombres tentativos; 1 se va a profundizar — suma Descripción, Siguiente paso y Origen de la campaña principal = "All Email Marketing" |
| Order | 7 | 6 genéricas relacionadas a la Account + 1 ligada en contenido a la Opportunity elegida (mismos productos, referencia textual a su nombre) |
| Case | 3 | Asuntos tentativos |
| Visit | 3 | 2 completas + 1 planeada, relacionadas a la Account vía 1 RetailStore reusado; `VisitorId` = Flavio Coulleri y `VisitPriority` completo en las 3 (objeto estándar, requiere Field Service/CG Cloud habilitado) |
| OpportunityLineItem | ≥3 | Productos elegidos del Pricebook, sobre la Opportunity elegida |
| Quote | 1 | Sobre la Opportunity elegida |
| QuoteLineItem | ≥3 | Espejo exacto de los productos (`PricebookEntryId`, cantidad, precio) de la OpportunityLineItem |
| Archivos adjuntos | 4 | "Facturación …" x2 sobre la Account, "Facturación …" x1 sobre la Order ligada a la Opportunity, "Cotización …" x1 sobre la Quote |
| Actividades (Task/Event) | ≥24 | 6 en Lead, 6 en Account, 6 en la Opportunity elegida, 6 en la Quote |

Valida campo por campo contra `references/write-map.md`: todo obligatorio (técnico + de negocio) tiene un valor propuesto no vacío. Si falta algo, **no escribas nada** — pide el dato faltante o decide un valor razonable y muéstralo en el resumen para confirmación.

**Espera la confirmación explícita del usuario antes de ejecutar cualquier DML.** Este es un volumen grande de escritura (~50+ registros) — no se ejecuta sin un "sí" puntual.

---

## Fase 4 — Elegir la Opportunity a profundizar

De las 3 Opportunities planeadas, define con el usuario (o propone y confirma) cuál es la que se va a completar en detalle, con productos y Quote. El resto queda con los campos mínimos de `write-map.md`.

---

## Fase 5 — Creación (orden de dependencias)

Ejecuta en lotes, en este orden (`references/sf-cli-patterns.md` sección 5), usando `Database.insert(records, false)` para permitir éxito parcial y reportar cualquier error registro por registro:

1. **Account** — campos de `write-map.md`, incluidos los 3 custom resueltos por Label.
2. **Lead** — todos los campos, `Status` = equivalente a "New".
3. **Actividades de Account y Lead** — 6 cada uno, mayor variedad de tipo posible.
4. **3 Opportunities** relacionadas a la Account, con nombres/etapas coherentes con la temática. Con esto ya se conoce el Id real de la Opportunity elegida (Fase 4) para los pasos siguientes.
5. **7 Orders** relacionadas a la Account: 6 genéricas ("Asunto" = nombre de la orden, monto en USD — ver nota sobre `TotalAmount` vs `OrderItem` en `write-map.md`) + 1 ligada a la Opportunity elegida, con los mismos productos del Pricebook que se van a usar en su `OpportunityLineItem` y el "Asunto"/Description referenciando el nombre de esa Opportunity.
6. **3 Cases** relacionados a la Account.
7. **3 `Visit`** relacionadas a la Account (objeto estándar) — primero 1 `RetailStore` (Name + AccountId) reusado como `PlaceId` en las 3: 2 con `Status = Completed` (`PlannedVisitStartTime`/`ActualVisitStartTime`/`ActualVisitEndTime` en el pasado) y 1 `Status = Planned` (`PlannedVisitStartTime`/`PlannedVisitEndTime` en el futuro, sin campos `Actual*`). Las 3 con `VisitorId` = Flavio Coulleri (Fase 2, punto 7) y `VisitPriority` completo.
8. **3 archivos adjuntos** vía `ContentVersion` + `ContentDocumentLink`: 2 ("Facturación …") sobre la Account, 1 ("Facturación …") sobre la Order ligada a la Opportunity del paso 5.
9. **3 Contacts** relacionados a la Account — el primero homónimo del Lead con el ajuste de `references/duplicate-workaround.md`, los otros dos coherentes con la temática.
10. Sobre la **Opportunity elegida**: completar todos los campos restantes (incluidos Descripción, Siguiente paso, y Origen de la campaña principal = Id de la Campaign "All Email Marketing" resuelta en la Fase 2), agregar ≥3 `OpportunityLineItem` con productos reales del Pricebook, y 6 actividades de distintos tipos.
11. **Quote** sobre esa misma Opportunity — todos los campos posibles, ≥3 `QuoteLineItem` que espejen exactamente los productos de la `OpportunityLineItem` del paso 10, 6 actividades de distintos tipos, y 1 archivo adjunto ("Cotización …") sobre la Quote.

---

## Fase 6 — Verificación post-write (bloqueante)

Para cada registro creado, re-consulta y confirma que los campos obligatorios de `write-map.md` (técnicos + de negocio) persistieron (`references/sf-cli-patterns.md` sección 6). Si algo quedó vacío por una validation rule o FLS que lo dropeó en silencio, **no des el registro por exitoso** — corrígelo o avisa al usuario exactamente qué campo no pudo guardarse y por qué.

---

## Fase 7 — Reporte final

Antes del panel, abrí con un **resumen narrativo corto** (3-5 oraciones, prosa, sin header, sin bullets) que cuente la historia del escenario como si se la contaras a un vendedor antes de mostrarle los links: quién es la persona del Lead y su cargo, por qué se interesó (coherente con el `LeadSource` real — formulario web, referido, evento, etc., no siempre "llenó un formulario"), cómo eso avanzó a la Opportunity elegida (monto, qué necesita), y en qué estado quedó (Quote armada, próximo paso). Usar siempre los datos reales de la corrida — nombres, empresa, industria, producto, monto — nunca una plantilla con placeholders genéricos tipo "cierto producto". Después de este párrafo va el panel.

Responde con este formato exacto — **markdown real (`##`/`###`), directo en la respuesta, nunca dentro de un bloque de código con triple backtick** (eso lo muestra como texto plano en un recuadro gris en vez de headers), y sin texto adicional antes o después salvo que haya errores para reportar:

```
## Sales Cloud

### Home
<link fijo>

### Lead
<link de la corrida>

### Cuenta
<link de la corrida>

### Oportunidad
<link de la corrida>

### Quote
<link de la corrida>

### Forecast
<link fijo>

### Dashboard
<link fijo>

## Cowork

<prompt 1>

<prompt 2>

<prompt 3>

<prompt 4>
```

(El bloque de arriba está en triple backtick únicamente para que se lea como plantilla dentro de este documento — la respuesta real al usuario no debe llevar ese fence, tiene que ser markdown renderizado.)

**Sección "Sales Cloud"**: `Lead`/`Cuenta`/`Oportunidad`/`Quote` usan el formato de link real de la corrida (`https://<mydomain>.lightning.force.com/lightning/r/<Object>/<Id>/view`). `Home`, `Forecast` y `Dashboard` son **links fijos, pedidos explícitamente por el usuario** — siempre los mismos, no se resuelven de nuevo en cada corrida:

- Home: `https://<mydomain>.lightning.force.com/lightning/page/home`
- Forecast: `https://<mydomain>.lightning.force.com/lightning/page/forecasting?c__forecastingTypeId=0Dbaj000009xD7JCAU&c__forecastingOwnerId=005aj00000Y5ysnAAB&c__forecastingTerritoryId=000000000000000`
- Dashboard: `https://<mydomain>.lightning.force.com/lightning/r/Dashboard/01Zaj000008MhlfEAC/view?queryScope=userFolders`

Estos 3 links fueron pedidos y fijados para el org de referencia `demos2026` (`pr1782405263810`). Si la corrida se hace en un **org distinto**, avisar al usuario antes de reusarlos tal cual — probablemente no resuelvan a nada válido ahí (distinto `ForecastingType`/`ForecastingOwner`/`Dashboard` Id) y haya que pedirle los 3 nuevos.

**Sección "Cowork"**: 4 prompts en texto plano (sin backticks, uno por línea/párrafo), pensados para que el usuario los copie y continúe la conversación sobre este mismo escenario. **No son una plantilla fija** — adaptalos a lo que realmente se creó en la corrida:

1. Estado del pipeline — mencionar el nombre real de la Account y preguntar por sus Opportunities abiertas (p. ej. "Qué oportunidades tengo abiertas con [Account] y cómo está esa gestión, ponéme al día").
2. Cómo avanzar — si la Opportunity elegida tiene un `NextStep` cargado, referenciarlo en vez de preguntarlo en genérico (p. ej. "Recomendame cómo avanzar rápido [Opportunity] — tiene sentido adelantar [NextStep]?").
3. Visita — **condicional al dato real**: si ya existe una `Visit` con `Status='Planned'` a futuro, formular el prompt para confirmar/prepararla (p. ej. "Tenemos una visita planeada con [Account] el [fecha] — ¿armamos la agenda para esa reunión?"); si no hay ninguna Visit futura, usar la versión original (p. ej. "Tenemos alguna visita programada con ellos? si no tenemos, drafteame un mail para proponerles visitarlos la semana que viene").
4. Reporte de pipeline — pedir un reporte de Opportunities en el rango de `CloseDate` que efectivamente tienen las 3 Opportunities creadas (p. ej. "Armame un reporte de todas las oportunidades en pipeline para [mes/rango real]" en vez de un mes fijo hardcodeado).

Si algún registro falló o quedó incompleto tras la Fase 6, repórtalo antes del bloque de arriba, sin ocultar el problema.

---

## Fase 8 — Contexto reutilizable (para pasar a otra skill)

Después del bloque de links de la Fase 7, agrega **siempre** un bloque adicional, pensado para que el usuario lo copie y se lo pase de contexto a otra skill (p. ej. `pc-crm-salesforce-demos-marketing`, `pc-crm-salesforce-demos-field-service`) sin tener que repetir toda la conversación:

```
--- Contexto de la demo (para reusar en otra skill) ---
Org: <alias> (<instanceUrl>)
Temática/industria: <la definida en la Fase 1, y por qué>
Account demo: <Nombre> (<Id>) — Industry: <valor>
Lead: <Nombre> — <Title/cargo>
Contacts: <Nombre 1 (homónimo del Lead)>, <Nombre 2>, <Nombre 3>
Opportunity elegida: <Nombre> (<Id>) — <StageName>, USD <Amount>
Productos usados (Pricebook <Id>): <Producto 1>, <Producto 2>, <Producto 3>
Quote: <Nombre> (<Id>)
Orders: <cantidad> (6 genéricas + 1 ligada a la Opportunity)
Otros datos fijos: Campaign "All Email Marketing" en Origen de campaña; Visitante fijo de las Visit = Flavio Coulleri
```

Completar cada línea con los valores reales de la corrida (nunca dejar placeholders `<...>` sin resolver). Si algún dato no aplica en esta corrida puntual (p. ej. no se tocaron Visit), omitir esa línea en vez de dejarla vacía.

---

## Referencias

- `references/write-map.md` — mapa de escritura completo por objeto (contrato Q07: campos, obligatoriedad técnica/negocio, notas de runtime).
- `references/duplicate-workaround.md` — regla exacta del ajuste de teléfono/email para el Contact homónimo del Lead.
- `references/sf-cli-patterns.md` — patrones de SF CLI en Windows (patrón `.bat`), consultas de schema, Pricebook, inserción por lotes y verificación post-write.
