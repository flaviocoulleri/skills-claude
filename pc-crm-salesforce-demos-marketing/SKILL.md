---
name: pc-crm-salesforce-demos-marketing
description: >
  Builds end-to-end Salesforce marketing demo journeys following the "SDO Marketing" pattern:
  a Campaign (Parent/Child/Partner-Led record type) linked to Salesforce CMS content (an Email
  built "Use components" style on the rich Archetype E template — white/light canvas, hero,
  highlight badge, stat box, items list, comparison section — and a WhatsApp Session Message)
  orchestrated by an AutoLaunchedFlow that by default sends the email, waits a day, then sends
  the WhatsApp (a plain linear chain; an engagement-branching variant with Decisions/follow-up
  Task/forward-to-agent is available opt-in, not the default). Use this skill whenever the user
  wants to build a demo/POC marketing campaign, a CMS Email or WhatsApp Session Message content
  item, or a marketing journey Flow that sends Email/WhatsApp actions triggered by a Data Cloud
  Segment. Also trigger on mentions of ManagedContentSpace, CMS workspace/content folders,
  sendEmailMessage or sendWhatsAppMessage flow actions, "Content Workspace for Marketing Cloud",
  or campaigns using the SDO_Marketing_ParentCampaign / SDO_Marketing_ChildCampaign record types.
  Also produces, as paste-ready text (not API calls), an Agentforce Campaign Builder prompt, an
  Einstein Segment natural-language prompt, and an ideal-segment description for the same
  campaign, plus a fixed final-output block (`# Data Cloud` standing links, then `# Marketing`
  with the Campaign/Email/WhatsApp/Flow/segment links). Reverse-engineered from real working
  examples in a ProContacto demo org via the Connect and Tooling REST APIs — includes exact JSON
  payloads and documented platform limitations (CMS folders can't be created via API, existing
  CMS content can't be edited via API).
license: MIT
metadata:
  author: ProContacto
  version: "1.7.3"
  domain: platform
  triggers: marketing campaign demo, CMS email, WhatsApp Session Message, ManagedContentSpace, Content Workspace for Marketing Cloud, sendEmailMessage, sendWhatsAppMessage, SDO Marketing, marketing journey flow, Segment-triggered flow, Use components email, demo marketing journey, engagement branching, createTask, forwardToBotOrAgent, Agentforce Campaign Builder, Einstein Segment, segmento ideal, ideal segment
  role: expert
  scope: implementation
  output-format: execution
  related-skills: pc-crm-salesforce-flow-builder, pc-crm-salesforce-dev-guide, pc-delivery-presentation-builder, pc-crm-salesforce-demos-segmentos
---

<!-- Changelog
1.7.3 (2026-08-19): Promotes **Quick Reply to the default** WhatsApp message type — user follow-up
right after 1.7.2 landed the variant: "guarda esa mejora de skill. ahora los whatsapp deben tener
quick reply." Every WhatsApp this skill builds now uses a tap-to-respond button by default (the
validated single-button shape from 1.7.2); the plain Text type (`Responde SÍ para...`) is demoted
to an opt-in legacy variant, only built if the user explicitly asks for it. Updates:
`references/api-recipes.md` step 4 (Quick Reply is now the primary template, Text moved to new
§4.2), SKILL.md Core Workflow step 8 and Critical Rules, `references/email-templates.md` WhatsApp
copy pattern's CTA line.
1.7.2 (2026-08-19): Adds the WhatsApp **Quick Reply** variant (`messageType: "QuickReply"`, a
tap-to-respond button instead of "type SÍ"), per the user asking "para el whatsapp puede ser que
en vez de texto sea quick reply?" Per this skill's own "never guess the schema" rule, didn't invent
the shape — found a real pre-existing example already sitting in the org (the oldest
`sfdc_cms__whatsappSession` content, created by hand before this skill existed) via
`GET /connect/cms/contents/{contentKey}`, confirmed its exact structure (`contentBlock.attributes.actions`
→ `sfdc_cms/waSessionInteractiveActions` → a `buttons` array of `sfdc_cms/waSessionInteractiveButton`
blocks, `type: "reply"`), and templated from that. Only a single-button example was found in the
org — documented as validated for exactly one button; 2-3 buttons is a reasonable but **unconfirmed**
generalization of the same shape, flagged as such. New `references/api-recipes.md` §4.1. Fixes copy that read as a neutral corporate announcement instead of marketing
copy — user feedback on the SMS Latam email/WhatsApp: "necesito que el email y el whatsapp sean
BIEN marketinero." The facts (theme, brief, brand) don't change — only how they're framed: headlines,
hero copy, item-list labels, comparison-box labels, and CTA text must all lead with a **benefit to
the reader** and read as persuasive marketing writing, not a factual bulletin ("qué es / dónde se
presentó" is a report; "su negocio ya puede crecer sin fronteras" is marketing). This applies even
to serious B2B/institutional themes — the lever is benefit-driven, confident language and stronger
CTA verbs, not emoji or retail slang, which stay governed by the existing tone-by-industry rule.
See the rewritten "Marketing voice" note in `references/email-templates.md` and the WhatsApp copy
pattern's tone line.
1.7.0 (2026-08-19): Adds a **demo persona** to ground the campaign in a concrete story, per explicit
user request ("dame un resumen y historia de la campaña... si podés inventar una historia mejor,
por ej Juan tiene una minera..."). New Core Workflow step 3.2: invent (or ask for) a fictional
recipient — first name, plausible role/company matching the Account's real target audience from
step 3.1, and a plausible reason they're in this campaign (visited the site, matches the segment
criteria, etc.). Unlike product/service claims, which must stay real (step 3.1's site crawl), the
persona's name and story are **explicitly authorized to invent** — it's demo flavor, not a fact
about the Account. Two consequences: (1) the final output gets a new `# Historia de la Campaña`
section, between `# Data Cloud` and `# Marketing`, summarizing the target segment, the campaign's
purpose, what's being promoted, and the persona's story in prose; (2) the Email and WhatsApp
greetings now use the persona's real first name **hardcoded directly** ("Hola, Juan," not a merge
tag) — this doesn't reopen the unvalidated `$unifiedIndividual.FirstName` merge-field question
from 1.5.3/1.5.4 (still don't invent that tag), it's a different mechanism: the persona is a fixed
named demo character, not a live token resolved per-recipient. Updates: SKILL.md "Final Output
Format" template, `references/email-templates.md` "Personalization" rule and the WhatsApp
greeting line (both now say to use the persona's literal name), Archetype E's greeting slot.
1.6.2 (2026-08-19): Fixes step 3.1 undershooting when the user hands over a bare website instead
of an Account link — the skill was fetching only the homepage, which is often too thin to safely
infer a theme or ground copy without guessing (a homepage rarely lists real products/services in
enough detail; the SMS Latam session needed a separate fetch of a specific news article to find a
real, groundable theme, and that was luck, not the workflow's design). Now requires crawling the
main-nav sections (Nosotros/Quiénes Somos, Productos, Servicios, Industrias, Novedades, etc.), not
just the landing page, before inferring the theme or writing copy — see the rewritten step 3.1.
Single-page sites that expose these as in-page anchors (`#servicios` etc., like SMS Latam's own
site) already get full coverage from one homepage fetch and don't need extra requests; the crawl
only kicks in for real multi-page sites, which is the common case. Brand colors (step 3.1's other
job) still come from the homepage/header, since those rarely vary by page.
1.6.1 (2026-08-19): Replaces the theme→archetype selection logic with a single **universal
default**, on the same SMS Latam session. The user pasted a real working example (Automotriz
Berrios "no-show recovery" campaign) that turned out to be Archetype A verbatim, said the
Archetype C email just built for SMS Latam "es horrible" by comparison, and confirmed via
follow-up that (1) Archetype A's structural richness — hero, highlight badge, big-number stat box,
items list, comparison section, CTA repeated — should be the default for **every** theme, not just
retail/loyalty, replacing the old theme-mapped table; then (2) corrected the canvas: "usa
background blancos, no negros" — Archetype A is always dark by design, so this isn't Archetype A
itself but a new **Archetype E**, the same structural skeleton rebuilt on a white/light canvas
colored from the Account's own real accent (never a fixed dark/orange palette). Rebuilt the SMS
Latam email on Archetype E (new CMS content `MCTM77QY7EVVA3HEBYB7TTWZXLNM`, replacing
`MCT3FRNP2ZMBGX5FFNLMMM2RTT2Y` from earlier in the same session — the old content is orphaned, not
deleted, per the existing "CMS content can't be edited" limitation) and `PATCH`ed the Flow's
`sendEmailMessage` action to the new `contentId` (new Flow Id `301aj00003NU5rVAAT`, same pattern
as `api-recipes.md` §6.4). Also confirms empirically that "highlight badge" / "big-number stat"
slots don't have to carry literal urgency/discount copy — reused for SMS Latam as an event
citation ("Presentado en ENGAGE 2026") and a date ("12 DE JUNIO") since that theme has no
expiry/discount; keep the *structural role*, let the theme's real facts fill it. See
`references/email-templates.md` "Choosing an archetype" (now points to Archetype E by default,
A–D demoted to opt-in legacy) and the new "Archetype E — Rich/Light" section.
1.6.0 (2026-08-19): Reverts the default Flow shape from **engagement-branching** (1.3.0) back to
a **plain linear chain** — `Send Email → Wait 1 Day → Send WhatsApp → end` — no Decisions, no
follow-up Task, no `forwardToBotOrAgent`, and no second Wait. Confirmed by inspecting the actual
Flow the user built on top of this skill's own scaffold on the SMS Latam campaign (same session as
1.5.6/1.5.7): `FlowRecord` `2aFaj00000PbK4bEAF`, `FlowDefinitionId` `300aj00003Iqy2c`, org
`flavio.coulleri@demos2026.com.mx`, fetched via `SELECT ... FROM Flow WHERE DefinitionId = '...'`
→ Tooling API `GET` on the current version (`301aj00003NTnplAAD`) — `Metadata.decisions: []`,
`Metadata.waits` has exactly one entry, `Metadata.actionCalls` has exactly two (`sendEmailMessage`,
`sendWhatsAppMessage`), the WhatsApp action's `connector` is unset (nothing after it). User
instruction: "de ahora en adelante los flow deben tener esa misma estructura" — this is now the
default for every future run, not a one-off. The engagement-branching shape from 1.3.0 is **not
deleted** — kept as a documented optional variant (see "Default Flow shape" below) in case a
future demo specifically asks for branching/Task/forward-to-agent, but it is no longer what this
skill builds unprompted. Updates: SKILL.md "Default Flow shape", Core Workflow step 9 (dropped the
now-unneeded `Campaign.OwnerId` query — nothing consumes it in the linear default), "What's Left
to Activate" (dropped items that only applied to Decisions), `references/api-recipes.md` step 6
(new trimmed `flow_body.json` template), `references/data-model.md` §4.1 (documents both shapes,
linear as current default).
1.5.7 (2026-08-19): Prepends a `# Data Cloud` section, with three links, before the `# Marketing`
block from 1.5.6 — confirmed immediately after, same SMS Latam session. One of the three
(`## Data stream`, the `DataStream` list view) is a generic non-record URL, same for every run in
a given org. The other two (`## Data model`, a `DataLakeObjectInstance` record; `## Identity
resolution`, an `IdentityResolution` record) are **not derivable by query** — checked directly in
the `flavio.coulleri@demos2026.com.mx` org and found genuinely ambiguous: dozens of
`DataLakeObjectInstance` rows exist (one per source object synced into Data Cloud) and two
`IdentityResolution` rulesets exist (`Individual Identity Resolution`, the platform default, and
`Account IdRes Demo`, the one actually referenced). Picking either "the first one" or "the most
recent one" would silently show the wrong object on a re-run or a different org — this skill does
not build Data Cloud objects at all (that's `pc-crm-salesforce-demos-segmentos`'s territory), so
it has no basis to prefer one over another. Treated instead as an **org-level standing constant**:
ask the user once per org which DLO/IdentityResolution these should point to (or reuse if already
known from a prior run against that same org), never guess. The confirmed values for
`pr1782405263810` are documented in "Final Output Format" as the worked reference, the same role
`sdo-alfa` plays for the rest of this skill — not assumed portable to a different org.
1.5.6 (2026-08-19): Rewrites "Final Output Format" again per a new explicit user template, on the
SMS Latam campaign (org `flavio.coulleri@demos2026.com.mx`). Differences from 1.5.4's shape: (1)
the whole block now opens with a single `# Marketing` H1; (2) the Agentforce Campaign Builder
section is now headed `## prompt campaing builder` (verbatim, including the user's own spelling)
and leads with a link to the org's Home page (`/lightning/page/home`) before the prompt text —
there's no deep link into Agentforce Campaign Builder itself, so Home is the standing placeholder;
(3) Email/WhatsApp headers dropped their `Email:`/`WhatsApp:` prefix — just the content title now;
(4) the Flow link changed from the Flow Builder canvas URL (`/builder_flow/flowBuilder.app?flowId=`)
to the `FlowRecord` record view (`/lightning/r/FlowRecord/{flowRecordId}/view`) — the same Id
already resolved in step 10 for the Campaign↔Flow link, so no extra query is needed; (5) the
Einstein Segment section is now headed `## prompt segmento → data space:default y en el otro
account` (verbatim reminder text, not to be reinterpreted or expanded — carry it as-is) and adds a
link to the `MarketSegment` object home (`/lightning/o/MarketSegment/home`) after the prompt, for
jumping straight to where the user builds it; (6) a new empty `## Segmento` section is inserted
before the ideal-segment prose — reserved for the real `MarketSegment` record link once one is
built (e.g. via `pc-crm-salesforce-demos-segmentos`), deliberately blank when this skill runs
standalone; `Segmento ideal:` moves from being its own `##` header to a plain-text line inside
that same `## Segmento` section; (7) a new closing `## Analytics → Marketing Executive Dashboard`
section links to the generic Analytics home (`/lightning/page/analytics`) — there's no known way
to deep-link a specific dashboard without its Id, so this points at the Analytics tab itself. Also
extends the URL formulas table with these three new non-record links (Home, MarketSegment object
home, Analytics home) — none need an Id, so unlike the other four they're the same for every run
against a given org.
1.5.5 (2026-08-12): Fixes a real misunderstanding from 1.4.0, caught by the user mid-build on the
Petenatti Hogar campaign ("el background de fondo, atrás del mail, ya sería background de SF —
dejalo blanco"). The CMS content JSON's top-level `contentBody.backgroundColor` is the Email
Builder's own "Fondo de email" canvas behind the email card in Salesforce's UI — it is NOT part
of the email's own design and has nothing to do with whatever background color the `rawHtml`
itself uses. 1.4.0 wrongly conflated the two and required them to match; this field now defaults
to `#ffffff` regardless of the archetype (a dark Archetype A email keeps its own `#0a0a0a` hero
canvas inside `rawHtml`, untouched). See SKILL.md step 8, `references/email-templates.md`
"Filling these in", `references/api-recipes.md` step 3's template. Also documents a new finding
made while fixing this on a live campaign: unlike CMS content (read-only after creation), an
already-created `Flow` draft CAN be updated via a Tooling API `PATCH` with the full `Metadata`
resent — confirmed working to swap a `sendEmailMessage` action's `contentId` after the fact
without needing to rebuild the Campaign/FlowRecord link. The platform issues a new Flow Id on
each such PATCH (same `VersionNumber`, new row Id) — the `FlowRecord` link survives since it's
keyed by `ApiName`, not the row Id, but the Flow Builder link needs re-deriving. New
`references/api-recipes.md` §6.4.
1.5.4 (2026-08-12): Rewrites "Final Output Format" per explicit user preference — the closing
summary must render as real markdown `##` headers directly in the chat reply, never inside a
triple-backtick code fence (that flattened the headers into literal text and showed a gray box
instead of actual section headers). Also reorders the block: Agentforce Campaign Builder prompt
now goes first, then Campaign → Email → WhatsApp → Flow, then the Einstein Segment prompt, then
the ideal segment description last — previously the three AI Prompt Companions were appended
after all four org records as a separate fenced block.
1.5.3 (2026-08-12): Fixes a real build-time hang, not a doc gap — building `email_body.json` via
PowerShell's `ConvertTo-Json -Depth 20` over the nested ordered-hashtable component tree (step 8)
hung for minutes with climbing CPU and no output, on a payload with nothing unusual (a single
~5KB `rawHtml` string, the same component tree shape used since 1.0.0). Killed and rebuilt via
plain here-string templating with a small JSON-escape helper (`\`, `"`, newlines) substituted
into a pre-written JSON skeleton — ran instantly, byte-identical structure. `ConvertTo-Json` on
deeply nested objects containing one large string is the trigger; ordinary-sized bodies (the WhatsApp
content, the Flow body) were never affected. The "write large JSON bodies to a scratch file" rule
in Critical Rules and step 3 of `references/api-recipes.md` now say to build the file this way,
not via `ConvertTo-Json`, whenever the body embeds `rawHtml` or another multi-KB string. Also
confirms (found while writing personalization copy for a real B2B account) that there is no
validated merge-field syntax for injecting `$unifiedIndividual` fields (e.g. a first name) into
`rawHtml` — despite the contentBody using `{!$brand.*}` merge syntax elsewhere in the same payload,
guessing an analogous `{!$unifiedIndividual.FirstName}` would be inventing untested schema per the
skill's own "never guess" rule. Default to a name-independent greeting ("Hola,") until a real
working example is found; don't invent the merge tag.
1.5.2 (2026-08-12): Recalibrates both prompt shapes in `references/ai-prompt-companions.md`
against real confirmed-style examples the user provided — they were still too long/structured
(a full paragraph with tone/CTA/cadence for Agentforce, a full sentence with "quiero un segmento
de..." framing for Einstein). Agentforce Campaign Builder prompts are now 1-2 short sentences
(type + core idea + channels + one-line why), matching the confirmed example "Campaña interactiva
para clientes para recordarles los días festivos próximos, que tenga un email y un WhatsApp...".
Einstein Segment prompts are now a bare comma/"y"-joined attribute chain capped at 2-4 attributes,
no framing sentence, matching the confirmed example "Cuentas mineras con actividad reciente,
originadas en Apollo y con estado de no afiliado."
1.5.1 (2026-08-12): The Agentforce Campaign Builder and Einstein Segment prompts in
`references/ai-prompt-companions.md` were written as labeled-field templates ("Audiencia
objetivo:", a bulleted criteria list) — not actually natural language, which is the whole point
of those two prompt boxes. Rewrote both as flowing paragraphs a person would type, with an
explicit instruction not to fall back into field-by-field structure.
1.5.0 (2026-08-12): Adds a third deliverable alongside the org records: `references/ai-prompt-companions.md`,
with templates for an Agentforce Campaign Builder prompt, an Einstein Segment natural-language
prompt, and an "ideal segment" prose description — all grounded in the same theme brief and brand
colors already gathered in steps 3/3.1/4, never a second freeform brief. Both Agentforce Campaign
Builder and Einstein Segment are UI prompt boxes, not APIs, so this skill generates their input
text rather than scripting them — explicitly flagged as copy generation, not an empirically
validated recipe like the rest of the skill. The Einstein Segment prompt is deliberately separate
from `pc-crm-salesforce-demos-segmentos` (which builds a real `MarketSegment` via API and needs
exact field names) — if the user wants the segment actually created, point them there instead.
New Core Workflow step 12, extended Final Output Format.
1.4.0 (2026-08-12): Four improvements from a skill self-review. (1) Fixes a real color-mismatch
bug: the CMS content JSON's top-level `contentBody.backgroundColor` was hardcoded to `#f3f3f3`
regardless of the chosen email archetype or the Account's actual brand — visibly wrong for e.g.
Archetype A's dark `#0a0a0a` canvas, and unrelated to the client's real site colors. Adds a
required step 3.1 to fetch the Account's real website before writing the email and derive its
actual brand colors (page background, header/nav background, accent/CTA color) from the page
itself, replacing the old "pull colors if known, otherwise guess" footnote in
`email-templates.md` with a required action; `backgroundColor` must now equal the same
page/canvas color used inside `rawHtml`. (2) Adds `pc-crm-salesforce-demos-segmentos` to
related-skills and to "What's Left to Activate" #2 — that companion skill already advertises
itself as complementary to this one for building the Data Cloud Segment, but this skill never
linked back; the Segment-attachment step can now be offered as a build, not left purely manual.
(3) The "dormant lead" `exitIndividualsFromFlow` branch is no longer documented as impossible to
script — the chicken-and-egg blocker (needing the Flow's own Id) is resolved right after step 6
creates the Flow, so it's now an offered, explicitly-unvalidated follow-up
(`references/api-recipes.md` step 6.6) gated on finding a real `IndividualId` value rather than
reusing the broken placeholder from the one example on file. (4) Adds a duplicate-Campaign check
before step 1's create, so re-running the skill for the same account/theme doesn't silently
clutter the org. See SKILL.md steps 1, 3.1, 6, 8, and "What's Left to Activate" #2/#6;
`references/api-recipes.md` steps 1, 3, 6.6; `references/data-model.md` §4.1;
`references/email-templates.md` "Filling these in".
1.3.0 (2026-08-05): Replaces the linear `Send Email → Wait 1 Day → Send WhatsApp → Wait 1 Day`
Flow with an **engagement-branching** default, reverse-engineered from a real Flow the user
hand-built in Flow Builder on top of this skill's scaffold (Campaign "LEBEN - Bienvenida Nuevo
Lead", org `matias.lopez@demos2026.com.mx`): after each wait, a Decision checks whether the
recipient interacted; "yes" creates a follow-up Task (assigned to the Campaign's `OwnerId`,
confirmed to match the real build) after the email branch, or forwards the conversation to an
agent (`forwardToBotOrAgent`, channel `WhatsApp`) after the WhatsApp branch. The user's own build
also had two placeholder/unfinished pieces — Decision conditions that compared an action to
itself (always `true`) and a "dormant lead" step (`exitIndividualsFromFlow`) pointing at an
unrelated, unconfigured Flow from another campaign — confirmed with the user to be WIP, not
intentional logic; the new default keeps the always-true placeholder condition (validated to be
accepted by the API) so the scaffold stays wireable in Flow Builder, but drops the
`exitIndividualsFromFlow` step entirely (documented instead as a manual-only addition, since it
would need this same Flow's own Id, which doesn't exist yet at creation time). See
`references/data-model.md` §4 and `references/api-recipes.md` step 6.
1.2.1 (2026-07-29): Agrega una sección "Typography system" en `email-templates.md` — dos font stacks seguros (moderno/casual vs. corporativo), regla sobre cuándo usar acento serif, y una escala tipográfica (tamaño/peso/letter-spacing por rol: eyebrow, headline, body, big number, botón, fine print) para que los cuatro arquetipos mantengan jerarquía visual consistente.
1.2.0 (2026-07-29): Corrige un bug real de renderizado en `email-templates.md` — los arquetipos C y D solo declaraban `font-family` en `<body>`, que el bloque `rawHtml` de CMS pierde al no preservar el wrapper `<html>/<body>`, cayendo al serif por default (reportado como "se ve como Times New Roman" en el email de Meximares). Ahora los cuatro arquetipos repiten `font-family` en cada `p`/`span`/`td`/`a`, como ya hacían A y B.
1.1.1 (2026-07-29): Documenta que el contenido CMS existente no se puede editar vía API (PATCH/PUT/POST al recurso `/connect/cms/contents/{id}` devuelven `METHOD_NOT_ALLOWED`) — solo la creación (POST) funciona. Descubierto al intentar aplicar los nuevos arquetipos de email-templates.md a un contenido ya creado (campaña "Naviera Meximares - Recordatorio de Pago 30 Dias" en la org sdo-sales); el fix quedó como texto listo para pegar a mano en la UI.
1.1.0 (2026-07-29): Agrega `references/email-templates.md` — cuatro arquetipos de email HTML (tabla, inline CSS, header/hero/oferta/CTA/footer) genericizados a partir de ejemplos reales del usuario, más el patrón de copy de WhatsApp. Antes el email se generaba como un único párrafo de HTML plano dentro del bloque `lightning/html`; ahora se exige usar uno de los arquetipos.
1.0.0 (2026-07-27): Primera versión. Basada en la exploración e implementación real en la org sdo-alfa (flavio.coulleri.sdo.alfa@procontacto.com.mx), reconstruyendo el patrón a partir de la campaña "Farmacias de Santiago - Producto Geniol" ya existente en la org.
-->

# Salesforce Marketing Demo Builder (SDO Marketing pattern)

Builds demo/POC marketing journeys inside Salesforce: **Campaign → CMS content (Email + WhatsApp Session Message) → orchestrating Flow**. This is for building sales-demo artifacts in an org (e.g. showing a prospect a marketing journey), not for production marketing configuration.

## Core Workflow

This skill always builds the **full chain in one go**: Campaign → CMS folder reminder → Email + WhatsApp content → orchestrating Flow → a final summary with clickable links. Don't stop halfway and wait for separate go-aheads at each record — gather the two inputs below up front, confirm once, then execute straight through.

1. **Confirm the target org** — ask for the org alias/username if not already connected (`sf org list` to check).
1.1. **Resolve the Data Cloud standing links** — the closing output opens with a `# Data Cloud` section pointing at a `DataLakeObjectInstance` ("Data model") and an `IdentityResolution` ruleset ("Identity resolution"). These are **org-level constants this skill cannot derive by query** — a real org typically has dozens of `DataLakeObjectInstance` rows and can have more than one `IdentityResolution` ruleset, so there's no deterministic "the" one to pick. If this org's values are already known (e.g. from a prior run in this session, or documented in "Final Output Format" below for `pr1782405263810`), reuse them. Otherwise ask the user which DLO/IdentityResolution to link, or run `SELECT Id, Name FROM DataLakeObjectInstance` / `SELECT Id, Name FROM IdentityResolution` and have them pick from the list — never guess by picking the first or most-recent row.
2. **Ask for the Account name** the demo is for (e.g. "Farmacias de Santiago", "Dermedica"). This drives the Campaign title and the CMS folder name.
3. **Ask for the campaign context/theme** — what kind of campaign is this a demo of? Give examples to prompt the user, don't leave it open-ended with no guidance: *cumpleaños/aniversario del cliente, carrito abandonado, promoción de una fecha importante (Navidad, Black Friday, Día de la Madre...), lanzamiento de producto, seguimiento post-evento/feria, reactivación de clientes inactivos (win-back)*, or anything else they describe freeform. This is the brief — **never invent marketing copy or product claims without it.** Use the theme to drive tone and structure (e.g. cumpleaños → warm/personal + a birthday perk; carrito abandonado → urgency + a direct link back to the cart; win-back → "te extrañamos" + an expiring incentive, matching the pattern of real examples in this org).
3.1. **Ask for (or infer) the Account's real website URL and crawl it — not just the homepage** — this is required, not optional, before writing the email or inferring a theme. Fetch the homepage first, then find its main navigation links (Nosotros/Quiénes Somos, Productos, Servicios, Industrias, Novedades, etc. — whatever the site's own menu actually has) and fetch each of those top-level sections too before drawing conclusions. A homepage alone is usually too thin to safely infer a theme or ground copy without guessing — real products, services, or recent news worth building a campaign around are typically one click deeper, not on the landing page. (If the site is a single-page layout that exposes these as in-page anchors on the homepage itself — `#servicios`, `#nosotros`, etc. — one homepage fetch already covers them; the extra fetches are for genuinely separate pages, which is the common case.) Skip sections that are clearly irrelevant to a marketing campaign (legal/terms, careers) unless the user's theme specifically calls for them. From this fuller picture:
    - Derive the Account's actual brand colors (page/canvas background, header/nav background, primary accent/CTA color) from what's actually on the page (look for a `theme-color` meta tag, CSS custom properties, the header/nav background, the primary button color) — these still typically come from the homepage/header markup, since colors rarely vary by section. These real hex values are what fill every `{{COLOR_*}}` placeholder in the chosen archetype (`references/email-templates.md`) — **the email's background must match the site's real colors, not a generic palette guess.**
    - When the user asks you to *infer* the campaign theme yourself (rather than stating one outright), ground it in something real found across these pages — a specific product, service, industry vertical, or recent news item — not a generic guess from the homepage's tagline alone.
    If the site is unreachable or the user has no URL, fall back to an industry-appropriate palette per the archetype's own guidance and say explicitly that you did so (don't silently substitute).
3.2. **Invent (or ask for) a demo persona to anchor the story** — a fictional recipient: a first name, a plausible role/company matching the Account's real target audience (from step 3.1's crawl), and a plausible reason they're in this campaign right now (e.g. visited the site, browsed a specific section, matches the segment's criteria). Unlike product/service claims — which must stay real, grounded in step 3.1 — **the persona's name and story are explicitly authorized to invent**; it's demo flavor, not a fact about the Account. Use the persona's real first name **hardcoded directly** in the Email and WhatsApp greetings ("Hola, Juan," not a generic fallback and not a merge tag — see `references/email-templates.md` "Personalization" for why this differs from the unvalidated `$unifiedIndividual.FirstName` merge field). Summarize the persona's story, the target segment, and the campaign's purpose/what's being promoted in the final output's `# Historia de la Campaña` section (see "Final Output Format" below).
4. **Build the Campaign title**: `{Account Name} - {short Campaign Name derived from the theme}` (e.g. "Farmacias de Santiago - Producto Geniol", "Melt Pizzas - Carrito Abandonado"). Dash is the default separator; a pipe (`|`) is an accepted alternate if the user prefers it for a given run — don't mix the two within the same campaign's own artifacts.
5. **Confirm the Campaign Record Type** — default to **Child Campaign** (`SDO_Marketing_ChildCampaign`, standalone, `ParentId = null`) unless the user explicitly wants a Parent Campaign hierarchy or a Partner-Led Campaign (see `references/data-model.md` — only the standalone Child Campaign path has been validated end-to-end).
6. **Check for an existing Campaign with the same Name first** (`SELECT Id, Name FROM Campaign WHERE Name = '<CAMPAIGN_TITLE>'`) — cheap, avoids silently cluttering the org with duplicate demo scaffolds when this skill gets re-run for the same account/theme (e.g. the user re-invokes it after a partial failure, or forgets a prior run exists). If found, tell the user and ask whether to reuse it (skip straight to CMS content + Flow, reusing its Id) or create a new one anyway with a disambiguating suffix — don't silently create a duplicate. Then **create the Campaign** record.
7. **CMS folder (manual step — cannot be automated)** — tell the user to create a folder named after the **Account** inside the CMS workspace ("Content Workspace for Marketing Cloud") from the Lightning UI. See "Known Limitation" below. If they skip it, create content at the workspace root and offer to move it later.
8. **Create the CMS content**: one **Email** item (`sfdc_cms__email`, built "Use components" style) and one **WhatsApp Session Message** item (`sfdc_cms__whatsappSession`, built as **Quick Reply** with a tap-to-respond button by default — see `references/api-recipes.md` §4 — plain Text only if the user explicitly asks) via the Connect REST API, with copy written for the theme from step 3, greeting the step 3.2 persona by their real first name in both (e.g. "Hola, Juan," — hardcoded literal text, not a merge tag). Build the Email's `rawHtml` from **Archetype E** (the default) in `references/email-templates.md` unless the user explicitly names a different archetype (A–D, kept as opt-in legacy variants) — never a plain paragraph of unstyled HTML, and fill its `{{COLOR_*}}` placeholders with the real website colors from step 3.1. Build the WhatsApp body following that same file's copy pattern. **The CMS content JSON's top-level `contentBody.backgroundColor` field is the Email Builder's own "Fondo de email" canvas behind the email card — Salesforce UI chrome, unrelated to the email's own design.** Default it to `#ffffff` regardless of the archetype's own inner canvas color (Archetype A's dark `#0a0a0a` hero stays inside the `rawHtml` untouched) — only change it from white if the user explicitly asks. (Corrected 2026-08-12 — see the 1.5.5 changelog entry; the 1.4.0-era guidance that this field had to match the `rawHtml` canvas was wrong.) Capture each `contentKey` **and** `managedContentId` from the response — the second one is what the final link uses.
9. **Create the orchestrating Flow** via the Tooling REST API, named after the Campaign, referencing both content items by their `contentId`. Default shape is a **plain linear chain** — `Send Email → Wait 1 Day → Send WhatsApp → end` — see "Default Flow shape" below and the full template in `references/api-recipes.md` step 6. (Prior to 1.6.0 the default was engagement-branching with Decisions/Task/forward-to-agent; that shape is still available as an opt-in variant if the user specifically asks for branching, but it's no longer built unprompted, and its `Campaign.OwnerId` lookup for the follow-up Task isn't needed for the linear default.)
10. **Link the Flow to the Campaign natively** — query the `FlowRecord` that the platform auto-created for the Flow (`SELECT Id FROM FlowRecord WHERE ApiName = '{the FullName used in step 9}'`), then `PATCH` its `AssociatedRecordId` to the Campaign Id via the **standard** REST API (not Tooling). This is what makes the Flow actually appear in the Campaign's "Flows" related list — don't skip it, it's the real fix for "the flow lives inside the campaign," not just a naming convention. See "FlowRecord: the real Campaign↔Flow link" below.
11. **Output the final summary with links** — see "Final Output Format" below. Always include this; it's the deliverable the user actually wants to click through.
12. **Generate the three AI Prompt Companions** — an Agentforce Campaign Builder prompt, an Einstein Segment natural-language prompt, and an "ideal segment" prose description, all grounded in the same brief/brand from steps 3–4 — see `references/ai-prompt-companions.md`. Include them in the final output as text blocks, clearly labeled as prompts to paste into those tools, not as org records this skill created.
13. Be explicit about what's still manual before this journey could actually run (see "What's Left to Activate" below) — this skill produces a realistic **scaffold**, not an activated journey.

Full API payloads and step-by-step commands: `references/api-recipes.md`.
Data model facts (record types, object prefixes, ID formats): `references/data-model.md`.
Email HTML archetypes and WhatsApp copy pattern: `references/email-templates.md`.
Agentforce Campaign Builder / Einstein Segment prompts and ideal segment description: `references/ai-prompt-companions.md`.

---

## Final Output Format

Always close by giving the user direct, clickable links to everything created — this is the actual deliverable, not optional. Get the instance's Lightning domain from `sf org display` (`Instance Url` field: swap `.my.salesforce.com` for `.lightning.force.com`, e.g. `https://pr1774493035899.my.salesforce.com` → `https://pr1774493035899.lightning.force.com`). URL formulas (all confirmed working, see `references/api-recipes.md` for the derivation of each Id):

| Link | URL | Needs an Id? |
|---|---|---|
| Data Stream list | `https://{domain}/lightning/o/DataStream/list?filterName=__Recent` | No — same for every run |
| Data model (`DataLakeObjectInstance`) | `https://{domain}/lightning/r/DataLakeObjectInstance/{dloInstanceId}/view` | Yes, but **not derivable by query** — org-level constant, see step 1.1 |
| Identity resolution (`IdentityResolution`) | `https://{domain}/lightning/r/IdentityResolution/{identityResolutionId}/view` | Yes, but **not derivable by query** — org-level constant, see step 1.1 |
| Home (for the Campaign Builder prompt) | `https://{domain}/lightning/page/home` | No — same for every run |
| Campaign | `https://{domain}/lightning/r/Campaign/{campaignId}/view` | Yes |
| Email | `https://{domain}/lightning/r/ManagedContent/{managedContentId}/view` | Yes |
| WhatsApp | `https://{domain}/lightning/r/ManagedContent/{managedContentId}/view` | Yes |
| Flow | `https://{domain}/lightning/r/FlowRecord/{flowRecordId}/view` | Yes — the same `FlowRecord` Id already resolved in step 10 |
| MarketSegment object home (for the Einstein Segment prompt) | `https://{domain}/lightning/o/MarketSegment/home` | No — same for every run |
| Analytics home (for the closing dashboard link) | `https://{domain}/lightning/page/analytics` | No — same for every run; there's no known way to deep-link a specific dashboard without its Id |

**Confirmed values for `pr1782405263810`** (org `flavio.coulleri@demos2026.com.mx`, worked reference from the SMS Latam session, 2026-08-19): Data model → the `Account_Home` DLO instance, `1dlaj000007zhTtAAI`; Identity resolution → the `Account IdRes Demo` ruleset, `1iraj000000Tq0AAAS` (not the platform-default `Individual Identity Resolution` ruleset, which also exists in that org). Treat these as specific to that org, not a portable default — reconfirm per step 1.1 in any other org.

Render the whole thing as **real markdown headers (`##`) directly in the chat reply — never inside a triple-backtick code fence.** A code fence flattens the `##` into literal text and renders as a gray box instead of actual headers; this final summary must render as real headers with the link as plain text on its own line underneath, no emojis unless the user has asked for them.

**Fixed template** (confirmed with the user 2026-08-19 on the SMS Latam campaign — supersedes the 2026-08-12 ordering, which is now only a historical note in the 1.5.6 changelog entry):

```
# Data Cloud
## Data stream 
{data stream list url}

## Data model
{data model / DataLakeObjectInstance url}

## Identity resolution
{identity resolution url}

# Historia de la Campaña
{2-4 sentence prose: the target segment, the campaign's purpose, what's being promoted, and the invented persona's story — e.g. "Juan Herrera dirige una empresa minera en Perú. Mientras buscaba información sobre auditoría transfronteriza, visitó smslatam.com y navegó la sección de Servicios. Por eso le enviamos este email presentando el SMS Delivery Center, la nueva iniciativa de la red para acompañar operaciones internacionales como la suya."}

# Marketing
## prompt campaing builder 
{home url}
{Agentforce Campaign Builder prompt text}

## Campaña de marketing: {Campaign title}
{campaign url}

## {Email title}
{email url}

## {WhatsApp title}
{whatsapp url}

## Flow: {Flow label}
{FlowRecord view url}

## prompt segmento → data space:default y en el otro account
{Einstein Segment prompt text}
{MarketSegment object home url}

## Segmento



Segmento ideal:

{prose description}

## Analytics → Marketing Executive Dashboard
{analytics url}
```

(The block above is shown fenced here purely so the template is readable in this doc — the actual chat output must NOT be fenced, per the rule above.) Notes on this exact shape:

- The block opens with `# Data Cloud` (three standing links — see step 1.1 for how the two record-specific ones are resolved), then `# Historia de la Campaña` (the persona/segment/purpose summary from step 3.2 — no link, just prose), then `# Marketing` — all three are top-level H1s, everything else under each is `##`.
- The header text `## prompt campaing builder` and `## prompt segmento → data space:default y en el otro account` are **verbatim** — reproduce them exactly as given, typo included, don't "fix" or rephrase them.
- `## {Email title}` / `## {WhatsApp title}` have no `Email:`/`WhatsApp:` prefix — just the CMS content's own title (e.g. `## Email - SMS Latam`).
- The empty `## Segmento` section (two blank lines, no content) is a deliberate placeholder for the real `MarketSegment` record link once one is built (e.g. via `pc-crm-salesforce-demos-segmentos`) — leave it blank when this skill runs standalone, don't fill it with anything invented. `Segmento ideal:` is a plain-text line inside that same section, not its own `##` header.
- The Agentforce/Einstein prompts and the ideal segment description still come from `references/ai-prompt-companions.md` — they're text to paste into Salesforce UI tools, not records this skill created.

---

## FlowRecord: the real Campaign↔Flow link

There **is** a native relationship object — `FlowRecord` (key prefix `2aF`) — that's what actually powers the "Flows" related list on the Campaign record page. It has an `AssociatedRecordId` field pointing at the Campaign. The naming-convention trick (`flow_{CampaignId}_{epoch}`) documented elsewhere in this skill is real and useful for humans reading Setup, but it is **not** what the UI related list reads — that reads `FlowRecord.AssociatedRecordId`.

Key discovery (confirmed empirically in this session, 2026-07-27):

- **You cannot directly `INSERT` a `FlowRecord`** — neither standard REST nor Tooling API. Standard REST returns a hard platform error: `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY: "entity type cannot be inserted: Flow"`. Tooling API returns `NOT_FOUND` (not registered there at all).
- **The platform auto-creates a `FlowRecord` for you** the moment you create a `Flow` via the Tooling API (step 9) — you don't have to do anything to trigger it, it just exists afterward. `AssociatedRecordId` starts out **unset** on this auto-created row.
- **You CAN `PATCH` (update) that auto-created `FlowRecord`** via the **standard** REST API (`/services/data/{v}/sobjects/FlowRecord/{id}`) — this is the only supported write path, and it's how you set `AssociatedRecordId` to the Campaign.
- Find the auto-created row with: `SELECT Id FROM FlowRecord WHERE ApiName = '{FullName used when creating the Flow}'` — `ApiName` on `FlowRecord` mirrors the Flow's `FullName`/developer name, so this lookup is deterministic, no guessing/listing required.
- `AssociatedRecordId` does **not** exist as a field on `Flow` or `FlowDefinition` themselves (tested directly — `INVALID_FIELD` on both) — don't waste time trying to set it there.

**Multi-Business-Unit orgs**: the `PATCH` can fail with `MISMATCHING_TYPES` — `"Campaign is associated with a Business Unit whose Data Space doesn't match with the Data Space set on the Flow"` — if the Campaign's `BusinessUnitId` is `null` or points to a different Data Space than the Flow's (`0vh...`, apiName `"default"` in the Flow's `Metadata.dataSpace`). Fix: query an existing linked `FlowRecord` in the org (`SELECT BusinessUnitId FROM Campaign WHERE Id IN (SELECT AssociatedRecordId FROM FlowRecord WHERE AssociatedRecordId != null)`, or simpler, `SELECT BusinessUnitId FROM Campaign` on any other real campaign) to find the working `BusinessUnitId`, then `UPDATE` your new Campaign with it before retrying the `PATCH`. Orgs with only one Data Space (like the original `sdo-alfa` reference org) never hit this — it only showed up on a second org with multiple Business Units.

Full commands in `references/api-recipes.md` step 6.5.

---

## Default Flow shape: plain linear chain

**As of 1.6.0, the default is a plain linear chain — no Decisions, no follow-up Task, no forward-to-agent:**

```
Start (Segment trigger)
 → Send Email
 → Wait 1 Day
 → Send WhatsApp
 → end
```

Confirmed by inspecting a real Flow the user hand-built on top of this skill's own engagement-branching scaffold (Campaign "SMS Latam - Lanzamiento SMS Delivery Center", org `flavio.coulleri@demos2026.com.mx`, 2026-08-19 — see the 1.6.0 changelog entry): they stripped the Decisions, follow-up Task, and forward-to-agent entirely, and confirmed this simpler shape should be the default "de ahora en adelante." Build exactly this — two `actionCalls` (`sendEmailMessage`, `sendWhatsAppMessage`), one `wait`, `decisions: []` — via the trimmed `flow_body.json` template in `references/api-recipes.md` step 6. No `Campaign.OwnerId` lookup is needed for this default (nothing consumes it).

### Optional variant: engagement branching

The **previous** default (1.3.0–1.5.x) is still available if a user specifically asks for branching/Task/forward-to-agent — it is not deleted, just no longer built unprompted:

```
Start (Segment trigger)
 → Send Email
 → Wait 1 Day
 → Decision "¿Tuvo interacción?"
     ├─ Sí → Create Task (follow-up call, assigned to the Campaign's OwnerId)
     └─ No (default) → Send WhatsApp
 → Wait 1 Day
 → Decision "¿Respondió?"
     ├─ Sí → Forward conversation to an agent (forwardToBotOrAgent, channel WhatsApp)
     └─ No (default) → end
```

This was originally reverse-engineered from a real Flow the user hand-built on top of an earlier version of this skill's linear scaffold (see the 1.3.0 changelog entry). Two things carried over from that build on purpose, and are **intentional placeholders**, not bugs, if this variant is used:

- **Both Decision "Sí" rules use an always-true placeholder condition** — they compare the preceding send action to itself (`leftValueReference` and `rightValue.elementReference` both set to the same action's `name`, `operator: EqualTo`). This is accepted by the API and keeps the branch structurally wired, but it does not actually check engagement yet. Tell the user this needs to be replaced in Flow Builder with a real condition once they know which field indicates the recipient opened/clicked/replied — don't invent that field.
- **The follow-up Task's `taskAssignedToId` is set to the Campaign's `OwnerId`**, queried at build time — confirmed to match what the user assigned by hand in the real build, so this one *is* real, working logic, not a placeholder. This lookup is only needed if the user asks for this variant.

One piece from that user's original build was **dropped, not carried over**: a third branch that called `exitIndividualsFromFlow` pointing at an unrelated, unconfigured Flow from a different campaign (its `IndividualId` was the literal string `"PLACEHOLDER"` and `FlowVersionId` was `null`) — confirmed with the user to be an unfinished exploration, not a pattern to template. A "dormant lead" exit action is a reasonable thing to want, and the **current Flow's own Id** is no longer the blocker it once was — it exists right after step 6 creates the Flow, so this can now be *offered* as an experimental follow-up (see `references/api-recipes.md` step 6.6) if this branching variant is in use. What still keeps it optional-and-manual is that the one real example on file used a broken placeholder `IndividualId`, so the real value needs the user or a genuinely working example — never invent it.

Full JSON templates (both shapes): `references/api-recipes.md` step 6. Element-level facts: `references/data-model.md` §4.

---

## Known Limitation: CMS folders can't be created via API

Confirmed through direct testing (every plausible endpoint tried): `POST /connect/cms/folders`, `POST /connect/cms/spaces/{id}/folders`, and `POST /connect/cms/folders/{id}/folders` all return `NOT_FOUND` (unregistered). The generic Chatter Files resource (`POST /connect/folders/{id}/items`) rejects CMS folder IDs with `INVALID_ID_FIELD` — it's a different object entirely. `GET` on folders works fine (`/connect/cms/spaces/{id}`, `/connect/cms/folders/{folderId}`); creation does not exist in the public REST surface.

**Consequence for this skill**: never attempt to create a CMS folder via API or guess an internal Aura endpoint. Ask the user to create it by hand (2 clicks in the CMS app: open the workspace → New Folder), or default new content to the workspace root (`contentSpaceOrFolderId` = the space Id) and let the user drag it into the folder afterward.

---

## Known Limitation: existing CMS content can't be edited via API either

Confirmed 2026-07-29: `POST /connect/cms/contents` (step 8, creation) works, but there is **no
write path for a CMS content item that already exists**. `PATCH`, `PUT`, and `POST` against
`/connect/cms/contents/{contentKeyOrId}` all return `METHOD_NOT_ALLOWED: "Allowed are GET,HEAD"`.
Guessed sub-resources (`/versions`, `/variants`) either don't exist (`NOT_FOUND`) or are gated
behind a disabled feature (`FUNCTIONALITY_NOT_ENABLED`) unrelated to this write path. The
`ManagedContent` SObject itself is `createable: false` / `updateable: false` at the describe
level, confirming this isn't a permissions gap — editing is UI-only.

**Consequence for this skill**: to improve an already-created Email/WhatsApp content item (e.g.
applying a better HTML template to a draft built by an earlier run), don't attempt any further
write-method guesses against `/connect/cms/contents/{id}`. Instead, produce the finished
`rawHtml` (for Email) or message body (for WhatsApp) as a ready-to-paste block and tell the user
to open the content in the Lightning CMS editor (`https://{domain}/lightning/r/ManagedContent/{managedContentId}/view`)
and paste it into the HTML source / message body field by hand — same manual-handoff pattern as
the CMS folder limitation above. This only affects **editing existing** content; creating new
content via step 8 is unaffected.

---

## Critical Rules

- **Confirm once, then run the whole chain.** After collecting the Account name and campaign theme, do a brief summary ("Voy a crear la campaña X para la cuenta Y, con un email y whatsapp de tema Z") and get a go-ahead — then execute Campaign → content → Flow straight through without pausing for approval at each individual record. Real, visible changes in the org, but this skill's whole value is doing it end-to-end in one pass.
- **Never fabricate campaign copy.** Get the real brief (product, audience, message) from the user first — a demo is still a bad demo if the copy is meaningless filler.
- **Use `sf api request rest` for anything Connect/Tooling API** — it authenticates automatically. Never try to print or export the org's raw access token (`SF_TEMP_SHOW_SECRETS=true` is blocked and unnecessary).
- **Run Salesforce CLI commands through PowerShell, not the Bash tool** — on Windows, Git Bash fails to resolve the `sf` CLI install path under `C:\Program Files\...` ("`C:\Program` no se reconoce..."), while PowerShell handles it correctly.
- **Write large JSON bodies to a scratch file and pass `-b "@<path>"`** instead of inline `-b '{...}'` — the Email content body especially gets large, and inline quoting in PowerShell is unreliable for nested JSON. **Build that file with here-string templating, not `ConvertTo-Json`** — `ConvertTo-Json -Depth <N>` over the nested ordered-hashtable component tree can hang for minutes (climbing CPU, no output) once a large `rawHtml`/message-body string is embedded in it, even at ordinary sizes (~5KB). See `references/api-recipes.md` step 3 for the working pattern (pre-written JSON skeleton + a small JSON-escape helper function substituted in via string interpolation).
- **Never guess the CMS "Use components" schema from scratch.** The validated shape is a component tree (`sfdc_cms/rootContentBlock` → `lightning/section` → `lightning/column` → a content component). If a future request needs a different component (Image, Button, Divider, Text) beyond the HTML block already documented in `references/api-recipes.md`, get a real example from the org first (create it by hand in the UI, fetch it via `GET /connect/cms/contents/{id}`) rather than inventing the block schema — a wrong schema silently corrupts the content.
- **Never write the email's `rawHtml` as a plain, unstyled paragraph.** The CMS shape (one `lightning/html` block) is fixed, but what goes inside it must be a full table-based, inline-styled marketing email — build it on **Archetype E** (rich structure, white/light canvas) from `references/email-templates.md` by default, filled with the theme's real copy and the Account's real accent color; only use Archetype A–D instead if the user explicitly names one. A one-`<p>`-tag email, or a sparse email missing the hero/highlight-badge/stat-box/items-list/comparison/repeated-CTA structure, is a quality bug, not an acceptable minimal version.
- **The Flow will show `InvalidDraft` after creation — that's expected**, not a bug. It mirrors the state of every real example found in the reference org. Don't try to force it to `Active`; that requires manual steps only the user can complete (see below).
- **Build the Flow as a plain linear chain by default** (see "Default Flow shape" above) — `Send Email → Wait 1 Day → Send WhatsApp → end`, no Decisions, no Task, no forward-to-agent. The engagement-branching variant (Decisions, follow-up Task via the Campaign's `OwnerId`, forward-to-agent) is only built if the user explicitly asks for it; when they do, its two Decision "Sí" conditions stay as the validated always-true placeholder (action compared to itself) until the user supplies a real engagement field — don't invent one.

---

## What's Left to Activate (always tell the user this)

The Flow this skill builds is intentionally a **scaffold** — matching how real campaigns look in this org before someone finishes wiring them by hand. After this skill runs, these are still manual, UI-only steps:

1. **Publish** both the Email and WhatsApp content items (Draft → Published).
2. **Attach a Data Cloud Segment** and a frequency to the Flow's `start` trigger (currently unset — this is why the Flow is `InvalidDraft`). This step doesn't have to stay manual: **offer to build the Segment with `pc-crm-salesforce-demos-segmentos`**, the companion skill that creates Account fields, maps them through to Data Cloud, and creates a real `MarketSegment` via the Segmentation REST API. It still can't attach the Segment to *this* Flow's `start` trigger via API (untested — the Flow's `start` element has no documented Segment-reference field), so wiring the created Segment onto the trigger stays a manual Flow Builder step, but the Segment itself no longer has to be built by hand.
3. **Select a valid From Address / communication subscription** on the Send Email action.
4. **Select a WhatsApp channel** on the Send WhatsApp action.
5. *(Only if the engagement-branching variant was used)* **Replace the two placeholder Decision conditions** ("¿Tuvo interacción?" / "¿Respondió?") with a real engagement field once the user knows which one applies — see "Default Flow shape" above. Not applicable to the plain linear default, which has no Decisions.
6. *(Only if the engagement-branching variant was used, and optional even then)* Add a "dormant lead" exit branch (`exitIndividualsFromFlow`) on the final Decision's default path. This can be **offered** right after step 6 creates the Flow (its own Id exists by then) — see `references/api-recipes.md` step 6.6 — but only as an experimental, unvalidated extra: the one real example on file used a broken placeholder `IndividualId`, so the real reference value still has to come from the user or a genuinely working example elsewhere in the org, never invented.
7. Activate the Flow once the above are in place.

Do not attempt to script steps 1–4 without a validated example — they weren't tested against the API in the session this skill was built from.
