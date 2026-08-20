# API Recipes — SDO Marketing Demo Pattern

All commands assume Windows + the `sf` CLI, run through **PowerShell** (not the Bash tool — see SKILL.md). Replace `-o sdo-alfa` with the actual target org alias. Every `<PLACEHOLDER>` must be filled with a real value from the current org/session — never leave a placeholder literal in a real API call.

## 0. Sanity checks

```powershell
sf org list
sf org display --target-org <ORG_ALIAS>
```

Find the CMS workspace Id and its `apiName` / `spaceType.apiName` (needed later for the `contentId` format):

```powershell
sf api request rest "/services/data/v60.0/connect/cms/spaces/<SPACE_ID>" -X GET -o <ORG_ALIAS>
```

## 1. Create the Campaign

**Check for a duplicate first** — cheap, avoids cluttering the org on a re-run for the same account/theme:

```powershell
sf data query --target-org <ORG_ALIAS> --query "SELECT Id, Name FROM Campaign WHERE Name = '<CAMPAIGN_NAME>'" --json
```

If a row comes back, tell the user and ask whether to reuse that Campaign's Id (skip to step 3) or proceed anyway with a disambiguating suffix on `<CAMPAIGN_NAME>` — don't silently create a duplicate.

Plain SObject, no special API needed:

```powershell
sf data create record --target-org <ORG_ALIAS> --sobject Campaign --values "Name='<CAMPAIGN_NAME>' Type='Advertisement' Status='Planned' RecordTypeId='<CHILD_CAMPAIGN_RECORD_TYPE_ID>'"
```

Get the Child Campaign RecordType Id once per org (it's stable, cache it — don't re-query every run):

```sql
SELECT Id FROM RecordType WHERE SobjectType = 'Campaign' AND DeveloperName = 'SDO_Marketing_ChildCampaign'
```

## 2. CMS folder (manual — do not attempt via API)

Tell the user: "Andá a `https://<instance>.lightning.force.com/lightning/cms/content?mcsId=<SPACE_ID>` y creá una carpeta llamada `<ACCOUNT_NAME>`." If they haven't done it yet, use `<SPACE_ID>` itself as `contentSpaceOrFolderId` in step 3 (content lands at the workspace root) and offer to move it later.

## 3. Create the Email content ("Use components")

Write the body to a scratch file first (`email_body.json`), then:

```powershell
sf api request rest "/services/data/v60.0/connect/cms/contents" -X POST -b "@<PATH_TO>\email_body.json" -H "Content-Type:application/json" -o <ORG_ALIAS>
```

**Build this file with here-string templating, not `ConvertTo-Json`.** Confirmed 2026-08-12: piping the nested ordered-hashtable component tree below through `ConvertTo-Json -Depth 20` hung for minutes (CPU climbing, no output) as soon as the `rawHtml` string was embedded in it — happened at an ordinary size (~5KB), not some pathological input. Killed it and rebuilt with a plain PowerShell here-string containing the literal JSON skeleton, with the HTML/text substituted in via a small escape helper. This ran instantly and produced the same structure:

```powershell
function JsonEscape([string]$s) {
  $s = $s -replace '\\', '\\\\'
  $s = $s -replace '"', '\"'
  $s = $s -replace "`r`n", '\n'
  $s = $s -replace "`n", '\n'
  $s = $s -replace "`t", '\t'
  return $s
}
$rawHtml = Get-Content -Raw -Encoding UTF8 "<PATH_TO>\raw_email.html"
$rawHtmlEsc = JsonEscape $rawHtml
$json = @"
{ "contentSpaceOrFolderId": "<SPACE_OR_FOLDER_ID>", ..., "rawHtml": "$rawHtmlEsc", ... }
"@
Set-Content -Path "<PATH_TO>\email_body.json" -Value $json -Encoding UTF8 -NoNewline
```

Write the full HTML to its own `.html` scratch file first (readable, real newlines), then read + escape + splice it into a JSON skeleton written directly as a here-string (matching the shape below) — never build the whole tree as a PowerShell object and pipe it through `ConvertTo-Json`. The same applies to the WhatsApp body in step 4 whenever its message text is long, though in practice that one is small enough to not trigger this.

`email_body.json` template — fill in `contentSpaceOrFolderId` (space Id or folder Id from step 2), `title`, `subjectLine`, and the `rawHtml` string (escape internal `"` as `\"`, avoid literal newlines — keep the HTML on one line or use `\n`):

