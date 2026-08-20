# Patrones de CLI (Salesforce CLI en Windows)

Mismo patrón que `pc-crm-salesforce-demo-sales` y `pc-crm-salesforce-user-creator`: en Windows, `sf` vive en una ruta con espacios (`C:\Program Files\sf\bin\sf`), lo que rompe la invocación directa desde bash con SOQL/argumentos complejos. Por eso, desde el tool Bash, **siempre** se escribe un `.bat` temporal y se ejecuta vía `cmd //c`, con el output pipeado a `python` para extraer solo lo necesario (nunca volcar JSON crudo).

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

El workaround `.bat`/`cmd //c` de arriba es necesario **solo** cuando se invoca `sf` desde el tool Bash (git bash) en Windows. Si el entorno tiene el tool **PowerShell** disponible, `sf` se invoca **directo**, sin `.bat` ni `cmd //c`:

```powershell
sf data query -q "SELECT Id, Name FROM ServiceTerritory WHERE IsActive=true" -o <alias> --json
```

Para parsear el JSON sin volcar crudo, usar `ConvertFrom-Json` (nativo, sin depender de `python`):

```powershell
$d = sf sobject describe -s WorkOrder -o <alias> --json 2>$null | ConvertFrom-Json
$fields = $d.result.fields
$fields | Where-Object { $_.createable -eq $true -and $_.nillable -eq $false } | ForEach-Object { Write-Output "$($_.name) | $($_.label)" }
```

**Nota de parsing**: si se redirige la salida a un archivo con `Out-File`, el wrapper de warnings de `sf` puede quedar mezclado antes del JSON real. Ubicar la línea que es exactamente `{` para encontrar el inicio real del JSON:

