<!-- ⚠️ AUTO-COPIADO desde _shared/presentation-builder/ por sync.sh — NO EDITAR ACÁ. Editá el canónico y volvé a correr sync.sh. -->

# Deck craft — Cómo se construye un deck que vende (no una plantilla rellenada)

> **Qué es esto.** La capa de *calidad del output* del skill. `industry-personalization.md`
> aporta el **vocabulario** del sector; las `templates/*.md` aportan la **estructura** de slides;
> este archivo aporta el **oficio**: el arco narrativo, la intención por slide y los principios
> de diseño que separan un deck profesional de uno que parece una plantilla con los huecos llenos.
>
> **Cómo se usa.** En el Paso 5, además de la estructura del template/base, el skill **inyecta en
> el prompt** el bloque marcado abajo como `### Bloque para el prompt` — textual. Eso le da a Claude
> Design no sólo *qué* slides hacer, sino *cómo* hacer que cada uno gane su lugar. El resto del
> archivo es guía para ti (el skill) al ensamblar.

---

## 1. El arco narrativo (un deck cuenta UNA historia, no lista secciones)

Un deck comercial bueno se lee como un argumento, no como un índice. Cada slide existe para empujar
al stakeholder un paso más cerca del "sí". El orden de los templates ya respeta esto; tu trabajo al
ensamblar el prompt es hacer **explícito el hilo** para que Claude Design no produzca slides sueltas.

**Arco comercial (a-medida y base-Drive):**

1. **Contexto / gancho** — quién es el cliente, en su lenguaje. Establece que entendemos su mundo.
2. **El problema, cuantificado** — el dolor en *sus* palabras, atado al **KPI que le duele** al stakeholder.
3. **El costo de no actuar** — qué pierde si esto sigue igual (tiempo, plata, riesgo, churn). Crea urgencia.
4. **La visión / el después** — cómo se ve su operación cuando esto está resuelto. Vende el resultado, no la feature.
5. **Cómo lo logramos** — alcance, método, equipo. Acá recién entran los "qué hacemos".
6. **Por qué nosotros / prueba** — casos reales (sólo verificados), método probado, equipo. Reduce el riesgo percibido.
7. **La inversión** — el número, enmarcado contra el costo de no actuar del paso 3.
8. **El próximo paso, concreto** — quién decide, qué firma, en qué plazo. Una sola acción clara.

**Arco delivery (kickoff / steering / status / cierre):**

1. **Dónde estamos** — el hito, el período, el estado en una frase.
2. **Qué logramos** — entregables/avances concretos, con evidencia (issues cerrados, hitos cumplidos).
3. **Qué aprendimos / qué cambió** — decisiones, ajustes de alcance, riesgos que aparecieron.
4. **Qué viene** — próximos hitos, dependencias, qué necesitamos del cliente.
5. **Pedido / cierre** — la decisión o confirmación que buscamos en esta reunión.

> **Regla del arco:** cada slide debe poder responder *"¿por qué este slide, acá, para ESTE cliente?"*.
> Si un slide no empuja el arco, se fusiona con otro o se elimina — no se deja "porque la plantilla lo tiene".

---

## 2. Principios de diseño por slide (el "oficio")

Estos son los que más suben la calidad percibida. Van al prompt (ver bloque al final).

- **Una idea por slide.** Si un slide tiene dos ideas, son dos slides. Si tiene media idea, se fusiona.
- **El título afirma, no rotula.** El headline es la conclusión, no el tema.
  - ✗ "Alcance" → ✓ "Qué incluye tu implementación de CG Cloud"
  - ✗ "Beneficios" → ✓ "Reducimos el tiempo de originación de 5 días a 4 horas"
  - ✗ "Problema" → ✓ "Hoy el 30% de las visitas no se registran en el PDV"
- **El cuerpo prueba el título.** Bullets/visual sostienen la afirmación del headline; no la repiten.
- **Concreto > abstracto.** Números, nombres, fechas, frases textuales del cliente. Un dato real vale más que tres adjetivos.
- **Conecta dolor → KPI.** Cada problema que planteas se ata a un KPI que el stakeholder ya mira
  (los KPIs por industria están en `industry-personalization.md`). "Quiebres de stock" → "impacto en GMV y ticket promedio".
