# 02 · Ambientes y mapping orgs ↔ ramas

> Fuente canónica: Confluence PROCMOD — "Salesforce Orgs y Git" (`2082111511`). Cada ambiente tiene un propósito y una rama asociada; la estructura final se define al inicio de cada proyecto.

La cantidad y tipo de ambientes depende del tamaño del proyecto, su complejidad y las licencias disponibles. Cada ambiente cumple un propósito específico y **debe estar vinculado a una rama** para garantizar trazabilidad y orden en los despliegues.

## Modelo propuesto (orgs ↔ ramas)

| Org | Tipo | Acceso cliente | Rama | Propósito |
|---|---|---|---|---|
| **dev** | Sandbox Developer | no | `develop` | Desarrollo (programático Apex/LWC y declarativo Flows/Validation Rules). Implementación inicial de requerimientos. **No** se hacen pruebas funcionales/automatizadas acá. |
| **test** | Sandbox Developer / Developer Pro | no | `test` | Entorno integrador: consolida los cambios de dev. QA ejecuta pruebas funcionales y automatizadas. Pueden surgir correcciones antes de promover. |
| **qa** | Sandbox Developer Pro / Partial Copy | sí | `qa` | Recibe lo probado y aprobado por QA interno. **Primer entorno accesible por el cliente** para revisión/aprobación de requerimientos. |
| **uat** | Sandbox Partial Copy / Full Copy | sí | `uat` | Pruebas de aceptación final y de carga. Data lo más cercana posible a producción. Último paso de validación pre-productivo. |
| **productivo** | Producción | sí | `master` / `main` | Ejecución real. Solo llegan cambios validados y aprobados en los ambientes anteriores. |

> El diseño final se define al inicio de cada proyecto y **se adapta** a las licencias/necesidades: no todos los clientes tienen Full Copy, y a veces QA y UAT no se diferencian.

## Política de refresco de Sandboxes

Los Sandboxes se desincronizan de la metadata y data viva de Producción con el tiempo. Refrescar es **mandatorio** pero requiere coordinación:

- **Cuándo refrescar:** al finalizar la salida a Producción de un Release mayor, o al iniciar un Sprint crítico (recomendado para `dev` y `test`).
- **🔴 Regla de oro (¡cuidado con la metadata!):** antes de gatillar el refresco, **todo el equipo debe haber extraído y resguardado en Git** sus configuraciones "en vuelo". Un refresco **destruye la Org entera** — borra para siempre cualquier layout, flow o clase que viviera solo en el Sandbox y no se haya hecho `retrieve`.
- **Post-refresco (re-alineación):** el nuevo Sandbox nace **sin** la config CI/CD. Hay que **re-inyectar/reactivar las External Client Apps, los usuarios técnicos y re-asignar los Permission Sets de integración** (ver módulo 05). Avisar siempre esto tras un refresh.

## Referencias

- Diagrama de ambientes: https://drive.google.com/file/d/1AZIwaRvT1A2zAFqFszzy692AW1U9b348/view
