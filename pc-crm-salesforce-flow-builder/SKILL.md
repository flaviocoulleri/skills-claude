---
name: pc-crm-salesforce-flow-builder
description: >
  Genera nombres estandarizados para Salesforce Flows y sus elementos internos siguiendo las convenciones de ProContacto.
  Cubre Screen Flows, Record-Triggered Flows, Schedule-Triggered Flows y Autolaunched Flows.
  Valida nombrado de variables, elementos, distribucion, best practices de performance, error handling y no-hardcoding.
  Use when creating, naming, reviewing, or documenting Salesforce Flows.
license: MIT
metadata:
  author: ProContacto
  version: "2.1.0"
  domain: platform
  triggers: flow, flows, salesforce flow, screen flow, record-triggered flow, schedule flow, autolaunched flow, RTF, SCF, STF, ALF, flow naming, flow builder, nombrado de flows, flow best practices
  role: expert
  scope: implementation
  output-format: documentation
  related-skills: pc-crm-salesforce-dev-guide, pc-crm-salesforce-lwc-builder, pc-crm-salesforce-field-creator
---

<!-- Changelog
2.1.0 (2026-04-25): Bump menor por aplicación de convención de naming pc-[área]-[sistema]-[objeto]-[acción]. Renombrado desde `sf-flow-builder` → `pc-crm-salesforce-flow-builder`. Sin cambios funcionales.
2.0.0: versión previa al rename.
-->

# Salesforce Flow Builder - ProContacto Standards

## Core Workflow

1. **Ask the admin for the Flow name** - ALWAYS ask the admin what name/label they want for the Flow. Never assume or generate the label without confirmation.
2. **Identify Flow type** - Determine if it's Screen (SCF), Record-Triggered (RTF), Schedule-Triggered (STF), or Autolaunched (ALF)
3. **Generate Flow name** - Apply the correct naming pattern for Label and API Name using the admin-provided name
4. **Require Description** - Every Flow and every element MUST have a Description field filled in
5. **Validate naming** - Ensure API Name is snake_case, Label follows the bracket convention, and abbreviations are correct
6. **Name internal elements** - Apply element naming conventions (Data, Logic, Interaction elements)
7. **Name variables** - Apply variable naming conventions with snake_case
8. **Validate best practices** - Check for performance anti-patterns, hardcoding, missing fault paths, null checks
9. **Review distribution method** - Confirm the Flow's distribution method matches its type
10. **Output summary** - Present a structured summary with Label, API Name, Description, element names, and distribution

---

## CRITICAL RULE: Always Ask the Admin

**NEVER generate a Flow Label without first asking the admin what they want it to be.**

The admin provides the descriptive name (e.g., "Establecer valores por defecto"). You then format it according to the naming convention for the corresponding Flow type.

Example interaction:
```
You: "Cual es el nombre/descripcion del Flow que queres crear?"
Admin: "Establecer valores por defecto"
You: "De que tipo es? (SCF, RTF, STF, ALF)"
Admin: "RTF"
-> Then you build: Account [RTF] | (CRT)-(FFU) | - Establecer valores por defecto | [SYN]
```

---

## CRITICAL RULE: Everything Must Have a Description

- **Flow Description**: Mandatory. Must explain the purpose, context, and expected behavior of the Flow.
- **Element Description**: Every single element (Screen, Get, Create, Update, Delete, Decision, Assignment, Loop, Subflow, Action) MUST have its Description field filled in explaining what it does and why.
- **Variable Description**: Every variable MUST have a description of its purpose.

If the admin does not provide a description, ASK for one. Never leave Description fields empty.

---

## CRITICAL RULE: No Hardcoding

**NEVER hardcode any of the following in Flow elements:**

