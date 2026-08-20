"""Mapa curado voseo (rioplatense) → español neutro (tuteo).

Fuente de verdad ÚNICA para:
  - neutralize_voseo.py  (el fixer que reescribe el catálogo)
  - audit_catalog.py :: check_default_dialect  (el detector Q09)

Diseño deliberado: el mapa es EXPLÍCITO token→token. Nada que no esté acá se
toca. Esto evita los tres pozos del voseo:
  1. Falsos positivos que terminan en -á/-é/-í y NO son voseo:
       está, acá, allá, ahí, así, qué, porqué, café,
       futuros 3ª pers: será, deberá, podrá, mostrará, creará, configurará…
       pretéritos 1ª pers: encontré, detecté…
     → simplemente no están en el mapa.
  2. Verbos con cambio de raíz cuyo imperativo tú NO es "quitar el acento":
       mostrá→muestra (no "mostra"), cerrá→cierra, hacé→haz, poné→pon…
     → mapeados a mano.
  3. Formas idénticas en tuteo y voseo (no son marcadores):
       estás (tú estás == vos estás), vas (tú vas == vos vas)
     → excluidas a propósito.

Regla de override (Q09): el default es neutro, pero si el usuario o el país del
cliente piden otro dialecto para el RESULTADO, se respeta. Este mapa normaliza la
prosa/instrucciones del catálogo y la salida por defecto, no fuerza el dialecto de
una salida que el usuario pidió explícitamente en otra variante.
"""

from __future__ import annotations

# --- Frases (se aplican ANTES que los tokens sueltos) --------------------------
# El pronombre "vos" tras preposición pide "ti"/"contigo", no "tú".
PHRASES: dict[str, str] = {
    "con vos": "contigo",
    "a vos": "a ti",
    "para vos": "para ti",
    "de vos": "de ti",
    "por vos": "por ti",
    "en vos": "en ti",
    "hacia vos": "hacia ti",
    "sin vos": "sin ti",
    "vos mismo": "tú mismo",
    "vos misma": "tú misma",
}

# --- Imperativos vos afirmativos CON clítico pegado ---------------------------
# El tú los separa/acentúa distinto; enumerados de lo que aparece en el repo.
CLITIC_IMPERATIVES: dict[str, str] = {
    "decílo": "dilo",
    "decíselo": "díselo",
    "decímelo": "dímelo",
    "pasámelo": "pásamelo",
    "pedíselo": "pídeselo",
    "pedíle": "pídele",
    "armámelo": "ármamelo",
    "armámela": "ármamela",
    "pegámelo": "pégamelo",
    "ofrecéle": "ofrécele",
    "parseálo": "parséalo",
    "presionálo": "presiónalo",
    "preguntáselo": "pregúntaselo",
    "mandáselo": "mándaselo",
    "incluílas": "inclúyelas",
    "incluílos": "inclúyelos",
    "excluílos": "exclúyelos",
    "excluílas": "exclúyelas",
    "escaláselo": "escálaselo",
    "disparála": "dispárala",
    "disparálo": "dispáralo",
    "compartíselo": "compárteselo",
    "citála": "cítala",
    "citálo": "cítalo",
    "cacheálos": "cachéalos",
    "cacheálo": "cachéalo",
    "buscála": "búscala",
    "buscálo": "búscalo",
    "mencionále": "menciónale",
    "mostrámelo": "muéstramelo",
    "mostrálo": "muéstralo",
    "mostrála": "muéstrala",
    "usála": "úsala",
    "usálo": "úsalo",
    "usálos": "úsalos",
    "revisálo": "revísalo",
    "revisála": "revísala",
    "dejalo": "déjalo",
    "dejala": "déjala",
    "hacelo": "hazlo",
    "hacela": "hazla",
    "ponelo": "ponlo",
    "ponela": "ponla",
    "ponele": "ponle",
    "tenelo": "tenlo",
    "quedate": "quédate",
    "acordate": "acuérdate",
    "fijate": "fíjate",
    "prepará": "prepara",
    "preparate": "prepárate",
    "tomate": "tómate",
}

