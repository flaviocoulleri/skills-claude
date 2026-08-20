#!/usr/bin/env node
/**
 * verificar-visual.mjs — Comprobación visual de un entregable antes de publicarlo.
 *
 * POR QUÉ EXISTE
 * --------------
 * Mirar una captura engaña. En la construcción de este motor, tres conclusiones
 * seguidas salieron mal por confiar en lo que "se veía"; los bugs reales los
 * encontró la medición: tokens de marca que no resolvían, un eje tipográfico que
 * no se aplicaba, un slide que desbordaba. Este script mide en vez de mirar.
 *
 * QUÉ REVISA
 * ----------
 *   1. Tokens del Design System        → que resuelvan de verdad (no que "se vea bien")
 *   2. Desborde                        → contenido fuera de su slide o de la hoja
 *   3. Contraste                       → texto vs su fondo real, umbral WCAG AA
 *   4. Alineación                      → bordes izquierdos que no comparten eje
 *   5. Márgenes                        → padding disparejo entre slides hermanos
 *   6. Tipografía                      → que cargó la de marca y no un fallback
 *   7. Recursos por red                → cualquier pedido externo no declarado
 *   8. Consola                         → errores en tiempo de ejecución
 *
 * USO
 * ---
 *   node verificar-visual.mjs <archivo.html> [--capturas=DIR] [--umbral-contraste=4.5]
 *
 * Sale con código 1 si hay hallazgos BLOQUEANTES, 0 si sólo hay avisos.
 */

import { createServer } from 'http';
import { readFileSync, existsSync, statSync, mkdirSync, writeFileSync } from 'fs';
import { join, dirname, basename, extname, resolve } from 'path';
import { createRequire } from 'module';
import os from 'os';

const argv = process.argv.slice(2);
if (!argv.length || argv[0].startsWith('--')) {
  console.error('Uso: node verificar-visual.mjs <archivo.html> [--capturas=DIR] [--umbral-contraste=4.5]');
  process.exit(1);
}
const ARCHIVO = resolve(argv[0]);
if (!existsSync(ARCHIVO)) { console.error(`✗ No encontré ${ARCHIVO}`); process.exit(1); }
const opt = (n, d) => { const a = argv.find(x => x.startsWith(`--${n}=`)); return a ? a.slice(n.length + 3) : d; };
const CAPTURAS = opt('capturas', null);
const UMBRAL = parseFloat(opt('umbral-contraste', '4.5'));

/* ─── Playwright (misma caché que el exportador) ─── */
function cargarPlaywright() {
  const req = createRequire(import.meta.url);
  try { return req('playwright'); } catch {}
  try { return createRequire(join(os.homedir(), '.cache', 'pc-deck-export', 'index.js'))('playwright'); }
  catch {
    console.error('✗ Playwright no está instalado. Corré primero el exportador, que lo instala.');
    process.exit(2);
  }
}

/* ─── Servidor local ─── */
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2' };
function servir(raiz) {
  return new Promise(ok => {
    const s = createServer((req, res) => {
      const f = join(raiz, decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, ''));
      if (!f.startsWith(raiz) || !existsSync(f) || statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
      res.writeHead(200, { 'Content-Type': MIME[extname(f).toLowerCase()] || 'application/octet-stream' });
      res.end(readFileSync(f));
    });
    s.listen(0, '127.0.0.1', () => ok({ server: s, puerto: s.address().port }));
  });
}

const { server, puerto } = await servir(dirname(ARCHIVO));
const { chromium } = cargarPlaywright();
const navegador = await chromium.launch();
const hallazgos = [];
const anotar = (nivel, area, detalle) => hallazgos.push({ nivel, area, detalle });

