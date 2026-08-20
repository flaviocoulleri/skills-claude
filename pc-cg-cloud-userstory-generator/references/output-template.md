# Output Template — Historia de Usuario

Use this exact structure for every User Story you produce. Do not skip sections. If a section doesn't apply, write "N/A" with a brief justification.

---

## Full Example

**Título:** App Offline | Registro de visita con captura fotográfica de anaquel

**Descripción:**
> Como Representante de Ventas en campo
> Quiero registrar una visita y capturar fotos del anaquel desde la app offline
> Para documentar la ejecución en punto de venta y alimentar los indicadores de cobertura

**Criterios de Aceptación:**
1. La pantalla de registro de visita se presenta según el diseño del prototipo adjunto, con los campos y disposición indicados. [Material a consultar: [Prototipo Registro de Visita](https://figma.com/file/xxxxx)]
2. Al abrir la app, el sistema muestra la lista de visitas programadas para el día actual, ordenadas por hora de inicio.
3. Al seleccionar una visita, el sistema presenta el formulario de registro con los campos: Tipo de Visita, Hora de Llegada, y Comentarios.
4. El botón "Capturar Foto" abre la cámara del dispositivo. La foto se almacena asociada al registro de visita con un tamaño no mayor a 2 MB. [Material a consultar: [Diccionario de Datos — Objeto Visit_Photo__c](link-al-DDD)]
4. Si el dispositivo no tiene conexión, el registro y las fotos se guardan localmente y se sincronizan al recuperar conexión.
5. Al guardar el registro, el sistema muestra el mensaje "Visita registrada" y regresa a la lista de visitas.

**Escenarios:**
1. Dado que el representante tiene conexión a internet, Cuando completa el formulario y presiona "Guardar", Entonces el registro se crea en Salesforce y las fotos se suben al Content Document relacionado.
2. Dado que el representante no tiene conexión, Cuando completa el formulario y presiona "Guardar", Entonces el registro se almacena en la base de datos local del dispositivo con estado "Pendiente de sincronización".
3. Dado que el representante intenta guardar sin haber seleccionado Tipo de Visita, Cuando presiona "Guardar", Entonces el sistema muestra el error "El campo Tipo de Visita es obligatorio" y no permite guardar.
4. Dado que la foto excede 2 MB, Cuando el representante la captura, Entonces el sistema la comprime automáticamente antes de almacenarla.
5. Dado que el representante no tiene el permiso "Field_Visit_User", Cuando intenta acceder al módulo de visitas, Entonces el sistema muestra "No tienes permisos para acceder a este módulo".

**Evaluación Funcional y Técnica:**
- Riesgo Técnico: 🟡 Amarilla — CG Offline tiene limitaciones en el manejo de archivos adjuntos. La compresión de fotos debe manejarse con lógica nativa del dispositivo, no con Apex. Verificar el límite de almacenamiento local.
- Alineación: Alineado a la Épica "Ejecución en Punto de Venta"
- Dependencias:
  - HU previa: "App Offline | Configuración de rutas y asignación de visitas" debe estar completada
  - Carga de datos base: Catálogo de Tipos de Visita
  - Configuración: Permission Set "Field_Visit_User" creado y asignado

**Tareas Sugeridas:**
1. **Administrador Salesforce**: Crear el objeto Visit_Photo__c con los campos: Photo_URL__c (URL), Captured_Date__c (DateTime), Visit__c (Lookup). Configurar el Permission Set "Field_Visit_User".
2. **Desarrollador App Offline**: Implementar en Modeler la lógica de captura y compresión de foto. Configurar el almacenamiento local y la cola de sincronización para fotos.
3. **Desarrollador Integraciones**: Implementar el proceso de sincronización que sube las fotos a Content Document y actualiza el campo Photo_URL__c.
4. **Tester**: Validar flujo completo online y offline. Probar con fotos de diferentes tamaños. Verificar sincronización después de pérdida de conexión prolongada (> 4 horas). Verificar restricción de permisos.
5. **PM**: Coordinar con el equipo de infraestructura los límites de almacenamiento en Content Document. Confirmar con el cliente los tipos de visita válidos.

> **Nota:** No se incluyen tareas para el Analista Funcional porque el usuario ES el analista. Las tareas del analista (documentar DDD, definir picklists, etc.) se cubren en el Anexo de este documento o se consultan directamente al usuario.

**Anexo — Diccionario de Datos:**

| Object | Field Label | API Name | Type | Values/Length | Required | Description |
|--------|------------|----------|------|---------------|----------|-------------|
| Visit_Photo__c | Photo URL | Photo_URL__c | URL | 255 | Yes | URL del Content Document |
| Visit_Photo__c | Captured Date | Captured_Date__c | DateTime | — | Yes | Fecha/hora de captura |
| Visit_Photo__c | Visit | Visit__c | Lookup(Visit) | — | Yes | Relación a la visita |
| Visit__c | Visit Type | Visit_Type__c | Picklist | Programada, Espontánea, Auditoría | Yes | Tipo de visita |

---

## Checklist Before Delivering a Story

Before presenting a story to the user, verify:

- [ ] Title follows `[Entorno] | [Descripción]` format
- [ ] Description uses "Como / Quiero / Para" structure
- [ ] Acceptance criteria contain ZERO interpretive adjectives (see Rule 3 for allowed vs. prohibited)
- [ ] Acceptance criteria use field LABELS (user-visible), not API names
- [ ] Acceptance criteria are written in colloquial tone (not Gherkin)
- [ ] Material references are included where needed
- [ ] Scenarios use strict Gherkin format
- [ ] Scenarios cover: happy path, error, App Offline (if applicable), permissions
- [ ] Environment was specified by the user (never assumed)
- [ ] If user specified both Backoffice AND App Offline, it is split into two separate HUs
- [ ] Technical risk is assessed with justification
- [ ] Dependencies are listed
- [ ] Tasks specify the responsible role and include technical detail (API names, etc.)
- [ ] Tasks do NOT include "Analista Funcional" as a role (the user is the analyst)
- [ ] If a prototype was provided, the first criterion references it with a hyperlink
- [ ] DDD appendix is included if new fields are needed
