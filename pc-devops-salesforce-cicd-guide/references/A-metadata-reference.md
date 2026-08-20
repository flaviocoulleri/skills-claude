# Anexo A · Referencia de metadata de Salesforce

> Fuente canónica: Confluence PROCMOD — "Referencia de Metadata de Salesforce" (`2084012041`). Documenta, por cada acción de configuración en SF, qué metadata XML se genera y cómo descargarla con `sf`. Formato **SFDX Source** (descompuesto) en `force-app/main/default/`. Los Metadata Type son los valores que van en `package.xml` y en `--metadata`.

## 1. Modelo de Datos (Objetos y Campos)

| # | Acción (Setup) | Metadata Type · Ruta SFDX | Retrieve |
|---|---|---|---|
| 1.1 | Objeto Custom | `CustomObject` `objects/MiObjeto__c/MiObjeto__c.object-meta.xml` (+ `CustomField` Name, `Layout`, `ListView` All, `CustomTab`) | `--metadata CustomObject:MiObjeto__c` · `CustomTab:MiObjeto__c` |
| 1.2 | Campo custom en objeto custom | `CustomField` `objects/MiObjeto__c/fields/MiCampo__c.field-meta.xml` (+ `Layout`) | `CustomField:MiObjeto__c.MiCampo__c` |
| 1.3 | Campo custom en objeto **standard** | `CustomField` `objects/Account/fields/MiCampo__c.field-meta.xml` (+ `Layout`) — no se baja el `.object-meta.xml` del standard, solo los componentes custom | `CustomField:Account.MiCampo__c` |
| 1.4 | Relación (Lookup / Master-Detail) | `CustomField` (+ `Layout` hijo y padre con Related List) | `CustomField:MiObjeto__c.Account__c` |
| 1.5 | Record Type | `RecordType` `objects/MiObjeto__c/recordTypes/...` (+ `BusinessProcess`, `Layout`, `PermissionSet`) | `RecordType:MiObjeto__c.MiRecordType` · `BusinessProcess:MiObjeto__c.MiProceso` |
| 1.6 | Picklist / Global Value Set | `GlobalValueSet` `globalValueSets/...` · `CustomField` (local) · `StandardValueSet` `standardValueSets/Industry...` | `GlobalValueSet:MiGlobalPicklist` · `StandardValueSet:Industry` |
| 1.7 | Validation Rule | `ValidationRule` `objects/MiObjeto__c/validationRules/...` | `ValidationRule:MiObjeto__c.MiRegla` |
| 1.8 | Compact Layout | `CompactLayout` `objects/MiObjeto__c/compactLayouts/...` | `CompactLayout:MiObjeto__c.MiCompact` |
| 1.9 | Field Set | `FieldSet` `objects/MiObjeto__c/fieldSets/...` | `FieldSet:MiObjeto__c.MiFieldSet` |
| 1.10 | Index / External ID / Unique | `CustomField` (modifica el campo: `<externalId>true</externalId>` / `<unique>true</unique>`) | — |
| 1.11 | Formula / Roll-Up Summary | `CustomField` con `<type>Formula</type>` o `Summary` | — |

## 2. Interfaz de Usuario (Layouts, Pages, Apps)

| # | Acción | Metadata Type · Ruta | Retrieve |
|---|---|---|---|
| 2.1 | Page Layout | `Layout` `layouts/MiObjeto__c-MiLayout.layout-meta.xml` | `Layout:MiObjeto__c-MiLayout` |
| 2.2 | Lightning App | `CustomApplication` `applications/MiApp.app-meta.xml` | `CustomApplication:MiApp` |
| 2.3 | Lightning Page (FlexiPage) | `FlexiPage` `flexipages/MiPagina.flexipage-meta.xml` | `FlexiPage:MiPagina` |
| 2.4 | Home Page Layout | `HomePageLayout` / `HomePageComponent` | — |
| 2.5 | Custom Tab (Objeto/Web/LWC/VF) | `CustomTab` `tabs/....tab-meta.xml` | `CustomTab:MiObjeto__c` |
| 2.6 | Custom Label | `CustomLabels` `labels/CustomLabels.labels-meta.xml` (**archivo único** para todas) | `CustomLabels` |
| 2.7 | Path / Sales Path | `PathAssistant` `pathAssistants/...` | — |
| 2.8 | Global / Quick Action | `QuickAction` `quickActions/...` o `objects/.../quickActions/...` | `QuickAction:MiAccion` · `QuickAction:MiObjeto__c.MiAccion` |
| 2.9 | Custom Buttons / Links | `WebLink` `objects/MiObjeto__c/webLinks/...` | `WebLink:MiObjeto__c.MiBoton` |
| 2.10 | Static Resource | `StaticResource` `staticresources/...` (+ binario `.zip`/`.js`/`.css`) | `StaticResource:MiRecurso` |
| 2.11 | ListView | `ListView` `objects/MiObjeto__c/listViews/...` — las "Visible solo para mí" NO son recuperables | `ListView:MiObjeto__c.MiVista` |

