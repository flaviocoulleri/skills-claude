# DM follow-up — templates, banned phrases y catálogo de métricas (Fase 7)

> Contenido extraído del SKILL.md para no inflarlo. La Fase 7 mantiene el
> **flujo** (pasos 7.1–7.8); este archivo tiene los **templates de texto**, las
> **frases prohibidas** y el **catálogo de métricas por módulo**. Cárgalo cuando
> armes el draft del DM.

## Reglas de tono inviolables — banned phrases

Valida el draft contra esta tabla **antes** de mostrarlo. Si detectas una frase
de la columna izquierda, reescribí con la equivalente de la derecha **antes de
renderizar**. Una banned phrase bloquea el render.

| ❌ NO usar | ✅ Sí usar |
|---|---|
| "te pedí ayer" | "cuando puedas" |
| "te pedí varias veces" | "te paso este recordatorio" |
| "esto ya te lo dije" | "pásame por cada uno" |
| "arrancamos esta semana" | (omitir o "te paso un repaso") |
| "como te dije" | "como te comenté" (solo si fue 1 vez y en ese DM) |
| "necesito que" | "¿me ayudas con" |
| "tienes pendiente" | "está faltando" |
| "esto es urgente" / "tiene que estar ya" | "este lo necesitamos puntualmente" |
| "necesito que lo hagas primero" | "si puedes priorizarlo, mejor" |
| Comandos imperativos secos | Pedidos colaborativos |

El tono es **siempre** de pedido de ayuda colaborativo, nunca reclamo, nunca
escalamiento. Ante ambigüedad, errar del lado de la suavidad.

**Para la sección de alta prioridad** (`priority <= 2`): se permite (no
obligatorio) una frase de énfasis, siempre dentro del tono de pedido. NO usar
exclamación, mayúsculas ni emojis de alarma (⚠️🚨) — el tono se construye por
palabras, no por signos.

| ✅ Permitido | ❌ Prohibido |
|---|---|
| "este lo necesitamos puntualmente" | "esto es urgente" |
| "este me ayuda mucho que lo cierres esta semana" | "esto tiene que estar ya" |
| "si puedes priorizarlo, mejor" | "necesito que lo hagas primero" |

---

## Sugerencia por proyecto (Paso 7.4.c)

Cada ítem del DM lleva debajo una línea `→ Sugerencia: <acción puntual>`
(≤140 chars, generada por Haiku con el contexto del proyecto). Reglas:

| Situación | Forma de la sugerencia |
|---|---|
| `client_blocker != none` + responsable identificado | "hazle un push amigable a <Nombre/Rol> para que <acción concreta>" |
| `client_blocker != none` sin nombre | "haz push al referente del cliente para que <acción del blocker>" |
| `status_completeness = incomplete` | "actualiza el status existente con <golive / próximos pasos / ambos>" |
| `status_completeness = missing` sin blocker | "postear status hoy con <avance reciente del sprint / contexto>" |
| `recent_golive = true` | "comparte las métricas de adopción del primer mes: <métricas del módulo>" |
| `last_pm_post_days > 14` (severo) | "priorizar este: postear status hoy con un resumen completo" |
| `project_type = Support` sin blocker | "actualizar al comercial con horas consumidas + próxima review" |

Tono de la sugerencia (hereda las reglas inviolables): NO "tienes que",
"necesitas", "urgente", "ya". SÍ "haz push amigable", "actualiza cuando
puedas", "sumá las métricas", "priorizá". Imperativo voseo amigable.