```json
{
  "contentSpaceOrFolderId": "<SPACE_OR_FOLDER_ID>",
  "title": "<TITLE, e.g. 'Email - <Account>'>",
  "contentType": "sfdc_cms__email",
  "contentBody": {
    "backgroundColor": "#ffffff — this is the Email Builder's own 'Fondo de email' canvas behind the email card (Salesforce UI chrome), NOT part of the email's design. Leave it white regardless of the archetype's own inner canvas color (e.g. Archetype A's dark #0a0a0a hero stays inside rawHtml, untouched) unless the user explicitly asks for a different builder background. Corrected 2026-08-12 (1.5.5) — earlier guidance wrongly said this had to match the rawHtml canvas color.",
    "lightning:brandSource": { "defaultBrandOption": "sfdcBrand" },
    "lightning:colorScheme": "{!$brand.colorScheme}",
    "lightning:dataProviders": [
      {
        "attributes": { "objectApiName": "UnifiedIndividual__dlm" },
        "definition": "sfdc_cms__unifiedIndividualDataProvider",
        "sfdcExpressionKey": "$unifiedIndividual"
      }
    ],
    "lightning:padding": "{!$brand.spacing.none}",
    "messagePurpose": "promotional",
    "sfdc_cms:block": {
      "definition": "sfdc_cms/rootContentBlock",
      "id": "<UUID-1>",
      "type": "block",
      "children": [
        {
          "attributes": {
            "lightning:borderRadius": "{!$brand.borderRadius.square}",
            "lightning:borderWidth": "{!$brand.borderWeight.none}",
            "lightning:colorScheme": "{!$brand.colorScheme}",
            "lightning:margin": "{!$brand.spacing.none}",
            "lightning:padding": "{!$brand.spacing.xSmall}",
            "stackOnMobile": true,
            "lightning:backgroundImage": { "repeat": "no-repeat", "position": "center center", "size": "cover" }
          },
          "definition": "lightning/section",
          "id": "<UUID-2>",
          "type": "block",
          "children": [
            {
              "attributes": {
                "columnWidth": 12,
                "lightning:borderRadius": "{!$brand.borderRadius.square}",
                "lightning:borderWidth": "{!$brand.borderWeight.none}",
                "lightning:colorScheme": "{!$brand.colorScheme}",
                "lightning:margin": "{!$brand.spacing.none}",
                "lightning:padding": "{!$brand.spacing.xSmall}",
                "lightning:verticalAlignment": "top",
                "lightning:backgroundImage": { "repeat": "no-repeat", "position": "center center", "size": "cover" }
              },
              "definition": "lightning/column",
              "id": "<UUID-3>",
              "type": "block",
              "children": [
                {
                  "attributes": {
                    "lightning:borderRadius": "{!$brand.borderRadius.square}",
                    "lightning:borderWidth": "{!$brand.borderWeight.none}",
                    "lightning:colorGroup": {
                      "backgroundColor": "{!$brand.colorScheme.root}",
                      "borderColor": "{!$brand.colorScheme.neutral}",
                      "linkColor": "{!$brand.colorScheme.primaryAccent}",
                      "textColor": "{!$brand.colorScheme.contrast}"
                    },
                    "lightning:margin": "{!$brand.spacing.none}",
                    "lightning:padding": "{!$brand.spacing.none}",
                    "rawHtml": "<RAW_HTML_EMAIL_STRING>"
                  },
                  "definition": "lightning/html",
                  "id": "<UUID-4>",
                  "type": "block"
                }
              ]
            }
          ]
        }
      ]
    },
    "sfdc_cms:title": "<TITLE>",
    "subjectLine": "<SUBJECT_LINE>",
    "lightning:expressions": [],
    "lightning:backgroundImage": { "repeat": "no-repeat", "position": "center center", "size": "cover" },
    "sfdc_cms:attachments": [],
    "sfdc_cms:variants": []
  }
}
```