## 3. Lógica de Negocio y Automatización

| # | Acción | Metadata Type · Ruta | Retrieve |
|---|---|---|---|
| 3.1 | Flow (Screen/Record-Triggered/Scheduled/Autolaunched) | `Flow` `flows/MiFlow.flow-meta.xml` | `Flow:MiFlow` · `Flow` (todos) |
| 3.2 | Workflow Rule (legacy) | `Workflow` `workflows/MiObjeto__c.workflow-meta.xml` (Alert/FieldUpdate/Task/OutboundMessage **inline**) | `Workflow:MiObjeto__c` |
| 3.3 | Approval Process | `ApprovalProcess` `approvalProcesses/MiObjeto__c.MiApproval...` | `ApprovalProcess:MiObjeto__c.MiApproval` |
| 3.4 | Process Builder (legacy) | Se almacena como `Flow` (igual que 3.1) | — |
| 3.5 | Assignment Rules (Lead/Case) | `AssignmentRules` `assignmentRules/Case.assignmentRules-meta.xml` | `AssignmentRules:Case` · `AssignmentRules:Lead` |
| 3.6 | Escalation Rules (Case) | `EscalationRules` `escalationRules/Case...` | `EscalationRules:Case` |
| 3.7 | Auto-Response Rules (Lead/Case) | `AutoResponseRules` `autoResponseRules/Case...` | `AutoResponseRules:Case` |

## 4. Seguridad y Acceso

| # | Acción | Metadata Type · Ruta | Retrieve |
|---|---|---|---|
| 4.1 | Permission Set | `PermissionSet` `permissionsets/MiPermSet.permissionset-meta.xml` (object/field perms, tabs, user perms, RT visibility, app/class/page access, custom perms) | `PermissionSet:MiPermSet` |
| 4.2 | Permission Set Group | `PermissionSetGroup` `permissionsetgroups/...` | `PermissionSetGroup:MiGrupo` |
| 4.3 | Muting Permission Set (dentro de un PSG) | `MutingPermissionSet` `permissionsets/MiGrupo_Muting...` | — |
| 4.4 | Profile | `Profile` `profiles/Admin.profile-meta.xml` — **enormes y propensos a conflictos; preferir Permission Sets** (ver módulo 06) | `Profile:Admin` |
| 4.5 | Sharing Rules (Owner/Criteria) | `SharingOwnerRule` / `SharingCriteriaRule` `sharingRules/MiObjeto__c...` | `SharingRules:MiObjeto__c` |
| 4.6 | Org-Wide Defaults (OWD) | `Settings` `settings/Sharing.settings-meta.xml` | — |
| 4.7 | Role (jerarquía) | `Role` `roles/MiRol.role-meta.xml` | `Role:MiRol` |
| 4.8 | Public Group / Queue | `Group` `groups/...` · `Queue` `queues/...` | `Group:MiGrupo` · `Queue:MiCola` |
| 4.9 | Custom Permission | `CustomPermission` `customPermissions/...` | `CustomPermission:MiPermiso` |
| 4.10 | Restriction / Scoping Rules | `RestrictionRule` `restrictionRules/...` | — |

## 5. Reportes, Dashboards y Analytics

| # | Acción | Metadata Type · Ruta | Retrieve |
|---|---|---|---|
| 5.1 | Report / Report Type | `Report` `reports/MiCarpeta/...` · `ReportFolder` · `ReportType` `reportTypes/...` | `Report:MiCarpeta/MiReporte` · `ReportType:MiTipoReporte` |
| 5.2 | Dashboard | `Dashboard` `dashboards/MiCarpeta/...` · `DashboardFolder` | `Dashboard:MiCarpeta/MiDashboard` |
| 5.3 | CRM Analytics (Einstein/Tableau) | `WaveApplication` `.wapp` · `WaveDashboard` `.wdash` · `WaveDataflow` `.wdf` · `WaveDataset` `.wds` · `WaveLens` `.wlens` · `WaveTemplateBundle` | — |

## 6. Código Personalizado (Apex, LWC, Aura, VF)

