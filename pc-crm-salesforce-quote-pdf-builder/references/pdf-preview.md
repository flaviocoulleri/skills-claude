# Mostrarle al usuario el PDF generado, sin depender del navegador

`renderAs="pdf"` en una Visualforce page hace que cualquier navegador (incluido el Browser
pane) dispare una descarga nativa en vez de renderizar inline — la pane no puede
componer/capturar ese estado, así que `screenshot` falla con
`"the Browser pane is not displayed"` aunque la página cargó bien. No pierdas tiempo
intentando forzar el toggle `renderAs` por query param (`?preview=1` vía
`{!IF(ISBLANK($CurrentPage.parameters.preview), 'pdf', '')}`) — en la sesión donde se probó
esto tiró "An internal server error has occurred" de forma consistente. El camino que sí
funciona de punta a punta es generar el PDF por Apex y traerlo al filesystem local.

## Técnica: generar el PDF vía Execute Anonymous y volcar el base64 en chunks

El PDF generado (con logo + foto embebidos) puede pesar varios cientos de KB en base64 —
mucho más de lo que entra cómodo en un solo `System.debug`. Se trocea:

```apex
QuotePdfResultDTO result = QuotePdfService{{SUFFIX}}.generatePdf(Id.valueOf('<quoteId>'));
String b64 = result.base64Data;
System.debug('PDF_LEN:' + b64.length());
Integer chunkSize = 2000;
Integer total = (b64.length() + chunkSize - 1) / chunkSize;
for (Integer i = 0; i < total; i++) {
    Integer start = i * chunkSize;
    Integer stop = Math.min(start + chunkSize, b64.length());
    System.debug('PDF_CHUNK_' + i + ':' + b64.substring(start, stop));
}
System.debug('PDF_CHUNKS_TOTAL:' + total);
```

Guardá este script en un archivo `.apex` (no lo pegues inline en la shell) y ejecutalo con:

```
sf apex run --target-org <org> --file <script>.apex > <log>.log 2>&1
```

Este comando específico (execute anonymous vía SOAP) es el que más sufre el error
transitorio `UNKNOWN_EXCEPTION` de `references/deploy-and-verify.md` — probá primero con un
`System.debug('PING_OK');` trivial si falla, para distinguir "la org está de verdad caída"
de "esta corrida puntual con mucho payload falló". Reintentá 2-3 veces seguidas si el ping
funciona pero el script grande falla — resolvió solo en la sesión de referencia.

## Reensamblar el PDF en PowerShell

```powershell
$log = Get-Content "<log>.log"
$chunks = @{}
foreach ($line in $log) {
    if ($line -match 'PDF_CHUNK_(\d+):(.*)$') {
        $chunks[[int]$matches[1]] = $matches[2]
    }
}
$ordered = 0..($chunks.Count - 1) | ForEach-Object { $chunks[$_] }
$b64 = -join $ordered
[IO.File]::WriteAllBytes("<ruta-scratchpad>\Quote-Preview.pdf", [Convert]::FromBase64String($b64))
```

Guardá el `.pdf` resultante en el directorio scratchpad de la sesión (nunca en carpetas del
usuario tipo Downloads sin permiso).

## Revisar antes de mandarlo

Usá la herramienta `Read` sobre el `.pdf` generado — soporta PDFs y te va a mostrar el
render página por página. Revisalo vos mismo (colores de marca aplicados, logo legible, foto
de producto bien recortada, totales correctos) antes de mandárselo al usuario.

## Entregar al usuario

Usá `SendUserFile` con `display: "render"` para que se vea inline, y un `caption` que diga
qué Quote y qué cliente/marca es. No hace falta subir el archivo a ningún lado ni publicarlo
como artifact — es un archivo de trabajo, no un entregable de Cowork (por eso esta skill no
aplica la política de `pc-meta-artifact-publisher` / regla Q11: el output final vive en
Salesforce como PDF de la Quote, este archivo es sólo la prueba visual de la corrida).

## Limpieza opcional

Si en el camino se creó un `ContentVersion` de prueba en la org (por ejemplo para intentar
la previsualización vía Salesforce Files), borralo al final con Apex anónimo
(`delete [SELECT Id FROM ContentDocument WHERE Id = '<id>']`) para no dejar basura de testing
en la org del cliente/demo.
