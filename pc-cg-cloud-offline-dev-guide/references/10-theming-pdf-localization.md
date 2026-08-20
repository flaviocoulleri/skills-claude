# Theming, PDF Reporting y Localization

Llegamos al tramo de acabado y entrega. Una app funcional no alcanza: tiene que verse con la marca del cliente, generar los documentos físicos que el negocio necesita (remitos, reportes de auditoría, invoices), y hablar el idioma de cada usuario. Este módulo cubre las tres capas de personalización final: el theming (apariencia), el PDF reporting (salida en papel/PDF) y la localization (idioma).

## Resumen operativo

- Theming: se gestiona en Sync Management -> Mobile App Themes (modelo RGBA); los temas base no se editan, se clonan en Custom Themes (ver `ref-sync-management.md`).
- PDF (PrintLayoutV2), tres bloques: Declarations (datos), DocumentProperties (props del PDF) y ReportLayout (el XHTML visual). Imagenes via `utils base64encode`.
- Localizacion: el idioma del usuario y la Sales Org apuntan al Locale Contract; fallback a ingles y al `defaultLabel`. Refresca con `refreshLocale` (flag `-c` para el Image Contract).
- Regla: todo texto visible sale del Locale Contract, nunca hardcodeado.

## 1. Tres capas de personalización final

Son tres mecanismos independientes que se aplican casi siempre al final del proyecto. El theming cambia cómo se ve la app (colores, logos). El PDF reporting define la salida documental que el rep genera en la tienda. La localization asegura que cada usuario vea los textos en su idioma. Ninguno toca la lógica de negocio; son la capa de presentación y entrega.

## 2. Theming

La apariencia se personaliza con Themes: grupos de configuraciones que controlan colores de fondo y borde, fuentes y la estructura de los componentes de la UI. Se gestionan en la app Sync Management, pestaña Mobile App Themes (que aparece en el mapa de la Referencia de Sync Management), sobre el modelo de color RGBA, con dos mecanismos:

- Color Macros: definen los colores estándar (por ejemplo Color1 = blanco, rgba(255,255,255,1)). Se configuran en la subpestaña Colors.

- Button Macros: definen fondo, borde y fuente de los botones primarios y secundarios, y pueden referenciar un Color Macro existente. Subpestaña Buttons.

### 2.1 Logos e íconos

- Íconos estáticos: se manejan localmente en el Modeler con un Image Contract (archivos .image.xml en $workspace/src/Images), que soporta .png y .svg. Para incrustar el binario de la imagen dentro del contract (en su bloque CDATA), lo conviertes a Base64 con sf modeler workspace utils base64encode --input <archivo> (p. ej. --input ./logo.svg).

- Logo por Sales Organization: se carga la imagen como ícono directamente en el registro de la Sales Organization en Salesforce, y se extrae con un Binding en el contrato de UI usando el tipo DomBlob.

Una restricción importante: no se pueden modificar los temas base (Salesforce Theme y Salesforce High Contrast Theme). Para personalizar, el administrador los clona, crea un Custom Theme y lo activa.

## 3. PDF Reporting: el contract PrintLayoutV2

Los reportes e invoices en PDF se generan con el contract PrintLayoutV2, escrito en XHTML simple con binding de datos. El archivo vive en el directorio PL (PrintLayout) de un objeto, por ejemplo $workspace/src/MyDisplay/PL/MyDisplayPDF.printlayoutv2.xml. Tiene un nodo raíz PrintLayout con tres partes:

> Diagrama (descrito, no embebido): Estructura de un PrintLayoutV2: Declarations (datos), DocumentProperties (props del PDF) y ReportLayout (el XHTML visual).

- Declarations: declara la interfaz de datos (los Business Objects y las imágenes a inyectar) con el tag DataDeclaration.

- DocumentProperties: las propiedades del documento PDF, por referencia literal o binding.

- ReportLayout: la estructura visual, con etiquetas XHTML soportadas: table, tr, th, td, h1, h2, p, header, footer, y macros de estilo.

## 4. PDF Reporting: invocar PRINTV2 y pasar datos

Desde el Process Contract disparas el reporte con un <Action actionType="PRINTV2">. El atributo printId apunta al layout, locale fija el idioma, showShareButton habilita compartir, y los <Input> del bloque <Parameters> inyectan los datos:

