# Email & WhatsApp Content Templates

The CMS "Use components" shape for an Email is always **one** `lightning/html` block holding
the full email as a `rawHtml` string (see `data-model.md` §3 — don't second-guess that part,
it's empirically validated). What goes **inside** that string was previously left to
freeform improvisation and came out looking like a plain paragraph. This file fixes that: it
gives five validated, professional email archetypes (real client examples, genericized into
placeholders) plus the WhatsApp copy pattern, so every demo email looks like a real marketing
email, not a wall of unstyled text. Build every email on **Archetype E** by default (see
"Choosing an archetype" below) — A–D are kept as opt-in legacy variants.

**Never write a single plain `<p>`/`<div>` of copy as the whole email.** Always build on one
of the five archetypes below: table-based layout, inline CSS only (email clients strip
`<style>` blocks and classes unreliably), a header band, a hero, a body/offer section, one or
two CTA buttons, and a footer with legal/unsubscribe text.

---

## Universal HTML email rules (apply in every archetype)

- **Table-based layout only.** `<table role="presentation" width="..." cellpadding="0" cellspacing="0" border="0">` nesting, never CSS flexbox/grid. This is the only layout method that survives Outlook/Gmail rendering.
- **All styling inline**, via `style="..."` attributes on every element. No `<style>` block, no classes — most email clients strip or ignore them.
- **Outer wrapper table** at `width="100%"`, background matching the page background, containing one **inner container table** at `width="600"` (`max-width:600px` for mobile), centered with `align="center"`.
- **Typography**: pick a font stack and type scale from the "Typography system" section right below, and repeat `font-family` inline on every text-bearing element — never rely on inheritance from `<body>`. See that section for why.
- **Header band**: brand wordmark/logo text, on a colored background strip, top of the email.
- **Hero section**: the emotional hook — an eyebrow label (small caps, colored), a bold headline (using the recipient's actual campaign theme, not generic filler), and 1–2 lines of supporting copy.
- **Body**: a greeting using the recipient's first name, 1–3 short paragraphs of context (from the theme brief in SKILL.md step 3 — never invented), and usually one **highlighted info/offer box** (bordered or tinted background, key facts as label/value rows or a big number).
- **CTA button**: an `<a>` styled as a button (background color, padding, border-radius, bold text, no underline), wrapped in its own small table cell so it centers reliably. Every email needs at least one; long emails can repeat it near the end.
- **Divider**: `<hr style="border:none; border-top:1px solid {color};" />` between major sections — cheap and reliable in every client.
- **Footer**: small gray legal text — company name + city/country, why the recipient is receiving this email, an `Unsubscribe` link, a privacy-policy link. For regulated industries (finance, health), add the relevant disclaimer register (rate/terms fine print, regulator name, data-protection law reference) — infer the right one from the account's country/industry, don't invent a fake law citation if unsure, ask instead.
- **Personalization**: always greet the SKILL.md step 3.2 demo persona by their real first name, **hardcoded as literal text** ("Hola, Juan," not "Estimado cliente"), and ideally once more in the body. **Two separate things, don't conflate them (confirmed 2026-08-12, extended 2026-08-19)**: (1) there is still no validated merge-field syntax for injecting a live `$unifiedIndividual` field (e.g. first name) into `rawHtml` — the `contentBody` uses `{!$brand.*}` merge syntax elsewhere in the payload, so an analogous `{!$unifiedIndividual.FirstName}` is tempting, but it's untested and would be guessing a field API name on a Data Cloud DMO; never write that merge tag. (2) That's unrelated to using the step 3.2 persona's name as plain hardcoded text — the persona is a single fixed named demo character the whole email/WhatsApp pair is written for, not a live token meant to resolve differently per actual recipient, so there's no merge field to invent in the first place. If no persona was defined (older workflow, or the user skipped it), fall back to a name-independent greeting ("Hola,") rather than a fabricated merge tag.
- **Marketing voice (confirmed 2026-08-19)**: every headline, hero line, item-list label, comparison-box label, and CTA must read as **persuasive marketing copy that leads with a benefit to the reader**, never a neutral factual bulletin. Diagnostic: "Qué es / Dónde se presentó / Qué representa para usted" is a report; "Su negocio ya puede crecer sin fronteras" is marketing — same facts, different framing. This applies even to serious B2B/institutional themes; the lever is confident, benefit-driven language and stronger CTA verbs ("Quiero conocer más", "Hablemos de tu expansión" vs. a flat "Coordinar una conversación" or "Más información"), not emoji or retail slang — those stay governed by the rule below. Still never invent a benefit/claim that isn't grounded in the real brief from step 3 / step 3.1's site crawl — reframe the real facts persuasively, don't add new ones.
- **Emoji**: fine for casual/retail brands (Pizza-style), sparing-to-none for financial/medical/institutional brands (Bancom/ZO/FEISA style) — match the theme's tone, not a fixed rule.
- **Links**: build the CTA `href` from a real or plausible destination tied to the Account (e.g. `https://{account-site}/...?ref={recipient-slug}`) — never a bare `#` for the primary CTA; a placeholder `#` is fine only for `Unsubscribe`/`Privacy policy` since those aren't the point of the demo.

---

## Typography system

**Two vetted font stacks — pick one per email, never mix them within the same message:**

| Stack | Value | Use for |
|---|---|---|
| Modern/casual | `-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif` | Retail, food, loyalty, consumer brands with an app/tech feel (Archetype A) |
| Corporate/traditional | `Arial, Helvetica, sans-serif` | Financial, institutional, B2B, professional-services brands (Archetypes B, C, D) |

A serif accent (`Georgia,'Times New Roman',serif`) is a **deliberate** design choice only for
big offer numbers/headlines in Archetype B, paired with the Arial body copy in the same email —
never as the email's only font, and never applied by omission (that's the bug below).

**Repeat `font-family` inline on every single text-bearing element** (`p`, `span`, `td`, `a`,
`h1`/`h2`, `strong`, `li`) — never declare it once on `<body>` and rely on inheritance. Confirmed
failure mode (2026-07-29, Meximares email): the CMS "Use components" `rawHtml` block can render
without its outer `<html>`/`<body>` wrapper applied, so a body-only `font-family` is silently
dropped and every element falls back to the viewer's serif default (renders as Times New Roman
even though the source says Arial). All four archetypes below already do this correctly — don't
regress it when customizing them or adding new sections.