# --- Imperativos vos + clítico, familia -ale/-ame/-alo… (2do lote medido) ------
# Voseo inequívoco (no colisiona con pretéritos). EXCLUIDOS a propósito por ser
# inglés o palabra/ nombre español: create, generate, incorporate (inglés),
# generales ("aspectos generales"), marcelo (nombre), dale (== tuteo da+le).
CLITIC_IMPERATIVES_EXTRA: dict[str, str] = {
    "abrila": "ábrela", "abrilo": "ábrelo", "activalo": "actívalo",
    "actualizalo": "actualízalo", "adaptalos": "adáptalos", "agregala": "agrégala",
    "agregalo": "agrégalo", "agrupalas": "agrúpalas", "agrupalos": "agrúpalos",
    "ajustala": "ajústala", "anotala": "anótala", "anotalo": "anótalo", "anotalos": "anótalos",
    "aplicala": "aplícala", "aplicalas": "aplícalas", "aplicalo": "aplícalo",
    "aplicalos": "aplícalos", "aprobalos": "apruébalos", "ayudame": "ayúdame",
    "bajalo": "bájalo", "basate": "básate", "calculalo": "calcúlalo", "capturala": "captúrala",
    "cerralo": "ciérralo", "clasificalo": "clasifícalo", "comparalo": "compáralo",
    "comparame": "compárame", "completalo": "complétalo", "conectalos": "conéctalos",
    "confirmalo": "confírmalo", "confirmame": "confírmame", "construilo": "constrúyelo",
    "consultalo": "consúltalo", "cruzala": "crúzala", "cuestionalo": "cuestiónalo",
    "definila": "defínela", "describilo": "descríbelo", "detectala": "detéctala",
    "detectame": "detéctame", "devolveme": "devuélveme", "distribuilo": "distribúyelo",
    "documentalo": "documéntalo", "editalo": "edítalo", "elegime": "elígeme",
    "estimame": "estímame", "excluila": "exclúyela", "extraelo": "extráelo",
    "filtralos": "fíltralos", "guardalo": "guárdalo", "guardalos": "guárdalos",
    "hablale": "háblale", "incluilo": "inclúyelo", "indicale": "indícale",
    "indicalo": "indícalo", "indicame": "indícame", "informales": "infórmales",
    "informame": "infórmame", "leela": "léela", "leelo": "léelo", "leelos": "léelos",
    "levantalo": "levántalo", "listalo": "lístalo", "listalos": "lístalos",
    "listame": "lístame", "llenalos": "llénalos", "manejala": "manéjala",
    "mantenelo": "mantenlo", "mencionala": "menciónala", "mencionale": "menciónale",
    "mencionalo": "menciónalo", "mencionalos": "menciónalos", "notalo": "nótalo",
    "paralo": "páralo", "parate": "párate", "pegalo": "pégalo", "pegame": "pégame",
    "presentalas": "preséntalas", "presentale": "preséntale", "quitalo": "quítalo",
    "recorrelo": "recórrelo", "reemplazalo": "reemplázalo", "registrala": "regístrala",
    "registralo": "regístralo", "releela": "reléela", "renombralos": "renómbralos",
    "repetile": "repítele", "reportala": "repórtala", "resolvelos": "resuélvelos",
    "respetala": "respétala", "respetalas": "respétalas", "respetalo": "respétalo",
    "respetalos": "respétalos", "resumila": "resúmela", "revisalo": "revísalo",
    "saltate": "sáltate", "seleccionalo": "selecciónalo", "separalo": "sepáralo",
    "señalalo": "señálalo", "subila": "súbela", "subilo": "súbelo", "sumalo": "súmalo",
    "sumalos": "súmalos", "sustituilos": "sustitúyelos", "traducilos": "tradúcelos",
    "traelo": "tráelo", "traeme": "tráeme", "tratala": "trátala", "tratalo": "trátalo",
    "validalo": "valídalo", "verificalo": "verifícalo",
}

