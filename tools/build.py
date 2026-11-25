"""Build the portfolio from data/site.json: / (Spanish), /en/ (English), 404, sitemap, robots.

Run: python3 tools/build.py   — never hand-edit the generated .html files.
"""
import json
import os
from html import escape as e

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(ROOT, "data/site.json"), encoding="utf-8"))
SITE = S["siteUrl"]
V = {"css": 1, "js": 1}
LANGS = S["langs"]


def icon(paths, cls="i"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths}</svg>')


I_ARROW = icon('<path d="M7 17 17 7"/><path d="M8 7h9v9"/>')
I_DOWN = icon('<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>')
I_PIN = icon('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>')
I_SUN = icon('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>', "i i-sun")
I_MOON = icon('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/>', "i i-moon")
I_IN = icon('<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>')
I_GH = icon('<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.1-1.3-.3-2.5-1-3.5.3-1.2.3-2.4 0-3.5 0 0-1 0-3 1.5a10.4 10.4 0 0 0-5.5 0C6.5 2 5.5 2 5.5 2c-.3 1.1-.3 2.3 0 3.5A5.4 5.4 0 0 0 4.5 9c0 3.5 3 5.5 6 5.5-.4.5-.8 1-1 1.6-.2.6-.3 1.2-.2 1.9v4"/><path d="M9 18c-4.5 2-5-2-7-2"/>')

SECTION_IDS = ["ahora", "caso", "trayectoria", "proyectos", "contacto"]
SECTION_IDS_EN = ["now", "case", "career", "projects", "contact"]


def ext(href, label, ui, cls="", inner=None):
    """External link: new tab, announced to screen readers."""
    c = f' class="{cls}"' if cls else ""
    return (f'<a{c} href="{e(href)}" target="_blank" rel="noopener">{inner or e(label)}'
            f'<span class="sr-only"> {e(ui["newTab"])}</span></a>')


def head(L, key, title, desc, canonical, alternates, noindex=False):
    alt = "".join(f'<link rel="alternate" hreflang="{h}" href="{u}">' for h, u in alternates)
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    pre = "../" * canonical.replace(SITE, "").count("/") if not noindex else "/"
    css = f'{pre}assets/css/site.css?v={V["css"]}' if not noindex else f'/assets/css/site.css?v={V["css"]}'
    js = f'{pre}assets/js/site.js?v={V["js"]}' if not noindex else f'/assets/js/site.js?v={V["js"]}'
    fav = f'{pre}assets/img/favicon.svg' if not noindex else "/assets/img/favicon.svg"
    return f"""<!doctype html>
<html lang="{L['htmlLang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{canonical}">{alt}
<meta name="theme-color" content="#0E1013">
<meta property="og:type" content="profile">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{L['locale']}">
<meta property="og:image" content="{SITE}assets/img/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{fav}" type="image/svg+xml">
<script>try{{var t=localStorage.getItem("theme");if(t==="light")document.documentElement.dataset.theme="light"}}catch(_){{}}</script>
<link rel="stylesheet" href="{css}">
<script src="{js}" defer></script>
</head>"""


def header(L, key, home, other_href):
    ui = L["ui"]
    ids = SECTION_IDS if key == "es" else SECTION_IDS_EN
    nav = "".join(f'<li><a href="{home}#{i}">{e(n)}</a></li>' for i, n in zip(ids, ui["nav"]))
    other = "en" if key == "es" else "es"
    return f"""<a class="skip" href="#main">{e(ui['skip'])}</a>
<header class="top"><div class="wrap top-in">
<a class="brand" href="{home}">vm<span class="brand-dot">.</span></a>
<nav aria-label="{e(ui['navLabel'])}"><ul class="nav">{nav}</ul></nav>
<div class="tools">
<a class="tool lang" href="{other_href}" hreflang="{other}" lang="{other}"><span aria-hidden="true">{ui['otherLangShort']}</span><span class="sr-only">{e(ui['otherLang'])}</span></a>
<button class="tool theme" type="button" hidden data-to-light="{e(ui['themeToLight'])}" data-to-dark="{e(ui['themeToDark'])}" aria-label="{e(ui['themeToLight'])}">{I_SUN}{I_MOON}</button>
</div></div></header>"""


