#!/usr/bin/env bash
# validate-commit-msg.sh — Valida un mensaje de commit contra Conventional Commits
# (ver references/03-branch-and-commit-conventions.md).
# Formato: <tipo>[scope opcional]: <descripción en infinitivo>
# Tipos permitidos: feat fix docs style refactor perf test chore
# Blocklist (rechazo directo): "fix" solo, "update", "WIP", "asdf", texto libre sin prefijo.
#
# Uso:   bash scripts/validate-commit-msg.sh "feat(lwc): crear componente de facturación"
#        bash scripts/validate-commit-msg.sh .git/COMMIT_EDITMSG    # o un archivo
# Exit 0 = válido; Exit 1 = inválido (imprime el motivo).
set -euo pipefail

arg="${1:-}"
[ -z "$arg" ] && { echo "ERROR: pasá el mensaje de commit (o la ruta a un archivo)." >&2; exit 1; }

# Si es un archivo existente, leer la primera línea (subject); si no, tratar el arg como el mensaje.
if [ -f "$arg" ]; then msg="$(head -1 "$arg")"; else msg="$arg"; fi

# Blocklist de mensajes basura.
low="$(printf '%s' "$msg" | tr '[:upper:]' '[:lower:]' | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')"
for bad in "wip" "asdf" "update" "fix" "fixes" "cambios" "test"; do
  if [ "$low" = "$bad" ]; then
    echo "❌ Mensaje en blocklist: '$msg'. No es Conventional Commit." >&2
    echo "   Ej. válido: feat(apex): agregar validación de monto en AccountService" >&2
    exit 1
  fi
done

# Patrón Conventional Commits: tipo(scope opcional)!: descripción
pattern='^(feat|fix|docs|style|refactor|perf|test|chore)(\([a-z0-9_-]+\))?(!)?: .+'
if printf '%s' "$msg" | grep -Eq "$pattern"; then
  echo "✅ Mensaje válido: $msg"
  exit 0
else
  echo "❌ No cumple Conventional Commits: '$msg'" >&2
  echo "   Formato: <tipo>[scope]: <descripción en infinitivo>" >&2
  echo "   Tipos: feat | fix | docs | style | refactor | perf | test | chore" >&2
  echo "   Ej.:   fix(apex): manejar el NullPointerException en el trigger de Contacto" >&2
  exit 1
fi
