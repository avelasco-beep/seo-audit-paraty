#!/usr/bin/env python3
"""
Consulta Core Web Vitals a la API de PageSpeed Insights (la misma que
pagespeed.web.dev) para una URL, en móvil y escritorio.

Uso:
    PAGESPEED_API_KEY=xxxx python3 psi.py <url> [<url> ...]

La clave se lee de la variable de entorno PAGESPEED_API_KEY. Si no está,
intenta leerla del archivo ~/.config/paraty/pagespeed.key.
Sin clave, la API responde 429 (cuota anónima compartida) y el script lo
dice claramente en vez de inventar datos.

Devuelve JSON por stdout con, para cada URL y estrategia:
  - puntuaciones performance / seo / accessibility / best-practices
  - métricas de laboratorio: LCP, CLS, TBT, FCP, Speed Index, TTI
  - métricas de campo (CrUX) si Google tiene datos reales de usuarios: el
    p75 y la categoría (FAST/AVERAGE/SLOW) de LCP, CLS, INP, FCP, TTFB
"""
import sys, os, json, urllib.request, urllib.parse, urllib.error

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
LAB = {
    "largest-contentful-paint": "LCP",
    "cumulative-layout-shift": "CLS",
    "total-blocking-time": "TBT",
    "first-contentful-paint": "FCP",
    "speed-index": "SpeedIndex",
    "interactive": "TTI",
    "server-response-time": "TTFB",
}
FIELD = {
    "LARGEST_CONTENTFUL_PAINT_MS": "LCP",
    "CUMULATIVE_LAYOUT_SHIFT_SCORE": "CLS",
    "INTERACTION_TO_NEXT_PAINT": "INP",
    "FIRST_CONTENTFUL_PAINT_MS": "FCP",
    "EXPERIENCE_TIME_TO_FIRST_BYTE": "TTFB",
}


def get_key():
    k = os.environ.get("PAGESPEED_API_KEY", "").strip()
    if k:
        return k
    p = os.path.expanduser("~/.config/paraty/pagespeed.key")
    if os.path.exists(p):
        return open(p).read().strip()
    return None


def query(url, strategy, key):
    params = {
        "url": url,
        "strategy": strategy,
        "category": ["performance", "seo", "accessibility", "best-practices"],
    }
    if key:
        params["key"] = key
    q = urllib.parse.urlencode(params, doseq=True)
    try:
        with urllib.request.urlopen(f"{API}?{q}", timeout=120) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            msg = json.loads(body)["error"]["message"]
        except Exception:
            msg = body[:200]
        return {"error": f"{e.code}: {msg}"}
    except Exception as e:
        return {"error": str(e)[:200]}

    lr = d.get("lighthouseResult", {})
    cats = lr.get("categories", {})
    audits = lr.get("audits", {})
    out = {
        "scores": {
            k: (round(v["score"] * 100) if v.get("score") is not None else None)
            for k, v in cats.items()
        },
        "lab": {},
        "field": {},
    }
    for aid, name in LAB.items():
        a = audits.get(aid)
        if a:
            out["lab"][name] = {"value": a.get("displayValue"), "score": a.get("score")}
    metrics = d.get("loadingExperience", {}).get("metrics", {})
    for mid, name in FIELD.items():
        m = metrics.get(mid)
        if m:
            out["field"][name] = {"p75": m.get("percentile"), "category": m.get("category")}
    out["field_data"] = bool(metrics)
    return out


def main():
    urls = sys.argv[1:]
    if not urls:
        print("uso: python3 psi.py <url> [<url> ...]", file=sys.stderr)
        sys.exit(2)
    key = get_key()
    result = {"has_key": bool(key), "results": {}}
    for u in urls:
        result["results"][u] = {s: query(u, s, key) for s in ("mobile", "desktop")}
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
