# Índice de presentaciones base de delivery (cache)

> **Qué es esto.** Un índice cacheado de las presentaciones base de **delivery** curadas en Drive
> (kickoff, steering, status, cierre, retros). **Drive es siempre la fuente de verdad** — este
> archivo es sólo una caché. El skill lo lee primero para mostrar opciones al instante y lo
> reconcilia contra Drive en runtime.

## Cómo se usa (lógica del skill)

1. Al entrar al sub-flujo base-Drive (Paso 1B), **lee este índice primero** y muestra las opciones (Patrón C).
2. **En paralelo, reconcilia contra Drive**: `search_files` recursivo en la carpeta raíz
   `1Tdy-IVpVhDmMECODq_bhZBdIfS5wqu_F` y subcarpetas (todos los archivos no-trashed). Compara por `fileId`:
   - Archivo nuevo en Drive que no está acá → agrégalo (clasifica `hito`/`tags` por el nombre).
   - Archivo del índice que ya no está en Drive (o quedó trashed) → quítalo.
   - Nombre/ubicación cambió → refresca la fila.
3. Si el índice y Drive divergen, **gana Drive**. Reescribí este archivo y actualiza `last_refreshed`.
4. Si Drive no responde, usa el índice como fallback y avisa en una línea que puede estar desactualizado.

**Regla de frescura:** si `last_refreshed` tiene más de 7 días, fuerza una reconciliación completa antes de mostrar opciones.

## Esquema de cada fila

| Campo | Significado |
|---|---|
| `nombre` | Nombre del archivo en Drive. |
| `hito` | Hito del proyecto al que aplica (Kickoff / Sprint review / Steering / Status / Cierre-Aceptación / Retro). `—` si es transversal. |
| `tags` | Etiquetas para filtrar fino (`kickoff`, `status`, `steering`, `cierre`, `retro`, `institucional`, `recurso`). |
| `para_que_sirve` | Una línea: cuándo conviene usar esta base. |
| `ubicacion` | Subcarpeta actual en Drive (`(raíz)` = suelto en la carpeta principal). |
| `fileId` | ID de Drive — clave única para reconciliar. |

---

## Delivery — carpeta `1Tdy-IVpVhDmMECODq_bhZBdIfS5wqu_F`

<!-- last_refreshed: nunca — el skill completa esta sección en su primera corrida contra Drive -->

| nombre | hito | tags | para_que_sirve | ubicacion | fileId |
|---|---|---|---|---|---|
| _(pendiente de primera reconciliación con Drive)_ | | | | | |