| # | Acción | Metadata Type · Ruta | Retrieve |
|---|---|---|---|
| 6.1 | Apex Class | `ApexClass` `classes/MiClase.cls` + `.cls-meta.xml` | `ApexClass:MiClase` |
| 6.2 | Apex Trigger | `ApexTrigger` `triggers/MiTrigger.trigger` + `.trigger-meta.xml` | `ApexTrigger:MiTrigger` |
| 6.3 | LWC | `LightningComponentBundle` `lwc/miComponente/` (js, html, css, `.js-meta.xml`, `__tests__/`) | `LightningComponentBundle:miComponente` |
| 6.4 | Aura Component | `AuraDefinitionBundle` `aura/MiComponente/` (.cmp, Controller.js, Helper.js, .css) | `AuraDefinitionBundle:MiComponente` |
| 6.5 | Visualforce Page / Component | `ApexPage` `pages/MiPagina.page` + meta · `ApexComponent` `components/...` | `ApexPage:MiPagina` · `ApexComponent:MiComp` |

## 7. Integración y Servicios Externos

| # | Acción | Metadata Type · Ruta | Retrieve |
|---|---|---|---|
| 7.1 | Connected App | `ConnectedApp` `connectedApps/...` | `ConnectedApp:MiConnApp` |
| 7.2 | Named / External Credentials | `NamedCredential` `namedCredentials/...` · `ExternalCredential` `externalCredentials/...` | `NamedCredential:MiCredencial` · `ExternalCredential:MiExtCred` |
| 7.3 | Remote Site Settings | `RemoteSiteSetting` `remoteSiteSettings/...` | `RemoteSiteSetting:MiSitio` |
| 7.4 | External Service (OpenAPI) | `ExternalServiceRegistration` `externalServiceRegistrations/...` | — |
| 7.5 | External Data Sources / External Objects | `ExternalDataSource` `dataSources/...` · `CustomObject` `objects/MiObjeto__x/...` | — |
| 7.6 | Custom Settings | `CustomObject` `objects/MiSetting__c/...` — la definición es metadata; los **registros/datos NO** (cargar aparte) | — |

## 8. Comunicaciones (Email, Notificaciones)

| # | Acción | Metadata Type · Ruta | Retrieve |
|---|---|---|---|
| 8.1 | Email Templates | `EmailTemplate` (Lightning `emailTemplates/...` o Classic `email/...`) · `EmailFolder` | `EmailTemplate:MiCarpeta/MiTemplate` |
| 8.2 | Letterhead | `Letterhead` `letterhead/...` | — |
| 8.3 | Custom Notifications | `CustomNotificationType` `notificationtypes/...` | `CustomNotificationType:MiNotificacion` |

## 9. Experience Cloud (Comunidades / Sites)

| Componente | Metadata Type · Ruta |
|---|---|
| Network (definición del site) | `Network` `networks/MiSitio.network-meta.xml` |
| Site Definition | `CustomSite` `sites/MiSitio.site-meta.xml` |
| Experience Bundle | `ExperienceBundle` `experiences/MiSitio1/` (directorio) |
| Navigation Menu | `NavigationMenu` `navigationMenus/...` |
| Audience | `Audience` `audience/...` |

Generan mucha metadata interrelacionada → conviene retrieve completo del bundle: `--metadata Network:MiSitio` · `ExperienceBundle:MiSitio1` · `CustomSite:MiSitio`.

## 10. Gestión de Datos (Duplicate, Matching)

| # | Acción | Metadata Type · Ruta | Retrieve |
|---|---|---|---|
| 10.1 | Duplicate Rules | `DuplicateRule` `duplicateRules/MiObjeto__c.MiDupRule...` | `DuplicateRule:MiObjeto__c.MiDupRule` |
| 10.2 | Matching Rules | `MatchingRule` `matchingRules/MiObjeto__c...` | `MatchingRules:MiObjeto__c` |

## 11. Service Cloud (Cases, Knowledge, Entitlements)

- **11.1 Case Management (combinado):** `AssignmentRules`/`EscalationRules`/`AutoResponseRules` (Case), `Layout` (Case-*), `RecordType` (Case), `BusinessProcess` (Support Process), `CustomField` (Case).
- **11.2 Knowledge:** `Settings` `settings/Knowledge.settings-meta.xml` · `CustomObject` `objects/Knowledge__kav/...`.
- **11.3 Entitlements / Milestones:** `EntitlementProcess` `entitlementProcesses/...` · `MilestoneType` `milestoneTypes/...`.

## 12. Sales Cloud (Leads, Opportunities, Forecasting)

