# Template — Diccionario de datos

> La especificación técnica que **consume el agente de IA**. Valida: **arquitecto**. Semana 2 del Sprint 0. Skill: `pc-crm-salesforce-data-dictionary-generator`.

## Estructura mínima (por objeto Salesforce)

| Columna | Contenido |
|---|---|
| Objeto | API name + label (estándar o custom) |
| Campo | API name + label |
| Tipo | Tipo de campo SF (Text, Picklist, Lookup, Formula…) |
| Requerido | Sí/No (técnico y de negocio) |
| Valores | Para picklists: valores exactos (del schema real, nunca inventados) |
| Relación | Para lookups/master-detail: objeto destino |
| Record Types | Si aplica |
| Regla de negocio | Validaciones, automatizaciones, defaults |
| HU relacionada | ID(s) del Anexo B |

## Reglas

- Es el **insumo directo del agente de IA** en ejecución: todo campo que una HU toca debe estar acá antes de que la HU sea AI-ready.
- Los valores de picklist salen del schema real del org (getObjectSchema) — nunca inventar.
- Cambios post-freeze al modelo de datos = orden de cambio.
- Formato oficial: planilla (ver `_registry.md`); este esqueleto define las columnas mínimas.