# --- Imperativos vos afirmativos (regulares -ar: solo cae el acento) -----------
REGULAR_AR_IMPERATIVES: dict[str, str] = {v: v[:-1] + "a" for v in [
    "usá", "creá", "armá", "cargá", "pasá", "buscá", "generá", "confirmá",
    "verificá", "marcá", "aplicá", "actualizá", "editá", "validá", "agregá",
    "llamá", "registrá", "guardá", "escalá", "capturá", "ejecutá", "mandá",
    "tomá", "consultá", "saltá", "derivá", "arrancá", "ajustá", "sumá",
    "seleccioná", "reemplazá", "pegá", "esperá", "clasificá", "chequeá",
    "filtrá", "preguntá", "avisá", "dejá", "notificá", "sincronizá",
    "provisioná", "indicá", "mencioná", "aclará", "tocá", "parseá", "cacheá",
    "citá", "dispará", "presioná", "revisá", "mirá", "fijá", "quedá",
    "cliqueá", "clickeá", "copiá", "anotá", "detallá", "listá", "ordená",
    "agrupá", "separá", "combiná", "integrá", "importá", "exportá",
    "descargá", "bajá", "pará", "estirá", "recortá", "acortá", "alargá",
    "revisá", "activá", "desactivá", "renombrá", "borrá", "eliminá",
    "asigná", "priorizá", "estimá", "calculá", "totalizá", "redondeá",
    "compará", "matcheá", "linkeá", "vinculá", "relacioná", "adjuntá",
    "nombrá", "titulá", "etiquetá", "categorizá", "documentá", "reportá",
    "sintetizá",
]}

# --- Imperativos vos con cambio de raíz o irregulares (-ar/-er/-ir) ------------
STEM_IRREGULAR_IMPERATIVES: dict[str, str] = {
    # -ar con diptongación / irregulares
    "mostrá": "muestra", "contá": "cuenta", "cerrá": "cierra",
    "encontrá": "encuentra", "recordá": "recuerda", "probá": "prueba",
    "acordá": "acuerda", "aprobá": "aprueba", "comenzá": "comienza",
    "empezá": "empieza", "pensá": "piensa", "sentá": "sienta",
    "calentá": "calienta", "apretá": "aprieta", "negá": "niega",
    "colgá": "cuelga", "jugá": "juega", "volá": "vuela", "forzá": "fuerza",
    "dá": "da",
    # -er (imperativo tú = raíz + e; irregulares aparte)
    "leé": "lee", "corré": "corre", "comé": "come", "bebé": "bebe",
    "respondé": "responde", "ofrecé": "ofrece", "extraé": "extrae",
    "aprendé": "aprende", "vendé": "vende", "prometé": "promete",
    "volvé": "vuelve", "resolvé": "resuelve", "mové": "mueve",
    "hacé": "haz", "poné": "pon", "tené": "ten", "mantené": "mantén",
    "obtené": "obtén", "detené": "detén", "sostené": "sostén",
    "proponé": "propón", "componé": "compón", "disponé": "dispón",
    "traé": "trae",
    # -ir (imperativo tú = raíz + e; irregulares aparte)
    "escribí": "escribe", "describí": "describe", "abrí": "abre",
    "subí": "sube", "cubrí": "cubre", "recibí": "recibe",
    "permití": "permite", "decidí": "decide", "dividí": "divide",
    "imprimí": "imprime", "insistí": "insiste", "asistí": "asiste",
    "definí": "define", "incluí": "incluye", "excluí": "excluye",
    "construí": "construye", "distribuí": "distribuye", "sustituí": "sustituye",
    "seguí": "sigue", "conseguí": "consigue", "perseguí": "persigue",
    "elegí": "elige", "pedí": "pide", "repetí": "repite", "medí": "mide",
    "serví": "sirve", "resumí": "resume", "compartí": "comparte",
    "reducí": "reduce", "traducí": "traduce", "producí": "produce",
    "decí": "di", "vení": "ven", "salí": "sal", "andá": "ve",
}

