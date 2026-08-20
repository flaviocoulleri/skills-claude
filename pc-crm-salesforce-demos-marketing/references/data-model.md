# Data Model — SDO Marketing Demo Pattern

Facts confirmed by direct inspection of a working example in a real org (Campaign "Farmacias de Santiago - Producto Geniol", org alias `sdo-alfa`). Anything not explicitly validated is marked as such.

## 1. Campaign

Standard `Campaign` object, three custom Record Types observed:

| Record Type (Label) | DeveloperName | Description | Validated in this skill? |
|---|---|---|---|
| Parent Campaign | `SDO_Marketing_ParentCampaign` | Top-level campaign | No — inferred from RecordType list only |
| Child Campaign | `SDO_Marketing_ChildCampaign` | Child of a parent campaign | **Yes** — this is the default/only path exercised |
| Partner-Led Campaign | `Partner_Led_Campaign` | Campaigns led/used by partners to market to their customers | No |

The validated pattern uses a **standalone Child Campaign** (`ParentId = null`) — it does not require an actual parent. Standard Campaign fields used: `Name`, `Type`, `Status`, `RecordTypeId`.

Query record type Ids with:
```sql
SELECT Id, Name, DeveloperName, IsActive, Description FROM RecordType WHERE SobjectType = 'Campaign'
```

## 2. CMS Workspace (ManagedContentSpace)

- SObject: `ManagedContentSpace`, key prefix `0Zu`, queryable via plain SOQL.
- In the reference org there's one relevant workspace: **"Content Workspace for Marketing Cloud"**, `apiName: "Default_Content_Workspace"`, `spaceType.apiName: "marketing"`, `isEnhancedSpace: true`, `isFlowOrchestrationEnabled: true`.
- Get full details (including `rootFolderId`) via Connect API — **not** via SOQL field, the space's folder info isn't exposed as a queryable field:
  ```
  GET /connect/cms/spaces/{spaceId}
  ```
  Returns `rootFolderId` (prefix `9Pu`).

### CMS Folders