| Forbidden | Use Instead |
|-----------|------------|
| Record IDs (15 or 18 char) | Get Records query or Custom Metadata Type |
| Email addresses | Custom Metadata Type, Custom Label, or Org-Wide Email Address |
| URLs | Custom Metadata Type or Custom Label |
| Profile/Role names as text | Get Records by Name or Custom Metadata Type |
| Picklist values as literal strings | Global Value Sets or Custom Metadata Type |
| Numeric thresholds / magic numbers | Custom Metadata Type or Custom Setting |
| Org-specific values | Custom Metadata Type or Custom Label |
| User IDs | Dynamic lookup (Owner, Running User, etc.) |

If a value might change between environments or over time, it MUST be configurable.

---

## Naming Patterns

### Screen Flow (SCF)

**Label format:**
```
{Objeto/Funcion} [SCF] - {Nombre dado por el admin}
```

**API Name format (snake_case):**
```
{objeto_funcion}_scf_{nombre_en_snake_case}
```

**Example:**
- Label: `Account [SCF] - Pantalla custom de creacion`
- API Name: `account_scf_pantalla_custom_de_creacion`

---

### Record-Triggered Flow (RTF)

**Label format:**
```
{Objeto} [RTF] | ({Trigger})-({Optimizacion}) | - {Nombre dado por el admin} | [{Ejecucion}]
```

**API Name format (snake_case):**
```
{objeto}_rtf_{trigger}_{optimizacion}_{nombre_en_snake_case}_{ejecucion}
```

**Example:**
- Label: `Account [RTF] | (CRT)-(FFU) | - Establecer valores por defecto | [SYN]`
- API Name: `account_rtf_crt_ffu_establecer_valores_por_defecto_syn`

#### Trigger Abbreviations

| Abbreviation | Meaning |
|-------------|---------|
| CRT | Created |
| UPD | Updated |
| COU | Created or Updated |
| DEL | Deleted |

#### Optimization Abbreviations

| Abbreviation | Meaning | When to Use |
|-------------|---------|-------------|
| FFU | Fast Field Updates (before save) | Only updating fields on the SAME triggering record. 10x faster, no DML consumed. |
| ARR | Actions and Related Records (after save) | Need to create/update OTHER records, send emails, call subflows, or invoke Apex. |

#### Execution Type Abbreviations

| Abbreviation | Meaning |
|-------------|---------|
| SYN | Contains synchronous path |
| ASY | Contains asynchronous path |
| SCH | Contains scheduled path |

---

### Schedule-Triggered Flow (STF)

**Label format:**
```
{Objeto/Proceso} [STF] | ({Frequency})-({Hora 24h}) | - {Nombre dado por el admin}
```

**API Name format (snake_case):**
```
{objeto_proceso}_stf_{frequency}_{hora}_{nombre_en_snake_case}
```

**Example:**
- Label: `Opportunity [STF] | (W)-(14:00) | - Notificar cierre proximo`
- API Name: `opportunity_stf_w_14_00_notificar_cierre_proximo`

#### Frequency Abbreviations

| Abbreviation | Meaning |
|-------------|---------|
| O | Once |
| D | Daily |
| W | Weekly |

---

### Autolaunched Flow (ALF)

**Label format:**
```
{Accion que realiza} [ALF] - ({Inputs y Outputs resumidos}) | [{Invocadores}]
```

**API Name format (snake_case):**
```
{accion_que_realiza}_alf_{inputs_outputs_resumidos}_{invocadores}
```

**Example:**
- Label: `Procesar valores labels [ALF] - (Recibe un string, retorna una coleccion de texto) | [F,A]`
- API Name: `procesar_valores_labels_alf_recibe_un_string_retorna_una_coleccion_de_texto_f_a`

#### Invoker Abbreviations

| Abbreviation | Meaning |
|-------------|---------|
| F | Flow |
| A | Apex |
| R | REST API |

---

## Element Naming Conventions

All element names MUST be unique within the Flow. Cloned elements MUST have their Labels and API Names adjusted. Every element MUST have a Description.

### Interaction Elements

