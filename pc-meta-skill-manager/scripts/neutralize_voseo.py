#!/usr/bin/env python3
"""Neutraliza voseo (rioplatense) → español neutro en el catálogo de skills.

Companion del detector Q09 (audit_catalog.py :: check_default_dialect). Ambos
consumen el mismo mapa curado (voseo_map.py). El script SOLO reemplaza tokens
presentes en el mapa: lo no mapeado queda intacto (y el detector lo reporta como
residuo para repaso humano).

Uso:
    python3.12 neutralize_voseo.py            # DRY-RUN (no escribe), reporte
    python3.12 neutralize_voseo.py --apply    # aplica los cambios en disco
    python3.12 neutralize_voseo.py --root DIR # raíz a barrer (default: repo)

Orden de pasadas (importa):
    1. Frases   (con vos → contigo, a vos → a ti, vos mismo → tú mismo)
    2. Tokens   (imperativos con/sin clítico + indicativo vos)
    3. Pronombre suelto  (vos → tú)
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from voseo_map import PHRASES, PRONOUN, build_map  # noqa: E402

# Extensiones de texto a barrer.
EXTS = {".md", ".html", ".htm", ".py", ".json", ".jsonl", ".txt"}

# Directorios que nunca se tocan.
SKIP_DIRS = {".git", ".claude", "node_modules", "__pycache__", "_deprecados",
             ".worktrees", "_backup"}

# Guard por LÍNEA: una línea que habla DE dialectos (política o ejemplo) usa el
# voseo como CONTENIDO, no como medio → no se toca. Cubre la tabla país→dialecto
# de presentaciones, "rioplatense (vos, no tú)", "Imperativo voseo amigable", etc.
# Los skills que declaran su registro en voseo quedan como decisión aparte.
#
# También protege plantillas de mensaje en 1ª persona del asistente donde una
# forma -í/-é es PRETÉRITO ("le pedí a Ariel", "recibí lo de X"), NO imperativo
# vos — sin esto, el fixer las rompería a "le pide"/"recibe" en cada corrida.
PROTECT_LINE_RE = re.compile(
    r"voseo|rioplatense|tuteo"
    r"|le ped[íi] a|te ped[íi] (ayer|varias)|recib[íi] lo de ",
    re.IGNORECASE,
)

# Archivos que CONTIENEN voseo como dato (el mapa y este script) → excluidos,
# o el fixer se corrompería a sí mismo.
SELF_FILES = {"voseo_map.py", "neutralize_voseo.py"}

TOKEN_MAP = build_map()

# Boundary unicode-aware: ni letra acentuada ni \w a los costados.
_WORDCHAR = r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ_]"


def _compile(keys: list[str]) -> re.Pattern[str]:
    alt = "|".join(re.escape(k) for k in sorted(keys, key=len, reverse=True))
    return re.compile(rf"(?<!{_WORDCHAR})({alt})(?!{_WORDCHAR})", re.IGNORECASE)


def _match_case(original: str, replacement: str) -> str:
    if original.isupper() and len(original) > 1:
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def _make_repl(mapping: dict[str, str], counter: Counter):
    def repl(m: re.Match[str]) -> str:
        original = m.group(0)
        rep = mapping[original.lower()]
        counter[original.lower()] += 1
        return _match_case(original, rep)
    return repl


PHRASE_RE = _compile(list(PHRASES))
TOKEN_RE = _compile(list(TOKEN_MAP))
PRONOUN_RE = _compile(list(PRONOUN))


def _neutralize_line(line: str, counter: Counter) -> str:
    if PROTECT_LINE_RE.search(line):
        return line  # línea que habla DE dialectos → voseo es contenido, no medio
    line = PHRASE_RE.sub(_make_repl(PHRASES, counter), line)
    line = TOKEN_RE.sub(_make_repl(TOKEN_MAP, counter), line)
    line = PRONOUN_RE.sub(_make_repl(PRONOUN, counter), line)
    return line


def neutralize(text: str, counter: Counter) -> str:
    return "\n".join(_neutralize_line(ln, counter) for ln in text.split("\n"))


def iter_files(root: Path):
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in SELF_FILES:
            continue
        if p.suffix.lower() not in EXTS:
            continue
        yield p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="escribir cambios")
    ap.add_argument("--root", default=None, help="raíz a barrer")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[3]

    total = Counter()
    changed_files: list[tuple[Path, int]] = []
    for path in iter_files(root):
        try:
            src = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        counter: Counter = Counter()
        out = neutralize(src, counter)
        if out != src:
            n = sum(counter.values())
            changed_files.append((path.relative_to(root), n))
            total.update(counter)
            if args.apply:
                path.write_text(out, encoding="utf-8")

    mode = "APLICADO" if args.apply else "DRY-RUN (sin escribir)"
    print(f"=== neutralize_voseo · {mode} ===")
    print(f"raíz: {root}")
    print(f"archivos afectados: {len(changed_files)}")
    print(f"reemplazos totales: {sum(total.values())}")
    print("\n--- top 40 tokens reemplazados ---")
    for tok, n in total.most_common(40):
        print(f"  {n:>5}  {tok} → {(_ALL := {**PHRASES, **TOKEN_MAP, **PRONOUN}).get(tok, '?')}")
    print("\n--- archivos (top 30 por cantidad) ---")
    for rel, n in sorted(changed_files, key=lambda x: x[1], reverse=True)[:30]:
        print(f"  {n:>4}  {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
