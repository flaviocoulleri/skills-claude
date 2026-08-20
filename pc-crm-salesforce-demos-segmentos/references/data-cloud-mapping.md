# Data Model — Account field → Data Lake Object → Data Model Object

Facts confirmed by direct inspection of a real Data Cloud tenant (org alias `sdo-alfa`, username
`flavio.coulleri.sdo.alfa@procontacto.com.mx`), 2026-07-27. Anything not explicitly validated here
is marked as such — don't extend the patterns below to field types or objects that weren't tested.

## 1. Where the three layers live

| Layer | What it is | How to find it | Example (sdo-alfa, Account) |
|---|---|---|---|
| Source field | Standard `CustomField` on the CRM object | `FieldDefinition` SOQL / Tooling API, same as `pc-crm-salesforce-field-creator` | `Cantidad_de_compras__c` on `Account` |
| DLO (Data Lake Object) | Raw ingested copy of the CRM object, 1:1 schema mirror, auto-synced by the connector's Data Stream | `ssot/metadata` endpoint, `category: "Profile"`, name ends in `__dll` | `Account_Home__dll` |
| DMO (Data Model Object) | Canonical modeled object Segments are built on | `ssot/metadata` endpoint, `category: "Profile"`, name ends in `__dlm`; standard Account is always `ssot__Account__dlm` | `ssot__Account__dlm` |

**DLOs do not appear in the standard `/sobjects` global describe** — they're invisible to plain
SOQL/Tooling. DMOs for standard objects (prefixed `ssot__`) **do** appear in `/sobjects` and are
directly queryable, but the field-level metadata (including custom DMO fields) is easier to read in
bulk from the `ssot/metadata` endpoint below.

## 2. Discovering the DLO/DMO names for a given org (do this first, every run)

Names are **not** guaranteed to be `Account_Home__dll` in every org — that depends on what the
admin named their Data Stream when they connected the Salesforce CRM source. Always discover live:

```
GET /services/data/v{version}/ssot/metadata
```

This returns `{"metadata": [ {category, name, displayName, primaryKeys, fields: [...]}, ... ]}` —
in `sdo-alfa` this was **766 KB** for 311 objects, so:
- Save the response to a scratch file (`-S <path>` with `sf api request rest`), never print it raw.
- Filter locally (python/jq) for `category == "Profile"` and `"account" in name.lower()`.
- You'll typically see 2-4 hits: the DLO (`*__dll`), the standard DMO (`ssot__Account__dlm`), and
  possibly Identity-Resolution byproducts (`UnifiedssotAccount*__dlm`,
  `UnifiedLinkssotAccount*__dlm`) — **ignore the Unified* ones**, they're the Identity Resolution
  output, not the object you map custom fields onto.
- If more than one plausible DLO shows up (multi-org / multi-source tenants), ask the admin which
  Data Stream/source is the one connected to the Account object they just added fields to.

## 3. Field name transformation: SF custom field → DLO field

Confirmed on 4 independent real fields in `sdo-alfa` (100% match, no exceptions found):

| Salesforce `Account` custom field (API name) | DLO field (`Account_Home__dll`) |
|---|---|
| `Cantidad__c` | `Cantidad_c__c` |
| `Cantidad_de_compras__c` | `Cantidad_de_compras_c__c` |
| `Destino_preferencia__c` | `Destino_preferencia_c__c` |
| `Melt_points__c` | `Melt_points_c__c` |

**Rule**: strip the trailing `__c` from the Salesforce API name, then append `_c__c`.
`{Name}__c` → `{Name}_c__c`. This is the standard CRM-connector ingestion transform (collapses the
double underscore to single, then Data Cloud appends its own `__c` field suffix) — it applies to
any custom field ingested this way, not just these four.

Use this to **predict** the DLO field name before it exists, so you can tell the admin exactly what
to look for when they refresh the Data Stream schema (see SKILL.md Phase 4) — don't make them guess.

## 4. DMO field naming — no fixed formula, admin sets it in the UI

Unlike the DLO transform above, the DMO field's API name is typed/confirmed by hand in the Data
Cloud "New Field" dialog and isn't perfectly deterministic. Real examples from the same org:

| SF field label | SF API name | DMO field (`ssot__Account__dlm`) |
|---|---|---|
| Cantidad de viajes | `Cantidad__c` | `Cantidad_de_viajes__c` (label-based, not copied from the SF API name) |
| Cantidad de compras | `Cantidad_de_compras__c` | `Cantidad_de_compras__c` |
| Destino preferencia | `Destino_preferencia__c` | `Destino_preferencia__c` |
| Melt points | `Melt_points__c` | `Melt_Points__c` (capitalization differs from the SF field) |

**Recommendation to give the admin**: suggest `Title_Case_With_Underscores__c` derived from the
field's label (this matches 3 of 4 real examples and is the DMO's own default auto-suggest
behavior from a label) — but always show it to them before they click Save in Setup, since it's a
manual step you can't execute via API (see §6).

## 5. What's automatable vs. UI-only

| Step | Automatable via API? | Evidence |
|---|---|---|
| Create the Account custom field | **Yes** — Metadata API deploy (`CustomField`), same pattern as `pc-crm-salesforce-field-creator` | Standard, well-trodden |
| Refresh the Data Stream so the DLO picks up the new field | **No** — no working API found | See below |
| Create the DMO field + map it to the DLO field | **No** — no working API found | See below |
| Create a Segment (`MarketSegment`) with filter criteria | **Yes** — standard REST, fully createable object | See `segment-criteria-schema.md` |

**Why DMO field creation / DLO mapping is UI-only in this skill**: the only plausible-looking
writable object for a DLO↔DMO field mapping, `MktDataLakeMapping` (`createable: true` on its
`SourceFieldRef`/`TargetFieldRef` fields per describe), had **zero records** in `sdo-alfa` despite
the org having several real, working custom DMO fields already mapped — meaning the platform does
not actually persist mappings there for the CRM-connector path. There is no `/ssot/*` metadata POST
endpoint that was found/verified to create DMO fields or field mappings. Per this skill family's
rule (see `pc-crm-salesforce-demos-marketing`), never guess a write schema that hasn't been
verified against a real successful call — so these two steps are precise, click-by-click UI
instructions instead (Phase 4 in SKILL.md), using the predicted names from §3/§4 so the admin isn't
guessing either. If a future session finds a verified write path, promote these steps to automated
and update this doc.

## 6. Segment Membership objects (informational, don't touch)

Publishing a Segment on a DMO auto-creates two more DMOs you'll see in `ssot/metadata`:
`{Object}_SM_{timestamp}__dlm` ("{Object} - Latest") and `{Object}_SMH_{timestamp}__dlm`
("{Object} - History"). These are platform-managed, not something this skill creates or edits.
