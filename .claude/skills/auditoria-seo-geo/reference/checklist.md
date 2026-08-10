# Checklist de auditoría SEO-GEO — hoteles con motor de reservas

Fuente canónica: `checklist-auditoria-seo.html` (misma carpeta). Este .md es la versión legible para el agente.
Leyenda de prioridad: **[C]** crítico · **[I]** importante · **[M]** mejora · **[PF]** patrón frecuente en hoteles · **[GEO]/[AEO]** motores generativos.

## 0. Accesos y punto de partida

_Antes de auditar: confirmar qué tenemos y a qué damos acceso._

- [ ] **¿Tiene web y motor?** — Confirmar que existe web corporativa y motor de reservas asociado.
- [ ] **Acceso a Perfil de Empresa de Google (GMB)** — Confirmar si tenemos acceso al panel.
- [ ] **Acceso a Microsoft Clarity** — Para heatmaps y grabaciones de sesión.
- [ ] **Acceso a Google Search Console** — Para impresiones, queries, indexación y sitemaps.
- [ ] **Acceso a Bing Webmaster Tools** — Cobertura, sitemap y rendimiento en Bing.
- [ ] **Carpeta de optimizaciones** — Si algo no está optimizado, comprobar si tenemos la carpeta de optimizaciones del hotel.

## 1. Indexación y rastreo

_Que Google rastree e indexe la versión correcta, sin duplicados, bloqueos ni desperdicio de crawl budget._

- [ ] **Canonical** [C] — Existe, apunta a la versión correcta y sin cadenas de canonicals.
- [ ] **Meta robots / X-Robots-Tag** [C] — Sin noindex ni nofollow accidentales. Las directivas deben ir dentro del <head>.
- [ ] **Sin noindex y canonical a la vez** — Señales contradictorias; una URL noindex no debe llevar canonical.
- [ ] **robots.txt** — No bloquea recursos de render (CSS/JS) ni secciones que deban indexar.
- [ ] **Sitemap.xml depurado** — Sin 3xx/4xx ni canonicalizadas, sin changefreq/priority; separar web y blog y añadir sitemap de imágenes.
- [ ] **Código de respuesta y redirecciones** [I] — 200 correcto; sin cadenas ni bucles 301/302/307.
- [ ] **404 real y página 404 útil** [I] — Las URLs inexistentes devuelven 404, no 302 a la home; página 404 con menú, buscador y enlazado.
- [ ] **Sin soft 404** — Nada de 200 OK mostrando "Error 404" e indexable.
- [ ] **URLs con mayúsculas: 301 a minúsculas** [PF] — No basta la canonical; redirigir para no arrastrar duplicidad.
- [ ] **URLs con acentos o no ASCII** [PF] — Suelen devolver 404; implementar 301 automática a la versión normalizada.
- [ ] **Filtros de búsqueda/reservas: noindex,follow** — La canonical no es directiva; sin noindex pueden acabar indexando.
- [ ] **Buscadores internos y entornos de test** — Generan URLs thin/duplicadas; marcar noindex,follow y no enlazar a staging.
- [ ] **Parámetros y UTM** [I] — namespace/fechas del motor no generan duplicados; UTM solo en enlaces externos entrantes, nunca internos.
- [ ] **Enlaces internos a páginas no indexables** [PF] — Área de cliente, legales y formularios en footer/menú: nofollow o fuera de zonas globales.
- [ ] **Enlaces internos siempre a 200** — Evitar enlazar a 3xx y a 403 (típico en imágenes con permiso denegado).
- [ ] **PDFs y subdominios residuales** — PDFs indexables sueltos (canonical vía header) y recursos fuera de www bajo control.
- [ ] **Redirección http a https** [C] — Todo el http fuerza a https con 301.
- [ ] **Coherencia de dominio** — Una sola versión: www vs no-www y con/sin barra final unificados con 301.
- [ ] **Sitemap enviado en GSC y en Bing** — Verificar que el sitemap.xml está dado de alta en Search Console y en Bing Webmaster Tools.
- [ ] **Archivo llms.txt** [M] — Buena práctica emergente para guiar a los buscadores con IA.

## 2. Contenido y semántica

_Etiquetas, jerarquía, duplicidades, idiomas y datos estructurados._

