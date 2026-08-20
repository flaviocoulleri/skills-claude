#!/usr/bin/env bash
#
# build-brand-font.sh — regenera assets/brand-font.css con Open Sans embebida.
#
# Sólo hay que correrlo si cambia la tipografía del Design System. El resultado
# se commitea: los skills consumen el .css, no la fuente.
#
# Requiere: python3 con fonttools y brotli  →  pip install fonttools brotli
#
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$AQUI/../../../.." && pwd)"
TTF="${1:-$REPO/comercial/pc-sales-sf-sow-builder/assets/branding/fonts/OpenSans-VariableFont_wdth_wght.ttf}"
SALIDA="$AQUI/../assets/brand-font.css"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

[ -f "$TTF" ] || { echo "✗ No encontré la fuente: $TTF" >&2; exit 1; }
command -v pyftsubset >/dev/null 2>&1 || { echo "✗ Falta pyftsubset (pip install fonttools brotli)" >&2; exit 1; }

# Subconjunto latino + puntuación tipográfica + símbolos de moneda y flechas.
pyftsubset "$TTF" \
  --output-file="$TMP/opensans.woff2" --flavor=woff2 --layout-features='*' --drop-tables+=DSIG \
  --unicodes='U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD,U+2018-201D,U+2039-203A,U+00AB,U+00BB'

python3 - "$TMP/opensans.woff2" "$SALIDA" <<'PY'
import base64, sys
b64 = base64.b64encode(open(sys.argv[1], 'rb').read()).decode()
open(sys.argv[2], 'w').write(
"""/* =========================================================================
   ProContacto — Open Sans embebida (variable, subconjunto latino)
   Generado con: scripts/build-brand-font.sh  (fuente: Manual de Marca 2026)

   Por qué va embebida y no por CDN: el artefacto corre con CSP estricta que
   bloquea todo host externo, y el .html tiene que abrir sin internet. Con la
   fuente adentro, el deck se ve con la tipografía real de la marca en Cowork,
   fuera de Cowork y en los PNG/JPG/PPTX exportados.

   Incluir este archivo ANTES del kit de slides. Pesa ~125 KB: es el precio de
   que la marca se vea bien en todos lados.
   ========================================================================= */
@font-face {
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 300 800;
  font-stretch: 75% 125%;
  font-display: swap;
  src: url(data:font/woff2;base64,""" + b64 + """) format('woff2');
}
""")
print("✓ escrito:", sys.argv[2])
PY
