---
name: auditoria-seo-geo
description: |
  Auditoría SEO-GEO en profundidad de la web de un hotel con motor de
  reservas, y su informe con identidad Paraty Tech. Úsalo cuando el usuario
  pase una URL o dominio de un hotel/cadena y pida auditar, revisar,
  analizar SEO, hacer una revisión técnica o un informe SEO. Triggers:
  "audita", "auditoría SEO", "revisa esta web", "informe SEO", "revisión
  SEO", "análisis SEO-GEO", o simplemente una URL de hotel sin más contexto.
user-invocable: true
---

# Auditoría SEO-GEO para hoteles — Paraty Tech

Proceso de trabajo para auditar la web de un hotel con motor de reservas y
entregar un informe accionable. Cubre SEO técnico clásico **y GEO/AEO**
(ser citado por ChatGPT, Perplexity y AI Overviews).

La lista de comprobaciones es `reference/checklist.md` (98 checks, 11
bloques). No la reinventes: audita **contra ella**. La versión imprimible
para el cliente es `reference/checklist-auditoria-seo.html`.

---

## 1. Antes de arrancar

Necesitas del usuario, y si no lo dice, **pregunta solo lo que bloquee**:

| Dato | Por qué | Si no lo dan |
|---|---|---|
| URL / dominio | Obvio | Bloqueante, pregunta |
| Mercado e idiomas | hreflang, contactos del informe | Asume ES y lo verificas en el crawl |
| Nombre del hotel y nombre anterior | Búsqueda de marca y rebranding (bloque 8) | Lo deduces del `<title>` y del schema |
| ¿Hay accesos a GSC / GBP / Clarity / Bing? | Bloque 0 | Marca los checks como "sin acceso", no como fallo |

No bloquees la auditoría técnica esperando accesos. Todo el bloque 1-7 y
buena parte del 9 se audita sin credenciales.

Y antes de empezar, **comprueba qué fuentes tienes vivas** (§1b). No es lo
mismo decir "sin datos de visibilidad" que no haber mirado si SISTRIX
responde.

---

## 1b. Fuentes declaradas y trazabilidad

**Toda cifra del informe sale de una fuente con nombre, fecha y alcance, y el
informe lo dice.** Es la diferencia entre un informe que el cliente puede
contrastar y uno que se tiene que creer. Dos reglas:

1. **Tabla de fuentes al principio del informe**, como apartado 0
   («Metodología y fuentes»), con una fila por fuente: código corto,
   herramienta, fecha, **muestra** y **qué apartados alimenta**. Códigos del
   tipo `SF-15/09`, `SM-16/09`, `GSC`, `GEO`, `SISTRIX`, `SISTRIX-AI`. La
   fecha es el **rango real** (`13/05/2025 - 12/09/2026, 488 días`), no «16
   meses»; y la muestra son las cifras (`2.940 URLs, 605 HTML, 598 con código
   200`), no un adjetivo.
2. **Ficha de fuente en cursiva debajo de cada título**, subapartados
   incluidos, con **cinco elementos**: herramienta, **filtro exacto**, rango
   de fechas, tamaño de la muestra y el anexo donde está el detalle. Por
   ejemplo: `*Fuente: Google Search Console, 13/05/2025 - 12/09/2026, pestaña
   Consultas (1.000 principales), impresiones y clics no-marca por cluster.*`
   El filtro es lo que hace el dato reproducible: sin él, el cliente no puede
   repetir la consulta. Si el apartado cruza dos fuentes, se citan las dos. Si
   es criterio propio, `*Elaboración propia a partir de los datos de los
   apartados anteriores.*`
3. **Bloque «Configuración de cada fuente»** debajo de la tabla, una entrada
   por código, para no repetirlo apartado por apartado: modo de rastreo y
   ámbito, si se respetó `robots.txt`, si se rastrearon subdominios, **si el
   renderizado de JavaScript estaba activado o no**, qué módulos se activaron,
   y en GSC la propiedad, el tipo de búsqueda, los filtros aplicados y las
   pestañas del export. Esto es lo que convierte el informe en reproducible.
   Y se dice lo incómodo: «el proyecto se creó el 01/09, así que no hay 30
   días de histórico», «AI Overviews está configurado pero no devolvió
   respuestas en esa ventana».

En esa misma tabla van **las fuentes que quedaron pendientes y por qué**, y
**las advertencias de muestreo**. Dos ejemplos reales que hay que replicar
siempre que apliquen: el export de consultas de Search Console trae las 1.000
principales, que pueden ser el 64% de los clics y solo el 30% de las
impresiones, así que los porcentajes de marca y no-marca se calculan sobre esa
muestra y hay que decirlo; y la tabla de páginas de GSC reparte impresiones de
forma que la suma por idioma supera el total del dominio, así que ese desglose
se lee como reparto relativo, no como cifras absolutas.

**Fuentes conectadas por MCP en este proyecto.** Compruébalo con una llamada,
no lo supongas:

| Fuente | MCP | Qué hace falta |
|---|---|---|
| Screaming Frog | `screaming-frog` | Modo Base de Datos + servidor MCP arrancado (Fase 1) |
| SISTRIX | `claude.ai Sistrix` | OAuth ya hecho. Visibilidad, keywords, enlaces y **AI Check** |
| GEO Metrics | `claude.ai Geo Metrics` | Conectado, pero **solo cubre dominios con proyecto creado**: `list_projects` primero |
| Semrush | `semrush` | Conectado. Consume unidades de API: `display_limit` bajo y nunca `phrase_questions` a lo grande |
| Google Search Console | `gscServer` | Necesita `~/.config/paraty/gsc_client_secrets.json`. Si no existe, el servidor no arranca: pídele el fichero de credenciales al usuario antes de dar GSC por imposible |
| Google Drive / Sheets | `claude.ai Google Drive` | Conectado. Es lo que permite montar los anexos (§5.6) |
| Supermetrics | `claude.ai Supermetrics` | Conectado. Alternativa para GSC, Ahrefs, Similarweb y Trends |
| PageSpeed Insights | `scripts/psi.py` | Clave en `~/.config/paraty/pagespeed.key` |