- [ ] **Title** [C] — Longitud adecuada, con keyword y marca, sin duplicar entre páginas y distinto del H1.
- [ ] **Meta description** — Única, atractiva y en el rango de longitud recomendado.
- [ ] **Un solo H1 y jerarquía correcta** [I] — H2-H3 sin saltos ni encabezados desordenados.
- [ ] **Duplicidades de texto** [I] — Entre fichas de hotel, entre idiomas, FAQs repetidas o contenido delgado; diferenciar o consolidar con canonical.
- [ ] **Sin cloaking** [C] — Mismo contenido a bots y usuarios; servir distinto puede acarrear penalización manual.
- [ ] **Módulos de FAQs con FAQPage** [PF] — En hoteles, destinos y landings de servicios; hoy suelen faltar por completo.
- [ ] **Alt en imágenes** — Presentes y descriptivos, no vacíos.
- [ ] **Datos estructurados ampliados** [PF] — Además de Hotel/Product/Breadcrumb/FAQ/Review: ItemList, Offer, HotelRoom, ImageObject, LocalBusiness/Organization, VideoObject, ContactPage, HowTo, Person.
- [ ] **Schema válido y coherente** — Un único marcado Hotel por página; @id/url del JSON-LD igual a la canónica; BreadcrumbList con migas visibles.
- [ ] **hreflang** [C] — En multiidioma, con retorno recíproco y x-default.
- [ ] **Ratio texto/HTML y legibilidad** — Suficiente texto real frente al maquetado; frases claras para usuario y para IA.
- [ ] **Frescura** — Fecha de publicación o actualización visible y en datos estructurados.
- [ ] **Open Graph y Twitter Cards** — og:title, og:image, og:description y equivalentes Twitter, por el CTR al compartir.

## 3. Enlaces internos

_Bloque clave y casi siempre débil: cómo se reparte la autoridad dentro del sitio._

- [ ] **Anchor text descriptivo** [PF] — Enlazar con la keyword o el nombre del hotel/sección, no "Saber más", "Ver más" o "Descubre".
- [ ] **Que los botones sean enlaces reales** [I] — Elementos con clases CSS/JS sin <a href> no transmiten enlazado.
- [ ] **Módulos de relacionados** — Hoteles y artículos relacionados por destino, cercanía o categoría en fichas y posts.
- [ ] **Enlaces contextuales en el contenido** — Dentro del cuerpo de artículos y secciones, no solo en navegación.
- [ ] **No depender de las cookies** — Los módulos de enlazado deben verse aunque no se acepte el banner; si no, los bots no los ven.

## 4. Arquitectura de URLs y secciones

_Estructura de contenidos que buscadores y LLMs entienden mejor._

- [ ] **Landings por sección del hotel** [PF] — Habitaciones, servicios, galería, ofertas, spa en URLs propias, no todo en una ficha.
- [ ] **Landings y listados de destino** [PF] — "Hoteles en [destino]" con texto propio y FAQs para atacar genéricas y contextualizar fichas.
- [ ] **URLs semánticas y jerárquicas** — hotel/sección con keyword de destino, actualizando enlazado y migas con su 301.
- [ ] **URLs de eventos sin año** — Usar URL perenne (/comuniones/) y redirigir las anuales para acumular autoridad.
- [ ] **Sin genéricas que canibalicen la home** — Retirar "hoteles y destinos" que compiten con la home; colgar fichas del dominio.

## 5. Internacionalización

_Más allá del hreflang: cómo se cambia de idioma y de mercado._

- [ ] **Selector de idioma con enlace directo** [PF] — <a href> a la URL traducida equivalente, no a la home ni por redirección JS.
- [ ] **Popup de geolocalización** [M] — Sugerir dominio/idioma sin redirección forzada, útil con dominios en varios países.

## 6. Rendimiento y Core Web Vitals

_Velocidad real, estabilidad visual, imágenes y peso de scripts, con foco en hero y GTM._

- [ ] **LCP, CLS e INP** [C] — Identificar qué elemento marca el LCP (a menudo el hero con lazyload mal puesto).
- [ ] **Lazyload en imágenes principales** [I] — El hero y lo above the fold no deben llevar lazyload.
- [ ] **Carruseles infinitos** — Que no carguen imágenes de más ni bloqueen el hilo principal.
- [ ] **Peso del GTM** [I] — Número de tags, píxeles y scripts de terceros que cargan.
- [ ] **Imágenes al tamaño mostrado** [PF] — WebP/AVIF con srcset/sizes; no servir una grande reescalada por CSS; con width/height.
- [ ] **Imágenes en <img>, no en background CSS** — Las de fondo pierden alt y width/height.
- [ ] **Nombres de archivo SEO-friendly** — Con guiones y keyword, sin espacios ni guiones bajos.
- [ ] **TTFB, caché y HTTP/2-3** — Respuesta del servidor, TTL de caché y protocolo como palancas del LCP.
- [ ] **JS y CSS que bloquean el render** — Minimizados y diferidos donde sea posible.
- [ ] **preconnect / preload** — Hacia recursos críticos y el dominio del motor de reservas.
- [ ] **Peso de página, DOM y fuentes** — Controlados; fuentes web con preload y font-display.
- [ ] **Métricas de laboratorio y Lighthouse** [M] — FCP, Speed Index, TTI, TBT; puntuaciones Performance, Best Practices, Accessibility y SEO.
- [ ] **Accesibilidad WCAG AA** — Nombre accesible en botones/enlaces, label en formularios, contraste.
- [ ] **AMP / PWA** [M] — Si existen, bien implementados y sin generar duplicados.

