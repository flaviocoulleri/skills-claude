---
name: pc-crm-salesforce-demos-segmentos
description: >
  Builds a full Account → Data Cloud Segment demo chain: creates custom field(s) on the standard
  Account object, guides mapping them through to Data Cloud (finding the Account Data Lake Object
  and Data Model Object, predicting/refreshing the field names at each layer), then creates a
  Data Cloud Segment on Account filtered by those fields via the Segmentation REST API. Use this
  skill whenever the user wants a demo/POC Data Cloud segment built from scratch on Account, wants
  to "crear un segmento" with specific fields, or mentions creating fields that need to flow into
  Data Cloud for segmentation. Also trigger on mentions of Data Lake Object, Data Model Object,
  DLO, DMO, ssot__Account__dlm, MarketSegment, IncludeCriteria, Data Stream refresh (Data Cloud),
  or "quiero armar un segmento sobre Account con estos campos". Reverse-engineered from real,
  working segments in a ProContacto demo org (sdo-alfa) via the ssot metadata endpoint and the
  MarketSegment REST object — includes the verified SF-field→DLO→DMO naming transform and the
  exact IncludeCriteria filter JSON. Complements pc-crm-salesforce-field-creator (general field
  governance) and pc-crm-salesforce-demos-marketing (Segment-triggered Flow demos) — this skill is
  the one that actually builds the Segment those flows trigger from.
license: MIT
metadata:
  author: ProContacto
  version: "1.0.0"
  domain: platform
  triggers: Data Cloud segment, crear segmento, Data Lake Object, Data Model Object, DLO, DMO, ssot__Account__dlm, MarketSegment, IncludeCriteria, Data Stream refresh, mapear campo Data Cloud, segmentación sobre Account
  role: expert
  scope: implementation
  output-format: execution
  related-skills: pc-crm-salesforce-field-creator, pc-crm-salesforce-demos-marketing, pc-crm-salesforce-dev-guide
---

<!-- Changelog
1.0.0 (2026-07-27): Primera versión. Basada en exploración real (read-only) de la org sdo-alfa (flavio.coulleri.sdo.alfa@procontacto.com.mx): endpoint ssot/metadata, describe de MarketSegment, y los 5 segmentos reales existentes en la org (Melt Points, Porto Alegre, Farmacias de Santiago). Confirma la fórmula de nombre SF field → DLO field (4/4 casos reales) y el JSON de IncludeCriteria (Number/Text/Date). DMO field creation y DLO field mapping quedan como pasos guiados de UI porque no se encontró/verificó un endpoint de escritura para esos dos pasos — ver references/data-cloud-mapping.md §5.
-->

# Salesforce Data Cloud Segment Demo Builder (Account)

Builds the full chain **Account custom field → Data Cloud Data Lake Object → Data Model Object →
Segment** for demo/POC purposes, scoped to the standard `Account` object. Only the first step
(field creation) and the last step (segment creation) have a verified API — the two middle steps
are Data Cloud Setup UI actions this skill walks the admin through precisely, using predicted field
names so there's no guessing on their end either.

Full technical detail — naming rules, discovery queries, real payloads: `references/data-cloud-mapping.md` and `references/segment-criteria-schema.md`. Read both before executing Phase 3+ the first time in a session.

## Core Workflow

Don't run this silently end-to-end — Phase 4 requires the admin to actually click through Data
Cloud Setup and confirm back before you continue, since there's no API to do it for them.

### Phase 1 — Target org + discover the Data Cloud layer

1. **Confirm the org** (`sf org list` / ask for alias). Must have Data Cloud enabled — the
   discovery in step 2 doubles as that check (no `__dlm`/`__dll` hits at all means Data Cloud isn't
   provisioned here).
2. **Discover the Account DLO and DMO live** — `GET /services/data/v{version}/ssot/metadata`,
   saved to a scratch file, filtered locally for `category == "Profile"` and `"account" in
   name.lower()`. Expect one `*__dll` (the DLO) and `ssot__Account__dlm` (the DMO); ignore any
   `UnifiedssotAccount*`/`UnifiedLinkssotAccount*` hits (Identity Resolution output, not this). If
   more than one plausible DLO turns up, ask the admin which source/Data Stream to target. See
   `references/data-cloud-mapping.md` §1-2.

### Phase 2 — Ask what fields to create (batch, one message)

3. Ask the admin for each field: **Label** and **Type** (Text/Number/Currency/Date/DateTime/
   Picklist/Checkbox/Long Text Area), plus type-specific params (length for Text, precision/scale
   for Number/Currency, values for Picklist). This is the literal ask from the user — don't invent
   fields, don't skip asking the type.
4. Propose the API name as `Title_Case_With_Underscores__c` derived from the label (this matches
   the real custom fields already feeding segments in this org — see
   `references/data-cloud-mapping.md` §4) and show it for confirmation before creating.
5. Flag if the field type is Picklist or Checkbox: mention up front (once, not per-field) that the
   Segment-filter JSON for those types isn't verified yet in this org (§4 of
   `segment-criteria-schema.md`) — the field itself will still be created and mapped fine, only the
   later filter-building step (Phase 5) may need a manual fallback.

### Phase 3 — Create the Account field(s)

6. Generate `.field-meta.xml` per field (same type-mapping table as
   `pc-crm-salesforce-field-creator`, `references/sf-limits-and-validation.md` in that skill) in a
   temporary SFDX project — if the current working directory is already an SFDX project
   (`sfdx-project.json` present), use its `force-app`; otherwise scaffold a minimal one under the
   session scratchpad (`force-app/main/default/objects/Account/fields/`).