Si una fuente no está disponible, el apartado que depende de ella se marca
como pendiente **con el motivo concreto** y se recoge en «Datos pendientes»
al final del informe. No se rellena con criterio general disfrazado de dato.

---

## 2. Fase 1 — Crawl con Screaming Frog (MCP)

El servidor MCP integrado de Screaming Frog está declarado en el
`.mcp.json` del proyecto como `screaming-frog` (`http://localhost:11435/mcp`).

**Requisitos que fallan a menudo** — compruébalos antes de culpar al crawl:

1. Screaming Frog debe estar **en modo Base de Datos**
   (Configuración → Sistema → Modo de almacenamiento). En modo memoria el
   servidor MCP no arranca: *"Spider MCP server needs to be run in DB mode"*.
2. El servidor MCP debe estar arrancado
   (Configuración → Sistema → MCP Server → Start), idealmente con
   auto-start activado.
3. Si el MCP no responde, dilo y sigue con la fase 2 en vez de abortar: se
   puede auditar mucho con `WebFetch` sobre las URLs clave, solo pierdes la
   cobertura a escala de sitio.

**Un crawl no basta. Hacen falta tres pasadas**, y cada una alimenta
apartados distintos del informe (dilo así en la tabla de fuentes del §1b):

1. **Crawl completo del dominio.** Códigos de respuesta y cadenas de
   redirección, canonicals, meta robots, titles y meta descriptions
   (duplicados y longitud), H1/H2, imágenes sin alt y sobredimensionadas,
   enlaces internos y rotos, profundidad de clic, recuento de palabras, thin
   content, legibilidad y ratio texto/HTML. Pide también el **«Resumen del
   rastreo»** (`sf_generate_report`): es la vista de pájaro con los problemas
   ordenados por gravedad, y va a un anexo tal cual.
2. **Rastreo del `sitemap.xml` en modo lista**, y **cruzado con el crawl
   anterior**. Es la única forma de encontrar las **URLs huérfanas**: las que
   están declaradas en el sitemap y no reciben ni un enlace interno. En
   Landmar eran 111, el 18,3% del sitemap, landings de captación de 837
   palabras de media, y resultó ser el hallazgo de mejor retorno de toda la
   auditoría. También saca lo contrario: URLs indexables enlazadas que no
   están en el sitemap. **Sin esta pasada el apartado del sitemap sale vacío
   y se da por limpio lo que no lo está.**
3. **Crawl con extracción de datos estructurados activada** (y validación de
   schema.org y de Google). Cambia el diagnóstico por completo: lo normal es
   que el marcado exista y sin errores de sintaxis, y que lo que falle sean
   los **campos que Google pide para activar el resultado enriquecido**.
   Reporta cobertura por plantilla, errores que bloquean, avisos, URLs sin
   marcado y tipos que no existen y deberían (Offer, FAQPage,
   AggregateRating, VideoObject). Y agrupa por plantilla del CMS, no por URL:
   «una corrección, 347 URLs arregladas» vende mucho mejor que «347 avisos».

Dos pasos más que se olvidan y conviene lanzar:

- **Análisis de rastreo** («Analizar rastreo» / crawl analysis). Es el paso
  que rellena los filtros de **contenido duplicado y semiduplicado** y los de
  enlazado. Si no se ejecuta, esos apartados quedan pendientes: dilo en «Datos
  pendientes» en vez de concluir que no hay duplicados.
- **Renderizado con JavaScript**, al menos sobre la home y una plantilla de
  cada tipo. El crawl por defecto va en modo texto, y hay schema y contenido
  que se inyecta en cliente (ver el patrón del FAQPage de Paraty). No des por
  ausente lo que no has mirado en el DOM.
- El **módulo de accesibilidad** si se quiere medición WCAG: va desactivado
  por defecto y hay que activarlo antes de lanzar, no después.

Comprueba a mano lo que el crawl no ve: `robots.txt`, `sitemap.xml`,
`llms.txt`, la 404 real (pide una URL inventada), la versión con mayúsculas
y con acentos de una URL, http→https, www vs no-www y la barra final.

---

## 3. Fase 2 — Lo que Screaming Frog no cubre

- **Rendimiento y CWV**: ejecuta `scripts/psi.py` sobre home, una ficha de
  hotel y una landing de destino:
  `PAGESPEED_API_KEY=… python3 scripts/psi.py <url1> <url2> <url3>`. Devuelve,
  en móvil y escritorio, las puntuaciones Lighthouse, las métricas de
  laboratorio (LCP, CLS, TBT, FCP, Speed Index, TTI) y las de campo CrUX
  (p75 y categoría de LCP, CLS, INP…) cuando Google tiene datos reales de
  usuarios. Lleva esas cifras al informe; identifica el elemento LCP (en
  hoteles casi siempre el hero con lazyload mal puesto).
  - **Vídeo de fondo pesado**: si la home lleva un `<video>` de fondo,
    descarga la fuente y mide su peso (`curl -o /dev/null -w '%{size_download}'`).
    Un mp4 de varios MB en el hero dispara el LCP y el consumo de datos en
    móvil aun con la etiqueta «LOW»; hay que apuntarlo con el peso real (no el
    supuesto) y recomendar poster + carga diferida / compresión. Comprueba
    también desde qué host se sirve (p. ej. un `www3` sin las cabeceras del
    dominio principal).
  - La clave se lee de la variable `PAGESPEED_API_KEY` o del archivo
    `~/.config/paraty/pagespeed.key`. **Sin clave la API responde 429**
    (cuota anónima compartida). Con clave, los datos van siempre.
  - **Sin clave y sin poder llamar a la API**, no inventes: pide al usuario
    que abra `pagespeed.web.dev`, analice las URLs y pegue las métricas
    (LCP, CLS, INP y la puntuación de rendimiento, móvil y escritorio). Con
    esos números se rellena el bloque de CWV igual. Solo si tampoco hay eso
    se escribe «sin dato de LCP/CLS/INP» y se explica por qué. No hay
    automatización de navegador en esta sesión.
