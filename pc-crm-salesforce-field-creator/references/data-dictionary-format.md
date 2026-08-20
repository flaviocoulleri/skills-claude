# Data Dictionary (Diccionario de Datos) Format

## Structure

The Data Dictionary is a spreadsheet (Google Sheets, .xlsx, or .csv) with:
- **Tutorial tab** — Usage instructions (skip when parsing)
- **Glosario tab** — Glossary of terms (skip when parsing)
- **One tab per Salesforce Object** — e.g., Contact, Account, Opportunity

## Column Schema (12 columns per object tab)

| # | Column Name | API Mapping | Required | Notes |
|---|------------|-------------|----------|-------|
| 1 | Nombre del campo | `label` | Yes | The field label as it should appear in Salesforce UI |
| 2 | Nombre API Salesforce | `apiName` | Yes | The API name of the field. Custom fields end in `__c` |
| 3 | Nombre API externo | `externalApiName` | No | API name in an external system, only if integration exists |
| 4 | ¿Integrar? | `integrate` | No | `Sí` / `No` / `-`. Indicates if field participates in an integration. Can be unidirectional or bidirectional |
| 5 | Tipo de dato | `dataType` | Yes | Salesforce data type (see mapping table below) |
| 6 | Límite de caracteres | `charLimit` | No | Maximum character length, only for text-based types |
| 7 | Valores del campo | `picklistValues` | Conditional | Required for Picklist and Multi-Select Picklist. All values must be listed |
| 8 | ¿Visible al Administrador? | `adminVisible` | No | Whether the System Admin profile can see/edit the field |
| 9 | Descripción del Campo | `description` | No | Functional description of the field |
| 10 | Comentarios Adicionales | `comments` | No | Additional notes from the client |
| 11 | ¿Obligatorio para la CREACIÓN? | `requiredForCreation` | No | Whether the field must be required — enforced via **Dynamic Forms**, NOT at field or page layout level |
| 12 | Tipo | `fieldType` | Yes | `Estándar` or `Personalizado`. Critical: Standard = native SF field, Personalizado = client-added custom field |

## Data Type Mapping

The "Tipo de dato" column may contain values in Spanish or English. Map them as follows:

| Spanish | English | SF Metadata Type |
|---------|---------|-----------------|
| Texto | Text | Text |
| Área de texto | Text Area | TextArea |
| Área de texto largo | Long Text Area | LongTextArea |
| Área de texto enriquecido | Rich Text Area | Html |
| Número | Number | Number |
| Moneda | Currency | Currency |
| Porcentaje | Percent | Percent |
| Fecha | Date | Date |
| Fecha/Hora | Date/Time | DateTime |
| Casilla de verificación / Checkbox | Checkbox | Checkbox |
| Lista de selección | Picklist | Picklist |
| Lista de selección múltiple | Multi-Select Picklist | MultiselectPicklist |
| Búsqueda / Lookup | Lookup | Lookup |
| Maestro-Detalle / Master-Detail | Master-Detail | MasterDetail |
| Fórmula | Formula | Formula type varies |
| Resumen | Roll-Up Summary | Summary |
| Numeración automática | Auto Number | AutoNumber |
| Teléfono | Phone | Phone |
| Email / Correo electrónico | Email | Email |
| URL | URL | Url |
| Geolocalización | Geolocation | Location |
| Dirección | Address | Address (compound) |

## Parsing Rules

1. Skip the "Tutorial" and "Glosario" tabs entirely
2. The tab name is the object name — may be in Spanish or English (see object-name-mapping.md)
3. Row 1 is always the header row
4. Empty rows should be skipped
5. If `fieldType` is "Estándar" or "Standard", the field already exists — use it only for reference/duplicate detection
6. Only fields with `fieldType` = "Personalizado" or "Custom" need to be created
7. If `picklistValues` is populated but `dataType` is not Picklist/Multi-Select, flag as a warning
8. The `integrate` column with value `Sí` means the field participates in integration — note direction if specified in comments