| Element | Naming Pattern | Example |
|---------|---------------|---------|
| Screen | Brief description of process/element displayed | `Formulario de datos del contacto` |
| Action | Summary of selected action and result | `Send Email Notification to Owner` |
| Subflow | Brief description of obtained result | `Obtener datos de cuenta padre` |

### Data Elements

| Element | Naming Pattern | Example |
|---------|---------------|---------|
| Create Records | `Create {Description}` | `Create Account Records` |
| Update Records | `Update {Description}` | `Update Contact Status` |
| Get Records | `Get {Query description}` | `Get Related Opportunities` |
| Delete Records | `Delete {Records to delete}` | `Delete Expired Tasks` |
| Roll Back Records | `Roll Back {Element name}` | `Roll Back Create Account Records` |

### Logic Elements

| Element | Naming Pattern | Example |
|---------|---------------|---------|
| Assignment | `{Verb} {Details}` — Verbs: Set, Assign, Count, Add, Subtract, Remove | `Set Default Values for Account` |
| Decision | `{Verb} {Condition details}` — Verbs: Check, Validate, Verify | `Check if Account has Contacts` |
| Loop | `Loop {Exact collection name}` | `Loop colContactRecords` |
| Collection Sort | `Sort {Exact collection name}` | `Sort colOpportunityRecords` |
| Collection Filter | `Filter {Description} {Exact collection name}` | `Filter Active Items colProductRecords` |

### Decision Outcome Naming

- Each outcome in a Decision element MUST have a descriptive name (not "Outcome 1", "Outcome 2").
- Use clear, affirmative labels: `Has Contacts`, `Is Active`, `Amount Over Threshold`.
- The default outcome should be named descriptively: `No Contacts Found`, `Is Inactive`, `Below Threshold`.

---

## Variable Naming Conventions

All variables use **snake_case**. Every variable MUST have a Description. Naming by type:

| Type | Convention | Example |
|------|-----------|---------|
| Text | Brief description of stored value | `account_name` |
| Record | `{Object name}_record` | `account_record` |
| Record Collection | `col_{Object name}_records` | `col_contact_records` |
| Number | Brief description of stored value | `total_contacts` |
| Currency | Brief description of stored value | `discount_amount` |
| Boolean | Description of evaluated condition | `is_primary_contact` |
| Date | Description of stored date | `contract_start_date` |
| Date/Time | Description of stored date/time | `last_login_datetime` |
| Picklist | Brief description + `_pkl` | `status_options_pkl` |
| Multi-Select Picklist | Short description + `_msp` | `selected_categories_msp` |
| Apex-Defined | Brief description | `wrapper_result` |

---

## Best Practices - Performance & Governor Limits

### NEVER Put DML/SOQL Inside Loops

This is the #1 cause of production failures. Each iteration consumes 1 SOQL or 1 DML operation.

**WRONG - Get inside Loop:**
```
Loop -> Get Records -> Assignment -> (next iteration)
```
200 records = 200 SOQL queries. Limit is 100. FLOW FAILS.

**CORRECT - Collection pattern:**
```
Get Records (BEFORE loop) -> Loop -> Assignment (add to collection) -> (after loop) -> Update Records
```
1 SOQL + 1 DML regardless of record count.

**Rule**: Get Records, Create Records, Update Records, Delete Records MUST be OUTSIDE of loops. Inside loops, only use Assignment elements to build collections.

### Use Before-Save (FFU) for Same-Record Updates

- Before-save flows are **10x faster** than after-save flows.
- Before-save flows do NOT consume DML operations.
- ONLY use After-Save (ARR) when you need to create/update OTHER records, send emails, call subflows, or invoke Apex.
- **NEVER use After-Save to update the triggering record itself** — this wastes a DML.

### Consolidate Record-Triggered Flows

- Aim for maximum **1 before-save RTF and 1 after-save RTF per object** when possible.
- Multiple RTFs on the same object increase execution order complexity and risk of governor limit hits.
- Use Decision elements within a single RTF to handle multiple scenarios.