**Type scale** — apply consistently across every archetype; nudge sizes ±2px to fit a brand, but
keep the hierarchy and never skip a role:

| Role | Size | Weight | Extra |
|---|---|---|---|
| Eyebrow / label | 10–13px | 700 | uppercase, `letter-spacing:1–3px` |
| Hero headline | 22–36px | 700–900 | `line-height:1.2–1.3` |
| Section heading (`h2`-style) | 18–20px | 700 | `line-height:1.3` |
| Subhead / hero supporting copy | 14–16px | 400 | `line-height:1.5` |
| Body paragraph | 14–16px | 400 | `line-height:1.6` |
| Big number / stat | 32–52px | 700–900 | `line-height:1`, use the serif accent here if the archetype calls for it |
| Button label | 14–18px | 700 | `letter-spacing:0.5–1px`; uppercase for retail/loyalty tone, normal case for professional/B2B tone |
| Label/value row (info box) | 13–14px | label 400 / value 700 | — |
| Fine print / legal / footer | 10–12px | 400 | `line-height:1.5–1.65`, gray (`#666`–`#999` depending on background) |

Don't use more than 4 distinct font sizes in one email outside this scale — visual noise reads as
unpolished, even with the layout otherwise correct.

---

## Choosing an archetype

**Default for every theme, as of 2026-08-19: Archetype E — Rich/Light (below).** Confirmed with
the user on the SMS Latam session: they held up Archetype A's structural richness (hero, urgency/
highlight badge, big-number stat box, items list, comparison section, CTA repeated) as the bar —
"el que haces ahora es horrible" about a plainer archetype (C) used for a B2B theme — then said
this structure should be the default **for every theme**, not just retail/loyalty, and then
corrected the canvas: "usa background blancos, no negros" — so Archetype E is Archetype A's exact
structural skeleton with a white/light canvas instead of a dark one, colored from the Account's
own real brand accent (step 3.1), never a fixed orange/dark palette. Build every email on
Archetype E unless the user explicitly asks for one of A–D by name.

Archetypes A–D below are kept as **opt-in legacy variants** — still fully valid HTML, still
theme-tested — for when a user specifically asks for a dark/bold retail canvas, a financial
serif-accent layout, a minimal advisor-style follow-up, or an institutional benefits band. The old
theme→archetype mapping table that used to drive the default choice is preserved here only as a
reference for picking among A–D when asked for one by name, not as the default-selection logic
anymore:

| Theme | Archetype (if explicitly requested) |
|---|---|
| Win-back / reactivación, loyalty points expiring, carrito abandonado (retail/food/consumer) | **A — Bold/Dark Loyalty** |
| Promoción financiera, preaprobado, producto bancario/seguro | **B — Corporate/Financial** |
| Seguimiento post-evento/feria, calificación de lead B2B, contacto profesional/médico | **C — Professional/B2B** |
| Cumpleaños/aniversario institucional, onboarding/welcome, renovación/cross-sell de beneficios | **D — Institutional/Benefits** |

---

## Archetype A — Bold/Dark Loyalty & Retail

Dark canvas, rounded card, gradient hero, urgency badge, a rewards/points box, a "what you get"
item list, a two-column "if you don't act / if you act" comparison, a numbered how-to strip,
CTA repeated twice, casual emoji throughout.

