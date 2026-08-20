# 10 · Conflictos de merge

> Fuente canónica: Confluence PROCMOD — "Resolución de Conflictos Masivos en Git" (`2082111518`).

Al versionar metadata de Salesforce (XMLs gigantes), los conflictos de merge son comunes. Layouts, Custom Objects, package.xml suelen romperse si dos devs los alteran a la vez.

## ¿Qué es un conflicto de merge?

Git detecta que la misma línea fue modificada de formas distintas en origen y destino y no puede decidir automáticamente cuál es la correcta.

## Tipos comunes en Salesforce

### 1. XMLs de metadata (Layouts, Objetos)

Dos personas agregan campos distintos a una página:

```xml
<<<<<<< HEAD
<layoutItems>
    <behavior>Edit</behavior>
    <field>Campo_de_Juan__c</field>
</layoutItems>
=======
<layoutItems>
    <behavior>Readonly</behavior>
    <field>Campo_de_Maria__c</field>
</layoutItems>
>>>>>>> feature/PROC-200
```

**Resolución correcta:** a diferencia del Apex (donde te quedas con una lógica u otra), en los XML de Salesforce **generalmente quieres conservar AMBOS bloques** de las distintas features. Editar manualmente para mantener nodos XML válidos con ambas sumatorias y **purgar los marcadores** `<<<<`, `====`, `>>>>`.

### 2. `package.xml`

Varios devs agregan componentes a sus manifiestos y al juntarlos rompen el tag `<types>`. Resolver **manteniendo a todos los `<members>` en orden alfabético** para no repetirlos.

## Herramientas

- **Nunca** resolver conflictos enormes en el editor de texto plano de Bitbucket.
- Usar el **Merge Editor interactivo de VSCode**: abrir los archivos en rojo del panel de Git; elegir **Accept Both Changes** cuando sean adiciones conjuntas (ej. dos campos nuevos), o el correcto si fue una modificación sobrepuesta de lógica.

## 🔴 Regla de oro post-merge

Si rompes la estructura del XML resolviendo torpemente (un `<` sin cerrar, una etiqueta suelta), el pipeline **explota** con `Malformed XML` o pierde metadata. **Siempre correr `sf project deploy validate` local después de un merge ruidoso, antes de pushear.**

> `git merge`/`git rebase` son **write** → pedir ✅. La validación `sf project deploy validate --dry-run` es read-only → se corre sin permiso.
