# AI Prompt Companions — Agentforce Campaign Builder, Einstein Segment, Ideal Segment

These three are **not API calls** — Agentforce Campaign Builder and Einstein Segment are both
natural-language prompt boxes inside the Salesforce UI (Marketing Cloud Growth / Data Cloud).
This skill can't script them, but it can generate the *text* to paste into them, the same way it
generates email/WhatsApp copy — grounded in the real theme brief from SKILL.md step 3 and the
real brand colors/tone from step 3.1, never invented. Hand all three to the user as plain text
blocks in the final output, alongside the Campaign/Email/WhatsApp/Flow links.

**Unlike the rest of this skill, these three are not empirically validated against a real org
run** (no confirmed example of pasting one into Agentforce Campaign Builder or Einstein Segment
exists yet) — they're copy generation, not a reverse-engineered API recipe. Say so if the user
asks whether this part has been tested.

---

## 1. Agentforce Campaign Builder prompt

Agentforce Campaign Builder takes a natural-language brief and proposes campaign structure/assets.
**Keep it short and direct — 1-2 sentences, the way someone actually types into a prompt box, not
a paragraph loaded with tone/CTA/cadence detail.** Real confirmed-style example (the user's own
phrasing, generic enough to reuse as the calibration anchor for this shape):

```
Campaña interactiva para clientes para recordarles los días festivos próximos, que tenga un
email y un WhatsApp. La idea es recordarles los días festivos por los días laborales.
```

Notice what it does and doesn't do: names the campaign type in one adjective/phrase ("interactiva"),
states the core idea in a short clause, names the channels plainly ("un email y un WhatsApp"),
and adds one short sentence for the *why*. No labeled fields, no tone/brand-voice paragraph, no
CTA text, no explicit mention of the wait/decision cadence — Agentforce Campaign Builder infers
that structure itself. Build each real prompt the same way, substituting the account and its
actual theme from SKILL.md step 3:

```
Campaña {adjetivo corto del tipo, ej. "interactiva", "de reactivación", "de bienvenida"} para
{ACCOUNT_NAME} para {la idea central del theme en una frase corta y concreta}, que tenga un email
y un WhatsApp. La idea es {el motivo o beneficio, en una frase corta}.
```

Never invent the theme or motivo — pull them straight from the real brief gathered in step 3.

---

## 2. Einstein Segment prompt (Data Cloud natural-language segmentation)

Einstein's natural-language segment box turns a plain description into filter criteria under the
hood — it does **not** require knowing real DMO/field API names (that's the difference from
`pc-crm-salesforce-demos-segmentos`, which builds a real `MarketSegment` via API and does need
exact field names). **Write it as a bare chain of attributes, not a full "quiero un segmento
de..." sentence and not a bulleted list** — Einstein's box reads a comma/`y`-joined attribute
chain directly. Real confirmed-style example (the user's own phrasing):

```
Cuentas mineras con actividad reciente, originadas en Apollo y con estado de no afiliado.
```

That's the whole prompt — four attributes (industry/type, activity recency, source, status),
chained with commas and a final "y", no framing sentence around them. **Cap it at 2-4 attributes**
— more than that stops reading like something a person would actually type and starts reading
like a spec. Build each real prompt the same shape, pulling only attributes the brief actually
supports (don't pad to 4 by inventing one):

```
{TIPO DE CUENTA/REGISTRO — segmento base, ej. "cuentas mineras", "clientes retail", "leads de
seguros"} con {ATRIBUTO — comportamiento/actividad, ej. "actividad reciente"}, originadas en
{ATRIBUTO — fuente/canal de origen, ej. "Apollo", "referidos", "sitio web"} y con estado de
{ATRIBUTO — status/etapa, ej. "no afiliado", "activo", "pendiente de aprobación"}.
```

If the user actually wants this segment **created** (not just a prompt to paste), point them to
`pc-crm-salesforce-demos-segmentos` — don't try to build the `MarketSegment` from this skill.

---

## 3. Ideal segment (prose description)

A short, human-readable paragraph describing the *perfect* member of this campaign's target
audience — for a stakeholder to read, not a tool prompt. Write it directly from the brief, 3-5
sentences: who they are, what behavior/state makes them a fit for this campaign right now, and
why the theme's message will land for them specifically. Example shape (fill from the real
brief, don't reuse this wording verbatim):

```
El segmento ideal para esta campaña son clientes de {ACCOUNT_NAME} que {estado/comportamiento
que dispara la campaña, ej. "abandonaron un carrito con al menos un producto de la categoría X
en las últimas 72 horas"}. Son personas que {contexto que las hace receptivas al mensaje, ej.
"ya mostraron intención de compra pero no completaron el proceso"}, por lo que {por qué el
theme/oferta de esta campaña específicamente las va a convencer}. Se excluyen quienes
{exclusiones razonables — ya compraron, ya fueron contactados, dieron de baja comunicaciones}.
```

---

## Where this fits in the final output

Add all three as a labeled block after the Campaign/Email/WhatsApp/Flow links in the "Final
Output Format" (SKILL.md), clearly marked as text to paste into Agentforce Campaign Builder /
Einstein Segment — not as records created in the org.