```html
<html lang="es"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta http-equiv="X-UA-Compatible" content="IE=edge" /><title>{{EMAIL_SUBJECT}}</title></head><body style="background-color:#0a0a0a; margin:0; padding:0;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#0a0a0a" style="background-color:#0a0a0a;"><tbody><tr><td align="center" style="padding:30px 16px;">
<table width="600" cellpadding="0" cellspacing="0" border="0" bgcolor="#111111" style="max-width:600px; border-radius:12px; overflow:hidden; background-color:#111111;"><tbody>
<tr><td align="center" style="padding:40px 30px 20px;">
  <p style="font-family:{{FONT_STACK}}; font-size:32px; font-weight:900; text-align:center; margin:0; letter-spacing:-1px;">
    <span style="color:#FFFFFF;">{{BRAND_WORD_PART_1}}</span><span style="color:{{COLOR_ACCENT}};">{{BRAND_WORD_PART_2}}</span>
  </p>
</td></tr>
<tr><td align="center" style="padding:0;">
  <div style="background: linear-gradient(135deg, #1a1a1a 0%, {{COLOR_DARK_ACCENT_BG}} 100%); padding:40px 30px; text-align:center;">
    <p style="font-family:{{FONT_STACK}}; font-size:13px; letter-spacing:3px; color:{{COLOR_ACCENT}}; text-transform:uppercase; margin:0 0 10px; font-weight:700;">{{EYEBROW_LABEL}}</p>
    <h1 style="font-family:{{FONT_STACK}}; font-size:36px; line-height:42px; color:#FFFFFF; margin:0 0 8px; font-weight:900;">{{HEADLINE_LINE_1}}<br />{{HEADLINE_LINE_2_PREFIX}} <span style="color:{{COLOR_HIGHLIGHT}};">{{HEADLINE_LINE_2_HIGHLIGHT}}</span></h1>
    <p style="font-family:{{FONT_STACK}}; font-size:16px; line-height:24px; color:#BBBBBB; margin:0;">{{HERO_SUBCOPY — theme context, from the brief}}</p>
  </div>
</td></tr>
<tr><td align="center" style="padding:30px 30px 12px;">
  <table cellpadding="0" cellspacing="0" border="0" style="border-radius:6px; background-color:{{COLOR_DARK_ACCENT_BG}}; border:1px solid {{COLOR_ACCENT}};"><tbody><tr><td style="padding:8px 18px;">
    <p style="font-family:{{FONT_STACK}}; font-size:13px; font-weight:700; color:{{COLOR_URGENCY_TEXT}}; margin:0;">⏳ {{URGENCY_BADGE_TEXT}}</p>
  </td></tr></tbody></table>
</td></tr>
<tr><td align="center" style="padding:6px 30px 30px;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#1a1a1a" style="border:1px solid #333; border-radius:10px; background-color:#1a1a1a;"><tbody><tr><td align="center" style="padding:24px 20px;">
    <p style="font-family:{{FONT_STACK}}; font-size:13px; color:#999; text-transform:uppercase; letter-spacing:2px; margin:0 0 8px;">{{OFFER_BOX_LABEL}}</p>
    <p style="font-family:{{FONT_STACK}}; font-size:48px; font-weight:900; color:{{COLOR_HIGHLIGHT}}; margin:0 0 4px; line-height:1;">{{OFFER_BOX_BIG_NUMBER}}</p>
    <p style="font-family:{{FONT_STACK}}; font-size:13px; color:{{COLOR_URGENCY_TEXT}}; margin:0; font-weight:700;">{{OFFER_BOX_SUBLABEL — e.g. expiry date}}</p>
  </td></tr></tbody></table>
</td></tr>
<tr><td align="center" style="padding:0 30px 30px;">
  <a href="{{CTA_URL}}" target="_blank" style="display:inline-block; background-color:{{COLOR_HIGHLIGHT}}; color:#0a0a0a; font-family:{{FONT_STACK}}; font-size:18px; font-weight:700; text-decoration:none; padding:16px 48px; border-radius:8px; text-transform:uppercase; letter-spacing:1px;">{{CTA_EMOJI}} {{CTA_TEXT}}</a>
</td></tr>
<tr><td style="padding:0 30px;"><hr style="border:none; border-top:1px solid #222;" /></td></tr>
<tr><td style="padding:30px;">
  <h2 style="font-family:{{FONT_STACK}}; font-size:20px; color:#FFFFFF; text-align:center; margin:0 0 8px;">{{ITEM_LIST_TITLE}}</h2>
  <p style="font-family:{{FONT_STACK}}; font-size:14px; color:#999; text-align:center; margin:0 0 20px;">{{ITEM_LIST_SUBTITLE}}</p>
  <table width="100%" cellpadding="0" cellspacing="0" border="0"><tbody>
  <!-- repeat this row per item (2-4 items), last row without border-bottom -->
  <tr><td style="padding:14px 0; border-bottom:1px solid #1a1a1a;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0"><tbody><tr>
      <td width="48" style="vertical-align:middle; padding-right:14px;"><span style="font-size:32px;">{{ITEM_EMOJI}}</span></td>
      <td style="vertical-align:middle;">
        <p style="font-family:{{FONT_STACK}}; font-size:16px; font-weight:700; color:#FFFFFF; margin:0;">{{ITEM_TITLE}}</p>
        <p style="font-family:{{FONT_STACK}}; font-size:13px; color:#888; margin:4px 0 0;">{{ITEM_SUBTITLE}}</p>
      </td>
      <td width="90" align="right" style="vertical-align:middle;"><p style="font-family:{{FONT_STACK}}; font-size:16px; font-weight:900; color:{{COLOR_HIGHLIGHT}}; margin:0;">{{ITEM_VALUE}}</p></td>
    </tr></tbody></table>
  </td></tr>
  </tbody></table>
</td></tr>
<tr><td style="padding:0 30px;"><hr style="border:none; border-top:1px solid #222;" /></td></tr>
<tr><td style="padding:30px;">
  <h2 style="font-family:{{FONT_STACK}}; font-size:20px; color:#FFFFFF; text-align:center; margin:0 0 20px;">{{COMPARISON_TITLE}}</h2>
  <table width="100%" cellpadding="0" cellspacing="0" border="0"><tbody><tr>
    <td width="50%" style="padding:16px; vertical-align:top; background-color:#1a1a1a; border-radius:8px; border:1px solid {{COLOR_DARK_ACCENT_BG}};">
      <p style="font-family:{{FONT_STACK}}; font-size:13px; font-weight:700; color:{{COLOR_URGENCY_TEXT}}; margin:0 0 6px; text-transform:uppercase; letter-spacing:1px;">{{COMPARISON_NEGATIVE_LABEL}}</p>
      <p style="font-family:{{FONT_STACK}}; font-size:14px; color:#999; margin:0;">{{COMPARISON_NEGATIVE_TEXT}}</p>
    </td>
    <td width="16">&nbsp;</td>
    <td width="50%" style="padding:16px; vertical-align:top; background-color:#1a1a1a; border-radius:8px; border:1px solid {{COLOR_HIGHLIGHT}};">
      <p style="font-family:{{FONT_STACK}}; font-size:13px; font-weight:700; color:{{COLOR_HIGHLIGHT}}; margin:0 0 6px; text-transform:uppercase; letter-spacing:1px;">{{COMPARISON_POSITIVE_LABEL}}</p>
      <p style="font-family:{{FONT_STACK}}; font-size:14px; color:#FFFFFF; margin:0;">{{COMPARISON_POSITIVE_TEXT}}</p>
    </td>
  </tr></tbody></table>
</td></tr>
<tr><td align="center" style="padding:0 30px 10px;">
  <a href="{{CTA_URL}}" target="_blank" style="display:inline-block; background-color:{{COLOR_HIGHLIGHT}}; color:#0a0a0a; font-family:{{FONT_STACK}}; font-size:18px; font-weight:700; text-decoration:none; padding:16px 48px; border-radius:8px; text-transform:uppercase; letter-spacing:1px;">{{CTA_TEXT_SECONDARY}}</a>
</td></tr>
<tr><td align="center" style="padding:0 30px 20px;">
  <p style="font-family:{{FONT_STACK}}; font-size:12px; color:#666; margin:0;">⏳ {{FINE_PRINT — expiry + validity terms}}</p>
</td></tr>
<tr><td style="padding:0 30px;"><hr style="border:none; border-top:1px solid #222;" /></td></tr>
<tr><td align="center" style="padding:30px;">
  <p style="font-family:{{FONT_STACK}}; font-size:11px; color:#666; line-height:18px; margin:0 0 12px;">
    {{ACCOUNT_NAME}} · {{ACCOUNT_DOMAIN}}<br />
    {{WHY_RECEIVING_TEXT}}<br />
    ¿No querés recibir más promos? <a href="#" style="color:{{COLOR_HIGHLIGHT}}; text-decoration:underline;">Unsubscribe</a>
  </p>
</td></tr>
</tbody></table>
</td></tr></tbody></table>
</body></html>
```

---

## Archetype B — Corporate/Financial