# --- Presente indicativo vos (2ª pers) ----------------------------------------
# OJO: 'estás' y 'vas' son idénticos en tuteo → NO van acá.
INDICATIVE: dict[str, str] = {
    "tenés": "tienes", "podés": "puedes", "querés": "quieres",
    "sabés": "sabes", "hacés": "haces", "decís": "dices", "sos": "eres",
    "necesitás": "necesitas", "ponés": "pones", "venís": "vienes",
    "seguís": "sigues", "elegís": "eliges", "contás": "cuentas",
    "preferís": "prefieres", "debés": "debes", "vés": "ves",
    "salís": "sales", "pedís": "pides", "servís": "sirves",
    "movés": "mueves", "volvés": "vuelves", "traés": "traes",
    "creés": "crees", "leés": "lees", "corrés": "corres",
}

# --- Indicativo/subjuntivo vos 2ª pers — tokens medidos del catálogo -----------
# Familias -ás (ind -ar), -és (ind -er / subj -ar), -ís (ind -ir). Generado por
# barrido real del repo (no por regla de sufijo, que rompería futuros del tuteo
# como "confirmarás", "verás", "tendrás"). Diptongos resueltos a mano. Los
# no-verbos "campopaís" y "nomás" quedan fuera a propósito.
INDICATIVE_EXTRA: dict[str, str] = {
    "abrís": "abres", "aburrís": "aburres", "accedés": "accedes",
    "acelerás": "aceleras", "aceptés": "aceptes", "aclarás": "aclaras",
    "activás": "activas", "actualizás": "actualizas", "adaptás": "adaptas",
    "adjuntás": "adjuntas", "agregás": "agregas", "aislás": "aislas",
    "ajustás": "ajustas", "animás": "animas", "anotás": "anotas",
    "aplicás": "aplicas", "aprendés": "aprendes", "aprobás": "apruebas",
    "armás": "armas", "arrancás": "arrancas", "asignás": "asignas",
    "autocompletás": "autocompletas", "avanzás": "avanzas", "avisás": "avisas",
    "ayudás": "ayudas", "bajás": "bajas", "basás": "basas",
    "cacheás": "cacheas", "capturás": "capturas", "cargás": "cargas",
    "cerrás": "cierras", "chequeás": "chequeas", "clasificás": "clasificas",
    "clonás": "clonas", "colapsás": "colapsas", "comentás": "comentas",
    "compartís": "compartes", "comparás": "comparas", "completás": "completas",
    "componés": "compones", "conectás": "conectas", "configurás": "configuras",
    "confirmás": "confirmas", "conformás": "conformas", "confundís": "confundes",
    "conocés": "conoces", "considerás": "consideras", "convertís": "conviertes",
    "copiás": "copias", "corregís": "corriges", "creás": "creas",
    "cruzás": "cruzas", "cubrís": "cubres", "curás": "curas",
    "customizás": "customizas", "decidís": "decides", "declarás": "declaras",
    "definís": "defines", "dejás": "dejas", "dependés": "dependes",
    "deployás": "deployas", "depurás": "depuras", "descargás": "descargas",
    "desplegás": "despliegas", "destildeás": "destildeas", "detectás": "detectas",
    "devolvés": "devuelves", "diagnosticás": "diagnosticas", "dibujás": "dibujas",
    "diseñás": "diseñas", "disparás": "disparas", "distinguís": "distingues",
    "distribuís": "distribuyes", "dudás": "dudas", "editás": "editas",
    "ejecutás": "ejecutas", "eliminás": "eliminas", "empaquetás": "empaquetas",
    "encontrás": "encuentras", "ensamblás": "ensamblas", "enseñás": "enseñas",
    "entrás": "entras", "errás": "yerras", "escribís": "escribes",
    "esperás": "esperas", "esponjés": "esponjes", "estimás": "estimas",
    "explicás": "explicas", "extraés": "extraes", "filtrás": "filtras",
    "generás": "generas", "gestionás": "gestionas", "guardás": "guardas",
    "habilitás": "habilitas", "hablás": "hablas", "heredás": "heredas",
    "imaginás": "imaginas", "importás": "importas", "ingresás": "ingresas",
    "inicializás": "inicializas", "inspeccionás": "inspeccionas", "instalás": "instalas",
    "intentás": "intentas", "interpretás": "interpretas", "inventés": "inventes",
    "inyectás": "inyectas", "inyectés": "inyectes", "juntás": "juntas",
    "lentificás": "lentificas", "limpiás": "limpias", "linkeás": "linkeas",
    "llamás": "llamas", "llenás": "llenas", "llevás": "llevas",
    "lográs": "logras", "mandás": "mandas", "mandés": "mandes",
    "manipulás": "manipulas", "matcheás": "matcheas", "mencionás": "mencionas",
    "mirás": "miras", "modelás": "modelas", "modificás": "modificas",
    "monitoreás": "monitoreas", "montás": "montas", "mostrás": "muestras",
    "mostrés": "muestres", "narrás": "narras", "obtenés": "obtienes",
    "omitís": "omites", "operás": "operas", "ordenás": "ordenas",
    "parás": "paras", "pasás": "pasas", "pegás": "pegas",
    "pensás": "piensas", "personalizás": "personalizas", "pesás": "pesas",
    "pisás": "pisas", "planteás": "planteas", "posteás": "posteas",
    "preparás": "preparas", "probás": "pruebas", "producís": "produces",
    "publicás": "publicas", "pusheás": "pusheas", "quedás": "quedas",
    "ramificás": "ramificas", "recibís": "recibes", "recomendás": "recomiendas",
    "reconocés": "reconoces", "recopilés": "recopiles", "recorrés": "recorres",
    "redibujás": "redibujas", "reemplazás": "reemplazas", "reescribís": "reescribes",
    "registrás": "registras", "reincorporás": "reincorporas", "repetís": "repites",
    "reportás": "reportas", "resolvés": "resuelves", "respondés": "respondes",
    "reutilizás": "reutilizas", "rompés": "rompes", "sacás": "sacas",
    "salteás": "salteas", "saltás": "saltas", "seleccionás": "seleccionas",
    "sentís": "sientes", "seteás": "seteas", "sincronizás": "sincronizas",
    "solés": "sueles", "sospechás": "sospechas", "subís": "subes",
    "sumás": "sumas", "superás": "superas", "sustituís": "sustituyes",
    "terminás": "terminas", "tirás": "tiras", "tomás": "tomas",
    "trabajás": "trabajas", "trackeás": "trackeas", "ubicás": "ubicas",
    "validás": "validas", "verificás": "verificas",
}

