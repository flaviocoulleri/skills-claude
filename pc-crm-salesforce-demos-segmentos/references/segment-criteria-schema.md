# MarketSegment — verified object schema and filter JSON

Confirmed by reading 5 real `MarketSegment` records and the object's `describe` in `sdo-alfa`
(2026-07-27). `MarketSegment` (key prefix `1sg`) is a **standard, fully createable SObject** —
reachable through the plain REST API, no Tooling API and no container dance needed.

## 1. Creating a segment — minimal payload

```
POST /services/data/v{version}/sobjects/MarketSegment
Content-Type: application/json

{
  "Name": "Clientes frecuentes con melt points",
  "Description": "Optional",
  "IncludeCriteria": "<JSON string — see §3, must be a STRING, i.e. escaped JSON inside JSON>"
}
```

`Name` is the only required field on create. Everything else (`SegmentStatus`, `MarketSegmentType`,
`PublishType`, member counts, etc.) is system-defaulted/computed after insert — don't set them.

Write the outer JSON body to a scratch file and POST with `-b "@<path>"` (nested JSON-in-JSON
quoting breaks in PowerShell inline strings) — same rule as `pc-crm-salesforce-demos-marketing`.

**Multi-Data-Space orgs**: `DataSpaceId` is createable and nillable. If the org has more than one
Data Space (check `SELECT DataSpaceId FROM MarketSegment` on existing segments — more than one
distinct value means multi-space), explicitly set `DataSpaceId` to the value used by other segments
built on the same DMO, or the create can silently land in the wrong space. `sdo-alfa` has a single
Data Space and was never observed hitting this.

## 2. Reading back the result

`SegmentStatus` starts `INACTIVE`/`COUNTING` and moves to `ACTIVE` asynchronously (platform-side,
same for API-created and UI-created segments — evaluation is a server-side process triggered on
save, not a UI-only action). Poll `SegmentStatus`, `LastSegmentMemberCount`,
`LastSegmentTotalCount` on the created Id after a short wait; don't block synchronously waiting for
`ACTIVE` — report back to the admin with whatever status is current and let them know it may still
be counting.

There is no confirmed direct-record Lightning URL for a Segment (`MarketSegment` doesn't have a
standard object Tab in `sdo-alfa`, so don't fabricate a `/lightning/r/MarketSegment/{id}/view`
link). Point the admin to: **Data Cloud app → Segments tab → search by the Segment name** instead.

## 3. `IncludeCriteria` — verified filter JSON shape

Value is a JSON **string** (the field is a `textarea`), containing:

```json
{
  "type": "LogicalComparison",
  "operator": "or",
  "filters": [ /* array of comparison objects, see §4 */ ]
}
```

- `operator` is `"or"` or `"and"` — this is the top-level combinator across every `filters` entry.
  Only single-level (flat) `filters` arrays were observed in this org — no confirmed example of
  nested `LogicalComparison` groups (e.g. `(A AND B) OR C`). If the admin needs nested grouping,
  treat it as unverified and fall back to building it by hand in the Segment UI.
- Every filter's `subject.objectApiName` in the base case is the **DMO you're segmenting on**
  (`ssot__Account__dlm` for Account). A field on a *related* DMO is possible via `path`/`joinPath`
  (see the "Farmacias de Santiago" example in §5) but that's a more advanced case — default to
  direct fields on the base DMO unless the admin explicitly asks to filter through a relationship.

`ExcludeCriteria` uses the exact same shape as `IncludeCriteria`, just for the exclusion set. All 5
real segments in this org had `ExcludeCriteria: null` — untested, but there's no reason to expect a
different shape from `IncludeCriteria` given they're the same field type on the same object.

## 4. Comparison types — verified operator vocabulary

| Field business type | Comparison `type` | Value key | Verified operators | Example |
|---|---|---|---|---|
| NUMBER | `NumberComparison` | `"value": <number>` (scalar, not array) | `"greater than or equal"` | see §5 |
| TEXT | `TextComparison` | `"values": [<string>, ...]` (**array**, plural key) | `"contains"`, `"equal"` | see §5 |
| DATE / DATE_TIME | `DateComparison` | `"value": [<"YYYY-MM-DD">]` (array, singular key) | `"after"` | see §5 |

Every comparison object also needs: `"path": null, "joinPath": null, "selfReference": false,
"subject": {"objectApiName": "...", "fieldApiName": "..."}, "subjectFieldDataType": "<matches
field's DataType from ssot/metadata, e.g. NUMBER/STRING/DATE_TIME>",
"subjectFieldBusinessType": "<matches the field's businessType>", "subjectFieldSourceType":
"DIRECT"`. `businessTypeArgument` was `null` in every example seen.