def footer(L):
    return f"""<footer class="foot"><div class="wrap foot-in">
<p>© 2026 {e(S['fullName'])}</p>
<p>{e(L['footer'])}</p>
</div></footer>
</body>
</html>
"""


def page(key):
    L = LANGS[key]
    ui = L["ui"]
    ids = SECTION_IDS if key == "es" else SECTION_IDS_EN
    canonical = SITE + L["path"]
    home = "./"
    other_key = "en" if key == "es" else "es"
    other_href = ("en/" if key == "es" else "../")
    alternates = [("es", SITE), ("en", SITE + "en/"), ("x-default", SITE)]
    pre = "" if key == "es" else "../"
    h = L["hero"]; n = L["now"]; c = L["case"]; cr = L["career"]; pj = L["projects"]; ct = L["contact"]

    highlights = "".join(
        f'<li class="hl"><h3>{e(x["title"])}</h3><p>{e(x["body"])}</p></li>' for x in n["highlights"])
    stack = "".join(f"<li>{e(s)}</li>" for s in n["stack"])
    points = "".join(f"<li>{e(p)}</li>" for p in c["points"])

    jobs = []
    for j in cr["jobs"]:
        place = f' · {e(j["place"])}' if j.get("place") else ""
        body = f'<p class="job-body">{e(j["body"])}</p>' if j["body"] else ""
        jobs.append(f'<li class="job"><p class="job-dates">{e(j["dates"])}</p><div>'
                    f'<h3>{e(j["company"])}</h3><p class="job-role">{e(j["role"])}{place}</p>{body}</div></li>')

    projects = []
    for p in pj["items"]:
        tags = "".join(f"<li>{e(t)}</li>" for t in p["tags"])
        link = (f'<p class="proj-link">{ext(p["repo"], ui["code"], ui, inner=e(ui["code"]) + I_ARROW)}</p>'
                if p["repo"] else "")
        projects.append(f'<li class="proj"><h3>{e(p["name"])}</h3><p>{e(p["body"])}</p>'
                        f'<ul class="tags" role="list">{tags}</ul>{link}</li>')

    edu = "".join(f'<li><p class="edu-t">{e(x["title"])}</p><p class="muted">{e(x["school"])} · {e(x["dates"])}</p></li>'
                  for x in L["education"])
    langs = "".join(f'<li><p class="edu-t">{e(x["name"])}</p><p class="muted">{e(x["level"])}</p></li>'
                    for x in L["languageList"])

    ld = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "inLanguage": L["htmlLang"],
        "url": canonical,
        "mainEntity": {
            "@type": "Person",
            "name": S["fullName"],
            "alternateName": S["name"],
            "jobTitle": h["kicker"].split(" · ")[0],
            "worksFor": {"@type": "Organization", "name": "ifeel"},
            "address": {"@type": "PostalAddress", "addressLocality": "Torrox", "addressRegion": "Málaga", "addressCountry": "ES"},
            "knowsLanguage": ["es", "en", "de"],
            "knowsAbout": n["stack"],
            "sameAs": [S["links"]["linkedin"], S["links"]["github"]],
            "url": SITE,
        },
    }

    html = head(L, key, L["title"], L["description"], canonical, alternates) + f"""
<body>
{header(L, key, home, other_href)}
<main id="main">
<section class="hero" aria-labelledby="hero-title"><div class="wrap">
<p class="kicker">{e(h['kicker'])}</p>
<h1 id="hero-title">{e(S['name'])}</h1>
<p class="lead">{e(h['lead'])}</p>
<p class="hero-body">{e(h['body'])}</p>
<div class="hero-row">
<a class="btn" href="#{ids[0]}">{e(h['cta'])}{I_DOWN}</a>
{ext(S['links']['linkedin'], 'LinkedIn', ui, 'btn btn-ghost', I_IN + 'LinkedIn')}
<p class="where">{I_PIN}{e(h['where'])}</p>
</div>
</div></section>

<section id="{ids[0]}" class="sec" aria-labelledby="t-now"><div class="wrap">
<p class="label"><span>01</span>{e(n['label'])}</p>
<h2 id="t-now">{e(n['title'])}</h2>
<p class="meta">{e(n['meta'])}</p>
<p class="intro">{e(n['product'])}</p>
<ul class="hls" role="list">{highlights}</ul>
<h3 class="sub">{e(ui['stack'])}</h3>
<ul class="tags tags-lg" role="list">{stack}</ul>
</div></section>

<section id="{ids[1]}" class="sec sec-alt" aria-labelledby="t-case"><div class="wrap case">
<div class="case-text">
<p class="label"><span>02</span>{e(c['label'])}</p>
<h2 id="t-case">{e(c['title'])}</h2>
<p class="meta">{e(c['meta'])}</p>
<p class="intro">{e(c['body'])}</p>
<ul class="checks" role="list">{points}</ul>
<p>{ext(c['url'], c['urlLabel'], ui, 'btn', e(ui['visit']) + I_ARROW)}</p>
</div>
<figure class="shot"><img src="{pre}assets/img/nadia.webp" width="1200" height="750" alt="{e(c['shotAlt'])}" loading="lazy" decoding="async"><figcaption>{e(c['urlLabel'])}</figcaption></figure>
</div></section>

<section id="{ids[2]}" class="sec" aria-labelledby="t-career"><div class="wrap">
<p class="label"><span>03</span>{e(cr['label'])}</p>
<h2 id="t-career">{e(cr['title'])}</h2>
<ol class="jobs" role="list">{''.join(jobs)}</ol>
<div class="duo">
<div><h3 class="sub">{e(ui['education'])}</h3><ul class="plain" role="list">{edu}</ul></div>
<div><h3 class="sub">{e(ui['languages'])}</h3><ul class="plain" role="list">{langs}</ul></div>
</div>
</div></section>

<section id="{ids[3]}" class="sec sec-alt" aria-labelledby="t-proj"><div class="wrap">
<p class="label"><span>04</span>{e(pj['label'])}</p>
<h2 id="t-proj">{e(pj['title'])}</h2>
<ul class="projs" role="list">{''.join(projects)}</ul>
</div></section>

<section id="{ids[4]}" class="sec contact" aria-labelledby="t-contact"><div class="wrap">
<p class="label"><span>05</span>{e(ct['label'])}</p>
<h2 id="t-contact">{e(ct['title'])}</h2>
<p class="intro">{e(ct['body'])}</p>
<div class="hero-row">
{ext(S['links']['linkedin'], 'LinkedIn', ui, 'btn', I_IN + 'LinkedIn')}
{ext(S['links']['github'], 'GitHub', ui, 'btn btn-ghost', I_GH + 'GitHub')}
</div>
</div></section>
</main>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
""" + footer(L)
    out = os.path.join(ROOT, L["path"], "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)


def not_found():
    L = LANGS["es"]; ui = L["ui"]
    html = head(L, "es", ui["notFoundTitle"] + " · " + S["name"], L["description"], SITE + "404.html",
                [], noindex=True) + f"""
<body>
{header(L, 'es', '/', '/en/')}
<main id="main"><section class="hero"><div class="wrap">
<p class="kicker">404</p>
<h1>{e(ui['notFoundTitle'])}</h1>
<p class="lead">{e(ui['notFoundBody'])}</p>
<p><a class="btn" href="/">{e(ui['notFoundBack'])}</a></p>
</div></section></main>
""" + footer(L)
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(html)


def sitemap():
    urls = []
    for key, L in LANGS.items():
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{k}" href="{SITE}{x["path"]}"/>' for k, x in LANGS.items())
        urls.append(f"<url><loc>{SITE}{L['path']}</loc>{alts}</url>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + "".join(urls) + "</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")


for k in LANGS:
    page(k)
not_found()
sitemap()
print("built:", ", ".join("/" + L["path"] for L in LANGS.values()), "+ 404, sitemap, robots")