# --- Imperativos vos -á (y whitelist -er) — 2do lote medido del catálogo ----
# Los -á son SEGUROS (ningún pretérito termina en -á). Excluidos: topónimos
# (Bogotá, Panamá, Boyacá), futuros 3ª (-rá) y no-verbos. Hiatos y diptongos a
# mano. Las -é whitelisted son imperativos -er (no pretéritos de 1ª persona).
IMPERATIVE_EXTRA: dict[str, str] = {
    "abandoná": "abandona", "abortá": "aborta", "aceptá": "acepta",
    "acknowledgeá": "acknowledgea", "acotá": "acota", "actuá": "actúa",
    "acumulá": "acumula", "adaptá": "adapta", "alertá": "alerta", "alineá": "alinea",
    "analizá": "analiza", "anclá": "ancla", "anidá": "anida", "apagá": "apaga",
    "aprovisioná": "aprovisiona", "apuntá": "apunta", "auditá": "audita",
    "autocompletá": "autocompleta", "avanzá": "avanza", "ayudá": "ayuda", "barré": "barre",
    "basá": "basa", "blindá": "blinda", "bloqueá": "bloquea", "cambiá": "cambia",
    "caminá": "camina", "cancelá": "cancela", "captá": "capta", "cloná": "clona",
    "colapsá": "colapsa", "comentá": "comenta", "completá": "completa",
    "condensá": "condensa", "conectá": "conecta", "consolidá": "consolida",
    "continuá": "continúa", "coordiná": "coordina", "cruzá": "cruza",
    "cuestioná": "cuestiona", "dedicá": "dedica", "deduplicá": "deduplica",
    "degradá": "degrada", "delegá": "delega", "deployá": "deploya", "deprecá": "depreca",
    "descartá": "descarta", "descomentá": "descomenta", "deseleccioná": "deselecciona",
    "desempatá": "desempata", "desglosá": "desglosa", "desinstalá": "desinstala",
    "destildá": "destilda", "detectá": "detecta", "determiná": "determina",
    "devolvé": "devuelve", "diagnosticá": "diagnostica", "diseñá": "diseña",
    "empaquetá": "empaqueta", "emulá": "emula", "encolá": "encola", "enganchá": "engancha",
    "enmarcá": "enmarca", "enriquecé": "enriquece", "entendé": "entiende",
    "entregá": "entrega", "enviá": "envía", "escapá": "escapa", "espejá": "espeja",
    "estandarizá": "estandariza", "evaluá": "evalúa", "evitá": "evita",
    "explicá": "explica", "exponé": "expón", "fetcheá": "fetchea", "formulá": "formula",
    "frená": "frena", "garantizá": "garantiza", "grabá": "graba", "graduá": "gradúa",
    "habilitá": "habilita", "hablá": "habla", "identificá": "identifica",
    "implementá": "implementa", "incliná": "inclina", "incrementá": "incrementa",
    "incrustá": "incrusta", "informá": "informa", "ingresá": "ingresa", "iniciá": "inicia",
    "insertá": "inserta", "instalá": "instala", "intentá": "intenta",
    "investigá": "investiga", "invitá": "invita", "invocá": "invoca", "inyectá": "inyecta",
    "juntá": "junta", "justificá": "justifica", "levantá": "levanta", "limitá": "limita",
    "llená": "llena", "llevá": "lleva", "localizá": "localiza", "logueá": "loguea",
    "manejá": "maneja", "mapeá": "mapea", "matá": "mata", "maximizá": "maximiza",
    "memorizá": "memoriza", "minimizá": "minimiza", "modelá": "modela", "montá": "monta",
    "navegá": "navega", "normalizá": "normaliza", "notá": "nota", "optimizá": "optimiza",
    "otorgá": "otorga", "overrideá": "overridea", "paginá": "pagina", "pausá": "pausa",
    "personalizá": "personaliza", "planificá": "planifica", "poblá": "puebla",
    "posteá": "postea", "prellená": "prellena", "presentá": "presenta",
    "preservá": "preserva", "procedé": "procede", "procesá": "procesa",
    "profundizá": "profundiza", "publicá": "publica", "quitá": "quita",
    "reaccioná": "reacciona", "reasigná": "reasigna", "recalculá": "recalcula",
    "recolectá": "recolecta", "recomendá": "recomienda", "recomponé": "recompón",
    "reconciliá": "reconcilia", "reconfirmá": "reconfirma", "recorré": "recorre",
    "redactá": "redacta", "refiná": "refina", "reformulá": "reformula",
    "refrescá": "refresca", "reiniciá": "reinicia", "reinstalá": "reinstala",
    "reintentá": "reintenta", "releé": "relee", "rellená": "rellena",
    "renderizá": "renderiza", "repasá": "repasa", "replicá": "replica",
    "respetá": "respeta", "restá": "resta", "retomá": "retoma", "reusá": "reusa",
    "reutilizá": "reutiliza", "sacá": "saca", "salteá": "saltea", "sanitizá": "sanitiza",
    "serializá": "serializa", "seteá": "setea", "señalá": "señala", "solicitá": "solicita",
    "stubeá": "stubea", "terminá": "termina", "tildá": "tilda", "tipeá": "tipea",
    "trabajá": "trabaja", "transicioná": "transiciona", "tratá": "trata", "ubicá": "ubica",
    "unificá": "unifica",
}

# --- Pronombre sujeto ----------------------------------------------------------
# Se aplica AL FINAL, tras las frases (con vos → contigo, etc.).
PRONOUN: dict[str, str] = {"vos": "tú"}


def build_map() -> dict[str, str]:
    """Mapa combinado token→neutro. NO incluye PHRASES ni PRONOUN, que se
    aplican en fases separadas por el fixer/detector (orden importa)."""
    combined: dict[str, str] = {}
    for d in (CLITIC_IMPERATIVES, CLITIC_IMPERATIVES_EXTRA, REGULAR_AR_IMPERATIVES,
              STEM_IRREGULAR_IMPERATIVES, INDICATIVE, INDICATIVE_EXTRA,
              IMPERATIVE_EXTRA):
        combined.update(d)
    return combined