Response includes `"contentKey": "MC..."` — save it as `<EMAIL_CONTENT_KEY>`.

## 4. Create the WhatsApp Session Message content

**Default (as of 1.7.3): Quick Reply (buttons)**, not plain Text — same POST endpoint, `whatsapp_body.json`. Confirmed 2026-08-19 by finding a **real pre-existing example already in the org** (`GET /connect/cms/contents/{contentKey}` on the oldest `sfdc_cms__whatsappSession` content, created by hand before this skill existed) rather than guessing the schema — per this skill's own rule. Build every WhatsApp with a tap-to-respond button (e.g. "Sí, hablemos") instead of asking the recipient to type a word, unless the user explicitly asks for plain text (§4.2):

```json
{
  "contentSpaceOrFolderId": "<SPACE_OR_FOLDER_ID>",
  "title": "<TITLE, e.g. 'Whatsapp - <Account>'>",
  "contentType": "sfdc_cms__whatsappSession",
  "contentBody": {
    "contentBlock": {
      "attributes": {
        "sfdc_cms:whatsappMessageBody": "<MESSAGE_TEXT>",
        "type": "QuickReply",
        "actions": {
          "definition": "sfdc_cms/waSessionInteractiveActions",
          "id": "<UUID-6>",
          "attributes": {
            "actionType": "button",
            "type": "block",
            "buttons": [
              {
                "definition": "sfdc_cms/waSessionInteractiveButton",
                "type": "block",
                "id": "<UUID-7>",
                "attributes": {
                  "id": "<BUTTON_LABEL>",
                  "title": "<BUTTON_LABEL>",
                  "type": "reply"
                }
              }
            ]
          }
        }
      },
      "definition": "sfdc_cms__whatsappMessageTypeQuickReply",
      "type": "block",
      "id": "<UUID-5>"
    },
    "lightning:dataProviders": [
      {
        "attributes": { "objectApiName": "UnifiedIndividual__dlm" },
        "definition": "sfdc_cms__unifiedIndividualDataProvider",
        "sfdcExpressionKey": "$unifiedIndividual"
      }
    ],
    "messageType": "QuickReply",
    "sfdc_cms:title": "<TITLE>",
    "lightning:expressions": []
  }
}
```

Notes:

- `<BUTTON_LABEL>` — the validated example used the same string for both `id` and `title` (e.g. `"Sí"`), keep that pattern. WhatsApp buttons have a short character limit (~20 chars) — keep it to 2-4 words.
- `buttons` is an array — the validated example has exactly **one** button. Multiple buttons (WhatsApp supports up to 3) is a reasonable generalization of the same object shape but has **not** itself been directly confirmed in this org — say so if the user asks for 2-3 buttons, don't present it as equally validated.
- Adjust `<MESSAGE_TEXT>` to lead naturally into the button (e.g. "Tocá el botón de abajo para..."), not a "Responde SÍ" instruction — that phrasing belongs to the plain Text variant (§4.2), not Quick Reply.
- Everything else (space/folder, title, dataProviders) is identical to the plain Text variant in §4.2.

Save the response `contentKey` as `<WHATSAPP_CONTENT_KEY>`.

### 4.2 Plain Text variant (legacy, opt-in)

Only build this if the user explicitly asks for plain text instead of a button — it is **not** the default as of 1.7.3:

```json
{
  "contentSpaceOrFolderId": "<SPACE_OR_FOLDER_ID>",
  "title": "<TITLE, e.g. 'Whatsapp - <Account>'>",
  "contentType": "sfdc_cms__whatsappSession",
  "contentBody": {
    "contentBlock": {
      "attributes": {
        "sfdc_cms:whatsappMessageBody": "<MESSAGE_TEXT>",
        "type": "Text"
      },
      "definition": "sfdc_cms__whatsappMessageTypeText",
      "type": "block",
      "id": "<UUID-5>"
    },
    "lightning:dataProviders": [
      {
        "attributes": { "objectApiName": "UnifiedIndividual__dlm" },
        "definition": "sfdc_cms__unifiedIndividualDataProvider",
        "sfdcExpressionKey": "$unifiedIndividual"
      }
    ],
    "messageType": "Text",
    "sfdc_cms:title": "<TITLE>",
    "lightning:expressions": []
  }
}
```