- **El "so-what" obligatorio.** Cada slide responde *"¿por qué le importa esto al cliente?"*. Si no lo responde, sobra.
- **Visual antes que texto.** Donde haya un diagrama, tabla o métrica mejor que un párrafo, úsalo:
  Gantt, diagrama de integración, tabla de SLAs, tabla de inversión, métrica grande. El deck no es un documento.
- **Divisores de sección entre bloques.** Cada bloque del arco (contexto, problema, solución, inversión, cierre…)
  abre con un **slide divisor** (`section-divider`) — número + etiqueta + título de sección, fondo azul full-bleed del DS.
  Le dan ritmo y "capítulos" al deck; sin ellos las slides se leen como una lista continua. Numéralos en orden (01, 02, 03…).
- **Ilustraciones en los slides clave.** Portada, cada divisor de sección, el slide de la "visión / el después" y el cierre
  llevan una **ilustración o composición gráfica real** (isotipo/patrón de marca, ilustración conceptual, imagen generada, íconos
  compuestos) — no sólo texto sobre fondo plano. La ilustración refuerza el mensaje del slide, no es decorado al azar.
- **Sin muros de texto.** Máximo ~5 bullets por slide, ~1 línea cada uno. Si necesitas un párrafo, va en las notas del orador, no en el slide.
- **El slide soporta una charla, no la reemplaza** (salvo leave-behind explícito). El detalle fino lo dice quien presenta.
- **Paralelismo.** Slides hermanos comparten layout (ej: un módulo por slide, todos con el mismo esqueleto). La consistencia se lee como prolijidad.

---

## 3. Personalización: que se sienta hecho para ESE cliente

Esto refuerza el corazón del skill (ver SKILL.md "Personalización"). Va al prompt:

- **El nombre del cliente/proyecto aparece en los slides clave** — problema, alcance, próximos pasos.
  "Para BBVA proponemos…", nunca "Para el cliente proponemos…".
- **Usa el vocabulario del sector** (de `industry-personalization.md`) y **evita los términos vetados**
  de ese sector. Un banco no tiene "compradores"; una farma no tiene "clientes", tiene "pacientes".
- **Frases textuales del cliente** (de transcripts/emails barridos) entre comillas en el slide del problema. Nada vende como sus propias palabras.
- **Adapta los ejemplos** al sector y geografía del cliente — pero sólo con evidencia real, nunca inventada.

---

## 4. Anti-patrones (decirle a Claude Design qué NO hacer)

- **Cero placeholders.** Nada de `[A completar]`, `[TODO]`, `[nombre]`, `[Personalizar]`, `[TBD]`.
  Si un dato no está, la sección no se incluye (el skill ya resolvió esto en el Paso 4.7 antes de llegar acá).
- **Cero placeholders de imagen.** Nunca dejes cajas grises, "imagen aquí", `[ilustración]`, `[foto]` ni marcos vacíos
  esperando un asset. Cada slide clave se entrega **con su ilustración ya materializada** (SVG/patrón de marca inline,
  imagen generada embebida como data URI, composición de íconos). Si no puedes generar una ilustración pertinente, resuelve
  el slide con una composición gráfica de marca real (isotipo/patrón/bloques de color) — nunca con un hueco.
- **Cero relleno.** Nada de "somos líderes en innovación" sin prueba. Cada claim se sostiene con un dato, un caso o un método.
- **Cero casos/números inventados.** Sólo los que vinieron en "Señales relevantes" o de pricing de Salesforce.
- **No repitas el headline en el primer bullet.** El cuerpo agrega, no eco.
- **No metas un slide "porque la plantilla lo tiene"** si no aporta a ESTE caso. Mejor fusionar que rellenar.

---

## 5. Checklist de calidad (Claude Design valida antes de cerrar el deck)

Va al prompt como auto-chequeo final:

- [ ] ¿Cada slide pasa el test del "so-what" para este cliente?
- [ ] ¿Cada headline **afirma** algo (no sólo rotula el tema)?
- [ ] ¿Cada slide tiene **una** idea y ≤5 bullets de ~1 línea?
- [ ] ¿El nombre del cliente/proyecto aparece en problema, alcance y próximos pasos?
- [ ] ¿El vocabulario es el del sector y se evitaron los términos vetados?
- [ ] ¿Cada problema se ató a un KPI que el stakeholder mira?
- [ ] ¿Cada bloque abre con su **divisor de sección** numerado?
- [ ] ¿Los slides clave (portada, divisores, visión, cierre) llevan **ilustración materializada** (no placeholder)?
- [ ] ¿No quedó ningún placeholder de texto **ni de imagen** ni claim sin prueba?
- [ ] ¿El deck cierra con **un** próximo paso concreto?

