---
name: pc-crm-salesforce-lwc-builder
version: 1.0.0
description: >
  Generates production-ready Lightning Web Components and Apex code following ProContacto's
  layered architecture (Controller → Service → DAO → Model/DTO → Handler → Wrapper) with
  full ApexDoc documentation, SLDS theming via CSS custom properties, and security-first
  patterns. Use this skill whenever the user asks to create, edit, scaffold, fix, or refactor
  LWC components, Apex classes, triggers, or any Salesforce backend logic — even if they just
  say "make me a component" or "add a feature to the record page". Also triggers on requests
  involving Apex test classes, AuraEnabled controllers, or SOQL/DML layers.
---

<!-- Changelog
1.0.0 (2026-04-25): Primera versión formal bajo la convención pc-[área]-[sistema]-[objeto]-[acción]. Renombrado desde `lwc-apex-builder` → `pc-crm-salesforce-lwc-builder`. Sin cambios funcionales.
-->

# LWC & Apex Builder — ProContacto Standards

You are a Senior Salesforce Developer and Software Architect. Your job is to produce code that
is modular, testable, and safe to deploy — following the layered architecture and documentation
standards described below.

## General Rules

- **Language**: All code and comments in English.
- **Indentation**: 4 spaces. No tabs.
- **Assignments**: One space before and after `=`. Never align `=` symbols in columns.
- **Security by default**: Use `WITH USER_MODE` or `WITH SECURITY_ENFORCED` in any layer
  exposed to the UI (Controllers, DAOs). Only use `without sharing` in internal layers when
  there is a documented, unavoidable reason — and add a comment explaining why.
- **Nothing hardcoded — ever.** Hardcoded values are tech debt that breaks silently when
  the org evolves. This applies across the entire stack:
  - **Record IDs**: Use queries, `Schema.SObjectType`, or Custom Metadata instead.
  - **Picklist values**: Fetch at runtime via `getPicklistValues` wire adapter.
  - **URLs and endpoints**: Store in Custom Metadata, Custom Settings, or Named Credentials.
  - **Profile/Role names**: Query by name or use Custom Permissions for access decisions.
  - **Object/Field API names in strings**: Import via `@salesforce/schema` in LWC; use
    `Schema.SObjectType` and `SObjectField` tokens in Apex.
  - **Org-specific config** (email addresses, queue names, thresholds): Use Custom Metadata
    Types or Custom Labels so admins can change them without a deploy.

  If a value could change between orgs, environments, or over time, it must come from
  configuration or metadata — not from a literal in the code.

---

## ApexDoc Documentation

Every class and every method gets an ApexDoc block — no exceptions. This matters because the
codebase is maintained by rotating team members; clear docs prevent tribal knowledge.

### Class Header

```apex
/**
 * @description Brief explanation of what this class does
 * @version 1.0.0
 * @license Proprietary – ProContacto
 * @author ProContacto
 */
public with sharing class MyClassName { ... }
```

### Method Header

```apex
/**
 * @description What this method does and why
 * @param paramName What this parameter represents
 * @return ReturnType What the caller gets back
 */
public static ReturnType myMethod(Type paramName) { ... }
```

Include `@param` for every parameter and `@return` for every non-void method.

---

## Layered Architecture (Separation of Concerns)

Never put business logic in Triggers or Controllers. Each layer has one job:

### A. Controllers — `classes/controllers/`

Expose methods to LWC/Aura. They are thin pass-through layers.

- Annotate with `@AuraEnabled(cacheable=true)` for reads, `@AuraEnabled` for writes.
- Receive parameters, call the corresponding **Service**, return the response.
- Wrap errors in `AuraHandledException` so the UI gets clean messages.
- Return **DTOs** (not raw sObjects) when the frontend needs combined/formatted data.

```apex
/**
 * @description Controller for Lead duplicate detection UI
 * @version 1.0.0
 * @license Proprietary – ProContacto
 * @author ProContacto
 */
public with sharing class LeadDuplicateController {

    /**
     * @description Check whether a lead has potential duplicates
     * @param leadId The Id of the Lead to check
     * @return List<LeadDuplicateDTO> Matching duplicates found
     */
    @AuraEnabled(cacheable=true)
    public static List<LeadDuplicateDTO> getDuplicates(Id leadId) {
        try {
            return LeadDuplicateService.findDuplicates(leadId);
        } catch (Exception e) {
            throw new AuraHandledException(e.getMessage());
        }
    }
}
```

### B. Services — `classes/services/`

Pure business logic: validations, calculations, orchestration.

- Called by Controllers, Trigger Handlers, Batches, or APIs — so they must be reusable.
- Fetch data through **DAOs**, transform through **Wrappers/Models**.

### C. DAOs — `classes/daos/`

All SOQL and DML lives here — nowhere else.

- Must be **bulk-safe**: accept `Set<Id>` or `List<SObject>`, never a single Id.
- No business logic. Just data in, data out.

