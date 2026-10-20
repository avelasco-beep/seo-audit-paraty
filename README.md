# Auditoría SEO-GEO — Herramienta

Herramienta interna de Paraty Tech para auditar la web de un hotel (o cualquier
sitio) con enfoque **SEO técnico + GEO/AEO** (ser citado por ChatGPT, Perplexity y
AI Overviews) y entregar un informe accionable con la identidad corporativa.

> **Repositorio privado.** Contiene metodología interna. Los datos de cliente
> (`informes/`) y los secretos (claves de API, credenciales) **no** se versionan.

## Contenido

```
.claude/skills/auditoria-seo-geo/
├── SKILL.md                     # Proceso, fuentes y formato del informe
├── reference/
│   ├── checklist.md             # Lista de comprobaciones
│   ├── checklist-auditoria-seo.html
│   ├── ejemplo-informe-pdf-corporativo.html   # Plantilla de informe corporativo
│   └── seo-control-guia-diseno.md
└── scripts/
    ├── psi.py                   # PageSpeed Insights / Core Web Vitals
    └── geo-redirect.sh          # Detección de redirección por idioma/geo
```

## Requisitos

- **Python 3** (solo librería estándar — sin dependencias que instalar).
- **curl** (para `geo-redirect.sh`).
- Opcional: [`uv`/`uvx`](https://docs.astral.sh/uv/) para el MCP de Search Console.

## Configuración (claves en variables de entorno)

Las claves **no** están en el código; se leen del entorno para que el repo sea
independiente. Copia la plantilla y rellena la tuya:

```bash
cp .env.example .env          # y edita .env con tu PAGESPEED_API_KEY
export $(grep -v '^#' .env | xargs)   # carga las variables en tu shell
```

`psi.py` también acepta la clave en `~/.config/paraty/pagespeed.key` como alternativa.

## Uso

```bash
# Core Web Vitals + Lighthouse (móvil y escritorio) de una o varias URLs
PAGESPEED_API_KEY=xxxx python3 .claude/skills/auditoria-seo-geo/scripts/psi.py \
  https://ejemplo.com/ https://ejemplo.com/ficha.html

# ¿La home redirige según idioma / Googlebot?
bash .claude/skills/auditoria-seo-geo/scripts/geo-redirect.sh https://ejemplo.com/
```

## Servidores MCP (opcional)

Copia la plantilla y ajusta las rutas a tu máquina:

```bash
cp .mcp.json.example .mcp.json
```

- **screaming-frog**: servidor MCP integrado de Screaming Frog. Requiere **modo
  Base de Datos** (Configuración → Sistema → Modo de almacenamiento) y el
  servidor MCP arrancado; en modo memoria no levanta.
- **semrush**: [MCP de Semrush](https://mcp.semrush.com/v2/mcp) por OAuth.
  Consume unidades de API por línea devuelta, así que conviene `display_limit`
  bajo.
- **gscServer**: [`mcp-search-console`](https://github.com/AminForou/mcp-gsc) para
  conectar Google Search Console. Necesita credenciales OAuth de Google Cloud
  (ver `.env.example`).

Además, el proceso de `SKILL.md` se apoya en conectores de claude.ai que se
autorizan desde la propia cuenta, no desde este repositorio: **SISTRIX**
(visibilidad, enlaces y AI Check), **GEO Metrics** (visibilidad en LLM),
**Google Drive** (los anexos del informe) y **Supermetrics** (alternativa para
GSC, Ahrefs, Similarweb y Trends). Cada apartado del informe declara de qué
fuente sale; ver §1b de `SKILL.md`.

## Convenciones

- Los informes finales se guardan en `informes/` (ignorada por Git: datos de cliente).
- Formato de entrega: HTML autocontenido y, para cliente, PDF corporativo (ver SKILL.md).
