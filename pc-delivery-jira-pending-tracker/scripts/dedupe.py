"""
dedupe.py — Fuzzy matching de pendings extraídos contra issues existentes en Jira.

Uso esperado:
    from dedupe import classify_pendings
    results = classify_pendings(extracted_pendings, existing_issues, threshold=80)

Cada elemento del resultado es un dict con:
    - pending: el pending original (de extraction-prompt)
    - veredicto: "new" | "update_date" | "duplicate"
    - match_issue: el issue existente que matcheó (si aplica), con su key, summary, duedate
    - score: 0-100 (fuzzy match score)

El script prefiere rapidfuzz si está disponible (~10x más rápido), pero cae a difflib
si no está instalado, para que el skill no tenga dependencias duras.

Diseño de idempotencia:
    - Los mismos inputs deben producir los mismos veredictos.
    - Por eso normalizamos títulos (lowercase, stripping de stopwords cortas) antes
      de matchear, y usamos token_sort_ratio que es invariante al orden de palabras.
"""

from __future__ import annotations

import re
from typing import Any

try:
    from rapidfuzz import fuzz as _rapidfuzz

    def _score(a: str, b: str) -> float:
        return _rapidfuzz.token_sort_ratio(a, b)

except ImportError:  # fallback a stdlib
    from difflib import SequenceMatcher

    def _score(a: str, b: str) -> float:
        # token_sort_ratio approximation: ordenar tokens y comparar
        a_tok = " ".join(sorted(a.split()))
        b_tok = " ".join(sorted(b.split()))
        return SequenceMatcher(None, a_tok, b_tok).ratio() * 100


_STOPWORDS = {
    "el", "la", "los", "las", "de", "del", "en", "y", "a", "al", "por", "para",
    "the", "a", "an", "of", "in", "on", "to", "for", "by",
    "pending", "pendiente",  # las pegamos porque vienen en los títulos
}


def normalize_title(title: str) -> str:
    """Normaliza un título para fuzzy matching estable.

    - lowercase
    - saca puntuación no alfanumérica (salvo espacios)
    - remueve stopwords cortas
    - colapsa espacios
    """
    if not title:
        return ""
    s = title.lower()
    s = re.sub(r"[^a-záéíóúñü0-9\s]", " ", s)
    tokens = [t for t in s.split() if t not in _STOPWORDS and len(t) > 1]
    return " ".join(tokens).strip()


def _find_best_match(
    pending_title: str,
    existing_issues: list[dict[str, Any]],
    threshold: float = 80.0,
) -> tuple[dict[str, Any] | None, float]:
    """Devuelve (mejor issue existente, score) si supera el threshold, si no (None, best_score)."""
    norm_pending = normalize_title(pending_title)
    if not norm_pending:
        return None, 0.0

    best: dict[str, Any] | None = None
    best_score = 0.0
    for issue in existing_issues:
        existing_summary = issue.get("summary", "") or issue.get("fields", {}).get("summary", "")
        norm_existing = normalize_title(existing_summary)
        if not norm_existing:
            continue
        s = _score(norm_pending, norm_existing)
        if s > best_score:
            best_score = s
            best = issue

    if best_score >= threshold:
        return best, best_score
    return None, best_score


def _get_issue_duedate(issue: dict[str, Any]) -> str | None:
    """Extrae el duedate de un issue Jira (tolera dos formas de payload)."""
    if "duedate" in issue:
        return issue["duedate"]
    return issue.get("fields", {}).get("duedate")


def classify_pendings(
    extracted: list[dict[str, Any]],
    existing: list[dict[str, Any]],
    threshold: float = 80.0,
) -> list[dict[str, Any]]:
    """Clasifica cada pending extraído contra los issues existentes.

    Args:
        extracted: lista de pendings del extraction prompt.
        existing: lista de issues de Jira (cada uno con al menos `key`, `summary`, `duedate`).
        threshold: score mínimo (0-100) para considerar match. Default 80.

    Returns:
        Lista de dicts con pending + veredicto + match_issue + score.
    """
    results = []
    for p in extracted:
        title = p.get("titulo", "") or p.get("title", "")
        match, score = _find_best_match(title, existing, threshold=threshold)

        if not match:
            verdict = "new"
            match_info = None
        else:
            tipo_cambio = p.get("tipo_cambio", "new")
            new_date = p.get("fecha_compromiso")
            old_date = _get_issue_duedate(match)

            if tipo_cambio == "reschedule" and new_date and new_date != old_date:
                verdict = "update_date"
            elif new_date and old_date and new_date != old_date and tipo_cambio != "reschedule":
                # Fecha nueva pero el modelo no marcó reschedule — tratar como duplicado conservadoramente.
                # Dejar que el PM decida en el artifact si quiere forzar el update.
                verdict = "duplicate"
            else:
                verdict = "duplicate"

            match_info = {
                "key": match.get("key"),
                "summary": match.get("summary") or match.get("fields", {}).get("summary"),
                "duedate": old_date,
                "status": (match.get("status") or match.get("fields", {}).get("status", {})).get("name")
                    if isinstance(match.get("status") or match.get("fields", {}).get("status"), dict)
                    else match.get("status") or match.get("fields", {}).get("status"),
            }

        results.append({
            "pending": p,
            "veredicto": verdict,
            "match_issue": match_info,
            "score": round(score, 1),
        })
    return results


# ============================================================
# Pruebas manuales: correr `python dedupe.py` para smoke test
# ============================================================

if __name__ == "__main__":
    import json

    extracted_sample = [
        {
            "titulo": "Confirmar acceso al ambiente de QA",
            "fecha_compromiso": "2026-04-24",
            "tipo_cambio": "new",
        },
        {
            "titulo": "Assessment Fase 2",
            "fecha_compromiso": "2026-05-06",
            "tipo_cambio": "reschedule",
        },
        {
            "titulo": "Pending que no existe en Jira",
            "fecha_compromiso": None,
            "tipo_cambio": "new",
        },
    ]

    existing_sample = [
        {"key": "SURA-EXT-23", "summary": "Assessment de fase 2", "duedate": "2026-04-22"},
        {"key": "SURA-EXT-10", "summary": "Confirmar acceso QA", "duedate": "2026-04-15"},
        {"key": "SURA-EXT-05", "summary": "Revisar dimensionamiento", "duedate": None},
    ]

    out = classify_pendings(extracted_sample, existing_sample)
    print(json.dumps(out, indent=2, ensure_ascii=False))