### Entry Conditions on RTFs

- ALWAYS define Entry Conditions on Record-Triggered Flows to filter unnecessary executions.
- Use formula-based conditions when checking multiple fields.
- This prevents the Flow from running on every single record change.

### Recursion Control

- Document recursion behavior in the Flow Description.
- Use the built-in "Run the flow only once per record update in a transaction" option when appropriate.
- If a Flow updates a record that triggers another Flow, ensure there is no infinite loop.

---

## Best Practices - Error Handling

### Fault Paths Are Mandatory

**Every data element (Get, Create, Update, Delete) MUST have a Fault Path connected.**

- Never leave a data element without a fault connector — this prevents silent failures.
- Use `{!$Flow.FaultMessage}` to capture and display meaningful error messages.

### Centralized Error Handling Subflow

Create a reusable **Autolaunched Flow** for error handling:
- **Inputs**: Flow Name, Element Name, Error Message, Record ID (optional)
- **Actions**: Log to custom "Flow_Error_Log__c" object, send email/Slack notification, post to Chatter
- Call this subflow from every fault path across all Flows.
- This allows modifying error handling logic in ONE place.

### Custom Error Messages in Screen Flows

- Use the **Custom Error** element for validation-style errors that keep users on the same screen.
- Provide clear, user-friendly messages — never show raw Salesforce errors to end users.
- Include context: what went wrong and what the user should do.

### Null Check After Every Get Records

**ALWAYS add a Decision element after Get Records to check if records were returned before using them.**

```
Get Records -> Decision (Check if records found) -> Yes: Continue / No: Handle empty result
```

Accessing fields on a null record variable causes an unhandled fault. Prevent it.

---

## Best Practices - Design & Maintenance

### Layout: Auto-Layout

- ALL Flows MUST use **Auto-Layout** view.
- Auto-Layout provides consistent, clean, and maintainable flow structures.
- Salesforce manages element positioning automatically.
- **No disconnected elements** in the active version.

### Subflows for Reusable Logic

- If the same logic appears in 2+ Flows, extract it into a Subflow (ALF).
- Subflows promote DRY principle and simplify maintenance.
- Document subflow inputs/outputs clearly.

### Version Tracking

- Use the Flow **Description** field to track version history:
  ```
  v1.0 - 2026-04-03 - Initial version: sets default values on account creation
  v1.1 - 2026-04-10 - Added validation for duplicate account names
  ```
- Update the description every time the Flow is modified.

### Language Rules

- Element naming mostly in **English**, except for custom field/object/element names.
- Flow Label (visible name) CAN be in **Spanish** (visible in documentation, error messages, logs).
- Descriptions can be in Spanish or English, as long as they are clear and complete.

---

## Pre-Activation Checklist

Before activating any Flow, verify ALL of the following:

| # | Check | Status |
|---|-------|--------|
| 1 | Flow has a Description filled in | |
| 2 | ALL elements have Descriptions | |
| 3 | ALL variables have Descriptions | |
| 4 | No Get/Create/Update/Delete inside loops | |
| 5 | ALL data elements have Fault Paths connected | |
| 6 | Decision after every Get Records (null check) | |
| 7 | No hardcoded IDs, emails, URLs, or magic numbers | |
| 8 | No disconnected elements | |
| 9 | All element names are unique | |
| 10 | API Names follow snake_case convention | |
| 11 | Flow Label follows naming convention with brackets | |
| 12 | Entry Conditions defined (for RTFs) | |
| 13 | Recursion control reviewed (for RTFs) | |
| 14 | Before-Save used for same-record updates (not After-Save) | |
| 15 | Subflow used for repeated logic | |
| 16 | Bulk tested with 200+ records (for RTFs) | |
| 17 | Decision outcomes have descriptive names (not "Outcome 1") | |
| 18 | Version history updated in Flow Description | |

