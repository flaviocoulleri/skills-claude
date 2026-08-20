#!/usr/bin/env node
/**
 * export-deck.mjs — Exporta un deck HTML de ProContacto a PDF / PNG / JPG / PPTX.
 *
 * CUÁNDO USARLO
 * -------------
 * El deck ya trae su propio panel "Exportar" y cubre los mismos formatos sin
 * instalar nada: esa es la ruta por defecto. Este script es la ruta B, para
 * cuando conviene entregar el archivo ya generado desde la sesión, o cuando se
 * necesita la tipografía exacta (en el navegador del artefacto las fuentes por
 * red están bloqueadas y caen al sistema).
 *
 * DE DÓNDE SALE CADA FORMATO
 * --------------------------
 *   PDF   → impresión del navegador headless: el texto queda seleccionable.
 *   PNG   → una captura de 1920×1080 por slide.
 *   JPG   → lo mismo, recomprimido.
 *   PPTX  → una diapositiva por slide, con la captura a página completa,
 *           vía ./pptx.mjs (empaquetador OOXML propio, sin dependencias).
 *
 * USO
 * ---
 *   node export-deck.mjs <deck.html> [opciones]
 *
 *   --formato=LISTA    pdf,png,jpg,pptx  o  todos        (por defecto: pdf)
 *   --salida=DIR       carpeta destino                   (por defecto: junto al deck)
 *   --compacto         renderiza a 1280×720 en vez de 1920×1080
 *   --calidad-jpg=N    calidad JPEG 1–100                (por defecto: 92)
 *
 * DEPENDENCIAS
 * ------------
 * Node y Playwright. Si Playwright no está, se instala en la caché del usuario
 * la primera vez (no toca el repo ni el sistema). Si no hay red o falla, el
 * script lo dice y termina: la ruta A (panel del deck) sigue disponible.
 */

import { createServer } from 'http';
import { readFileSync, writeFileSync, mkdirSync, existsSync, statSync } from 'fs';
import { join, dirname, basename, extname, resolve } from 'path';
import { execSync } from 'child_process';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import os from 'os';
import { pptx } from './pptx.mjs';

const AQUI = dirname(fileURLToPath(import.meta.url));

/* ─── 1. Argumentos ──────────────────────────────────────────────────── */
const argv = process.argv.slice(2);
if (!argv.length || argv[0].startsWith('--')) {
  console.error('Uso: node export-deck.mjs <deck.html> [--formato=todos] [--salida=DIR] [--compacto] [--calidad-jpg=92]');
  process.exit(1);
}
const opt = (n, d) => {
  const a = argv.find(x => x.startsWith(`--${n}=`));
  return a ? a.slice(n.length + 3) : d;
};
const DECK = resolve(argv[0]);
if (!existsSync(DECK) || !statSync(DECK).isFile()) {
  console.error(`✗ No encontré el deck: ${DECK}`);
  process.exit(1);
}
const NOMBRE   = basename(DECK, extname(DECK));
const SALIDA   = resolve(opt('salida', dirname(DECK)));
const COMPACTO = argv.includes('--compacto');
const ANCHO    = COMPACTO ? 1280 : 1920;
const ALTO     = COMPACTO ? 720 : 1080;
const CALIDAD  = Math.min(100, Math.max(1, parseInt(opt('calidad-jpg', '92'), 10)));

let formatos = opt('formato', 'pdf').toLowerCase().split(',').map(s => s.trim()).filter(Boolean);
if (formatos.includes('todos') || formatos.includes('all')) formatos = ['pdf', 'png', 'jpg', 'pptx'];
const validos = ['pdf', 'png', 'jpg', 'pptx'];
const invalido = formatos.find(f => !validos.includes(f));
if (invalido) { console.error(`✗ Formato desconocido: "${invalido}". Válidos: ${validos.join(', ')} o "todos".`); process.exit(1); }

mkdirSync(SALIDA, { recursive: true });

/* ─── 2. Playwright (instalación perezosa en la caché del usuario) ───── */
const CACHE = join(os.homedir(), '.cache', 'pc-deck-export');
function cargarPlaywright() {
  const req = createRequire(import.meta.url);
  try { return req('playwright'); } catch { /* sigue */ }
  console.log('· Playwright no está instalado. Lo instalo en la caché del usuario (una sola vez)…');
  mkdirSync(CACHE, { recursive: true });
  if (!existsSync(join(CACHE, 'package.json'))) writeFileSync(join(CACHE, 'package.json'), '{"name":"pc-deck-export","private":true}');
  try {
    execSync('npm install --silent --no-audit --no-fund playwright', { cwd: CACHE, stdio: 'inherit' });
    execSync('npx --yes playwright install chromium', { cwd: CACHE, stdio: 'inherit' });
  } catch {
    console.error('✗ No pude instalar Playwright (¿sin red o sin permisos?).');
    console.error('  No es un bloqueo: exportá desde el panel "Exportar" del propio deck.');
    process.exit(2);
  }
  return createRequire(join(CACHE, 'index.js'))('playwright');
}

/* ─── 3. Servidor local (para que las rutas relativas resuelvan) ─────── */
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml',
  '.webp': 'image/webp', '.gif': 'image/gif', '.woff2': 'font/woff2', '.json': 'application/json' };
