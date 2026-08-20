# Métricas, roadmap de adopción y evolución de los nodos

Fuente: deck "ProContacto Blueprint v2", slides 17–22.

## Cómo sabremos que funciona (métricas de gobernanza)

1. **Lead time firma → go-live: reducción ≥ 40%** vs baseline.
2. **% de proyectos rechazados en G1** — tiende a **cero** con catálogo maduro.
3. **100% de pedidos post-freeze** capturados como CR cobrado o fase 2.
4. **Tasa de rechazo de la revisión humana por HU** — mide la calidad del pipeline de IA.
5. **NPS del cliente** — la disciplina de alcance **no debe deteriorar la relación**.

## Roadmap de adopción

| Cuándo | Qué |
|---|---|
| Mes 1 | Catálogo de unidades, plantillas y cláusulas con legales. Entrenar a comercial en venta con wireframes |
| Mes 2–3 | Piloto: 1 nodo dividido en 2, con 2–3 proyectos nuevos de tamaño medio. Medir todo |
| Mes 4 | Retrospectiva del piloto, ajuste de catálogo, gates y cláusulas. Decisión de rollout |
| Mes 5+ | Rollout gradual al resto de los nodos. **Los proyectos legacy terminan con el modelo anterior** |

## Evolución de los nodos

| Momento | Personas | Estructura | vs hoy |
|---|---|---|---|
| Hoy (baseline) | 8 | 1 nodo | — |
| Fase 1 · Vibe Coding | 6 | 2 nodos × 3 | −25% |
| Fase 2 · Agentes autónomos | 4 | 2 nodos × 2 | −50% |

### Fase 1 — Vibe Coding · Cowork (el humano dirige, Claude ejecuta)

Nodos de 3 con estos perfiles — **los skills no cambian, cambia quién los invoca**:

- **PM / Analista** — skills de HUs, análisis y relevamiento
- **Configurador** — skills de campos y configuración Salesforce
- **Dev** — skills de LWC, Apex y código personalizado

### Fase 2 — Agentes autónomos (el agente hace lo que hoy hace el humano)

Ciclo del agente: (1) lee el ticket en Jira → (2) selecciona el skill correspondiente → (3) ejecuta sin intervención humana → (4) cierra el ticket.

Composición del nodo 2×2: **PM/Analista + perfil técnico** por nodo.

## El nuevo rol del equipo: de ejecutores a directores

El trabajo no desaparece — cambia quién lo hace y quién lo dirige.

| Rol anterior | Nuevo rol |
|---|---|
| Ejecutar tickets en Jira | Dirigir y orquestar agentes |
| Configurar y codificar directamente | Diseñar el Blueprint y validar con el cliente |
| Ser el recurso que entrega | Ser el socio estratégico del cliente |
