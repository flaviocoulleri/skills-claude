#!/usr/bin/env bash
# check-env.sh — Valida los prerequisitos locales del flujo CI/CD de ProContacto.
# Requisitos (ver references/01-onboarding.md): Git, Node 20+, npm, Salesforce CLI (sf),
# JRE/JDK 11+ (para Code Analyzer/PMD). Read-only: solo inspecciona, no instala nada.
#
# Uso:  bash scripts/check-env.sh
set -uo pipefail

ok=0; fail=0
green(){ printf "  ✅ %s\n" "$1"; ok=$((ok+1)); }
bad(){ printf "  ❌ %s\n" "$1"; fail=$((fail+1)); }

echo "Chequeo de entorno CI/CD — ProContacto"
echo "--------------------------------------"

# Git
if command -v git >/dev/null 2>&1; then green "git: $(git --version)"; else bad "git no está instalado"; fi

# Node 20+
if command -v node >/dev/null 2>&1; then
  major="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)"
  if [ "${major:-0}" -ge 20 ]; then green "node: $(node --version) (>=20)"; else bad "node $(node --version) — se requiere v20+"; fi
else bad "node no está instalado (se requiere v20+)"; fi

# npm
if command -v npm >/dev/null 2>&1; then green "npm: $(npm --version)"; else bad "npm no está instalado"; fi

# Salesforce CLI
if command -v sf >/dev/null 2>&1; then green "sf CLI: $(sf --version 2>/dev/null | head -1)"; else bad "Salesforce CLI (sf) no está instalado"; fi

# Java 11+ (para Code Analyzer / PMD)
if command -v java >/dev/null 2>&1; then
  jv="$(java -version 2>&1 | head -1)"
  green "java: $jv (requerido por Code Analyzer/PMD)"
else bad "java (JRE/JDK 11+) no está instalado — Code Analyzer/PMD lo necesita"; fi

# Dependencias del proyecto (Husky/ESLint/Prettier) — solo si estamos en un repo con package.json
if [ -f package.json ]; then
  if [ -d node_modules ]; then green "node_modules presente (npm install ejecutado)";
  else bad "falta 'npm install' — los hooks de Husky no correrán y el PR fallará"; fi
else
  printf "  ℹ️  no hay package.json en el cwd — corré este script desde la raíz del repo\n"
fi

echo "--------------------------------------"
echo "OK: $ok   Faltantes: $fail"
[ "$fail" -eq 0 ] && echo "Entorno listo. 🎉" || echo "Resolvé los faltantes antes de trabajar (ver references/01-onboarding.md)."
exit "$fail"