function servir(raiz) {
  return new Promise(ok => {
    const s = createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      const f = join(raiz, rel);
      if (!f.startsWith(raiz) || !existsSync(f) || statSync(f).isDirectory()) { res.writeHead(404); return res.end('no'); }
      res.writeHead(200, { 'Content-Type': MIME[extname(f).toLowerCase()] || 'application/octet-stream' });
      res.end(readFileSync(f));
    });
    s.listen(0, '127.0.0.1', () => ok({ server: s, puerto: s.address().port }));
  });
}

/* ─── 4. Exportar ────────────────────────────────────────────────────── */
const hechos = [];
const { server, puerto } = await servir(dirname(DECK));
const { chromium } = cargarPlaywright();
const navegador = await chromium.launch();

try {
  const pagina = await navegador.newPage({ viewport: { width: ANCHO, height: ALTO }, deviceScaleFactor: 1 });
  const errores = [];
  pagina.on('pageerror', e => errores.push(e.message));
  await pagina.goto(`http://127.0.0.1:${puerto}/${encodeURIComponent(basename(DECK))}`, { waitUntil: 'networkidle' });

  const total = await pagina.evaluate(() => (window.PCDeck ? window.PCDeck.count()
    : document.querySelectorAll('.slide').length));
  if (!total) throw new Error('el deck no tiene slides (.slide): ¿es un deck de ProContacto?');
  console.log(`· ${total} slide(s) a ${ANCHO}×${ALTO}${COMPACTO ? ' (compacto)' : ''}`);
  await pagina.evaluate(() => { if (window.PCDeck) window.PCDeck.freeze(true); });

  /* PDF — impresión del navegador: conserva el texto seleccionable */
  if (formatos.includes('pdf')) {
    const destino = join(SALIDA, `${NOMBRE}.pdf`);
    await pagina.emulateMedia({ media: 'print' });
    await pagina.pdf({ path: destino, width: `${ANCHO}px`, height: `${ALTO}px`,
      printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '' });
    await pagina.emulateMedia({ media: 'screen' });
    hechos.push([destino, total]);
    console.log(`  ✓ PDF  → ${destino}`);
  }

  /* Capturas por slide — base de PNG, JPG y PPTX */
  let capturas = null;
  const necesitaCapturas = formatos.some(f => f === 'png' || f === 'jpg' || f === 'pptx');
  if (necesitaCapturas) {
    capturas = [];
    for (let i = 0; i < total; i++) {
      await pagina.evaluate(n => { window.PCDeck ? window.PCDeck.go(n) : null; }, i);
      await pagina.waitForTimeout(120);
      capturas.push(await pagina.screenshot({ type: 'png', clip: { x: 0, y: 0, width: ANCHO, height: ALTO } }));
    }
  }

  if (formatos.includes('png') || formatos.includes('jpg')) {
    for (const tipo of ['png', 'jpg']) {
      if (!formatos.includes(tipo)) continue;
      const dir = join(SALIDA, `${NOMBRE}-${tipo}`);
      mkdirSync(dir, { recursive: true });
      for (let i = 0; i < total; i++) {
        const n = String(i + 1).padStart(2, '0');
        if (tipo === 'png') writeFileSync(join(dir, `${NOMBRE}-slide-${n}.png`), capturas[i]);
        else {
          await pagina.evaluate(n2 => { window.PCDeck ? window.PCDeck.go(n2) : null; }, i);
          await pagina.waitForTimeout(60);
          writeFileSync(join(dir, `${NOMBRE}-slide-${n}.jpg`),
            await pagina.screenshot({ type: 'jpeg', quality: CALIDAD, clip: { x: 0, y: 0, width: ANCHO, height: ALTO } }));
        }
      }
      hechos.push([dir, total]);
      console.log(`  ✓ ${tipo.toUpperCase()}  → ${dir}/ (${total} imágenes)`);
    }
  }

  if (formatos.includes('pptx')) {
    const blob = await pptx(capturas.map(b => new Blob([b], { type: 'image/png' })));
    const destino = join(SALIDA, `${NOMBRE}.pptx`);
    writeFileSync(destino, Buffer.from(await blob.arrayBuffer()));
    hechos.push([destino, total]);
    console.log(`  ✓ PPTX → ${destino}`);
  }

  if (errores.length) console.warn(`⚠ El deck reportó ${errores.length} error(es) en consola: ${errores[0]}`);
} finally {
  await navegador.close();
  server.close();
}

/* ─── 5. Verificación: no reportar éxito sin comprobarlo ─────────────── */
let ok = true;
for (const [ruta] of hechos) {
  if (!existsSync(ruta)) { console.error(`✗ Falta la salida esperada: ${ruta}`); ok = false; continue; }
  const st = statSync(ruta);
  if (st.isFile() && st.size < 1024) { console.error(`✗ ${ruta} quedó vacío (${st.size} bytes)`); ok = false; }
}
if (!ok) { console.error('✗ La exportación no se completó bien. Revisá y volvé a correr.'); process.exit(3); }
console.log(`✓ Listo — ${hechos.length} salida(s) en ${SALIDA}`);
