#!/usr/bin/env python3
"""
normalize_name.py — Propone un nombre normalizado para un skill nuevo.

Fórmula:
    pc-[área]-[sistema?]-[objeto]-[acción]

- `pc-` siempre va (skills propios de ProContacto).
- `[área]` obligatoria (de VALID_AREAS).
- `[sistema]` opcional: se omite cuando el área lo implica (AREAS_OMIT_SYSTEM)
  o cuando no hay sistema externo.
- `[objeto]` obligatorio (entidad/dominio).
- `[acción]` obligatoria, un único verbo de VALID_ACTIONS.

Uso:
    python3 normalize_name.py "skill para crear oportunidades de Salesforce desde Gmail"
    python3 normalize_name.py --json "..."

Notas:
- El parsing es heurístico: detecta área/sistema/objeto/acción por keywords.
- Cuando hay ambigüedad, devuelve múltiples candidatos ordenados por confianza.
- El humano (o Claude) decide el final.
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Any

# --- Dominio de la convención ---------------------------------------------

VALID_AREAS = {
    "crm", "cg-cloud", "data-cloud", "marketing-cloud",
    "integrations", "devops", "data", "delivery",
    "admin-interno", "meta",
}

AREAS_OMIT_SYSTEM = {
    "cg-cloud", "data-cloud", "marketing-cloud",
    "admin-interno", "meta",
}

VALID_SYSTEMS = {
    "salesforce", "jira", "gcal", "gmail", "slack",
    "snowflake", "bigquery", "databricks", "postgres",
    "mulesoft", "github", "sf-cli",
}

VALID_ACTIONS = {
    "creator", "builder", "generator", "viewer", "guide",
    "tracker", "auditor", "architect", "applier", "manager",
    "workflow", "orchestrator", "validator", "prototyper",
    "publisher",
}

BLOCKLIST_TOKENS = {
    "tool", "helper", "utility", "assistant", "smart", "ai", "pro",
    "v2", "new", "my", "custom",
}

# --- Keywords → dimensión --------------------------------------------------

AREA_KEYWORDS: dict[str, list[str]] = {
    "crm": ["sales cloud", "service cloud", "crm", "opportunity", "oportunidad",
            "account", "cuenta", "contact", "contacto", "lead", "case", "caso"],
    "cg-cloud": ["consumer goods", "cg cloud", "retail execution", "visit job",
                 "tactic", "penny perfect", "promotion", "cgcloud"],
    "data-cloud": ["data cloud", "cdp", "customer data platform"],
    "marketing-cloud": ["marketing cloud", "account engagement", "pardot",
                        "journey builder", "email studio"],
    "integrations": ["mulesoft", "integración", "api integration", "middleware",
                     "webhook", "event-driven"],
    "devops": ["release", "ci/cd", "pipeline", "deployment", "sf-cli", "sfdx",
               "sandbox", "production push"],
    "data": ["sql", "snowflake", "bigquery", "databricks", "warehouse",
             "analytics", "dashboard", "métrica", "metric", "etl"],
    "delivery": ["proyecto", "pmo", "sprint", "worklog", "timesheet",
                 "retro", "estimación", "jira"],
    "admin-interno": ["procontacto", "adr", "brand", "marca", "manual",
                      "interno", "gobernanza", "política"],
    "meta": ["skill", "memory", "memoria", "schedule", "setup", "briefing",
             "claude", "cowork"],
}

SYSTEM_KEYWORDS: dict[str, list[str]] = {
    "salesforce": ["salesforce", " sf ", "apex", "soql", "sobject", "lightning",
                   "picklist", "record type", "validation rule", "sharing rule",
                   "permission set", "lwc"],
    "jira": ["jira", "atlassian"],
    "gcal": ["google calendar", "gcal"],
    "gmail": ["gmail", "email", "correo"],
    "slack": ["slack"],
    "snowflake": ["snowflake"],
    "bigquery": ["bigquery"],
    "databricks": ["databricks"],
    "postgres": ["postgres", "postgresql"],
    "mulesoft": ["mulesoft"],
    "github": ["github"],
    "sf-cli": ["sf cli", "sfdx", "salesforce cli"],
}

OBJECT_KEYWORDS: dict[str, list[str]] = {
    "field":       ["field", "campo", "fields", "campos"],
    "user":        ["user", "usuario", "users", "usuarios"],
    "opportunity": ["opportunity", "oportunidad"],
    "account":     ["account", "cuenta"],
    "contact":     ["contact", "contacto"],
    "case":        ["case", "caso"],
    "lead":        ["lead"],
    "flow":        ["flow"],
    "perm":        ["permiso", "permisos", "permission", "permissions"],
    "record":      ["record", "registro"],
    "worklog":     ["worklog", "horas", "timesheet"],
    "issue":       ["issue", "ticket", "tarea"],
    "adr":         ["adr", "decisión", "decision record"],
    "brand":       ["brand", "marca", "identidad"],
    "briefing":    ["briefing", "resumen", "morning"],
    "skill":       ["skill", "catálogo", "catalog"],
    "lwc":         ["lwc", "lightning web component"],
    "apex":        ["apex", "clase apex", "trigger"],
    "visit-job":   ["visit job", "visita programada"],
    "tactic":      ["tactic", "táctica"],
    "promotion":   ["promotion", "promoción"],
    "order":       ["order", "pedido", "orden"],
    "product":     ["product", "producto"],
    "territory":   ["territory", "territorio", "org unit"],
}

ACTION_KEYWORDS: dict[str, list[str]] = {
    "creator":    ["crear", "create", "alta", "nuevo registro", "generar registro"],
    "builder":    ["armar", "build", "construir", "configurar", "scaffold"],
    "generator":  ["generar", "generate", "producir", "redactar"],
    "viewer":     ["ver", "visualizar", "mostrar", "inspect", "view"],
    "guide":      ["guía", "guide", "referencia", "documentar", "explicar"],
    "tracker":    ["trackear", "log", "worklog", "seguimiento", "registrar horas"],
    "auditor":    ["auditar", "audit", "validar conformidad", "revisar estándar"],
    "architect":  ["arquitectura", "architect", "diseñar modelo"],
    "applier":    ["aplicar", "apply", "estilar", "brandear"],
    "manager":    ["gestionar", "administrar", "orquestar dominio", "manage"],
    "workflow":   ["workflow", "flujo paso a paso", "orquestar pasos"],
    "orchestrator": ["orchestrator", "coordinar sistemas"],
    "validator":  ["validar", "validate", "chequear"],
    "prototyper": ["prototipo", "mockup", "prototype", "wireframe"],
    "publisher":  ["publicar", "publish", "compartir por link", "versionar entregable"],
}

# --- Modelos ---------------------------------------------------------------

@dataclass
class NameProposal:
    name: str
    confidence: str  # "high" | "medium" | "low"
    rationale: str
    warnings: list[str] = field(default_factory=list)


META_PREFIX_RE = re.compile(
    r"^\s*"
    # Cero o más palabras de framing: quiero/necesito/estoy/armar/hacer/crear/etc.,
    # cada una seguida opcionalmente de un/una.
    r"(?:(?:quiero|necesito|estoy|armar|armando|hacer|haciendo|crear|creando|construir|construyendo|generar|generando)"
    r"\s+(?:un\s+|una\s+|el\s+|la\s+)?)*"
    r"skill\s+(?:para|que|de|sobre)\s+",
    re.IGNORECASE,
)


def strip_meta_framing(text: str) -> str:
    """Quita frases de meta-lenguaje ('quiero un skill para X') que contaminan el scoring.
    Deja sólo el contenido real que describe qué hace el skill."""
    return META_PREFIX_RE.sub("", text, count=1)


def score_keywords(text: str, mapping: dict[str, list[str]]) -> list[tuple[str, int]]:
    """Cuenta matches con word-boundaries para evitar falsos positivos por substring
    (ej: 'contacto' matcheando dentro de 'procontacto')."""
    text_low = text.lower()
    scores: list[tuple[str, int]] = []
    for key, kws in mapping.items():
        hits = 0
        for kw in kws:
            # Para frases multi-palabra, substring alcanza (son suficientemente específicas).
            # Para palabras sueltas, exigir boundary.
            if " " in kw:
                if kw in text_low:
                    hits += 1
            else:
                # \b asegura que "contact" no matchee dentro de "procontacto".
                # s?/es? captura plurales básicos ES/EN ("oportunidades", "tactics").
                if re.search(rf"\b{re.escape(kw)}(?:es|s)?\b", text_low):
                    hits += 1
        if hits > 0:
            scores.append((key, hits))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def build_name(area: str, system: str | None, obj: str, action: str) -> str:
    parts = ["pc", area]
    if system and area not in AREAS_OMIT_SYSTEM:
        parts.append(system)
    parts.extend([obj, action])
    return "-".join(parts)


def propose(description: str) -> list[NameProposal]:
    # Quitamos "quiero un skill para...", "armar un skill que...", etc.,
    # para que no contaminen el scoring de área=meta / objeto=skill.
    content = strip_meta_framing(description)
    areas = score_keywords(content, AREA_KEYWORDS)
    systems = score_keywords(content, SYSTEM_KEYWORDS)
    objects = score_keywords(content, OBJECT_KEYWORDS)
    actions = score_keywords(content, ACTION_KEYWORDS)

    proposals: list[NameProposal] = []

    if not areas:
        proposals.append(NameProposal(
            name="<incierto>",
            confidence="low",
            rationale=(
                "No detecté un área/práctica en la descripción. "
                "¿Es CRM, CG Cloud, data, delivery, admin-interno, meta? "
                "Pide clarificación al usuario antes de proponer nombre."
            ),
            warnings=["sin área detectable"],
        ))
        return proposals

    if not actions:
        proposals.append(NameProposal(
            name="<incierto>",
            confidence="low",
            rationale=(
                "Detecté área pero no una acción clara. "
                "¿El skill crea, genera, valida, visualiza, guía, audita? "
                "Pide clarificación al usuario."
            ),
            warnings=["sin acción detectable"],
        ))
        return proposals

    if not objects:
        proposals.append(NameProposal(
            name="<incierto>",
            confidence="low",
            rationale=(
                "Detecté área y acción pero no un objeto/entidad concreta. "
                "¿Sobre qué entidad opera el skill? (user, field, opportunity, etc.)"
            ),
            warnings=["sin objeto detectable"],
        ))
        return proposals

    top_area = areas[0][0]
    top_action = actions[0][0]
    top_object = objects[0][0]
    top_system: str | None = None

    # Preferencias de sistema dentro de áreas: el sistema "destino" del skill
    # gana frente a sistemas "fuente" (ej: CRM → Salesforce aunque Gmail sea origen).
    AREA_PREFERRED_SYSTEM = {
        "crm": "salesforce",
        "devops": "sf-cli",
        "integrations": "mulesoft",
    }

    if top_area not in AREAS_OMIT_SYSTEM and systems:
        preferred = AREA_PREFERRED_SYSTEM.get(top_area)
        detected_names = {s[0] for s in systems}
        if preferred and preferred in detected_names:
            top_system = preferred
        else:
            top_system = systems[0][0]

    primary = build_name(top_area, top_system, top_object, top_action)
    confidence = "high"
    rationale_bits = [
        f"área: {top_area} (matches: {areas[0][1]})",
        f"objeto: {top_object} (matches: {objects[0][1]})",
        f"acción: {top_action} (matches: {actions[0][1]})",
    ]
    if top_system:
        rationale_bits.insert(1, f"sistema: {top_system} (matches: {systems[0][1]})")
    elif top_area in AREAS_OMIT_SYSTEM:
        rationale_bits.insert(1, f"sistema: omitido (área '{top_area}' lo implica)")
    else:
        rationale_bits.insert(1, "sistema: no detectado (skill sin sistema externo)")
        confidence = "medium"

    proposals.append(NameProposal(
        name=primary,
        confidence=confidence,
        rationale=" · ".join(rationale_bits),
    ))

    # Alternativa 1: si hay segunda acción con peso similar (posible manager paraguas)
    if len(actions) > 1 and actions[1][1] >= actions[0][1]:
        alt_action = actions[1][0]
        alt_name = build_name(top_area, top_system, top_object, alt_action)
        proposals.append(NameProposal(
            name=alt_name,
            confidence="medium",
            rationale=(
                f"Alternativa con acción '{alt_action}' (empate con '{top_action}'). "
                "Si el skill hace múltiples operaciones sobre el mismo objeto, "
                "considerá acción paraguas: 'manager', 'workflow' u 'orchestrator'."
            ),
        ))

    # Alternativa 2: acción paraguas si hay varias acciones detectadas
    if len(actions) >= 2 and top_action != "manager":
        umbrella_name = build_name(top_area, top_system, top_object, "manager")
        proposals.append(NameProposal(
            name=umbrella_name,
            confidence="medium",
            rationale=(
                f"Se detectaron varias acciones ({[a[0] for a in actions]}). "
                "Si el skill hace más de una cosa sobre el mismo objeto, "
                "usar 'manager' como acción paraguas evita concatenar verbos."
            ),
        ))

    # Alternativa 3: segundo sistema con peso similar
    if top_area not in AREAS_OMIT_SYSTEM and len(systems) > 1 and systems[1][1] >= systems[0][1]:
        alt_system = systems[1][0]
        alt_name = build_name(top_area, alt_system, top_object, top_action)
        proposals.append(NameProposal(
            name=alt_name,
            confidence="medium",
            rationale=(
                f"El sistema dominante podría ser '{alt_system}' "
                f"(empate con '{top_system}'). Elegir según identidad del skill — "
                "los otros sistemas van como dependencias, no en el nombre."
            ),
        ))

    # Warnings globales
    for proposal in proposals:
        tokens = set(proposal.name.split("-"))
        offenders = tokens & BLOCKLIST_TOKENS
        if offenders:
            proposal.warnings.append(f"token(s) prohibido(s): {sorted(offenders)}")
        if len(proposal.name.split("-")) > 6:
            proposal.warnings.append("nombre muy largo (> 6 tokens) — considerar simplificar")

    return proposals


def main() -> int:
    ap = argparse.ArgumentParser(description="Propone nombre normalizado de skill.")
    ap.add_argument("description", nargs="+", help="Descripción libre del skill.")
    ap.add_argument("--json", action="store_true", help="Output JSON en lugar de texto.")
    args = ap.parse_args()

    description = " ".join(args.description)
    proposals = propose(description)

    if args.json:
        payload: dict[str, Any] = {
            "input": description,
            "proposals": [
                {
                    "name": p.name,
                    "confidence": p.confidence,
                    "rationale": p.rationale,
                    "warnings": p.warnings,
                }
                for p in proposals
            ],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"Input: {description}\n")
        for i, p in enumerate(proposals, 1):
            tag = "PRIMARIO" if i == 1 else f"ALTERNATIVA {i-1}"
            print(f"[{tag}] {p.name}")
            print(f"  confianza: {p.confidence}")
            print(f"  razón: {p.rationale}")
            if p.warnings:
                print(f"  warnings: {p.warnings}")
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