Light neutral canvas, white card, colored header band, dark navy hero with a serif big-number
offer, a 3-column stat row (bordered mini-cards), one CTA plus a phone fallback, and a dense
regulatory disclaimer footer.

```html
<html lang="es"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>{{EMAIL_SUBJECT}}</title></head><body style="margin:0;padding:0;background-color:{{COLOR_PAGE_BG}};font-family:{{FONT_STACK}};">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{{COLOR_PAGE_BG}};padding:32px 0;"><tbody><tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;background-color:#ffffff;"><tbody>
<tr><td style="background-color:{{COLOR_BRAND}};padding:20px 32px;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0"><tbody><tr>
    <td style="font-size:26px;font-weight:800;color:#ffffff;letter-spacing:-0.5px;font-family:{{FONT_STACK}};">{{BRAND_WORD_PART_1}}<span style="color:{{COLOR_ACCENT}};">{{BRAND_WORD_PART_2}}</span></td>
    <td align="right" style="font-size:10px;color:rgba(255,255,255,0.7);line-height:1.4;font-family:{{FONT_STACK}};">{{ACCOUNT_TAGLINE}}<br />{{ACCOUNT_LOCATION}}</td>
  </tr></tbody></table>
</td></tr>
<tr><td style="background-color:{{COLOR_DARK}};padding:36px 32px 32px;">
  <p style="margin:0 0 12px 0;font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:{{COLOR_ACCENT}};font-family:{{FONT_STACK}};">{{EYEBROW_LABEL}}</p>
  <p style="margin:0 0 4px 0;font-size:16px;color:rgba(255,255,255,0.85);font-family:{{SERIF_FONT_STACK}};">{{OFFER_LEAD_IN — "Tu préstamo preaprobado hasta"}}</p>
  <p style="margin:0 0 16px 0;font-size:52px;font-weight:700;color:{{COLOR_ACCENT}};font-family:{{SERIF_FONT_STACK}};letter-spacing:-1px;line-height:1.1;">{{OFFER_BIG_NUMBER}}</p>
  <p style="margin:0;font-size:13px;color:rgba(255,255,255,0.65);line-height:1.6;font-family:{{FONT_STACK}};">{{HERO_SUBCOPY — why they qualify}}</p>
</td></tr>
<tr><td style="padding:28px 32px 0;background-color:{{COLOR_LIGHT_BG}};">
  <p style="margin:0 0 24px 0;font-size:14px;color:#2E2218;line-height:1.65;font-family:{{FONT_STACK}};">Hola <strong style="color:{{COLOR_BRAND}};">{{RECIPIENT_NAME}}</strong>,<br /><br />{{BODY_PARAGRAPH — from the brief}}</p>
</td></tr>
<tr><td style="padding:0 32px 0;background-color:{{COLOR_LIGHT_BG}};">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:24px;"><tbody><tr>
  <!-- 3 stat cells, adjust widths to 32%/4%/32%/4%/32% -->
    <td width="32%" style="text-align:center;padding:16px 10px;background-color:#ffffff;border:1px solid #E8E3DB;">
      <span style="font-size:24px;display:block;margin-bottom:6px;">{{STAT_1_EMOJI}}</span>
      <span style="font-size:18px;font-weight:700;color:{{COLOR_DARK}};font-family:{{SERIF_FONT_STACK}};display:block;">{{STAT_1_VALUE}}</span>
      <span style="font-size:10px;color:#7A6F62;margin-top:3px;font-family:{{FONT_STACK}};display:block;">{{STAT_1_LABEL}}</span>
    </td>
    <td width="4%">&nbsp;</td>
    <td width="32%" style="text-align:center;padding:16px 10px;background-color:#ffffff;border:1px solid #E8E3DB;">
      <span style="font-size:24px;display:block;margin-bottom:6px;">{{STAT_2_EMOJI}}</span>
      <span style="font-size:18px;font-weight:700;color:{{COLOR_DARK}};font-family:{{SERIF_FONT_STACK}};display:block;">{{STAT_2_VALUE}}</span>
      <span style="font-size:10px;color:#7A6F62;margin-top:3px;font-family:{{FONT_STACK}};display:block;">{{STAT_2_LABEL}}</span>
    </td>
    <td width="4%">&nbsp;</td>
    <td width="32%" style="text-align:center;padding:16px 10px;background-color:#ffffff;border:1px solid #E8E3DB;">
      <span style="font-size:24px;display:block;margin-bottom:6px;">{{STAT_3_EMOJI}}</span>
      <span style="font-size:18px;font-weight:700;color:{{COLOR_DARK}};font-family:{{SERIF_FONT_STACK}};display:block;">{{STAT_3_VALUE}}</span>
      <span style="font-size:10px;color:#7A6F62;margin-top:3px;font-family:{{FONT_STACK}};display:block;">{{STAT_3_LABEL}}</span>
    </td>
  </tr></tbody></table>
</td></tr>
<tr><td style="text-align:center;padding:20px 32px 28px;background-color:{{COLOR_LIGHT_BG}};">
  <a href="{{CTA_URL}}" style="display:inline-block;background-color:{{COLOR_BRAND}};color:#ffffff;text-decoration:none;font-weight:700;font-size:14px;letter-spacing:0.05em;padding:15px 44px;font-family:{{FONT_STACK}};">{{CTA_TEXT}} →</a>
  <p style="margin:12px 0 0;font-size:12px;color:#7A6F62;font-family:{{FONT_STACK}};">O llámanos al <strong style="color:{{COLOR_DARK}};">{{PHONE_NUMBER}}</strong> · {{OPENING_HOURS}}</p>
</td></tr>
<tr><td style="padding:0 32px;"><hr style="border:none;border-top:1px solid #E8E3DB;margin:0;" /></td></tr>
<tr><td style="padding:20px 32px 28px;background-color:{{COLOR_LIGHT_BG}};">
  <p style="margin:0 0 14px 0;font-size:10px;color:#9C8E7E;line-height:1.65;font-family:{{FONT_STACK}};">{{REGULATORY_DISCLAIMER — terms, validity date, regulator name; ask the user if unsure rather than inventing}}</p>
  <p style="margin:0;font-size:10px;font-family:{{FONT_STACK}};"><a href="#" style="color:{{COLOR_BRAND}};text-decoration:none;margin-right:16px;">Cancelar suscripción</a><a href="#" style="color:{{COLOR_BRAND}};text-decoration:none;margin-right:16px;">Política de privacidad</a><a href="{{ACCOUNT_URL}}" style="color:{{COLOR_BRAND}};text-decoration:none;">{{ACCOUNT_DOMAIN}}</a></p>
</td></tr>
</tbody></table>
</td></tr></tbody></table>
</body></html>
```