**Casos especiales:** bloqueo interno a PC → "alinearte con <área>" en vez de
"push al cliente". Múltiples blockers → priorizar el más reciente, mencionar el
secundario en paréntesis. Sin nombre claro → usar rol genérico ("el referente
del cliente"), NUNCA inventar nombres. Si Haiku rompe tono → regenerar.
Fallback si Haiku falla: "postear status con el último avance" / "alinearte con
el referente del cliente". Nunca omitir la línea de sugerencia.

---

## Template del DM

```
[Si is_first_dm_today]
¡Hola <PM_FIRST_NAME>! ¿Cómo estás?

[Apertura SIEMPRE — sin "arrancamos esta semana" ni equivalentes]
Quería pedirte una mano con unos canales externos donde está faltando
update para el comercial SF.

═══════════════════════════════════════════════════════════
[BLOQUE A · DELIVERY — solo si hay items con project_type=Delivery]
═══════════════════════════════════════════════════════════

[Sub-bloque A.0 · Recientemente en producción — solo si hay items
 delivery con recent_golive=true]
🎉 Estos salieron a producción hace poco, ¿puedes pasarme métricas para
confirmar que se está usando?

<#CHANNEL_GL_1> — golive el 15/05 (hace 18 días) — Sales Cloud
  → cantidad de cuentas, oportunidades, contactos y cotizaciones creadas
    en el último mes
<#CHANNEL_GL_2> — golive el 25/05 (hace 8 días) — Marketing Cloud
  → cantidad de envíos del último mes, tasa de apertura y clicks
<#CHANNEL_GL_3> — golive el 20/05 (hace 13 días) — módulo no identificado
  → cuéntame qué módulo entregaste y te paso las métricas a chequear

[Sección de alta prioridad delivery, si hay items con priority <=2]
🚀 De delivery, estos los necesitamos puntualmente:

<#CHANNEL_P1> — P1 · hace 12 días sin status
  → Sugerencia: hazle un push amigable a Juan Pérez (sponsor) para que
    apruebe los wireframes que están trabando el Sprint 5
<#CHANNEL_P2> — P2 · hace 9 días sin status
  → Sugerencia: postear status hoy con el avance del UAT y la fecha
    estimada de salida a producción

[Status incompletos delivery]
En estos de delivery pasaste status hace poco pero quedó sin golive o
sin próximos pasos — si me los completas, mejor:

<#CHANNEL_X> — P4 · status del 22/05 sin golive

[Account Groups delivery — si una cuenta tiene >=2 proyectos delivery]
Para BetaCorp tienes 3 proyectos delivery activos, pásame status de los 3:
<#CHANNEL_BETA_1> — P3 · hace 14 días
<#CHANNEL_BETA_2> — P5 · hace 9 días
<#CHANNEL_BETA_3> — P5 · hace 8 días

[Resto delivery sin status >=7d]
Y en estos de delivery no veo update hace tiempo:

<#CHANNEL_A> — P3 · hace 31 días sin status
<#CHANNEL_B> — P5 · hace 18 días sin status

═══════════════════════════════════════════════════════════
[BLOQUE B · SOPORTE — solo si hay items con project_type=Support]
═══════════════════════════════════════════════════════════

🛟 Para los proyectos de soporte también necesito tu update:

[Sección de alta prioridad support]
[Status incompletos support]
[Account groups support]
[Resto support sin status >=7d]

<#CHANNEL_SUP_1> — P2 · hace 15 días sin status
<#CHANNEL_SUP_2> — P5 · hace 9 días sin status

═══════════════════════════════════════════════════════════
[BLOQUE C · BLOQUEOS DEL CLIENTE — cruza ambos tipos]
═══════════════════════════════════════════════════════════

[Solo si hay client_blocker != none en alguna fila, delivery o support]
Vi que algunos están trabados con el cliente:
• En <#CHANNEL_A> (delivery), el cliente todavía no nos contestó. Si lo
  destrabamos esta semana, la fecha tentativa de golive sería semana del 22/06.
• En <#CHANNEL_SUP_2> (soporte), el cliente no entregó los pendientes.

═══════════════════════════════════════════════════════════
[BLOQUE D · PROYECTOS FINALIZADOS — si los hay]
═══════════════════════════════════════════════════════════

Por otro lado, vi que estos proyectos figuran como activos pero ya cerraron.
¿Los das de baja del seguimiento?

<#CHANNEL_FIN_1> — finalizó el 12/05
<#CHANNEL_FIN_2> — finalizó el 03/05

═══════════════════════════════════════════════════════════
[CIERRES — uno por tipo, solo si hay items de ese tipo]
═══════════════════════════════════════════════════════════

[Cierre DELIVERY — solo si hay items delivery]
🚀 Para los de delivery, cuando puedas pásame por cada uno:

• Fecha estimada de golive del proyecto.
• **Qué módulo o producto se está entregando** (Sales Cloud, Service
  Cloud, Marketing Cloud, Consumer Goods Cloud, Field Service,
  Experience Cloud, CRM custom, Integration, etc.).
• Los próximos 2-3 pasos.
• Si el proyecto está en Sprint 0, la fecha de finalización del Sprint 0.
• Si ya está en un sprint posterior, la fecha de cierre del sprint actual.

[Cierre SOPORTE — solo si hay items support]
🛟 Para los de soporte, cuando puedas pásame por cada uno:

• Horas consumidas y horas restantes del contrato de soporte.
• Fecha de la próxima review o fecha de renovación / vencimiento del contrato.
• Issues o pendientes con el cliente que tengas activos.

[Cierre genérico bloqueos]
Si hay algo que se está trabando con el cliente (no responde, no define
temas, no entrega pendings) dime y vemos cómo destrabarlo entre los dos.

¡Gracias!
```

**Reglas de armado del DM (v2.8+):**
- Si solo hay items de un tipo (Delivery O Support), el otro bloque y su cierre
  se omiten completos. No renderizar headers vacíos.
- Account groups respetan el tipo: una cuenta con 2 delivery + 1 support → el
  group delivery va en Bloque A, el support standalone en Bloque B.
- Client blockers (Bloque C) mezclan ambos tipos pero etiquetan cada uno con su
  tipo entre paréntesis.
- Proyectos finalizados (Bloque D) no diferencian tipo.

**Reglas del sub-bloque A.0 — Recientemente en producción (v2.9+):**
- Una línea por proyecto con `recent_golive = true`. Formato
  `<#CHANNEL_ID> — golive el <DD/MM> (hace N días) — <Módulo>` + bullet de
  métricas del catálogo.
- `mentioned_module` null → "módulo no identificado" + fila Other del catálogo.
- Ordenar por `mentioned_golive_date DESC` (más recientes primero, en hypercare).
- Sin proyectos `recent_golive` → omitir el sub-bloque entero.
- Solo Delivery. Support nunca entra acá.

**Cierre y Jira (v2.7+):** el cierre NO consulta Jira automáticamente. Pedido
genérico ("si está en Sprint 0, fecha de fin; si en sprint posterior, fecha de
cierre"). El cross-check contra Jira se hace a posteriori vía la acción kebab
"Cross-check Jira" (Fase 8). Jira siempre detrás de pedido explícito.

---

## Catálogo de métricas por módulo (v2.9+)

Qué métricas pedir cuando `recent_golive = true`, según `mentioned_module`. Si
es null, usar la fila "Other / módulo no identificado".

| Módulo | Métricas a pedir (últimos 30 días post-golive) |
|---|---|
| Sales Cloud | Cuentas creadas, Oportunidades creadas y avanzadas de etapa, Contactos creados, Cotizaciones armadas, Leads convertidos. |
| Service Cloud | Casos abiertos, casos cerrados, tiempo medio de resolución, SLA cumplido %. |
| Marketing Cloud / Account Engagement (Pardot) | Envíos realizados, tasa de apertura, clicks, leads generados, journeys activos. |
| Consumer Goods Cloud | Visitas planificadas vs ejecutadas, órdenes generadas, presencia en góndola, productos auditados, KPIs de retail execution. |
| Field Service | Citas/Service Appointments completadas, work orders cerradas, tiempo promedio en campo, first-time fix rate. |
| Experience Cloud | Usuarios activos en la comunidad, posts/threads creados, casos resueltos por self-service. |
| Financial Services Cloud | Households activos, financial accounts cargadas, referrals generados. |
| Health Cloud | Pacientes registrados, care plans activos, encounters logueados. |
| Industries (otra cloud vertical) | KPIs del módulo vertical específico — pedirle al PM que defina cuáles aplican. |
| CRM Custom | "¿Qué métricas de tu desarrollo demuestran que el usuario está usándolo? (records creados, automatizaciones disparadas, transacciones procesadas, etc.)" |
| Integration | "¿Qué volumen de mensajes/transacciones procesó la integración en el último mes? ¿Hubo errores? ¿Tiempo medio de procesamiento?" |
| Data Cloud | DMOs activos, Calculated Insights ejecutados, Activations corriendo, volumen ingerido. |
| Agentforce | Sesiones del agente, conversaciones resueltas sin handoff, satisfaction score, top intents. |
| Other / módulo no identificado | "Cuéntame qué módulo entregaste y te paso las métricas a chequear." |