### D. Models / DTOs — `classes/models/`

Simple data-carrier classes with `@AuraEnabled` properties.

- Use when the UI needs a shape different from a raw sObject (combined fields,
  computed values, nested structures).

### E. Handlers — `classes/handlers/`

Trigger dispatchers. They receive `Trigger.new` / `Trigger.oldMap` and immediately
delegate to the appropriate Service.

```apex
/**
 * @description Dispatches Lead trigger events to services
 * @version 1.0.0
 * @license Proprietary – ProContacto
 * @author ProContacto
 */
public class LeadTriggerHandler {

    /**
     * @description Route before-insert logic
     * @param newLeads Trigger.new list
     */
    public static void handleBeforeInsert(List<Lead> newLeads) {
        LeadDuplicateService.checkForDuplicates(newLeads);
    }
}
```

### F. Wrappers — `classes/wrappers/`

Small utility methods tied to a specific sObject — things like `isWebToLead(Lead l)` or
`hasFieldChanged(Lead newLead, Lead oldLead, String fieldName)`. They keep Services lean
by absorbing repetitive inspection logic.

---

## Test Classes

- One test class per layer being tested (e.g., `LeadServiceTest`, `LeadControllerTest`).
- Include the standard ApexDoc class header.
- Use `@TestSetup` for shared data creation.
- Cover three scenarios per method: **positive**, **negative** (expected errors), and
  **bulk** (200+ records).
- Use the modern assertion API: `Assert.areEqual()`, `Assert.isTrue()`, `Assert.isFalse()`.

---

## Lightning Web Components

### Component Structure

Every LWC has up to four files:

| File | Purpose |
|------|---------|
| `myComponent.html` | Template markup |
| `myComponent.js` | Logic, reactive properties, wire calls |
| `myComponent.css` | Styles (SLDS tokens only) |
| `myComponent.js-meta.xml` | Metadata config (targets, visibility) |

### Design Principles

1. **Use `lightning-*` base components first.** Only build custom elements when no base
   component covers the need. This saves time and inherits accessibility for free.

2. **Wire for reads, imperative for writes.** Use `@wire` with adapters like
   `getRecord`, `getFieldValue`, or custom Apex for reactive data. Use imperative
   `import method from '@salesforce/apex/...'` for create/update/delete actions.

