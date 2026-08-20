# Salesforce Object Name Mapping (Spanish ↔ English)

When parsing the Data Dictionary, the tab/sheet name represents the Salesforce object.
These names may be in Spanish or English. Use this table to resolve them.

## Standard Objects

| Spanish Name | English Name | SF API Name |
|-------------|-------------|-------------|
| Cuenta | Account | Account |
| Contacto | Contact | Contact |
| Oportunidad | Opportunity | Opportunity |
| Caso | Case | Case |
| Lead / Prospecto / Cliente Potencial | Lead | Lead |
| Campaña | Campaign | Campaign |
| Tarea | Task | Task |
| Evento | Event | Event |
| Contrato | Contract | Contract |
| Pedido / Orden | Order | Order |
| Producto | Product | Product2 |
| Libro de precios / Lista de precios | Pricebook | Pricebook2 |
| Entrada de libro de precios | Pricebook Entry | PricebookEntry |
| Línea de oportunidad / Producto de oportunidad | Opportunity Line Item | OpportunityLineItem |
| Cotización / Presupuesto | Quote | Quote |
| Línea de cotización | Quote Line Item | QuoteLineItem |
| Activo | Asset | Asset |
| Solución | Solution | Solution |
| Artículo de conocimiento | Knowledge Article | Knowledge__kav |
| Grupo | Group | Group |
| Usuario | User | User |
| Perfil | Profile | Profile |
| Rol | Role | UserRole |
| Informe | Report | Report |
| Panel / Tablero | Dashboard | Dashboard |
| Archivo / Documento | Document | Document |
| Nota | Note | Note |
| Archivo adjunto | Attachment | Attachment |
| Feed | Feed | FeedItem |

## Matching Rules

1. **Exact match first** — check both Spanish and English columns
2. **Case-insensitive** — "contacto" matches "Contacto"
3. **With/without accents** — "Oportunidad" matches "Oportunidad"
4. **Plural forms** — "Contactos" should match "Contact", "Cuentas" should match "Account"
5. **If no match found** — assume it's a custom object. Append `__c` if not already present
6. **Ask the admin** — if ambiguous, present options and let them confirm the mapping

## Common Variations

Some orgs rename standard object tabs. If you see a tab name that doesn't match anything above but the fields look like a standard object (e.g., has `AccountId`, `OwnerId`), suggest the standard object mapping and confirm with the admin.