- **Módulos que cargan todo el listado en la home**: revisa el HTML de la
  home en busca de secciones de blog/noticias que rendericen *todas* las
  entradas de golpe (cuéntalo, p. ej. `grep -c 'Ver más'` y los enlaces al
  detalle). Es un patrón real del CMS: la home del blog vuelca las ~450
  entradas → cientos de «Ver más» y una página enorme. Lo correcto son 3-4
  destacadas + un «Ver más» que enlace al listado (`/noticias.html`), no
  cargar el listado completo. Y **el título de cada entrada debe ser el
  enlace** (no un `<a>` vacío con el texto fuera, que además dispara el
  hallazgo «enlaces sin texto de anclaje» a escala de todo el sitio).
- **Motor de reservas**: entra al proceso de reserva. Verifica el logo (host
  logo) que debe llevar a la misma web sin redirección, que el motor no
  genera URLs indexables basura, y la continuidad de medición web↔motor.
- **Hreflang — no confundir `x-default` con duplicado.** Screaming Frog marca
  «entradas múltiples» cuando ve dos entradas para la misma URL, pero el patrón
  correcto `es/en/pt` + `x-default` apuntando `x-default` a la versión por
  defecto (misma URL que `es`) **es válido, no un error**. Antes de reportar
  hreflang duplicado, abre el HTML y míralo: si el «duplicado» es el
  `x-default`, está bien. El defecto real que sí vale la pena señalar es
  hreflang apuntando a URLs que no dan 200 (redirigen) o a páginas `noindex`.
- **Redirección automática por geo/idioma**: ejecuta
  `bash scripts/geo-redirect.sh <url>`. Pide la home con varios
  `Accept-Language` y como Googlebot. **Si la URL final cambia según el
  idioma, o la raíz fuerza siempre un 3xx a un idioma**, hay redirección
  automática: es mala para el rastreo porque Googlebot llega casi siempre
  como `en-US` y no verá los demás idiomas. La solución Paraty es una
  ventana que **sugiere** el idioma/versión, sin redirigir. La
  geolocalización por país (IP) se confirma a mano (VPN o ficha de Google).
- **Ficha de Google — y NAP con datos públicos, sin esperar accesos**: busca
  el nombre del hotel en Google (WebSearch) y lee el panel de conocimiento.
  **El NAP se verifica sin acceso al GBP**: compara el nombre, la dirección y
  el teléfono que muestra Google con los de la web (schema `Hotel`, página de
  contacto). Cualquier desajuste —dirección abreviada, teléfono distinto,
  centralita vs. hotel— es un hallazgo, y no requiere credenciales. Revisa
  también categorías, reseñas, fotos, Q&A y **menciones al nombre anterior si
  hubo rebranding** — mismo problema de consistencia que el NAP.
- **GEO/AEO**: pregunta por el hotel a un LLM y comprueba si lo cita y con
  qué datos. Revisa densidad factual, E-E-A-T, FAQPage y desambiguación de
  marca.
- **GSC / Analytics**: si hay acceso, cruza queries de marca vs genéricas,
  keywords en segunda página e impresiones sin clics. Los conectores de
  Supermetrics y Google Drive de la sesión sirven para esto.
- **Off-page y autoridad** (ver Fase 2b).

## 3b. Fase 2b — Off-page, autoridad y competencia

Mide la autoridad, el perfil de enlaces, la visibilidad y con quién compite de
verdad el dominio. **La fuente principal es SISTRIX por MCP**, que está
conectada y no necesita accesos del hotel.

**SISTRIX — `mcp__claude_ai_Sistrix__*`, siempre con el `country` del mercado
(`es`, `uk`, `fr`, `de`…), nunca con el `de` que trae por defecto:**

- `domain` con `view=visindex_overview`, y `view=visindex` + `history` →
  índice de visibilidad y su evolución de las últimas 13 semanas. Di si hay
  tendencia o si el dominio lleva un trimestre oscilando en la misma banda:
  "no hay caída estructural, pero tampoco crecimiento" es un diagnóstico.
- `domain` con `view=kwcount`, `kwcount_top10` y `urlcount` → keywords
  posicionadas, cuántas en top 10 y cuántas URLs distintas rankean. **El
  ratio top10/total es el dato que vale.** Muchas keywords mal posicionadas
  valen menos que pocas bien posicionadas, y ese ratio permite compararse de
  tú a tú con cadenas mucho mayores.
- `domain` con `view=competitors` → competidores orgánicos **reales**, no los
  que elegiría el cliente. Casi siempre salen OTAs y portales de reseñas
  (Booking, TripAdvisor, Trivago) ocupando el espacio antes que la web
  oficial; dilo con esas palabras. Y si aparecen dominios ajenos al sector,
  suelen ser la consecuencia de algún contenido de blog que rankea fuera de
  nicho: mirarlo, porque conecta con el apartado de contenidos.
- `domain` con `view=opportunities` → keywords en posición 11-12, a un paso
  de la primera página. **Cruza cada una con la URL que la trabaja**: si esa
  URL es huérfana o está en noindex, ese cruce es el hallazgo.
- `domain` con `view=ranking_distribution` y `view=traffic_estimation` →
  reparto por páginas de SERP y dónde está el tráfico dentro del dominio
  (raíz, blog, fichas de hotel). Si las fichas que venden apenas capturan
  tráfico propio, eso va al resumen ejecutivo.
- `links` → URLs más enlazadas, dominios referentes y **anchor text**. Mira
  el reparto entre `https://www.`, sin www y `http://`, y **si las URLs con
  parámetros reciben enlaces externos**, que agrava cualquier canibalización.
  En el anchor text es donde aparecen las **redes de spam**: busca anclas del
  tipo «telegram @…», «pbn», «dofollow backlinks da 50», «link-legion». Si
  las hay, rastrea su origen y **cuenta los dominios del mismo patrón**
  (p. ej. 19 dominios `seo-anomaly-top-1XX.xyz` apuntando todos a la misma
  URL con el mismo anchor y la misma fecha). Es un hallazgo de primer nivel,
  riesgo de SEO negativo con recomendación de disavow, y no se detecta de
  ninguna otra forma.