try {
  const pagina = await navegador.newPage({ viewport: { width: 1440, height: 900 } });
  const errores = [], pedidos = [];
  pagina.on('pageerror', e => errores.push(e.message));
  pagina.on('request', r => { if (/^https?:/.test(r.url()) && !r.url().includes('127.0.0.1')) pedidos.push(r.url()); });
  await pagina.goto(`http://127.0.0.1:${puerto}/${encodeURIComponent(basename(ARCHIVO))}`, { waitUntil: 'networkidle' });
  await pagina.waitForTimeout(700);   // que asiente el layout: medir antes da falsos positivos

  const r = await pagina.evaluate((UMBRAL) => {
    const out = { tipo: null, tokens: {}, desbordes: [], contraste: [], degradados: [], alineacion: [], margenes: [], fuentes: [] };

    /* Qué clase de entregable es */
    out.tipo = document.querySelector('.slide') ? 'deck'
             : document.querySelector('.wf-screen') ? 'wireframe'
             : document.getElementById('doc-wrap') ? 'documento' : 'desconocido';

    /* 1 · Tokens del Design System — el bug más silencioso: el entregable
       renderiza igual pero pierde la marca. */
    const cs = getComputedStyle(document.documentElement);
    ['--pc-blue', '--pc-violet', '--w-extrabold', '--pc-ink', '--font-sans', '--ui-font']
      .forEach(t => { const v = cs.getPropertyValue(t).trim(); if (v) out.tokens[t] = v; });

    /* Utilidades de color */
    const rgb = c => (c.match(/[\d.]+/g) || []).slice(0, 3).map(Number);
    const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); };
      return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
    const ratio = (a, b) => { const [l1, l2] = [lum(a), lum(b)].sort((x, y) => y - x); return (l1 + .05) / (l2 + .05); };
    function fondoReal(el) {
      let n = el;
      while (n && n !== document.documentElement) {
        const bg = getComputedStyle(n).backgroundColor;
        const p = rgb(bg); const alpha = (bg.match(/[\d.]+/g) || [])[3];
        if (p.length === 3 && alpha !== '0') return p;
        n = n.parentElement;
      }
      return [255, 255, 255];
    }

    const contenedores = out.tipo === 'deck' ? [...document.querySelectorAll('.slide')]
                       : out.tipo === 'wireframe' ? [...document.querySelectorAll('.wf-screen')]
                       : [document.getElementById('contenido') || document.body];

    contenedores.forEach((cont, idx) => {
      const activo = out.tipo === 'documento' || cont.classList.contains('active') || cont.classList.contains('activa');
      if (!activo && out.tipo !== 'documento') { cont.classList.add(out.tipo === 'deck' ? 'active' : 'activa'); }
      const cb = cont.getBoundingClientRect();

      cont.querySelectorAll('*').forEach(el => {
        const b = el.getBoundingClientRect();
        if (!b.width || !b.height) return;
        const est = getComputedStyle(el);
        if (est.position === 'fixed' || est.visibility === 'hidden' || est.display === 'none') return;

        /* 2 · Desborde: lo que no entra, se pierde */
        if (b.right > cb.right + 1 || b.bottom > cb.bottom + 1 || b.left < cb.left - 1 || b.top < cb.top - 1) {
          out.desbordes.push({ n: idx + 1, el: el.tagName + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''),
            sale: Math.round(Math.max(b.right - cb.right, b.bottom - cb.bottom, cb.left - b.left, cb.top - b.top)) + 'px' });
        }

        /* 3 · Contraste — sólo nodos con texto propio.
           Ojo con el texto con degradado (`background-clip:text` + color
           transparente, la firma de la marca): el color computado es
           transparente y el cálculo daría 1:1, que es un falso positivo. No se
           puede medir automáticamente, así que se avisa para que lo mire una
           persona en vez de bloquear. */
        const propio = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 2);
        const clipEnTexto = (est.webkitBackgroundClip || est.backgroundClip) === 'text';
        if (propio && clipEnTexto) {
          out.degradados.push({ n: idx + 1, texto: el.textContent.trim().slice(0, 42) });
        } else if (propio) {
          const fg = rgb(est.color);
          if (fg.length === 3) {
            const cr = ratio(fg, fondoReal(el));
            const px = parseFloat(est.fontSize), grande = px >= 24 || (px >= 18.66 && parseInt(est.fontWeight) >= 700);
            const min = grande ? 3 : UMBRAL;
            if (cr < min) out.contraste.push({ n: idx + 1, texto: el.textContent.trim().slice(0, 42),
              ratio: cr.toFixed(2), minimo: min, px: Math.round(px) });
          }
        }
      });

      /* 4 · Alineación: los bloques principales deberían compartir eje izquierdo */
      const hijos = [...cont.children].flatMap(c => [...c.children].length ? [...c.children] : [c])
        .filter(e => { const b = e.getBoundingClientRect(); return b.width > 80 && b.height > 12; });
      const ejes = {};
      hijos.forEach(e => { const x = Math.round(e.getBoundingClientRect().left); ejes[x] = (ejes[x] || 0) + 1; });
      const claves = Object.keys(ejes).map(Number).sort((a, b) => a - b);
      claves.forEach(x => {
        if (ejes[x] !== 1) return;
        const cerca = claves.find(o => o !== x && Math.abs(o - x) <= 12 && ejes[o] > 1);
        if (cerca !== undefined) out.alineacion.push({ n: idx + 1, x, esperado: cerca, desvio: Math.abs(x - cerca) });
      });

      /* 5 · Márgenes del contenedor */
      const e = getComputedStyle(cont);
      out.margenes.push({ n: idx + 1, top: e.paddingTop, right: e.paddingRight, bottom: e.paddingBottom, left: e.paddingLeft });
    });

    /* 6 · Tipografía realmente cargada */
    document.fonts.forEach(f => out.fuentes.push(`${f.family} ${f.weight} ${f.status}`));
    const h = document.querySelector('h1, h2, .pc-slide__title');
    if (h) out.tipografiaTitulo = { familia: getComputedStyle(h).fontFamily.split(',')[0].replace(/['"]/g, ''), peso: getComputedStyle(h).fontWeight };
    return out;
  }, UMBRAL);

  /* ─── Evaluar ─── */
  console.log(`\n· Entregable: ${basename(ARCHIVO)}  ·  tipo: ${r.tipo}\n`);

  const esperados = { '--pc-blue': '#0062FF', '--w-extrabold': '800' };
  for (const [t, v] of Object.entries(esperados)) {
    if (r.tokens[t] === undefined) anotar('aviso', 'Tokens', `${t} no está definido (puede ser normal en documentos)`);
    else if (r.tokens[t].toUpperCase() !== v) anotar('bloqueante', 'Tokens', `${t} vale "${r.tokens[t]}" y debería ser ${v}`);
  }
  if (r.tipografiaTitulo && !/Open Sans/i.test(r.tipografiaTitulo.familia))
    anotar('bloqueante', 'Tipografía', `los títulos usan "${r.tipografiaTitulo.familia}" en vez de Open Sans`);
  if (!r.fuentes.some(f => /Open Sans/i.test(f) && /loaded/.test(f)))
    anotar('aviso', 'Tipografía', 'Open Sans no figura cargada — puede estar cayendo al fallback del sistema');

  r.desbordes.slice(0, 12).forEach(d => anotar('bloqueante', 'Desborde', `${r.tipo === 'documento' ? '' : '#' + d.n + ' · '}${d.el} se sale ${d.sale}`));
  r.contraste.slice(0, 12).forEach(c => anotar('bloqueante', 'Contraste', `${c.ratio}:1 (mínimo ${c.minimo}) en ${c.px}px — "${c.texto}"`));
  if (r.degradados.length)
    anotar('aviso', 'Contraste', `${r.degradados.length} texto(s) con degradado de marca — el contraste no se puede medir automáticamente, revisalo a ojo: ${r.degradados.slice(0, 3).map(d => '"' + d.texto + '"').join(', ')}`);
  r.alineacion.slice(0, 10).forEach(a => anotar('aviso', 'Alineación', `#${a.n} · un bloque arranca en x=${a.x}, ${a.desvio}px fuera del eje ${a.esperado}`));

  const distintos = [...new Set(r.margenes.map(m => `${m.top}|${m.right}|${m.bottom}|${m.left}`))];
  if (distintos.length > 1 && r.tipo !== 'documento')
    anotar('aviso', 'Márgenes', `${distintos.length} combinaciones de padding distintas entre slides — revisá que sea intencional`);

  const externos = [...new Set(pedidos)].filter(u => !/fonts\.(googleapis|gstatic)\.com/.test(u));
  externos.slice(0, 6).forEach(u => anotar('bloqueante', 'Red', `pide un recurso externo: ${u.slice(0, 80)}`));
  errores.slice(0, 6).forEach(e => anotar('bloqueante', 'Consola', e.slice(0, 110)));

  /* ─── Capturas, si se piden ─── */
  if (CAPTURAS) {
    mkdirSync(CAPTURAS, { recursive: true });
    if (r.tipo === 'deck') {
      const n = await pagina.evaluate(() => window.PCDeck ? window.PCDeck.count() : 1);
      for (let i = 0; i < n; i++) {
        await pagina.evaluate(k => window.PCDeck && window.PCDeck.go(k), i);
        await pagina.waitForTimeout(120);
        await pagina.screenshot({ path: join(CAPTURAS, `slide-${String(i + 1).padStart(2, '0')}.png`) });
      }
      console.log(`  capturas: ${n} en ${CAPTURAS}`);
    } else {
      await pagina.screenshot({ path: join(CAPTURAS, 'pagina.png'), fullPage: true });
      console.log(`  captura: ${join(CAPTURAS, 'pagina.png')}`);
    }
  }
} finally {
  await navegador.close();
  server.close();
}

/* ─── Informe ─── */
const bloq = hallazgos.filter(h => h.nivel === 'bloqueante');
const avisos = hallazgos.filter(h => h.nivel === 'aviso');
if (!hallazgos.length) console.log('✓ Sin hallazgos. Tokens, encaje, contraste, alineación y red en orden.\n');
else {
  if (bloq.length) { console.log(`✗ ${bloq.length} bloqueante(s):`); bloq.forEach(h => console.log(`   [${h.area}] ${h.detalle}`)); console.log(''); }
  if (avisos.length) { console.log(`⚠ ${avisos.length} aviso(s):`); avisos.forEach(h => console.log(`   [${h.area}] ${h.detalle}`)); console.log(''); }
}
process.exit(bloq.length ? 1 : 0);