**Not verified in this org — no real example existed to confirm against** (only 5 segments total,
none used these): Picklist fields, Checkbox/Boolean fields, MultiPicklist fields. Notable hint:
Salesforce `Checkbox` fields showed up in the DLO schema (`Account_Home__dll`) typed as
`STRING` (e.g. `IsActive__c`, `IsBuyer__c`), not `BOOLEAN` — so a Boolean condition may actually be
a `TextComparison` with `"values": ["true"]` or `["false"]`, but **this is inference, not a
confirmed example**. Before building a filter on a Picklist or Checkbox field: either find a real
segment in the target org that already filters on one and copy its shape, or tell the admin you
can't verify that specific condition's JSON and offer to create the segment with the
verified conditions only, letting them add the Picklist/Checkbox condition by hand in Setup.

## 5. Full real examples (verbatim, from `sdo-alfa`)

**"Clientes frecuentes con melt points"** — 3-condition OR, Number + Number + Date:

```json
{"type":"LogicalComparison","operator":"or","filters":[
  {"type":"NumberComparison","path":null,"joinPath":null,"subject":{"objectApiName":"ssot__Account__dlm","fieldApiName":"Melt_Points__c"},"selfReference":false,"operator":"greater than or equal","businessTypeArgument":null,"subjectFieldDataType":"NUMBER","subjectFieldBusinessType":"NUMBER","subjectFieldSourceType":"DIRECT","value":200},
  {"type":"NumberComparison","path":null,"joinPath":null,"subject":{"objectApiName":"ssot__Account__dlm","fieldApiName":"Cantidad_de_compras__c"},"selfReference":false,"operator":"greater than or equal","businessTypeArgument":null,"subjectFieldDataType":"NUMBER","subjectFieldBusinessType":"NUMBER","subjectFieldSourceType":"DIRECT","value":5},
  {"type":"DateComparison","path":null,"joinPath":null,"subject":{"objectApiName":"ssot__Account__dlm","fieldApiName":"ssot__LastActivityDate__c"},"selfReference":false,"operator":"after","subjectFieldDataType":"DATE","subjectFieldBusinessType":"DATE","subjectFieldSourceType":"DIRECT","value":["2026-04-01"]}
]}
```

**"Campaña Porto Alegre"** — Number + Text(`contains`) + Date:

```json
{"type":"LogicalComparison","operator":"or","filters":[
  {"type":"NumberComparison","path":null,"joinPath":null,"subject":{"objectApiName":"ssot__Account__dlm","fieldApiName":"Cantidad_de_viajes__c"},"selfReference":false,"operator":"greater than or equal","businessTypeArgument":null,"subjectFieldDataType":"NUMBER","subjectFieldBusinessType":"NUMBER","subjectFieldSourceType":"DIRECT","value":2},
  {"type":"TextComparison","path":null,"joinPath":null,"subject":{"objectApiName":"ssot__Account__dlm","fieldApiName":"Destino_preferencia__c"},"selfReference":false,"operator":"contains","subjectFieldDataType":"TEXT","subjectFieldBusinessType":"TEXT","subjectFieldSourceType":"DIRECT","values":["Porto Alegre"]},
  {"type":"DateComparison","path":null,"joinPath":null,"subject":{"objectApiName":"ssot__Account__dlm","fieldApiName":"ssot__LastActivityDate__c"},"selfReference":false,"operator":"after","subjectFieldDataType":"DATE","subjectFieldBusinessType":"DATE","subjectFieldSourceType":"DIRECT","value":["2026-04-01"]}
]}
```

**"Farmacias de Santiago"** — Text(`contains`) on the base DMO + Text(`equal`) through a
relationship (`path`/`joinPath` populated) — advanced case, shown for reference only:

```json
{"type":"LogicalComparison","operator":"or","filters":[
  {"type":"TextComparison","path":null,"joinPath":null,"subject":{"objectApiName":"ssot__Account__dlm","fieldApiName":"ssot__Name__c"},"selfReference":false,"operator":"contains","subjectFieldDataType":"TEXT","subjectFieldBusinessType":"TEXT","subjectFieldSourceType":"DIRECT","values":["Farmacia"]},
  {"type":"TextComparison","path":[[{"objectApiName":"ssot__Account__dlm","fieldApiName":"ssot__BillContactAddressId__c"},{"objectApiName":"ssot__ContactPointAddress__dlm","fieldApiName":"ssot__Id__c"}]],"joinPath":[[{"objectApiName":"ssot__Account__dlm","fieldApiName":"ssot__BillContactAddressId__c"},{"objectApiName":"ssot__ContactPointAddress__dlm","fieldApiName":"ssot__Id__c"}]],"subject":{"objectApiName":"ssot__ContactPointAddress__dlm","fieldApiName":"ssot__CityId__c"},"selfReference":false,"operator":"equal","subjectFieldDataType":"TEXT","subjectFieldBusinessType":"TEXT","subjectFieldSourceType":"DIRECT","values":["Santiago"]}
]}
```