## 7. Técnico y seguridad

_HTTPS, cabeceras, enlaces rotos y usabilidad móvil._

- [ ] **HTTPS y mixed content** [C] — Certificado correcto y sin recursos servidos por HTTP.
- [ ] **Cabeceras de seguridad** — HSTS, Content-Security-Policy, X-Frame-Options, X-Content-Type-Options.
- [ ] **Enlaces rotos** [I] — Internos y externos, con sus códigos de estado.
- [ ] **Breadcrumbs y profundidad de clic** — Migas coherentes y páginas clave a pocos clics.
- [ ] **Usabilidad móvil** — Viewport correcto, favicon y experiencia móvil real.

## 8. Ficha de Google (Perfil de Empresa)

_Clave en hoteles: muchas reservas y llamadas salen de aquí antes de entrar en la web._

- [ ] **NAP coherente** [C] — Nombre, dirección y teléfono idénticos a la web; sin fichas duplicadas ni fantasma.
- [ ] **Búsqueda de marca en Google** [C] — Buscar el nombre del hotel y revisar qué muestra Google: ficha, sitio, opiniones y coherencia general.
- [ ] **Menciones del nombre anterior (rebranding)** [PF] — Tras un cambio de nombre, muchos sitios, directorios y citas siguen usando el nombre antiguo; unificar como con el NAP.
- [ ] **Categorías** — Principal correcta (Hotel, Hotel de playa) y secundarias bien elegidas.
- [ ] **Redes sociales integradas** — Perfiles sociales vinculados a la ficha y coherentes con la marca.
- [ ] **Sección de descripción** — Descripción de la ficha completa y con las keywords relevantes.
- [ ] **Enlaces** — Sitio web y enlace de reservas al motor con parámetros limpios y UTM de control.
- [ ] **Horarios** — Horarios, especiales de temporada y zona horaria correctos.
- [ ] **Descripción y atributos** — Descripción completa con keywords; atributos activados (piscina, parking, wifi, mascotas).
- [ ] **Fotos** — Suficientes y actualizadas (fachada, habitaciones, zonas comunes, logo) en buena resolución.
- [ ] **Reseñas** [I] — Volumen, nota media, ritmo de entrada y porcentaje de respuesta del hotel.
- [ ] **Preguntas y publicaciones** — Q&A sin respuestas de terceros y Posts/ofertas recientes.
- [ ] **Coherencia con la web** — Alineada con los datos estructurados de tipo Hotel del sitio.

## 9. GEO, AEO y entidad de marca

_Ser citado por ChatGPT, Perplexity y AI Overviews, y que Google entienda bien la marca._

- [ ] **Señales E-E-A-T y autoría** [GEO] — Autores/expertos verificados (director, revenue, chef) con credenciales y schema Person.
- [ ] **Claridad de entidades** [GEO] — Hotel, marca y ubicación sin ambigüedad y conectados con datos estructurados.
- [ ] **Desambiguación de la marca** [I] — Si el buscador la confunde con otros grupos: "Sobre nosotros", sede, consolidar knowledge graph.
- [ ] **Opiniones propias** — Secciones de opiniones en home y fichas enlazando a los GBP, para no ceder "opiniones [marca]" a terceros.
- [ ] **Densidad factual** [GEO] — Datos concretos (distancias, precio desde, nº de habitaciones, servicios) frente a relleno.
- [ ] **Respuesta directa y FAQ/HowTo** [GEO] — Responder en las primeras líneas; encabezados como pregunta con FAQPage/HowTo schema.
- [ ] **Off-page y backlinks** — Autoridad y perfil de enlaces del país objetivo; monitorizar a la competencia.

## 10. Motor, analítica y estrategia

_Continuidad de medición y lectura de datos para priorizar._

- [ ] **Continuidad de medición web-motor** [I] — El Page View dispara en ambos contextos aunque no coincidan los IDs (regex de activador).
- [ ] **URLs del motor** — No genera URLs indexables basura; enlaces limpios y sin nofollow innecesario.
- [ ] **Logo del motor (host logo) enlaza a la web** — En el proceso de reserva, el logo debe llevar a la misma web y sin redirección.
- [ ] **Configuración del motor coherente** — Revisar ajustes detectados (p. ej. ocupación mal configurada) frente al contenido de la ficha.
- [ ] **Dependencia de marca vs genérico (GSC)** [PF] — Si casi todo el tráfico es de marca o UTMs de GBP, las secciones no posicionan por genéricas.
- [ ] **Solape SEM/SEO en marca** — Si el SEO ya está en top de marca, reasignar presupuesto SEM a genéricas con volumen.
- [ ] **Keywords en segunda página** [M] — Con volumen e impresiones altas: empujarlas al Top 10 (también ayuda a ser citado por LLMs).
- [ ] **Seguimiento de rankings** — Marca, "hotel + destino" y genéricas, para cruzar con los hallazgos técnicos.