- Compara el índice de visibilidad con **5-10 competidores**, etiquetando
  cada uno (cadena nacional, cadena local, resort, internacional). La lectura
  correcta no es compararse con el gigante del sector, que juega otra liga, es
  compararse con su grupo real.

**Semrush** (`backlinks_research`, `domain_overview`) cuando haga falta
Authority Score o el crecimiento de backlinks en el tiempo. Ojo al consumo de
unidades de API.

**Supermetrics** como alternativa si falla lo anterior: `ds_id=GW` (GSC),
`AHRF2` / `SR`, `SW` (Similarweb, estimado, útil para comparar con la
competencia sin sus accesos) y `GT` (Trends, sin login).

Qué llevar al informe: índice de visibilidad y evolución, keywords y ratio
top 10, competidores reales etiquetados, dónde se concentran los enlaces,
perfil de anchor text, **enlaces tóxicos con el recuento de dominios del
mismo patrón**, enlaces de calidad que sí tiene el dominio, y targets
naturales de link building cruzando los dominios que ya citan los LLM
(Fase 2c) con los que ya enlazan a la competencia.

---

## 3c. Fase 2c — Visibilidad en IA, medida

No vale con preguntarle a un LLM y contar la anécdota. Hay dos fuentes que dan
cifras, y cada una es un apartado propio del informe.

**SISTRIX AI Check — `mcp__claude_ai_Sistrix__ai_check`**, más `ai_tracker`,
`ai_tracker_overview`, `ai_prompt_answers` y `ai_topicresearch`. Da, por país:

- En **cuántos prompts** aparece el dominio, separando AI Overviews de AI
  Mode, y si el dato lleva un mes estable o es un pico puntual.
- **Citaciones** totales y **posición del dominio en el ranking de fuentes
  citadas**. Puede ser la primera, por delante de YouTube o de las cadenas
  grandes: eso es un titular en sí mismo.
- **Qué URLs cita la IA**, con citaciones y prompts por URL. Aquí salen los
  hallazgos que no aparecen en ninguna otra parte: que la URL más citada no
  venda nada, o que la segunda más citada sea una **página huérfana** que la
  IA encuentra y el propio site no enlaza.
- **Qué prompts** la citan y **contra qué marcas** compite en las respuestas.
  Esa lista no coincide con la competencia orgánica clásica, y conviene
  tenerla delante al redactar contenido.
- Si Search Console todavía no reporta AI Overviews para la propiedad, **dilo
  explícitamente**: que GSC no lo reporte no significa que el dominio no esté
  en las respuestas de IA.

**GEO Metrics — `mcp__claude_ai_Geo_Metrics__*`.** Solo cubre dominios con
proyecto creado: empieza por `list_projects` y, si el dominio no está, dilo y
recomienda crear el proyecto en vez de dejar el apartado vacío. Si está:

- `get_project_overview` → prompts activos, ejecuciones, **posición media
  global**, **Share of Voice** y citaciones al dominio en 30 días.
- `list_project_prompts` + `get_ranking_prompt_details` → rendimiento prompt a
  prompt (posición, SOV, citaciones, menciones) y **desglose por motor**:
  ChatGPT, Gemini, Claude, Perplexity, Copilot, DeepSeek, Grok, AI Mode y AI
  Overviews. Señala el prompt donde la marca es fuerte y el prompt cabeza del
  sector donde es invisible: ese contraste es el diagnóstico. Y si un motor
  da cero, dilo con nombre.
- `list_project_competitors` → ranking competitivo por SOV.
- `list_project_citation_domains` + `get_citation_domain_details` →
  **ecosistema de citación**. Clasifica los dominios en OTAs, portales de
  reseñas, medios generalistas, blogs de viaje y competidores, y cuenta cada
  grupo. De ahí sale la lista de targets de PR y de link building, y el dato
  de cuántas citaciones suman los medios frente a las del cliente.
- `get_project_domain_endpoints` → por qué URLs propias la citan. Pocos
  endpoints citados significa que la web no está sirviendo como fuente de
  verdad para los LLM.
- `list_project_recommendations` + `get_recommendation_detail` → las
  recomendaciones que genera la herramienta (social media, influencers, PR).
  Van al informe resumidas y accionables, no copiadas en bruto.
- `list_project_tracked_websites` + `get_website_traffic_overview` → tráfico
  real de bots y referidos de IA. **Si el snippet no está verificado no hay
  datos**, y entonces el hallazgo es instalar el snippet.
- `get_geo_readiness_score`, `get_content_readiness_score`,
  `get_seo_readiness_score` por endpoint y `get_topic_graph` del dominio,
  cuando el análisis on-page esté configurado. Si no lo está, el hallazgo es
  configurarlo.

Cierra el apartado con **KPIs con valor objetivo a 3-6 meses** —SOV global,
posición media, citaciones al dominio, SOV en el prompt cabeza del sector—, no
con buenas intenciones.

---

## 3d. Fase 2d — Search Console, cuando hay acceso

Es la fuente que convierte un hallazgo técnico en dinero: la que permite
escribir «hay 2,4M de impresiones atrapadas en posición 51» en vez de «hay una
canibalización». Pide **16 meses**, el máximo. Con `gscServer`
(`get_search_analytics`, `get_advanced_search_analytics`,
`compare_search_periods`, `get_search_by_page_query`, `inspect_url_enhanced`)
o con el export manual que pegue el usuario.

Qué se saca, y todo va al informe:

- **Volumen global**: impresiones, clics, CTR y posición media ponderados.
- **Split marca vs no-marca**, con una regex que incluya **las variantes mal
  escritas de la marca y las submarcas**, que también son búsquedas de marca.
  El gap de no-marca es casi siempre el titular del informe: "la marca
  convierte, los genéricos aparecen y no capturan".
