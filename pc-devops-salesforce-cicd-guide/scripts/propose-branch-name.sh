#!/usr/bin/env bash
# propose-branch-name.sh — Propone un nombre de rama según la convención de ProContacto
# (ver references/03-branch-and-commit-conventions.md): <prefijo>/<TICKET-JIRA>-<descripcion-kebab>
# Prefijos válidos: feature | bugfix | hotfix | chore
# NO crea la rama — solo imprime el nombre sugerido (el checkout -b es write y requiere ✅).
#
# Uso:   bash scripts/propose-branch-name.sh <prefijo> <TICKET> "<descripción libre>"
# Ej:    bash scripts/propose-branch-name.sh feature PROC-102 "Alta de clientes"
#        -> feature/PROC-102-alta-de-clientes
set -euo pipefail

prefix="${1:-}"; ticket="${2:-}"; shift 2 2>/dev/null || true
desc="${*:-}"

case "$prefix" in
  feature|bugfix|hotfix|chore) : ;;
  *) echo "ERROR: prefijo inválido '$prefix'. Usá: feature | bugfix | hotfix | chore" >&2; exit 1 ;;
esac

# Ticket Jira: LETRAS-NUMERO (ej. PROC-102, COLOM-303). Normalizar a mayúsculas.
ticket_up="$(printf '%s' "$ticket" | tr '[:lower:]' '[:upper:]')"
if ! printf '%s' "$ticket_up" | grep -Eq '^[A-Z][A-Z0-9]+-[0-9]+$'; then
  echo "ERROR: ticket inválido '$ticket'. Formato esperado: PROYECTO-123 (ej. PROC-102)." >&2
  exit 1
fi

# Descripción -> kebab-case: minúsculas, sin tildes, espacios/símbolos -> guiones, colapsar.
slug="$(printf '%s' "$desc" \
  | tr '[:upper:]' '[:lower:]' \
  | iconv -f UTF-8 -t ASCII//TRANSLIT 2>/dev/null || printf '%s' "$desc" | tr '[:upper:]' '[:lower:]')"
slug="$(printf '%s' "$slug" | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g')"

if [ -n "$slug" ]; then
  echo "${prefix}/${ticket_up}-${slug}"
else
  echo "${prefix}/${ticket_up}"
fi

# hotfix: recordatorio — nace de main, no de develop (ver módulo 11).
if [ "$prefix" = "hotfix" ]; then
  echo "# recordá: los hotfix nacen desde 'main' (git checkout main && git pull && git checkout -b <arriba>)" >&2
fi