Here `<MESSAGE_TEXT>` ends with an explicit typed instruction ("Responde SÍ para...") since there's no button to tap.

## 5. Build the `contentId` reference strings

Format: `"{spaceType.apiName}--{space.apiName}.{contentType}--{contentKey}"` (values for the first two segments come from the step-0 `GET /connect/cms/spaces/{id}` call — in the reference org these are `marketing` and `Default_Content_Workspace`, but **don't hardcode them for a different org/space** — re-fetch).

```
marketing--Default_Content_Workspace.sfdc_cms__email--<EMAIL_CONTENT_KEY>
marketing--Default_Content_Workspace.sfdc_cms__whatsappSession--<WHATSAPP_CONTENT_KEY>
```

## 6. Create the orchestrating Flow

**Default shape (as of 1.6.0) is a plain linear chain** — `Send Email → Wait 1 Day → Send WhatsApp → end`, no Decisions, no follow-up Task, no forward-to-agent — see SKILL.md "Default Flow shape" and `data-model.md` §4.1 for why. No `Campaign.OwnerId` lookup is needed for this default.

```powershell
sf api request rest "/services/data/v67.0/tooling/sobjects/Flow" -X POST -b "@<PATH_TO>\flow_body.json" -H "Content-Type:application/json" -o <ORG_ALIAS>
```

Get an epoch-millis suffix for the `FullName` (must be a real, freshly-generated value — don't reuse one from a prior run):

```bash
date +%s%3N
```

`flow_body.json` template (default, linear):

```json
{
  "FullName": "flow_<CAMPAIGN_ID_18CHAR>_<EPOCH_MILLIS>",
  "Metadata": {
    "processType": "AutoLaunchedFlow",
    "status": "Draft",
    "apiVersion": 67,
    "label": "<Campaign Name> Flow",
    "interviewLabel": "<Campaign Name> Flow {!$Flow.CurrentDateTime}",
    "environments": ["Default"],
    "dataSpace": "default",
    "processMetadataValues": [
      { "name": "BuilderType", "value": { "stringValue": "LightningFlowBuilder" } },
      { "name": "CanvasMode", "value": { "stringValue": "AUTO_LAYOUT_CANVAS" } },
      { "name": "OriginBuilderType", "value": { "stringValue": "LightningFlowBuilder" } }
    ],
    "start": {
      "triggerType": "Segment",
      "locationX": 0,
      "locationY": 0,
      "connector": { "targetReference": "Send_Email_Message_Action" }
    },
    "actionCalls": [
      {
        "name": "Send_Email_Message_Action",
        "label": "<Email content title>",
        "actionName": "sendEmailMessage",
        "actionType": "sendEmailMessage",
        "locationX": 0,
        "locationY": 0,
        "flowTransactionModel": "CurrentTransaction",
        "connector": { "targetReference": "Wait_After_Email" },
        "inputParameters": [
          { "name": "clickTracking", "value": { "booleanValue": true } },
          { "name": "openTracking", "value": { "booleanValue": true } },
          { "name": "contentId", "value": { "stringValue": "<EMAIL_CONTENT_ID_FROM_STEP_5>" } }
        ]
      },
      {
        "name": "Send_Whatsapp_Message_Action",
        "label": "Send Whatsapp Message Action",
        "actionName": "sendWhatsAppMessage",
        "actionType": "sendWhatsAppMessage",
        "locationX": 0,
        "locationY": 0,
        "flowTransactionModel": "CurrentTransaction",
        "inputParameters": [
          { "name": "contentId", "value": { "stringValue": "<WHATSAPP_CONTENT_ID_FROM_STEP_5>" } }
        ]
      }
    ],
    "waits": [
      {
        "name": "Wait_After_Email",
        "label": "Wait 1 Day",
        "locationX": 0,
        "locationY": 0,
        "elementSubtype": "WaitDuration",
        "defaultConnectorLabel": "Default Path",
        "waitEvents": [
          {
            "label": "el_0",
            "conditionLogic": "and",
            "offset": 1,
            "offsetUnit": "Days",
            "connector": { "targetReference": "Send_Whatsapp_Message_Action" }
          }
        ]
      }
    ]
  }
}
```

Note `Send_Whatsapp_Message_Action` has **no `connector`** — nothing follows it, the Flow ends there. `decisions` is omitted entirely (empty).

Expected response: `"success": true` plus an `infos` array listing exactly the missing-configuration warnings described in SKILL.md's "What's Left to Activate" (unpublished content, no Segment, no From Address, no WhatsApp channel). That is **success**, not failure — a `success: false` or an `errors` array with content is a real problem to investigate.

Verify afterward:

```powershell
sf data query --target-org <ORG_ALIAS> --use-tooling-api --query "SELECT Id, DefinitionId, MasterLabel, Status, VersionNumber FROM Flow WHERE Id = '<RETURNED_FLOW_ID>'" --json
```

Expect `Status: InvalidDraft`, `VersionNumber: 1` — matches the reference example exactly.

### 6.3 Optional variant: engagement branching

Only build this if the user explicitly asks for branching/a follow-up Task/forward-to-agent — it is **not** the default as of 1.6.0 (see SKILL.md "Default Flow shape"). Before building this variant's payload, get the Campaign's `OwnerId` (feeds the follow-up Task's assignee):

```powershell
sf data query --target-org <ORG_ALIAS> --query "SELECT OwnerId FROM Campaign WHERE Id = '<CAMPAIGN_ID>'" --json
```

`flow_body.json` template (branching variant — same `FullName`/header fields as above, `actionCalls`/`waits`/`decisions` replaced with this shape):

```json
{
  "actionCalls": [
    {
      "name": "Send_Email_Message_Action",
      "label": "<Email content title>",
      "actionName": "sendEmailMessage",
      "actionType": "sendEmailMessage",
      "locationX": 0,
      "locationY": 0,
      "flowTransactionModel": "CurrentTransaction",
      "connector": { "targetReference": "Wait_After_Email" },
      "inputParameters": [
        { "name": "clickTracking", "value": { "booleanValue": true } },
        { "name": "openTracking", "value": { "booleanValue": true } },
        { "name": "contentId", "value": { "stringValue": "<EMAIL_CONTENT_ID_FROM_STEP_5>" } }
      ]
    },
    {
      "name": "Send_Whatsapp_Message_Action",
      "label": "Send Whatsapp Message Action",
      "actionName": "sendWhatsAppMessage",
      "actionType": "sendWhatsAppMessage",
      "locationX": 0,
      "locationY": 0,
      "flowTransactionModel": "CurrentTransaction",
      "connector": { "targetReference": "Wait_After_Whatsapp" },
      "inputParameters": [
        { "name": "contentId", "value": { "stringValue": "<WHATSAPP_CONTENT_ID_FROM_STEP_5>" } }
      ]
    },
    {
      "name": "Create_Follow_Up_Task",
      "label": "Crear tarea de seguimiento",
      "actionName": "createTask",
      "actionType": "createTask",
      "locationX": 0,
      "locationY": 0,
      "flowTransactionModel": "CurrentTransaction",
      "inputParameters": [
        { "name": "taskSubjectName", "value": { "stringValue": "Seguimiento - <Campaign Name>" } },
        { "name": "taskAssignedToId", "value": { "stringValue": "<CAMPAIGN_OWNER_ID>" } },
        { "name": "taskPriority", "value": { "stringValue": "Normal" } },
        { "name": "taskStatus", "value": { "stringValue": "Not Started" } }
      ]
    },
    {
      "name": "Forward_To_Agent",
      "label": "Enviar conversación a un agente",
      "actionName": "forwardToBotOrAgent",
      "actionType": "forwardToBotOrAgent",
      "locationX": 0,
      "locationY": 0,
      "flowTransactionModel": "CurrentTransaction",
      "inputParameters": [
        { "name": "channel", "value": { "stringValue": "WhatsApp" } }
      ]
    }
  ],
  "waits": [
    {
      "name": "Wait_After_Email",
      "label": "Wait 1 Day",
      "locationX": 0,
      "locationY": 0,
      "elementSubtype": "WaitDuration",
      "defaultConnectorLabel": "Default Path",
      "waitEvents": [
        {
          "label": "el_0",
          "conditionLogic": "and",
          "offset": 1,
          "offsetUnit": "Days",
          "connector": { "targetReference": "Decision_Interacted_After_Email" }
        }
      ]
    },
    {
      "name": "Wait_After_Whatsapp",
      "label": "Wait 1 Day",
      "locationX": 0,
      "locationY": 0,
      "elementSubtype": "WaitDuration",
      "defaultConnectorLabel": "Default Path",
      "waitEvents": [
        {
          "label": "el_1",
          "conditionLogic": "and",
          "offset": 1,
          "offsetUnit": "Days",
          "connector": { "targetReference": "Decision_Interacted_After_Whatsapp" }
        }
      ]
    }
  ],
  "decisions": [
    {
      "name": "Decision_Interacted_After_Email",
      "label": "¿Tuvo interacción?",
      "locationX": 0,
      "locationY": 0,
      "defaultConnectorLabel": "No",
      "defaultConnector": { "targetReference": "Send_Whatsapp_Message_Action" },
      "rules": [
        {
          "name": "Interacted_Yes_After_Email",
          "label": "Sí",
          "conditionLogic": "and",
          "conditions": [
            {
              "leftValueReference": "Send_Email_Message_Action",
              "operator": "EqualTo",
              "rightValue": { "elementReference": "Send_Email_Message_Action" }
            }
          ],
          "connector": { "targetReference": "Create_Follow_Up_Task" }
        }
      ]
    },
    {
      "name": "Decision_Interacted_After_Whatsapp",
      "label": "¿Respondió?",
      "locationX": 0,
      "locationY": 0,
      "defaultConnectorLabel": "No",
      "rules": [
        {
          "name": "Interacted_Yes_After_Whatsapp",
          "label": "Sí",
          "conditionLogic": "and",
          "conditions": [
            {
              "leftValueReference": "Send_Whatsapp_Message_Action",
              "operator": "EqualTo",
              "rightValue": { "elementReference": "Send_Whatsapp_Message_Action" }
            }
          ],
          "connector": { "targetReference": "Forward_To_Agent" }
        }
      ]
    }
  ]
}
```

Notes on this variant's placeholders:

- `<CAMPAIGN_OWNER_ID>` — the real, working value from the `SELECT OwnerId FROM Campaign` query above, not a guess.
- The `Interacted_Yes_*` rule conditions are a **deliberate always-true placeholder** (an action compared to itself) — validated to be accepted by the API, but not real engagement logic. Tell the user it needs replacing with a real field in Flow Builder once they know which one signals engagement. See SKILL.md "Default Flow shape".
- `Decision_Interacted_After_Whatsapp` has **no `defaultConnector`** — its "No" path simply ends the Flow. This mirrors where the reference build's (unfinished, dropped) "dormant lead" branch would have gone; add one manually in Flow Builder if the user wants that branch — it needs this same Flow's own Id, which doesn't exist yet at creation time, so it can't be scripted here.

### 6.4 Fixing a mistake after the Flow already exists

Confirmed 2026-08-12: unlike CMS content (`ManagedContent`, read-only after creation — see the
Known Limitation below), an already-created `Flow` draft **can** be updated:

```powershell
sf api request rest "/services/data/v67.0/tooling/sobjects/Flow/<FLOW_ID>" -X PATCH -b "@<PATH_TO>\flow_body.json" -H "Content-Type:application/json" -o <ORG_ALIAS>
```

Send the **full** `Metadata` object (same shape as step 6's create, with the corrected value —
e.g. a `contentId` pointing at a newly-created replacement CMS content item after fixing a copy
or color mistake in the original). A successful `PATCH` returns empty output (204), same as the
`FlowRecord` PATCH in step 6.5.

**Important**: the platform issues a **new Flow Id** for the patched version — `VersionNumber`
stays `1`, but the row Id changes (e.g. `301aj00003LkqIwAAJ` → `301aj00003Ll2ggAAB` in the
session this was found in), and the old Id stops resolving (`SELECT ... WHERE Id = '<old id>'`
returns zero rows). Re-query by `DefinitionId` to get the current Id:

```powershell
sf data query --target-org <ORG_ALIAS> --use-tooling-api --query "SELECT Id, Status, VersionNumber FROM Flow WHERE DefinitionId = '<DEFINITION_ID>'" --json
```

Then rebuild the Flow Builder link (`references/api-recipes.md` step 7) with the new Id — the
old link 404s. The `FlowRecord` created in step 6.5 is unaffected by this — it's keyed by
`ApiName` (the Flow's `FullName`), not by the version row Id, so the Campaign↔Flow link survives
the swap with no further action needed.

When the fix is a CMS content mistake specifically (e.g. the wrong `backgroundColor`, per the
Known Limitation below and the 1.5.5 changelog entry): create a **new** content item via step 3/4
with the correction (the old one can't be edited), then PATCH the Flow's matching `actionCalls`
entry's `contentId` input parameter to the new content's `contentId` string from step 5. The old,
now-orphaned content item stays in the CMS workspace (harmless — it's just unreferenced) unless
the user wants it manually deleted.

## 6.5. Link the Flow to the Campaign (FlowRecord)

The platform auto-creates a `FlowRecord` row the moment the Flow from step 6 exists — no action needed to trigger it, but its `AssociatedRecordId` starts unset. Find it and set that field:

```powershell
sf data query --target-org <ORG_ALIAS> --query "SELECT Id FROM FlowRecord WHERE ApiName = '<FULLNAME_USED_IN_STEP_6>'" --json
```

Then `PATCH` it — **standard REST API, not Tooling** (Tooling API returns `NOT_FOUND` for `FlowRecord`, and a direct `INSERT` on either API is hard-blocked with `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY: "entity type cannot be inserted: Flow"` — only `UPDATE` on the auto-created row works):

```powershell
sf api request rest "/services/data/v67.0/sobjects/FlowRecord/<FLOWRECORD_ID>" -X PATCH -b "@<PATH_TO>\assoc_body.json" -H "Content-Type:application/json" -o <ORG_ALIAS>
```

`assoc_body.json`:

```json
{ "AssociatedRecordId": "<CAMPAIGN_ID>" }
```

A successful `PATCH` returns empty output (HTTP 204) — that's success, not a silent failure. Verify with:

```powershell
sf data query --target-org <ORG_ALIAS> --query "SELECT Id, AssociatedRecordId FROM FlowRecord WHERE Id = '<FLOWRECORD_ID>'" --json
```

Confirm `AssociatedRecordId` now equals the Campaign Id. This is what makes the Flow show up in the Campaign's "Flows" related list in the UI — the naming convention alone (step 6) does not.

### If the PATCH fails with `MISMATCHING_TYPES`

```json
[{ "message": "Campaign is associated with a Business Unit whose Data Space doesn't match with the Data Space set on the Flow", "errorCode": "MISMATCHING_TYPES", "fields": ["AssociatedRecordId"] }]
```

Only seen in orgs with more than one Data Space/Business Unit. Cause: the new Campaign's `BusinessUnitId` is `null` (default when created via plain `sf data create record`) while the Flow's `FlowRecord.DataSpaceId` resolved to the org's `"default"` Data Space — no match. Fix:

```powershell
# Find a working BusinessUnitId from any existing campaign in the org
sf data query --target-org <ORG_ALIAS> --query "SELECT Id, BusinessUnitId FROM Campaign WHERE BusinessUnitId != null LIMIT 1" --json

# Set it on your new Campaign
sf data update record --target-org <ORG_ALIAS> --sobject Campaign --record-id <CAMPAIGN_ID> --values "BusinessUnitId='<BUSINESS_UNIT_ID>'"
```

Then retry the `PATCH` on the `FlowRecord`. Confirmed fix (validated on the `sdo-sales` org, which has 2 Data Spaces — the original `sdo-alfa` reference org has only 1, so this never came up there).

## 6.6. Optional: wire the "dormant lead" exit branch (offer, don't force)

The chicken-and-egg problem that used to block this entirely — the branch needing the Flow's own Id — is solved once step 6 has run: the Flow's `Id` (301-prefix) and `FullName` now exist, so a second Tooling API `PATCH` on that same Flow record can add the branch. **This part is UNTESTED against a real org** (unlike the rest of this file) — offer it to the user as an experimental extra, not a guaranteed step, and fall back to the manual Flow Builder note below if it errors.

There's a second, more important reason this stayed manual, beyond the Id problem: the one real example on file (`data-model.md` §4.1) is itself broken — `IndividualId` was the literal string `"PLACEHOLDER"` (not a real record reference) and `FlowVersionId` was `null`. Copying that shape verbatim would template a known-broken action, which conflicts with this skill's own "never guess a schema, get a real example first" rule. **Before attempting this, check whether any *other* Flow in the target org has a genuinely wired `exitIndividualsFromFlow` action** (`SELECT Id, Metadata FROM Flow WHERE Metadata LIKE '%exitIndividualsFromFlow%'` via Tooling API) — if one exists with a real `IndividualId` value, use its shape as ground truth instead of the broken one below.

If no valid example exists in the org, don't guess the missing fields — instead hand the user this **ready-to-paste** element (not a script) for the final Decision's default path in Flow Builder, with the now-known values already filled in:

```json
{
  "name": "Exit_Dormant_Leads",
  "label": "Salir del flujo (lead inactivo)",
  "actionName": "<THIS_FLOW's_OWN_FullName_from_step_6>",
  "actionType": "exitIndividualsFromFlow",
  "inputParameters": [
    { "name": "IndividualId", "value": { "elementReference": "<REAL_INDIVIDUAL_VARIABLE — ask the user or find a working example; do not reuse the literal 'PLACEHOLDER' string from the broken reference build>" } },
    { "name": "FlowVersionId", "value": { "stringValue": "<THIS_FLOW's_OWN_Id_from_step_6>" } }
  ]
}
```

Attach it as `Decision_Interacted_After_Whatsapp`'s `defaultConnector` (currently unset, meaning "No" just ends the Flow). Tell the user this is optional and only worth wiring once they know the real `IndividualId` reference — same "don't invent it" rule as the engagement Decision conditions.

## 7. Build the final links

Confirmed working (validated by the user directly, 2026-07-27 — the CMS content editor for both Email and WhatsApp content resolves through the **standard Lightning record view route** using the `ManagedContent` object, not a custom CMS-app URL as one might expect).

Get the Lightning domain once per org:

```powershell
sf org display --target-org <ORG_ALIAS>
```

Take the `Instance Url` value and swap `.my.salesforce.com` → `.lightning.force.com` (same subdomain, different host). Example: `https://pr1774493035899.my.salesforce.com` → `https://pr1774493035899.lightning.force.com`.

| Link | Formula | Id source |
|---|---|---|
| Campaign | `https://<domain>/lightning/r/Campaign/<Id>/view` | `Id` returned by `sf data create record` in step 1 |
| Email | `https://<domain>/lightning/r/ManagedContent/<Id>/view` | `managedContentId` field in the step 3 POST response |
| WhatsApp | `https://<domain>/lightning/r/ManagedContent/<Id>/view` | `managedContentId` field in the step 4 POST response |
| Flow | `https://<domain>/builder_flow/flowBuilder.app?flowId=<Id>` | `id` field in the step 6 POST response (the Flow **version** Id, prefix `301`, not the `DefinitionId`) |

Present these at the end per SKILL.md's "Final Output Format" — this is the actual deliverable, don't skip it or bury it in a wall of JSON.

## CLI gotchas (apply to every command above)

- Run through **PowerShell**. The Bash tool fails on the `sf` CLI's `C:\Program Files\...` install path with `"C:\Program" no se reconoce como un comando interno o externo`.
- Never redirect `sf` command stderr with `2>&1` inside PowerShell for these calls — it wraps successful output in a `NativeCommandError` and pollutes the result. If you need to inspect a large JSON response, redirect stdout only (`> file.json`) and read the file, or better, keep responses on stdout and let the tool capture them directly.
- `sf api request rest` prints a `Warning: This command is currently in beta` line before the JSON body on every call — expected, not an error.
- Don't try `SF_TEMP_SHOW_SECRETS=true sf org display` to get the access token — it's blocked by the permission classifier. You don't need it; `sf api request rest -o <alias>` authenticates for you.