- **12.1 Lead/Sales Process:** `BusinessProcess` en `objects/Lead/businessProcesses/...` y `objects/Opportunity/businessProcesses/...`.
- **12.2 Lead Assignment & Auto-Response:** `AssignmentRules:Lead` · `AutoResponseRules:Lead`.
- **12.3 Products / Price Books:** solo los **campos custom** (`CustomField` en `Product2`, `PricebookEntry`) y layouts son deploy-ables; los registros de Products/Price Books son **datos, no metadata**.

## 13. Plataforma Avanzada (Platform Events, Big Objects, CMT)

| # | Acción | Metadata Type · Ruta | Retrieve |
|---|---|---|---|
| 13.1 | Platform Event | `CustomObject` `objects/MiEvento__e/...` (+ `CustomField`) | `CustomObject:MiEvento__e` |
| 13.2 | Custom Metadata Type (CMT) | `CustomObject` `objects/MiConfig__mdt/...` · `CustomMetadata` `customMetadata/MiConfig.MiRegistro.md-meta.xml` — **los registros CMT SÍ son metadata** (ideales para config que migra entre ambientes) | `CustomObject:MiConfig__mdt` · `CustomMetadata:MiConfig.MiRegistro` · `CustomMetadata:MiConfig` (todos) |
| 13.3 | Big Object | `CustomObject` `objects/MiBigObj__b/...` | — |
| 13.4 | Org-level Settings | `AccountSettings`/`CaseSettings`/`SecuritySettings`/`OrgPreferenceSettings`/... `settings/*.settings-meta.xml` | `Settings` |
| 13.5 | Translation / Object Translation | `CustomObjectTranslation` `objectTranslations/MiObjeto__c-es/...` · `Translations` `translations/es.translation-meta.xml` | `CustomObjectTranslation:MiObjeto__c-es` · `Translations:es` |

## 14. OmniStudio / Industries

Requiere habilitar **"OmniStudio Metadata"** en Setup para que sean recuperables vía Metadata API.

| Componente | Metadata Type · Ruta |
|---|---|
| OmniScript | `OmniScript` `omniScripts/...` |
| OmniProcess | `OmniProcess` (varía) |
| OmniDataTransform | `OmniDataTransform` `omniDataTransforms/...` |
| OmniUiCard (FlexCard) | `OmniUiCard` `omniUiCards/...` |
| OmniIntegrationProcedure | `OmniIntegrationProcedure` (varía) |

## 15. Metadata NO Soportada / Configuración Manual

Estos NO son recuperables vía Metadata API — requieren config manual post-deploy:

| Configuración | Razón | Workaround |
|---|---|---|
| List Views privadas | No accesibles vía API | Crearlas públicas |
| Org-Wide Email Addresses | No soportado | Config manual por org |
| Algunos Settings de LEX | Parcial | Verificar Metadata Coverage |
| Data Cloud Configurations | Limitado | Config manual |
| Scheduled Jobs (CronTrigger) | No es metadata | Re-programar manual o vía Apex |
| Live Agent (Chat) routing | Parcial | Validar en org destino |
| User records y asignaciones | Son datos | Data Loader / Scripts |
| Connected App secrets/tokens | Sensible / no exportable | Regenerar por ambiente |
| Feature Licenses assignments | Datos de usuario | Asignar manual |
| Forecasting Configuration | Parcial | Config manual |
| File / Content Assets privados | No accesibles | Subir manual |

> **Siempre consultar el Metadata Coverage Report** para verificar si un componente es soportado antes de incluirlo en el pipeline.

## 16. Comandos generales de retrieve

**Con `package.xml`** (recomendado para proyectos completos):

```xml
<!-- manifest/package.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
  <types><members>*</members><name>CustomObject</name></types>
  <types><members>*</members><name>CustomField</name></types>
  <types><members>*</members><name>Layout</name></types>
  <types><members>*</members><name>Flow</name></types>
  <types><members>*</members><name>PermissionSet</name></types>
  <types><members>*</members><name>ApexClass</name></types>
  <types><members>*</members><name>ApexTrigger</name></types>
  <types><members>*</members><name>LightningComponentBundle</name></types>
  <version>62.0</version>
</Package>
```

```bash
# Con package.xml
sf project retrieve start --manifest manifest/package.xml --target-org mi-org

# Por tipo completo / componente específico / múltiples tipos
sf project retrieve start --metadata ApexClass --target-org mi-org
sf project retrieve start --metadata ApexClass:MiClase --target-org mi-org
sf project retrieve start --metadata ApexClass ApexTrigger LightningComponentBundle --target-org mi-org

# Todo un source dir (genera package.xml automático)
sf project retrieve start --source-dir force-app --target-org mi-org

# Listar tipos / componentes disponibles en una org (read-only)
sf org list metadata-types --target-org mi-org
sf org list metadata --metadata-type ApexClass --target-org mi-org
```
