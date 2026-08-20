#!/usr/bin/env python3
"""
validate_name.py — Valida un nombre de skill contra la convención
                   pc-[área]-[sistema?]-[objeto]-[acción].

Uso:
    python3 validate_name.py pc-crm-salesforce-opportunity-creator
    # → exit 0, imprime breakdown

    python3 validate_name.py sf-field-creator-pro
    # → exit 1, imprime error en stderr

Pensado para:
- Ser invocado por el propio workflow del skill antes de crear un directorio.
- Ser llamado desde un pre-commit hook o CI sin dependencias externas.
- Uso directo en línea de comandos durante una sesión de naming.

Reusa el parser `parse_name()` de `audit_catalog.py` para mantener una
única fuente de verdad sobre la convención.
"""
import sys
from pathlib import Path

# Importar parse_name del hermano audit_catalog.py
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit_catalog import parse_name  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: validate_name.py <nombre-del-skill>", file=sys.stderr)
        print("Ejemplo: validate_name.py pc-crm-salesforce-opportunity-creator", file=sys.stderr)
        return 2

    name = sys.argv[1].strip()
    parts = parse_name(name)

    if not parts.valid:
        print(f"INVALID: {name}", file=sys.stderr)
        print(f"  razón: {parts.error}", file=sys.stderr)
        print(
            "  fórmula esperada: pc-[área]-[sistema?]-[objeto]-[acción]",
            file=sys.stderr,
        )
        print(
            "  ver: pc-meta-skill-manager/references/naming-convention.md",
            file=sys.stderr,
        )
        return 1

    system_str = parts.system if parts.system else "(omitido — área lo implica)"
    print(f"OK: {name}")
    print(f"  pc:     {parts.pc_prefix}")
    print(f"  área:   {parts.area}")
    print(f"  sistema:{system_str}")
    print(f"  objeto: {parts.object}")
    print(f"  acción: {parts.action}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
