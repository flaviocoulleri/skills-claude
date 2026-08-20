# Salesforce Limits and Validation Rules

## Field Limits Per Object

| Edition | Custom Fields per Object | With Permission |
|---------|------------------------|-----------------|
| Enterprise | 500 | 800 (via support request) |
| Unlimited | 500 | 800 |
| Developer | 500 | 500 |

**Alert threshold:** Warn the admin when custom field count reaches 80% of the limit (400+ fields).

## Field Type Constraints

| Data Type | Max Length | Notes |
|-----------|-----------|-------|
| Text | 255 chars | — |
| Text Area | 255 chars | Plain text only |
| Long Text Area | 131,072 chars | Not searchable, not filterable |
| Rich Text Area | 131,072 chars | Supports HTML formatting |
| Number | 18 digits | Including decimal places |
| Currency | 18 digits | Including decimal places |
| Percent | 18 digits | Including decimal places |
| Auto Number | — | Display format up to 30 chars |
| Phone | 40 chars | — |
| Email | 80 chars | — |
| URL | 255 chars | — |

## Picklist Limits

| Limit | Value |
|-------|-------|
| Active values per picklist | 1,000 |
| Inactive values per picklist | 1,000 |
| Total values (active + inactive) | 2,000 |
| Characters per picklist value | 255 |
| Global Value Sets per org | 500 |

## Relationship Limits

| Limit | Value |
|-------|-------|
| Master-Detail per object | 2 |
| Lookup per object | 40 (varies by edition) |
| Cascade delete depth | 3 levels |

## Naming Validation Rules

### Valid API Name Pattern
```regex
^[a-zA-Z][a-zA-Z0-9_]*__c$
```

### Rejected Patterns
- Starts with number
- Contains spaces or special characters (except underscore)
- Reserved words: `Name`, `Id`, `Type`, `Status`, `Owner`, `Record`
- Generic names: `field1`, `test`, `value`, `data`, `info`, `temp`, `custom`, `new`
- Shorter than 3 characters (before `__c`)

### CamelCase Enforcement
Transform examples:
- `customer segment` → `customerSegment__c`
- `order_delivery_date` → `orderDeliveryDate__c`
- `ACCOUNT TYPE` → `accountType__c`

## PII Detection Keywords

Flag fields whose API name or description contains any of these terms:

**Identity:** `ssn`, `social_security`, `passport`, `dni`, `cuil`, `cuit`, `national_id`, `license_number`, `cedula`

**Financial:** `credit_card`, `bank_account`, `routing_number`, `salary`, `compensation`, `income`, `tax_id`

**Health:** `medical`, `health`, `diagnosis`, `prescription`, `patient`, `blood_type`

**Authentication:** `password`, `token`, `secret`, `api_key`, `credential`

**Personal:** `date_of_birth`, `birthdate`, `gender`, `ethnicity`, `religion`, `sexual_orientation`

When PII is detected:
1. Flag the field clearly
2. Recommend Shield Platform Encryption if available
3. Recommend restricted FLS (not visible to standard profiles)
4. Suggest audit trail configuration
