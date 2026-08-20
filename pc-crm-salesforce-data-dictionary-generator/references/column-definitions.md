# DDD Column Definitions

Each DDD sheet uses exactly these 13 columns (A through M), in this order. Do not add, remove, or reorder columns.

## Column A — Sección

Groups related fields visually. Common values:
- **Información del sistema** — for standard Salesforce fields (Owner, Name, CreatedBy, LastModifiedBy)
- **Ficha técnica** — for the core business fields of the object
- Custom section names as needed (e.g., "Resultados", "Configuración", "Integración", "Datos de contacto")

Rules:
- The first section must always be "Información del sistema"
- Write the section name only in the first row of each group; leave blank for subsequent rows in the same section

## Column B — Nombre del campo

The human-readable field label as it will appear in the Salesforce UI.

Rules:
- Maximum **40 characters** (Salesforce platform limit)
- Written in Spanish
- Descriptive and unambiguous
- If the name exceeds 40 chars, abbreviate sensibly (e.g., "No. Sujetos Eval. Medidos" instead of "Número de Sujetos de Evaluación Medidos")

## Column C — Nombre API Salesforce

The Salesforce API name for the field.

Rules:
- **UpperCamelCase** format
- English translation of the Spanish label
- Custom fields end with `__c` (double underscore + lowercase c)
- Standard fields use Salesforce-native names (e.g., `OwnerId`, `Name`, `CreatedById`, `LastModifiedById`)
- No spaces, no hyphens — only letters and underscores (for __c suffix)

Examples from the Medición sheet:
| Nombre del campo | Nombre API Salesforce |
|---|---|
| Propietario | OwnerId |
| Nombre de Medición | Name |
| Creado por | CreatedById |
| Última modificación por | LastModifiedById |
| Año | Year__c |
| Mes | Month__c |
| Tipo de medición | MeasurementType__c |
| Unidad / UEN | BusinessUnit__c |
| Canal | Channel__c |
| País | Country__c |
| Gerente Canal/Comercial | ChannelCommercialManager__c |
| # de medición | MeasurementNumber__c |
| Evaluador | Evaluator__c |
| Sujeto de evaluación | EvaluationSubject__c |
| Territorio | Territory__c |
| No. Sujetos Eval. Medidos | EvalSubjectsMeasured__c |
| Universo potencial (Eval) | EvalPotentialUniverse__c |
| % de penetración (Eval) | EvalPenetrationPercent__c |
| No. Sujetos Obs. medidos | ObsSubjectsMeasured__c |
| Universo potencial (Obs) | ObsPotentialUniverse__c |
| % de penetración (Obs) | ObsPenetrationPercent__c |

## Column D — Nombre API externo

The field name in an external system, only when the field maps to an integration.

Rules:
- Leave empty if no integration applies
- Fill with the external system's field name/path when integration is defined

## Column E — ¿Integrar?

Whether this field participates in an integration with an external system.

Values: **Sí** or **No**
Default: **No** (when no integration context is provided)

## Column F — Tipo de Dato

The Salesforce field type. Must be a valid Salesforce field type — see `salesforce-field-types.md` for the complete list.

Write it in the format used in the example:
- `Lookup (Usuario)` — for Lookup fields, specify the related object in parentheses
- `Auto Number` — for auto-number Name fields
- `Picklist` — single-select picklist
- `Multi-Select Picklist` — multi-select picklist
- `Text` — single-line text
- `Long Text Area` — multi-line text
- `Number (entero)` — whole numbers; use `Number (decimal)` for decimals
- `Formula (Percent)` — formula that returns a percentage
- `Checkbox` — boolean true/false

## Column G — Límite de caracteres (Si aplica)

The character or digit limit for the field, when applicable.

Rules:
- Fill for Text, Long Text Area, Number fields
- For Auto Number, show the format (e.g., `MD-{00000}`)
- Leave empty for Lookup, Checkbox, Picklist, Date, DateTime fields
- For Number fields, you can specify the total digits

## Column H — Valores del campo (si aplica)

Predefined values for Picklist and Multi-Select Picklist fields. Also used for formula expressions.

Rules:
- For Picklist: list values separated by semicolons (e.g., `ADHERENCIA; CONTROL`)
- For Formula: show the formula expression (e.g., `EvalSubjectsMeasured__c / EvalPotentialUniverse__c`)
- For Lookup: leave empty (the related object is in column F)
- For other types: leave empty unless there's a default value to note

## Column I — ¿Visible al Administrador del Sistema?

Whether the field is visible to the System Administrator profile.

Values: **Sí** or **No**
Default: **Sí** (most fields should be admin-visible)

Note: Fields that are Formula or Auto Number are typically visible to admins. Technical-only fields should also be visible to admins.

## Column J — Descripcion del Campo

A clear, concise description of the field's purpose. Explains what data the field stores and why.

Rules:
- Written in Spanish
- Factual and specific — no vague descriptions
- For system fields that auto-populate, note that (e.g., "Campo auto-populado a partir del Sujeto de evaluación seleccionado")
- For non-editable fields, mention it (e.g., "Campo estándar del sistema. No editable")
- For formula fields, explain the calculation logic in plain language

## Column K — Comentarios Adicionales

Additional notes, clarifications, or context about the field.

Rules:
- Use for technical notes (e.g., "Lookup al objeto User")
- Use for business context (e.g., "Por ahora solo contiene el valor B4B. Se podrán agregar más valores en el futuro")
- Use for formula details (e.g., "Campo de fórmula, no editable. Considerar manejo de división por cero")
- Use for validation notes or pending decisions
- Can be left empty if column J is sufficient

## Column L — ¿Obligatorio para la CREACIÓN?

Whether this field is required when creating a new record of this object.

Values: **Sí** or **No** or **-** (dash, for system fields that auto-populate)

Rules:
- Standard system fields (CreatedBy, LastModifiedBy) → **-** (auto-populated)
- Auto Number Name → **-** (auto-generated)
- OwnerId → **-** (defaults to creating user)
- Formula fields → **No** (calculated, not entered)
- Business-required fields → **Sí**
- Optional fields → **No**

## Column M — Tipo

Whether the field is standard or custom.

Values:
- **Estándar** — fields that come out-of-the-box with Salesforce
- **Personalizado** — custom fields created for the project (any field with `__c` in its API name)
