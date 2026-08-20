#!/usr/bin/env node
/**
 * pptx.mjs — Empaquetador OOXML: convierte una lista de imágenes PNG en un
 * .pptx con una diapositiva por imagen, a página completa y en 16:9.
 *
 * Vive del lado del exportador (no en el deck): el deck ya no arma archivos,
 * sus botones le piden el export al agente. Sin dependencias externas — el ZIP
 * se escribe acá con entradas STORE, que es un ZIP válido.
 *
 * Validado con python-pptx: 16:9 exacto (12192000 x 6858000 EMU) y una imagen
 * full-bleed por diapositiva.
 */

var CRC = (function(){
  var t = new Uint32Array(256);
  for(var n = 0; n < 256; n++){
    var c = n;
    for(var k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    t[n] = c >>> 0;
  }
  return t;
})();
function crc32(u8){
  var c = 0xFFFFFFFF;
  for(var i = 0; i < u8.length; i++) c = CRC[(c ^ u8[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}
function bytes(x){
  if(typeof x === 'string') return new TextEncoder().encode(x);
  return x;
}
/* entries: [{name, blob}] o [{name, data:Uint8Array|string}] */
function zip(entries){
  return Promise.all(entries.map(function(e){
    if(e.data !== undefined) return Promise.resolve({ name: e.name, u8: bytes(e.data) });
    return e.blob.arrayBuffer().then(function(ab){ return { name: e.name, u8: new Uint8Array(ab) }; });
  })).then(function(items){
    var chunks = [], central = [], offset = 0;
    items.forEach(function(it){
      var nameU8 = bytes(it.name), crc = crc32(it.u8), size = it.u8.length;
      var lh = new DataView(new ArrayBuffer(30));
      lh.setUint32(0, 0x04034b50, true); lh.setUint16(4, 20, true); lh.setUint16(6, 0x0800, true);
      lh.setUint16(8, 0, true); lh.setUint16(10, 0, true); lh.setUint16(12, 0x21, true);
      lh.setUint32(14, crc, true); lh.setUint32(18, size, true); lh.setUint32(22, size, true);
      lh.setUint16(26, nameU8.length, true); lh.setUint16(28, 0, true);
      chunks.push(new Uint8Array(lh.buffer), nameU8, it.u8);
      var ch = new DataView(new ArrayBuffer(46));
      ch.setUint32(0, 0x02014b50, true); ch.setUint16(4, 20, true); ch.setUint16(6, 20, true);
      ch.setUint16(8, 0x0800, true); ch.setUint16(10, 0, true);
      ch.setUint16(12, 0, true); ch.setUint16(14, 0x21, true);
      ch.setUint32(16, crc, true); ch.setUint32(20, size, true); ch.setUint32(24, size, true);
      ch.setUint16(28, nameU8.length, true); ch.setUint16(30, 0, true); ch.setUint16(32, 0, true);
      ch.setUint16(34, 0, true); ch.setUint16(36, 0, true); ch.setUint32(38, 0, true);
      ch.setUint32(42, offset, true);
      central.push(new Uint8Array(ch.buffer), nameU8);
      offset += 30 + nameU8.length + size;
    });
    var cSize = central.reduce(function(a, b){ return a + b.length; }, 0);
    var eo = new DataView(new ArrayBuffer(22));
    eo.setUint32(0, 0x06054b50, true); eo.setUint16(8, items.length, true);
    eo.setUint16(10, items.length, true); eo.setUint32(12, cSize, true); eo.setUint32(16, offset, true);
    return new Blob(chunks.concat(central, [new Uint8Array(eo.buffer)]), { type: 'application/zip' });
  });
}

/* ═══════════ 9. PPTX — OOXML mínimo, una imagen full-bleed por diapositiva ═══════════ */
function pptx(images){
  var W = 12192000, H = 6858000;   /* 13.333in × 7.5in en EMU = 16:9 */
  var n = images.length;
  var head = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n';
  var NS_P = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" ' +
             'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ' +
             'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"';
  var REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/';
  var e = [], i;

  var types = head + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' +
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' +
    '<Default Extension="xml" ContentType="application/xml"/>' +
    '<Default Extension="png" ContentType="image/png"/>' +
    '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>' +
    '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>' +
    '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>' +
    '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>';
  for(i = 1; i <= n; i++) types += '<Override PartName="/ppt/slides/slide' + i +
    '.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>';
  types += '</Types>';
  e.push({ name: '[Content_Types].xml', data: types });

  e.push({ name: '_rels/.rels', data: head +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
    '<Relationship Id="rId1" Type="' + REL + 'officeDocument" Target="ppt/presentation.xml"/>' +
    '</Relationships>' });

  var sldIds = '', presRels = '<Relationship Id="rId1" Type="' + REL + 'slideMaster" Target="slideMasters/slideMaster1.xml"/>';
  for(i = 1; i <= n; i++){
    sldIds += '<p:sldId id="' + (255 + i) + '" r:id="rId' + (i + 1) + '"/>';
    presRels += '<Relationship Id="rId' + (i + 1) + '" Type="' + REL + 'slide" Target="slides/slide' + i + '.xml"/>';
  }
  presRels += '<Relationship Id="rId' + (n + 2) + '" Type="' + REL + 'theme" Target="theme/theme1.xml"/>';
  e.push({ name: 'ppt/presentation.xml', data: head + '<p:presentation ' + NS_P + '>' +
    '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>' +
    '<p:sldIdLst>' + sldIds + '</p:sldIdLst>' +
    '<p:sldSz cx="' + W + '" cy="' + H + '"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>' });
  e.push({ name: 'ppt/_rels/presentation.xml.rels', data: head +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + presRels + '</Relationships>' });

  var emptyTree = '<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/>' +
    '</p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>';
  e.push({ name: 'ppt/slideMasters/slideMaster1.xml', data: head + '<p:sldMaster ' + NS_P + '>' + emptyTree +
    '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" hlink="hlink" folHlink="folHlink" ' +
    'accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6"/>' +
    '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>' });
  e.push({ name: 'ppt/slideMasters/_rels/slideMaster1.xml.rels', data: head +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
    '<Relationship Id="rId1" Type="' + REL + 'slideLayout" Target="../slideLayouts/slideLayout1.xml"/>' +
    '<Relationship Id="rId2" Type="' + REL + 'theme" Target="../theme/theme1.xml"/></Relationships>' });
  e.push({ name: 'ppt/slideLayouts/slideLayout1.xml', data: head + '<p:sldLayout ' + NS_P + ' type="blank" preserve="1">' +
    '<p:cSld name="En blanco"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/>' +
    '</p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>' });
  e.push({ name: 'ppt/slideLayouts/_rels/slideLayout1.xml.rels', data: head +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
    '<Relationship Id="rId1" Type="' + REL + 'slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>' });
  e.push({ name: 'ppt/theme/theme1.xml', data: theme(head) });

  for(i = 1; i <= n; i++){
    e.push({ name: 'ppt/media/image' + i + '.png', blob: images[i - 1] });
    e.push({ name: 'ppt/slides/slide' + i + '.xml', data: head + '<p:sld ' + NS_P + '><p:cSld><p:spTree>' +
      '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>' +
      '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="' + W + '" cy="' + H + '"/>' +
      '<a:chOff x="0" y="0"/><a:chExt cx="' + W + '" cy="' + H + '"/></a:xfrm></p:grpSpPr>' +
      '<p:pic><p:nvPicPr><p:cNvPr id="2" name="Slide ' + i + '"/>' +
      '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>' +
      '<p:blipFill><a:blip r:embed="rId2"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>' +
      '<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="' + W + '" cy="' + H + '"/></a:xfrm>' +
      '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>' +
      '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>' });
    e.push({ name: 'ppt/slides/_rels/slide' + i + '.xml.rels', data: head +
      '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
      '<Relationship Id="rId1" Type="' + REL + 'slideLayout" Target="../slideLayouts/slideLayout1.xml"/>' +
      '<Relationship Id="rId2" Type="' + REL + 'image" Target="../media/image' + i + '.png"/></Relationships>' });
  }
  return zip(e).then(function(b){
    return b.slice(0, b.size, 'application/vnd.openxmlformats-officedocument.presentationml.presentation');
  });
}
/* Tema mínimo válido, con la paleta de marca en los acentos. */
function theme(head){
  var A = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"';
  function sc(tag, hex){ return '<a:' + tag + '><a:srgbClr val="' + hex + '"/></a:' + tag + '>'; }
  var fill = '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>';
  var line = '<a:ln w="9525" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/>' +
             '</a:solidFill><a:prstDash val="solid"/></a:ln>';
  return head + '<a:theme ' + A + ' name="ProContacto"><a:themeElements>' +
    '<a:clrScheme name="ProContacto">' +
    '<a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>' +
    '<a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>' +
    sc('dk2', '0B0C0E') + sc('lt2', 'F2F2F2') + sc('accent1', '0062FF') + sc('accent2', '8F7AFF') +
    sc('accent3', '009060') + sc('accent4', '0070DD') + sc('accent5', 'D21E41') + sc('accent6', 'DF4D03') +
    sc('hlink', '66ACFF') + sc('folHlink', 'BEAFFF') + '</a:clrScheme>' +
    '<a:fontScheme name="ProContacto">' +
    '<a:majorFont><a:latin typeface="Open Sans"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>' +
    '<a:minorFont><a:latin typeface="Open Sans"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>' +
    '</a:fontScheme>' +
    '<a:fmtScheme name="ProContacto">' +
    '<a:fillStyleLst>' + fill + fill + fill + '</a:fillStyleLst>' +
    '<a:lnStyleLst>' + line + line + line + '</a:lnStyleLst>' +
    '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/>' +
    '</a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>' +
    '<a:bgFillStyleLst>' + fill + fill + fill + '</a:bgFillStyleLst>' +
    '</a:fmtScheme></a:themeElements></a:theme>';
}

export { zip, pptx };