```
<Action name="PrintPDF" actionType="PRINTV2" printId="MyDisplayPDF"
        locale="ApplicationContext::user.languageSpoken" showShareButton="true">
  <Parameters>
    <Input name="currentDisplay" value="ProcessContext::CurrentDisplay" />
    <Input name="loDisplays"     value="ProcessContext::DisplayList" />
  </Parameters>
</Action>
```

En el layout, las variables se resuelven con macros: {{Declarations::[ruta]}} para los datos y {{Labels::[id]}} para los textos traducibles. Nota el <thead> con anchos en porcentaje (obligatorio, ver sección 7):

```
<PrintLayout name="MyDisplayPDF"
             xmlns="https://www.salesforce.com/cgcloud/xsds">
  <Declarations>
    <DataDeclaration name="currentDisplay" type="BoMyDisplay" />
  </Declarations>
  <ReportLayout pageMargins="[30]" pageSize="[216, auto]">
    <h2 alignment="center">
      {{Labels::CurrentDisplayId; defaultLabel=Current Display}}
    </h2>
    <table name="CurrentDisplayTable" tableLayout="noBorders">
      <thead>
        <tr><th width="40%">Campo</th><th width="60%">Valor</th></tr>
      </thead>
      <tbody>
        <tr>
          <td alignment="right">{{Labels::NameId; defaultLabel=Name:}}</td>
          <td alignment="left">{{Declarations::currentDisplay.name}}</td>
        </tr>
      </tbody>
    </table>
  </ReportLayout>
</PrintLayout>
```

La previsualización se dispara cuando el usuario toca un botón de la UI (un evento que el proceso enruta al PRINTV2). El atributo generateAndSave fuerza a escribir el PDF en disco (encriptado o no) y devolver el path en vez de previsualizar. En desarrollo, lo pruebas con el simulador (sf mdl simulate).

## 5. Localization: el Locale Contract

La internacionalización se configura con el Locale Contract, en $workspace/src/Locale. Hay un archivo por idioma (en.locale.xml, de.locale.xml, es.locale.xml) y un archivo central Global Labels.globallabel.xml. Los textos se agrupan en secciones: Global, UserInterfaceContracts y ValidationMessages.

Los labels y las imágenes localizadas se declaran así:

```
<!-- texto traducible -->
<Label id="NameId" text="Nombre:" translationStatus="7" />
 
<!-- imagen alternativa para esta localización -->
<Images>
  <Image id="HeaderLogo" alternativeId="HeaderLogo_de" />
</Images>
```

El translationStatus marca el estado de cada label: 0 inicial, 1 requiere traducción, valores mayores indican traducido/revisado.

## 6. Localization: refreshLocale y resolución

Cuando agregas o modificas labels globales o de framework, corres el comando sf modeler workspace refreshLocale. Ese proceso busca las etiquetas nuevas (las marcadas AUTO-GENERATED), busca traducciones por defecto, e inserta las faltantes en todos los contratos de locale con translationStatus="1" (requiere traducción). Algo crucial: nunca borra labels, solo agrega las que faltan. Si quieres actualizar un solo idioma en lugar de todos, pasas el flag -c con el archivo, por ejemplo refreshLocale -c de.locale.xml.

> Diagrama (descrito, no embebido): Resolución de localización: el usuario y la Sales Org definen el idioma, que apunta al Locale Contract; con fallback a inglés y al defaultLabel.

En runtime, la app determina el idioma según la Sales Organization y el usuario. Si el idioma por defecto de la empresa no coincide con los definidos en la sales org, la UI usa el del campo Language1 de la Sales Org. Si un código de idioma no está cargado, cae al inglés (en). Y en la UI o el PDF, la macro {{Labels::[Id]; defaultLabel=[Fallback]}} usa el defaultLabel si no encuentra el id en el Locale Contract.

## 7. Errores comunes