- **Split por dispositivo, país e idioma.** Busca el país con buena posición
  media y sin contenido nativo: es un mercado escondido, y es un hallazgo.
- **Top URLs por clics**, comparando cada URL con su variante parametrizada
  (`?utm_source=…`) si existe. **Ojo: que la URL con UTM de la ficha de Google
  concentre los clics no es una canibalización.** Si la canonical apunta a la
  limpia, es medición válida y Search Console simplemente atribuye el tráfico
  a la URL con parámetro. Se describe en neutro —«es tráfico de la ficha de
  hotel que Search Console atribuye a la URL con UTM»— y no se marca como
  crítico. Comprueba la canonical antes de escribir nada. La canibalización de
  verdad se detecta con el cruce de keywords de SISTRIX: dos URLs propias
  compitiendo por la misma consulta.
- **Consultas en segunda página** (posición 11-30 con más de 100
  impresiones), con sus impresiones y clics sumados. Es el bloque de retorno
  más rápido de la auditoría, porque se mueve con contenido y no con enlaces.
- **Clusters de oportunidad cuantificados**: agrupa las consultas no-marca por
  tema y da consultas, impresiones y clics de cada cluster. Un cluster
  cuantificado justifica una landing; una intuición, no.
- **Páginas con impresiones y cero clics**, con su porcentaje sobre el total
  de páginas indexables. Es la lista de refresh de contenido.
- **Marcas de la competencia** por las que rankea el dominio: justifican un
  contenido comparativo.
- **Cruce con el sitemap y con el crawl** para contar páginas indexables sin
  ninguna impresión, y para detectar huérfanas que sí reciben impresiones.

---

## 4. Fase 3 — Priorización

Cada hallazgo lleva: **qué pasa, dónde (URLs de ejemplo), por qué importa,
qué hacer**. Sin las cuatro cosas, no es un hallazgo, es una observación.

Prioriza por impacto × esfuerzo, no por número de URLs afectadas:

1. **Crítico** — bloquea indexación, canibaliza o rompe la conversión.
2. **Importante** — pierde tráfico o autoridad de forma medible.
3. **Mejora** — suma, pero no antes que lo anterior.

Y el plan de acción del informe no es una lista plana: va en **cuatro bloques
por impacto × esfuerzo**, que es lo que permite al cliente empezar el lunes.

| Bloque | Qué entra | Plazo |
|---|---|---|
| **A** | Impacto alto, esfuerzo bajo — los quick wins | 1-2 semanas |
| **B** | Impacto alto, esfuerzo medio-alto | 2-6 semanas |
| **C** | Impacto medio | Trimestre |
| **D** | Complementarias, de recorrido largo (E-E-A-T, PR, monitorización) | Continuo |

Las acciones se numeran **del 1 al N de corrido a lo largo de los cuatro
bloques**, no reiniciando en cada uno: así se puede decir «la 7» en una
reunión y todos miran lo mismo. Cada acción lleva **la referencia al apartado
que la justifica** («ver 2.2.2»), el impacto y el esfuerzo. Y las que no
deberían ejecutarse sin que las valide una persona —retiradas del índice,
redirecciones masivas, disavow— se marcan **«Para revisión humana»**. Y cuando haya datos de GSC, el
impacto va cuantificado: impresiones a consolidar, clics que no se capturan,
uplift estimado — marcado como estimación si lo es.

Los **[PF] patrones frecuentes** de la checklist son los que más se repiten
entre hoteles: revísalos siempre aunque el crawl salga limpio.

Nunca infles el informe. Un hallazgo real bien documentado vale más que
veinte genéricos. Si algo está bien, dilo: el cliente necesita saber qué no
tocar.

---

## 5. Fase 4 — Informe

**Carga la skill `paraty-tech-brand` antes de generar la pieza — es un paso
obligatorio, no una recomendación.** Léela y aplícala; no reproduzcas la
identidad de memoria. Es vinculante en colores, tipografía, logo, tono
partner, nomenclatura de producto y cifras aprobadas. Ring2Travel es marca
hermana, nunca producto de Paraty Tech, y no se critica a la competencia.

### 5.1 Marca aplicada al informe — concreto

Estos son los valores que debe cumplir el HTML, ya validados en los informes
de Landmar y METT:

- **Paleta (tokens exactos).** `--blue:#0088CC`, `--dark:#202B37`,
  `--gray:#A7A7A8`, texto tenue `#57595A`. Preferir `#202B37` al negro puro.
  Superficies en modo claro: **fondo general blanco `#FFFFFF`** (preferencia
  fija del usuario: el informe siempre con fondo blanco, no `#F5F7FA`), cards
  en `#FFFFFF` diferenciadas con borde fino gris claro y sombra sutil (nada de
  gradientes ni sombras exageradas). Para las etiquetas de prioridad usar los secundarios de la
  brand skill, con este mapeo fijo: crítico `#CC2376` (loyalty), importante
  `#F28E2A` (voz), mejora `#A3BD31` (revenue), GEO/AEO `#68AEE5` (ai-blue). No
  introducir colores fuera de estos.
- **Enlaces y AA.** El azul de marca `#0088CC` cumple contraste AA para
  botones e iconos, pero se queda corto para texto de enlace pequeño sobre
  blanco. En modo claro, el **texto de enlace usa `#0072AB`**; en modo oscuro
  puede seguir en `#0088CC`. Regla de la guía de SEO Control (ver 5.4).
- **Tipografía.** Roboto con el fallback declarado:
  `'Roboto',-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif`.
  Pesos: Thin 100 para el H1 y los números grandes de KPI, Regular 400 para
  el cuerpo, Medium 500 para H2/H3 y etiquetas. Nada de Bold ni Black.
