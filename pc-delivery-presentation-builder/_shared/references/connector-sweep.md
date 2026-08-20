<!-- ⚠️ AUTO-COPIADO desde _shared/presentation-builder/ por sync.sh — NO EDITAR ACÁ. Editá el canónico y volvé a correr sync.sh. -->

# Connector sweep — Cómo enriquecer el contexto del cliente / proyecto

Cuando el usuario confirma que quiere enriquecimiento (paso 3 del SKILL.md), barre los conectores disponibles para sumar señales reales al prompt. La regla es: **usar todas las fuentes disponibles sin preguntar cuáles**.

> **Fuentes según área.** En **comercial** la fuente primaria es Salesforce (Account/Opp) — arranca por ahí. En **delivery** la fuente primaria es Jira/Confluence del proyecto, más el canal de Slack del proyecto. Gmail, Calendar, ReadAI y Drive aplican a ambas áreas. Cada `SKILL.md` detalla el foco de su área; abajo está el catálogo completo.

## Fuentes y qué buscar en cada una

### Jira / Confluence (fuente primaria en delivery)

- **Issues cerrados en el período** → entregables/avances concretos con evidencia para el slide "qué logramos".
- **Blockers e issues abiertos de alta prioridad** → riesgos y pedidos al cliente.
- **Hitos / epics cumplidos vs pendientes** → estado real del proyecto contra el plan.
- **Páginas de Confluence** (actas, decisiones, scope) → decisiones y cambios de alcance para "qué cambió/aprendimos".

### Salesforce (siempre intentar primero)

Es la fuente más densa y estructurada. Si el AE pasó una Opportunity Id o un Account Id, arranca por ahí. Si no, busca por Account.Name.

- **Account** — Industria, país, sitio web, descripción, fecha de alta, owner.
- **Contacts del Account** — Nombres, roles, antigüedad como contactos. Stakeholders identificados.
- **Opportunities abiertas y cerradas** — Histórico comercial. Si ya hubo proyectos, mencionarlos genera continuidad.
- **Project__c relacionados** — Proyectos vigentes o finalizados. Para Support, esto es oro: "continuamos cuidando lo que ya construimos juntos".
- **Use_Case__c y Success_Story__c del Account** — Casos de éxito documentados con este cliente o de su industria.
- **Notas en Opportunity** — Algunas oportunidades tienen notas con el dolor o la historia.

### Gmail

Buscar threads recientes con el dominio del cliente (últimos 90 días).

- Asuntos repetidos → señales de los temas que están conversando.
- Adjuntos que envió el cliente → posibles RFPs, briefs, requirements.
- Tono de los emails → indica seniority del interlocutor.

No leas contenido sensible (NDAs, números, datos personales) — solo extrae temas y señales de contexto.

### Google Calendar

Eventos pasados y futuros con asistentes del dominio del cliente (últimos 60 días + próximos 30).

- Títulos de reuniones → ¿hubo discovery? ¿demo? ¿pricing?
- Frecuencia → indica intensidad del deal.
- Asistentes internos de ProContacto → quién más estuvo, podrías sumarlos al equipo del deck.

### ReadAI (transcripts de Meet)

Si hay grabaciones/transcripts de reuniones recientes con el cliente, son la fuente más rica de personalización.

- Frases textuales del cliente sobre su dolor → úsalas (entre comillas) en "Qué problemas vemos".
- KPIs que el cliente mencionó → úsalos en el deck.
- Decisiones tomadas en reunión → respétalas en la propuesta (alcance, fechas, etc.).

### Google Drive

Busca la carpeta del cliente (creada por `pc-sales-sf-account-builder` o por convención `país/cliente`).

- Briefs, RFPs, presentaciones recibidas del cliente.
- Documentos internos sobre el deal (estimaciones, working docs).
- Si hay propuestas anteriores al mismo cliente, leerlas para no repetir cosas que ya prometimos o ya cobramos.

### Slack

Canales con el dominio del cliente o canales internos donde se discute el deal.

- Hilos recientes sobre el cliente.
- Notas de los AEs / PMs sobre el cliente.
- Si hay un canal externo con el cliente (cc-/proy-/ext- prefix), el tono general de la conversación.

## Reglas de barrido

1. **Sin picker**. No le preguntes al AE qué conectores barrer. Si está conectado, úsalo. (Regla de feedback en memoria.)
2. **Time budget**. El barrido completo no debe tomar más de 60-90 segundos. Si una fuente tarda, salteala y avisa ("Calendar tardó, no lo incluye en este pase").
3. **Resumir, no copiar**. Los hallazgos van resumidos al prompt — no copies emails enteros ni transcripts crudos. 1-3 líneas por señal.
4. **Aprobación selectiva del AE**. Después del barrido, muéstrale al AE una lista de las señales encontradas y deja que tilde cuáles sumar al prompt. Esto es importante porque puede haber datos del barrido que el AE no quiere meter al deck (por ejemplo, info confidencial o de un deal viejo que no aplica).
5. **Citar fuente**. Para cada señal incluida en el prompt, dejar entre paréntesis de dónde salió ("(transcript ReadAI 2026-05-03)" o "(email del cliente 2026-04-22)"). Esto le permite a Claude Design verificar y al AE trazarla.

## Qué NO incluir en el prompt

- Números de pricing de propuestas anteriores (el AE los pone a mano).
- Datos personales sensibles (DNIs, teléfonos).
- Información que el AE no haya autorizado explícitamente al revisar el resumen.
- Conversaciones que estén bajo NDA salvo que el AE confirme.

## Si no hay nada que barrer

Si todas las fuentes vuelven vacías, dile al AE honestamente:

> No encontré señales del cliente en los conectores. La personalización del prompt se va a basar exclusivamente en el brief que me pasaste y en las heurísticas de industria. Si tienes un transcript, un email o un brief en Drive que sepas que aplica, pásamelo y lo sumo.

No simules señales con info inventada.