---

## Archetype C — Professional/B2B

Light gray canvas, white card, dark minimal header, a numbered/left-accent question box, one
dark CTA button, an alt-contact line, and a named signature block — reads like a real advisor's
follow-up, not a mass blast.

```html
<html lang="es"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>{{EMAIL_SUBJECT}}</title></head><body style="margin:0;padding:0;background-color:#f4f4f4;font-family:{{FONT_STACK}};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4;padding:24px 0;"><tbody><tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;max-width:600px;width:100%;"><tbody>
<tr><td style="background-color:#111111;padding:32px 40px;text-align:center;">
  <span style="color:#ffffff;font-size:22px;letter-spacing:3px;font-weight:bold;font-family:{{FONT_STACK}};">{{BRAND_WORD}}</span><br />
  <span style="color:{{COLOR_ACCENT}};font-size:12px;letter-spacing:2px;text-transform:uppercase;font-family:{{FONT_STACK}};">{{ACCOUNT_TAGLINE}}</span>
</td></tr>
<tr><td style="padding:40px;">
  <p style="font-family:{{FONT_STACK}};font-size:15px;color:#333333;line-height:1.6;margin:0 0 20px;">{{GREETING — "Estimado/a" + name/title}},</p>
  <p style="font-family:{{FONT_STACK}};font-size:15px;color:#333333;line-height:1.6;margin:0 0 20px;">{{BODY_PARAGRAPH_1 — context, e.g. thanks for visiting the booth}}</p>
  <p style="font-family:{{FONT_STACK}};font-size:15px;color:#333333;line-height:1.6;margin:0 0 20px;">{{BODY_PARAGRAPH_2 — the ask}}</p>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 28px;"><tbody>
  <!-- repeat per question/point, separated by an 8px spacer row -->
  <tr><td style="font-family:{{FONT_STACK}};padding:12px 16px;background-color:#f8f8f6;border-left:3px solid {{COLOR_ACCENT}};font-size:14px;color:#333333;line-height:1.5;"><strong>1.</strong> {{QUESTION_1}}</td></tr>
  <tr><td style="height:8px;line-height:8px;font-size:0;">&nbsp;</td></tr>
  <tr><td style="font-family:{{FONT_STACK}};padding:12px 16px;background-color:#f8f8f6;border-left:3px solid {{COLOR_ACCENT}};font-size:14px;color:#333333;line-height:1.5;"><strong>2.</strong> {{QUESTION_2}}</td></tr>
  <tr><td style="height:8px;line-height:8px;font-size:0;">&nbsp;</td></tr>
  <tr><td style="font-family:{{FONT_STACK}};padding:12px 16px;background-color:#f8f8f6;border-left:3px solid {{COLOR_ACCENT}};font-size:14px;color:#333333;line-height:1.5;"><strong>3.</strong> {{QUESTION_3}}</td></tr>
  </tbody></table>
  <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 auto;"><tbody><tr><td align="center" style="border-radius:4px;background-color:#111111;">
    <a href="{{CTA_URL}}" target="_blank" style="display:inline-block;padding:14px 32px;color:#ffffff;text-decoration:none;font-size:14px;letter-spacing:1px;text-transform:uppercase;font-weight:bold;font-family:{{FONT_STACK}};">{{CTA_TEXT}}</a>
  </td></tr></tbody></table>
  <p style="font-family:{{FONT_STACK}};font-size:13px;color:#777777;line-height:1.6;margin:28px 0 0;">{{ALT_CONTACT_LINE — reply or WhatsApp number}}</p>
</td></tr>
<tr><td style="padding:0 40px 40px;">
  <p style="font-family:{{FONT_STACK}};font-size:14px;color:#333333;line-height:1.6;margin:0;">Saludos,<br /><strong>{{SENDER_NAME}}</strong><br />{{SENDER_ROLE}} — {{SENDER_ORG}}</p>
</td></tr>
<tr><td style="background-color:#f4f4f4;padding:24px 40px;text-align:center;border-top:1px solid #e5e5e5;">
  <p style="font-family:{{FONT_STACK}};font-size:11px;color:#999999;line-height:1.5;margin:0;">{{WHY_RECEIVING_TEXT}}</p>
</td></tr>
</tbody></table>
</td></tr></tbody></table>
</body></html>
```

---

## Archetype D — Institutional/Benefits

Light blue-gray canvas, rounded white card, navy header band, a colored hero band whose color
signals the journey purpose (purple/urgent = renewal or cross-sell, green = welcome/good news,
amber = general reminder), an info/offer box of label→value rows, one CTA, an alt-contact line,
and a data-protection footer.