- **Portada azul oscuro + logo blanco; el resto del informe en blanco
  (preferencia fija del usuario).** Solo la **portada** va sobre fondo azul
  oscuro `#202B37` con borde inferior azul de 4px y **logo blanco**
  (`assets/logos/logo-paraty-tech-blanco.png`); **del §1 (resumen ejecutivo) en
  adelante el fondo es blanco `#FFFFFF`**. El logo blanco se embebe como data
  URI base64 (no enlaces locales) con **altura fija (~40px) y `width:auto`**
  —`base64 -i …/logo-paraty-tech-blanco.png`—. Ojo: si la portada es un
  contenedor flex en columna, `align-items:stretch` (por defecto) estira el
  `<img>` a lo ancho y lo deforma; ponle **`align-self:flex-start`** (y un
  `max-width` de seguridad) para que respete su proporción. El H1 de
  portada es el nombre del cliente/marca a secas (p. ej. «Paraty Tech»), sin
  epígrafes tipo «Nuestra propia web».
- **Tono neutro, sin autorreferencia.** Aunque la web auditada sea la propia
  de Paraty, se trata como una web más: nada de framing tipo «auditar nuestra
  propia web es incómodo» ni «la casa del herrero». Los hallazgos van igual
  que en cualquier cliente, sin disculpas ni chascarrillos.
- **Pie.** `<Hotel> · Auditoría SEO-GEO · <mes año>` a la izquierda y
  **Paraty Tech · In technology we trust** a la derecha. El tagline siempre
  en inglés, nunca se traduce. Al ser informe de trabajo interno no hacen
  falta los contactos de mercado; si el informe se entrega al cliente, añadir
  el pie estándar de `reference/markets-contacts.md` con el contacto del
  mercado que corresponda.
- **Favicon del artefacto** (si se publica como Artifact): un emoji, coherente
  con el isotipo Y de Paraty; mantenerlo estable entre versiones.
- **Theme.** El HTML responde a claro y oscuro (`prefers-color-scheme` +
  `data-theme`), como en los informes existentes.

### 5.2 Estructura del informe

**El informe cubre toda la superficie auditada, no solo lo que falla.** Un
listado plano de N hallazgos se lee como una lista de la compra; la estructura
numerada por bloques deja ver al cliente qué se ha mirado, qué está bien y
qué hay que tocar. Esta es la estructura de referencia, la de la auditoría de
Landmar de septiembre de 2026:

| Apartado | Contenido |
|---|---|
| **0** | **Metodología y fuentes** — tabla de fuentes con código, fecha, alcance y apartados que alimenta (§1b); fuentes pendientes; advertencias de muestreo |
| — | **Índice** con todos los apartados y subapartados, y el enlace a la carpeta de anexos |
| **1** | **Situación actual** — 1.1 tráfico (GSC) · 1.2 palabras clave y clusters de oportunidad · 1.3 competencia y visibilidad (SISTRIX) |
| **2** | **Factores on-page** — 2.1 arquitectura · 2.2 rastreo y enlazado (robots, sitemap y huérfanas, 404, 3xx, subdominios, mayúsculas y no-ASCII, parámetros, etiquetas residuales en URL, canibalización por parámetros) · 2.3 titles · 2.4 meta descriptions · 2.5 encabezados · 2.6 imágenes · 2.7 canonicals · 2.8 noindex · 2.9 enlazado interno del site · 2.10 enlazado dentro de cada hotel y breadcrumb · 2.11 datos estructurados · 2.12 WPO por tipo de página · 2.13 hreflang e internacionalización · 2.14 seguridad, validación HTML y rendimiento móvil |
| **3** | **Contenidos** — canibalización en el dominio y con subdominios, optimización de fichas de hotel, de artículos y de categorías, contenidos corporativos, duplicidades y thin content, contenido y consultas sin tráfico |
| **4** | **AI Overviews y visibilidad en GEO** — medición de SISTRIX AI Check y lo que GSC reporta o no (Fase 2c), más el `llms.txt` propuesto escrito |
| **5** | **Visibilidad GEO en LLMs** — GEO Metrics: overview, prompts monitorizados, Share of Model por motor, ranking competitivo, dominios citados, recomendaciones, diagnóstico y KPIs |
| **6** | **SEO off-page** — métricas de autoridad, dónde se concentran los enlaces, anchor text, enlaces tóxicos y de calidad, targets de link building |
| **7** | **Priorización de acciones** — bloques A/B/C/D por impacto × esfuerzo (Fase 3) |
| — | **Puntos nuevos respecto a la auditoría anterior**, si hay una previa con la que comparar |
| — | **Datos pendientes** — qué falta, por qué y cómo se consigue |

Adapta la numeración a lo que tenga el cliente: si no es un hotel, los
apartados de fichas y de motor de reservas se sustituyen por lo que
corresponda. Pero **el esqueleto de 0 a 7 se mantiene**, igual que la línea de
fuente bajo cada título y los anexos.

**El resumen ejecutivo abre el cuerpo y tiene anatomía propia.** No es un
párrafo de relleno: es la pieza que lee quien decide, y en la versión de
cliente de Landmar ocupa seis bloques en este orden:

1. **Una frase de diagnóstico** que reencuadra el problema, no que lo
   enumere: «Landmar tiene un problema de captación, no de visibilidad».
   Seguida de 3-4 líneas que la sostienen con dos cifras y un ejemplo en
   lenguaje de cliente («la gente que ya conoce la marca entra, y la que busca
   “hotel todo incluido en Tenerife” ve la marca y pasa de largo»).
2. **Fila de 4 KPI** con su línea de fuente debajo.
3. **«Lo que ya funciona»**: cuatro o cinco frases, cada una con su cifra y su
   fuente entre paréntesis. El cliente necesita saber qué no tocar, y esto es
   lo que hace creíble el resto.
4. **«Dónde está el dinero»**: tabla de clusters de demanda con impresiones,
   clics y una columna «qué falla» de una línea.
5. **«Los N hallazgos que hay que atender primero»**: tres o cuatro, numerados,
   cada uno con la cifra, la fuente y la referencia al apartado («ver 2.2.2»).
6. **«Plan de trabajo»**: dos o tres líneas diciendo cuántas acciones hay y
   cómo se reparten por bloques.

