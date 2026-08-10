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

Del crawl saca, como mínimo: códigos de respuesta y cadenas de redirección,
canonicals, meta robots, titles y meta descriptions (duplicados y longitud),
H1/H2, hreflang, imágenes sin alt y sobredimensionadas, enlaces internos y
rotos, profundidad de clic, datos estructurados y ratio texto/HTML.

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

## 3b. Fase 2b — Off-page y autoridad

Era el mayor punto ciego del método: mide la autoridad, el perfil de enlaces
y el tráfico orgánico. Todo vía **Supermetrics** (flujo: `data_source_discovery`
→ `accounts_discovery` → `field_discovery` → `data_query`). Orden de
preferencia, del dato más fiable y gratis al estimado:

1. **Google Search Console** (`ds_id=GW`) — la fuente primero: enlaces que
   Google **de verdad** cuenta (sitios que más enlazan, páginas más
   enlazadas, textos de anclaje) y el tráfico orgánico real (clics,
   impresiones, queries). Requiere que el hotel dé acceso a la propiedad.
2. **Ahrefs** (`ds_id=AHRF2`) o **Semrush** (`ds_id=SR`) — profundidad de
   off-page: Domain Rating / Authority Score, dominios de referencia,
   **crecimiento de backlinks en el tiempo** (para pillar picos raros que
   pidan disavow) y anchors. Necesita cuenta del hotel/agencia en esa
   herramienta.
3. **Similarweb** (`ds_id=SW`) — tráfico y engagement estimados; sirve para
   **comparar con la competencia** sin necesitar sus accesos.
4. **Google Trends** (`ds_id=GT`, sin login) — interés de marca vs genéricas
   y estacionalidad; disponible siempre, útil aunque no haya ningún acceso.

Qué llevar al informe: autoridad del dominio y evolución, nº de dominios de
referencia y calidad, **picos anómalos de enlaces** (riesgo de SEO negativo →
disavow), reparto marca vs genéricas del tráfico, y comparación con 1-2
competidores de la misma plaza. Si no hay ningún acceso ni cuenta, dilo y
tira de Trends y Similarweb (estimados), marcándolo como estimación.

---

## 4. Fase 3 — Priorización

Cada hallazgo lleva: **qué pasa, dónde (URLs de ejemplo), por qué importa,
qué hacer**. Sin las cuatro cosas, no es un hallazgo, es una observación.

Prioriza por impacto × esfuerzo, no por número de URLs afectadas:

1. **Crítico** — bloquea indexación, canibaliza o rompe la conversión.
2. **Importante** — pierde tráfico o autoridad de forma medible.
3. **Mejora** — suma, pero no antes que lo anterior.

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

Estructura que funciona (la de los informes mensuales del equipo):

1. Portada — fondo azul oscuro `#202B37` con logo blanco (altura fija, sin
   estirar), marca/hotel como H1, URL, fecha, alcance del crawl. El cuerpo del
   informe (del §1 en adelante) va sobre blanco.
2. Resumen ejecutivo — 5-8 líneas, lo crítico primero, en lenguaje de
   negocio, no de crawler. Rematar con una fila de KPI (3-4 cifras).
3. Hallazgos por bloque, en el orden de la checklist, cada uno con su
   etiqueta de prioridad y las cuatro partes de la Fase 3. Incluye un bloque
   de **off-page y autoridad** (Fase 2b) cuando haya datos.
4. Plan de acción priorizado — qué se toca primero y quién lo toca
   (hotel, desarrollo, Paraty).
5. Método y limitaciones — qué se auditó y qué quedó sin comprobar y por qué.

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
y plan por fases). Si el usuario pide PPTX, usa el template de `paraty-tech-brand`
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

---

## 6. Reglas de honestidad del informe

- Lo que no has podido comprobar se dice, no se rellena.
- Nada de métricas inventadas: si no la has medido, no la pongas.
- Las cifras corporativas de Paraty solo salen de la lista aprobada de la
  brand skill.
- Si un hallazgo depende de una hipótesis, se marca como hipótesis y se
  indica cómo confirmarla.
