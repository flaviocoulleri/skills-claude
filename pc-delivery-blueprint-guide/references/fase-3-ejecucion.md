# Fase 3 — Ejecución con IA: la IA construye, el nodo controla

Fuente: deck "ProContacto Blueprint v2", slide 13. Sprints de 1 semana. Gate de salida: **G3 · Criterios cubiertos**.

**Nodo de 3:** Líder funcional · Revisor técnico · Operador del agente. Capacidad: **3 proyectos en paralelo** por nodo.

## El ciclo del sprint (5 pasos)

1. **Selección** — entran solo HUs **AI-ready**: criterios de aceptación + diccionario de datos (DDD) + wireframe asociado.
2. **Construcción** — el agente ejecuta con las skills sobre sandbox.
3. **Revisión humana** — checklist **binario** contra criterios y wireframe.
4. **Demo semanal** — muestra el incremento; **no abre el alcance**.
5. **Despliegue continuo** — el cliente toca lo demostrado en validación.

## Reglas que protegen la velocidad

Citarlas textual cuando el PM pregunte:

1. **Nada entra sin estar AI-ready.** Sin excepciones, ni siquiera «es chiquito».
2. **Feedback consolidado en 48 h hábiles por el PO** — o el incremento queda aceptado.
3. **Defecto = criterio firmado incumplido.** Todo lo demás es cambio, y se clasifica en la propia demo.
4. **Los cambios aprobados van al final de la cola.** Nunca interrumpen el sprint en curso.

## Definición de HU AI-ready

Una historia está AI-ready cuando tiene las tres cosas:
- Criterios de aceptación Gherkin verificables (pasa / no pasa)
- Entrada correspondiente en el diccionario de datos
- Wireframe/pantalla asociada (Anexo C)

Si falta cualquiera de las tres, la HU no entra al sprint. Se resuelve la ambigüedad primero (principio 2: la ambigüedad se resuelve antes de construir, nunca durante).

## Métricas de la fase

- **Tasa de rechazo de la revisión humana por HU** — mide la calidad del pipeline de IA.
- 100% de pedidos post-freeze capturados como CR cobrado o fase 2.

## Gate 3 · Criterios cubiertos

Todas las HUs del alcance comprometido pasaron la revisión humana binaria contra criterios y wireframes. Checklist en `gates-checklists.md`.

## Práctica recomendada: comité operativo semanal con métricas

Para el reporting semanal al cliente en esta fase, usar el patrón de comité operativo con métricas cuantitativas de backlog (`templates/status-semanal.md` y `practica-real-dm.md` §2): abiertos/en progreso/listos para validar/cerrados, clasificación error-vs-cambio delante del cliente, % avance real vs. plan. Es donde la regla defecto≠mejora se sostiene en la práctica. *(Práctica recomendada de campo, no canon del deck.)*

> Hay una propuesta pendiente de validación sobre cómo reconciliar el ciclo continuo de feedback/tickets con la regla "máx. 2 rondas de observaciones" — ver `propuestas-metodologicas.md` P4.