---

## Flow Distribution Methods

| Flow Type | Distribution Methods |
|-----------|---------------------|
| Screen Flow | Lightning Page, Button, Quick Action, LWC, Experience Site, Utility Bar, URL |
| Autolaunched Flow | Apex, Process Builder, Subflow, API, Schedule, Platform Event |
| Record-Triggered Flow | Automatic execution on record changes |
| Scheduled Flow | Automatic CRON by date/time |
| Platform Event-Triggered | Executes on Platform Event publish |

---

## Initial Setup Checklist

When starting a new project with Flows:

1. **Managed Packages**: If the project has Managed Packages installed, create a copy of the Flow Templates that will be used
2. **Create List View** for Flows:
   - **Name**: `Custom Flows - ProContacto`
   - **Visibility**: All users can see this list view
   - **Columns**: Flow Label, Flow API Name, Flow Description, Process Type, Active, Trigger
   - **Filter**: Last Modified Date >= [Configuration day]
3. **Use the name generator** from the Data Dictionary for Flow naming

---

## Constraints

### MUST DO
- ALWAYS ask the admin for the Flow name before generating it
- Fill in Description on EVERY Flow, element, and variable — no exceptions
- Use snake_case for ALL API Names
- Include the type abbreviation in brackets: [SCF], [RTF], [STF], [ALF]
- Include trigger, optimization, and execution abbreviations for RTF flows
- Include frequency and time for STF flows
- Include invoker abbreviations for ALF flows
- Make all element names unique within the Flow
- Use Auto-Layout view for all Flows
- Add Fault Paths to ALL data elements (Get, Create, Update, Delete)
- Add null check Decision after every Get Records
- Keep Get/Create/Update/Delete OUTSIDE of loops — use collections
- Use Before-Save (FFU) for same-record updates
- Define Entry Conditions on all RTFs
- Use Custom Metadata Types or Custom Labels for configurable values
- Track version changes in Flow Description
- Bulk test RTFs with 200+ records before activation
- Use English for element naming (except custom names)
- Name Decision outcomes descriptively

### MUST NOT DO
- Generate Flow names without asking the admin first
- Leave any Description field empty on Flows, elements, or variables
- Hardcode IDs, emails, URLs, profile names, picklist values, or magic numbers
- Put Get Records, Create Records, Update Records, or Delete Records inside loops
- Use After-Save to update the triggering record itself
- Leave data elements without Fault Paths
- Use Get Records results without checking for null first
- Leave disconnected elements in the active version
- Use duplicate element names within a Flow
- Skip type abbreviations in Flow names
- Use camelCase or PascalCase for API Names (must be snake_case)
- Create recursive Flows without proper safeguards
- Name Decision outcomes as "Outcome 1", "Outcome 2", etc.
- Skip Entry Conditions on Record-Triggered Flows

---

## Interactive Mode

When the user asks to create or name a Flow, follow this process:

1. **Ask for the Flow name/description** — "Cual es el nombre/descripcion que queres para este Flow?"
2. **Ask for the Flow type** (SCF, RTF, STF, ALF) if not specified
3. **Ask for the object or function** involved
4. For RTF: Ask for trigger type, optimization, and execution type
5. For STF: Ask for frequency and scheduled time
6. For ALF: Ask for inputs/outputs summary and invokers
7. **Ask for the Flow Description** — "Que descripcion queres que tenga? Debe explicar que hace y por que."
8. Generate both **Label** and **API Name**
9. Present the result in a clear format:

```
Flow Label:       {generated label}
API Name:         {generated api name}
Type:             {flow type}
Description:      {admin-provided description}
Distribution:     {suggested distribution method}
Layout:           Auto-Layout
```

10. When reviewing elements, validate that all have descriptions and follow naming conventions.
11. When reviewing an existing Flow, run through the Pre-Activation Checklist and report issues.