- Folders (prefix `9Pu`) are **not** a normal queryable SObject — `ManagedContentFolder` does not exist in the global describe. The only way to read them is `GET /connect/cms/folders/{folderId}`.
- Convention observed: **one folder per Account/Campaign** (e.g. a folder literally named "Dermedica" holds all of that account's Email/WhatsApp content). Folder response shape:
  ```json
  {
    "id": "9Pu...",
    "name": "Dermedica",
    "parentFolderId": "9Pu..." ,
    "folderHierarchy": [ { "id": "9Pu...", "name": "...", "parentFolderId": null } ]
  }
  ```
- **Folders cannot be created via API** — see SKILL.md "Known Limitation". Must be created by hand in the Lightning CMS app (`/lightning/cms/content?mcsId={spaceId}` → New Folder).

## 3. ManagedContent (the actual Email / WhatsApp records)

- SObject: `ManagedContent`, key prefix `20Y`, **queryable** but **not createable via plain DML** (`createable: false` in describe) — creation only works through the Connect REST API (`POST /connect/cms/contents`).
- Useful SOQL fields: `Id, Name, ApiName, ContentTypeFullyQualifiedName, PrimaryLanguage, AuthoredManagedContentSpaceId`.
- Content types seen in this pattern:

| `ContentTypeFullyQualifiedName` | Display name | Purpose |
|---|---|---|
| `sfdc_cms__email` | Email | The marketing email |
| `sfdc_cms__whatsappSession` | WhatsApp Session Message | The WhatsApp message (session-window message) |
| `sfdc_cms__languageSettings` | — | Space-level system content, not campaign-specific, ignore |
| `sfdc_cms__externalAssetsProviderSettings` | — | Space-level system content, ignore |
| `sfdc_cms__image` | Image | Used for reusable assets (e.g. default template header/logo), not part of this pattern |

- The `contentKey` returned when creating content (format `MC` + ~28 alphanumeric chars) is what gets referenced later by the Flow — see `api-recipes.md` for the exact `contentId` string format used in the Flow's action inputs.
- Every real Email example inspected in this org (5+ campaigns) uses the **same JSON shape**: a component tree rooted at `sfdc_cms/rootContentBlock`, containing one `lightning/section` → one `lightning/column` → one `lightning/html` block holding the full email HTML in its `rawHtml` attribute. This **is** what "Use components" produces when the HTML block is the component you use — do not treat it as the "Code your own" method. No example of a multi-component build (separate Text/Image/Button/Divider blocks) exists in this org; if one is ever needed, get a real example first (see SKILL.md rule). The *outer* CMS shape being a single block does **not** mean the `rawHtml` content should be simple — it's a full table-based, inline-styled marketing email (header/hero/offer/CTA/footer). See `references/email-templates.md` for the four validated archetypes.

## 4. Flow (the orchestrator)

- `FlowDefinition` (prefix `300`) / `Flow` (prefix `301`, one row per version) via **Tooling API**, not the plain REST/SOQL API.
- **Naming convention observed**: `FullName` (a.k.a. developer name) = `flow_{18-char CampaignId}_{epoch millis}`, e.g. `flow_701Kh000001Q49wIAC_1781636151084`. This ties the Flow 1:1 to the Campaign it belongs to — there's no separate lookup field for this relationship, it's purely encoded in the name.
- `Label` / `MasterLabel` convention: `"{Campaign Name} Flow"`.
- `ProcessType: AutoLaunchedFlow`, `start.triggerType: "Segment"` (Data Cloud Segment trigger).
- A freshly-scaffolded Flow (no Segment attached, content unpublished, no From Address/WhatsApp channel selected) reports `Status: InvalidDraft`. This is the **expected, normal state** for a demo scaffold in this org — every real example found was also `InvalidDraft` at this stage. Full JSON template in `api-recipes.md`.

### 4.1 Default shape (as of 1.6.0): plain linear chain

Confirmed by direct inspection (2026-08-19, Tooling API `SELECT Id, Metadata FROM Flow WHERE DefinitionId = '<id>'`) of a real Flow the user hand-built on top of this skill's own 1.3.0-era engagement-branching scaffold (Campaign "SMS Latam - Lanzamiento SMS Delivery Center", org `flavio.coulleri@demos2026.com.mx`, FlowDefinitionId `300aj00003Iqy2cAAB`). The shape found: `Metadata.decisions: []`, exactly two `actionCalls` (`sendEmailMessage`, `sendWhatsAppMessage`), exactly one `wait` connecting them, and the WhatsApp action's `connector` unset — i.e. `sendEmailMessage` → `WaitDuration` (1 day) → `sendWhatsAppMessage` → end. The user confirmed this simpler shape should be the default going forward, superseding 4.1's prior (1.3.0) engagement-branching default, which is documented below §4.1.1 as an opt-in variant.

### 4.1.1 Optional variant: engagement branching (default from 1.3.0 through 1.5.x)

Confirmed by direct inspection (2026-08-05, Tooling API `SELECT Id, Metadata FROM Flow WHERE Id = '<id>'`) of a real Flow the user hand-built in Flow Builder on top of an earlier linear scaffold from this skill (Campaign "LEBEN - Bienvenida Nuevo Lead", org `matias.lopez@demos2026.com.mx`, FlowDefinitionId `300aj00003DJip8AAD`). The shape:

`sendEmailMessage` → `WaitDuration` (1 day) → `Decision` ("¿Tuvo interacción?") → **Sí**: `createTask` (follow-up) / **No (default)**: `sendWhatsAppMessage` → `WaitDuration` (1 day) → `Decision` ("¿Respondió?") → **Sí**: `forwardToBotOrAgent` / **No (default)**: end.

Element facts, straight from that inspection (only relevant if building this variant — see SKILL.md "Default Flow shape" for when to use it):

- **`Decision` "Sí" rule condition**: both Decisions in the real build used `conditionLogic: "and"`, one condition with `leftValueReference` set to the *name* of the preceding action call (e.g. `"Send_Email_Message_Action"`) and `rightValue.elementReference` set to that **same** name, `operator: "EqualTo"` — i.e. the action compared to itself, which is trivially always `true`. This is a known Flow Builder default/stub for a not-yet-configured Decision outcome, not real engagement logic. It **is** accepted by the Tooling API create call (validated — it's live in the org), so it's a safe placeholder to scaffold, but the skill must tell the user it needs replacing with a real field once they know which one signals engagement (email open/click, WhatsApp reply) — don't invent that field without a validated example, per this skill's general schema-guessing rule.
- **`createTask` action** (`actionType: "createTask"`) inputs used: `taskSubjectName` (stringValue, e.g. `"Call"`), `taskAssignedToId` (stringValue, a User Id), `taskPriority` (stringValue, e.g. `"Normal"`), `taskStatus` (stringValue, e.g. `"Not Started"`). In the real build this was hardcoded to the demo user's Id — **confirmed to equal `Campaign.OwnerId`** for that Campaign (`SELECT OwnerId FROM Campaign WHERE Id = '<id>'` returned the same Id), so the skill resolves it dynamically from the Campaign at build time instead of hardcoding a person.
- **`forwardToBotOrAgent` action** (`actionType: "forwardToBotOrAgent"`) inputs used: `channel` (stringValue, `"WhatsApp"` in the real build — matches the channel already in play for this journey).
- **NOT carried into the skill's template**: the real build also had a third branch calling `exitIndividualsFromFlow` (`actionType: "exitIndividualsFromFlow"`) with `IndividualId` set to the **literal string** `"PLACEHOLDER"` and `FlowVersionId: null`, `actionName` pointing at an unrelated Flow from a different campaign (`flow_701aj00003EeO3eAAF_1785169045080`, `MasterLabel: "Reactivacion de Clientes Flow"`, looked up via `SELECT Id, DeveloperName, MasterLabel FROM FlowDefinition WHERE DeveloperName = '...'`). Confirmed with the user this was unfinished exploration, not intentional. Also, structurally, this action needs a real Flow's Id to target — the Flow being scaffolded doesn't have one yet at creation time (it's being created in the same call), so a genuine self-referencing "exit individuals from *this* flow" action can only be added **after** the Flow exists, via a manual Flow Builder edit. Don't attempt to reference the Flow's own not-yet-assigned `FullName`/Id inside its own creation payload (step 6) — it doesn't exist yet at that point. It **does** exist right after step 6 returns, though, which is what makes the offered follow-up in `api-recipes.md` step 6.6 possible; that path is still unvalidated against a real org and gated on finding (or asking for) a real `IndividualId` value, since the only example on file used a broken placeholder.
- The real build also had a `GoTo` connector from the second Decision's "Sí" rule back into the *first* Decision element — almost certainly a Flow Builder artifact of reusing an existing outcome rather than a deliberate loop. The skill's template does not reproduce this; the second Decision's "Sí" path goes straight to `forwardToBotOrAgent`.

Full JSON template (with placeholders for `<CAMPAIGN_OWNER_ID>` etc.) in `api-recipes.md` step 6.3. The plain linear default's template is step 6 (no §6.3 suffix).

## 5. FlowRecord — the actual Campaign↔Flow relationship

Separate object, key prefix `2aF`, queryable via plain SOQL. This — not the `flow_{CampaignId}_...` naming convention — is what the Campaign record page's "Flows" related list actually reads. Key fields: `Name`, `ApiName` (mirrors the Flow's `FullName`), `FlowDefinition` (the FlowDefinition Id, 15-char), `AssociatedRecordId` (lookup-like field to the Campaign — **this is the link**), `Type` (`"Segment"`), `FlowType` (`"SegmentTrigAutolnch"`), `ProgressStatus` (mirrors the Flow's `Status`), `DataSpaceId`, `CapacityCategory` (`"MarketingCloudFlow"`).

Behavior, confirmed empirically:

- The platform **auto-creates** a `FlowRecord` row as soon as the corresponding `Flow` exists (created via Tooling API in section 4 above) — no separate action needed to trigger its creation. `AssociatedRecordId` starts unset on this auto-created row.
- **Direct `INSERT` is hard-blocked** on both standard REST and Tooling API — standard REST: `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY` / `"entity type cannot be inserted: Flow"`; Tooling API: `NOT_FOUND` (not registered there). This is a platform restriction for every user, not a permissions issue.
- **`UPDATE` (PATCH) works fine** via the standard REST API on the auto-created row — that's the supported way to set `AssociatedRecordId` after the fact.
- `AssociatedRecordId` is **not** a field on `Flow` or `FlowDefinition` — confirmed via `INVALID_FIELD` errors testing both directly. It only exists on `FlowRecord`.
- Find the right `FlowRecord` deterministically with `SELECT Id FROM FlowRecord WHERE ApiName = '{the Flow's FullName}'` — no need to list/guess.

This is part of "Marketing Cloud Next" / "Marketing Cloud Growth" (Salesforce's newer segment-triggered flow product) — `FlowRecord` is the generic wrapper that ties any such Flow to whatever business record it's scoped to (Campaign in this pattern, but the field name `AssociatedRecordId` suggests it's polymorphic/usable with other objects too — not tested).

**Multi-Business-Unit orgs**: Campaign has a `BusinessUnitId` field (null by default on a freshly-created Campaign). In orgs with more than one Data Space, the `FlowRecord` PATCH fails with `MISMATCHING_TYPES` unless the Campaign's Business Unit resolves to the same Data Space as the Flow (`"default"` apiName in this pattern). Fix by copying `BusinessUnitId` from any other real campaign in the org — see `api-recipes.md` step 6.5. Confirmed: `sdo-alfa` (1 Data Space) never hits this; `sdo-sales` (2 Data Spaces) does.
