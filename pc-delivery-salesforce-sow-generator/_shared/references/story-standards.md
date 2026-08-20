<!-- ⚠️ AUTO-COPIADO desde _shared/sow/ por sync.sh — NO EDITAR ACÁ. Edita el canónico y vuelve a correr sync.sh. -->

# Estándares de historia de usuario del SOW (familia SOW — comercial y delivery)

Reglas comunes de redacción y clasificación que aplican a TODA historia de un SOW de
ProContacto, tanto en el SOW comercial (historias como `QuoteLineItem` sobre una Quote,
`pc-sales-sf-sow-builder`) como en el SOW Refinado de delivery (documento Word,
`pc-delivery-salesforce-sow-generator`). Mantener estas reglas idénticas en ambos lados es lo
que hace que delivery pueda **refinar** el alcance comercial en Sprint 0 en lugar de reescribirlo.

## Tipo de Funcionalidad (Estándar / Personalizada / Híbrida)

Toda historia se clasifica, priorizando SIEMPRE el estándar ("clicks before code"):

- **Estándar**: se resuelve con configuración out-of-the-box (objetos/campos estándar, page
  layouts, list views, reglas de validación, Flows declarativos simples, reportes).
- **Personalizada**: requiere código o componentes custom (Apex, LWC, objetos custom no
  triviales, integraciones a medida).
- **Híbrida**: combina configuración estándar + una porción custom.

Cuando la clasificación es **Personalizada** o **Híbrida**, la justificación es obligatoria:
explicar por escrito por qué el estándar no cubre el caso ("Por limitaciones de la funcionalidad
estándar de X, se realizará Y"). Cuando el proceso del cliente sea innecesariamente complejo,
cuestionarlo y proponer la alternativa estándar de Salesforce explicando el trade-off.

Dónde vive la clasificación:
- **Comercial**: en `QuoteLineItem.Scope__c` (no se ve en el contrato; la lee implementación).
- **Delivery**: campo "Tipo de Funcionalidad" de cada historia del documento.

## Narrativa

- Formato: **"Como [ACTOR], quiero [ACCIÓN], para [BENEFICIO]"**.
- **ACTOR** = rol real del cliente (Ejecutivo comercial, Supervisor de ruta, Agente de servicio,
  Administrador del sistema) — nunca "usuario" a secas.
- **ACCIÓN** = capacidad concreta sobre la plataforma.
- **BENEFICIO** = valor de negocio; no una repetición de la acción. Toda historia resuelve una
  problemática puntual del negocio del cliente — no se admiten historias que sean solo
  configuración técnica sin valor de negocio (la configuración va como criterio/tarea dentro de
  una historia con valor).
- **Una historia = una capacidad.** Si la narrativa necesita dos "quiero", son dos historias.

## Criterios de Aceptación

- **3 a 6 por historia**, cada uno **verificable en una demo** (condición observable, no
  intención ni adjetivo interpretativo).
- Incluir criterios **negativos/de borde** cuando el proceso lo amerite ("Si el candidato no
  posee correo electrónico, el sistema impedirá la conversión mostrando un mensaje de error").
- Redactarlos coloquiales y factuales, usando **labels de campos**, no API names.
- **NO inventar requisitos no funcionales (NFR):** nada de SLAs/umbrales fabricados ("responde
  en < X segundos", uptime, performance) que no estén en el contexto provisto. Un NFR solo se
  incluye si el cliente/contexto lo especifica.

## Completitud

- Todo proceso reconstruido del negocio debe quedar cubierto por al menos una historia
  (trazabilidad proceso→historias).
- Recorrer SIEMPRE el checklist de procesos transversales (`transversal-checklist.md`, en esta
  misma carpeta): por cada transversal, generar historia(s), diferir con nota explícita, o
  delimitar negativamente ("No se considera…").
- Lo detectado pero excluido va a **Fuera de Alcance** con narrativa resumida, motivo y estado
  ("En revisión" por defecto) — nunca se pierde en silencio.
