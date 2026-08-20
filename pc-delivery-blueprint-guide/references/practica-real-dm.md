# Práctica real del DM — patrones observados en campo

> **Fuente y estatus:** patrones extraídos del análisis de ~92 reuniones reales de un Delivery Manager de ProContacto (enero–julio 2026, múltiples proyectos incluyendo CMI, GeoVictoria, Experian, SMU/ALVI, Aeropuertos Argentina). **NO son canon del deck Blueprint v2** — son práctica recomendada validada por observación. Al citarlos, aclarar que son "práctica recomendada", no regla de la metodología.

## 1. Protocolo de escalamiento en capas

Diseñado por un DM real para no saturar a los referentes especializados (4-5 personas cubriendo ~8 equipos). Orden obligatorio antes de escalar:

1. **IA / documentación** — agotar Claude, Confluence, documentación del proyecto.
2. **Compañeros del equipo** — consulta lateral dentro del nodo.
3. **PM / líder del nodo** — si el equipo no lo resuelve.
4. **Referente especializado** (admin / dev / QA / análisis) — **último recurso**.

Recomendarlo en kickoffs internos y cuando un PM pregunte "a quién le pregunto X".

## 2. Comité operativo semanal con métricas cuantitativas

El patrón de reporting más consistente observado (todas las instancias de CMI). En fase de ejecución, el DM reporta semanalmente al cliente:

- Backlog cuantificado: **abiertos / en progreso / listos para validar / cerrados**.
- Clasificación de tickets: **error (defecto) / modificación simple (cambio) / limitación de plataforma / permiso**.
- **% de avance real vs. plan** (ej. 61% real vs 62% plan).
- Criterio de secuenciación explícito (ej. "primero los N errores críticos salvo bloqueantes").

Template: `templates/status-semanal.md`. Este ritual refuerza la disciplina defecto≠mejora de la metodología ante el cliente, semana a semana.

## 3. El go-live no es el final: venta de soporte post-hypercare

Actividad real y esperada del DM en F5 que el deck no nombra: **en paralelo al cierre del proyecto, el DM abre la conversación comercial de soporte**. El hypercare (1-2 semanas, solo defectos) es la ventana para que el cliente dimensione lo que significa operar sin equipo — el DM debe:

1. Recordar al cliente desde el kickoff de F5 que el hypercare es acotado y el soporte es contrato aparte (la metodología ya lo dice).
2. Cuantificar durante el hypercare el volumen de tickets/consultas que seguirá llegando después.
3. Conectar con el AE/comercial ANTES de que termine el hypercare para que la propuesta de soporte llegue con el proyecto aún caliente.

Sin esto, el cierre deja un vacío de atención que deteriora la relación (y el revenue de la etapa Operar, que es el piso de revenue de ProContacto).

## 4. Definir garantía vs. control de cambios ANTES del go-live

Fricción real observada: la frontera entre garantía (defectos sin costo), hypercare y control de cambios se terminó negociando ad-hoc en llamadas improvisadas releyendo el contrato. Práctica recomendada: **cerrar por escrito, antes del go-live, el acuerdo de garantía** usando `templates/garantia-vs-cambios.md`. En proyectos multi-salida (varios países/oleadas), definir el hypercare **por salida** explícitamente — el contrato genérico "1 mes de hypercare" es ambiguo con 9 salidas.

## 5. Matriz de responsables por rol (no por persona)

Fricción real observada: la rotación de personal del cliente impide fijar responsables por nombre (tickets sin dueño, decisiones huérfanas). Práctica recomendada: desde Sprint 0, la matriz de responsables del cliente se define **por rol** con la persona actual como instancia, y se revisa en cada comité (template: `templates/matriz-responsables-rol.md`). Complementa la limitante 12 (continuidad de decisiones): el rol hereda las decisiones aunque cambie la persona.

## 6. Densidad del Sprint 0 (calculadora)

Fricción real observada: Sprint 0 que ya nace excedido (50-70 sesiones estimadas en 6-7 semanas) y la conversación gira en "cómo comprimir" en vez de "qué recortar". Chequeo recomendado al planificar la parrilla de la semana 1:

```
densidad = (nº de dominios/procesos × sesiones por dominio) / semanas disponibles
```

- **> 10 sesiones/semana sostenidas → alerta roja**: no comprimir el calendario; **recortar alcance** (diferir dominios a fase 2) o replantear el tamaño del proyecto con el AE. La metodología ya lo respalda: el Sprint 0 no se extiende, y lo que no se define se excluye o difiere.
- Recordar que el Sprint 0 canónico es de nodo de 3 con dedicación completa: una parrilla que requiere más gente es señal de un G1 mal cerrado.
