#!/usr/bin/env python3
"""
audit_catalog.py — Escanea un directorio de skills y produce:
  --mode audit   → lista de hallazgos contra las reglas de audit-checklist.md
  --mode catalog → inventario con las dimensiones de taxonomy.md

Convención de nombres aplicada:
  pc-[área]-[sistema]-[objeto]-[acción]

Uso:
    python3 audit_catalog.py --skills-dir /path/to/skills --mode audit   --output audit.json
    python3 audit_catalog.py --skills-dir /path/to/skills --mode catalog --output catalog.json

Diseño:
- Idempotente: misma entrada → mismo output.
- No modifica skills. Solo lee SKILL.md y propone.
- Las reglas están hardcodeadas pero documentadas 1:1 con audit-checklist.md.
"""
# Difiere la evaluación de los type hints (PEP 563): permite usar `str | None`,
# `set[str]`, etc. también en Python 3.7/3.8, no sólo 3.10+.
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # PyYAML — para parser robusto
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

# --- Configuración de la convención ---------------------------------------

# Prefijo obligatorio para skills de ProContacto.
PC_PREFIX = "pc"

# Áreas válidas. Algunas son multi-palabra (usan kebab internamente).
VALID_AREAS = {
    "crm", "cg-cloud", "data-cloud", "marketing-cloud",
    "marketing", "integrations", "devops", "data", "delivery",
    "admin-interno", "meta", "legal",
}

# Áreas donde el sistema se OMITE del nombre porque ya está implícito
# (el área sólo tiene sentido dentro de ese sistema) o porque no hay sistema externo.
AREAS_OMIT_SYSTEM = {
    "cg-cloud", "data-cloud", "marketing-cloud",
    "admin-interno", "meta",
}

# Sistemas externos válidos cuando el slot aplica.
VALID_SYSTEMS = {
    "salesforce", "jira", "gcal", "gmail", "slack",
    "snowflake", "bigquery", "databricks", "postgres",
    "mulesoft", "github", "sf-cli",
}

# Acciones válidas (una sola por skill).
VALID_ACTIONS = {
    "creator", "builder", "generator", "viewer", "guide",
    "tracker", "auditor", "architect", "applier", "manager",
    "workflow", "orchestrator", "validator", "prototyper",
    "publisher",
}

BLOCKLIST_TOKENS = {
    "tool", "helper", "utility", "assistant", "smart",
    "ai", "pro", "v2", "new", "my", "custom",
}

# Skills externos que NO se auditan con reglas ProContacto.
EXTERNAL_SKILLS = {
    "docx", "pptx", "pdf", "xlsx",
    "skill-creator", "consolidate-memory", "schedule", "setup-cowork",
}

# --- Q09 · detector de voseo ----------------------------------------------
# Reusa el mapa curado voseo→neutro (fuente única: voseo_map.py). Best-effort:
# reporta candidatos; el humano confirma. Las líneas que hablan DE dialectos
# (política/ejemplos) no cuentan — el voseo ahí es contenido, no medio.
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from voseo_map import build_map as _voseo_map, PHRASES as _voseo_ph, PRONOUN as _voseo_pr
    # Mismo guard por línea que el fixer (dialecto-como-contenido + plantillas de
    # 1ª persona con pretérito -í/-é) → detector y fixer coinciden exactamente.
    from neutralize_voseo import PROTECT_LINE_RE as VOSEO_PROTECT_RE
    _VOSEO_KEYS = sorted({*_voseo_map(), *_voseo_ph, *_voseo_pr}, key=len, reverse=True)
    _WC = r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ_]"
    VOSEO_RE: re.Pattern[str] | None = re.compile(
        rf"(?<!{_WC})(" + "|".join(re.escape(k) for k in _VOSEO_KEYS) + rf")(?!{_WC})",
        re.IGNORECASE,
    )
except Exception:  # noqa: BLE001 — si falta el mapa, Q09 queda inerte
    VOSEO_RE = None
    VOSEO_PROTECT_RE = re.compile(r"voseo|rioplatense|tuteo", re.IGNORECASE)

# --- Modelos --------------------------------------------------------------

@dataclass
class NameParts:
    raw: str
    pc_prefix: str | None = None
    area: str | None = None
    system: str | None = None
    object_tokens: list[str] = field(default_factory=list)
    action: str | None = None
    valid: bool = False
    error: str | None = None

    @property
    def object(self) -> str | None:
        return "-".join(self.object_tokens) if self.object_tokens else None


