#!/usr/bin/env python3
"""
validate_description.py — Valida que el campo `description` de un skill respete
los límites del validador de Anthropic (skill-creator).

Límites aplicados:
  - HARD LIMIT: description <= 1024 caracteres. Arriba de eso el skill NO se puede
    crear, empaquetar ni modificar (el validador lo rechaza / lo trunca).
  - Piso recomendado ProContacto: >= 300 caracteres (si no, no triggerea bien).
  - Banda de aviso: > 950 caracteres (cerca del techo, conviene dejar margen).

Uso:
    # Desde un SKILL.md (extrae la description del frontmatter):
    python3 validate_description.py --skill-md path/to/SKILL.md

    # Desde un archivo de texto que contiene SOLO la description:
    python3 validate_description.py --file desc.txt

    # Inline:
    python3 validate_description.py "Crea ... cuando el usuario diga ..."

Exit codes:
    0  OK — description <= 1024 (puede avisar por stderr si está corta o al límite)
    1  BLOQUEANTE — description > 1024 (detener el flow de creación/modificación)
    2  Error de uso o no se encontró description

Pensado para:
- Ser invocado por el workflow del skill ANTES de crear/empaquetar un skill,
  como gate bloqueante complementario a validate_name.py.
- Correr en un pre-commit hook o CI sin dependencias externas obligatorias.

Reusa parse_frontmatter() de audit_catalog.py para mantener una única fuente de
verdad sobre cómo se lee el frontmatter (folded scalars, comillas, metadata, etc).
"""
import argparse
import sys
from pathlib import Path

HARD_LIMIT = 1024        # límite del validador de Anthropic
WARN_CEIL = 950          # banda de aviso (cerca del techo)
RECOMMENDED_FLOOR = 300  # piso recomendado ProContacto

# Reusar el parser de frontmatter del hermano audit_catalog.py.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    from audit_catalog import parse_frontmatter  # noqa: E402
except Exception:  # pragma: no cover - fallback si se corre aislado
    import re as _re

    _FM_RE = _re.compile(r"^---\s*\n(.*?)\n---\s*\n", _re.DOTALL)

    def parse_frontmatter(content: str):
        m = _FM_RE.match(content)
        if not m:
            return {}, content
        raw, body = m.group(1), content[m.end():]
        try:
            import yaml
            loaded = yaml.safe_load(raw)
            if isinstance(loaded, dict):
                return loaded, body
        except Exception:
            pass
        fm, lines, i = {}, raw.split("\n"), 0
        while i < len(lines):
            mm = _re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", lines[i])
            if not mm:
                i += 1
                continue
            key, value = mm.group(1), mm.group(2).strip()
            if value in (">", "|"):
                i += 1
                collected = []
                while i < len(lines) and (lines[i].startswith("  ") or lines[i] == ""):
                    collected.append(lines[i].strip())
                    i += 1
                fm[key] = " ".join(s for s in collected if s)
                continue
            if (value[:1], value[-1:]) in (('"', '"'), ("'", "'")):
                value = value[1:-1]
            fm[key] = value
            i += 1
        return fm, body


def resolve_description(args):
    if args.skill_md:
        p = Path(args.skill_md)
        if not p.is_file():
            print(f"Error: no existe el archivo '{p}'.", file=sys.stderr)
            return None
        fm, _ = parse_frontmatter(p.read_text(encoding="utf-8"))
        desc = fm.get("description")
        if not desc:
            print("Error: el SKILL.md no tiene campo `description` en el frontmatter.",
                  file=sys.stderr)
            return None
        return str(desc)
    if args.file:
        p = Path(args.file)
        if not p.is_file():
            print(f"Error: no existe el archivo '{p}'.", file=sys.stderr)
            return None
        return p.read_text(encoding="utf-8")
    if args.description:
        return args.description
    return None


def main():
    ap = argparse.ArgumentParser(
        description="Valida la longitud de la description de un skill (<=1024).")
    ap.add_argument("description", nargs="?", help="Description inline.")
    ap.add_argument("--skill-md", help="Ruta a un SKILL.md (extrae la description).")
    ap.add_argument("--file", help="Ruta a un archivo con solo la description.")
    args = ap.parse_args()

    desc = resolve_description(args)
    if desc is None:
        print("Uso: validate_description.py (--skill-md F | --file F | \"<texto>\")",
              file=sys.stderr)
        return 2

    n = len(desc)

    if n > HARD_LIMIT:
        print(f"INVALID: description = {n} caracteres (máximo {HARD_LIMIT}).",
              file=sys.stderr)
        print(f"  sobra: {n - HARD_LIMIT} caracteres.", file=sys.stderr)
        print("  El validador de Anthropic rechaza/trunca arriba de 1024.",
              file=sys.stderr)
        print("  Fix: dejar 1 oración de qué hace + 5-8 frases disparadoras clave; "
              "mover workflow/sistemas/reglas al cuerpo del SKILL.md.", file=sys.stderr)
        return 1

    print(f"OK: description = {n} caracteres (máximo {HARD_LIMIT}).")
    if n > WARN_CEIL:
        print(f"  aviso: a {HARD_LIMIT - n} caracteres del techo. Deja margen "
              "(apunta a 700-900).", file=sys.stderr)
    elif n < RECOMMENDED_FLOOR:
        print(f"  aviso: por debajo del piso recomendado ({RECOMMENDED_FLOOR}). "
              "Descriptions cortas no triggerean bien.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
