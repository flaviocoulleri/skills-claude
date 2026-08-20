# Example DDD Sheet — Medición

This is the complete Medición sheet from a real CG Cloud project DDD. Use it as the canonical example of how a DDD sheet should look.

**Sheet tab name:** Medición
**Object:** Medición (Custom Object)

| Row | Sección | Nombre del campo | Nombre API Salesforce | Nombre API externo | ¿Integrar? | Tipo de Dato | Límite chars | Valores del campo | ¿Visible Admin? | Descripcion del Campo | Comentarios Adicionales | ¿Obligatorio CREACIÓN? | Tipo |
|-----|---------|------------------|-----------------------|-------------------|-------------|--------------|-------------|-------------------|-----------------|----------------------|------------------------|----------------------|------|
| 2 | Información del sistema | Propietario | OwnerId | | No | Lookup (Usuario) | | | Sí | Indica el propietario asignado al registro de medición | N/A | - | Estándar |
| 3 | Información del sistema | Nombre de Medición | Name | | No | Auto Number | MD-{00000} | | Sí | Identificador único del registro de medición. Formato auto-numérico secuencial | Formato: MD-00001, MD-00002, etc. | - | Estándar |
| 4 | Información del sistema | Creado por | CreatedById | | No | Lookup (Usuario) | | | Sí | Usuario que creó el registro de medición | Campo estándar del sistema. No editable | - | Estándar |
| 5 | Información del sistema | Última modificación por | LastModifiedById | | No | Lookup (Usuario) | | | Sí | Usuario que realizó la última modificación al registro de medición | Campo estándar del sistema. No editable | - | Estándar |
| 6 | Ficha técnica | Año | Year__c | | No | Picklist | | 2020; 2021; 2022; 2023; 2024; 2025; 2026; 2027 | Sí | Año en el que se realiza la medición | | Sí | Personalizado |
| 7 | Ficha técnica | Mes | Month__c | | No | Picklist | | Enero; Febrero; Marzo; Abril; Mayo; Junio; Julio; Agosto; Septiembre; Octubre; Noviembre; Diciembre | Sí | Mes en el que se realiza la medición | Se muestra en el listado junto al Año (ej: 12/2025) | Sí | Personalizado |
| 8 | Ficha técnica | Tipo de medición | MeasurementType__c | | No | Picklist | | ADHERENCIA; CONTROL | Sí | Tipo de medición que se realiza. Se asigna de forma automática según el perfil del usuario | ADHERENCIA = Excelencia Comercial (EC). CONTROL = Gerente de País (GP). No editable por el usuario | Sí | Personalizado |
| 9 | Ficha técnica | Unidad / UEN | BusinessUnit__c | | No | Picklist | | B4B | Sí | Unidad Estratégica de Negocio asociada a la medición | Por ahora solo contiene el valor B4B. Se podrán agregar más valores en el futuro | Sí | Personalizado |
| 10 | Ficha técnica | Canal | Channel__c | | No | Picklist | | Desarrollador; Televentas | Sí | Canal comercial sobre el cual se realiza la medición | Se muestra como tercera línea en el listado de registros | Sí | Personalizado |
| 11 | Ficha técnica | País | Country__c | | No | Picklist | | Colombia; Costa Rica; El Salvador; Guatemala; Honduras; Nicaragua; Panamá; República Dominicana | Sí | País donde se ejecuta la medición | | Sí | Personalizado |
| 12 | Ficha técnica | Gerente Canal/Comercial | ChannelCommercialManager__c | | No | Lookup (Usuario) | | | Sí | Usuario con rol de Gerente de Canal o Comercial responsable de la medición | Lookup al objeto User | Sí | Personalizado |
| 13 | Ficha técnica | # de medición | MeasurementNumber__c | | No | Picklist | | 0 - Inicial; 1 - Primera; 2 - Segunda; 3 - Tercera | Sí | Número secuencial que indica la iteración de la medición realizada | Los valores representan la cantidad de mediciones previas realizadas sobre el mismo contexto | Sí | Personalizado |
| 14 | Ficha técnica | Evaluador | Evaluator__c | | No | Lookup (Usuario) | | | Sí | Usuario que genera el registro de medición. Se completa de forma automática con el usuario logueado | Campo auto-populado. No debe ser editable por el usuario en el formulario de creación | Sí | Personalizado |
| 15 | Ficha técnica | Sujeto de evaluación | EvaluationSubject__c | | No | Lookup (Usuario) | | | Sí | Usuario que será evaluado o medido en la medición | Lookup al objeto User | Sí | Personalizado |
| 16 | Ficha técnica | Territorio | Territory__c | | No | Text | 255 | | Sí | Territorio donde se realiza la medición. Se hereda del Sujeto de evaluación seleccionado | Campo auto-populado a partir del Sujeto de evaluación. Pendiente definir de qué campo del User se obtiene el territorio (requiere creación del campo en User si no existe) | Sí | Personalizado |
| 17 | Ficha técnica | No. Sujetos Eval. Medidos | EvalSubjectsMeasured__c | | No | Number (entero) | | | Sí | Cantidad de sujetos de evaluación que fueron medidos | | Sí | Personalizado |
| 18 | Ficha técnica | Universo potencial (Eval) | EvalPotentialUniverse__c | | No | Number (entero) | | | Sí | Cantidad total de sujetos de evaluación posibles en el universo de la medición | | Sí | Personalizado |
| 19 | Ficha técnica | % de penetración (Eval) | EvalPenetrationPercent__c | | No | Formula (Percent) | | EvalSubjectsMeasured__c / EvalPotentialUniverse__c | Sí | Porcentaje de penetración de evaluación. Resultado de dividir No. Sujetos Eval. Medidos entre Universo potencial (Eval) | Campo de fórmula, no editable. Considerar manejo de división por cero (si Universo = 0, mostrar 0%) | No | Personalizado |
| 20 | Ficha técnica | No. Sujetos Obs. medidos | ObsSubjectsMeasured__c | | No | Number (entero) | | | Sí | Cantidad de sujetos de observación que fueron medidos | | Sí | Personalizado |
| 21 | Ficha técnica | Universo potencial (Obs) | ObsPotentialUniverse__c | | No | Number (entero) | | | Sí | Cantidad total de sujetos de observación posibles en el universo de la medición | | Sí | Personalizado |
| 22 | Ficha técnica | % de penetración (Obs) | ObsPenetrationPercent__c | | No | Formula (Percent) | | ObsSubjectsMeasured__c / ObsPotentialUniverse__c | Sí | Porcentaje de penetración de observación. Resultado de dividir No. Sujetos Obs. medidos entre Universo potencial (Obs) | Campo de fórmula, no editable. Considerar manejo de división por cero (si Universo = 0, mostrar 0%) | No | Personalizado |

## Key Patterns to Observe

1. **Standard fields first** — rows 2-5 are always the system fields, in the "Información del sistema" section
2. **Section labels** — "Información del sistema" appears in column A for the first standard field row; "Ficha técnica" appears for the first custom field row. Subsequent rows in the same section repeat the section name.
3. **Picklist values** — separated by semicolons with spaces: `valor1; valor2; valor3`
4. **Formula expressions** — written as Salesforce formula syntax in column H
5. **Lookup type notation** — `Lookup (Usuario)` specifies the related object in parentheses
6. **Abbreviations** — used to stay within 40-char limit: "No." for "Número", "Eval." for "Evaluación", "Obs." for "Observación"
7. **Comentarios** — rich context: business rules, pending decisions, auto-population logic, edge cases
8. **Obligatorio column** — uses dash (-) for system/auto fields, Sí/No for the rest