```html
<html lang="es"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>{{EMAIL_SUBJECT}}</title></head><body style="margin:0; padding:0; background-color:{{COLOR_PAGE_BG}}; font-family:{{FONT_STACK}};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:{{COLOR_PAGE_BG}}; padding:24px 0;"><tbody><tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background-color:#FFFFFF; border-radius:8px; overflow:hidden; max-width:600px; width:100%;"><tbody>
<tr><td style="background-color:{{COLOR_BRAND_DARK}}; padding:24px 32px;" align="left">
  <span style="color:#FFFFFF; font-size:22px; font-weight:bold; letter-spacing:1px; font-family:{{FONT_STACK}};">{{BRAND_WORD}}</span>
  <span style="color:{{COLOR_ACCENT}}; font-size:13px; font-weight:bold; display:block; margin-top:2px; font-family:{{FONT_STACK}};">{{ACCOUNT_TAGLINE}}</span>
</td></tr>
<tr><td style="background-color:{{COLOR_HERO_BAND — purple/green/amber per journey purpose}}; padding:28px 32px;">
  <p style="color:#FFFFFF; font-size:24px; font-weight:bold; margin:0 0 8px 0; line-height:1.3; font-family:{{FONT_STACK}};">{{HEADLINE}}</p>
  <p style="color:{{COLOR_HERO_SUBTEXT}}; font-size:16px; margin:0; line-height:1.5; font-family:{{FONT_STACK}};">{{HERO_SUBCOPY}}</p>
</td></tr>
<tr><td style="padding:32px;">
  <p style="color:#1A1A1A; font-size:16px; line-height:1.6; margin:0 0 16px 0; font-family:{{FONT_STACK}};">Hola <strong>{{RECIPIENT_NAME}}</strong>,</p>
  <p style="color:#1A1A1A; font-size:16px; line-height:1.6; margin:0 0 16px 0; font-family:{{FONT_STACK}};">{{BODY_PARAGRAPH_1}}</p>
  <p style="color:#1A1A1A; font-size:16px; line-height:1.6; margin:0 0 24px 0; font-family:{{FONT_STACK}};">{{BODY_PARAGRAPH_2}}</p>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:{{COLOR_INFO_BOX_BG}}; border-left:4px solid {{COLOR_HERO_BAND}}; border-radius:6px; margin-bottom:24px;"><tbody><tr><td style="padding:20px 24px;">
    <p style="color:{{COLOR_HERO_BAND}}; font-size:14px; font-weight:bold; margin:0 0 12px 0; text-transform:uppercase; letter-spacing:0.5px; font-family:{{FONT_STACK}};">{{INFO_BOX_TITLE}}</p>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tbody>
    <!-- repeat per fact, 3-5 rows -->
    <tr><td style="color:#4A4A4A; font-size:14px; padding:4px 0; font-family:{{FONT_STACK}};">{{FACT_1_LABEL}}</td><td style="color:#1A1A1A; font-size:14px; font-weight:bold; padding:4px 0; font-family:{{FONT_STACK}};" align="right">{{FACT_1_VALUE}}</td></tr>
    <tr><td style="color:#4A4A4A; font-size:14px; padding:4px 0; font-family:{{FONT_STACK}};">{{FACT_2_LABEL}}</td><td style="color:#1A1A1A; font-size:14px; font-weight:bold; padding:4px 0; font-family:{{FONT_STACK}};" align="right">{{FACT_2_VALUE}}</td></tr>
    <tr><td style="color:#4A4A4A; font-size:14px; padding:4px 0; font-family:{{FONT_STACK}};">{{FACT_3_LABEL}}</td><td style="color:#1A1A1A; font-size:14px; font-weight:bold; padding:4px 0; font-family:{{FONT_STACK}};" align="right">{{FACT_3_VALUE}}</td></tr>
    </tbody></table>
  </td></tr></tbody></table>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tbody><tr><td align="center" style="padding:8px 0 24px 0;">
    <a href="{{CTA_URL}}" style="background-color:{{COLOR_HERO_BAND}}; color:#FFFFFF; font-size:16px; font-weight:bold; text-decoration:none; padding:14px 32px; border-radius:6px; display:inline-block; font-family:{{FONT_STACK}};">{{CTA_TEXT}}</a>
  </td></tr></tbody></table>
  <p style="color:#4A4A4A; font-size:13px; line-height:1.5; margin:0; font-family:{{FONT_STACK}};">{{ALT_CONTACT_LINE}}</p>
</td></tr>
<tr><td style="padding:0 32px;"><hr style="border:none; border-top:1px solid #E3E8ED; margin:0;" /></td></tr>
<tr><td style="padding:24px 32px;">
  <p style="color:#8A8A8A; font-size:12px; line-height:1.6; margin:0 0 8px 0; font-family:{{FONT_STACK}};">{{ACCOUNT_NAME}} — {{ACCOUNT_TAGLINE}} · {{ACCOUNT_LOCATION}}<br />{{DATA_PROTECTION_DISCLAIMER — cite the real applicable law only if known; otherwise ask}}</p>
  <p style="color:#8A8A8A; font-size:12px; margin:0; font-family:{{FONT_STACK}};"><a href="#" style="color:{{COLOR_BRAND_DARK}}; text-decoration:underline;">Cancelar suscripción</a> · <a href="#" style="color:{{COLOR_BRAND_DARK}}; text-decoration:underline;">Política de privacidad</a></p>
</td></tr>
</tbody></table>
</td></tr></tbody></table>
</body></html>
```

---

## Archetype E — Rich/Light (default, 2026-08-19)

Archetype A's exact structural skeleton — wordmark header, gradient hero, highlight/urgency
badge, big-number stat box, CTA, an items list of 3, a two-column comparison box, CTA repeated,
footer — rebuilt on a **white/light canvas** instead of a dark one. Validated on the SMS Latam
"SMS Delivery Center" campaign: the highlight badge and big-number box don't have to be literal
retail urgency/discount copy — reused there as "presented at ENGAGE 2026" and "12 DE JUNIO" (the
announcement date) respectively, since the theme had no expiry/discount to report. Keep the slots'
*structural role* (a short highlight callout; one prominent stat) but let the theme's real facts
fill them — never force a discount or countdown onto a theme that doesn't have one.