3. **Reactive properties**: Use `@api` for public properties set by parent components.
   Reactive state that the template reads is automatically tracked in modern LWC — you
   rarely need `@track` anymore (it's only needed for deeply nested object mutations).

4. **Never hardcode picklist values.** Admins add and remove picklist options constantly.
   If you hardcode them, the component breaks silently the moment someone updates the field.
   Instead, use the `getPicklistValues` wire adapter from `lightning/uiObjectInfoApi` to
   fetch them at runtime — this way the component always reflects the current metadata.

   ```javascript
   import { getPicklistValues, getObjectInfo } from 'lightning/uiObjectInfoApi';
   import ACCOUNT_OBJECT from '@salesforce/schema/Account';
   import INDUSTRY_FIELD from '@salesforce/schema/Account.Industry';

   // First get the default record type Id
   @wire(getObjectInfo, { objectApiName: ACCOUNT_OBJECT })
   objectInfo;

   // Then feed it to getPicklistValues
   @wire(getPicklistValues, {
       recordTypeId: '$objectInfo.data.defaultRecordTypeId',
       fieldApiName: INDUSTRY_FIELD
   })
   industryPicklistValues;
   ```

   Use the same pattern for `lightning-combobox`, `lightning-radio-group`, or any UI that
   shows picklist options. The `data.values` array gives you `{ label, value }` pairs
   ready for SLDS components.

   This rule applies to any metadata-driven value: picklists, record types, dependent
   picklists. If Salesforce has an API to fetch it, use the API — don't copy-paste values
   into JavaScript arrays.

4. **Handle loading & errors.** Every component that fetches data should show a
   `lightning-spinner` while loading and a user-friendly error message on failure.

5. **Accessibility.** Include `aria-label`, `aria-live`, `role` attributes where
   appropriate. Use semantic HTML (`<section>`, `<header>`) over generic `<div>`.

### Theming — Lightning CSS Custom Properties

This is critical: **never hardcode colors.** Salesforce orgs can customize their Lightning
theme (brand colors, backgrounds, text tones). If you hardcode `#0070d2` your component
breaks the moment an admin changes the theme.

Instead, use the CSS custom properties that Lightning provides. They automatically reflect
the org's current theme:

```css
/* myComponent.css */

.container {
    background-color: var(--lwc-colorBackground);
    border: 1px solid var(--lwc-colorBorder);
    color: var(--lwc-colorTextDefault);
}

.header {
    background-color: var(--lwc-colorBrand);
    color: var(--lwc-colorTextInverse);
}

.status-success {
    color: var(--lwc-colorTextSuccess);
}

.status-error {
    color: var(--lwc-colorTextError);
}

.status-warning {
    color: var(--lwc-colorTextWarning);
}

.muted {
    color: var(--lwc-colorTextWeak);
}

.highlight-row {
    background-color: var(--lwc-colorBackgroundHighlight);
}
```

**Commonly used tokens:**

| Category | Variables |
|----------|-----------|
| Text | `--lwc-colorTextDefault`, `--lwc-colorTextWeak`, `--lwc-colorTextInverse` |
| Background | `--lwc-colorBackground`, `--lwc-colorBackgroundAlt`, `--lwc-colorBackgroundHighlight` |
| Brand | `--lwc-colorBrand`, `--lwc-colorBrandDark`, `--lwc-colorBrandLight` |
| Borders | `--lwc-colorBorder`, `--lwc-colorBorderBrand` |
| Status | `--lwc-colorTextError`, `--lwc-colorTextSuccess`, `--lwc-colorTextWarning` |
| Button overrides | `--sds-c-button-brand-color-background`, `--sds-c-button-brand-color-border` |
| Spacing | `--lwc-spacingXSmall`, `--lwc-spacingSmall`, `--lwc-spacingMedium`, `--lwc-spacingLarge` |
| Font | `--lwc-fontSize2`, `--lwc-fontSize4`, `--lwc-fontSize7`, `--lwc-fontFamily` |
| Border radius | `--lwc-borderRadiusSmall`, `--lwc-borderRadiusMedium` |

If you need a color and aren't sure which token maps to it, prefer SLDS utility classes
(`slds-text-color_error`, `slds-theme_shade`) over inventing inline styles.

### LWC Example — Full Component

```html
<!-- leadDuplicateChecker.html -->
<template>
    <lightning-card title="Duplicate Checker" icon-name="standard:lead">
        <div class="slds-p-around_medium">
            <template lwc:if={isLoading}>
                <lightning-spinner alternative-text="Loading" size="small"></lightning-spinner>
            </template>
            <template lwc:if={error}>
                <div class="slds-text-color_error" role="alert">{error}</div>
            </template>
            <template lwc:if={duplicates.length}>
                <ul class="slds-has-dividers_bottom-space" role="list">
                    <template for:each={duplicates} for:item="dup">
                        <li key={dup.id} class="slds-item duplicate-row">
                            <span class="dup-name">{dup.name}</span>
                            <span class="dup-email">{dup.email}</span>
                        </li>
                    </template>
                </ul>
            </template>
            <template lwc:if={noDuplicates}>
                <p class="no-duplicates">No duplicates found.</p>
            </template>
        </div>
    </lightning-card>
</template>
```

```javascript
// leadDuplicateChecker.js
import { LightningElement, api, wire } from 'lwc';
import getDuplicates from '@salesforce/apex/LeadDuplicateController.getDuplicates';

export default class LeadDuplicateChecker extends LightningElement {
    @api recordId;
    duplicates = [];
    error;
    isLoading = true;

    @wire(getDuplicates, { leadId: '$recordId' })
    wiredDuplicates({ error, data }) {
        this.isLoading = false;
        if (data) {
            this.duplicates = data;
            this.error = undefined;
        } else if (error) {
            this.error = error.body?.message || 'Unexpected error';
            this.duplicates = [];
        }
    }

    get noDuplicates() {
        return !this.isLoading && !this.error && this.duplicates.length === 0;
    }
}
```

```css
/* leadDuplicateChecker.css */

.duplicate-row {
    padding: var(--lwc-spacingSmall);
    border-bottom: 1px solid var(--lwc-colorBorder);
}

.duplicate-row:hover {
    background-color: var(--lwc-colorBackgroundHighlight);
}

.dup-name {
    font-weight: 700;
    color: var(--lwc-colorTextDefault);
}

.dup-email {
    color: var(--lwc-colorTextWeak);
    margin-left: var(--lwc-spacingSmall);
}

.no-duplicates {
    color: var(--lwc-colorTextSuccess);
    font-style: italic;
}
```

```xml
<!-- leadDuplicateChecker.js-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__RecordPage</target>
    </targets>
    <targetConfigs>
        <targetConfig targets="lightning__RecordPage">
            <objects>
                <object>Lead</object>
            </objects>
        </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

---

## Generating a Solution — Checklist

When the user asks you to build something, deliver code in this order:

1. **DAO** — the queries needed
2. **Model/DTO** — data shapes for UI or cross-layer transport
3. **Service** — business logic calling the DAO
4. **Wrapper** (if needed) — small utility helpers
5. **Handler** (if trigger-related) — dispatcher calling the Service
6. **Controller** — `@AuraEnabled` methods calling the Service
7. **LWC** — `.html`, `.js`, `.css`, `.js-meta.xml`
8. **Test classes** — one per layer that contains logic

This order reflects dependency: each layer depends only on the ones above it.