```powershell
$lines = Get-Content -Path $outFile
$startIdx = -1
for ($i=0; $i -lt $lines.Count; $i++) { if ($lines[$i].Trim() -eq '{') { $startIdx = $i; break } }
$json = ($lines[$startIdx..($lines.Count-1)] -join "`n") | ConvertFrom-Json
```

Regla general: usar el patrón que soporte el tool disponible en la sesión — no asumir de antemano.

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

Si `Industry`/`Description` vienen vacíos o son poco informativos, y las notas del analista tampoco alcanzan → preguntar directo al usuario sobre qué temática/tipo de equipo construir (regla de la Fase 1, sin inventar).

---

## 3. Describe de objeto (schema real, nunca hardcodear)

Para cada objeto que el skill va a escribir o leer (WorkOrder, WorkOrderLineItem, ServiceAppointment, AssignedResource, ServiceResource, ServiceTerritory, Account, Contact, Asset, Case, Task, Event, ContentVersion):

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

### 3a. Resolver un campo custom por Label

Si el usuario pide un campo custom explícito (p. ej. un campo de "Contrato de mantenimiento"):

```bash
cmd //c /tmp/sf_describe.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
target_labels = ['Contrato de mantenimiento']
for f in d.get('result',{}).get('fields',[]):
    if f['label'] in target_labels:
        print(f\"{f['label']} -> {f['name']} (type={f['type']})\")
"
```

Si alguna Label no aparece en el describe → **no inventar el API name**. Avisar al usuario que el campo no existe en el org con ese nombre exacto y pedirle el nombre correcto o confirmar que se omite.

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

Usar esto para: `Case.Status/Origin/Priority`, `Asset.Status`, `WorkOrder.Status/Priority`, `WorkOrderLineItem.Status`, `ServiceAppointment.Status` (confirmar los valores equivalentes a "Completada"/"Programada"/"Despachada"), `Task.Type`.

### 3c. Confirmar que Field Service está habilitado

`WorkOrder`, `WorkOrderLineItem`, `ServiceAppointment`, `AssignedResource`, `ServiceResource` y `ServiceTerritory` son objetos **estándar** que sólo responden si el org tiene Field Service habilitado — no son custom objects a buscar por Label, pero sí hay que confirmar que el describe responde antes de escribir nada sobre ellos:

```bash
cat > /tmp/sf_describe_wo.bat << 'BEOF'
@echo off
sf sobject describe -s WorkOrder -o <alias> --json
BEOF
cmd //c /tmp/sf_describe_wo.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
if d.get('status')==0:
    print('OK — WorkOrder disponible')
else:
    print('NO DISPONIBLE:', d.get('message'))
"
```

Repetir para cada uno de los 6 objetos. Si alguno falla (típicamente `INVALID_TYPE`), el org no tiene Field Service habilitado. En ese caso, **avisar al usuario y detener el skill** — no inventar objetos custom alternativos.

### 3d. Buscar Service Territory, Service Resource y Work Type existentes (nunca crearlos)

```bash
cat > /tmp/sf_fsl_config.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Name, IsActive FROM ServiceTerritory WHERE IsActive=true" -o <alias> --json
BEOF
cmd //c /tmp/sf_fsl_config.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
for r in d.get('result',{}).get('records',[]): print(f\"{r['Id']} | {r['Name']}\")
"
```

Elegido el territorio, buscar recursos activos que sean miembros de ese territorio:

```bash
cat > /tmp/sf_service_resources.bat << 'BEOF'
@echo off
sf data query -q "SELECT ServiceResource.Id, ServiceResource.Name FROM ServiceTerritoryMember WHERE ServiceTerritoryId='<TERRITORY_ID>' AND ServiceResource.IsActive=true" -o <alias> --json
BEOF
cmd //c /tmp/sf_service_resources.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
for r in d.get('result',{}).get('records',[]): print(f\"{r['ServiceResource']['Id']} | {r['ServiceResource']['Name']}\")
"
```

Y los `WorkType` existentes:

```bash
cat > /tmp/sf_worktypes.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Name, EstimatedDuration FROM WorkType" -o <alias> --json
BEOF
cmd //c /tmp/sf_worktypes.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
for r in d.get('result',{}).get('records',[]): print(f\"{r['Id']} | {r['Name']}\")
"
```

Si `ServiceTerritory` o `ServiceTerritoryMember` no devuelven ningún registro, **detener el skill y avisar al usuario** (regla de la Fase 2 del SKILL.md) — no crear ninguno de estos tres objetos bajo ninguna circunstancia; son configuración compartida del org.

---

## 4. Pricebook y productos (para Asset, WorkOrderLineItem)

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

Elegir del listado real los productos más coherentes con el equipo de la temática (tanto para representar el `Asset.Product2Id` como los repuestos de `WorkOrderLineItem`). Si ninguno encaja, avisar al usuario antes de forzar productos genéricos (ver `write-map.md`).

---

## 5. Inserción (Apex anónimo, mismo patrón que `pc-crm-salesforce-demo-sales`)

Un único script Apex por lote de objetos con la misma dependencia. Usar `Database.insert(records, false)` para permitir éxito parcial y reportar errores registro por registro — nunca dejar que un registro con error tumbe todo el lote.

**Gotcha (heredado de `pc-crm-salesforce-demo-sales`)**: si se define una clase helper dentro del mismo script de Apex anónimo, sus métodos **no pueden ser `static`** — Anonymous Apex tira `static can only be used on methods of a top level type`. Usar un método de instancia, creado una sola vez:

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
DemoUtil du = new DemoUtil();
```

**Tip de reporte para todo el script en un solo lote**: encadenar todo (Account, Contacts, Assets, Case, Work Order, Work Order Line Items, Service Appointments, Assigned Resources, actividades, adjuntos) en el mismo archivo `.apex`, reutilizando los Ids ya insertados (`acc.Id`, `wo.Id`, `sas[0].Id`, etc.) para resolver las dependencias de la Fase 5 en una sola ejecución de `sf apex run`. Imprimir los Ids clave con prefijo grepeable (`System.debug('RESULT_ACCOUNT_ID:' + acc.Id)`) y filtrar por el patrón exacto `|USER_DEBUG|` más el prefijo propio (`RESULT_`/`SUMMARY`/`FAIL`) — el log de `sf apex run` incluye ruido de otros procesos del org.

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
2. Contacts (2, necesitan el Id de Account)
3. Assets (2, necesitan el Id de Account y opcionalmente de Contact)
4. Case (necesita Id de Account, Contact y Asset)
5. Work Order (necesita Id de Account, Contact, Asset, Case, y los Ids del Service Territory/Work Type elegidos en la Fase 4 — estos últimos ya existían, no se insertan)
6. Work Order Line Items (≥2, necesitan el Id del Work Order)
7. Service Appointments (3, necesitan el Id del Work Order como `ParentRecordId`)
8. Assigned Resources (hasta 3, necesitan los Ids de cada Service Appointment y el Id del Service Resource elegido — que ya existía)
9. Actividades sobre Case, Work Order y la Service Appointment de reparación (necesitan sus Ids respectivos)
10. Archivos adjuntos sobre la Service Appointment de reparación y el Asset afectado (necesitan sus Ids)

---

## 6. Verificación post-write

Tras cada lote, re-consultar los registros insertados y confirmar que los campos obligatorios (técnicos + de negocio, según `write-map.md`) persistieron:

```bash
cat > /tmp/sf_verify.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Status, ServiceTerritoryId, WorkTypeId /* ...resto de obligatorios */ FROM WorkOrder WHERE Id='<ID>'" -o <alias> --json
BEOF
cmd //c /tmp/sf_verify.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
r=d['result']['records'][0]
missing=[k for k,v in r.items() if v in (None,'') and k!='attributes']
print('FALTAN:', missing) if missing else print('OK — todos los obligatorios persistieron')
"
```

Para `AssignedResource`, además de verificar que el registro existe, confirmar contra `ServiceTerritoryMember` que el `ServiceResource` usado efectivamente pertenece al territorio del Work Order — si no, el dato quedó guardado pero no representa un despacho realista y hay que avisarlo en el reporte final.

Si algo obligatorio quedó vacío (drop silencioso por validation rule o FLS) → no dar el registro por bueno. Corregir el valor y reintentar, o escalar al usuario explicando qué campo no pudo persistir y por qué.