| Área | Error / limitación y solución |
| --- | --- |
| Theming | El nombre de una macro debe empezar en mayúscula y usar camelCase. Si un componente referencia una macro inexistente, el estilo falla. Un SVG no soportado cae a la imagen estándar del framework. |
| PDF | Las tablas deben tener <thead>, y los <th> llevan width en porcentaje sumando exactamente 100%. Un ancho < 8% o texto en negrita que desborda la celda lanza una excepción en runtime. |
| PDF | No se soportan <div> ni Image dentro de tablas, ni colSpan/rowSpan: rompen el build. eval() está prohibido (impide generar el Deployment Package). La impresión térmica de 3" (ESC/POS) es solo texto: omite caracteres especiales como $, subíndices y negritas largas. |
| PDF | Los Labels en macros son case-sensitive: si yerras la mayúscula, el PDF muestra la macro sin procesar. Si una imagen/firma no resuelve, o hay más de 4 firmas, aparece el ícono de imagen rota. |
| Localization | refreshLocale nunca borra IDs: si eliminas un Global/Framework Label, sigue existiendo en el contrato compilado. Un datetimeFormat fuera de ANSI/ISO 8601 imprime ### en pantalla y PDF. |

## 8. Caso práctico de punta a punta

Cerremos con un entregable real que combina las tres capas: un PDF de auditoría de exhibidor, con la marca del cliente y en el idioma del rep.

- Tema de marca. En Sync Management → Mobile App Themes, clonas el Salesforce Theme, ajustas las Color Macros al color corporativo y las Button Macros, y activas el Custom Theme. El logo de la cadena lo cargas como ícono en su Sales Organization y lo muestras en el header con un Binding DomBlob.

- El reporte. Creas MyDisplayPDF.printlayoutv2.xml en src/MyDisplay/PL: en Declarations declaras el BoMyDisplay, y en ReportLayout armas la tabla (con su <thead> y anchos al 100%) usando {{Declarations::currentDisplay.name}} para los datos y {{Labels::NameId; defaultLabel=Name:}} para los rótulos.

- La invocación. En el proceso, el botón "Generar PDF" dispara un evento que enruta a la acción PRINTV2 con printId="MyDisplayPDF" y locale="ApplicationContext::user.languageSpoken", pasando CurrentDisplay como Input.

- El idioma. Defines NameId y CurrentDisplayId en en.locale.xml y es.locale.xml, corres sf modeler workspace refreshLocale para propagar las faltantes, y verificas los translationStatus. En runtime, un rep en español ve los rótulos en español; uno cuya org no tiene su idioma cae al Language1 de la Sales Org o, en última instancia, al inglés y al defaultLabel.

Leído de corrido: el rep abre la auditoría en una app con los colores y el logo del cliente (theming) → toca "Generar PDF" → el PRINTV2 arma el reporte con los datos del exhibidor (PrintLayoutV2) → los rótulos salen en su idioma (localization), con fallback prolijo si falta alguna traducción → lo comparte desde el botón. Las tres capas, trabajando juntas, convierten una app funcional en un entregable listo para producción.

## 9. Puntos clave

- Theming: se hace en Sync Management → Mobile App Themes con Color y Button Macros (RGBA). Los íconos van por Image Contract (.png/.svg); el logo por Sales Org con Binding DomBlob. Los temas base no se editan: se clonan.

- PDF: el PrintLayoutV2 (XHTML) tiene Declarations, DocumentProperties y ReportLayout. Vive en el directorio PL del objeto.

- Se invoca con un Action PRINTV2 (printId, locale, showShareButton, Parameters); los datos se resuelven con {{Declarations::…}} y los textos con {{Labels::…}}.

- Regla del PDF: las tablas necesitan <thead> con anchos en % sumando 100%; nada de div/Image/colSpan/rowSpan en tablas; los Labels son case-sensitive.

- Localization: el Locale Contract (un archivo por idioma + global) define Labels e imágenes; refreshLocale agrega las faltantes (translationStatus=1) y nunca borra.

- Resolución: idioma por Sales Org + usuario, con fallback a Language1, luego a inglés (en), y la macro usa defaultLabel si no encuentra el id.

## Checklist de verificacion

- Los temas los clonaste en Custom Themes (no tocaste los base).
- PrintLayoutV2: separaste Declarations / DocumentProperties / ReportLayout.
- Todo texto visible viene del Locale Contract (con defaultLabel de fallback), sin hardcodear.
- Refrescaste locale/imagenes con `refreshLocale` cuando cambiaste textos.
