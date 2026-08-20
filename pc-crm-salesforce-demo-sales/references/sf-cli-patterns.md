# Patrones de CLI (Salesforce CLI en Windows)

Mismo patrón que usa `pc-crm-salesforce-user-creator`: en Windows, `sf` vive en una ruta con espacios (`C:\Program Files\sf\bin\sf`), lo que rompe la invocación directa desde bash con SOQL/argumentos complejos. Por eso **siempre** se escribe un `.bat` temporal y se ejecuta vía `cmd //c`, con el output pipeado a `python` para extraer solo lo necesario (nunca volcar JSON crudo).

```bash
cat > /tmp/sf_query.bat << 'EOF'
@echo off
sf data query -q "YOUR SOQL HERE" -o <alias> --json
EOF
cmd //c /tmp/sf_query.bat 2>/dev/null | python -c "
import sys,json
d=json.load(sys.stdin)
# parsear result.records
"
```

Excepción: `sf org list --json` no necesita `.bat` (no tiene SOQL con comas/espacios).

## Bash vs. PowerShell — cuál patrón usar

El workaround `.bat`/`cmd //c` de arriba es necesario **solo cuando se invoca `sf` desde el tool Bash** (git bash) en Windows: ahí el hop bash→cmd.exe mangling rompe comillas/comas del SOQL. **Probado en corrida real (2026-07-29, org `sdo_comercial`)**: si el entorno tiene el tool **PowerShell** disponible, `sf` se invoca **directo**, sin `.bat` ni `cmd //c`, sin problemas de escaping — incluso con SOQL con comillas, comas y subqueries:

```powershell
sf data query -q "SELECT Id, Name FROM Account WHERE Industry='Agriculture' LIMIT 5" -o <alias> --json
```

Para parsear el JSON sin volcar crudo, usar `ConvertFrom-Json` (nativo, sin depender de `python`):

```powershell
$d = sf sobject describe -s Account -o <alias> --json 2>$null | ConvertFrom-Json
$fields = $d.result.fields
$fields | Where-Object { $_.createable -eq $true -and $_.nillable -eq $false } | ForEach-Object { Write-Output "$($_.name) | $($_.label)" }
```

**Nota de parsing**: cuando se redirige la salida de `sf` a un archivo con `Out-File` en PowerShell, el wrapper de warnings de `sf` (actualización de CLI disponible, etc.) puede quedar mezclado antes del JSON real. Para ubicar el inicio del JSON de forma robusta, buscar la línea que es exactamente `{` (no el primer carácter `{` del archivo, que puede aparecer antes dentro del texto de warning):

