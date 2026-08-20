# Salesforce Custom Field Types

This is the definitive list of field types available in Salesforce. When populating column F ("Tipo de Dato") of the DDD, you must use ONLY types from this list. Never invent field types.

## Text-Based Fields

| Type | DDD Label | Description | Character Limit |
|------|-----------|-------------|-----------------|
| Text | Text | Single-line text | Up to 255 chars |
| Text Area | Text Area | Multi-line text, plain | Up to 131,072 chars |
| Long Text Area | Long Text Area | Large multi-line text | Up to 131,072 chars |
| Rich Text Area | Rich Text Area | Formatted text with HTML | Up to 131,072 chars |
| Text (Encrypted) | Text (Encrypted) | Encrypted text field | Up to 175 chars |

## Numeric Fields

| Type | DDD Label | Description | Notes |
|------|-----------|-------------|-------|
| Number | Number (entero) or Number (decimal) | Numeric value | Specify integer vs decimal in DDD |
| Currency | Currency | Monetary amount | Includes currency code |
| Percent | Percent | Percentage value | Stored as decimal |
| Auto Number | Auto Number | Auto-incrementing identifier | Format specified in column G |

## Date/Time Fields

| Type | DDD Label | Description |
|------|-----------|-------------|
| Date | Date | Date only (no time) |
| Date/Time | DateTime | Date and time combined |
| Time | Time | Time only (no date) |

## Selection Fields

| Type | DDD Label | Description |
|------|-----------|-------------|
| Checkbox | Checkbox | Boolean true/false |
| Picklist | Picklist | Single-select dropdown |
| Multi-Select Picklist | Multi-Select Picklist | Multi-select dropdown |

## Relationship Fields

| Type | DDD Label | Description |
|------|-----------|-------------|
| Lookup | Lookup (Objeto) | Soft reference to another object — specify the related object in parentheses |
| Master-Detail | Master-Detail (Objeto) | Hard parent-child relationship — specify the parent object in parentheses |
| Hierarchical | Hierarchical | Self-referencing lookup (User object only) |
| External Lookup | External Lookup | Lookup to an external object |
| Indirect Lookup | Indirect Lookup | Lookup using external ID |

## Computed / Special Fields

| Type | DDD Label | Description |
|------|-----------|-------------|
| Formula | Formula (return_type) | Calculated field — specify return type in parentheses: Text, Number, Currency, Date, DateTime, Percent, Checkbox |
| Roll-Up Summary | Roll-Up Summary | Aggregation from child records (only on master side of Master-Detail) |

## Other Fields

| Type | DDD Label | Description |
|------|-----------|-------------|
| URL | URL | Web address / hyperlink |
| Email | Email | Email address with validation |
| Phone | Phone | Phone number |
| Geolocation | Geolocation | Latitude/longitude coordinates |

## Standard Field Types (not created as custom, but appear in DDD)

These are field types that exist on standard fields. You don't "create" them, but they appear in the DDD for documentation purposes:

| Type | DDD Label | Context |
|------|-----------|---------|
| Lookup (Usuario) | Lookup (Usuario) | OwnerId, CreatedById, LastModifiedById |
| Auto Number | Auto Number | Name field when configured as auto-number |
| Text | Text | Name field when configured as text |

## DDD Label Conventions

When writing the type in column F:
- For Lookup and Master-Detail, always specify the related object: `Lookup (Usuario)`, `Lookup (Account)`, `Master-Detail (Opportunity)`
- For Formula, always specify the return type: `Formula (Percent)`, `Formula (Text)`, `Formula (Number)`
- For Number, clarify integer vs decimal: `Number (entero)`, `Number (decimal)`
- For all others, use the plain label: `Text`, `Picklist`, `Checkbox`, `Date`, etc.