```html
<html lang="es"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta http-equiv="X-UA-Compatible" content="IE=edge" /><title>{{EMAIL_SUBJECT}}</title></head><body style="background-color:#f4f4f4; margin:0; padding:0;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f4f4f4" style="background-color:#f4f4f4;"><tbody><tr><td align="center" style="padding:30px 16px;">
<table width="600" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff" style="max-width:600px; border-radius:12px; overflow:hidden; background-color:#ffffff; border:1px solid #e5e5e5;"><tbody>
<tr><td align="center" style="padding:40px 30px 20px;">
  <p style="font-family:{{FONT_STACK}}; font-size:26px; font-weight:900; text-align:center; margin:0; letter-spacing:-0.5px;">
    <span style="color:#111111;">{{BRAND_WORD_PART_1}}</span><span style="color:{{COLOR_ACCENT}};">{{BRAND_WORD_PART_2}}</span>
  </p>
</td></tr>
<tr><td align="center" style="padding:0;">
  <div style="background: linear-gradient(135deg, {{COLOR_ACCENT_TINT_LIGHT}} 0%, {{COLOR_ACCENT_TINT}} 100%); padding:40px 30px; text-align:center;">
    <p style="font-family:{{FONT_STACK}}; font-size:13px; letter-spacing:3px; color:{{COLOR_ACCENT}}; text-transform:uppercase; margin:0 0 10px; font-weight:700;">{{EYEBROW_LABEL}}</p>
    <h1 style="font-family:{{FONT_STACK}}; font-size:32px; line-height:38px; color:#111111; margin:0 0 8px; font-weight:900;">{{HEADLINE_LINE_1}}<br />{{HEADLINE_LINE_2_PREFIX}} <span style="color:{{COLOR_ACCENT}};">{{HEADLINE_LINE_2_HIGHLIGHT}}</span></h1>
    <p style="font-family:{{FONT_STACK}}; font-size:16px; line-height:24px; color:#4a4a4a; margin:0;">{{HERO_SUBCOPY — theme context, from the brief}}</p>
  </div>
</td></tr>
<tr><td style="padding:26px 30px 0;">
  <p style="font-family:{{FONT_STACK}}; font-size:15px; color:#333333; line-height:1.6; margin:0;">Hola, <strong>{{RECIPIENT_NAME}}</strong> — {{PERSONA_CONTEXT_LINE — one short sentence tying the persona's story to why they're getting this, from SKILL.md step 3.2}}</p>
</td></tr>
<tr><td align="center" style="padding:18px 30px 12px;">
  <table cellpadding="0" cellspacing="0" border="0" style="border-radius:6px; background-color:{{COLOR_ACCENT_TINT_LIGHT}}; border:1px solid {{COLOR_ACCENT}};"><tbody><tr><td style="padding:8px 18px;">
    <p style="font-family:{{FONT_STACK}}; font-size:13px; font-weight:700; color:{{COLOR_ACCENT}}; margin:0;">{{HIGHLIGHT_BADGE_TEXT — urgency, or a relevant callout if the theme has no deadline}}</p>
  </td></tr></tbody></table>
</td></tr>
<tr><td align="center" style="padding:6px 30px 30px;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f8f8f6" style="border:1px solid #e5e5e5; border-radius:10px; background-color:#f8f8f6;"><tbody><tr><td align="center" style="padding:24px 20px;">
    <p style="font-family:{{FONT_STACK}}; font-size:13px; color:#7a7a7a; text-transform:uppercase; letter-spacing:2px; margin:0 0 8px;">{{STAT_BOX_LABEL}}</p>
    <p style="font-family:{{FONT_STACK}}; font-size:44px; font-weight:900; color:{{COLOR_ACCENT}}; margin:0 0 4px; line-height:1;">{{STAT_BOX_BIG_VALUE — a number, date, or percentage; whatever the theme's real key fact is}}</p>
    <p style="font-family:{{FONT_STACK}}; font-size:13px; color:#4a4a4a; margin:0; font-weight:700;">{{STAT_BOX_SUBLABEL}}</p>
  </td></tr></tbody></table>
</td></tr>
<tr><td align="center" style="padding:0 30px 30px;">
  <a href="{{CTA_URL}}" target="_blank" style="display:inline-block; background-color:#111111; color:#ffffff; font-family:{{FONT_STACK}}; font-size:16px; font-weight:700; text-decoration:none; padding:16px 48px; border-radius:8px; letter-spacing:0.5px;">{{CTA_TEXT}}</a>
</td></tr>
<tr><td style="padding:0 30px;"><hr style="border:none; border-top:1px solid #e5e5e5;" /></td></tr>
<tr><td style="padding:30px;">
  <h2 style="font-family:{{FONT_STACK}}; font-size:20px; color:#111111; text-align:center; margin:0 0 8px;">{{ITEM_LIST_TITLE}}</h2>
  <p style="font-family:{{FONT_STACK}}; font-size:14px; color:#7a7a7a; text-align:center; margin:0 0 20px;">{{ITEM_LIST_SUBTITLE}}</p>
  <table width="100%" cellpadding="0" cellspacing="0" border="0"><tbody>
  <!-- repeat this row per item (2-4 items), last row without border-bottom -->
  <tr><td style="padding:14px 0; border-bottom:1px solid #f0f0f0;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0"><tbody><tr>
      <td width="8" style="vertical-align:top; padding-right:14px; padding-top:4px;"><span style="display:inline-block; width:8px; height:8px; border-radius:50%; background-color:{{COLOR_ACCENT}};"></span></td>
      <td style="vertical-align:middle;">
        <p style="font-family:{{FONT_STACK}}; font-size:16px; font-weight:700; color:#111111; margin:0;">{{ITEM_TITLE}}</p>
        <p style="font-family:{{FONT_STACK}}; font-size:13px; color:#4a4a4a; margin:4px 0 0;">{{ITEM_SUBTITLE}}</p>
      </td>
    </tr></tbody></table>
  </td></tr>
  </tbody></table>
</td></tr>
<tr><td style="padding:0 30px;"><hr style="border:none; border-top:1px solid #e5e5e5;" /></td></tr>
<tr><td style="padding:30px;">
  <h2 style="font-family:{{FONT_STACK}}; font-size:20px; color:#111111; text-align:center; margin:0 0 20px;">{{COMPARISON_TITLE}}</h2>
  <table width="100%" cellpadding="0" cellspacing="0" border="0"><tbody><tr>
    <td width="50%" style="padding:16px; vertical-align:top; background-color:#f8f8f6; border-radius:8px; border:1px solid #e5e5e5;">
      <p style="font-family:{{FONT_STACK}}; font-size:12px; font-weight:700; color:#7a7a7a; margin:0 0 6px; text-transform:uppercase; letter-spacing:1px;">{{COMPARISON_NEGATIVE_LABEL}}</p>
      <p style="font-family:{{FONT_STACK}}; font-size:14px; color:#4a4a4a; margin:0;">{{COMPARISON_NEGATIVE_TEXT}}</p>
    </td>
    <td width="16">&nbsp;</td>
    <td width="50%" style="padding:16px; vertical-align:top; background-color:{{COLOR_ACCENT_TINT_LIGHT}}; border-radius:8px; border:1px solid {{COLOR_ACCENT}};">
      <p style="font-family:{{FONT_STACK}}; font-size:12px; font-weight:700; color:{{COLOR_ACCENT}}; margin:0 0 6px; text-transform:uppercase; letter-spacing:1px;">{{COMPARISON_POSITIVE_LABEL}}</p>
      <p style="font-family:{{FONT_STACK}}; font-size:14px; color:#111111; margin:0;">{{COMPARISON_POSITIVE_TEXT}}</p>
    </td>
  </tr></tbody></table>
</td></tr>
<tr><td align="center" style="padding:0 30px 10px;">
  <a href="{{CTA_URL}}" target="_blank" style="display:inline-block; background-color:#111111; color:#ffffff; font-family:{{FONT_STACK}}; font-size:16px; font-weight:700; text-decoration:none; padding:16px 48px; border-radius:8px; letter-spacing:0.5px;">{{CTA_TEXT_SECONDARY}}</a>
</td></tr>
<tr><td align="center" style="padding:0 30px 20px;">
  <p style="font-family:{{FONT_STACK}}; font-size:12px; color:#7a7a7a; margin:0;">{{ALT_CONTACT_LINE}}</p>
</td></tr>
<tr><td style="padding:0 30px;"><hr style="border:none; border-top:1px solid #e5e5e5;" /></td></tr>
<tr><td align="center" style="padding:30px;">
  <p style="font-family:{{FONT_STACK}}; font-size:11px; color:#999999; line-height:18px; margin:0 0 12px;">
    {{ACCOUNT_NAME}} · {{ACCOUNT_DOMAIN}}<br />
    {{WHY_RECEIVING_TEXT}}<br />
    {{UNSUBSCRIBE_LABEL — e.g. "¿No querés recibir más comunicaciones?"}} <a href="#" style="color:{{COLOR_ACCENT}}; text-decoration:underline;">Cancelar suscripción</a>
  </p>
</td></tr>
</tbody></table>
</td></tr></tbody></table>
</body></html>
```