```powershell
$lines = Get-Content -Path $outFile
$startIdx = -1
for ($i=0; $i -lt $lines.Count; $i++) { if ($lines[$i].Trim() -eq '{') { $startIdx = $i; break } }
$json = ($lines[$startIdx..($lines.Count-1)] -join "`n") | ConvertFrom-Json
```

Regla general: **usar el patrón que soporte el tool disponible en la sesión** (Bash → `.bat`/`cmd`; PowerShell → invocación directa). No asumir de antemano — si ambos tools están disponibles, PowerShell es más simple y evita el hop extra.

---

## 1. Selección de org

```bash
sf org list --json 2>/dev/null | python -c "
import sys,json
d=json.load(sys.stdin)
for t in ['nonScratchOrgs','scratchOrgs']:
    for o in d.get('result',{}).get(t,[]):
        if o.get('connectedStatus')=='Connected':
            print(f\"{o.get('alias','—')} | {o.get('username','—')}\")
"
```

Mostrar solo orgs **Connected**. Preguntar en cuál correr el escenario de demo — nunca asumir la default.

---

## 2. Leer la Account existente (contexto de la Fase 1)

El link que pasa el usuario trae un Id de 15/18 caracteres al final de la URL (`/lightning/r/Account/001.../view`). Extraerlo y consultar:

```bash
cat > /tmp/sf_ctx_account.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Name, Industry, Description, NumberOfEmployees, Website FROM Account WHERE Id='<ACCOUNT_ID>'" -o <alias> --json
BEOF
cmd //c /tmp/sf_ctx_account.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
for r in d.get('result',{}).get('records',[]): print(r)
"
```

Si `Industry`/`Description` vienen vacíos o son poco informativos, y las notas del analista tampoco alcanzan → preguntar directo al usuario sobre qué temática construir (regla de la Fase 1, sin inventar).

---

## 3. Describe de objeto (schema real, nunca hardcodear)

Para cada objeto que el skill va a escribir (Account, Lead, Contact, Opportunity, OpportunityLineItem, Order, Case, Quote, Task, Event, ContentVersion):

```bash
cat > /tmp/sf_describe.bat << 'BEOF'
@echo off
sf sobject describe -s <ObjectApiName> -o <alias> --json
BEOF
cmd //c /tmp/sf_describe.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
fields=d.get('result',{}).get('fields',[])
for f in fields:
    req = f.get('createable') and not f.get('nillable') and not f.get('defaultedOnCreate')
    print(f\"{f['name']} | label={f['label']} | type={f['type']} | createable={f['createable']} | required={req}\")
"
```

Cachear el resultado por objeto en memoria de la corrida (`orgMeta`) — **no volver a describir el mismo objeto dos veces** en la misma ejecución.

### 3a. Resolver un campo custom por Label (Account "Frecuencia de compra", "Campañas respondidas", "Cantidad total de compras"; Order "Asunto")

```bash
cmd //c /tmp/sf_describe.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
target_labels = ['Frecuencia de compra','Campañas respondidas','Cantidad total de compras']
for f in d.get('result',{}).get('fields',[]):
    if f['label'] in target_labels:
        print(f\"{f['label']} -> {f['name']} (type={f['type']})\")
"
```

Si alguna Label no aparece en el describe → **no inventar el API name**. Avisar al usuario que el campo no existe en el org con ese nombre exacto y pedirle el nombre correcto o confirmar que se omite.

**Gotcha de encoding (confirmado en corrida real, 2026-08-19, org `demos2026`)**: al comparar Labels con tildes/ñ (`-eq` exacto) desde un script PowerShell, un mismatch de encoding entre cómo se escribió el script y cómo `sf`/la consola emiten el JSON puede hacer que la comparación falle en falso — el campo existe pero el match da `NOT_FOUND`. Forzar `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` al inicio del script ayuda, pero no siempre alcanza. Patrón más robusto: en vez de comparar el Label completo con `-eq`, filtrar por una **subcadena ASCII-segura** del label con `-match` (p. ej. `-match "ompra"` en vez de `-eq "Frecuencia de compra"`, o `-match "ampa"` en vez de comparar "Campañas respondidas" completo) y listar todos los campos que matchean para inspección visual — evita que un carácter especial mal codificado te haga perder un campo que sí existe.

**Ambigüedad de labels casi-idénticos (confirmado en la misma corrida)**: es común encontrar más de un campo custom cuyo Label difiere solo en mayúscula/minúscula o singular/plural (p. ej. `Frecuencia_de_compra__c` con Label "Frecuencia de compra" vs `Frecuencia_de_Compras__c` con Label "Frecuencia de Compra"). El match debe tratarse como **case-sensitive y exacto** contra lo que pidió el usuario; si el filtro por subcadena devuelve más de un campo, no elegir por criterio propio — mostrar Name + Label exacto + Type de cada candidato y que el usuario confirme cuál usar antes de avanzar a la Fase 3.

**Cuando el Label pedido no existe ni exacto ni por subcadena**: antes de reportarlo como "no existe" sin más alternativas, ampliar la búsqueda a campos (estándar o custom) cuyo Label sea semánticamente cercano — por ejemplo, para "Origen de la campaña principal" en Opportunity, ninguna Label calzaba exacto, pero filtrando por `-match "ampa"` o `-match "rigen"` aparecieron `CampaignId` (Label real "Id. de campaña"), `LeadSource` (Label real "Origen del candidato") y `SourceId` (Label real "Id. de origen"). Presentar esos candidatos con su Label real y su tipo (lookup vs picklist) y dejar que el usuario confirme cuál es el campo correcto — no adivinar ni rendirse.

### 3b. Valores reales de un picklist

```bash
cmd //c /tmp/sf_describe.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
for f in d.get('result',{}).get('fields',[]):
    if f['name']=='<FieldApiName>' and f.get('picklistValues'):
        for pv in f['picklistValues']:
            if pv.get('active'): print(pv['value'])
"
```

Usar esto para: `Lead.Status` (confirmar el valor equivalente a "New"), `Account.Industry`/`Type`, `Opportunity.StageName`, `Order.Status`, `Case.Status/Origin/Priority`, `Task.Type`, `Quote.Status`.

### 3c. Campaign fija para "Origen de la campaña principal" (Opportunity elegida)

El pedido fija ese campo en la Campaign existente **"All Email Marketing"** — nunca crearla, solo resolver su Id:

```bash
cat > /tmp/sf_campaign.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Name FROM Campaign WHERE Name='All Email Marketing' LIMIT 1" -o <alias> --json
BEOF
cmd //c /tmp/sf_campaign.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
recs=d.get('result',{}).get('records',[])
print(recs[0]['Id'] if recs else 'NOT_FOUND')
"
```

Si devuelve `NOT_FOUND`, avisar al usuario antes de escribir la Opportunity elegida — no dejar el campo en blanco en silencio ni crear la Campaign sin que el usuario lo pida explícitamente.

### 3d. Confirmar que el objeto estándar `Visit` está disponible

`Visit` es un objeto **estándar** de Salesforce (no custom, sin `__c`) que viene con Field Service / Consumer Goods Cloud — no hace falta buscarlo por Label, pero sí confirmar que el org lo tiene habilitado antes de escribir sobre él:

```bash
cat > /tmp/sf_describe_visit.bat << 'BEOF'
@echo off
sf sobject describe -s Visit -o <alias> --json
BEOF
cmd //c /tmp/sf_describe_visit.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
if d.get('status')==0:
    print('OK — Visit disponible')
else:
    print('NO DISPONIBLE:', d.get('message'))
"
```

Si el describe falla (típicamente `INVALID_TYPE`), el org no tiene la nube/feature que trae `Visit` habilitada. En ese caso, **avisar al usuario antes de escribir nada** — no inventar un objeto custom alternativo (`Visita__c` u otro) sin que el usuario lo pida explícitamente. Si el describe responde, seguir el patrón normal de la sección 3 para resolver los valores reales del picklist `Status` (equivalentes a "Completada"/"Planificada").

### 3e. Resolver el User fijo para `Visit.VisitorId` ("Flavio Coulleri")

Pedido explícito: el `Visitor` de las 3 Visit siempre debe ser Flavio Coulleri, no el usuario que corre el script. Resolver su Id por nombre — **no hardcodear el Id entre orgs**, cada org tiene un Id distinto:

```bash
cat > /tmp/sf_user_visitor.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Name, IsActive FROM User WHERE Name='Flavio Coulleri'" -o <alias> --json
BEOF
cmd //c /tmp/sf_user_visitor.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
recs=d.get('result',{}).get('records',[])
print(recs[0]['Id'] if recs else 'NOT_FOUND')
"
```

Si devuelve `NOT_FOUND`, avisar al usuario antes de escribir las Visit — no dejar `VisitorId` en blanco en silencio ni asignarlo a otro User por defecto.

### 3f. Gotchas de campos específicos confirmados en corrida real (2026-08-19, org `demos2026`)

No asumir ninguno de estos sin describe — cada uno depende de la configuración del org:

- **`Order.OpportunityId`**: el mapa de escritura asumía que `Order` estándar no trae lookup directo a `Opportunity`. En un org con esa relación habilitada, el describe de `Order` sí trae un campo `OpportunityId` createable (buscar en el describe los campos cuyo `referenceTo` incluya `Opportunity`, no solo por nombre). Si existe, usarlo directo para la 7ma Order en vez de depender solo de la referencia textual en "Asunto"/Description.
- **`Case.BusinessHoursId`**: en orgs con Entitlement Process/Business Hours habilitado puede ser **técnicamente obligatorio** (`createable=true`, `nillable=false`) aunque no esté en el mapa de escritura original. Si el describe de `Case` lo marca así, resolver el `BusinessHours` default antes de insertar los 3 Case: `SELECT Id, Name, IsDefault FROM BusinessHours WHERE IsActive = true` y usar el que tenga `IsDefault=true` (o el más genérico, p. ej. "24/7 ...").
- **`QuoteLineItem.Product2Id`**: a diferencia de `OrderItem`/`OpportunityLineItem` (donde `Product2Id` suele ser opcional si se setea `PricebookEntryId`), en `QuoteLineItem` el describe puede marcar **ambos** como obligatorios. Resolver `Product2Id` con una consulta a `PricebookEntry` (`SELECT Id, Product2Id FROM PricebookEntry WHERE Id IN (...)`) antes de armar los `QuoteLineItem`, no asumir que se autocompleta.
- **`Opportunity.Pricebook2Id`**: si el org tiene "Enable custom pricebooks" u orgs multi-pricebook, hay que setear `Pricebook2Id` en la Opportunity elegida (mismo Id del Pricebook estándar usado en sus `OpportunityLineItem`) **antes** de insertar esos line items — si no, el insert puede fallar pidiendo elegir un price book primero. Setearlo directo en la creación de la Opportunity es más simple que hacerlo en un update aparte.

---

## 4. Pricebook y productos (para OpportunityLineItem y Quote)

```bash
cat > /tmp/sf_pricebook.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Product2Id, Product2.Name, UnitPrice FROM PricebookEntry WHERE Pricebook2.IsStandard=true AND IsActive=true" -o <alias> --json
BEOF
cmd //c /tmp/sf_pricebook.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
for r in d.get('result',{}).get('records',[]):
    print(f\"{r['Id']} | {r['Product2']['Name']} | {r['UnitPrice']}\")
"
```

Elegir del listado real los ≥3 productos más coherentes con la temática. Si ninguno encaja, avisar al usuario antes de forzar productos genéricos (ver `write-map.md`).

---

## 5. Inserción (Apex anónimo, mismo patrón que `pc-crm-salesforce-user-creator`)

Un único script Apex por lote de objetos con la misma dependencia (p. ej. primero Account+Lead, después todo lo que depende de sus Ids). Usar `Database.insert(records, false)` para permitir éxito parcial y reportar errores registro por registro — nunca dejar que un registro con error tumbe todo el lote.

**Gotcha probado (2026-07-29)**: si se define una clase helper dentro del mismo script de Apex anónimo para no repetir el loop de reporte de errores, sus métodos **no pueden ser `static`** — el compilador de Anonymous Apex tira `static can only be used on methods of a top level type`. Usar un método de instancia y crear el helper una sola vez al principio del script:

```apex
public class DemoUtil {
    public void report(String label, List<Database.SaveResult> results) {
        Integer ok = 0, fail = 0;
        for (Database.SaveResult r : results) {
            if (r.isSuccess()) { ok++; }
            else { fail++; for (Database.Error e : r.getErrors()) System.debug('FAIL ' + label + ': ' + e.getStatusCode() + ' ' + e.getMessage()); }
        }
        System.debug('SUMMARY ' + label + ': ok=' + ok + ' fail=' + fail);
    }
}
DemoUtil du = new DemoUtil(); // instanciar una vez, reusar en todo el script con du.report(...)
```

**Tip de reporte para todo el script en un solo lote**: para poder correr el escenario completo (Account, Lead, actividades, Opportunities, Orders+OrderItems, Cases, adjuntos, Contacts, line items, Quote y sus actividades) en **una sola ejecución de `sf apex run`** en vez de un round-trip por objeto, encadenar todo el script en el mismo archivo `.apex` reutilizando los Ids ya insertados (`acc.Id`, `ld.Id`, `opps[0].Id`, etc.) — así se resuelven las dependencias de la Fase 5 sin múltiples invocaciones del CLI. Al final, imprimir los Ids clave con un prefijo grepeable (`System.debug('RESULT_ACCOUNT_ID:' + acc.Id)`) para poder armarlos en la Fase 7 con `Select-String`/regex en vez de parsear todo el log (el log de `sf apex run` incluye ruido de otros procesos del org que también matchean `USER_DEBUG` como substring — p. ej. `DATAWEAVE_USER_DEBUG` — filtrar por el patrón exacto `|USER_DEBUG|` y además por el prefijo propio, `RESULT_`/`SUMMARY`/`FAIL`).

```apex
List<Account> accs = new List<Account>{ new Account(Name='...', Industry='...', /* ... */) };
Database.SaveResult[] results = Database.insert(accs, false);
for (Integer i = 0; i < results.size(); i++) {
    if (results[i].isSuccess()) {
        System.debug('OK:' + results[i].getId());
    } else {
        for (Database.Error e : results[i].getErrors()) {
            System.debug('FAIL:' + e.getStatusCode() + ' ' + e.getMessage());
        }
    }
}
```

Ejecutar con el mismo patrón `.bat`:

```bash
cat > /tmp/sf_run_apex.bat << 'BEOF'
@echo off
sf apex run -f "<absolute-path>.apex" -o <alias> --json
BEOF
cmd //c /tmp/sf_run_apex.bat 2>/dev/null | python -c "
import sys,json
d=json.load(sys.stdin); r=d.get('result',{})
if r.get('success'):
    for line in r.get('logs','').split('\n'):
        if 'USER_DEBUG' in line: print(line.split('USER_DEBUG|')[1])
else:
    print('ERROR:', r.get('compileProblem') or r.get('exceptionMessage'))
"
```

**IMPORTANTE**: el path del `.apex` en el `.bat` debe ser una ruta absoluta de Windows (`C:\Users\...\archivo.apex`), no una ruta Unix.

Orden de lotes (respeta dependencias — ver Fase 5 del SKILL.md):

1. Account
2. Lead
3. Activities de Account y Lead (necesitan los Ids del paso 1-2)
4. Opportunities, las 3 (necesitan el Id de Account) — con esto ya se conoce el Id real de la Opportunity elegida (Fase 4) para los pasos 5, 9 y 10
5. Orders (7: 6 genéricas + 1 con `OrderItem` de los mismos productos elegidos para la Opportunity elegida, y "Asunto"/Description referenciándola), Cases, Visit (3: 2 completas + 1 planeada, objeto estándar — ver sección 3d), 2 archivos adjuntos de la Account
   - **Patrón seguro de Status en Orders**: insertar las 7 Orders siempre con `Status='Draft'` primero, después cargar sus `OrderItem`, y **recién al final** hacer un `update` puntual llevando cada Order a su `Status` objetivo (`Activated`/`Delivered`/`Shipped`/queda en `Draft` la que corresponda). Insertar directo con un `Status` ya "avanzado" (p. ej. `Activated`) y agregar `OrderItem` después corre el riesgo de que el org bloquee la edición de productos en órdenes activadas — el patrón Draft-primero lo evita sin necesidad de saber de antemano si ese lock existe en el org.
6. Contacts (necesitan el Id de Account; el Contact #1 además necesita los datos del Lead ya creado)
7. Archivo adjunto ("Facturación …") sobre la Order del paso 5 ligada a la Opportunity (necesita el Id de esa Order)
8. OpportunityLineItem + actividades sobre la Opportunity elegida (necesitan su Id; los productos elegidos acá son los mismos que ya se usaron en el paso 5)
9. Quote + QuoteLineItem (espejo exacto de los productos del paso 8) sobre la Opportunity elegida (necesita el Id de la Opportunity y de sus `OpportunityLineItem`)
10. Actividades de la Quote + archivo adjunto ("Cotización …") sobre la Quote (necesitan el Id de la Quote)

---

## 6. Verificación post-write

Tras cada lote, re-consultar los registros insertados y confirmar que los campos obligatorios (técnicos + de negocio, según `write-map.md`) persistieron:

```bash
cat > /tmp/sf_verify.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Name, Industry, Phone /* ...resto de obligatorios */ FROM Account WHERE Id='<ID>'" -o <alias> --json
BEOF
cmd //c /tmp/sf_verify.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
r=d['result']['records'][0]
missing=[k for k,v in r.items() if v in (None,'') and k!='attributes']
print('FALTAN:', missing) if missing else print('OK — todos los obligatorios persistieron')
"
```

Si algo obligatorio quedó vacío (drop silencioso por validation rule o FLS) → no dar el registro por bueno. Corregir el valor y reintentar, o escalar al usuario explicando qué campo no pudo persistir y por qué.