7. Deploy: `sf project deploy start --source-dir force-app -o <org>`. Grant FLS via the `PC ADMIN`
   Permission Set (create it if it doesn't exist yet) — reuse the same convention as
   `pc-crm-salesforce-field-creator` rather than inventing a different one.
8. Confirm the field(s) exist: `SELECT QualifiedApiName FROM FieldDefinition WHERE
   EntityDefinition.QualifiedApiName='Account' AND QualifiedApiName IN (...)`.

### Phase 4 — Data Cloud: refresh the Data Stream, create the DMO field, map it (UI-guided)

No verified write API exists for either of these two steps — see
`references/data-cloud-mapping.md` §5 for why. Give the admin exact instructions, not vague
pointers, using the predicted names so they're just confirming, not guessing:

9. **Refresh the Data Stream**: *Data Cloud app → Data Streams → the stream feeding `{DLO name}`
   → Refresh Schema* (or wait for its scheduled refresh). For each new field, predict its resulting
   DLO field name with the verified transform — `{SF API Name}__c` → `{SF API Name}_c__c` (strip
   the trailing `__c`, append `_c__c`) — and tell the admin exactly what to look for:
   `"Cantidad_de_compras__c` should appear as `Cantidad_de_compras_c__c` in the `{DLO name}`
   schema."
10. **Create the DMO field**: *Data Cloud app → Data Model → `{DMO name}` (e.g. `ssot__Account__dlm`
    / "Account") → New Field*. Give the admin the suggested Field Label (same as the SF field's
    label) and API name (from Phase 2 step 4) to type in — tell them it's editable, this is just a
    starting suggestion. Data Type should match the source field's type.
11. **Map it**: in the same New Field dialog (or the field's mapping tab), set the source to the
    DLO field predicted in step 9. Save.
12. **Ask the admin to confirm** the field is created and mapped before moving on — don't assume a
    fixed wait time; Data Cloud processing duration depends on data volume and this skill has no
    way to poll DMO field readiness.

### Phase 5 — Build the Segment

13. Ask: **Segment name**, and for each filter condition — which field (the ones just created, or
    any other DMO field), operator, value(s), and whether the top-level combinator across
    conditions is AND or OR (matches `MarketSegment.IncludeCriteria`'s single flat `LogicalComparison`
    — see `references/segment-criteria-schema.md` §3, nested groups are unverified).
14. Build the `IncludeCriteria` JSON per the verified shape in `segment-criteria-schema.md` §3-4 —
    `NumberComparison` (`"value": <scalar>`), `TextComparison` (`"values": [...]`, plural key),
    `DateComparison` (`"value": [...]`, array). For Picklist/Checkbox conditions, don't invent the
    shape — either find a real segment in this org filtering on that type and copy its structure,
    or create the segment with the verified conditions only and tell the admin to add that specific
    condition by hand in Setup.
15. `POST /services/data/v{version}/sobjects/MarketSegment` with `Name` (+ `Description` if given)
    and `IncludeCriteria` as a JSON-encoded string. Write the body to a scratch file and pass
    `-b "@<path>"` — don't fight inline PowerShell quoting on nested JSON.
16. Read back `SegmentStatus`, `LastSegmentMemberCount`, `LastSegmentTotalCount` on the new Id.
    Evaluation is async — report whatever status is current, don't block waiting for `ACTIVE`.

### Final Output

Close with a plain summary — fields created, DMO field names, segment name and Id, current
`SegmentStatus`/member count, and how to find it (*Data Cloud app → Segments → search by name* —
there's no confirmed direct record URL, don't fabricate one, see `segment-criteria-schema.md` §2).

---

## Critical Rules

- **This is a demo/POC tool scoped to `Account`.** Don't generalize the naming formulas in
  `references/data-cloud-mapping.md` to other objects without re-verifying against a real DLO/DMO
  pair for that object first — the transform was confirmed on Account only.
- **Never guess the DLO/DMO names for a new org.** Always run the live discovery in Phase 1 step 2
  — `Account_Home__dll` is what this specific org happens to call it, not a universal name.
- **Never fabricate the `IncludeCriteria` JSON for an unverified field type.** Picklist, Checkbox,
  and MultiPicklist comparisons have no confirmed real example — see
  `segment-criteria-schema.md` §4. Guessing wrong here silently creates a segment with the wrong
  membership, which is worse than asking the admin to add that one condition by hand.
- **Phase 4 cannot be automated — say so plainly, don't pretend to have done it.** If a future
  session finds a verified write path for DMO fields or DLO mappings, update
  `references/data-cloud-mapping.md` §5 and promote those steps to automated; don't silently start
  attempting untested POST calls against Data Cloud metadata endpoints in a live org.
- **Use `sf api request rest` for anything under `/services/data/.../ssot/*` or `/sobjects/MarketSegment`** — it authenticates automatically.
- **Run Salesforce CLI commands through PowerShell, not the Bash tool** on Windows — `sf`'s install
  path under `C:\Program Files\...` doesn't resolve from Git Bash.
- **Save large API responses (`ssot/metadata` especially) to a scratch file and filter locally** —
  never print raw JSON into the conversation; same token-discipline rule as
  `pc-crm-salesforce-field-creator`.
