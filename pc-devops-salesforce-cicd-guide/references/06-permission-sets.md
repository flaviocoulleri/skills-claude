# 06 · Permission Sets exclusivos

> Fuente canónica: Confluence PROCMOD — "Manejo de Seguridad Estándar: Exclusividad de Permission Sets" (`2082209816`). Política oficial: **mínimo privilegio basado exclusivamente en Permission Sets y Permission Set Groups** — nunca Profiles para permisos operativos.

## El dolor de los Profiles

Los Profiles son colecciones monolíticas enormes (`Admin.profile-meta.xml` puede pesar 10 MB). Hacer commit de un Profile versiona **todos** sus tags OLS/FLS/Tab Settings/IP Ranges.

- **Problema con source-tracking:** traer Profiles genera caos en Git. Dos devs commiteando el mismo Profile producen **conflictos de merge que destruyen metadata e introducen agujeros de seguridad accidentales**.

## La solución: Permission Sets

Todos los permisos de nuevos desarrollos (FLS, acceso a objetos, VF Pages) van **exclusivamente** por Permission Sets.

**Reglas de oro para todo nuevo desarrollo:**

1. **Perfil base mínimo y genérico** (*Minimum Access Profile*): los Profiles solo asignan **Licencias, Rangos de IP y Visualforce Pages default**. **No** se usan para otorgar permisos operativos.
2. **Permission Sets modulares:** cada feature o rol tiene su propio Permission Set (ej. `Permisos_Ejecutivo_Ventas`, `Acceso_LWC_Calculadora`).
3. **Control de FLS:** al crear un campo, **quitarle la visibilidad a todos los profiles** en la UI de creación e **inmediatamente incluirlo en un Permission Set** en VSCode para trackearlo en el CI/CD.
4. **🔴 Exclusión estricta (`.forceignore`):** el `.forceignore` está configurado para **ignorar toda metadata `*.profile-meta.xml`**. Si intentas arrastrar un Profile entero al código local, el pipeline **no lo sube**.

## Permission Set Groups

Para no asignar 50 Permission Sets por persona, se crean **PermissionSetGroups**: un grupo paquetiza conjuntos granulares (ej. `Ventas Básico` + `Soporte Medio`) en un solo paquete, que es el que se asigna al usuario final desde Setup.

## Regla inflexible

**Todo deploy de feature que incluya nuevos campos/objetos DEBE venir acompañado de la creación/modificación de un `<PermissionSet>`.** Si tu PR incluye `CustomObjects` pero **no** `PermissionSets`, nadie tendrá acceso una vez desplegado en Producción.

> Si el usuario insiste en tocar Profiles para FLS de features nuevos, advertir y citar esta página (`2082209816`).