Y un **recuadro de una sola frase** con la única cosa que hay que hacer si
solo se hace una: «Si solo se hace una cosa este trimestre, que sea enlazar
las 111 URLs huérfanas y sacar del noindex la landing de todo incluido. El
contenido ya está escrito y pagado. Solo hay que dejar que Google lo vea.» Es
el párrafo que se recuerda; merece la pena pelearlo.

**Lo que no va en la pieza de cliente.** El apartado «Puntos nuevos respecto a
la auditoría anterior» es control interno: sirve para no repetirse entre
auditorías, pero al cliente no le interesa qué vio o no vio la versión
pasada. Se mantiene en la versión de trabajo y se quita de la entregable.
«Datos pendientes» sí se queda, y cierra el documento.

El pie de la pieza de cliente lleva el contacto del mercado que corresponda
(`reference/markets-contacts.md` de la brand skill), no solo el tagline.

**Cada apartado y subapartado lleva, en este orden:**

1. La **línea de fuente** en cursiva (§1b).
2. **Qué pasa**, con la cifra exacta y URLs de ejemplo. Si está bien, se dice
   que está bien y con qué cifra se demuestra: el cliente necesita saber qué
   no tocar.
3. **Por qué importa**, en lenguaje de negocio.
4. **Solución propuesta**, como lista numerada de acciones concretas y en
   orden. No una frase: lo que hay que tocar, paso a paso.
5. El **enlace al anexo** con el detalle completo (§5.6).

Y hay dos cosas que separan un informe correcto de uno convincente:

- **Cruza los apartados entre sí.** «Esto conecta con 1.2», «las dos primeras
  son justo las que 2.8 propone sacar del noindex», «es la tercera vez que
  aparece el mismo patrón, con tres fuentes distintas». Cuando Search
  Console, SISTRIX y las citaciones de IA apuntan al mismo problema, dilo
  explícitamente: eso es lo que hace que el cliente actúe.
- **Cuantifica el impacto** con los datos de GSC, y marca las estimaciones
  como estimaciones.

Cuando el informe se use también como argumento comercial, cerrar con un
**caso de éxito** (una cadena similar que mejoró tras entrar en Paraty, con
datos reales de la lista aprobada de la brand skill) y, si aplica, la
recomendación de sustituir herramientas externas por las de Paraty. Es el
patrón de los informes del equipo; nunca inventar cifras del caso de éxito.

Formato por defecto: HTML autocontenido en `informes/`, nombrado
`AAAA_MM <Hotel> Informe SEO.html`, siguiendo la convención del equipo. **Para
la pieza que se entrega al cliente, el formato validado por el usuario es el
PDF corporativo multipágina del §5.5** (portada oscura, cabecera/pie con nº de
página, tabla-resumen de hallazgos con píldoras, fichas con caja RECOMENDACIÓN
y plan por fases). Un informe con esta estructura completa se va a 50-70
páginas, y eso es lo esperable: el detalle vive en los anexos, no en el
cuerpo. Si el usuario pide PPTX, usa el template de `paraty-tech-brand`
(`templates/pptx/pptx_template.py`).

### 5.3 Pre-flight antes de entregar

Repasar el `checklist.md` de la brand skill. Como mínimo: logo correcto para
el fondo, paleta sin colores no autorizados, Roboto con fallback, tono
partner sin buzzwords, Ring2Travel como marca hermana, sin críticas a la
competencia, y cifras de Paraty solo de la lista aprobada.

### 5.4 Guía de diseño de SEO Control

`reference/seo-control-guia-diseno.md` es la guía visual de la herramienta
interna SEO Control de Paraty Tech. Define la misma identidad que aplicamos a
los informes (azul `#0088CC`, Roboto, superficies claras, tono partner), así
que **el informe debe verse como parte del mismo sistema**. De ahí salen las
superficies claras y el azul de enlace AA `#0072AB` de la sección 5.1.

Es una guía pensada para una app Next.js/Tailwind/shadcn; de ella se toma la
**identidad visual** (color, tipografía, superficies, radios suaves, aire,
badges de estado por color), no el stack. Consúltala cuando haya que decidir
un detalle visual que 5.1 no cubra, o si algún día se genera una interfaz y
no solo un informe.

### 5.5 Formato PDF corporativo multipágina (preferido para entrega a cliente)

Formato validado por el usuario como estándar de entrega. HTML como fuente,
PDF A4 como pieza final. **Ejemplo canónico a clonar:**
`reference/ejemplo-informe-pdf-corporativo.html` (auditoría METT). Estructura:

1. **Portada** a sangre, fondo `#202B37`, logo Paraty **blanco**, «Auditoría
   SEO» en peso 300, subtítulo en azul grisáceo, y abajo bloque de metadatos
   (Cliente / destinos / Fecha) + «In technology we trust.». Sin cabecera ni pie.
2. **Cabecera y pie corriendo en cada página de contenido**: logo Paraty color
   (izq.) + «Auditoría SEO · <Cliente>» (der.) con línea fina; pie con
   `Paraty Tech · paratytech.com` · contacto de mercado · «Página N».
3. **Fila de 3 tarjetas KPI** con borde izquierdo de color (azul / magenta /
   naranja) y número grande en peso 300.
4. **Cuadro de hallazgos**: tabla con cabecera `#202B37`, filas alternas y
   **píldora de prioridad** (Alta `#CC2376` / Media `#F28E2A` / Baja `#A3BD31`)
   + columna de ámbito.
5. **Hallazgos en detalle**: cada uno con badge numerado `#202B37`, título,
   píldora de prioridad y caja **RECOMENDACIÓN** con borde del color de la
   prioridad.
6. **Lo que ya está bien** (lista con check) — mantiene la honestidad del §6.
7. **Plan de acción priorizado por fases** (tabla Fase / Acción / Prioridad).
8. Cierre con tagline aprobado.

Mapeo de prioridad al lenguaje de la Fase 3: Crítico→**Alta**, Importante→
**Media**, Mejora→**Baja**. El eyebrow y los acentos usan azul `#0093D0`.