@dataclass
class Finding:
    rule_id: str
    type: str
    severity: str
    skill: str
    description: str
    suggested_fix: str
    proposed_new_value: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class SkillEntry:
    name: str
    directory_name: str
    path: str
    description: str
    origin: str  # "procontacto" | "external"
    # Parseo estructural del nombre
    name_parts: dict[str, Any] = field(default_factory=dict)
    # Dimensiones inferidas (best-effort)
    inferred_systems: list[str] = field(default_factory=list)
    language: str = "unknown"  # es | en | bi | unknown
    char_count_description: int = 0
    trigger_phrase_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# --- Parsing de SKILL.md --------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Devuelve (frontmatter_dict, body).

    Usa PyYAML si está disponible (permite dicts anidados como `metadata:`).
    Fallback: parser naive que sólo maneja keys planas.
    """
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}, content
    raw = match.group(1)
    body = content[match.end():]

    if _HAS_YAML:
        try:
            loaded = yaml.safe_load(raw)
            if isinstance(loaded, dict):
                return loaded, body
        except yaml.YAMLError:
            pass  # cae al fallback

    # Fallback: parser plano (no maneja metadata anidado)
    fm: dict[str, Any] = {}
    lines = raw.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        if value in (">", "|"):
            i += 1
            collected: list[str] = []
            while i < len(lines) and (lines[i].startswith("  ") or lines[i] == ""):
                collected.append(lines[i].strip())
                i += 1
            fm[key] = " ".join(s for s in collected if s)
            continue
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        fm[key] = value
        i += 1
    return fm, body


def count_trigger_phrases(description: str) -> int:
    """Cuenta frases entre comillas dobles o simples — proxy de frases disparadoras."""
    double = re.findall(r'"([^"]{3,})"', description)
    single = re.findall(r"'([^']{3,})'", description)
    return len(double) + len(single)


def infer_language(description: str) -> str:
    desc_low = description.lower()
    has_es = bool(re.search(r"\b(activar|cuando|usuario|crea|genera|guía|español)\b", desc_low))
    has_en = bool(re.search(r"\b(when|user|create|generate|guide|english)\b", desc_low))
    if has_es and has_en:
        return "bi"
    if has_es:
        return "es"
    if has_en:
        return "en"
    return "unknown"


def infer_systems(name: str, description: str) -> list[str]:
    systems: list[str] = []
    hay = f"{name} {description}".lower()
    if re.search(r"\bsalesforce\b|\bsf[-_ ]|apex|lwc|soql|sobject", hay):
        systems.append("salesforce")
    if re.search(r"\bjira\b|atlassian|worklog", hay):
        systems.append("jira")
    if re.search(r"google\s*calendar|gcal", hay):
        systems.append("gcal")
    if re.search(r"\bgmail\b", hay):
        systems.append("gmail")
    if re.search(r"\bslack\b", hay):
        systems.append("slack")
    if re.search(r"\.docx|\.pptx|\.pdf|\.xlsx|powerpoint|word document", hay):
        systems.append("ms-office")
    return systems


def parse_name(name: str) -> NameParts:
    """Parsea un nombre según la fórmula pc-[área]-[sistema?]-[objeto]-[acción].

    Algoritmo:
      1. Primer token debe ser 'pc'.
      2. Área: busca match greedy entre las áreas válidas (pueden ser multi-palabra).
      3. Sistema: opcional. Si el siguiente token matchea un VALID_SYSTEMS y el área
         NO está en AREAS_OMIT_SYSTEM, se consume como sistema.
      4. Acción: último token, debe estar en VALID_ACTIONS.
      5. Objeto: lo que queda en el medio (al menos 1 token).
    """
    parts = NameParts(raw=name)
    tokens = name.split("-")
    if len(tokens) < 4:
        parts.error = f"El nombre '{name}' tiene menos de 4 tokens (mínimo pc-área-objeto-acción)."
        return parts

    # 1. Prefijo pc-
    if tokens[0] != PC_PREFIX:
        parts.error = f"El nombre no empieza con '{PC_PREFIX}-'."
        return parts
    parts.pc_prefix = tokens[0]
    cursor = 1

    # 2. Área (greedy multi-palabra)
    area_match: str | None = None
    # Probar matches de 2 tokens primero (ej: cg-cloud), luego 1
    for length in (2, 1):
        candidate = "-".join(tokens[cursor:cursor + length])
        if candidate in VALID_AREAS:
            area_match = candidate
            cursor += length
            break
    if area_match is None:
        parts.error = (
            f"No se reconoció un área válida después de 'pc-'. "
            f"Áreas válidas: {sorted(VALID_AREAS)}."
        )
        return parts
    parts.area = area_match

    # 3. Sistema (opcional)
    if cursor < len(tokens):
        # Probar tokens multi-palabra primero (sf-cli) luego single
        for length in (2, 1):
            if cursor + length > len(tokens):
                continue
            candidate = "-".join(tokens[cursor:cursor + length])
            if candidate in VALID_SYSTEMS:
                if parts.area in AREAS_OMIT_SYSTEM:
                    parts.error = (
                        f"El área '{parts.area}' no debe incluir sistema en el nombre "
                        f"(está en AREAS_OMIT_SYSTEM). Se encontró '{candidate}'."
                    )
                    return parts
                parts.system = candidate
                cursor += length
                break

    # 4. Acción (último token)
    if tokens[-1] not in VALID_ACTIONS:
        parts.error = (
            f"El último token '{tokens[-1]}' no es una acción válida. "
            f"Acciones válidas: {sorted(VALID_ACTIONS)}."
        )
        return parts
    parts.action = tokens[-1]

    # 5. Objeto = lo que queda entre cursor y antes de la acción
    object_tokens = tokens[cursor:-1]
    if not object_tokens:
        parts.error = "Falta el slot de objeto entre área/sistema y acción."
        return parts
    parts.object_tokens = object_tokens

    parts.valid = True
    return parts


# --- Reglas de audit ------------------------------------------------------

def check_name_directory_match(skill: SkillEntry, fm_name: str) -> Finding | None:
    if fm_name and fm_name != skill.directory_name:
        return Finding(
            rule_id="N01",
            type="naming",
            severity="high",
            skill=skill.directory_name,
            description=(
                f"El campo `name` en frontmatter ('{fm_name}') no coincide con el nombre "
                f"del directorio ('{skill.directory_name}')."
            ),
            suggested_fix=(
                f"Cambiar el `name` del frontmatter a '{skill.directory_name}' "
                "(kebab-case, sin Title Case)."
            ),
            proposed_new_value=skill.directory_name,
        )
    return None


def check_name_structure(skill: SkillEntry) -> list[Finding]:
    findings: list[Finding] = []
    name = skill.directory_name
    parts = parse_name(name)

    # N02a: debe empezar con pc-
    if parts.pc_prefix != PC_PREFIX:
        findings.append(Finding(
            rule_id="N02",
            type="naming",
            severity="high",
            skill=name,
            description=(
                f"El nombre '{name}' no empieza con el prefijo obligatorio 'pc-'. "
                "Todos los skills propios de ProContacto deben empezar con pc-."
            ),
            suggested_fix=(
                "Renombrar el directorio anteponiendo 'pc-'. Formato completo: "
                "pc-[área]-[sistema?]-[objeto]-[acción]."
            ),
        ))

    # N02b: área válida
    if parts.area is None and parts.pc_prefix == PC_PREFIX:
        findings.append(Finding(
            rule_id="N02",
            type="naming",
            severity="high",
            skill=name,
            description=(
                f"No se reconoció un área válida después de 'pc-' en '{name}'. "
                f"Áreas permitidas: {sorted(VALID_AREAS)}."
            ),
            suggested_fix=(
                "Insertar un área válida como segundo slot. Ver la tabla de áreas "
                "en references/naming-convention.md."
            ),
        ))

    # N02c: acción válida al final
    if parts.action is None and parts.area is not None:
        findings.append(Finding(
            rule_id="N02",
            type="naming",
            severity="medium",
            skill=name,
            description=(
                f"El nombre '{name}' no termina con una acción válida. "
                f"Acciones permitidas: {sorted(VALID_ACTIONS)}."
            ),
            suggested_fix=(
                "Agregar un verbo de acción al final. Si el skill hace muchas cosas "
                "sobre el mismo objeto, usar acción paraguas (manager, workflow, orchestrator)."
            ),
        ))

    # N03a: sistema presente cuando el área lo prohíbe
    if parts.error and "AREAS_OMIT_SYSTEM" in (parts.error or ""):
        findings.append(Finding(
            rule_id="N03",
            type="naming",
            severity="medium",
            skill=name,
            description=parts.error or "",
            suggested_fix=(
                f"Quitar el slot de sistema — el área '{parts.area}' ya lo implica."
            ),
        ))

    # N03b: objeto faltante
    if parts.area is not None and parts.action is not None and not parts.object_tokens:
        findings.append(Finding(
            rule_id="N03",
            type="naming",
            severity="medium",
            skill=name,
            description=f"Falta el slot de objeto en '{name}'.",
            suggested_fix="Insertar un sustantivo que identifique la entidad sobre la que opera el skill.",
        ))

    # N04: blocklist
    for token in name.split("-"):
        if token in BLOCKLIST_TOKENS:
            findings.append(Finding(
                rule_id="N04",
                type="naming",
                severity="medium",
                skill=name,
                description=f"El nombre contiene el token prohibido '{token}'.",
                suggested_fix=f"Eliminar '{token}' del nombre — es demasiado genérico.",
            ))

    # N05: parse error genérico no cubierto arriba
    if parts.error and parts.pc_prefix == PC_PREFIX and parts.area is not None:
        already_covered = (
            "AREAS_OMIT_SYSTEM" in parts.error
            or "Falta el slot de objeto" in parts.error
            or "no es una acción válida" in parts.error
        )
        if not already_covered:
            findings.append(Finding(
                rule_id="N05",
                type="naming",
                severity="low",
                skill=name,
                description=parts.error,
                suggested_fix="Revisar estructura del nombre contra naming-convention.md.",
            ))

    return findings


def check_description(skill: SkillEntry) -> list[Finding]:
    findings: list[Finding] = []
    desc = skill.description

    if skill.char_count_description < 300:
        findings.append(Finding(
            rule_id="D01",
            type="description",
            severity="high",
            skill=skill.directory_name,
            description=(
                f"La description tiene {skill.char_count_description} caracteres "
                "(mínimo recomendado: 300). Descriptions cortas no triggerean."
            ),
            suggested_fix=(
                "Expandir la description con: (1) verbo activo inicial, "
                "(2) al menos 5 frases disparadoras entre comillas, "
                "(3) contexto de uso y sistemas involucrados."
            ),
        ))

    # D04 — techo duro del validador de Anthropic (skill-creator). BLOQUEANTE:
    # arriba de 1024 caracteres el skill no se puede empaquetar ni modificar.
    if skill.char_count_description > 1024:
        findings.append(Finding(
            rule_id="D04",
            type="description",
            severity="high",
            skill=skill.directory_name,
            description=(
                f"La description tiene {skill.char_count_description} caracteres y "
                "supera el limite duro de 1024 del validador de Anthropic. El skill "
                "no se puede crear, empaquetar ni modificar hasta acortarla."
            ),
            suggested_fix=(
                f"Recortar {skill.char_count_description - 1024} caracteres. "
                "Dejar en la description 1 oracion de que hace + 5-8 frases "
                "disparadoras clave; mover workflow, sistemas y reglas al cuerpo "
                "del SKILL.md (que no tiene limite)."
            ),
        ))
    elif skill.char_count_description > 950:
        findings.append(Finding(
            rule_id="D04",
            type="description",
            severity="low",
            skill=skill.directory_name,
            description=(
                f"La description tiene {skill.char_count_description} caracteres, "
                "cerca del techo de 1024. Riesgo de cruzarlo en la proxima edicion."
            ),
            suggested_fix="Dejar margen: apuntar a 700-900 caracteres.",
        ))

    if skill.trigger_phrase_count < 5:
        findings.append(Finding(
            rule_id="D02",
            type="description",
            severity="medium",
            skill=skill.directory_name,
            description=(
                f"La description incluye {skill.trigger_phrase_count} frases entre "
                "comillas (mínimo: 5). Las frases disparadoras son lo que mejor "
                "matchea intenciones reales."
            ),
            suggested_fix=(
                'Agregar al menos 5 frases literales que un usuario diría, entre '
                'comillas dobles. Ejemplo: "quiero cargar horas", "registrar worklog".'
            ),
        ))

    if desc:
        first_word_match = re.match(r"^\s*(\w+)", desc)
        if first_word_match:
            first = first_word_match.group(1).lower()
            active_verbs = {
                "crea", "genera", "audita", "aplica", "permite", "guía", "guia",
                "construye", "valida", "muestra", "registra", "gobierna", "orquesta",
                "diseña", "produce", "escanea", "propone",
                "creates", "generates", "audits", "applies", "allows", "guides",
                "builds", "validates", "shows", "tracks", "designs",
            }
            if first not in active_verbs:
                findings.append(Finding(
                    rule_id="D03",
                    type="description",
                    severity="low",
                    skill=skill.directory_name,
                    description=(
                        f"La description empieza con '{first}', que no es un verbo activo."
                    ),
                    suggested_fix="Reformular para empezar con un verbo en presente.",
                ))

    return findings


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
ISODATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def check_metadata(skill: SkillEntry, fm: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    if "name" not in fm:
        findings.append(Finding(
            rule_id="M02", type="metadata", severity="high",
            skill=skill.directory_name,
            description="Falta el campo `name` en el frontmatter.",
            suggested_fix=f"Agregar `name: {skill.directory_name}` al frontmatter.",
        ))
    if "description" not in fm:
        findings.append(Finding(
            rule_id="M02", type="metadata", severity="high",
            skill=skill.directory_name,
            description="Falta el campo `description` en el frontmatter.",
            suggested_fix="Agregar una description siguiendo la plantilla de naming-convention.md.",
        ))
    # Set permitido por el validador del skill-creator de Anthropic. `metadata`
    # es el slot oficial para extensiones custom (incluye version/last_modified).
    allowed = {"name", "description", "compatibility", "metadata", "license", "allowed-tools"}
    unknown = set(fm.keys()) - allowed
    if unknown:
        findings.append(Finding(
            rule_id="M03", type="metadata", severity="low",
            skill=skill.directory_name,
            description=f"Frontmatter contiene campos desconocidos: {sorted(unknown)}.",
            suggested_fix=(
                f"Remover o mover a `metadata:`: {sorted(unknown)}. "
                "El validador sólo acepta: name, description, compatibility, metadata, "
                "license, allowed-tools."
            ),
        ))
    # Versioning vive dentro de metadata.* para no chocar con el validador.
    md = fm.get("metadata") or {}
    if not isinstance(md, dict):
        md = {}
    # V01 — metadata.version
    version = str(md.get("version", "")).strip()
    if not version:
        findings.append(Finding(
            rule_id="V01", type="versioning", severity="medium",
            skill=skill.directory_name,
            description="Falta `metadata.version` en el frontmatter.",
            suggested_fix="Agregar bajo `metadata:` el campo `version: 1.0.0` (publicado) o `0.1.0` (desarrollo).",
        ))
    elif not SEMVER_RE.match(version):
        findings.append(Finding(
            rule_id="V01", type="versioning", severity="medium",
            skill=skill.directory_name,
            description=f"`metadata.version: {version}` no está en formato SemVer MAJOR.MINOR.PATCH.",
            suggested_fix="Corregir al formato `X.Y.Z` con enteros no negativos (ej: 1.2.3).",
        ))
    # V02 — metadata.last_modified
    lm = str(md.get("last_modified", "")).strip()
    if not lm:
        findings.append(Finding(
            rule_id="V02", type="versioning", severity="medium",
            skill=skill.directory_name,
            description="Falta `metadata.last_modified` en el frontmatter.",
            suggested_fix="Agregar bajo `metadata:` el campo `last_modified: YYYY-MM-DD` con la fecha del último cambio.",
        ))
    elif not ISODATE_RE.match(lm):
        findings.append(Finding(
            rule_id="V02", type="versioning", severity="medium",
            skill=skill.directory_name,
            description=f"`metadata.last_modified: {lm}` no está en formato ISO 8601 (YYYY-MM-DD).",
            suggested_fix="Corregir al formato `YYYY-MM-DD` (ej: 2026-04-23).",
        ))
    else:
        # Sanity check: no futuro, no anterior a 2025-01-01
        try:
            parsed = datetime.strptime(lm, "%Y-%m-%d").date()
            today = datetime.now(timezone.utc).date()
            if parsed > today:
                findings.append(Finding(
                    rule_id="V02", type="versioning", severity="low",
                    skill=skill.directory_name,
                    description=f"`metadata.last_modified: {lm}` está en el futuro (hoy: {today}).",
                    suggested_fix="Ajustar a una fecha real de modificación.",
                ))
            elif parsed < datetime(2025, 1, 1).date():
                findings.append(Finding(
                    rule_id="V02", type="versioning", severity="low",
                    skill=skill.directory_name,
                    description=f"`metadata.last_modified: {lm}` es anterior a 2025-01-01 — sospechoso.",
                    suggested_fix="Verificar la fecha. Si el skill fue tocado recientemente, actualizarla.",
                ))
        except ValueError:
            pass
    return findings


def check_duplicates(skills: list[SkillEntry]) -> list[Finding]:
    """DUP01/DUP02 — solapamientos entre skills."""
    findings: list[Finding] = []

    trigger_map: dict[str, list[str]] = {}
    for s in skills:
        phrases = set(re.findall(r'"([^"]{3,})"', s.description))
        phrases |= set(re.findall(r"'([^']{3,})'", s.description))
        for p in phrases:
            trigger_map.setdefault(p.lower(), []).append(s.directory_name)

    seen_pairs: set[tuple[str, str]] = set()
    for phrase, owners in trigger_map.items():
        if len(owners) > 1:
            for i in range(len(owners)):
                for j in range(i + 1, len(owners)):
                    pair = tuple(sorted([owners[i], owners[j]]))
                    if pair in seen_pairs:
                        continue
                    seen_pairs.add(pair)
                    shared = sum(
                        1 for p, o in trigger_map.items()
                        if pair[0] in o and pair[1] in o
                    )
                    if shared >= 3:
                        findings.append(Finding(
                            rule_id="DUP01",
                            type="duplicate",
                            severity="medium",
                            skill=f"{pair[0]} ↔ {pair[1]}",
                            description=(
                                f"Los skills '{pair[0]}' y '{pair[1]}' comparten "
                                f"{shared} frases disparadoras — posible solapamiento."
                            ),
                            suggested_fix=(
                                "Revisar si son realmente distintos. Opciones: "
                                "(a) merge, (b) afinar descriptions para diferenciar, "
                                "(c) aceptar el solapamiento y documentarlo."
                            ),
                        ))
    return findings


# --- Reglas de diseño (Q01–Q11) ------------------------------------------
# Spec completa en references/skill-design-rules.md. El script sólo puede
# chequear (heurísticamente) Q01, Q06, Q07, Q08, Q09 y Q11; las demás las
# evalúa Claude leyendo el skill.

# Extensiones / nombres que cuentan como "template de output" en assets/.
TEMPLATE_EXTS = (
    ".html", ".htm", ".html.j2", ".htm.j2",
    ".jinja", ".jinja2", ".tpl", ".mustache", ".hbs",
)

# Señales fuertes de que el skill produce HTML/artefacto como output.
HTML_OUTPUT_RE = re.compile(
    r"create_artifact|show_widget|mcp__visualize|\.html\b", re.IGNORECASE
)
# Señal débil: la palabra "html" sólo cuenta si co-ocurre con un verbo de salida.
HTML_WORD_RE = re.compile(r"\bhtml\b", re.IGNORECASE)
HTML_VERB_RE = re.compile(
    r"gener|produce|produce|render|reporte|report|dashboard|widget|artifact|entrega|construye",
    re.IGNORECASE,
)

FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
# Nombre de skill plausible: pc- + al menos 3 segmentos (área-objeto-acción).
SKILL_REF_RE = re.compile(r"pc-[a-z0-9]+(?:-[a-z0-9]+){2,}")


def _has_output_template(skill_dir: Path) -> bool:
    """True si assets/ tiene algún archivo que parezca un template de output."""
    assets = skill_dir / "assets"
    if not assets.is_dir():
        return False
    for f in assets.rglob("*"):
        if not f.is_file():
            continue
        low = f.name.lower()
        if "template" in low or any(low.endswith(ext) for ext in TEMPLATE_EXTS):
            return True
    return False


def check_output_template(entry: SkillEntry, body: str) -> list[Finding]:
    """Q01 — si el skill genera HTML como output, debe traer un template en assets/."""
    produces_html = bool(HTML_OUTPUT_RE.search(body)) or (
        bool(HTML_WORD_RE.search(body)) and bool(HTML_VERB_RE.search(body))
    )
    if not produces_html or _has_output_template(Path(entry.path)):
        return []
    return [Finding(
        rule_id="Q01",
        type="design",
        severity="high",
        skill=entry.directory_name,
        description=(
            "El skill parece generar HTML/artifact como output pero no hay ningún "
            "template en assets/ (heurística). El layout se estaría improvisando en "
            "cada ejecución."
        ),
        suggested_fix=(
            "Crear assets/<output>-template.html con placeholders y hacer que el paso "
            "de generación lo rellene, en vez de idear el markup. "
            "Ver Q01 en references/skill-design-rules.md."
        ),
    )]


def check_skill_references(entry: SkillEntry, body: str, known: set[str]) -> list[Finding]:
    """Q06 — las referencias pc-… a otros skills deben existir en el catálogo.

    Escanea la description + el body del SKILL.md sin los bloques de código
    (donde viven los ejemplos ilustrativos). Sólo considera nombres que parsean
    como skill válido, para no flaggear ejemplos de nombres mal formados.
    """
    findings: list[Finding] = []
    text = (entry.description or "") + "\n" + FENCE_RE.sub("", body)
    for ref in dict.fromkeys(SKILL_REF_RE.findall(text)):  # únicos, orden estable
        if ref in (entry.directory_name, entry.name):
            continue  # auto-referencia
        if not parse_name(ref).valid:
            continue  # ejemplo de nombre inválido / placeholder, no una referencia real
        if ref in known:
            continue
        findings.append(Finding(
            rule_id="Q06",
            type="design",
            severity="high",
            skill=entry.directory_name,
            description=(
                f"El SKILL.md referencia el skill '{ref}', que no existe en el catálogo "
                "escaneado. Puede ser un typo, un nombre viejo post-rename, o un skill "
                "que vive en otro directorio."
            ),
            suggested_fix=(
                f"Verificar '{ref}'. Si fue renombrado, actualizar la referencia al nombre "
                "vigente; si no existe, quitarla. Ver Q06 en references/skill-design-rules.md."
            ),
        ))
    return findings


# Señal de que el skill escribe registros en un sistema externo.
WRITE_OP_RE = re.compile(
    r"createSobjectRecord|updateSobjectRecord|odoo_create|odoo_write", re.IGNORECASE
)
# Señales de que el skill aplica el contrato de escritura (mapa + gate + verificación).
WRITE_CONTRACT_RE = re.compile(
    r"getObjectSchema|mapa de escritura|contrato de escritura|pre-write|pre-escritura|"
    r"post-write|post-escritura|campos? obligatori|verificaci[oó]n post|re-query",
    re.IGNORECASE,
)


def check_write_contract(entry: SkillEntry, body: str) -> list[Finding]:
    """Q07 — skills que crean/actualizan registros deben declarar mapa de escritura +
    resolver valores a runtime (getObjectSchema) + gate pre-write + verificación post-write.

    Heurística: si el body (sin bloques de código) menciona una operación de escritura
    pero NO aparece ninguna señal del contrato de escritura, se flagea.
    """
    no_fences = FENCE_RE.sub("", body)
    writes = bool(WRITE_OP_RE.search(body))  # la op puede estar en un ejemplo de código
    if not writes:
        return []
    if WRITE_CONTRACT_RE.search(no_fences):
        return []
    return [Finding(
        rule_id="Q07",
        type="design",
        severity="high",
        skill=entry.directory_name,
        description=(
            "El skill crea/actualiza registros en un sistema externo pero no documenta "
            "el contrato de escritura (heurística): no se ve mapa de escritura, ni "
            "resolución de schema/valores con getObjectSchema, ni gate de campos "
            "obligatorios / verificación post-write. Riesgo de crear registros incompletos "
            "(ej. una Opp sin Amount) o de hardcodear picklists."
        ),
        suggested_fix=(
            "Declarar el mapa de escritura por objeto (campos + rol + obligatoriedad "
            "técnica/negocio), resolver valores/API names con getObjectSchema a runtime, "
            "y agregar gate pre-write + verificación post-write. Modelo: "
            "pc-sales-sf-quote-builder (Paso 16.5 + 17.5). Ver Q07 en "
            "references/skill-design-rules.md."
        ),
    )]


# Q08 — interactividad cableada en templates HTML.
# Elemento clickeable en un template (conservador: button / role=button / data-act).
ACTIONABLE_RE = re.compile(
    r"<button\b|role\s*=\s*[\"']button[\"']|data-act(?:ion)?\s*=", re.IGNORECASE
)
# Señal de que hay cableado de acción en el archivo (incluye event delegation).
WIRING_RE = re.compile(r"\bon[a-z]+\s*=|addEventListener|sendPrompt", re.IGNORECASE)
# Placeholder de datos (dato inyectado, no comportamiento).
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}|__[A-Z0-9_]+__")
# Handler inline on*="..." con su valor capturado.
INLINE_HANDLER_RE = re.compile(r"\bon[a-z]+\s*=\s*(\"[^\"]*\"|'[^']*')", re.IGNORECASE)


def _template_html_files(skill_dir: Path) -> list[Path]:
    """Archivos .html/.htm dentro de assets/ (ignora _deprecados)."""
    assets = skill_dir / "assets"
    if not assets.is_dir():
        return []
    out: list[Path] = []
    for f in assets.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in (".html", ".htm"):
            continue
        if any("deprecad" in p.lower() for p in f.parts):
            continue
        out.append(f)
    return out


def check_html_actionability(entry: SkillEntry) -> list[Finding]:
    """Q08 — cada control interactivo de un template HTML debe estar cableado a una
    acción real en el archivo (sendPrompt / href / listener) y el comportamiento no
    puede vivir en placeholders. Heurística estática: reporta candidatos a botón
    muerto; el humano confirma con la prueba de humo de interactividad.
    """
    findings: list[Finding] = []
    for tpl in _template_html_files(Path(entry.path)):
        try:
            text = tpl.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if not ACTIONABLE_RE.search(text):
            continue  # sin controles clickeables → Q08 no aplica a este archivo
        rel = tpl.relative_to(entry.path)
        if not WIRING_RE.search(text):
            findings.append(Finding(
                rule_id="Q08",
                type="design",
                severity="high",
                skill=entry.directory_name,
                description=(
                    f"El template '{rel}' tiene controles clickeables (botones/data-act) "
                    "pero no se ve ningún cableado de acción (onclick / addEventListener / "
                    "sendPrompt) en el archivo. Posibles botones muertos: la acción se "
                    "estaría dejando para improvisar en runtime."
                ),
                suggested_fix=(
                    "Cablear cada control en el template a sendPrompt(prompt completo), "
                    "un href real, o un listener local (preferí event delegation para "
                    "filas dinámicas), y correr la prueba de humo de interactividad. "
                    "Ver Q08 en references/skill-design-rules.md."
                ),
            ))
            continue
        # Comportamiento diferido a runtime: placeholder dentro de un handler inline.
        for m in INLINE_HANDLER_RE.finditer(text):
            if PLACEHOLDER_RE.search(m.group(1)):
                snippet = m.group(0)[:60]
                findings.append(Finding(
                    rule_id="Q08",
                    type="design",
                    severity="high",
                    skill=entry.directory_name,
                    description=(
                        f"El template '{rel}' tiene un handler inline con un placeholder "
                        f"({snippet}…): el comportamiento del control se difiere a runtime "
                        "en vez de estar horneado en el template."
                    ),
                    suggested_fix=(
                        "Los placeholders deben inyectar sólo datos, no comportamiento. "
                        "Escribe la acción fija en el template (sendPrompt/href/listener) y "
                        "construye cualquier variante por fila en JS desde los datos. "
                        "Ver Q08 en references/skill-design-rules.md."
                    ),
                ))
                break  # un hallazgo de este tipo por template basta
    return findings


# --- Q11 · publicación del entregable en el gestor -------------------------
# Vocabulario que distingue un ENTREGABLE (sobrevive a la conversación: alguien lo
# vuelve a abrir, lo comparte o lo corrige) de una pantalla de trabajo.
DELIVERABLE_RE = re.compile(
    r"\bentregable|propuesta|cotizaci[oó]n|\bSOW\b|wireframe|deck|presentaci[oó]n|"
    r"documento|informe|minuta|\bacta\b|diagrama|historias de usuario|"
    r"diccionario de datos|caso de [eé]xito",
    re.IGNORECASE,
)
# Declaración explícita de "esto es una pantalla de trabajo, va al chat". Cuando el
# skill la trae, Q11 NO se le aplica: la instrucción del skill manda.
PANEL_DECLARED_RE = re.compile(
    r"(?:panel|tablero|widget|vista|visor)[^.\n]{0,90}mcp__visualize__show_widget"
    r"|mcp__visualize__show_widget[^.\n]{0,90}(?:nunca|never)\s+"
    r"(?:create_artifact|publicar_artefacto)"
    r"|nunca\s+create_artifact",
    re.IGNORECASE,
)
PUBLISH_CITE_RE = re.compile(r"_shared/artifact-publish", re.IGNORECASE)
# Líneas que hablan *de* la regla en vez de aplicarla (este mismo skill documenta
# Q11, y sin este filtro el chequeo se dispara contra su propia spec). Mismo
# criterio que VOSEO_PROTECT_RE en Q09: el texto ahí es contenido, no conducta.
RULE_META_RE = re.compile(
    r"\bQ11\b|skill-design-rules|audit-checklist|check_artifact_publish"
    r"|reglas de diseño|TARGETS\b",
    re.IGNORECASE,
)


def check_artifact_publish(entry: SkillEntry, body: str) -> list[Finding]:
    """Q11 — todo skill que produce un ENTREGABLE HTML tiene que citar la política
    de publicación (`_shared/artifact-publish/`) y estar en el TARGETS de su sync.sh
    (que es lo que mete el módulo dentro del bundle .skill).

    Las dos mitades fallan distinto y las dos fallan en silencio: sin la cita el
    módulo viaja y nadie lo lee; sin el TARGETS la cita apunta a un archivo que en
    la máquina del usuario no existe.

    No aplica a las pantallas de trabajo del chat. La forma de salir del chequeo es
    DECLARARLO en el SKILL.md (`… via mcp__visualize__show_widget`), no una excepción
    en el script: si el skill no dice a dónde va su output, la decisión queda librada
    a cada corrida, que es justamente el bug.
    """
    lineas = [ln for ln in (entry.description + "\n" + body).split("\n")
              if not RULE_META_RE.search(ln)]
    texto = "\n".join(lineas)
    produce_html = bool(HTML_OUTPUT_RE.search(texto)) or (
        bool(HTML_WORD_RE.search(texto)) and bool(HTML_VERB_RE.search(texto))
    )
    if not produce_html or not DELIVERABLE_RE.search(texto):
        return []
    if PANEL_DECLARED_RE.search(texto):
        return []

    cita = bool(PUBLISH_CITE_RE.search(texto))
    propagado = (Path(entry.path) / "_shared" / "artifact-publish" /
                 "artifact-publish.md").is_file()
    if cita and propagado:
        return []

    if not cita and not propagado:
        falta = ("no cita `_shared/artifact-publish/` ni lo tiene propagado dentro "
                 "del skill")
    elif not cita:
        falta = ("tiene el módulo propagado pero **ningún paso lo invoca**: viaja en "
                 "el bundle y nadie lo lee")
    else:
        falta = ("cita `_shared/artifact-publish/` pero el módulo NO está dentro del "
                 "skill: falta en el TARGETS de sync.sh (o no se corrió), así que el "
                 "bundle .skill deployado no lo lleva")

    return [Finding(
        rule_id="Q11",
        type="design",
        severity="blocking",
        skill=entry.directory_name,
        description=(
            f"Parece producir un entregable HTML y {falta}. Sin la política, el "
            "entregable sale como artefacto de la conversación (sin versionado ni "
            "trazabilidad) o se republica de cero, dejando viejo el link ya "
            "compartido."
        ),
        suggested_fix=(
            "Agregar al SKILL.md la sección de publicación citando "
            "`_shared/artifact-publish/artifact-publish.md` (modelo: "
            "pc-crm-userstory-generator), sumar \"<área>/<skill>\" al TARGETS de "
            "_shared/artifact-publish/sync.sh y correrlo. Si el output es una "
            "pantalla de trabajo y no un entregable, declararlo en el SKILL.md "
            "(\"… via mcp__visualize__show_widget\") y Q11 deja de aplicar. "
            "Ver Q11 en references/skill-design-rules.md."
        ),
    )]


def check_default_dialect(entry: SkillEntry, body: str) -> list[Finding]:
    """Q09 — el registro por defecto del catálogo es español neutro (tuteo). Marca
    skills cuya description/prosa usa voseo rioplatense. Best-effort sobre el mapa
    curado de voseo_map.py. Override: si el skill necesita otro dialecto a propósito
    (salida al cliente por país, registro interno), lo documenta en una línea que
    mencione el dialecto — esas líneas no cuentan (el voseo ahí es contenido).
    """
    if VOSEO_RE is None:
        return []
    counts: Counter = Counter()
    for line in (entry.description + "\n" + body).split("\n"):
        if VOSEO_PROTECT_RE.search(line):
            continue
        for m in VOSEO_RE.finditer(line):
            counts[m.group(0).lower()] += 1
    if not counts:
        return []
    total = sum(counts.values())
    top = ", ".join(f"{tok}×{n}" for tok, n in counts.most_common(8))
    return [Finding(
        rule_id="Q09",
        type="language",
        severity="medium",
        skill=entry.directory_name,
        description=(
            f"Usa voseo rioplatense ({total} formas; ej.: {top}). El registro por "
            "defecto del catálogo es español neutro (tuteo)."
        ),
        suggested_fix=(
            "Neutralizar con scripts/neutralize_voseo.py (mapa curado en voseo_map.py). "
            "Si el skill necesita otro dialecto a propósito (salida al cliente por país, "
            "registro interno), dejarlo documentado en una línea que mencione el dialecto "
            "— el detector respeta esas líneas. Ver Q09 en references/skill-design-rules.md."
        ),
    )]


# --- Catálogo / extracción ------------------------------------------------

def load_skill(skill_dir: Path) -> tuple[SkillEntry, dict[str, str], str] | None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return None
    content = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    name = fm.get("name", skill_dir.name)
    description = fm.get("description", "")
    origin = "external" if skill_dir.name in EXTERNAL_SKILLS else "procontacto"
    parts = parse_name(skill_dir.name)

    entry = SkillEntry(
        name=name,
        directory_name=skill_dir.name,
        path=str(skill_dir),
        description=description,
        origin=origin,
        name_parts={
            "pc_prefix": parts.pc_prefix,
            "area": parts.area,
            "system": parts.system,
            "object": parts.object,
            "action": parts.action,
            "valid": parts.valid,
            "error": parts.error,
        },
        inferred_systems=infer_systems(skill_dir.name, description),
        language=infer_language(description),
        char_count_description=len(description),
        trigger_phrase_count=count_trigger_phrases(description),
    )
    return entry, fm, body


def audit(skills: list[tuple[SkillEntry, dict[str, str], str]]) -> list[Finding]:
    findings: list[Finding] = []
    # Set de skills conocidos para validar referencias cruzadas (Q06).
    known: set[str] = {e.directory_name for e, _, _ in skills}
    known |= {e.name for e, _, _ in skills if e.name}
    known |= EXTERNAL_SKILLS
    for entry, fm, body in skills:
        if entry.origin == "external":
            continue
        findings.extend(check_metadata(entry, fm))
        fm_name = fm.get("name")
        if fm_name:
            f = check_name_directory_match(entry, fm_name)
            if f:
                findings.append(f)
        findings.extend(check_name_structure(entry))
        findings.extend(check_description(entry))
        findings.extend(check_output_template(entry, body))
        findings.extend(check_skill_references(entry, body, known))
        findings.extend(check_write_contract(entry, body))
        findings.extend(check_html_actionability(entry))
        findings.extend(check_default_dialect(entry, body))
        findings.extend(check_artifact_publish(entry, body))

    findings.extend(check_duplicates([e for e, _, _ in skills if e.origin == "procontacto"]))
    return findings


def summarize(findings: list[Finding]) -> dict[str, Any]:
    by_sev: dict[str, int] = {"high": 0, "medium": 0, "low": 0}
    by_type: dict[str, int] = {}
    for f in findings:
        by_sev[f.severity] = by_sev.get(f.severity, 0) + 1
        by_type[f.type] = by_type.get(f.type, 0) + 1
    return {"total": len(findings), "by_severity": by_sev, "by_type": by_type}


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit/catalog ProContacto skills.")
    ap.add_argument("--skills-dir", required=True, help="Directorio que contiene los skills.")
    ap.add_argument("--mode", choices=["audit", "catalog"], default="audit")
    ap.add_argument("--output", help="Archivo de salida JSON. Si se omite, stdout.")
    args = ap.parse_args()

    skills_dir = Path(args.skills_dir)
    if not skills_dir.is_dir():
        print(f"Error: '{skills_dir}' no es un directorio.", file=sys.stderr)
        return 2

    loaded: list[tuple[SkillEntry, dict[str, str], str]] = []
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        result = load_skill(child)
        if result is None:
            continue
        loaded.append(result)

    now = datetime.now(timezone.utc).isoformat()

    if args.mode == "audit":
        findings = audit(loaded)
        payload = {
            "generated_at": now,
            "skills_dir": str(skills_dir),
            "summary": summarize(findings),
            "findings": [f.to_dict() for f in findings],
        }
    else:
        payload = {
            "generated_at": now,
            "skills_dir": str(skills_dir),
            "count": len(loaded),
            "skills": [entry.to_dict() for entry, _, _ in loaded],
        }

    out_text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(out_text, encoding="utf-8")
        print(f"Escrito {args.output} ({len(out_text)} bytes)", file=sys.stderr)
    else:
        print(out_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