Fill `{{COLOR_ACCENT}}` from the Account's real accent color (step 3.1). `{{COLOR_ACCENT_TINT_LIGHT}}`/`{{COLOR_ACCENT_TINT}}` are very light tints of that same accent for the gradient hero and highlight backgrounds (e.g. an accent of `#A2224C` → tints around `#fdf4f7`/`#fbe6ec`) — derive them by mixing the accent toward white, don't invent an unrelated pastel. `{{FONT_STACK}}` follows the same Typography system rules above (corporate stack for B2B/institutional, modern/casual stack for consumer brands) — Archetype E's *layout* is now universal, but font choice still follows brand tone.

---

## WhatsApp Session Message copy pattern

WhatsApp copy is plain text (no HTML, no bold markup was used in the validated examples) —
short, scannable, mobile-first, one clear action. Structure, in order:

1. **Greeting** — `Hola {{RECIPIENT_NAME}} 👋` (+ optionally `Soy de {{ACCOUNT_NAME}}.` when it's a cold or reactivation touch, to (re)introduce the sender).
2. **Context line** — one sentence on why you're messaging now (reminder, follow-up, offer), matching the campaign theme.
3. **The key fact, on its own line** — the number/amount/offer, isolated so it's scannable (e.g. a points balance, a loan amount).
4. **Optional short list** — 2–4 lines, one emoji + item each, only when there are multiple things to enumerate (redeemable rewards, offer features). Skip entirely for simpler messages.
5. **Urgency line** — a deadline/expiry sentence, only if the theme has one.
6. **Single CTA** — as of 1.7.3, **default to a Quick Reply button** (`references/api-recipes.md` §4) rather than an explicit typed instruction: write the body to lead into the button naturally ("Tocá el botón de abajo para...") rather than "Responde SÍ para...". Only fall back to a typed instruction or a bare link (§4.2, plain Text) if the user explicitly asks for it. Never more than one call to action either way.
7. **Optional disclaimer** — one short line, only for regulated offers (finance/health), e.g. validity date + "sujeto a evaluación."

Keep it to what a real person would type — short paragraphs, blank lines between them, 1 emoji
per line at most, no walls of text. Tone follows the theme/brand (casual for retail, more
measured for finance/institutional) — but "measured" still means **persuasive marketing copy**,
not a neutral status update; see the "Marketing voice" rule above, it applies here too. Always
use the recipient's real first name (the SKILL.md step 3.2 persona, hardcoded).

```
Hola {{RECIPIENT_NAME}} 👋 {{OPTIONAL_SENDER_INTRO}}

{{CONTEXT_LINE}}

{{KEY_FACT_LINE}}

{{OPTIONAL_BULLET_1}}
{{OPTIONAL_BULLET_2}}
{{OPTIONAL_BULLET_3}}

{{URGENCY_LINE}}

{{CTA_LINE}}

{{OPTIONAL_DISCLAIMER}}
```

---

## Filling these in

- Replace every `{{PLACEHOLDER}}` — never leave one literal in the API payload.
- **Colors come from the Account's real website, not a guess.** Per SKILL.md step 3.1, fetch the Account's site before writing the email and pull real hex values from it: page/canvas background (`theme-color` meta tag, `<body>`/main wrapper background, or a CSS custom property like `--brand-color`), header/nav background, and the primary button/accent color. Map those into every `{{COLOR_*}}` placeholder in the chosen archetype. **Do not** also set these into the CMS content's top-level `backgroundColor` field — see the correction below, that field is unrelated to the email's own design. Only fall back to an industry-appropriate palette (see archetype descriptions) when the site is genuinely unreachable or the user has no URL — and say so explicitly rather than presenting a guess as the brand's real colors.
- **The CMS content's top-level `backgroundColor` field is the Email Builder's own "Fondo de email" setting — the canvas behind the email card in Salesforce's own UI chrome, not part of the email's visual design.** It is unrelated to whatever background color the `rawHtml` itself uses (Archetype A's inner canvas stays `#0a0a0a` regardless). Default this field to `#ffffff` unless the user explicitly asks for something else — see `api-recipes.md` step 3 for the corrected template. (This corrects the 1.4.0 guidance, which wrongly conflated the two — see the 1.5.5 changelog entry.)
- Copy (headline, body, offer details, disclaimers) must come from the theme brief gathered in SKILL.md step 3 — never invent product claims, prices, or legal terms; if a fact isn't in the brief, ask rather than fabricate it.
- Before pasting into `email_body.json`'s `rawHtml` field, collapse the template to a single line (or escaped `\n`) and escape internal `"` as `\"` — see the "Write large JSON bodies to a scratch file" rule in SKILL.md.