**Receta técnica de render (no obvia — respétala):**
- Render: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=<out>.pdf
  file://<in>.html`. `--no-pdf-header-footer` quita la fecha/URL por defecto de
  Chrome pero **mantiene** los margin boxes de `@page`.
- La cabecera y el pie corriendo **deben ir en `@page` margin boxes**
  (`@top-left`/`@top-right`, `@bottom-left`/`@bottom-center`/`@bottom-right`),
  **no** con `position:fixed`: este Chrome coloca los `fixed` dentro de la caja
  de contenido y pisan el H1. Número de página con
  `@bottom-right{content:"Página " counter(page)}`.
- Portada limpia: `@page:first{margin:0; @top-*{content:""} @bottom-*{content:""}}`
  y la portada como bloque a sangre 210×297mm con `z-index` alto (tapa cualquier
  chrome en la página 1).
- El logo de la cabecera va en un margin box con `content:url(<datauri>)`, que
  se renderiza **a tamaño natural**: incrusta una copia **rasterizada pequeña**
  (~44 px de alto; `sips --resampleHeight 44 logo.png --out logo44.png` y luego
  a data URI base64) o saldrá gigante.
- Margen superior ~27mm para que el contenido no toque la línea de la cabecera.
- Verificación: `qlmanage -t -s 1100 -o <dir> <pdf>` solo saca la **página 1**
  (la portada). Para revisar una página de contenido, genera una copia sin la
  portada y con el bloque `@page:first` neutralizado, y saca su página 1. En
  esta sesión no había `poppler`/`gs`/`pdftoppm`, solo `qlmanage`/`sips`.

Nombrado: `AAAA_MM <Hotel> Informe SEO (formato corporativo).pdf` con el HTML
fuente al lado en `informes/`.

### 5.6 Anexos — el detalle no va en el cuerpo del informe

**Toda lista de URLs va a un anexo, no al informe.** El cuerpo lleva la cifra,
dos o tres ejemplos y el enlace; el anexo lleva las 111 URLs con su estado.
Así el informe se lee y el detalle se puede trabajar. La auditoría de Landmar
de septiembre de 2026 tiene **77 anexos**, y es la razón por la que el
documento se sostiene en 60 páginas en vez de 300.

Cómo se montan, con el MCP de Google Drive:

1. **Una carpeta por auditoría**: `create_file` con
   `contentMimeType: application/vnd.google-apps.folder`, nombrada
   `Anexos SEO - <Cliente> - <Mes Año>`.
2. **Un Sheet por lista**, dentro de esa carpeta (`parentId`): sube el CSV con
   `create_file` y `contentMimeType: text/csv` y Drive lo convierte a Sheet.
   Nombres descriptivos y con prefijo de fuente: `Anexo SEO - URLs huerfanas`,
   `Anexo GSC - Keywords segunda pagina`, `Anexo Sistrix - Backlinks de spam`,
   `Anexo GEO - URLs citadas por la IA`.
3. **Si una lista es muy larga, pártela** en `… parte 1`, `… parte 2`, y
   enlázalas todas desde el apartado.
4. **Cada anexo se enlaza desde el apartado que lo usa**, con la fórmula
   «Podéis encontrar todas las URLs en: …», y la carpeta completa se enlaza
   además desde la cabecera del informe y desde el índice.
5. Las columnas son **las que hacen falta para trabajar el anexo**, no un
   volcado del crawler: URL, el dato del hallazgo, y la decisión o prioridad
   cuando aplique.

Anexos que salen en casi cualquier auditoría:

- **Del crawl**: URLs del sitemap con su estado y si están enlazadas
  internamente; URLs huérfanas aisladas; errores 4xx; redirecciones 3xx con el
  número de enlaces internos que las apuntan; titles y meta descriptions
  duplicados o fuera de longitud; encabezados; imágenes sin alt y por peso;
  canonicals; noindex; recuento de palabras; thin content; cabeceras de
  seguridad ausentes; y el **resumen de problemas del crawl ordenado por
  gravedad**, que es el que da la vista de pájaro.
- **De datos estructurados**: cobertura por plantilla, resumen de validación
  con cada error y aviso y sus URLs afectadas, URLs con errores que bloquean
  el resultado enriquecido, URLs sin ningún marcado, y el detalle URL a URL.
- **De hreflang**: con vuelta a noindex, hacia URLs sin código 200, y sin
  enlace de vuelta.
- **De Search Console**: evolución mensual; keywords de marca y de no-marca;
  keywords por clics; keywords de segunda página; un anexo por cluster de
  oportunidad; países; dispositivos; URLs por idioma; URLs con más tráfico;
  URLs con impresiones y cero clics.
- **De SISTRIX**: visibilidad frente a competidores; evolución del índice;
  distribución de rankings; competidores orgánicos; oportunidades de
  keywords; tráfico estimado por sección; URLs más enlazadas; anchor text;
  backlinks de spam; backlinks de calidad.
- **De GEO**: prompts con respuesta de IA; URLs propias citadas; dominios
  citados junto al cliente; URLs externas más citadas; marcas que compiten en
  las respuestas; evolución de prompts.

Si no hay acceso a Drive, los anexos se entregan como CSV en
`informes/anexos/<cliente>-<mes>/` y el informe enlaza las rutas relativas.
Lo que no se hace nunca es meter una lista de 300 URLs en el cuerpo del PDF ni
dejarla sin entregar.

---

## 6. Reglas de honestidad del informe

- Lo que no has podido comprobar se dice, no se rellena.
- Nada de métricas inventadas: si no la has medido, no la pongas.
- Las cifras corporativas de Paraty solo salen de la lista aprobada de la
  brand skill.
- Si un hallazgo depende de una hipótesis, se marca como hipótesis y se
  indica cómo confirmarla.
- Lo pendiente se recoge **dos veces**: en la tabla de fuentes del apartado 0
  y en la sección final «Datos pendientes», con el motivo y cómo se consigue.
- Las advertencias de muestreo se escriben, no se omiten porque afeen la
  cifra.