---

### Bloque para el prompt

> **Pega este bloque textual en el prompt final (Paso 5), bajo el título "## Principios de diseño del deck (obligatorios)".**
> Es lenguaje dirigido a Claude Design. Ajusta "cliente"/"proyecto" según área (comercial/delivery).

```
## Principios de diseño del deck (obligatorios)

Este deck cuenta UNA historia, no es una lista de secciones. Constrúyelo así:

**Arco narrativo** — cada slide empuja al lector un paso más cerca de la decisión:
[Comercial] contexto → problema cuantificado → costo de no actuar → la visión del "después" →
cómo lo logramos (alcance/método/equipo) → por qué nosotros (prueba) → inversión → un próximo paso concreto.
[Delivery] dónde estamos → qué logramos (con evidencia) → qué cambió/aprendimos → qué viene → el pedido/cierre.

**Oficio, slide por slide:**
- Una idea por slide. Si hay dos ideas, son dos slides.
- El título AFIRMA la conclusión, no rotula el tema. ✗ "Alcance" → ✓ "Qué incluye tu implementación".
  ✗ "Problema" → ✓ "Hoy el 30% de las visitas no se registra en el PDV".
- El cuerpo prueba el título; no lo repite. Máximo ~5 bullets de ~1 línea. Sin muros de texto.
- Concreto > abstracto: números, nombres, fechas, frases textuales del cliente. Un dato real > tres adjetivos.
- Cada problema se ata a un KPI que el stakeholder ya mira.
- Visual antes que texto: diagrama, tabla o métrica grande donde mejore sobre un párrafo.
- Slides hermanos comparten layout (ej: un módulo por slide, mismo esqueleto).

**Estructura por capítulos (obligatoria):**
- Cada bloque narrativo abre con un **slide divisor de sección** (fondo azul full-bleed de la marca, número correlativo
  01/02/03…, etiqueta y título de sección). Sin excepción: separan visualmente contexto → problema → solución → inversión → cierre.

**Ilustraciones (obligatorio en slides clave):**
- La portada, cada divisor de sección, el slide de la visión/"el después" y el cierre llevan una **ilustración o composición
  gráfica real** que refuerza el mensaje (isotipo/patrón de marca, ilustración conceptual, imagen generada, íconos compuestos).
- **Nunca dejes placeholders de imagen**: ni cajas grises, ni "imagen aquí", ni `[ilustración]`, ni marcos vacíos. La ilustración
  va materializada en el entregable (SVG o patrón de marca inline, o imagen generada embebida como data URI). Si no hay una
  ilustración pertinente, resuelve el slide con una composición gráfica de marca real — jamás con un hueco reservado.

**Personalización (innegociable):**
- El nombre del cliente/proyecto aparece en los slides de problema, alcance y próximos pasos. "Para [CLIENTE] proponemos…", nunca "Para el cliente…".
- Usa el vocabulario del sector indicado arriba y evita los términos vetados. Frases textuales del cliente entre comillas en el slide del problema.

**Prohibido:** placeholders de texto ([A completar], [TODO], [nombre]); **placeholders de imagen** (cajas grises,
"imagen aquí", [ilustración], marcos vacíos); claims sin prueba ("somos líderes…"); casos o números inventados
(sólo los que figuran arriba); repetir el headline en el primer bullet;
**[Comercial] spoilers de precio** — no adelantes cifras, montos ni % de descuento en ningún slide previo al de inversión
(el número aparece por primera vez en el slide de precio final), salvo que el prompt lo pida expresamente.

**Antes de cerrar, verifica cada slide:** ¿pasa el "so-what" para este cliente? ¿el headline afirma?
¿una idea, ≤5 bullets? ¿aparece el nombre del cliente donde corresponde? ¿cada bloque abre con su divisor de sección?
¿los slides clave (portada, divisores, visión, cierre) llevan ilustración materializada? ¿cero placeholders de texto
Y de imagen? ¿cero claims sin prueba? ¿el deck cierra con UN próximo paso concreto?
```
